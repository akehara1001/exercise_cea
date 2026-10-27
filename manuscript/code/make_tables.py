"""Tables 1 to 3 of the manuscript (tables_<VER>.docx).

Reads the phase 1 and phase 2 outputs and the parameter workbook; does not run
the model. Writes _build/tables_marked.docx, with reference markers that
number_refs.py turns into numbers in manuscript/<VER>/tables_<VER>.docx, and the table
part of the number registry (manuscript/code/_build/_ledger_tables.json, used by make_ledger.py).
"""
from __future__ import annotations

import json
import sys

import numpy as np

from docx_util import new_document, new_section, para, table
from references import cite
from common import (BUILD, VER, OUT, P1, ROOT, STAR, SUPP, Params, Registry, csv, fk,
                       fnum, fyen, one, pct, rel)

sys.stdout.reconfigure(encoding="utf-8")
REG = Registry()
PR = Params()
S1, S2, S3, S4 = STAR, STAR * 2, STAR * 3, STAR * 4


def line_of(path, needle: str) -> str:
    for i, ln in enumerate((ROOT / path).read_text(encoding="utf-8").splitlines(), start=1):
        if needle in ln:
            return f"{path} line {i}"
    raise ValueError(f"{needle!r} not found in {path}")


def sup(sym: str) -> str:
    return "^{" + sym + "}"


# ---------------------------------------------------------------- names (one name per thing)
ARM_MAIN = "Exercise added to chemotherapy plus pembrolizumab"
ARM_SEC = "Exercise added to chemotherapy alone"
PROG = {"E01": "CHALLENGE-based supervised program",
        "E02": "fee-schedule-based program",
        "E03": "remote low-cost program"}
SC = {"base": "Base case",
      "kext": "Higher mortality after early recurrence with pembrolizumab",
      "sjp": "Japanese post-operative treatment",
      "m50": "Metastatic treatment costs halved",
      "eri": "Eribulin-based later-line treatment",
      "dur1": "Effect until 1 year after surgery",
      "dur2": "No waning"}

# ================================================================ Table 1
T = "Table 1"


def doc_num(shown, where, path, needle, raw=None):
    return REG.r(shown, f"{T}, {where}", path, line_of(path, needle), raw if raw is not None else shown)


pc = csv("pcr_counts.csv", ROOT / "data")
k22 = one(pc, source="K22 (IA4)")
n_pc_p, n_np_p, n_pc_c, n_np_c = (int(k22[c]) for c in ("pcr_pembro", "nonpcr_pembro", "pcr_placebo", "nonpcr_placebo"))
f7 = csv("kn522_final_7y.csv", ROOT / "data")
cal = csv("calibration.csv", P1)
calr = cal[(cal.stage == "calibrated") & (cal.arm == "pembro")].iloc[0]
kx = csv("kext_derivation.csv", P1 / "round14")
kval = float(one(kx, quantity="k_external")["value"])

PCR_SRC = "data/pcr_counts.csv"


def pcr_cell():
    a = REG.r(str(n_pc_p), f"{T}, pCR", PCR_SRC, "row K22 (IA4), column pcr_pembro", n_pc_p)
    b = REG.r(str(n_pc_p + n_np_p), f"{T}, pCR", PCR_SRC, "row K22 (IA4), pcr_pembro + nonpcr_pembro", n_pc_p + n_np_p)
    c = REG.r(pct(n_pc_p / (n_pc_p + n_np_p)), f"{T}, pCR", PCR_SRC, "pcr_pembro / (pcr_pembro + nonpcr_pembro)", n_pc_p / (n_pc_p + n_np_p))
    d = REG.r(str(n_pc_c), f"{T}, pCR", PCR_SRC, "row K22 (IA4), column pcr_placebo", n_pc_c)
    e = REG.r(str(n_pc_c + n_np_c), f"{T}, pCR", PCR_SRC, "row K22 (IA4), pcr_placebo + nonpcr_placebo", n_pc_c + n_np_c)
    f = REG.r(pct(n_pc_c / (n_pc_c + n_np_c)), f"{T}, pCR", PCR_SRC, "pcr_placebo / (pcr_placebo + nonpcr_placebo)", n_pc_c / (n_pc_c + n_np_c))
    return f"{a}/{b} ({c}%) with pembrolizumab; {d}/{e} ({f}%) with chemotherapy alone"


def efs7(idv):
    v = float(one(f7, id=idv)["value"])
    return REG.r(fnum(v, 1), f"{T}, event-free survival", "data/kn522_final_7y.csv", f"row id = {idv}, column value", v)


def calv(col, nd):
    v = float(calr[col])
    return REG.r(fnum(v, nd), f"{T}, survival after distant recurrence", rel(P1 / "calibration.csv"), f"row stage = calibrated, arm = pembro, column {col}", v)


def msk(pid, n, d):
    v, loc = PR.get(pid)
    if abs(v - n / d) > 5e-6:
        raise ValueError((pid, v, n, d))
    a = REG.r(str(n), f"{T}, musculoskeletal adverse events", "docs/model_spec.md", line_of("docs/model_spec.md", f"{n}/{d}"), n)
    b = REG.r(str(d), f"{T}, musculoskeletal adverse events", "docs/model_spec.md", line_of("docs/model_spec.md", f"{n}/{d}"), d)
    c = REG.r(pct(v), f"{T}, musculoskeletal adverse events", "input/params/parameters_v10.xlsx", loc, v)
    return f"{a}/{b} ({c}%)"


XL = "input/params/parameters_v10.xlsx"
MS = "docs/model_spec.md"
AP = "docs/analysis_plan_phase2.md"


