"""Manuscript v7: direct edit of manuscript_v6.docx (WRITING_RULES 1.2 rule 2).

Opens manuscript/archive/v6/manuscript_v6.docx (sha256 checked against MANIFEST_v6), turns its
superscript reference numbers back into markers (number -> key from the reference list of the same
file) and removes that list. Instruction "v7" section 1: the two pathway-B sentences leave Results
paragraph 1 and a new paragraph, the user's text, follows it. Section 2: the Discussion,
Implications and Limitations of v6 are replaced by the user's text. All other paragraphs are kept
word for word (their reference numbers change with the renumbering). The new text is compared
mechanically with the user's text (USER below). Every number of a new sentence is registered with
its source and checked there; the numbers of the kept paragraphs are carried over from the v6
ledger and checked again against the current registries. number_refs.py then numbers the markers.

Writes _build/manuscript_marked.docx, _build/_ledger_results.json (and a _v7 copy),
_build/_ledger_manuscript.json and _build/_manuscript_map.json. Runs for v7 only; later versions
edit manuscript_v7.docx directly.
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

from common import ARCHIVE_PREV, BUILD, PREV, ROOT, SUPP, VER, fnum, num_tokens, sha256
from references import MARK_RE, PUBMED, REFS, entry, expand

sys.stdout.reconfigure(encoding="utf-8")
if VER != "v7":
    raise SystemExit("edit_manuscript_v7.py holds the edits of v7 only; write the next version's edits on manuscript_v7.docx")

SNAP = BUILD / "v6_snapshot"  # _build records of v6, copied before this build
REGS = {name: json.load(open(BUILD / f"_ledger_{name}.json", encoding="utf-8")) for name in ("tables", "supplement", "figures", "suppfigs")}
led_m6 = json.load(open(SNAP / "_ledger_manuscript.json", encoding="utf-8"))
led_r6 = json.load(open(SNAP / f"_ledger_results_{PREV}.json", encoding="utf-8"))
map6 = json.load(open(SNAP / "_manuscript_map.json", encoding="utf-8"))
S = SUPP
JB = "input/params/cohort_N_jbcs2024.csv"

# ================================================================ the base: manuscript_v6.docx and its manifest
SRC = ARCHIVE_PREV / f"manuscript_{PREV}.docx"
man = (ARCHIVE_PREV / f"MANIFEST_{PREV}.md").read_text(encoding="utf-8")
assert f"| manuscript/{PREV}/manuscript_{PREV}.docx | {sha256(SRC)} |" in man, "manuscript_v6.docx differs from MANIFEST_v6.md"
doc = Document(SRC)
allp = [p for p in doc.paragraphs if p.text.strip()]
i_ref = next(i for i, p in enumerate(allp) if p.text == "References")
assert i_ref == len(map6["order"]), (i_ref, len(map6["order"]))

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


# the v6 docx, its paragraph map and its ledgers must agree
TEXT6, ELEM6 = {}, {}
for o, p in zip(map6["order"], allp[:i_ref]):
    t = demark(p)
    if o["kind"] == "heading":
        assert t == o["text"] and all(r.bold for r in p.runs if r.text.strip()), (o, t)
        continue
    TEXT6[o["id"]], ELEM6[o["id"]] = t, p
    assert keyset_norm(t) == keyset_norm(o["text"]), ("v6 docx and paragraph map differ", o["id"])
for x in led_m6["paragraphs"]:
    assert keyset_norm(" ".join(x["sentences"])) == keyset_norm(TEXT6[x["id"]]), ("v6 ledger and docx differ", x["id"])
RES6 = led_r6["paragraphs"]
for i, ps in enumerate(RES6, start=1):
    assert TEXT6[f"R.{i}"] == " ".join(s["text"] for s in ps), ("v6 Results ledger and docx differ", i)

# ================================================================ number registration (as in edit_manuscript_v6.py)
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
    if kind == "lit":  # printed in the abstract of the cited article
        (key,) = a
        assert tok in PUBMED[key]["abstract"], (tok, key)
        src, loc = f"PubMed {PUBMED[key]['pmid']} ({key})", "abstract"
    elif kind == "doc":  # written in a project file
        path, needle = a
        i, ln = _line(path, needle)
        assert tok in ln, (tok, path, ln)
        src, loc = path, f"line {i}: {needle}"
    elif kind == "reg":  # shown in a table, figure or supplementary table
        reg, prefix = a
        rows = _reg_rows(reg, prefix, tok)
        assert rows, (tok, reg, prefix)
        src, loc = f"_ledger_{reg}.json", f"{rows[0]['where']} ({rows[0].get('source', rows[0].get('reason', ''))})"
    elif kind == "csv":  # value of the registry file of Japanese patient numbers
        path, item = a
        assert fnum(float(_csv(path, item)), 0) == tok, (tok, item)
        src, loc = path, f"item = {item}, value"
    elif kind == "csvpct":  # proportion in the same file, shown in %
        path, item, nd = a
        v = float(_csv(path, item))
        assert fnum(100 * v, nd) == tok, (tok, item, v)
        src, loc = path, f"item = {item}, value {v} x 100"
    else:
        raise ValueError(kind)
    MROWS.append(dict(shown=tok, where=CUR[0], source=src, loc=loc))
    return tok


def recheck(r):
    """A number carried over from the v6 ledger, checked again at its source."""
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
        assert fnum(float(_csv(src, item)), 0) == tok, r
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

# ================================================================ the user's text (instruction sections 1 and 2), word for word
# "[a, b]" are reference keys (keys start with a letter; "[238, 570]" in the Results text is a 95% UI)
USER = {
    "R.2": "Supplementary Table S5 shows the maximum affordable cost when exercise acted through pCR instead of the recurrence HR. An increase of 1 percentage point in pCR gave JPY 389 thousand (95% UI [238, 570]), and an increase of 10 percentage points gave JPY 3,898 thousand (95% UI [2,388, 5,713]).",
    "D.1": "In Japan, adding a structured exercise program to neoadjuvant chemotherapy for stage II or III TNBC would be cost-effective even if it lowered the risk of recurrence only slightly. With chemotherapy plus pembrolizumab, the fee-schedule-based program became cost-effective once it lowered the recurrence hazard by 1.1% (Table 2). How much a program could cost depended mostly on how large its effect was and how long it lasted. Pembrolizumab itself was cost-effective at both Japanese thresholds (Table 3).",
    "D.2": "Most of the value of exercise came from the distant recurrences it would prevent. In Japan, one month of treatment after distant recurrence costs more than the whole exercise program (Table 1). The medical costs avoided alone paid for the program once the recurrence hazard fell by 4.2% to 8.6%, depending on the cost of metastatic treatment (Table 2). Cheaper metastatic treatment reduced these savings but barely moved the point at which the program became cost-effective (Table 2).",
    "D.3": "Duration changed the maximum affordable cost more than any cost input did (Table 2; Fig. 3). Most recurrences after neoadjuvant chemo-immunotherapy occur within 24 months of randomization [licata2025]. An effect that holds through the first years after surgery therefore captures most of the value. When the effect of the neoadjuvant program alone would fade early, continuing exercise after surgery raised the maximum affordable cost (Supplementary Table S7).",
    "D.4": "Exercise cannot replace pembrolizumab. To gain as many QALYs as pembrolizumab, exercise added to chemotherapy alone would need to lower the recurrence hazard by more than half (Table 3). Trials of exercise in cancer have reported much smaller effects [courneya2025, courneya2014]. The maximum affordable cost was higher without pembrolizumab, because more patients relapse and the same relative effect prevents more recurrences (Table 2). In 2024, 2,294 of 3,451 patients in Japan who received neoadjuvant chemotherapy for stage II or III TNBC also received pembrolizumab [jbcs55]. The main comparison therefore reflects most current practice.",
    "D.5": "Pembrolizumab added to neoadjuvant chemotherapy was cost-effective in Japan, as in analyses from the United States, Hong Kong, Switzerland and Egypt [huang2023, kwong2024, favrebulle2024, pollinger2025]. Its cost-effectiveness depended most on its price and on whether capecitabine or olaparib was added after surgery, as in Japanese practice (Table 3; Supplementary Fig. S2). The regimen has not been designated for Japan's cost-effectiveness evaluation [c2h_list], and our estimate gives a reference in the meantime.",
    "D.6": "Earlier economic evaluations of exercise in cancer valued effects on fatigue, fitness or quality of life during or shortly after treatment [khan2019, gublergut2021, wang2023], and their conclusions varied [may2017, vanwaart2018, perrier2020]. The cost-utility analysis of CHALLENGE valued an effect on disease-free survival over 5 years [chan2026]. The program cost less and gave more health than health education, and recurrence, new cancers and their treatment drove the costs [chan2026]. Our results point the same way. Each recurrence prevented avoids months of costly treatment and years of lost health, which together outweigh the cost of an exercise program.",
    "D.7": "In Japanese practice, a given effect of exercise may be worth more than the model suggests. In the 2024 national registry, 47% of patients treated with neoadjuvant chemotherapy had a pCR [jbcs55], fewer than in either arm of KEYNOTE-522 (Table 1). More patients therefore have residual disease, a higher risk of recurrence and more recurrences for exercise to prevent.",
    "IMP.1": "Clinicians already have reasons to offer exercise during chemotherapy, because trials have shown better fitness and, in some, less fatigue [furmaniak2016, courneya2007, vanwaart2015, mijwel2018]. This analysis adds that an effect on recurrence, if present, would carry large economic value. Trials of exercise during neoadjuvant chemotherapy should record recurrence and follow patients long enough to see whether the effect lasts after the program ends. A higher pCR alone cannot settle the question, because it is unknown how a change in pCR with exercise would translate into fewer recurrences (Supplementary Table S5). Funders can weigh the cost of such trials against the net benefit for one year of Japanese patients if an effect is confirmed (Supplementary Table S8).",
    "IMP.2": "For payers, the price of a supervised program is far below what a confirmed effect would justify (Table 2). Support that keeps patients exercising after surgery, such as remote programs, would add value if it extends the effect (Supplementary Table S7). For pembrolizumab, this analysis gives Japan a reference value before any formal cost-effectiveness evaluation.",
    "L.1": "The effect of exercise during neoadjuvant chemotherapy on recurrence is unknown, so all results for exercise are conditional on the assumed HR and duration. The CHALLENGE estimate shown for reference comes from a 3-year program after adjuvant chemotherapy for colon cancer and may not apply to breast cancer. The model credited exercise only with fewer recurrences after surgery. Effects on fatigue, quality of life or completion of chemotherapy were not counted, so the maximum affordable cost is likely understated. Survival was modeled from data reconstructed from published curves, and the 7-year event-free survival by pCR status came from the presentation of the final analysis. Errors in these inputs would change the baseline risk of recurrence and, with it, the value of a given effect.",
    "L.2": "Survival after distant recurrence came from a French cohort diagnosed in 2008 to 2020, largely before immunotherapy and antibody–drug conjugates [grinda2023]. Longer survival with current treatment would raise the costs avoided by each prevented recurrence but lower the QALYs gained, with opposite effects on the maximum affordable cost. Several costs relied on clinical expert input, and ranges were set by rule where sources gave none, but no single cost changed the conclusion (Fig. 3). Utilities came from the German value set, and values from Japanese populations gave nearly the same results (Supplementary Table S10). The registry does not capture every case, so the one-year net benefit is likely understated.",
}


def from_user(pid):
    return re.sub(r" \[([a-z][a-z0-9_]*(?:, [a-z][a-z0-9_]*)*)\]", lambda m: "⟦ref:" + m.group(1).replace(", ", ",") + "⟧", USER[pid])


def verbatim(pid, sents):
    built, want = " ".join(sents), from_user(pid)
    if built != want:
        i = next((k for k in range(min(len(built), len(want))) if built[k] != want[k]), min(len(built), len(want)))
        raise AssertionError(("text differs from the instruction", pid, built[max(0, i - 25):i + 25], want[max(0, i - 25):i + 25]))


# ================================================================ Introduction and Methods: kept word for word
heads_before, pending = {}, []
for o in map6["order"]:
    if o["kind"] == "heading":
        pending.append(o["text"])
    else:
        heads_before[o["id"]] = pending
        pending = []
KEEP = [x for x in led_m6["paragraphs"] if x["id"].startswith(("I.", "M."))]
INTRO_METHODS = [[x["id"], heads_before[x["id"]], list(x["sentences"])] for x in KEEP]
ROWS6 = {x["id"]: [recheck(r) for r in x["numbers"]] for x in KEEP}
OLD_DIL = [x["id"] for x in led_m6["paragraphs"] if x["id"].startswith(("D.", "IMP.", "L."))]
assert OLD_DIL == ["D.1", "D.2", "D.3", "D.4", "D.5", "D.6", "D.7", "IMP.1", "L.1"], OLD_DIL


# ================================================================ Results (section 1)
def V(reg, where, idx=0):
    rows = [x for x in REGS[reg]["rows"] if x["where"] == where]
    if len(rows) <= idx:
        raise KeyError(f"{reg}: no entry {idx} for {where!r}")
    return rows[idx]


for u in led_r6["used"]:  # every number of the v6 Results is still shown at the same place
    rows = REGS[u["registry"]]["rows"] + (REGS[u["registry"]]["labels"] if u.get("source") == "label" else [])
    assert u["shown"] in {x["shown"] for x in rows if x["where"] == u["where"]}, ("value no longer in the registry", u)
SPB = f"Supplementary Table {S['pathB']}"
p1 = copy.deepcopy(RES6[0])
assert p1[5]["text"].startswith("Through an effect on pCR instead, an increase of 1 percentage point") and p1[6]["text"].startswith("An increase of 10 percentage points")
dropped = p1[5:]
p1 = p1[:5]
LOG.append(("R.1", "edit", "section 1: the two pathway-B sentences deleted from Results paragraph 1",
            " ".join(s["text"] for s in RES6[0]), " ".join(s["text"] for s in p1)))
w1, w10 = f"{SPB}, A, pcr 0.010, main base", f"{SPB}, A, pcr 0.100, main base"
a1, a10 = [V("supplement", w1, i)["shown"] for i in range(3)], [V("supplement", w10, i)["shown"] for i in range(3)]
r_lab = {x["shown"]: x for x in REGS["supplement"]["rows"] if x["where"] == f"{SPB}, row label"}
p2 = [dict(text=f"{SPB} shows the maximum affordable cost when exercise acted through pCR instead of the recurrence HR.", cites=[SPB], keys=[], origin="new in v7"),
      dict(text=f"An increase of {r_lab['1']['shown']} percentage point in pCR gave JPY {a1[0]} thousand (95% UI [{a1[1]}, {a1[2]}]), and an increase of "
                f"{r_lab['10']['shown']} percentage points gave JPY {a10[0]} thousand (95% UI [{a10[1]}, {a10[2]}]).",
           cites=[SPB], keys=["1", "a1", "b1", "c1", "10", "a10", "b10", "c10"], origin="new in v7")]
verbatim("R.2", [s["text"] for s in p2])
LOG.append(("R.2", "new", "section 1: new paragraph after Results paragraph 1 (pathway B, Supplementary Table S5), the user's text", "", " ".join(s["text"] for s in p2)))
RES = [p1, p2] + [copy.deepcopy(ps) for ps in RES6[1:]]
USED = []
for u in led_r6["used"]:
    if u["paragraph"] == 1 and u["sentence"] >= 6:
        continue  # the deleted sentences
    USED.append(dict(u, paragraph=u["paragraph"] + (1 if u["paragraph"] >= 2 else 0)))
for ph, where, i in (("a1", w1, 0), ("b1", w1, 1), ("c1", w1, 2), ("a10", w10, 0), ("b10", w10, 1), ("c10", w10, 2)):
    x = V("supplement", where, i)
    USED.append(dict(paragraph=2, sentence=2, placeholder=ph, registry="supplement", where=where, shown=x["shown"], source=x["source"], loc=x["loc"]))
for ph in ("1", "10"):
    x = r_lab[ph]
    USED.append(dict(paragraph=2, sentence=2, placeholder=ph, registry="supplement", where=f"{SPB}, row label", shown=x["shown"], source=x["source"], loc=x["loc"]))

# ================================================================ Discussion, Implications, Limitations (section 2)
T1, T2, T3 = "Table 1", "Table 2", "Table 3"
SNB, SDU, S10 = (f"Supplementary Table {S[k]}" for k in ("netbenefit", "duration", "other"))
NEW = []  # (id, heading or None, sentences)


def para_new(pid, head, sents):
    verbatim(pid, sents)
    NEW.append((pid, head, sents))


CUR[0] = "D.1"
para_new("D.1", "Discussion", [
    "In Japan, adding a structured exercise program to neoadjuvant chemotherapy for stage II or III TNBC would be cost-effective even if it lowered "
    "the risk of recurrence only slightly.",
    "With chemotherapy plus pembrolizumab, the fee-schedule-based program became cost-effective once it lowered the recurrence hazard by "
    f"{N('1.1', 'reg', 'tables', 'Table 2, Panel A, cap = E02, main, reduction %')}% ({T2}).",
    "How much a program could cost depended mostly on how large its effect was and how long it lasted.",
    f"Pembrolizumab itself was cost-effective at both Japanese thresholds ({T3}).",
])
CUR[0] = "D.2"
para_new("D.2", None, [
    "Most of the value of exercise came from the distant recurrences it would prevent.",
    f"In Japan, one month of treatment after distant recurrence costs more than the whole exercise program ({T1}).",
    f"The medical costs avoided alone paid for the program once the recurrence hazard fell by {N('4.2', 'reg', 'tables', 'Table 2, Panel A, avoided = E02, main, reduction %')}% "
    f"to {N('8.6', 'reg', 'tables', 'Table 2, Panel C, eri, avoided = E02, main, reduction %')}%, depending on the cost of metastatic treatment ({T2}).",
    f"Cheaper metastatic treatment reduced these savings but barely moved the point at which the program became cost-effective ({T2}).",
])
CUR[0] = "D.3"
para_new("D.3", None, [
    f"Duration changed the maximum affordable cost more than any cost input did ({T2}; Fig. 3).",
    f"Most recurrences after neoadjuvant chemo-immunotherapy occur within {N('24', 'lit', 'licata2025')} months of randomization{cite('licata2025')}.",
    "An effect that holds through the first years after surgery therefore captures most of the value.",
    f"When the effect of the neoadjuvant program alone would fade early, continuing exercise after surgery raised the maximum affordable cost ({SDU}).",
])
CUR[0] = "D.4"
para_new("D.4", None, [
    "Exercise cannot replace pembrolizumab.",
    f"To gain as many QALYs as pembrolizumab, exercise added to chemotherapy alone would need to lower the recurrence hazard by more than half ({T3}).",
    f"Trials of exercise in cancer have reported much smaller effects{cite('courneya2025', 'courneya2014')}.",
    f"The maximum affordable cost was higher without pembrolizumab, because more patients relapse and the same relative effect prevents more recurrences ({T2}).",
    f"In {N('2024', 'doc', JB, '（2024 年）')}, {N('2,294', 'csv', JB, 'nac_pembro')} of {N('3,451', 'csv', JB, 'nac_total')} patients in Japan who received "
    f"neoadjuvant chemotherapy for stage II or III TNBC also received pembrolizumab{cite('jbcs55')}.",
    "The main comparison therefore reflects most current practice.",
])
CUR[0] = "D.5"
para_new("D.5", None, [
    "Pembrolizumab added to neoadjuvant chemotherapy was cost-effective in Japan, as in analyses from the United States, Hong Kong, Switzerland and "
    f"Egypt{cite('huang2023', 'kwong2024', 'favrebulle2024', 'pollinger2025')}.",
    "Its cost-effectiveness depended most on its price and on whether capecitabine or olaparib was added after surgery, as in Japanese practice "
    f"({T3}; Supplementary Fig. {S['fig_icer']}).",
    f"The regimen has not been designated for Japan's cost-effectiveness evaluation{cite('c2h_list')}, and our estimate gives a reference in the meantime.",
])
CUR[0] = "D.6"
para_new("D.6", None, [
    "Earlier economic evaluations of exercise in cancer valued effects on fatigue, fitness or quality of life during or shortly after treatment"
    f"{cite('khan2019', 'gublergut2021', 'wang2023')}, and their conclusions varied{cite('may2017', 'vanwaart2018', 'perrier2020')}.",
    f"The cost-utility analysis of CHALLENGE valued an effect on disease-free survival over {N('5', 'lit', 'chan2026')} years{cite('chan2026')}.",
    f"The program cost less and gave more health than health education, and recurrence, new cancers and their treatment drove the costs{cite('chan2026')}.",
    "Our results point the same way.",
    "Each recurrence prevented avoids months of costly treatment and years of lost health, which together outweigh the cost of an exercise program.",
])
CUR[0] = "D.7"
para_new("D.7", None, [
    "In Japanese practice, a given effect of exercise may be worth more than the model suggests.",
    f"In the {N('2024', 'doc', JB, '（2024 年）')} national registry, {N('47', 'csvpct', JB, 'pcr_registry', 0)}% of patients treated with neoadjuvant chemotherapy "
    f"had a pCR{cite('jbcs55')}, fewer than in either arm of KEYNOTE-522 ({T1}).",
    "More patients therefore have residual disease, a higher risk of recurrence and more recurrences for exercise to prevent.",
])
CUR[0] = "IMP.1"
para_new("IMP.1", "Implications", [
    "Clinicians already have reasons to offer exercise during chemotherapy, because trials have shown better fitness and, in some, less fatigue"
    f"{cite('furmaniak2016', 'courneya2007', 'vanwaart2015', 'mijwel2018')}.",
    "This analysis adds that an effect on recurrence, if present, would carry large economic value.",
    "Trials of exercise during neoadjuvant chemotherapy should record recurrence and follow patients long enough to see whether the effect lasts after "
    "the program ends.",
    "A higher pCR alone cannot settle the question, because it is unknown how a change in pCR with exercise would translate into fewer recurrences "
    f"({SPB}).",
    f"Funders can weigh the cost of such trials against the net benefit for one year of Japanese patients if an effect is confirmed ({SNB}).",
])
CUR[0] = "IMP.2"
para_new("IMP.2", None, [
    f"For payers, the price of a supervised program is far below what a confirmed effect would justify ({T2}).",
    f"Support that keeps patients exercising after surgery, such as remote programs, would add value if it extends the effect ({SDU}).",
    "For pembrolizumab, this analysis gives Japan a reference value before any formal cost-effectiveness evaluation.",
])
CUR[0] = "L.1"
para_new("L.1", "Limitations", [
    "The effect of exercise during neoadjuvant chemotherapy on recurrence is unknown, so all results for exercise are conditional on the assumed HR "
    "and duration.",
    f"The CHALLENGE estimate shown for reference comes from a {N('3', 'reg', 'tables', 'Table 1, reference value')}-year program after adjuvant "
    "chemotherapy for colon cancer and may not apply to breast cancer.",
    "The model credited exercise only with fewer recurrences after surgery.",
    "Effects on fatigue, quality of life or completion of chemotherapy were not counted, so the maximum affordable cost is likely understated.",
    "Survival was modeled from data reconstructed from published curves, and the "
    f"{N('7', 'reg', 'supplement', 'Supplementary Methods ' + S['methods_survival'])}-year event-free survival by pCR status came from the presentation "
    "of the final analysis.",
    "Errors in these inputs would change the baseline risk of recurrence and, with it, the value of a given effect.",
])
CUR[0] = "L.2"
para_new("L.2", None, [
    f"Survival after distant recurrence came from a French cohort diagnosed in {N('2008', 'lit', 'grinda2023')} to {N('2020', 'lit', 'grinda2023')}, "
    f"largely before immunotherapy and antibody–drug conjugates{cite('grinda2023')}.",
    "Longer survival with current treatment would raise the costs avoided by each prevented recurrence but lower the QALYs gained, with opposite "
    "effects on the maximum affordable cost.",
    "Several costs relied on clinical expert input, and ranges were set by rule where sources gave none, but no single cost changed the conclusion "
    "(Fig. 3).",
    f"Utilities came from the German value set, and values from Japanese populations gave nearly the same results ({S10}).",
    "The registry does not capture every case, so the one-year net benefit is likely understated.",
])
for pid, head, sents in NEW:
    LOG.append((pid, "new", "section 2: Discussion, Implications and Limitations replaced by the user's text", "", " ".join(sents)))
LOG.append(("D.1-D.7, IMP.1, L.1 (v6)", "delete", "section 2: replaced as a whole", " ".join(" ".join(x["sentences"]) for x in led_m6["paragraphs"]
                                                                                           if x["id"] in OLD_DIL), ""))

# the statements of the new text that rest on table values without printing them (instruction section 3)
P = __import__("common").Params()
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
TEXT_CHECKS = {
    "D.2 s2 one month after distant recurrence > whole program": dict(monthly_yen={k: round(v, 2) for k, v in monthly.items()}, programs_yen=progs,
                                                                      lowest_monthly=min(monthly, key=monthly.get), highest_program=max(progs, key=progs.get)),
    "D.4 s2 more than half": dict(hr_table3_panel_c=hr_c, reduction=round(1 - hr_c, 4)),
    "L.2 s3 no single cost changed the conclusion": dict(caps_s9_n=len(caps9), caps_min_yen=round(min(caps9), 2), program_max_yen=max(progs.values()),
                                                         icers_s9_n=len(icers9), icer_max_yen_per_qaly=round(max(icers9), 2), threshold=5e6),
}

# ================================================================ docx
set_runs = {}


def set_text(p, text):
    """One run with the format of the paragraph's first run (number_refs.py splits it at the markers)."""
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
    t = runs[0].find(qn("w:t"))
    t.text = text
    t.set(qn("xml:space"), "preserve")
    return el


