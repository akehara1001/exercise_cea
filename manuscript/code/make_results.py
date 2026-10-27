"""Results section, first version (results_v3.docx).

Every number in the text is taken from the registries of the tables, the
supplement and the figures (the value shown in a cell), so the text and the
tables carry the same value with the same digits. Writes results_<VER>.docx and
_build/_ledger_results.json (sentence -> cited tables -> cells).

WRITING_RULES 1.2 rule 2: this script writes the first version of the Results
only. Later versions are made by editing results_<VER>.docx directly.
"""
from __future__ import annotations

import json
import re
import sys

from docx.enum.text import WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from common import BUILD, OUT, VER
from docx_util import add_runs, new_document

sys.stdout.reconfigure(encoding="utf-8")
if VER != "v3":
    raise SystemExit("make_results.py writes only the first version (v3); edit the previous results docx directly")

REGS = {name: json.load(open(BUILD / f"_ledger_{name}.json", encoding="utf-8")) for name in ("tables", "supplement", "figures")}
USED = []  # (paragraph, sentence, placeholder, registry, where, shown)


def V(reg, where, idx=0):
    rows = [x for x in REGS[reg]["rows"] if x["where"] == where]
    if len(rows) <= idx:
        raise KeyError(f"{reg}: no entry {idx} for {where!r}")
    return rows[idx]


def rng(reg, pattern):
    """Smallest and largest shown value among entries whose where matches pattern (HR-type values)."""
    rows = [x for x in REGS[reg]["rows"] if re.fullmatch(pattern, x["where"])]
    vals = sorted(rows, key=lambda x: float(x["shown"].replace("−", "-").replace(",", "")))
    return vals[0], vals[-1]


T2A, T2B, T2C = "Table 2, Panel A", "Table 2, Panel B", "Table 2, Panel C"
BASE_M = f"{T2B}, base case, main (intended repeat of Supplementary Table S4)"
BASE_S = f"{T2B}, base case, secondary (intended repeat of Supplementary Table S4)"
S4 = "Supplementary Table S4, A, hr0"
lo_cap, hi_cap = rng("supplement", r"Supplementary Table S10, [a-z_]+, main, cap_eq_programme")

