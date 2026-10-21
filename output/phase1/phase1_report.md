# 第1阶段（生存引擎）报告

生成时间：2026-10-21 20:35。本文件由 `R/99_phase1_report.R` 从代码输出生成，表中数字均读自 `output/phase1/` 与 `data/` 下的文件。

## 状态：停在步骤 3（验证）

- 步骤 1（清点）、2（数字化）、3（重建与验证）已完成。验证共 49 项，4 项不达标，全部来自 Yau 2022；按任务书规定停止，步骤 4–7 未开始。
- KEYNOTE-522 的 10 条曲线（5 张图）全部达标。
- 另有 3 张正文引用的补充材料 KM 图不在 `input/papers/`（Schmid 2022 NEJM 386:556 Fig. S3；Schmid 2022 NEJM 386:556 Fig. S4；Schmid 2024 NEJM 391:1981 Fig. S4），其中 Schmid 2022 NEJM 386:556 Fig. S4 是模型核心输入（臂 × pCR 的 EFS）。

### 不达标项

| curve | check | time | unit | reported | reconstructed | abs_diff | tolerance | note |
|---|---|---|---|---|---|---|---|---|
| Y22_F4A_EFS_TNBC_RCB1 | events | 12 | years (cumulative) |  41.00 |  40.0000 | 1.0000 | 2% (0.82) | reference derived from the published risk table |
| Y22_F4A_EFS_TNBC_RCB2 | events | 12 | years (cumulative) | 189.00 | 185.0000 | 4.0000 | 2% (3.78) | reference derived from the published risk table |
| Y22_F4A_EFS_TNBC | hr |  | RCB-2 vs RCB-0 |   3.94 |   4.0773 | 0.1373 | 0.03 | reported: pooled 12-cohort model on all follow-up; reconstructed: single Cox on curves truncated at 12 y |
| Y22_F4A_EFS_TNBC | hr |  | RCB-3 vs RCB-0 |  13.04 |  13.3280 | 0.2880 | 0.03 | reported: pooled 12-cohort model on all follow-up; reconstructed: single Cox on curves truncated at 12 y |

## 1. 输入文件

| file | bytes | pages | sha256 |
|---|---|---|---|
| NEJMoa1910549.pdf |  586012 | 12 | 918ddcc6fb4751bcb2623c347e479960e6b0aac122d582054bfc1a2fdce01019 |
| NEJMoa2112651.pdf |  634005 | 12 | d706ac0b8c8bb886472d8fe14ebed855585fec468c2b6386d5102a4e79792be2 |
| NEJMoa2409932.pdf |  653287 | 11 | c65b2cbcffe20de49c4183d1775e817286e0ae8dee0c39d4e0ede0a394475aaf |
| Yau2022_LancetOncol_appendix_mmc1.pdf | 1416731 | 16 | 5a54d5805fcc2886a00cc18b5e41738ca88d16c76ac18fbf9c703f3818588ef4 |
| eScholarship UC item 0f60710w.pdf | 1448698 | 24 | 7539c502ee052465bec15a603ad91436d9507c8a4b803fbdb8ddd07bc32a8703 |

生命表：令和7(2025)年簡易生命表（女），见 `input/lifetable/SOURCE.md` 与 `data/lifetable_female_2025.csv`。

## 2. 清点表（`output/phase1/inventory.csv`）

