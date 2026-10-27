"""Manuscript v6: direct edit of manuscript_v5.docx (WRITING_RULES 1.2 rule 2).

Opens manuscript/archive/v5/manuscript_v5.docx, turns its superscript reference numbers back
into markers (number -> key from the reference list of the same file), removes that list,
changes only the sentences named in the instruction "执笔第 4 步（v6）" (sections 1 to 3) and
inserts the Discussion, Implications and Limitations of section 5 after the Results. The new
text is the user's text word for word (USER below, compared mechanically), except the two
places marked "CC:", which are completed from the abstracts of the cited articles. Every
number of a new or changed sentence is registered with its source and checked there; the
numbers of the unchanged paragraphs are carried over from the v5 ledger and checked again
against the current registries. number_refs.py then numbers the markers in reading order.

Writes _build/manuscript_marked.docx, _build/_ledger_results.json (and a _v6 copy),
_build/_ledger_manuscript.json and _build/_manuscript_map.json. Runs for v6 only; later
versions edit manuscript_v6.docx directly.
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
if VER != "v6":
    raise SystemExit("edit_manuscript_v6.py holds the edits of v6 only; write the next version's edits on manuscript_v6.docx")

SNAP = BUILD / "v5_snapshot"  # _build records of v5, copied before this build
REGS = {name: json.load(open(BUILD / f"_ledger_{name}.json", encoding="utf-8")) for name in ("tables", "supplement", "figures", "suppfigs")}
led_m5 = json.load(open(SNAP / "_ledger_manuscript.json", encoding="utf-8"))
led_r5 = json.load(open(SNAP / f"_ledger_results_{PREV}.json", encoding="utf-8"))
map5 = json.load(open(SNAP / "_manuscript_map.json", encoding="utf-8"))
S = SUPP
JB = "input/params/cohort_N_jbcs2024.csv"

# ================================================================ the base: manuscript_v5.docx and its manifest
SRC = ARCHIVE_PREV / f"manuscript_{PREV}.docx"
man = (ARCHIVE_PREV / f"MANIFEST_{PREV}.md").read_text(encoding="utf-8")
assert f"| manuscript/{PREV}/manuscript_{PREV}.docx | {sha256(SRC)} |" in man, "manuscript_v5.docx differs from MANIFEST_v5.md"
doc = Document(SRC)
allp = [p for p in doc.paragraphs if p.text.strip()]
i_ref = next(i for i, p in enumerate(allp) if p.text == "References")
assert i_ref == len(map5["order"]), (i_ref, len(map5["order"]))

# number -> key from the reference list of the same file
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
    """Markers with their keys sorted, so that the key order inside a marker does not matter."""
    return MARK_RE.sub(lambda m: "⟦ref:" + ",".join(sorted(m.group(1).split(","))) + "⟧", t)


# the v5 docx, its paragraph map and its ledgers must agree
TEXT5 = {}
for o, p in zip(map5["order"], allp[:i_ref]):
    t = demark(p)
    if o["kind"] == "heading":
        assert t == o["text"] and all(r.bold for r in p.runs if r.text.strip()), (o, t)
        continue
    TEXT5[o["id"]] = t
    assert keyset_norm(t) == keyset_norm(o["text"]), ("v5 docx and paragraph map differ", o["id"])
SENT5 = {x["id"]: list(x["sentences"]) for x in led_m5["paragraphs"]}
for pid, ss in SENT5.items():
    assert keyset_norm(" ".join(ss)) == keyset_norm(TEXT5[pid]), ("v5 ledger and docx differ", pid)
RES5 = led_r5["paragraphs"]
for i, ps in enumerate(RES5, start=1):
    assert TEXT5[f"R.{i}"] == " ".join(s["text"] for s in ps), ("v5 Results ledger and docx differ", i)

# ================================================================ number registration (as in edit_manuscript.py, v5)
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
    elif kind == "regneg":  # the table shows the incremental cost; the text gives medical costs avoided, its sign reversed (Methods, Outcome)
        reg, prefix = a
        rows = _reg_rows(reg, prefix, "−" + tok)
        assert rows, (tok, reg, prefix)
        src, loc = f"_ledger_{reg}.json", f"{rows[0]['where']} shows −{tok} ({rows[0]['source']}); medical costs avoided = −(incremental medical costs other than the program cost)"
    elif kind == "csv":  # value of the registry file of Japanese patient numbers
        path, item = a
        assert fnum(float(_csv(path, item)), 0) == tok, (tok, item)
        src, loc = path, f"item = {item}, value"
    elif kind == "csvpct":  # proportion in the same file, shown in %
        path, item, nd = a
        v = float(_csv(path, item))
        assert fnum(100 * v, nd) == tok, (tok, item, v)
        src, loc = path, f"item = {item}, value {v} x 100"
    elif kind == "label":  # name or definition, reason given
        (why,) = a
        src, loc = "definition", why
    else:
        raise ValueError(kind)
    MROWS.append(dict(shown=tok, where=CUR[0], source=src, loc=loc))
    return tok


def recheck(r):
    """A number carried over from the v5 ledger, checked again at its source."""
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
        assert fnum(float(_csv(src, loc.split(" = ")[1].split(",")[0])), 0) == tok, r
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

# ================================================================ the user's text (instruction sections 1 and 5), word for word
# "[a, b]" are reference keys; "[CC: ...]" the two places to complete. In paragraph 3 of the Introduction the
# instruction writes "[chisaki2025 至 kashiwa2024 的 7 篇]" for the seven Japanese analyses cited there in v5.
JAPAN7 = ["chisaki2025", "sugiura2023", "taniguchi2026", "kakinuma2025", "morimoto2026", "tomura2025", "kashiwa2024"]
assert "⟦ref:" + ",".join(JAPAN7) + "⟧" in SENT5["I.3"][5]
USER = {
    "I.3": "Economic evaluations of exercise in cancer have valued effects measured in trials, mostly on fatigue, fitness or quality of life during or after adjuvant treatment [khan2019, gublergut2021, wang2023], and in breast cancer they reached different conclusions [may2017, vanwaart2018, perrier2020]. No economic evaluation of exercise during neoadjuvant therapy for breast cancer was identified (Supplementary Methods S1); the nearest, Phys-Can, compared two exercise intensities during neoadjuvant or adjuvant treatment of breast, colorectal or prostate cancer [ax2023]. When the effect on recurrence is unknown, a cost-effectiveness ratio cannot be estimated, but the highest program cost that remains cost-effective can be calculated for each possible effect [boudewijns2023]. Cost-effectiveness analyses of the KEYNOTE-522 regimen come from the United States, Hong Kong, Switzerland and Egypt [huang2023, kwong2024, favrebulle2024, pollinger2025], whereas the Japanese analyses identified concerned pembrolizumab for advanced cancers, including metastatic TNBC [chisaki2025 至 kashiwa2024 的 7 篇], and as of October 2026 the regimen had not been designated for Japan's cost-effectiveness evaluation [c2h_list].",
    "I.4 s3": "Expressing the value of an unproven program as the cost a health system can afford for each possible effect gives future trials of exercise during neoadjuvant therapy a benchmark against which their results can be judged.",
    "D.1": "The value of adding a structured exercise program to neoadjuvant chemotherapy for stage II or III TNBC in Japan depends on how much and for how long the program lowers the risk of recurrence. With chemotherapy plus pembrolizumab, a program could cost up to JPY 2,726 thousand per patient at a recurrence HR of 0.85 and remain cost-effective (Table 2). The most expensive design costed in this study was JPY 239,508 (Table 1). A reduction of 1.1% in the recurrence hazard was enough for the fee-schedule-based program to be cost-effective, and a reduction of 4.2% to 8.6% was enough for it to lower total medical costs (Table 2). For patients in Japan, what remains unknown is whether exercise lowers recurrence at all, and for how long.",
    "D.2": "Most of this value comes from distant recurrences that the program would prevent. Treatment after distant recurrence in Japan now costs JPY 1,215,933 to 1,458,318 per month in first-line treatment and JPY 1,412,953 per month in later lines (Table 1). Medical costs avoided made up JPY 702 thousand of the maximum affordable cost at an HR of 0.85 (Supplementary Table S6). Lower metastatic treatment costs reduced these savings but left the threshold for cost-effectiveness almost unchanged. With these costs halved, or with eribulin-based later-line treatment, the break-even HR was 0.988 and 0.987, while the HR at which exercise lowered total costs fell to 0.918 and 0.914 (Table 2).",
    "D.3": "How long the effect lasts changed the result more than any single cost. If the effect faded from 1 year after surgery, the maximum affordable cost at an HR of 0.85 fell to JPY 1,772 thousand, and if it did not wane, it rose to JPY 3,404 thousand (Table 2). In the one-way analyses, no input moved this cost outside JPY 2,617 thousand to 2,836 thousand (Fig. 3). After neoadjuvant chemo-immunotherapy, most recurrences occur within 24 months of randomization [licata2025], so an effect that lasts through the first years after surgery carries most of the value. Continuing exercise after surgery raised the maximum affordable cost when the effect would otherwise have faded early (Supplementary Table S7).",
    "D.4": "For pembrolizumab, the ICER of JPY 2,053 thousand per QALY lay below both Japanese thresholds (Table 3). Analyses of the same regimen from the United States, Hong Kong, Switzerland and Egypt [huang2023, kwong2024, favrebulle2024, pollinger2025] [CC: 按四篇摘要各自的结论补一句，例如在各自阈值下是否划算]. In Japan, the regimen has not been designated for cost-effectiveness evaluation [c2h_list]. Its ICER rose to JPY 3,044 thousand per QALY when capecitabine or olaparib was added after surgery for patients without pCR, as in Japanese practice, and fell to JPY 1,296 thousand at 75% of the list price of pembrolizumab (Table 3; Supplementary Fig. S2).",
    "D.5": "Exercise cannot stand in for pembrolizumab. To gain as many QALYs as pembrolizumab, exercise added to chemotherapy alone would need a recurrence HR of 0.425 (Table 3), a far larger effect than has been reported for exercise in other settings [courneya2025, courneya2014]. The maximum affordable cost was higher when exercise was added to chemotherapy alone (Table 2), because more recurrences remain for exercise to prevent without pembrolizumab. Exercise is therefore best judged as an addition to the standard regimen, which in Japan was given to 2,294 of 3,451 patients in 2024 [jbcs55].",
    "D.6": "Previous economic evaluations of exercise in cancer valued effects on fatigue, fitness or quality of life during or shortly after treatment [khan2019, gublergut2021, wang2023]. The cost-utility analysis of CHALLENGE valued an effect on disease-free survival over the long term [chan2026] [CC: 按摘要补一句其结论]. Our results agree with it on the main point: once a program changes the risk of recurrence, its value reflects the cost and the loss of health that each prevented recurrence avoids, and both are large relative to the cost of the program. Headroom analysis is used to judge technologies before their effect is known [boudewijns2023]. Here it shows that an effect far smaller than a trial could detect would still pay for the program.",
    "D.7": "In Japanese practice, the value of a given effect may be larger than modeled. In the 2024 national registry, 47% of patients treated with neoadjuvant chemotherapy had a pCR [jbcs55], fewer than in either arm of KEYNOTE-522 (63.0% and 55.6%; Table 1). More patients therefore carry residual disease and the higher risk of recurrence on which exercise would act. Even at an HR of 0.95, the net benefit for one year of Japanese patients would be JPY 2.68 billion (Supplementary Table S8).",
    "IMP.1": "Trials of exercise during neoadjuvant chemotherapy for TNBC should measure recurrence and follow patients long enough to show whether any effect persists after the program ends. A higher pCR would help but cannot settle the question alone. In this model, 1 percentage point more pCR was worth JPY 389 thousand per patient (Supplementary Table S5), but how a change in pCR caused by exercise would translate into fewer recurrences is unknown. Given the net benefit at stake for each year of patients in Japan (Supplementary Table S8), such trials are a sound use of research funds. For payers, the fee-schedule price of a supervised program is far below what a confirmed effect would justify, and support that keeps patients exercising after surgery, such as remote or app-based programs, would add value if it extends the effect (Supplementary Table S7). For pembrolizumab, the analysis provides a Japanese estimate for a regimen that has not been designated for cost-effectiveness evaluation.",
    "L.1": "The effect of exercise during neoadjuvant chemotherapy on recurrence is unknown, so all results for exercise are conditional on an assumed HR and duration of effect. The CHALLENGE estimate used as a reference comes from a 3-year program after adjuvant chemotherapy for colon cancer. The model credited exercise only with fewer recurrences after surgery; effects on fatigue, quality of life or completion of chemotherapy were not counted, so the maximum affordable cost may be understated. Survival was modeled from patient-level data reconstructed from published curves, and the 7-year event-free survival by pCR status came from the presentation of the final analysis rather than a full report. Survival after distant recurrence came from a French cohort treated largely before immunotherapy and antibody–drug conjugates were available, whereas treatment costs reflect regimens used in 2026. Several costs relied on clinical expert input, and ranges were set by rule where sources gave none (Fig. 3). Utilities used the German value set; values from Japanese populations gave similar results (Supplementary Table S10). The number of eligible patients came from a registry that does not capture every case.",
}
# the two completions (instruction section 5: one sentence each, only what the abstracts state; passages in references_v6.md)
CC = {
    "D.4": ("[CC: 按四篇摘要各自的结论补一句，例如在各自阈值下是否划算]", "found it cost-effective, with ICERs below the threshold used in each setting"),
    "D.6": ("[CC: 按摘要补一句其结论]", ". The structured exercise program was less costly and more effective than health education materials, and cancer recurrence "
                                    "or new malignancy and anticancer therapy were the major cost drivers [chan2026]"),
}
# the place before the completion: "... Egypt [refs] [CC]" and "... long term [chan2026] [CC]" (no space before "." after the D.6 completion)
CC_JOIN = {"D.4": " ", "D.6": ""}


def from_user(pid):
    """The user's paragraph in marker form, with the completion in place of its CC bracket."""
    t = USER[pid].replace("chisaki2025 至 kashiwa2024 的 7 篇", ", ".join(JAPAN7))
    if pid in CC:
        ph, txt = CC[pid]
        assert t.count(" " + ph) == 1, pid
        t = t.replace(" " + ph, CC_JOIN[pid] + txt)
    return re.sub(r" \[([a-z0-9_]+(?:, [a-z0-9_]+)*)\]", lambda m: "⟦ref:" + m.group(1).replace(", ", ",") + "⟧", t)