for pid, _, sents in INTRO_METHODS:
    set_text(ELEM6[pid], " ".join(sents))
for i in range(1, len(RES6) + 1):  # v6 R.1 -> v7 R.1, v6 R.k -> v7 R.(k+1)
    set_text(ELEM6[f"R.{i}"], " ".join(s["text"] for s in RES[0 if i == 1 else i]))
i_dis = next(i for i, p in enumerate(allp) if p.text == "Discussion")
HEAD = copy.deepcopy(allp[i_dis]._p)
BODY = copy.deepcopy(ELEM6["R.10"]._p)
for p in allp[i_dis:]:  # Discussion to Limitations of v6 and the reference list (number_refs.py writes the list of v7)
    p._p.getparent().remove(p._p)
r2 = clone(BODY, " ".join(s["text"] for s in RES[1]))
ELEM6["R.1"]._p.addnext(r2)
anchor = ELEM6["R.10"]._p
for pid, head, sents in NEW:
    if head:
        h = clone(HEAD, head)
        anchor.addnext(h)
        anchor = h
    b = clone(BODY, " ".join(sents))
    anchor.addnext(b)
    anchor = b
out = BUILD / "manuscript_marked.docx"
doc.save(out)

# ================================================================ ledgers and paragraph map
order = []
for o in map6["order"]:
    if o["kind"] == "heading":
        if o["text"] == "Discussion":
            break
        order.append(dict(id=None, kind="heading", text=o["text"]))
    elif o["id"].startswith("R."):
        k = int(o["id"][2:])
        if k == 1:
            order.append(dict(id="R.1", kind="body", text=" ".join(s["text"] for s in RES[0])))
            order.append(dict(id="R.2", kind="body", text=" ".join(s["text"] for s in RES[1])))
        else:
            order.append(dict(id=f"R.{k + 1}", kind="body", text=" ".join(s["text"] for s in RES[k])))
    else:
        order.append(dict(id=o["id"], kind="body", text=" ".join(next(x[2] for x in INTRO_METHODS if x[0] == o["id"]))))