| fig_key | source | figure | location | available | format | endpoint | population | analysis | data_cutoff | median_fu_months | time_origin | landmark_at_surgery |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K20_F2_EFS | Schmid 2020 NEJM 382:810 | Fig. 2 | main text | yes | vector | EFS | ITT, by arm | IA2 | April 24, 2019 | 15.5 | randomization | n/a (ITT) |
| K22_F1_EFS | Schmid 2022 NEJM 386:556 | Fig. 1 | main text | yes | vector | EFS | ITT, by arm | IA4 | March 23, 2021 | 39.1 | randomization | n/a (ITT) |
| K22_F3_OS | Schmid 2022 NEJM 386:556 | Fig. 3 | main text | yes | vector | OS | ITT, by arm | IA4 | March 23, 2021 | 39.1 | randomization | n/a (ITT) |
| K22_S3_DRFS | Schmid 2022 NEJM 386:556 | Fig. S3 | supplementary appendix | no | unknown | DRFS (distant progression/recurrence or death) | ITT, by arm | IA4 | March 23, 2021 | 39.1 | randomization (per protocol definition) | n/a (ITT) |
| K22_S4_EFS_by_pCR | Schmid 2022 NEJM 386:556 | Fig. S4 | supplementary appendix | no | unknown | EFS | arm x pCR (ypT0/Tis ypN0) | IA4 | March 23, 2021 | 39.1 | randomization per EFS definition; to confirm on the figure | yes if origin is randomization |
| K24_F1A_OS | Schmid 2024 NEJM 391:1981 | Fig. 1A | main text | yes | vector (with 2x inset) | OS | ITT, by arm | IA7 (final OS) | March 22, 2024 | 75.1 | randomization | n/a (ITT) |
| K24_F2A_EFS | Schmid 2024 NEJM 391:1981 | Fig. 2A | main text | yes | vector (with 2x inset) | EFS | ITT, by arm | IA7 | March 22, 2024 | 75.1 | randomization | n/a (ITT) |
| K24_S4_OS_by_pCR | Schmid 2024 NEJM 391:1981 | Fig. S4 | supplementary appendix | no | unknown | OS | arm x pCR (ypT0/Tis ypN0) | IA7 | March 22, 2024 | 75.1 | randomization per OS definition; to confirm on the figure | yes if origin is randomization |
| Y22_F4A_EFS_TNBC | Yau 2022 Lancet Oncol 23:149 (author manuscript) + appendix | Fig. 4A | main text; KM estimates in appendix Table S2 | yes | raster (JPEG 1920x1881, 300 dpi as placed) | EFS (Any locoregional recurrence, distant recurrence, or death from any cause) | HR-negative/HER2-negative (TNBC) by RCB class | pooled 12 cohorts | Nov 2019 (data collection) |  | start of neoadjuvant treatment | yes (origin = start of NAC) |

坐标轴、风险表时点、人数、事件数、里程碑与 HR：

| fig_key | x_axis | y_axis | risk_times | n | events | milestones | hr |
|---|---|---|---|---|---|---|---|
| K20_F2_EFS | 0-27 months (labels every 3) | 0-100% | 0;3;6;9;12;15;18;21;24;27 | pembro 784; placebo 390 | pembro 58/784; placebo 46/390 | 18-mo EFS pembro 91.3% (88.8-93.3), placebo 85.3% (80.3-89.1) | 0.63 (0.43-0.93), stratified Cox |
| K22_F1_EFS | 0-51 months (labels every 3) | 0-100% | 0;3;6;9;12;15;18;21;24;27;30;33;36;39;42;45;48;51 | pembro 784; placebo 390 | pembro 123/784; placebo 93/390 | 36-mo EFS pembro 84.5% (81.7-86.9), placebo 76.8% (72.2-80.7) | 0.63 (0.48-0.82), stratified Cox |
| K22_F3_OS | 0-51 months (labels every 3) | 0-100% | 0;3;6;9;12;15;18;21;24;27;30;33;36;39;42;45;48;51 | pembro 784; placebo 390 | deaths pembro 80/784; placebo 55/390 | 36-mo OS pembro 89.7% (87.3-91.7), placebo 86.9% (83.0-89.9) | 0.72 (0.51-1.02), stratified Cox |
| K22_S3_DRFS |  |  |  | pembro 784; placebo 390 | not in main text | not in main text | 0.61 (0.46-0.82) |
| K22_S4_EFS_by_pCR |  |  |  | pCR: pembro 494, placebo 217; non-pCR: pembro 290, placebo 173 | pCR: pembro 27, placebo 16; non-pCR: pembro 96, placebo 77 | not in main text | pCR 0.73 (0.39-1.36); non-pCR 0.70 (0.52-0.95) |
| K24_F1A_OS | 0-84 months (labels every 6) | 0-100% | 0;6;12;18;24;30;36;42;48;54;60;66;72;78;84 | pembro 784; placebo 390 | deaths pembro 115/784; placebo 85/390 | 3-y OS pembro 89.5% (87.1-91.5), placebo 86.9% (83.1-89.9); 4-y OS pembro 87.8% (85.3-89.9), placebo 83.5% (79.4-86.9); 5-y OS pembro 86.6% (84.0-88.8), placebo 81.7% (77.5-85.2) | overall stratified HR not reported in main text; unstratified piecewise HR 0.87 (0.57-1.32) before 2 y, 0.51 (0.35-0.75) after; event-weighted average 0.66 |
| K24_F2A_EFS | 0-84 months (labels every 6) | 0-100% | 0;6;12;18;24;30;36;42;48;54;60;66;72;78;84 | pembro 784; placebo 390 | pembro 159/784; placebo 114/390 | 5-y EFS pembro 81.2% (78.3-83.8), placebo 72.2% (67.4-76.4) | 0.65 (0.51-0.83), stratified Cox |
| K24_S4_OS_by_pCR |  |  |  | pCR: pembro 495, placebo 217; non-pCR: pembro 289, placebo 173 | deaths pCR: pembro 27, placebo 17; non-pCR: pembro 88, placebo 68 | 5-y OS difference pCR 0.7 pp (-2.9 to 4.3); non-pCR 6.1 pp (-2.7 to 14.9); arm-level 5-y values not in main text | not reported |
| Y22_F4A_EFS_TNBC | 0-12 years | 0-100% | 0;2;4;6;8;10;12 | RCB0 770; RCB1 212; RCB2 590; RCB3 202 | TNBC total 450 (all follow-up); by class from risk table | RCB-0 3/5/10-y 93/91/86%; RCB-1 3/5/10-y 84/80/75%; RCB-2 3/5/10-y 70/66/61%; RCB-3 3/5/10-y 32/28/25% | RCB-1 vs RCB-0 2.16 (1.48-3.15); RCB-2 vs RCB-0 3.94 (3-5.18); RCB-3 vs RCB-0 13.04 (9.8-17.35) |