# Each sentence: (text with {k} placeholders, {k: (registry, where, idx)}, cited tables or figures)
P = [
    [("Fig. 2a shows that the maximum affordable cost of an exercise program per patient, in Japanese yen (JPY), rose as the recurrence hazard ratio (HR) with exercise fell.",
      {}, ["Fig. 2"]),
     ("Added to chemotherapy plus pembrolizumab, exercise had a maximum affordable cost of JPY {a} thousand per patient at an HR of 0.85 (Table 2).",
      {"a": ("tables", BASE_M, 0)}, ["Table 2"]),
     ("Its 95% uncertainty interval (UI) was [{b}, {c}] (Table 2).",
      {"b": ("tables", BASE_M, 1), "c": ("tables", BASE_M, 2)}, ["Table 2"]),
     ("At an HR of 0.70, it was JPY {a} thousand (95% UI [{b}, {c}]; Supplementary Table S4).",
      {"a": ("supplement", f"{S4} 0.700, main base", 0), "b": ("supplement", f"{S4} 0.700, main base", 1), "c": ("supplement", f"{S4} 0.700, main base", 2)},
      ["Supplementary Table S4", "Table 1"]),
     ("Table 2 (panel A) shows that the maximum affordable cost equaled the cost of the fee-schedule-based program at an HR of {a}, a {b}% reduction in the recurrence hazard.",
      {"a": ("tables", f"{T2A}, cap = E02, main", 0), "b": ("tables", f"{T2A}, cap = E02, main, reduction %", 0)}, ["Table 2"]),
     ("Medical costs avoided by exercise equaled the same program cost at an HR of {a}, a {b}% reduction (Table 2).",
      {"a": ("tables", f"{T2A}, avoided = E02, main", 0), "b": ("tables", f"{T2A}, avoided = E02, main, reduction %", 0)}, ["Table 2"])],
    [("Supplementary Table S5 shows the incremental costs by category for exercise added to chemotherapy plus pembrolizumab at an HR of 0.85.", {}, ["Supplementary Table S5", "Table 2"]),
     ("Incremental medical costs other than the program cost were JPY {a} thousand per patient (Supplementary Table S5).",
      {"a": ("supplement", "Supplementary Table S5, total_without_programme, d_base", 0)}, ["Supplementary Table S5"]),
     ("Second-line and later treatment of distant recurrence contributed JPY {a} thousand (Supplementary Table S5).",
      {"a": ("supplement", "Supplementary Table S5, dr_later_lines, d_base", 0)}, ["Supplementary Table S5"]),
     ("First-line treatment of distant recurrence contributed JPY {a} thousand (Supplementary Table S5).",
      {"a": ("supplement", "Supplementary Table S5, dr_first_line, d_base", 0)}, ["Supplementary Table S5"])],
    [("Table 2 (panel B) shows that the maximum affordable cost at an HR of 0.85 depended on how long the effect lasted.", {}, ["Table 2"]),
     ("It was JPY {a} thousand when the effect lasted until 1 year after surgery, against JPY {b} thousand in the base case (Table 2).",
      {"a": ("tables", f"{T2B}, dur1, main", 0), "b": ("tables", BASE_M, 0)}, ["Table 2"]),
     ("It was JPY {a} thousand when the effect did not wane (Table 2; Supplementary Table S6).",
      {"a": ("tables", f"{T2B}, dur2, main", 0)}, ["Table 2", "Supplementary Table S6"])],
    [("Table 2 (panel C) shows that, with metastatic treatment costs halved, medical costs avoided equaled the cost of the fee-schedule-based program at an HR of {a}, an {b}% reduction.",
      {"a": ("tables", f"{T2C}, m50, avoided = E02, main", 0), "b": ("tables", f"{T2C}, m50, avoided = E02, main, reduction %", 0)}, ["Table 2"]),
     ("With eribulin-based later-line treatment, this HR was {a}, an {b}% reduction (Table 2).",
      {"a": ("tables", f"{T2C}, eri, avoided = E02, main", 0), "b": ("tables", f"{T2C}, eri, avoided = E02, main, reduction %", 0)}, ["Table 2"]),
     ("The HR at which the maximum affordable cost equaled the program cost was {a} with metastatic treatment costs halved and {b} with eribulin-based treatment (Table 2).",
      {"a": ("tables", f"{T2C}, m50, cap = E02, main", 0), "b": ("tables", f"{T2C}, eri, cap = E02, main", 0)}, ["Table 2"]),
     ("The reductions of {a}% to {b}% at which medical costs avoided equaled the program cost held only for exercise added to chemotherapy plus pembrolizumab "
      "with the fee-schedule-based program (Table 2).",
      {"a": ("tables", f"{T2A}, avoided = E02, main, reduction %", 0), "b": ("tables", f"{T2C}, eri, avoided = E02, main, reduction %", 0)}, ["Table 2"])],
    [("Supplementary Table S7 shows the net benefit for the {n} patients a year in Japan who would be eligible, if exercise reduced the recurrence hazard.",
      {"n": ("supplement", "Supplementary Table S7, header", 0)}, ["Supplementary Table S7"]),
     ("At an HR of 0.95, the net benefit for one year of patients was JPY {a} billion (95% UI [{b}, {c}]; Supplementary Table S7).",
      {"a": ("supplement", "Supplementary Table S7, B, main base 0.95", 0), "b": ("supplement", "Supplementary Table S7, B, main base 0.95", 1),
       "c": ("supplement", "Supplementary Table S7, B, main base 0.95", 2)}, ["Supplementary Table S7"]),
     ("At an HR of 0.85, it was JPY {a} billion (95% UI [{b}, {c}]; Supplementary Table S7).",
      {"a": ("supplement", "Supplementary Table S7, B, main base 0.85", 0), "b": ("supplement", "Supplementary Table S7, B, main base 0.85", 1),
       "c": ("supplement", "Supplementary Table S7, B, main base 0.85", 2)}, ["Supplementary Table S7"])],
    [("Fig. 2 and Table 2 also show exercise added to chemotherapy alone.", {}, ["Fig. 2", "Table 2"]),
     ("Its maximum affordable cost at an HR of 0.85 was JPY {a} thousand per patient (95% UI [{b}, {c}]; Table 2).",
      {"a": ("tables", BASE_S, 0), "b": ("tables", BASE_S, 1), "c": ("tables", BASE_S, 2)}, ["Table 2"]),
     ("This cost equaled the cost of the fee-schedule-based program at an HR of {a}, a {b}% reduction in the recurrence hazard (Table 2).",
      {"a": ("tables", f"{T2A}, cap = E02, secondary", 0), "b": ("tables", f"{T2A}, cap = E02, secondary, reduction %", 0)}, ["Table 2"]),
     ("Medical costs avoided equaled the program cost at an HR of {a}, a {b}% reduction (Table 2).",
      {"a": ("tables", f"{T2A}, avoided = E02, secondary", 0), "b": ("tables", f"{T2A}, avoided = E02, secondary, reduction %", 0)}, ["Table 2"])],
    [("Table 3 shows the costs, quality-adjusted life years (QALYs) and cost-effectiveness of pembrolizumab added to neoadjuvant chemotherapy.", {}, ["Table 3"]),
     ("In the base case, pembrolizumab added JPY {a} thousand per patient in costs (95% UI [{b}, {c}]; Table 3).",
      {"a": ("tables", "Table 3, base, total", 0), "b": ("tables", "Table 3, base, total", 1), "c": ("tables", "Table 3, base, total", 2)}, ["Table 3"]),
     ("It added {a} QALYs (95% UI [{b}, {c}]; Table 3).",
      {"a": ("tables", "Table 3, base, QALY", 0), "b": ("tables", "Table 3, base, QALY", 1), "c": ("tables", "Table 3, base, QALY", 2)}, ["Table 3"]),
     ("The pembrolizumab drug cost was JPY {a} thousand (Table 3).",
      {"a": ("tables", "Table 3, Panel A, pembrolizumab_drug, base", 0)}, ["Table 3"]),
     ("Second-line and later treatment of distant recurrence contributed JPY {a} thousand (Table 3).",
      {"a": ("tables", "Table 3, Panel A, dr_later_lines, base", 0)}, ["Table 3"]),
     ("The incremental cost-effectiveness ratio (ICER) was JPY {a} thousand per QALY (Table 3).",
      {"a": ("tables", "Table 3, base, ICER", 0)}, ["Table 3"]),
     ("The probability that pembrolizumab was cost-effective was {a}% at JPY 5 million per QALY and {b}% at JPY 7.5 million per QALY (Table 3).",
      {"a": ("tables", "Table 3, base, P(CE) 5M", 0), "b": ("tables", "Table 3, base, P(CE) 7.5M", 0)}, ["Table 3"])],
    [("Table 3 also shows that the ICER was JPY {a} thousand per QALY with Japanese post-operative treatment.",
      {"a": ("tables", "Table 3, sjp, ICER", 0)}, ["Table 3"]),
     ("It was JPY {a} thousand with metastatic treatment costs halved and JPY {b} thousand with eribulin-based later-line treatment (Table 3).",
      {"a": ("tables", "Table 3, m50, ICER", 0), "b": ("tables", "Table 3, eri, ICER", 0)}, ["Table 3"]),
     ("It was JPY {a} thousand with higher mortality after early recurrence with pembrolizumab (Table 3).",
      {"a": ("tables", "Table 3, kext, ICER", 0)}, ["Table 3"])],
    [("Table 3 (panel C) shows the exercise effect at which exercise added to chemotherapy alone would gain as many QALYs as pembrolizumab.", {}, ["Table 3"]),
     ("This required a recurrence HR of {a} (Table 3).", {"a": ("tables", "Table 3, Panel C, HR", 0)}, ["Table 3"]),
     ("Through an effect on pathological complete response (pCR), it required an increase in pCR of {a} percentage points (Table 3).",
      {"a": ("tables", "Table 3, Panel C, pCR", 0)}, ["Table 3"]),
     ("Both values lay outside the ranges studied (Supplementary Tables S4 and S8).", {}, ["Supplementary Table S4", "Supplementary Table S8"])],
    [("Fig. 3 shows the one-way sensitivity analysis of the maximum affordable cost for exercise added to chemotherapy plus pembrolizumab at an HR of 0.85 (Supplementary Table S9).",
      {}, ["Fig. 3", "Supplementary Table S9", "Table 2"]),
     ("The monthly cost of second-line and later treatment moved this cost most, from JPY {a} thousand at its lower bound to JPY {b} thousand at its upper bound (Fig. 3).",
      {"a": ("supplement", "Supplementary Table S9, D05, cap_low", 0), "b": ("supplement", "Supplementary Table S9, D05, cap_high", 0)}, ["Fig. 3", "Supplementary Table S9"]),
     ("Supplementary Fig. S2 shows that the pembrolizumab drug cost moved the ICER most, to JPY {a} thousand per QALY at its lower bound.",
      {"a": ("supplement", "Supplementary Table S9, A03, icer_low", 0)}, ["Supplementary Fig. S2", "Supplementary Table S9"]),
     ("Supplementary Table S10 shows that, with utility values from Japanese populations, the maximum affordable cost at an HR of 0.85 was JPY {a} thousand.",
      {"a": ("supplement", "Supplementary Table S10, utility_jp, main, cap 0.85", 0)}, ["Supplementary Table S10", "Table 2"]),
     ("Across the six scenarios in this table, the HR at which the maximum affordable cost equaled the cost of the fee-schedule-based program ranged from {a} to {b} (Supplementary Table S10).",
      {"a": ("supplement", lo_cap["where"], 0), "b": ("supplement", hi_cap["where"], 0)}, ["Supplementary Table S10"])],
]

