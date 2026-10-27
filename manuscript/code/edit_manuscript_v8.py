"""Manuscript v8: direct edit of manuscript_v7.docx (WRITING_RULES 1.2 rule 2).

Opens manuscript/archive/v7/manuscript_v7.docx (sha256 checked against MANIFEST_v7), turns its
superscript reference numbers back into markers and removes the reference list. Instruction "v8"
section 1: six sentence-level replacements in Results, Discussion, Implications and Limitations;
section 2: the title as a plain paragraph at the top, followed by empty lines for the front matter
(filled by A. Ozaki); section 3: the Abstract (bold labels on their own lines) before the
Introduction. The new text is the user's text word for word (USER below, compared mechanically),
with the two changes the user chose on 2026-10-27 (DECISIONS). Every number of a new sentence is
registered with its source and checked there; the numbers of the kept paragraphs are carried over
from the v7 ledger and checked again. number_refs.py then numbers the markers.

Writes _build/manuscript_marked.docx, _build/_ledger_results.json (and a _v8 copy),
_build/_ledger_manuscript.json and _build/_manuscript_map.json. Runs for v8 only; later versions
edit manuscript_v8.docx directly.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys

import pandas as pd
from docx import Document
from docx.oxml.ns import qn
from lxml import etree

from common import ARCHIVE_PREV, BUILD, PREV, ROOT, SUPP, VER, Params, fnum, num_tokens, sha256
from references import MARK_RE, PUBMED, REFS, entry, expand

sys.stdout.reconfigure(encoding="utf-8")
if VER != "v8":
    raise SystemExit("edit_manuscript_v8.py holds the edits of v8 only; write the next version's edits on manuscript_v8.docx")

SNAP = BUILD / "v7_snapshot"  # _build records of v7, copied before this build
REGS = {name: json.load(open(BUILD / f"_ledger_{name}.json", encoding="utf-8")) for name in ("tables", "supplement", "figures", "suppfigs")}
led_m7 = json.load(open(SNAP / "_ledger_manuscript.json", encoding="utf-8"))
led_r7 = json.load(open(SNAP / f"_ledger_results_{PREV}.json", encoding="utf-8"))
map7 = json.load(open(SNAP / "_manuscript_map.json", encoding="utf-8"))
S = SUPP
JB = "input/params/cohort_N_jbcs2024.csv"

# ================================================================ the base: manuscript_v7.docx and its manifest
SRC = ARCHIVE_PREV / f"manuscript_{PREV}.docx"
man = (ARCHIVE_PREV / f"MANIFEST_{PREV}.md").read_text(encoding="utf-8")
assert f"| manuscript/{PREV}/manuscript_{PREV}.docx | {sha256(SRC)} |" in man, "manuscript_v7.docx differs from MANIFEST_v7.md"
doc = Document(SRC)
allp = [p for p in doc.paragraphs if p.text.strip()]
assert len(doc.paragraphs) == len(allp), "v7 has empty paragraphs"
i_ref = next(i for i, p in enumerate(allp) if p.text == "References")
assert i_ref == len(map7["order"]), (i_ref, len(map7["order"]))

num2key = {}
for p in allp[i_ref + 1:]:
    m = re.fullmatch(r"(\d+)\. (.*)", p.text, re.S)
    ks = [k for k in REFS if entry(k) == m.group(2)]
    assert len(ks) == 1, (m.group(1), ks)
    num2key[int(m.group(1))] = ks[0]
assert sorted(num2key) == list(range(1, len(num2key) + 1)) and len(set(num2key.values())) == len(num2key) == len(REFS)
CIT = re.compile(r"[\d,–]+")


def _rpr(r, drop_va=False):
    rpr = copy.deepcopy(r._r.find(qn("w:rPr")))
    if drop_va and rpr is not None and rpr.find(qn("w:vertAlign")) is not None:
        rpr.remove(rpr.find(qn("w:vertAlign")))
    return etree.tostring(rpr) if rpr is not None else b""


def demark(p):
    """Paragraph text with each superscript reference run turned back into its marker; all runs must share one format."""
    runs = [r for r in p.runs if r.text]
    fmt = _rpr(runs[0])
    out = []
    for r in runs:
        assert len(r._r.findall(qn("w:t"))) == 1 and len(r._r) == 2, ("run with other content", r.text)
        if r.font.superscript and CIT.fullmatch(r.text):
            assert _rpr(r, drop_va=True) == fmt, ("reference run with another format", r.text)
            out.append("⟦ref:" + ",".join(num2key[n] for n in expand(r.text)) + "⟧")
        else:
            assert _rpr(r) == fmt, ("text run with another format", r.text[:40])
            out.append(r.text)
    return "".join(out)


def keyset_norm(t):
    return MARK_RE.sub(lambda m: "⟦ref:" + ",".join(sorted(m.group(1).split(","))) + "⟧", t)


TEXT7, ELEM7 = {}, {}
for o, p in zip(map7["order"], allp[:i_ref]):
    t = demark(p)
    if o["kind"] == "heading":
        assert t == o["text"] and all(r.bold for r in p.runs if r.text.strip()), (o, t)
        continue
    TEXT7[o["id"]], ELEM7[o["id"]] = t, p
    assert keyset_norm(t) == keyset_norm(o["text"]), ("v7 docx and paragraph map differ", o["id"])
SENT7 = {x["id"]: list(x["sentences"]) for x in led_m7["paragraphs"]}
for pid, ss in SENT7.items():
    assert keyset_norm(" ".join(ss)) == keyset_norm(TEXT7[pid]), ("v7 ledger and docx differ", pid)
RES7 = led_r7["paragraphs"]
for i, ps in enumerate(RES7, start=1):
    assert TEXT7[f"R.{i}"] == " ".join(s["text"] for s in ps), ("v7 Results ledger and docx differ", i)

# ================================================================ number registration (as in edit_manuscript_v7.py)
MROWS: list[dict] = []
CUR = [None]


def _line(path, needle):
    for i, ln in enumerate((ROOT / path).read_text(encoding="utf-8").splitlines(), start=1):
        if needle in ln:
            return i, ln
    raise ValueError(f"{needle!r} not found in {path}")


def _csv(path, item):
    return pd.read_csv(ROOT / path).set_index("item").loc[item, "value"]


def _reg_rows(reg, prefix, tok):
    return [x for x in REGS[reg]["rows"] + REGS[reg]["labels"] if x["where"].startswith(prefix) and x["shown"] == tok]


def N(tok: str, kind: str, *a) -> str:
    """Register a number of the current paragraph with its source and check it there."""
    if kind == "lit":
        (key,) = a
        assert tok in PUBMED[key]["abstract"], (tok, key)
        src, loc = f"PubMed {PUBMED[key]['pmid']} ({key})", "abstract"
    elif kind == "doc":
        path, needle = a
        i, ln = _line(path, needle)
        assert tok in ln, (tok, path, ln)
        src, loc = path, f"line {i}: {needle}"
    elif kind == "reg":
        reg, prefix = a
        rows = _reg_rows(reg, prefix, tok)
        assert rows, (tok, reg, prefix)
        src, loc = f"_ledger_{reg}.json", f"{rows[0]['where']} ({rows[0].get('source', rows[0].get('reason', ''))})"
    elif kind == "label":
        (why,) = a
        src, loc = "definition", why
    else:
        raise ValueError(kind)
    MROWS.append(dict(shown=tok, where=CUR[0], source=src, loc=loc))
    return tok


def recheck(r):
    """A number carried over from the v7 ledger, checked again at its source."""
    tok, src, loc = r["shown"], r["source"], r["loc"]
    if src.startswith("PubMed "):
        key = re.search(r"\((\w+)\)$", src).group(1)
        assert tok in PUBMED[key]["abstract"], r
    elif src.startswith("_ledger_"):
        reg = src[len("_ledger_"):-len(".json")]
        assert any(x["shown"] == tok and loc.startswith(x["where"] + " (") for x in REGS[reg]["rows"] + REGS[reg]["labels"]), r
    elif src == "definition":
        pass
    elif loc.startswith("item = "):
        item = loc.split(" = ")[1].split(",")[0]
        v = float(_csv(src, item))
        assert fnum(v, 0) == tok or (loc.endswith("x 100") and fnum(100 * v, 0) == tok), r
    else:
        needle = loc.split(": ", 1)[1]
        i, ln = _line(src, needle)
        assert tok in ln, r
        r = dict(r, loc=f"line {i}: {needle}")
    return r


def cite(*keys):
    for k in keys:
        assert k in REFS, k
    return "⟦ref:" + ",".join(keys) + "⟧"


LOG = []  # (paragraph, kind, instruction, before, after)

# ================================================================ the user's text (instruction sections 1 to 3), word for word
USER = {
    "TITLE": "The maximum affordable cost of structured exercise during neoadjuvant chemotherapy for triple-negative breast cancer in Japan: a cost-effectiveness analysis",
    "A.1": "To estimate the maximum cost at which a structured exercise program added to neoadjuvant chemotherapy for stage II or III triple-negative breast cancer would be cost-effective in Japan.",
    "A.2": "A state-transition model used KEYNOTE-522 data, including the final analysis, to simulate chemotherapy with or without pembrolizumab, each with or without exercise. The analysis took the Japanese public healthcare payer perspective over a lifetime, with discounting at 2% per year. The effect of exercise was expressed as a hazard ratio (HR) for recurrence after surgery, from 0.70 to 1.00, with alternative durations. The maximum affordable cost was the threshold of JPY 5 million per quality-adjusted life year (QALY) times the incremental QALYs, minus incremental medical costs.",
    "A.3": "Added to chemotherapy plus pembrolizumab, exercise had a maximum affordable cost of JPY 2,726 thousand per patient at an HR of 0.85 (95% uncertainty interval [2,223, 3,040]). A program priced from the medical fee schedule (JPY 192,400) became cost-effective at an HR of 0.989. Medical costs avoided alone paid for it at HRs of 0.958 to 0.914, depending on metastatic treatment costs. The duration of the effect changed the maximum affordable cost more than any cost input. Pembrolizumab had an incremental cost-effectiveness ratio of JPY 2,053 thousand per QALY, and exercise would need an HR of 0.425 to match its QALY gain.",
    "A.4": "In Japan, the value of exercise during neoadjuvant chemotherapy depends on the size and duration of its effect on recurrence far more than on its price. Even a small effect on recurrence would pay for a program. Trials should measure recurrence and whether the effect lasts.",
    "R.2 s2-s3": "An increase of 1 percentage point in pCR gave JPY 389 thousand (95% UI [238, 570]). An increase of 10 percentage points gave JPY 3,898 thousand (95% UI [2,388, 5,713]).",
    "D.3 s2-s3": "Because most recurrences after this regimen occur early [licata2025], an effect that holds through the first years after surgery captures most of the value.",
    "D.4 s5-s6": "Because most patients in Japan received pembrolizumab with neoadjuvant chemotherapy in 2024 [jbcs55], the main comparison is the one that matters most for practice.",
    "D.6": "Our results agree with the cost-utility analysis of CHALLENGE, which also valued an effect of exercise on recurrence [chan2026]. Over 5 years, the program cost less and gave more health than health education, and recurrence, new cancers and their treatment drove the costs [chan2026]. Evaluations that valued only short-term effects on fatigue, fitness or quality of life [khan2019, gublergut2021, wang2023] could not capture this source of value. Each recurrence prevented avoids months of costly treatment and years of lost health, which together outweigh the cost of an exercise program.",
    "IMP.1 s1-s2": "Clinicians can offer exercise during neoadjuvant chemotherapy for its known benefits on fitness [furmaniak2016, courneya2007, vanwaart2015, mijwel2018] while its effect on recurrence is tested. This analysis adds that an effect on recurrence, if present, would carry large economic value.",
    "L.2 phrase": ("Longer survival with current treatment", "Longer survival with the treatments used in 2026"),
}
# the user's answers of 2026-10-27 to the two questions asked before the edit
DECISIONS = {
    "IMP.1 s1-s2": ("[furmaniak2016, courneya2007, vanwaart2015, mijwel2018]", "[furmaniak2016, courneya2007, vanwaart2015]",
                    "mijwel2018 reports fatigue, health-related quality of life and symptoms but no fitness outcome (PMC5847033 full text); "
                    "removed from this sentence, still cited in Introduction paragraph 2"),
    "A.2": ("minus incremental medical costs.", "minus incremental medical costs other than the program cost.",
            "definition as in Methods, Outcome"),
}


def from_user(key):
    t = USER[key]
    if key in DECISIONS:
        a, b, _ = DECISIONS[key]
        assert t.count(a) == 1, key
        t = t.replace(a, b)
    return re.sub(r" \[([a-z][a-z0-9_]*(?:, [a-z][a-z0-9_]*)*)\]", lambda m: "⟦ref:" + m.group(1).replace(", ", ",") + "⟧", t)


def verbatim(key, sents):
    built, want = " ".join(sents), from_user(key)
    if built != want:
        i = next((k for k in range(min(len(built), len(want))) if built[k] != want[k]), min(len(built), len(want)))
        raise AssertionError(("text differs from the instruction", key, built[max(0, i - 25):i + 25], want[max(0, i - 25):i + 25]))


for key, (a, b, why) in DECISIONS.items():
    LOG.append((key.split()[0], "decision", f"user's answer (2026-10-27): {why}", a, b))

# ================================================================ Introduction and Methods: kept word for word
heads_before, pending = {}, []
for o in map7["order"]:
    if o["kind"] == "heading":
        pending.append(o["text"])
    else:
        heads_before[o["id"]] = pending
        pending = []
PARAS = {x["id"]: list(x["sentences"]) for x in led_m7["paragraphs"]}  # non-Results paragraphs of v7, edited below
ROWS = {x["id"]: [recheck(r) for r in x["numbers"]] for x in led_m7["paragraphs"]}


def replace(pid, old_idx, new_sents, key, why):
    """Replace sentences old_idx (1-based) of paragraph pid by new_sents; new_sents must be the user's text."""
    verbatim(key, new_sents)
    before = list(PARAS[pid])
    i0 = old_idx[0] - 1
    PARAS[pid] = before[:i0] + new_sents + before[old_idx[-1]:]
    LOG.append((pid, "edit", why, " ".join(before[i0:old_idx[-1]]), " ".join(new_sents)))