def verbatim(pid, sents):
    built = " ".join(sents)
    want = from_user(pid)
    assert built == want, ("text differs from the instruction", pid, next((i, built[i - 20:i + 20], want[i - 20:i + 20]) for i in range(min(len(built), len(want)))
                                                                         if built[i] != want[i]) if built != want else None)


# ================================================================ Introduction and Methods
INTRO_METHODS = []  # (id, heading(s) before it, sentences) in reading order, from the v5 map
heads_before, pending = {}, []
for o in map5["order"]:
    if o["kind"] == "heading":
        pending.append(o["text"])
    else:
        heads_before[o["id"]] = pending
        pending = []
for x in led_m5["paragraphs"]:
    INTRO_METHODS.append([x["id"], heads_before[x["id"]], list(x["sentences"])])
ROWS5 = {x["id"]: [recheck(r) for r in x["numbers"]] for x in led_m5["paragraphs"]}
IM = {x[0]: x for x in INTRO_METHODS}


def sub_sent(pid, si, a, b, why):
    s = IM[pid][2][si - 1]
    assert s.count(a) == 1, (pid, si, a)
    IM[pid][2][si - 1] = s.replace(a, b)
    LOG.append((pid, "edit", why, s, IM[pid][2][si - 1]))


# section 1, paragraph 1
sub_sent("I.1", 1, "is confined to the first", "is concentrated in the first", "section 1: Introduction paragraph 1, 'is confined to' -> 'is concentrated in'")
# section 1, paragraph 3: the whole paragraph replaced
CUR[0] = "I.3"
I3 = [
    "Economic evaluations of exercise in cancer have valued effects measured in trials, mostly on fatigue, fitness or quality of life during or "
    f"after adjuvant treatment{cite('khan2019', 'gublergut2021', 'wang2023')}, and in breast cancer they reached different conclusions"
    f"{cite('may2017', 'vanwaart2018', 'perrier2020')}.",
    f"No economic evaluation of exercise during neoadjuvant therapy for breast cancer was identified (Supplementary Methods {S['methods_survival']}); "
    f"the nearest, Phys-Can, compared two exercise intensities during neoadjuvant or adjuvant treatment of breast, colorectal or prostate cancer{cite('ax2023')}.",
    "When the effect on recurrence is unknown, a cost-effectiveness ratio cannot be estimated, but the highest program cost that remains cost-effective "
    f"can be calculated for each possible effect{cite('boudewijns2023')}.",
    "Cost-effectiveness analyses of the KEYNOTE-522 regimen come from the United States, Hong Kong, Switzerland and Egypt"
    f"{cite('huang2023', 'kwong2024', 'favrebulle2024', 'pollinger2025')}, whereas the Japanese analyses identified concerned pembrolizumab for advanced "
    f"cancers, including metastatic TNBC{cite(*JAPAN7)}, and as of October "
    f"{N('2026', 'label', 'date of the C2H list consulted (reference c2h_list, cited 2026 Oct 26)')} the regimen had not been designated for Japan's "
    f"cost-effectiveness evaluation{cite('c2h_list')}.",
]
verbatim("I.3", I3)
LOG.append(("I.3", "replace", "section 1: Introduction paragraph 3 replaced by the text of the instruction", " ".join(IM["I.3"][2]), " ".join(I3)))
IM["I.3"][2] = I3
ROWS5["I.3"] = []
# section 1, paragraph 4: the two aims kept, the search and Phys-Can sentences deleted, one sentence added
CUR[0] = "I.4"
old4 = list(IM["I.4"][2])
assert old4[2].startswith("No economic evaluation of exercise") and old4[3].startswith("The nearest, Phys-Can")
I4_3 = ("Expressing the value of an unproven program as the cost a health system can afford for each possible effect gives future trials of exercise "
        "during neoadjuvant therapy a benchmark against which their results can be judged.")
