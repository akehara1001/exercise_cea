# 第1阶段（生存引擎）报告

生成时间：2026-10-21 22:19。由 `R/99_phase1_report.R` 从代码输出生成，表中数字均读自 `output/` 与 `data/` 下的文件。模型规格见 `docs/model_spec.md`。

## 状态

- 已完成：步骤 1（清点，含两份补充材料）、2（数字化）、3（重建与验证）、一致性检查、步骤 4（拟合与选择）、步骤 5（校准）；引擎接口已按 `docs/model_spec.md` 扩展。
- 验证共 71 项，其中门槛项 64 项，**1 项不达标**；非门槛项（Yau 的 HR 与事件数）4 项不符，按 2026-10-21 的决定只报告。
- 按规则在此停止：步骤 6（bootstrap）与 7（生存引擎的最终输出）未进行。

### 不达标的门槛项

| curve | check | unit | reported | reconstructed | abs_diff | tolerance | reference | note |
|---|---|---|---|---|---|---|---|---|
| K22_S4_EFS_pCR | hr | pCR (user-supplied reference) | 0.65 | 0.7224 | 0.0724 | 0.03 | input/user_supplied_values.csv | reference 0.65 [0.39, 1.08]: user instruction 2026-10-21 (stratum HR for the EFS by arm x pCR check); source not given and not found in input/papers |

同一组重建曲线对 2022 年补充材料 Fig. S4（IA4）印的层内 HR：pCR 原文 0.73、重建 0.7224（差 0.0076）；non-pCR 原文 0.7、重建 0.7117（差 0.0117）。用户提供的参照值不在输入文献中；其 pCR 层 95% CI 上限比 IA4 窄，可能来自更晚的数据截点。如果参照值来自另一次分析，用 IA4 的曲线无法复现它：需要该分析的按臂 × pCR 分层 KM 图，或改为不作门槛的跨分析对照。

## 1. 输入文件

| file | bytes | pages | sha256 |
|---|---|---|---|
| NEJMoa1910549.pdf |  586012 | 12 | 918ddcc6fb4751bcb2623c347e479960e6b0aac122d582054bfc1a2fdce01019 |
| NEJMoa2112651.pdf |  634005 | 12 | d706ac0b8c8bb886472d8fe14ebed855585fec468c2b6386d5102a4e79792be2 |
| NEJMoa2409932.pdf |  653287 | 11 | c65b2cbcffe20de49c4183d1775e817286e0ae8dee0c39d4e0ede0a394475aaf |
| SOURCE.md |     772 |  1 | 0da505d18951e426779725cf17630ae2e7eb1a5ab22af2949d343f0864a16aec |
| Yau2022_LancetOncol_appendix_mmc1.pdf | 1416731 | 16 | 5a54d5805fcc2886a00cc18b5e41738ca88d16c76ac18fbf9c703f3818588ef4 |
| eScholarship UC item 0f60710w.pdf | 1448698 | 24 | 7539c502ee052465bec15a603ad91436d9507c8a4b803fbdb8ddd07bc32a8703 |
| nejmoa2112651_appendix.pdf | 1697609 | 32 | 9c763e0ce6eff9127bde821ab33abec9a27a74c4195e2dda8d1b358562e39c99 |
| nejmoa2409932_appendix.pdf | 1148372 | 21 | 05e6a362b2ebb49d7c1d8101120c2e6d8254fb8bc216a1534a02733c6e0c317c |

生命表：令和7(2025)年簡易生命表（女），`input/lifetable/SOURCE.md`、`data/lifetable_female_2025.csv`。

## 2. 清点表（`output/phase1/inventory.csv`）

| fig_key | source | figure | location | available | format | endpoint | population | analysis | data_cutoff | median_fu_months | time_origin | landmark_at_surgery |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K20_F2_EFS | Schmid 2020 NEJM 382:810 | Fig. 2 | main text | yes | vector | EFS | ITT, by arm | IA2 | April 24, 2019 | 15.5 | randomization | n/a (ITT) |
| K22_F1_EFS | Schmid 2022 NEJM 386:556 | Fig. 1 | main text | yes | vector | EFS | ITT, by arm | IA4 | March 23, 2021 | 39.1 | randomization | n/a (ITT) |
| K22_F3_OS | Schmid 2022 NEJM 386:556 | Fig. 3 | main text | yes | vector | OS | ITT, by arm | IA4 | March 23, 2021 | 39.1 | randomization | n/a (ITT) |
| K22_S3_DRFS | Schmid 2022 NEJM 386:556 appendix | Fig. S3 | supplementary appendix | yes | raster (PNG 1430x1106, 220 dpi as placed) | DRFS (distant progression, distant recurrence or death) | Intention-to-Treat Population, by arm | IA4 | March 23, 2021 | 39.1 | randomization (axis from 0, full ITT at risk at 0) | n/a (ITT) |
| K22_S4_EFS_by_pCR | Schmid 2022 NEJM 386:556 appendix | Fig. S4 | supplementary appendix | yes | raster (PNG 1282x1038, 191 dpi as placed) | EFS | arm x pCR (ypT0/Tis ypN0), ITT | IA4 | March 23, 2021 | 39.1 | randomization (axis from 0; pCR groups have no events before surgery) | yes |
| K24_F1A_OS | Schmid 2024 NEJM 391:1981 | Fig. 1A | main text | yes | vector (with 2x inset) | OS | ITT, by arm | IA7 (final OS) | March 22, 2024 | 75.1 | randomization | n/a (ITT) |
| K24_F2A_EFS | Schmid 2024 NEJM 391:1981 | Fig. 2A | main text | yes | vector (with 2x inset) | EFS | ITT, by arm | IA7 | March 22, 2024 | 75.1 | randomization | n/a (ITT) |
| K24_S4_OS_by_pCR | Schmid 2024 NEJM 391:1981 appendix | Fig. S4 | supplementary appendix | yes | raster (JPEG 1099x1143, 204 dpi as placed) | OS | arm x pCR (ypT0/Tis ypN0), ITT | IA7 | March 22, 2024 | 75.1 | randomization (axis from 0) | yes |
| Y22_F4A_EFS_TNBC | Yau 2022 Lancet Oncol 23:149 (author manuscript) + appendix | Fig. 4A | main text; KM estimates in appendix Table S2 | yes | raster (JPEG 1920x1881, 300 dpi as placed) | EFS (Any locoregional recurrence, distant recurrence, or death from any cause) | HR-negative/HER2-negative (TNBC) by RCB class | pooled 12 cohorts | Nov 2019 (data collection) |  | start of neoadjuvant treatment | yes (origin = start of NAC) |

| fig_key | x_axis | risk_times | n | events | milestones | hr |
|---|---|---|---|---|---|---|
| K20_F2_EFS | 0-27 months (labels every 3) | 0;3;6;9;12;15;18;21;24;27 | pembro 784; placebo 390 | pembro 58/784; placebo 46/390 | 18-mo EFS pembro 91.3% (88.8-93.3), placebo 85.3% (80.3-89.1) | 0.63 (0.43-0.93), stratified Cox |
| K22_F1_EFS | 0-51 months (labels every 3) | 0;3;6;9;12;15;18;21;24;27;30;33;36;39;42;45;48;51 | pembro 784; placebo 390 | pembro 123/784; placebo 93/390 | 36-mo EFS pembro 84.5% (81.7-86.9), placebo 76.8% (72.2-80.7) | 0.63 (0.48-0.82), stratified Cox |
| K22_F3_OS | 0-51 months (labels every 3) | 0;3;6;9;12;15;18;21;24;27;30;33;36;39;42;45;48;51 | pembro 784; placebo 390 | deaths pembro 80/784; placebo 55/390 | 36-mo OS pembro 89.7% (87.3-91.7), placebo 86.9% (83.0-89.9) | 0.72 (0.51-1.02), stratified Cox |
| K22_S3_DRFS | 0-51 months (labels every 3) | 0;3;6;9;12;15;18;21;24;27;30;33;36;39;42;45;48;51 | pembro 784; placebo 390 | not reported | 36-mo DRFS pembro 87.0%, placebo 80.7% (printed in figure) | 0.61 (0.46-0.82), Cox regression model with treatment as a covariate stratified by the randomization stratification factors |
| K22_S4_EFS_by_pCR | 0-51 months (labels every 3) | 0;3;6;9;12;15;18;21;24;27;30;33;36;39;42;45;48;51 | pembro_pCR 494; placebo_pCR 217; pembro_nonpCR 290; placebo_nonpCR 173 | pCR: pembro 27/494, placebo 16/217; non-pCR: pembro 96/290, placebo 77/173 | 36-mo EFS pembro_pCR 94.4%, placebo_pCR 92.5%, pembro_nonpCR 67.4%, placebo_nonpCR 56.8% (printed in figure) | pCR 0.73 (0.39-1.36); non-pCR 0.70 (0.52-0.95); Cox regression model with treatment as a covariate (unstratified) |
| K24_F1A_OS | 0-84 months (labels every 6) | 0;6;12;18;24;30;36;42;48;54;60;66;72;78;84 | pembro 784; placebo 390 | deaths pembro 115/784; placebo 85/390 | 3-y OS pembro 89.5% (87.1-91.5), placebo 86.9% (83.1-89.9); 4-y OS pembro 87.8% (85.3-89.9), placebo 83.5% (79.4-86.9); 5-y OS pembro 86.6% (84.0-88.8), placebo 81.7% (77.5-85.2) | 0.66 (0.50-0.87), protocol-specified (stratified) Cox, appendix p11; unstratified piecewise HR 0.87 (0.57-1.32) before 2 y, 0.51 (0.35-0.75) after; event-weighted average 0.66 |
| K24_F2A_EFS | 0-84 months (labels every 6) | 0;6;12;18;24;30;36;42;48;54;60;66;72;78;84 | pembro 784; placebo 390 | pembro 159/784; placebo 114/390 | 5-y EFS pembro 81.2% (78.3-83.8), placebo 72.2% (67.4-76.4) | 0.65 (0.51-0.83), stratified Cox |
| K24_S4_OS_by_pCR | 0-84 months (labels every 6) | 0;6;12;18;24;30;36;42;48;54;60;66;72;78;84 | pembro_pCR 495; placebo_pCR 217; pembro_nonpCR 289; placebo_nonpCR 173 | deaths pCR: pembro 27/495, placebo 17/217; non-pCR: pembro 88/289, placebo 68/173 | 5-y OS difference (pembro - placebo) pCR 0.7 pp (-2.9 to 4.3); non-pCR 6.1 pp (-2.7 to 14.9); arm-level values not reported | not reported |
| Y22_F4A_EFS_TNBC | 0-12 years (labels every 2) | 0;2;4;6;8;10;12 | RCB0 770; RCB1 212; RCB2 590; RCB3 202 | TNBC total 450 (all follow-up); by class from risk table | RCB-0 3/5/10-y 93/91/86%; RCB-1 3/5/10-y 84/80/75%; RCB-2 3/5/10-y 70/66/61%; RCB-3 3/5/10-y 32/28/25% | RCB-1 vs RCB-0 2.16 (1.48-3.15); RCB-2 vs RCB-0 3.94 (3-5.18); RCB-3 vs RCB-0 13.04 (9.8-17.35) |