# ================================================================ Results (section 1)
def V(reg, where, idx=0):
    rows = [x for x in REGS[reg]["rows"] if x["where"] == where]
    if len(rows) <= idx:
        raise KeyError(f"{reg}: no entry {idx} for {where!r}")
    return rows[idx]


for u in led_r7["used"]:
    rows = REGS[u["registry"]]["rows"] + (REGS[u["registry"]]["labels"] if u.get("source") == "label" else [])
    assert u["shown"] in {x["shown"] for x in rows if x["where"] == u["where"]}, ("value no longer in the registry", u)
SPB = f"Supplementary Table {S['pathB']}"
RES = copy.deepcopy(RES7)
p2 = RES[1]
assert len(p2) == 2 and p2[1]["text"].startswith("An increase of 1 percentage point in pCR gave")
w1, w10 = f"{SPB}, A, pcr 0.010, main base", f"{SPB}, A, pcr 0.100, main base"
a1, a10 = [V("supplement", w1, i)["shown"] for i in range(3)], [V("supplement", w10, i)["shown"] for i in range(3)]
r_lab = {x["shown"]: x for x in REGS["supplement"]["rows"] if x["where"] == f"{SPB}, row label"}
new2 = [dict(text=f"An increase of {r_lab['1']['shown']} percentage point in pCR gave JPY {a1[0]} thousand (95% UI [{a1[1]}, {a1[2]}]).",
             cites=[SPB], keys=["1", "a1", "b1", "c1"], origin="v7 R.2 s2, split in v8"),
        dict(text=f"An increase of {r_lab['10']['shown']} percentage points gave JPY {a10[0]} thousand (95% UI [{a10[1]}, {a10[2]}]).",
             cites=[SPB], keys=["10", "a10", "b10", "c10"], origin="v7 R.2 s2, split in v8")]