def yen(pid, where):
    v, loc = PR.get(pid)
    return REG.r(fyen(v), f"{T}, {where}", XL, loc, v)


def val(pid, where, nd):
    v, loc = PR.get(pid)
    return REG.r(fnum(v, nd), f"{T}, {where}", XL, loc, v)


m50_d05, m50_mult, m50_loc = PR.scenario("sc_metcost50", "D05")
eri_d05, eri_mult, eri_loc = PR.scenario("sc_eribulin", "D05")

t1 = [["Input", "Base case", "Source"]]
bold1 = set()


def grp(name):
    t1.append([name])
    bold1.add(len(t1) - 1)


grp("Model settings")
t1.append(["Perspective", "Japanese public healthcare payer", "—"])
t1.append(["Cohort",
           f"Women aged {doc_num('49', 'cohort', MS, '队列起始年龄 49 岁', 49)} years starting neoadjuvant chemotherapy for stage II or III triple-negative breast cancer",
           "KEYNOTE-522 trial population" + cite("schmid2020")])
t1.append(["Time horizon and cycle",
           f"Lifetime (to age {doc_num('100', 'time horizon', MS, '模拟到 100 岁', 100)} years); {doc_num('1', 'cycle', MS, '周期 1 个月', 1)}-month cycles; surgery at month {doc_num('7', 'surgery', MS, '手术时点（landmark）为随机化后 7 个月', 7)}",
           "—"])
t1.append(["Discounting",
           f"{doc_num('2', 'discounting', MS, '按年 2% 折现', 2)}% per year for costs and QALYs", "—"])
PRICE_LOC = f"{XL} sheet パラメータ column J (価格の年度) = 令和8年度 in the cost rows; 令和8年度 = fiscal year 2026"
t1.append(["Prices",
           f"JPY, fiscal year {REG.r('2026', f'{T}, prices', XL, PRICE_LOC, '令和8年度')}",
           "National drug price list and medical fee schedule" + cite("price2026", "fee2026")])
n_psa = int(csv("psa_caps_summary.csv").n.iloc[0])
t1.append(["Uncertainty",
           f"{REG.r(fnum(n_psa, 0), f'{T}, uncertainty', 'output/phase2/main/psa_caps_summary.csv', 'column n (all rows)', n_psa)} probabilistic sensitivity analysis samples, "
           "each pairing one bootstrap replicate of the survival model with one draw of the cost and utility inputs; "
           f"95% uncertainty interval from the {REG.label('2.5', f'{T}, uncertainty', 'UI percentile (' + line_of(AP, '中位数与 2.5、97.5 百分位') + ')')}th and "
           f"{REG.label('97.5', f'{T}, uncertainty', 'UI percentile (' + line_of(AP, '中位数与 2.5、97.5 百分位') + ')')}th percentiles",
           "—"])

grp("Survival")
t1.append(["Pathological complete response (pCR)", pcr_cell(), "KEYNOTE-522 (interim analysis 4)" + cite("schmid2022")])
t1.append(["Event-free survival after surgery",
           "Parametric models fitted to reconstructed patient-level data by arm and pCR status (pCR, Weibull; no pCR, Weibull cure model); "
           f"7-year values fixed at the final analysis: pCR {efs7('efs_pcr_pembro')}% vs {efs7('efs_pcr_placebo')}%, no pCR {efs7('efs_nonpcr_pembro')}% vs {efs7('efs_nonpcr_placebo')}% (with pembrolizumab vs chemotherapy alone)",
           "KEYNOTE-522 (interim analysis 4 and final analysis)" + cite("guyot2012", "schmid2022", "kn522final2026")])
t1.append(["Arms with exercise",
           "Survival inputs of the corresponding arm without exercise, changed only by the exercise effect", "—"])
t1.append(["Survival after distant recurrence",
           f"Log-logistic excess mortality, same in all arms: median {calv('dr_median_months', 2)} months for recurrence within "
           f"{doc_num('18', 'survival after distant recurrence', MS, '随机化后 18 个月以内的远处复发', 18)} months of randomization and "
           f"{calv('dr_late_median_months', 2)} months thereafter; common shape {calv('dr_shape', 3)}",
           "ESME cohort, reconstructed overall survival" + cite("grinda2023", "guyot2012")])
t1.append(["Survival after progression during neoadjuvant therapy",
           "Same distribution as distant recurrence within the first 18 months".replace(" 18 ", " " + REG.r("18", f"{T}, progression during neoadjuvant therapy", MS, line_of(MS, "随机化后 18 个月以内的远处复发"), 18) + " "),
           "ESME cohort" + cite("grinda2023")])
t1.append(["Background mortality", "Japanese women",
           f"Abridged life table ({REG.r('2025', f'{T}, background mortality', 'data/lifetable_female_2025.csv', 'file name (令和7年簡易生命表, women)', 2025)})" + cite("lifetable2025")])
t1.append(["Overall survival in KEYNOTE-522", f"Not used to fit the model; used only for validation (Supplementary Methods {SUPP['methods_survival']})", "KEYNOTE-522 reports" + cite("schmid2024", "kn522final2026")])

grp("Costs, JPY")
t1.append(["Pembrolizumab, per dose",
           f"{yen('A03', 'pembrolizumab')} ({REG.r('200', f'{T}, pembrolizumab', XL, PR.get('A03', 'note')[1], '200 mg')} mg every "
           f"{REG.r('3', f'{T}, pembrolizumab', XL, PR.get('A03', 'note')[1], '3週毎')} weeks; "
           f"{REG.r('8', f'{T}, pembrolizumab', XL, PR.get('A03', 'note')[1], '術前8回')} doses before and "
           f"{REG.r('9', f'{T}, pembrolizumab', XL, PR.get('A03', 'note')[1], '術後9回')} after surgery)",
           "National drug price list; KEYNOTE-522 dosing" + cite("price2026", "schmid2020")])
