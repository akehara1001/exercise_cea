"""Supplementary tables, figures and methods (supplement_<VER>.docx).

Reads the phase 1 and phase 2 outputs, the parameter workbook and the figure
files written by make_figures.py; does not run the model. The CHEERS checklist
(Supplementary Table S1) gives for each item its place in the manuscript, read from
_build/_manuscript_map.json (written by edit_manuscript.py) and the page numbers in
_build/_manuscript_pages.json (word_pages.ps1); run this script again once both exist.
Writes _build/supplement_marked.docx with reference markers (number_refs.py writes
manuscript/<VER>/supplement_<VER>.docx) and _build/_ledger_supplement.json.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from docx.shared import Mm

from common import (BUILD, FIGDIR, MAIN, OUT, P1, ROOT, STAR, SUPP, VER, Params, Registry,
                    csv, fk, fnum, fyen, num_tokens, one, pct, rel)
from docx_util import new_document, new_section, page_break, para, table
from param_names import ARM, RANGE_RULE, UNIT, item, source
from references import cite

sys.stdout.reconfigure(encoding="utf-8")
REG = Registry()
PR = Params()
S = {i: STAR * i for i in range(1, 7)}
XL = "input/params/parameters_v10.xlsx"
ARM_MAIN = "Exercise added to chemotherapy plus pembrolizumab"
ARM_SEC = "Exercise added to chemotherapy alone"
KEXT = "Higher mortality after early recurrence with pembrolizumab"
COHORT = ("Modeled cohort: women aged 49 years starting neoadjuvant chemotherapy for stage II or III triple-negative breast cancer in Japan "
          "(Table 1). ")
COSTS = "Costs in JPY 1,000 at fiscal year 2026 prices, discounted at 2% per year over a lifetime horizon. "
UI = "95% UI: 2.5th and 97.5th percentiles of 1,000 probabilistic sensitivity analysis samples. "


def sup(sym):
    return "^{" + sym + "}"


def lab(tok, where, why):
    return REG.label(tok, where, why)


def sig4(v):
    """Four significant digits (distribution parameters only)."""
    if v == 0:
        return "0"
    nd = max(4 - 1 - int(math.floor(math.log10(abs(v)))), 0)
    return fnum(v, nd)


def fval(v, unit):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    if unit.startswith("JPY"):
        return fyen(v)
    if unit in ("utility", "utility decrement", "events per patient"):
        return fnum(v, 3)
    if unit in ("HR", "months"):
        return fnum(v, 2)
    if unit == "proportion":
        return fnum(v, 5)
    raise ValueError(unit)


UNITS = []  # (title paragraph, [(rows, bold_rows)], notes, landscape)


def add_unit(title, tables, notes, landscape=True):
    UNITS.append((title, tables, notes, landscape))


# ================================================================ S1  all inputs
T = f"Supplementary Table {SUPP['params']}"
pc = one(csv("pcr_counts.csv", ROOT / "data"), source="K22 (IA4)")
f7 = csv("kn522_final_7y.csv", ROOT / "data")
cal = csv("calibration.csv", P1)
calr = cal[(cal.stage == "calibrated") & (cal.arm == "pembro")].iloc[0]
bs = csv("bootstrap_summary.csv", P1)
ex = pd.read_csv(BUILD / "engine_params_extract.csv")
aed = csv("ae_deaths.csv", P1)
kx = csv("kext_derivation.csv", P1 / "round14")
pps = csv("preprog_survival.csv", P1 / "round15")
EXF = "manuscript/code/_build/engine_params_extract.csv (from data/fits/engine_params.rds)"


def exv(q, arm):
    return float(ex[(ex.quantity == q) & (ex.arm == arm)].value.iloc[0])


def bsr(q, scale=1.0, nd=2):
    r = one(bs, quantity=q)
    lo = REG.r(fnum(r.boot_lo * scale, nd), f"{T}, Panel A, {q}, 2.5th", "output/phase1/bootstrap_summary.csv", f"quantity = {q}, boot_lo" + (f" x {scale}" if scale != 1 else ""), r.boot_lo * scale)
    hi = REG.r(fnum(r.boot_hi * scale, nd), f"{T}, Panel A, {q}, 97.5th", "output/phase1/bootstrap_summary.csv", f"quantity = {q}, boot_hi" + (f" x {scale}" if scale != 1 else ""), r.boot_hi * scale)
    return f"{lo} to {hi}"


A = [["Input", "Arms", "Base case", "Bootstrap 2.5th to 97.5th percentile", "Source"]]
nP, nPn, nC, nCn = int(pc.pcr_pembro), int(pc.nonpcr_pembro), int(pc.pcr_placebo), int(pc.nonpcr_placebo)
A.append(["Starting age, years", "All arms",
          REG.r(fnum(exv("start_age", "all"), 0), f"{T}, Panel A, starting age", EXF, "quantity = start_age", exv("start_age", "all")), "—", "KEYNOTE-522 population" + cite("schmid2020")])
for arm, n1, n0, lab_ in (("pembro", nP, nPn, "With pembrolizumab"), ("placebo", nC, nCn, "Without pembrolizumab")):
    A.append(["Pathological complete response (pCR)", lab_,
              f"{REG.r(str(n1), f'{T}, Panel A, pCR {arm}', 'data/pcr_counts.csv', f'row K22 (IA4), pcr_{arm}', n1)}/"
              f"{REG.r(str(n1 + n0), f'{T}, Panel A, pCR {arm}', 'data/pcr_counts.csv', f'row K22 (IA4), pcr_{arm} + nonpcr_{arm}', n1 + n0)} "
              f"({REG.r(pct(n1 / (n1 + n0)), f'{T}, Panel A, pCR {arm}', 'data/pcr_counts.csv', 'pcr / (pcr + nonpcr)', n1 / (n1 + n0))}%)",
              "—", "KEYNOTE-522 (interim analysis 4)" + cite("schmid2022")])
for arm, lab_ in (("pembro", "With pembrolizumab"), ("placebo", "Without pembrolizumab")):
    for strat, sname in (("pCR", "pCR"), ("nonpCR", "no pCR")):
        tid = f"efs_{'pcr' if strat == 'pCR' else 'nonpcr'}_{arm}"
        v = float(one(f7, id=tid).value)
        q = f"efs_target_EFS_{arm}_{strat}"
        A.append([f"Event-free survival at 7 years, {sname} (fixed in fitting)", lab_,
                  REG.r(fnum(v, 1), f"{T}, Panel A, {tid}", "data/kn522_final_7y.csv", f"id = {tid}, value", v) + "%",
                  bsr(q, 1.0, 1) + "%", "KEYNOTE-522 final analysis" + cite("kn522final2026")])
for arm, lab_ in (("pembro", "With pembrolizumab"), ("placebo", "Without pembrolizumab")):
    for strat, sname, fam in (("pCR", "pCR", "Weibull"), ("nonpCR", "no pCR", "Weibull cure model")):
        for par in (["shape", "scale"] if strat == "pCR" else ["theta", "shape", "scale"]):
            q = f"EFS_{arm}_{strat}_{par}"
            r = one(bs, quantity=q)
            pname = {"theta": "cure fraction", "shape": "shape", "scale": "scale (years)"}[par]
            A.append([f"Event-free survival after surgery, {sname}: {fam}, {pname}", lab_,
                      REG.r(sig4(r.base), f"{T}, Panel A, {q}", "output/phase1/bootstrap_summary.csv", f"quantity = {q}, base", r.base),
                      f"{REG.r(sig4(r.boot_lo), f'{T}, Panel A, {q}', 'output/phase1/bootstrap_summary.csv', f'quantity = {q}, boot_lo', r.boot_lo)} to "
                      f"{REG.r(sig4(r.boot_hi), f'{T}, Panel A, {q}', 'output/phase1/bootstrap_summary.csv', f'quantity = {q}, boot_hi', r.boot_hi)}",
                      "Fitted to reconstructed KEYNOTE-522 data (interim analysis 4)" + cite("guyot2012", "schmid2022")])
for arm, lab_ in (("pembro", "With pembrolizumab"), ("placebo", "Without pembrolizumab")):
    v = exv("preprog_share_nonpcr", arm)
    A.append(["Progression precluding surgery, proportion of patients without pCR", lab_,
              REG.r(pct(v, 2), f"{T}, Panel A, preprog {arm}", EXF, f"quantity = preprog_share_nonpcr, arm = {arm}", v) + "%", "—", "KEYNOTE-522 (2024 report)" + cite("schmid2024")])
for arm, lab_ in (("pembro", "With pembrolizumab"), ("placebo", "Without pembrolizumab")):
    parts = []
    for comp, cname in (("LRR", "locoregional recurrence"), ("DR", "distant recurrence"), ("death", "death without recurrence")):
        v = exv(f"first_event_share_{comp}", arm)
        parts.append(f"{cname} {REG.r(pct(v, 1), f'{T}, Panel A, first events {arm}', EXF, f'quantity = first_event_share_{comp}, arm = {arm}', v)}%")
    A.append(["Composition of first events after surgery", lab_, "; ".join(parts), "—", "KEYNOTE-522 (2024 report)" + cite("schmid2024")])
for arm, lab_ in (("pembro", "With pembrolizumab"), ("placebo", "Without pembrolizumab")):
    r = one(aed, arm=arm)
    A.append(["Deaths from adverse events during treatment", lab_,
              f"{REG.r(str(int(r.deaths)), f'{T}, Panel A, AE deaths {arm}', 'output/phase1/ae_deaths.csv', f'arm = {arm}, deaths', r.deaths)}/"
              f"{REG.r(str(int(r.n_treated)), f'{T}, Panel A, AE deaths {arm}', 'output/phase1/ae_deaths.csv', f'arm = {arm}, n_treated', r.n_treated)}",
              "—", "KEYNOTE-522 (interim analysis 4)" + cite("schmid2022")])
A.append(["Locoregional to distant recurrence, rate per year", "All arms",
          f"{REG.r(fnum(exv('lrr_dr_rate_per_year', 'all'), 3), f'{T}, Panel A, LRR to DR', EXF, 'quantity = lrr_dr_rate_per_year', exv('lrr_dr_rate_per_year', 'all'))} "
          f"({REG.r(fnum(exv('lrr_dr_n_local_then_distant', 'all'), 0), f'{T}, Panel A, LRR to DR', EXF, 'quantity = lrr_dr_n_local_then_distant', exv('lrr_dr_n_local_then_distant', 'all'))} of "
          f"{REG.r(fnum(exv('lrr_dr_n_local', 'all'), 0), f'{T}, Panel A, LRR to DR', EXF, 'quantity = lrr_dr_n_local', exv('lrr_dr_n_local', 'all'))} patients; "
          f"{REG.r(fnum(exv('lrr_dr_exposure_years', 'all'), 2), f'{T}, Panel A, LRR to DR', EXF, 'quantity = lrr_dr_exposure_years', exv('lrr_dr_exposure_years', 'all'))} years of follow-up)",
          "—", "KEYNOTE-522 (2022 report)" + cite("schmid2022")])
for q, name, col in (("dr_median", "Excess mortality after distant recurrence within 18 months of randomization: log-logistic median, months", "dr_median_months"),
                     ("dr_late_median", "Excess mortality after later distant recurrence: log-logistic median, months", "dr_late_median_months"),
                     ("dr_shape", "Excess mortality after distant recurrence or progression during neoadjuvant therapy: common log-logistic shape", "dr_shape")):
    v = float(calr[col])
    nd = 3 if q == "dr_shape" else 2
    scale = 1.0 if q == "dr_shape" else 12.0
    A.append([name, "All arms", REG.r(fnum(v, nd), f"{T}, Panel A, {q}", "output/phase1/calibration.csv", f"stage = calibrated, arm = pembro, {col}", v),
              bsr(q, scale, nd), "ESME cohort, reconstructed overall survival" + cite("grinda2023", "guyot2012")])
lab("18", T, "early distant recurrence cut-off (Table 1)")
A.append(["Excess mortality after progression during neoadjuvant therapy", "All arms", "Same as distant recurrence within the first 18 months", "As above", "ESME cohort" + cite("grinda2023")])
A.append(["Background mortality", "All arms", "Japanese women", "—", "Abridged life table (2025)" + cite("lifetable2025")])
kv = float(one(kx, quantity="k_external").value)
A.append([f"Scenario: {KEXT}, multiplier", "With pembrolizumab",
          REG.r(fnum(kv, 3), f"{T}, Panel A, k", "output/phase1/round14/kext_derivation.csv", "quantity = k_external, value", kv), "—",
          "Italian real-world cohort after neoadjuvant pembrolizumab" + cite("fedele2026")])
ev = float(pps[pps.setting.str.contains("Elmore")].median_months.iloc[0])
A.append(["Scenario: progression during neoadjuvant therapy with longer survival, log-logistic median, months", "All arms",
          REG.r(fnum(ev, 0), f"{T}, Panel A, Elmore", "output/phase1/round15/preprog_survival.csv", "setting = round 15 scenario Elmore, median_months", ev), "—",
          "Single-center cohort with locoregional progression during neoadjuvant therapy" + cite("elmore2021")])
for tok in ("49", "7", "2024", "2022", "2025", "4"):
    lab(tok, T, "definition or name (Table 1; report years)")

# Panel B: parameter workbook rows
dist = pd.read_csv(ROOT / "data" / "params_dist.csv")
B = [["Code", "Input", "Arms", "Unit", "Base case", "Range", "Distribution", "Source"]]
prev_src = None
for i, r in enumerate(PR.ws.iter_rows(min_row=2, values_only=True), start=2):
    pid = r[0]
    if not pid:
        continue
    unit = UNIT[r[5]]
    d = one(dist, param_id=pid)
    src = source(r[10], prev_src)
    prev_src = src
    base = REG.r(fval(r[6], unit), f"{T}, Panel B, {pid}, base", XL, f"sheet パラメータ cell G{i} ({pid})", r[6])
    lo = REG.r(fval(r[7], unit), f"{T}, Panel B, {pid}, low", XL, f"sheet パラメータ cell H{i} ({pid})", r[7])
    hi = REG.r(fval(r[8], unit), f"{T}, Panel B, {pid}, high", XL, f"sheet パラメータ cell I{i} ({pid})", r[8])
    rule = d.range_rule if isinstance(d.range_rule, str) else ""
    rng = f"{lo} to {hi}" + (f" [{RANGE_RULE[rule]}]" if rule else "")
    if d.dist == "fixed":
        dd = "Fixed"
    else:
        p1 = REG.r(sig4(d.p1), f"{T}, Panel B, {pid}, p1", "data/params_dist.csv", f"param_id = {pid}, p1", d.p1)
        p2 = REG.r(sig4(d.p2), f"{T}, Panel B, {pid}, p2", "data/params_dist.csv", f"param_id = {pid}, p2", d.p2)
        dd = {"gamma": f"Gamma (shape {p1}, scale {p2})", "beta": f"Beta (alpha {p1}, beta {p2})",
              "lognormal": f"Lognormal (meanlog {p1}, sdlog {p2})"}[d.dist]
    B.append([pid, item(pid), ARM[r[3]], unit, base, rng, dd, src])
    for tok in num_tokens(src):
        lab(tok, f"{T}, Panel B source column", "bibliographic detail (volume, pages, DOI, PMID or year) of the cited source")
for tok, why in (("25", "±25% rule"), ("75", "drug price rule"), ("12.5", "U05 duration (Table 1)"), ("6", "6-month program (Table 1)"),
                 ("3", "3 months of end-of-life care (Table 1)"), ("12", "12 weeks (A01)"), ("4", "4 cycles (A02)"), ("1", "type 1 diabetes / years 1 to 2"),
                 ("2", "years 1 to 2"), ("5", "years 3 to 5 / EQ-5D"), ("2026", "fiscal year / report years"), ("2017", "citation year"), ("2020", "citation year"),
                 ("2007", "citation year"), ("2018", "citation year"), ("2021", "citation year"), ("2023", "guideline year"), ("2024", "PPP year"), ("2025", "citation year")):
    lab(tok, f"{T}, Panel B labels", why)
add_unit(f"{T}. All model " + "inputs" + sup(S[1]),
         [(["A. Survival and model structure"], A, {0}), (["B. Costs, adverse events, utilities, exercise and post-operative treatment"], B, {0})],
         [f"{S[1]}" + COHORT + "Costs are in JPY at fiscal year 2026 prices except the CHALLENGE-based supervised program (converted from 2024 Canadian dollars; Table 1). "
          "Panel A: base-case values of the survival model and the 2.5th to 97.5th percentiles across 1,000 bootstrap replicates (dash, fixed in all replicates). "
          "Panel B: ranges are those of the one-way sensitivity analysis and, for distributions other than fixed, the 95% range of the probabilistic analysis; "
          "brackets mark ranges set by rule: [±25% (assumed)], ±25% around the base value; [mirrored (assumed)], the missing bound mirrored; "
          "[drug price, lower only], lower bound 75% of the list price and the value fixed in the probabilistic analysis; [zero events, fixed in PSA], upper bound from zero events. "
          "Inputs with suffix P or C apply to arms with or without pembrolizumab. "
          "AE, adverse event; BRCA, breast cancer gene; ESME, Epidemiological Strategy and Medical Economics database; G-CSF, granulocyte colony-stimulating factor; "
          "HR, hazard ratio; JPY, Japanese yen; pCR, pathological complete response; PSA, probabilistic sensitivity analysis; TNBC, triple-negative breast cancer."])

# ================================================================ S2  validation
T = f"Supplementary Table {SUPP['validation']}"
g = csv("calibration_gate.csv", P1)
GA = [["Year", "Kaplan-Meier, chemotherapy plus pembrolizumab [95% CI]", "Model, chemotherapy plus pembrolizumab", "Kaplan-Meier, chemotherapy alone [95% CI]", "Model, chemotherapy alone"]]
for m in (12, 24, 36, 48, 60):
    row = [REG.r(str(m // 12), f"{T}, Panel A, year", "output/phase1/calibration_gate.csv", f"month = {m} / 12", m // 12)]
    for arm in ("pembro", "placebo"):
        r = one(g, arm=arm, month=m)
        kmv = REG.r(fnum(r.km, 1), f"{T}, Panel A, {arm} {m}", "output/phase1/calibration_gate.csv", f"arm = {arm}, month = {m}, km", r.km)
        lo = REG.r(fnum(r.ci95_lo, 1), f"{T}, Panel A, {arm} {m}", "output/phase1/calibration_gate.csv", f"arm = {arm}, month = {m}, ci95_lo", r.ci95_lo)
        hi = REG.r(fnum(r.ci95_hi, 1), f"{T}, Panel A, {arm} {m}", "output/phase1/calibration_gate.csv", f"arm = {arm}, month = {m}, ci95_hi", r.ci95_hi)
        eng = REG.r(fnum(r.engine, 1), f"{T}, Panel A, {arm} {m}", "output/phase1/calibration_gate.csv", f"arm = {arm}, month = {m}, engine", r.engine)
        row += [f"{kmv} [{lo}, {hi}]", eng + ("" if bool(r.inside) else sup(S[2]))]
    GA.append(row)
gr = csv("calibration_gate_rmst.csv", P1).iloc[0]
GB = [["Quantity", "Kaplan-Meier [bootstrap 95% CI]", "Model"],
      ["Difference in 5-year restricted mean survival time, years",
       f"{REG.r(fnum(gr.km, 4), f'{T}, Panel B', 'output/phase1/calibration_gate_rmst.csv', 'km', gr.km)} "
       f"[{REG.r(fnum(gr.km_boot_ci95_lo, 4), f'{T}, Panel B', 'output/phase1/calibration_gate_rmst.csv', 'km_boot_ci95_lo', gr.km_boot_ci95_lo)}, "
       f"{REG.r(fnum(gr.km_boot_ci95_hi, 4), f'{T}, Panel B', 'output/phase1/calibration_gate_rmst.csv', 'km_boot_ci95_hi', gr.km_boot_ci95_hi)}]",
       REG.r(fnum(gr.engine, 4), f"{T}, Panel B", "output/phase1/calibration_gate_rmst.csv", "engine", gr.engine)]]
fy = csv("calibration_final7y.csv", P1)
GC = [["Quantity at 7 years", "Arm", "Final analysis [95% CI]", "Model"]]
for idv, qn, armn in (("os7_pembro", "Overall survival, %", "Chemotherapy plus pembrolizumab"), ("os7_placebo", "Overall survival, %", "Chemotherapy alone"),
                      ("efs7_pembro", "Event-free survival, %", "Chemotherapy plus pembrolizumab"), ("efs7_placebo", "Event-free survival, %", "Chemotherapy alone"),
                      ("os_pcr_pembro", "Overall survival with pCR, %", "Chemotherapy plus pembrolizumab"), ("os_pcr_placebo", "Overall survival with pCR, %", "Chemotherapy alone"),
                      ("os_nonpcr_pembro", "Overall survival without pCR, %", "Chemotherapy plus pembrolizumab"), ("os_nonpcr_placebo", "Overall survival without pCR, %", "Chemotherapy alone")):
    r = one(fy, id=idv)
    rep = REG.r(fnum(r.value, 1), f"{T}, Panel C, {idv}", "output/phase1/calibration_final7y.csv", f"id = {idv}, value", r.value)
    if not np.isnan(r.ci95_lo):
        rep += f" [{REG.r(fnum(r.ci95_lo, 1), f'{T}, Panel C, {idv}', 'output/phase1/calibration_final7y.csv', f'id = {idv}, ci95_lo', r.ci95_lo)}, " \
               f"{REG.r(fnum(r.ci95_hi, 1), f'{T}, Panel C, {idv}', 'output/phase1/calibration_final7y.csv', f'id = {idv}, ci95_hi', r.ci95_hi)}]"
    else:
        rep += sup(S[3])
    GC.append([qn, armn, rep, REG.r(fnum(r.engine, 1), f"{T}, Panel C, {idv}", "output/phase1/calibration_final7y.csv", f"id = {idv}, engine", r.engine)])
GD = [["Quantity", "Arm", "10 years [bootstrap 2.5th to 97.5th percentile]", "20 years [bootstrap 2.5th to 97.5th percentile]"]]
for ep, epn in (("OS", "Overall survival, %"), ("EFS", "Event-free survival, %")):
    for arm, armn in (("pembro", "Chemotherapy plus pembrolizumab"), ("chemo", "Chemotherapy alone")):
        row = [epn, armn]
        for yr in (10, 20):
            q = f"{ep}_{yr}y_{arm}_all"
            r = one(bs, quantity=q)
            row.append(f"{REG.r(fnum(r.base, 1), f'{T}, Panel D, {q}', 'output/phase1/bootstrap_summary.csv', f'quantity = {q}, base', r.base)} "
                       f"[{REG.r(fnum(r.boot_lo, 1), f'{T}, Panel D, {q}', 'output/phase1/bootstrap_summary.csv', f'quantity = {q}, boot_lo', r.boot_lo)}, "
                       f"{REG.r(fnum(r.boot_hi, 1), f'{T}, Panel D, {q}', 'output/phase1/bootstrap_summary.csv', f'quantity = {q}, boot_hi', r.boot_hi)}]")
        GD.append(row)
for tok in ("95", "99.5", "5", "7", "10", "20", "2.5", "97.5", "1,000", "2024", "14", "2025", "4"):
    lab(tok, T, "definitions, cut-off date and percentiles")
add_unit(f"{T}. Comparison of the survival model with KEYNOTE-522 overall survival and event-free " + "survival" + sup(S[1]),
         [(["A. Overall survival, %, at years 1 to 5"], GA, {0}), (["B. Restricted mean survival time"], GB, {0}),
          (["C. Final analysis at 7 years"], GC, {0}), (["D. Model extrapolation"], GD, {0})],
         [f"{S[1]}Kaplan-Meier estimates from patient-level data reconstructed from the published KEYNOTE-522 curves (overall survival, 2024 report)" + cite("guyot2012", "schmid2024") + "; "
          "final analysis" + cite("kn522final2026") + ": data cutoff 14 October 2025. Overall survival was not used to fit the model; event-free survival at 7 years in each pCR stratum was fixed at the final-analysis values during fitting (Table 1); the model was accepted if the 10 points of panel A lay within "
          "their pointwise 95% CIs or within Bonferroni-adjusted 99.5% CIs, the difference in panel B lay within its bootstrap 95% CI, and the four 7-year values with a CI "
          "in panel C lay within their 95% CIs. Panel D: 2.5th and 97.5th percentiles across 1,000 bootstrap replicates. "
          "CI, confidence interval; pCR, pathological complete response.",
          f"{S[2]}Outside the pointwise 95% CI and within the Bonferroni-adjusted 99.5% CI.",
          f"{S[3]}No CI reported; shown for comparison only and not part of the acceptance rule."])

# ================================================================ S4  cap grid (data of Fig. 2)
T = f"Supplementary Table {SUPP['capgrid']}"
dc, ps = csv("det_caps.csv"), csv("psa_caps_summary.csv")


def capui(df_d, df_p, comp, col, axis, x, lam, where, fd, fp):
    d = df_d[(df_d.comparison == comp) & (df_d.column == col) & (df_d.axis == axis) & np.isclose(df_d.x, x)].iloc[0]
    p = df_p[(df_p.comparison == comp) & (df_p.column == col) & (df_p.axis == axis) & np.isclose(df_p.x, x)].iloc[0]
    dv, lo, hi = d[f"cap_{lam}"], p[f"cap{lam}_lo"], p[f"cap{lam}_hi"]
    assert lo <= dv <= hi, (comp, col, axis, x, lam)
    loc = f"comparison = {comp}, column = {col}, axis = {axis}, x = {x:.3f}"
    return (f"{REG.r(fk(dv), where, fd, loc + f', cap_{lam}', dv)} [{REG.r(fk(lo), where, fp, loc + f', cap{lam}_lo', lo)}, "
            f"{REG.r(fk(hi), where, fp, loc + f', cap{lam}_hi', hi)}]",
            REG.r(pct(p[f"p_cap{lam}_ge_E02"]), where + ", P", fp, loc + f", p_cap{lam}_ge_E02", p[f"p_cap{lam}_ge_E02"]))


def grid_panels(axis, xs, xfmt, xlabel):
    panels = []
    for lam, laml in ((500, "A. Threshold JPY 5 million per QALY"), (750, "B. Threshold JPY 7.5 million per QALY")):
        hdr = [xlabel, ARM_MAIN + ", base case", ARM_MAIN + ", " + KEXT[0].lower() + KEXT[1:], ARM_SEC,
               "Probability above the fee-schedule-based program cost, %: " + ARM_MAIN.lower() + ", base case",
               "Same, " + KEXT[0].lower() + KEXT[1:], "Same, " + ARM_SEC.lower()]
        rows = [hdr]
        for x in xs:
            cells, probs = [], []
            for comp, col in (("main", "base"), ("main", "kext"), ("secondary", "base")):
                c, pr = capui(dc, ps, comp, col, axis, x, lam, f"{T}, {laml[:1]}, {axis} {x:.3f}, {comp} {col}",
                              "output/phase2/main/det_caps.csv", "output/phase2/main/psa_caps_summary.csv")
                cells.append(c)
                probs.append(pr)
            rows.append([xfmt(x)] + cells + probs)
        panels.append(([laml], rows, {0}))
    return panels


TB = f"Supplementary Table {SUPP['pathB']}"
hr_grid = sorted(dc[(dc.axis == "hr0") & (dc.comparison == "main") & (dc.column == "base")].x.round(3).unique())
assert len(hr_grid) == 13
add_unit(f"{T}. Maximum affordable cost of an exercise program per patient by the recurrence hazard ratio with " + "exercise" + sup(S[1]),
         grid_panels("hr0", hr_grid, lambda x: REG.r(fnum(x, 3), f"{T}, row label", "output/phase2/main/det_caps.csv", "x (hr0 grid)", x), "Recurrence HR"),
         [f"{S[1]}" + COHORT + "Data of Fig. 2. Cells show the deterministic estimate and the 95% UI. " + UI + COSTS +
          f"The effect is held for 5 years after randomization and then halves every year. {KEXT}: Table 1. "
          "Probability above the fee-schedule-based program cost: share of samples in which the maximum affordable cost exceeds the base-case cost of that program (Table 1). "
          "HR, hazard ratio; JPY, Japanese yen; QALY, quality-adjusted life year; UI, uncertainty interval."])
for tok in ("5", "7.5", "95", "2.5", "97.5", "1,000", "2026", "2", "49"):
    lab(tok, T, "threshold, percentiles, price year, discount rate")

# ================================================================ S5  cost decomposition, main comparison, HR 0.85
T = f"Supplementary Table {SUPP['decomp']}"
dm = csv("decomp_main_hr085.csv")
CATS = [("exercise_programme", "Exercise program (fee-schedule-based program)"), ("exercise_ae", "Musculoskeletal adverse events of exercise"),
        ("pembrolizumab_drug", "Pembrolizumab"), ("administration", "Drug administration"), ("immune_ae", "Immune-related adverse events"),
        ("chemo_ae", "Febrile neutropenia"), ("follow_up", "Follow-up"), ("lrr", "Locoregional recurrence"),
        ("dr_first_line", "Distant recurrence, first-line treatment"), ("dr_later_lines", "Distant recurrence, second-line and later treatment"),
        ("terminal_care", "End-of-life care"), ("other", "Other (chemotherapy drugs, supportive care, surgery, radiotherapy)"),
        ("total", "Total, fee-schedule-based program"), ("total_without_programme", "Total without the program cost" + sup(S[2])),
        ("total_with_E01", "Total, CHALLENGE-based supervised program"), ("total_with_E03", "Total, remote low-cost program")]
D5 = [["Category", "Base case", KEXT]]
for cat, labl in CATS:
    r = one(dm, category=cat)
    D5.append([labl] + [REG.r(fk(r[c]), f"{T}, {cat}, {c}", "output/phase2/main/decomp_main_hr085.csv", f"category = {cat}, {c}", r[c]) for c in ("d_base", "d_kext")])
chk = sum(one(dm, category=c).d_base for c, _ in CATS[:12])
assert abs(chk - one(dm, category="total").d_base) < 1e-3
add_unit(f"{T}. Incremental costs by category for exercise added to chemotherapy plus pembrolizumab at a recurrence hazard ratio of " + "0.85" + sup(S[1]),
         [(["Incremental cost, JPY 1,000"], D5, {0})],
         [f"{S[1]}" + COHORT + "Exercise added to chemotherapy plus pembrolizumab compared with chemotherapy plus pembrolizumab; negative values are costs avoided. "
          "Deterministic estimates. " + COSTS + "The effect is held for 5 years after randomization and then halves every year. "
          "Categories may not add to the totals because of rounding. JPY, Japanese yen.",
          f"{S[2]}Equals minus the medical costs avoided (Table 2)."])
for tok in ("0.85", "5", "2026", "2", "49", "1,000"):
    lab(tok, T, "definitions")

# ================================================================ S6  effect duration, full grid
T = f"Supplementary Table {SUPP['duration']}"
sc = csv("scenario_caps.csv")
D6 = []
for lam, laml in ((500, "A. Threshold JPY 5 million per QALY"), (750, "B. Threshold JPY 7.5 million per QALY")):
    hdr = ["Recurrence HR"]
    for scen, sname in (("path_a_s1", "Effect until 1 year after surgery"), ("path_a_s2", "No waning"), ("continue_s1", "Exercise continued after surgery")):
        hdr += [f"{sname}: main comparison", f"{sname}: secondary comparison"]
    rows = [hdr]
    for x in hr_grid:
        row = [fnum(x, 3)]
        for scen in ("path_a_s1", "path_a_s2", "continue_s1"):
            for comp in ("main", "secondary"):
                r = sc[(sc.scenario == scen) & (sc.comparison == comp) & (sc.axis == "hr0") & np.isclose(sc.x, x)]
                assert len(r) == 1
                v = float(r.iloc[0][f"cap_{lam}"])
                row.append(REG.r(fk(v), f"{T}, {laml[:1]}, {scen}, {comp}, {x:.3f}", "output/phase2/main/scenario_caps.csv",
                                 f"scenario = {scen}, comparison = {comp}, axis = hr0, x = {x:.3f}, cap_{lam}", v))
        rows.append(row)
    D6.append(([laml], rows, {0}))
for x in hr_grid:
    lab(fnum(x, 3), T, f"HR grid point (Supplementary Table {SUPP['capgrid']})")
add_unit(f"{T}. Maximum affordable cost of an exercise program per patient under alternative effect " + "durations" + sup(S[1]),
         D6,
         [f"{S[1]}" + COHORT + "Deterministic estimates in JPY 1,000 per patient. Main comparison: exercise added to chemotherapy plus pembrolizumab; "
          "secondary comparison: exercise added to chemotherapy alone. Effect until 1 year after surgery: the recurrence HR is held until 1 year after surgery and then halves every year; "
          "no waning: held for life; exercise continued after surgery: as the first, with exercise continued for 30 months after surgery at its monthly cost, the effect held until the end of continuation "
          f"and halving every year thereafter, and the continuation cost counted among medical costs (inputs E04 and E05, Supplementary Table {SUPP['params']}). "
          f"The base-case duration is in Supplementary Table {SUPP['capgrid']}. " + COSTS + "HR, hazard ratio; JPY, Japanese yen; QALY, quality-adjusted life year."])
for tok in ("5", "7.5", "1", "30", "2026", "2", "49"):
    lab(tok, T, "definitions")

# ================================================================ S7  net benefit (JBCS registry report no. 55)
T = f"Supplementary Table {SUPP['netbenefit']}"
cv = csv("cohort_value_jbcs2024.csv")
nN = csv("cohort_N_jbcs2024.csv", ROOT / "input" / "params")
nt = int(one(nN, item="nac_total").value)
npb = int(one(nN, item="nac_pembro").value)
n29 = int(one(nN, item="sens_N_2023").value)
n40 = int(one(nN, item="sens_N_upper").value)
CVF = "output/phase2/main/cohort_value_jbcs2024.csv"
NF = "input/params/cohort_N_jbcs2024.csv"
s_nt = REG.r(fnum(nt, 0), f"{T}, header", NF, "item = nac_total, value", nt)
s_np = REG.r(fnum(npb, 0), f"{T}, header", NF, "item = nac_pembro, value", npb)
s_no = REG.r(fnum(nt - npb, 0), f"{T}, header", NF, "nac_total - nac_pembro", nt - npb)
s_29 = REG.r(fnum(n29, 0), f"{T}, header", NF, "item = sens_N_2023, value", n29)
s_40 = REG.r(fnum(n40, 0), f"{T}, header", NF, "item = sens_N_upper, value", n40)
A7 = [["Recurrence HR", ARM_MAIN + ", base case", ARM_MAIN + ", " + KEXT[0].lower() + KEXT[1:], ARM_SEC]]
B7 = [["Recurrence HR", f"N = {s_nt}: base case", f"N = {s_nt}: {KEXT[0].lower() + KEXT[1:]}", f"N = {s_29}: base case", f"N = {s_29}: {KEXT[0].lower() + KEXT[1:]}",
       f"N = {s_40}: base case", f"N = {s_40}: {KEXT[0].lower() + KEXT[1:]}"]]
for h in (0.95, 0.90, 0.85):
    hl = fnum(h, 2)
    rb = one(cv, setting="main", column="base", hr0=h)
    rk = one(cv, setting="main", column="kext", hr0=h)
    A7.append([hl, REG.r(fk(rb.nb_person_main_det), f"{T}, A, {hl}, main base", CVF, f"setting = main, column = base, hr0 = {hl}, nb_person_main_det", rb.nb_person_main_det),
               REG.r(fk(rk.nb_person_main_det), f"{T}, A, {hl}, main kext", CVF, f"setting = main, column = kext, hr0 = {hl}, nb_person_main_det", rk.nb_person_main_det),
               REG.r(fk(rb.nb_person_secondary_det), f"{T}, A, {hl}, secondary", CVF, f"setting = main, column = base, hr0 = {hl}, nb_person_secondary_det", rb.nb_person_secondary_det)])
    assert abs(rb.nb_person_secondary_det - rk.nb_person_secondary_det) < 1e-6
    row = [hl]
    for setting in ("main", "sens_2023", "sens_upper"):
        for col in ("base", "kext"):
            r = one(cv, setting=setting, column=col, hr0=h)
            assert r.total_lo <= r.total_det <= r.total_hi
            loc = f"setting = {setting}, column = {col}, hr0 = {hl}"
            row.append(f"{REG.r(fnum(r.total_det / 1e9, 2), f'{T}, B, {setting} {col} {hl}', CVF, loc + ', total_det / 1e9', r.total_det / 1e9)} "
                       f"[{REG.r(fnum(r.total_lo / 1e9, 2), f'{T}, B, {setting} {col} {hl}', CVF, loc + ', total_lo / 1e9', r.total_lo / 1e9)}, "
                       f"{REG.r(fnum(r.total_hi / 1e9, 2), f'{T}, B, {setting} {col} {hl}', CVF, loc + ', total_hi / 1e9', r.total_hi / 1e9)}]")
    B7.append(row)
add_unit(f"{T}. Net benefit of an exercise program for one year of eligible patients in Japan, if exercise reduced the recurrence " + "hazard" + sup(S[1]),
         [(["A. Net benefit per patient, JPY 1,000"], A7, {0}), (["B. Net benefit for one year of patients, JPY billion"], B7, {0})],
         [f"{S[1]}Values are conditional on the recurrence HR shown, not expected values. Net benefit per patient: maximum affordable cost at JPY 5 million per QALY "
          "minus the cost of the fee-schedule-based program (Table 1). N: patients with stage II or III triple-negative breast cancer (M0) who received neoadjuvant chemotherapy in 2024, "
          f"{s_nt} in total, of whom {s_np} received neoadjuvant pembrolizumab (main comparison) and {s_no} did not (secondary comparison); "
          "Japanese Breast Cancer Society, National Breast Cancer Registry Report No. 55 (cases diagnosed in 2024, final version)" + cite("jbcs55") + ". "
          f"Sensitivity analyses: N = {s_29} (registrations in 2023) and N = {s_40} (allowing for incomplete registration), with the same share receiving pembrolizumab. "
          "Panel B: deterministic estimate and 95% UI. " + UI + COSTS +
          "HR, hazard ratio; JPY, Japanese yen; QALY, quality-adjusted life year; UI, uncertainty interval."])
for tok in ("0.95", "0.90", "0.85", "5", "2024", "2023", "55", "2026", "2", "95", "2.5", "97.5", "1,000"):
    lab(tok, T, "definitions")

# ================================================================ S8  path B (pCR)
T = TB
pcr_grid = sorted(dc[(dc.axis == "pcr") & (dc.comparison == "main") & (dc.column == "base")].x.round(4).unique())
assert len(pcr_grid) == 11
add_unit(f"{T}. Maximum affordable cost of an exercise program per patient by the increase in pathological complete " + "response" + sup(S[1]),
         grid_panels("pcr", pcr_grid, lambda x: REG.r(fnum(100 * x, 0), f"{T}, row label", "output/phase2/main/det_caps.csv", "x (pcr grid) x 100", 100 * x),
                     "Increase in pCR, percentage points"),
         [f"{S[1]}" + COHORT + "Exercise increases the proportion with pCR by the amount shown (capped at 100%) and does not change the recurrence HR. "
          "Cells show the deterministic estimate and the 95% UI. " + UI + COSTS +
          "Probability above the fee-schedule-based program cost: share of samples in which the maximum affordable cost exceeds the base-case cost of that program (Table 1). "
          "HR, hazard ratio; JPY, Japanese yen; pCR, pathological complete response; QALY, quality-adjusted life year; UI, uncertainty interval."])
for tok in ("100", "5", "7.5", "95", "2.5", "97.5", "1,000", "2026", "2", "49"):
    lab(tok, T, "definitions")

# ================================================================ S9  one-way values (Fig. 3 and Supplementary Fig. S2)
T = f"Supplementary Table {SUPP['oneway']}"
ow = csv("oneway_base.csv")
capb, icb = float(ow.cap_base.iloc[0]), float(ow.icer_base.iloc[0])
xlrow = {r[0]: i for i, r in enumerate(PR.ws.iter_rows(min_row=1, values_only=True), start=1) if r[0]}
D9 = [["Code", "Input", "Lower bound", "Upper bound", "Maximum affordable cost, input at lower bound", "Maximum affordable cost, input at upper bound",
       "ICER, input at lower bound", "ICER, input at upper bound"]]
n_union = 0
for _, r in ow.iterrows():
    cw = abs(r.cap_high - r.cap_low) > 1e-6 * abs(capb)
    iw = abs(r.icer_high - r.icer_low) > 1e-6 * abs(icb)
    if not (cw or iw):
        continue
    n_union += 1
    unit = UNIT[PR.ws[f"F{xlrow[r.param_id]}"].value]
    rule = r.range_rule if isinstance(r.range_rule, str) else ""
    lo = REG.r(fval(r.low_value, unit), f"{T}, {r.param_id}, low", "output/phase2/main/oneway_base.csv", f"param_id = {r.param_id}, low_value", r.low_value)
    hi = REG.r(fval(r.high_value, unit), f"{T}, {r.param_id}, high", "output/phase2/main/oneway_base.csv", f"param_id = {r.param_id}, high_value", r.high_value)
    row = [r.param_id, item(r.param_id), lo, hi + (f" [{RANGE_RULE[rule]}]" if rule else "")]
    for col, ok in (("cap_low", cw), ("cap_high", cw), ("icer_low", iw), ("icer_high", iw)):
        row.append(REG.r(fk(r[col]), f"{T}, {r.param_id}, {col}", "output/phase2/main/oneway_base.csv", f"param_id = {r.param_id}, {col}", r[col]) if ok else "—")
    D9.append(row)
s_union = REG.r(str(n_union), f"{T}, footnote", "output/phase2/main/oneway_base.csv", "rows that change either result", n_union)
add_unit(f"{T}. One-way sensitivity analysis: maximum affordable cost for exercise added to chemotherapy plus pembrolizumab and ICER of chemotherapy plus pembrolizumab compared with chemotherapy " + "alone" + sup(S[1]),
         [(["Inputs that changed either result"], D9, {0})],
         [f"{S[1]}" + COHORT + "Data of Fig. 3 and Supplementary Fig. S2. Each input was set to its lower or upper bound with all other inputs at base-case values. "
          "Maximum affordable cost: recurrence HR 0.85, threshold JPY 5 million per QALY, JPY 1,000 per patient (base case in Table 2). "
          f"ICER: JPY 1,000 per QALY (base case in Table 3). Bounds are in the units of Supplementary Table {SUPP['params']}; brackets mark ranges set by rule (Supplementary Table {SUPP['params']}). "
          f"All {s_union} inputs that changed either result are listed; a dash means that the input did not change that result. " + COSTS +
          "HR, hazard ratio; ICER, incremental cost-effectiveness ratio; JPY, Japanese yen; QALY, quality-adjusted life year."])
for tok in ("0.85", "5", "25", "75", "2026", "2", "49", "1,000", "12", "4", "1", "3", "6", "12.5"):
    lab(tok, T, "definitions")

# ================================================================ S10  other scenarios (needs sc_util_jp and sc_crossings)
T = f"Supplementary Table {SUPP['other']}"
OTHER_READY = (MAIN / "sc_crossings.csv").exists() and (MAIN / "sc_util_jp_det_caps.csv").exists()
ELMORE = None
if OTHER_READY:
    xc = csv("sc_crossings.csv")
    jp_caps, jp_ref = csv("sc_util_jp_det_caps.csv"), csv("sc_util_jp_det_reference.csv")
    sref = csv("scenario_reference.csv")

    def cap85(scen, comp):
        if scen == "utility_jp":
            d, f = jp_caps, "output/phase2/main/sc_util_jp_det_caps.csv"
        else:
            d, f = sc, "output/phase2/main/scenario_caps.csv"
        r = d[(d.scenario == scen) & (d.comparison == comp) & (d.column == "base") & (d.axis == "hr0") & np.isclose(d.x, 0.85)]
        assert len(r) == 1, (scen, comp)
        v = float(r.iloc[0].cap_500)
        return REG.r(fk(v), f"{T}, {scen}, {comp}, cap 0.85", f, f"scenario = {scen}, comparison = {comp}, axis = hr0, x = 0.85, cap_500", v)

    def xr(scen, comp, typ):
        sub = xc[(xc.scenario == scen) & (xc.comparison == comp) & (xc.column == "base") & (xc.type == typ) & (xc.programme == "E02")]
        if typ == "cap_eq_programme":
            sub = sub[np.isclose(sub["lambda"], 5e6)]
        assert len(sub) == 1, (scen, comp, typ)
        v = float(sub.iloc[0].hr0)
        loc = f"scenario = {scen}, comparison = {comp}, type = {typ}, programme = E02" + (", lambda = 5e+06" if typ == "cap_eq_programme" else "")
        a = REG.r(fnum(v, 3), f"{T}, {scen}, {comp}, {typ}", "output/phase2/main/sc_crossings.csv", loc + ", hr0", v)
        b = REG.r(fnum(100 * (1 - v), 1), f"{T}, {scen}, {comp}, {typ}, reduction %", "output/phase2/main/sc_crossings.csv", loc + ": 100 x (1 - hr0)", 100 * (1 - v))
        return f"{a} ({b})"

    # the base case of sc_crossings.csv must equal the crossings used in Table 2
    xb = csv("sc_base_crossings.csv")
    for _, r in xb[xb.column == "base"].iterrows():
        m = xc[(xc.scenario == "base") & (xc.comparison == r.comparison) & (xc.column == r.column) & (xc.type == r.type) & (xc.programme == r.programme)]
        if r.type == "cap_eq_programme":
            m = m[np.isclose(m["lambda"], r["lambda"])]
        assert len(m) == 1 and abs(float(m.iloc[0].hr0) - r.hr0) < 1e-6, ("sc_crossings base differs from sc_base_crossings", r.to_dict())

    def icer(scen):
        if scen == "utility_jp":
            r = one(jp_ref, scenario="utility_jp", column="base")
            f = "output/phase2/main/sc_util_jp_det_reference.csv"
        else:
            r = one(sref, scenario=scen, column="base")
            f = "output/phase2/main/scenario_reference.csv"
        return REG.r(fk(r.icer), f"{T}, {scen}, ICER", f, f"scenario = {scen}, column = base, icer", r.icer)

    RED = " (reduction in recurrence hazard, %)"
    D10 = [["Scenario",
            "Main comparison: maximum affordable cost at recurrence HR 0.85",
            "Main comparison: recurrence HR" + RED + " at which the maximum affordable cost equals the program cost",
            "Main comparison: recurrence HR" + RED + " at which medical costs avoided equal the program cost",
            "Secondary comparison: maximum affordable cost at recurrence HR 0.85",
            "Secondary comparison: recurrence HR" + RED + " at which the maximum affordable cost equals the program cost",
            "Secondary comparison: recurrence HR" + RED + " at which medical costs avoided equal the program cost",
            "ICER of chemotherapy plus pembrolizumab compared with chemotherapy alone"]]
    for scen, sname in (("utility_jp", "Utility values from Japanese populations" + sup(S[2])), ("utility_us", "Utility value set: United States"),
                        # N11 (decision 2026-10-27): the Australian reimbursement submission does not name its value set
                        ("utility_uk", "Utility value set: United Kingdom"), ("utility_au", "Australian reimbursement submission"),
                        ("elmore", "Longer survival after progression during neoadjuvant therapy" + sup(S[3])),
                        ("sjp", "Japanese post-operative treatment" + sup(S[4]))):
        D10.append([sname, cap85(scen, "main"), xr(scen, "main", "cap_eq_programme"), xr(scen, "main", "avoided_eq_programme"),
                    cap85(scen, "secondary"), xr(scen, "secondary", "cap_eq_programme"), xr(scen, "secondary", "avoided_eq_programme"), icer(scen)])
        if scen == "elmore":
            el_row = D10[-1]

    # Elmore row (footnote S[3]): progression during neoadjuvant therapy comes before surgery and the
    # recurrence HR acts after it, so the exercise cells must show the base-case values of Table 2.
    # The raw differences from the base case are recorded (scenario_caps.csv on the hr0 grid, sc_crossings.csv).
    T2 = {}
    for x in json.load(open(BUILD / "_ledger_tables.json", encoding="utf-8"))["rows"]:
        T2.setdefault(x["where"], x["shown"])
    want = []
    for comp in ("main", "secondary"):
        want += [T2[f"Table 2, Panel B, base case, {comp} (intended repeat of Supplementary Table S4)"]]
        for kind in ("cap", "avoided"):
            w = f"Table 2, Panel A, {kind} = E02, {comp}"
            want.append(f"{T2[w]} ({T2[w + ', reduction %']})")
    assert el_row[1:7] == want, ("Elmore exercise cells differ from Table 2", el_row[1:7], want)
    ELMORE = {"cells_equal_to_table_2": list(zip(el_row[1:7], want))}
    for comp in ("main", "secondary"):
        g = sc[(sc.comparison == comp) & (sc.column == "base") & (sc.axis == "hr0")]
        gb, ge = (g[g.scenario == s].set_index("x").cap_500 for s in ("base", "elmore"))
        k = ["column", "type", "lambda", "programme"]
        xb_, xe_ = (xc[(xc.scenario == s) & (xc.comparison == comp)].set_index(k).hr0 for s in ("base", "elmore"))
        ELMORE[comp] = {"cap_500_hr0_grid_max_abs_diff_yen": float((ge - gb.reindex(ge.index)).abs().max()), "grid_points": int(len(ge)),
                        "crossings_hr0_max_abs_diff": float((xe_ - xb_.reindex(xe_.index)).abs().max()), "crossings": int(len(xe_))}
    # N10 (decision 2026-10-26): the six exercise cells of the Elmore row equal Table 2 (asserted above) and show
    # "Same as base case (Table 2)"; E4 (decision 2026-10-26): the S-JP reference ICER is given in Table 3 and its
    # cell here shows "Table 3". The values are still computed and checked, and their registry rows are dropped.
    SAME = "Same as base case (Table 2)"
    i_el = next(i for i, r in enumerate(D10) if r is el_row)
    D10[i_el] = [el_row[0]] + [SAME] * 6 + [el_row[7]]
    i_sjp = next(i for i, r in enumerate(D10) if r[0].startswith("Japanese post-operative treatment"))
    assert D10[i_sjp][7] == T2["Table 3, sjp, ICER"], ("S-JP ICER differs from Table 3", D10[i_sjp][7], T2["Table 3, sjp, ICER"])
    D10[i_sjp] = D10[i_sjp][:7] + ["Table 3"]
    dropped = [x for x in REG.rows if (x["where"].startswith(f"{T}, elmore,") and not x["where"].endswith(", ICER")) or x["where"] == f"{T}, sjp, ICER"]
    REG.rows[:] = [x for x in REG.rows if x not in dropped]
    ELMORE["registry_rows_dropped_N10_E4"] = [dict(where=x["where"], shown=x["shown"]) for x in dropped]
    jp = pd.read_csv(ROOT / "input" / "params" / "sources_utility" / "utilities_scenario_jp.csv")
    u01 = REG.r(fnum(float(one(jp, param_id="U01").value), 2), f"{T}, footnote", "input/params/sources_utility/utilities_scenario_jp.csv", "param_id = U01, value", float(one(jp, param_id="U01").value))
    u04 = REG.r(fnum(float(one(jp, param_id="U04").value), 3), f"{T}, footnote", "input/params/sources_utility/utilities_scenario_jp.csv", "param_id = U04, value", float(one(jp, param_id="U04").value))
    add_unit(f"{T}. Maximum affordable cost, break-even recurrence hazard ratios and the ICER of pembrolizumab under other " + "scenarios" + sup(S[1]),
             [(["Scenario results"], D10, {0})],
             [f"{S[1]}" + COHORT + "Deterministic estimates. Main comparison: exercise added to chemotherapy plus pembrolizumab; secondary comparison: exercise added to chemotherapy alone; "
              "program cost: the fee-schedule-based program (Table 1). Maximum affordable cost in JPY 1,000 per patient at JPY 5 million per QALY; ICER in JPY 1,000 per QALY. "
              "The value in parentheses is the reduction in the recurrence hazard, 100 × (1 − HR), in %. Base-case values are in Tables 2 and 3. " + COSTS +
              "HR, hazard ratio; ICER, incremental cost-effectiveness ratio; JPY, Japanese yen; QALY, quality-adjusted life year.",
              f"{S[2]}Event-free survival during and after treatment {u01} (EQ-5D-5L with the Japanese value set, a Japanese single-center cohort with primary breast cancer); distant recurrence and progression during neoadjuvant therapy {u04} "
              "(taxane arm of the SELECT BC trial, Japanese value set); no values from Japanese populations were found for locoregional recurrence or the decrement for grade 3 or higher adverse events, which keep their base-case values.",
              f"{S[3]}Median survival of 26 months after progression during neoadjuvant therapy instead of the early-recurrence distribution (Supplementary Table {SUPP['params']}); this scenario did not reproduce trial overall survival in years 1 to 3. "
              "Progression during neoadjuvant therapy occurs before surgery and is the same with and without exercise, whereas the exercise effect on recurrence acts only after surgery. "
              "The maximum affordable costs and break-even hazard ratios for exercise therefore equal the base-case values in Table 2 at the precision shown; this scenario changes only the ICER of pembrolizumab.",
              f"{S[4]}Capecitabine or olaparib after surgery for patients without pCR (Table 1)."])
    for tok in ("0.85", "5", "100", "1", "2026", "2", "49", "3", "26", "1,000"):
        lab(tok, T, "definitions and citation years")

# ================================================================ S1  CHEERS 2022 checklist (Methods, Study background)
T = f"Supplementary Table {SUPP['cheers']}"
CH = json.load(open(Path(__file__).with_name("refs") / "cheers2022_items.json", encoding="utf-8"))
MAPF, PAGEF = BUILD / "_manuscript_map.json", BUILD / "_manuscript_pages.json"
MMAP = json.load(open(MAPF, encoding="utf-8")) if MAPF.exists() else None
if MMAP and MMAP.get("version") != VER:
    MMAP = None  # paragraph map of the previous version (first run of this build)
PAGES = json.load(open(PAGEF, encoding="utf-8")) if PAGEF.exists() else None
if MMAP and PAGES and PAGES.get("manuscript_sha256_before_numbering") != MMAP.get("manuscript_sha256"):
    PAGES = None  # pages of an older manuscript build
CHEERS_LOG = {"pages_present": bool(MMAP and PAGES), "rows": []}
SECTION_NAME = {"I": "Introduction", "M.SB": "Methods, Study background", "M.OUT": "Methods, Outcome", "M.VAR": "Methods, Variables",
                "M.SA": "Methods, Statistical analysis", "R": "Results", "D": "Discussion", "IMP": "Implications", "L": "Limitations",
                "A": "Abstract"}


def page_of(pid):
    if not CHEERS_LOG["pages_present"]:
        return None
    pg = PAGES["by_id"][pid]
    lab(str(pg), T, f"page of manuscript paragraph {pid} (_build/_manuscript_pages.json, Word page count)")
    return pg


def loc(*parts):
    """Paragraph ids ('M.SB.2'), ranges ('I.1-I.4') or plain text ('Table 1'), joined by semicolons."""
    out = []
    for prt in parts:
        m = re.fullmatch(r"([A-Z.]+?)\.(\d+)(?:-\1\.(\d+))?", prt)
        if not m:
            out.append(prt)
            continue
        sec, a, b = m.group(1), m.group(2), m.group(3)
        if MMAP:
            for k in [a] + ([b] if b else []):
                assert f"{sec}.{k}" in MMAP["ids"], ("CHEERS location not in the manuscript", sec, k)
        lab(a, T, "paragraph number within the section (_build/_manuscript_map.json)")
        if b is None:
            pg = page_of(f"{sec}.{a}")
            out.append(f"{SECTION_NAME[sec]}, paragraph {a}" + (f" (p. {pg})" if pg else ""))
        else:
            lab(b, T, "paragraph number within the section (_build/_manuscript_map.json)")
            p1, p2 = page_of(f"{sec}.{a}"), page_of(f"{sec}.{b}")
            pp = "" if not p1 else (f" (p. {p1})" if p1 == p2 else f" (pp. {p1} to {p2})")
            out.append(f"{SECTION_NAME[sec]}, paragraphs {a} to {b}" + pp)
    return "; ".join(out)


SM = f"Supplementary Methods {SUPP['methods_survival']}"
if MMAP:
    assert "T.1" in MMAP["ids"], "the manuscript has no title paragraph"
_pt = page_of("T.1")
LOC = {
    1: "Title" + (f" (p. {_pt})" if _pt else ""),  # v8: title and abstract written
    2: loc("A.1-A.4"),
    3: loc("I.1-I.4"),
    4: loc("M.SB.3"),
    5: loc("M.SB.1", "Table 1"),
    6: loc("M.SB.1-M.SB.2"),
    7: loc("M.SB.1"),
    8: loc("M.SB.2"),
    9: loc("M.SB.2"),
    10: loc("M.SB.2"),
    11: loc("M.OUT.1-M.OUT.2"),
    12: loc("M.VAR.4", "M.VAR.5", SM),
    13: loc("M.VAR.5"),
    14: loc("M.VAR.3", "M.VAR.5", "Table 1", f"Supplementary Table {SUPP['params']}"),
    15: loc("M.VAR.3", "M.VAR.5"),
    16: loc("M.SA.1-M.SA.2", "Fig. 1", SM),
    17: loc("M.SA.2-M.SA.3", SM),
    18: "No subgroup analyses beyond the two comparisons; " + loc("M.SB.1"),
    19: "Not performed",
    20: loc("M.SA.4-M.SA.6", SM),
    21: "Not performed",
    22: loc("Table 1", f"Supplementary Table {SUPP['params']}"),
    23: loc("R.1-R.10", "Fig. 2", "Tables 2 and 3"),  # v7: pathway B became Results paragraph 2
    24: loc("R.11", "Fig. 3", f"Supplementary Tables {SUPP['capgrid']}, {SUPP['duration']}, {SUPP['oneway']} and {SUPP['other']}",
            f"Supplementary Fig. {SUPP['fig_icer']}"),
    25: "Not applicable (item 21)",
    26: loc("D.1-D.7", "L.1-L.2"),  # v6: Discussion and Limitations written; v7: Limitations in two paragraphs
    27: "Title page",
    28: "Title page",
}
C1 = [["Section or topic", "Item", "Guidance for reporting", "Location in the manuscript"]]
sec_prev = None
panels = []
for it in CH["items"]:
    if it["section"] != sec_prev:
        if sec_prev is not None:
            panels.append(([sec_prev], C1, {0}))
            C1 = [["Section or topic", "Item", "Guidance for reporting", "Location in the manuscript"]]
        sec_prev = it["section"]
    C1.append([it["topic"], lab(str(it["item"]), T, "CHEERS 2022 item number (refs/cheers2022_items.json)"), it["guidance"], LOC[it["item"]]])
    CHEERS_LOG["rows"].append(dict(item=it["item"], location=LOC[it["item"]]))
panels.append(([sec_prev], C1, {0}))
for tok in ("2022", "1", "21"):
    lab(tok, T, "CHEERS 2022 (name); item numbers")
add_unit(f"{T}. Consolidated Health Economic Evaluation Reporting Standards 2022 " + "checklist" + sup(S[1]),
         panels,
         [f"{S[1]}Checklist and guidance as published" + cite("husereau2022") + ". Locations give the section, the paragraph within the section or "
          "subsection and the page of the manuscript file; tables and figures are named where they report the item. "
          "CHEERS, Consolidated Health Economic Evaluation Reporting Standards."])

# ================================================================ Supplementary Methods S1 (Methods, Statistical analysis stage 1)
MS = "docs/model_spec.md"
P1R = "output/phase1/phase1_report.md"


def ml(tok, why):
    return lab(tok, SM, why)


for tok, why in (("23", "IA4 data cutoff 23 March 2021 (Schmid 2022 abstract)"), ("2021", "IA4 data cutoff year"), ("22", "OS data cutoff 22 March 2024 (Schmid 2024 abstract)"),
                 ("2024", "OS data cutoff year / 2024 report"), ("1", f"milestone tolerance 1 percentage point ({P1R} section 4) / years 1 to 5"),
                 ("0.03", f"HR tolerance ({P1R} section 4)"), ("2", f"event-count tolerance 2% ({P1R} section 4)"),
                 ("7", f"surgery at month 7 / 7-year values ({MS} section 1)"), ("95", "95% intervals; criterion 1 of model selection"),
                 ("20", f"at least 20 at risk ({P1R} section 6) / 20-year hazard check"), ("3", f"hazard peak within 3 years ({P1R} section 6)"),
                 ("10", f"10-year hazard check ({P1R} section 6)"), ("4", f"AIC window of 4 ({MS} section 1)"), ("5", "5-year extrapolation / years 1 to 5"),
                 ("12", f"treatment period of about 12 months ({MS} section 1)"), ("18", f"early distant recurrence cut-off ({MS} section 1)"),
                 ("2025", "abridged life table 2025"), ("49", f"starting age ({MS} section 1)"), ("99.5", f"Bonferroni-adjusted interval ({MS} section 1)"),
                 ("1,000", "1,000 bootstrap and probabilistic samples (analysis plan section 5)"),
                 ("20261023", "base seed boot_seed (docs/model_spec.md section 7)"), ("2.5", "UI percentile"), ("97.5", "UI percentile")):
    ml(tok, why)
TS3, TS2 = f"Supplementary Table {SUPP['validation']}", f"Supplementary Table {SUPP['params']}"
# Literature searches behind the statement of Introduction paragraph 3 that no economic evaluation of exercise during
# neoadjuvant therapy for breast cancer was identified (v6: databases, period, date and search strings moved here from
# the Introduction, instruction "执笔第 4 步（v6）" section 1). Strings are printed as run (refs/searches/search_<key>.json).
NOVELTY = [("novelty", "First search"), ("novelty_variants", "Second search"), ("novelty_chemo", "Third search")]
SRCH = {k: json.load(open(Path(__file__).with_name("refs") / "searches" / f"search_{k}.json", encoding="utf-8")) for k, _ in NOVELTY}
for k, s in SRCH.items():
    assert s["date"] == "2026-10-26", k
    assert '("2000/01/01"[dp] : "2026/12/31"[dp])' in s["pubmed"]["query"] and "PUB_YEAR:[2000 TO 2026]" in s["europepmc"]["query"], k
for tok, why in (("26", "search date 26 October 2026 (refs/searches/search_novelty*.json, field date)"),
                 ("2026", "search date / upper limit of publication years in the search strings"),
                 ("2000", "lower limit of publication years in the search strings"),
                 ("01", "date limit 2000/01/01 in the PubMed search strings"), ("12", "date limit 2026/12/31 in the PubMed search strings"),
                 ("31", "date limit 2026/12/31 in the PubMed search strings")):
    ml(tok, why)
SEARCHES = [
    ("heading", "Literature searches"),
    ("text", "The statement in the Introduction that no economic evaluation of exercise during neoadjuvant therapy for breast cancer was identified "
             "rests on three searches, run on 26 October 2026 in PubMed (title and abstract words and Medical Subject Headings) and Europe PMC "
             "(title and abstract words), each limited to publication years 2000 to 2026. The first search combined exercise, neoadjuvant or "
             "preoperative treatment, breast cancer and economic evaluation. The second searched cancer of any type with neoadjuvant treatment, in any "
             "spelling, or with the phrases during treatment and during oncological treatment. The third searched breast cancer with chemotherapy in "
             "any setting. The title and abstract of every record were read. The search strings were as follows."),
] + [("text", f"{label}, {db}: {SRCH[k][fld]['query']}") for k, label in NOVELTY for db, fld in (("PubMed", "pubmed"), ("Europe PMC", "europepmc"))]
METHODS_S1 = [
    ("title", f"{SM}. Literature searches, survival model, validation and probabilistic sampling"),
    *SEARCHES,
    ("heading", "Reconstructed patient-level data"),
    ("text", "Kaplan-Meier curves of KEYNOTE-522 were digitized from the published figures: event-free survival by arm and pathological complete response "
             "(pCR) status at interim analysis 4, with a data cutoff of 23 March 2021" + cite("schmid2022") + ", and overall survival by arm at the final "
             "analysis of overall survival, with a data cutoff of 22 March 2024" + cite("schmid2024") + ". Patient-level data were reconstructed from the "
             "digitized curves and the published numbers at risk with the algorithm of Guyot and colleagues" + cite("guyot2012") + ". A reconstruction was "
             "accepted when it reproduced each published milestone estimate within 1 percentage point, each published hazard ratio (HR) within 0.03 "
             "and each reported number of events within 2%; the reported numbers of events were not given to the algorithm. The proportions with pCR "
             f"were those of interim analysis 4 ({TS2})."),
    ("heading", "Event-free survival after surgery"),
    ("text", "Event-free survival was modeled from surgery, set at 7 months after randomization, separately for the four combinations of arm and pCR status. "
             "The candidate models were six standard parametric distributions, six Royston-Parmar spline models and three mixture cure models on the relative "
             "survival scale, with background mortality from the Japanese life table for women" + cite("lifetable2025") + ". A model was eligible if at least "
             "95% of the monthly points with at least 20 patients at risk lay within the pointwise 95% confidence interval of the Kaplan-Meier estimate, if its "
             "excess hazard peaked within 3 years after surgery and declined thereafter, and if its all-cause hazard at 10 and 20 years was not below background "
             "mortality."),
    ("text", "Within each pCR stratum, both arms used the same distribution family. Among the families eligible in both arms whose summed Akaike information "
             "criterion was within 4 of the lowest, the family whose 5-year extrapolation was closest to the 5-year event-free survival reported at a later "
             "data cutoff was selected" + cite("esmo2023") + ". This gave a Weibull model for patients with pCR and a Weibull mixture cure model for patients "
             "without pCR. Event-free survival at 7 years in each stratum was then fixed at the value of the final analysis" + cite("kn522final2026") +
             f" ({TS2}), by maximizing the likelihood subject to this equality."),
    ("heading", "Events before surgery, first events after surgery and deaths from adverse events"),
    ("text", "Before surgery, event-free survival in each stratum followed its Kaplan-Meier estimate, and patients with pCR had no events before surgery. "
             "Progression that precluded surgery occurred only in patients without pCR, in the proportion reported for each arm" + cite("schmid2024") +
             ", with the monthly shape of the Kaplan-Meier estimate before surgery. When the reported proportion exceeded the decline of that estimate, "
             "the excess was placed in the first cycle after surgery and taken from the excess hazard, so the total was unchanged."),
    ("text", "First events after surgery were divided into locoregional recurrence, including second primary cancers, distant recurrence and death without "
             "recurrence, in the proportions of the 2024 report" + cite("schmid2024") + ". Locoregional recurrence progressed to distant recurrence at a "
             "constant rate" + cite("schmid2022") + ". Deaths from adverse events, in the numbers reported for each arm" + cite("schmid2022") + ", occurred "
             "at a constant hazard during the 12 months of treatment and were moved within the fitted event-free survival without changing it."),
    ("heading", "Survival after recurrence and background mortality"),
    ("text", "Overall survival curves of patients with early and late relapse in the Epidemiological Strategy and Medical Economics (ESME) cohort" +
             cite("grinda2023") + " were digitized and reconstructed in the same way, and log-logistic distributions were fitted to them. A common shape was "
             "used because the shapes of the two groups did not differ significantly. Excess mortality after distant recurrence within 18 months of "
             "randomization followed the early-relapse distribution and after later recurrence the late-relapse distribution, in the same way in all arms. "
             "Excess mortality after progression that precluded surgery followed the early-relapse distribution."),
    ("text", "Survival after locoregional recurrence carried background mortality only. Background mortality came from the 2025 abridged life table for "
             "Japanese women" + cite("lifetable2025") + ", from age 49 years. The all-cause hazard was never below background mortality; where a fitted "
             "model for patients with pCR fell below it late in follow-up, background mortality applied."),
    ("heading", "Validation"),
    ("text", "Overall survival was not used to fit or calibrate any parameter. The model was accepted if three criteria, fixed before the comparison, were "
             "met. First, overall survival of each arm at years 1 to 5 lay within the pointwise 95% confidence intervals of the reconstructed Kaplan-Meier "
             "estimates, or all ten points lay within Bonferroni-adjusted 99.5% intervals. Second, the 5-year difference in restricted mean survival time "
             "between arms lay within the bootstrap 95% interval of the Kaplan-Meier difference. Third, overall and event-free survival at 7 years lay "
             "within the 95% confidence intervals of the final analysis" + cite("kn522final2026") + f". Supplementary Fig. {SUPP['fig_validation']} and "
             f"{TS3} show the comparison."),
    ("heading", "Probabilistic sensitivity analysis"),
    ("text", "Each of the 1,000 probabilistic samples combined one bootstrap replicate of the survival model with one draw of the other inputs. In each "
             "replicate, the reconstructed event-free survival data were resampled within arm together with their pCR status and the models were refitted "
             "with the 7-year equality; the 7-year values were drawn from binomial distributions with the stratum sizes of interim analysis 4. The "
             "reconstructed ESME data were resampled within group and the log-logistic distributions refitted."),
    ("text", f"The other inputs were drawn independently from the distributions in {TS2}: gamma distributions for costs, durations and events per "
             "patient, beta distributions for proportions and utilities, and lognormal distributions for hazard ratios, with parameters derived from "
             "the 95% ranges. Drug prices and rates based on zero events were fixed, and the duration of the utility decrement for adverse events and the "
             "discount rate were not varied. Every sample can be reproduced from its random seed (base seed 20261023, plus the sample number for the "
             "bootstrap). The 2.5th and 97.5th percentiles across samples give the 95% uncertainty intervals."),
]
for k2, t in METHODS_S1:
    for tok in num_tokens(t):
        assert tok in {x["shown"] for x in REG.labels if x["where"] == SM} or tok in ("4",), ("unregistered number in Supplementary Methods S1", tok, t[:60])

# ================================================================ supplementary figures (images from make_figures.py)
SF = json.load(open(BUILD / "_ledger_suppfigs.json", encoding="utf-8"))
sfr = {x["where"]: x for x in SF["rows"]}
n_icer_all = next(x["shown"] for x in SF["rows"] if x["where"].startswith("Supplementary Fig. S2 legend (number of inputs that changed"))
n_icer_shown = next(x["shown"] for x in SF["rows"] if x["where"].startswith("Supplementary Fig. S2 legend (number of inputs shown)"))
FIGCAP = {
    "figS1": [f"Supplementary Fig. {SUPP['fig_validation']}. Overall survival and event-free survival in KEYNOTE-522: reconstructed Kaplan-Meier curves, the model and the final " + "analysis" + sup(S[1]),
              "(a) Overall survival. (b) Event-free survival. Thin step lines: Kaplan-Meier estimates from patient-level data reconstructed from the published curves of the 2024 report" + cite("guyot2012", "schmid2024") + " "
              "(solid, chemotherapy plus pembrolizumab; dashed, chemotherapy alone), with their 95% CIs shaded. Thick grey lines: the model (solid and dashed as before). "
              "Points with bars: 7-year estimates of the final analysis" + cite("kn522final2026") + " with 95% CIs (filled, chemotherapy plus pembrolizumab; open, chemotherapy alone). "
              f"Overall survival was not used to fit the model. Values are given in Supplementary Table {SUPP['validation']}.",
              f"{S[1]}CI, confidence interval."],
    "figS2": [f"Supplementary Fig. {SUPP['fig_icer']}. One-way sensitivity analysis of the incremental cost-effectiveness ratio of chemotherapy plus pembrolizumab compared with chemotherapy " + "alone" + sup(S[1]),
              "Bars show the ICER when one input is set to its lower bound (dark bars) or upper bound (light bars) and all other inputs keep their base-case values; the vertical line is the base-case estimate (Table 3). "
              f"The {n_icer_shown} inputs with the widest ranges of the {n_icer_all} that changed the ICER are shown. Brackets mark ranges set by rule: [±25%], ±25% around the base value; [mirrored], the missing bound mirrored; "
              f"[price], drug price varied downward only, to 75% of the list price. Codes refer to Supplementary Table {SUPP['params']}; all values are listed in Supplementary Table {SUPP['oneway']}.",
              f"{S[1]}" + COHORT + COSTS + "AE, adverse event; ICER, incremental cost-effectiveness ratio; JPY, Japanese yen; QALY, quality-adjusted life year."],
}
for tok in ("2024", "7", "95", "25", "75", "2026", "2", "49", "1,000"):
    lab(tok, "supplementary figure legends", "definitions")

# ================================================================ assemble in the planned order of first citation
# v6: Supplementary Methods S1 is first cited in Introduction paragraph 3, before Supplementary Table S1 (Methods, Study background)
ORDER = [("methods", f"Supplementary Methods {SUPP['methods_survival']}"), ("table", f"Supplementary Table {SUPP['cheers']}"),
         ("table", f"Supplementary Table {SUPP['params']}"), ("figure", "figS1"), ("table", f"Supplementary Table {SUPP['validation']}"),
         ("table", f"Supplementary Table {SUPP['capgrid']}"), ("table", f"Supplementary Table {SUPP['pathB']}"),
         ("table", f"Supplementary Table {SUPP['decomp']}"), ("table", f"Supplementary Table {SUPP['duration']}"),
         ("table", f"Supplementary Table {SUPP['netbenefit']}"), ("table", f"Supplementary Table {SUPP['oneway']}"), ("figure", "figS2"),
         ("table", f"Supplementary Table {SUPP['other']}")]
units = {u[0].split(".")[0]: u for u in UNITS}
doc = new_document(landscape=ORDER[0][0] == "table")
first = True
kinds = []
for kind, key in ORDER:
    if kind == "methods":
        kinds.append(kind)
        if not first:
            new_section(doc, landscape=False)
        for k2, t in METHODS_S1:
            para(doc, t, bold=(k2 == "heading"), space_after=6 if k2 == "title" else 0)
        first = False
        continue
    if kind == "table":
        if key not in units:
            continue
        kinds.append(kind)
        title, tables, notes, landscape = units[key]
        if not first:
            new_section(doc, landscape=True)
        para(doc, title, space_after=6)
        for hdr, rows, bold in tables:
            has_digit = any(ch.isdigit() for ch in hdr[0])
            table(doc, [[hdr[0]]] + rows, bold_rows=set() if has_digit else {0})
            para(doc, "")
        for n in notes:
            para(doc, n)
    else:
        kinds.append(kind)
        new_section(doc, landscape=False)
        png = FIGDIR / f"{key}.png"
        from PIL import Image
        w = Image.open(png).size[0] / 600 * 25.4
        doc.add_paragraph().add_run().add_picture(str(png), width=Mm(w))
        for t in FIGCAP[key]:
            para(doc, t)
    first = False
doc.save(BUILD / "supplement_marked.docx")
json.dump({"rows": REG.rows, "labels": REG.labels, "other_ready": OTHER_READY, "order_kinds": kinds, "elmore_check": ELMORE, "cheers": CHEERS_LOG},
          open(BUILD / "_ledger_supplement.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
print("_build/supplement_marked.docx written;", len(REG.rows), "registered numbers; S10 included:", OTHER_READY)
print("Elmore check", {k: v for k, v in ELMORE.items() if k != "registry_rows_dropped_N10_E4"}, "dropped", len(ELMORE["registry_rows_dropped_N10_E4"]))
print("CHEERS pages present:", CHEERS_LOG["pages_present"])