verbatim("R.2 s2-s3", [s["text"] for s in new2])
LOG.append(("R.2", "edit", "section 1: the second sentence of the pathway-B paragraph split into two", p2[1]["text"], " ".join(s["text"] for s in new2)))
RES[1] = [p2[0]] + new2
USED = []
for u in led_r7["used"]:
    if u["paragraph"] == 2 and u["sentence"] == 2:
        USED.append(dict(u, sentence=2 if u["placeholder"] in ("1", "a1", "b1", "c1") else 3))
    else:
        USED.append(dict(u))
assert sorted(u["placeholder"] for u in USED if u["paragraph"] == 2 and u["sentence"] == 3) == sorted(["10", "a10", "b10", "c10"])

# ================================================================ Discussion, Implications, Limitations (section 1)
CUR[0] = "D.3"
replace("D.3", [2, 3], [f"Because most recurrences after this regimen occur early{cite('licata2025')}, an effect that holds through the first years after "
                        "surgery captures most of the value."], "D.3 s2-s3", "section 1: Discussion paragraph 3, sentences 2 and 3 replaced by one sentence")
ROWS["D.3"] = []  # the 24 months of v7 sentence 2 are gone
CUR[0] = "D.4"
replace("D.4", [5, 6], [f"Because most patients in Japan received pembrolizumab with neoadjuvant chemotherapy in {N('2024', 'doc', JB, '（2024 年）')}"
                        f"{cite('jbcs55')}, the main comparison is the one that matters most for practice."],
        "D.4 s5-s6", "section 1: Discussion paragraph 4, the last two sentences replaced by one sentence")