EFS 首次事件构成：

| fig_key | efs_event_composition |
|---|---|
| K22_F1_EFS | first events (pembro/placebo): progression precluding surgery 14/15, local 28/17, distant 60/51, second primary 6/4, death 15/6; local followed by distant 13/9 |
| K24_F2A_EFS | first events (pembro/placebo): progression precluding surgery 14/15, local 33/20, distant 77/56, second primary 16/10, death 19/13 |

两份补充材料的全部图（8 张，其中 KM 图 3 张；2024 年补充材料没有按 pCR 分层的 EFS）：

| pdf | figure | page | title | kaplan_meier | by_pcr |
|---|---|---|---|---|---|
| nejmoa2112651_appendix.pdf | S1 | 13 | Trial Enrollment and Outcomes of the Patients at the Fourth Interim Analysis | False | False |
| nejmoa2112651_appendix.pdf | S2 | 14 | Additional Subgroup Analyses for Event-Free Survival | False | False |
| nejmoa2112651_appendix.pdf | S3 | 15 | Kaplan-Meier Estimates of Distant Progression- or Distant Recurrence- Free Survival According to Treatment Group in the Intention-to-Treat Population | True | False |
| nejmoa2112651_appendix.pdf | S4 | 16 | Kaplan-Meier Estimates of Event-Free Survival by Pathological Complete Response (ypT0/Tis ypN0) According to Treatment Group in the Intention-to-Treat Population | True | True |
| nejmoa2409932_appendix.pdf | S1 | 12 | Trial Enrollment and Outcomes of the Patients at the Seventh Interim Analysis | False | False |
| nejmoa2409932_appendix.pdf | S2 | 13 | Additional Subgroup Analyses of Overall Survival | False | False |
| nejmoa2409932_appendix.pdf | S3 | 14 | Additional Subgroup Analyses of Event-Free Survival | False | False |
| nejmoa2409932_appendix.pdf | S4 | 15 | Kaplan-Meier Estimates of Overall Survival by Pathological Complete Response (ypT0/Tis ypN0) According to Treatment Group in the Intention-to-Treat Population | True | True |

栅格图里印的数字（风险表、里程碑、HR）从图像转录；与正文文字层的同一数值交叉核对 19 项，不一致 0 项（`data/transcription_checks.csv`）。报告值共 203 个，均由正则从 PDF 文字层抽取（`data/reported_values.csv`）。

## 3. 数字化（`data/digitized/`）

矢量图：PyMuPDF `get_drawings()` 读取阶梯路径。x 轴用全部带标签刻度最小二乘；y 轴用 0% 与 100% 两端刻度锚定（2024 年两图的 100% 刻度偏离等距，插图读数支持两端锚定）。

| fig_id | arm | legend_colour_matches_spec | n_vertices | n_censor_marks | s_first | t_last | calib_resid_x | calib_resid_y | inset_median_abs_diff |
|---|---|---|---|---|---|---|---|---|---|
| K20_F2_EFS | pembro | True | 101 | 385 |  99.9966 | 24.533 | 0.0005 | 0.0039 |  |
| K20_F2_EFS | placebo | True |  91 | 245 |  99.9966 | 24.466 | 0.0005 | 0.0039 |  |
| K22_F1_EFS | pembro | no legend sample | 214 | 661 |  99.9977 | 47.791 | 0.0009 | 0.0035 |  |
| K22_F1_EFS | placebo | no legend sample | 184 | 297 |  99.9977 | 46.941 | 0.0009 | 0.0035 |  |
| K22_F3_OS | pembro | no legend sample | 152 | 704 | 100.0007 | 47.891 | 0.0154 | 0.0035 |  |
| K22_F3_OS | placebo | no legend sample | 106 | 335 | 100.0007 | 46.947 | 0.0154 | 0.0035 |  |
| K24_F1A_OS | pembro | no legend sample | 230 | 669 | 100.0006 | 83.745 | 0.0014 | 0.1241 | 0.0030 |
| K24_F1A_OS | placebo | no legend sample | 179 | 305 | 100.0006 | 83.092 | 0.0014 | 0.1241 | 0.0030 |
| K24_F2A_EFS | pembro | no legend sample | 293 | 625 | 100.0364 | 83.607 | 0.0014 | 0.1172 | 0.0172 |
| K24_F2A_EFS | placebo | no legend sample | 238 | 276 | 100.0364 | 83.109 | 0.0014 | 0.1172 | 0.0172 |

栅格图：在嵌入图像的原生像素上做颜色分离（以更高 dpi 栅格化只会插值）。线条用单调阶梯的动态规划追踪；Yau 的「+」删失标记上下对称，NEJM 补充材料的删失标记只向上延伸、密集处连成色块，所以 NEJM 图追踪色块下沿。深色曲线的抗锯齿边缘会被误判为同色系浅色曲线，浅色类在深色曲线 2 像素内的像素剔除。

| fig_id | arm | native_px | dpi_as_placed | column_coverage | n_steps | t_last | s_last | calib_resid_x | calib_resid_y |
|---|---|---|---|---|---|---|---|---|---|
| Y22_F4A_EFS_TNBC | RCB0 | 1920x1881 | 300.0 | 0.9550 | 23 | 12.0000 | 83.652 | 0.0034 | 0.0537 |
| Y22_F4A_EFS_TNBC | RCB1 | 1920x1881 | 300.0 | 0.9669 | 30 | 12.0000 | 75.032 | 0.0034 | 0.0537 |
| Y22_F4A_EFS_TNBC | RCB2 | 1920x1881 | 300.0 | 0.9788 | 45 | 12.0000 | 58.630 | 0.0034 | 0.0537 |
| Y22_F4A_EFS_TNBC | RCB3 | 1920x1881 | 300.0 | 0.9974 | 61 | 12.0000 | 17.959 | 0.0034 | 0.0537 |
| K22_S3_DRFS | pembro | 1430x1106 | 220.0 | 0.9955 | 34 | 47.8297 | 86.834 | 0.0210 | 0.0336 |
| K22_S3_DRFS | placebo | 1430x1106 | 220.0 | 0.7989 | 42 | 46.9167 | 77.664 | 0.0210 | 0.0336 |
| K22_S4_EFS_pCR | pembro_pCR | 1282x1038 | 190.7 | 0.9957 | 11 | 47.8239 | 94.176 | 0.0261 | 0.0383 |
| K22_S4_EFS_pCR | placebo_pCR | 1282x1038 | 190.7 | 0.7670 | 10 | 47.0067 | 92.615 | 0.0261 | 0.0383 |
| K22_S4_EFS_pCR | pembro_nonpCR | 1282x1038 | 190.7 | 0.9237 | 49 | 47.2791 | 65.132 | 0.0261 | 0.0383 |
| K22_S4_EFS_pCR | placebo_nonpCR | 1282x1038 | 190.7 | 0.8690 | 58 | 46.7343 | 48.737 | 0.0261 | 0.0383 |
| K24_S4_OS_pCR | pembro_pCR | 1099x1143 | 203.9 | 0.9968 | 15 | 83.7535 | 94.178 | 0.0369 | 0.0627 |
| K24_S4_OS_pCR | placebo_pCR | 1099x1143 | 203.9 | 0.7231 | 13 | 83.0452 | 91.776 | 0.0369 | 0.0627 |
| K24_S4_OS_pCR | pembro_nonpCR | 1099x1143 | 203.9 | 0.9534 | 66 | 83.5765 | 66.465 | 0.0369 | 0.0627 |
| K24_S4_OS_pCR | placebo_nonpCR | 1099x1143 | 203.9 | 0.8883 | 52 | 83.1337 | 59.937 | 0.0369 | 0.0627 |