EFS 首次事件构成：

| fig_key | efs_event_composition | source_pages |
|---|---|---|
| K20_F2_EFS | in supplementary Table S5 (not provided) | text p1,6; figure p8 |
| K22_F1_EFS | first events (pembro/placebo): progression precluding surgery 14/15, local 28/17, distant 60/51, second primary 6/4, death 15/6; local followed by distant 13/9 | text p5,5; Table 1 p6; figure p5 |
| K22_S4_EFS_by_pCR | not in main text | text p6 |
| K24_F2A_EFS | first events (pembro/placebo): progression precluding surgery 14/15, local 33/20, distant 77/56, second primary 16/10, death 19/13 | text p6; Table 1 p8; figure p7 |

每个报告值的出处（页码与原文片段）见 `data/reported_values.csv`（189 个值，正则从 PDF 正文抽取）。

## 3. 数字化（`data/digitized/`）

矢量图：PyMuPDF `get_drawings()` 直接读取阶梯路径坐标。x 轴用全部带标签刻度做最小二乘；y 轴用 0% 与 100% 两端刻度锚定（NEJM 2024 两图的 100% 刻度与 0–90% 刻度间距不一致，插图读数支持两端锚定，见 inset 列）。删失标记为同色短竖线。

| fig_id | arm | legend_colour_matches_spec | n_vertices | n_drops | n_censor_marks | s_first | t_last | s_last | calib_resid_x | calib_resid_y | inset_median_abs_diff | inset_max_abs_diff |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K20_F2_EFS | pembro | True | 101 |  50 | 385 |  99.9966 | 24.533 | 90.308 | 0.0005 | 0.0039 |  |  |
| K20_F2_EFS | placebo | True |  91 |  45 | 245 |  99.9966 | 24.466 | 81.592 | 0.0005 | 0.0039 |  |  |
| K22_F1_EFS | pembro | no legend sample | 214 | 110 | 661 |  99.9977 | 47.791 | 83.469 | 0.0009 | 0.0035 |  |  |
| K22_F1_EFS | placebo | no legend sample | 184 |  91 | 297 |  99.9977 | 46.941 | 72.954 | 0.0009 | 0.0035 |  |  |
| K22_F3_OS | pembro | no legend sample | 152 |  76 | 704 | 100.0007 | 47.891 | 89.227 | 0.0154 | 0.0035 |  |  |
| K22_F3_OS | placebo | no legend sample | 106 |  52 | 335 | 100.0007 | 46.947 | 84.078 | 0.0154 | 0.0035 |  |  |
| K24_F1A_OS | pembro | no legend sample | 230 | 110 | 669 | 100.0006 | 83.745 | 84.073 | 0.0014 | 0.1241 | 0.0030 | 0.2563 |
| K24_F1A_OS | placebo | no legend sample | 179 |  82 | 305 | 100.0006 | 83.092 | 77.624 | 0.0014 | 0.1241 | 0.0030 | 0.2563 |
| K24_F2A_EFS | pembro | no legend sample | 293 | 146 | 625 | 100.0364 | 83.607 | 78.424 | 0.0014 | 0.1172 | 0.0172 | 0.2784 |
| K24_F2A_EFS | placebo | no legend sample | 238 | 112 | 276 | 100.0364 | 83.109 | 70.238 | 0.0014 | 0.1172 | 0.0172 | 0.2784 |