ROWS["D.4"] = []  # 2024, 2,294 and 3,451 of v7; 2024 registered again above
CUR[0] = "D.6"
replace("D.6", list(range(1, len(PARAS["D.6"]) + 1)), [
    f"Our results agree with the cost-utility analysis of CHALLENGE, which also valued an effect of exercise on recurrence{cite('chan2026')}.",
    f"Over {N('5', 'lit', 'chan2026')} years, the program cost less and gave more health than health education, and recurrence, new cancers and their "
    f"treatment drove the costs{cite('chan2026')}.",
    f"Evaluations that valued only short-term effects on fatigue, fitness or quality of life{cite('khan2019', 'gublergut2021', 'wang2023')} could not "
    "capture this source of value.",
    "Each recurrence prevented avoids months of costly treatment and years of lost health, which together outweigh the cost of an exercise program.",
], "D.6", "section 1: Discussion paragraph 6 replaced as a whole")
ROWS["D.6"] = []  # the 5 of v7; registered again above
CUR[0] = "IMP.1"
assert PARAS["IMP.1"][1] == "This analysis adds that an effect on recurrence, if present, would carry large economic value."
replace("IMP.1", [1, 2], [
    f"Clinicians can offer exercise during neoadjuvant chemotherapy for its known benefits on fitness{cite('furmaniak2016', 'courneya2007', 'vanwaart2015')} "
    "while its effect on recurrence is tested.",
    "This analysis adds that an effect on recurrence, if present, would carry large economic value.",
], "IMP.1 s1-s2", "section 1: Implications sentences 1 and 2 replaced (mijwel2018 removed, user's answer)")
CUR[0] = "L.2"
a, b = USER["L.2 phrase"]
s = PARAS["L.2"][1]
assert s.count(a) == 1
PARAS["L.2"][1] = s.replace(a, f"Longer survival with the treatments used in {N('2026', 'reg', 'tables', 'Table 1, prices')}")
assert PARAS["L.2"][1] == s.replace(a, b)
LOG.append(("L.2", "edit", "section 1: 'Longer survival with current treatment' -> 'Longer survival with the treatments used in 2026'", s, PARAS["L.2"][1]))