assert I4_3 == USER["I.4 s3"]
IM["I.4"][2] = old4[:2] + [I4_3]
ROWS5["I.4"] = []  # the four numbers of v5 were in the deleted search sentence
LOG.append(("I.4", "edit", "section 1: Introduction paragraph 4, search and Phys-Can sentences deleted (search record moved to Supplementary Methods S1), "
            "closing sentence added", " ".join(old4), " ".join(IM["I.4"][2])))
# section 2: Methods, the multiple-comparison sentence deleted
old8 = list(IM["M.SA.8"][2])
assert old8[0] == "No statistical tests were performed, so no adjustment for multiple comparisons was needed."
IM["M.SA.8"][2] = old8[1:]
LOG.append(("M.SA.8", "edit", "section 2: Methods, multiple-comparison sentence deleted; only the software sentence kept", " ".join(old8), " ".join(IM["M.SA.8"][2])))

# ================================================================ Results (section 3)
def V(reg, where, idx=0):
    rows = [x for x in REGS[reg]["rows"] if x["where"] == where]
    if len(rows) <= idx:
        raise KeyError(f"{reg}: no entry {idx} for {where!r}")
    return rows[idx]


for u in led_r5["used"]:  # every number of the v5 Results is still shown at the same place
    if u.get("source") == "label":
        continue
    assert u["shown"] in {x["shown"] for x in REGS[u["registry"]]["rows"] if x["where"] == u["where"]}, ("value no longer in the registry", u)