栅格图（Yau Fig. 4A）：嵌入图像为 1920x1881，按原生像素做颜色分离（以 600 dpi 栅格化只会对该图插值，不增加信息）；线条水平用单调阶梯的动态规划追踪，以免密集删失标记把线条拉低。风险表与刻度值从图像转录（栅格无文字层），脚本检查了“人数 − 在险 − 累计删失”的单调性。

| arm | n_pixels | column_coverage | n_steps | t_last | s_last | calib_resid_x | calib_resid_y | px_per_unit_x | px_per_pct_y |
|---|---|---|---|---|---|---|---|---|---|
| RCB0 | 6228 | 0.9550 | 23 | 12 | 83.671 | 0.0034 | 0.0537 | 62.946 | 5.975 |
| RCB1 | 2996 | 0.9669 | 30 | 12 | 75.028 | 0.0034 | 0.0537 | 62.946 | 5.975 |
| RCB2 | 4954 | 0.9788 | 45 | 12 | 58.644 | 0.0034 | 0.0537 | 62.946 | 5.975 |
| RCB3 | 2562 | 0.9974 | 61 | 12 | 17.997 | 0.0034 | 0.0537 | 62.946 | 5.975 |

叠图质控：`data/digitized/qa/*_overlay.png`。

## 4. 个体数据重建与验证（`output/phase1/validation.csv`）

Guyot 2012 算法（`R/guyot.R`，按原文 R 代码实现；`IPDfromKM::getIPD` 用同一输入交叉核对）。重建时不输入报告总事件数，事件数检查因此不是循环验证。
门槛：里程碑差 ≤ 1 个百分点；Cox HR 差 ≤ 0.03；事件数差 ≤ 2%。