# ================================================================ title and Abstract (sections 2 and 3)
CUR[0] = "T.1"
TITLE = USER["TITLE"]
verbatim("TITLE", [TITLE])
T2, T3 = "Table 2", "Table 3"
ABS = []  # (id, label, sentences)
CUR[0] = "A.1"
ABS.append(("A.1", "Objectives", [
    "To estimate the maximum cost at which a structured exercise program added to neoadjuvant chemotherapy for stage II or III triple-negative breast "
    "cancer would be cost-effective in Japan."]))
CUR[0] = "A.2"
ABS.append(("A.2", "Methods", [
    "A state-transition model used KEYNOTE-522 data, including the final analysis, to simulate chemotherapy with or without pembrolizumab, each with or "
    "without exercise.",
    f"The analysis took the Japanese public healthcare payer perspective over a lifetime, with discounting at {N('2', 'doc', 'docs/model_spec.md', '按年 2% 折现')}% per year.",
    f"The effect of exercise was expressed as a hazard ratio (HR) for recurrence after surgery, from {N('0.70', 'reg', 'tables', 'Table 1, effect on recurrence')} "
    f"to {N('1.00', 'reg', 'tables', 'Table 1, effect on recurrence')}, with alternative durations.",
    f"The maximum affordable cost was the threshold of JPY {N('5', 'reg', 'tables', 'Table 2, title')} million per quality-adjusted life year (QALY) times "
    "the incremental QALYs, minus incremental medical costs other than the program cost."]))