t1.append(["First-line treatment of distant recurrence, per month",
           f"{yen('D03', 'first-line treatment')} in arms without pembrolizumab; {yen('D03P', 'first-line treatment')} in arms with pembrolizumab (no immunotherapy rechallenge); "
           f"mean duration {val('D04', 'first-line treatment', 2)} and {val('D04P', 'first-line treatment', 2)} months",
           "Clinical expert input on the regimen mix; trials; national drug price list" + cite("tropion2025", "cortes2020", "miller2007", "price2026")])
d05note = PR.get("D05", "note")[1]
t1.append(["Second-line and later treatment, per month",
           f"{yen('D05', 'second-line treatment')} (trastuzumab deruxtecan {REG.r('32', f'{T}, second-line treatment', XL, d05note, '32%')}%, "
           f"sacituzumab govitecan {REG.r('68', f'{T}, second-line treatment', XL, d05note.replace('cell N', 'cell N (32%) and D03 note'), '68%')}%)",
           "Clinical expert input; national drug price list" + cite("price2026")])
t1.append(["End-of-life care, last 3 months".replace("3", REG.r("3", f"{T}, end-of-life care", XL, PR.get("D06")[1].replace("cell G", "cell C"), "死亡前3か月")),
           yen("D06", "end-of-life care"), "Published Japanese estimates" + cite("nusawat2026", "ohtera2018")])
t1.append([f"Exercise program, total over the {REG.r('6', f'{T}, exercise program', XL, PR.get('E02')[1].replace('cell G', 'cell C'), 'NAC中6か月')} months of neoadjuvant therapy",
           f"{PROG['E01'][0].upper() + PROG['E01'][1:]}{sup(S2)} {yen('E01', 'exercise program')}; {PROG['E02']} {yen('E02', 'exercise program')}; {PROG['E03']} {yen('E03', 'exercise program')}",
           "CHALLENGE program cost; medical fee schedule" + cite("chan2026", "worldbank_ppp", "boc_fx", "fee2026")])
t1.append(["Musculoskeletal adverse event of exercise, per event", yen("E08", "musculoskeletal adverse event cost"), "Medical fee schedule" + cite("fee2026")])

grp("Utilities" + sup(S3))
t1.append(["Event-free, during treatment", val("U01", "utilities", 3), "KEYNOTE-522 EQ-5D, German value set" + cite("favrebulle2024")])
t1.append(["Event-free, after treatment", val("U02", "utilities", 3), "KEYNOTE-522 EQ-5D, German value set" + cite("favrebulle2024")])
t1.append(["Locoregional recurrence", val("U03", "utilities", 3), "KEYNOTE-522 EQ-5D, German value set" + cite("favrebulle2024")])
t1.append(["Distant recurrence or progression during neoadjuvant therapy", val("U04", "utilities", 3), "KEYNOTE-522 EQ-5D, German value set" + cite("favrebulle2024")])
u05note = PR.get("U05", "note")[1]
t1.append(["Grade 3 or higher adverse event",
           f"Decrement {val('U05', 'utilities', 3)} for {REG.r('12.5', f'{T}, utilities', XL, u05note, '12.5 週')} weeks per event "
           f"({val('B33P', 'utilities', 3)} events per patient with pembrolizumab, {val('B33C', 'utilities', 3)} without)",
           "KEYNOTE-522 EQ-5D and adverse event tables" + cite("favrebulle2024", "schmid2022")])

grp("Exercise effect")
t1.append(["Effect on recurrence",
           f"Recurrence HR{sup(S4)} from {doc_num('0.70', 'effect on recurrence', AP, 'hr0 取 0.70 至 1.00', 0.70)} to {doc_num('1.00', 'effect on recurrence', AP, 'hr0 取 0.70 至 1.00', 1.00)}; "
           "no effect on deaths without recurrence or on events before surgery", "Assumption"])
t1.append(["Effect duration, base case",
           f"HR held for {doc_num('5', 'effect duration', AP, '随机化后 5 年内保持 hr0', 5)} years after randomization, then the effect halves every year", "Assumption"])
t1.append(["Effect duration, alternatives",
           f"{SC['dur1']}, then halving every year; {SC['dur2'].lower()}".replace(" 1 year", " " + doc_num("1", "effect duration", AP, "情景①：效应维持到手术后 1 年", 1) + " year"),
           "Assumption"])
t1.append(["Reference value",
           f"HR {REG.r('0.72', f'{T}, reference value', 'input/papers/CHALLENGE.pdf', 'p.7 (also p.1): hazard ratio for disease recurrence, new primary cancer, or death, 0.72; and ' + line_of(AP, '图中标出 0.72'), 0.72)} for disease-free survival with a "
           f"{REG.r('3', f'{T}, reference value', AP, line_of(AP, 'CHALLENGE（结肠癌、3 年方案、DFS）'), 3)}-year exercise program in colon cancer",
           "CHALLENGE trial" + cite("courneya2025")])
