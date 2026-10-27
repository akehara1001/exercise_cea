"""Manuscript v5: Introduction and Methods added to the Results of v4, and the Results edits of v5.

Direct edit of manuscript/archive/v4/results_v4.docx (WRITING_RULES 1.2 rule 2): the ten
Results paragraphs of v4 are kept and changed only where RESULTS lists an edit
(instruction "执笔第 3 步（v5）" section 2, and the supplementary renumbering of
section 1), and the Introduction and Methods (sections 3 and 4) are inserted before
them as new paragraphs with the formatting of the existing ones. Every number is a
value shown in a table or figure (registries in _build), a number printed in the
abstract of the cited source, a model setting written in a project file, or a date,
and is recorded with its source. Citations are markers (references.cite) that
number_refs.py numbers in reading order. Runs for v5 only; later versions edit
manuscript_v5.docx directly.

Writes _build/manuscript_marked.docx, _build/_ledger_results.json (and a _v5 copy),
_build/_ledger_manuscript.json and _build/_manuscript_map.json.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys

from docx import Document
from docx.oxml.ns import qn

from common import ARCHIVE_PREV, BUILD, PREV, ROOT, SUPP, SUPP_RENUMBER_V4_V5, VER, fnum, num_tokens
from references import MARK_RE, PUBMED, cite

sys.stdout.reconfigure(encoding="utf-8")
if VER != "v5":
    raise SystemExit("edit_manuscript.py holds the edits of v5 only; write the next version's edits on manuscript_v5.docx")

REGS = {name: json.load(open(BUILD / f"_ledger_{name}.json", encoding="utf-8")) for name in ("tables", "supplement", "figures", "suppfigs")}
base = json.load(open(BUILD / f"_ledger_results_{PREV}.json", encoding="utf-8"))
S = SUPP  # short alias for the supplementary labels used in the text


# ================================================================ numbers of the Introduction and Methods
MROWS: list[dict] = []
CUR = [None]


def _line(path, needle):
    for i, ln in enumerate((ROOT / path).read_text(encoding="utf-8").splitlines(), start=1):
        if needle in ln:
            return i, ln
    raise ValueError(f"{needle!r} not found in {path}")


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
        rows = [x for x in REGS[reg]["rows"] + REGS[reg]["labels"] if x["where"].startswith(prefix) and x["shown"] == tok]
        assert rows, (tok, reg, prefix)
        src, loc = f"_ledger_{reg}.json", f"{rows[0]['where']} ({rows[0].get('source', rows[0].get('reason', ''))})"
    elif kind == "csv":  # value of the registry file of Japanese patient numbers
        path, item = a
        import pandas as pd
        v = pd.read_csv(ROOT / path).set_index("item").loc[item, "value"]
        assert fnum(float(v), 0) == tok, (tok, v)
        src, loc = path, f"item = {item}, value"
    elif kind == "label":  # name or definition, reason given
        (why,) = a
        src, loc = "definition", why
    else:
        raise ValueError(kind)
    MROWS.append(dict(shown=tok, where=CUR[0], source=src, loc=loc))
    return tok


MS, AP, P1R = "docs/model_spec.md", "docs/analysis_plan_phase2.md", "output/phase1/phase1_report.md"
SDUR = f"Supplementary Table {S['duration']}"
STAGE = "number of the analysis stage (Statistical analysis)"
NOV = "manuscript/code/refs/searches/search_novelty.json"
INTRO, METHODS = [], []  # (paragraph id, heading before it or None, [sentences])

# ---------------------------------------------------------------- Introduction (section 4)
CUR[0] = "I.1"
INTRO.append(("I.1", "Introduction", [
    "Triple-negative breast cancer (TNBC) recurs more often than other breast cancers, and its excess risk of distant recurrence is confined to the "
    f"first {N('5', 'lit', 'dent2007')} years after diagnosis{cite('dent2007')}.",
    "After neoadjuvant chemotherapy, patients with TNBC and residual disease have worse survival than those with a pathological complete response "
    f"(pCR){cite('liedtke2008')}.",
    "In the KEYNOTE-522 trial of stage II or III TNBC, adding pembrolizumab to neoadjuvant chemotherapy and continuing it after surgery increased pCR "
    f"and prolonged event-free and overall survival{cite('schmid2020', 'schmid2022', 'schmid2024')}.",
    f"After this regimen, most recurrences still occur within {N('24', 'lit', 'licata2025')} months of randomization{cite('licata2025')}.",
    f"In Japan, {N('2,294', 'csv', 'input/params/cohort_N_jbcs2024.csv', 'nac_pembro')} of the {N('3,451', 'csv', 'input/params/cohort_N_jbcs2024.csv', 'nac_total')} "
    f"patients who received neoadjuvant chemotherapy for stage II or III TNBC in {N('2024', 'doc', 'input/params/cohort_N_jbcs2024.csv', '（2024 年）')} "
    f"also received pembrolizumab{cite('jbcs55')}.",
    f"Pembrolizumab is given in eight doses before surgery and up to nine after{cite('schmid2020')}, and one dose costs "
    f"{N('398,924', 'reg', 'tables', 'Table 1, pembrolizumab')} Japanese yen (JPY) at the {N('2026', 'reg', 'tables', 'Table 1, prices')} list price{cite('price2026')}.",
]))
CUR[0] = "I.2"
INTRO.append(("I.2", None, [
    f"In the CHALLENGE trial, structured exercise for {N('3', 'lit', 'courneya2025')} years after adjuvant chemotherapy for colon cancer prolonged "
    f"disease-free survival{cite('courneya2025')}.",
    f"Its hazard ratio (HR) for recurrence, new primary cancer or death was {N('0.72', 'lit', 'courneya2025')}, with a "
    f"{N('95', 'label', 'confidence level')}% confidence interval (CI) of [{N('0.55', 'lit', 'courneya2025')}, {N('0.94', 'lit', 'courneya2025')}]{cite('courneya2025')}.",
    f"In breast cancer, randomized trials of exercise during adjuvant chemotherapy found better physical fitness and, in some, less fatigue"
    f"{cite('furmaniak2016', 'courneya2007', 'vanwaart2015', 'mijwel2018')}.",
    f"An exploratory follow-up of one trial found an HR for disease-free survival of {N('0.68', 'lit', 'courneya2014')} "
    f"({N('95', 'label', 'confidence level')}% CI [{N('0.37', 'lit', 'courneya2014')}, {N('1.24', 'lit', 'courneya2014')}]){cite('courneya2014')}.",
    f"During neoadjuvant chemotherapy, diet and exercise were associated with a higher pCR in one trial{cite('sanft2023')}; supervised "
    f"exercise did not change tumor size in two others{cite('kjeldsted2025', 'schmidt2025')}.",
    f"A meta-analysis of eight trials across cancer types found no difference in pCR{cite('diasrato2026')}.",
    f"A trial powered for pCR, with disease-free survival as a secondary outcome, was registered in {N('2022', 'lit', 'deboniface2022')}{cite('deboniface2022')}.",
    "None of these trials reported recurrence, so the effect of exercise during neoadjuvant chemotherapy on recurrence is unknown.",
]))
CUR[0] = "I.3"
INTRO.append(("I.3", None, [
    "The evidence needed to judge exercise during neoadjuvant chemotherapy lacks two things.",
    "First, economic evaluations of exercise in cancer have valued effects measured in trials, mostly on fatigue, fitness or quality of life during or "
    f"after adjuvant treatment{cite('khan2019', 'gublergut2021', 'wang2023')}.",
    f"In breast cancer, such evaluations of exercise during adjuvant chemotherapy reached different conclusions{cite('may2017', 'vanwaart2018', 'perrier2020')}.",
    "When the effect on recurrence is unknown, a cost-effectiveness ratio cannot be estimated, but the highest program cost that remains cost-effective "
    f"can be calculated for each possible effect{cite('boudewijns2023')}.",
    "Second, cost-effectiveness analyses of the KEYNOTE-522 regimen came from the United States, Hong Kong, Switzerland and "
    f"Egypt{cite('huang2023', 'kwong2024', 'favrebulle2024', 'pollinger2025')}.",
    "The Japanese analyses identified concerned pembrolizumab for advanced cancers, including metastatic "
    f"TNBC{cite('chisaki2025', 'sugiura2023', 'taniguchi2026', 'kakinuma2025', 'morimoto2026', 'tomura2025', 'kashiwa2024')}.",
    f"As of October {N('2026', 'label', 'date of the C2H list consulted (reference c2h_list, cited 2026 Oct 26)')}, pembrolizumab had not been designated "
    f"for Japan's cost-effectiveness evaluation{cite('c2h_list')}.",
    "Without a Japanese estimate for pembrolizumab, there is no reference against which the cost and health gain of exercise can be judged.",
]))
CUR[0] = "I.4"
INTRO.append(("I.4", None, [
    # the aims, word for word as given in the instruction (section 4)
    "This study aimed to estimate, from the perspective of the Japanese public healthcare payer, the maximum cost per patient at which adding a structured "
    "exercise program to neoadjuvant chemotherapy with pembrolizumab for stage II or III triple-negative breast cancer would be cost-effective, and how "
    "this cost depends on the size and duration of the effect of exercise on recurrence.",
    "The secondary aims were to estimate the same cost when exercise is added to neoadjuvant chemotherapy alone, to evaluate the cost-effectiveness of "
    "pembrolizumab in Japan as a reference, and to estimate the effect of exercise that would yield the same gain in quality-adjusted life years as pembrolizumab.",
    "No economic evaluation of exercise during neoadjuvant therapy for breast cancer was identified in searches of PubMed and Europe PMC covering "
    f"{N('2000', 'doc', NOV, '2000/01/01')} to {N('2026', 'doc', NOV, '2026/12/31')}, last run on {N('26', 'doc', NOV, '2026-10-26')} October "
    f"{N('2026', 'doc', NOV, '2026-10-26')}.",
    "The nearest, Phys-Can, compared two exercise intensities during neoadjuvant or adjuvant treatment of breast, colorectal or prostate cancer"
    f"{cite('ax2023')}.",
]))

# ---------------------------------------------------------------- Methods (section 3)
CUR[0] = "M.SB.1"
METHODS.append(("M.SB.1", ("Methods", "Study background"), [
    "The decision problem was whether, and up to what cost per patient, a structured exercise program added to neoadjuvant chemotherapy for stage II "
    "or III TNBC was cost-effective in Japan.",
    f"A state-transition model simulated a cohort of women aged {N('49', 'doc', MS, '队列起始年龄 49 岁')} years who started neoadjuvant chemotherapy for "
    f"stage II or III TNBC, with the regimens and outcomes of KEYNOTE-522{cite('schmid2020')}.",
    "Four arms were modeled: chemotherapy alone, as in the placebo arm of the trial; chemotherapy plus pembrolizumab; and each of these with exercise added.",
    "The main comparison was exercise added to chemotherapy plus pembrolizumab against chemotherapy plus pembrolizumab, and the secondary comparison "
    "was exercise added to chemotherapy alone against chemotherapy alone.",
    f"Both treatments to which exercise was added were in use in Japan in {N('2024', 'doc', 'input/params/cohort_N_jbcs2024.csv', '（2024 年）')}{cite('jbcs55')}.",
    "Chemotherapy plus pembrolizumab against chemotherapy alone formed the reference comparison.",
]))
CUR[0] = "M.SB.2"
METHODS.append(("M.SB.2", None, [
    "The analysis took the perspective of the Japanese public healthcare payer and a lifetime horizon, to capture differences in survival.",
    f"Costs and quality-adjusted life years (QALYs) were discounted at {N('2', 'doc', MS, '按年 2% 折现')}% per year, as the Japanese guideline for "
    f"cost-effectiveness evaluation specifies{cite('c2h_guideline')}.",
    f"The willingness-to-pay threshold for exercise was JPY {N('5', 'reg', 'tables', 'Table 2, title')} million per QALY{cite('hasegawa2020', 'mhlw_ce2026')}.",
    f"In Japan's cost-effectiveness evaluation, the higher threshold of JPY {N('7.5', 'reg', 'tables', 'Table 3, title')} million per QALY applies only "
    f"to designated drugs and devices given special consideration, such as those for malignant tumors{cite('mhlw_ce2026')}.",
    f"An exercise program is not such a product, so its maximum affordable cost was judged at JPY {N('5', 'reg', 'tables', 'Table 2, title')} million per QALY.",
    f"Pembrolizumab was also assessed at JPY {N('7.5', 'reg', 'tables', 'Table 3, title')} million per QALY.",
]))
CUR[0] = "M.SB.3"
METHODS.append(("M.SB.3", None, [
    f"Trial inputs came from KEYNOTE-522 reports with data cutoffs of {N('23', 'lit', 'schmid2022')} March {N('2021', 'lit', 'schmid2022')}, "
    f"{N('23', 'doc', MS, '2023-03-23')} March {N('2023', 'doc', MS, '2023-03-23')}, "
    f"{N('22', 'lit', 'schmid2024')} March {N('2024', 'lit', 'schmid2024')} and {N('14', 'doc', P1R, '截点 2025-10-14')} October "
    f"{N('2025', 'doc', P1R, '截点 2025-10-14')}{cite('schmid2022', 'esmo2023', 'schmid2024', 'kn522final2026')}.",
    f"Published data were extracted from {N('21', 'doc', 'input/lifetable/SOURCE.md', '取得日: 2026-10-21')} to "
    f"{N('26', 'doc', 'manuscript/code/references.py', 'cited 2026 Oct 26')} October {N('2026', 'doc', 'input/lifetable/SOURCE.md', '取得日: 2026-10-21')}.",
    "The analysis plan was written before any economic computation, and each later addition was written before the computation it added; the plan "
    "was not registered.",
    f"The study follows the Consolidated Health Economic Evaluation Reporting Standards {N('2022', 'label', 'name of the guideline (CHEERS 2022)')} "
    f"(CHEERS {N('2022', 'label', 'name of the guideline (CHEERS 2022)')}){cite('husereau2022')}; the checklist is in Supplementary Table {S['cheers']}.",
]))
CUR[0] = "M.OUT.1"
METHODS.append(("M.OUT.1", ("Outcome",), [
    "The primary outcome was the maximum affordable cost of an exercise program per patient.",
    "It was the willingness-to-pay threshold multiplied by the incremental QALYs, minus the incremental medical costs other than the program cost, "
    "in JPY per patient.",
    "Increments compared an arm with exercise with the same treatment without exercise, and a program costing less than this amount would be cost-effective.",
    "Medical costs avoided were the incremental medical costs other than the program cost, with the sign reversed.",
]))
CUR[0] = "M.OUT.2"
METHODS.append(("M.OUT.2", None, [
    "Two secondary outcomes were recurrence HRs: the HR at which the maximum affordable cost equaled the cost of a program, and the HR at which "
    "medical costs avoided equaled it.",
    "For pembrolizumab, the secondary outcome was the incremental cost-effectiveness ratio (ICER) against chemotherapy alone.",
    "The exercise effect that would gain as many QALYs as pembrolizumab was expressed as a recurrence HR and as an increase in pCR.",
    "The one-year net benefit was the maximum affordable cost minus the program cost, summed over the eligible patients treated in Japan in one year.",
]))
CUR[0] = "M.VAR.1"
METHODS.append(("M.VAR.1", ("Variables",), [
    "The exposure was the effect of exercise on recurrence, expressed as the recurrence HR with exercise.",
    "This was the HR for locoregional and distant recurrence after surgery in an arm with exercise, relative to the same treatment without exercise "
    "(Table 1).",
    f"It ranged from {N('0.70', 'reg', 'tables', 'Table 1, effect on recurrence')} to {N('1.00', 'reg', 'tables', 'Table 1, effect on recurrence')}, "
    f"where {N('1.00', 'reg', 'tables', 'Table 1, effect on recurrence')} means no effect, and did not act on deaths without recurrence or on events before surgery.",
    f"The CHALLENGE estimate of {N('0.72', 'reg', 'tables', 'Table 1, reference value')} served as a reference point{cite('courneya2025')}.",
]))
CUR[0] = "M.VAR.2"
METHODS.append(("M.VAR.2", None, [
    f"In the base case, the HR held for {N('5', 'reg', 'tables', 'Table 1, effect duration')} years after randomization, after which the effect halved every year.",
    f"Alternative durations held it until {N('1', 'reg', 'tables', 'Table 1, effect duration')} year after surgery or for life.",
    f"In a further alternative, exercise continued for {N('30', 'reg', 'supplement', SDUR)} months after surgery, the effect "
    "held until it stopped, and the cost of continuation counted among medical costs.",
    f"In an alternative pathway, exercise raised the proportion with pCR by {N('0', 'reg', 'tables', 'Table 1, effect on pCR')} to "
    f"{N('10', 'reg', 'tables', 'Table 1, effect on pCR')} percentage points and did not change the recurrence HR.",
    f"Musculoskeletal adverse events of exercise occurred at the rates observed in CHALLENGE{cite('courneya2025')}, with their management costs and utility decrements.",
]))
CUR[0] = "M.VAR.3"
METHODS.append(("M.VAR.3", None, [
    f"Three exercise programs were costed for the {N('6', 'reg', 'tables', 'Table 1, exercise program')} months of neoadjuvant chemotherapy.",
    f"The CHALLENGE-based supervised program used the program cost reported for CHALLENGE{cite('chan2026')}, converted from "
    f"{N('2024', 'reg', 'tables', 'Table 1, footnotes')} Canadian dollars by purchasing power parity{cite('worldbank_ppp')}.",
    f"The fee-schedule-based program and the remote low-cost program were priced from the medical fee schedule{cite('fee2026')}.",
]))
CUR[0] = "M.VAR.4"
METHODS.append(("M.VAR.4", None, [
    "Event-free survival after surgery came from parametric models fitted to patient-level data reconstructed from the published curves of KEYNOTE-522 "
    f"by arm and pCR status{cite('guyot2012', 'schmid2022')}.",
    f"Event-free survival at {N('7', 'reg', 'tables', 'Table 1')} years in each stratum was fixed at the values of the final analysis{cite('kn522final2026')}.",
    "Excess mortality after distant recurrence came from the French Epidemiological Strategy and Medical Economics (ESME) cohort and was the same in "
    f"all arms{cite('grinda2023')}.",
    f"It differed between recurrence within {N('18', 'reg', 'tables', 'Table 1, survival after distant recurrence')} months of randomization and later "
    "recurrence, and progression that precluded surgery took the early-recurrence values.",
    f"Background mortality came from the {N('2025', 'reg', 'tables', 'Table 1, background mortality')} Japanese abridged life table for women{cite('lifetable2025')}.",
]))
CUR[0] = "M.VAR.5"
METHODS.append(("M.VAR.5", None, [
    f"Costs were in JPY at fiscal year {N('2026', 'reg', 'tables', 'Table 1, prices')} prices.",
    f"Drug costs came from the national drug price list{cite('price2026')}, and other costs from the medical fee schedule{cite('fee2026')}, published "
    "Japanese estimates and clinical experts.",
    f"Adverse events of pembrolizumab and chemotherapy came from KEYNOTE-522 and the European Medicines Agency assessment report{cite('schmid2022', 'ema2022')}.",
    f"Utilities were EuroQol {N('5', 'label', 'EuroQol 5-dimension questionnaire (instrument name)')}-dimension {N('5', 'label', 'five response levels (instrument name)')}-level "
    f"(EQ-5D-5L) values from KEYNOTE-522 with the German value set{cite('favrebulle2024', 'ludwig2018')}.",
    "This set was the base case because no report applying a Japanese value set to KEYNOTE-522 data with standard errors was found.",
    f"Values from Japanese populations were used in a scenario{cite('iwatani2021', 'shiroiwa2017')}.",
    f"Table 1 summarizes the inputs, and Supplementary Table {S['params']} lists all of them with their ranges, distributions and sources.",
]))
CUR[0] = "M.SA.1"
METHODS.append(("M.SA.1", ("Statistical analysis",), [
    f"Fig. 1 shows the model: {N('1', 'reg', 'tables', 'Table 1, cycle')}-month cycles from the start of neoadjuvant therapy to age "
    f"{N('100', 'reg', 'tables', 'Table 1, time horizon')} years, with the cohort split by pCR at surgery in month {N('7', 'reg', 'tables', 'Table 1, surgery')}.",
]))
CUR[0] = "M.SA.2"
METHODS.append(("M.SA.2", None, [
    f"({N('1', 'label', STAGE)}) To reproduce the trial outcomes, the survival model was built from event-free survival and external survival after recurrence, without using "
    "overall survival.",
    f"Overall survival in KEYNOTE-522 served only to validate the model, against acceptance criteria fixed before each comparison{cite('schmid2024', 'kn522final2026')}.",
    f"Supplementary Methods {S['methods_survival']} describes the model and the criteria, and Supplementary Fig. {S['fig_validation']} and "
    f"Supplementary Table {S['validation']} show the comparison.",
]))
CUR[0] = "M.SA.3"
METHODS.append(("M.SA.3", None, [
    f"({N('2', 'label', STAGE)}) To estimate the outcomes, the model was run with base-case inputs at recurrence HRs from {N('0.70', 'reg', 'tables', 'Table 1, effect on recurrence')} "
    f"to {N('1.00', 'reg', 'tables', 'Table 1, effect on recurrence')} in steps of {N('0.025', 'doc', AP, '间隔 0.025')}.",
    f"Increases in pCR ran from {N('0', 'reg', 'tables', 'Table 1, effect on pCR')} to {N('10', 'reg', 'tables', 'Table 1, effect on pCR')} percentage points "
    f"in steps of {N('1', 'doc', AP, '间隔 1 个百分点')}.",
    "The HRs at which the maximum affordable cost or the medical costs avoided equaled a program cost were found numerically between "
    f"{N('0.30', 'doc', AP, '在 [0.30, 1.00] 内解')} and {N('1.00', 'doc', AP, '在 [0.30, 1.00] 内解')}.",
    "The exercise effect matching the QALY gain of pembrolizumab was found the same way, between HRs of "
    f"{N('0.30', 'doc', AP, '在 [0.30, 1.00] 内求解')} and {N('1.00', 'doc', AP, '在 [0.30, 1.00] 内求解')} and pCR increases of "
    f"{N('0', 'doc', AP, '[0, 37] 个百分点')} to {N('37', 'doc', AP, '[0, 37] 个百分点')} percentage points.",
    "The results are in Fig. 2 and Tables 2 and 3.",
]))
CUR[0] = "M.SA.4"
METHODS.append(("M.SA.4", None, [
    f"({N('3', 'label', STAGE)}) To reflect uncertainty, each of {N('1,000', 'reg', 'tables', 'Table 1, uncertainty')} probabilistic samples paired one bootstrap replicate of the "
    f"survival model with one draw of the cost and utility inputs (Supplementary Methods {S['methods_survival']}).",
    "Costs, durations and events per patient followed gamma distributions, proportions and utilities beta distributions, and HRs lognormal distributions.",
    "Drug prices and rates based on zero events were fixed.",
    f"The {N('2.5', 'reg', 'tables', 'Table 1, uncertainty')}th and {N('97.5', 'reg', 'tables', 'Table 1, uncertainty')}th percentiles of the samples gave the "
    f"{N('95', 'label', 'interval level')}% uncertainty interval (UI).",
    "The share of samples in which the maximum affordable cost exceeded a program cost, or in which pembrolizumab was cost-effective, gave probabilities.",
]))
CUR[0] = "M.SA.5"
METHODS.append(("M.SA.5", None, [
    f"({N('4', 'label', STAGE)}) To find the inputs that move the results, one-way sensitivity analyses set each input to its lower and upper bounds (Fig. 3).",
    f"They covered the maximum affordable cost in the main comparison at an HR of {N('0.85', 'reg', 'tables', 'Table 2, Panels B and C row label')} and the ICER "
    "of pembrolizumab.",
    f"When a source gave no range, the range was ±{N('25', 'reg', 'figures', 'figure legends')}% of the base value, or the missing bound mirrored the given one.",
    f"Drug prices varied downward only, to {N('75', 'reg', 'figures', 'figure legends')}% of the list price, and these assumed ranges are marked in the figures.",
]))
CUR[0] = "M.SA.6"
METHODS.append(("M.SA.6", None, [
    f"({N('5', 'label', STAGE)}) To examine alternative assumptions, scenario analyses changed one assumption at a time (Table 1).",
    "Besides the alternative effect durations, they used utility values scored with the United States and United Kingdom value "
    f"sets{cite('huang2023', 'kwong2024')} and those of the Australian reimbursement submission{cite('pbac2023')}.",
    "Higher mortality after early recurrence with pembrolizumab multiplied excess mortality after early distant recurrence, and after progression "
    f"during neoadjuvant therapy, by a factor from an Italian cohort{cite('fedele2026')}.",
    "Longer survival after progression during neoadjuvant therapy took the median survival of a single-center cohort with locoregional "
    f"progression{cite('elmore2021')}.",
    f"Other scenarios halved the monthly costs of treatment after distant recurrence, used eribulin-based later-line treatment{cite('cortes2011')}, or "
    f"added post-operative capecitabine or olaparib for patients without pCR{cite('masuda2017', 'tutt2021', 'garber2026')}.",
    "Results involving pembrolizumab were reported both in the base case and with higher mortality after early recurrence with pembrolizumab.",
]))
CUR[0] = "M.SA.7"
METHODS.append(("M.SA.7", None, [
    f"({N('6', 'label', STAGE)}) To express the result for Japan, the one-year net benefit used the fee-schedule-based program at JPY {N('5', 'reg', 'tables', 'Table 2, title')} "
    f"million per QALY for recurrence HRs of {N('0.95', 'reg', 'supplement', 'Supplementary Table ' + S['netbenefit'])}, "
    f"{N('0.90', 'reg', 'supplement', 'Supplementary Table ' + S['netbenefit'])} and {N('0.85', 'reg', 'supplement', 'Supplementary Table ' + S['netbenefit'])}.",
    f"Patients who received neoadjuvant pembrolizumab in the {N('2024', 'doc', 'input/params/cohort_N_jbcs2024.csv', '（2024 年）')} national registry took "
    f"the net benefit of the main comparison, and the other patients that of the secondary comparison{cite('jbcs55')}.",
    "These values are conditional on the HR and are not expected values.",
]))
CUR[0] = "M.SA.8"
METHODS.append(("M.SA.8", None, [
    "No statistical tests were performed, so no adjustment for multiple comparisons was needed.",
    f"All analyses were performed in R version {N('4.5.1', 'doc', 'renv.lock', chr(34) + 'Version' + chr(34) + ': ' + chr(34) + '4.5.1' + chr(34))}.",
]))


# ================================================================ Results: the v4 paragraphs with the edits of v5
def renum(text: str) -> str:
    """Supplementary table numbers of v4 -> v5 (all at once, so S5 -> S6 and S8 -> S5 do not chain)."""
    def one(m):
        return SUPP_RENUMBER_V4_V5.get(m.group(0), m.group(0))
    return re.sub(r"(?<=Supplementary Table )S\d+|(?<=Supplementary Tables )S\d+|(?<= and )S\d+(?=\))", one, text)


def renum_where(w: str) -> str:
    m = re.match(r"Supplementary Table (S\d+)(.*)", w)
    return f"Supplementary Table {SUPP_RENUMBER_V4_V5.get(m.group(1), m.group(1))}{m.group(2)}" if m else w


def V(reg, where, idx=0):
    rows = [x for x in REGS[reg]["rows"] if x["where"] == where]
    if len(rows) <= idx:
        raise KeyError(f"{reg}: no entry {idx} for {where!r}")
    return rows[idx]


OLD = base["paragraphs"]
assert [len(p) for p in OLD] == [6, 4, 3, 4, 3, 4, 7, 3, 4, 6]
LOG = []  # (paragraph, sentence, kind, reason, before, after)


def old(p, s):
    """v4 sentence p.s with the v5 supplementary numbers, and its numbers."""
    src = OLD[p - 1][s - 1]
    e = dict(text=renum(src["text"]), cites=[renum(c) for c in src["cites"]], keys=list(src["keys"]), origin=f"v4 P{p}.{s}", nums=[])
    for u in base["used"]:
        if u["paragraph"] == p and u["sentence"] == s:
            w = renum_where(u["where"])
            assert u["shown"] in {x["shown"] for x in REGS[u["registry"]]["rows"] if x["where"] == w}, ("value no longer in the registry", u, w)
            e["nums"].append(dict(placeholder=u["placeholder"], registry=u["registry"], where=w, shown=u["shown"],
                                  source=next(x["source"] for x in REGS[u["registry"]]["rows"] if x["where"] == w and x["shown"] == u["shown"]),
                                  loc=next(x["loc"] for x in REGS[u["registry"]]["rows"] if x["where"] == w and x["shown"] == u["shown"])))
    if e["text"] != src["text"]:
        LOG.append((p, s, "renumber", "section 1: supplementary numbering by first citation", src["text"], e["text"]))
    return e


def sub(e, a, b, reason):
    assert e["text"].count(a) == 1, (a, e["text"])
    before = e["text"]
    e["text"] = e["text"].replace(a, b)
    LOG.append((e["origin"], None, "edit", reason, before, e["text"]))
    return e


def drop(e, tab, reason="section 2: the same table cited in consecutive sentences is cited once, at the end of the last one"):
    for a, b in ((f" ({tab}).", "."), (f"; {tab})", ")")):
        if e["text"].count(a) == 1:
            return sub(e, a, b, reason)
    raise ValueError((tab, e["text"]))


def new(tpl, keys, cites, reason):
    vals, nums = {}, []
    for k, (reg, where, idx) in keys.items():
        x = V(reg, where, idx)
        vals[k] = x["shown"]
        nums.append(dict(placeholder=k, registry=reg, where=where, shown=x["shown"], source=x["source"], loc=x["loc"]))
    e = dict(text=tpl.format(**vals), cites=cites, keys=list(keys), origin="new in v5", nums=nums)
    LOG.append(("new", None, "new", reason, "", e["text"]))
    return e


ACR = "section 3/4: the abbreviation is defined at its first use in the Introduction or Methods, so the Results use it without repeating the definition"
T2, T3 = "Table 2", "Table 3"
SPB, SDE, SDU, SNB = (f"Supplementary Table {S[k]}" for k in ("pathB", "decomp", "duration", "netbenefit"))
R = []
R.append([
    sub(sub(old(1, 1), ", in Japanese yen (JPY),", "", ACR), "recurrence hazard ratio (HR) with exercise", "recurrence HR with exercise", ACR),
    new("At an HR of 0.85, exercise added to chemotherapy plus pembrolizumab had a maximum affordable cost of JPY {a} thousand per patient "
        "(95% UI [{b}, {c}]; Table 2).",
        {k: ("tables", "Table 2, Panel B, base case, main (intended repeat of Supplementary Table S4)", i) for i, k in enumerate("abc")}, [T2],
        "section 2: the estimate and its 95% UI in the same sentence (v4 P1.2 and P1.3 merged)"),
    old(1, 4),
    sub(old(1, 5), "equaled the cost of the fee-schedule-based program at", "equaled the fee-schedule-based program cost at",
        "section 2: wording shortened to keep the paragraph within 150 words after the pathway B sentences were added"),
    old(1, 6),
    new("Through an effect on pCR instead, an increase of 1 percentage point gave a maximum affordable cost of JPY {a} thousand (95% UI [{b}, {c}]).",
        {k: ("supplement", f"{SPB}, A, pcr 0.010, main base", i) for i, k in enumerate("abc")}, [SPB],
        "section 2: pathway B, the maximum affordable cost per percentage point of pCR (the cap rises by the same amount for each point)"),
    new(f"Each further point added about the same amount ({SPB}).", {}, [SPB], "section 2: pathway B (continued)"),
])
R.append([old(2, 1), drop(old(2, 2), SDE), drop(old(2, 3), SDE), old(2, 4)])
R.append([
    old(3, 1), drop(old(3, 2), T2), drop(old(3, 3), SDU),
    new("With exercise continued after surgery, it was JPY {a} thousand, against JPY {b} thousand when the effect lasted until 1 year after surgery "
        f"without continuation ({SDU}).",
        {"a": ("supplement", f"{SDU}, A, continue_s1, main, 0.850", 0), "b": ("supplement", f"{SDU}, A, path_a_s1, main, 0.850", 0)}, [SDU],
        "section 2: exercise continued after surgery, compared with the effect lasting until 1 year after surgery"),
])
R.append([old(4, 1), drop(old(4, 2), T2), drop(old(4, 3), T2), old(4, 4)])
R.append([old(5, 1), drop(old(5, 2), SNB), old(5, 3)])
R.append([old(6, 1), drop(old(6, 2), T2), drop(old(6, 3), T2), old(6, 4)])
R.append([
    sub(old(7, 1), "quality-adjusted life years (QALYs)", "QALYs", ACR), drop(old(7, 2), T3), drop(old(7, 3), T3), drop(old(7, 4), T3), drop(old(7, 5), T3),
    drop(sub(old(7, 6), "The incremental cost-effectiveness ratio (ICER) was", "The ICER was", ACR), T3), old(7, 7),
])
R.append([old(8, 1), drop(old(8, 2), T3), old(8, 3)])
R.append([old(9, 1), drop(old(9, 2), T3), sub(old(9, 3), "pathological complete response (pCR)", "pCR", ACR), old(9, 4)])
LIM = "section 2: last paragraph kept within 150 words by shortening the wording (no result removed)"
R.append([
    sub(sub(old(10, 1), "the one-way sensitivity analysis of", "one-way sensitivity analyses of", LIM), "for exercise added to chemotherapy plus pembrolizumab at",
        "in the main comparison at", LIM),
    sub(old(10, 2), "from JPY 2,617 thousand at its lower bound to JPY 2,836 thousand at its upper bound", "to JPY 2,617 and 2,836 thousand at its lower and upper bounds", LIM),
    new("With higher mortality after early recurrence with pembrolizumab, this cost was JPY {a} thousand (95% UI [{b}, {c}]; Supplementary Table S4).",
        {k: ("supplement", "Supplementary Table S4, A, hr0 0.850, main kext", i) for i, k in enumerate("abc")}, ["Supplementary Table S4"],
        "section 2: main comparison at HR 0.85 with higher mortality after early recurrence with pembrolizumab (Supplementary Table S4)"),
    sub(old(10, 3), "Supplementary Fig. S2 shows that the pembrolizumab drug cost moved the ICER most, to JPY 1,296 thousand per QALY at its lower bound.",
        "The pembrolizumab drug cost moved the ICER most, to JPY 1,296 thousand per QALY at its lower bound (Supplementary Fig. S2).", LIM),
    sub(sub(old(10, 4), "Supplementary Table S10 shows that, with utility values from Japanese populations, the maximum", "With utility values from Japanese populations, the maximum", LIM),
        "affordable cost at an HR of 0.85 was", "affordable cost at that HR was", LIM),
    drop(old(10, 5), "Supplementary Table S10"),
    sub(old(10, 6), "the ICER of pembrolizumab was", "the ICER was", LIM),
])
# a sentence without its own reference must be followed, in the same paragraph, by one that cites the same table
for pi, ps in enumerate(R, start=1):
    for si, e in enumerate(ps):
        own = set(re.findall(r"(Supplementary Tables? S\d+|Supplementary Fig\. S\d+|Table \d|Fig\. \d)", e["text"]))
        if not own and si > 0:
            later = " ".join(x["text"] for x in ps[si + 1:])
            assert any(c in later or c.replace("Table ", "Tables ") in later for c in e["cites"]), ("reference missing", pi, e["text"])
paras_res = [[dict(text=e["text"], cites=e["cites"], keys=e["keys"], origin=e["origin"]) for e in ps] for ps in R]
used = []
for pi, ps in enumerate(R, start=1):
    for si, e in enumerate(ps, start=1):
        for u in e["nums"]:
            used.append(dict(paragraph=pi, sentence=si, **u))

# ================================================================ docx
doc = Document(ARCHIVE_PREV / f"results_{PREV}.docx")
body = [p for p in doc.paragraphs if p.text.strip()]
assert body[0].text == "Results"
assert [p.text for p in body[1:]] == [" ".join(s["text"] for s in ps) for ps in OLD], "ledger of the previous version does not match its docx"
for p, ps in zip(body[1:], paras_res):
    assert len(p.runs) == 1
    p.runs[0].text = " ".join(s["text"] for s in ps)
HEAD, BODY = copy.deepcopy(body[0]._p), copy.deepcopy(body[1]._p)


def par(tmpl, text):
    el = copy.deepcopy(tmpl)
    runs = el.findall(qn("w:r"))
    for r in runs[1:]:
        el.remove(r)
    t = runs[0].find(qn("w:t"))
    t.text = text
    t.set(qn("xml:space"), "preserve")
    return el


anchor = body[0]._p
order = []  # (id, kind, text) in reading order
for pid, head, sents in INTRO + METHODS:
    if head:
        for h in ([head] if isinstance(head, str) else head):
            anchor.addprevious(par(HEAD, h))
            order.append((None, "heading", h))
    anchor.addprevious(par(BODY, " ".join(sents)))
    order.append((pid, "body", " ".join(sents)))
order.append((None, "heading", "Results"))
for i, ps in enumerate(paras_res, start=1):
    order.append((f"R.{i}", "body", " ".join(s["text"] for s in ps)))
out = BUILD / "manuscript_marked.docx"
doc.save(out)

# ================================================================ ledgers
led = {"paragraphs": paras_res, "used": used, "base": f"results_{PREV}.docx", "edits": [dict(zip(("paragraph", "sentence", "kind", "reason", "before", "after"), x)) for x in LOG]}
for name in ("_ledger_results.json", f"_ledger_results_{VER}.json"):
    json.dump(led, open(BUILD / name, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
secs = []
for pid, head, sents in INTRO + METHODS:
    secs.append(dict(id=pid, sentences=sents, numbers=[r for r in MROWS if r["where"] == pid]))
json.dump({"paragraphs": secs, "rows": MROWS}, open(BUILD / "_ledger_manuscript.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ids = [pid for pid, _, _ in order if pid]
json.dump({"ids": ids, "order": [dict(id=a, kind=b, text=c) for a, b, c in order], "manuscript_sha256": hashlib.sha256(out.read_bytes()).hexdigest()},
          open(BUILD / "_manuscript_map.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# numbers of the Introduction and Methods: every token of a paragraph must be registered for it
strip = lambda t: MARK_RE.sub("", re.sub(r"\b(?:Supplementary )?(?:Tables?|Figs?\.|Methods) S?\d+[a-z]?(?:\s*(?:and|to|,)\s*S?\d+)*", " ", t))
bad = []
for pid, _, sents in INTRO + METHODS:
    reg = {r["shown"] for r in MROWS if r["where"] == pid}
    for s in sents:
        for t in num_tokens(strip(s)):
            if t not in reg:
                bad.append((pid, t, s[:60]))
assert not bad, bad


def words(t):
    return len(MARK_RE.sub("", t).split())


print("manuscript_marked.docx written from", f"results_{PREV}.docx")
for pid, _, sents in INTRO + METHODS:
    w = [words(s) for s in sents]
    print(f"  {pid}: {sum(w)} words, longest sentence {max(w)}")
for i, ps in enumerate(paras_res, start=1):
    w = [len(s["text"].split()) for s in ps]
    print(f"  R.{i}: {sum(w)} words, longest sentence {max(w)}")
print("Results edits:", len(LOG), "| numbers registered for Introduction and Methods:", len(MROWS))