CUR[0] = "A.3"
ABS.append(("A.3", "Results", [
    f"Added to chemotherapy plus pembrolizumab, exercise had a maximum affordable cost of JPY {N('2,726', 'reg', 'tables', 'Table 2, Panel B, base case, main')} "
    f"thousand per patient at an HR of {N('0.85', 'reg', 'tables', 'Table 2, Panels B and C row label')} "
    f"({N('95', 'label', '95% uncertainty interval (Methods, Statistical analysis stage 3)')}% uncertainty interval "
    f"[{N('2,223', 'reg', 'tables', 'Table 2, Panel B, base case, main')}, {N('3,040', 'reg', 'tables', 'Table 2, Panel B, base case, main')}]).",
    f"A program priced from the medical fee schedule (JPY {N('192,400', 'reg', 'tables', 'Table 1, exercise program')}) became cost-effective at an HR of "
    f"{N('0.989', 'reg', 'tables', 'Table 2, Panel A, cap = E02, main')}.",
    f"Medical costs avoided alone paid for it at HRs of {N('0.958', 'reg', 'tables', 'Table 2, Panel A, avoided = E02, main')} to "
    f"{N('0.914', 'reg', 'tables', 'Table 2, Panel C, eri, avoided = E02, main')}, depending on metastatic treatment costs.",
    "The duration of the effect changed the maximum affordable cost more than any cost input.",
    f"Pembrolizumab had an incremental cost-effectiveness ratio of JPY {N('2,053', 'reg', 'tables', 'Table 3, base, ICER')} thousand per QALY, and exercise "
    f"would need an HR of {N('0.425', 'reg', 'tables', 'Table 3, Panel C, HR')} to match its QALY gain."]))
CUR[0] = "A.4"
ABS.append(("A.4", "Conclusions", [
    "In Japan, the value of exercise during neoadjuvant chemotherapy depends on the size and duration of its effect on recurrence far more than on its price.",
    "Even a small effect on recurrence would pay for a program.",
    "Trials should measure recurrence and whether the effect lasts."]))
for pid, lab, sents in ABS:
    verbatim(pid, sents)
LOG.append(("T.1", "new", "section 2: title, a plain paragraph at the top of the manuscript, followed by empty lines for the front matter", "", TITLE))
for pid, lab, sents in ABS:
    LOG.append((pid, "new", f"section 3: Abstract, {lab}" + ("; definition completed (user's answer)" if pid == "A.2" else ""), "", " ".join(sents)))