| curve | check | time | unit | reported | reconstructed | abs_diff | tolerance | pass | reference | note |
|---|---|---|---|---|---|---|---|---|---|---|
| K20_F2_EFS_pembro | milestone | 18 | months |  91.30 |  91.4053 | 0.1053 | 1 | 达标 | NEJMoa1910549 p6 |  |
| K20_F2_EFS_pembro | events |  |  |  58.00 |  57.0000 | 1.0000 | 2% (1.16) | 达标 | NEJMoa1910549 p1 |  |
| K20_F2_EFS_placebo | milestone | 18 | months |  85.30 |  85.3111 | 0.0111 | 1 | 达标 | NEJMoa1910549 p6 |  |
| K20_F2_EFS_placebo | events |  |  |  46.00 |  46.0000 | 0.0000 | 2% (0.92) | 达标 | NEJMoa1910549 p1 |  |
| K20_F2_EFS | hr |  |  |   0.63 |   0.6163 | 0.0137 | 0.03 | 达标 | NEJMoa1910549 p1 | reported: stratified Cox; reconstructed: unstratified Cox |
| K22_F1_EFS_pembro | milestone | 36 | months |  84.50 |  84.4726 | 0.0274 | 1 | 达标 | NEJMoa2112651 p5 |  |
| K22_F1_EFS_pembro | events |  |  | 123.00 | 123.0000 | 0.0000 | 2% (2.46) | 达标 | NEJMoa2112651 p5 |  |
| K22_F1_EFS_placebo | milestone | 36 | months |  76.80 |  76.7529 | 0.0471 | 1 | 达标 | NEJMoa2112651 p5 |  |
| K22_F1_EFS_placebo | events |  |  |  93.00 |  93.0000 | 0.0000 | 2% (1.86) | 达标 | NEJMoa2112651 p5 |  |
| K22_F1_EFS | hr |  |  |   0.63 |   0.6288 | 0.0012 | 0.03 | 达标 | NEJMoa2112651 p5 | reported: stratified Cox; reconstructed: unstratified Cox |
| K22_F3_OS_pembro | milestone | 36 | months |  89.70 |  89.7290 | 0.0290 | 1 | 达标 | NEJMoa2112651 p6 |  |
| K22_F3_OS_pembro | events |  |  |  80.00 |  80.0000 | 0.0000 | 2% (1.60) | 达标 | NEJMoa2112651 p6 |  |
| K22_F3_OS_placebo | milestone | 36 | months |  86.90 |  86.8641 | 0.0359 | 1 | 达标 | NEJMoa2112651 p6 |  |
| K22_F3_OS_placebo | events |  |  |  55.00 |  55.0000 | 0.0000 | 2% (1.10) | 达标 | NEJMoa2112651 p6 |  |
| K22_F3_OS | hr |  |  |   0.72 |   0.7213 | 0.0013 | 0.03 | 达标 | NEJMoa2112651 p6 | reported: stratified Cox; reconstructed: unstratified Cox |
| K24_F1A_OS_pembro | milestone | 36 | months |  89.50 |  89.5096 | 0.0096 | 1 | 达标 | NEJMoa2409932 p6 |  |
| K24_F1A_OS_pembro | milestone | 48 | months |  87.80 |  87.8410 | 0.0410 | 1 | 达标 | NEJMoa2409932 p6 |  |
| K24_F1A_OS_pembro | milestone | 60 | months |  86.60 |  86.5517 | 0.0483 | 1 | 达标 | NEJMoa2409932 p6 |  |
| K24_F1A_OS_pembro | events |  |  | 115.00 | 115.0000 | 0.0000 | 2% (2.30) | 达标 | NEJMoa2409932 p4 |  |
| K24_F1A_OS_placebo | milestone | 36 | months |  86.90 |  86.9029 | 0.0029 | 1 | 达标 | NEJMoa2409932 p6 |  |
| K24_F1A_OS_placebo | milestone | 48 | months |  83.50 |  83.5319 | 0.0319 | 1 | 达标 | NEJMoa2409932 p6 |  |
| K24_F1A_OS_placebo | milestone | 60 | months |  81.70 |  81.7063 | 0.0063 | 1 | 达标 | NEJMoa2409932 p6 |  |
| K24_F1A_OS_placebo | events |  |  |  85.00 |  85.0000 | 0.0000 | 2% (1.70) | 达标 | NEJMoa2409932 p4 |  |
| K24_F1A_OS | hr | 24 | months (before) |   0.87 |   0.8690 | 0.0010 | 0.03 | 达标 | NEJMoa2409932 p6 | reported: unstratified piecewise Cox, as reconstructed |
| K24_F1A_OS | hr | 24 | months (after) |   0.51 |   0.5105 | 0.0005 | 0.03 | 达标 | NEJMoa2409932 p6 | reported: unstratified piecewise Cox, as reconstructed |
| K24_F2A_EFS_pembro | milestone | 60 | months |  81.20 |  81.2196 | 0.0196 | 1 | 达标 | NEJMoa2409932 p6 |  |
| K24_F2A_EFS_pembro | events |  |  | 159.00 | 159.0000 | 0.0000 | 2% (3.18) | 达标 | NEJMoa2409932 p6 |  |
| K24_F2A_EFS_placebo | milestone | 60 | months |  72.20 |  72.2182 | 0.0182 | 1 | 达标 | NEJMoa2409932 p6 |  |
| K24_F2A_EFS_placebo | events |  |  | 114.00 | 114.0000 | 0.0000 | 2% (2.28) | 达标 | NEJMoa2409932 p6 |  |
| K24_F2A_EFS | hr |  |  |   0.65 |   0.6551 | 0.0051 | 0.03 | 达标 | NEJMoa2409932 p6 | reported: stratified Cox; reconstructed: unstratified Cox |
| Y22_F4A_EFS_TNBC_RCB0 | milestone |  3 | years |  93.00 |  93.0340 | 0.0340 | 1 | 达标 | Yau2022_LancetOncol_appendix_mmc1 p5 | reported value rounded to whole % |
| Y22_F4A_EFS_TNBC_RCB0 | milestone |  5 | years |  91.00 |  90.1473 | 0.8527 | 1 | 达标 | Yau2022_LancetOncol_appendix_mmc1 p5 | reported value rounded to whole % |
| Y22_F4A_EFS_TNBC_RCB0 | milestone | 10 | years |  86.00 |  85.6627 | 0.3373 | 1 | 达标 | Yau2022_LancetOncol_appendix_mmc1 p5 | reported value rounded to whole % |
| Y22_F4A_EFS_TNBC_RCB0 | events | 12 | years (cumulative) |  67.00 |  67.0000 | 0.0000 | 2% (1.34) | 达标 | figure risk table: N - at risk - censored at 12 y | reference derived from the published risk table |
| Y22_F4A_EFS_TNBC_RCB1 | milestone |  3 | years |  84.00 |  84.2706 | 0.2706 | 1 | 达标 | Yau2022_LancetOncol_appendix_mmc1 p5 | reported value rounded to whole % |
| Y22_F4A_EFS_TNBC_RCB1 | milestone |  5 | years |  80.00 |  79.8673 | 0.1327 | 1 | 达标 | Yau2022_LancetOncol_appendix_mmc1 p5 | reported value rounded to whole % |
| Y22_F4A_EFS_TNBC_RCB1 | milestone | 10 | years |  75.00 |  75.3058 | 0.3058 | 1 | 达标 | Yau2022_LancetOncol_appendix_mmc1 p5 | reported value rounded to whole % |
| Y22_F4A_EFS_TNBC_RCB1 | events | 12 | years (cumulative) |  41.00 |  40.0000 | 1.0000 | 2% (0.82) | **不达标** | figure risk table: N - at risk - censored at 12 y | reference derived from the published risk table |
| Y22_F4A_EFS_TNBC_RCB2 | milestone |  3 | years |  70.00 |  70.1883 | 0.1883 | 1 | 达标 | Yau2022_LancetOncol_appendix_mmc1 p5 | reported value rounded to whole % |
| Y22_F4A_EFS_TNBC_RCB2 | milestone |  5 | years |  66.00 |  66.2417 | 0.2417 | 1 | 达标 | Yau2022_LancetOncol_appendix_mmc1 p5 | reported value rounded to whole % |
| Y22_F4A_EFS_TNBC_RCB2 | milestone | 10 | years |  61.00 |  61.3548 | 0.3548 | 1 | 达标 | Yau2022_LancetOncol_appendix_mmc1 p5 | reported value rounded to whole % |
| Y22_F4A_EFS_TNBC_RCB2 | events | 12 | years (cumulative) | 189.00 | 185.0000 | 4.0000 | 2% (3.78) | **不达标** | figure risk table: N - at risk - censored at 12 y | reference derived from the published risk table |
| Y22_F4A_EFS_TNBC_RCB3 | milestone |  3 | years |  32.00 |  31.4412 | 0.5588 | 1 | 达标 | Yau2022_LancetOncol_appendix_mmc1 p5 | reported value rounded to whole % |
| Y22_F4A_EFS_TNBC_RCB3 | milestone |  5 | years |  28.00 |  28.0982 | 0.0982 | 1 | 达标 | Yau2022_LancetOncol_appendix_mmc1 p5 | reported value rounded to whole % |
| Y22_F4A_EFS_TNBC_RCB3 | milestone | 10 | years |  25.00 |  25.4526 | 0.4526 | 1 | 达标 | Yau2022_LancetOncol_appendix_mmc1 p5 | reported value rounded to whole % |
| Y22_F4A_EFS_TNBC_RCB3 | events | 12 | years (cumulative) | 144.00 | 142.0000 | 2.0000 | 2% (2.88) | 达标 | figure risk table: N - at risk - censored at 12 y | reference derived from the published risk table |
| Y22_F4A_EFS_TNBC | hr |  | RCB-1 vs RCB-0 |   2.16 |   2.1536 | 0.0064 | 0.03 | 达标 | Yau2022_LancetOncol_appendix_mmc1 p5 | reported: pooled 12-cohort model on all follow-up; reconstructed: single Cox on curves truncated at 12 y |
| Y22_F4A_EFS_TNBC | hr |  | RCB-2 vs RCB-0 |   3.94 |   4.0773 | 0.1373 | 0.03 | **不达标** | Yau2022_LancetOncol_appendix_mmc1 p5 | reported: pooled 12-cohort model on all follow-up; reconstructed: single Cox on curves truncated at 12 y |
| Y22_F4A_EFS_TNBC | hr |  | RCB-3 vs RCB-0 |  13.04 |  13.3280 | 0.2880 | 0.03 | **不达标** | Yau2022_LancetOncol_appendix_mmc1 p5 | reported: pooled 12-cohort model on all follow-up; reconstructed: single Cox on curves truncated at 12 y |