t1.append(["Effect on pCR (alternative pathway)",
           f"pCR proportion increased by {doc_num('0', 'effect on pCR', AP, 'pCR 比例提高 0 至 10 个百分点', 0)} to {doc_num('10', 'effect on pCR', AP, 'pCR 比例提高 0 至 10 个百分点', 10)} percentage points, with recurrence HR 1.00".replace("HR 1.00", "HR " + doc_num("1.00", "effect on pCR", AP, "路径 B 的实现：pCR 比例 = min(该臂的 pCR 比例 + 提高幅度, 1)，hr0 = 1", 1.00)),
           "Assumption"])
t1.append(["Musculoskeletal adverse events",
           f"Any grade {msk('E06', 79, 428)} with exercise vs {msk('E07', 53, 461)} without; grade 3 or higher {msk('E09', 3, 428)} vs {msk('E10', 1, 461)}",
           "CHALLENGE trial, as-treated" + cite("courneya2025")])

grp("Scenarios")
t1.append([SC["kext"],
           f"Excess mortality after distant recurrence within the first 18 months and after progression during neoadjuvant therapy multiplied by "
           .replace(" 18 ", " " + REG.r("18", f"{T}, scenarios", MS, line_of(MS, "随机化后 18 个月以内的远处复发"), 18) + " ")
           + f"{REG.r(fnum(kval, 3), f'{T}, scenarios', rel(P1 / 'round14' / 'kext_derivation.csv'), 'row quantity = k_external, column value', kval)} in arms with pembrolizumab",
           "Italian real-world cohort after neoadjuvant pembrolizumab" + cite("fedele2026")])
t1.append([SC["m50"],
           f"Monthly costs of first-line and later-line treatment of distant recurrence multiplied by {REG.r(fnum(m50_mult, 1), f'{T}, scenarios', XL, m50_loc, m50_mult)}",
           "—"])
t1.append([SC["eri"],
           f"{REG.r(fyen(eri_d05), f'{T}, scenarios', XL, eri_loc, eri_d05)} per month for second-line and later treatment",
           "EMBRACE dosing; national drug price list" + cite("cortes2011", "price2026")])
t1.append([SC["sjp"],
           f"Capecitabine (HR {val('F07', 'scenarios', 2)}) or olaparib (HR {val('F08', 'scenarios', 2)}) for patients without pCR, by germline BRCA status",
           "CREATE-X; OlympiA" + cite("masuda2017", "tutt2021", "garber2026")])

t1_notes = [
    f"{S1}All inputs with their ranges, distributions and sources are listed in Supplementary Table {SUPP['params']}. Costs are in JPY at fiscal year 2026 prices except where noted. "
    "A dash in the source column marks a setting of the analysis rather than an external source. "
    "BRCA, breast cancer gene; EQ-5D, EuroQol 5-dimension questionnaire; ESME, Epidemiological Strategy and Medical Economics database; "
    "HR, hazard ratio; JPY, Japanese yen; pCR, pathological complete response; QALY, quality-adjusted life year.",
    f"{S2}Program cost reported in the CHALLENGE cost analysis for the 3-year program, condensed to the 6 months of neoadjuvant therapy and converted from 2024 Canadian dollars by purchasing power parity.",
    f"{S3}Base case: EQ-5D values from KEYNOTE-522 with the German value set, because no report applying a Japanese value set to KEYNOTE-522 data with standard errors was found. "
    f"Values from Japanese populations are used in a scenario (Supplementary Table {SUPP['other']}).",
    f"{S4}Recurrence HR: hazard ratio for locoregional and distant recurrence after surgery in an arm with exercise, relative to the same treatment without exercise; 1.00 means no effect.",
]
# numbers in the notes that are not values of the table body: register as definitions
for tok, why in (("2026", "price year, as in the Prices row"), ("5", "EQ-5D instrument name (EuroQol 5-dimension)"),
                 ("3", "3-year CHALLENGE program, as in the Reference value row"), ("6", "6 months of neoadjuvant therapy, as in the Exercise program row"),
                 ("2024", "currency year of the CHALLENGE cost analysis (parameters_v10.xlsx E01 column 価格の年度: 2024年（CAD）)"),
                 ("1.00", "no-effect value of the HR, as in the Effect on recurrence row")):
    REG.label(tok, f"{T}, footnotes", why)
REG.label("4", f"{T}, source column", "name of the trial analysis (interim analysis 4, IA4)")

# ================================================================ Table 2
T = "Table 2"
dc = csv("det_caps.csv")
ps = csv("psa_caps_summary.csv")
xb = csv("sc_base_crossings.csv")
scap = csv("scenario_caps.csv")


def capcell(comp, h, det_file, psa_file, d_df, p_df, where):
    d = d_df[(d_df.comparison == comp) & (d_df.column == "base") & (d_df.axis == "hr0") & (np.isclose(d_df.x, h))]
    p = p_df[(p_df.comparison == comp) & (p_df.column == "base") & (p_df.axis == "hr0") & (np.isclose(p_df.x, h))]
    assert len(d) == 1 and len(p) == 1, (comp, h, det_file)
    d, p = d.iloc[0], p.iloc[0]
    if not (p.cap500_lo <= d.cap_500 <= p.cap500_hi):
        raise ValueError(f"point estimate outside its UI: {comp} {h} {det_file}")
    a = REG.r(fk(d.cap_500), where, det_file, f"comparison = {comp}, column = base, axis = hr0, x = {h:.2f}, cap_500", d.cap_500)
    b = REG.r(fk(p.cap500_lo), where, psa_file, f"comparison = {comp}, column = base, axis = hr0, x = {h:.2f}, cap500_lo", p.cap500_lo)
    c = REG.r(fk(p.cap500_hi), where, psa_file, f"comparison = {comp}, column = base, axis = hr0, x = {h:.2f}, cap500_hi", p.cap500_hi)
    return f"{a} [{b}, {c}]"