叠图质控：`data/digitized/qa/*_overlay.png`。

## 4. 个体数据重建与验证（`output/phase1/validation.csv`）

Guyot 2012 算法（`R/guyot.R`；`IPDfromKM::getIPD` 交叉核对）。重建时不输入报告的总事件数。门槛：里程碑差 ≤ 1 个百分点；Cox HR 差 ≤ 0.03；事件数差 ≤ 2%。

Yau 2022 只以里程碑为门槛（2026-10-21 的决定）。HR 不作门槛的理由：原文 HR 出自 12 个队列汇总、含队列效应的模型并使用全部随访，重建数据只到 12 年、只能做单一 Cox，估计量不同。事件数不作门槛的理由：参照值是从风险表推算的 12 年累计事件数（人数 − 在险 − 累计删失），原文没有报告。

| curve | check | time | unit | reported | reconstructed | abs_diff | tolerance | pass | gate | reference |
|---|---|---|---|---|---|---|---|---|---|---|
| K20_F2_EFS_pembro | milestone | 18 | months |  91.30 |  91.4053 | 0.1053 | 1 | 达标 | 是 | NEJMoa1910549 p6 |
| K20_F2_EFS_pembro | events |  |  |  58.00 |  57.0000 | 1.0000 | 2% (1.16) | 达标 | 是 | NEJMoa1910549 p1 |
| K20_F2_EFS_placebo | milestone | 18 | months |  85.30 |  85.3111 | 0.0111 | 1 | 达标 | 是 | NEJMoa1910549 p6 |
| K20_F2_EFS_placebo | events |  |  |  46.00 |  46.0000 | 0.0000 | 2% (0.92) | 达标 | 是 | NEJMoa1910549 p1 |
| K20_F2_EFS | hr |  |  |   0.63 |   0.6163 | 0.0137 | 0.03 | 达标 | 是 | NEJMoa1910549 p1 |
| K22_F1_EFS_pembro | milestone | 36 | months |  84.50 |  84.4726 | 0.0274 | 1 | 达标 | 是 | NEJMoa2112651 p5 |
| K22_F1_EFS_pembro | events |  |  | 123.00 | 123.0000 | 0.0000 | 2% (2.46) | 达标 | 是 | NEJMoa2112651 p5 |
| K22_F1_EFS_placebo | milestone | 36 | months |  76.80 |  76.7529 | 0.0471 | 1 | 达标 | 是 | NEJMoa2112651 p5 |
| K22_F1_EFS_placebo | events |  |  |  93.00 |  93.0000 | 0.0000 | 2% (1.86) | 达标 | 是 | NEJMoa2112651 p5 |
| K22_F1_EFS | hr |  |  |   0.63 |   0.6288 | 0.0012 | 0.03 | 达标 | 是 | NEJMoa2112651 p5 |
| K22_F3_OS_pembro | milestone | 36 | months |  89.70 |  89.7290 | 0.0290 | 1 | 达标 | 是 | NEJMoa2112651 p6 |
| K22_F3_OS_pembro | events |  |  |  80.00 |  80.0000 | 0.0000 | 2% (1.60) | 达标 | 是 | NEJMoa2112651 p6 |
| K22_F3_OS_placebo | milestone | 36 | months |  86.90 |  86.8641 | 0.0359 | 1 | 达标 | 是 | NEJMoa2112651 p6 |
| K22_F3_OS_placebo | events |  |  |  55.00 |  55.0000 | 0.0000 | 2% (1.10) | 达标 | 是 | NEJMoa2112651 p6 |
| K22_F3_OS | hr |  |  |   0.72 |   0.7213 | 0.0013 | 0.03 | 达标 | 是 | NEJMoa2112651 p6 |
| K24_F1A_OS_pembro | milestone | 36 | months |  89.50 |  89.5096 | 0.0096 | 1 | 达标 | 是 | NEJMoa2409932 p6 |
| K24_F1A_OS_pembro | milestone | 48 | months |  87.80 |  87.8410 | 0.0410 | 1 | 达标 | 是 | NEJMoa2409932 p6 |
| K24_F1A_OS_pembro | milestone | 60 | months |  86.60 |  86.5517 | 0.0483 | 1 | 达标 | 是 | NEJMoa2409932 p6 |
| K24_F1A_OS_pembro | events |  |  | 115.00 | 115.0000 | 0.0000 | 2% (2.30) | 达标 | 是 | NEJMoa2409932 p4 |
| K24_F1A_OS_placebo | milestone | 36 | months |  86.90 |  86.9029 | 0.0029 | 1 | 达标 | 是 | NEJMoa2409932 p6 |
| K24_F1A_OS_placebo | milestone | 48 | months |  83.50 |  83.5319 | 0.0319 | 1 | 达标 | 是 | NEJMoa2409932 p6 |
| K24_F1A_OS_placebo | milestone | 60 | months |  81.70 |  81.7063 | 0.0063 | 1 | 达标 | 是 | NEJMoa2409932 p6 |
| K24_F1A_OS_placebo | events |  |  |  85.00 |  85.0000 | 0.0000 | 2% (1.70) | 达标 | 是 | NEJMoa2409932 p4 |
| K24_F1A_OS | hr | 24 | months (before) |   0.87 |   0.8690 | 0.0010 | 0.03 | 达标 | 是 | NEJMoa2409932 p6 |
| K24_F1A_OS | hr | 24 | months (after) |   0.51 |   0.5105 | 0.0005 | 0.03 | 达标 | 是 | NEJMoa2409932 p6 |
| K24_F1A_OS | hr |  | overall |   0.66 |   0.6562 | 0.0038 | 0.03 | 达标 | 是 | nejmoa2409932_appendix p11 |
| K24_F2A_EFS_pembro | milestone | 60 | months |  81.20 |  81.2196 | 0.0196 | 1 | 达标 | 是 | NEJMoa2409932 p6 |
| K24_F2A_EFS_pembro | events |  |  | 159.00 | 159.0000 | 0.0000 | 2% (3.18) | 达标 | 是 | NEJMoa2409932 p6 |
| K24_F2A_EFS_placebo | milestone | 60 | months |  72.20 |  72.2182 | 0.0182 | 1 | 达标 | 是 | NEJMoa2409932 p6 |
| K24_F2A_EFS_placebo | events |  |  | 114.00 | 114.0000 | 0.0000 | 2% (2.28) | 达标 | 是 | NEJMoa2409932 p6 |
| K24_F2A_EFS | hr |  |  |   0.65 |   0.6551 | 0.0051 | 0.03 | 达标 | 是 | NEJMoa2409932 p6 |
| Y22_F4A_EFS_TNBC_RCB0 | milestone |  3 | years |  93.00 |  92.8647 | 0.1353 | 1 | 达标 | 是 | Yau2022_LancetOncol_appendix_mmc1 p5 |
| Y22_F4A_EFS_TNBC_RCB0 | milestone |  5 | years |  91.00 |  90.2264 | 0.7736 | 1 | 达标 | 是 | Yau2022_LancetOncol_appendix_mmc1 p5 |
| Y22_F4A_EFS_TNBC_RCB0 | milestone | 10 | years |  86.00 |  85.7378 | 0.2622 | 1 | 达标 | 是 | Yau2022_LancetOncol_appendix_mmc1 p5 |
| Y22_F4A_EFS_TNBC_RCB0 | events | 12 | years (cumulative) |  67.00 |  67.0000 | 0.0000 | 2% (1.34) | 达标 | 否（只报告） | figure risk table: N - at risk - censored at 12 y |
| Y22_F4A_EFS_TNBC_RCB1 | milestone |  3 | years |  84.00 |  84.3073 | 0.3073 | 1 | 达标 | 是 | Yau2022_LancetOncol_appendix_mmc1 p5 |
| Y22_F4A_EFS_TNBC_RCB1 | milestone |  5 | years |  80.00 |  79.9021 | 0.0979 | 1 | 达标 | 是 | Yau2022_LancetOncol_appendix_mmc1 p5 |
| Y22_F4A_EFS_TNBC_RCB1 | milestone | 10 | years |  75.00 |  75.3386 | 0.3386 | 1 | 达标 | 是 | Yau2022_LancetOncol_appendix_mmc1 p5 |
| Y22_F4A_EFS_TNBC_RCB1 | events | 12 | years (cumulative) |  41.00 |  40.0000 | 1.0000 | 2% (0.82) | **不达标** | 否（只报告） | figure risk table: N - at risk - censored at 12 y |
| Y22_F4A_EFS_TNBC_RCB2 | milestone |  3 | years |  70.00 |  70.1389 | 0.1389 | 1 | 达标 | 是 | Yau2022_LancetOncol_appendix_mmc1 p5 |
| Y22_F4A_EFS_TNBC_RCB2 | milestone |  5 | years |  66.00 |  66.1951 | 0.1951 | 1 | 达标 | 是 | Yau2022_LancetOncol_appendix_mmc1 p5 |
| Y22_F4A_EFS_TNBC_RCB2 | milestone | 10 | years |  61.00 |  61.3117 | 0.3117 | 1 | 达标 | 是 | Yau2022_LancetOncol_appendix_mmc1 p5 |
| Y22_F4A_EFS_TNBC_RCB2 | events | 12 | years (cumulative) | 189.00 | 185.0000 | 4.0000 | 2% (3.78) | **不达标** | 否（只报告） | figure risk table: N - at risk - censored at 12 y |
| Y22_F4A_EFS_TNBC_RCB3 | milestone |  3 | years |  32.00 |  31.4421 | 0.5579 | 1 | 达标 | 是 | Yau2022_LancetOncol_appendix_mmc1 p5 |
| Y22_F4A_EFS_TNBC_RCB3 | milestone |  5 | years |  28.00 |  28.0990 | 0.0990 | 1 | 达标 | 是 | Yau2022_LancetOncol_appendix_mmc1 p5 |
| Y22_F4A_EFS_TNBC_RCB3 | milestone | 10 | years |  25.00 |  25.4534 | 0.4534 | 1 | 达标 | 是 | Yau2022_LancetOncol_appendix_mmc1 p5 |
| Y22_F4A_EFS_TNBC_RCB3 | events | 12 | years (cumulative) | 144.00 | 142.0000 | 2.0000 | 2% (2.88) | 达标 | 否（只报告） | figure risk table: N - at risk - censored at 12 y |
| Y22_F4A_EFS_TNBC | hr |  | RCB-1 vs RCB-0 |   2.16 |   2.1576 | 0.0024 | 0.03 | 达标 | 否（只报告） | Yau2022_LancetOncol_appendix_mmc1 p5 |
| Y22_F4A_EFS_TNBC | hr |  | RCB-2 vs RCB-0 |   3.94 |   4.0855 | 0.1455 | 0.03 | **不达标** | 否（只报告） | Yau2022_LancetOncol_appendix_mmc1 p5 |
| Y22_F4A_EFS_TNBC | hr |  | RCB-3 vs RCB-0 |  13.04 |  13.3204 | 0.2804 | 0.03 | **不达标** | 否（只报告） | Yau2022_LancetOncol_appendix_mmc1 p5 |
| K22_S3_DRFS_pembro | milestone | 36 | months |  87.00 |  87.1576 | 0.1576 | 1 | 达标 | 是 | nejmoa2112651_appendix p15 (printed in figure, transcribed) |
| K22_S3_DRFS_placebo | milestone | 36 | months |  80.70 |  80.6318 | 0.0682 | 1 | 达标 | 是 | nejmoa2112651_appendix p15 (printed in figure, transcribed) |
| K22_S3_DRFS | hr |  |  |   0.61 |   0.6098 | 0.0002 | 0.03 | 达标 | 是 | NEJMoa2112651 p6 |
| K22_S4_EFS_pCR_pembro_pCR | milestone | 36 | months |  94.40 |  94.0889 | 0.3111 | 1 | 达标 | 是 | nejmoa2112651_appendix p16 (printed in figure, transcribed) |
| K22_S4_EFS_pCR_placebo_pCR | milestone | 36 | months |  92.50 |  92.5080 | 0.0080 | 1 | 达标 | 是 | nejmoa2112651_appendix p16 (printed in figure, transcribed) |
| K22_S4_EFS_pCR_pembro_nonpCR | milestone | 36 | months |  67.40 |  67.2985 | 0.1015 | 1 | 达标 | 是 | nejmoa2112651_appendix p16 (printed in figure, transcribed) |
| K22_S4_EFS_pCR_placebo_nonpCR | milestone | 36 | months |  56.80 |  56.8165 | 0.0165 | 1 | 达标 | 是 | nejmoa2112651_appendix p16 (printed in figure, transcribed) |
| K22_S4_EFS_pCR_pembro_pCR | events |  |  |  27.00 |  27.0000 | 0.0000 | 2% (0.54) | 达标 | 是 | NEJMoa2112651 p6 |
| K22_S4_EFS_pCR_pembro_nonpCR | events |  |  |  96.00 |  96.0000 | 0.0000 | 2% (1.92) | 达标 | 是 | NEJMoa2112651 p6 |
| K22_S4_EFS_pCR_placebo_pCR | events |  |  |  16.00 |  16.0000 | 0.0000 | 2% (0.32) | 达标 | 是 | NEJMoa2112651 p6 |
| K22_S4_EFS_pCR_placebo_nonpCR | events |  |  |  77.00 |  77.0000 | 0.0000 | 2% (1.54) | 达标 | 是 | NEJMoa2112651 p6 |
| K22_S4_EFS_pCR | hr |  | pCR |   0.73 |   0.7224 | 0.0076 | 0.03 | 达标 | 是 | NEJMoa2112651 p6 |
| K22_S4_EFS_pCR | hr |  | non-pCR |   0.70 |   0.7117 | 0.0117 | 0.03 | 达标 | 是 | NEJMoa2112651 p6 |
| K22_S4_EFS_pCR | hr |  | pCR (user-supplied reference) |   0.65 |   0.7224 | 0.0724 | 0.03 | **不达标** | 是 | input/user_supplied_values.csv |
| K22_S4_EFS_pCR | hr |  | nonpCR (user-supplied reference) |   0.72 |   0.7117 | 0.0083 | 0.03 | 达标 | 是 | input/user_supplied_values.csv |
| K24_S4_OS_pCR_pembro_pCR | events |  |  |  27.00 |  27.0000 | 0.0000 | 2% (0.54) | 达标 | 是 | NEJMoa2409932 p6 |
| K24_S4_OS_pCR_pembro_nonpCR | events |  |  |  88.00 |  88.0000 | 0.0000 | 2% (1.76) | 达标 | 是 | NEJMoa2409932 p6 |
| K24_S4_OS_pCR_placebo_pCR | events |  |  |  17.00 |  17.0000 | 0.0000 | 2% (0.34) | 达标 | 是 | NEJMoa2409932 p6 |
| K24_S4_OS_pCR_placebo_nonpCR | events |  |  |  68.00 |  68.0000 | 0.0000 | 2% (1.36) | 达标 | 是 | NEJMoa2409932 p6 |
| K24_S4_OS_pCR_pCR | milestone_diff | 60 | months (pembro - placebo) |   0.70 |   0.7061 | 0.0061 | 1 | 达标 | 是 | NEJMoa2409932 p6 |
| K24_S4_OS_pCR_nonpCR | milestone_diff | 60 | months (pembro - placebo) |   6.10 |   6.2010 | 0.1010 | 1 | 达标 | 是 | NEJMoa2409932 p6 |

