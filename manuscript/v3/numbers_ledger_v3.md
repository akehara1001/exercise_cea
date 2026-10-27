# 数字对照表 v3（2026-10-26 20:05，由 `manuscript/code/make_ledger.py` 从登记表生成）

每个显示的数字：显示值、位置、来源文件、来源中的位置、原始值。舍入：从原始值一次四舍五入（half up）；舍入为 0 的值不带负号；费用以千日元（JPY 1,000）显示，与第 2 阶段报告的“万日元 1 位小数”精度相同。

## 1. Results：每句所依据的表格位置

- P1.1　Fig. 2a shows that the maximum affordable cost of an exercise program per patient, in Japanese yen (JPY), rose as the recurrence hazard ratio (HR) with exercise fell.
  - 所引：Fig. 2
- P1.2　Added to chemotherapy plus pembrolizumab, exercise had a maximum affordable cost of JPY 2,726 thousand per patient at an HR of 0.85 (Table 2).
  - 所引：Table 2
  - 2,726 ← Table 2, Panel B, base case, main (intended repeat of Supplementary Table S4)（`output/phase2/main/det_caps.csv`：comparison = main, column = base, axis = hr0, x = 0.85, cap_500）
- P1.3　Its 95% uncertainty interval (UI) was [2,223, 3,040] (Table 2).
  - 所引：Table 2
  - 2,223 ← Table 2, Panel B, base case, main (intended repeat of Supplementary Table S4)（`output/phase2/main/psa_caps_summary.csv`：comparison = main, column = base, axis = hr0, x = 0.85, cap500_lo）
  - 3,040 ← Table 2, Panel B, base case, main (intended repeat of Supplementary Table S4)（`output/phase2/main/psa_caps_summary.csv`：comparison = main, column = base, axis = hr0, x = 0.85, cap500_hi）
- P1.4　At an HR of 0.70, it was JPY 5,596 thousand (95% UI [4,545, 6,256]; Supplementary Table S4).
  - 所引：Supplementary Table S4、Table 1
  - 5,596 ← Supplementary Table S4, A, hr0 0.700, main base（`output/phase2/main/det_caps.csv`：comparison = main, column = base, axis = hr0, x = 0.700, cap_500）
  - 4,545 ← Supplementary Table S4, A, hr0 0.700, main base（`output/phase2/main/psa_caps_summary.csv`：comparison = main, column = base, axis = hr0, x = 0.700, cap500_lo）
  - 6,256 ← Supplementary Table S4, A, hr0 0.700, main base（`output/phase2/main/psa_caps_summary.csv`：comparison = main, column = base, axis = hr0, x = 0.700, cap500_hi）
- P1.5　Table 2 (panel A) shows that the maximum affordable cost equaled the cost of the fee-schedule-based program at an HR of 0.989, a 1.1% reduction in the recurrence hazard.
  - 所引：Table 2
  - 0.989 ← Table 2, Panel A, cap = E02, main（`output/phase2/main/sc_base_crossings.csv`：comparison = main, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02, hr0）
  - 1.1 ← Table 2, Panel A, cap = E02, main, reduction %（`output/phase2/main/sc_base_crossings.csv`：comparison = main, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02: 100 x (1 - hr0)）
- P1.6　Medical costs avoided by exercise equaled the same program cost at an HR of 0.958, a 4.2% reduction (Table 2).
  - 所引：Table 2
  - 0.958 ← Table 2, Panel A, avoided = E02, main（`output/phase2/main/sc_base_crossings.csv`：comparison = main, column = base, type = avoided_eq_programme, programme = E02, hr0）
  - 4.2 ← Table 2, Panel A, avoided = E02, main, reduction %（`output/phase2/main/sc_base_crossings.csv`：comparison = main, column = base, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0)）
- P2.1　Supplementary Table S5 shows the incremental costs by category for exercise added to chemotherapy plus pembrolizumab at an HR of 0.85.
  - 所引：Supplementary Table S5、Table 2
- P2.2　Incremental medical costs other than the program cost were JPY −702 thousand per patient (Supplementary Table S5).
  - 所引：Supplementary Table S5
  - −702 ← Supplementary Table S5, total_without_programme, d_base（`output/phase2/main/decomp_main_hr085.csv`：category = total_without_programme, d_base）
- P2.3　Second-line and later treatment of distant recurrence contributed JPY −437 thousand (Supplementary Table S5).
  - 所引：Supplementary Table S5
  - −437 ← Supplementary Table S5, dr_later_lines, d_base（`output/phase2/main/decomp_main_hr085.csv`：category = dr_later_lines, d_base）
- P2.4　First-line treatment of distant recurrence contributed JPY −254 thousand (Supplementary Table S5).
  - 所引：Supplementary Table S5
  - −254 ← Supplementary Table S5, dr_first_line, d_base（`output/phase2/main/decomp_main_hr085.csv`：category = dr_first_line, d_base）
- P3.1　Table 2 (panel B) shows that the maximum affordable cost at an HR of 0.85 depended on how long the effect lasted.
  - 所引：Table 2
- P3.2　It was JPY 1,772 thousand when the effect lasted until 1 year after surgery, against JPY 2,726 thousand in the base case (Table 2).
  - 所引：Table 2
  - 1,772 ← Table 2, Panel B, dur1, main（`output/phase2/main/scenario_caps.csv`：scenario = path_a_s1, comparison = main, column = base, axis = hr0, x = 0.85, cap_500）
  - 2,726 ← Table 2, Panel B, base case, main (intended repeat of Supplementary Table S4)（`output/phase2/main/det_caps.csv`：comparison = main, column = base, axis = hr0, x = 0.85, cap_500）
- P3.3　It was JPY 3,404 thousand when the effect did not wane (Table 2; Supplementary Table S6).
  - 所引：Table 2、Supplementary Table S6
  - 3,404 ← Table 2, Panel B, dur2, main（`output/phase2/main/scenario_caps.csv`：scenario = path_a_s2, comparison = main, column = base, axis = hr0, x = 0.85, cap_500）
- P4.1　Table 2 (panel C) shows that, with metastatic treatment costs halved, medical costs avoided equaled the cost of the fee-schedule-based program at an HR of 0.918, an 8.2% reduction.
  - 所引：Table 2
  - 0.918 ← Table 2, Panel C, m50, avoided = E02, main（`output/phase2/main/sc_metcost50_crossings.csv`：comparison = main, column = base, type = avoided_eq_programme, programme = E02, hr0）
  - 8.2 ← Table 2, Panel C, m50, avoided = E02, main, reduction %（`output/phase2/main/sc_metcost50_crossings.csv`：comparison = main, column = base, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0)）
- P4.2　With eribulin-based later-line treatment, this HR was 0.914, an 8.6% reduction (Table 2).
  - 所引：Table 2
  - 0.914 ← Table 2, Panel C, eri, avoided = E02, main（`output/phase2/main/sc_eribulin_crossings.csv`：comparison = main, column = base, type = avoided_eq_programme, programme = E02, hr0）
  - 8.6 ← Table 2, Panel C, eri, avoided = E02, main, reduction %（`output/phase2/main/sc_eribulin_crossings.csv`：comparison = main, column = base, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0)）
- P4.3　The HR at which the maximum affordable cost equaled the program cost was 0.988 with metastatic treatment costs halved and 0.987 with eribulin-based treatment (Table 2).
  - 所引：Table 2
  - 0.988 ← Table 2, Panel C, m50, cap = E02, main（`output/phase2/main/sc_metcost50_crossings.csv`：comparison = main, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02, hr0）
  - 0.987 ← Table 2, Panel C, eri, cap = E02, main（`output/phase2/main/sc_eribulin_crossings.csv`：comparison = main, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02, hr0）
- P4.4　The reductions of 4.2% to 8.6% at which medical costs avoided equaled the program cost held only for exercise added to chemotherapy plus pembrolizumab with the fee-schedule-based program (Table 2).
  - 所引：Table 2
  - 4.2 ← Table 2, Panel A, avoided = E02, main, reduction %（`output/phase2/main/sc_base_crossings.csv`：comparison = main, column = base, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0)）
  - 8.6 ← Table 2, Panel C, eri, avoided = E02, main, reduction %（`output/phase2/main/sc_eribulin_crossings.csv`：comparison = main, column = base, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0)）
- P5.1　Supplementary Table S7 shows the net benefit for the 3,451 patients a year in Japan who would be eligible, if exercise reduced the recurrence hazard.
  - 所引：Supplementary Table S7
  - 3,451 ← Supplementary Table S7, header（`input/params/cohort_N_jbcs2024.csv`：item = nac_total, value）
- P5.2　At an HR of 0.95, the net benefit for one year of patients was JPY 2.68 billion (95% UI [2.22, 2.94]; Supplementary Table S7).
  - 所引：Supplementary Table S7
  - 2.68 ← Supplementary Table S7, B, main base 0.95（`output/phase2/main/cohort_value_jbcs2024.csv`：setting = main, column = base, hr0 = 0.95, total_det / 1e9）
  - 2.22 ← Supplementary Table S7, B, main base 0.95（`output/phase2/main/cohort_value_jbcs2024.csv`：setting = main, column = base, hr0 = 0.95, total_lo / 1e9）
  - 2.94 ← Supplementary Table S7, B, main base 0.95（`output/phase2/main/cohort_value_jbcs2024.csv`：setting = main, column = base, hr0 = 0.95, total_hi / 1e9）
- P5.3　At an HR of 0.85, it was JPY 9.57 billion (95% UI [8.15, 10.36]; Supplementary Table S7).
  - 所引：Supplementary Table S7
  - 9.57 ← Supplementary Table S7, B, main base 0.85（`output/phase2/main/cohort_value_jbcs2024.csv`：setting = main, column = base, hr0 = 0.85, total_det / 1e9）
  - 8.15 ← Supplementary Table S7, B, main base 0.85（`output/phase2/main/cohort_value_jbcs2024.csv`：setting = main, column = base, hr0 = 0.85, total_lo / 1e9）
  - 10.36 ← Supplementary Table S7, B, main base 0.85（`output/phase2/main/cohort_value_jbcs2024.csv`：setting = main, column = base, hr0 = 0.85, total_hi / 1e9）
- P6.1　Fig. 2 and Table 2 also show exercise added to chemotherapy alone.
  - 所引：Fig. 2、Table 2
- P6.2　Its maximum affordable cost at an HR of 0.85 was JPY 3,443 thousand per patient (95% UI [2,881, 3,785]; Table 2).
  - 所引：Table 2
  - 3,443 ← Table 2, Panel B, base case, secondary (intended repeat of Supplementary Table S4)（`output/phase2/main/det_caps.csv`：comparison = secondary, column = base, axis = hr0, x = 0.85, cap_500）
  - 2,881 ← Table 2, Panel B, base case, secondary (intended repeat of Supplementary Table S4)（`output/phase2/main/psa_caps_summary.csv`：comparison = secondary, column = base, axis = hr0, x = 0.85, cap500_lo）
  - 3,785 ← Table 2, Panel B, base case, secondary (intended repeat of Supplementary Table S4)（`output/phase2/main/psa_caps_summary.csv`：comparison = secondary, column = base, axis = hr0, x = 0.85, cap500_hi）
- P6.3　This cost equaled the cost of the fee-schedule-based program at an HR of 0.991, a 0.9% reduction in the recurrence hazard (Table 2).
  - 所引：Table 2
  - 0.991 ← Table 2, Panel A, cap = E02, secondary（`output/phase2/main/sc_base_crossings.csv`：comparison = secondary, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02, hr0）
  - 0.9 ← Table 2, Panel A, cap = E02, secondary, reduction %（`output/phase2/main/sc_base_crossings.csv`：comparison = secondary, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02: 100 x (1 - hr0)）
- P6.4　Medical costs avoided equaled the program cost at an HR of 0.966, a 3.4% reduction (Table 2).
  - 所引：Table 2
  - 0.966 ← Table 2, Panel A, avoided = E02, secondary（`output/phase2/main/sc_base_crossings.csv`：comparison = secondary, column = base, type = avoided_eq_programme, programme = E02, hr0）
  - 3.4 ← Table 2, Panel A, avoided = E02, secondary, reduction %（`output/phase2/main/sc_base_crossings.csv`：comparison = secondary, column = base, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0)）
- P7.1　Table 3 shows the costs, quality-adjusted life years (QALYs) and cost-effectiveness of pembrolizumab added to neoadjuvant chemotherapy.
  - 所引：Table 3
- P7.2　In the base case, pembrolizumab added JPY 4,426 thousand per patient in costs (95% UI [−330, 8,901]; Table 3).
  - 所引：Table 3
  - 4,426 ← Table 3, base, total（`output/phase2/main/det_reference.csv`：column = base, dC）
  - −330 ← Table 3, base, total（`output/phase2/main/psa_reference_summary.csv`：column = base, dC_lo）
  - 8,901 ← Table 3, base, total（`output/phase2/main/psa_reference_summary.csv`：column = base, dC_hi）
- P7.3　It added 2.156 QALYs (95% UI [0.245, 4.228]; Table 3).
  - 所引：Table 3
  - 2.156 ← Table 3, base, QALY（`output/phase2/main/det_reference.csv`：column = base, dQ）
  - 0.245 ← Table 3, base, QALY（`output/phase2/main/psa_reference_summary.csv`：column = base, dQ_lo）
  - 4.228 ← Table 3, base, QALY（`output/phase2/main/psa_reference_summary.csv`：column = base, dQ_hi）
- P7.4　The pembrolizumab drug cost was JPY 6,531 thousand (Table 3).
  - 所引：Table 3
  - 6,531 ← Table 3, Panel A, pembrolizumab_drug, base（`output/phase2/main/decomp_reference.csv`：category = pembrolizumab_drug, d_base）
- P7.5　Second-line and later treatment of distant recurrence contributed JPY −1,911 thousand (Table 3).
  - 所引：Table 3
  - −1,911 ← Table 3, Panel A, dr_later_lines, base（`output/phase2/main/decomp_reference.csv`：category = dr_later_lines, d_base）
- P7.6　The incremental cost-effectiveness ratio (ICER) was JPY 2,053 thousand per QALY (Table 3).
  - 所引：Table 3
  - 2,053 ← Table 3, base, ICER（`output/phase2/main/det_reference.csv`：column = base, icer）
- P7.7　The probability that pembrolizumab was cost-effective was 83.1% at JPY 5 million per QALY and 90.8% at JPY 7.5 million per QALY (Table 3).
  - 所引：Table 3
  - 83.1 ← Table 3, base, P(CE) 5M（`output/phase2/main/psa_reference_summary.csv`：column = base, p_ce_500）
  - 90.8 ← Table 3, base, P(CE) 7.5M（`output/phase2/main/psa_reference_summary.csv`：column = base, p_ce_750）
- P8.1　Table 3 also shows that the ICER was JPY 3,044 thousand per QALY with Japanese post-operative treatment.
  - 所引：Table 3
  - 3,044 ← Table 3, sjp, ICER（`output/phase2/main/scenario_reference.csv`：scenario = sjp, column = base, icer）
- P8.2　It was JPY 2,565 thousand with metastatic treatment costs halved and JPY 2,785 thousand with eribulin-based later-line treatment (Table 3).
  - 所引：Table 3
  - 2,565 ← Table 3, m50, ICER（`output/phase2/main/sc_metcost50_det_reference.csv`：column = base, icer）
  - 2,785 ← Table 3, eri, ICER（`output/phase2/main/sc_eribulin_det_reference.csv`：column = base, icer）
- P8.3　It was JPY 1,920 thousand with higher mortality after early recurrence with pembrolizumab (Table 3).
  - 所引：Table 3
  - 1,920 ← Table 3, kext, ICER（`output/phase2/main/det_reference.csv`：column = kext, icer）
- P9.1　Table 3 (panel C) shows the exercise effect at which exercise added to chemotherapy alone would gain as many QALYs as pembrolizumab.
  - 所引：Table 3
- P9.2　This required a recurrence HR of 0.425 (Table 3).
  - 所引：Table 3
  - 0.425 ← Table 3, Panel C, HR（`output/phase2/main/det_yardstick.csv`：axis = hr0, root）
- P9.3　Through an effect on pathological complete response (pCR), it required an increase in pCR of 35.9 percentage points (Table 3).
  - 所引：Table 3
  - 35.9 ← Table 3, Panel C, pCR（`output/phase2/main/det_yardstick.csv`：axis = pcr, root x 100）
- P9.4　Both values lay outside the ranges studied (Supplementary Tables S4 and S8).
  - 所引：Supplementary Table S4、Supplementary Table S8
- P10.1　Fig. 3 shows the one-way sensitivity analysis of the maximum affordable cost for exercise added to chemotherapy plus pembrolizumab at an HR of 0.85 (Supplementary Table S9).
  - 所引：Fig. 3、Supplementary Table S9、Table 2
- P10.2　The monthly cost of second-line and later treatment moved this cost most, from JPY 2,617 thousand at its lower bound to JPY 2,836 thousand at its upper bound (Fig. 3).
  - 所引：Fig. 3、Supplementary Table S9
  - 2,617 ← Supplementary Table S9, D05, cap_low（`output/phase2/main/oneway_base.csv`：param_id = D05, cap_low）
  - 2,836 ← Supplementary Table S9, D05, cap_high（`output/phase2/main/oneway_base.csv`：param_id = D05, cap_high）
- P10.3　Supplementary Fig. S2 shows that the pembrolizumab drug cost moved the ICER most, to JPY 1,296 thousand per QALY at its lower bound.
  - 所引：Supplementary Fig. S2、Supplementary Table S9
  - 1,296 ← Supplementary Table S9, A03, icer_low（`output/phase2/main/oneway_base.csv`：param_id = A03, icer_low）
- P10.4　Supplementary Table S10 shows that, with utility values from Japanese populations, the maximum affordable cost at an HR of 0.85 was JPY 2,733 thousand.
  - 所引：Supplementary Table S10、Table 2
  - 2,733 ← Supplementary Table S10, utility_jp, main, cap 0.85（`output/phase2/main/sc_util_jp_det_caps.csv`：scenario = utility_jp, comparison = main, axis = hr0, x = 0.85, cap_500）
- P10.5　Across the six scenarios in this table, the HR at which the maximum affordable cost equaled the cost of the fee-schedule-based program ranged from 0.988 to 0.989 (Supplementary Table S10).
  - 所引：Supplementary Table S10
  - 0.988 ← Supplementary Table S10, utility_au, main, cap_eq_programme（`output/phase2/main/sc_crossings.csv`：scenario = utility_au, comparison = main, type = cap_eq_programme, programme = E02, lambda = 5e+06, hr0）
  - 0.989 ← Supplementary Table S10, elmore, main, cap_eq_programme（`output/phase2/main/sc_crossings.csv`：scenario = elmore, comparison = main, type = cap_eq_programme, programme = E02, lambda = 5e+06, hr0）

## 2. Table 1–3（tables_v3.docx）

| # | 显示 | 位置 | 来源文件 | 来源中的位置 | 原始值 | 暂定 |
|---|---|---|---|---|---|---|
| 1 | 49 | Table 1, cohort | `docs/model_spec.md` | docs/model_spec.md line 8 | 49 |  |
| 2 | 100 | Table 1, time horizon | `docs/model_spec.md` | docs/model_spec.md line 8 | 100 |  |
| 3 | 1 | Table 1, cycle | `docs/model_spec.md` | docs/model_spec.md line 8 | 1 |  |
| 4 | 7 | Table 1, surgery | `docs/model_spec.md` | docs/model_spec.md line 10 | 7 |  |
| 5 | 2 | Table 1, discounting | `docs/model_spec.md` | docs/model_spec.md line 93 | 2 |  |
| 6 | 2026 | Table 1, prices | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ column J (価格の年度) = 令和8年度 in the cost rows; 令和8年度 = fiscal year 2026 | 令和8年度 |  |
| 7 | 1,000 | Table 1, uncertainty | `output/phase2/main/psa_caps_summary.csv` | column n (all rows) | 1000 |  |
| 8 | 494 | Table 1, pCR | `data/pcr_counts.csv` | row K22 (IA4), column pcr_pembro | 494 |  |
| 9 | 784 | Table 1, pCR | `data/pcr_counts.csv` | row K22 (IA4), pcr_pembro + nonpcr_pembro | 784 |  |
| 10 | 63.0 | Table 1, pCR | `data/pcr_counts.csv` | pcr_pembro / (pcr_pembro + nonpcr_pembro) | 0.6301020408163265 |  |
| 11 | 217 | Table 1, pCR | `data/pcr_counts.csv` | row K22 (IA4), column pcr_placebo | 217 |  |
| 12 | 390 | Table 1, pCR | `data/pcr_counts.csv` | row K22 (IA4), pcr_placebo + nonpcr_placebo | 390 |  |
| 13 | 55.6 | Table 1, pCR | `data/pcr_counts.csv` | pcr_placebo / (pcr_placebo + nonpcr_placebo) | 0.5564102564102564 |  |
| 14 | 90.4 | Table 1, event-free survival | `data/kn522_final_7y.csv` | row id = efs_pcr_pembro, column value | 90.4 |  |
| 15 | 85.9 | Table 1, event-free survival | `data/kn522_final_7y.csv` | row id = efs_pcr_placebo, column value | 85.9 |  |
| 16 | 57.6 | Table 1, event-free survival | `data/kn522_final_7y.csv` | row id = efs_nonpcr_pembro, column value | 57.6 |  |
| 17 | 49.7 | Table 1, event-free survival | `data/kn522_final_7y.csv` | row id = efs_nonpcr_placebo, column value | 49.7 |  |
| 18 | 9.73 | Table 1, survival after distant recurrence | `output/phase1/calibration.csv` | row stage = calibrated, arm = pembro, column dr_median_months | 9.73391157650877 |  |
| 19 | 18 | Table 1, survival after distant recurrence | `docs/model_spec.md` | docs/model_spec.md line 19 | 18 |  |
| 20 | 16.93 | Table 1, survival after distant recurrence | `output/phase1/calibration.csv` | row stage = calibrated, arm = pembro, column dr_late_median_months | 16.9299027330314 |  |
| 21 | 1.660 | Table 1, survival after distant recurrence | `output/phase1/calibration.csv` | row stage = calibrated, arm = pembro, column dr_shape | 1.65983596262318 |  |
| 22 | 18 | Table 1, progression during neoadjuvant therapy | `docs/model_spec.md` | docs/model_spec.md line 19 | 18 |  |
| 23 | 2025 | Table 1, background mortality | `data/lifetable_female_2025.csv` | file name (令和7年簡易生命表, women) | 2025 |  |
| 24 | 398,924 | Table 1, pembrolizumab | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G4 (A03) | 398924 |  |
| 25 | 200 | Table 1, pembrolizumab | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell N4 (A03) | 200 mg |  |
| 26 | 3 | Table 1, pembrolizumab | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell N4 (A03) | 3週毎 |  |
| 27 | 8 | Table 1, pembrolizumab | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell N4 (A03) | 術前8回 |  |
| 28 | 9 | Table 1, pembrolizumab | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell N4 (A03) | 術後9回 |  |
| 29 | 1,215,933 | Table 1, first-line treatment | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G52 (D03) | 1215932.77556 |  |
| 30 | 1,458,318 | Table 1, first-line treatment | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G53 (D03P) | 1458318.23014286 |  |
| 31 | 10.37 | Table 1, first-line treatment | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G54 (D04) | 10.36576 |  |
| 32 | 10.84 | Table 1, first-line treatment | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G55 (D04P) | 10.84 |  |
| 33 | 1,412,953 | Table 1, second-line treatment | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G56 (D05) | 1412953.27571429 |  |
| 34 | 32 | Table 1, second-line treatment | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell N56 (D05) | 32% |  |
| 35 | 68 | Table 1, second-line treatment | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell N (32%) and D03 note56 (D05) | 68% |  |
| 36 | 3 | Table 1, end-of-life care | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell C57 (D06) | 死亡前3か月 |  |
| 37 | 1,120,001 | Table 1, end-of-life care | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G57 (D06) | 1120000.5 |  |
| 38 | 6 | Table 1, exercise program | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell C59 (E02) | NAC中6か月 |  |
| 39 | 239,508 | Table 1, exercise program | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G58 (E01) | 239508.135965065 |  |
| 40 | 192,400 | Table 1, exercise program | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G59 (E02) | 192400 |  |
| 41 | 11,260 | Table 1, exercise program | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G60 (E03) | 11260 | 【要確認】E03 |
| 42 | 8,810 | Table 1, musculoskeletal adverse event cost | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G65 (E08) | 8810 |  |
| 43 | 0.889 | Table 1, utilities | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G78 (U01) | 0.889 |  |
| 44 | 0.887 | Table 1, utilities | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G79 (U02) | 0.887 |  |
| 45 | 0.830 | Table 1, utilities | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G80 (U03) | 0.83 |  |
| 46 | 0.735 | Table 1, utilities | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G81 (U04) | 0.735 |  |
| 47 | 0.022 | Table 1, utilities | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G82 (U05) | 0.022 |  |
| 48 | 12.5 | Table 1, utilities | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell N82 (U05) | 12.5 週 |  |
| 49 | 1.064 | Table 1, utilities | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G45 (B33P) | 1.06386 |  |
| 50 | 0.982 | Table 1, utilities | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G46 (B33C) | 0.98201 |  |
| 51 | 0.70 | Table 1, effect on recurrence | `docs/analysis_plan_phase2.md` | docs/analysis_plan_phase2.md line 19 | 0.7 |  |
| 52 | 1.00 | Table 1, effect on recurrence | `docs/analysis_plan_phase2.md` | docs/analysis_plan_phase2.md line 19 | 1.0 |  |
| 53 | 5 | Table 1, effect duration | `docs/analysis_plan_phase2.md` | docs/analysis_plan_phase2.md line 20 | 5 |  |
| 54 | 1 | Table 1, effect duration | `docs/analysis_plan_phase2.md` | docs/analysis_plan_phase2.md line 21 | 1 |  |
| 55 | 0.72 | Table 1, reference value | `input/papers/CHALLENGE.pdf` | p.7 (also p.1): hazard ratio for disease recurrence, new primary cancer, or death, 0.72; and docs/analysis_plan_phase2.md line 22 | 0.72 |  |
| 56 | 3 | Table 1, reference value | `docs/analysis_plan_phase2.md` | docs/analysis_plan_phase2.md line 22 | 3 |  |
| 57 | 0 | Table 1, effect on pCR | `docs/analysis_plan_phase2.md` | docs/analysis_plan_phase2.md line 23 | 0 |  |
| 58 | 10 | Table 1, effect on pCR | `docs/analysis_plan_phase2.md` | docs/analysis_plan_phase2.md line 23 | 10 |  |
| 59 | 1.00 | Table 1, effect on pCR | `docs/analysis_plan_phase2.md` | docs/analysis_plan_phase2.md line 59 | 1.0 |  |
| 60 | 79 | Table 1, musculoskeletal adverse events | `docs/model_spec.md` | docs/model_spec.md line 81 | 79 |  |
| 61 | 428 | Table 1, musculoskeletal adverse events | `docs/model_spec.md` | docs/model_spec.md line 81 | 428 |  |
| 62 | 18.5 | Table 1, musculoskeletal adverse events | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G63 (E06) | 0.18458 |  |
| 63 | 53 | Table 1, musculoskeletal adverse events | `docs/model_spec.md` | docs/model_spec.md line 81 | 53 |  |
| 64 | 461 | Table 1, musculoskeletal adverse events | `docs/model_spec.md` | docs/model_spec.md line 81 | 461 |  |
| 65 | 11.5 | Table 1, musculoskeletal adverse events | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G64 (E07) | 0.11497 |  |
| 66 | 3 | Table 1, musculoskeletal adverse events | `docs/model_spec.md` | docs/model_spec.md line 81 | 3 |  |
| 67 | 428 | Table 1, musculoskeletal adverse events | `docs/model_spec.md` | docs/model_spec.md line 81 | 428 |  |
| 68 | 0.7 | Table 1, musculoskeletal adverse events | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G66 (E09) | 0.00701 |  |
| 69 | 1 | Table 1, musculoskeletal adverse events | `docs/model_spec.md` | docs/model_spec.md line 81 | 1 |  |
| 70 | 461 | Table 1, musculoskeletal adverse events | `docs/model_spec.md` | docs/model_spec.md line 81 | 461 |  |
| 71 | 0.2 | Table 1, musculoskeletal adverse events | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G67 (E10) | 0.00217 |  |
| 72 | 18 | Table 1, scenarios | `docs/model_spec.md` | docs/model_spec.md line 19 | 18 |  |
| 73 | 1.307 | Table 1, scenarios | `output/phase1/round14/kext_derivation.csv` | row quantity = k_external, column value | 1.30672744305531 |  |
| 74 | 0.5 | Table 1, scenarios | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet シナリオ row 4 (sc_metcost50, D05; E = scenario value, F = multiplier) | 0.5 |  |
| 75 | 245,683 | Table 1, scenarios | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet シナリオ row 5 (sc_eribulin, D05; E = scenario value, F = multiplier) | 245682.8035714286 |  |
| 76 | 0.58 | Table 1, scenarios | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G76 (F07) | 0.58 |  |
| 77 | 0.65 | Table 1, scenarios | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G77 (F08) | 0.65 |  |
| 78 | 0.989 | Table 2, Panel A, cap = E02, main | `output/phase2/main/sc_base_crossings.csv` | comparison = main, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02, hr0 | 0.989124409938088 |  |
| 79 | 1.1 | Table 2, Panel A, cap = E02, main, reduction % | `output/phase2/main/sc_base_crossings.csv` | comparison = main, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02: 100 x (1 - hr0) | 1.0875590061911966 |  |
| 80 | 0.991 | Table 2, Panel A, cap = E02, secondary | `output/phase2/main/sc_base_crossings.csv` | comparison = secondary, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02, hr0 | 0.991338563312171 |  |
| 81 | 0.9 | Table 2, Panel A, cap = E02, secondary, reduction % | `output/phase2/main/sc_base_crossings.csv` | comparison = secondary, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02: 100 x (1 - hr0) | 0.8661436687829038 |  |
| 82 | 0.948 | Table 2, Panel A, avoided = E01, main | `output/phase2/main/sc_base_crossings.csv` | comparison = main, column = base, type = avoided_eq_programme, programme = E01, hr0 | 0.947779594164701 |  |
| 83 | 5.2 | Table 2, Panel A, avoided = E01, main, reduction % | `output/phase2/main/sc_base_crossings.csv` | comparison = main, column = base, type = avoided_eq_programme, programme = E01: 100 x (1 - hr0) | 5.222040583529896 |  |
| 84 | 0.958 | Table 2, Panel A, avoided = E01, secondary | `output/phase2/main/sc_base_crossings.csv` | comparison = secondary, column = base, type = avoided_eq_programme, programme = E01, hr0 | 0.957598592541626 |  |
| 85 | 4.2 | Table 2, Panel A, avoided = E01, secondary, reduction % | `output/phase2/main/sc_base_crossings.csv` | comparison = secondary, column = base, type = avoided_eq_programme, programme = E01: 100 x (1 - hr0) | 4.240140745837396 |  |
| 86 | 0.958 | Table 2, Panel A, avoided = E02, main | `output/phase2/main/sc_base_crossings.csv` | comparison = main, column = base, type = avoided_eq_programme, programme = E02, hr0 | 0.957946897629302 |  |
| 87 | 4.2 | Table 2, Panel A, avoided = E02, main, reduction % | `output/phase2/main/sc_base_crossings.csv` | comparison = main, column = base, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 4.205310237069804 |  |
| 88 | 0.966 | Table 2, Panel A, avoided = E02, secondary | `output/phase2/main/sc_base_crossings.csv` | comparison = secondary, column = base, type = avoided_eq_programme, programme = E02, hr0 | 0.96585500798515 |  |
| 89 | 3.4 | Table 2, Panel A, avoided = E02, secondary, reduction % | `output/phase2/main/sc_base_crossings.csv` | comparison = secondary, column = base, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 3.4144992014849995 |  |
| 90 | 0.997 | Table 2, Panel A, avoided = E03, main | `output/phase2/main/sc_base_crossings.csv` | comparison = main, column = base, type = avoided_eq_programme, programme = E03, hr0 | 0.997394530523012 | 【要確認】E03 |
| 91 | 0.3 | Table 2, Panel A, avoided = E03, main, reduction % | `output/phase2/main/sc_base_crossings.csv` | comparison = main, column = base, type = avoided_eq_programme, programme = E03: 100 x (1 - hr0) | 0.26054694769880316 | 【要確認】E03 |
| 92 | 0.998 | Table 2, Panel A, avoided = E03, secondary | `output/phase2/main/sc_base_crossings.csv` | comparison = secondary, column = base, type = avoided_eq_programme, programme = E03, hr0 | 0.997884688387754 | 【要確認】E03 |
| 93 | 0.2 | Table 2, Panel A, avoided = E03, secondary, reduction % | `output/phase2/main/sc_base_crossings.csv` | comparison = secondary, column = base, type = avoided_eq_programme, programme = E03: 100 x (1 - hr0) | 0.21153116122459847 | 【要確認】E03 |
| 94 | 2,726 | Table 2, Panel B, base case, main (intended repeat of Supplementary Table S4) | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.85, cap_500 | 2726400.8870362 |  |
| 95 | 2,223 | Table 2, Panel B, base case, main (intended repeat of Supplementary Table S4) | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.85, cap500_lo | 2222889.94969549 |  |
| 96 | 3,040 | Table 2, Panel B, base case, main (intended repeat of Supplementary Table S4) | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.85, cap500_hi | 3039571.6727006 |  |
| 97 | 3,443 | Table 2, Panel B, base case, secondary (intended repeat of Supplementary Table S4) | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.85, cap_500 | 3442898.84929941 |  |
| 98 | 2,881 | Table 2, Panel B, base case, secondary (intended repeat of Supplementary Table S4) | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.85, cap500_lo | 2880585.1480882 |  |
| 99 | 3,785 | Table 2, Panel B, base case, secondary (intended repeat of Supplementary Table S4) | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.85, cap500_hi | 3785042.45783867 |  |
| 100 | 1,772 | Table 2, Panel B, dur1, main | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, column = base, axis = hr0, x = 0.85, cap_500 | 1772364.98201127 |  |
| 101 | 2,279 | Table 2, Panel B, dur1, secondary | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, column = base, axis = hr0, x = 0.85, cap_500 | 2279438.16744623 |  |
| 102 | 3,404 | Table 2, Panel B, dur2, main | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, column = base, axis = hr0, x = 0.85, cap_500 | 3403938.77458484 |  |
| 103 | 4,420 | Table 2, Panel B, dur2, secondary | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, column = base, axis = hr0, x = 0.85, cap_500 | 4419672.68859316 |  |
| 104 | 2,726 | Table 2, Panel C, base case, main (intended repeat of Supplementary Table S4) | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.85, cap_500 | 2726400.8870362 |  |
| 105 | 2,223 | Table 2, Panel C, base case, main (intended repeat of Supplementary Table S4) | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.85, cap500_lo | 2222889.94969549 |  |
| 106 | 3,040 | Table 2, Panel C, base case, main (intended repeat of Supplementary Table S4) | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.85, cap500_hi | 3039571.6727006 |  |
| 107 | 3,443 | Table 2, Panel C, base case, secondary (intended repeat of Supplementary Table S4) | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.85, cap_500 | 3442898.84929941 |  |
| 108 | 2,881 | Table 2, Panel C, base case, secondary (intended repeat of Supplementary Table S4) | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.85, cap500_lo | 2880585.1480882 |  |
| 109 | 3,785 | Table 2, Panel C, base case, secondary (intended repeat of Supplementary Table S4) | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.85, cap500_hi | 3785042.45783867 |  |
| 110 | 2,381 | Table 2, Panel C, m50, cap, main | `output/phase2/main/sc_metcost50_det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.85, cap_500 | 2380571.076723 |  |
| 111 | 1,958 | Table 2, Panel C, m50, cap, main | `output/phase2/main/sc_metcost50_psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.85, cap500_lo | 1958308.58504917 |  |
| 112 | 2,633 | Table 2, Panel C, m50, cap, main | `output/phase2/main/sc_metcost50_psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.85, cap500_hi | 2633342.55902628 |  |
| 113 | 3,022 | Table 2, Panel C, m50, cap, secondary | `output/phase2/main/sc_metcost50_det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.85, cap_500 | 3022079.92666038 |  |
| 114 | 2,544 | Table 2, Panel C, m50, cap, secondary | `output/phase2/main/sc_metcost50_psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.85, cap500_lo | 2544218.62978064 |  |
| 115 | 3,307 | Table 2, Panel C, m50, cap, secondary | `output/phase2/main/sc_metcost50_psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.85, cap500_hi | 3306739.96076224 |  |
| 116 | 0.988 | Table 2, Panel C, m50, cap = E02, main | `output/phase2/main/sc_metcost50_crossings.csv` | comparison = main, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02, hr0 | 0.987550927594885 |  |
| 117 | 1.2 | Table 2, Panel C, m50, cap = E02, main, reduction % | `output/phase2/main/sc_metcost50_crossings.csv` | comparison = main, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02: 100 x (1 - hr0) | 1.2449072405114947 |  |
| 118 | 0.990 | Table 2, Panel C, m50, cap = E02, secondary | `output/phase2/main/sc_metcost50_crossings.csv` | comparison = secondary, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02, hr0 | 0.990138163251119 |  |
| 119 | 1.0 | Table 2, Panel C, m50, cap = E02, secondary, reduction % | `output/phase2/main/sc_metcost50_crossings.csv` | comparison = secondary, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02: 100 x (1 - hr0) | 0.986183674888097 |  |
| 120 | 0.918 | Table 2, Panel C, m50, avoided = E02, main | `output/phase2/main/sc_metcost50_crossings.csv` | comparison = main, column = base, type = avoided_eq_programme, programme = E02, hr0 | 0.917724940035636 |  |
| 121 | 8.2 | Table 2, Panel C, m50, avoided = E02, main, reduction % | `output/phase2/main/sc_metcost50_crossings.csv` | comparison = main, column = base, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 8.227505996436403 |  |
| 122 | 0.934 | Table 2, Panel C, m50, avoided = E02, secondary | `output/phase2/main/sc_metcost50_crossings.csv` | comparison = secondary, column = base, type = avoided_eq_programme, programme = E02, hr0 | 0.934327038620795 |  |
| 123 | 6.6 | Table 2, Panel C, m50, avoided = E02, secondary, reduction % | `output/phase2/main/sc_metcost50_crossings.csv` | comparison = secondary, column = base, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 6.567296137920497 |  |
| 124 | 2,365 | Table 2, Panel C, eri, cap, main | `output/phase2/main/sc_eribulin_det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.85, cap_500 | 2365229.64363299 |  |
| 125 | 1,943 | Table 2, Panel C, eri, cap, main | `output/phase2/main/sc_eribulin_psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.85, cap500_lo | 1943020.29608397 |  |
| 126 | 2,621 | Table 2, Panel C, eri, cap, main | `output/phase2/main/sc_eribulin_psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.85, cap500_hi | 2620716.38331352 |  |
| 127 | 2,966 | Table 2, Panel C, eri, cap, secondary | `output/phase2/main/sc_eribulin_det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.85, cap_500 | 2966383.62449385 |  |
| 128 | 2,501 | Table 2, Panel C, eri, cap, secondary | `output/phase2/main/sc_eribulin_psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.85, cap500_lo | 2501046.00976405 |  |
| 129 | 3,242 | Table 2, Panel C, eri, cap, secondary | `output/phase2/main/sc_eribulin_psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.85, cap500_hi | 3241657.39636459 |  |
| 130 | 0.987 | Table 2, Panel C, eri, cap = E02, main | `output/phase2/main/sc_eribulin_crossings.csv` | comparison = main, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02, hr0 | 0.98747184731439 |  |
| 131 | 1.3 | Table 2, Panel C, eri, cap = E02, main, reduction % | `output/phase2/main/sc_eribulin_crossings.csv` | comparison = main, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02: 100 x (1 - hr0) | 1.2528152685610028 |  |
| 132 | 0.990 | Table 2, Panel C, eri, cap = E02, secondary | `output/phase2/main/sc_eribulin_crossings.csv` | comparison = secondary, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02, hr0 | 0.989955240912061 |  |
| 133 | 1.0 | Table 2, Panel C, eri, cap = E02, secondary, reduction % | `output/phase2/main/sc_eribulin_crossings.csv` | comparison = secondary, column = base, type = cap_eq_programme, lambda = 5e+06, programme = E02: 100 x (1 - hr0) | 1.0044759087939004 |  |
| 134 | 0.914 | Table 2, Panel C, eri, avoided = E02, main | `output/phase2/main/sc_eribulin_crossings.csv` | comparison = main, column = base, type = avoided_eq_programme, programme = E02, hr0 | 0.914109241632172 |  |
| 135 | 8.6 | Table 2, Panel C, eri, avoided = E02, main, reduction % | `output/phase2/main/sc_eribulin_crossings.csv` | comparison = main, column = base, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 8.5890758367828 |  |
| 136 | 0.925 | Table 2, Panel C, eri, avoided = E02, secondary | `output/phase2/main/sc_eribulin_crossings.csv` | comparison = secondary, column = base, type = avoided_eq_programme, programme = E02, hr0 | 0.925223314414617 |  |
| 137 | 7.5 | Table 2, Panel C, eri, avoided = E02, secondary, reduction % | `output/phase2/main/sc_eribulin_crossings.csv` | comparison = secondary, column = base, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 7.477668558538298 |  |
| 138 | 6,531 | Table 3, Panel A, pembrolizumab_drug, base | `output/phase2/main/decomp_reference.csv` | category = pembrolizumab_drug, d_base | 6531184.11682446 |  |
| 139 | 6,531 | Table 3, Panel A, pembrolizumab_drug, kext | `output/phase2/main/decomp_reference.csv` | category = pembrolizumab_drug, d_kext | 6531184.11682446 |  |
| 140 | 6,531 | Table 3, Panel A, pembrolizumab_drug, m50 | `output/phase2/main/decomp_reference.csv` | category = pembrolizumab_drug, d_base (unchanged in this scenario) [derived; see check] | 6531184.11682446 |  |
| 141 | 6,531 | Table 3, Panel A, pembrolizumab_drug, eri | `output/phase2/main/decomp_reference.csv` | category = pembrolizumab_drug, d_base (unchanged in this scenario) [derived; see check] | 6531184.11682446 |  |
| 142 | 132 | Table 3, Panel A, administration, base | `output/phase2/main/decomp_reference.csv` | category = administration, d_base | 131845.330724252 |  |
| 143 | 132 | Table 3, Panel A, administration, kext | `output/phase2/main/decomp_reference.csv` | category = administration, d_kext | 131845.330724252 |  |
| 144 | 132 | Table 3, Panel A, administration, m50 | `output/phase2/main/decomp_reference.csv` | category = administration, d_base (unchanged in this scenario) [derived; see check] | 131845.330724252 |  |
| 145 | 132 | Table 3, Panel A, administration, eri | `output/phase2/main/decomp_reference.csv` | category = administration, d_base (unchanged in this scenario) [derived; see check] | 131845.330724252 |  |
| 146 | 32 | Table 3, Panel A, immune_ae, base | `output/phase2/main/decomp_reference.csv` | category = immune_ae, d_base | 31896.59246 |  |
| 147 | 32 | Table 3, Panel A, immune_ae, kext | `output/phase2/main/decomp_reference.csv` | category = immune_ae, d_kext | 31896.59246 |  |
| 148 | 32 | Table 3, Panel A, immune_ae, m50 | `output/phase2/main/decomp_reference.csv` | category = immune_ae, d_base (unchanged in this scenario) [derived; see check] | 31896.59246 |  |
| 149 | 32 | Table 3, Panel A, immune_ae, eri | `output/phase2/main/decomp_reference.csv` | category = immune_ae, d_base (unchanged in this scenario) [derived; see check] | 31896.59246 |  |
| 150 | 5 | Table 3, Panel A, chemo_ae, base | `output/phase2/main/decomp_reference.csv` | category = chemo_ae, d_base | 5182.55999999999 |  |
| 151 | 5 | Table 3, Panel A, chemo_ae, kext | `output/phase2/main/decomp_reference.csv` | category = chemo_ae, d_kext | 5182.55999999999 |  |
| 152 | 5 | Table 3, Panel A, chemo_ae, m50 | `output/phase2/main/decomp_reference.csv` | category = chemo_ae, d_base (unchanged in this scenario) [derived; see check] | 5182.55999999999 |  |
| 153 | 5 | Table 3, Panel A, chemo_ae, eri | `output/phase2/main/decomp_reference.csv` | category = chemo_ae, d_base (unchanged in this scenario) [derived; see check] | 5182.55999999999 |  |
| 154 | 42 | Table 3, Panel A, follow_up, base | `output/phase2/main/decomp_reference.csv` | category = follow_up, d_base | 42397.8841846642 |  |
| 155 | 42 | Table 3, Panel A, follow_up, kext | `output/phase2/main/decomp_reference.csv` | category = follow_up, d_kext | 42397.8841846642 |  |
| 156 | 42 | Table 3, Panel A, follow_up, m50 | `output/phase2/main/decomp_reference.csv` | category = follow_up, d_base (unchanged in this scenario) [derived; see check] | 42397.8841846642 |  |
| 157 | 42 | Table 3, Panel A, follow_up, eri | `output/phase2/main/decomp_reference.csv` | category = follow_up, d_base (unchanged in this scenario) [derived; see check] | 42397.8841846642 |  |
| 158 | −24 | Table 3, Panel A, lrr, base | `output/phase2/main/decomp_reference.csv` | category = lrr, d_base | -24119.6831181298 |  |
| 159 | −24 | Table 3, Panel A, lrr, kext | `output/phase2/main/decomp_reference.csv` | category = lrr, d_kext | -24119.6831181298 |  |
| 160 | −24 | Table 3, Panel A, lrr, m50 | `output/phase2/main/decomp_reference.csv` | category = lrr, d_base (unchanged in this scenario) [derived; see check] | -24119.6831181298 |  |
| 161 | −24 | Table 3, Panel A, lrr, eri | `output/phase2/main/decomp_reference.csv` | category = lrr, d_base (unchanged in this scenario) [derived; see check] | -24119.6831181298 |  |
| 162 | −299 | Table 3, Panel A, dr_first_line, base | `output/phase2/main/decomp_reference.csv` | category = dr_first_line, d_base | -299251.205651269 |  |
| 163 | −338 | Table 3, Panel A, dr_first_line, kext | `output/phase2/main/decomp_reference.csv` | category = dr_first_line, d_kext | -338242.080675689 |  |
| 164 | −150 | Table 3, Panel A, dr_first_line, m50 | `output/phase2/main/decomp_reference.csv` | category = dr_first_line, d_base x scenario multiplier 0.5 (input/params/parameters_v10.xlsx sheet シナリオ) [derived; see check] | -149625.6028256345 |  |
| 165 | −299 | Table 3, Panel A, dr_first_line, eri | `output/phase2/main/decomp_reference.csv` | category = dr_first_line, d_base (unchanged in this scenario) [derived; see check] | -299251.205651269 |  |
| 166 | −1,911 | Table 3, Panel A, dr_later_lines, base | `output/phase2/main/decomp_reference.csv` | category = dr_later_lines, d_base | -1910715.31944843 |  |
| 167 | −2,197 | Table 3, Panel A, dr_later_lines, kext | `output/phase2/main/decomp_reference.csv` | category = dr_later_lines, d_kext | -2196899.90344332 |  |
| 168 | −955 | Table 3, Panel A, dr_later_lines, m50 | `output/phase2/main/decomp_reference.csv` | category = dr_later_lines, d_base x scenario multiplier 0.5 (input/params/parameters_v10.xlsx sheet シナリオ) [derived; see check] | -955357.659724215 |  |
| 169 | −332 | Table 3, Panel A, dr_later_lines, eri | `output/phase2/main/decomp_reference.csv` | category = dr_later_lines, d_base x scenario multiplier 0.1738789298940041 (input/params/parameters_v10.xlsx sheet シナリオ) [derived; see check] | -332233.13507777324 |  |
| 170 | −101 | Table 3, Panel A, terminal_care, base | `output/phase2/main/decomp_reference.csv` | category = terminal_care, d_base | -101251.189651018 |  |
| 171 | −101 | Table 3, Panel A, terminal_care, kext | `output/phase2/main/decomp_reference.csv` | category = terminal_care, d_kext | -100660.554821773 |  |
| 172 | −101 | Table 3, Panel A, terminal_care, m50 | `output/phase2/main/decomp_reference.csv` | category = terminal_care, d_base (unchanged in this scenario) [derived; see check] | -101251.189651018 |  |
| 173 | −101 | Table 3, Panel A, terminal_care, eri | `output/phase2/main/decomp_reference.csv` | category = terminal_care, d_base (unchanged in this scenario) [derived; see check] | -101251.189651018 |  |
| 174 | 19 | Table 3, Panel A, other, base | `output/phase2/main/decomp_reference.csv` | category = other, d_base | 19275.1254969553 |  |
| 175 | 19 | Table 3, Panel A, other, kext | `output/phase2/main/decomp_reference.csv` | category = other, d_kext | 19275.1254969553 |  |
| 176 | 19 | Table 3, Panel A, other, m50 | `output/phase2/main/decomp_reference.csv` | category = other, d_base (unchanged in this scenario) [derived; see check] | 19275.1254969553 |  |
| 177 | 19 | Table 3, Panel A, other, eri | `output/phase2/main/decomp_reference.csv` | category = other, d_base (unchanged in this scenario) [derived; see check] | 19275.1254969553 |  |
| 178 | 4,426 | Table 3, base, total | `output/phase2/main/det_reference.csv` | column = base, dC | 4426444.21182148 |  |
| 179 | −330 | Table 3, base, total | `output/phase2/main/psa_reference_summary.csv` | column = base, dC_lo | -330227.688151215 |  |
| 180 | 8,901 | Table 3, base, total | `output/phase2/main/psa_reference_summary.csv` | column = base, dC_hi | 8901031.51910191 |  |
| 181 | 2.156 | Table 3, base, QALY | `output/phase2/main/det_reference.csv` | column = base, dQ | 2.15634301985791 |  |
| 182 | 0.245 | Table 3, base, QALY | `output/phase2/main/psa_reference_summary.csv` | column = base, dQ_lo | 0.245084978196081 |  |
| 183 | 4.228 | Table 3, base, QALY | `output/phase2/main/psa_reference_summary.csv` | column = base, dQ_hi | 4.22838927384795 |  |
| 184 | 83.1 | Table 3, base, P(CE) 5M | `output/phase2/main/psa_reference_summary.csv` | column = base, p_ce_500 | 0.831 |  |
| 185 | 90.8 | Table 3, base, P(CE) 7.5M | `output/phase2/main/psa_reference_summary.csv` | column = base, p_ce_750 | 0.908 |  |
| 186 | 2,053 | Table 3, base, ICER | `output/phase2/main/det_reference.csv` | column = base, icer | 2052755.1373126 |  |
| 187 | 4,102 | Table 3, kext, total | `output/phase2/main/det_reference.csv` | column = kext, dC | 4101859.38763142 |  |
| 188 | −744 | Table 3, kext, total | `output/phase2/main/psa_reference_summary.csv` | column = kext, dC_lo | -744288.681675664 |  |
| 189 | 8,558 | Table 3, kext, total | `output/phase2/main/psa_reference_summary.csv` | column = kext, dC_hi | 8558249.78597497 |  |
| 190 | 2.137 | Table 3, kext, QALY | `output/phase2/main/det_reference.csv` | column = kext, dQ | 2.13682523039882 |  |
| 191 | 0.230 | Table 3, kext, QALY | `output/phase2/main/psa_reference_summary.csv` | column = kext, dQ_lo | 0.22966161874911 |  |
| 192 | 4.207 | Table 3, kext, QALY | `output/phase2/main/psa_reference_summary.csv` | column = kext, dQ_hi | 4.20734642632207 |  |
| 193 | 84.4 | Table 3, kext, P(CE) 5M | `output/phase2/main/psa_reference_summary.csv` | column = kext, p_ce_500 | 0.844 |  |
| 194 | 91.1 | Table 3, kext, P(CE) 7.5M | `output/phase2/main/psa_reference_summary.csv` | column = kext, p_ce_750 | 0.911 |  |
| 195 | 1,920 | Table 3, kext, ICER | `output/phase2/main/det_reference.csv` | column = kext, icer | 1919604.52791258 |  |
| 196 | 4,990 | Table 3, sjp, total | `output/phase2/main/scenario_reference.csv` | scenario = sjp, column = base, dC | 4989524.20858509 | 【要確認】S-JP 依赖 F01P |
| 197 | 1.639 | Table 3, sjp, QALY | `output/phase2/main/scenario_reference.csv` | scenario = sjp, column = base, dQ | 1.63888097707382 | 【要確認】S-JP 依赖 F01P |
| 198 | 3,044 | Table 3, sjp, ICER | `output/phase2/main/scenario_reference.csv` | scenario = sjp, column = base, icer | 3044470.14663246 | 【要確認】S-JP 依赖 F01P |
| 199 | 5,531 | Table 3, m50, total | `output/phase2/main/sc_metcost50_det_reference.csv` | column = base, dC | 5531427.47437133 |  |
| 200 | 3,093 | Table 3, m50, total | `output/phase2/main/sc_metcost50_psa_reference_summary.csv` | column = base, dC_lo | 3093347.65369722 |  |
| 201 | 7,822 | Table 3, m50, total | `output/phase2/main/sc_metcost50_psa_reference_summary.csv` | column = base, dC_hi | 7822101.43328648 |  |
| 202 | 2.156 | Table 3, m50, QALY | `output/phase2/main/sc_metcost50_det_reference.csv` | column = base, dQ | 2.15634301985791 |  |
| 203 | 0.245 | Table 3, m50, QALY | `output/phase2/main/sc_metcost50_psa_reference_summary.csv` | column = base, dQ_lo | 0.245084978196081 |  |
| 204 | 4.228 | Table 3, m50, QALY | `output/phase2/main/sc_metcost50_psa_reference_summary.csv` | column = base, dQ_hi | 4.22838927384795 |  |
| 205 | 82.1 | Table 3, m50, P(CE) 5M | `output/phase2/main/sc_metcost50_psa_reference_summary.csv` | column = base, p_ce_500 | 0.821 |  |
| 206 | 91.3 | Table 3, m50, P(CE) 7.5M | `output/phase2/main/sc_metcost50_psa_reference_summary.csv` | column = base, p_ce_750 | 0.913 |  |
| 207 | 2,565 | Table 3, m50, ICER | `output/phase2/main/sc_metcost50_det_reference.csv` | column = base, icer | 2565189.03691669 |  |
| 208 | 6,005 | Table 3, eri, total | `output/phase2/main/sc_eribulin_det_reference.csv` | column = base, dC | 6004926.39619214 |  |
| 209 | 3,759 | Table 3, eri, total | `output/phase2/main/sc_eribulin_psa_reference_summary.csv` | column = base, dC_lo | 3759354.1534946 |  |
| 210 | 8,229 | Table 3, eri, total | `output/phase2/main/sc_eribulin_psa_reference_summary.csv` | column = base, dC_hi | 8229266.7120642 |  |
| 211 | 2.156 | Table 3, eri, QALY | `output/phase2/main/sc_eribulin_det_reference.csv` | column = base, dQ | 2.15634301985791 |  |
| 212 | 0.245 | Table 3, eri, QALY | `output/phase2/main/sc_eribulin_psa_reference_summary.csv` | column = base, dQ_lo | 0.245084978196081 |  |
| 213 | 4.228 | Table 3, eri, QALY | `output/phase2/main/sc_eribulin_psa_reference_summary.csv` | column = base, dQ_hi | 4.22838927384795 |  |
| 214 | 80.3 | Table 3, eri, P(CE) 5M | `output/phase2/main/sc_eribulin_psa_reference_summary.csv` | column = base, p_ce_500 | 0.803 |  |
| 215 | 90.5 | Table 3, eri, P(CE) 7.5M | `output/phase2/main/sc_eribulin_psa_reference_summary.csv` | column = base, p_ce_750 | 0.905 |  |
| 216 | 2,785 | Table 3, eri, ICER | `output/phase2/main/sc_eribulin_det_reference.csv` | column = base, icer | 2784773.26700454 |  |
| 217 | 0.425 | Table 3, Panel C, HR | `output/phase2/main/det_yardstick.csv` | axis = hr0, root | 0.424844086027943 |  |
| 218 | 35.9 | Table 3, Panel C, pCR | `output/phase2/main/det_yardstick.csv` | axis = pcr, root x 100 | 35.8556422277975 |  |

### 派生值的核对（Table 3 的“转移复发治疗费 50%”“艾立布林”两栏的类别值）

- m50：类别之和 5531427.474371 日元，模型 5531427.474371 日元，差 4.657e-09 日元
- eri：类别之和 6004926.396192 日元，模型 6004926.396192 日元，差 1.863e-09 日元

## 3. Fig. 1–3（figures_v3.docx）

图中的线、带、柱直接由下列文件的列画出；刻度数字是标度，不登记。

| # | 显示 | 位置 | 来源文件 | 来源中的位置 | 原始值 | 暂定 |
|---|---|---|---|---|---|---|
| 1 | 13 points | Fig. 2, line, main | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.700 to 1.000 by 0.025, cap_500 / 1,000 | see file |  |
| 2 | 13 points | Fig. 2, band, main | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.700 to 1.000 by 0.025, cap500_lo and cap500_hi / 1,000 | see file |  |
| 3 | 13 points | Fig. 2, line, secondary | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.700 to 1.000 by 0.025, cap_500 / 1,000 | see file |  |
| 4 | 13 points | Fig. 2, band, secondary | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.700 to 1.000 by 0.025, cap500_lo and cap500_hi / 1,000 | see file |  |
| 5 | line | Fig. 2, horizontal line E01 | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G58 (E01) / 1,000 | 239508.135965065 |  |
| 6 | line | Fig. 2, horizontal line E02 | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G59 (E02) / 1,000 | 192400 |  |
| 7 | line | Fig. 2, horizontal line E03 | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G60 (E03) / 1,000 | 11260 | 【要確認】E03 |
| 8 | 21 | Fig. 3 legend (number of inputs that changed the result) | `output/phase2/main/oneway_base.csv` | rows with |cap_high - cap_low| > 1e-6 x cap_base (same rule as R/23_phase2b_report.R tornado()) | 21 |  |
| 9 | 21 rows | Fig. 3, bars | `output/phase2/main/oneway_base.csv` | param_id, cap_low, cap_high, cap_base / 1,000 | see file | 【要確認】含 D02 的一行 |
| 10 | 21 | Fig. 3 legend | `output/phase2/main/oneway_base.csv` | number of rows that change the result (see Fig. 3 bars) | 21 |  |

## 4. 补充表（supplement_v3.docx）

| # | 显示 | 位置 | 来源文件 | 来源中的位置 | 原始值 | 暂定 |
|---|---|---|---|---|---|---|
| 1 | 49 | Supplementary Table S1, Panel A, starting age | `manuscript/code/_build/engine_params_extract.csv (from data/fits/engine_params.rds)` | quantity = start_age | 49.0 |  |
| 2 | 494 | Supplementary Table S1, Panel A, pCR pembro | `data/pcr_counts.csv` | row K22 (IA4), pcr_pembro | 494 |  |
| 3 | 784 | Supplementary Table S1, Panel A, pCR pembro | `data/pcr_counts.csv` | row K22 (IA4), pcr_pembro + nonpcr_pembro | 784 |  |
| 4 | 63.0 | Supplementary Table S1, Panel A, pCR pembro | `data/pcr_counts.csv` | pcr / (pcr + nonpcr) | 0.6301020408163265 |  |
| 5 | 217 | Supplementary Table S1, Panel A, pCR placebo | `data/pcr_counts.csv` | row K22 (IA4), pcr_placebo | 217 |  |
| 6 | 390 | Supplementary Table S1, Panel A, pCR placebo | `data/pcr_counts.csv` | row K22 (IA4), pcr_placebo + nonpcr_placebo | 390 |  |
| 7 | 55.6 | Supplementary Table S1, Panel A, pCR placebo | `data/pcr_counts.csv` | pcr / (pcr + nonpcr) | 0.5564102564102564 |  |
| 8 | 90.4 | Supplementary Table S1, Panel A, efs_pcr_pembro | `data/kn522_final_7y.csv` | id = efs_pcr_pembro, value | 90.4 |  |
| 9 | 87.7 | Supplementary Table S1, Panel A, efs_target_EFS_pembro_pCR, 2.5th | `output/phase1/bootstrap_summary.csv` | quantity = efs_target_EFS_pembro_pCR, boot_lo | 87.6518218623482 |  |
| 10 | 92.9 | Supplementary Table S1, Panel A, efs_target_EFS_pembro_pCR, 97.5th | `output/phase1/bootstrap_summary.csv` | quantity = efs_target_EFS_pembro_pCR, boot_hi | 92.914979757085 |  |
| 11 | 57.6 | Supplementary Table S1, Panel A, efs_nonpcr_pembro | `data/kn522_final_7y.csv` | id = efs_nonpcr_pembro, value | 57.6 |  |
| 12 | 52.1 | Supplementary Table S1, Panel A, efs_target_EFS_pembro_nonpCR, 2.5th | `output/phase1/bootstrap_summary.csv` | quantity = efs_target_EFS_pembro_nonpCR, boot_lo | 52.0689655172414 |  |
| 13 | 63.4 | Supplementary Table S1, Panel A, efs_target_EFS_pembro_nonpCR, 97.5th | `output/phase1/bootstrap_summary.csv` | quantity = efs_target_EFS_pembro_nonpCR, boot_hi | 63.448275862069 |  |
| 14 | 85.9 | Supplementary Table S1, Panel A, efs_pcr_placebo | `data/kn522_final_7y.csv` | id = efs_pcr_placebo, value | 85.9 |  |
| 15 | 81.1 | Supplementary Table S1, Panel A, efs_target_EFS_placebo_pCR, 2.5th | `output/phase1/bootstrap_summary.csv` | quantity = efs_target_EFS_placebo_pCR, boot_lo | 81.1059907834101 |  |
| 16 | 90.3 | Supplementary Table S1, Panel A, efs_target_EFS_placebo_pCR, 97.5th | `output/phase1/bootstrap_summary.csv` | quantity = efs_target_EFS_placebo_pCR, boot_hi | 90.3225806451613 |  |
| 17 | 49.7 | Supplementary Table S1, Panel A, efs_nonpcr_placebo | `data/kn522_final_7y.csv` | id = efs_nonpcr_placebo, value | 49.7 |  |
| 18 | 41.6 | Supplementary Table S1, Panel A, efs_target_EFS_placebo_nonpCR, 2.5th | `output/phase1/bootstrap_summary.csv` | quantity = efs_target_EFS_placebo_nonpCR, boot_lo | 41.6184971098266 |  |
| 19 | 57.8 | Supplementary Table S1, Panel A, efs_target_EFS_placebo_nonpCR, 97.5th | `output/phase1/bootstrap_summary.csv` | quantity = efs_target_EFS_placebo_nonpCR, boot_hi | 57.8034682080925 |  |
| 20 | 0.6685 | Supplementary Table S1, Panel A, EFS_pembro_pCR_shape | `output/phase1/bootstrap_summary.csv` | quantity = EFS_pembro_pCR_shape, base | 0.668514164630413 |  |
| 21 | 0.5106 | Supplementary Table S1, Panel A, EFS_pembro_pCR_shape | `output/phase1/bootstrap_summary.csv` | quantity = EFS_pembro_pCR_shape, boot_lo | 0.510600186697401 |  |
| 22 | 0.9761 | Supplementary Table S1, Panel A, EFS_pembro_pCR_shape | `output/phase1/bootstrap_summary.csv` | quantity = EFS_pembro_pCR_shape, boot_hi | 0.976064423247597 |  |
| 23 | 198.2 | Supplementary Table S1, Panel A, EFS_pembro_pCR_scale | `output/phase1/bootstrap_summary.csv` | quantity = EFS_pembro_pCR_scale, base | 198.23330560128 |  |
| 24 | 59.79 | Supplementary Table S1, Panel A, EFS_pembro_pCR_scale | `output/phase1/bootstrap_summary.csv` | quantity = EFS_pembro_pCR_scale, boot_lo | 59.7856466726511 |  |
| 25 | 803.0 | Supplementary Table S1, Panel A, EFS_pembro_pCR_scale | `output/phase1/bootstrap_summary.csv` | quantity = EFS_pembro_pCR_scale, boot_hi | 803.036466952279 |  |
| 26 | 0.5961 | Supplementary Table S1, Panel A, EFS_pembro_nonpCR_theta | `output/phase1/bootstrap_summary.csv` | quantity = EFS_pembro_nonpCR_theta, base | 0.596140575887004 |  |
| 27 | 0.3655 | Supplementary Table S1, Panel A, EFS_pembro_nonpCR_theta | `output/phase1/bootstrap_summary.csv` | quantity = EFS_pembro_nonpCR_theta, boot_lo | 0.36553095264248 |  |
| 28 | 0.6769 | Supplementary Table S1, Panel A, EFS_pembro_nonpCR_theta | `output/phase1/bootstrap_summary.csv` | quantity = EFS_pembro_nonpCR_theta, boot_hi | 0.676945442884765 |  |
| 29 | 0.8468 | Supplementary Table S1, Panel A, EFS_pembro_nonpCR_shape | `output/phase1/bootstrap_summary.csv` | quantity = EFS_pembro_nonpCR_shape, base | 0.846753687559558 |  |
| 30 | 0.6664 | Supplementary Table S1, Panel A, EFS_pembro_nonpCR_shape | `output/phase1/bootstrap_summary.csv` | quantity = EFS_pembro_nonpCR_shape, boot_lo | 0.6663899840563 |  |
| 31 | 1.145 | Supplementary Table S1, Panel A, EFS_pembro_nonpCR_shape | `output/phase1/bootstrap_summary.csv` | quantity = EFS_pembro_nonpCR_shape, boot_hi | 1.14514943379396 |  |
| 32 | 1.683 | Supplementary Table S1, Panel A, EFS_pembro_nonpCR_scale | `output/phase1/bootstrap_summary.csv` | quantity = EFS_pembro_nonpCR_scale, base | 1.68275295440409 |  |
| 33 | 0.9405 | Supplementary Table S1, Panel A, EFS_pembro_nonpCR_scale | `output/phase1/bootstrap_summary.csv` | quantity = EFS_pembro_nonpCR_scale, boot_lo | 0.940511212950558 |  |
| 34 | 5.291 | Supplementary Table S1, Panel A, EFS_pembro_nonpCR_scale | `output/phase1/bootstrap_summary.csv` | quantity = EFS_pembro_nonpCR_scale, boot_hi | 5.29143031095246 |  |
| 35 | 0.7593 | Supplementary Table S1, Panel A, EFS_placebo_pCR_shape | `output/phase1/bootstrap_summary.csv` | quantity = EFS_placebo_pCR_shape, base | 0.759320201953044 |  |
| 36 | 0.5748 | Supplementary Table S1, Panel A, EFS_placebo_pCR_shape | `output/phase1/bootstrap_summary.csv` | quantity = EFS_placebo_pCR_shape, boot_lo | 0.574762898187373 |  |
| 37 | 1.164 | Supplementary Table S1, Panel A, EFS_placebo_pCR_shape | `output/phase1/bootstrap_summary.csv` | quantity = EFS_placebo_pCR_shape, boot_hi | 1.16370011692072 |  |
| 38 | 76.71 | Supplementary Table S1, Panel A, EFS_placebo_pCR_scale | `output/phase1/bootstrap_summary.csv` | quantity = EFS_placebo_pCR_scale, base | 76.7089772183217 |  |
| 39 | 28.14 | Supplementary Table S1, Panel A, EFS_placebo_pCR_scale | `output/phase1/bootstrap_summary.csv` | quantity = EFS_placebo_pCR_scale, boot_lo | 28.142554267582 |  |
| 40 | 284.7 | Supplementary Table S1, Panel A, EFS_placebo_pCR_scale | `output/phase1/bootstrap_summary.csv` | quantity = EFS_placebo_pCR_scale, boot_hi | 284.732855932272 |  |
| 41 | 0.5427 | Supplementary Table S1, Panel A, EFS_placebo_nonpCR_theta | `output/phase1/bootstrap_summary.csv` | quantity = EFS_placebo_nonpCR_theta, base | 0.542681102956425 |  |
| 42 | 0.4249 | Supplementary Table S1, Panel A, EFS_placebo_nonpCR_theta | `output/phase1/bootstrap_summary.csv` | quantity = EFS_placebo_nonpCR_theta, boot_lo | 0.42494589816945 |  |
| 43 | 0.6334 | Supplementary Table S1, Panel A, EFS_placebo_nonpCR_theta | `output/phase1/bootstrap_summary.csv` | quantity = EFS_placebo_nonpCR_theta, boot_hi | 0.633429684007878 |  |
| 44 | 1.216 | Supplementary Table S1, Panel A, EFS_placebo_nonpCR_shape | `output/phase1/bootstrap_summary.csv` | quantity = EFS_placebo_nonpCR_shape, base | 1.21576605809721 |  |
| 45 | 0.9402 | Supplementary Table S1, Panel A, EFS_placebo_nonpCR_shape | `output/phase1/bootstrap_summary.csv` | quantity = EFS_placebo_nonpCR_shape, boot_lo | 0.940184402119264 |  |
| 46 | 1.627 | Supplementary Table S1, Panel A, EFS_placebo_nonpCR_shape | `output/phase1/bootstrap_summary.csv` | quantity = EFS_placebo_nonpCR_shape, boot_hi | 1.6267105531547 |  |
| 47 | 1.424 | Supplementary Table S1, Panel A, EFS_placebo_nonpCR_scale | `output/phase1/bootstrap_summary.csv` | quantity = EFS_placebo_nonpCR_scale, base | 1.42372813975312 |  |
| 48 | 1.038 | Supplementary Table S1, Panel A, EFS_placebo_nonpCR_scale | `output/phase1/bootstrap_summary.csv` | quantity = EFS_placebo_nonpCR_scale, boot_lo | 1.03785829851619 |  |
| 49 | 2.451 | Supplementary Table S1, Panel A, EFS_placebo_nonpCR_scale | `output/phase1/bootstrap_summary.csv` | quantity = EFS_placebo_nonpCR_scale, boot_hi | 2.45068510968715 |  |
| 50 | 4.83 | Supplementary Table S1, Panel A, preprog pembro | `manuscript/code/_build/engine_params_extract.csv (from data/fits/engine_params.rds)` | quantity = preprog_share_nonpcr, arm = pembro | 0.0482758620689655 |  |
| 51 | 8.67 | Supplementary Table S1, Panel A, preprog placebo | `manuscript/code/_build/engine_params_extract.csv (from data/fits/engine_params.rds)` | quantity = preprog_share_nonpcr, arm = placebo | 0.0867052023121387 |  |
| 52 | 37.1 | Supplementary Table S1, Panel A, first events pembro | `manuscript/code/_build/engine_params_extract.csv (from data/fits/engine_params.rds)` | quantity = first_event_share_LRR, arm = pembro | 0.371101583251126 |  |
| 53 | 58.3 | Supplementary Table S1, Panel A, first events pembro | `manuscript/code/_build/engine_params_extract.csv (from data/fits/engine_params.rds)` | quantity = first_event_share_DR, arm = pembro | 0.583159630823198 |  |
| 54 | 4.6 | Supplementary Table S1, Panel A, first events pembro | `manuscript/code/_build/engine_params_extract.csv (from data/fits/engine_params.rds)` | quantity = first_event_share_death, arm = pembro | 0.0457387859256764 |  |
| 55 | 31.5 | Supplementary Table S1, Panel A, first events placebo | `manuscript/code/_build/engine_params_extract.csv (from data/fits/engine_params.rds)` | quantity = first_event_share_LRR, arm = placebo | 0.314785298570004 |  |
| 56 | 58.8 | Supplementary Table S1, Panel A, first events placebo | `manuscript/code/_build/engine_params_extract.csv (from data/fits/engine_params.rds)` | quantity = first_event_share_DR, arm = placebo | 0.587599223997341 |  |
| 57 | 9.8 | Supplementary Table S1, Panel A, first events placebo | `manuscript/code/_build/engine_params_extract.csv (from data/fits/engine_params.rds)` | quantity = first_event_share_death, arm = placebo | 0.0976154774326544 |  |
| 58 | 7 | Supplementary Table S1, Panel A, AE deaths pembro | `output/phase1/ae_deaths.csv` | arm = pembro, deaths | 7.0 |  |
| 59 | 783 | Supplementary Table S1, Panel A, AE deaths pembro | `output/phase1/ae_deaths.csv` | arm = pembro, n_treated | 783.0 |  |
| 60 | 1 | Supplementary Table S1, Panel A, AE deaths placebo | `output/phase1/ae_deaths.csv` | arm = placebo, deaths | 1.0 |  |
| 61 | 389 | Supplementary Table S1, Panel A, AE deaths placebo | `output/phase1/ae_deaths.csv` | arm = placebo, n_treated | 389.0 |  |
| 62 | 0.340 | Supplementary Table S1, Panel A, LRR to DR | `manuscript/code/_build/engine_params_extract.csv (from data/fits/engine_params.rds)` | quantity = lrr_dr_rate_per_year | 0.339542996040039 |  |
| 63 | 22 | Supplementary Table S1, Panel A, LRR to DR | `manuscript/code/_build/engine_params_extract.csv (from data/fits/engine_params.rds)` | quantity = lrr_dr_n_local_then_distant | 22.0 |  |
| 64 | 45 | Supplementary Table S1, Panel A, LRR to DR | `manuscript/code/_build/engine_params_extract.csv (from data/fits/engine_params.rds)` | quantity = lrr_dr_n_local | 45.0 |  |
| 65 | 1.98 | Supplementary Table S1, Panel A, LRR to DR | `manuscript/code/_build/engine_params_extract.csv (from data/fits/engine_params.rds)` | quantity = lrr_dr_exposure_years | 1.97668125 |  |
| 66 | 9.73 | Supplementary Table S1, Panel A, dr_median | `output/phase1/calibration.csv` | stage = calibrated, arm = pembro, dr_median_months | 9.73391157650877 |  |
| 67 | 9.10 | Supplementary Table S1, Panel A, dr_median, 2.5th | `output/phase1/bootstrap_summary.csv` | quantity = dr_median, boot_lo x 12.0 | 9.100004544386689 |  |
| 68 | 10.43 | Supplementary Table S1, Panel A, dr_median, 97.5th | `output/phase1/bootstrap_summary.csv` | quantity = dr_median, boot_hi x 12.0 | 10.431004116041413 |  |
| 69 | 16.93 | Supplementary Table S1, Panel A, dr_late_median | `output/phase1/calibration.csv` | stage = calibrated, arm = pembro, dr_late_median_months | 16.9299027330314 |  |
| 70 | 15.88 | Supplementary Table S1, Panel A, dr_late_median, 2.5th | `output/phase1/bootstrap_summary.csv` | quantity = dr_late_median, boot_lo x 12.0 | 15.88129719590064 |  |
| 71 | 18.01 | Supplementary Table S1, Panel A, dr_late_median, 97.5th | `output/phase1/bootstrap_summary.csv` | quantity = dr_late_median, boot_hi x 12.0 | 18.00744216919248 |  |
| 72 | 1.660 | Supplementary Table S1, Panel A, dr_shape | `output/phase1/calibration.csv` | stage = calibrated, arm = pembro, dr_shape | 1.65983596262318 |  |
| 73 | 1.590 | Supplementary Table S1, Panel A, dr_shape, 2.5th | `output/phase1/bootstrap_summary.csv` | quantity = dr_shape, boot_lo | 1.59021350242721 |  |
| 74 | 1.736 | Supplementary Table S1, Panel A, dr_shape, 97.5th | `output/phase1/bootstrap_summary.csv` | quantity = dr_shape, boot_hi | 1.73569802269134 |  |
| 75 | 1.307 | Supplementary Table S1, Panel A, k | `output/phase1/round14/kext_derivation.csv` | quantity = k_external, value | 1.30672744305531 |  |
| 76 | 26 | Supplementary Table S1, Panel A, Elmore | `output/phase1/round15/preprog_survival.csv` | setting = round 15 scenario Elmore, median_months | 26.0 |  |
| 77 | 113,736 | Supplementary Table S1, Panel B, A01, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G2 (A01) | 113736 |  |
| 78 | 85,302 | Supplementary Table S1, Panel B, A01, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H2 (A01) | 85302 |  |
| 79 | 113,736 | Supplementary Table S1, Panel B, A01, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I2 (A01) | 113736 |  |
| 80 | 33,496 | Supplementary Table S1, Panel B, A02, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G3 (A02) | 33496 |  |
| 81 | 25,122 | Supplementary Table S1, Panel B, A02, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H3 (A02) | 25122 |  |
| 82 | 33,496 | Supplementary Table S1, Panel B, A02, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I3 (A02) | 33496 |  |
| 83 | 398,924 | Supplementary Table S1, Panel B, A03, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G4 (A03) | 398924 |  |
| 84 | 299,193 | Supplementary Table S1, Panel B, A03, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H4 (A03) | 299193 |  |
| 85 | 398,924 | Supplementary Table S1, Panel B, A03, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I4 (A03) | 398924 |  |
| 86 | 15,565 | Supplementary Table S1, Panel B, A04, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G5 (A04) | 15565 |  |
| 87 | 10,768 | Supplementary Table S1, Panel B, A04, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H5 (A04) | 10767.5 |  |
| 88 | 18,160 | Supplementary Table S1, Panel B, A04, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I5 (A04) | 18160 |  |
| 89 | 68.12 | Supplementary Table S1, Panel B, A04, p1 | `data/params_dist.csv` | param_id = A04, p1 | 68.119547909593 |  |
| 90 | 228.5 | Supplementary Table S1, Panel B, A04, p2 | `data/params_dist.csv` | param_id = A04, p2 | 228.495350859603 |  |
| 91 | 36,558 | Supplementary Table S1, Panel B, A05, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G6 (A05) | 36557.5 |  |
| 92 | 5,820 | Supplementary Table S1, Panel B, A05, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H6 (A05) | 5819.5 |  |
| 93 | 67,296 | Supplementary Table S1, Panel B, A05, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I6 (A05) | 67295.5 |  |
| 94 | 5.434 | Supplementary Table S1, Panel B, A05, p1 | `data/params_dist.csv` | param_id = A05, p1 | 5.4337286508086 |  |
| 95 | 6,728 | Supplementary Table S1, Panel B, A05, p2 | `data/params_dist.csv` | param_id = A05, p2 | 6727.88472691949 |  |
| 96 | 1,000,000 | Supplementary Table S1, Panel B, A06, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G7 (A06) | 1000000 |  |
| 97 | 641,441 | Supplementary Table S1, Panel B, A06, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H7 (A06) | 641440.786 |  |
| 98 | 1,250,000 | Supplementary Table S1, Panel B, A06, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I7 (A06) | 1250000 |  |
| 99 | 41.49 | Supplementary Table S1, Panel B, A06, p1 | `data/params_dist.csv` | param_id = A06, p1 | 41.49067389385 |  |
| 100 | 24,102 | Supplementary Table S1, Panel B, A06, p2 | `data/params_dist.csv` | param_id = A06, p2 | 24101.8018304163 |  |
| 101 | 0.63230 | Supplementary Table S1, Panel B, A07, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G8 (A07) | 0.632299333333333 |  |
| 102 | 0.50600 | Supplementary Table S1, Panel B, A07, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H8 (A07) | 0.506 |  |
| 103 | 0.90000 | Supplementary Table S1, Panel B, A07, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I8 (A07) | 0.9 |  |
| 104 | 13.92 | Supplementary Table S1, Panel B, A07, p1 | `data/params_dist.csv` | param_id = A07, p1 | 13.9190609865372 |  |
| 105 | 8.094 | Supplementary Table S1, Panel B, A07, p2 | `data/params_dist.csv` | param_id = A07, p2 | 8.09434350838644 |  |
| 106 | 445,300 | Supplementary Table S1, Panel B, A08, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G9 (A08) | 445300 |  |
| 107 | 405,300 | Supplementary Table S1, Panel B, A08, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H9 (A08) | 405300 |  |
| 108 | 485,300 | Supplementary Table S1, Panel B, A08, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I9 (A08) | 485300 |  |
| 109 | 476.1 | Supplementary Table S1, Panel B, A08, p1 | `data/params_dist.csv` | param_id = A08, p1 | 476.081811377733 |  |
| 110 | 935.3 | Supplementary Table S1, Panel B, A08, p2 | `data/params_dist.csv` | param_id = A08, p2 | 935.343441731887 |  |
| 111 | 38,586 | Supplementary Table S1, Panel B, B01, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G10 (B01) | 38586 |  |
| 112 | 19,293 | Supplementary Table S1, Panel B, B01, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H10 (B01) | 19293 |  |
| 113 | 236,000 | Supplementary Table S1, Panel B, B01, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I10 (B01) | 236000 |  |
| 114 | 0.4872 | Supplementary Table S1, Panel B, B01, p1 | `data/params_dist.csv` | param_id = B01, p1 | 0.487157971390112 |  |
| 115 | 79,206 | Supplementary Table S1, Panel B, B01, p2 | `data/params_dist.csv` | param_id = B01, p2 | 79206.3401731769 |  |
| 116 | 38,856 | Supplementary Table S1, Panel B, B02, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G11 (B02) | 38856 |  |
| 117 | 19,428 | Supplementary Table S1, Panel B, B02, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H11 (B02) | 19428 |  |
| 118 | 236,000 | Supplementary Table S1, Panel B, B02, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I11 (B02) | 236000 |  |
| 119 | 0.4946 | Supplementary Table S1, Panel B, B02, p1 | `data/params_dist.csv` | param_id = B02, p1 | 0.494615520518277 |  |
| 120 | 78,558 | Supplementary Table S1, Panel B, B02, p2 | `data/params_dist.csv` | param_id = B02, p2 | 78557.9877462908 |  |
| 121 | 236,000 | Supplementary Table S1, Panel B, B03, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G12 (B03) | 236000 |  |
| 122 | 118,000 | Supplementary Table S1, Panel B, B03, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H12 (B03) | 118000 |  |
| 123 | 472,000 | Supplementary Table S1, Panel B, B03, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I12 (B03) | 472000 |  |
| 124 | 6.829 | Supplementary Table S1, Panel B, B03, p1 | `data/params_dist.csv` | param_id = B03, p1 | 6.82926012567844 |  |
| 125 | 34,557 | Supplementary Table S1, Panel B, B03, p2 | `data/params_dist.csv` | param_id = B03, p2 | 34557.184183485 |  |
| 126 | 236,000 | Supplementary Table S1, Panel B, B04, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G13 (B04) | 236000 |  |
| 127 | 118,000 | Supplementary Table S1, Panel B, B04, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H13 (B04) | 118000 |  |
| 128 | 472,000 | Supplementary Table S1, Panel B, B04, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I13 (B04) | 472000 |  |
| 129 | 6.829 | Supplementary Table S1, Panel B, B04, p1 | `data/params_dist.csv` | param_id = B04, p1 | 6.82926012567844 |  |
| 130 | 34,557 | Supplementary Table S1, Panel B, B04, p2 | `data/params_dist.csv` | param_id = B04, p2 | 34557.184183485 |  |
| 131 | 63,257 | Supplementary Table S1, Panel B, B05, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G14 (B05) | 63256.5 |  |
| 132 | 31,628 | Supplementary Table S1, Panel B, B05, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H14 (B05) | 31628.25 |  |
| 133 | 236,000 | Supplementary Table S1, Panel B, B05, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I14 (B05) | 236000 |  |
| 134 | 1.472 | Supplementary Table S1, Panel B, B05, p1 | `data/params_dist.csv` | param_id = B05, p1 | 1.47205746207536 |  |
| 135 | 42,971 | Supplementary Table S1, Panel B, B05, p2 | `data/params_dist.csv` | param_id = B05, p2 | 42971.4882942263 |  |
| 136 | 40,740 | Supplementary Table S1, Panel B, B06, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G15 (B06) | 40740 |  |
| 137 | 20,370 | Supplementary Table S1, Panel B, B06, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H15 (B06) | 20370 |  |
| 138 | 236,000 | Supplementary Table S1, Panel B, B06, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I15 (B06) | 236000 |  |
| 139 | 0.5485 | Supplementary Table S1, Panel B, B06, p1 | `data/params_dist.csv` | param_id = B06, p1 | 0.548504073075626 |  |
| 140 | 74,275 | Supplementary Table S1, Panel B, B06, p2 | `data/params_dist.csv` | param_id = B06, p2 | 74274.7447098408 |  |
| 141 | 40,740 | Supplementary Table S1, Panel B, B07, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G16 (B07) | 40740 |  |
| 142 | 20,370 | Supplementary Table S1, Panel B, B07, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H16 (B07) | 20370 |  |
| 143 | 236,000 | Supplementary Table S1, Panel B, B07, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I16 (B07) | 236000 |  |
| 144 | 0.5485 | Supplementary Table S1, Panel B, B07, p1 | `data/params_dist.csv` | param_id = B07, p1 | 0.548504073075626 |  |
| 145 | 74,275 | Supplementary Table S1, Panel B, B07, p2 | `data/params_dist.csv` | param_id = B07, p2 | 74274.7447098408 |  |
| 146 | 236,000 | Supplementary Table S1, Panel B, B08, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G17 (B08) | 236000 |  |
| 147 | 38,057 | Supplementary Table S1, Panel B, B08, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H17 (B08) | 38056.5 |  |
| 148 | 472,000 | Supplementary Table S1, Panel B, B08, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I17 (B08) | 472000 |  |
| 149 | 4.545 | Supplementary Table S1, Panel B, B08, p1 | `data/params_dist.csv` | param_id = B08, p1 | 4.54478982875085 |  |
| 150 | 51,928 | Supplementary Table S1, Panel B, B08, p2 | `data/params_dist.csv` | param_id = B08, p2 | 51927.5937705716 |  |
| 151 | 236,000 | Supplementary Table S1, Panel B, B09, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G18 (B09) | 236000 |  |
| 152 | 118,000 | Supplementary Table S1, Panel B, B09, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H18 (B09) | 118000 |  |
| 153 | 472,000 | Supplementary Table S1, Panel B, B09, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I18 (B09) | 472000 |  |
| 154 | 6.829 | Supplementary Table S1, Panel B, B09, p1 | `data/params_dist.csv` | param_id = B09, p1 | 6.82926012567844 |  |
| 155 | 34,557 | Supplementary Table S1, Panel B, B09, p2 | `data/params_dist.csv` | param_id = B09, p2 | 34557.184183485 |  |
| 156 | 236,000 | Supplementary Table S1, Panel B, B10, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G19 (B10) | 236000 |  |
| 157 | 118,000 | Supplementary Table S1, Panel B, B10, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H19 (B10) | 118000 |  |
| 158 | 472,000 | Supplementary Table S1, Panel B, B10, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I19 (B10) | 472000 |  |
| 159 | 6.829 | Supplementary Table S1, Panel B, B10, p1 | `data/params_dist.csv` | param_id = B10, p1 | 6.82926012567844 |  |
| 160 | 34,557 | Supplementary Table S1, Panel B, B10, p2 | `data/params_dist.csv` | param_id = B10, p2 | 34557.184183485 |  |
| 161 | 236,000 | Supplementary Table S1, Panel B, B11, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G20 (B11) | 236000 |  |
| 162 | 189,000 | Supplementary Table S1, Panel B, B11, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H20 (B11) | 189000 |  |
| 163 | 283,000 | Supplementary Table S1, Panel B, B11, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I20 (B11) | 283000 |  |
| 164 | 96.86 | Supplementary Table S1, Panel B, B11, p1 | `data/params_dist.csv` | param_id = B11, p1 | 96.8555411848709 |  |
| 165 | 2,437 | Supplementary Table S1, Panel B, B11, p2 | `data/params_dist.csv` | param_id = B11, p2 | 2436.61846408498 |  |
| 166 | 0.15070 | Supplementary Table S1, Panel B, B21P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G21 (B21P) | 0.1507 |  |
| 167 | 0.12636 | Supplementary Table S1, Panel B, B21P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H21 (B21P) | 0.12636 |  |
| 168 | 0.17771 | Supplementary Table S1, Panel B, B21P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I21 (B21P) | 0.17771 |  |
| 169 | 112.2 | Supplementary Table S1, Panel B, B21P, p1 | `data/params_dist.csv` | param_id = B21P, p1 | 112.248418748986 |  |
| 170 | 632.6 | Supplementary Table S1, Panel B, B21P, p2 | `data/params_dist.csv` | param_id = B21P, p2 | 632.598420992132 |  |
| 171 | 0.05656 | Supplementary Table S1, Panel B, B21C, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G22 (B21C) | 0.05656 |  |
| 172 | 0.03578 | Supplementary Table S1, Panel B, B21C, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H22 (B21C) | 0.03578 |  |
| 173 | 0.08438 | Supplementary Table S1, Panel B, B21C, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I22 (B21C) | 0.08438 |  |
| 174 | 19.58 | Supplementary Table S1, Panel B, B21C, p1 | `data/params_dist.csv` | param_id = B21C, p1 | 19.5777987496535 |  |
| 175 | 326.6 | Supplementary Table S1, Panel B, B21C, p2 | `data/params_dist.csv` | param_id = B21C, p2 | 326.564329073075 |  |
| 176 | 0.05236 | Supplementary Table S1, Panel B, B22P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G23 (B22P) | 0.05236 |  |
| 177 | 0.03783 | Supplementary Table S1, Panel B, B22P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H23 (B22P) | 0.03783 |  |
| 178 | 0.07037 | Supplementary Table S1, Panel B, B22P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I23 (B22P) | 0.07037 |  |
| 179 | 37.65 | Supplementary Table S1, Panel B, B22P, p1 | `data/params_dist.csv` | param_id = B22P, p1 | 37.6495833026441 |  |
| 180 | 681.4 | Supplementary Table S1, Panel B, B22P, p2 | `data/params_dist.csv` | param_id = B22P, p2 | 681.402809795983 |  |
| 181 | 0.01799 | Supplementary Table S1, Panel B, B22C, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G24 (B22C) | 0.01799 |  |
| 182 | 0.00726 | Supplementary Table S1, Panel B, B22C, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H24 (B22C) | 0.00726 |  |
| 183 | 0.03672 | Supplementary Table S1, Panel B, B22C, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I24 (B22C) | 0.03672 |  |
| 184 | 5.609 | Supplementary Table S1, Panel B, B22C, p1 | `data/params_dist.csv` | param_id = B22C, p1 | 5.60890648003387 |  |
| 185 | 306.2 | Supplementary Table S1, Panel B, B22C, p2 | `data/params_dist.csv` | param_id = B22C, p2 | 306.170219703061 |  |
| 186 | 0.02554 | Supplementary Table S1, Panel B, B23P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G25 (B23P) | 0.02554 |  |
| 187 | 0.01567 | Supplementary Table S1, Panel B, B23P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H25 (B23P) | 0.01567 |  |
| 188 | 0.03917 | Supplementary Table S1, Panel B, B23P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I25 (B23P) | 0.03917 |  |
| 189 | 17.66 | Supplementary Table S1, Panel B, B23P, p1 | `data/params_dist.csv` | param_id = B23P, p1 | 17.6603227922825 |  |
| 190 | 673.8 | Supplementary Table S1, Panel B, B23P, p2 | `data/params_dist.csv` | param_id = B23P, p2 | 673.816685519484 |  |
| 191 | 0.00000 | Supplementary Table S1, Panel B, B23C, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G26 (B23C) | 0 |  |
| 192 | 0.00000 | Supplementary Table S1, Panel B, B23C, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H26 (B23C) | 0 |  |
| 193 | 0.00944 | Supplementary Table S1, Panel B, B23C, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I26 (B23C) | 0.00944 |  |
| 194 | 0.01916 | Supplementary Table S1, Panel B, B24P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G27 (B24P) | 0.01916 |  |
| 195 | 0.01076 | Supplementary Table S1, Panel B, B24P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H27 (B24P) | 0.01076 |  |
| 196 | 0.03140 | Supplementary Table S1, Panel B, B24P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I27 (B24P) | 0.0314 |  |
| 197 | 12.97 | Supplementary Table S1, Panel B, B24P, p1 | `data/params_dist.csv` | param_id = B24P, p1 | 12.9683521125842 |  |
| 198 | 663.9 | Supplementary Table S1, Panel B, B24P, p2 | `data/params_dist.csv` | param_id = B24P, p2 | 663.87674770914 |  |
| 199 | 0.00257 | Supplementary Table S1, Panel B, B24C, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G28 (B24C) | 0.00257 |  |
| 200 | 0.00007 | Supplementary Table S1, Panel B, B24C, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H28 (B24C) | 7e-05 |  |
| 201 | 0.01424 | Supplementary Table S1, Panel B, B24C, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I28 (B24C) | 0.01424 |  |
| 202 | 0.5016 | Supplementary Table S1, Panel B, B24C, p1 | `data/params_dist.csv` | param_id = B24C, p1 | 0.501586239011122 |  |
| 203 | 194.7 | Supplementary Table S1, Panel B, B24C, p2 | `data/params_dist.csv` | param_id = B24C, p2 | 194.668156566873 |  |
| 204 | 0.00894 | Supplementary Table S1, Panel B, B25P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G29 (B25P) | 0.00894 |  |
| 205 | 0.00360 | Supplementary Table S1, Panel B, B25P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H29 (B25P) | 0.0036 |  |
| 206 | 0.01833 | Supplementary Table S1, Panel B, B25P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I29 (B25P) | 0.01833 |  |
| 207 | 5.601 | Supplementary Table S1, Panel B, B25P, p1 | `data/params_dist.csv` | param_id = B25P, p1 | 5.6005795414894 |  |
| 208 | 620.9 | Supplementary Table S1, Panel B, B25P, p2 | `data/params_dist.csv` | param_id = B25P, p2 | 620.862456419294 |  |
| 209 | 0.00514 | Supplementary Table S1, Panel B, B25C, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G30 (B25C) | 0.00514 |  |
| 210 | 0.00062 | Supplementary Table S1, Panel B, B25C, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H30 (B25C) | 0.00062 |  |
| 211 | 0.01845 | Supplementary Table S1, Panel B, B25C, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I30 (B25C) | 0.01845 |  |
| 212 | 1.265 | Supplementary Table S1, Panel B, B25C, p1 | `data/params_dist.csv` | param_id = B25C, p1 | 1.26526353836146 |  |
| 213 | 244.9 | Supplementary Table S1, Panel B, B25C, p2 | `data/params_dist.csv` | param_id = B25C, p2 | 244.89495793274 |  |
| 214 | 0.00766 | Supplementary Table S1, Panel B, B26P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G31 (B26P) | 0.00766 |  |
| 215 | 0.00282 | Supplementary Table S1, Panel B, B26P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H31 (B26P) | 0.00282 |  |
| 216 | 0.01660 | Supplementary Table S1, Panel B, B26P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I31 (B26P) | 0.0166 |  |
| 217 | 4.704 | Supplementary Table S1, Panel B, B26P, p1 | `data/params_dist.csv` | param_id = B26P, p1 | 4.70401986957571 |  |
| 218 | 609.4 | Supplementary Table S1, Panel B, B26P, p2 | `data/params_dist.csv` | param_id = B26P, p2 | 609.397790779995 |  |
| 219 | 0.00000 | Supplementary Table S1, Panel B, B26C, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G32 (B26C) | 0 |  |
| 220 | 0.00000 | Supplementary Table S1, Panel B, B26C, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H32 (B26C) | 0 |  |
| 221 | 0.00944 | Supplementary Table S1, Panel B, B26C, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I32 (B26C) | 0.00944 |  |
| 222 | 0.01149 | Supplementary Table S1, Panel B, B27P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G33 (B27P) | 0.01149 |  |
| 223 | 0.00527 | Supplementary Table S1, Panel B, B27P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H33 (B27P) | 0.00527 |  |
| 224 | 0.02171 | Supplementary Table S1, Panel B, B27P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I33 (B27P) | 0.02171 |  |
| 225 | 7.408 | Supplementary Table S1, Panel B, B27P, p1 | `data/params_dist.csv` | param_id = B27P, p1 | 7.4079934672521 |  |
| 226 | 637.3 | Supplementary Table S1, Panel B, B27P, p2 | `data/params_dist.csv` | param_id = B27P, p2 | 637.325989757474 |  |
| 227 | 0.00000 | Supplementary Table S1, Panel B, B27C, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G34 (B27C) | 0 |  |
| 228 | 0.00000 | Supplementary Table S1, Panel B, B27C, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H34 (B27C) | 0 |  |
| 229 | 0.00944 | Supplementary Table S1, Panel B, B27C, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I34 (B27C) | 0.00944 |  |
| 230 | 0.04725 | Supplementary Table S1, Panel B, B28P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G35 (B28P) | 0.04725 |  |
| 231 | 0.03349 | Supplementary Table S1, Panel B, B28P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H35 (B28P) | 0.03349 |  |
| 232 | 0.06455 | Supplementary Table S1, Panel B, B28P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I35 (B28P) | 0.06455 |  |
| 233 | 33.83 | Supplementary Table S1, Panel B, B28P, p1 | `data/params_dist.csv` | param_id = B28P, p1 | 33.8321611783112 |  |
| 234 | 682.2 | Supplementary Table S1, Panel B, B28P, p2 | `data/params_dist.csv` | param_id = B28P, p2 | 682.192414024043 |  |
| 235 | 0.00257 | Supplementary Table S1, Panel B, B28C, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G36 (B28C) | 0.00257 |  |
| 236 | 0.00007 | Supplementary Table S1, Panel B, B28C, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H36 (B28C) | 7e-05 |  |
| 237 | 0.01424 | Supplementary Table S1, Panel B, B28C, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I36 (B28C) | 0.01424 |  |
| 238 | 0.5016 | Supplementary Table S1, Panel B, B28C, p1 | `data/params_dist.csv` | param_id = B28C, p1 | 0.501586239011122 |  |
| 239 | 194.7 | Supplementary Table S1, Panel B, B28C, p2 | `data/params_dist.csv` | param_id = B28C, p2 | 194.668156566873 |  |
| 240 | 0.00511 | Supplementary Table S1, Panel B, B29P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G37 (B29P) | 0.00511 |  |
| 241 | 0.00139 | Supplementary Table S1, Panel B, B29P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H37 (B29P) | 0.00139 |  |
| 242 | 0.01303 | Supplementary Table S1, Panel B, B29P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I37 (B29P) | 0.01303 |  |
| 243 | 2.941 | Supplementary Table S1, Panel B, B29P, p1 | `data/params_dist.csv` | param_id = B29P, p1 | 2.94112292551552 |  |
| 244 | 572.6 | Supplementary Table S1, Panel B, B29P, p2 | `data/params_dist.csv` | param_id = B29P, p2 | 572.621093418031 |  |
| 245 | 0.00000 | Supplementary Table S1, Panel B, B29C, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G38 (B29C) | 0 |  |
| 246 | 0.00000 | Supplementary Table S1, Panel B, B29C, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H38 (B29C) | 0 |  |
| 247 | 0.00944 | Supplementary Table S1, Panel B, B29C, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I38 (B29C) | 0.00944 |  |
| 248 | 0.02043 | Supplementary Table S1, Panel B, B30P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G39 (B30P) | 0.02043 |  |
| 249 | 0.01172 | Supplementary Table S1, Panel B, B30P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H39 (B30P) | 0.01172 |  |
| 250 | 0.03297 | Supplementary Table S1, Panel B, B30P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I39 (B30P) | 0.03297 |  |
| 251 | 13.89 | Supplementary Table S1, Panel B, B30P, p1 | `data/params_dist.csv` | param_id = B30P, p1 | 13.8922409578008 |  |
| 252 | 666.1 | Supplementary Table S1, Panel B, B30P, p2 | `data/params_dist.csv` | param_id = B30P, p2 | 666.099974304108 |  |
| 253 | 0.00257 | Supplementary Table S1, Panel B, B30C, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G40 (B30C) | 0.00257 |  |
| 254 | 0.00007 | Supplementary Table S1, Panel B, B30C, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H40 (B30C) | 7e-05 |  |
| 255 | 0.01424 | Supplementary Table S1, Panel B, B30C, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I40 (B30C) | 0.01424 |  |
| 256 | 0.5016 | Supplementary Table S1, Panel B, B30C, p1 | `data/params_dist.csv` | param_id = B30C, p1 | 0.501586239011122 |  |
| 257 | 194.7 | Supplementary Table S1, Panel B, B30C, p2 | `data/params_dist.csv` | param_id = B30C, p2 | 194.668156566873 |  |
| 258 | 0.18391 | Supplementary Table S1, Panel B, B31P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G41 (B31P) | 0.18391 |  |
| 259 | 0.15737 | Supplementary Table S1, Panel B, B31P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H41 (B31P) | 0.15737 |  |
| 260 | 0.21285 | Supplementary Table S1, Panel B, B31P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I41 (B31P) | 0.21285 |  |
| 261 | 137.6 | Supplementary Table S1, Panel B, B31P, p1 | `data/params_dist.csv` | param_id = B31P, p1 | 137.610631349131 |  |
| 262 | 610.6 | Supplementary Table S1, Panel B, B31P, p2 | `data/params_dist.csv` | param_id = B31P, p2 | 610.639226457031 |  |
| 263 | 0.16195 | Supplementary Table S1, Panel B, B31C, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G42 (B31C) | 0.16195 |  |
| 264 | 0.12675 | Supplementary Table S1, Panel B, B31C, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H42 (B31C) | 0.12675 |  |
| 265 | 0.20240 | Supplementary Table S1, Panel B, B31C, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I42 (B31C) | 0.2024 |  |
| 266 | 58.85 | Supplementary Table S1, Panel B, B31C, p1 | `data/params_dist.csv` | param_id = B31C, p1 | 58.8541007285721 |  |
| 267 | 304.6 | Supplementary Table S1, Panel B, B31C, p2 | `data/params_dist.csv` | param_id = B31C, p2 | 304.554980645754 |  |
| 268 | 0.82375 | Supplementary Table S1, Panel B, B32P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G43 (B32P) | 0.82375 |  |
| 269 | 0.79522 | Supplementary Table S1, Panel B, B32P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H43 (B32P) | 0.79522 |  |
| 270 | 0.84982 | Supplementary Table S1, Panel B, B32P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I43 (B32P) | 0.84982 |  |
| 271 | 615.6 | Supplementary Table S1, Panel B, B32P, p1 | `data/params_dist.csv` | param_id = B32P, p1 | 615.616330983291 |  |
| 272 | 131.7 | Supplementary Table S1, Panel B, B32P, p2 | `data/params_dist.csv` | param_id = B32P, p2 | 131.717606477457 |  |
| 273 | 0.78663 | Supplementary Table S1, Panel B, B32C, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G44 (B32C) | 0.78663 |  |
| 274 | 0.74253 | Supplementary Table S1, Panel B, B32C, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H44 (B32C) | 0.74253 |  |
| 275 | 0.82631 | Supplementary Table S1, Panel B, B32C, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I44 (B32C) | 0.82631 |  |
| 276 | 288.2 | Supplementary Table S1, Panel B, B32C, p1 | `data/params_dist.csv` | param_id = B32C, p1 | 288.247966172197 |  |
| 277 | 78.19 | Supplementary Table S1, Panel B, B32C, p2 | `data/params_dist.csv` | param_id = B32C, p2 | 78.1860195290819 |  |
| 278 | 1.064 | Supplementary Table S1, Panel B, B33P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G45 (B33P) | 1.06386 |  |
| 279 | 0.993 | Supplementary Table S1, Panel B, B33P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H45 (B33P) | 0.99283 |  |
| 280 | 1.139 | Supplementary Table S1, Panel B, B33P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I45 (B33P) | 1.13862 |  |
| 281 | 818.2 | Supplementary Table S1, Panel B, B33P, p1 | `data/params_dist.csv` | param_id = B33P, p1 | 818.219191648461 |  |
| 282 | 0.001300 | Supplementary Table S1, Panel B, B33P, p2 | `data/params_dist.csv` | param_id = B33P, p2 | 0.0013002139412748 |  |
| 283 | 0.982 | Supplementary Table S1, Panel B, B33C, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G46 (B33C) | 0.98201 |  |
| 284 | 0.886 | Supplementary Table S1, Panel B, B33C, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H46 (B33C) | 0.88599 |  |
| 285 | 1.086 | Supplementary Table S1, Panel B, B33C, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I46 (B33C) | 1.08559 |  |
| 286 | 371.9 | Supplementary Table S1, Panel B, B33C, p1 | `data/params_dist.csv` | param_id = B33C, p1 | 371.934890064942 |  |
| 287 | 0.002640 | Supplementary Table S1, Panel B, B33C, p2 | `data/params_dist.csv` | param_id = B33C, p2 | 0.0026402739464117 |  |
| 288 | 18,270 | Supplementary Table S1, Panel B, C01, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G47 (C01) | 18270 |  |
| 289 | 11,660 | Supplementary Table S1, Panel B, C01, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H47 (C01) | 11660 |  |
| 290 | 24,880 | Supplementary Table S1, Panel B, C01, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I47 (C01) | 24880 |  |
| 291 | 29.35 | Supplementary Table S1, Panel B, C01, p1 | `data/params_dist.csv` | param_id = C01, p1 | 29.3474490809568 |  |
| 292 | 622.5 | Supplementary Table S1, Panel B, C01, p2 | `data/params_dist.csv` | param_id = C01, p2 | 622.541330580421 |  |
| 293 | 16,730 | Supplementary Table S1, Panel B, C02, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G48 (C02) | 16730 |  |
| 294 | 10,120 | Supplementary Table S1, Panel B, C02, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H48 (C02) | 10120 |  |
| 295 | 23,340 | Supplementary Table S1, Panel B, C02, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I48 (C02) | 23340 |  |
| 296 | 24.61 | Supplementary Table S1, Panel B, C02, p1 | `data/params_dist.csv` | param_id = C02, p1 | 24.6085001534524 |  |
| 297 | 679.8 | Supplementary Table S1, Panel B, C02, p2 | `data/params_dist.csv` | param_id = C02, p2 | 679.846390299121 |  |
| 298 | 15,960 | Supplementary Table S1, Panel B, C03, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G49 (C03) | 15960 |  |
| 299 | 9,350 | Supplementary Table S1, Panel B, C03, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H49 (C03) | 9350 |  |
| 300 | 22,570 | Supplementary Table S1, Panel B, C03, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I49 (C03) | 22570 |  |
| 301 | 22.40 | Supplementary Table S1, Panel B, C03, p1 | `data/params_dist.csv` | param_id = C03, p1 | 22.3954110043079 |  |
| 302 | 712.6 | Supplementary Table S1, Panel B, C03, p2 | `data/params_dist.csv` | param_id = C03, p2 | 712.64599684864 |  |
| 303 | 1,222,650 | Supplementary Table S1, Panel B, D01, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G50 (D01) | 1222650 |  |
| 304 | 916,988 | Supplementary Table S1, Panel B, D01, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H50 (D01) | 916987.5 |  |
| 305 | 1,528,313 | Supplementary Table S1, Panel B, D01, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I50 (D01) | 1528312.5 |  |
| 306 | 61.46 | Supplementary Table S1, Panel B, D01, p1 | `data/params_dist.csv` | param_id = D01, p1 | 61.463341131106 |  |
| 307 | 19,892 | Supplementary Table S1, Panel B, D01, p2 | `data/params_dist.csv` | param_id = D01, p2 | 19892.3452174849 |  |
| 308 | 3,045 | Supplementary Table S1, Panel B, D02, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G51 (D02) | 3045 | 【要確認】D02 |
| 309 | 2,284 | Supplementary Table S1, Panel B, D02, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H51 (D02) | 2283.75 | 【要確認】D02 |
| 310 | 3,806 | Supplementary Table S1, Panel B, D02, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I51 (D02) | 3806.25 | 【要確認】D02 |
| 311 | 61.46 | Supplementary Table S1, Panel B, D02, p1 | `data/params_dist.csv` | param_id = D02, p1 | 61.463341131106 | 【要確認】D02 |
| 312 | 49.54 | Supplementary Table S1, Panel B, D02, p2 | `data/params_dist.csv` | param_id = D02, p2 | 49.5417259127646 | 【要確認】D02 |
| 313 | 1,215,933 | Supplementary Table S1, Panel B, D03, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G52 (D03) | 1215932.77556 |  |
| 314 | 915,446 | Supplementary Table S1, Panel B, D03, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H52 (D03) | 915445.948078572 |  |
| 315 | 1,416,257 | Supplementary Table S1, Panel B, D03, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I52 (D03) | 1416257.32721429 |  |
| 316 | 90.58 | Supplementary Table S1, Panel B, D03, p1 | `data/params_dist.csv` | param_id = D03, p1 | 90.5788760236816 |  |
| 317 | 13,424 | Supplementary Table S1, Panel B, D03, p2 | `data/params_dist.csv` | param_id = D03, p2 | 13424.0214599494 |  |
| 318 | 1,458,318 | Supplementary Table S1, Panel B, D03P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G53 (D03P) | 1458318.23014286 |  |
| 319 | 973,662 | Supplementary Table S1, Panel B, D03P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H53 (D03P) | 973662.056785714 |  |
| 320 | 1,781,422 | Supplementary Table S1, Panel B, D03P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I53 (D03P) | 1781422.34571429 |  |
| 321 | 50.08 | Supplementary Table S1, Panel B, D03P, p1 | `data/params_dist.csv` | param_id = D03P, p1 | 50.0836285488757 |  |
| 322 | 29,118 | Supplementary Table S1, Panel B, D03P, p2 | `data/params_dist.csv` | param_id = D03P, p2 | 29117.6632443816 |  |
| 323 | 10.37 | Supplementary Table S1, Panel B, D04, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G54 (D04) | 10.36576 |  |
| 324 | 7.77 | Supplementary Table S1, Panel B, D04, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H54 (D04) | 7.77432 |  |
| 325 | 12.96 | Supplementary Table S1, Panel B, D04, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I54 (D04) | 12.9572 |  |
| 326 | 61.46 | Supplementary Table S1, Panel B, D04, p1 | `data/params_dist.csv` | param_id = D04, p1 | 61.463341131106 |  |
| 327 | 0.1686 | Supplementary Table S1, Panel B, D04, p2 | `data/params_dist.csv` | param_id = D04, p2 | 0.168649471526272 |  |
| 328 | 10.84 | Supplementary Table S1, Panel B, D04P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G55 (D04P) | 10.84 |  |
| 329 | 8.13 | Supplementary Table S1, Panel B, D04P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H55 (D04P) | 8.13 |  |
| 330 | 13.55 | Supplementary Table S1, Panel B, D04P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I55 (D04P) | 13.55 |  |
| 331 | 61.46 | Supplementary Table S1, Panel B, D04P, p1 | `data/params_dist.csv` | param_id = D04P, p1 | 61.463341131106 |  |
| 332 | 0.1764 | Supplementary Table S1, Panel B, D04P, p2 | `data/params_dist.csv` | param_id = D04P, p2 | 0.176365290277296 |  |
| 333 | 1,412,953 | Supplementary Table S1, Panel B, D05, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G56 (D05) | 1412953.27571429 |  |
| 334 | 1,059,715 | Supplementary Table S1, Panel B, D05, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H56 (D05) | 1059714.95678572 |  |
| 335 | 1,766,192 | Supplementary Table S1, Panel B, D05, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I56 (D05) | 1766191.59464286 |  |
| 336 | 61.46 | Supplementary Table S1, Panel B, D05, p1 | `data/params_dist.csv` | param_id = D05, p1 | 61.4633411311069 |  |
| 337 | 22,989 | Supplementary Table S1, Panel B, D05, p2 | `data/params_dist.csv` | param_id = D05, p2 | 22988.5530091886 |  |
| 338 | 1,120,001 | Supplementary Table S1, Panel B, D06, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G57 (D06) | 1120000.5 |  |
| 339 | 956,901 | Supplementary Table S1, Panel B, D06, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H57 (D06) | 956901 |  |
| 340 | 1,283,100 | Supplementary Table S1, Panel B, D06, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I57 (D06) | 1283100 |  |
| 341 | 181.1 | Supplementary Table S1, Panel B, D06, p1 | `data/params_dist.csv` | param_id = D06, p1 | 181.145419088774 |  |
| 342 | 6,183 | Supplementary Table S1, Panel B, D06, p2 | `data/params_dist.csv` | param_id = D06, p2 | 6182.88061400616 |  |
| 343 | 239,508 | Supplementary Table S1, Panel B, E01, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G58 (E01) | 239508.135965065 |  |
| 344 | 95,803 | Supplementary Table S1, Panel B, E01, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H58 (E01) | 95803.2543860259 |  |
| 345 | 322,320 | Supplementary Table S1, Panel B, E01, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I58 (E01) | 322320.44198895 |  |
| 346 | 17.18 | Supplementary Table S1, Panel B, E01, p1 | `data/params_dist.csv` | param_id = E01, p1 | 17.1788620867368 |  |
| 347 | 13,942 | Supplementary Table S1, Panel B, E01, p2 | `data/params_dist.csv` | param_id = E01, p2 | 13942.0256566342 |  |
| 348 | 192,400 | Supplementary Table S1, Panel B, E02, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G59 (E02) | 192400 |  |
| 349 | 96,200 | Supplementary Table S1, Panel B, E02, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H59 (E02) | 96200 |  |
| 350 | 232,440 | Supplementary Table S1, Panel B, E02, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I59 (E02) | 232440 |  |
| 351 | 30.64 | Supplementary Table S1, Panel B, E02, p1 | `data/params_dist.csv` | param_id = E02, p1 | 30.6448174671071 |  |
| 352 | 6,278 | Supplementary Table S1, Panel B, E02, p2 | `data/params_dist.csv` | param_id = E02, p2 | 6278.38622979282 |  |
| 353 | 11,260 | Supplementary Table S1, Panel B, E03, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G60 (E03) | 11260 | 【要確認】E03 |
| 354 | 8,445 | Supplementary Table S1, Panel B, E03, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H60 (E03) | 8445 | 【要確認】E03 |
| 355 | 14,075 | Supplementary Table S1, Panel B, E03, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I60 (E03) | 14075 | 【要確認】E03 |
| 356 | 61.46 | Supplementary Table S1, Panel B, E03, p1 | `data/params_dist.csv` | param_id = E03, p1 | 61.463341131106 | 【要確認】E03 |
| 357 | 183.2 | Supplementary Table S1, Panel B, E03, p2 | `data/params_dist.csv` | param_id = E03, p2 | 183.198631782505 | 【要確認】E03 |
| 358 | 3,700 | Supplementary Table S1, Panel B, E04, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G61 (E04) | 3700 |  |
| 359 | 1,260 | Supplementary Table S1, Panel B, E04, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H61 (E04) | 1260 |  |
| 360 | 7,400 | Supplementary Table S1, Panel B, E04, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I61 (E04) | 7400 |  |
| 361 | 5.580 | Supplementary Table S1, Panel B, E04, p1 | `data/params_dist.csv` | param_id = E04, p1 | 5.57985456135371 |  |
| 362 | 663.1 | Supplementary Table S1, Panel B, E04, p2 | `data/params_dist.csv` | param_id = E04, p2 | 663.099720488478 |  |
| 363 | 30.00 | Supplementary Table S1, Panel B, E05, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G62 (E05) | 30 |  |
| 364 | 6.00 | Supplementary Table S1, Panel B, E05, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H62 (E05) | 6 |  |
| 365 | 30.00 | Supplementary Table S1, Panel B, E05, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I62 (E05) | 30 |  |
| 366 | 24.01 | Supplementary Table S1, Panel B, E05, p1 | `data/params_dist.csv` | param_id = E05, p1 | 24.0091176293383 |  |
| 367 | 1.250 | Supplementary Table S1, Panel B, E05, p2 | `data/params_dist.csv` | param_id = E05, p2 | 1.24952530380963 |  |
| 368 | 0.18458 | Supplementary Table S1, Panel B, E06, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G63 (E06) | 0.18458 |  |
| 369 | 0.14895 | Supplementary Table S1, Panel B, E06, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H63 (E06) | 0.14895 |  |
| 370 | 0.22464 | Supplementary Table S1, Panel B, E06, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I63 (E06) | 0.22464 |  |
| 371 | 74.33 | Supplementary Table S1, Panel B, E06, p1 | `data/params_dist.csv` | param_id = E06, p1 | 74.3280350642086 |  |
| 372 | 328.4 | Supplementary Table S1, Panel B, E06, p2 | `data/params_dist.csv` | param_id = E06, p2 | 328.35933661316 |  |
| 373 | 0.11497 | Supplementary Table S1, Panel B, E07, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G64 (E07) | 0.11497 |  |
| 374 | 0.08731 | Supplementary Table S1, Panel B, E07, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H64 (E07) | 0.08731 |  |
| 375 | 0.14767 | Supplementary Table S1, Panel B, E07, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I64 (E07) | 0.14767 |  |
| 376 | 49.22 | Supplementary Table S1, Panel B, E07, p1 | `data/params_dist.csv` | param_id = E07, p1 | 49.2233964381052 |  |
| 377 | 378.9 | Supplementary Table S1, Panel B, E07, p2 | `data/params_dist.csv` | param_id = E07, p2 | 378.917826821051 |  |
| 378 | 8,810 | Supplementary Table S1, Panel B, E08, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G65 (E08) | 8810 |  |
| 379 | 6,540 | Supplementary Table S1, Panel B, E08, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H65 (E08) | 6540 |  |
| 380 | 11,080 | Supplementary Table S1, Panel B, E08, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I65 (E08) | 11080 |  |
| 381 | 57.86 | Supplementary Table S1, Panel B, E08, p1 | `data/params_dist.csv` | param_id = E08, p1 | 57.8623788493619 |  |
| 382 | 152.3 | Supplementary Table S1, Panel B, E08, p2 | `data/params_dist.csv` | param_id = E08, p2 | 152.257825813484 |  |
| 383 | 0.00701 | Supplementary Table S1, Panel B, E09, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G66 (E09) | 0.00701 |  |
| 384 | 0.00145 | Supplementary Table S1, Panel B, E09, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H66 (E09) | 0.00145 |  |
| 385 | 0.02035 | Supplementary Table S1, Panel B, E09, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I66 (E09) | 0.02035 |  |
| 386 | 2.092 | Supplementary Table S1, Panel B, E09, p1 | `data/params_dist.csv` | param_id = E09, p1 | 2.09199501334142 |  |
| 387 | 296.3 | Supplementary Table S1, Panel B, E09, p2 | `data/params_dist.csv` | param_id = E09, p2 | 296.338106747203 |  |
| 388 | 0.00217 | Supplementary Table S1, Panel B, E10, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G67 (E10) | 0.00217 |  |
| 389 | 0.00005 | Supplementary Table S1, Panel B, E10, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H67 (E10) | 5e-05 |  |
| 390 | 0.01203 | Supplementary Table S1, Panel B, E10, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I67 (E10) | 0.01203 |  |
| 391 | 0.5009 | Supplementary Table S1, Panel B, E10, p1 | `data/params_dist.csv` | param_id = E10, p1 | 0.500888581558025 |  |
| 392 | 230.3 | Supplementary Table S1, Panel B, E10, p2 | `data/params_dist.csv` | param_id = E10, p2 | 230.323342551172 |  |
| 393 | 0.85000 | Supplementary Table S1, Panel B, F01, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G68 (F01) | 0.85 |  |
| 394 | 0.80000 | Supplementary Table S1, Panel B, F01, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H68 (F01) | 0.8 |  |
| 395 | 0.90000 | Supplementary Table S1, Panel B, F01, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I68 (F01) | 0.9 |  |
| 396 | 165.7 | Supplementary Table S1, Panel B, F01, p1 | `data/params_dist.csv` | param_id = F01, p1 | 165.67723987709 |  |
| 397 | 29.24 | Supplementary Table S1, Panel B, F01, p2 | `data/params_dist.csv` | param_id = F01, p2 | 29.2371599783101 |  |
| 398 | 0.50000 | Supplementary Table S1, Panel B, F01P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G69 (F01P) | 0.5 | 【要確認】S-JP 依赖 F01P |
| 399 | 0.05000 | Supplementary Table S1, Panel B, F01P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H69 (F01P) | 0.05 | 【要確認】S-JP 依赖 F01P |
| 400 | 0.90000 | Supplementary Table S1, Panel B, F01P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I69 (F01P) | 0.9 | 【要確認】S-JP 依赖 F01P |
| 401 | 2.158 | Supplementary Table S1, Panel B, F01P, p1 | `data/params_dist.csv` | param_id = F01P, p1 | 2.15844901086099 |  |
| 402 | 2.158 | Supplementary Table S1, Panel B, F01P, p2 | `data/params_dist.csv` | param_id = F01P, p2 | 2.15844901086099 |  |
| 403 | 121,402 | Supplementary Table S1, Panel B, F02, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G70 (F02) | 121401.6 |  |
| 404 | 91,051 | Supplementary Table S1, Panel B, F02, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H70 (F02) | 91051.2 |  |
| 405 | 203,251 | Supplementary Table S1, Panel B, F02, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I70 (F02) | 203251.2 |  |
| 406 | 17.99 | Supplementary Table S1, Panel B, F02, p1 | `data/params_dist.csv` | param_id = F02, p1 | 17.9895077801589 |  |
| 407 | 6,748 | Supplementary Table S1, Panel B, F02, p2 | `data/params_dist.csv` | param_id = F02, p2 | 6748.46702219929 |  |
| 408 | 0.20000 | Supplementary Table S1, Panel B, F03, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G71 (F03) | 0.2 |  |
| 409 | 0.15000 | Supplementary Table S1, Panel B, F03, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H71 (F03) | 0.15 |  |
| 410 | 0.25000 | Supplementary Table S1, Panel B, F03, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I71 (F03) | 0.25 |  |
| 411 | 48.97 | Supplementary Table S1, Panel B, F03, p1 | `data/params_dist.csv` | param_id = F03, p1 | 48.9706729048848 |  |
| 412 | 195.9 | Supplementary Table S1, Panel B, F03, p2 | `data/params_dist.csv` | param_id = F03, p2 | 195.882691619539 |  |
| 413 | 0.90000 | Supplementary Table S1, Panel B, F04, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G72 (F04) | 0.9 |  |
| 414 | 0.70000 | Supplementary Table S1, Panel B, F04, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H72 (F04) | 0.7 |  |
| 415 | 1.00000 | Supplementary Table S1, Panel B, F04, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I72 (F04) | 1 |  |
| 416 | 12.93 | Supplementary Table S1, Panel B, F04, p1 | `data/params_dist.csv` | param_id = F04, p1 | 12.9292517544988 |  |
| 417 | 1.437 | Supplementary Table S1, Panel B, F04, p2 | `data/params_dist.csv` | param_id = F04, p2 | 1.43658352827765 |  |
| 418 | 0.90000 | Supplementary Table S1, Panel B, F04P, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G73 (F04P) | 0.9 |  |
| 419 | 0.50000 | Supplementary Table S1, Panel B, F04P, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H73 (F04P) | 0.5 |  |
| 420 | 1.00000 | Supplementary Table S1, Panel B, F04P, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I73 (F04P) | 1 |  |
| 421 | 4.079 | Supplementary Table S1, Panel B, F04P, p1 | `data/params_dist.csv` | param_id = F04P, p1 | 4.07853063161958 |  |
| 422 | 0.4532 | Supplementary Table S1, Panel B, F04P, p2 | `data/params_dist.csv` | param_id = F04P, p2 | 0.453170070179954 |  |
| 423 | 7,079,040 | Supplementary Table S1, Panel B, F05, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G74 (F05) | 7079040 |  |
| 424 | 3,539,520 | Supplementary Table S1, Panel B, F05, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H74 (F05) | 3539520 |  |
| 425 | 7,079,040 | Supplementary Table S1, Panel B, F05, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I74 (F05) | 7079040 |  |
| 426 | 203,000 | Supplementary Table S1, Panel B, F06, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G75 (F06) | 203000 |  |
| 427 | 193,000 | Supplementary Table S1, Panel B, F06, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H75 (F06) | 193000 |  |
| 428 | 213,000 | Supplementary Table S1, Panel B, F06, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I75 (F06) | 213000 |  |
| 429 | 1,583 | Supplementary Table S1, Panel B, F06, p1 | `data/params_dist.csv` | param_id = F06, p1 | 1583.02676541984 |  |
| 430 | 128.2 | Supplementary Table S1, Panel B, F06, p2 | `data/params_dist.csv` | param_id = F06, p2 | 128.235355481284 |  |
| 431 | 0.58 | Supplementary Table S1, Panel B, F07, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G76 (F07) | 0.58 |  |
| 432 | 0.39 | Supplementary Table S1, Panel B, F07, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H76 (F07) | 0.39 |  |
| 433 | 0.87 | Supplementary Table S1, Panel B, F07, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I76 (F07) | 0.87 |  |
| 434 | −0.5447 | Supplementary Table S1, Panel B, F07, p1 | `data/params_dist.csv` | param_id = F07, p1 | -0.544727175441672 |  |
| 435 | 0.2047 | Supplementary Table S1, Panel B, F07, p2 | `data/params_dist.csv` | param_id = F07, p2 | 0.204683983699125 |  |
| 436 | 0.65 | Supplementary Table S1, Panel B, F08, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G77 (F08) | 0.65 |  |
| 437 | 0.53 | Supplementary Table S1, Panel B, F08, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H77 (F08) | 0.53 |  |
| 438 | 0.78 | Supplementary Table S1, Panel B, F08, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I77 (F08) | 0.78 |  |
| 439 | −0.4308 | Supplementary Table S1, Panel B, F08, p1 | `data/params_dist.csv` | param_id = F08, p1 | -0.430782916092454 |  |
| 440 | 0.09858 | Supplementary Table S1, Panel B, F08, p2 | `data/params_dist.csv` | param_id = F08, p2 | 0.0985775545330111 |  |
| 441 | 0.889 | Supplementary Table S1, Panel B, U01, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G78 (U01) | 0.889 |  |
| 442 | 0.881 | Supplementary Table S1, Panel B, U01, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H78 (U01) | 0.8812 |  |
| 443 | 0.897 | Supplementary Table S1, Panel B, U01, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I78 (U01) | 0.8968 |  |
| 444 | 5,538 | Supplementary Table S1, Panel B, U01, p1 | `data/params_dist.csv` | param_id = U01, p1 | 5538.13793961054 |  |
| 445 | 691.5 | Supplementary Table S1, Panel B, U01, p2 | `data/params_dist.csv` | param_id = U01, p2 | 691.488539141473 |  |
| 446 | 0.887 | Supplementary Table S1, Panel B, U02, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G79 (U02) | 0.887 |  |
| 447 | 0.877 | Supplementary Table S1, Panel B, U02, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H79 (U02) | 0.8772 |  |
| 448 | 0.897 | Supplementary Table S1, Panel B, U02, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I79 (U02) | 0.8968 |  |
| 449 | 3,555 | Supplementary Table S1, Panel B, U02, p1 | `data/params_dist.csv` | param_id = U02, p1 | 3555.17818933309 |  |
| 450 | 452.9 | Supplementary Table S1, Panel B, U02, p2 | `data/params_dist.csv` | param_id = U02, p2 | 452.914470568928 |  |
| 451 | 0.830 | Supplementary Table S1, Panel B, U03, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G80 (U03) | 0.83 |  |
| 452 | 0.787 | Supplementary Table S1, Panel B, U03, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H80 (U03) | 0.7869 |  |
| 453 | 0.873 | Supplementary Table S1, Panel B, U03, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I80 (U03) | 0.8731 |  |
| 454 | 241.4 | Supplementary Table S1, Panel B, U03, p1 | `data/params_dist.csv` | param_id = U03, p1 | 241.354724925012 |  |
| 455 | 49.43 | Supplementary Table S1, Panel B, U03, p2 | `data/params_dist.csv` | param_id = U03, p2 | 49.4341002858458 |  |
| 456 | 0.735 | Supplementary Table S1, Panel B, U04, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G81 (U04) | 0.735 |  |
| 457 | 0.700 | Supplementary Table S1, Panel B, U04, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H81 (U04) | 0.6997 |  |
| 458 | 0.770 | Supplementary Table S1, Panel B, U04, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I81 (U04) | 0.7703 |  |
| 459 | 440.6 | Supplementary Table S1, Panel B, U04, p1 | `data/params_dist.csv` | param_id = U04, p1 | 440.598935930401 |  |
| 460 | 158.9 | Supplementary Table S1, Panel B, U04, p2 | `data/params_dist.csv` | param_id = U04, p2 | 158.855398668784 |  |
| 461 | 0.022 | Supplementary Table S1, Panel B, U05, base | `input/params/parameters_v10.xlsx` | sheet パラメータ cell G82 (U05) | 0.022 |  |
| 462 | 0.000 | Supplementary Table S1, Panel B, U05, low | `input/params/parameters_v10.xlsx` | sheet パラメータ cell H82 (U05) | 0 |  |
| 463 | 0.059 | Supplementary Table S1, Panel B, U05, high | `input/params/parameters_v10.xlsx` | sheet パラメータ cell I82 (U05) | 0.059 |  |
| 464 | 2.067 | Supplementary Table S1, Panel B, U05, p1 | `data/params_dist.csv` | param_id = U05, p1 | 2.06747108956415 |  |
| 465 | 91.91 | Supplementary Table S1, Panel B, U05, p2 | `data/params_dist.csv` | param_id = U05, p2 | 91.9084875269883 |  |
| 466 | 1 | Supplementary Table S2, Panel A, year | `output/phase1/calibration_gate.csv` | month = 12 / 12 | 1 |  |
| 467 | 97.2 | Supplementary Table S2, Panel A, pembro 12 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 12, km | 97.1889575641417 |  |
| 468 | 96.0 | Supplementary Table S2, Panel A, pembro 12 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 12, ci95_lo | 96.0378119687505 |  |
| 469 | 98.4 | Supplementary Table S2, Panel A, pembro 12 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 12, ci95_hi | 98.3539012267174 |  |
| 470 | 98.0 | Supplementary Table S2, Panel A, pembro 12 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 12, engine | 98.0031933544027 |  |
| 471 | 98.7 | Supplementary Table S2, Panel A, placebo 12 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 12, km | 98.7179487179487 |  |
| 472 | 97.6 | Supplementary Table S2, Panel A, placebo 12 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 12, ci95_lo | 97.607718911536 |  |
| 473 | 99.8 | Supplementary Table S2, Panel A, placebo 12 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 12, ci95_hi | 99.840806728737 |  |
| 474 | 97.9 | Supplementary Table S2, Panel A, placebo 12 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 12, engine | 97.9466832925982 |  |
| 475 | 2 | Supplementary Table S2, Panel A, year | `output/phase1/calibration_gate.csv` | month = 24 / 12 | 2 |  |
| 476 | 92.2 | Supplementary Table S2, Panel A, pembro 24 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 24, km | 92.2002242016099 |  |
| 477 | 90.3 | Supplementary Table S2, Panel A, pembro 24 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 24, ci95_lo | 90.3397682672189 |  |
| 478 | 94.1 | Supplementary Table S2, Panel A, pembro 24 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 24, ci95_hi | 94.0989943397032 |  |
| 479 | 94.5 | Supplementary Table S2, Panel A, pembro 24 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 24, engine | 94.5104815057816 |  |
| 480 | 91.0 | Supplementary Table S2, Panel A, placebo 24 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 24, km | 91.0213675213676 |  |
| 481 | 88.2 | Supplementary Table S2, Panel A, placebo 24 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 24, ci95_lo | 88.2272049252933 |  |
| 482 | 93.9 | Supplementary Table S2, Panel A, placebo 24 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 24, ci95_hi | 93.9040214690596 |  |
| 483 | 92.2 | Supplementary Table S2, Panel A, placebo 24 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 24, engine | 92.2028943890153 |  |
| 484 | 3 | Supplementary Table S2, Panel A, year | `output/phase1/calibration_gate.csv` | month = 36 / 12 | 3 |  |
| 485 | 89.5 | Supplementary Table S2, Panel A, pembro 36 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 36, km | 89.5095999377472 |  |
| 486 | 87.4 | Supplementary Table S2, Panel A, pembro 36 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 36, ci95_lo | 87.3869305197701 |  |
| 487 | 91.7 | Supplementary Table S2, Panel A, pembro 36 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 36, ci95_hi | 91.6838299887757 |  |
| 488 | 91.7 | Supplementary Table S2, Panel A, pembro 36 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 36, engine | 91.7062440140556 |  |
| 489 | 86.9 | Supplementary Table S2, Panel A, placebo 36 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 36, km | 86.9028831007071 |  |
| 490 | 83.6 | Supplementary Table S2, Panel A, placebo 36 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 36, ci95_lo | 83.615568426269 |  |
| 491 | 90.3 | Supplementary Table S2, Panel A, placebo 36 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 36, ci95_hi | 90.3194373171605 |  |
| 492 | 87.6 | Supplementary Table S2, Panel A, placebo 36 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 36, engine | 87.5857196746797 |  |
| 493 | 4 | Supplementary Table S2, Panel A, year | `output/phase1/calibration_gate.csv` | month = 48 / 12 | 4 |  |
| 494 | 87.8 | Supplementary Table S2, Panel A, pembro 48 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 48, km | 87.8410234758521 |  |
| 495 | 85.6 | Supplementary Table S2, Panel A, pembro 48 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 48, ci95_lo | 85.5789619737478 |  |
| 496 | 90.2 | Supplementary Table S2, Panel A, pembro 48 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 48, ci95_hi | 90.1628768020367 |  |
| 497 | 89.2 | Supplementary Table S2, Panel A, pembro 48 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 48, engine | 89.2067534884269 |  |
| 498 | 83.5 | Supplementary Table S2, Panel A, placebo 48 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 48, km | 83.5319303548649 |  |
| 499 | 79.9 | Supplementary Table S2, Panel A, placebo 48 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 48, ci95_lo | 79.9239050633645 |  |
| 500 | 87.3 | Supplementary Table S2, Panel A, placebo 48 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 48, ci95_hi | 87.3028336550636 |  |
| 501 | 83.7 | Supplementary Table S2, Panel A, placebo 48 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 48, engine | 83.7100766177509 |  |
| 502 | 5 | Supplementary Table S2, Panel A, year | `output/phase1/calibration_gate.csv` | month = 60 / 12 | 5 |  |
| 503 | 86.6 | Supplementary Table S2, Panel A, pembro 60 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 60, km | 86.5516825738285 |  |
| 504 | 84.2 | Supplementary Table S2, Panel A, pembro 60 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 60, ci95_lo | 84.191130100389 |  |
| 505 | 89.0 | Supplementary Table S2, Panel A, pembro 60 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 60, ci95_hi | 88.9784202614731 |  |
| 506 | 86.9 | Supplementary Table S2, Panel A, pembro 60 | `output/phase1/calibration_gate.csv` | arm = pembro, month = 60, engine | 86.9497143622995 |  |
| 507 | 81.7 | Supplementary Table S2, Panel A, placebo 60 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 60, km | 81.7062702065303 |  |
| 508 | 77.9 | Supplementary Table S2, Panel A, placebo 60 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 60, ci95_lo | 77.9478195513071 |  |
| 509 | 85.6 | Supplementary Table S2, Panel A, placebo 60 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 60, ci95_hi | 85.6459440365525 |  |
| 510 | 80.5 | Supplementary Table S2, Panel A, placebo 60 | `output/phase1/calibration_gate.csv` | arm = placebo, month = 60, engine | 80.5121963906288 |  |
| 511 | 0.0985 | Supplementary Table S2, Panel B | `output/phase1/calibration_gate_rmst.csv` | km | 0.0984983828339958 |  |
| 512 | −0.0381 | Supplementary Table S2, Panel B | `output/phase1/calibration_gate_rmst.csv` | km_boot_ci95_lo | -0.0380528344287493 |  |
| 513 | 0.2421 | Supplementary Table S2, Panel B | `output/phase1/calibration_gate_rmst.csv` | km_boot_ci95_hi | 0.242089365569215 |  |
| 514 | 0.1524 | Supplementary Table S2, Panel B | `output/phase1/calibration_gate_rmst.csv` | engine | 0.152363910107302 |  |
| 515 | 85.1 | Supplementary Table S2, Panel C, os7_pembro | `output/phase1/calibration_final7y.csv` | id = os7_pembro, value | 85.1 |  |
| 516 | 82.5 | Supplementary Table S2, Panel C, os7_pembro | `output/phase1/calibration_final7y.csv` | id = os7_pembro, ci95_lo | 82.5 |  |
| 517 | 87.5 | Supplementary Table S2, Panel C, os7_pembro | `output/phase1/calibration_final7y.csv` | id = os7_pembro, ci95_hi | 87.5 |  |
| 518 | 83.2 | Supplementary Table S2, Panel C, os7_pembro | `output/phase1/calibration_final7y.csv` | id = os7_pembro, engine | 83.2398941811347 |  |
| 519 | 77.2 | Supplementary Table S2, Panel C, os7_placebo | `output/phase1/calibration_final7y.csv` | id = os7_placebo, value | 77.2 |  |
| 520 | 72.7 | Supplementary Table S2, Panel C, os7_placebo | `output/phase1/calibration_final7y.csv` | id = os7_placebo, ci95_lo | 72.7 |  |
| 521 | 81.1 | Supplementary Table S2, Panel C, os7_placebo | `output/phase1/calibration_final7y.csv` | id = os7_placebo, ci95_hi | 81.1 |  |
| 522 | 75.8 | Supplementary Table S2, Panel C, os7_placebo | `output/phase1/calibration_final7y.csv` | id = os7_placebo, engine | 75.8033428985808 |  |
| 523 | 78.3 | Supplementary Table S2, Panel C, efs7_pembro | `output/phase1/calibration_final7y.csv` | id = efs7_pembro, value | 78.3 |  |
| 524 | 75.3 | Supplementary Table S2, Panel C, efs7_pembro | `output/phase1/calibration_final7y.csv` | id = efs7_pembro, ci95_lo | 75.3 |  |
| 525 | 81.1 | Supplementary Table S2, Panel C, efs7_pembro | `output/phase1/calibration_final7y.csv` | id = efs7_pembro, ci95_hi | 81.1 |  |
| 526 | 78.3 | Supplementary Table S2, Panel C, efs7_pembro | `output/phase1/calibration_final7y.csv` | id = efs7_pembro, engine | 78.2673469387755 |  |
| 527 | 69.8 | Supplementary Table S2, Panel C, efs7_placebo | `output/phase1/calibration_final7y.csv` | id = efs7_placebo, value | 69.8 |  |
| 528 | 65.0 | Supplementary Table S2, Panel C, efs7_placebo | `output/phase1/calibration_final7y.csv` | id = efs7_placebo, ci95_lo | 65.0 |  |
| 529 | 74.2 | Supplementary Table S2, Panel C, efs7_placebo | `output/phase1/calibration_final7y.csv` | id = efs7_placebo, ci95_hi | 74.2 |  |
| 530 | 69.8 | Supplementary Table S2, Panel C, efs7_placebo | `output/phase1/calibration_final7y.csv` | id = efs7_placebo, engine | 69.8420512820513 |  |
| 531 | 94.5 | Supplementary Table S2, Panel C, os_pcr_pembro | `output/phase1/calibration_final7y.csv` | id = os_pcr_pembro, value | 94.5 |  |
| 532 | 93.2 | Supplementary Table S2, Panel C, os_pcr_pembro | `output/phase1/calibration_final7y.csv` | id = os_pcr_pembro, engine | 93.1879758519972 |  |
| 533 | 91.1 | Supplementary Table S2, Panel C, os_pcr_placebo | `output/phase1/calibration_final7y.csv` | id = os_pcr_placebo, value | 91.1 |  |
| 534 | 90.2 | Supplementary Table S2, Panel C, os_pcr_placebo | `output/phase1/calibration_final7y.csv` | id = os_pcr_placebo, engine | 90.2000532820433 |  |
| 535 | 69.0 | Supplementary Table S2, Panel C, os_nonpcr_pembro | `output/phase1/calibration_final7y.csv` | id = os_nonpcr_pembro, value | 69.0 |  |
| 536 | 66.3 | Supplementary Table S2, Panel C, os_nonpcr_pembro | `output/phase1/calibration_final7y.csv` | id = os_nonpcr_pembro, engine | 66.293851610769 |  |
| 537 | 59.8 | Supplementary Table S2, Panel C, os_nonpcr_placebo | `output/phase1/calibration_final7y.csv` | id = os_nonpcr_placebo, value | 59.8 |  |
| 538 | 57.7 | Supplementary Table S2, Panel C, os_nonpcr_placebo | `output/phase1/calibration_final7y.csv` | id = os_nonpcr_placebo, engine | 57.7450414349312 |  |
| 539 | 79.3 | Supplementary Table S2, Panel D, OS_10y_pembro_all | `output/phase1/bootstrap_summary.csv` | quantity = OS_10y_pembro_all, base | 79.2761589677087 |  |
| 540 | 76.5 | Supplementary Table S2, Panel D, OS_10y_pembro_all | `output/phase1/bootstrap_summary.csv` | quantity = OS_10y_pembro_all, boot_lo | 76.4813781323067 |  |
| 541 | 82.0 | Supplementary Table S2, Panel D, OS_10y_pembro_all | `output/phase1/bootstrap_summary.csv` | quantity = OS_10y_pembro_all, boot_hi | 81.9668560589016 |  |
| 542 | 71.6 | Supplementary Table S2, Panel D, OS_20y_pembro_all | `output/phase1/bootstrap_summary.csv` | quantity = OS_20y_pembro_all, base | 71.6468838624189 |  |
| 543 | 65.2 | Supplementary Table S2, Panel D, OS_20y_pembro_all | `output/phase1/bootstrap_summary.csv` | quantity = OS_20y_pembro_all, boot_lo | 65.1746430469087 |  |
| 544 | 76.0 | Supplementary Table S2, Panel D, OS_20y_pembro_all | `output/phase1/bootstrap_summary.csv` | quantity = OS_20y_pembro_all, boot_hi | 75.9700790039844 |  |
| 545 | 71.1 | Supplementary Table S2, Panel D, OS_10y_chemo_all | `output/phase1/bootstrap_summary.csv` | quantity = OS_10y_chemo_all, base | 71.1344578440501 |  |
| 546 | 66.6 | Supplementary Table S2, Panel D, OS_10y_chemo_all | `output/phase1/bootstrap_summary.csv` | quantity = OS_10y_chemo_all, boot_lo | 66.5859311309447 |  |
| 547 | 75.3 | Supplementary Table S2, Panel D, OS_10y_chemo_all | `output/phase1/bootstrap_summary.csv` | quantity = OS_10y_chemo_all, boot_hi | 75.28461464179 |  |
| 548 | 61.7 | Supplementary Table S2, Panel D, OS_20y_chemo_all | `output/phase1/bootstrap_summary.csv` | quantity = OS_20y_chemo_all, base | 61.7388772083542 |  |
| 549 | 52.3 | Supplementary Table S2, Panel D, OS_20y_chemo_all | `output/phase1/bootstrap_summary.csv` | quantity = OS_20y_chemo_all, boot_lo | 52.2654059303494 |  |
| 550 | 68.0 | Supplementary Table S2, Panel D, OS_20y_chemo_all | `output/phase1/bootstrap_summary.csv` | quantity = OS_20y_chemo_all, boot_hi | 68.0003567421987 |  |
| 551 | 76.0 | Supplementary Table S2, Panel D, EFS_10y_pembro_all | `output/phase1/bootstrap_summary.csv` | quantity = EFS_10y_pembro_all, base | 76.0284631831042 |  |
| 552 | 72.0 | Supplementary Table S2, Panel D, EFS_10y_pembro_all | `output/phase1/bootstrap_summary.csv` | quantity = EFS_10y_pembro_all, boot_lo | 71.988302122837 |  |
| 553 | 79.7 | Supplementary Table S2, Panel D, EFS_10y_pembro_all | `output/phase1/bootstrap_summary.csv` | quantity = EFS_10y_pembro_all, boot_hi | 79.6654390135681 |  |
| 554 | 70.7 | Supplementary Table S2, Panel D, EFS_20y_pembro_all | `output/phase1/bootstrap_summary.csv` | quantity = EFS_20y_pembro_all, base | 70.7341251084516 |  |
| 555 | 62.6 | Supplementary Table S2, Panel D, EFS_20y_pembro_all | `output/phase1/bootstrap_summary.csv` | quantity = EFS_20y_pembro_all, boot_lo | 62.6336854595369 |  |
| 556 | 75.5 | Supplementary Table S2, Panel D, EFS_20y_pembro_all | `output/phase1/bootstrap_summary.csv` | quantity = EFS_20y_pembro_all, boot_hi | 75.5296853403704 |  |
| 557 | 67.3 | Supplementary Table S2, Panel D, EFS_10y_chemo_all | `output/phase1/bootstrap_summary.csv` | quantity = EFS_10y_chemo_all, base | 67.258386826658 |  |
| 558 | 61.1 | Supplementary Table S2, Panel D, EFS_10y_chemo_all | `output/phase1/bootstrap_summary.csv` | quantity = EFS_10y_chemo_all, boot_lo | 61.0575401892912 |  |
| 559 | 72.1 | Supplementary Table S2, Panel D, EFS_10y_chemo_all | `output/phase1/bootstrap_summary.csv` | quantity = EFS_10y_chemo_all, boot_hi | 72.1305113610167 |  |
| 560 | 60.1 | Supplementary Table S2, Panel D, EFS_20y_chemo_all | `output/phase1/bootstrap_summary.csv` | quantity = EFS_20y_chemo_all, base | 60.1240002136683 |  |
| 561 | 48.4 | Supplementary Table S2, Panel D, EFS_20y_chemo_all | `output/phase1/bootstrap_summary.csv` | quantity = EFS_20y_chemo_all, boot_lo | 48.3566082265628 |  |
| 562 | 67.1 | Supplementary Table S2, Panel D, EFS_20y_chemo_all | `output/phase1/bootstrap_summary.csv` | quantity = EFS_20y_chemo_all, boot_hi | 67.126875938465 |  |
| 563 | 5,596 | Supplementary Table S4, A, hr0 0.700, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.700, cap_500 | 5595776.10847557 |  |
| 564 | 4,545 | Supplementary Table S4, A, hr0 0.700, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.700, cap500_lo | 4545499.30391027 |  |
| 565 | 6,256 | Supplementary Table S4, A, hr0 0.700, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.700, cap500_hi | 6256345.34624927 |  |
| 566 | 100.0 | Supplementary Table S4, A, hr0 0.700, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.700, p_cap500_ge_E02 | 1.0 |  |
| 567 | 5,524 | Supplementary Table S4, A, hr0 0.700, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.700, cap_500 | 5523541.74007503 |  |
| 568 | 4,491 | Supplementary Table S4, A, hr0 0.700, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.700, cap500_lo | 4491469.48151977 |  |
| 569 | 6,164 | Supplementary Table S4, A, hr0 0.700, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.700, cap500_hi | 6164180.9681631 |  |
| 570 | 100.0 | Supplementary Table S4, A, hr0 0.700, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.700, p_cap500_ge_E02 | 1.0 |  |
| 571 | 7,107 | Supplementary Table S4, A, hr0 0.700, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.700, cap_500 | 7106810.66807256 |  |
| 572 | 5,923 | Supplementary Table S4, A, hr0 0.700, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.700, cap500_lo | 5923067.31247807 |  |
| 573 | 7,869 | Supplementary Table S4, A, hr0 0.700, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.700, cap500_hi | 7868859.01713853 |  |
| 574 | 100.0 | Supplementary Table S4, A, hr0 0.700, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.700, p_cap500_ge_E02 | 1.0 |  |
| 575 | 0.700 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.7 |  |
| 576 | 5,107 | Supplementary Table S4, A, hr0 0.725, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.725, cap_500 | 5107283.23574881 |  |
| 577 | 4,151 | Supplementary Table S4, A, hr0 0.725, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.725, cap500_lo | 4150600.95492105 |  |
| 578 | 5,707 | Supplementary Table S4, A, hr0 0.725, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.725, cap500_hi | 5707458.2216323 |  |
| 579 | 100.0 | Supplementary Table S4, A, hr0 0.725, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.725, p_cap500_ge_E02 | 1.0 |  |
| 580 | 5,041 | Supplementary Table S4, A, hr0 0.725, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.725, cap_500 | 5041197.61488921 |  |
| 581 | 4,101 | Supplementary Table S4, A, hr0 0.725, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.725, cap500_lo | 4100867.95777681 |  |
| 582 | 5,623 | Supplementary Table S4, A, hr0 0.725, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.725, cap500_hi | 5623095.08779944 |  |
| 583 | 100.0 | Supplementary Table S4, A, hr0 0.725, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.725, p_cap500_ge_E02 | 1.0 |  |
| 584 | 6,480 | Supplementary Table S4, A, hr0 0.725, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.725, cap_500 | 6480153.98928057 |  |
| 585 | 5,408 | Supplementary Table S4, A, hr0 0.725, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.725, cap500_lo | 5408061.93447256 |  |
| 586 | 7,167 | Supplementary Table S4, A, hr0 0.725, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.725, cap500_hi | 7167068.49615858 |  |
| 587 | 100.0 | Supplementary Table S4, A, hr0 0.725, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.725, p_cap500_ge_E02 | 1.0 |  |
| 588 | 0.725 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.725 |  |
| 589 | 4,623 | Supplementary Table S4, A, hr0 0.750, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.750, cap_500 | 4622953.57814769 |  |
| 590 | 3,758 | Supplementary Table S4, A, hr0 0.750, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.750, cap500_lo | 3758428.54595357 |  |
| 591 | 5,164 | Supplementary Table S4, A, hr0 0.750, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.750, cap500_hi | 5163753.85987483 |  |
| 592 | 100.0 | Supplementary Table S4, A, hr0 0.750, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.750, p_cap500_ge_E02 | 1.0 |  |
| 593 | 4,563 | Supplementary Table S4, A, hr0 0.750, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.750, cap_500 | 4562992.85676355 |  |
| 594 | 3,713 | Supplementary Table S4, A, hr0 0.750, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.750, cap500_lo | 3713344.8727981 |  |
| 595 | 5,087 | Supplementary Table S4, A, hr0 0.750, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.750, cap500_hi | 5086572.51890025 |  |
| 596 | 100.0 | Supplementary Table S4, A, hr0 0.750, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.750, p_cap500_ge_E02 | 1.0 |  |
| 597 | 5,860 | Supplementary Table S4, A, hr0 0.750, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.750, cap_500 | 5860005.5604669 |  |
| 598 | 4,895 | Supplementary Table S4, A, hr0 0.750, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.750, cap500_lo | 4894905.22185895 |  |
| 599 | 6,473 | Supplementary Table S4, A, hr0 0.750, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.750, cap500_hi | 6473355.81223986 |  |
| 600 | 100.0 | Supplementary Table S4, A, hr0 0.750, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.750, p_cap500_ge_E02 | 1.0 |  |
| 601 | 0.750 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.75 |  |
| 602 | 4,143 | Supplementary Table S4, A, hr0 0.775, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.775, cap_500 | 4142743.46879809 |  |
| 603 | 3,369 | Supplementary Table S4, A, hr0 0.775, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.775, cap500_lo | 3369293.00021999 |  |
| 604 | 4,625 | Supplementary Table S4, A, hr0 0.775, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.775, cap500_hi | 4625172.09768162 |  |
| 605 | 100.0 | Supplementary Table S4, A, hr0 0.775, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.775, p_cap500_ge_E02 | 1.0 |  |
| 606 | 4,089 | Supplementary Table S4, A, hr0 0.775, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.775, cap_500 | 4088883.90615239 |  |
| 607 | 3,330 | Supplementary Table S4, A, hr0 0.775, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.775, cap500_lo | 3329621.10301248 |  |
| 608 | 4,555 | Supplementary Table S4, A, hr0 0.775, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.775, cap500_hi | 4555068.98451339 |  |
| 609 | 100.0 | Supplementary Table S4, A, hr0 0.775, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.775, p_cap500_ge_E02 | 1.0 |  |
| 610 | 5,246 | Supplementary Table S4, A, hr0 0.775, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.775, cap_500 | 5246284.82823615 |  |
| 611 | 4,384 | Supplementary Table S4, A, hr0 0.775, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.775, cap500_lo | 4384182.69202997 |  |
| 612 | 5,788 | Supplementary Table S4, A, hr0 0.775, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.775, cap500_hi | 5788345.84065741 |  |
| 613 | 100.0 | Supplementary Table S4, A, hr0 0.775, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.775, p_cap500_ge_E02 | 1.0 |  |
| 614 | 0.775 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.775 |  |
| 615 | 3,667 | Supplementary Table S4, A, hr0 0.800, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.800, cap_500 | 3666609.71795855 |  |
| 616 | 2,983 | Supplementary Table S4, A, hr0 0.800, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.800, cap500_lo | 2983165.14833969 |  |
| 617 | 4,092 | Supplementary Table S4, A, hr0 0.800, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.800, cap500_hi | 4091635.99176277 |  |
| 618 | 100.0 | Supplementary Table S4, A, hr0 0.800, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.800, p_cap500_ge_E02 | 1.0 |  |
| 619 | 3,619 | Supplementary Table S4, A, hr0 0.800, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.800, cap_500 | 3618827.6801507 |  |
| 620 | 2,951 | Supplementary Table S4, A, hr0 0.800, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.800, cap500_lo | 2951485.62331637 |  |
| 621 | 4,029 | Supplementary Table S4, A, hr0 0.800, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.800, cap500_hi | 4029211.9262885 |  |
| 622 | 100.0 | Supplementary Table S4, A, hr0 0.800, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.800, p_cap500_ge_E02 | 1.0 |  |
| 623 | 4,639 | Supplementary Table S4, A, hr0 0.800, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.800, cap_500 | 4638912.2827981 |  |
| 624 | 3,879 | Supplementary Table S4, A, hr0 0.800, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.800, cap500_lo | 3879138.85297923 |  |
| 625 | 5,110 | Supplementary Table S4, A, hr0 0.800, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.800, cap500_hi | 5109701.34161143 |  |
| 626 | 100.0 | Supplementary Table S4, A, hr0 0.800, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.800, p_cap500_ge_E02 | 1.0 |  |
| 627 | 0.800 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.8 |  |
| 628 | 3,195 | Supplementary Table S4, A, hr0 0.825, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.825, cap_500 | 3194509.60776564 |  |
| 629 | 2,602 | Supplementary Table S4, A, hr0 0.825, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.825, cap500_lo | 2602495.20275702 |  |
| 630 | 3,564 | Supplementary Table S4, A, hr0 0.825, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.825, cap500_hi | 3563767.51486497 |  |
| 631 | 100.0 | Supplementary Table S4, A, hr0 0.825, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.825, p_cap500_ge_E02 | 1.0 |  |
| 632 | 3,153 | Supplementary Table S4, A, hr0 0.825, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.825, cap_500 | 3152781.56724109 |  |
| 633 | 2,575 | Supplementary Table S4, A, hr0 0.825, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.825, cap500_lo | 2575402.5726415 |  |
| 634 | 3,509 | Supplementary Table S4, A, hr0 0.825, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.825, cap500_hi | 3508600.84052541 |  |
| 635 | 100.0 | Supplementary Table S4, A, hr0 0.825, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.825, p_cap500_ge_E02 | 1.0 |  |
| 636 | 4,038 | Supplementary Table S4, A, hr0 0.825, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.825, cap_500 | 4037809.44429319 |  |
| 637 | 3,377 | Supplementary Table S4, A, hr0 0.825, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.825, cap500_lo | 3377485.64174696 |  |
| 638 | 4,444 | Supplementary Table S4, A, hr0 0.825, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.825, cap500_hi | 4443929.83975749 |  |
| 639 | 100.0 | Supplementary Table S4, A, hr0 0.825, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.825, p_cap500_ge_E02 | 1.0 |  |
| 640 | 0.825 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.825 |  |
| 641 | 2,726 | Supplementary Table S4, A, hr0 0.850, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.850, cap_500 | 2726400.8870362 |  |
| 642 | 2,223 | Supplementary Table S4, A, hr0 0.850, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.850, cap500_lo | 2222889.94969549 |  |
| 643 | 3,040 | Supplementary Table S4, A, hr0 0.850, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.850, cap500_hi | 3039571.6727006 |  |
| 644 | 100.0 | Supplementary Table S4, A, hr0 0.850, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.850, p_cap500_ge_E02 | 1.0 |  |
| 645 | 2,691 | Supplementary Table S4, A, hr0 0.850, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.850, cap_500 | 2690703.42209718 |  |
| 646 | 2,201 | Supplementary Table S4, A, hr0 0.850, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.850, cap500_lo | 2201372.06901273 |  |
| 647 | 2,994 | Supplementary Table S4, A, hr0 0.850, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.850, cap500_hi | 2994018.48115396 |  |
| 648 | 100.0 | Supplementary Table S4, A, hr0 0.850, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.850, p_cap500_ge_E02 | 1.0 |  |
| 649 | 3,443 | Supplementary Table S4, A, hr0 0.850, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.850, cap_500 | 3442898.84929941 |  |
| 650 | 2,881 | Supplementary Table S4, A, hr0 0.850, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.850, cap500_lo | 2880585.1480882 |  |
| 651 | 3,785 | Supplementary Table S4, A, hr0 0.850, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.850, cap500_hi | 3785042.45783867 |  |
| 652 | 100.0 | Supplementary Table S4, A, hr0 0.850, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.850, p_cap500_ge_E02 | 1.0 |  |
| 653 | 0.850 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.85 |  |
| 654 | 2,262 | Supplementary Table S4, A, hr0 0.875, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.875, cap_500 | 2262241.76612502 |  |
| 655 | 1,846 | Supplementary Table S4, A, hr0 0.875, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.875, cap500_lo | 1845581.02685846 |  |
| 656 | 2,521 | Supplementary Table S4, A, hr0 0.875, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.875, cap500_hi | 2520893.14326824 |  |
| 657 | 100.0 | Supplementary Table S4, A, hr0 0.875, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.875, p_cap500_ge_E02 | 1.0 |  |
| 658 | 2,233 | Supplementary Table S4, A, hr0 0.875, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.875, cap_500 | 2232551.56044558 |  |
| 659 | 1,829 | Supplementary Table S4, A, hr0 0.875, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.875, cap500_lo | 1828559.21924675 |  |
| 660 | 2,483 | Supplementary Table S4, A, hr0 0.875, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.875, cap500_hi | 2483290.45074591 |  |
| 661 | 100.0 | Supplementary Table S4, A, hr0 0.875, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.875, p_cap500_ge_E02 | 1.0 |  |
| 662 | 2,854 | Supplementary Table S4, A, hr0 0.875, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.875, cap_500 | 2854104.03751429 |  |
| 663 | 2,389 | Supplementary Table S4, A, hr0 0.875, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.875, cap500_lo | 2388622.74466122 |  |
| 664 | 3,134 | Supplementary Table S4, A, hr0 0.875, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.875, cap500_hi | 3134019.51999435 |  |
| 665 | 100.0 | Supplementary Table S4, A, hr0 0.875, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.875, p_cap500_ge_E02 | 1.0 |  |
| 666 | 0.875 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.875 |  |
| 667 | 1,802 | Supplementary Table S4, A, hr0 0.900, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.900, cap_500 | 1801990.91184234 |  |
| 668 | 1,471 | Supplementary Table S4, A, hr0 0.900, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.900, cap500_lo | 1471094.57758093 |  |
| 669 | 2,007 | Supplementary Table S4, A, hr0 0.900, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.900, cap500_hi | 2007047.17040087 |  |
| 670 | 100.0 | Supplementary Table S4, A, hr0 0.900, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.900, p_cap500_ge_E02 | 1.0 |  |
| 671 | 1,778 | Supplementary Table S4, A, hr0 0.900, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.900, cap_500 | 1778284.75398465 |  |
| 672 | 1,457 | Supplementary Table S4, A, hr0 0.900, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.900, cap500_lo | 1457057.87494703 |  |
| 673 | 1,977 | Supplementary Table S4, A, hr0 0.900, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.900, cap500_hi | 1976975.00951638 |  |
| 674 | 100.0 | Supplementary Table S4, A, hr0 0.900, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.900, p_cap500_ge_E02 | 1.0 |  |
| 675 | 2,271 | Supplementary Table S4, A, hr0 0.900, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.900, cap_500 | 2271349.53861421 |  |
| 676 | 1,902 | Supplementary Table S4, A, hr0 0.900, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.900, cap500_lo | 1902118.14956824 |  |
| 677 | 2,492 | Supplementary Table S4, A, hr0 0.900, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.900, cap500_hi | 2492170.50682024 |  |
| 678 | 100.0 | Supplementary Table S4, A, hr0 0.900, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.900, p_cap500_ge_E02 | 1.0 |  |
| 679 | 0.900 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.9 |  |
| 680 | 1,346 | Supplementary Table S4, A, hr0 0.925, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.925, cap_500 | 1345607.44242529 |  |
| 681 | 1,100 | Supplementary Table S4, A, hr0 0.925, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.925, cap500_lo | 1099526.52775372 |  |
| 682 | 1,498 | Supplementary Table S4, A, hr0 0.925, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.925, cap500_hi | 1497977.83910555 |  |
| 683 | 100.0 | Supplementary Table S4, A, hr0 0.925, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.925, p_cap500_ge_E02 | 1.0 |  |
| 684 | 1,328 | Supplementary Table S4, A, hr0 0.925, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.925, cap_500 | 1327862.22535721 |  |
| 685 | 1,088 | Supplementary Table S4, A, hr0 0.925, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.925, cap500_lo | 1088377.04538529 |  |
| 686 | 1,475 | Supplementary Table S4, A, hr0 0.925, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.925, cap500_hi | 1475479.1782126 |  |
| 687 | 100.0 | Supplementary Table S4, A, hr0 0.925, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.925, p_cap500_ge_E02 | 1.0 |  |
| 688 | 1,695 | Supplementary Table S4, A, hr0 0.925, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.925, cap_500 | 1694560.8592846 |  |
| 689 | 1,421 | Supplementary Table S4, A, hr0 0.925, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.925, cap500_lo | 1420591.73627263 |  |
| 690 | 1,859 | Supplementary Table S4, A, hr0 0.925, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.925, cap500_hi | 1858745.18751158 |  |
| 691 | 100.0 | Supplementary Table S4, A, hr0 0.925, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.925, p_cap500_ge_E02 | 1.0 |  |
| 692 | 0.925 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.925 |  |
| 693 | 893 | Supplementary Table S4, A, hr0 0.950, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.950, cap_500 | 893050.922566834 |  |
| 694 | 730 | Supplementary Table S4, A, hr0 0.950, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.950, cap500_lo | 730429.179444587 |  |
| 695 | 994 | Supplementary Table S4, A, hr0 0.950, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.950, cap500_hi | 993777.720192172 |  |
| 696 | 100.0 | Supplementary Table S4, A, hr0 0.950, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.950, p_cap500_ge_E02 | 1.0 |  |
| 697 | 881 | Supplementary Table S4, A, hr0 0.950, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.950, cap_500 | 881243.643184178 |  |
| 698 | 722 | Supplementary Table S4, A, hr0 0.950, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.950, cap500_lo | 722490.611563188 |  |
| 699 | 979 | Supplementary Table S4, A, hr0 0.950, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.950, cap500_hi | 978771.674750348 |  |
| 700 | 100.0 | Supplementary Table S4, A, hr0 0.950, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.950, p_cap500_ge_E02 | 1.0 |  |
| 701 | 1,124 | Supplementary Table S4, A, hr0 0.950, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.950, cap_500 | 1123664.47042199 |  |
| 702 | 943 | Supplementary Table S4, A, hr0 0.950, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.950, cap500_lo | 943241.898366675 |  |
| 703 | 1,232 | Supplementary Table S4, A, hr0 0.950, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.950, cap500_hi | 1232205.07904342 |  |
| 704 | 100.0 | Supplementary Table S4, A, hr0 0.950, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.950, p_cap500_ge_E02 | 1.0 |  |
| 705 | 0.950 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.95 |  |
| 706 | 444 | Supplementary Table S4, A, hr0 0.975, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.975, cap_500 | 444281.358496908 |  |
| 707 | 364 | Supplementary Table S4, A, hr0 0.975, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.975, cap500_lo | 363782.279594977 |  |
| 708 | 494 | Supplementary Table S4, A, hr0 0.975, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.975, cap500_hi | 494439.174366553 |  |
| 709 | 100.0 | Supplementary Table S4, A, hr0 0.975, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.975, p_cap500_ge_E02 | 1.0 |  |
| 710 | 438 | Supplementary Table S4, A, hr0 0.975, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.975, cap_500 | 438389.117145039 |  |
| 711 | 359 | Supplementary Table S4, A, hr0 0.975, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.975, cap500_lo | 359372.702504042 |  |
| 712 | 487 | Supplementary Table S4, A, hr0 0.975, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.975, cap500_hi | 486692.667585847 |  |
| 713 | 100.0 | Supplementary Table S4, A, hr0 0.975, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.975, p_cap500_ge_E02 | 1.0 |  |
| 714 | 559 | Supplementary Table S4, A, hr0 0.975, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.975, cap_500 | 558587.794503014 |  |
| 715 | 469 | Supplementary Table S4, A, hr0 0.975, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.975, cap500_lo | 469405.543001108 |  |
| 716 | 612 | Supplementary Table S4, A, hr0 0.975, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.975, cap500_hi | 612299.516134842 |  |
| 717 | 100.0 | Supplementary Table S4, A, hr0 0.975, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.975, p_cap500_ge_E02 | 1.0 |  |
| 718 | 0.975 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.975 |  |
| 719 | −1 | Supplementary Table S4, A, hr0 1.000, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 1.000, cap_500 | -740.806878935912 |  |
| 720 | −2 | Supplementary Table S4, A, hr0 1.000, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 1.000, cap500_lo | -1542.24790409717 |  |
| 721 | 0 | Supplementary Table S4, A, hr0 1.000, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 1.000, cap500_hi | -220.922133505826 |  |
| 722 | 0.0 | Supplementary Table S4, A, hr0 1.000, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 1.000, p_cap500_ge_E02 | 0.0 |  |
| 723 | −1 | Supplementary Table S4, A, hr0 1.000, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 1.000, cap_500 | -740.806878934049 |  |
| 724 | −2 | Supplementary Table S4, A, hr0 1.000, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 1.000, cap500_lo | -1542.24790409717 |  |
| 725 | 0 | Supplementary Table S4, A, hr0 1.000, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 1.000, cap500_hi | -220.922133505779 |  |
| 726 | 0.0 | Supplementary Table S4, A, hr0 1.000, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 1.000, p_cap500_ge_E02 | 0.0 |  |
| 727 | −1 | Supplementary Table S4, A, hr0 1.000, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 1.000, cap_500 | -740.806878934049 |  |
| 728 | −2 | Supplementary Table S4, A, hr0 1.000, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 1.000, cap500_lo | -1542.24790409722 |  |
| 729 | 0 | Supplementary Table S4, A, hr0 1.000, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 1.000, cap500_hi | -220.922133503963 |  |
| 730 | 0.0 | Supplementary Table S4, A, hr0 1.000, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 1.000, p_cap500_ge_E02 | 0.0 |  |
| 731 | 1.000 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 1.0 |  |
| 732 | 7,672 | Supplementary Table S4, B, hr0 0.700, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.700, cap_750 | 7672050.73102011 |  |
| 733 | 6,266 | Supplementary Table S4, B, hr0 0.700, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.700, cap750_lo | 6265759.42036875 |  |
| 734 | 8,533 | Supplementary Table S4, B, hr0 0.700, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.700, cap750_hi | 8533062.62462082 |  |
| 735 | 100.0 | Supplementary Table S4, B, hr0 0.700, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.700, p_cap750_ge_E02 | 1.0 |  |
| 736 | 7,610 | Supplementary Table S4, B, hr0 0.700, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.700, cap_750 | 7609779.87182034 |  |
| 737 | 6,215 | Supplementary Table S4, B, hr0 0.700, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.700, cap750_lo | 6214702.32447475 |  |
| 738 | 8,454 | Supplementary Table S4, B, hr0 0.700, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.700, cap750_hi | 8453606.13236826 |  |
| 739 | 100.0 | Supplementary Table S4, B, hr0 0.700, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.700, p_cap750_ge_E02 | 1.0 |  |
| 740 | 9,761 | Supplementary Table S4, B, hr0 0.700, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.700, cap_750 | 9760622.34224905 |  |
| 741 | 8,173 | Supplementary Table S4, B, hr0 0.700, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.700, cap750_lo | 8172731.79469586 |  |
| 742 | 10,782 | Supplementary Table S4, B, hr0 0.700, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.700, cap750_hi | 10781892.1215201 |  |
| 743 | 100.0 | Supplementary Table S4, B, hr0 0.700, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.700, p_cap750_ge_E02 | 1.0 |  |
| 744 | 0.700 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.7 |  |
| 745 | 7,003 | Supplementary Table S4, B, hr0 0.725, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.725, cap_750 | 7002546.08671047 |  |
| 746 | 5,722 | Supplementary Table S4, B, hr0 0.725, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.725, cap750_lo | 5721513.01509258 |  |
| 747 | 7,783 | Supplementary Table S4, B, hr0 0.725, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.725, cap750_hi | 7783435.49061369 |  |
| 748 | 100.0 | Supplementary Table S4, B, hr0 0.725, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.725, p_cap750_ge_E02 | 1.0 |  |
| 749 | 6,946 | Supplementary Table S4, B, hr0 0.725, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.725, cap_750 | 6945575.85936095 |  |
| 750 | 5,672 | Supplementary Table S4, B, hr0 0.725, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.725, cap750_lo | 5672237.75623071 |  |
| 751 | 7,711 | Supplementary Table S4, B, hr0 0.725, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.725, cap750_hi | 7711472.63652642 |  |
| 752 | 100.0 | Supplementary Table S4, B, hr0 0.725, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.725, p_cap750_ge_E02 | 1.0 |  |
| 753 | 8,900 | Supplementary Table S4, B, hr0 0.725, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.725, cap_750 | 8900297.42976925 |  |
| 754 | 7,455 | Supplementary Table S4, B, hr0 0.725, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.725, cap750_lo | 7455499.80535562 |  |
| 755 | 9,822 | Supplementary Table S4, B, hr0 0.725, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.725, cap750_hi | 9822304.35310831 |  |
| 756 | 100.0 | Supplementary Table S4, B, hr0 0.725, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.725, p_cap750_ge_E02 | 1.0 |  |
| 757 | 0.725 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.725 |  |
| 758 | 6,339 | Supplementary Table S4, B, hr0 0.750, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.750, cap_750 | 6338706.82569226 |  |
| 759 | 5,181 | Supplementary Table S4, B, hr0 0.750, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.750, cap750_lo | 5181407.74518489 |  |
| 760 | 7,042 | Supplementary Table S4, B, hr0 0.750, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.750, cap750_hi | 7041691.14247097 |  |
| 761 | 100.0 | Supplementary Table S4, B, hr0 0.750, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.750, p_cap750_ge_E02 | 1.0 |  |
| 762 | 6,287 | Supplementary Table S4, B, hr0 0.750, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.750, cap_750 | 6287016.67156104 |  |
| 763 | 5,137 | Supplementary Table S4, B, hr0 0.750, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.750, cap750_lo | 5136719.52392232 |  |
| 764 | 6,976 | Supplementary Table S4, B, hr0 0.750, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.750, cap750_hi | 6976406.34649201 |  |
| 765 | 100.0 | Supplementary Table S4, B, hr0 0.750, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.750, p_cap750_ge_E02 | 1.0 |  |
| 766 | 8,049 | Supplementary Table S4, B, hr0 0.750, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.750, cap_750 | 8048849.76241996 |  |
| 767 | 6,744 | Supplementary Table S4, B, hr0 0.750, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.750, cap750_lo | 6743854.67241189 |  |
| 768 | 8,868 | Supplementary Table S4, B, hr0 0.750, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.750, cap750_hi | 8868222.12183894 |  |
| 769 | 100.0 | Supplementary Table S4, B, hr0 0.750, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.750, p_cap750_ge_E02 | 1.0 |  |
| 770 | 0.750 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.75 |  |
| 771 | 5,680 | Supplementary Table S4, B, hr0 0.775, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.775, cap_750 | 5680473.72472728 |  |
| 772 | 4,645 | Supplementary Table S4, B, hr0 0.775, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.775, cap750_lo | 4645433.94142924 |  |
| 773 | 6,307 | Supplementary Table S4, B, hr0 0.775, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.775, cap750_hi | 6307011.09233036 |  |
| 774 | 100.0 | Supplementary Table S4, B, hr0 0.775, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.775, p_cap750_ge_E02 | 1.0 |  |
| 775 | 5,634 | Supplementary Table S4, B, hr0 0.775, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.775, cap_750 | 5634043.1777065 |  |
| 776 | 4,605 | Supplementary Table S4, B, hr0 0.775, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.775, cap750_lo | 4605281.08441232 |  |
| 777 | 6,246 | Supplementary Table S4, B, hr0 0.775, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.775, cap750_hi | 6246488.0752917 |  |
| 778 | 100.0 | Supplementary Table S4, B, hr0 0.775, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.775, p_cap750_ge_E02 | 1.0 |  |
| 779 | 7,206 | Supplementary Table S4, B, hr0 0.775, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.775, cap_750 | 7206169.73162784 |  |
| 780 | 6,042 | Supplementary Table S4, B, hr0 0.775, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.775, cap750_lo | 6042158.43572615 |  |
| 781 | 7,930 | Supplementary Table S4, B, hr0 0.775, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.775, cap750_hi | 7930222.36583811 |  |
| 782 | 100.0 | Supplementary Table S4, B, hr0 0.775, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.775, p_cap750_ge_E02 | 1.0 |  |
| 783 | 0.775 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.775 |  |
| 784 | 5,028 | Supplementary Table S4, B, hr0 0.800, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.800, cap_750 | 5027788.20663172 |  |
| 785 | 4,114 | Supplementary Table S4, B, hr0 0.800, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.800, cap750_lo | 4113552.74195334 |  |
| 786 | 5,579 | Supplementary Table S4, B, hr0 0.800, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.800, cap750_hi | 5579312.70332724 |  |
| 787 | 100.0 | Supplementary Table S4, B, hr0 0.800, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.800, p_cap750_ge_E02 | 1.0 |  |
| 788 | 4,987 | Supplementary Table S4, B, hr0 0.800, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.800, cap_750 | 4986596.8927139 |  |
| 789 | 4,078 | Supplementary Table S4, B, hr0 0.800, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.800, cap750_lo | 4077883.45642681 |  |
| 790 | 5,524 | Supplementary Table S4, B, hr0 0.800, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.800, cap750_hi | 5523904.45350043 |  |
| 791 | 100.0 | Supplementary Table S4, B, hr0 0.800, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.800, p_cap750_ge_E02 | 1.0 |  |
| 792 | 6,372 | Supplementary Table S4, B, hr0 0.800, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.800, cap_750 | 6372149.14746403 |  |
| 793 | 5,349 | Supplementary Table S4, B, hr0 0.800, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.800, cap750_lo | 5348952.34933021 |  |
| 794 | 7,004 | Supplementary Table S4, B, hr0 0.800, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.800, cap750_hi | 7004033.47580122 |  |
| 795 | 100.0 | Supplementary Table S4, B, hr0 0.800, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.800, p_cap750_ge_E02 | 1.0 |  |
| 796 | 0.800 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.8 |  |
| 797 | 4,381 | Supplementary Table S4, B, hr0 0.825, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.825, cap_750 | 4380592.33316748 |  |
| 798 | 3,586 | Supplementary Table S4, B, hr0 0.825, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.825, cap750_lo | 3585678.82598587 |  |
| 799 | 4,859 | Supplementary Table S4, B, hr0 0.825, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.825, cap750_hi | 4858514.34389412 |  |
| 800 | 100.0 | Supplementary Table S4, B, hr0 0.825, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.825, p_cap750_ge_E02 | 1.0 |  |
| 801 | 4,345 | Supplementary Table S4, B, hr0 0.825, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.825, cap_750 | 4344619.97002284 |  |
| 802 | 3,554 | Supplementary Table S4, B, hr0 0.825, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.825, cap750_lo | 3554488.04588831 |  |
| 803 | 4,810 | Supplementary Table S4, B, hr0 0.825, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.825, cap750_hi | 4809814.21403544 |  |
| 804 | 100.0 | Supplementary Table S4, B, hr0 0.825, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.825, p_cap750_ge_E02 | 1.0 |  |
| 805 | 5,547 | Supplementary Table S4, B, hr0 0.825, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.825, cap_750 | 5546681.2200635 |  |
| 806 | 4,659 | Supplementary Table S4, B, hr0 0.825, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.825, cap750_lo | 4659247.2752232 |  |
| 807 | 6,090 | Supplementary Table S4, B, hr0 0.825, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.825, cap750_hi | 6089614.20402583 |  |
| 808 | 100.0 | Supplementary Table S4, B, hr0 0.825, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.825, p_cap750_ge_E02 | 1.0 |  |
| 809 | 0.825 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.825 |  |
| 810 | 3,739 | Supplementary Table S4, B, hr0 0.850, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.850, cap_750 | 3738828.79801032 |  |
| 811 | 3,062 | Supplementary Table S4, B, hr0 0.850, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.850, cap750_lo | 3061807.46077957 |  |
| 812 | 4,144 | Supplementary Table S4, B, hr0 0.850, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.850, cap750_hi | 4144141.05531306 |  |
| 813 | 100.0 | Supplementary Table S4, B, hr0 0.850, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.850, p_cap750_ge_E02 | 1.0 |  |
| 814 | 3,708 | Supplementary Table S4, B, hr0 0.850, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.850, cap_750 | 3708055.19456433 |  |
| 815 | 3,035 | Supplementary Table S4, B, hr0 0.850, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.850, cap750_lo | 3035145.3733384 |  |
| 816 | 4,103 | Supplementary Table S4, B, hr0 0.850, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.850, cap750_hi | 4103133.56657498 |  |
| 817 | 100.0 | Supplementary Table S4, B, hr0 0.850, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.850, p_cap750_ge_E02 | 1.0 |  |
| 818 | 4,730 | Supplementary Table S4, B, hr0 0.850, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.850, cap_750 | 4729660.54129083 |  |
| 819 | 3,976 | Supplementary Table S4, B, hr0 0.850, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.850, cap750_lo | 3975879.01843642 |  |
| 820 | 5,188 | Supplementary Table S4, B, hr0 0.850, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.850, cap750_hi | 5188138.12064227 |  |
| 821 | 100.0 | Supplementary Table S4, B, hr0 0.850, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.850, p_cap750_ge_E02 | 1.0 |  |
| 822 | 0.850 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.85 |  |
| 823 | 3,102 | Supplementary Table S4, B, hr0 0.875, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.875, cap_750 | 3102440.9197926 |  |
| 824 | 2,542 | Supplementary Table S4, B, hr0 0.875, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.875, cap750_lo | 2541870.0489242 |  |
| 825 | 3,436 | Supplementary Table S4, B, hr0 0.875, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.875, cap750_hi | 3436473.66088406 |  |
| 826 | 100.0 | Supplementary Table S4, B, hr0 0.875, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.875, p_cap750_ge_E02 | 1.0 |  |
| 827 | 3,077 | Supplementary Table S4, B, hr0 0.875, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.875, cap_750 | 3076845.97580843 |  |
| 828 | 2,520 | Supplementary Table S4, B, hr0 0.875, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.875, cap750_lo | 2519745.1560473 |  |
| 829 | 3,403 | Supplementary Table S4, B, hr0 0.875, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.875, cap750_hi | 3403037.13469593 |  |
| 830 | 100.0 | Supplementary Table S4, B, hr0 0.875, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.875, p_cap750_ge_E02 | 1.0 |  |
| 831 | 3,921 | Supplementary Table S4, B, hr0 0.875, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.875, cap_750 | 3920983.06664373 |  |
| 832 | 3,298 | Supplementary Table S4, B, hr0 0.875, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.875, cap750_lo | 3298302.89809054 |  |
| 833 | 4,297 | Supplementary Table S4, B, hr0 0.875, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.875, cap750_hi | 4297177.98832863 |  |
| 834 | 100.0 | Supplementary Table S4, B, hr0 0.875, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.875, p_cap750_ge_E02 | 1.0 |  |
| 835 | 0.875 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.875 |  |
| 836 | 2,471 | Supplementary Table S4, B, hr0 0.900, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.900, cap_750 | 2471372.63522738 |  |
| 837 | 2,026 | Supplementary Table S4, B, hr0 0.900, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.900, cap750_lo | 2025836.62597371 |  |
| 838 | 2,736 | Supplementary Table S4, B, hr0 0.900, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.900, cap750_hi | 2736146.67665548 |  |
| 839 | 100.0 | Supplementary Table S4, B, hr0 0.900, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.900, p_cap750_ge_E02 | 1.0 |  |
| 840 | 2,451 | Supplementary Table S4, B, hr0 0.900, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.900, cap_750 | 2450936.34088904 |  |
| 841 | 2,008 | Supplementary Table S4, B, hr0 0.900, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.900, cap750_lo | 2008184.35364733 |  |
| 842 | 2,709 | Supplementary Table S4, B, hr0 0.900, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.900, cap750_hi | 2709448.7846217 |  |
| 843 | 100.0 | Supplementary Table S4, B, hr0 0.900, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.900, p_cap750_ge_E02 | 1.0 |  |
| 844 | 3,121 | Supplementary Table S4, B, hr0 0.900, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.900, cap_750 | 3120546.09739762 |  |
| 845 | 2,628 | Supplementary Table S4, B, hr0 0.900, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.900, cap750_lo | 2628499.33606298 |  |
| 846 | 3,416 | Supplementary Table S4, B, hr0 0.900, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.900, cap750_hi | 3415714.2910078 |  |
| 847 | 100.0 | Supplementary Table S4, B, hr0 0.900, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.900, p_cap750_ge_E02 | 1.0 |  |
| 848 | 0.900 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.9 |  |
| 849 | 1,846 | Supplementary Table S4, B, hr0 0.925, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.925, cap_750 | 1845568.49230514 |  |
| 850 | 1,514 | Supplementary Table S4, B, hr0 0.925, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.925, cap750_lo | 1513634.77130526 |  |
| 851 | 2,042 | Supplementary Table S4, B, hr0 0.925, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.925, cap750_hi | 2042278.34389702 |  |
| 852 | 100.0 | Supplementary Table S4, B, hr0 0.925, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.925, p_cap750_ge_E02 | 1.0 |  |
| 853 | 1,830 | Supplementary Table S4, B, hr0 0.925, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.925, cap_750 | 1830270.92780084 |  |
| 854 | 1,500 | Supplementary Table S4, B, hr0 0.925, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.925, cap750_lo | 1500426.89691706 |  |
| 855 | 2,022 | Supplementary Table S4, B, hr0 0.925, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.925, cap750_hi | 2022293.30502221 |  |
| 856 | 100.0 | Supplementary Table S4, B, hr0 0.925, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.925, p_cap750_ge_E02 | 1.0 |  |
| 857 | 2,328 | Supplementary Table S4, B, hr0 0.925, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.925, cap_750 | 2328248.26298218 |  |
| 858 | 1,962 | Supplementary Table S4, B, hr0 0.925, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.925, cap750_lo | 1962336.49803798 |  |
| 859 | 2,546 | Supplementary Table S4, B, hr0 0.925, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.925, cap750_hi | 2545904.90740806 |  |
| 860 | 100.0 | Supplementary Table S4, B, hr0 0.925, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.925, p_cap750_ge_E02 | 1.0 |  |
| 861 | 0.925 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.925 |  |
| 862 | 1,225 | Supplementary Table S4, B, hr0 0.950, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.950, cap_750 | 1224973.64356851 |  |
| 863 | 1,005 | Supplementary Table S4, B, hr0 0.950, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.950, cap750_lo | 1005221.50769014 |  |
| 864 | 1,355 | Supplementary Table S4, B, hr0 0.950, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.950, cap750_hi | 1354794.24562511 |  |
| 865 | 100.0 | Supplementary Table S4, B, hr0 0.950, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.950, p_cap750_ge_E02 | 1.0 |  |
| 866 | 1,215 | Supplementary Table S4, B, hr0 0.950, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.950, cap_750 | 1214794.97867989 |  |
| 867 | 997 | Supplementary Table S4, B, hr0 0.950, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.950, cap750_lo | 997092.96526682 |  |
| 868 | 1,342 | Supplementary Table S4, B, hr0 0.950, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.950, cap750_hi | 1342488.01603026 |  |
| 869 | 100.0 | Supplementary Table S4, B, hr0 0.950, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.950, p_cap750_ge_E02 | 1.0 |  |
| 870 | 1,544 | Supplementary Table S4, B, hr0 0.950, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.950, cap_750 | 1543989.50359149 |  |
| 871 | 1,302 | Supplementary Table S4, B, hr0 0.950, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.950, cap750_lo | 1301820.56740515 |  |
| 872 | 1,686 | Supplementary Table S4, B, hr0 0.950, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.950, cap750_hi | 1686317.18391732 |  |
| 873 | 100.0 | Supplementary Table S4, B, hr0 0.950, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.950, p_cap750_ge_E02 | 1.0 |  |
| 874 | 0.950 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.95 |  |
| 875 | 610 | Supplementary Table S4, B, hr0 0.975, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.975, cap_750 | 609533.839457311 |  |
| 876 | 501 | Supplementary Table S4, B, hr0 0.975, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.975, cap750_lo | 500561.350682947 |  |
| 877 | 674 | Supplementary Table S4, B, hr0 0.975, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.975, cap750_hi | 673960.156126594 |  |
| 878 | 100.0 | Supplementary Table S4, B, hr0 0.975, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.975, p_cap750_ge_E02 | 1.0 |  |
| 879 | 604 | Supplementary Table S4, B, hr0 0.975, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 0.975, cap_750 | 604454.333146033 |  |
| 880 | 497 | Supplementary Table S4, B, hr0 0.975, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.975, cap750_lo | 496769.301353055 |  |
| 881 | 668 | Supplementary Table S4, B, hr0 0.975, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.975, cap750_hi | 667838.294418456 |  |
| 882 | 100.0 | Supplementary Table S4, B, hr0 0.975, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 0.975, p_cap750_ge_E02 | 1.0 |  |
| 883 | 768 | Supplementary Table S4, B, hr0 0.975, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.975, cap_750 | 767671.053020855 |  |
| 884 | 648 | Supplementary Table S4, B, hr0 0.975, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.975, cap750_lo | 647619.538631383 |  |
| 885 | 838 | Supplementary Table S4, B, hr0 0.975, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.975, cap750_hi | 837549.420592121 |  |
| 886 | 100.0 | Supplementary Table S4, B, hr0 0.975, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.975, p_cap750_ge_E02 | 1.0 |  |
| 887 | 0.975 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 0.975 |  |
| 888 | −1 | Supplementary Table S4, B, hr0 1.000, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 1.000, cap_750 | -804.578268402805 |  |
| 889 | −2 | Supplementary Table S4, B, hr0 1.000, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 1.000, cap750_lo | -1808.47512853255 |  |
| 890 | 0 | Supplementary Table S4, B, hr0 1.000, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 1.000, cap750_hi | -160.242131257079 |  |
| 891 | 0.0 | Supplementary Table S4, B, hr0 1.000, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 1.000, p_cap750_ge_E02 | 0.0 |  |
| 892 | −1 | Supplementary Table S4, B, hr0 1.000, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = hr0, x = 1.000, cap_750 | -804.578268400943 |  |
| 893 | −2 | Supplementary Table S4, B, hr0 1.000, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 1.000, cap750_lo | -1808.47512853255 |  |
| 894 | 0 | Supplementary Table S4, B, hr0 1.000, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 1.000, cap750_hi | -160.242131257079 |  |
| 895 | 0.0 | Supplementary Table S4, B, hr0 1.000, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = hr0, x = 1.000, p_cap750_ge_E02 | 0.0 |  |
| 896 | −1 | Supplementary Table S4, B, hr0 1.000, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 1.000, cap_750 | -804.578268400943 |  |
| 897 | −2 | Supplementary Table S4, B, hr0 1.000, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 1.000, cap750_lo | -1808.47512853503 |  |
| 898 | 0 | Supplementary Table S4, B, hr0 1.000, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 1.000, cap750_hi | -160.242131256986 |  |
| 899 | 0.0 | Supplementary Table S4, B, hr0 1.000, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 1.000, p_cap750_ge_E02 | 0.0 |  |
| 900 | 1.000 | Supplementary Table S4, row label | `output/phase2/main/det_caps.csv` | x (hr0 grid) | 1.0 |  |
| 901 | 192 | Supplementary Table S5, exercise_programme, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = exercise_programme, d_base | 192400.0 |  |
| 902 | 192 | Supplementary Table S5, exercise_programme, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = exercise_programme, d_kext | 192400.0 |  |
| 903 | 1 | Supplementary Table S5, exercise_ae, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = exercise_ae, d_base | 613.2641 |  |
| 904 | 1 | Supplementary Table S5, exercise_ae, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = exercise_ae, d_kext | 613.2641 |  |
| 905 | 12 | Supplementary Table S5, pembrolizumab_drug, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = pembrolizumab_drug, d_base | 11961.8146891827 |  |
| 906 | 12 | Supplementary Table S5, pembrolizumab_drug, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = pembrolizumab_drug, d_kext | 11961.8146891827 |  |
| 907 | 0 | Supplementary Table S5, administration, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = administration, d_base | 466.719589789398 |  |
| 908 | 0 | Supplementary Table S5, administration, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = administration, d_kext | 466.719589789398 |  |
| 909 | 0 | Supplementary Table S5, immune_ae, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = immune_ae, d_base | 0.0 |  |
| 910 | 0 | Supplementary Table S5, immune_ae, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = immune_ae, d_kext | 0.0 |  |
| 911 | 0 | Supplementary Table S5, chemo_ae, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = chemo_ae, d_base | 0.0 |  |
| 912 | 0 | Supplementary Table S5, chemo_ae, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = chemo_ae, d_kext | 0.0 |  |
| 913 | 8 | Supplementary Table S5, follow_up, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = follow_up, d_base | 8225.89015031757 |  |
| 914 | 8 | Supplementary Table S5, follow_up, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = follow_up, d_kext | 8225.89015031757 |  |
| 915 | −10 | Supplementary Table S5, lrr, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = lrr, d_base | -10249.1546983995 |  |
| 916 | −10 | Supplementary Table S5, lrr, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = lrr, d_kext | -10249.1546983995 |  |
| 917 | −254 | Supplementary Table S5, dr_first_line, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = dr_first_line, d_base | -254470.37988126 |  |
| 918 | −249 | Supplementary Table S5, dr_first_line, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = dr_first_line, d_kext | -249002.126174163 |  |
| 919 | −437 | Supplementary Table S5, dr_later_lines, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = dr_later_lines, d_base | -437189.240745146 |  |
| 920 | −397 | Supplementary Table S5, dr_later_lines, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = dr_later_lines, d_kext | -397052.703994157 |  |
| 921 | −21 | Supplementary Table S5, terminal_care, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = terminal_care, d_base | -20903.9782924511 |  |
| 922 | −21 | Supplementary Table S5, terminal_care, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = terminal_care, d_kext | -20963.5808254562 |  |
| 923 | 0 | Supplementary Table S5, other, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = other, d_base | 0.0 |  |
| 924 | 0 | Supplementary Table S5, other, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = other, d_kext | 0.0 |  |
| 925 | −509 | Supplementary Table S5, total, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = total, d_base | -509145.065087968 |  |
| 926 | −464 | Supplementary Table S5, total, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = total, d_kext | -463599.877162886 |  |
| 927 | −702 | Supplementary Table S5, total_without_programme, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = total_without_programme, d_base | -701545.065087968 |  |
| 928 | −656 | Supplementary Table S5, total_without_programme, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = total_without_programme, d_kext | -655999.877162886 |  |
| 929 | −462 | Supplementary Table S5, total_with_E01, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = total_with_E01, d_base | -462036.929122903 |  |
| 930 | −416 | Supplementary Table S5, total_with_E01, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = total_with_E01, d_kext | -416491.741197821 |  |
| 931 | −690 | Supplementary Table S5, total_with_E03, d_base | `output/phase2/main/decomp_main_hr085.csv` | category = total_with_E03, d_base | -690285.065087968 | 【要確認】E03 |
| 932 | −645 | Supplementary Table S5, total_with_E03, d_kext | `output/phase2/main/decomp_main_hr085.csv` | category = total_with_E03, d_kext | -644739.877162886 | 【要確認】E03 |
| 933 | 3,613 | Supplementary Table S6, A, path_a_s1, main, 0.700 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.700, cap_500 | 3613437.80080788 |  |
| 934 | 4,669 | Supplementary Table S6, A, path_a_s1, secondary, 0.700 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.700, cap_500 | 4669040.99908229 |  |
| 935 | 6,989 | Supplementary Table S6, A, path_a_s2, main, 0.700 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.700, cap_500 | 6988806.55122441 |  |
| 936 | 9,120 | Supplementary Table S6, A, path_a_s2, secondary, 0.700 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.700, cap_500 | 9119936.80294006 |  |
| 937 | 4,685 | Supplementary Table S6, A, continue_s1, main, 0.700 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.700, cap_500 | 4684842.53070858 |  |
| 938 | 6,187 | Supplementary Table S6, A, continue_s1, secondary, 0.700 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.700, cap_500 | 6186898.54452575 |  |
| 939 | 3,302 | Supplementary Table S6, A, path_a_s1, main, 0.725 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.725, cap_500 | 3301739.9842515 |  |
| 940 | 4,263 | Supplementary Table S6, A, path_a_s1, secondary, 0.725 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.725, cap_500 | 4262914.53757279 |  |
| 941 | 6,378 | Supplementary Table S6, A, path_a_s2, main, 0.725 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.725, cap_500 | 6378315.71358554 |  |
| 942 | 8,316 | Supplementary Table S6, A, path_a_s2, secondary, 0.725 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.725, cap_500 | 8316288.28421822 |  |
| 943 | 4,269 | Supplementary Table S6, A, continue_s1, main, 0.725 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.725, cap_500 | 4269177.76288847 |  |
| 944 | 5,635 | Supplementary Table S6, A, continue_s1, secondary, 0.725 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.725, cap_500 | 5634557.16694944 |  |
| 945 | 2,992 | Supplementary Table S6, A, path_a_s1, main, 0.750 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.750, cap_500 | 2992002.74210093 |  |
| 946 | 3,860 | Supplementary Table S6, A, path_a_s1, secondary, 0.750 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.750, cap_500 | 3859970.5924779 |  |
| 947 | 5,773 | Supplementary Table S6, A, path_a_s2, main, 0.750 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.750, cap_500 | 5773104.84853378 |  |
| 948 | 7,521 | Supplementary Table S6, A, path_a_s2, secondary, 0.750 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.750, cap_500 | 7520873.78688036 |  |
| 949 | 3,857 | Supplementary Table S6, A, continue_s1, main, 0.750 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.750, cap_500 | 3856754.60667177 |  |
| 950 | 5,088 | Supplementary Table S6, A, continue_s1, secondary, 0.750 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.750, cap_500 | 5087734.20475724 |  |
| 951 | 2,684 | Supplementary Table S6, A, path_a_s1, main, 0.775 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.775, cap_500 | 2684211.26191368 |  |
| 952 | 3,460 | Supplementary Table S6, A, path_a_s1, secondary, 0.775 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.775, cap_500 | 3460179.86634374 |  |
| 953 | 5,173 | Supplementary Table S6, A, path_a_s2, main, 0.775 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.775, cap_500 | 5173117.35101693 |  |
| 954 | 6,734 | Supplementary Table S6, A, path_a_s2, secondary, 0.775 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.775, cap_500 | 6733598.27100795 |  |
| 955 | 3,448 | Supplementary Table S6, A, continue_s1, main, 0.775 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.775, cap_500 | 3447542.35385429 |  |
| 956 | 4,546 | Supplementary Table S6, A, continue_s1, secondary, 0.775 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.775, cap_500 | 4546364.58055247 |  |
| 957 | 2,378 | Supplementary Table S6, A, path_a_s1, main, 0.800 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.800, cap_500 | 2378350.84582233 |  |
| 958 | 3,064 | Supplementary Table S6, A, path_a_s1, secondary, 0.800 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.800, cap_500 | 3063513.33878606 |  |
| 959 | 4,578 | Supplementary Table S6, A, path_a_s2, main, 0.800 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.800, cap_500 | 4578297.26983252 |  |
| 960 | 5,954 | Supplementary Table S6, A, path_a_s2, secondary, 0.800 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.800, cap_500 | 5954367.86768845 |  |
| 961 | 3,042 | Supplementary Table S6, A, continue_s1, main, 0.800 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.800, cap_500 | 3041510.59625585 |  |
| 962 | 4,010 | Supplementary Table S6, A, continue_s1, secondary, 0.800 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.800, cap_500 | 4010384.01024641 |  |
| 963 | 2,074 | Supplementary Table S6, A, path_a_s1, main, 0.825 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.825, cap_500 | 2074406.90964656 |  |
| 964 | 2,670 | Supplementary Table S6, A, path_a_s1, secondary, 0.825 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.825, cap_500 | 2669942.26385834 |  |
| 965 | 3,989 | Supplementary Table S6, A, path_a_s2, main, 0.825 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.825, cap_500 | 3988589.29989299 |  |
| 966 | 5,183 | Supplementary Table S6, A, path_a_s2, secondary, 0.825 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.825, cap_500 | 5183089.86406821 |  |
| 967 | 2,639 | Supplementary Table S6, A, continue_s1, main, 0.825 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.825, cap_500 | 2638629.2227741 |  |
| 968 | 3,480 | Supplementary Table S6, A, continue_s1, secondary, 0.825 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.825, cap_500 | 3479728.99332491 |  |
| 969 | 1,772 | Supplementary Table S6, A, path_a_s1, main, 0.850 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.850, cap_500 | 1772364.98201127 |  |
| 970 | 2,279 | Supplementary Table S6, A, path_a_s1, secondary, 0.850 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.850, cap_500 | 2279438.16744623 |  |
| 971 | 3,404 | Supplementary Table S6, A, path_a_s2, main, 0.850 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.850, cap_500 | 3403938.77458484 |  |
| 972 | 4,420 | Supplementary Table S6, A, path_a_s2, secondary, 0.850 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.850, cap_500 | 4419672.68859316 |  |
| 973 | 2,239 | Supplementary Table S6, A, continue_s1, main, 0.850 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.850, cap_500 | 2238868.41647028 |  |
| 974 | 2,954 | Supplementary Table S6, A, continue_s1, secondary, 0.850 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.850, cap_500 | 2954336.80323356 |  |
| 975 | 1,472 | Supplementary Table S6, A, path_a_s1, main, 0.875 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.875, cap_500 | 1472210.70347324 |  |
| 976 | 1,892 | Supplementary Table S6, A, path_a_s1, secondary, 0.875 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.875, cap_500 | 1891972.84468846 |  |
| 977 | 2,824 | Supplementary Table S6, A, path_a_s2, main, 0.875 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.875, cap_500 | 2824291.65821594 |  |
| 978 | 3,664 | Supplementary Table S6, A, path_a_s2, secondary, 0.875 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.875, cap_500 | 3664025.89644674 |  |
| 979 | 1,842 | Supplementary Table S6, A, continue_s1, main, 0.875 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.875, cap_500 | 1842198.65167888 |  |
| 980 | 2,434 | Supplementary Table S6, A, continue_s1, secondary, 0.875 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.875, cap_500 | 2434145.47788207 |  |
| 981 | 1,174 | Supplementary Table S6, A, path_a_s1, main, 0.900 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.900, cap_500 | 1173929.82565212 |  |
| 982 | 1,508 | Supplementary Table S6, A, path_a_s1, secondary, 0.900 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.900, cap_500 | 1507518.35741812 |  |
| 983 | 2,250 | Supplementary Table S6, A, path_a_s2, main, 0.900 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.900, cap_500 | 2249594.53855456 |  |
| 984 | 2,916 | Supplementary Table S6, A, path_a_s2, secondary, 0.900 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.900, cap_500 | 2916060.15517547 |  |
| 985 | 1,449 | Supplementary Table S6, A, continue_s1, main, 0.900 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.900, cap_500 | 1448590.69115077 |  |
| 986 | 1,919 | Supplementary Table S6, A, continue_s1, secondary, 0.900 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.900, cap_500 | 1919093.81026521 |  |
| 987 | 878 | Supplementary Table S6, A, path_a_s1, main, 0.925 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.925, cap_500 | 877508.210369908 |  |
| 988 | 1,126 | Supplementary Table S6, A, path_a_s1, secondary, 0.925 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.925, cap_500 | 1126047.03163298 |  |
| 989 | 1,680 | Supplementary Table S6, A, path_a_s2, main, 0.925 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.925, cap_500 | 1679794.61945915 |  |
| 990 | 2,176 | Supplementary Table S6, A, path_a_s2, secondary, 0.925 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.925, cap_500 | 2175687.23050115 |  |
| 991 | 1,058 | Supplementary Table S6, A, continue_s1, main, 0.925 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.925, cap_500 | 1058015.58322092 |  |
| 992 | 1,409 | Supplementary Table S6, A, continue_s1, secondary, 0.925 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.925, cap_500 | 1409121.3391993 |  |
| 993 | 583 | Supplementary Table S6, A, path_a_s1, main, 0.950 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.950, cap_500 | 582931.828797003 |  |
| 994 | 748 | Supplementary Table S6, A, path_a_s1, secondary, 0.950 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.950, cap_500 | 747531.454986247 |  |
| 995 | 1,115 | Supplementary Table S6, A, path_a_s2, main, 0.950 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.950, cap_500 | 1114839.71359233 |  |
| 996 | 1,443 | Supplementary Table S6, A, path_a_s2, secondary, 0.950 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.950, cap_500 | 1442819.97231815 |  |
| 997 | 670 | Supplementary Table S6, A, continue_s1, main, 0.950 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.950, cap_500 | 670444.659004776 |  |
| 998 | 904 | Supplementary Table S6, A, continue_s1, secondary, 0.950 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.950, cap_500 | 904168.340171162 |  |
| 999 | 290 | Supplementary Table S6, A, path_a_s1, main, 0.975 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.975, cap_500 | 290186.760604207 |  |
| 1000 | 372 | Supplementary Table S6, A, path_a_s1, secondary, 0.975 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.975, cap_500 | 371944.47430346 |  |
| 1001 | 555 | Supplementary Table S6, A, path_a_s2, main, 0.975 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.975, cap_500 | 554678.235224205 |  |
| 1002 | 717 | Supplementary Table S6, A, path_a_s2, secondary, 0.975 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.975, cap_500 | 717372.300872216 |  |
| 1003 | 286 | Supplementary Table S6, A, continue_s1, main, 0.975 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.975, cap_500 | 285849.529623509 |  |
| 1004 | 404 | Supplementary Table S6, A, continue_s1, secondary, 0.975 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.975, cap_500 | 404175.81630156 |  |
| 1005 | −1 | Supplementary Table S6, A, path_a_s1, main, 1.000 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 1.000, cap_500 | -740.806878935912 |  |
| 1006 | −1 | Supplementary Table S6, A, path_a_s1, secondary, 1.000 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 1.000, cap_500 | -740.806878934049 |  |
| 1007 | −1 | Supplementary Table S6, A, path_a_s2, main, 1.000 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 1.000, cap_500 | -740.806878935912 |  |
| 1008 | −1 | Supplementary Table S6, A, path_a_s2, secondary, 1.000 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 1.000, cap_500 | -740.806878934049 |  |
| 1009 | −96 | Supplementary Table S6, A, continue_s1, main, 1.000 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 1.000, cap_500 | -95797.9165457081 |  |
| 1010 | −91 | Supplementary Table S6, A, continue_s1, secondary, 1.000 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 1.000, cap_500 | -90914.5105820563 |  |
| 1011 | 4,990 | Supplementary Table S6, B, path_a_s1, main, 0.700 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.700, cap_750 | 4990291.94378184 |  |
| 1012 | 6,448 | Supplementary Table S6, B, path_a_s1, secondary, 0.700 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.700, cap_750 | 6448489.7205114 |  |
| 1013 | 9,535 | Supplementary Table S6, B, path_a_s2, main, 0.700 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.700, cap_750 | 9534684.67496282 |  |
| 1014 | 12,451 | Supplementary Table S6, B, path_a_s2, secondary, 0.700 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.700, cap_750 | 12451378.1017695 |  |
| 1015 | 6,476 | Supplementary Table S6, B, continue_s1, main, 0.700 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.700, cap_750 | 6475759.64151967 |  |
| 1016 | 8,546 | Supplementary Table S6, B, continue_s1, secondary, 0.700 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.700, cap_750 | 8545557.73766746 |  |
| 1017 | 4,560 | Supplementary Table S6, B, path_a_s1, main, 0.725 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.725, cap_750 | 4559958.29186289 |  |
| 1018 | 5,888 | Supplementary Table S6, B, path_a_s1, secondary, 0.725 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.725, cap_750 | 5887792.04373594 |  |
| 1019 | 8,702 | Supplementary Table S6, B, path_a_s2, main, 0.725 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.725, cap_750 | 8702045.39541211 |  |
| 1020 | 11,355 | Supplementary Table S6, B, path_a_s2, secondary, 0.725 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.725, cap_750 | 11354512.4610965 |  |
| 1021 | 5,905 | Supplementary Table S6, B, continue_s1, main, 0.725 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.725, cap_750 | 5904558.09867604 |  |
| 1022 | 7,786 | Supplementary Table S6, B, continue_s1, secondary, 0.725 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.725, cap_750 | 7785987.79805765 |  |
| 1023 | 4,132 | Supplementary Table S6, B, path_a_s1, main, 0.750 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.750, cap_750 | 4132310.62736908 |  |
| 1024 | 5,331 | Supplementary Table S6, B, path_a_s1, secondary, 0.750 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.750, cap_750 | 5331453.28004451 |  |
| 1025 | 7,877 | Supplementary Table S6, B, path_a_s2, main, 0.750 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.750, cap_750 | 7876566.7140667 |  |
| 1026 | 10,269 | Supplementary Table S6, B, path_a_s2, secondary, 0.750 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.750, cap_750 | 10268825.5225691 |  |
| 1027 | 5,338 | Supplementary Table S6, B, continue_s1, main, 0.750 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.750, cap_750 | 5337777.43143206 |  |
| 1028 | 7,034 | Supplementary Table S6, B, continue_s1, secondary, 0.750 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.750, cap_750 | 7033952.30054594 |  |
| 1029 | 3,707 | Supplementary Table S6, B, path_a_s1, main, 0.775 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.775, cap_750 | 3707328.75004005 |  |
| 1030 | 4,779 | Supplementary Table S6, B, path_a_s1, secondary, 0.775 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.775, cap_750 | 4779433.45481234 |  |
| 1031 | 7,058 | Supplementary Table S6, B, path_a_s2, main, 0.775 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.775, cap_750 | 7058172.05628113 |  |
| 1032 | 9,194 | Supplementary Table S6, B, path_a_s2, secondary, 0.775 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.775, cap_750 | 9194188.37779063 |  |
| 1033 | 4,775 | Supplementary Table S6, B, continue_s1, main, 0.775 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.775, cap_750 | 4775375.91761018 |  |
| 1034 | 6,289 | Supplementary Table S6, B, continue_s1, secondary, 0.775 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.775, cap_750 | 6289362.63752974 |  |
| 1035 | 3,285 | Supplementary Table S6, B, path_a_s1, main, 0.800 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.800, cap_750 | 3284992.61544322 |  |
| 1036 | 4,232 | Supplementary Table S6, B, path_a_s1, secondary, 0.800 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.800, cap_750 | 4231692.97074881 |  |
| 1037 | 6,247 | Supplementary Table S6, B, path_a_s2, main, 0.800 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.800, cap_750 | 6246785.73063127 |  |
| 1038 | 8,130 | Supplementary Table S6, B, path_a_s2, secondary, 0.800 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.800, cap_750 | 8130473.70692911 |  |
| 1039 | 4,217 | Supplementary Table S6, B, continue_s1, main, 0.800 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.800, cap_750 | 4217312.24189862 |  |
| 1040 | 5,552 | Supplementary Table S6, B, continue_s1, secondary, 0.800 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.800, cap_750 | 5552131.28035806 |  |
| 1041 | 2,865 | Supplementary Table S6, B, path_a_s1, main, 0.825 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.825, cap_750 | 2865282.33376812 |  |
| 1042 | 3,688 | Supplementary Table S6, B, path_a_s1, secondary, 0.825 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.825, cap_750 | 3688192.60431636 |  |
| 1043 | 5,442 | Supplementary Table S6, B, path_a_s2, main, 0.825 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.825, cap_750 | 5442332.91847617 |  |
| 1044 | 7,078 | Supplementary Table S6, B, path_a_s2, secondary, 0.825 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.825, cap_750 | 7077555.75843456 |  |
| 1045 | 3,664 | Supplementary Table S6, B, continue_s1, main, 0.825 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.825, cap_750 | 3663545.4918598 |  |
| 1046 | 4,822 | Supplementary Table S6, B, continue_s1, secondary, 0.825 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.825, cap_750 | 4822171.76609972 |  |
| 1047 | 2,448 | Supplementary Table S6, B, path_a_s1, main, 0.850 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.850, cap_750 | 2448178.16862878 |  |
| 1048 | 3,149 | Supplementary Table S6, B, path_a_s1, secondary, 0.850 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.850, cap_750 | 3148893.50218542 |  |
| 1049 | 4,645 | Supplementary Table S6, B, path_a_s2, main, 0.850 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.850, cap_750 | 4644739.66364707 |  |
| 1050 | 6,035 | Supplementary Table S6, B, path_a_s2, secondary, 0.850 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.850, cap_750 | 6035310.32900987 |  |
| 1051 | 3,114 | Supplementary Table S6, B, continue_s1, main, 0.850 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.850, cap_750 | 3114035.15398265 |  |
| 1052 | 4,099 | Supplementary Table S6, B, continue_s1, secondary, 0.850 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.850, cap_750 | 4099398.68447263 |  |
| 1053 | 2,034 | Supplementary Table S6, B, path_a_s1, main, 0.875 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.875, cap_750 | 2033660.53587824 |  |
| 1054 | 2,614 | Supplementary Table S6, B, path_a_s1, secondary, 0.875 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.875, cap_750 | 2613757.17772556 |  |
| 1055 | 3,854 | Supplementary Table S6, B, path_a_s2, main, 0.875 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.875, cap_750 | 3853932.8622549 |  |
| 1056 | 5,004 | Supplementary Table S6, B, path_a_s2, secondary, 0.875 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.875, cap_750 | 5003614.74385018 |  |
| 1057 | 2,569 | Supplementary Table S6, B, continue_s1, main, 0.875 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.875, cap_750 | 2568741.10976624 |  |
| 1058 | 3,384 | Supplementary Table S6, B, continue_s1, secondary, 0.875 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.875, cap_750 | 3383727.6649352 |  |
| 1059 | 1,622 | Supplementary Table S6, B, path_a_s1, main, 0.900 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.900, cap_750 | 1621710.0024281 |  |
| 1060 | 2,083 | Supplementary Table S6, B, path_a_s1, secondary, 0.900 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.900, cap_750 | 2082745.50752366 |  |
| 1061 | 3,070 | Supplementary Table S6, B, path_a_s2, main, 0.900 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.900, cap_750 | 3069840.25262148 |  |
| 1062 | 3,982 | Supplementary Table S6, B, path_a_s2, secondary, 0.900 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.900, cap_750 | 3982347.83713686 |  |
| 1063 | 2,028 | Supplementary Table S6, B, continue_s1, main, 0.900 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.900, cap_750 | 2027623.63184974 |  |
| 1064 | 2,675 | Supplementary Table S6, B, continue_s1, secondary, 0.900 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.900, cap_750 | 2675075.36393604 |  |
| 1065 | 1,212 | Supplementary Table S6, B, path_a_s1, main, 0.925 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.925, cap_750 | 1212307.28508032 |  |
| 1066 | 1,556 | Supplementary Table S6, B, path_a_s1, secondary, 0.925 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.925, cap_750 | 1555820.72794251 |  |
| 1067 | 2,292 | Supplementary Table S6, B, path_a_s2, main, 0.925 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.925, cap_750 | 2292390.40533359 |  |
| 1068 | 2,971 | Supplementary Table S6, B, path_a_s2, secondary, 0.925 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.925, cap_750 | 2971389.93278454 |  |
| 1069 | 1,491 | Supplementary Table S6, B, continue_s1, main, 0.925 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.925, cap_750 | 1490643.38017508 |  |
| 1070 | 1,973 | Supplementary Table S6, B, continue_s1, secondary, 0.925 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.925, cap_750 | 1973359.45232094 |  |
| 1071 | 805 | Supplementary Table S6, B, path_a_s1, main, 0.950 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.950, cap_750 | 805433.249367611 |  |
| 1072 | 1,033 | Supplementary Table S6, B, path_a_s1, secondary, 0.950 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.950, cap_750 | 1032945.43170627 |  |
| 1073 | 1,522 | Supplementary Table S6, B, path_a_s2, main, 0.950 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.950, cap_750 | 1521512.71340992 |  |
| 1074 | 1,971 | Supplementary Table S6, B, path_a_s2, secondary, 0.950 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.950, cap_750 | 1970622.82543965 |  |
| 1075 | 958 | Supplementary Table S6, B, continue_s1, main, 0.950 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.950, cap_750 | 957761.39818849 |  |
| 1076 | 1,278 | Supplementary Table S6, B, continue_s1, secondary, 0.950 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.950, cap_750 | 1278498.60289235 |  |
| 1077 | 401 | Supplementary Table S6, B, path_a_s1, main, 0.975 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 0.975, cap_750 | 401068.908401951 |  |
| 1078 | 514 | Supplementary Table S6, B, path_a_s1, secondary, 0.975 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 0.975, cap_750 | 514082.564522246 |  |
| 1079 | 757 | Supplementary Table S6, B, path_a_s2, main, 0.975 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 0.975, cap_750 | 757137.382588912 |  |
| 1080 | 980 | Supplementary Table S6, B, path_a_s2, secondary, 0.975 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 0.975, cap_750 | 979929.761724995 |  |
| 1081 | 429 | Supplementary Table S6, B, continue_s1, main, 0.975 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 0.975, cap_750 | 428939.109081392 |  |
| 1082 | 590 | Supplementary Table S6, B, continue_s1, secondary, 0.975 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 0.975, cap_750 | 590412.47812474 |  |
| 1083 | −1 | Supplementary Table S6, B, path_a_s1, main, 1.000 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = main, axis = hr0, x = 1.000, cap_750 | -804.578268402805 |  |
| 1084 | −1 | Supplementary Table S6, B, path_a_s1, secondary, 1.000 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s1, comparison = secondary, axis = hr0, x = 1.000, cap_750 | -804.578268400943 |  |
| 1085 | −1 | Supplementary Table S6, B, path_a_s2, main, 1.000 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = main, axis = hr0, x = 1.000, cap_750 | -804.578268402805 |  |
| 1086 | −1 | Supplementary Table S6, B, path_a_s2, secondary, 1.000 | `output/phase2/main/scenario_caps.csv` | scenario = path_a_s2, comparison = secondary, axis = hr0, x = 1.000, cap_750 | -804.578268400943 |  |
| 1087 | −96 | Supplementary Table S6, B, continue_s1, main, 1.000 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = main, axis = hr0, x = 1.000, cap_750 | -95861.687935175 |  |
| 1088 | −91 | Supplementary Table S6, B, continue_s1, secondary, 1.000 | `output/phase2/main/scenario_caps.csv` | scenario = continue_s1, comparison = secondary, axis = hr0, x = 1.000, cap_750 | -90978.2819715232 |  |
| 1089 | 3,451 | Supplementary Table S7, header | `input/params/cohort_N_jbcs2024.csv` | item = nac_total, value | 3451 |  |
| 1090 | 2,294 | Supplementary Table S7, header | `input/params/cohort_N_jbcs2024.csv` | item = nac_pembro, value | 2294 |  |
| 1091 | 1,157 | Supplementary Table S7, header | `input/params/cohort_N_jbcs2024.csv` | nac_total - nac_pembro | 1157 |  |
| 1092 | 2,900 | Supplementary Table S7, header | `input/params/cohort_N_jbcs2024.csv` | item = sens_N_2023, value | 2900 |  |
| 1093 | 4,000 | Supplementary Table S7, header | `input/params/cohort_N_jbcs2024.csv` | item = sens_N_upper, value | 4000 |  |
| 1094 | 701 | Supplementary Table S7, A, 0.95, main base | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = base, hr0 = 0.95, nb_person_main_det | 700650.922566834 |  |
| 1095 | 689 | Supplementary Table S7, A, 0.95, main kext | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = kext, hr0 = 0.95, nb_person_main_det | 688843.643184178 |  |
| 1096 | 931 | Supplementary Table S7, A, 0.95, secondary | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = base, hr0 = 0.95, nb_person_secondary_det | 931264.47042199 |  |
| 1097 | 2.68 | Supplementary Table S7, B, main base 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = base, hr0 = 0.95, total_det / 1e9 | 2.6847662086465602 |  |
| 1098 | 2.22 | Supplementary Table S7, B, main base 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = base, hr0 = 0.95, total_lo / 1e9 | 2.22351871179738 |  |
| 1099 | 2.94 | Supplementary Table S7, B, main base 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = base, hr0 = 0.95, total_hi / 1e9 | 2.93826668809199 |  |
| 1100 | 2.66 | Supplementary Table S7, B, main kext 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = kext, hr0 = 0.95, total_det / 1e9 | 2.65768030974275 |  |
| 1101 | 2.21 | Supplementary Table S7, B, main kext 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = kext, hr0 = 0.95, total_lo / 1e9 | 2.20678618132004 |  |
| 1102 | 2.91 | Supplementary Table S7, B, main kext 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = kext, hr0 = 0.95, total_hi / 1e9 | 2.90769793260886 |  |
| 1103 | 2.26 | Supplementary Table S7, B, sens_2023 base 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = base, hr0 = 0.95, total_det / 1e9 | 2.25610605768618 |  |
| 1104 | 1.87 | Supplementary Table S7, B, sens_2023 base 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = base, hr0 = 0.95, total_lo / 1e9 | 1.86850311915746 |  |
| 1105 | 2.47 | Supplementary Table S7, B, sens_2023 base 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = base, hr0 = 0.95, total_hi / 1e9 | 2.4691316706655404 |  |
| 1106 | 2.23 | Supplementary Table S7, B, sens_2023 kext 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = kext, hr0 = 0.95, total_det / 1e9 | 2.23334479810315 |  |
| 1107 | 1.85 | Supplementary Table S7, B, sens_2023 kext 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = kext, hr0 = 0.95, total_lo / 1e9 | 1.85444216917651 |  |
| 1108 | 2.44 | Supplementary Table S7, B, sens_2023 kext 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = kext, hr0 = 0.95, total_hi / 1e9 | 2.4434436408477804 |  |
| 1109 | 3.11 | Supplementary Table S7, B, sens_upper base 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = base, hr0 = 0.95, total_det / 1e9 | 3.11187042439474 |  |
| 1110 | 2.58 | Supplementary Table S7, B, sens_upper base 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = base, hr0 = 0.95, total_lo / 1e9 | 2.5772456815965 |  |
| 1111 | 3.41 | Supplementary Table S7, B, sens_upper base 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = base, hr0 = 0.95, total_hi / 1e9 | 3.4056988560904 |  |
| 1112 | 3.08 | Supplementary Table S7, B, sens_upper kext 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = kext, hr0 = 0.95, total_det / 1e9 | 3.08047558359055 |  |
| 1113 | 2.56 | Supplementary Table S7, B, sens_upper kext 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = kext, hr0 = 0.95, total_lo / 1e9 | 2.55785126782966 |  |
| 1114 | 3.37 | Supplementary Table S7, B, sens_upper kext 0.95 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = kext, hr0 = 0.95, total_hi / 1e9 | 3.3702670908245302 |  |
| 1115 | 1,610 | Supplementary Table S7, A, 0.90, main base | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = base, hr0 = 0.90, nb_person_main_det | 1609590.91184234 |  |
| 1116 | 1,586 | Supplementary Table S7, A, 0.90, main kext | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = kext, hr0 = 0.90, nb_person_main_det | 1585884.75398465 |  |
| 1117 | 2,079 | Supplementary Table S7, A, 0.90, secondary | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = base, hr0 = 0.90, nb_person_secondary_det | 2078949.53861421 |  |
| 1118 | 6.10 | Supplementary Table S7, B, main base 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = base, hr0 = 0.90, total_det / 1e9 | 6.0977461679429705 |  |
| 1119 | 5.16 | Supplementary Table S7, B, main base 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = base, hr0 = 0.90, total_lo / 1e9 | 5.16258776993529 |  |
| 1120 | 6.61 | Supplementary Table S7, B, main base 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = base, hr0 = 0.90, total_hi / 1e9 | 6.613410026291411 |  |
| 1121 | 6.04 | Supplementary Table S7, B, main kext 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = kext, hr0 = 0.90, total_det / 1e9 | 6.04336424181743 |  |
| 1122 | 5.13 | Supplementary Table S7, B, main kext 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = kext, hr0 = 0.90, total_lo / 1e9 | 5.12903973850971 |  |
| 1123 | 6.55 | Supplementary Table S7, B, main kext 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = kext, hr0 = 0.90, total_hi / 1e9 | 6.54693429618104 |  |
| 1124 | 5.12 | Supplementary Table S7, B, sens_2023 base 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = base, hr0 = 0.90, total_det / 1e9 | 5.12415644364955 |  |
| 1125 | 4.34 | Supplementary Table S7, B, sens_2023 base 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = base, hr0 = 0.90, total_lo / 1e9 | 4.33830905036579 |  |
| 1126 | 5.56 | Supplementary Table S7, B, sens_2023 base 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = base, hr0 = 0.90, total_hi / 1e9 | 5.5574874170516 |  |
| 1127 | 5.08 | Supplementary Table S7, B, sens_2023 kext 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = kext, hr0 = 0.90, total_det / 1e9 | 5.07845734606507 |  |
| 1128 | 4.31 | Supplementary Table S7, B, sens_2023 kext 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = kext, hr0 = 0.90, total_lo / 1e9 | 4.3101174273190805 |  |
| 1129 | 5.50 | Supplementary Table S7, B, sens_2023 kext 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = kext, hr0 = 0.90, total_hi / 1e9 | 5.50162545897567 |  |
| 1130 | 7.07 | Supplementary Table S7, B, sens_upper base 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = base, hr0 = 0.90, total_det / 1e9 | 7.06780199124076 |  |
| 1131 | 5.98 | Supplementary Table S7, B, sens_upper base 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = base, hr0 = 0.90, total_lo / 1e9 | 5.98387455222868 |  |
| 1132 | 7.67 | Supplementary Table S7, B, sens_upper base 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = base, hr0 = 0.90, total_hi / 1e9 | 7.66549988558842 |  |
| 1133 | 7.00 | Supplementary Table S7, B, sens_upper kext 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = kext, hr0 = 0.90, total_det / 1e9 | 7.00476875319319 |  |
| 1134 | 5.94 | Supplementary Table S7, B, sens_upper kext 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = kext, hr0 = 0.90, total_lo / 1e9 | 5.94498955492287 |  |
| 1135 | 7.59 | Supplementary Table S7, B, sens_upper kext 0.90 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = kext, hr0 = 0.90, total_hi / 1e9 | 7.58844890893195 |  |
| 1136 | 2,534 | Supplementary Table S7, A, 0.85, main base | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = base, hr0 = 0.85, nb_person_main_det | 2534000.8870362 |  |
| 1137 | 2,498 | Supplementary Table S7, A, 0.85, main kext | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = kext, hr0 = 0.85, nb_person_main_det | 2498303.42209718 |  |
| 1138 | 3,250 | Supplementary Table S7, A, 0.85, secondary | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = base, hr0 = 0.85, nb_person_secondary_det | 3250498.84929941 |  |
| 1139 | 9.57 | Supplementary Table S7, B, main base 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = base, hr0 = 0.85, total_det / 1e9 | 9.57382520350046 |  |
| 1140 | 8.15 | Supplementary Table S7, B, main base 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = base, hr0 = 0.85, total_lo / 1e9 | 8.15181106272254 |  |
| 1141 | 10.36 | Supplementary Table S7, B, main base 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = base, hr0 = 0.85, total_hi / 1e9 | 10.3606370185432 |  |
| 1142 | 9.49 | Supplementary Table S7, B, main kext 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = kext, hr0 = 0.85, total_det / 1e9 | 9.49193521893035 |  |
| 1143 | 8.10 | Supplementary Table S7, B, main kext 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = kext, hr0 = 0.85, total_lo / 1e9 | 8.10136404658124 |  |
| 1144 | 10.25 | Supplementary Table S7, B, main kext 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = main, column = kext, hr0 = 0.85, total_hi / 1e9 | 10.2531553239554 |  |
| 1145 | 8.05 | Supplementary Table S7, B, sens_2023 base 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = base, hr0 = 0.85, total_det / 1e9 | 8.04523126344576 |  |
| 1146 | 6.85 | Supplementary Table S7, B, sens_2023 base 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = base, hr0 = 0.85, total_lo / 1e9 | 6.85026139724583 |  |
| 1147 | 8.71 | Supplementary Table S7, B, sens_2023 base 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = base, hr0 = 0.85, total_hi / 1e9 | 8.70641766264138 |  |
| 1148 | 7.98 | Supplementary Table S7, B, sens_2023 kext 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = kext, hr0 = 0.85, total_det / 1e9 | 7.97641615036164 |  |
| 1149 | 6.81 | Supplementary Table S7, B, sens_2023 kext 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = kext, hr0 = 0.85, total_lo / 1e9 | 6.80786894670692 |  |
| 1150 | 8.62 | Supplementary Table S7, B, sens_2023 kext 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_2023, column = kext, hr0 = 0.85, total_hi / 1e9 | 8.6160969108869 |  |
| 1151 | 11.10 | Supplementary Table S7, B, sens_upper base 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = base, hr0 = 0.85, total_det / 1e9 | 11.096870708201099 |  |
| 1152 | 9.45 | Supplementary Table S7, B, sens_upper base 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = base, hr0 = 0.85, total_lo / 1e9 | 9.448636409994249 |  |
| 1153 | 12.01 | Supplementary Table S7, B, sens_upper base 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = base, hr0 = 0.85, total_hi / 1e9 | 12.0088519484709 |  |
| 1154 | 11.00 | Supplementary Table S7, B, sens_upper kext 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = kext, hr0 = 0.85, total_det / 1e9 | 11.0019533108436 |  |
| 1155 | 9.39 | Supplementary Table S7, B, sens_upper kext 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = kext, hr0 = 0.85, total_lo / 1e9 | 9.39016406442334 |  |
| 1156 | 11.88 | Supplementary Table S7, B, sens_upper kext 0.85 | `output/phase2/main/cohort_value_jbcs2024.csv` | setting = sens_upper, column = kext, hr0 = 0.85, total_hi / 1e9 | 11.8842716012233 |  |
| 1157 | −1 | Supplementary Table S8, A, pcr 0.000, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.000, cap_500 | -740.806878935912 |  |
| 1158 | −2 | Supplementary Table S8, A, pcr 0.000, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.000, cap500_lo | -1542.24790409717 |  |
| 1159 | 0 | Supplementary Table S8, A, pcr 0.000, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.000, cap500_hi | -220.922133505826 |  |
| 1160 | 0.0 | Supplementary Table S8, A, pcr 0.000, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.000, p_cap500_ge_E02 | 0.0 |  |
| 1161 | −1 | Supplementary Table S8, A, pcr 0.000, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.000, cap_500 | -740.806878934049 |  |
| 1162 | −2 | Supplementary Table S8, A, pcr 0.000, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.000, cap500_lo | -1542.24790409717 |  |
| 1163 | 0 | Supplementary Table S8, A, pcr 0.000, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.000, cap500_hi | -220.922133505779 |  |
| 1164 | 0.0 | Supplementary Table S8, A, pcr 0.000, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.000, p_cap500_ge_E02 | 0.0 |  |
| 1165 | −1 | Supplementary Table S8, A, pcr 0.000, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.000, cap_500 | -740.806878934049 |  |
| 1166 | −2 | Supplementary Table S8, A, pcr 0.000, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.000, cap500_lo | -1542.24790409722 |  |
| 1167 | 0 | Supplementary Table S8, A, pcr 0.000, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.000, cap500_hi | -220.922133503963 |  |
| 1168 | 0.0 | Supplementary Table S8, A, pcr 0.000, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.000, p_cap500_ge_E02 | 0.0 |  |
| 1169 | 0 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 0.0 |  |
| 1170 | 389 | Supplementary Table S8, A, pcr 0.010, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.010, cap_500 | 389138.722985376 |  |
| 1171 | 238 | Supplementary Table S8, A, pcr 0.010, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.010, cap500_lo | 238085.85464704 |  |
| 1172 | 570 | Supplementary Table S8, A, pcr 0.010, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.010, cap500_hi | 570400.288388543 |  |
| 1173 | 99.0 | Supplementary Table S8, A, pcr 0.010, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.010, p_cap500_ge_E02 | 0.99 |  |
| 1174 | 385 | Supplementary Table S8, A, pcr 0.010, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.010, cap_500 | 384598.552132936 |  |
| 1175 | 233 | Supplementary Table S8, A, pcr 0.010, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.010, cap500_lo | 233207.05054128 |  |
| 1176 | 566 | Supplementary Table S8, A, pcr 0.010, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.010, cap500_hi | 565707.768136197 |  |
| 1177 | 99.0 | Supplementary Table S8, A, pcr 0.010, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.010, p_cap500_ge_E02 | 0.99 |  |
| 1178 | 345 | Supplementary Table S8, A, pcr 0.010, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.010, cap_500 | 344703.39961624 |  |
| 1179 | 95 | Supplementary Table S8, A, pcr 0.010, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.010, cap500_lo | 94971.7546478846 |  |
| 1180 | 533 | Supplementary Table S8, A, pcr 0.010, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.010, cap500_hi | 533229.985107931 |  |
| 1181 | 88.4 | Supplementary Table S8, A, pcr 0.010, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.010, p_cap500_ge_E02 | 0.884 |  |
| 1182 | 1 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 1.0 |  |
| 1183 | 779 | Supplementary Table S8, A, pcr 0.020, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.020, cap_500 | 779018.252849525 |  |
| 1184 | 477 | Supplementary Table S8, A, pcr 0.020, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.020, cap500_lo | 476947.125284586 |  |
| 1185 | 1,142 | Supplementary Table S8, A, pcr 0.020, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.020, cap500_hi | 1141800.16528786 |  |
| 1186 | 100.0 | Supplementary Table S8, A, pcr 0.020, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.020, p_cap500_ge_E02 | 1.0 |  |
| 1187 | 770 | Supplementary Table S8, A, pcr 0.020, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.020, cap_500 | 769937.911144783 |  |
| 1188 | 467 | Supplementary Table S8, A, pcr 0.020, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.020, cap500_lo | 467189.517072836 |  |
| 1189 | 1,132 | Supplementary Table S8, A, pcr 0.020, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.020, cap500_hi | 1132216.88113935 |  |
| 1190 | 100.0 | Supplementary Table S8, A, pcr 0.020, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.020, p_cap500_ge_E02 | 1.0 |  |
| 1191 | 690 | Supplementary Table S8, A, pcr 0.020, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.020, cap_500 | 690147.606111444 |  |
| 1192 | 190 | Supplementary Table S8, A, pcr 0.020, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.020, cap500_lo | 190350.772293056 |  |
| 1193 | 1,067 | Supplementary Table S8, A, pcr 0.020, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.020, cap500_hi | 1067006.70044931 |  |
| 1194 | 97.4 | Supplementary Table S8, A, pcr 0.020, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.020, p_cap500_ge_E02 | 0.974 |  |
| 1195 | 2 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 2.0 |  |
| 1196 | 1,169 | Supplementary Table S8, A, pcr 0.030, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.030, cap_500 | 1168897.78271379 |  |
| 1197 | 716 | Supplementary Table S8, A, pcr 0.030, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.030, cap500_lo | 715808.395921972 |  |
| 1198 | 1,713 | Supplementary Table S8, A, pcr 0.030, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.030, cap500_hi | 1713200.04218711 |  |
| 1199 | 100.0 | Supplementary Table S8, A, pcr 0.030, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.030, p_cap500_ge_E02 | 1.0 |  |
| 1200 | 1,155 | Supplementary Table S8, A, pcr 0.030, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.030, cap_500 | 1155277.27015647 |  |
| 1201 | 701 | Supplementary Table S8, A, pcr 0.030, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.030, cap500_lo | 701171.983604601 |  |
| 1202 | 1,699 | Supplementary Table S8, A, pcr 0.030, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.030, cap500_hi | 1698725.99414245 |  |
| 1203 | 100.0 | Supplementary Table S8, A, pcr 0.030, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.030, p_cap500_ge_E02 | 1.0 |  |
| 1204 | 1,036 | Supplementary Table S8, A, pcr 0.030, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.030, cap_500 | 1035591.81260657 |  |
| 1205 | 286 | Supplementary Table S8, A, pcr 0.030, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.030, cap500_lo | 285729.78993832 |  |
| 1206 | 1,601 | Supplementary Table S8, A, pcr 0.030, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.030, cap500_hi | 1600783.41579061 |  |
| 1207 | 98.4 | Supplementary Table S8, A, pcr 0.030, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.030, p_cap500_ge_E02 | 0.984 |  |
| 1208 | 3 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 3.0 |  |
| 1209 | 1,559 | Supplementary Table S8, A, pcr 0.040, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.040, cap_500 | 1558777.31257782 |  |
| 1210 | 955 | Supplementary Table S8, A, pcr 0.040, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.040, cap500_lo | 954669.66655942 |  |
| 1211 | 2,285 | Supplementary Table S8, A, pcr 0.040, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.040, cap500_hi | 2284599.91908651 |  |
| 1212 | 100.0 | Supplementary Table S8, A, pcr 0.040, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.040, p_cap500_ge_E02 | 1.0 |  |
| 1213 | 1,541 | Supplementary Table S8, A, pcr 0.040, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.040, cap_500 | 1540616.62916834 |  |
| 1214 | 935 | Supplementary Table S8, A, pcr 0.040, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.040, cap500_lo | 935154.450136092 |  |
| 1215 | 2,265 | Supplementary Table S8, A, pcr 0.040, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.040, cap500_hi | 2265235.10714554 |  |
| 1216 | 100.0 | Supplementary Table S8, A, pcr 0.040, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.040, p_cap500_ge_E02 | 1.0 |  |
| 1217 | 1,381 | Supplementary Table S8, A, pcr 0.040, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.040, cap_500 | 1381036.01910188 |  |
| 1218 | 381 | Supplementary Table S8, A, pcr 0.040, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.040, cap500_lo | 381108.807583553 |  |
| 1219 | 2,135 | Supplementary Table S8, A, pcr 0.040, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.040, cap500_hi | 2134560.13113184 |  |
| 1220 | 99.1 | Supplementary Table S8, A, pcr 0.040, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.040, p_cap500_ge_E02 | 0.991 |  |
| 1221 | 4 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 4.0 |  |
| 1222 | 1,949 | Supplementary Table S8, A, pcr 0.050, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.050, cap_500 | 1948656.84244217 |  |
| 1223 | 1,194 | Supplementary Table S8, A, pcr 0.050, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.050, cap500_lo | 1193530.93719672 |  |
| 1224 | 2,856 | Supplementary Table S8, A, pcr 0.050, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.050, cap500_hi | 2855999.79598578 |  |
| 1225 | 100.0 | Supplementary Table S8, A, pcr 0.050, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.050, p_cap500_ge_E02 | 1.0 |  |
| 1226 | 1,926 | Supplementary Table S8, A, pcr 0.050, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.050, cap_500 | 1925955.98818002 |  |
| 1227 | 1,169 | Supplementary Table S8, A, pcr 0.050, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.050, cap500_lo | 1169136.91666754 |  |
| 1228 | 2,832 | Supplementary Table S8, A, pcr 0.050, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.050, cap500_hi | 2831744.2201487 |  |
| 1229 | 100.0 | Supplementary Table S8, A, pcr 0.050, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.050, p_cap500_ge_E02 | 1.0 |  |
| 1230 | 1,726 | Supplementary Table S8, A, pcr 0.050, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.050, cap_500 | 1726480.22559694 |  |
| 1231 | 476 | Supplementary Table S8, A, pcr 0.050, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.050, cap500_lo | 476487.825228802 |  |
| 1232 | 2,668 | Supplementary Table S8, A, pcr 0.050, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.050, cap500_hi | 2668336.84647316 |  |
| 1233 | 99.2 | Supplementary Table S8, A, pcr 0.050, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.050, p_cap500_ge_E02 | 0.992 |  |
| 1234 | 5 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 5.0 |  |
| 1235 | 2,339 | Supplementary Table S8, A, pcr 0.060, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.060, cap_500 | 2338536.37230647 |  |
| 1236 | 1,432 | Supplementary Table S8, A, pcr 0.060, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.060, cap500_lo | 1432392.207834 |  |
| 1237 | 3,427 | Supplementary Table S8, A, pcr 0.060, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.060, cap500_hi | 3427399.67288509 |  |
| 1238 | 100.0 | Supplementary Table S8, A, pcr 0.060, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.060, p_cap500_ge_E02 | 1.0 |  |
| 1239 | 2,311 | Supplementary Table S8, A, pcr 0.060, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.060, cap_500 | 2311295.34719204 |  |
| 1240 | 1,403 | Supplementary Table S8, A, pcr 0.060, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.060, cap500_lo | 1403119.38319934 |  |
| 1241 | 3,398 | Supplementary Table S8, A, pcr 0.060, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.060, cap500_hi | 3398253.33315189 |  |
| 1242 | 100.0 | Supplementary Table S8, A, pcr 0.060, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.060, p_cap500_ge_E02 | 1.0 |  |
| 1243 | 2,072 | Supplementary Table S8, A, pcr 0.060, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.060, cap_500 | 2071924.43209198 |  |
| 1244 | 572 | Supplementary Table S8, A, pcr 0.060, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.060, cap500_lo | 571866.842874015 |  |
| 1245 | 3,202 | Supplementary Table S8, A, pcr 0.060, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.060, cap500_hi | 3202113.56181438 |  |
| 1246 | 99.3 | Supplementary Table S8, A, pcr 0.060, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.060, p_cap500_ge_E02 | 0.993 |  |
| 1247 | 6 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 6.0 |  |
| 1248 | 2,728 | Supplementary Table S8, A, pcr 0.070, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.070, cap_500 | 2728415.90217078 |  |
| 1249 | 1,671 | Supplementary Table S8, A, pcr 0.070, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.070, cap500_lo | 1671253.47847137 |  |
| 1250 | 3,999 | Supplementary Table S8, A, pcr 0.070, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.070, cap500_hi | 3998799.5497843 |  |
| 1251 | 100.0 | Supplementary Table S8, A, pcr 0.070, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.070, p_cap500_ge_E02 | 1.0 |  |
| 1252 | 2,697 | Supplementary Table S8, A, pcr 0.070, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.070, cap_500 | 2696634.70620369 |  |
| 1253 | 1,637 | Supplementary Table S8, A, pcr 0.070, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.070, cap500_lo | 1637101.84973081 |  |
| 1254 | 3,965 | Supplementary Table S8, A, pcr 0.070, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.070, cap500_hi | 3964762.44615485 |  |
| 1255 | 100.0 | Supplementary Table S8, A, pcr 0.070, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.070, p_cap500_ge_E02 | 1.0 |  |
| 1256 | 2,417 | Supplementary Table S8, A, pcr 0.070, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.070, cap_500 | 2417368.63858745 |  |
| 1257 | 667 | Supplementary Table S8, A, pcr 0.070, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.070, cap500_lo | 667245.860519323 |  |
| 1258 | 3,736 | Supplementary Table S8, A, pcr 0.070, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.070, cap500_hi | 3735890.27715579 |  |
| 1259 | 99.3 | Supplementary Table S8, A, pcr 0.070, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.070, p_cap500_ge_E02 | 0.993 |  |
| 1260 | 7 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 7.000000000000001 |  |
| 1261 | 3,118 | Supplementary Table S8, A, pcr 0.080, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.080, cap_500 | 3118295.43203491 |  |
| 1262 | 1,910 | Supplementary Table S8, A, pcr 0.080, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.080, cap500_lo | 1910114.74910879 |  |
| 1263 | 4,570 | Supplementary Table S8, A, pcr 0.080, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.080, cap500_hi | 4570199.42668374 |  |
| 1264 | 100.0 | Supplementary Table S8, A, pcr 0.080, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.080, p_cap500_ge_E02 | 1.0 |  |
| 1265 | 3,082 | Supplementary Table S8, A, pcr 0.080, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.080, cap_500 | 3081974.06521543 |  |
| 1266 | 1,871 | Supplementary Table S8, A, pcr 0.080, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.080, cap500_lo | 1871084.31626258 |  |
| 1267 | 4,531 | Supplementary Table S8, A, pcr 0.080, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.080, cap500_hi | 4531271.55915804 |  |
| 1268 | 100.0 | Supplementary Table S8, A, pcr 0.080, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.080, p_cap500_ge_E02 | 1.0 |  |
| 1269 | 2,763 | Supplementary Table S8, A, pcr 0.080, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.080, cap_500 | 2762812.8450825 |  |
| 1270 | 763 | Supplementary Table S8, A, pcr 0.080, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.080, cap500_lo | 762624.878164588 |  |
| 1271 | 4,270 | Supplementary Table S8, A, pcr 0.080, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.080, cap500_hi | 4269666.99249704 |  |
| 1272 | 99.3 | Supplementary Table S8, A, pcr 0.080, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.080, p_cap500_ge_E02 | 0.993 |  |
| 1273 | 8 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 8.0 |  |
| 1274 | 3,508 | Supplementary Table S8, A, pcr 0.090, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.090, cap_500 | 3508174.96189906 |  |
| 1275 | 2,149 | Supplementary Table S8, A, pcr 0.090, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.090, cap500_lo | 2148976.01974615 |  |
| 1276 | 5,142 | Supplementary Table S8, A, pcr 0.090, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.090, cap500_hi | 5141599.30358276 |  |
| 1277 | 100.0 | Supplementary Table S8, A, pcr 0.090, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.090, p_cap500_ge_E02 | 1.0 |  |
| 1278 | 3,467 | Supplementary Table S8, A, pcr 0.090, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.090, cap_500 | 3467313.42422726 |  |
| 1279 | 2,105 | Supplementary Table S8, A, pcr 0.090, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.090, cap500_lo | 2105066.78279393 |  |
| 1280 | 5,098 | Supplementary Table S8, A, pcr 0.090, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.090, cap500_hi | 5097780.67216128 |  |
| 1281 | 100.0 | Supplementary Table S8, A, pcr 0.090, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.090, p_cap500_ge_E02 | 1.0 |  |
| 1282 | 3,108 | Supplementary Table S8, A, pcr 0.090, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.090, cap_500 | 3108257.05157769 |  |
| 1283 | 858 | Supplementary Table S8, A, pcr 0.090, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.090, cap500_lo | 858003.895809789 |  |
| 1284 | 4,803 | Supplementary Table S8, A, pcr 0.090, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.090, cap500_hi | 4803443.7078384 |  |
| 1285 | 99.3 | Supplementary Table S8, A, pcr 0.090, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.090, p_cap500_ge_E02 | 0.993 |  |
| 1286 | 9 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 9.0 |  |
| 1287 | 3,898 | Supplementary Table S8, A, pcr 0.100, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.100, cap_500 | 3898054.4917634 |  |
| 1288 | 2,388 | Supplementary Table S8, A, pcr 0.100, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.100, cap500_lo | 2387837.29038345 |  |
| 1289 | 5,713 | Supplementary Table S8, A, pcr 0.100, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.100, cap500_hi | 5712999.18048233 |  |
| 1290 | 100.0 | Supplementary Table S8, A, pcr 0.100, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.100, p_cap500_ge_E02 | 1.0 |  |
| 1291 | 3,853 | Supplementary Table S8, A, pcr 0.100, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.100, cap_500 | 3852652.78323903 |  |
| 1292 | 2,339 | Supplementary Table S8, A, pcr 0.100, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.100, cap500_lo | 2339049.24932579 |  |
| 1293 | 5,664 | Supplementary Table S8, A, pcr 0.100, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.100, cap500_hi | 5664289.78516441 |  |
| 1294 | 100.0 | Supplementary Table S8, A, pcr 0.100, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.100, p_cap500_ge_E02 | 1.0 |  |
| 1295 | 3,454 | Supplementary Table S8, A, pcr 0.100, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.100, cap_500 | 3453701.25807293 |  |
| 1296 | 953 | Supplementary Table S8, A, pcr 0.100, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.100, cap500_lo | 953382.913455071 |  |
| 1297 | 5,337 | Supplementary Table S8, A, pcr 0.100, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.100, cap500_hi | 5337220.42317975 |  |
| 1298 | 99.3 | Supplementary Table S8, A, pcr 0.100, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.100, p_cap500_ge_E02 | 0.993 |  |
| 1299 | 10 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 10.0 |  |
| 1300 | −1 | Supplementary Table S8, B, pcr 0.000, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.000, cap_750 | -804.578268402805 |  |
| 1301 | −2 | Supplementary Table S8, B, pcr 0.000, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.000, cap750_lo | -1808.47512853255 |  |
| 1302 | 0 | Supplementary Table S8, B, pcr 0.000, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.000, cap750_hi | -160.242131257079 |  |
| 1303 | 0.0 | Supplementary Table S8, B, pcr 0.000, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.000, p_cap750_ge_E02 | 0.0 |  |
| 1304 | −1 | Supplementary Table S8, B, pcr 0.000, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.000, cap_750 | -804.578268400943 |  |
| 1305 | −2 | Supplementary Table S8, B, pcr 0.000, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.000, cap750_lo | -1808.47512853255 |  |
| 1306 | 0 | Supplementary Table S8, B, pcr 0.000, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.000, cap750_hi | -160.242131257079 |  |
| 1307 | 0.0 | Supplementary Table S8, B, pcr 0.000, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.000, p_cap750_ge_E02 | 0.0 |  |
| 1308 | −1 | Supplementary Table S8, B, pcr 0.000, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.000, cap_750 | -804.578268400943 |  |
| 1309 | −2 | Supplementary Table S8, B, pcr 0.000, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.000, cap750_lo | -1808.47512853503 |  |
| 1310 | 0 | Supplementary Table S8, B, pcr 0.000, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.000, cap750_hi | -160.242131256986 |  |
| 1311 | 0.0 | Supplementary Table S8, B, pcr 0.000, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.000, p_cap750_ge_E02 | 0.0 |  |
| 1312 | 0 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 0.0 |  |
| 1313 | 546 | Supplementary Table S8, B, pcr 0.010, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.010, cap_750 | 546074.534689362 |  |
| 1314 | 345 | Supplementary Table S8, B, pcr 0.010, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.010, cap750_lo | 344998.274211851 |  |
| 1315 | 788 | Supplementary Table S8, B, pcr 0.010, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.010, cap750_hi | 787626.288700962 |  |
| 1316 | 100.0 | Supplementary Table S8, B, pcr 0.010, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.010, p_cap750_ge_E02 | 1.0 |  |
| 1317 | 543 | Supplementary Table S8, B, pcr 0.010, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.010, cap_750 | 542633.280878429 |  |
| 1318 | 341 | Supplementary Table S8, B, pcr 0.010, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.010, cap750_lo | 341313.945840635 |  |
| 1319 | 785 | Supplementary Table S8, B, pcr 0.010, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.010, cap750_hi | 785014.486156235 |  |
| 1320 | 100.0 | Supplementary Table S8, B, pcr 0.010, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.010, p_cap750_ge_E02 | 1.0 |  |
| 1321 | 495 | Supplementary Table S8, B, pcr 0.010, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.010, cap_750 | 494990.339748958 |  |
| 1322 | 155 | Supplementary Table S8, B, pcr 0.010, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.010, cap750_lo | 154847.648367217 |  |
| 1323 | 751 | Supplementary Table S8, B, pcr 0.010, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.010, cap750_hi | 751237.052308343 |  |
| 1324 | 96.2 | Supplementary Table S8, B, pcr 0.010, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.010, p_cap750_ge_E02 | 0.962 |  |
| 1325 | 1 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 1.0 |  |
| 1326 | 1,093 | Supplementary Table S8, B, pcr 0.020, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.020, cap_750 | 1092953.64764688 |  |
| 1327 | 691 | Supplementary Table S8, B, pcr 0.020, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.020, cap750_lo | 690801.331559456 |  |
| 1328 | 1,576 | Supplementary Table S8, B, pcr 0.020, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.020, cap750_hi | 1575912.5139363 |  |
| 1329 | 100.0 | Supplementary Table S8, B, pcr 0.020, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.020, p_cap750_ge_E02 | 1.0 |  |
| 1330 | 1,086 | Supplementary Table S8, B, pcr 0.020, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.020, cap_750 | 1086071.14002523 |  |
| 1331 | 683 | Supplementary Table S8, B, pcr 0.020, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.020, cap750_lo | 683448.217104278 |  |
| 1332 | 1,571 | Supplementary Table S8, B, pcr 0.020, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.020, cap750_hi | 1570571.05410284 |  |
| 1333 | 100.0 | Supplementary Table S8, B, pcr 0.020, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.020, p_cap750_ge_E02 | 1.0 |  |
| 1334 | 991 | Supplementary Table S8, B, pcr 0.020, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.020, cap_750 | 990785.257766364 |  |
| 1335 | 310 | Supplementary Table S8, B, pcr 0.020, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.020, cap750_lo | 310123.128465523 |  |
| 1336 | 1,503 | Supplementary Table S8, B, pcr 0.020, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.020, cap750_hi | 1503466.38579944 |  |
| 1337 | 99.1 | Supplementary Table S8, B, pcr 0.020, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.020, p_cap750_ge_E02 | 0.991 |  |
| 1338 | 2 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 2.0 |  |
| 1339 | 1,640 | Supplementary Table S8, B, pcr 0.030, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.030, cap_750 | 1639832.76060456 |  |
| 1340 | 1,037 | Supplementary Table S8, B, pcr 0.030, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.030, cap750_lo | 1036612.1600506 |  |
| 1341 | 2,364 | Supplementary Table S8, B, pcr 0.030, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.030, cap750_hi | 2364198.73917214 |  |
| 1342 | 100.0 | Supplementary Table S8, B, pcr 0.030, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.030, p_cap750_ge_E02 | 1.0 |  |
| 1343 | 1,630 | Supplementary Table S8, B, pcr 0.030, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.030, cap_750 | 1629508.99917178 |  |
| 1344 | 1,026 | Supplementary Table S8, B, pcr 0.030, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.030, cap750_lo | 1025582.48836824 |  |
| 1345 | 2,356 | Supplementary Table S8, B, pcr 0.030, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.030, cap750_hi | 2356127.6220498 |  |
| 1346 | 100.0 | Supplementary Table S8, B, pcr 0.030, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.030, p_cap750_ge_E02 | 1.0 |  |
| 1347 | 1,487 | Supplementary Table S8, B, pcr 0.030, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.030, cap_750 | 1486580.17578365 |  |
| 1348 | 465 | Supplementary Table S8, B, pcr 0.030, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.030, cap750_lo | 465398.608563975 |  |
| 1349 | 2,256 | Supplementary Table S8, B, pcr 0.030, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.030, cap750_hi | 2255687.31737532 |  |
| 1350 | 99.3 | Supplementary Table S8, B, pcr 0.030, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.030, p_cap750_ge_E02 | 0.993 |  |
| 1351 | 3 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 3.0 |  |
| 1352 | 2,187 | Supplementary Table S8, B, pcr 0.040, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.040, cap_750 | 2186711.87356191 |  |
| 1353 | 1,382 | Supplementary Table S8, B, pcr 0.040, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.040, cap750_lo | 1382422.98854188 |  |
| 1354 | 3,152 | Supplementary Table S8, B, pcr 0.040, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.040, cap750_hi | 3152484.96440762 |  |
| 1355 | 100.0 | Supplementary Table S8, B, pcr 0.040, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.040, p_cap750_ge_E02 | 1.0 |  |
| 1356 | 2,173 | Supplementary Table S8, B, pcr 0.040, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.040, cap_750 | 2172946.85831863 |  |
| 1357 | 1,368 | Supplementary Table S8, B, pcr 0.040, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.040, cap750_lo | 1367716.75963179 |  |
| 1358 | 3,142 | Supplementary Table S8, B, pcr 0.040, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.040, cap750_hi | 3141684.18999648 |  |
| 1359 | 100.0 | Supplementary Table S8, B, pcr 0.040, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.040, p_cap750_ge_E02 | 1.0 |  |
| 1360 | 1,982 | Supplementary Table S8, B, pcr 0.040, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.040, cap_750 | 1982375.09380122 |  |
| 1361 | 621 | Supplementary Table S8, B, pcr 0.040, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.040, cap750_lo | 620674.08866237 |  |
| 1362 | 3,008 | Supplementary Table S8, B, pcr 0.040, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.040, cap750_hi | 3007908.24895091 |  |
| 1363 | 99.3 | Supplementary Table S8, B, pcr 0.040, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.040, p_cap750_ge_E02 | 0.993 |  |
| 1364 | 4 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 4.0 |  |
| 1365 | 2,734 | Supplementary Table S8, B, pcr 0.050, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.050, cap_750 | 2733590.98651973 |  |
| 1366 | 1,728 | Supplementary Table S8, B, pcr 0.050, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.050, cap750_lo | 1728233.8170329 |  |
| 1367 | 3,941 | Supplementary Table S8, B, pcr 0.050, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.050, cap750_hi | 3940771.18964304 |  |
| 1368 | 100.0 | Supplementary Table S8, B, pcr 0.050, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.050, p_cap750_ge_E02 | 1.0 |  |
| 1369 | 2,716 | Supplementary Table S8, B, pcr 0.050, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.050, cap_750 | 2716384.71746516 |  |
| 1370 | 1,710 | Supplementary Table S8, B, pcr 0.050, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.050, cap750_lo | 1709851.03089527 |  |
| 1371 | 3,927 | Supplementary Table S8, B, pcr 0.050, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.050, cap750_hi | 3927240.75794352 |  |
| 1372 | 100.0 | Supplementary Table S8, B, pcr 0.050, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.050, p_cap750_ge_E02 | 1.0 |  |
| 1373 | 2,478 | Supplementary Table S8, B, pcr 0.050, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.050, cap_750 | 2478170.0118184 |  |
| 1374 | 776 | Supplementary Table S8, B, pcr 0.050, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.050, cap750_lo | 775949.568760797 |  |
| 1375 | 3,760 | Supplementary Table S8, B, pcr 0.050, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.050, cap750_hi | 3760129.18052653 |  |
| 1376 | 99.3 | Supplementary Table S8, B, pcr 0.050, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.050, p_cap750_ge_E02 | 0.993 |  |
| 1377 | 5 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 5.0 |  |
| 1378 | 3,280 | Supplementary Table S8, B, pcr 0.060, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.060, cap_750 | 3280470.09947748 |  |
| 1379 | 2,074 | Supplementary Table S8, B, pcr 0.060, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.060, cap750_lo | 2074044.64552391 |  |
| 1380 | 4,729 | Supplementary Table S8, B, pcr 0.060, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.060, cap750_hi | 4729057.41487859 |  |
| 1381 | 100.0 | Supplementary Table S8, B, pcr 0.060, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.060, p_cap750_ge_E02 | 1.0 |  |
| 1382 | 3,260 | Supplementary Table S8, B, pcr 0.060, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.060, cap_750 | 3259822.57661222 |  |
| 1383 | 2,052 | Supplementary Table S8, B, pcr 0.060, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.060, cap750_lo | 2051985.30215929 |  |
| 1384 | 4,713 | Supplementary Table S8, B, pcr 0.060, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.060, cap750_hi | 4712797.32588997 |  |
| 1385 | 100.0 | Supplementary Table S8, B, pcr 0.060, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.060, p_cap750_ge_E02 | 1.0 |  |
| 1386 | 2,974 | Supplementary Table S8, B, pcr 0.060, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.060, cap_750 | 2973964.92983557 |  |
| 1387 | 931 | Supplementary Table S8, B, pcr 0.060, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.060, cap750_lo | 931225.048859172 |  |
| 1388 | 4,512 | Supplementary Table S8, B, pcr 0.060, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.060, cap750_hi | 4512350.1121026 |  |
| 1389 | 99.4 | Supplementary Table S8, B, pcr 0.060, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.060, p_cap750_ge_E02 | 0.994 |  |
| 1390 | 6 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 6.0 |  |
| 1391 | 3,827 | Supplementary Table S8, B, pcr 0.070, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.070, cap_750 | 3827349.21243523 |  |
| 1392 | 2,420 | Supplementary Table S8, B, pcr 0.070, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.070, cap750_lo | 2419855.47401504 |  |
| 1393 | 5,517 | Supplementary Table S8, B, pcr 0.070, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.070, cap750_hi | 5517343.6401141 |  |
| 1394 | 100.0 | Supplementary Table S8, B, pcr 0.070, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.070, p_cap750_ge_E02 | 1.0 |  |
| 1395 | 3,803 | Supplementary Table S8, B, pcr 0.070, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.070, cap_750 | 3803260.43575873 |  |
| 1396 | 2,394 | Supplementary Table S8, B, pcr 0.070, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.070, cap750_lo | 2394119.5734228 |  |
| 1397 | 5,498 | Supplementary Table S8, B, pcr 0.070, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.070, cap750_hi | 5498353.89383682 |  |
| 1398 | 100.0 | Supplementary Table S8, B, pcr 0.070, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.070, p_cap750_ge_E02 | 1.0 |  |
| 1399 | 3,470 | Supplementary Table S8, B, pcr 0.070, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.070, cap_750 | 3469759.84785337 |  |
| 1400 | 1,087 | Supplementary Table S8, B, pcr 0.070, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.070, cap750_lo | 1086500.52895769 |  |
| 1401 | 5,265 | Supplementary Table S8, B, pcr 0.070, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.070, cap750_hi | 5264571.04367776 |  |
| 1402 | 99.4 | Supplementary Table S8, B, pcr 0.070, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.070, p_cap750_ge_E02 | 0.994 |  |
| 1403 | 7 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 7.000000000000001 |  |
| 1404 | 4,374 | Supplementary Table S8, B, pcr 0.080, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.080, cap_750 | 4374228.32539272 |  |
| 1405 | 2,766 | Supplementary Table S8, B, pcr 0.080, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.080, cap750_lo | 2765666.30250627 |  |
| 1406 | 6,306 | Supplementary Table S8, B, pcr 0.080, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.080, cap750_hi | 6305629.86534974 |  |
| 1407 | 100.0 | Supplementary Table S8, B, pcr 0.080, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.080, p_cap750_ge_E02 | 1.0 |  |
| 1408 | 4,347 | Supplementary Table S8, B, pcr 0.080, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.080, cap_750 | 4346698.29490537 |  |
| 1409 | 2,736 | Supplementary Table S8, B, pcr 0.080, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.080, cap750_lo | 2736253.84468677 |  |
| 1410 | 6,284 | Supplementary Table S8, B, pcr 0.080, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.080, cap750_hi | 6283910.46178363 |  |
| 1411 | 100.0 | Supplementary Table S8, B, pcr 0.080, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.080, p_cap750_ge_E02 | 1.0 |  |
| 1412 | 3,966 | Supplementary Table S8, B, pcr 0.080, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.080, cap_750 | 3965554.76587054 |  |
| 1413 | 1,242 | Supplementary Table S8, B, pcr 0.080, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.080, cap750_lo | 1241776.00905613 |  |
| 1414 | 6,017 | Supplementary Table S8, B, pcr 0.080, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.080, cap750_hi | 6016791.97525354 |  |
| 1415 | 99.6 | Supplementary Table S8, B, pcr 0.080, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.080, p_cap750_ge_E02 | 0.996 |  |
| 1416 | 8 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 8.0 |  |
| 1417 | 4,921 | Supplementary Table S8, B, pcr 0.090, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.090, cap_750 | 4921107.43835025 |  |
| 1418 | 3,111 | Supplementary Table S8, B, pcr 0.090, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.090, cap750_lo | 3111477.13099739 |  |
| 1419 | 7,094 | Supplementary Table S8, B, pcr 0.090, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.090, cap750_hi | 7093916.09058509 |  |
| 1420 | 100.0 | Supplementary Table S8, B, pcr 0.090, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.090, p_cap750_ge_E02 | 1.0 |  |
| 1421 | 4,890 | Supplementary Table S8, B, pcr 0.090, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.090, cap_750 | 4890136.15405214 |  |
| 1422 | 3,078 | Supplementary Table S8, B, pcr 0.090, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.090, cap750_lo | 3078388.1159501 |  |
| 1423 | 7,069 | Supplementary Table S8, B, pcr 0.090, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.090, cap750_hi | 7069467.02973034 |  |
| 1424 | 100.0 | Supplementary Table S8, B, pcr 0.090, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.090, p_cap750_ge_E02 | 1.0 |  |
| 1425 | 4,461 | Supplementary Table S8, B, pcr 0.090, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.090, cap_750 | 4461349.68388794 |  |
| 1426 | 1,397 | Supplementary Table S8, B, pcr 0.090, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.090, cap750_lo | 1397051.48915448 |  |
| 1427 | 6,769 | Supplementary Table S8, B, pcr 0.090, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.090, cap750_hi | 6769012.90682962 |  |
| 1428 | 99.6 | Supplementary Table S8, B, pcr 0.090, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.090, p_cap750_ge_E02 | 0.996 |  |
| 1429 | 9 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 9.0 |  |
| 1430 | 5,468 | Supplementary Table S8, B, pcr 0.100, main base | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = pcr, x = 0.100, cap_750 | 5467986.55130805 |  |
| 1431 | 3,457 | Supplementary Table S8, B, pcr 0.100, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.100, cap750_lo | 3457287.95948843 |  |
| 1432 | 7,882 | Supplementary Table S8, B, pcr 0.100, main base | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.100, cap750_hi | 7882202.31582088 |  |
| 1433 | 100.0 | Supplementary Table S8, B, pcr 0.100, main base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = pcr, x = 0.100, p_cap750_ge_E02 | 1.0 |  |
| 1434 | 5,434 | Supplementary Table S8, B, pcr 0.100, main kext | `output/phase2/main/det_caps.csv` | comparison = main, column = kext, axis = pcr, x = 0.100, cap_750 | 5433574.01319883 |  |
| 1435 | 3,421 | Supplementary Table S8, B, pcr 0.100, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.100, cap750_lo | 3420522.3872142 |  |
| 1436 | 7,855 | Supplementary Table S8, B, pcr 0.100, main kext | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.100, cap750_hi | 7855023.59767723 |  |
| 1437 | 100.0 | Supplementary Table S8, B, pcr 0.100, main kext, P | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = kext, axis = pcr, x = 0.100, p_cap750_ge_E02 | 1.0 |  |
| 1438 | 4,957 | Supplementary Table S8, B, pcr 0.100, secondary base | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = pcr, x = 0.100, cap_750 | 4957144.6019054 |  |
| 1439 | 1,552 | Supplementary Table S8, B, pcr 0.100, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.100, cap750_lo | 1552326.96925295 |  |
| 1440 | 7,521 | Supplementary Table S8, B, pcr 0.100, secondary base | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.100, cap750_hi | 7521233.83840494 |  |
| 1441 | 99.6 | Supplementary Table S8, B, pcr 0.100, secondary base, P | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = pcr, x = 0.100, p_cap750_ge_E02 | 0.996 |  |
| 1442 | 10 | Supplementary Table S8, row label | `output/phase2/main/det_caps.csv` | x (pcr grid) x 100 | 10.0 |  |
| 1443 | 85,302 | Supplementary Table S9, A01, low | `output/phase2/main/oneway_base.csv` | param_id = A01, low_value | 85302.0 |  |
| 1444 | 113,736 | Supplementary Table S9, A01, high | `output/phase2/main/oneway_base.csv` | param_id = A01, high_value | 113736.0 |  |
| 1445 | 2,053 | Supplementary Table S9, A01, icer_low | `output/phase2/main/oneway_base.csv` | param_id = A01, icer_low | 2052725.39930975 |  |
| 1446 | 2,053 | Supplementary Table S9, A01, icer_high | `output/phase2/main/oneway_base.csv` | param_id = A01, icer_high | 2052755.1373126 |  |
| 1447 | 25,122 | Supplementary Table S9, A02, low | `output/phase2/main/oneway_base.csv` | param_id = A02, low_value | 25122.0 |  |
| 1448 | 33,496 | Supplementary Table S9, A02, high | `output/phase2/main/oneway_base.csv` | param_id = A02, high_value | 33496.0 |  |
| 1449 | 2,053 | Supplementary Table S9, A02, icer_low | `output/phase2/main/oneway_base.csv` | param_id = A02, icer_low | 2052742.90734567 |  |
| 1450 | 2,053 | Supplementary Table S9, A02, icer_high | `output/phase2/main/oneway_base.csv` | param_id = A02, icer_high | 2052755.1373126 |  |
| 1451 | 299,193 | Supplementary Table S9, A03, low | `output/phase2/main/oneway_base.csv` | param_id = A03, low_value | 299193.0 |  |
| 1452 | 398,924 | Supplementary Table S9, A03, high | `output/phase2/main/oneway_base.csv` | param_id = A03, high_value | 398924.0 |  |
| 1453 | 2,729 | Supplementary Table S9, A03, cap_low | `output/phase2/main/oneway_base.csv` | param_id = A03, cap_low | 2729391.34070849 |  |
| 1454 | 2,726 | Supplementary Table S9, A03, cap_high | `output/phase2/main/oneway_base.csv` | param_id = A03, cap_high | 2726400.8870362 |  |
| 1455 | 1,296 | Supplementary Table S9, A03, icer_low | `output/phase2/main/oneway_base.csv` | param_id = A03, icer_low | 1295549.06473065 |  |
| 1456 | 2,053 | Supplementary Table S9, A03, icer_high | `output/phase2/main/oneway_base.csv` | param_id = A03, icer_high | 2052755.1373126 |  |
| 1457 | 10,768 | Supplementary Table S9, A04, low | `output/phase2/main/oneway_base.csv` | param_id = A04, low_value | 10767.5 |  |
| 1458 | 18,160 | Supplementary Table S9, A04, high | `output/phase2/main/oneway_base.csv` | param_id = A04, high_value | 18160.0 |  |
| 1459 | 2,727 | Supplementary Table S9, A04, cap_low | `output/phase2/main/oneway_base.csv` | param_id = A04, cap_low | 2726544.74101834 |  |
| 1460 | 2,726 | Supplementary Table S9, A04, cap_high | `output/phase2/main/oneway_base.csv` | param_id = A04, cap_high | 2726323.07545024 |  |
| 1461 | 2,034 | Supplementary Table S9, A04, icer_low | `output/phase2/main/oneway_base.csv` | param_id = A04, icer_low | 2033909.41597996 |  |
| 1462 | 2,063 | Supplementary Table S9, A04, icer_high | `output/phase2/main/oneway_base.csv` | param_id = A04, icer_high | 2062948.9146671 |  |
| 1463 | 5,820 | Supplementary Table S9, A05, low | `output/phase2/main/oneway_base.csv` | param_id = A05, low_value | 5819.5 |  |
| 1464 | 67,296 | Supplementary Table S9, A05, high | `output/phase2/main/oneway_base.csv` | param_id = A05, high_value | 67295.5 |  |
| 1465 | 2,052 | Supplementary Table S9, A05, icer_low | `output/phase2/main/oneway_base.csv` | param_id = A05, icer_low | 2052473.14754375 |  |
| 1466 | 2,053 | Supplementary Table S9, A05, icer_high | `output/phase2/main/oneway_base.csv` | param_id = A05, icer_high | 2053037.12708145 |  |
| 1467 | 641,441 | Supplementary Table S9, A06, low | `output/phase2/main/oneway_base.csv` | param_id = A06, low_value | 641440.786 |  |
| 1468 | 1,250,000 | Supplementary Table S9, A06, high | `output/phase2/main/oneway_base.csv` | param_id = A06, high_value | 1250000.0 |  |
| 1469 | 2,050 | Supplementary Table S9, A06, icer_low | `output/phase2/main/oneway_base.csv` | param_id = A06, icer_low | 2050395.01483007 |  |
| 1470 | 2,054 | Supplementary Table S9, A06, icer_high | `output/phase2/main/oneway_base.csv` | param_id = A06, icer_high | 2054400.69709072 |  |
| 1471 | 0.50600 | Supplementary Table S9, A07, low | `output/phase2/main/oneway_base.csv` | param_id = A07, low_value | 0.506 |  |
| 1472 | 0.90000 | Supplementary Table S9, A07, high | `output/phase2/main/oneway_base.csv` | param_id = A07, high_value | 0.9 |  |
| 1473 | 2,052 | Supplementary Table S9, A07, icer_low | `output/phase2/main/oneway_base.csv` | param_id = A07, icer_low | 2052384.94498965 |  |
| 1474 | 2,054 | Supplementary Table S9, A07, icer_high | `output/phase2/main/oneway_base.csv` | param_id = A07, icer_high | 2053539.7869939 |  |
| 1475 | 405,300 | Supplementary Table S9, A08, low | `output/phase2/main/oneway_base.csv` | param_id = A08, low_value | 405300.0 |  |
| 1476 | 485,300 | Supplementary Table S9, A08, high | `output/phase2/main/oneway_base.csv` | param_id = A08, high_value | 485300.0 |  |
| 1477 | 2,053 | Supplementary Table S9, A08, icer_low | `output/phase2/main/oneway_base.csv` | param_id = A08, icer_low | 2052588.65949649 |  |
| 1478 | 2,053 | Supplementary Table S9, A08, icer_high | `output/phase2/main/oneway_base.csv` | param_id = A08, icer_high | 2052921.61512871 |  |
| 1479 | 19,293 | Supplementary Table S9, B01, low | `output/phase2/main/oneway_base.csv` | param_id = B01, low_value | 19293.0 |  |
| 1480 | 236,000 | Supplementary Table S9, B01, high | `output/phase2/main/oneway_base.csv` | param_id = B01, high_value | 236000.0 |  |
| 1481 | 2,052 | Supplementary Table S9, B01, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B01, icer_low | 2051912.85804475 |  |
| 1482 | 2,061 | Supplementary Table S9, B01, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B01, icer_high | 2061373.68908699 |  |
| 1483 | 19,428 | Supplementary Table S9, B02, low | `output/phase2/main/oneway_base.csv` | param_id = B02, low_value | 19428.0 |  |
| 1484 | 236,000 | Supplementary Table S9, B02, high | `output/phase2/main/oneway_base.csv` | param_id = B02, high_value | 236000.0 |  |
| 1485 | 2,052 | Supplementary Table S9, B02, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B02, icer_low | 2052445.47398267 |  |
| 1486 | 2,056 | Supplementary Table S9, B02, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B02, icer_high | 2055897.41997245 |  |
| 1487 | 118,000 | Supplementary Table S9, B03, low | `output/phase2/main/oneway_base.csv` | param_id = B03, low_value | 118000.0 |  |
| 1488 | 472,000 | Supplementary Table S9, B03, high | `output/phase2/main/oneway_base.csv` | param_id = B03, high_value | 472000.0 |  |
| 1489 | 2,051 | Supplementary Table S9, B03, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B03, icer_low | 2051357.53035849 |  |
| 1490 | 2,056 | Supplementary Table S9, B03, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B03, icer_high | 2055550.35122082 |  |
| 1491 | 118,000 | Supplementary Table S9, B04, low | `output/phase2/main/oneway_base.csv` | param_id = B04, low_value | 118000.0 |  |
| 1492 | 472,000 | Supplementary Table S9, B04, high | `output/phase2/main/oneway_base.csv` | param_id = B04, high_value | 472000.0 |  |
| 1493 | 2,052 | Supplementary Table S9, B04, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B04, icer_low | 2051847.29473747 |  |
| 1494 | 2,055 | Supplementary Table S9, B04, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B04, icer_high | 2054570.82246285 |  |
| 1495 | 31,628 | Supplementary Table S9, B05, low | `output/phase2/main/oneway_base.csv` | param_id = B05, low_value | 31628.25 |  |
| 1496 | 236,000 | Supplementary Table S9, B05, high | `output/phase2/main/oneway_base.csv` | param_id = B05, high_value | 236000.0 |  |
| 1497 | 2,053 | Supplementary Table S9, B05, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B05, icer_low | 2052699.40065619 |  |
| 1498 | 2,053 | Supplementary Table S9, B05, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B05, icer_high | 2053059.55330484 |  |
| 1499 | 20,370 | Supplementary Table S9, B06, low | `output/phase2/main/oneway_base.csv` | param_id = B06, low_value | 20370.0 |  |
| 1500 | 236,000 | Supplementary Table S9, B06, high | `output/phase2/main/oneway_base.csv` | param_id = B06, high_value | 236000.0 |  |
| 1501 | 2,053 | Supplementary Table S9, B06, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B06, icer_low | 2052682.77674725 |  |
| 1502 | 2,053 | Supplementary Table S9, B06, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B06, icer_high | 2053448.76146526 |  |
| 1503 | 20,370 | Supplementary Table S9, B07, low | `output/phase2/main/oneway_base.csv` | param_id = B07, low_value | 20370.0 |  |
| 1504 | 236,000 | Supplementary Table S9, B07, high | `output/phase2/main/oneway_base.csv` | param_id = B07, high_value | 236000.0 |  |
| 1505 | 2,053 | Supplementary Table S9, B07, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B07, icer_low | 2052646.59646458 |  |
| 1506 | 2,054 | Supplementary Table S9, B07, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B07, icer_high | 2053795.57354159 |  |
| 1507 | 38,057 | Supplementary Table S9, B08, low | `output/phase2/main/oneway_base.csv` | param_id = B08, low_value | 38056.5 |  |
| 1508 | 472,000 | Supplementary Table S9, B08, high | `output/phase2/main/oneway_base.csv` | param_id = B08, high_value | 472000.0 |  |
| 1509 | 2,049 | Supplementary Table S9, B08, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B08, icer_low | 2048653.69542763 |  |
| 1510 | 2,058 | Supplementary Table S9, B08, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B08, icer_high | 2057645.11998368 |  |
| 1511 | 118,000 | Supplementary Table S9, B09, low | `output/phase2/main/oneway_base.csv` | param_id = B09, low_value | 118000.0 |  |
| 1512 | 472,000 | Supplementary Table S9, B09, high | `output/phase2/main/oneway_base.csv` | param_id = B09, high_value | 472000.0 |  |
| 1513 | 2,052 | Supplementary Table S9, B09, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B09, icer_low | 2052475.50647722 |  |
| 1514 | 2,053 | Supplementary Table S9, B09, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B09, icer_high | 2053314.39898335 |  |
| 1515 | 118,000 | Supplementary Table S9, B10, low | `output/phase2/main/oneway_base.csv` | param_id = B10, low_value | 118000.0 |  |
| 1516 | 472,000 | Supplementary Table S9, B10, high | `output/phase2/main/oneway_base.csv` | param_id = B10, high_value | 472000.0 |  |
| 1517 | 2,052 | Supplementary Table S9, B10, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B10, icer_low | 2051777.79744571 |  |
| 1518 | 2,055 | Supplementary Table S9, B10, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B10, icer_high | 2054709.81704638 |  |
| 1519 | 189,000 | Supplementary Table S9, B11, low | `output/phase2/main/oneway_base.csv` | param_id = B11, low_value | 189000.0 |  |
| 1520 | 283,000 | Supplementary Table S9, B11, high | `output/phase2/main/oneway_base.csv` | param_id = B11, high_value | 283000.0 |  |
| 1521 | 2,052 | Supplementary Table S9, B11, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B11, icer_low | 2052276.49361329 |  |
| 1522 | 2,053 | Supplementary Table S9, B11, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B11, icer_high | 2053233.78101191 |  |
| 1523 | 0.03578 | Supplementary Table S9, B21C, low | `output/phase2/main/oneway_base.csv` | param_id = B21C, low_value | 0.03578 |  |
| 1524 | 0.08438 | Supplementary Table S9, B21C, high | `output/phase2/main/oneway_base.csv` | param_id = B21C, high_value | 0.08438 |  |
| 1525 | 2,053 | Supplementary Table S9, B21C, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B21C, icer_low | 2053126.97846803 |  |
| 1526 | 2,052 | Supplementary Table S9, B21C, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B21C, icer_high | 2052257.32109778 |  |
| 1527 | 0.12636 | Supplementary Table S9, B21P, low | `output/phase2/main/oneway_base.csv` | param_id = B21P, low_value | 0.12636 |  |
| 1528 | 0.17771 | Supplementary Table S9, B21P, high | `output/phase2/main/oneway_base.csv` | param_id = B21P, high_value | 0.17771 |  |
| 1529 | 2,052 | Supplementary Table S9, B21P, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B21P, icer_low | 2052319.59286009 |  |
| 1530 | 2,053 | Supplementary Table S9, B21P, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B21P, icer_high | 2053238.45923792 |  |
| 1531 | 0.00726 | Supplementary Table S9, B22C, low | `output/phase2/main/oneway_base.csv` | param_id = B22C, low_value | 0.00726 |  |
| 1532 | 0.03672 | Supplementary Table S9, B22C, high | `output/phase2/main/oneway_base.csv` | param_id = B22C, high_value | 0.03672 |  |
| 1533 | 2,053 | Supplementary Table S9, B22C, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B22C, icer_low | 2052948.48543772 |  |
| 1534 | 2,052 | Supplementary Table S9, B22C, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B22C, icer_high | 2052417.63401498 |  |
| 1535 | 0.03783 | Supplementary Table S9, B22P, low | `output/phase2/main/oneway_base.csv` | param_id = B22P, low_value | 0.03783 |  |
| 1536 | 0.07037 | Supplementary Table S9, B22P, high | `output/phase2/main/oneway_base.csv` | param_id = B22P, high_value | 0.07037 |  |
| 1537 | 2,052 | Supplementary Table S9, B22P, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B22P, icer_low | 2052493.31548054 |  |
| 1538 | 2,053 | Supplementary Table S9, B22P, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B22P, icer_high | 2053079.66664469 |  |
| 1539 | 0.00000 | Supplementary Table S9, B23C, low | `output/phase2/main/oneway_base.csv` | param_id = B23C, low_value | 0.0 |  |
| 1540 | 0.00944 | Supplementary Table S9, B23C, high | `output/phase2/main/oneway_base.csv` | param_id = B23C, high_value | 0.00944 |  |
| 1541 | 2,053 | Supplementary Table S9, B23C, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B23C, icer_low | 2052755.1373126 |  |
| 1542 | 2,052 | Supplementary Table S9, B23C, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B23C, icer_high | 2051721.98072319 |  |
| 1543 | 0.01567 | Supplementary Table S9, B23P, low | `output/phase2/main/oneway_base.csv` | param_id = B23P, low_value | 0.01567 |  |
| 1544 | 0.03917 | Supplementary Table S9, B23P, high | `output/phase2/main/oneway_base.csv` | param_id = B23P, high_value | 0.03917 |  |
| 1545 | 2,052 | Supplementary Table S9, B23P, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B23P, icer_low | 2051674.91956498 |  |
| 1546 | 2,054 | Supplementary Table S9, B23P, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B23P, icer_high | 2054246.86658312 |  |
| 1547 | 0.00007 | Supplementary Table S9, B24C, low | `output/phase2/main/oneway_base.csv` | param_id = B24C, low_value | 7e-05 |  |
| 1548 | 0.01424 | Supplementary Table S9, B24C, high | `output/phase2/main/oneway_base.csv` | param_id = B24C, high_value | 0.01424 |  |
| 1549 | 2,053 | Supplementary Table S9, B24C, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B24C, icer_low | 2053028.74869751 |  |
| 1550 | 2,051 | Supplementary Table S9, B24C, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B24C, icer_high | 2051477.91936785 |  |
| 1551 | 0.01076 | Supplementary Table S9, B24P, low | `output/phase2/main/oneway_base.csv` | param_id = B24P, low_value | 0.01076 |  |
| 1552 | 0.03140 | Supplementary Table S9, B24P, high | `output/phase2/main/oneway_base.csv` | param_id = B24P, high_value | 0.0314 |  |
| 1553 | 2,052 | Supplementary Table S9, B24P, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B24P, icer_low | 2051835.80305931 |  |
| 1554 | 2,054 | Supplementary Table S9, B24P, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B24P, icer_high | 2054094.73865311 |  |
| 1555 | 0.00062 | Supplementary Table S9, B25C, low | `output/phase2/main/oneway_base.csv` | param_id = B25C, low_value | 0.00062 |  |
| 1556 | 0.01845 | Supplementary Table S9, B25C, high | `output/phase2/main/oneway_base.csv` | param_id = B25C, high_value | 0.01845 |  |
| 1557 | 2,053 | Supplementary Table S9, B25C, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B25C, icer_low | 2052887.73188469 |  |
| 1558 | 2,052 | Supplementary Table S9, B25C, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B25C, icer_high | 2052364.68736691 |  |
| 1559 | 0.00360 | Supplementary Table S9, B25P, low | `output/phase2/main/oneway_base.csv` | param_id = B25P, low_value | 0.0036 |  |
| 1560 | 0.01833 | Supplementary Table S9, B25P, high | `output/phase2/main/oneway_base.csv` | param_id = B25P, high_value | 0.01833 |  |
| 1561 | 2,053 | Supplementary Table S9, B25P, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B25P, icer_low | 2052598.487973 |  |
| 1562 | 2,053 | Supplementary Table S9, B25P, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B25P, icer_high | 2053030.59373559 |  |
| 1563 | 0.00000 | Supplementary Table S9, B26C, low | `output/phase2/main/oneway_base.csv` | param_id = B26C, low_value | 0.0 |  |
| 1564 | 0.00944 | Supplementary Table S9, B26C, high | `output/phase2/main/oneway_base.csv` | param_id = B26C, high_value | 0.00944 |  |
| 1565 | 2,053 | Supplementary Table S9, B26C, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B26C, icer_low | 2052755.1373126 |  |
| 1566 | 2,053 | Supplementary Table S9, B26C, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B26C, icer_high | 2052576.78646746 |  |
| 1567 | 0.00282 | Supplementary Table S9, B26P, low | `output/phase2/main/oneway_base.csv` | param_id = B26P, low_value | 0.00282 |  |
| 1568 | 0.01660 | Supplementary Table S9, B26P, high | `output/phase2/main/oneway_base.csv` | param_id = B26P, high_value | 0.0166 |  |
| 1569 | 2,053 | Supplementary Table S9, B26P, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B26P, icer_low | 2052663.69471827 |  |
| 1570 | 2,053 | Supplementary Table S9, B26P, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B26P, icer_high | 2052924.04160874 |  |
| 1571 | 0.00000 | Supplementary Table S9, B27C, low | `output/phase2/main/oneway_base.csv` | param_id = B27C, low_value | 0.0 |  |
| 1572 | 0.00944 | Supplementary Table S9, B27C, high | `output/phase2/main/oneway_base.csv` | param_id = B27C, high_value | 0.00944 |  |
| 1573 | 2,053 | Supplementary Table S9, B27C, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B27C, icer_low | 2052755.1373126 |  |
| 1574 | 2,053 | Supplementary Table S9, B27C, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B27C, icer_high | 2052576.78646746 |  |
| 1575 | 0.00527 | Supplementary Table S9, B27P, low | `output/phase2/main/oneway_base.csv` | param_id = B27P, low_value | 0.00527 |  |
| 1576 | 0.02171 | Supplementary Table S9, B27P, high | `output/phase2/main/oneway_base.csv` | param_id = B27P, high_value | 0.02171 |  |
| 1577 | 2,053 | Supplementary Table S9, B27P, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B27P, icer_low | 2052637.62224303 |  |
| 1578 | 2,053 | Supplementary Table S9, B27P, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B27P, icer_high | 2052948.22477418 |  |
| 1579 | 0.00007 | Supplementary Table S9, B28C, low | `output/phase2/main/oneway_base.csv` | param_id = B28C, low_value | 7e-05 |  |
| 1580 | 0.01424 | Supplementary Table S9, B28C, high | `output/phase2/main/oneway_base.csv` | param_id = B28C, high_value | 0.01424 |  |
| 1581 | 2,053 | Supplementary Table S9, B28C, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B28C, icer_low | 2053028.74869751 |  |
| 1582 | 2,051 | Supplementary Table S9, B28C, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B28C, icer_high | 2051477.91936785 |  |
| 1583 | 0.03349 | Supplementary Table S9, B28P, low | `output/phase2/main/oneway_base.csv` | param_id = B28P, low_value | 0.03349 |  |
| 1584 | 0.06455 | Supplementary Table S9, B28P, high | `output/phase2/main/oneway_base.csv` | param_id = B28P, high_value | 0.06455 |  |
| 1585 | 2,051 | Supplementary Table S9, B28P, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B28P, icer_low | 2051249.18025007 |  |
| 1586 | 2,055 | Supplementary Table S9, B28P, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B28P, icer_high | 2054648.52809616 |  |
| 1587 | 0.00000 | Supplementary Table S9, B29C, low | `output/phase2/main/oneway_base.csv` | param_id = B29C, low_value | 0.0 |  |
| 1588 | 0.00944 | Supplementary Table S9, B29C, high | `output/phase2/main/oneway_base.csv` | param_id = B29C, high_value | 0.00944 |  |
| 1589 | 2,053 | Supplementary Table S9, B29C, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B29C, icer_low | 2052755.1373126 |  |
| 1590 | 2,052 | Supplementary Table S9, B29C, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B29C, icer_high | 2051721.98072319 |  |
| 1591 | 0.00139 | Supplementary Table S9, B29P, low | `output/phase2/main/oneway_base.csv` | param_id = B29P, low_value | 0.00139 |  |
| 1592 | 0.01303 | Supplementary Table S9, B29P, high | `output/phase2/main/oneway_base.csv` | param_id = B29P, high_value | 0.01303 |  |
| 1593 | 2,052 | Supplementary Table S9, B29P, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B29P, icer_low | 2052348.00357186 |  |
| 1594 | 2,054 | Supplementary Table S9, B29P, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B29P, icer_high | 2053621.93817999 |  |
| 1595 | 0.00007 | Supplementary Table S9, B30C, low | `output/phase2/main/oneway_base.csv` | param_id = B30C, low_value | 7e-05 |  |
| 1596 | 0.01424 | Supplementary Table S9, B30C, high | `output/phase2/main/oneway_base.csv` | param_id = B30C, high_value | 0.01424 |  |
| 1597 | 2,053 | Supplementary Table S9, B30C, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B30C, icer_low | 2053028.74869751 |  |
| 1598 | 2,051 | Supplementary Table S9, B30C, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B30C, icer_high | 2051477.91936785 |  |
| 1599 | 0.01172 | Supplementary Table S9, B30P, low | `output/phase2/main/oneway_base.csv` | param_id = B30P, low_value | 0.01172 |  |
| 1600 | 0.03297 | Supplementary Table S9, B30P, high | `output/phase2/main/oneway_base.csv` | param_id = B30P, high_value | 0.03297 |  |
| 1601 | 2,052 | Supplementary Table S9, B30P, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B30P, icer_low | 2051801.87524758 |  |
| 1602 | 2,054 | Supplementary Table S9, B30P, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B30P, icer_high | 2054127.5720193 |  |
| 1603 | 0.12675 | Supplementary Table S9, B31C, low | `output/phase2/main/oneway_base.csv` | param_id = B31C, low_value | 0.12675 |  |
| 1604 | 0.20240 | Supplementary Table S9, B31C, high | `output/phase2/main/oneway_base.csv` | param_id = B31C, high_value | 0.2024 |  |
| 1605 | 2,057 | Supplementary Table S9, B31C, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B31C, icer_low | 2056607.5856121 |  |
| 1606 | 2,048 | Supplementary Table S9, B31C, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B31C, icer_high | 2048328.10510479 |  |
| 1607 | 0.15737 | Supplementary Table S9, B31P, low | `output/phase2/main/oneway_base.csv` | param_id = B31P, low_value | 0.15737 |  |
| 1608 | 0.21285 | Supplementary Table S9, B31P, high | `output/phase2/main/oneway_base.csv` | param_id = B31P, high_value | 0.21285 |  |
| 1609 | 2,050 | Supplementary Table S9, B31P, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B31P, icer_low | 2049850.47885042 |  |
| 1610 | 2,056 | Supplementary Table S9, B31P, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B31P, icer_high | 2055922.46270429 |  |
| 1611 | 0.886 | Supplementary Table S9, B33C, low | `output/phase2/main/oneway_base.csv` | param_id = B33C, low_value | 0.88599 |  |
| 1612 | 1.086 | Supplementary Table S9, B33C, high | `output/phase2/main/oneway_base.csv` | param_id = B33C, high_value | 1.08559 |  |
| 1613 | 2,053 | Supplementary Table S9, B33C, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B33C, icer_low | 2053237.00016306 |  |
| 1614 | 2,052 | Supplementary Table S9, B33C, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B33C, icer_high | 2052235.58918581 |  |
| 1615 | 0.993 | Supplementary Table S9, B33P, low | `output/phase2/main/oneway_base.csv` | param_id = B33P, low_value | 0.99283 |  |
| 1616 | 1.139 | Supplementary Table S9, B33P, high | `output/phase2/main/oneway_base.csv` | param_id = B33P, high_value | 1.13862 |  |
| 1617 | 2,052 | Supplementary Table S9, B33P, icer_low | `output/phase2/main/oneway_base.csv` | param_id = B33P, icer_low | 2052398.82877006 |  |
| 1618 | 2,053 | Supplementary Table S9, B33P, icer_high | `output/phase2/main/oneway_base.csv` | param_id = B33P, icer_high | 2053130.29034817 |  |
| 1619 | 11,660 | Supplementary Table S9, C01, low | `output/phase2/main/oneway_base.csv` | param_id = C01, low_value | 11660.0 |  |
| 1620 | 24,880 | Supplementary Table S9, C01, high | `output/phase2/main/oneway_base.csv` | param_id = C01, high_value | 24880.0 |  |
| 1621 | 2,727 | Supplementary Table S9, C01, cap_low | `output/phase2/main/oneway_base.csv` | param_id = C01, cap_low | 2726524.35765035 |  |
| 1622 | 2,726 | Supplementary Table S9, C01, cap_high | `output/phase2/main/oneway_base.csv` | param_id = C01, cap_high | 2726277.41642205 |  |
| 1623 | 2,053 | Supplementary Table S9, C01, icer_low | `output/phase2/main/oneway_base.csv` | param_id = C01, icer_low | 2052524.34058291 |  |
| 1624 | 2,053 | Supplementary Table S9, C01, icer_high | `output/phase2/main/oneway_base.csv` | param_id = C01, icer_high | 2052985.93404229 |  |
| 1625 | 10,120 | Supplementary Table S9, C02, low | `output/phase2/main/oneway_base.csv` | param_id = C02, low_value | 10120.0 |  |
| 1626 | 23,340 | Supplementary Table S9, C02, high | `output/phase2/main/oneway_base.csv` | param_id = C02, high_value | 23340.0 |  |
| 1627 | 2,727 | Supplementary Table S9, C02, cap_low | `output/phase2/main/oneway_base.csv` | param_id = C02, cap_low | 2726724.35004204 |  |
| 1628 | 2,726 | Supplementary Table S9, C02, cap_high | `output/phase2/main/oneway_base.csv` | param_id = C02, cap_high | 2726077.42403036 |  |
| 1629 | 2,052 | Supplementary Table S9, C02, icer_low | `output/phase2/main/oneway_base.csv` | param_id = C02, icer_low | 2052088.90337869 |  |
| 1630 | 2,053 | Supplementary Table S9, C02, icer_high | `output/phase2/main/oneway_base.csv` | param_id = C02, icer_high | 2053421.37124651 |  |
| 1631 | 9,350 | Supplementary Table S9, C03, low | `output/phase2/main/oneway_base.csv` | param_id = C03, low_value | 9350.0 |  |
| 1632 | 22,570 | Supplementary Table S9, C03, high | `output/phase2/main/oneway_base.csv` | param_id = C03, high_value | 22570.0 |  |
| 1633 | 2,729 | Supplementary Table S9, C03, cap_low | `output/phase2/main/oneway_base.csv` | param_id = C03, cap_low | 2729327.31496135 |  |
| 1634 | 2,723 | Supplementary Table S9, C03, cap_high | `output/phase2/main/oneway_base.csv` | param_id = C03, cap_high | 2723474.45911105 |  |
| 1635 | 2,046 | Supplementary Table S9, C03, icer_low | `output/phase2/main/oneway_base.csv` | param_id = C03, icer_low | 2045574.51923167 |  |
| 1636 | 2,060 | Supplementary Table S9, C03, icer_high | `output/phase2/main/oneway_base.csv` | param_id = C03, icer_high | 2059935.75539353 |  |
| 1637 | 916,988 | Supplementary Table S9, D01, low | `output/phase2/main/oneway_base.csv` | param_id = D01, low_value | 916987.5 |  |
| 1638 | 1,528,313 | Supplementary Table S9, D01, high | `output/phase2/main/oneway_base.csv` | param_id = D01, high_value | 1528312.5 |  |
| 1639 | 2,724 | Supplementary Table S9, D01, cap_low | `output/phase2/main/oneway_base.csv` | param_id = D01, cap_low | 2724037.1621415 |  |
| 1640 | 2,729 | Supplementary Table S9, D01, cap_high | `output/phase2/main/oneway_base.csv` | param_id = D01, cap_high | 2728764.6119309 |  |
| 1641 | 2,055 | Supplementary Table S9, D01, icer_low | `output/phase2/main/oneway_base.csv` | param_id = D01, icer_low | 2055335.9006584 |  |
| 1642 | 2,050 | Supplementary Table S9, D01, icer_high | `output/phase2/main/oneway_base.csv` | param_id = D01, icer_high | 2050174.3739668 |  |
| 1643 | 2,284 | Supplementary Table S9, D02, low | `output/phase2/main/oneway_base.csv` | param_id = D02, low_value | 2283.75 | 【要確認】D02 |
| 1644 | 3,806 | Supplementary Table S9, D02, high | `output/phase2/main/oneway_base.csv` | param_id = D02, high_value | 3806.25 | 【要確認】D02 |
| 1645 | 2,726 | Supplementary Table S9, D02, cap_low | `output/phase2/main/oneway_base.csv` | param_id = D02, cap_low | 2726202.3232563 | 【要確認】D02 |
| 1646 | 2,727 | Supplementary Table S9, D02, cap_high | `output/phase2/main/oneway_base.csv` | param_id = D02, cap_high | 2726599.4508161 | 【要確認】D02 |
| 1647 | 2,053 | Supplementary Table S9, D02, icer_low | `output/phase2/main/oneway_base.csv` | param_id = D02, icer_low | 2052970.73833184 | 【要確認】D02 |
| 1648 | 2,053 | Supplementary Table S9, D02, icer_high | `output/phase2/main/oneway_base.csv` | param_id = D02, icer_high | 2052539.53629336 | 【要確認】D02 |
| 1649 | 915,446 | Supplementary Table S9, D03, low | `output/phase2/main/oneway_base.csv` | param_id = D03, low_value | 915445.948078572 |  |
| 1650 | 1,416,257 | Supplementary Table S9, D03, high | `output/phase2/main/oneway_base.csv` | param_id = D03, high_value | 1416257.32721429 |  |
| 1651 | 2,379 | Supplementary Table S9, D03, icer_low | `output/phase2/main/oneway_base.csv` | param_id = D03, icer_low | 2379407.59045124 |  |
| 1652 | 1,835 | Supplementary Table S9, D03, icer_high | `output/phase2/main/oneway_base.csv` | param_id = D03, icer_high | 1834986.83522016 |  |
| 1653 | 973,662 | Supplementary Table S9, D03P, low | `output/phase2/main/oneway_base.csv` | param_id = D03P, low_value | 973662.056785714 |  |
| 1654 | 1,781,422 | Supplementary Table S9, D03P, high | `output/phase2/main/oneway_base.csv` | param_id = D03P, high_value | 1781422.34571429 |  |
| 1655 | 2,642 | Supplementary Table S9, D03P, cap_low | `output/phase2/main/oneway_base.csv` | param_id = D03P, cap_low | 2641830.42909583 |  |
| 1656 | 2,783 | Supplementary Table S9, D03P, cap_high | `output/phase2/main/oneway_base.csv` | param_id = D03P, cap_high | 2782781.19232979 |  |
| 1657 | 1,660 | Supplementary Table S9, D03P, icer_low | `output/phase2/main/oneway_base.csv` | param_id = D03P, icer_low | 1659586.0415438 |  |
| 1658 | 2,315 | Supplementary Table S9, D03P, icer_high | `output/phase2/main/oneway_base.csv` | param_id = D03P, icer_high | 2314867.86782513 |  |
| 1659 | 7.77 | Supplementary Table S9, D04, low | `output/phase2/main/oneway_base.csv` | param_id = D04, low_value | 7.77432 |  |
| 1660 | 12.96 | Supplementary Table S9, D04, high | `output/phase2/main/oneway_base.csv` | param_id = D04, high_value | 12.9572 |  |
| 1661 | 2,009 | Supplementary Table S9, D04, icer_low | `output/phase2/main/oneway_base.csv` | param_id = D04, icer_low | 2008654.49156298 |  |
| 1662 | 2,091 | Supplementary Table S9, D04, icer_high | `output/phase2/main/oneway_base.csv` | param_id = D04, icer_high | 2090969.99472693 |  |
| 1663 | 8.13 | Supplementary Table S9, D04P, low | `output/phase2/main/oneway_base.csv` | param_id = D04P, low_value | 8.13 |  |
| 1664 | 13.55 | Supplementary Table S9, D04P, high | `output/phase2/main/oneway_base.csv` | param_id = D04P, high_value | 13.55 |  |
| 1665 | 2,725 | Supplementary Table S9, D04P, cap_low | `output/phase2/main/oneway_base.csv` | param_id = D04P, cap_low | 2724819.29015682 |  |
| 1666 | 2,728 | Supplementary Table S9, D04P, cap_high | `output/phase2/main/oneway_base.csv` | param_id = D04P, cap_high | 2727745.58432353 |  |
| 1667 | 2,045 | Supplementary Table S9, D04P, icer_low | `output/phase2/main/oneway_base.csv` | param_id = D04P, icer_low | 2045292.44939884 |  |
| 1668 | 2,059 | Supplementary Table S9, D04P, icer_high | `output/phase2/main/oneway_base.csv` | param_id = D04P, icer_high | 2059145.72519386 |  |
| 1669 | 1,059,715 | Supplementary Table S9, D05, low | `output/phase2/main/oneway_base.csv` | param_id = D05, low_value | 1059714.95678572 |  |
| 1670 | 1,766,192 | Supplementary Table S9, D05, high | `output/phase2/main/oneway_base.csv` | param_id = D05, high_value | 1766191.59464286 |  |
| 1671 | 2,617 | Supplementary Table S9, D05, cap_low | `output/phase2/main/oneway_base.csv` | param_id = D05, cap_low | 2617103.57684991 |  |
| 1672 | 2,836 | Supplementary Table S9, D05, cap_high | `output/phase2/main/oneway_base.csv` | param_id = D05, cap_high | 2835698.19722251 |  |
| 1673 | 2,274 | Supplementary Table S9, D05, icer_low | `output/phase2/main/oneway_base.csv` | param_id = D05, icer_low | 2274277.79185463 |  |
| 1674 | 1,831 | Supplementary Table S9, D05, icer_high | `output/phase2/main/oneway_base.csv` | param_id = D05, icer_high | 1831232.48277059 |  |
| 1675 | 956,901 | Supplementary Table S9, D06, low | `output/phase2/main/oneway_base.csv` | param_id = D06, low_value | 956901.0 |  |
| 1676 | 1,283,100 | Supplementary Table S9, D06, high | `output/phase2/main/oneway_base.csv` | param_id = D06, high_value | 1283100.0 |  |
| 1677 | 2,723 | Supplementary Table S9, D06, cap_low | `output/phase2/main/oneway_base.csv` | param_id = D06, cap_low | 2723356.75588848 |  |
| 1678 | 2,729 | Supplementary Table S9, D06, cap_high | `output/phase2/main/oneway_base.csv` | param_id = D06, cap_high | 2729445.01818392 |  |
| 1679 | 2,060 | Supplementary Table S9, D06, icer_low | `output/phase2/main/oneway_base.csv` | param_id = D06, icer_low | 2059592.94213924 |  |
| 1680 | 2,046 | Supplementary Table S9, D06, icer_high | `output/phase2/main/oneway_base.csv` | param_id = D06, icer_high | 2045917.33248596 |  |
| 1681 | 0.14895 | Supplementary Table S9, E06, low | `output/phase2/main/oneway_base.csv` | param_id = E06, low_value | 0.14895 |  |
| 1682 | 0.22464 | Supplementary Table S9, E06, high | `output/phase2/main/oneway_base.csv` | param_id = E06, high_value | 0.22464 |  |
| 1683 | 2,727 | Supplementary Table S9, E06, cap_low | `output/phase2/main/oneway_base.csv` | param_id = E06, cap_low | 2726714.7873362 |  |
| 1684 | 2,726 | Supplementary Table S9, E06, cap_high | `output/phase2/main/oneway_base.csv` | param_id = E06, cap_high | 2726047.9584362 |  |
| 1685 | 0.08731 | Supplementary Table S9, E07, low | `output/phase2/main/oneway_base.csv` | param_id = E07, low_value | 0.08731 |  |
| 1686 | 0.14767 | Supplementary Table S9, E07, high | `output/phase2/main/oneway_base.csv` | param_id = E07, high_value | 0.14767 |  |
| 1687 | 2,726 | Supplementary Table S9, E07, cap_low | `output/phase2/main/oneway_base.csv` | param_id = E07, cap_low | 2726157.2024362 |  |
| 1688 | 2,727 | Supplementary Table S9, E07, cap_high | `output/phase2/main/oneway_base.csv` | param_id = E07, cap_high | 2726688.9740362 |  |
| 1689 | 6,540 | Supplementary Table S9, E08, low | `output/phase2/main/oneway_base.csv` | param_id = E08, low_value | 6540.0 |  |
| 1690 | 11,080 | Supplementary Table S9, E08, high | `output/phase2/main/oneway_base.csv` | param_id = E08, high_value | 11080.0 |  |
| 1691 | 2,727 | Supplementary Table S9, E08, cap_low | `output/phase2/main/oneway_base.csv` | param_id = E08, cap_low | 2726558.9017362 |  |
| 1692 | 2,726 | Supplementary Table S9, E08, cap_high | `output/phase2/main/oneway_base.csv` | param_id = E08, cap_high | 2726242.8723362 |  |
| 1693 | 0.00145 | Supplementary Table S9, E09, low | `output/phase2/main/oneway_base.csv` | param_id = E09, low_value | 0.00145 |  |
| 1694 | 0.02035 | Supplementary Table S9, E09, high | `output/phase2/main/oneway_base.csv` | param_id = E09, high_value | 0.02035 |  |
| 1695 | 2,727 | Supplementary Table S9, E09, cap_low | `output/phase2/main/oneway_base.csv` | param_id = E09, cap_low | 2726547.40312108 |  |
| 1696 | 2,726 | Supplementary Table S9, E09, cap_high | `output/phase2/main/oneway_base.csv` | param_id = E09, cap_high | 2726049.35383976 |  |
| 1697 | 0.00005 | Supplementary Table S9, E10, low | `output/phase2/main/oneway_base.csv` | param_id = E10, low_value | 5e-05 |  |
| 1698 | 0.01203 | Supplementary Table S9, E10, high | `output/phase2/main/oneway_base.csv` | param_id = E10, high_value | 0.01203 |  |
| 1699 | 2,726 | Supplementary Table S9, E10, cap_low | `output/phase2/main/oneway_base.csv` | param_id = E10, cap_low | 2726345.0211909 |  |
| 1700 | 2,727 | Supplementary Table S9, E10, cap_high | `output/phase2/main/oneway_base.csv` | param_id = E10, cap_high | 2726660.71592053 |  |
| 1701 | 0.881 | Supplementary Table S9, U01, low | `output/phase2/main/oneway_base.csv` | param_id = U01, low_value | 0.8812 |  |
| 1702 | 0.897 | Supplementary Table S9, U01, high | `output/phase2/main/oneway_base.csv` | param_id = U01, high_value | 0.8968 |  |
| 1703 | 2,726 | Supplementary Table S9, U01, cap_low | `output/phase2/main/oneway_base.csv` | param_id = U01, cap_low | 2726320.6294272 |  |
| 1704 | 2,726 | Supplementary Table S9, U01, cap_high | `output/phase2/main/oneway_base.csv` | param_id = U01, cap_high | 2726481.1446452 |  |
| 1705 | 2,056 | Supplementary Table S9, U01, icer_low | `output/phase2/main/oneway_base.csv` | param_id = U01, icer_low | 2056225.58747783 |  |
| 1706 | 2,049 | Supplementary Table S9, U01, icer_high | `output/phase2/main/oneway_base.csv` | param_id = U01, icer_high | 2049296.38210054 |  |
| 1707 | 0.877 | Supplementary Table S9, U02, low | `output/phase2/main/oneway_base.csv` | param_id = U02, low_value | 0.8772 |  |
| 1708 | 0.897 | Supplementary Table S9, U02, high | `output/phase2/main/oneway_base.csv` | param_id = U02, high_value | 0.8968 |  |
| 1709 | 2,701 | Supplementary Table S9, U02, cap_low | `output/phase2/main/oneway_base.csv` | param_id = U02, cap_low | 2701494.9586612 |  |
| 1710 | 2,751 | Supplementary Table S9, U02, cap_high | `output/phase2/main/oneway_base.csv` | param_id = U02, cap_high | 2751306.81541123 |  |
| 1711 | 2,073 | Supplementary Table S9, U02, icer_low | `output/phase2/main/oneway_base.csv` | param_id = U02, icer_low | 2073207.74137727 |  |
| 1712 | 2,033 | Supplementary Table S9, U02, icer_high | `output/phase2/main/oneway_base.csv` | param_id = U02, icer_high | 2032702.12911736 |  |
| 1713 | 0.787 | Supplementary Table S9, U03, low | `output/phase2/main/oneway_base.csv` | param_id = U03, low_value | 0.7869 |  |
| 1714 | 0.873 | Supplementary Table S9, U03, high | `output/phase2/main/oneway_base.csv` | param_id = U03, high_value | 0.8731 |  |
| 1715 | 2,731 | Supplementary Table S9, U03, cap_low | `output/phase2/main/oneway_base.csv` | param_id = U03, cap_low | 2731085.12289497 |  |
| 1716 | 2,722 | Supplementary Table S9, U03, cap_high | `output/phase2/main/oneway_base.csv` | param_id = U03, cap_high | 2721716.6511776 |  |
| 1717 | 2,051 | Supplementary Table S9, U03, icer_low | `output/phase2/main/oneway_base.csv` | param_id = U03, icer_low | 2050669.1333813 |  |
| 1718 | 2,055 | Supplementary Table S9, U03, icer_high | `output/phase2/main/oneway_base.csv` | param_id = U03, icer_high | 2054845.38946051 |  |
| 1719 | 0.700 | Supplementary Table S9, U04, low | `output/phase2/main/oneway_base.csv` | param_id = U04, low_value | 0.6997 |  |
| 1720 | 0.770 | Supplementary Table S9, U04, high | `output/phase2/main/oneway_base.csv` | param_id = U04, high_value | 0.7703 |  |
| 1721 | 2,734 | Supplementary Table S9, U04, cap_low | `output/phase2/main/oneway_base.csv` | param_id = U04, cap_low | 2733518.41127429 |  |
| 1722 | 2,719 | Supplementary Table S9, U04, cap_high | `output/phase2/main/oneway_base.csv` | param_id = U04, cap_high | 2719283.36279841 |  |
| 1723 | 2,046 | Supplementary Table S9, U04, icer_low | `output/phase2/main/oneway_base.csv` | param_id = U04, icer_low | 2046320.32286524 |  |
| 1724 | 2,059 | Supplementary Table S9, U04, icer_high | `output/phase2/main/oneway_base.csv` | param_id = U04, icer_high | 2059230.5489766 |  |
| 1725 | 0.000 | Supplementary Table S9, U05, low | `output/phase2/main/oneway_base.csv` | param_id = U05, low_value | 0.0 |  |
| 1726 | 0.059 | Supplementary Table S9, U05, high | `output/phase2/main/oneway_base.csv` | param_id = U05, high_value | 0.059 |  |
| 1727 | 2,727 | Supplementary Table S9, U05, cap_low | `output/phase2/main/oneway_base.csv` | param_id = U05, cap_low | 2726528.42981513 |  |
| 1728 | 2,726 | Supplementary Table S9, U05, cap_high | `output/phase2/main/oneway_base.csv` | param_id = U05, cap_high | 2726186.38327167 |  |
| 1729 | 2,052 | Supplementary Table S9, U05, icer_low | `output/phase2/main/oneway_base.csv` | param_id = U05, icer_low | 2052344.56314518 |  |
| 1730 | 2,053 | Supplementary Table S9, U05, icer_high | `output/phase2/main/oneway_base.csv` | param_id = U05, icer_high | 2053446.01899704 |  |
| 1731 | 64 | Supplementary Table S9, footnote | `output/phase2/main/oneway_base.csv` | rows that change either result | 64 |  |
| 1732 | 2,733 | Supplementary Table S10, utility_jp, main, cap 0.85 | `output/phase2/main/sc_util_jp_det_caps.csv` | scenario = utility_jp, comparison = main, axis = hr0, x = 0.85, cap_500 | 2732624.03318908 |  |
| 1733 | 0.989 | Supplementary Table S10, utility_jp, main, cap_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_jp, comparison = main, type = cap_eq_programme, programme = E02, lambda = 5e+06, hr0 | 0.989149149534636 |  |
| 1734 | 1.1 | Supplementary Table S10, utility_jp, main, cap_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_jp, comparison = main, type = cap_eq_programme, programme = E02, lambda = 5e+06: 100 x (1 - hr0) | 1.0850850465364048 |  |
| 1735 | 0.958 | Supplementary Table S10, utility_jp, main, avoided_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_jp, comparison = main, type = avoided_eq_programme, programme = E02, hr0 | 0.957946897629302 |  |
| 1736 | 4.2 | Supplementary Table S10, utility_jp, main, avoided_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_jp, comparison = main, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 4.205310237069804 |  |
| 1737 | 3,451 | Supplementary Table S10, utility_jp, secondary, cap 0.85 | `output/phase2/main/sc_util_jp_det_caps.csv` | scenario = utility_jp, comparison = secondary, axis = hr0, x = 0.85, cap_500 | 3450778.05700699 |  |
| 1738 | 0.991 | Supplementary Table S10, utility_jp, secondary, cap_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_jp, comparison = secondary, type = cap_eq_programme, programme = E02, lambda = 5e+06, hr0 | 0.991358325731865 |  |
| 1739 | 0.9 | Supplementary Table S10, utility_jp, secondary, cap_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_jp, comparison = secondary, type = cap_eq_programme, programme = E02, lambda = 5e+06: 100 x (1 - hr0) | 0.8641674268135002 |  |
| 1740 | 0.966 | Supplementary Table S10, utility_jp, secondary, avoided_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_jp, comparison = secondary, type = avoided_eq_programme, programme = E02, hr0 | 0.96585500798515 |  |
| 1741 | 3.4 | Supplementary Table S10, utility_jp, secondary, avoided_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_jp, comparison = secondary, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 3.4144992014849995 |  |
| 1742 | 2,047 | Supplementary Table S10, utility_jp, ICER | `output/phase2/main/sc_util_jp_det_reference.csv` | scenario = utility_jp, column = base, icer | 2047405.73835191 |  |
| 1743 | 2,638 | Supplementary Table S10, utility_us, main, cap 0.85 | `output/phase2/main/scenario_caps.csv` | scenario = utility_us, comparison = main, axis = hr0, x = 0.85, cap_500 | 2637516.8050404 |  |
| 1744 | 0.989 | Supplementary Table S10, utility_us, main, cap_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_us, comparison = main, type = cap_eq_programme, programme = E02, lambda = 5e+06, hr0 | 0.988754559528051 |  |
| 1745 | 1.1 | Supplementary Table S10, utility_us, main, cap_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_us, comparison = main, type = cap_eq_programme, programme = E02, lambda = 5e+06: 100 x (1 - hr0) | 1.1245440471948975 |  |
| 1746 | 0.958 | Supplementary Table S10, utility_us, main, avoided_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_us, comparison = main, type = avoided_eq_programme, programme = E02, hr0 | 0.957946897629302 |  |
| 1747 | 4.2 | Supplementary Table S10, utility_us, main, avoided_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_us, comparison = main, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 4.205310237069804 |  |
| 1748 | 3,330 | Supplementary Table S10, utility_us, secondary, cap 0.85 | `output/phase2/main/scenario_caps.csv` | scenario = utility_us, comparison = secondary, axis = hr0, x = 0.85, cap_500 | 3330069.97040045 |  |
| 1749 | 0.991 | Supplementary Table S10, utility_us, secondary, cap_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_us, comparison = secondary, type = cap_eq_programme, programme = E02, lambda = 5e+06, hr0 | 0.991042291593741 |  |
| 1750 | 0.9 | Supplementary Table S10, utility_us, secondary, cap_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_us, comparison = secondary, type = cap_eq_programme, programme = E02, lambda = 5e+06: 100 x (1 - hr0) | 0.895770840625898 |  |
| 1751 | 0.966 | Supplementary Table S10, utility_us, secondary, avoided_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_us, comparison = secondary, type = avoided_eq_programme, programme = E02, hr0 | 0.96585500798515 |  |
| 1752 | 3.4 | Supplementary Table S10, utility_us, secondary, avoided_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_us, comparison = secondary, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 3.4144992014849995 |  |
| 1753 | 2,154 | Supplementary Table S10, utility_us, ICER | `output/phase2/main/scenario_reference.csv` | scenario = utility_us, column = base, icer | 2153680.01619112 |  |
| 1754 | 2,673 | Supplementary Table S10, utility_uk, main, cap 0.85 | `output/phase2/main/scenario_caps.csv` | scenario = utility_uk, comparison = main, axis = hr0, x = 0.85, cap_500 | 2673461.69326432 |  |
| 1755 | 0.989 | Supplementary Table S10, utility_uk, main, cap_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_uk, comparison = main, type = cap_eq_programme, programme = E02, lambda = 5e+06, hr0 | 0.988908395311631 |  |
| 1756 | 1.1 | Supplementary Table S10, utility_uk, main, cap_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_uk, comparison = main, type = cap_eq_programme, programme = E02, lambda = 5e+06: 100 x (1 - hr0) | 1.1091604688369006 |  |
| 1757 | 0.958 | Supplementary Table S10, utility_uk, main, avoided_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_uk, comparison = main, type = avoided_eq_programme, programme = E02, hr0 | 0.957946897629302 |  |
| 1758 | 4.2 | Supplementary Table S10, utility_uk, main, avoided_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_uk, comparison = main, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 4.205310237069804 |  |
| 1759 | 3,376 | Supplementary Table S10, utility_uk, secondary, cap 0.85 | `output/phase2/main/scenario_caps.csv` | scenario = utility_uk, comparison = secondary, axis = hr0, x = 0.85, cap_500 | 3375680.39907373 |  |
| 1760 | 0.991 | Supplementary Table S10, utility_uk, secondary, cap_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_uk, comparison = secondary, type = cap_eq_programme, programme = E02, lambda = 5e+06, hr0 | 0.991165510166977 |  |
| 1761 | 0.9 | Supplementary Table S10, utility_uk, secondary, cap_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_uk, comparison = secondary, type = cap_eq_programme, programme = E02, lambda = 5e+06: 100 x (1 - hr0) | 0.883448983302304 |  |
| 1762 | 0.966 | Supplementary Table S10, utility_uk, secondary, avoided_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_uk, comparison = secondary, type = avoided_eq_programme, programme = E02, hr0 | 0.96585500798515 |  |
| 1763 | 3.4 | Supplementary Table S10, utility_uk, secondary, avoided_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_uk, comparison = secondary, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 3.4144992014849995 |  |
| 1764 | 2,111 | Supplementary Table S10, utility_uk, ICER | `output/phase2/main/scenario_reference.csv` | scenario = utility_uk, column = base, icer | 2111001.68956341 |  |
| 1765 | 2,518 | Supplementary Table S10, utility_au, main, cap 0.85 | `output/phase2/main/scenario_caps.csv` | scenario = utility_au, comparison = main, axis = hr0, x = 0.85, cap_500 | 2517692.14651729 |  |
| 1766 | 0.988 | Supplementary Table S10, utility_au, main, cap_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_au, comparison = main, type = cap_eq_programme, programme = E02, lambda = 5e+06, hr0 | 0.988218449391632 |  |
| 1767 | 1.2 | Supplementary Table S10, utility_au, main, cap_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_au, comparison = main, type = cap_eq_programme, programme = E02, lambda = 5e+06: 100 x (1 - hr0) | 1.1781550608368052 |  |
| 1768 | 0.958 | Supplementary Table S10, utility_au, main, avoided_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_au, comparison = main, type = avoided_eq_programme, programme = E02, hr0 | 0.957946897629302 |  |
| 1769 | 4.2 | Supplementary Table S10, utility_au, main, avoided_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_au, comparison = main, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 4.205310237069804 |  |
| 1770 | 3,178 | Supplementary Table S10, utility_au, secondary, cap 0.85 | `output/phase2/main/scenario_caps.csv` | scenario = utility_au, comparison = secondary, axis = hr0, x = 0.85, cap_500 | 3177744.28053289 |  |
| 1771 | 0.991 | Supplementary Table S10, utility_au, secondary, cap_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_au, comparison = secondary, type = cap_eq_programme, programme = E02, lambda = 5e+06, hr0 | 0.990612032896817 |  |
| 1772 | 0.9 | Supplementary Table S10, utility_au, secondary, cap_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_au, comparison = secondary, type = cap_eq_programme, programme = E02, lambda = 5e+06: 100 x (1 - hr0) | 0.9387967103183015 |  |
| 1773 | 0.966 | Supplementary Table S10, utility_au, secondary, avoided_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = utility_au, comparison = secondary, type = avoided_eq_programme, programme = E02, hr0 | 0.96585500798515 |  |
| 1774 | 3.4 | Supplementary Table S10, utility_au, secondary, avoided_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = utility_au, comparison = secondary, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 3.4144992014849995 |  |
| 1775 | 2,301 | Supplementary Table S10, utility_au, ICER | `output/phase2/main/scenario_reference.csv` | scenario = utility_au, column = base, icer | 2301205.56784615 |  |
| 1776 | 2,726 | Supplementary Table S10, elmore, main, cap 0.85 | `output/phase2/main/scenario_caps.csv` | scenario = elmore, comparison = main, axis = hr0, x = 0.85, cap_500 | 2726400.88703615 |  |
| 1777 | 0.989 | Supplementary Table S10, elmore, main, cap_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = elmore, comparison = main, type = cap_eq_programme, programme = E02, lambda = 5e+06, hr0 | 0.98912440993811 |  |
| 1778 | 1.1 | Supplementary Table S10, elmore, main, cap_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = elmore, comparison = main, type = cap_eq_programme, programme = E02, lambda = 5e+06: 100 x (1 - hr0) | 1.0875590061889984 |  |
| 1779 | 0.958 | Supplementary Table S10, elmore, main, avoided_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = elmore, comparison = main, type = avoided_eq_programme, programme = E02, hr0 | 0.957946897629303 |  |
| 1780 | 4.2 | Supplementary Table S10, elmore, main, avoided_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = elmore, comparison = main, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 4.205310237069703 |  |
| 1781 | 3,443 | Supplementary Table S10, elmore, secondary, cap 0.85 | `output/phase2/main/scenario_caps.csv` | scenario = elmore, comparison = secondary, axis = hr0, x = 0.85, cap_500 | 3442903.61500287 |  |
| 1782 | 0.991 | Supplementary Table S10, elmore, secondary, cap_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = elmore, comparison = secondary, type = cap_eq_programme, programme = E02, lambda = 5e+06, hr0 | 0.991338575633033 |  |
| 1783 | 0.9 | Supplementary Table S10, elmore, secondary, cap_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = elmore, comparison = secondary, type = cap_eq_programme, programme = E02, lambda = 5e+06: 100 x (1 - hr0) | 0.8661424366967041 |  |
| 1784 | 0.966 | Supplementary Table S10, elmore, secondary, avoided_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = elmore, comparison = secondary, type = avoided_eq_programme, programme = E02, hr0 | 0.965855009130932 |  |
| 1785 | 3.4 | Supplementary Table S10, elmore, secondary, avoided_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = elmore, comparison = secondary, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 3.414499086906797 |  |
| 1786 | 2,082 | Supplementary Table S10, elmore, ICER | `output/phase2/main/scenario_reference.csv` | scenario = elmore, column = base, icer | 2081860.29392172 |  |
| 1787 | 2,413 | Supplementary Table S10, sjp, main, cap 0.85 | `output/phase2/main/scenario_caps.csv` | scenario = sjp, comparison = main, axis = hr0, x = 0.85, cap_500 | 2413307.87500617 | 【要確認】S-JP 依赖 F01P |
| 1788 | 0.988 | Supplementary Table S10, sjp, main, cap_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = sjp, comparison = main, type = cap_eq_programme, programme = E02, lambda = 5e+06, hr0 | 0.987778588446373 | 【要確認】S-JP 依赖 F01P |
| 1789 | 1.2 | Supplementary Table S10, sjp, main, cap_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = sjp, comparison = main, type = cap_eq_programme, programme = E02, lambda = 5e+06: 100 x (1 - hr0) | 1.2221411553626993 | 【要確認】S-JP 依赖 F01P |
| 1790 | 0.953 | Supplementary Table S10, sjp, main, avoided_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = sjp, comparison = main, type = avoided_eq_programme, programme = E02, hr0 | 0.953107568244506 | 【要確認】S-JP 依赖 F01P |
| 1791 | 4.7 | Supplementary Table S10, sjp, main, avoided_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = sjp, comparison = main, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 4.689243175549396 | 【要確認】S-JP 依赖 F01P |
| 1792 | 2,893 | Supplementary Table S10, sjp, secondary, cap 0.85 | `output/phase2/main/scenario_caps.csv` | scenario = sjp, comparison = secondary, axis = hr0, x = 0.85, cap_500 | 2893035.43685527 | 【要確認】S-JP 依赖 F01P |
| 1793 | 0.990 | Supplementary Table S10, sjp, secondary, cap_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = sjp, comparison = secondary, type = cap_eq_programme, programme = E02, lambda = 5e+06, hr0 | 0.989795551244954 | 【要確認】S-JP 依赖 F01P |
| 1794 | 1.0 | Supplementary Table S10, sjp, secondary, cap_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = sjp, comparison = secondary, type = cap_eq_programme, programme = E02, lambda = 5e+06: 100 x (1 - hr0) | 1.0204448755046003 | 【要確認】S-JP 依赖 F01P |
| 1795 | 0.960 | Supplementary Table S10, sjp, secondary, avoided_eq_programme | `output/phase2/main/sc_crossings.csv` | scenario = sjp, comparison = secondary, type = avoided_eq_programme, programme = E02, hr0 | 0.959943094567255 | 【要確認】S-JP 依赖 F01P |
| 1796 | 4.0 | Supplementary Table S10, sjp, secondary, avoided_eq_programme, reduction % | `output/phase2/main/sc_crossings.csv` | scenario = sjp, comparison = secondary, type = avoided_eq_programme, programme = E02: 100 x (1 - hr0) | 4.005690543274499 | 【要確認】S-JP 依赖 F01P |
| 1797 | 3,044 | Supplementary Table S10, sjp, ICER | `output/phase2/main/scenario_reference.csv` | scenario = sjp, column = base, icer | 3044470.14663246 | 【要確認】S-JP 依赖 F01P |
| 1798 | 0.89 | Supplementary Table S10, footnote | `input/params/sources_utility/utilities_scenario_jp.csv` | param_id = U01, value | 0.89 |  |
| 1799 | 0.742 | Supplementary Table S10, footnote | `input/params/sources_utility/utilities_scenario_jp.csv` | param_id = U04, value | 0.742 |  |

## 5. 补充图（supplement 中的 Supplementary Fig. S1、S2）

| # | 显示 | 位置 | 来源文件 | 来源中的位置 | 原始值 | 暂定 |
|---|---|---|---|---|---|---|
| 1 | curves | Supplementary Fig. S1a, KM and 95% CI | `output/phase1/calibration_curves.csv` | arm, month, km, km_lo, km_hi (reconstructed OS, KEYNOTE-522 2024 Fig. 1A) | see file |  |
| 2 | curves | Supplementary Fig. S1a, model OS | `output/phase1/calibration_curves.csv` | arm, month, after (engine OS, round 15) | see file |  |
| 3 | curves | Supplementary Fig. S1b, KM and 95% CI | `data/ipd/K24_F2A_EFS_pembro.csv; data/ipd/K24_F2A_EFS_placebo.csv` | time (months), status; Kaplan-Meier with log-transformed Greenwood 95% CI computed in make_figures.py | see files |  |
| 4 | curves | Supplementary Fig. S1b, model EFS | `output/phase1/engine_curves.csv` | arm = pembro / chemo, pcr = all, scenario = base, time x 12, EFS | see file |  |
| 5 | 4 points | Supplementary Fig. S1a and b, final analysis 7-year estimates | `output/phase1/calibration_final7y.csv` | id = os7_pembro, os7_placebo, efs7_pembro, efs7_placebo: value, ci95_lo, ci95_hi (month 84) | see file |  |
| 6 | 59 | Supplementary Fig. S2 legend (number of inputs that changed the result) | `output/phase2/main/oneway_base.csv` | rows with |icer_high - icer_low| > 1e-6 x icer_base (same rule as R/23_phase2b_report.R tornado()) | 59 |  |
| 7 | 20 | Supplementary Fig. S2 legend (number of inputs shown) | `output/phase2/main/oneway_base.csv` | the 20 widest rows (R/23_phase2b_report.R tornado(top = 20)) | 20 |  |
| 8 | 20 rows | Supplementary Fig. S2, bars | `output/phase2/main/oneway_base.csv` | param_id, icer_low, icer_high, icer_base / 1,000 | see file |  |

## 6. 暂定值（【要確認】）

入力表 v10 中备考为【要確認】、并在表图中显示（或直接由其算出）的值：E03（远程低价方案费用）、D02（局部区域复发后的月额）与 F01P（S-JP 情景）。其余【要確認】行（B03、B04、B07–B10）只在 Supplementary Table S1 中作为输入列出。

| 显示 | 位置 | 标记 |
|---|---|---|
| 11,260 | Table 1, exercise program | 【要確認】E03 |
| 0.997 | Table 2, Panel A, avoided = E03, main | 【要確認】E03 |
| 0.3 | Table 2, Panel A, avoided = E03, main, reduction % | 【要確認】E03 |
| 0.998 | Table 2, Panel A, avoided = E03, secondary | 【要確認】E03 |
| 0.2 | Table 2, Panel A, avoided = E03, secondary, reduction % | 【要確認】E03 |
| 4,990 | Table 3, sjp, total | 【要確認】S-JP 依赖 F01P |
| 1.639 | Table 3, sjp, QALY | 【要確認】S-JP 依赖 F01P |
| 3,044 | Table 3, sjp, ICER | 【要確認】S-JP 依赖 F01P |
| line | Fig. 2, horizontal line E03 | 【要確認】E03 |
| 21 rows | Fig. 3, bars | 【要確認】含 D02 的一行 |
| 3,045 | Supplementary Table S1, Panel B, D02, base | 【要確認】D02 |
| 2,284 | Supplementary Table S1, Panel B, D02, low | 【要確認】D02 |
| 3,806 | Supplementary Table S1, Panel B, D02, high | 【要確認】D02 |
| 61.46 | Supplementary Table S1, Panel B, D02, p1 | 【要確認】D02 |
| 49.54 | Supplementary Table S1, Panel B, D02, p2 | 【要確認】D02 |
| 11,260 | Supplementary Table S1, Panel B, E03, base | 【要確認】E03 |
| 8,445 | Supplementary Table S1, Panel B, E03, low | 【要確認】E03 |
| 14,075 | Supplementary Table S1, Panel B, E03, high | 【要確認】E03 |
| 61.46 | Supplementary Table S1, Panel B, E03, p1 | 【要確認】E03 |
| 183.2 | Supplementary Table S1, Panel B, E03, p2 | 【要確認】E03 |
| 0.50000 | Supplementary Table S1, Panel B, F01P, base | 【要確認】S-JP 依赖 F01P |
| 0.05000 | Supplementary Table S1, Panel B, F01P, low | 【要確認】S-JP 依赖 F01P |
| 0.90000 | Supplementary Table S1, Panel B, F01P, high | 【要確認】S-JP 依赖 F01P |
| −690 | Supplementary Table S5, total_with_E03, d_base | 【要確認】E03 |
| −645 | Supplementary Table S5, total_with_E03, d_kext | 【要確認】E03 |
| 2,284 | Supplementary Table S9, D02, low | 【要確認】D02 |
| 3,806 | Supplementary Table S9, D02, high | 【要確認】D02 |
| 2,726 | Supplementary Table S9, D02, cap_low | 【要確認】D02 |
| 2,727 | Supplementary Table S9, D02, cap_high | 【要確認】D02 |
| 2,053 | Supplementary Table S9, D02, icer_low | 【要確認】D02 |
| 2,053 | Supplementary Table S9, D02, icer_high | 【要確認】D02 |
| 2,413 | Supplementary Table S10, sjp, main, cap 0.85 | 【要確認】S-JP 依赖 F01P |
| 0.988 | Supplementary Table S10, sjp, main, cap_eq_programme | 【要確認】S-JP 依赖 F01P |
| 1.2 | Supplementary Table S10, sjp, main, cap_eq_programme, reduction % | 【要確認】S-JP 依赖 F01P |
| 0.953 | Supplementary Table S10, sjp, main, avoided_eq_programme | 【要確認】S-JP 依赖 F01P |
| 4.7 | Supplementary Table S10, sjp, main, avoided_eq_programme, reduction % | 【要確認】S-JP 依赖 F01P |
| 2,893 | Supplementary Table S10, sjp, secondary, cap 0.85 | 【要確認】S-JP 依赖 F01P |
| 0.990 | Supplementary Table S10, sjp, secondary, cap_eq_programme | 【要確認】S-JP 依赖 F01P |
| 1.0 | Supplementary Table S10, sjp, secondary, cap_eq_programme, reduction % | 【要確認】S-JP 依赖 F01P |
| 0.960 | Supplementary Table S10, sjp, secondary, avoided_eq_programme | 【要確認】S-JP 依赖 F01P |
| 4.0 | Supplementary Table S10, sjp, secondary, avoided_eq_programme, reduction % | 【要確認】S-JP 依赖 F01P |
| 3,044 | Supplementary Table S10, sjp, ICER | 【要確認】S-JP 依赖 F01P |

## 7. 编号与定义中的数字（不是结果）

| 显示 | 位置 | 说明 |
|---|---|---|
| 2.5 | Table 1, uncertainty | UI percentile (docs/analysis_plan_phase2.md line 35) |
| 97.5 | Table 1, uncertainty | UI percentile (docs/analysis_plan_phase2.md line 35) |
| 2026 | Table 1, footnotes | price year, as in the Prices row |
| 5 | Table 1, footnotes | EQ-5D instrument name (EuroQol 5-dimension) |
| 3 | Table 1, footnotes | 3-year CHALLENGE program, as in the Reference value row |
| 6 | Table 1, footnotes | 6 months of neoadjuvant therapy, as in the Exercise program row |
| 2024 | Table 1, footnotes | currency year of the CHALLENGE cost analysis (parameters_v10.xlsx E01 column 価格の年度: 2024年（CAD）) |
| 1.00 | Table 1, footnotes | no-effect value of the HR, as in the Effect on recurrence row |
| 4 | Table 1, source column | name of the trial analysis (interim analysis 4, IA4) |
| 0.85 | Table 2, Panels B and C row label | recurrence HR of the base-case comparison row (Supplementary Table S4 grid point) |
| 49 | Table 2, footnote | starting age (Table 1) |
| 5 | Table 2, title/footnote | JPY 5 million per QALY threshold (analysis plan section 2: λ = 500 万日元/QALY) / 5-year base-case effect duration (Table 1) |
| 2026 | Table 2, footnote | price year (Table 1) |
| 2 | Table 2, footnote | discount rate (Table 1) |
| 1,000 | Table 2, footnote/header | number of PSA samples (Table 1) or the JPY 1,000 unit |
| 2.5 | Table 2, footnote | percentile definition of the UI (Table 1) |
| 97.5 | Table 2, footnote | percentile definition of the UI (Table 1) |
| 95 | Table 2, footnote | 95% UI |
| 1.00 | Table 2, footnote | no-effect value of the HR (Table 1) |
| 100 | Table 2, footnote | reduction = 100 x (1 - HR) |
| 1 | Table 2, footnote | reduction = 100 x (1 - HR) |
| 5 | Table 3, title/footnotes | JPY 5 million threshold |
| 7.5 | Table 3, title/footnotes | JPY 7.5 million threshold (analysis plan section 1) |
| 1,000 | Table 3, title/footnotes | JPY 1,000 unit / 1,000 PSA samples |
| 2.5 | Table 3, title/footnotes | UI percentile |
| 97.5 | Table 3, title/footnotes | UI percentile |
| 95 | Table 3, title/footnotes | 95% UI |
| 2026 | Table 3, title/footnotes | price year |
| 2 | Table 3, title/footnotes | discount rate |
| 0.70 | Table 3, title/footnotes | lower end of the HR range (Table 1) |
| 1.00 | Table 3, title/footnotes | upper end of the HR range (Table 1) |
| 0 | Table 3, title/footnotes | lower end of the pCR range in Table 1 |
| 10 | Table 3, title/footnotes | upper end of the pCR range in Table 1 |
| 0.5 | Table 3, title/footnotes | multiplier in Table 1 |
| 49 | Table 3, title/footnotes | starting age (Table 1) |
| 7 | Fig. 1, box text | surgery at month 7 (docs/model_spec.md line 10) |
| 18 | Fig. 1, box text | early distant recurrence within 18 months of randomization (docs/model_spec.md line 19) |
| 0.72 | Fig. 2a, vertical line label | CHALLENGE DFS HR (input/papers/CHALLENGE.pdf p.7; docs/analysis_plan_phase2.md line 22) |
| 95 | Fig. 2 legend | 95% UI |
| 25 | Fig. 3, labels | ±25% range rule (docs/model_spec.md section 6) |
| 1 | figure legends | 1-month cycles (Table 1) |
| 49 | figure legends | starting age (Table 1) |
| 100 | figure legends | time horizon (Table 1) |
| 7 | figure legends | surgery month (Table 1) |
| 18 | figure legends | early recurrence cut-off (Table 1) |
| 0.70 | figure legends | HR range (Table 1) |
| 1.00 | figure legends | HR range (Table 1) |
| 0.95 | figure legends | zoom range lower end (Fig. 2b axis; Supplementary Table S4 grid point) |
| 5 | figure legends | threshold JPY 5 million / 5-year effect duration (Table 1) |
| 95 | figure legends | 95% UI |
| 0.72 | figure legends | CHALLENGE HR (Table 1) |
| 3 | figure legends | 3-year CHALLENGE program (Table 1) |
| 2026 | figure legends | price year |
| 2 | figure legends | discount rate |
| 2.5 | figure legends | UI percentile |
| 97.5 | figure legends | UI percentile |
| 1,000 | figure legends | PSA samples / JPY 1,000 unit |
| 0.85 | figure legends | HR of the one-way analysis (Table 2 base-case rows) |
| 25 | figure legends | range rule ±25% (docs/model_spec.md section 6) |
| 75 | figure legends | drug-price rule: lower bound 0.75 x base (docs/model_spec.md section 6) |
| 18 | Supplementary Table S1 | early distant recurrence cut-off (Table 1) |
| 49 | Supplementary Table S1 | definition or name (Table 1; report years) |
| 7 | Supplementary Table S1 | definition or name (Table 1; report years) |
| 2024 | Supplementary Table S1 | definition or name (Table 1; report years) |
| 2022 | Supplementary Table S1 | definition or name (Table 1; report years) |
| 2025 | Supplementary Table S1 | definition or name (Table 1; report years) |
| 4 | Supplementary Table S1 | definition or name (Table 1; report years) |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 14 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 14 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 14 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2023 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 33 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 5550 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2025 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 32 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 857 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2025 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 32 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 857 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2025 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 32 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 857 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2025 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 32 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 857 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2025 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 32 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 857 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2025 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 32 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 857 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 003820 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 0110 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 257879 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 003820 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 0110 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 257879 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 003820 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 0110 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 257879 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 003820 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 0110 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 257879 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 003820 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 0110 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 257879 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 003820 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 0110 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 257879 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 003820 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 0110 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 257879 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 003820 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 0110 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 257879 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 386 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 556 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2025 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2020 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2025 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2020 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2025 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2020 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2025 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2020 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2022 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2018 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 44 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2130 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2024 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2024 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2025 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 393 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 13 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2025 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 393 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 13 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1056 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2025 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 393 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 13 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1056 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2025 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 393 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 13 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1056 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2025 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 393 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 13 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1056 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 216 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 27 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 135 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 329 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2017 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 376 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2147 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2021 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 14 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 96 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.3892 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2017 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 376 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2147 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1056 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2026 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1016 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2024 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 8 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 1 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 91 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 37999854 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2024 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 8 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 1 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 91 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 37999854 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2024 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 8 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 1 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 91 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 37999854 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2024 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 8 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 1 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 91 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 37999854 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 2024 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 8 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 1 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 91 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 10.1007 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 37999854 | Supplementary Table S1, Panel B source column | bibliographic detail (volume, pages, DOI, PMID or year) of the cited source |
| 25 | Supplementary Table S1, Panel B labels | ±25% rule |
| 75 | Supplementary Table S1, Panel B labels | drug price rule |
| 12.5 | Supplementary Table S1, Panel B labels | U05 duration (Table 1) |
| 6 | Supplementary Table S1, Panel B labels | 6-month program (Table 1) |
| 3 | Supplementary Table S1, Panel B labels | 3 months of end-of-life care (Table 1) |
| 12 | Supplementary Table S1, Panel B labels | 12 weeks (A01) |
| 4 | Supplementary Table S1, Panel B labels | 4 cycles (A02) |
| 1 | Supplementary Table S1, Panel B labels | type 1 diabetes / years 1 to 2 |
| 2 | Supplementary Table S1, Panel B labels | years 1 to 2 |
| 5 | Supplementary Table S1, Panel B labels | years 3 to 5 / EQ-5D |
| 2026 | Supplementary Table S1, Panel B labels | fiscal year / report years |
| 2017 | Supplementary Table S1, Panel B labels | citation year |
| 2020 | Supplementary Table S1, Panel B labels | citation year |
| 2007 | Supplementary Table S1, Panel B labels | citation year |
| 2018 | Supplementary Table S1, Panel B labels | citation year |
| 2021 | Supplementary Table S1, Panel B labels | citation year |
| 2023 | Supplementary Table S1, Panel B labels | guideline year |
| 2024 | Supplementary Table S1, Panel B labels | PPP year |
| 2025 | Supplementary Table S1, Panel B labels | citation year |
| 95 | Supplementary Table S2 | definitions, cut-off date and percentiles |
| 99.5 | Supplementary Table S2 | definitions, cut-off date and percentiles |
| 5 | Supplementary Table S2 | definitions, cut-off date and percentiles |
| 7 | Supplementary Table S2 | definitions, cut-off date and percentiles |
| 10 | Supplementary Table S2 | definitions, cut-off date and percentiles |
| 20 | Supplementary Table S2 | definitions, cut-off date and percentiles |
| 2.5 | Supplementary Table S2 | definitions, cut-off date and percentiles |
| 97.5 | Supplementary Table S2 | definitions, cut-off date and percentiles |
| 1,000 | Supplementary Table S2 | definitions, cut-off date and percentiles |
| 2024 | Supplementary Table S2 | definitions, cut-off date and percentiles |
| 14 | Supplementary Table S2 | definitions, cut-off date and percentiles |
| 2025 | Supplementary Table S2 | definitions, cut-off date and percentiles |
| 4 | Supplementary Table S2 | definitions, cut-off date and percentiles |
| 5 | Supplementary Table S4 | threshold, percentiles, price year, discount rate |
| 7.5 | Supplementary Table S4 | threshold, percentiles, price year, discount rate |
| 95 | Supplementary Table S4 | threshold, percentiles, price year, discount rate |
| 2.5 | Supplementary Table S4 | threshold, percentiles, price year, discount rate |
| 97.5 | Supplementary Table S4 | threshold, percentiles, price year, discount rate |
| 1,000 | Supplementary Table S4 | threshold, percentiles, price year, discount rate |
| 2026 | Supplementary Table S4 | threshold, percentiles, price year, discount rate |
| 2 | Supplementary Table S4 | threshold, percentiles, price year, discount rate |
| 49 | Supplementary Table S4 | threshold, percentiles, price year, discount rate |
| 0.85 | Supplementary Table S5 | definitions |
| 5 | Supplementary Table S5 | definitions |
| 2026 | Supplementary Table S5 | definitions |
| 2 | Supplementary Table S5 | definitions |
| 49 | Supplementary Table S5 | definitions |
| 1,000 | Supplementary Table S5 | definitions |
| 0.700 | Supplementary Table S6 | HR grid point (Supplementary Table S4) |
| 0.725 | Supplementary Table S6 | HR grid point (Supplementary Table S4) |
| 0.750 | Supplementary Table S6 | HR grid point (Supplementary Table S4) |
| 0.775 | Supplementary Table S6 | HR grid point (Supplementary Table S4) |
| 0.800 | Supplementary Table S6 | HR grid point (Supplementary Table S4) |
| 0.825 | Supplementary Table S6 | HR grid point (Supplementary Table S4) |
| 0.850 | Supplementary Table S6 | HR grid point (Supplementary Table S4) |
| 0.875 | Supplementary Table S6 | HR grid point (Supplementary Table S4) |
| 0.900 | Supplementary Table S6 | HR grid point (Supplementary Table S4) |
| 0.925 | Supplementary Table S6 | HR grid point (Supplementary Table S4) |
| 0.950 | Supplementary Table S6 | HR grid point (Supplementary Table S4) |
| 0.975 | Supplementary Table S6 | HR grid point (Supplementary Table S4) |
| 1.000 | Supplementary Table S6 | HR grid point (Supplementary Table S4) |
| 5 | Supplementary Table S6 | definitions |
| 7.5 | Supplementary Table S6 | definitions |
| 1 | Supplementary Table S6 | definitions |
| 30 | Supplementary Table S6 | definitions |
| 2026 | Supplementary Table S6 | definitions |
| 2 | Supplementary Table S6 | definitions |
| 49 | Supplementary Table S6 | definitions |
| 0.95 | Supplementary Table S7 | definitions |
| 0.90 | Supplementary Table S7 | definitions |
| 0.85 | Supplementary Table S7 | definitions |
| 5 | Supplementary Table S7 | definitions |
| 2024 | Supplementary Table S7 | definitions |
| 2023 | Supplementary Table S7 | definitions |
| 55 | Supplementary Table S7 | definitions |
| 2026 | Supplementary Table S7 | definitions |
| 2 | Supplementary Table S7 | definitions |
| 95 | Supplementary Table S7 | definitions |
| 2.5 | Supplementary Table S7 | definitions |
| 97.5 | Supplementary Table S7 | definitions |
| 1,000 | Supplementary Table S7 | definitions |
| 100 | Supplementary Table S8 | definitions |
| 5 | Supplementary Table S8 | definitions |
| 7.5 | Supplementary Table S8 | definitions |
| 95 | Supplementary Table S8 | definitions |
| 2.5 | Supplementary Table S8 | definitions |
| 97.5 | Supplementary Table S8 | definitions |
| 1,000 | Supplementary Table S8 | definitions |
| 2026 | Supplementary Table S8 | definitions |
| 2 | Supplementary Table S8 | definitions |
| 49 | Supplementary Table S8 | definitions |
| 0.85 | Supplementary Table S9 | definitions |
| 5 | Supplementary Table S9 | definitions |
| 25 | Supplementary Table S9 | definitions |
| 75 | Supplementary Table S9 | definitions |
| 2026 | Supplementary Table S9 | definitions |
| 2 | Supplementary Table S9 | definitions |
| 49 | Supplementary Table S9 | definitions |
| 1,000 | Supplementary Table S9 | definitions |
| 12 | Supplementary Table S9 | definitions |
| 4 | Supplementary Table S9 | definitions |
| 1 | Supplementary Table S9 | definitions |
| 3 | Supplementary Table S9 | definitions |
| 6 | Supplementary Table S9 | definitions |
| 12.5 | Supplementary Table S9 | definitions |
| 0.85 | Supplementary Table S10 | definitions and citation years |
| 5 | Supplementary Table S10 | definitions and citation years |
| 100 | Supplementary Table S10 | definitions and citation years |
| 1 | Supplementary Table S10 | definitions and citation years |
| 2026 | Supplementary Table S10 | definitions and citation years |
| 2 | Supplementary Table S10 | definitions and citation years |
| 49 | Supplementary Table S10 | definitions and citation years |
| 3 | Supplementary Table S10 | definitions and citation years |
| 26 | Supplementary Table S10 | definitions and citation years |
| 1,000 | Supplementary Table S10 | definitions and citation years |
| 2024 | supplementary figure legends | definitions |
| 7 | supplementary figure legends | definitions |
| 95 | supplementary figure legends | definitions |
| 25 | supplementary figure legends | definitions |
| 75 | supplementary figure legends | definitions |
| 2026 | supplementary figure legends | definitions |
| 2 | supplementary figure legends | definitions |
| 49 | supplementary figure legends | definitions |
| 1,000 | supplementary figure legends | definitions |
| 25 | Supplementary Fig. S2, labels | ±25% range rule (docs/model_spec.md section 6) |

## 8. 来源文件的 sha256（生成时）

| 文件 | sha256 |
|---|---|
| `data/ipd/K24_F2A_EFS_pembro.csv` | 55c68dee37923aeea2aa44c7098a9307cf643c456fafbc193614aaef2ad903d8 |
| `data/ipd/K24_F2A_EFS_placebo.csv` | c11b24f5ea47fc1651054fba33f71fa4e2232a068c99d32b5025eca1dbf0568f |
| `data/kn522_final_7y.csv` | 0f40a51bb51c1d412e7e6ee578c3cd98631980df61d8a1e12e3d193aafe3258a |
| `data/lifetable_female_2025.csv` | 213403bd92ac2669014a8b4edfba3210ed334c51031bf92e1a7bb87049fed733 |
| `data/params_dist.csv` | 3b8e10fcc27eb396dd7c3738dedd22f4ba6a1abe2ae60e14d7cf22841960b8b2 |
| `data/pcr_counts.csv` | 0d8cf779b0ffd827981d87e926ddc74b4483ab54ca02b5c1c47ebe88f9d030c1 |
| `docs/analysis_plan_phase2.md` | 7d386c574d7933de88cd1749f1b53ef64ccf8b6188acb6de03205f66ade9c41a |
| `docs/model_spec.md` | 38fede5399f9b70c166d8cf5baf5982f50e03ac27e44c2f68106af46887714ab |
| `input/papers/CHALLENGE.pdf` | cc531c2cd7d6e079d549025ef2907f8bc92e3bdcaf15d32deb44f518bf44fccb |
| `input/params/cohort_N_jbcs2024.csv` | 8dd976c1e47643e612feb0ee866e58f0a5cfd59347f1f4fb362b5fdc01d71f10 |
| `input/params/parameters_v10.xlsx` | 5e9396531d92fc8d8b0a0cbcf59aafcc6307676be5b48f8e09965088aae34510 |
| `input/params/sources_utility/utilities_scenario_jp.csv` | 59c1ac7f4de93e67fcd7b04b5e605eb71d2f38987f6a0623eb32889c98180448 |
| `manuscript/code/_build/engine_params_extract.csv` | 7aef325510f7d6241f17b9bc8bc34517a7d352667375d2752dc0679c4142a089 |
| `output/phase1/ae_deaths.csv` | 5de37965c1bd5f3d8a0b18631694d31fc67048a427b23a2fe4296418ed16d7c8 |
| `output/phase1/bootstrap_summary.csv` | c120a8caad3d1fcf4760df8c252dd86c1a9cf6aff42827b5a1e753e401ec2a6f |
| `output/phase1/calibration.csv` | d40cc1e71dff4acdbc7c76a514bed19a02d5b01a2cc7d4540cb2487b7de087bf |
| `output/phase1/calibration_curves.csv` | 9c7d8c8de5d83b54d5482859724b00117213cbaa4d87a81a6130d315356f12c9 |
| `output/phase1/calibration_final7y.csv` | 6b605ef7539af833981969e7dcba9a293f3329a06f64a623098ea8bfe7d400f7 |
| `output/phase1/calibration_gate.csv` | bbe3cf8cc4898e8b235c50092d8f28d98f982384e3d385333f04f09cc00eb505 |
| `output/phase1/calibration_gate_rmst.csv` | 25f95c894458658ec473a5c23bdae4a9d3d98f8289befee1cb01f44e22f82e22 |
| `output/phase1/engine_curves.csv` | fafcc2eaa939739c68c5fc06214d6f591b5bd65c0a81e553b081ced7f23f8ff5 |
| `output/phase1/round14/kext_derivation.csv` | df9012d396ccc2f18190571cfff1021210914cbfd48c476f96fdb125b5b43d1a |
| `output/phase1/round15/preprog_survival.csv` | d4a23c547d3f46be3c67277d834420d160976dd1c51064fee5430bf2f5c240f2 |
| `output/phase2/main/cohort_value_jbcs2024.csv` | d0689d50db6cddfa6bf102f2cd9e67a3162bef50eda8d43ec2faf7f347699c4a |
| `output/phase2/main/decomp_main_hr085.csv` | be47f4f12d860e2b763b671d9ea27853e873c56ebe8cae4c6517f162456063d3 |
| `output/phase2/main/decomp_reference.csv` | 35dfc9294341a9dbf7c8855bb014d7226986a4b075d92cff440245822fb853ee |
| `output/phase2/main/det_caps.csv` | 0f63eeecb6e2fc78ea12024bc1b54e822d5265bc02cfe702d47073e201eac0ef |
| `output/phase2/main/det_reference.csv` | 4b431ed1b804112adb2d1da256c89f9432f880c66df9b19cb2016cc6b7fccb44 |
| `output/phase2/main/det_yardstick.csv` | 68ad2c46a7b232d20cc29bc6055c6b5bfb186280a97ee63a78fef528357fb9aa |
| `output/phase2/main/oneway_base.csv` | 432601b43420909daccc9bc6d282f1a6134b7706861309fa326db122e918dae1 |
| `output/phase2/main/psa_caps_summary.csv` | 417e9f3832c97f3802209c847e157b92d30f7ddca2b38ab4402845d81cfae1ad |
| `output/phase2/main/psa_reference_summary.csv` | 68028e245ffab5387dd565ce0be02903d30b626bb72798696fef0f89e6b89173 |
| `output/phase2/main/sc_base_crossings.csv` | c8665b64726aac059ae3e23403d6b56550c018b3f0857da3abf92d7d22eebf9c |
| `output/phase2/main/sc_crossings.csv` | accdcc8331e664e9c7ef09cc1dc0ea3a7d1f4a44214bea8166008eda13678963 |
| `output/phase2/main/sc_eribulin_crossings.csv` | c1b0cdc1a209ebd91338e120a9636697ea36e35ed75cfda322f4f18ca324b4f1 |
| `output/phase2/main/sc_eribulin_det_caps.csv` | bfae73d45d1229b812c220cfff6d6097b1f547e6cbab6f873bedf5cc7f016414 |
| `output/phase2/main/sc_eribulin_det_reference.csv` | 5486010df2d8647857dcdb9ab3bddb72ebbbd3296fa2ed5503e42ae8793d0f4b |
| `output/phase2/main/sc_eribulin_psa_caps_summary.csv` | f8f313e178925831a15cdf1f4aaa56222481f276c7550573e27bcf14e04e818c |
| `output/phase2/main/sc_eribulin_psa_reference_summary.csv` | 65f8a8d01381c829fe380c029cfcd970f8725f7cba8488bc336f14d185f439a5 |
| `output/phase2/main/sc_metcost50_crossings.csv` | d0c243cad7eb453a0c49242d9478ffc1f34a804bec312aca08a004b9f791fd89 |
| `output/phase2/main/sc_metcost50_det_caps.csv` | 09e07587396981745468156061d11ae849d5679ce4768e1219b8a292c18ddfed |
| `output/phase2/main/sc_metcost50_det_reference.csv` | f46bf1c938f39bf36f2bce9214af9ba6b4ba3231a561ae1b2046b2e8a4b66399 |
| `output/phase2/main/sc_metcost50_psa_caps_summary.csv` | f908cb86ff31e4f9275ad4f4f349f952214087a99d717e42068d9eaa5b5516e3 |
| `output/phase2/main/sc_metcost50_psa_reference_summary.csv` | aab4b3b45d535e646671255835a2edd80b3b2991099b4b10e95b2209180e0231 |
| `output/phase2/main/sc_util_jp_det_caps.csv` | a3d81057b579f4cc55f95d5bfb9dd4bcbc1de7c1330b12bc89db04073b21ef4d |
| `output/phase2/main/sc_util_jp_det_reference.csv` | 53c2b36636efa103e4e8b5e853d6df30056479ff1a70a1d19f132344db35aa4e |
| `output/phase2/main/scenario_caps.csv` | a5489cb0c9301be9b1d32f511c462e89071cc2ee896cd6d38d3a04bae350a71e |
| `output/phase2/main/scenario_reference.csv` | eb3ad8dfc8f2e9bf988ce5506c286b452f457e6889977cdefc314d1e5d9f354f |