def cross(df, file, comp, typ, prog, where):
    sub = df[(df.comparison == comp) & (df.column == "base") & (df.type == typ) & (df.programme == prog)]
    if typ == "cap_eq_programme":
        sub = sub[np.isclose(sub["lambda"], 5e6)]
    assert len(sub) == 1, (file, comp, typ, prog)
    v = float(sub.iloc[0].hr0)
    lam = ", lambda = 5e+06" if typ == "cap_eq_programme" else ""
    return REG.r(fnum(v, 3), where, file, f"comparison = {comp}, column = base, type = {typ}{lam}, programme = {prog}, hr0", v)


t2 = [["Break-even point or scenario", ARM_MAIN, ARM_SEC]]
bold2 = set()
RED = " (reduction in recurrence hazard, %)"
avoided_e02_main = []  # reductions behind the range stated in footnote ✳✳✳


def crossred(df, file, comp, typ, prog, where):
    """Break-even cell 'HR (reduction %)': reduction = 100 x (1 - HR) from the raw HR, 1 decimal."""
    hr = cross(df, file, comp, typ, prog, where)
    sub = df[(df.comparison == comp) & (df.column == "base") & (df.type == typ) & (df.programme == prog)]
    if typ == "cap_eq_programme":
        sub = sub[np.isclose(sub["lambda"], 5e6)]
    v = float(sub.iloc[0].hr0)
    red = 100.0 * (1.0 - v)
    if comp == "main" and typ == "avoided_eq_programme" and prog == "E02":
        avoided_e02_main.append(red)
    lam = ", lambda = 5e+06" if typ == "cap_eq_programme" else ""
    r = REG.r(fnum(red, 1), where + ", reduction %", file,
              f"comparison = {comp}, column = base, type = {typ}{lam}, programme = {prog}: 100 x (1 - hr0)", red)
    return f"{hr} ({r})"


t2.append(["A. Recurrence HR" + sup(S2) + RED + " at which, in the base case,"])
bold2.add(len(t2) - 1)
XBF = "output/phase2/main/sc_base_crossings.csv"
t2.append([f"The maximum affordable cost equals the cost of the {PROG['E02']}",
           crossred(xb, XBF, "main", "cap_eq_programme", "E02", f"{T}, Panel A, cap = E02, main"),
           crossred(xb, XBF, "secondary", "cap_eq_programme", "E02", f"{T}, Panel A, cap = E02, secondary")])
for e in ("E01", "E02", "E03"):
    t2.append([f"Medical costs avoided{sup(S3)} equal the cost of the {PROG[e]}",
               crossred(xb, XBF, "main", "avoided_eq_programme", e, f"{T}, Panel A, avoided = {e}, main"),
               crossred(xb, XBF, "secondary", "avoided_eq_programme", e, f"{T}, Panel A, avoided = {e}, secondary")])

DCF, PSF = "output/phase2/main/det_caps.csv", "output/phase2/main/psa_caps_summary.csv"
BASE_ROW = "Base case, recurrence HR " + REG.label("0.85", f"{T}, Panels B and C row label", "recurrence HR of the base-case comparison row (Supplementary Table S4 grid point)")
t2.append(["B. Maximum affordable cost under alternative effect durations" + sup(S4)])
bold2.add(len(t2) - 1)
t2.append([BASE_ROW,
           capcell("main", 0.85, DCF, PSF, dc, ps, f"{T}, Panel B, base case, main (intended repeat of Supplementary Table S4)"),
           capcell("secondary", 0.85, DCF, PSF, dc, ps, f"{T}, Panel B, base case, secondary (intended repeat of Supplementary Table S4)")])
for key, scen in (("dur1", "path_a_s1"), ("dur2", "path_a_s2")):
    cells = []
    for comp in ("main", "secondary"):
        r = scap[(scap.scenario == scen) & (scap.comparison == comp) & (scap.axis == "hr0") & np.isclose(scap.x, 0.85)]
        assert len(r) == 1
        v = float(r.iloc[0].cap_500)
        cells.append(REG.r(fk(v), f"{T}, Panel B, {key}, {comp}", "output/phase2/main/scenario_caps.csv",
                           f"scenario = {scen}, comparison = {comp}, column = base, axis = hr0, x = 0.85, cap_500", v))
    t2.append([SC[key], *cells])
# check: the base row of scenario_caps.csv equals det_caps.csv at 0.85 (the base-case row)
for comp in ("main", "secondary"):
    a = scap[(scap.scenario == "base") & (scap.comparison == comp) & (scap.axis == "hr0") & np.isclose(scap.x, 0.85)].cap_500.iloc[0]
    b = dc[(dc.comparison == comp) & (dc.column == "base") & (dc.axis == "hr0") & np.isclose(dc.x, 0.85)].cap_500.iloc[0]
    assert abs(a - b) < 1e-6, (comp, a, b)
t2.append(["C. Metastatic treatment cost scenarios" + sup(S4)])
bold2.add(len(t2) - 1)
t2.append([BASE_ROW,
           capcell("main", 0.85, DCF, PSF, dc, ps, f"{T}, Panel C, base case, main (intended repeat of Supplementary Table S4)"),
           capcell("secondary", 0.85, DCF, PSF, dc, ps, f"{T}, Panel C, base case, secondary (intended repeat of Supplementary Table S4)")])