诊断（不作门槛）：

| curve | n | events_guyot | events_ipdfromkm | max_abs_km_vs_digitized_pp | max_abs_guyot_vs_ipdfromkm_pp | max_abs_risk_table_diff | censor_marks_drawn | censored_guyot |
|---|---|---|---|---|---|---|---|---|
| K20_F2_EFS_pembro | 784 |  57 |  55 | 0.114 | 0.356 | 0 | 385 | 727 |
| K20_F2_EFS_placebo | 390 |  46 |  45 | 0.173 | 0.751 | 0 | 245 | 344 |
| K22_F1_EFS_pembro | 784 | 123 | 122 | 0.035 | 0.239 | 0 | 661 | 661 |
| K22_F1_EFS_placebo | 390 |  93 |  92 | 0.442 | 1.209 | 1 | 297 | 297 |
| K22_F3_OS_pembro | 784 |  80 |  80 | 0.024 | 0.070 | 1 | 704 | 704 |
| K22_F3_OS_placebo | 390 |  55 |  55 | 0.043 | 0.163 | 0 | 335 | 335 |
| K24_F1A_OS_pembro | 784 | 115 | 115 | 0.222 | 0.001 | 0 | 669 | 669 |
| K24_F1A_OS_placebo | 390 |  85 |  85 | 0.065 | 0.001 | 0 | 305 | 305 |
| K24_F2A_EFS_pembro | 784 | 159 | 159 | 0.183 | 0.293 | 0 | 625 | 625 |
| K24_F2A_EFS_placebo | 390 | 114 | 114 | 0.046 | 0.088 | 0 | 276 | 276 |
| Y22_F4A_EFS_TNBC_RCB0 | 770 |  67 |  66 | 0.161 | 0.381 | 0 |  | 703 |
| Y22_F4A_EFS_TNBC_RCB1 | 212 |  40 |  40 | 0.348 | 0.552 | 0 |  | 172 |
| Y22_F4A_EFS_TNBC_RCB2 | 590 | 185 | 182 | 0.272 | 0.760 | 0 |  | 405 |
| Y22_F4A_EFS_TNBC_RCB3 | 202 | 142 | 142 | 0.430 | 1.719 | 0 |  |  60 |
| K22_S3_DRFS_pembro | 784 | 100 |  99 | 0.078 | 0.127 | 1 |  | 684 |
| K22_S3_DRFS_placebo | 390 |  79 |  79 | 0.149 | 0.350 | 1 |  | 311 |
| K22_S4_EFS_pCR_pembro_pCR | 494 |  27 |  26 | 0.100 | 0.205 | 1 |  | 467 |
| K22_S4_EFS_pCR_placebo_pCR | 217 |  16 |  16 | 0.220 | 0.055 | 1 |  | 201 |
| K22_S4_EFS_pCR_pembro_nonpCR | 290 |  96 |  95 | 0.176 | 0.382 | 2 |  | 194 |
| K22_S4_EFS_pCR_placebo_nonpCR | 173 |  77 |  77 | 1.201 | 3.368 | 1 |  |  96 |
| K24_S4_OS_pCR_pembro_pCR | 495 |  27 |  27 | 0.093 | 0.351 | 1 |  | 468 |
| K24_S4_OS_pCR_placebo_pCR | 217 |  17 |  16 | 0.106 | 0.493 | 2 |  | 200 |
| K24_S4_OS_pCR_pembro_nonpCR | 289 |  88 |  88 | 0.607 | 0.269 | 1 |  | 201 |
| K24_S4_OS_pCR_placebo_nonpCR | 173 |  68 |  67 | 0.273 | 0.526 | 2 |  | 105 |