# ---------------------------------------------------------------- statements resting on table values (kept from v7, and the Abstract)
P = Params()
progs = {pid: float(P.get(pid)[0]) for pid in ("E01", "E02", "E03")}
monthly = {pid: float(P.get(pid)[0]) for pid in ("D03", "D03P", "D05")}
monthly.update({f"{pid} ({sc})": float(P.scenario(sc, pid)[0]) for sc, pids in (("sc_eribulin", ("D05",)), ("sc_metcost50", ("D03", "D03P", "D05"))) for pid in pids})
assert min(monthly.values()) > max(progs.values()), (monthly, progs)
hr_c = float(next(x for x in REGS["tables"]["rows"] if x["where"] == "Table 3, Panel C, HR")["raw"])
assert 1 - hr_c > 0.5, hr_c
S9 = f"Supplementary Table {S['oneway']}"
caps9 = [float(x["raw"]) for x in REGS["supplement"]["rows"] if x["where"].startswith(S9 + ", ") and re.search(r", cap_(low|high)$", x["where"])]
icers9 = [float(x["raw"]) for x in REGS["supplement"]["rows"] if x["where"].startswith(S9 + ", ") and re.search(r", icer_(low|high)$", x["where"])]
assert len(caps9) == 42 and min(caps9) > 10 * max(progs.values()) and max(icers9) < 5e6, (min(caps9), max(icers9))
dur = {k: float(next(x for x in REGS["tables"]["rows"] if x["where"] == f"Table 2, Panel B, {k}, main")["raw"]) for k in ("dur1", "dur2")}
assert dur["dur1"] < min(caps9) and dur["dur2"] > max(caps9), (dur, min(caps9), max(caps9))
TEXT_CHECKS = {
    "D.2 s2 one month after distant recurrence > whole program": dict(monthly_yen={k: round(v, 2) for k, v in monthly.items()}, programs_yen=progs),
    "D.4 s2 more than half": dict(hr_table3_panel_c=hr_c, reduction=round(1 - hr_c, 4)),
    "L.2 s3 no single cost changed the conclusion": dict(caps_s9_n=len(caps9), caps_min_yen=round(min(caps9), 2), program_max_yen=max(progs.values()),
                                                         icers_s9_n=len(icers9), icer_max_yen_per_qaly=round(max(icers9), 2), threshold=5e6),
    "A.3 s4 duration changed the cap more than any cost input": dict(duration_range_yen=[round(dur["dur1"], 2), round(dur["dur2"], 2)],
                                                                    one_way_range_yen=[round(min(caps9), 2), round(max(caps9), 2)]),
}

# ================================================================ docx
def set_text(p, text):
    runs = p._p.findall(qn("w:r"))
    for r in runs[1:]:
        p._p.remove(r)
    t = runs[0].find(qn("w:t"))
    t.text = text
    t.set(qn("xml:space"), "preserve")
    assert runs[0].find(qn("w:rPr")).find(qn("w:vertAlign")) is None


def clone(tmpl, text):
    el = copy.deepcopy(tmpl)
    runs = el.findall(qn("w:r"))
    for r in runs[1:]:
        el.remove(r)
    if text is None:  # empty line
        el.remove(runs[0])
        return el
    t = runs[0].find(qn("w:t"))
    t.text = text
    t.set(qn("xml:space"), "preserve")
    return el


for pid, sents in PARAS.items():
    set_text(ELEM7[pid], " ".join(sents))
for i, ps in enumerate(RES, start=1):
    set_text(ELEM7[f"R.{i}"], " ".join(s["text"] for s in ps))
for p in allp[i_ref:]:  # the reference list of v7 (number_refs.py writes the list of v8)
    p._p.getparent().remove(p._p)
HEAD = copy.deepcopy(allp[0]._p)  # "Introduction": bold Normal paragraph
assert allp[0].text == "Introduction"
BODY = copy.deepcopy(ELEM7["I.1"]._p)
assert not any(r.bold for r in ELEM7["I.1"].runs)
N_BLANK = 3  # authors, affiliations, corresponding author (front matter by A. Ozaki; WRITING_RULES 14)
anchor = allp[0]._p
new_front = [clone(BODY, TITLE)] + [clone(BODY, None) for _ in range(N_BLANK)]
for pid, lab, sents in ABS:
    new_front += [clone(HEAD, lab), clone(BODY, " ".join(sents))]
for el in new_front:
    anchor.addprevious(el)
out = BUILD / "manuscript_marked.docx"
doc.save(out)

# ================================================================ ledgers and paragraph map
order = [dict(id="T.1", kind="title", text=TITLE)]
for pid, lab, sents in ABS:
    order += [dict(id=None, kind="abstract label", text=lab), dict(id=pid, kind="body", text=" ".join(sents))]