for key, pre in (("m50", "sc_metcost50"), ("eri", "sc_eribulin")):
    det_f, psa_f, x_f = (f"output/phase2/main/{pre}_{s}" for s in ("det_caps.csv", "psa_caps_summary.csv", "crossings.csv"))
    d_df, p_df, x_df = csv(f"{pre}_det_caps.csv"), csv(f"{pre}_psa_caps_summary.csv"), csv(f"{pre}_crossings.csv")
    t2.append([SC[key]])
    t2.append(["Maximum affordable cost",
               capcell("main", 0.85, det_f, psa_f, d_df, p_df, f"{T}, Panel C, {key}, cap, main"),
               capcell("secondary", 0.85, det_f, psa_f, d_df, p_df, f"{T}, Panel C, {key}, cap, secondary")])
    t2.append([f"Recurrence HR{RED} at which the maximum affordable cost equals the cost of the {PROG['E02']}",
               crossred(x_df, x_f, "main", "cap_eq_programme", "E02", f"{T}, Panel C, {key}, cap = E02, main"),
               crossred(x_df, x_f, "secondary", "cap_eq_programme", "E02", f"{T}, Panel C, {key}, cap = E02, secondary")])
    t2.append([f"Recurrence HR{RED} at which medical costs avoided{sup(S3)} equal the cost of the {PROG['E02']}",
               crossred(x_df, x_f, "main", "avoided_eq_programme", "E02", f"{T}, Panel C, {key}, avoided = E02, main"),
               crossred(x_df, x_f, "secondary", "avoided_eq_programme", "E02", f"{T}, Panel C, {key}, avoided = E02, secondary")])
assert len(avoided_e02_main) == 3
red_lo, red_hi = fnum(min(avoided_e02_main), 1), fnum(max(avoided_e02_main), 1)
REG.label("49", f"{T}, footnote", "starting age (Table 1)")
REG.label("5", f"{T}, title/footnote", "JPY 5 million per QALY threshold (analysis plan section 2: λ = 500 万日元/QALY) / 5-year base-case effect duration (Table 1)")
REG.label("2026", f"{T}, footnote", "price year (Table 1)")
REG.label("2", f"{T}, footnote", "discount rate (Table 1)")
REG.label("1,000", f"{T}, footnote/header", "number of PSA samples (Table 1) or the JPY 1,000 unit")
REG.label("2.5", f"{T}, footnote", "percentile definition of the UI (Table 1)")
REG.label("97.5", f"{T}, footnote", "percentile definition of the UI (Table 1)")
REG.label("95", f"{T}, footnote", "95% UI")
REG.label("1.00", f"{T}, footnote", "no-effect value of the HR (Table 1)")
REG.label("100", f"{T}, footnote", "reduction = 100 x (1 - HR)")
REG.label("1", f"{T}, footnote", "reduction = 100 x (1 - HR)")
assert (ps.n == 1000).all()

t2_title = ("Table 2. Recurrence hazard ratios at which exercise breaks even, and the maximum affordable cost of an exercise program per patient "
            "under alternative effect durations and metastatic treatment costs, at a willingness-to-pay threshold of JPY 5 million per " + "QALY" + sup(S1))
t2_notes = [
    f"{S1}Modeled cohort: women aged 49 years starting neoadjuvant chemotherapy for stage II or III triple-negative breast cancer in Japan (Table 1). Maximum affordable cost: the largest program cost per patient at which adding exercise remains cost-effective, equal to the threshold "
    "multiplied by the incremental QALYs minus the incremental medical costs other than the program cost (musculoskeletal adverse events of exercise included). "
    "Cells with a bracket show the deterministic estimate and the 95% UI [2.5th and 97.5th percentiles of 1,000 probabilistic sensitivity analysis samples]. "
    "Costs in JPY 1,000 at fiscal year 2026 prices, discounted at 2% per year over a lifetime horizon. "
    "HR, hazard ratio; JPY, Japanese yen; QALY, quality-adjusted life year; UI, uncertainty interval.",
    f"{S2}Hazard ratio for locoregional and distant recurrence after surgery in the arm with exercise, relative to the same treatment without exercise; 1.00 means no effect. "
    "The value in parentheses is the reduction in the recurrence hazard, 100 × (1 − HR), in %. "
    "In panels A and C the effect is held for 5 years after randomization and then halves every year (Table 1).",
    f"{S3}Reduction in lifetime medical costs other than the program cost. At recurrence HRs below these values, the arm with exercise has lower total costs, program included, and more QALYs. "
    f"The reductions of {red_lo}% to {red_hi}% at which medical costs avoided equal the program cost (base case and both metastatic cost scenarios) "
    f"hold only for exercise added to chemotherapy plus pembrolizumab with the {PROG['E02']}.",
    f"{S4}At a recurrence HR of 0.85. The base-case row repeats the base-case estimate (Supplementary Table {SUPP['capgrid']}) for comparison within the panel. "
    "Effect durations and cost scenarios are defined in Table 1. The alternative effect durations show deterministic estimates only (no probabilistic analysis was run for them); "
    "panel C keeps the base-case effect duration.",
]

# ================================================================ Table 3
T = "Table 3"
dec = csv("decomp_reference.csv")
dr = csv("det_reference.csv")
pr = csv("psa_reference_summary.csv")
srf = csv("scenario_reference.csv")
CAT = [("pembrolizumab_drug", "Pembrolizumab"), ("administration", "Drug administration"),
       ("immune_ae", "Immune-related adverse events"), ("chemo_ae", "Febrile neutropenia"),
       ("follow_up", "Follow-up"), ("lrr", "Locoregional recurrence"),
       ("dr_first_line", "Distant recurrence, first-line treatment"),
       ("dr_later_lines", "Distant recurrence, second-line and later treatment"),
       ("terminal_care", "End-of-life care"), ("other", "Other (chemotherapy drugs, supportive care, surgery, radiotherapy)")]