RES = copy.deepcopy(RES5)
USED = [dict(u) for u in led_r5["used"]]
SPB, SNB = f"Supplementary Table {S['pathB']}", f"Supplementary Table {S['netbenefit']}"
# P1, last sentence: pathway B at 10 percentage points
p1 = RES[0]
assert p1[-1]["text"] == f"Each further point added about the same amount ({SPB})."
w10 = f"{SPB}, A, pcr 0.100, main base"
vals = {k: V("supplement", w10, i)["shown"] for i, k in enumerate("abc")}
new_s = f"An increase of 10 percentage points gave JPY {vals['a']} thousand (95% UI [{vals['b']}, {vals['c']}]; {SPB})."
LOG.append(("R.1", "edit", "section 3: pathway B, the maximum affordable cost and 95% UI at an increase in pCR of 10 percentage points (Supplementary Table S5)",
            p1[-1]["text"], new_s))
p1[-1] = dict(text=new_s, cites=[SPB], keys=list("abc"), origin="new in v6")
si = len(p1)
assert not [u for u in USED if u["paragraph"] == 1 and u["sentence"] == si]
for i, k in enumerate("abc"):
    x = V("supplement", w10, i)
    USED.append(dict(paragraph=1, sentence=si, placeholder=k, registry="supplement", where=w10, shown=x["shown"], source=x["source"], loc=x["loc"]))
