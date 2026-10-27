"""Manuscript v9: direct edit of manuscript_v8.docx (WRITING_RULES 1.2 rule 2).

Opens manuscript/archive/v8/manuscript_v8.docx (sha256 checked against MANIFEST_v8), turns its
superscript reference numbers back into markers and removes the reference list. Instruction "v9":
section 1, Implications sentence 1 replaced by two sentences, one phrase of Discussion paragraph 3
and the last sentence of Discussion paragraph 5 deleted; section 2, the title; section 3, the four
Abstract paragraphs (labels and the empty lines after the title unchanged). The new text is the
user's text word for word (USER below, compared mechanically). Every number of a new sentence is
registered with its source and checked there; the numbers of the kept paragraphs are carried over
from the v8 ledger and checked again. number_refs.py then numbers the markers.

Writes _build/manuscript_marked.docx, _build/_ledger_results.json (and a _v9 copy),
_build/_ledger_manuscript.json and _build/_manuscript_map.json. Runs for v9 only; later versions
edit manuscript_v9.docx directly.
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
if VER != "v9":
    raise SystemExit("edit_manuscript_v9.py holds the edits of v9 only; write the next version's edits on manuscript_v9.docx")

SNAP = BUILD / "v8_snapshot"  # _build records of v8, copied before this build
REGS = {name: json.load(open(BUILD / f"_ledger_{name}.json", encoding="utf-8")) for name in ("tables", "supplement", "figures", "suppfigs")}
led_m8 = json.load(open(SNAP / "_ledger_manuscript.json", encoding="utf-8"))
led_r8 = json.load(open(SNAP / f"_ledger_results_{PREV}.json", encoding="utf-8"))
map8 = json.load(open(SNAP / "_manuscript_map.json", encoding="utf-8"))
S = SUPP

# ================================================================ the base: manuscript_v8.docx and its manifest
SRC = ARCHIVE_PREV / f"manuscript_{PREV}.docx"
man = (ARCHIVE_PREV / f"MANIFEST_{PREV}.md").read_text(encoding="utf-8")
assert f"| manuscript/{PREV}/manuscript_{PREV}.docx | {sha256(SRC)} |" in man, "manuscript_v8.docx differs from MANIFEST_v8.md"
doc = Document(SRC)
N_BLANK = map8["front_matter_empty_lines"]
assert [p.text for p in doc.paragraphs[1:1 + N_BLANK]] == [""] * N_BLANK and sum(1 for p in doc.paragraphs if not p.text.strip()) == N_BLANK
allp = [p for p in doc.paragraphs if p.text.strip()]
i_ref = next(i for i, p in enumerate(allp) if p.text == "References")
assert i_ref == len(map8["order"]), (i_ref, len(map8["order"]))

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


TEXT8, ELEM8 = {}, {}
for o, p in zip(map8["order"], allp[:i_ref]):
    t = demark(p)
    if o["kind"] in ("heading", "abstract label"):
        assert t == o["text"] and all(r.bold for r in p.runs if r.text.strip()), (o, t)
        continue
    TEXT8[o["id"]], ELEM8[o["id"]] = t, p
    assert keyset_norm(t) == keyset_norm(o["text"]), ("v8 docx and paragraph map differ", o["id"])
SENT8 = {x["id"]: list(x["sentences"]) for x in led_m8["paragraphs"]}
for pid, ss in SENT8.items():
    assert keyset_norm(" ".join(ss)) == keyset_norm(TEXT8[pid]), ("v8 ledger and docx differ", pid)
RES8 = led_r8["paragraphs"]
for i, ps in enumerate(RES8, start=1):
    assert TEXT8[f"R.{i}"] == " ".join(s["text"] for s in ps), ("v8 Results ledger and docx differ", i)

# ================================================================ number registration (as in edit_manuscript_v8.py)
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
    if kind == "doc":
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
    """A number carried over from the v8 ledger, checked again at its source."""
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
    "IMP.1 s1": "Exercise during adjuvant chemotherapy improves fitness [furmaniak2016, courneya2007, vanwaart2015], and trials have delivered supervised exercise during neoadjuvant chemotherapy [kjeldsted2025, schmidt2025]. Clinicians can therefore offer it while its effect on recurrence is tested.",
    "D.3 phrase": ("Because most recurrences after this regimen occur early", "Because most recurrences after neoadjuvant chemotherapy with pembrolizumab occur early"),
    "D.5 deleted": "The regimen has not been designated for Japan's cost-effectiveness evaluation [c2h_list], and our estimate gives a reference in the meantime.",
    "TITLE": "Cost-effectiveness of exercise added to neoadjuvant chemotherapy for triple-negative breast cancer in Japan",
    "A.1": "To estimate the maximum cost at which a structured exercise program added to neoadjuvant chemotherapy for stage II or III triple-negative breast cancer would be cost-effective in Japan.",
    "A.2": "A state-transition model based on KEYNOTE-522 simulated chemotherapy with or without pembrolizumab, each with or without exercise. The analysis took the Japanese public healthcare payer perspective over a lifetime, with discounting at 2% per year. The exercise effect was a hazard ratio (HR) for recurrence after surgery of 0.70 to 1.00, with alternative durations. The maximum affordable cost was the threshold of JPY 5 million per quality-adjusted life year (QALY) times the incremental QALYs, minus incremental medical costs other than the program cost.",
    "A.3": "Added to chemotherapy plus pembrolizumab, exercise had a maximum affordable cost of JPY 2,726 thousand per patient at an HR of 0.85 (95% uncertainty interval [2,223, 3,040]). Added to chemotherapy alone, it was JPY 3,443 thousand. A program priced from the medical fee schedule (JPY 192,400) became cost-effective at an HR of 0.989. Medical costs avoided alone paid for it at HRs of 0.958 to 0.914, depending on metastatic treatment costs. The duration of the effect changed the maximum affordable cost more than any cost input. Pembrolizumab cost JPY 2,053 thousand per QALY gained, and exercise would need an HR of 0.425 to match its QALY gain.",
    "A.4": "In Japan, the value of exercise during neoadjuvant chemotherapy depends on the size and duration of its effect on recurrence far more than on its price. Trials should measure recurrence and whether the effect lasts.",
}


def from_user(key):
    return re.sub(r" \[([a-z][a-z0-9_]*(?:, [a-z][a-z0-9_]*)*)\]", lambda m: "⟦ref:" + m.group(1).replace(", ", ",") + "⟧", USER[key])


def verbatim(key, sents):
    built, want = " ".join(sents), from_user(key)
    if built != want:
        i = next((k for k in range(min(len(built), len(want))) if built[k] != want[k]), min(len(built), len(want)))
        raise AssertionError(("text differs from the instruction", key, built[max(0, i - 25):i + 25], want[max(0, i - 25):i + 25]))


# ================================================================ kept paragraphs; the edits of section 1
PARAS = {x["id"]: list(x["sentences"]) for x in led_m8["paragraphs"] if not x["id"].startswith(("T.", "A."))}
ROWS = {x["id"]: [recheck(r) for r in x["numbers"]] for x in led_m8["paragraphs"] if not x["id"].startswith(("T.", "A."))}

# Implications sentence 1 -> two sentences
CUR[0] = "IMP.1"
old = PARAS["IMP.1"][0]
assert old.startswith("Clinicians can offer exercise during neoadjuvant chemotherapy for its known benefits on fitness")
new = [f"Exercise during adjuvant chemotherapy improves fitness{cite('furmaniak2016', 'courneya2007', 'vanwaart2015')}, and trials have delivered "
       f"supervised exercise during neoadjuvant chemotherapy{cite('kjeldsted2025', 'schmidt2025')}.",
       "Clinicians can therefore offer it while its effect on recurrence is tested."]
verbatim("IMP.1 s1", new)
PARAS["IMP.1"] = new + PARAS["IMP.1"][1:]
assert PARAS["IMP.1"][2] == "This analysis adds that an effect on recurrence, if present, would carry large economic value."
LOG.append(("IMP.1", "edit", "section 1: Implications sentence 1 replaced by two sentences", old, " ".join(new)))
# Discussion paragraph 3: one phrase
a, b = USER["D.3 phrase"]
s = PARAS["D.3"][1]
assert s.count(a) == 1
PARAS["D.3"][1] = s.replace(a, b)
LOG.append(("D.3", "edit", "section 1: 'after this regimen' -> 'after neoadjuvant chemotherapy with pembrolizumab'", s, PARAS["D.3"][1]))
# Discussion paragraph 5: the last sentence deleted
gone = from_user("D.5 deleted")
assert PARAS["D.5"][-1] == gone, PARAS["D.5"][-1]
PARAS["D.5"] = PARAS["D.5"][:-1]
LOG.append(("D.5", "delete", "section 1: last sentence of Discussion paragraph 5 deleted (c2h_list still cited in the Introduction)", gone, ""))

# ================================================================ title and Abstract (sections 2 and 3)
TITLE = USER["TITLE"]
verbatim("TITLE", [TITLE])
LOG.append(("T.1", "edit", "section 2: title replaced", SENT8["T.1"][0], TITLE))
ABS = []
CUR[0] = "A.1"
ABS.append(("A.1", "Objectives", [
    "To estimate the maximum cost at which a structured exercise program added to neoadjuvant chemotherapy for stage II or III triple-negative breast "
    "cancer would be cost-effective in Japan."]))
CUR[0] = "A.2"
ABS.append(("A.2", "Methods", [
    "A state-transition model based on KEYNOTE-522 simulated chemotherapy with or without pembrolizumab, each with or without exercise.",
    f"The analysis took the Japanese public healthcare payer perspective over a lifetime, with discounting at {N('2', 'doc', 'docs/model_spec.md', '按年 2% 折现')}% per year.",
    f"The exercise effect was a hazard ratio (HR) for recurrence after surgery of {N('0.70', 'reg', 'tables', 'Table 1, effect on recurrence')} to "
    f"{N('1.00', 'reg', 'tables', 'Table 1, effect on recurrence')}, with alternative durations.",
    f"The maximum affordable cost was the threshold of JPY {N('5', 'reg', 'tables', 'Table 2, title')} million per quality-adjusted life year (QALY) times "
    "the incremental QALYs, minus incremental medical costs other than the program cost."]))
CUR[0] = "A.3"
ABS.append(("A.3", "Results", [
    f"Added to chemotherapy plus pembrolizumab, exercise had a maximum affordable cost of JPY {N('2,726', 'reg', 'tables', 'Table 2, Panel B, base case, main')} "
    f"thousand per patient at an HR of {N('0.85', 'reg', 'tables', 'Table 2, Panels B and C row label')} "
    f"({N('95', 'label', '95% uncertainty interval (Methods, Statistical analysis stage 3)')}% uncertainty interval "
    f"[{N('2,223', 'reg', 'tables', 'Table 2, Panel B, base case, main')}, {N('3,040', 'reg', 'tables', 'Table 2, Panel B, base case, main')}]).",
    f"Added to chemotherapy alone, it was JPY {N('3,443', 'reg', 'tables', 'Table 2, Panel B, base case, secondary')} thousand.",
    f"A program priced from the medical fee schedule (JPY {N('192,400', 'reg', 'tables', 'Table 1, exercise program')}) became cost-effective at an HR of "
    f"{N('0.989', 'reg', 'tables', 'Table 2, Panel A, cap = E02, main')}.",
    f"Medical costs avoided alone paid for it at HRs of {N('0.958', 'reg', 'tables', 'Table 2, Panel A, avoided = E02, main')} to "
    f"{N('0.914', 'reg', 'tables', 'Table 2, Panel C, eri, avoided = E02, main')}, depending on metastatic treatment costs.",
    "The duration of the effect changed the maximum affordable cost more than any cost input.",
    f"Pembrolizumab cost JPY {N('2,053', 'reg', 'tables', 'Table 3, base, ICER')} thousand per QALY gained, and exercise would need an HR of "
    f"{N('0.425', 'reg', 'tables', 'Table 3, Panel C, HR')} to match its QALY gain."]))
CUR[0] = "A.4"
ABS.append(("A.4", "Conclusions", [
    "In Japan, the value of exercise during neoadjuvant chemotherapy depends on the size and duration of its effect on recurrence far more than on its price.",
    "Trials should measure recurrence and whether the effect lasts."]))
for pid, lab, sents in ABS:
    verbatim(pid, sents)
    LOG.append((pid, "edit", f"section 3: Abstract, {lab} replaced", " ".join(SENT8[pid]), " ".join(sents)))
# the Abstract numbers of "Added to chemotherapy alone": the cap at HR 0.85 of the secondary comparison (Table 2, Panel B, base case)
assert next(x for x in REGS["tables"]["rows"] if x["where"].startswith("Table 2, Panel B, base case, secondary"))["shown"] == "3,443"

# ---------------------------------------------------------------- statements resting on table values (kept from v8)
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
    "A.3 s5 duration changed the cap more than any cost input": dict(duration_range_yen=[round(dur["dur1"], 2), round(dur["dur2"], 2)],
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


set_text(ELEM8["T.1"], TITLE)
for pid, _, sents in ABS:
    set_text(ELEM8[pid], " ".join(sents))
for pid, sents in PARAS.items():
    set_text(ELEM8[pid], " ".join(sents))
for i, ps in enumerate(RES8, start=1):
    set_text(ELEM8[f"R.{i}"], " ".join(s["text"] for s in ps))
for p in allp[i_ref:]:  # the reference list of v8 (number_refs.py writes the list of v9)
    p._p.getparent().remove(p._p)
out = BUILD / "manuscript_marked.docx"
doc.save(out)

# ================================================================ ledgers and paragraph map
ABS_TEXT = {pid: " ".join(sents) for pid, _, sents in ABS}
order = []
for o in map8["order"]:
    if o["kind"] in ("heading", "abstract label"):
        order.append(dict(o))
    elif o["id"] == "T.1":
        order.append(dict(id="T.1", kind="title", text=TITLE))
    elif o["id"].startswith("A."):
        order.append(dict(id=o["id"], kind="body", text=ABS_TEXT[o["id"]]))
    elif o["id"].startswith("R."):
        order.append(dict(id=o["id"], kind="body", text=" ".join(s["text"] for s in RES8[int(o["id"][2:]) - 1])))
    else:
        order.append(dict(id=o["id"], kind="body", text=" ".join(PARAS[o["id"]])))
d9 = Document(out)
assert [p.text for p in d9.paragraphs if p.text.strip()] == [o["text"] for o in order], "manuscript_marked.docx does not read back as the paragraph map"
assert [p.text for p in d9.paragraphs[:1 + N_BLANK]] == [TITLE] + [""] * N_BLANK and not any(r.bold for r in d9.paragraphs[0].runs)

rows_all = [r for pid in PARAS for r in ROWS[pid]] + MROWS
secs = [dict(id="T.1", sentences=[TITLE], numbers=[])] + [dict(id=pid, sentences=sents, numbers=[r for r in rows_all if r["where"] == pid]) for pid, _, sents in ABS] + \
       [dict(id=pid, sentences=sents, numbers=[r for r in rows_all if r["where"] == pid]) for pid, sents in PARAS.items()]

strip = lambda t: MARK_RE.sub("", re.sub(r"\b(?:Supplementary )?(?:Tables?|Figs?\.|Methods) S?\d+[a-z]?(?:\s*(?:and|to|,)\s*S?\d+)*", " ", t))
main_tok = {t for pid, ss in PARAS.items() for s in ss for t in num_tokens(strip(s))} | {t for ps in RES8 for s in ps for t in num_tokens(strip(s["text"]))}
ABS_CHECK = []
for pid, _, sents in ABS:
    for s in sents:
        for t in num_tokens(strip(s)):
            in_tab = any(x["shown"] == t for x in REGS["tables"]["rows"] + REGS["tables"]["labels"])
            ABS_CHECK.append(dict(paragraph=pid, shown=t, in_main_text=t in main_tok, in_tables=in_tab))
            assert t in main_tok or in_tab, (pid, t)
json.dump({"paragraphs": secs, "rows": rows_all, "text_checks": TEXT_CHECKS, "abstract_numbers": ABS_CHECK},
          open(BUILD / "_ledger_manuscript.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
USED = []
for u in led_r8["used"]:  # Results unchanged; every number still shown at the same place
    rows = REGS[u["registry"]]["rows"] + (REGS[u["registry"]]["labels"] if u.get("source") == "label" else [])
    assert u["shown"] in {x["shown"] for x in rows if x["where"] == u["where"]}, ("value no longer in the registry", u)
    USED.append(dict(u))
led = {"paragraphs": RES8, "used": USED, "base": f"manuscript_{PREV}.docx", "edits": [dict(zip(("paragraph", "kind", "reason", "before", "after"), x)) for x in LOG]}
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
    if x["id"].startswith(("A.", "D.3", "D.5", "IMP.1")):
        w = [words(s) for s in x["sentences"]]
        print(f"  {x['id']}: {sum(w)} words, longest sentence {max(w)}, numbers {len(x['numbers'])}")
print("abstract numbers not in the main-text prose:", [(a["paragraph"], a["shown"]) for a in ABS_CHECK if not a["in_main_text"]])
print("edits:", len(LOG))