for o in map7["order"]:
    if o["kind"] == "heading":
        order.append(dict(id=None, kind="heading", text=o["text"]))
    elif o["id"].startswith("R."):
        order.append(dict(id=o["id"], kind="body", text=" ".join(s["text"] for s in RES[int(o["id"][2:]) - 1])))
    else:
        order.append(dict(id=o["id"], kind="body", text=" ".join(PARAS[o["id"]])))
d8 = Document(out)
chk = [p for p in d8.paragraphs if p.text.strip()]
assert [p.text for p in chk] == [o["text"] for o in order], "manuscript_marked.docx does not read back as the paragraph map"
assert [p.text for p in d8.paragraphs[:1 + N_BLANK]] == [TITLE] + [""] * N_BLANK
assert not any(r.bold for r in d8.paragraphs[0].runs) and all(r.bold for o, p in zip(order, chk) if o["kind"] == "abstract label" for r in p.runs)

rows_all = [r for pid in PARAS for r in ROWS[pid]] + MROWS
secs = [dict(id="T.1", sentences=[TITLE], numbers=[])] + [dict(id=pid, sentences=sents, numbers=[r for r in rows_all if r["where"] == pid]) for pid, _, sents in ABS] + \
       [dict(id=pid, sentences=sents, numbers=[r for r in rows_all if r["where"] == pid]) for pid, sents in PARAS.items()]

# every number of the Abstract must be in the main text (Introduction to Limitations) or in a table
strip = lambda t: MARK_RE.sub("", re.sub(r"\b(?:Supplementary )?(?:Tables?|Figs?\.|Methods) S?\d+[a-z]?(?:\s*(?:and|to|,)\s*S?\d+)*", " ", t))
main_tok = {t for pid, ss in PARAS.items() for s in ss for t in num_tokens(strip(s))} | {t for ps in RES for s in ps for t in num_tokens(strip(s["text"]))}
ABS_CHECK = []
for pid, _, sents in ABS:
    for s in sents:
        for t in num_tokens(strip(s)):
            in_tab = any(x["shown"] == t for x in REGS["tables"]["rows"] + REGS["tables"]["labels"])
            ABS_CHECK.append(dict(paragraph=pid, shown=t, in_main_text=t in main_tok, in_tables=in_tab))
            assert t in main_tok or in_tab, (pid, t)
json.dump({"paragraphs": secs, "rows": rows_all, "text_checks": TEXT_CHECKS, "abstract_numbers": ABS_CHECK, "decisions": {k: v[2] for k, v in DECISIONS.items()}},
          open(BUILD / "_ledger_manuscript.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
led = {"paragraphs": RES, "used": USED, "base": f"manuscript_{PREV}.docx", "edits": [dict(zip(("paragraph", "kind", "reason", "before", "after"), x)) for x in LOG]}
for name in ("_ledger_results.json", f"_ledger_results_{VER}.json"):
    json.dump(led, open(BUILD / name, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"version": VER, "ids": [o["id"] for o in order if o["id"]], "order": order, "manuscript_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
           "front_matter_empty_lines": N_BLANK, "edits": [dict(zip(("paragraph", "kind", "reason", "before", "after"), x)) for x in LOG]},
          open(BUILD / "_manuscript_map.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

bad = [(x["id"], t, s[:60]) for x in secs for s in x["sentences"] for t in num_tokens(strip(s)) if t not in {r["shown"] for r in x["numbers"]}]
assert not bad, bad


def words(t):
    return len(MARK_RE.sub("", t).split())


print("manuscript_marked.docx written from", SRC.name)
aw = sum(words(s) for _, _, ss in ABS for s in ss)
print(f"  title: {words(TITLE)} words | Abstract: {aw} words without labels, {aw + len(ABS)} with labels")
for x in secs:
    if x["id"].startswith(("A.", "D.3", "D.4", "D.6", "IMP.1", "L.2")):
        w = [words(s) for s in x["sentences"]]
        print(f"  {x['id']}: {sum(w)} words, longest sentence {max(w)}, numbers {len(x['numbers'])}")
w = [len(s["text"].split()) for s in RES[1]]
print(f"  R.2: {sum(w)} words, longest sentence {max(w)}")
print("abstract numbers not in the main-text prose:", [(a["paragraph"], a["shown"]) for a in ABS_CHECK if not a["in_main_text"]])
print("edits:", len(LOG))