mult = {"m50": {"dr_first_line": PR.scenario("sc_metcost50", "D03")[1], "dr_later_lines": m50_mult},
        "eri": {"dr_later_lines": eri_mult}}
assert abs(PR.scenario("sc_metcost50", "D03P")[1] - PR.scenario("sc_metcost50", "D03")[1]) < 1e-12
scen_ref = {"m50": ("sc_metcost50", csv("sc_metcost50_det_reference.csv"), csv("sc_metcost50_psa_reference_summary.csv")),
            "eri": ("sc_eribulin", csv("sc_eribulin_det_reference.csv"), csv("sc_eribulin_psa_reference_summary.csv"))}
DECF = "output/phase2/main/decomp_reference.csv"
derived_check = {}
cols = ["base", "kext", "sjp", "m50", "eri"]
cat_vals = {c: {} for c in cols}
for cat, _ in CAT:
    r = one(dec, category=cat)
    cat_vals["base"][cat] = (float(r.d_base), DECF, f"category = {cat}, d_base")
    cat_vals["kext"][cat] = (float(r.d_kext), DECF, f"category = {cat}, d_kext")
    for s in ("m50", "eri"):
        f = mult[s].get(cat, 1.0)
        cat_vals[s][cat] = (float(r.d_base) * f, DECF,
                            f"category = {cat}, d_base" + (f" x scenario multiplier {f!r} ({XL} sheet シナリオ)" if f != 1.0 else " (unchanged in this scenario)"))
assert abs(sum(cat_vals["base"][c][0] for c, _ in CAT) - float(one(dec, category="total").d_base)) < 1e-6
for s in ("m50", "eri"):
    tot = sum(cat_vals[s][c][0] for c, _ in CAT)
    model_tot = float(one(scen_ref[s][1], column="base").dC)
    derived_check[s] = (tot, model_tot, tot - model_tot)
    if abs(tot - model_tot) > 1e-3:
        raise ValueError(f"derived decomposition does not reproduce the modeled total for {s}: {tot} vs {model_tot}")

hdr3 = ["Quantity", SC["base"], SC["kext"], SC["sjp"] + sup(S2), SC["m50"] + sup(S3), SC["eri"] + sup(S3)]
t3 = [hdr3]
bold3 = set()
t3.append(["A. Incremental costs by category"])
bold3.add(len(t3) - 1)
for cat, lab in CAT:
    row = [lab]
    for c in cols:
        if c == "sjp":
            row.append("—")
            continue
        v, f, loc = cat_vals[c][cat]
        row.append(REG.r(fk(v), f"{T}, Panel A, {cat}, {c}", f, loc + (" [derived; see check]" if c in ("m50", "eri") else ""), v))
    t3.append(row)


def det_psa(c):
    if c in ("base", "kext"):
        return one(dr, column=c), one(pr, column=c), "output/phase2/main/det_reference.csv", "output/phase2/main/psa_reference_summary.csv"
    if c == "sjp":
        return one(srf, scenario="sjp", column="base"), None, "output/phase2/main/scenario_reference.csv", None
    pre, ddf, pdf = scen_ref[c]
    return one(ddf, column="base"), one(pdf, column="base"), f"output/phase2/main/{pre}_det_reference.csv", f"output/phase2/main/{pre}_psa_reference_summary.csv"


def keyloc(c, f):
    return ("scenario = sjp, column = base" if c == "sjp" else ("column = " + (c if c in ("base", "kext") else "base")))


row_tot, row_q, row_icer, row_p5, row_p7 = ["Total"], ["Incremental QALYs"], ["ICER, JPY 1,000 per QALY"], \
    ["Probability cost-effective at JPY 5 million per QALY, %"], ["Probability cost-effective at JPY 7.5 million per QALY, %"]
for c in cols:
    d, p, fd, fp = det_psa(c)
    w = f"{T}, {c}"
    if p is not None:
        for est, lo, hi in ((d.dC, p.dC_lo, p.dC_hi), (d.dQ, p.dQ_lo, p.dQ_hi)):
            if not (lo <= est <= hi):
                raise ValueError(f"point estimate outside UI in {c}")
        row_tot.append(f"{REG.r(fk(d.dC), w + ', total', fd, keyloc(c, fd) + ', dC', d.dC)} "
                       f"[{REG.r(fk(p.dC_lo), w + ', total', fp, keyloc(c, fp) + ', dC_lo', p.dC_lo)}, {REG.r(fk(p.dC_hi), w + ', total', fp, keyloc(c, fp) + ', dC_hi', p.dC_hi)}]")
        row_q.append(f"{REG.r(fnum(d.dQ, 3), w + ', QALY', fd, keyloc(c, fd) + ', dQ', d.dQ)} "
                     f"[{REG.r(fnum(p.dQ_lo, 3), w + ', QALY', fp, keyloc(c, fp) + ', dQ_lo', p.dQ_lo)}, {REG.r(fnum(p.dQ_hi, 3), w + ', QALY', fp, keyloc(c, fp) + ', dQ_hi', p.dQ_hi)}]")
        row_p5.append(REG.r(pct(p.p_ce_500), w + ", P(CE) 5M", fp, keyloc(c, fp) + ", p_ce_500", p.p_ce_500))
        row_p7.append(REG.r(pct(p.p_ce_750), w + ", P(CE) 7.5M", fp, keyloc(c, fp) + ", p_ce_750", p.p_ce_750))
    else:
        row_tot.append(REG.r(fk(d.dC), w + ", total", fd, keyloc(c, fd) + ", dC", d.dC))
        row_q.append(REG.r(fnum(d.dQ, 3), w + ", QALY", fd, keyloc(c, fd) + ", dQ", d.dQ))
        row_p5.append("—")
        row_p7.append("—")
    row_icer.append(REG.r(fk(d.icer), w + ", ICER", fd, keyloc(c, fd) + ", icer", d.icer))
    if c in ("m50", "eri"):
        tot_derived = sum(cat_vals[c][k][0] for k, _ in CAT)
        assert abs(tot_derived - d.dC) < 1e-3