诊断（不作门槛）：重建 KM 与数字化曲线的最大差、风险表再现、与 IPDfromKM 的差异，以及每个风险区间内“图上删失标记数/Guyot 删失数”。

| curve | n | events_guyot | events_ipdfromkm | max_abs_km_vs_digitized_pp | max_abs_guyot_vs_ipdfromkm_pp | max_abs_risk_table_diff | censor_marks_drawn | censored_guyot | censored_by_interval_marks_vs_guyot |
|---|---|---|---|---|---|---|---|---|---|
| K20_F2_EFS_pembro | 784 |  57 |  55 | 0.114 | 0.356 | 0 | 385 | 727 | 2/2;4/4;52/80;65/133;67/138;67/130;77/167;49/71;2/2 |
| K20_F2_EFS_placebo | 390 |  46 |  45 | 0.173 | 0.751 | 0 | 245 | 344 | 2/2;2/2;23/29;46/66;51/69;44/64;46/77;30/34;1/1 |
| K22_F1_EFS_pembro | 784 | 123 | 122 | 0.035 | 0.239 | 0 | 661 | 661 | 1/1;1/1;1/0;1/2;0/0;0/0;0/0;4/4;1/1;12/12;97/97;114/114;127/127;137/137;137/137;28/28 |
| K22_F1_EFS_placebo | 390 |  93 |  92 | 0.442 | 1.209 | 1 | 297 | 297 | 1/1;1/1;0/0;1/1;3/3;1/1;0/0;0/0;0/0;2/2;43/43;54/54;54/54;55/55;66/65;16/17 |
| K22_F3_OS_pembro | 784 |  80 |  80 | 0.024 | 0.070 | 1 | 704 | 704 | 1/1;0/0;0/0;2/3;0/0;0/0;0/0;1/0;1/1;10/10;110/110;120/120;136/136;145/145;148/148;30/30 |
| K22_F3_OS_placebo | 390 |  55 |  55 | 0.043 | 0.163 | 0 | 335 | 335 | 0/0;0/0;0/0;0/0;0/0;0/0;1/1;0/0;1/1;1/1;54/54;60/60;62/62;67/67;72/72;17/17 |
| K24_F1A_OS_pembro | 784 | 115 | 115 | 0.222 | 0.001 | 0 | 669 | 669 | 1/1;1/1;0/0;1/1;0/0;1/1;0/0;2/2;2/2;1/1;12/11;208/205;265/269;175/175 |
| K24_F1A_OS_placebo | 390 |  85 |  85 | 0.065 | 0.001 | 0 | 305 | 305 | 0/0;0/0;0/0;1/1;0/0;2/2;1/1;1/1;1/1;0/0;7/7;94/94;116/116;82/82 |
| K24_F2A_EFS_pembro | 784 | 159 | 159 | 0.183 | 0.293 | 0 | 625 | 625 | 2/2;2/2;0/0;4/4;0/0;2/2;1/1;3/3;3/3;3/3;12/12;187/187;241/243;165/163 |
| K24_F2A_EFS_placebo | 390 | 114 | 114 | 0.046 | 0.088 | 0 | 276 | 276 | 2/2;1/1;2/2;0/0;0/0;1/1;2/2;0/0;1/1;1/1;6/6;82/82;102/102;76/76 |
| Y22_F4A_EFS_TNBC_RCB0 | 770 |  67 |  65 | 0.101 | 0.194 | 0 |  | 703 |  |
| Y22_F4A_EFS_TNBC_RCB1 | 212 |  40 |  40 | 0.333 | 0.588 | 0 |  | 172 |  |
| Y22_F4A_EFS_TNBC_RCB2 | 590 | 185 | 182 | 0.299 | 0.762 | 0 |  | 405 |  |
| Y22_F4A_EFS_TNBC_RCB3 | 202 | 142 | 142 | 0.431 | 1.715 | 0 |  |  60 |  |