for pid, head, sents in NEW:
    if head:
        order.append(dict(id=None, kind="heading", text=head))
    order.append(dict(id=pid, kind="body", text=" ".join(sents)))
chk = [p for p in Document(out).paragraphs if p.text.strip()]
assert [p.text for p in chk] == [o["text"] for o in order], "manuscript_marked.docx does not read back as the paragraph map"
assert [o["id"] for o in order if o["id"] and o["id"].startswith("R.")] == [f"R.{k}" for k in range(1, len(RES) + 1)]

rows_all = [r for pid, _, _ in INTRO_METHODS for r in ROWS6[pid]] + MROWS
secs = [dict(id=pid, sentences=sents, numbers=[r for r in rows_all if r["where"] == pid]) for pid, _, sents in INTRO_METHODS] + \
       [dict(id=pid, sentences=sents, numbers=[r for r in rows_all if r["where"] == pid]) for pid, _, sents in NEW]
json.dump({"paragraphs": secs, "rows": rows_all, "text_checks": TEXT_CHECKS}, open(BUILD / "_ledger_manuscript.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
led = {"paragraphs": RES, "used": USED, "base": f"manuscript_{PREV}.docx", "edits": [dict(zip(("paragraph", "kind", "reason", "before", "after"), x)) for x in LOG]}
for name in ("_ledger_results.json", f"_ledger_results_{VER}.json"):
    json.dump(led, open(BUILD / name, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"version": VER, "ids": [o["id"] for o in order if o["id"]], "order": order, "manuscript_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
           "edits": [dict(zip(("paragraph", "kind", "reason", "before", "after"), x)) for x in LOG]},
          open(BUILD / "_manuscript_map.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# every number of a non-Results paragraph must be registered for it
strip = lambda t: MARK_RE.sub("", re.sub(r"\b(?:Supplementary )?(?:Tables?|Figs?\.|Methods) S?\d+[a-z]?(?:\s*(?:and|to|,)\s*S?\d+)*", " ", t))
bad = [(x["id"], t, s[:60]) for x in secs for s in x["sentences"] for t in num_tokens(strip(s)) if t not in {r["shown"] for r in x["numbers"]}]
assert not bad, bad


def words(t):
    return len(MARK_RE.sub("", t).split())


print("manuscript_marked.docx written from", SRC.name)
for x in secs:
    if x["id"].startswith(("D.", "IMP.", "L.")):
        w = [words(s) for s in x["sentences"]]
        print(f"  {x['id']}: {sum(w)} words, longest sentence {max(w)}, numbers {len(x['numbers'])}")
for i, ps in enumerate(RES, start=1):
    w = [len(s["text"].split()) for s in ps]
    print(f"  R.{i}: {sum(w)} words, longest sentence {max(w)}")
print("edits:", len(LOG), "| text checks:", json.dumps(TEXT_CHECKS, ensure_ascii=False))