r10 = [x for x in REGS["supplement"]["rows"] if x["where"] == f"{SPB}, row label" and x["shown"] == "10"]
assert r10
USED.append(dict(paragraph=1, sentence=si, placeholder="10", registry="supplement", where=f"{SPB}, row label", shown="10", source=r10[0]["source"], loc=r10[0]["loc"]))
# P5, first sentence: the patients of the net benefit
p5 = RES[4]
a5 = "the net benefit for the 3,451 patients a year in Japan who would be eligible"
b5 = "the net benefit for the 3,451 patients registered in 2024 who received neoadjuvant chemotherapy for stage II or III TNBC"
assert p5[0]["text"].count(a5) == 1
before = p5[0]["text"]
p5[0] = dict(p5[0], text=before.replace(a5, b5), origin=p5[0]["origin"] + "; edited in v6")
LOG.append(("R.5", "edit", "section 3: the patients of the net benefit (registered in 2024, neoadjuvant chemotherapy, stage II or III TNBC)", before, p5[0]["text"]))
lab24 = [x for x in REGS["supplement"]["labels"] if x["where"] == SNB and x["shown"] == "2024"]
assert lab24
USED.append(dict(paragraph=5, sentence=1, placeholder="2024", registry="supplement", where=SNB, shown="2024", source="label", loc=lab24[0]["reason"]))

# ================================================================ Discussion, Implications, Limitations (section 5)
T1, T2, T3 = "Table 1", "Table 2", "Table 3"
NEW = []  # (id, heading or None, sentences)


def para_new(pid, head, sents):
    verbatim(pid, sents)
    NEW.append((pid, head, sents))