2022 和 2024 年正文矢量图上每个删失病例都画了标记；每个风险区间内的「图上标记数/Guyot 删失数」见 `validation_diagnostics.csv`。图：`fig_validation_*.png`。

## 5. 一致性检查（`output/phase1/consistency_check.csv`）

2022 年 Fig. S4 的分层 KM 按 pCR 比例（帕博利珠单抗 0.6301，安慰剂 0.5564）加权混合，与整体 EFS 比较，时点为 3 个月至 42 个月（四层在险均 ≥ 20），门槛 1 个百分点。不达标 0 处。

| arm | comparator | max_abs_diff |
|---|---|---|
| pembro | K22_F1_EFS | 0.293 |
| placebo | K22_F1_EFS | 0.356 |
| pembro | K24_F2A_EFS | 0.421 |
| placebo | K24_F2A_EFS | 0.452 |

图：`fig_consistency_pCR_mixture.png`。

## 6. 拟合与模型选择（步骤 4）

数据：4 条 EFS（2022 年 Fig. S4，臂 × pCR）在手术时点（随机化后 7 个月）做 landmark；2 条 OS（2024 年 Fig. 1A，按臂）从随机化起。候选 15 个：6 个标准分布、6 个 RP 样条（1 至 3 个内结点，累积风险与累积比值尺度）、3 个相对生存混合治愈模型（Weibull、对数正态、对数 logistic；背景为日本女性生命表，治愈比例作用于超额死亡）。AIC/BIC 用全因对数似然，使治愈模型与全因模型可比。

选择规则（拟合前固定）：
1. 与 KM 的重合：模型曲线落在 KM 逐点 95% CI 内的月份比例 ≥ 0.95（在险 ≥ 20 的时点）。最初定为全部时点（100%），结果 6 条中有 3 条没有任何候选达到；逐点 95% CI 下真实曲线也约有 5% 的时点在区间外，故第一次运行后改为 95%。
2. 风险形状：超额风险不晚于术后 3 年达峰，3→5→10 年递减（EFS）；OS 为 5→10→20 年递减；10 年和 20 年的全因风险不低于背景。
3. 外部长期数据（只用于 EFS）：术后 5 至 10 年的条件 EFS S(10)/S(5)，与 Yau 2022 TNBC 在 0.5 年 landmark 后的同一量比较（pCR 对 RCB-0，非 pCR 对 RCB-1 至 3 合并）。Yau 没有 OS，OS 无第 3 条。
满足 1 和 2 的模型中保留 AIC 差 ≤ 4 者；EFS 取第 3 条最接近 Yau 的，OS 取 AIC 最小的。

Yau 的参照值（`yau_landmark_reference.csv`）：

| group | S5 | S10 | C5_10 |
|---|---|---|---|
| RCB0 | 0.9023 | 0.8574 | 0.9503 |
| RCB1_3 | 0.6045 | 0.5598 | 0.9260 |

选定的模型与理由（`model_selection.csv`）：

| curve | model | AIC | S5 | S10 | S20 | cure_fraction | reason |
|---|---|---|---|---|---|---|---|
| EFS_pembro_pCR | llogis |  259.70 | 91.63 | 87.17 | 80.83 |  | 15/15 converged; 0 fail criterion 1 (KM 95% CI), 3 more fail criterion 2 (hazard shape / below background); 12 eligible, 10 within 4 AIC of the best eligible (llogis, AIC 259.7); chosen as closest to Yau on S(10)/S(5): model 0.951 vs Yau RCB0 0.950 |
| EFS_placebo_pCR | lnorm |  145.28 | 88.48 | 82.89 | 75.83 |  | 15/15 converged; 1 fail criterion 1 (KM 95% CI), 7 more fail criterion 2 (hazard shape / below background); 7 eligible, 7 within 4 AIC of the best eligible (cure_weibull, AIC 143.2); chosen as closest to Yau on S(10)/S(5): model 0.937 vs Yau RCB0 0.950 |
| EFS_pembro_nonpCR | cure_llogis |  460.89 | 63.06 | 57.10 | 51.47 | 0.5007 | 15/15 converged; 1 fail criterion 1 (KM 95% CI), 1 more fail criterion 2 (hazard shape / below background); 13 eligible, 13 within 4 AIC of the best eligible (lnorm, AIC 459.5); chosen as closest to Yau on S(10)/S(5): model 0.905 vs Yau RCB1_3 0.926 |
| EFS_placebo_nonpCR | cure_weibull |  331.31 | 53.03 | 51.82 | 49.70 | 0.5283 | 15/15 converged; 0 fail criterion 1 (KM 95% CI), 1 more fail criterion 2 (hazard shape / below background); 14 eligible, 14 within 4 AIC of the best eligible (lnorm, AIC 331.2); chosen as closest to Yau on S(10)/S(5): model 0.977 vs Yau RCB1_3 0.926 |
| OS_pembro | cure_lnorm | 1041.23 | 86.42 | 83.27 | 79.42 | 0.8406 | 15/15 converged; 6 fail criterion 1 (KM 95% CI), 5 more fail criterion 2 (hazard shape / below background); 4 eligible, 4 within 4 AIC of the best eligible (cure_lnorm, AIC 1041.2); chosen as lowest AIC (no external OS data for criterion 3) |
| OS_placebo | rp_hazard_k2 |  702.91 | 81.10 | 70.20 | 55.04 |  | 15/15 converged; 7 fail criterion 1 (KM 95% CI), 0 more fail criterion 2 (hazard shape / below background); 8 eligible, 7 within 4 AIC of the best eligible (rp_hazard_k2, AIC 702.9); chosen as lowest AIC (no external OS data for criterion 3) |

S5/S10/S20 为所选模型的全因生存（%）：EFS 为术后年数，OS 为随机化后年数。

全部候选的比较（`model_comparison.csv`）：