# render, record every placeholder
paras = []
for pi, sents in enumerate(P, start=1):
    out = []
    for si, (tpl, keys, cites) in enumerate(sents, start=1):
        vals = {}
        for k, (reg, where, idx) in keys.items():
            e = V(reg, where, idx)
            vals[k] = e["shown"]
            USED.append(dict(paragraph=pi, sentence=si, placeholder=k, registry=reg, where=where, shown=e["shown"], source=e["source"], loc=e["loc"]))
        txt = tpl.format(**vals)
        out.append(dict(text=txt, cites=cites, keys=list(keys)))
    paras.append(out)

doc = new_document(landscape=False)
sect = doc.sections[0]
ln = OxmlElement("w:lnNumType")
ln.set(qn("w:countBy"), "1")
ln.set(qn("w:restart"), "continuous")
sect._sectPr.append(ln)


def body_para(text, bold=False):
    p = doc.add_paragraph()
    add_runs(p, text, bold=bold)
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    return p


body_para("Results", bold=True)
for sents in paras:
    body_para(" ".join(s["text"] for s in sents))
doc.save(OUT / f"results_{VER}.docx")
json.dump({"paragraphs": paras, "used": USED}, open(BUILD / "_ledger_results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
words = sum(len(s["text"].split()) for sents in paras for s in sents)
print(f"results_{VER}.docx written; paragraphs {len(paras)}, sentences {sum(len(x) for x in paras)}, words {words}, numbers {len(USED)}")