CUR[0] = "D.1"
para_new("D.1", "Discussion", [
    "The value of adding a structured exercise program to neoadjuvant chemotherapy for stage II or III TNBC in Japan depends on how much and for how "
    "long the program lowers the risk of recurrence.",
    f"With chemotherapy plus pembrolizumab, a program could cost up to JPY {N('2,726', 'reg', 'tables', 'Table 2, Panel B, base case, main')} thousand "
    f"per patient at a recurrence HR of {N('0.85', 'reg', 'tables', 'Table 2, Panels B and C row label')} and remain cost-effective ({T2}).",
    f"The most expensive design costed in this study was JPY {N('239,508', 'reg', 'tables', 'Table 1, exercise program')} ({T1}).",
    f"A reduction of {N('1.1', 'reg', 'tables', 'Table 2, Panel A, cap = E02, main, reduction %')}% in the recurrence hazard was enough for the "
    f"fee-schedule-based program to be cost-effective, and a reduction of {N('4.2', 'reg', 'tables', 'Table 2, Panel A, avoided = E02, main, reduction %')}% "
    f"to {N('8.6', 'reg', 'tables', 'Table 2, Panel C, eri, avoided = E02, main, reduction %')}% was enough for it to lower total medical costs ({T2}).",
    "For patients in Japan, what remains unknown is whether exercise lowers recurrence at all, and for how long.",
])
CUR[0] = "D.2"
para_new("D.2", None, [
    "Most of this value comes from distant recurrences that the program would prevent.",
    f"Treatment after distant recurrence in Japan now costs JPY {N('1,215,933', 'reg', 'tables', 'Table 1, first-line treatment')} to "
    f"{N('1,458,318', 'reg', 'tables', 'Table 1, first-line treatment')} per month in first-line treatment and JPY "
    f"{N('1,412,953', 'reg', 'tables', 'Table 1, second-line treatment')} per month in later lines ({T1}).",
    f"Medical costs avoided made up JPY {N('702', 'regneg', 'supplement', 'Supplementary Table ' + S['decomp'] + ', total_without_programme, d_base')} thousand "
    f"of the maximum affordable cost at an HR of {N('0.85', 'reg', 'supplement', 'Supplementary Table ' + S['decomp'])} (Supplementary Table {S['decomp']}).",
    "Lower metastatic treatment costs reduced these savings but left the threshold for cost-effectiveness almost unchanged.",
    f"With these costs halved, or with eribulin-based later-line treatment, the break-even HR was {N('0.988', 'reg', 'tables', 'Table 2, Panel C, m50, cap = E02, main')} "
    f"and {N('0.987', 'reg', 'tables', 'Table 2, Panel C, eri, cap = E02, main')}, while the HR at which exercise lowered total costs fell to "
    f"{N('0.918', 'reg', 'tables', 'Table 2, Panel C, m50, avoided = E02, main')} and {N('0.914', 'reg', 'tables', 'Table 2, Panel C, eri, avoided = E02, main')} ({T2}).",
])
# "no input moved this cost outside JPY 2,617 thousand to 2,836 thousand": the bounds of every input of Fig. 3 (values in Supplementary Table S9)
S9 = f"Supplementary Table {S['oneway']}"
caps9 = [x for x in REGS["supplement"]["rows"] if x["where"].startswith(S9 + ", ") and re.search(r", cap_(low|high)$", x["where"])]
lo9, hi9 = min(caps9, key=lambda x: float(x["raw"])), max(caps9, key=lambda x: float(x["raw"]))
assert (lo9["where"], lo9["shown"], hi9["where"], hi9["shown"]) == (f"{S9}, D05, cap_low", "2,617", f"{S9}, D05, cap_high", "2,836"), (lo9, hi9)
FIG3_RANGE = dict(inputs_x_bounds=len(caps9), lowest=(lo9["where"], lo9["shown"], lo9["raw"]), highest=(hi9["where"], hi9["shown"], hi9["raw"]))
CUR[0] = "D.3"
para_new("D.3", None, [
    "How long the effect lasts changed the result more than any single cost.",
    f"If the effect faded from {N('1', 'reg', 'tables', 'Table 1, effect duration')} year after surgery, the maximum affordable cost at an HR of "
    f"{N('0.85', 'reg', 'tables', 'Table 2, Panels B and C row label')} fell to JPY {N('1,772', 'reg', 'tables', 'Table 2, Panel B, dur1, main')} thousand, "
    f"and if it did not wane, it rose to JPY {N('3,404', 'reg', 'tables', 'Table 2, Panel B, dur2, main')} thousand ({T2}).",
    f"In the one-way analyses, no input moved this cost outside JPY {N('2,617', 'reg', 'supplement', S9 + ', D05, cap_low')} thousand to "
    f"{N('2,836', 'reg', 'supplement', S9 + ', D05, cap_high')} thousand (Fig. 3).",
    f"After neoadjuvant chemo-immunotherapy, most recurrences occur within {N('24', 'lit', 'licata2025')} months of randomization{cite('licata2025')}, "
    "so an effect that lasts through the first years after surgery carries most of the value.",
    f"Continuing exercise after surgery raised the maximum affordable cost when the effect would otherwise have faded early (Supplementary Table {S['duration']}).",
])
CUR[0] = "D.4"
para_new("D.4", None, [
    f"For pembrolizumab, the ICER of JPY {N('2,053', 'reg', 'tables', 'Table 3, base, ICER')} thousand per QALY lay below both Japanese thresholds ({T3}).",
    "Analyses of the same regimen from the United States, Hong Kong, Switzerland and Egypt"
    f"{cite('huang2023', 'kwong2024', 'favrebulle2024', 'pollinger2025')} found it cost-effective, with ICERs below the threshold used in each setting.",
    f"In Japan, the regimen has not been designated for cost-effectiveness evaluation{cite('c2h_list')}.",
    f"Its ICER rose to JPY {N('3,044', 'reg', 'tables', 'Table 3, sjp, ICER')} thousand per QALY when capecitabine or olaparib was added after surgery "
    f"for patients without pCR, as in Japanese practice, and fell to JPY {N('1,296', 'reg', 'supplement', S9 + ', A03, icer_low')} thousand at "
    f"{N('75', 'reg', 'supplement', 'supplementary figure legends')}% of the list price of pembrolizumab ({T3}; Supplementary Fig. {S['fig_icer']}).",
])
CUR[0] = "D.5"
para_new("D.5", None, [
    "Exercise cannot stand in for pembrolizumab.",
    f"To gain as many QALYs as pembrolizumab, exercise added to chemotherapy alone would need a recurrence HR of {N('0.425', 'reg', 'tables', 'Table 3, Panel C, HR')} "
    f"({T3}), a far larger effect than has been reported for exercise in other settings{cite('courneya2025', 'courneya2014')}.",
    f"The maximum affordable cost was higher when exercise was added to chemotherapy alone ({T2}), because more recurrences remain for exercise to prevent "
    "without pembrolizumab.",
    f"Exercise is therefore best judged as an addition to the standard regimen, which in Japan was given to {N('2,294', 'csv', JB, 'nac_pembro')} of "
    f"{N('3,451', 'csv', JB, 'nac_total')} patients in {N('2024', 'doc', JB, '（2024 年）')}{cite('jbcs55')}.",
])
CUR[0] = "D.6"
para_new("D.6", None, [
    "Previous economic evaluations of exercise in cancer valued effects on fatigue, fitness or quality of life during or shortly after treatment"
    f"{cite('khan2019', 'gublergut2021', 'wang2023')}.",
    f"The cost-utility analysis of CHALLENGE valued an effect on disease-free survival over the long term{cite('chan2026')}.",
    "The structured exercise program was less costly and more effective than health education materials, and cancer recurrence or new malignancy and "
    f"anticancer therapy were the major cost drivers{cite('chan2026')}.",
    "Our results agree with it on the main point: once a program changes the risk of recurrence, its value reflects the cost and the loss of health that "
    "each prevented recurrence avoids, and both are large relative to the cost of the program.",
    f"Headroom analysis is used to judge technologies before their effect is known{cite('boudewijns2023')}.",
    "Here it shows that an effect far smaller than a trial could detect would still pay for the program.",
])
CUR[0] = "D.7"
para_new("D.7", None, [
    "In Japanese practice, the value of a given effect may be larger than modeled.",
    f"In the {N('2024', 'doc', JB, '（2024 年）')} national registry, {N('47', 'csvpct', JB, 'pcr_registry', 0)}% of patients treated with neoadjuvant "
    f"chemotherapy had a pCR{cite('jbcs55')}, fewer than in either arm of KEYNOTE-522 ({N('63.0', 'reg', 'tables', 'Table 1, pCR')}% and "
    f"{N('55.6', 'reg', 'tables', 'Table 1, pCR')}%; {T1}).",
    "More patients therefore carry residual disease and the higher risk of recurrence on which exercise would act.",
    f"Even at an HR of {N('0.95', 'reg', 'supplement', SNB)}, the net benefit for one year of Japanese patients would be JPY "
    f"{N('2.68', 'reg', 'supplement', SNB + ', B, main base 0.95')} billion ({SNB}).",
])
CUR[0] = "IMP.1"
para_new("IMP.1", "Implications", [
    "Trials of exercise during neoadjuvant chemotherapy for TNBC should measure recurrence and follow patients long enough to show whether any effect "
    "persists after the program ends.",
    "A higher pCR would help but cannot settle the question alone.",
    f"In this model, {N('1', 'reg', 'supplement', SPB + ', row label')} percentage point more pCR was worth JPY "
    f"{N('389', 'reg', 'supplement', SPB + ', A, pcr 0.010, main base')} thousand per patient ({SPB}), but how a change in pCR caused by exercise would "
    "translate into fewer recurrences is unknown.",
    f"Given the net benefit at stake for each year of patients in Japan ({SNB}), such trials are a sound use of research funds.",
    "For payers, the fee-schedule price of a supervised program is far below what a confirmed effect would justify, and support that keeps patients "
    "exercising after surgery, such as remote or app-based programs, would add value if it extends the effect "
    f"(Supplementary Table {S['duration']}).",
    "For pembrolizumab, the analysis provides a Japanese estimate for a regimen that has not been designated for cost-effectiveness evaluation.",
])
CUR[0] = "L.1"
para_new("L.1", "Limitations", [
    "The effect of exercise during neoadjuvant chemotherapy on recurrence is unknown, so all results for exercise are conditional on an assumed HR and "
    "duration of effect.",
    f"The CHALLENGE estimate used as a reference comes from a {N('3', 'reg', 'tables', 'Table 1, reference value')}-year program after adjuvant "
    "chemotherapy for colon cancer.",
    "The model credited exercise only with fewer recurrences after surgery; effects on fatigue, quality of life or completion of chemotherapy were not "
    "counted, so the maximum affordable cost may be understated.",
    "Survival was modeled from patient-level data reconstructed from published curves, and the "
    f"{N('7', 'reg', 'supplement', 'Supplementary Methods ' + S['methods_survival'])}-year event-free survival by pCR status came from the presentation "
    "of the final analysis rather than a full report.",
    "Survival after distant recurrence came from a French cohort treated largely before immunotherapy and antibody–drug conjugates were available, "
    f"whereas treatment costs reflect regimens used in {N('2026', 'reg', 'tables', 'Table 1, prices')}.",
    "Several costs relied on clinical expert input, and ranges were set by rule where sources gave none (Fig. 3).",
    f"Utilities used the German value set; values from Japanese populations gave similar results (Supplementary Table {S['other']}).",
    "The number of eligible patients came from a registry that does not capture every case.",
])
for pid, head, sents in NEW:
    LOG.append((pid, "new", "section 5: inserted as given" + ("; CC sentence completed from the abstracts" if pid in CC else ""), "", " ".join(sents)))