| curve | model | AIC | BIC | c1_frac_inside_ci | c1_max_abs_diff_pp | c1_pass | peak_excess_haz_year | c2_pass | S5 | S10 | S20 | cond_5_10 | yau_cond_5_10 | within_aic_window | selected |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EFS_pembro_pCR | exp |  262.49 |  266.70 | 1.0000 | 1.240 | TRUE |  0.02 | TRUE | 89.65 | 80.38 | 64.61 | 0.8965 | 0.9503 | TRUE | FALSE |
| EFS_pembro_pCR | weibull |  259.71 |  268.12 | 1.0000 | 0.668 | TRUE |  0.02 | TRUE | 91.56 | 86.83 | 79.77 | 0.9484 | 0.9503 | TRUE | FALSE |
| EFS_pembro_pCR | lnorm |  259.35 |  267.76 | 1.0000 | 0.694 | TRUE |  0.02 | FALSE | 92.11 | 88.79 | 84.58 | 0.9640 | 0.9503 | FALSE | FALSE |
| EFS_pembro_pCR | llogis |  259.70 |  268.10 | 1.0000 | 0.663 | TRUE |  0.02 | TRUE | 91.63 | 87.17 | 80.83 | 0.9513 | 0.9503 | TRUE | TRUE |
| EFS_pembro_pCR | gompertz |  261.11 |  269.52 | 1.0000 | 0.750 | TRUE |  0.02 | FALSE | 92.93 | 92.26 | 92.18 | 0.9927 | 0.9503 | FALSE | FALSE |
| EFS_pembro_pCR | gengamma |  261.74 |  274.35 | 1.0000 | 0.675 | TRUE |  0.02 | TRUE | 91.48 | 86.46 | 78.47 | 0.9451 | 0.9503 | TRUE | FALSE |
| EFS_pembro_pCR | rp_hazard_k1 |  261.55 |  274.16 | 1.0000 | 0.672 | TRUE |  0.02 | TRUE | 91.81 | 87.62 | 81.50 | 0.9543 | 0.9503 | TRUE | FALSE |
| EFS_pembro_pCR | rp_hazard_k2 |  263.03 |  279.84 | 1.0000 | 0.690 | TRUE |  0.02 | TRUE | 91.30 | 86.02 | 77.94 | 0.9422 | 0.9503 | TRUE | FALSE |
| EFS_pembro_pCR | rp_hazard_k3 |  265.04 |  286.05 | 1.0000 | 0.704 | TRUE |  0.02 | TRUE | 91.12 | 85.41 | 76.55 | 0.9374 | 0.9503 | FALSE | FALSE |
| EFS_pembro_pCR | rp_odds_k1 |  261.56 |  274.17 | 1.0000 | 0.674 | TRUE |  0.02 | FALSE | 91.86 | 87.84 | 82.22 | 0.9562 | 0.9503 | FALSE | FALSE |
| EFS_pembro_pCR | rp_odds_k2 |  263.02 |  279.83 | 1.0000 | 0.688 | TRUE |  0.02 | TRUE | 91.35 | 86.31 | 79.00 | 0.9448 | 0.9503 | TRUE | FALSE |
| EFS_pembro_pCR | rp_odds_k3 |  265.03 |  286.04 | 1.0000 | 0.702 | TRUE |  0.02 | TRUE | 91.16 | 85.71 | 77.72 | 0.9402 | 0.9503 | FALSE | FALSE |
| EFS_pembro_pCR | cure_weibull |  261.70 |  274.31 | 1.0000 | 0.674 | TRUE |  0.02 | TRUE | 91.89 | 88.16 | 82.13 | 0.9594 | 0.9503 | TRUE | FALSE |
| EFS_pembro_pCR | cure_lnorm |  261.34 |  273.94 | 1.0000 | 0.686 | TRUE |  0.02 | TRUE | 92.02 | 88.19 | 81.32 | 0.9585 | 0.9503 | TRUE | FALSE |
| EFS_pembro_pCR | cure_llogis |  261.68 |  274.29 | 1.0000 | 0.678 | TRUE |  0.02 | TRUE | 91.90 | 88.09 | 81.60 | 0.9585 | 0.9503 | TRUE | FALSE |
| EFS_placebo_pCR | exp |  146.07 |  149.45 | 0.9722 | 2.330 | TRUE |  0.02 | TRUE | 86.01 | 73.98 | 54.74 | 0.8601 | 0.9503 | TRUE | FALSE |
| EFS_placebo_pCR | weibull |  146.80 |  153.56 | 0.9722 | 1.740 | TRUE |  0.02 | TRUE | 87.92 | 80.30 | 68.82 | 0.9134 | 0.9503 | TRUE | FALSE |
| EFS_placebo_pCR | lnorm |  145.28 |  152.04 | 0.9722 | 1.587 | TRUE |  0.06 | TRUE | 88.48 | 82.89 | 75.83 | 0.9369 | 0.9503 | TRUE | TRUE |
| EFS_placebo_pCR | llogis |  146.62 |  153.38 | 0.9722 | 1.698 | TRUE |  0.02 | TRUE | 88.00 | 80.94 | 71.10 | 0.9198 | 0.9503 | TRUE | FALSE |
| EFS_placebo_pCR | gompertz |  143.48 |  150.24 | 0.9444 | 1.437 | FALSE |  0.02 | FALSE | 91.47 | 91.25 | 91.25 | 0.9976 | 0.9503 | FALSE | FALSE |
| EFS_placebo_pCR | gengamma |  144.90 |  155.04 | 0.9722 | 1.138 | TRUE |  0.22 | FALSE | 90.29 | 87.91 | 85.55 | 0.9736 | 0.9503 | FALSE | FALSE |
| EFS_placebo_pCR | rp_hazard_k1 |  145.04 |  155.18 | 0.9722 | 1.020 | TRUE |  0.40 | FALSE | 90.22 | 87.01 | 82.86 | 0.9645 | 0.9503 | FALSE | FALSE |
| EFS_placebo_pCR | rp_hazard_k2 |  146.38 |  159.90 | 0.9722 | 1.152 | TRUE |  0.64 | FALSE | 90.82 | 88.60 | 85.88 | 0.9755 | 0.9503 | FALSE | FALSE |
| EFS_placebo_pCR | rp_hazard_k3 |  148.06 |  164.96 | 0.9722 | 1.177 | TRUE |  0.76 | FALSE | 91.03 | 89.12 | 86.83 | 0.9790 | 0.9503 | FALSE | FALSE |
| EFS_placebo_pCR | rp_odds_k1 |  145.04 |  155.18 | 0.9722 | 1.020 | TRUE |  0.40 | FALSE | 90.22 | 87.07 | 83.11 | 0.9651 | 0.9503 | FALSE | FALSE |
| EFS_placebo_pCR | rp_odds_k2 |  146.38 |  159.90 | 0.9722 | 1.149 | TRUE |  0.64 | FALSE | 90.82 | 88.63 | 85.99 | 0.9758 | 0.9503 | FALSE | FALSE |
| EFS_placebo_pCR | rp_odds_k3 |  148.07 |  164.97 | 0.9722 | 1.171 | TRUE |  0.72 | FALSE | 91.03 | 89.13 | 86.89 | 0.9792 | 0.9503 | FALSE | FALSE |
| EFS_placebo_pCR | cure_weibull |  143.20 |  153.34 | 0.9722 | 1.131 | TRUE |  0.54 | TRUE | 91.98 | 90.94 | 87.22 | 0.9886 | 0.9503 | TRUE | FALSE |
| EFS_placebo_pCR | cure_lnorm |  144.19 |  154.33 | 0.9722 | 1.049 | TRUE |  0.32 | TRUE | 91.22 | 89.87 | 86.13 | 0.9852 | 0.9503 | TRUE | FALSE |
| EFS_placebo_pCR | cure_llogis |  143.85 |  153.99 | 0.9722 | 1.010 | TRUE |  0.46 | TRUE | 91.40 | 90.12 | 86.36 | 0.9859 | 0.9503 | TRUE | FALSE |
| EFS_pembro_nonpCR | exp |  477.58 |  481.19 | 0.6389 | 6.287 | FALSE |  0.02 | TRUE | 48.60 | 23.62 |  5.58 | 0.4860 | 0.9260 | FALSE | FALSE |
| EFS_pembro_nonpCR | weibull |  462.59 |  469.80 | 1.0000 | 2.959 | TRUE |  0.02 | TRUE | 57.26 | 41.25 | 24.50 | 0.7204 | 0.9260 | TRUE | FALSE |
| EFS_pembro_nonpCR | lnorm |  459.49 |  466.70 | 1.0000 | 1.959 | TRUE |  0.02 | TRUE | 60.63 | 50.04 | 39.45 | 0.8253 | 0.9260 | TRUE | FALSE |
| EFS_pembro_nonpCR | llogis |  461.05 |  468.26 | 1.0000 | 2.437 | TRUE |  0.02 | TRUE | 58.63 | 46.03 | 33.92 | 0.7851 | 0.9260 | TRUE | FALSE |
| EFS_pembro_nonpCR | gompertz |  458.95 |  466.16 | 1.0000 | 1.486 | TRUE |  0.02 | FALSE | 66.07 | 65.22 | 65.19 | 0.9871 | 0.9260 | FALSE | FALSE |
| EFS_pembro_nonpCR | gengamma |  461.48 |  472.30 | 1.0000 | 2.032 | TRUE |  0.02 | TRUE | 60.82 | 50.45 | 40.11 | 0.8296 | 0.9260 | TRUE | FALSE |
| EFS_pembro_nonpCR | rp_hazard_k1 |  462.26 |  473.08 | 1.0000 | 1.990 | TRUE |  0.02 | TRUE | 59.89 | 47.11 | 33.12 | 0.7866 | 0.9260 | TRUE | FALSE |
| EFS_pembro_nonpCR | rp_hazard_k2 |  462.80 |  477.22 | 1.0000 | 1.587 | TRUE |  0.02 | TRUE | 61.91 | 51.82 | 40.60 | 0.8369 | 0.9260 | TRUE | FALSE |
| EFS_pembro_nonpCR | rp_hazard_k3 |  462.94 |  480.97 | 1.0000 | 1.007 | TRUE |  0.02 | TRUE | 63.59 | 55.76 | 47.07 | 0.8769 | 0.9260 | TRUE | FALSE |
| EFS_pembro_nonpCR | rp_odds_k1 |  461.96 |  472.78 | 1.0000 | 1.900 | TRUE |  0.02 | TRUE | 60.34 | 49.27 | 38.27 | 0.8166 | 0.9260 | TRUE | FALSE |
| EFS_pembro_nonpCR | rp_odds_k2 |  462.84 |  477.27 | 1.0000 | 1.612 | TRUE |  0.02 | TRUE | 62.08 | 52.87 | 43.46 | 0.8516 | 0.9260 | TRUE | FALSE |
| EFS_pembro_nonpCR | rp_odds_k3 |  462.92 |  480.95 | 1.0000 | 0.999 | TRUE |  0.02 | TRUE | 63.71 | 56.46 | 48.92 | 0.8862 | 0.9260 | TRUE | FALSE |
| EFS_pembro_nonpCR | cure_weibull |  460.33 |  471.15 | 1.0000 | 1.762 | TRUE |  0.02 | TRUE | 65.18 | 63.12 | 60.45 | 0.9684 | 0.9260 | TRUE | FALSE |
| EFS_pembro_nonpCR | cure_lnorm |  461.45 |  472.27 | 1.0000 | 2.115 | TRUE |  0.02 | TRUE | 61.17 | 51.30 | 40.88 | 0.8386 | 0.9260 | TRUE | FALSE |
| EFS_pembro_nonpCR | cure_llogis |  460.89 |  471.71 | 1.0000 | 1.862 | TRUE |  0.02 | TRUE | 63.06 | 57.10 | 51.47 | 0.9054 | 0.9260 | TRUE | TRUE |
| EFS_placebo_nonpCR | exp |  332.56 |  335.62 | 1.0000 | 4.941 | TRUE |  0.02 | TRUE | 35.80 | 12.81 |  1.64 | 0.3580 | 0.9260 | TRUE | FALSE |
| EFS_placebo_nonpCR | weibull |  333.51 |  339.63 | 1.0000 | 4.219 | TRUE |  0.02 | TRUE | 38.98 | 17.44 |  3.93 | 0.4474 | 0.9260 | TRUE | FALSE |
| EFS_placebo_nonpCR | lnorm |  331.23 |  337.35 | 1.0000 | 2.918 | TRUE |  0.20 | TRUE | 44.99 | 30.37 | 18.36 | 0.6750 | 0.9260 | TRUE | FALSE |
| EFS_placebo_nonpCR | llogis |  331.49 |  337.62 | 1.0000 | 3.213 | TRUE |  0.10 | TRUE | 42.15 | 26.40 | 15.00 | 0.6262 | 0.9260 | TRUE | FALSE |
| EFS_placebo_nonpCR | gompertz |  330.87 |  337.00 | 1.0000 | 3.093 | TRUE |  0.02 | FALSE | 47.60 | 40.55 | 38.88 | 0.8520 | 0.9260 | FALSE | FALSE |
| EFS_placebo_nonpCR | gengamma |  333.11 |  342.30 | 1.0000 | 3.086 | TRUE |  0.18 | TRUE | 43.93 | 28.29 | 15.71 | 0.6440 | 0.9260 | TRUE | FALSE |
| EFS_placebo_nonpCR | rp_hazard_k1 |  333.05 |  342.24 | 1.0000 | 2.852 | TRUE |  0.28 | TRUE | 43.64 | 25.71 | 10.80 | 0.5890 | 0.9260 | TRUE | FALSE |
| EFS_placebo_nonpCR | rp_hazard_k2 |  331.85 |  344.10 | 1.0000 | 1.827 | TRUE |  0.86 | TRUE | 49.04 | 37.20 | 25.34 | 0.7585 | 0.9260 | TRUE | FALSE |
| EFS_placebo_nonpCR | rp_hazard_k3 |  333.86 |  349.18 | 1.0000 | 1.770 | TRUE |  0.78 | TRUE | 49.12 | 37.36 | 25.57 | 0.7606 | 0.9260 | TRUE | FALSE |
| EFS_placebo_nonpCR | rp_odds_k1 |  332.69 |  341.88 | 1.0000 | 2.759 | TRUE |  0.28 | TRUE | 44.54 | 30.00 | 18.61 | 0.6735 | 0.9260 | TRUE | FALSE |
| EFS_placebo_nonpCR | rp_odds_k2 |  331.93 |  344.18 | 1.0000 | 1.880 | TRUE |  0.82 | TRUE | 49.33 | 38.83 | 29.27 | 0.7871 | 0.9260 | TRUE | FALSE |
| EFS_placebo_nonpCR | rp_odds_k3 |  333.96 |  349.27 | 1.0000 | 1.753 | TRUE |  0.82 | TRUE | 49.51 | 39.19 | 29.76 | 0.7916 | 0.9260 | TRUE | FALSE |
| EFS_placebo_nonpCR | cure_weibull |  331.31 |  340.49 | 1.0000 | 1.926 | TRUE |  0.50 | TRUE | 53.03 | 51.82 | 49.70 | 0.9771 | 0.9260 | TRUE | TRUE |
| EFS_placebo_nonpCR | cure_lnorm |  333.23 |  342.41 | 1.0000 | 2.864 | TRUE |  0.20 | TRUE | 45.29 | 31.14 | 19.42 | 0.6876 | 0.9260 | TRUE | FALSE |
| EFS_placebo_nonpCR | cure_llogis |  331.53 |  340.71 | 1.0000 | 2.152 | TRUE |  0.44 | TRUE | 49.55 | 43.24 | 38.86 | 0.8728 | 0.9260 | TRUE | FALSE |
| OS_pembro | exp | 1071.99 | 1076.65 | 0.5904 | 3.232 | FALSE |  0.02 | TRUE | 87.84 | 77.15 | 59.53 |  |  | FALSE | FALSE |
| OS_pembro | weibull | 1071.88 | 1081.21 | 0.7590 | 2.545 | FALSE |  0.02 | TRUE | 87.60 | 78.38 | 63.89 |  |  | FALSE | FALSE |
| OS_pembro | lnorm | 1059.27 | 1068.60 | 0.8795 | 2.379 | FALSE |  0.64 | TRUE | 87.25 | 79.24 | 68.84 |  |  | FALSE | FALSE |
| OS_pembro | llogis | 1069.57 | 1078.90 | 0.8072 | 2.454 | FALSE |  0.02 | TRUE | 87.42 | 78.59 | 65.96 |  |  | FALSE | FALSE |
| OS_pembro | gompertz | 1059.78 | 1069.11 | 0.8675 | 1.690 | FALSE |  0.02 | FALSE | 86.84 | 82.38 | 80.18 |  |  | FALSE | FALSE |
| OS_pembro | gengamma | 1042.81 | 1056.80 | 0.9759 | 1.186 | TRUE |  0.80 | FALSE | 86.79 | 81.93 | 77.20 |  |  | FALSE | FALSE |
| OS_pembro | rp_hazard_k1 | 1039.61 | 1053.60 | 0.9759 | 0.743 | TRUE |  1.24 | FALSE | 86.52 | 82.35 | 77.13 |  |  | FALSE | FALSE |
| OS_pembro | rp_hazard_k2 | 1041.70 | 1060.36 | 0.9759 | 0.686 | TRUE |  1.14 | FALSE | 86.58 | 82.17 | 76.58 |  |  | FALSE | FALSE |
| OS_pembro | rp_hazard_k3 | 1042.50 | 1065.82 | 0.9759 | 0.529 | TRUE |  1.40 | TRUE | 86.69 | 81.82 | 75.47 |  |  | TRUE | FALSE |
| OS_pembro | rp_odds_k1 | 1039.58 | 1053.58 | 0.9759 | 0.729 | TRUE |  1.22 | FALSE | 86.52 | 82.37 | 77.32 |  |  | FALSE | FALSE |
| OS_pembro | rp_odds_k2 | 1041.74 | 1060.40 | 0.9759 | 0.695 | TRUE |  1.14 | FALSE | 86.58 | 82.23 | 76.89 |  |  | FALSE | FALSE |
| OS_pembro | rp_odds_k3 | 1042.51 | 1065.83 | 0.9759 | 0.532 | TRUE |  1.40 | TRUE | 86.68 | 81.87 | 75.83 |  |  | TRUE | FALSE |
| OS_pembro | cure_weibull | 1049.00 | 1062.99 | 0.9398 | 1.334 | FALSE |  1.44 | TRUE | 86.31 | 84.09 | 80.80 |  |  | FALSE | FALSE |
| OS_pembro | cure_lnorm | 1041.23 | 1055.22 | 0.9759 | 0.883 | TRUE |  1.10 | TRUE | 86.42 | 83.27 | 79.42 |  |  | TRUE | TRUE |
| OS_pembro | cure_llogis | 1042.74 | 1056.74 | 0.9759 | 0.854 | TRUE |  1.32 | TRUE | 86.33 | 83.57 | 79.79 |  |  | TRUE | FALSE |
| OS_placebo | exp |  719.38 |  723.34 | 0.8193 | 3.017 | FALSE |  0.06 | TRUE | 81.89 | 67.06 | 44.97 |  |  | FALSE | FALSE |
| OS_placebo | weibull |  720.35 |  728.28 | 0.8313 | 2.930 | FALSE | 15.98 | FALSE | 82.17 | 65.38 | 39.87 |  |  | FALSE | FALSE |
| OS_placebo | lnorm |  711.25 |  719.19 | 0.8795 | 2.473 | FALSE |  1.98 | TRUE | 81.56 | 67.61 | 50.59 |  |  | FALSE | FALSE |
| OS_placebo | llogis |  718.10 |  726.03 | 0.8313 | 2.693 | FALSE |  3.98 | TRUE | 81.80 | 66.27 | 46.20 |  |  | FALSE | FALSE |
| OS_placebo | gompertz |  720.88 |  728.82 | 0.8193 | 3.470 | FALSE |  0.02 | TRUE | 81.58 | 69.14 | 54.22 |  |  | FALSE | FALSE |
| OS_placebo | gengamma |  705.46 |  717.36 | 0.9398 | 1.787 | FALSE |  1.42 | TRUE | 80.97 | 71.54 | 62.45 |  |  | FALSE | FALSE |
| OS_placebo | rp_hazard_k1 |  703.10 |  715.00 | 0.9518 | 1.526 | TRUE |  1.78 | TRUE | 80.69 | 71.44 | 59.07 |  |  | TRUE | FALSE |
| OS_placebo | rp_hazard_k2 |  702.91 |  718.77 | 0.9518 | 1.472 | TRUE |  1.48 | TRUE | 81.10 | 70.20 | 55.04 |  |  | TRUE | TRUE |
| OS_placebo | rp_hazard_k3 |  705.06 |  724.89 | 0.9518 | 1.481 | TRUE |  1.46 | TRUE | 81.15 | 69.99 | 54.35 |  |  | TRUE | FALSE |
| OS_placebo | rp_odds_k1 |  702.97 |  714.87 | 0.9518 | 1.498 | TRUE |  1.76 | TRUE | 80.66 | 71.68 | 60.60 |  |  | TRUE | FALSE |
| OS_placebo | rp_odds_k2 |  702.92 |  718.79 | 0.9518 | 1.473 | TRUE |  1.46 | TRUE | 81.08 | 70.54 | 57.23 |  |  | TRUE | FALSE |
| OS_placebo | rp_odds_k3 |  705.06 |  724.89 | 0.9518 | 1.466 | TRUE |  1.48 | TRUE | 81.14 | 70.29 | 56.53 |  |  | TRUE | FALSE |
| OS_placebo | cure_weibull |  710.79 |  722.69 | 0.8916 | 1.777 | FALSE |  2.36 | TRUE | 80.40 | 75.50 | 72.47 |  |  | FALSE | FALSE |
| OS_placebo | cure_lnorm |  704.87 |  716.77 | 0.9518 | 1.566 | TRUE |  1.76 | TRUE | 80.46 | 74.09 | 69.50 |  |  | TRUE | FALSE |
| OS_placebo | cure_llogis |  707.20 |  719.10 | 0.9518 | 1.785 | TRUE |  2.00 | TRUE | 80.25 | 74.71 | 70.43 |  |  | FALSE | FALSE |

