# 数字对照表 v2（2026-10-26 17:01，由 `manuscript/code/make_ledger.py` 从登记表生成）

每个显示在表或图中的数字：显示值、位置、来源文件、来源中的位置、原始值。舍入：从原始值一次四舍五入（half up）；舍入为 0 的值不带负号；费用以千日元（JPY 1,000）显示，与第 2 阶段报告的“万日元 1 位小数”精度相同（例：272.6 万日元 = 2,726 千日元）。

## 1. Table 1–3（tables_v2.docx）

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
| 196 | 4,990 | Table 3, sjp, total | `output/phase2/main/scenario_reference.csv` | scenario = sjp, column = base, dC | 4989524.20858509 |  |
| 197 | 1.639 | Table 3, sjp, QALY | `output/phase2/main/scenario_reference.csv` | scenario = sjp, column = base, dQ | 1.63888097707382 |  |
| 198 | 3,044 | Table 3, sjp, ICER | `output/phase2/main/scenario_reference.csv` | scenario = sjp, column = base, icer | 3044470.14663246 |  |
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

两情景只改变费用参数，生存不变，所以各类别 = 基准栏的类别值 × 情景倍率（D03/D03P 与 D05 的类别），其余类别不变。核对：各类别之和与模型算出的 Δ费用（`sc_*_det_reference.csv` 的 dC）之差：

- m50：类别之和 5531427.474371 日元，模型 5531427.474371 日元，差 4.657e-09 日元
- eri：类别之和 6004926.396192 日元，模型 6004926.396192 日元，差 1.863e-09 日元

## 2. Fig. 1–3（figures_v2.docx 与 manuscript/v2/figures/）

图中的线、带、柱直接由下列文件的列画出（数值不经手写）；刻度数字是坐标轴的标度，不是结果，不登记。

| # | 显示 | 位置 | 来源文件 | 来源中的位置 | 原始值 | 暂定 |
|---|---|---|---|---|---|---|
| 1 | 13 points | Fig. 2, line, main | `output/phase2/main/det_caps.csv` | comparison = main, column = base, axis = hr0, x = 0.700 to 1.000 by 0.025, cap_500 / 1,000 | see file |  |
| 2 | 13 points | Fig. 2, band, main | `output/phase2/main/psa_caps_summary.csv` | comparison = main, column = base, axis = hr0, x = 0.700 to 1.000 by 0.025, cap500_lo and cap500_hi / 1,000 | see file |  |
| 3 | 13 points | Fig. 2, line, secondary | `output/phase2/main/det_caps.csv` | comparison = secondary, column = base, axis = hr0, x = 0.700 to 1.000 by 0.025, cap_500 / 1,000 | see file |  |
| 4 | 13 points | Fig. 2, band, secondary | `output/phase2/main/psa_caps_summary.csv` | comparison = secondary, column = base, axis = hr0, x = 0.700 to 1.000 by 0.025, cap500_lo and cap500_hi / 1,000 | see file |  |
| 5 | line | Fig. 2, horizontal line E01 | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G58 (E01) / 1,000 | 239508.135965065 |  |
| 6 | line | Fig. 2, horizontal line E02 | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G59 (E02) / 1,000 | 192400 |  |
| 7 | line | Fig. 2, horizontal line E03 | `input/params/parameters_v10.xlsx` | input/params/parameters_v10.xlsx sheet パラメータ cell G60 (E03) / 1,000 | 11260 | 【要確認】E03 |
| 8 | 21 | Fig. 3 legend (number of inputs shown) | `output/phase2/main/oneway_base.csv` | rows with |cap_high - cap_low| > 1e-6 x cap_base (same rule as R/23_phase2b_report.R tornado()) | 21 |  |
| 9 | 21 rows | Fig. 3, bars | `output/phase2/main/oneway_base.csv` | param_id, cap_low, cap_high, cap_base / 1,000 | see file | 【要確認】含 D02 的一行 |
| 10 | 21 | Fig. 3 legend | `output/phase2/main/oneway_base.csv` | number of rows that change the result (see Fig. 3 bars) | 21 |  |

### 暂定值（【要確認】）

入力表 v10 中备考为【要確認】、并在本版表图中显示（或直接由其算出）的值：E03（远程低价方案费用）与 D02（局部区域复发后的月额，只出现在 Fig. 3 的一行）。其余【要確認】行（B03、B04、B07–B10、F01P）只进入模型，不在表图中单独显示。