# ================================================================ docx
body_ps = allp[:i_ref]
by_id = {}
for o, p in zip(map5["order"], body_ps):
    if o["id"]:
        by_id[o["id"]] = p


def set_text(p, text):
    """One run with the format of the paragraph's first run (number_refs.py splits it at the markers)."""
    runs = p._p.findall(qn("w:r"))
    keep = runs[0]
    for r in runs[1:]:
        p._p.remove(r)
    t = keep.find(qn("w:t"))
    t.text = text
    t.set(qn("xml:space"), "preserve")
    assert keep.find(qn("w:rPr")).find(qn("w:vertAlign")) is None


for pid, _, sents in INTRO_METHODS:
    set_text(by_id[pid], " ".join(sents))
for i, ps in enumerate(RES, start=1):
    set_text(by_id[f"R.{i}"], " ".join(s["text"] for s in ps))
for p in allp[i_ref:]:  # the reference list of v5 (number_refs.py writes the list of v6)
    p._p.getparent().remove(p._p)
HEAD = copy.deepcopy(next(p for p in body_ps if p.text == "Results")._p)
BODY = copy.deepcopy(by_id["R.10"]._p)


def clone(tmpl, text):
    el = copy.deepcopy(tmpl)
    runs = el.findall(qn("w:r"))
    for r in runs[1:]:
        el.remove(r)
    t = runs[0].find(qn("w:t"))
    t.text = text
    t.set(qn("xml:space"), "preserve")
    return el