图：KM 与拟合曲线 `fig_fit_*.png`；超额风险与平滑后的 KM 风险 `fig_hazard_*.png`。

值得注意：两条非 pCR 曲线选中的模型不同（帕博利珠单抗 cure_llogis，安慰剂 cure_weibull）。安慰剂一侧第 3 条的差距，所选模型为 0.0511，次优的 cure_llogis 为 0.0533，选择对第 3 条敏感；20 年时两组非 pCR 层的 EFS 分别为 51.47% 与 49.7%。引擎给出的按臂 EFS 与随访更长的 2024 年 EFS（IA7）的对照见第 7 节。

## 7. 校准（步骤 5）

引擎结构参数：pCR 比例 帕博利珠单抗 0.6301、安慰剂 0.5564；首发事件中超额部分的分配（局部区域复发/远处复发/超额死亡）帕博利珠单抗 0.268/0.626/0.106、安慰剂 0.232/0.649/0.119（预期背景死亡 6.0、2.7 例已扣除；第二原发癌按比例摊入）；局部区域复发 → 远处复发 0.340/年（22/45 例，暴露 1.98 年）。

远处复发后的超额死亡（复发后时间的 Weibull，两臂共用）使两臂 OS 与 2024 年 Fig. 1A 的 KM 在第 1 至 78 个月逐月吻合（平方误差和最小）。校准前为起点值（指数分布、中位 1.5 年，不是估计值）。结果：形状 0.3543、尺度 1.5356 年（中位 0.546 年）。这是吸收了结构假设的有效参数，不宜直接解读为临床上的复发后生存。