| 显示 | 位置 | 输入 |
|---|---|---|
| 11,260 | Table 1, exercise program | 【要確認】E03 |
| 0.997 | Table 2, Panel A, avoided = E03, main | 【要確認】E03 |
| 0.3 | Table 2, Panel A, avoided = E03, main, reduction % | 【要確認】E03 |
| 0.998 | Table 2, Panel A, avoided = E03, secondary | 【要確認】E03 |
| 0.2 | Table 2, Panel A, avoided = E03, secondary, reduction % | 【要確認】E03 |
| line | Fig. 2, horizontal line E03 | 【要確認】E03 |
| 21 rows | Fig. 3, bars | 【要確認】含 D02 的一行 |
| — | 输入 E03 | remote low-cost program cost (input table v10 note: 【要確認】) |
| — | 输入 D02 | monthly cost after locoregional recurrence (input table v10 note: 【要確認】) |

## 3. 编号与定义中的数字（不是结果；同一数字在别处作为值登记时以那里为准）

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

## 4. 来源文件的 sha256（生成时）

| 文件 | sha256 |
|---|---|
| `data/kn522_final_7y.csv` | 0f40a51bb51c1d412e7e6ee578c3cd98631980df61d8a1e12e3d193aafe3258a |
| `data/lifetable_female_2025.csv` | 213403bd92ac2669014a8b4edfba3210ed334c51031bf92e1a7bb87049fed733 |
| `data/pcr_counts.csv` | 0d8cf779b0ffd827981d87e926ddc74b4483ab54ca02b5c1c47ebe88f9d030c1 |
| `docs/analysis_plan_phase2.md` | e66e4b9180f740cffc1e8cd4a17288f5f62016e9c485ca13710a6812ab5c07e2 |
| `docs/model_spec.md` | 38fede5399f9b70c166d8cf5baf5982f50e03ac27e44c2f68106af46887714ab |
| `input/papers/CHALLENGE.pdf` | cc531c2cd7d6e079d549025ef2907f8bc92e3bdcaf15d32deb44f518bf44fccb |
| `input/params/parameters_v10.xlsx` | 5e9396531d92fc8d8b0a0cbcf59aafcc6307676be5b48f8e09965088aae34510 |
| `output/phase1/calibration.csv` | d40cc1e71dff4acdbc7c76a514bed19a02d5b01a2cc7d4540cb2487b7de087bf |
| `output/phase1/round14/kext_derivation.csv` | df9012d396ccc2f18190571cfff1021210914cbfd48c476f96fdb125b5b43d1a |
| `output/phase2/main/decomp_reference.csv` | 35dfc9294341a9dbf7c8855bb014d7226986a4b075d92cff440245822fb853ee |
| `output/phase2/main/det_caps.csv` | 0f63eeecb6e2fc78ea12024bc1b54e822d5265bc02cfe702d47073e201eac0ef |
| `output/phase2/main/det_reference.csv` | 4b431ed1b804112adb2d1da256c89f9432f880c66df9b19cb2016cc6b7fccb44 |
| `output/phase2/main/det_yardstick.csv` | 68ad2c46a7b232d20cc29bc6055c6b5bfb186280a97ee63a78fef528357fb9aa |
| `output/phase2/main/oneway_base.csv` | 432601b43420909daccc9bc6d282f1a6134b7706861309fa326db122e918dae1 |
| `output/phase2/main/psa_caps_summary.csv` | 417e9f3832c97f3802209c847e157b92d30f7ddca2b38ab4402845d81cfae1ad |
| `output/phase2/main/psa_reference_summary.csv` | 68028e245ffab5387dd565ce0be02903d30b626bb72798696fef0f89e6b89173 |
| `output/phase2/main/sc_base_crossings.csv` | c8665b64726aac059ae3e23403d6b56550c018b3f0857da3abf92d7d22eebf9c |
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
| `output/phase2/main/scenario_caps.csv` | a5489cb0c9301be9b1d32f511c462e89071cc2ee896cd6d38d3a04bae350a71e |
| `output/phase2/main/scenario_reference.csv` | eb3ad8dfc8f2e9bf988ce5506c286b452f457e6889977cdefc314d1e5d9f354f |