图：`output/phase1/fig_validation_*.png`（灰线为数字化曲线，红虚线为重建个体数据的 KM，圆点为原文里程碑，竖线为 ±1 个百分点）。

## 5. 需要决定的事项

1. **Yau 2022 不达标项的处理。**
   - Y22_F4A_EFS_TNBC_RCB1 events years (cumulative)：原文 41，重建 40，差 1（门槛 2% (0.82)）。reference derived from the published risk table
   - Y22_F4A_EFS_TNBC_RCB2 events years (cumulative)：原文 189，重建 185，差 4（门槛 2% (3.78)）。reference derived from the published risk table
   - Y22_F4A_EFS_TNBC hr RCB-2 vs RCB-0：原文 3.94，重建 4.0773，差 0.1373（门槛 0.03）。reported: pooled 12-cohort model on all follow-up; reconstructed: single Cox on curves truncated at 12 y
   - Y22_F4A_EFS_TNBC hr RCB-3 vs RCB-0：原文 13.04，重建 13.328，差 0.288（门槛 0.03）。reported: pooled 12-cohort model on all follow-up; reconstructed: single Cox on curves truncated at 12 y
   - HR 两项：原文 HR 出自 12 个队列汇总、含队列效应的模型，用全部随访；重建数据只到 12 年、只能做单一 Cox，两者不是同一估计量。
   - 事件数两项：参照值是由风险表推出的 12 年累计事件数（人数 − 在险 − 累计删失），差异来自 Guyot 对区间内删失均匀分布的假设；把数字化的下降惩罚改为 0.5 或 3.0，RCB-2 仍为同一事件数。
   - Yau 在本模型中只用作外推的外部对照（步骤 4 的第③条），不进入模型参数。
2. **补充材料。** 需要 Schmid 2022 NEJM 386:556 Fig. S3（DRFS (distant progression/recurrence or death)，ITT, by arm）；Schmid 2022 NEJM 386:556 Fig. S4（EFS，arm x pCR (ypT0/Tis ypN0)）；Schmid 2024 NEJM 391:1981 Fig. S4（OS，arm x pCR (ypT0/Tis ypN0)）。NEJM 网站拒绝脚本下载（HTTP 403），需手动下载放入 `input/papers/`。
3. **pCR 比例的出处。** 正文的 pCR 亚组人数：K22 (IA4) 帕博利珠单抗组 494/784（63.0%）、安慰剂组 217/390（55.6%）；K24 (IA7) 为 495/784（63.1%）、217/390（55.6%）。“最终分析的全体 ITT 数值”取哪一版需确认。
4. **队列起始年龄。** 基线表只给各臂中位数（帕博利珠单抗组 49 岁，范围 22–80；安慰剂组 48 岁，范围 24–79），没有全体中位数。

## 6. 未开始的步骤

步骤 4（参数与样条、治愈模型拟合）、5（远处复发后死亡率校准）、6（bootstrap B = 1000）、7（生存引擎函数）。