| arm | stage | rmse_pp | max_abs_diff_pp | diff_36m | diff_60m | diff_78m | dr_shape | dr_scale | dr_median_years | SSE_both_arms |
|---|---|---|---|---|---|---|---|---|---|---|
| pembro | before (start value) | 1.904 | 3.752 | 2.940 | 0.442 | -1.053 | 1.0000 | 2.1640 | 1.5000 | 432.28 |
| placebo | before (start value) | 1.385 | 2.650 | 1.693 | -1.293 | -1.347 | 1.0000 | 2.1640 | 1.5000 | 432.28 |
| pembro | after calibration | 0.931 | 2.040 | 1.639 | 0.491 | -0.170 | 0.3543 | 1.5356 | 0.5457 | 125.34 |
| placebo | after calibration | 0.861 | 2.763 | -0.512 | -1.092 | 0.284 | 0.3543 | 1.5356 | 0.5457 | 125.34 |
| pembro | arm-specific calibration | 0.445 | 1.064 | 0.613 | 0.081 | -0.110 | 0.0649 | 0.0497 | 0.0002 | 50.83 |
| placebo | arm-specific calibration | 0.674 | 2.161 | 0.237 | -0.820 | 0.216 | 0.4829 | 1.9149 | 0.8965 | 50.83 |

两臂各自校准的变体：规则（运行前固定）为只有当它在两臂所有未用于校准的 OS 检查上都改善时才采用。结果未采用（OS non-pCR vs 2024 Fig. S4 (IA7) pembro：3.75 → 2.51；OS non-pCR vs 2024 Fig. S4 (IA7) placebo：4.25 → 3.21；OS pCR vs 2024 Fig. S4 (IA7) pembro：0.76 → 0.97；OS pCR vs 2024 Fig. S4 (IA7) placebo：1.47 → 1.47）；且帕博利珠单抗臂的参数退化（中位接近 0）。

未用于校准的曲线与引擎的对照（`engine_checks.csv`，不作门槛）：

| check | arm | max_abs_diff |
|---|---|---|
| DRFS vs 2022 Fig. S3 (IA4) | pembro | 1.350 |
| EFS vs 2024 Fig. 2A (IA7) | pembro | 0.788 |
| OS non-pCR vs 2024 Fig. S4 (IA7) | pembro | 3.750 |
| OS pCR vs 2024 Fig. S4 (IA7) | pembro | 0.764 |
| DRFS vs 2022 Fig. S3 (IA4) | placebo | 2.838 |
| EFS vs 2024 Fig. 2A (IA7) | placebo | 1.527 |
| OS non-pCR vs 2024 Fig. S4 (IA7) | placebo | 4.252 |
| OS pCR vs 2024 Fig. S4 (IA7) | placebo | 1.473 |

图：`fig_calibration_OS.png`、`fig_engine_checks.png`。帕博利珠单抗组 OS 在 20 至 40 个月模型偏高，安慰剂非 pCR 层 OS 第一年模型偏低；推测原因是无复发死亡（治疗相关死亡等）在时间上的分布与模型假设（与 EFS 超额风险成比例）不同，且两臂复发后的生存可能不同。

## 8. 需要决定的事项

1. **层内 HR 的参照值**（上文「不达标的门槛项」）：请给出 pCR 层 0.65 [0.39, 1.08]、non-pCR 层 0.72 [0.54, 0.96] 的出处。若来自 IA4 以后的分析，需要该分析的按臂 × pCR 分层 KM 图才能重建；否则可改为不作门槛的跨分析对照。
2. 非 pCR 两层的分布族不同（第 6 节），是否要求两臂用同一分布族。
3. 第二原发癌的处理（现为按比例摊入三类）。
4. 远处复发后死亡率为两臂共用的有效参数（第 7 节）。
5. S-JP 的权重定义与 BRCA 检查的对象范围（`docs/model_spec.md` 第 2 节，待尾崎确认）。

## 9. 未进行的步骤

步骤 6（bootstrap，B = 1000）与步骤 7（生存引擎的最终输出：5、10、20 年 EFS 与 OS 等）。引擎函数与扩展接口已在 `R/engine.R`，接口测试见 `engine_interface_test.csv`。