t3.append(row_tot)
t3.append(["B. Health outcomes and cost-effectiveness"])
bold3.add(len(t3) - 1)
t3 += [row_q, row_icer, row_p5, row_p7]
t3.append(["C. Exercise effect needed to match the QALY gain of pembrolizumab" + sup(S4)])
bold3.add(len(t3) - 1)
ys = csv("det_yardstick.csv")
yh, yp = one(ys, axis="hr0"), one(ys, axis="pcr")
assert np.isclose(yh.target_dQ, float(one(dr, column="base").dQ))
t3.append(["Recurrence HR with exercise added to chemotherapy alone",
           REG.r(fnum(yh.root, 3), f"{T}, Panel C, HR", "output/phase2/main/det_yardstick.csv", "axis = hr0, root", yh.root), "—", "—", "—", "—"])
t3.append(["Increase in pCR with exercise added to chemotherapy alone, percentage points",
           REG.r(fnum(100 * yp.root, 1), f"{T}, Panel C, pCR", "output/phase2/main/det_yardstick.csv", "axis = pcr, root x 100", 100 * yp.root), "—", "—", "—", "—"])
for tok, why in (("5", "JPY 5 million threshold"), ("7.5", "JPY 7.5 million threshold (analysis plan section 1)"), ("1,000", "JPY 1,000 unit / 1,000 PSA samples"),
                 ("2.5", "UI percentile"), ("97.5", "UI percentile"), ("95", "95% UI"), ("2026", "price year"), ("2", "discount rate"),
                 ("0.70", "lower end of the HR range (Table 1)"), ("1.00", "upper end of the HR range (Table 1)"),
                 ("0", "lower end of the pCR range in Table 1"), ("10", "upper end of the pCR range in Table 1"), ("0.5", "multiplier in Table 1"), ("49", "starting age (Table 1)")):
    REG.label(tok, f"{T}, title/footnotes", why)
assert (pr.n == 1000).all()

t3_title = ("Table 3. Incremental costs, QALYs and cost-effectiveness of pembrolizumab added to neoadjuvant chemotherapy, "
            "and the exercise effect that would match its QALY " + "gain" + sup(S1))
t3_notes = [
    f"{S1}Modeled cohort: women aged 49 years starting neoadjuvant chemotherapy for stage II or III triple-negative breast cancer in Japan (Table 1). Chemotherapy plus pembrolizumab compared with chemotherapy alone. Cells show deterministic estimates; where probabilistic analysis was run, the 95% UI "
    "[2.5th and 97.5th percentiles of 1,000 probabilistic sensitivity analysis samples] follows in brackets. Probability cost-effective: share of samples with a positive net monetary benefit. "
    "Costs in JPY 1,000 at fiscal year 2026 prices, discounted at 2% per year over a lifetime horizon; categories may not add to the total because of rounding. "
    "Scenarios are defined in Table 1. A dash means not computed. "
    "HR, hazard ratio; ICER, incremental cost-effectiveness ratio; JPY, Japanese yen; pCR, pathological complete response; "
    "QALY, quality-adjusted life year; UI, uncertainty interval.",
    f"{S2}Probabilistic analysis and the cost decomposition were not run for this scenario.",
    f"{S3}Category values equal the base-case values with the distant-recurrence treatment costs multiplied by the scenario factor in Table 1 (survival is unchanged); they add to the modeled total.",
    f"{S4}Effect at which exercise added to chemotherapy alone yields the same incremental QALYs as pembrolizumab in the base case. "
    f"Both values lie outside the ranges studied: recurrence HR 0.70 to 1.00 (Supplementary Table {SUPP['capgrid']}) and pCR increase 0 to 10 percentage points (Supplementary Table {SUPP['pathB']}).",
]

# ================================================================ write docx
doc = new_document(landscape=True)
para(doc, "Table 1. Key model " + "inputs" + sup(S1), space_after=6)
table(doc, t1, bold_rows=bold1)
for n in t1_notes:
    para(doc, n)
new_section(doc, landscape=True)
para(doc, t2_title, space_after=6)
table(doc, t2, bold_rows=bold2)
for n in t2_notes:
    para(doc, n)
new_section(doc, landscape=True)
para(doc, t3_title, space_after=6)
table(doc, t3, bold_rows=bold3)
for n in t3_notes:
    para(doc, n)
OUT.mkdir(parents=True, exist_ok=True)
doc.save(BUILD / "tables_marked.docx")

json.dump({"rows": REG.rows, "labels": REG.labels,
           "derived_check": {k: dict(sum_of_categories=v[0], modelled_total=v[1], difference=v[2]) for k, v in derived_check.items()}},
          open(BUILD / "_ledger_tables.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
print("_build/tables_marked.docx written;", len(REG.rows), "registered numbers,", len(REG.labels), "labels")
print("derived decomposition check (yen):", {k: round(v[2], 9) for k, v in derived_check.items()})