anchor = by_id["R.10"]._p
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
for o in map5["order"]:
    if o["kind"] == "heading":
        order.append(dict(id=None, kind="heading", text=o["text"]))
    elif o["id"].startswith("R."):
        order.append(dict(id=o["id"], kind="body", text=" ".join(s["text"] for s in RES[int(o["id"][2:]) - 1])))
    else:
        order.append(dict(id=o["id"], kind="body", text=" ".join(IM[o["id"]][2])))
for pid, head, sents in NEW:
    if head:
        order.append(dict(id=None, kind="heading", text=head))
    order.append(dict(id=pid, kind="body", text=" ".join(sents)))
# the saved docx must read back as the map (heading and body paragraphs in order)
chk = [p for p in Document(out).paragraphs if p.text.strip()]
assert [p.text for p in chk] == [o["text"] for o in order], "manuscript_marked.docx does not read back as the paragraph map"

rows_all = []
for pid, _, _ in INTRO_METHODS:
    rows_all += ROWS5[pid] if pid not in ("I.3",) else []
rows_all += MROWS  # I.3 and the new paragraphs
for r in rows_all:
    assert r["where"] in {o["id"] for o in order if o["id"]}
secs = [dict(id=pid, sentences=sents, numbers=[r for r in rows_all if r["where"] == pid]) for pid, _, sents in INTRO_METHODS] + \
       [dict(id=pid, sentences=sents, numbers=[r for r in rows_all if r["where"] == pid]) for pid, _, sents in NEW]
json.dump({"paragraphs": secs, "rows": rows_all, "fig3_range_check": FIG3_RANGE, "cc": {k: v[1] for k, v in CC.items()}},
          open(BUILD / "_ledger_manuscript.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
led = {"paragraphs": RES, "used": USED, "base": f"manuscript_{PREV}.docx", "edits": [dict(zip(("paragraph", "kind", "reason", "before", "after"), x)) for x in LOG]}
for name in ("_ledger_results.json", f"_ledger_results_{VER}.json"):
    json.dump(led, open(BUILD / name, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"version": VER, "ids": [o["id"] for o in order if o["id"]], "order": order, "manuscript_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
           "edits": [dict(zip(("paragraph", "kind", "reason", "before", "after"), x)) for x in LOG]},
          open(BUILD / "_manuscript_map.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# every number of a non-Results paragraph must be registered for it
strip = lambda t: MARK_RE.sub("", re.sub(r"\b(?:Supplementary )?(?:Tables?|Figs?\.|Methods) S?\d+[a-z]?(?:\s*(?:and|to|,)\s*S?\d+)*", " ", t))
bad = []
for x in secs:
    reg = {r["shown"] for r in x["numbers"]}
    for s in x["sentences"]:
        for t in num_tokens(strip(s)):
            if t not in reg:
                bad.append((x["id"], t, s[:60]))
assert not bad, bad


def words(t):
    return len(MARK_RE.sub("", t).split())


print("manuscript_marked.docx written from", SRC.name)
for x in secs:
    w = [words(s) for s in x["sentences"]]
    print(f"  {x['id']}: {sum(w)} words, longest sentence {max(w)}, numbers {len(x['numbers'])}")
for i, ps in enumerate(RES, start=1):
    w = [len(s["text"].split()) for s in ps]
    print(f"  R.{i}: {sum(w)} words, longest sentence {max(w)}")
print("edits:", len(LOG), "| Fig. 3 range check:", FIG3_RANGE)
