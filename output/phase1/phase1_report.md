# 第1阶段（生存引擎）报告

生成时间：2026-10-22 03:10。由 `R/99_phase1_report.R` 从代码输出生成，表中数字均读自 `output/`、`data/` 与 `input/` 下的文件。模型规格见 `docs/model_spec.md`。

## 状态

- 已完成：步骤 1 至 4（含 2026-10-21 与 2026-10-22 的修正）与一致性检查；非 pCR 层分布族已复核。
- 重建与一致性的门槛项 62 项，不达标 0 项。
- 步骤 5（校准第四轮，2026-10-22）达标：(a) 两臂第 1 至 5 年的 10 个时点全部落在重建 KM 的逐点 95% 置信区间内；(b) 模型的 5 年 RMST 两臂差 0.1768 年，落在 KM 差（0.0985 年）的 bootstrap 95% 区间 -0.0381 至 0.2421 年内；点估计的差距（模型减 KM）为 0.0783 年。
- 步骤 6（bootstrap，B = 1000）与步骤 7（引擎输出）已完成（第 9、10 节）。
- 门槛在看到结果后修改过，见下一节「门槛修改记录」。

门槛 (a)（`calibration_gate.csv`）：

| arm | month | km | ci95_lo | ci95_hi | engine | diff | inside |
|---|---|---|---|---|---|---|---|
| pembro | 12 | 97.19 | 96.04 | 98.35 | 98.04 | 0.853 | 是 |
| pembro | 24 | 92.20 | 90.34 | 94.10 | 93.69 | 1.485 | 是 |
| pembro | 36 | 89.51 | 87.39 | 91.68 | 91.25 | 1.736 | 是 |
| pembro | 48 | 87.84 | 85.58 | 90.16 | 89.18 | 1.340 | 是 |
| pembro | 60 | 86.55 | 84.19 | 88.98 | 87.43 | 0.874 | 是 |
| placebo | 12 | 98.72 | 97.61 | 99.84 | 98.22 | -0.500 | 是 |
| placebo | 24 | 91.02 | 88.23 | 93.90 | 90.36 | -0.659 | 是 |
| placebo | 36 | 86.90 | 83.62 | 90.32 | 86.28 | -0.625 | 是 |
| placebo | 48 | 83.53 | 79.92 | 87.30 | 83.03 | -0.505 | 是 |
| placebo | 60 | 81.71 | 77.95 | 85.65 | 80.45 | -1.254 | 是 |

门槛 (b)（`calibration_gate_rmst.csv`）：

| quantity | km | km_boot_ci95_lo | km_boot_ci95_hi | boot_B | engine | engine_minus_km | pass |
|---|---|---|---|---|---|---|---|
| 5-year OS RMST difference, pembro - placebo (years) | 0.0985 | -0.0381 | 0.2421 | 1000 | 0.1768 | 0.0783 | 达标 |

## 门槛修改记录

按时间列出验证与校准门槛的每次修改。全部都是看到结果后修改的；第 4、5 项的理由都是门槛比抽样误差更严。

| 序号 | 日期 | 对象 | 修改前 | 修改后 | 时点 | 看到的结果 | 理由 |
|---|---|---|---|---|---|---|---|
| 1 | 2026-10-21 | Yau 2022 的重建验证 | 里程碑差 ≤ 1 个百分点、HR 差 ≤ 0.03、事件数差 ≤ 2% 三项都作门槛 | 只保留里程碑为门槛；HR 与事件数只报告 | 看到结果后修改 | Yau 有 4 项不达标（事件数 2 项、HR 2 项） | HR 的估计量与原文不同（原文为 12 个队列、含队列效应的汇总模型，使用全部随访；重建只能在 12 年内做单一 Cox）；事件数的参照值从风险表推算，原文没有报告 |
| 2 | 2026-10-21 | 拟合准则 1（选模） | 模型落在 KM 逐点 95% CI 内的月份比例 = 100% | ≥ 95% | 看到结果后修改 | 6 条曲线中 3 条没有任何候选模型通过 | 设定错误：逐点 95% 置信区间本来就预期约 5% 的点落在区间外 |
| 3 | 2026-10-21 | 按 pCR 分层的 EFS 层内 HR（较晚截点的参照值） | 与参照值的差 ≤ 0.03（门槛） | 不作门槛的跨分析对照 | 看到结果后修改 | pCR 层重建 0.722 对参照 0.65，差 0.072 | 参照值来自比 IA4 更晚的数据截点，IA4 的曲线不可能与之吻合；IA4 原文印的 0.73 与 0.70 已在 0.012 以内复现 |
| 4 | 2026-10-22 | 校准门槛 | 各臂第 1 至 5 年整年时点 OS 与 KM 的差 ≤ 1 个百分点 | (a) 各臂第 1 至 5 年整年时点落在 KM 逐点 95% CI 内；(b) 5 年 RMST 两臂差相对误差 ≤ 20% | 看到结果后修改 | 第一轮（2026-10-21）与第二轮（2026-10-22）校准都不达标 | 门槛比抽样误差更严：1 个百分点小于安慰剂组（n = 390）5 年 OS 的 Greenwood 标准误 1.96 个百分点 |
| 5 | 2026-10-22 | 校准门槛 (b) | 5 年 RMST 两臂差：模型与 KM 的相对误差 ≤ 20%（允许 0.079 至 0.118 年） | (b) 模型的 5 年 RMST 两臂差落在 KM 差的 bootstrap 95% 区间内；点估计差距照常报告 | 看到结果后修改 | 第三轮校准不达标（(a) 与 (b) 都不达标） | 门槛比抽样误差更严：允许带宽 0.039 年，远窄于 KM 差的 bootstrap 95% 区间宽度 0.280 年 |

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

生命表：令和7(2025)年簡易生命表（女），`input/lifetable/SOURCE.md`、`data/lifetable_female_2025.csv`。较晚截点的数值：`input/user_supplied_values.csv`。复发后生存的文献摘要：`input/params/pubmed/`。

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

两份补充材料的全部图（8 张，其中 KM 图 3 张；2024 年补充材料没有按 pCR 分层的 EFS，故分层 EFS 与 pCR 比例都取 2022 年 IA4）：

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

栅格图中印的数字从图像转录，与正文文字层交叉核对 19 项，不一致 0 项（`data/transcription_checks.csv`）。报告值 212 个由正则从 PDF 文字层抽取（`data/reported_values.csv`）。

## 3. 数字化（`data/digitized/`）

矢量图：PyMuPDF `get_drawings()` 读取阶梯路径；x 轴用全部带标签刻度最小二乘，y 轴用 0% 与 100% 两端锚定（2024 年两图的 100% 刻度偏离等距，插图读数支持两端锚定）。

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

栅格图：嵌入图像原生像素上的颜色分离（更高 dpi 栅格化只会插值）。线条用单调阶梯的动态规划追踪；Yau 的「+」删失标记上下对称，NEJM 补充材料的删失标记只向上延伸并在密集处连成色块，故追踪色块下沿；深色曲线的抗锯齿边缘会被分到同色系浅色曲线，浅色类在深色曲线 2 像素内的像素剔除。

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

不作门槛、只报告的项目：
- Yau 2022 的 HR 与事件数（2026-10-21 的决定）。HR：原文出自 12 个队列汇总、含队列效应的模型并使用全部随访，重建数据只到 12 年、只能做单一 Cox，估计量不同。事件数：参照值是从风险表推算的 12 年累计事件数，原文没有报告。
- 按 pCR 分层的 EFS 层内 HR 与较晚截点值（pCR 0.65 [0.39, 1.08]、non-pCR 0.72 [0.54, 0.96]）的跨分析对照。该参照值来自比 IA4（2021-03-23）晚的截点，IA4 的曲线不可能与之吻合；IA4 原文印的 0.73 与 0.70 已在 0.012 以内复现（下表 K22_S4_EFS_pCR 的 hr 行）。出处：OncLive 2023-10-20 的报道与 Ann Oncol 2023;34(S2):S1256-S1257（ESMO 2023；数据截点 2023-03-23，中位随访 63.1 个月），待尾崎确认原始出处后替换。

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
| K22_S4_EFS_pCR | hr |  | pCR (later cutoff, cross-analysis) |   0.65 |   0.7224 | 0.0724 | 0.03 | **不达标** | 否（只报告） | input/user_supplied_values.csv |
| K22_S4_EFS_pCR | hr |  | nonpCR (later cutoff, cross-analysis) |   0.72 |   0.7117 | 0.0083 | 0.03 | 达标 | 否（只报告） | input/user_supplied_values.csv |
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

图：`fig_validation_*.png`。

## 5. 一致性检查（`output/phase1/consistency_check.csv`）

2022 年 Fig. S4 的分层 KM 按 pCR 比例（帕博利珠单抗 0.6301，安慰剂 0.5564）加权混合，与整体 EFS 比较（3 至 42 个月，四层在险均 ≥ 20），门槛 1 个百分点，不达标 0 处。

| arm | comparator | max_abs_diff |
|---|---|---|
| pembro | K22_F1_EFS | 0.293 |
| placebo | K22_F1_EFS | 0.356 |
| pembro | K24_F2A_EFS | 0.421 |
| placebo | K24_F2A_EFS | 0.452 |

图：`fig_consistency_pCR_mixture.png`。

## 6. 拟合与模型选择（步骤 4）

数据：4 条 EFS（2022 年 Fig. S4，臂 × pCR）在手术时点（随机化后 7 个月）做 landmark；2 条 OS（2024 年 Fig. 1A，按臂）从随机化起。候选 15 个：6 个标准分布、6 个 RP 样条（1 至 3 个内结点，累积风险与累积比值尺度）、3 个相对生存混合治愈模型（Weibull、对数正态、对数 logistic；背景为日本女性生命表，治愈比例作用于超额死亡）。AIC/BIC 用全因对数似然，使治愈模型与全因模型可比。

准则：
1. 与 KM 的重合：模型曲线落在 KM 逐点 95% CI 内的月份比例 ≥ 0.95（在险 ≥ 20 的时点）。最初设为 100% 是设定错误：逐点 95% 置信区间本来就预期约 5% 的点落在区间外；首轮运行后已修正为 95%。
2. 风险形状：超额风险不晚于术后 3 年达峰，3→5→10 年递减（EFS）；OS 为 5→10→20 年递减；10 年和 20 年的全因风险不低于背景。
3. 10 年、20 年外推与外部长期数据：Yau 2022 TNBC 在手术时点 landmark 后的条件 EFS S(10)/S(5)（pCR 对 RCB-0，非 pCR 对 RCB-1 至 3 合并），列出供参照。
选择：EFS 同一 pCR 层两臂用同一分布族。两臂都满足 1 和 2 的族中，保留两臂合计 AIC 与最优者相差 ≤ 4 的族，再取 5 年外推检验中两臂差值绝对值之和最小的族；次优者保留为情景分析。OS 按臂取满足 1 和 2 的 AIC 最小者。

5 年外推检验（不作门槛）：所选分层 EFS 模型外推到随机化后 5 年（术前 KM × 术后模型），与较晚截点报告的 5 年分层 EFS 比较。外部数据出处：OncLive 2023-10-20 的报道与 Ann Oncol 2023;34(S2):S1256-S1257（ESMO 2023；数据截点 2023-03-23，中位随访 63.1 个月）。

| curve | model | efs5_from_randomization | efs5_later_cutoff | efs5_diff |
|---|---|---|---|---|
| EFS_pembro_pCR | weibull | 92.21 | 92.2 | 0.01 |
| EFS_placebo_pCR | weibull | 88.95 | 88.2 | 0.75 |
| EFS_pembro_nonpCR | cure_weibull | 62.39 | 62.6 | -0.21 |
| EFS_placebo_nonpCR | cure_weibull | 49.53 | 52.3 | -2.77 |

5 年约束（2026-10-22，`efs5_constraint.csv`）：所选 EFS 模型在随机化后 60 个月的预测须落在较晚截点 5 年分层 EFS 的 95% 置信区间内。报道没有给出置信区间，故用二项近似（Wald）：p ± 1.960 × √(p(1 − p)/n)，n 为同一次 pCR 分析（IA4）的分层人数。此近似不考虑删失，比 KM 的区间窄，即约束偏严。超出区间时在较近的边界上重新最大化似然（治愈 Weibull 由形状与尺度推出治愈比例，Weibull 由形状推出尺度）；落在区间内则参数不变。约束对非 pCR 层（cure_weibull）与 pCR 层（weibull）都检查。结果：四条曲线约束前都在区间内（4/4），约束不起作用，参数与外推不变；bootstrap 的各次重拟合同样带此约束。约束函数在人为移动边界时都能落到边界上（`R/test_efs5_constraint.R`）。

| curve | model | n_stratum | efs5_later_cutoff | ci95_lo | ci95_hi | efs5_before | binding | efs5_after | efs10_before | efs10_after | efs20_before | efs20_after | pars_before | pars_after |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EFS_pembro_pCR | weibull | 494 | 92.2 | 89.84 | 94.56 | 92.212 | FALSE | 92.212 | 87.324 | 87.324 | 80.132 | 80.132 | shape = 0.67867; scale = 178.96 | shape = 0.67867; scale = 178.96 |
| EFS_placebo_pCR | weibull | 217 | 88.2 | 83.91 | 92.49 | 88.953 | FALSE | 88.953 | 81.103 | 81.103 | 69.403 | 69.403 | shape = 0.76839; scale = 72.02 | shape = 0.76839; scale = 72.02 |
| EFS_pembro_nonpCR | cure_weibull | 290 | 62.6 | 57.03 | 68.17 | 62.390 | FALSE | 62.390 | 59.951 | 59.951 | 57.507 | 57.507 | theta = 0.64257; shape = 0.89539; scale = 1.3566 | theta = 0.64257; shape = 0.89539; scale = 1.3566 |
| EFS_placebo_nonpCR | cure_weibull | 173 | 52.3 | 44.86 | 59.74 | 49.533 | FALSE | 49.533 | 47.968 | 47.968 | 46.097 | 46.097 | theta = 0.52828; shape = 1.197; scale = 1.4708 | theta = 0.52828; shape = 1.197; scale = 1.4708 |

（efs5/10/20：随机化后 5、10、20 年的 EFS %，术前 KM × 术后模型。）

各层的分布族比较（`family_selection.csv`，两臂都合格的族）：

| stratum | model | AIC_sum | dAIC_sum | within_aic_window | efs5_diff_pembro | efs5_diff_placebo | efs5_abs_diff_sum | selected | scenario |
|---|---|---|---|---|---|---|---|---|---|
| nonpCR | lnorm | 790.72 | 0.00 | TRUE | -3.390 |  -8.179 | 11.569 | FALSE | FALSE |
| nonpCR | cure_weibull | 791.64 | 0.92 | TRUE | -0.210 |  -2.767 |  2.977 | TRUE | FALSE |
| nonpCR | cure_llogis | 792.42 | 1.70 | TRUE | -1.670 |  -5.085 |  6.755 | FALSE | TRUE |
| nonpCR | llogis | 792.54 | 1.82 | TRUE | -4.956 | -10.464 | 15.420 | FALSE | FALSE |
| nonpCR | gengamma | 794.59 | 3.87 | TRUE | -3.246 |  -8.981 | 12.227 | FALSE | FALSE |
| nonpCR | rp_hazard_k2 | 794.65 | 3.93 | TRUE | -2.350 |  -5.098 |  7.448 | FALSE | FALSE |
| nonpCR | rp_odds_k1 | 794.65 | 3.93 | TRUE | -3.600 |  -8.560 | 12.160 | FALSE | FALSE |
| nonpCR | cure_lnorm | 794.68 | 3.96 | TRUE | -2.984 |  -7.958 | 10.942 | FALSE | FALSE |
| nonpCR | rp_odds_k2 | 794.77 | 4.05 | FALSE | -2.265 |  -4.944 |  7.209 | FALSE | FALSE |
| nonpCR | rp_hazard_k1 | 795.31 | 4.59 | FALSE | -3.872 |  -9.038 | 12.910 | FALSE | FALSE |
| nonpCR | weibull | 796.10 | 5.38 | FALSE | -5.870 | -12.547 | 18.417 | FALSE | FALSE |
| nonpCR | rp_hazard_k3 | 796.80 | 6.08 | FALSE | -1.099 |  -5.041 |  6.140 | FALSE | FALSE |
| nonpCR | rp_odds_k3 | 796.88 | 6.16 | FALSE | -1.030 |  -4.806 |  5.836 | FALSE | FALSE |
| pCR | cure_weibull | 404.90 | 0.00 | TRUE |  0.250 |   3.887 |  4.137 | FALSE | FALSE |
| pCR | cure_lnorm | 405.53 | 0.63 | TRUE |  0.356 |   3.235 |  3.591 | FALSE | FALSE |
| pCR | cure_llogis | 405.53 | 0.63 | TRUE |  0.261 |   3.386 |  3.647 | FALSE | FALSE |
| pCR | llogis | 406.32 | 1.42 | TRUE |  0.061 |   0.790 |  0.851 | FALSE | TRUE |
| pCR | weibull | 406.51 | 1.61 | TRUE |  0.012 |   0.753 |  0.765 | TRUE | FALSE |
| pCR | exp | 408.56 | 3.66 | TRUE | -1.396 |  -0.661 |  2.057 | FALSE | FALSE |

非 pCR 层分布族复核（2026-10-22，`nonpcr_family_review.csv`）：规则为若有某族两臂 5 年差都在 1 个百分点以内、且两臂合计 AIC 与最优族相差 ≤ 4，则基准改用该族。全部候选中满足者 0 个（两臂 5 年差都在 1 个百分点以内的族 0 个），故维持 cure_weibull。

| model | eligible_both_arms | AIC_sum | dAIC_sum | efs5_diff_pembro | efs5_diff_placebo | both_arms_within_1pt | review_pass | selected | scenario |
|---|---|---|---|---|---|---|---|---|---|
| gompertz | FALSE | 789.82 | -0.90 |   0.440 |  -6.519 | FALSE | FALSE | FALSE | FALSE |
| lnorm | TRUE | 790.72 |  0.00 |  -3.390 |  -8.179 | FALSE | FALSE | FALSE | FALSE |
| cure_weibull | TRUE | 791.64 |  0.92 |  -0.210 |  -2.767 | FALSE | FALSE | TRUE | FALSE |
| cure_llogis | TRUE | 792.42 |  1.70 |  -1.670 |  -5.085 | FALSE | FALSE | FALSE | TRUE |
| llogis | TRUE | 792.54 |  1.82 |  -4.956 | -10.464 | FALSE | FALSE | FALSE | FALSE |
| gengamma | TRUE | 794.59 |  3.87 |  -3.246 |  -8.981 | FALSE | FALSE | FALSE | FALSE |
| rp_odds_k1 | TRUE | 794.65 |  3.93 |  -3.600 |  -8.560 | FALSE | FALSE | FALSE | FALSE |
| rp_hazard_k2 | TRUE | 794.65 |  3.93 |  -2.350 |  -5.098 | FALSE | FALSE | FALSE | FALSE |
| cure_lnorm | TRUE | 794.68 |  3.96 |  -2.984 |  -7.958 | FALSE | FALSE | FALSE | FALSE |
| rp_odds_k2 | TRUE | 794.77 |  4.05 |  -2.265 |  -4.944 | FALSE | FALSE | FALSE | FALSE |
| rp_hazard_k1 | TRUE | 795.31 |  4.59 |  -3.872 |  -9.038 | FALSE | FALSE | FALSE | FALSE |
| weibull | TRUE | 796.10 |  5.38 |  -5.870 | -12.547 | FALSE | FALSE | FALSE | FALSE |
| rp_hazard_k3 | TRUE | 796.80 |  6.08 |  -1.099 |  -5.041 | FALSE | FALSE | FALSE | FALSE |
| rp_odds_k3 | TRUE | 796.88 |  6.16 |  -1.030 |  -4.806 | FALSE | FALSE | FALSE | FALSE |
| exp | FALSE | 810.14 | 19.42 | -12.493 | -15.007 | FALSE | FALSE | FALSE | FALSE |

偏差的方向及其影响：cure_weibull 在安慰剂非 pCR 层的 5 年 EFS 比较晚截点的报告值低 2.77 个百分点（帕博利珠单抗非 pCR 层 -0.21 个百分点）；所有候选在安慰剂非 pCR 层都是负偏差。安慰剂（单用化疗）组的 EFS 被低估，帕博利珠单抗相对于化疗的效果因此偏向高估。

Yau 的参照值（`yau_landmark_reference.csv`）：

| group | S5 | S10 | C5_10 |
|---|---|---|---|
| RCB0 | 0.9023 | 0.8574 | 0.9503 |
| RCB1_3 | 0.6045 | 0.5598 | 0.9260 |

选定的模型与理由（`model_selection.csv`；S5/S10/S20 为全因生存 %，EFS 为术后年数，OS 为随机化后年数）：

| curve | model | AIC | S5 | S10 | S20 | cure_fraction | efs5_diff | scenario_model | reason |
|---|---|---|---|---|---|---|---|---|---|
| EFS_pembro_pCR | weibull |  259.71 | 91.56 | 86.83 | 79.77 |  |  0.012 | llogis | same model for both arms of the pCR stratum; 6 of 15 models eligible (criteria 1 and 2) in both arms, 6 within 4 of the best two-arm AIC sum (cure_weibull); chosen with the smallest two-arm sum of \|5-year EFS - later-cutoff value\| = 0.76 points (AIC sum 406.5, dAIC 1.6); runner-up kept as scenario: llogis (sum 0.85, dAIC 1.4) |
| EFS_placebo_pCR | weibull |  146.80 | 87.92 | 80.30 | 68.82 |  |  0.753 | llogis | same model for both arms of the pCR stratum; 6 of 15 models eligible (criteria 1 and 2) in both arms, 6 within 4 of the best two-arm AIC sum (cure_weibull); chosen with the smallest two-arm sum of \|5-year EFS - later-cutoff value\| = 0.76 points (AIC sum 406.5, dAIC 1.6); runner-up kept as scenario: llogis (sum 0.85, dAIC 1.4) |
| EFS_pembro_nonpCR | cure_weibull |  460.33 | 65.18 | 63.12 | 60.45 | 0.6426 | -0.210 | cure_llogis | same model for both arms of the nonpCR stratum; 13 of 15 models eligible (criteria 1 and 2) in both arms, 8 within 4 of the best two-arm AIC sum (lnorm); chosen with the smallest two-arm sum of \|5-year EFS - later-cutoff value\| = 2.98 points (AIC sum 791.6, dAIC 0.9); runner-up kept as scenario: cure_llogis (sum 6.75, dAIC 1.7) |
| EFS_placebo_nonpCR | cure_weibull |  331.31 | 53.03 | 51.82 | 49.70 | 0.5283 | -2.767 | cure_llogis | same model for both arms of the nonpCR stratum; 13 of 15 models eligible (criteria 1 and 2) in both arms, 8 within 4 of the best two-arm AIC sum (lnorm); chosen with the smallest two-arm sum of \|5-year EFS - later-cutoff value\| = 2.98 points (AIC sum 791.6, dAIC 0.9); runner-up kept as scenario: cure_llogis (sum 6.75, dAIC 1.7) |
| OS_pembro | cure_lnorm | 1041.23 | 86.42 | 83.27 | 79.42 | 0.8406 |  |  | 15/15 converged; 6 fail criterion 1 (KM 95% CI), 5 more fail criterion 2; 4 eligible; lowest AIC (no external OS data for criterion 3) |
| OS_placebo | rp_hazard_k2 |  702.91 | 81.10 | 70.20 | 55.04 |  |  |  | 15/15 converged; 7 fail criterion 1 (KM 95% CI), 0 more fail criterion 2; 8 eligible; lowest AIC (no external OS data for criterion 3) |

全部候选（`model_comparison.csv`）：

| curve | model | AIC | BIC | c1_frac_inside_ci | c1_max_abs_diff_pp | c1_pass | peak_excess_haz_year | c2_pass | S5 | S10 | S20 | cond_5_10 | yau_cond_5_10 | efs5_diff | selected | scenario |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EFS_pembro_pCR | exp |  262.49 |  266.70 | 1.0000 | 1.240 | TRUE |  0.02 | TRUE | 89.65 | 80.38 | 64.61 | 0.8965 | 0.9503 |  -1.396 | FALSE | FALSE |
| EFS_pembro_pCR | weibull |  259.71 |  268.12 | 1.0000 | 0.668 | TRUE |  0.02 | TRUE | 91.56 | 86.83 | 79.77 | 0.9484 | 0.9503 |   0.012 | TRUE | FALSE |
| EFS_pembro_pCR | lnorm |  259.35 |  267.76 | 1.0000 | 0.694 | TRUE |  0.02 | FALSE | 92.11 | 88.79 | 84.58 | 0.9640 | 0.9503 |   0.412 | FALSE | FALSE |
| EFS_pembro_pCR | llogis |  259.70 |  268.10 | 1.0000 | 0.663 | TRUE |  0.02 | TRUE | 91.63 | 87.17 | 80.83 | 0.9513 | 0.9503 |   0.061 | FALSE | TRUE |
| EFS_pembro_pCR | gompertz |  261.11 |  269.52 | 1.0000 | 0.750 | TRUE |  0.02 | FALSE | 92.93 | 92.26 | 92.18 | 0.9927 | 0.9503 |   0.966 | FALSE | FALSE |
| EFS_pembro_pCR | gengamma |  261.74 |  274.35 | 1.0000 | 0.675 | TRUE |  0.02 | TRUE | 91.48 | 86.46 | 78.47 | 0.9451 | 0.9503 |  -0.039 | FALSE | FALSE |
| EFS_pembro_pCR | rp_hazard_k1 |  261.55 |  274.16 | 1.0000 | 0.672 | TRUE |  0.02 | TRUE | 91.81 | 87.62 | 81.50 | 0.9543 | 0.9503 |   0.206 | FALSE | FALSE |
| EFS_pembro_pCR | rp_hazard_k2 |  263.03 |  279.84 | 1.0000 | 0.690 | TRUE |  0.02 | TRUE | 91.30 | 86.02 | 77.94 | 0.9422 | 0.9503 |  -0.176 | FALSE | FALSE |
| EFS_pembro_pCR | rp_hazard_k3 |  265.04 |  286.05 | 1.0000 | 0.704 | TRUE |  0.02 | TRUE | 91.12 | 85.41 | 76.55 | 0.9374 | 0.9503 |  -0.314 | FALSE | FALSE |
| EFS_pembro_pCR | rp_odds_k1 |  261.56 |  274.17 | 1.0000 | 0.674 | TRUE |  0.02 | FALSE | 91.86 | 87.84 | 82.22 | 0.9562 | 0.9503 |   0.236 | FALSE | FALSE |
| EFS_pembro_pCR | rp_odds_k2 |  263.02 |  279.83 | 1.0000 | 0.688 | TRUE |  0.02 | TRUE | 91.35 | 86.31 | 79.00 | 0.9448 | 0.9503 |  -0.148 | FALSE | FALSE |
| EFS_pembro_pCR | rp_odds_k3 |  265.03 |  286.04 | 1.0000 | 0.702 | TRUE |  0.02 | TRUE | 91.16 | 85.71 | 77.72 | 0.9402 | 0.9503 |  -0.291 | FALSE | FALSE |
| EFS_pembro_pCR | cure_weibull |  261.70 |  274.31 | 1.0000 | 0.674 | TRUE |  0.02 | TRUE | 91.89 | 88.16 | 82.13 | 0.9594 | 0.9503 |   0.250 | FALSE | FALSE |
| EFS_pembro_pCR | cure_lnorm |  261.34 |  273.94 | 1.0000 | 0.686 | TRUE |  0.02 | TRUE | 92.02 | 88.19 | 81.32 | 0.9585 | 0.9503 |   0.356 | FALSE | FALSE |
| EFS_pembro_pCR | cure_llogis |  261.68 |  274.29 | 1.0000 | 0.678 | TRUE |  0.02 | TRUE | 91.90 | 88.09 | 81.60 | 0.9585 | 0.9503 |   0.261 | FALSE | FALSE |
| EFS_placebo_pCR | exp |  146.07 |  149.45 | 0.9722 | 2.330 | TRUE |  0.02 | TRUE | 86.01 | 73.98 | 54.74 | 0.8601 | 0.9503 |  -0.661 | FALSE | FALSE |
| EFS_placebo_pCR | weibull |  146.80 |  153.56 | 0.9722 | 1.740 | TRUE |  0.02 | TRUE | 87.92 | 80.30 | 68.82 | 0.9134 | 0.9503 |   0.753 | TRUE | FALSE |
| EFS_placebo_pCR | lnorm |  145.28 |  152.04 | 0.9722 | 1.587 | TRUE |  0.06 | TRUE | 88.48 | 82.89 | 75.83 | 0.9369 | 0.9503 |   1.121 | FALSE | FALSE |
| EFS_placebo_pCR | llogis |  146.62 |  153.38 | 0.9722 | 1.698 | TRUE |  0.02 | TRUE | 88.00 | 80.94 | 71.10 | 0.9198 | 0.9503 |   0.790 | FALSE | TRUE |
| EFS_placebo_pCR | gompertz |  143.48 |  150.24 | 0.9444 | 1.437 | FALSE |  0.02 | FALSE | 91.47 | 91.25 | 91.25 | 0.9976 | 0.9503 |   3.389 | FALSE | FALSE |
| EFS_placebo_pCR | gengamma |  144.90 |  155.04 | 0.9722 | 1.138 | TRUE |  0.22 | FALSE | 90.29 | 87.91 | 85.55 | 0.9736 | 0.9503 |   2.518 | FALSE | FALSE |
| EFS_placebo_pCR | rp_hazard_k1 |  145.04 |  155.18 | 0.9722 | 1.020 | TRUE |  0.40 | FALSE | 90.22 | 87.01 | 82.86 | 0.9645 | 0.9503 |   2.504 | FALSE | FALSE |
| EFS_placebo_pCR | rp_hazard_k2 |  146.38 |  159.90 | 0.9722 | 1.152 | TRUE |  0.64 | FALSE | 90.82 | 88.60 | 85.88 | 0.9755 | 0.9503 |   2.975 | FALSE | FALSE |
| EFS_placebo_pCR | rp_hazard_k3 |  148.06 |  164.96 | 0.9722 | 1.177 | TRUE |  0.76 | FALSE | 91.03 | 89.12 | 86.83 | 0.9790 | 0.9503 |   3.141 | FALSE | FALSE |
| EFS_placebo_pCR | rp_odds_k1 |  145.04 |  155.18 | 0.9722 | 1.020 | TRUE |  0.40 | FALSE | 90.22 | 87.07 | 83.11 | 0.9651 | 0.9503 |   2.503 | FALSE | FALSE |
| EFS_placebo_pCR | rp_odds_k2 |  146.38 |  159.90 | 0.9722 | 1.149 | TRUE |  0.64 | FALSE | 90.82 | 88.63 | 85.99 | 0.9758 | 0.9503 |   2.975 | FALSE | FALSE |
| EFS_placebo_pCR | rp_odds_k3 |  148.07 |  164.97 | 0.9722 | 1.171 | TRUE |  0.72 | FALSE | 91.03 | 89.13 | 86.89 | 0.9792 | 0.9503 |   3.132 | FALSE | FALSE |
| EFS_placebo_pCR | cure_weibull |  143.20 |  153.34 | 0.9722 | 1.131 | TRUE |  0.54 | TRUE | 91.98 | 90.94 | 87.22 | 0.9886 | 0.9503 |   3.887 | FALSE | FALSE |
| EFS_placebo_pCR | cure_lnorm |  144.19 |  154.33 | 0.9722 | 1.049 | TRUE |  0.32 | TRUE | 91.22 | 89.87 | 86.13 | 0.9852 | 0.9503 |   3.235 | FALSE | FALSE |
| EFS_placebo_pCR | cure_llogis |  143.85 |  153.99 | 0.9722 | 1.010 | TRUE |  0.46 | TRUE | 91.40 | 90.12 | 86.36 | 0.9859 | 0.9503 |   3.386 | FALSE | FALSE |
| EFS_pembro_nonpCR | exp |  477.58 |  481.19 | 0.6389 | 6.287 | FALSE |  0.02 | TRUE | 48.60 | 23.62 |  5.58 | 0.4860 | 0.9260 | -12.493 | FALSE | FALSE |
| EFS_pembro_nonpCR | weibull |  462.59 |  469.80 | 1.0000 | 2.959 | TRUE |  0.02 | TRUE | 57.26 | 41.25 | 24.50 | 0.7204 | 0.9260 |  -5.870 | FALSE | FALSE |
| EFS_pembro_nonpCR | lnorm |  459.49 |  466.70 | 1.0000 | 1.959 | TRUE |  0.02 | TRUE | 60.63 | 50.04 | 39.45 | 0.8253 | 0.9260 |  -3.390 | FALSE | FALSE |
| EFS_pembro_nonpCR | llogis |  461.05 |  468.26 | 1.0000 | 2.437 | TRUE |  0.02 | TRUE | 58.63 | 46.03 | 33.92 | 0.7851 | 0.9260 |  -4.956 | FALSE | FALSE |
| EFS_pembro_nonpCR | gompertz |  458.95 |  466.16 | 1.0000 | 1.486 | TRUE |  0.02 | FALSE | 66.07 | 65.22 | 65.19 | 0.9871 | 0.9260 |   0.440 | FALSE | FALSE |
| EFS_pembro_nonpCR | gengamma |  461.48 |  472.30 | 1.0000 | 2.032 | TRUE |  0.02 | TRUE | 60.82 | 50.45 | 40.11 | 0.8296 | 0.9260 |  -3.246 | FALSE | FALSE |
| EFS_pembro_nonpCR | rp_hazard_k1 |  462.26 |  473.08 | 1.0000 | 1.990 | TRUE |  0.02 | TRUE | 59.89 | 47.11 | 33.12 | 0.7866 | 0.9260 |  -3.872 | FALSE | FALSE |
| EFS_pembro_nonpCR | rp_hazard_k2 |  462.80 |  477.22 | 1.0000 | 1.587 | TRUE |  0.02 | TRUE | 61.91 | 51.82 | 40.60 | 0.8369 | 0.9260 |  -2.350 | FALSE | FALSE |
| EFS_pembro_nonpCR | rp_hazard_k3 |  462.94 |  480.97 | 1.0000 | 1.007 | TRUE |  0.02 | TRUE | 63.59 | 55.76 | 47.07 | 0.8769 | 0.9260 |  -1.099 | FALSE | FALSE |
| EFS_pembro_nonpCR | rp_odds_k1 |  461.96 |  472.78 | 1.0000 | 1.900 | TRUE |  0.02 | TRUE | 60.34 | 49.27 | 38.27 | 0.8166 | 0.9260 |  -3.600 | FALSE | FALSE |
| EFS_pembro_nonpCR | rp_odds_k2 |  462.84 |  477.27 | 1.0000 | 1.612 | TRUE |  0.02 | TRUE | 62.08 | 52.87 | 43.46 | 0.8516 | 0.9260 |  -2.265 | FALSE | FALSE |
| EFS_pembro_nonpCR | rp_odds_k3 |  462.92 |  480.95 | 1.0000 | 0.999 | TRUE |  0.02 | TRUE | 63.71 | 56.46 | 48.92 | 0.8862 | 0.9260 |  -1.030 | FALSE | FALSE |
| EFS_pembro_nonpCR | cure_weibull |  460.33 |  471.15 | 1.0000 | 1.762 | TRUE |  0.02 | TRUE | 65.18 | 63.12 | 60.45 | 0.9684 | 0.9260 |  -0.210 | TRUE | FALSE |
| EFS_pembro_nonpCR | cure_lnorm |  461.45 |  472.27 | 1.0000 | 2.115 | TRUE |  0.02 | TRUE | 61.17 | 51.30 | 40.88 | 0.8386 | 0.9260 |  -2.984 | FALSE | FALSE |
| EFS_pembro_nonpCR | cure_llogis |  460.89 |  471.71 | 1.0000 | 1.862 | TRUE |  0.02 | TRUE | 63.06 | 57.10 | 51.47 | 0.9054 | 0.9260 |  -1.670 | FALSE | TRUE |
| EFS_placebo_nonpCR | exp |  332.56 |  335.62 | 1.0000 | 4.941 | TRUE |  0.02 | TRUE | 35.80 | 12.81 |  1.64 | 0.3580 | 0.9260 | -15.007 | FALSE | FALSE |
| EFS_placebo_nonpCR | weibull |  333.51 |  339.63 | 1.0000 | 4.219 | TRUE |  0.02 | TRUE | 38.98 | 17.44 |  3.93 | 0.4474 | 0.9260 | -12.547 | FALSE | FALSE |
| EFS_placebo_nonpCR | lnorm |  331.23 |  337.35 | 1.0000 | 2.918 | TRUE |  0.20 | TRUE | 44.99 | 30.37 | 18.36 | 0.6750 | 0.9260 |  -8.179 | FALSE | FALSE |
| EFS_placebo_nonpCR | llogis |  331.49 |  337.62 | 1.0000 | 3.213 | TRUE |  0.10 | TRUE | 42.15 | 26.40 | 15.00 | 0.6262 | 0.9260 | -10.464 | FALSE | FALSE |
| EFS_placebo_nonpCR | gompertz |  330.87 |  337.00 | 1.0000 | 3.093 | TRUE |  0.02 | FALSE | 47.60 | 40.55 | 38.88 | 0.8520 | 0.9260 |  -6.519 | FALSE | FALSE |
| EFS_placebo_nonpCR | gengamma |  333.11 |  342.30 | 1.0000 | 3.086 | TRUE |  0.18 | TRUE | 43.93 | 28.29 | 15.71 | 0.6440 | 0.9260 |  -8.981 | FALSE | FALSE |
| EFS_placebo_nonpCR | rp_hazard_k1 |  333.05 |  342.24 | 1.0000 | 2.852 | TRUE |  0.28 | TRUE | 43.64 | 25.71 | 10.80 | 0.5890 | 0.9260 |  -9.038 | FALSE | FALSE |
| EFS_placebo_nonpCR | rp_hazard_k2 |  331.85 |  344.10 | 1.0000 | 1.827 | TRUE |  0.86 | TRUE | 49.04 | 37.20 | 25.34 | 0.7585 | 0.9260 |  -5.098 | FALSE | FALSE |
| EFS_placebo_nonpCR | rp_hazard_k3 |  333.86 |  349.18 | 1.0000 | 1.770 | TRUE |  0.78 | TRUE | 49.12 | 37.36 | 25.57 | 0.7606 | 0.9260 |  -5.041 | FALSE | FALSE |
| EFS_placebo_nonpCR | rp_odds_k1 |  332.69 |  341.88 | 1.0000 | 2.759 | TRUE |  0.28 | TRUE | 44.54 | 30.00 | 18.61 | 0.6735 | 0.9260 |  -8.560 | FALSE | FALSE |
| EFS_placebo_nonpCR | rp_odds_k2 |  331.93 |  344.18 | 1.0000 | 1.880 | TRUE |  0.82 | TRUE | 49.33 | 38.83 | 29.27 | 0.7871 | 0.9260 |  -4.944 | FALSE | FALSE |
| EFS_placebo_nonpCR | rp_odds_k3 |  333.96 |  349.27 | 1.0000 | 1.753 | TRUE |  0.82 | TRUE | 49.51 | 39.19 | 29.76 | 0.7916 | 0.9260 |  -4.806 | FALSE | FALSE |
| EFS_placebo_nonpCR | cure_weibull |  331.31 |  340.49 | 1.0000 | 1.926 | TRUE |  0.50 | TRUE | 53.03 | 51.82 | 49.70 | 0.9771 | 0.9260 |  -2.767 | TRUE | FALSE |
| EFS_placebo_nonpCR | cure_lnorm |  333.23 |  342.41 | 1.0000 | 2.864 | TRUE |  0.20 | TRUE | 45.29 | 31.14 | 19.42 | 0.6876 | 0.9260 |  -7.958 | FALSE | FALSE |
| EFS_placebo_nonpCR | cure_llogis |  331.53 |  340.71 | 1.0000 | 2.152 | TRUE |  0.44 | TRUE | 49.55 | 43.24 | 38.86 | 0.8728 | 0.9260 |  -5.085 | FALSE | TRUE |
| OS_pembro | exp | 1071.99 | 1076.65 | 0.5904 | 3.232 | FALSE |  0.02 | TRUE | 87.84 | 77.15 | 59.53 |  |  |  | FALSE | FALSE |
| OS_pembro | weibull | 1071.88 | 1081.21 | 0.7590 | 2.545 | FALSE |  0.02 | TRUE | 87.60 | 78.38 | 63.89 |  |  |  | FALSE | FALSE |
| OS_pembro | lnorm | 1059.27 | 1068.60 | 0.8795 | 2.379 | FALSE |  0.64 | TRUE | 87.25 | 79.24 | 68.84 |  |  |  | FALSE | FALSE |
| OS_pembro | llogis | 1069.57 | 1078.90 | 0.8072 | 2.454 | FALSE |  0.02 | TRUE | 87.42 | 78.59 | 65.96 |  |  |  | FALSE | FALSE |
| OS_pembro | gompertz | 1059.78 | 1069.11 | 0.8675 | 1.690 | FALSE |  0.02 | FALSE | 86.84 | 82.38 | 80.18 |  |  |  | FALSE | FALSE |
| OS_pembro | gengamma | 1042.81 | 1056.80 | 0.9759 | 1.186 | TRUE |  0.80 | FALSE | 86.79 | 81.93 | 77.20 |  |  |  | FALSE | FALSE |
| OS_pembro | rp_hazard_k1 | 1039.61 | 1053.60 | 0.9759 | 0.743 | TRUE |  1.24 | FALSE | 86.52 | 82.35 | 77.13 |  |  |  | FALSE | FALSE |
| OS_pembro | rp_hazard_k2 | 1041.70 | 1060.36 | 0.9759 | 0.686 | TRUE |  1.14 | FALSE | 86.58 | 82.17 | 76.58 |  |  |  | FALSE | FALSE |
| OS_pembro | rp_hazard_k3 | 1042.50 | 1065.82 | 0.9759 | 0.529 | TRUE |  1.40 | TRUE | 86.69 | 81.82 | 75.47 |  |  |  | FALSE | FALSE |
| OS_pembro | rp_odds_k1 | 1039.58 | 1053.58 | 0.9759 | 0.729 | TRUE |  1.22 | FALSE | 86.52 | 82.37 | 77.32 |  |  |  | FALSE | FALSE |
| OS_pembro | rp_odds_k2 | 1041.74 | 1060.40 | 0.9759 | 0.695 | TRUE |  1.14 | FALSE | 86.58 | 82.23 | 76.89 |  |  |  | FALSE | FALSE |
| OS_pembro | rp_odds_k3 | 1042.51 | 1065.83 | 0.9759 | 0.532 | TRUE |  1.40 | TRUE | 86.68 | 81.87 | 75.83 |  |  |  | FALSE | FALSE |
| OS_pembro | cure_weibull | 1049.00 | 1062.99 | 0.9398 | 1.334 | FALSE |  1.44 | TRUE | 86.31 | 84.09 | 80.80 |  |  |  | FALSE | FALSE |
| OS_pembro | cure_lnorm | 1041.23 | 1055.22 | 0.9759 | 0.883 | TRUE |  1.10 | TRUE | 86.42 | 83.27 | 79.42 |  |  |  | TRUE | FALSE |
| OS_pembro | cure_llogis | 1042.74 | 1056.74 | 0.9759 | 0.854 | TRUE |  1.32 | TRUE | 86.33 | 83.57 | 79.79 |  |  |  | FALSE | FALSE |
| OS_placebo | exp |  719.38 |  723.34 | 0.8193 | 3.017 | FALSE |  0.06 | TRUE | 81.89 | 67.06 | 44.97 |  |  |  | FALSE | FALSE |
| OS_placebo | weibull |  720.35 |  728.28 | 0.8313 | 2.930 | FALSE | 15.98 | FALSE | 82.17 | 65.38 | 39.87 |  |  |  | FALSE | FALSE |
| OS_placebo | lnorm |  711.25 |  719.19 | 0.8795 | 2.473 | FALSE |  1.98 | TRUE | 81.56 | 67.61 | 50.59 |  |  |  | FALSE | FALSE |
| OS_placebo | llogis |  718.10 |  726.03 | 0.8313 | 2.693 | FALSE |  3.98 | TRUE | 81.80 | 66.27 | 46.20 |  |  |  | FALSE | FALSE |
| OS_placebo | gompertz |  720.88 |  728.82 | 0.8193 | 3.470 | FALSE |  0.02 | TRUE | 81.58 | 69.14 | 54.22 |  |  |  | FALSE | FALSE |
| OS_placebo | gengamma |  705.46 |  717.36 | 0.9398 | 1.787 | FALSE |  1.42 | TRUE | 80.97 | 71.54 | 62.45 |  |  |  | FALSE | FALSE |
| OS_placebo | rp_hazard_k1 |  703.10 |  715.00 | 0.9518 | 1.526 | TRUE |  1.78 | TRUE | 80.69 | 71.44 | 59.07 |  |  |  | FALSE | FALSE |
| OS_placebo | rp_hazard_k2 |  702.91 |  718.77 | 0.9518 | 1.472 | TRUE |  1.48 | TRUE | 81.10 | 70.20 | 55.04 |  |  |  | TRUE | FALSE |
| OS_placebo | rp_hazard_k3 |  705.06 |  724.89 | 0.9518 | 1.481 | TRUE |  1.46 | TRUE | 81.15 | 69.99 | 54.35 |  |  |  | FALSE | FALSE |
| OS_placebo | rp_odds_k1 |  702.97 |  714.87 | 0.9518 | 1.498 | TRUE |  1.76 | TRUE | 80.66 | 71.68 | 60.60 |  |  |  | FALSE | FALSE |
| OS_placebo | rp_odds_k2 |  702.92 |  718.79 | 0.9518 | 1.473 | TRUE |  1.46 | TRUE | 81.08 | 70.54 | 57.23 |  |  |  | FALSE | FALSE |
| OS_placebo | rp_odds_k3 |  705.06 |  724.89 | 0.9518 | 1.466 | TRUE |  1.48 | TRUE | 81.14 | 70.29 | 56.53 |  |  |  | FALSE | FALSE |
| OS_placebo | cure_weibull |  710.79 |  722.69 | 0.8916 | 1.777 | FALSE |  2.36 | TRUE | 80.40 | 75.50 | 72.47 |  |  |  | FALSE | FALSE |
| OS_placebo | cure_lnorm |  704.87 |  716.77 | 0.9518 | 1.566 | TRUE |  1.76 | TRUE | 80.46 | 74.09 | 69.50 |  |  |  | FALSE | FALSE |
| OS_placebo | cure_llogis |  707.20 |  719.10 | 0.9518 | 1.785 | TRUE |  2.00 | TRUE | 80.25 | 74.71 | 70.43 |  |  |  | FALSE | FALSE |

图：KM 与拟合曲线 `fig_fit_*.png`；超额风险与平滑后的 KM 风险 `fig_hazard_*.png`。

## 7. 引擎结构

状态：无事件、术前进展（2026-10-22 新增）、局部区域复发（含第二原发癌）、远处复发（复发后月数的隧道态）、死亡。首发事件构成（2024 年 Table 1，IA7）与分配：无法手术的进展 → 术前进展（比例为报告例数除以该臂非 pCR 人数，时间分布按非 pCR 层术前 KM 的形状）；局部区域复发与第二原发癌 → 局部区域复发；远处复发 → 远处复发；无复发死亡 → 死亡（扣除术后无事件人时中预期的背景死亡，因背景死亡单列；2026-10-22 起再扣除单列的因不良事件死亡）。

| arm | any_event | progression_precluding_surgery | preprog_share_of_arm_pct | preprog_share_of_nonpCR_pct | local | distant | second_primary | death | second_primary_share_of_EFS_events_pct | expected_background_deaths | ae_deaths | death_without_recurrence_used | share_LRR | share_DR | share_death |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pembro | 159 | 14 | 1.79 | 4.83 | 33 | 77 | 16 | 19 | 10.1 | 6.0 | 7 | 6.0 | 0.371 | 0.583 | 0.046 |
| placebo | 114 | 15 | 3.85 | 8.67 | 20 | 56 | 10 | 13 | 8.8 | 2.7 | 1 | 9.3 | 0.315 | 0.588 | 0.098 |

因不良事件死亡（2026-10-22，`ae_deaths.csv`）：nejmoa2112651_appendix.pdf 的 Table S5（p.23；IA4，数据截点 March 23, 2021）中「因不良事件死亡」的人数，帕博利珠单抗组 7/783，安慰剂组 1/389（安全性分析人群）。用这一次而不用最新报告（2024 年，IA7）的理由：2024 年正文只给出治疗相关不良事件导致的死亡（4/1，NEJMoa2409932.pdf p.6），没有全部因不良事件死亡的人数；而 2022 年与 2024 年正文都写明全部患者在 February 2020 前完成试验治疗（NEJMoa2112651.pdf p.6），IA4 之后不会再有治疗期内的不良事件死亡。两臂分别设定，在治疗期（术前加术后，1 年）内以常数风险从无事件状态发生，pCR 层与非 pCR 层用同一风险，故不随 pCR 比例改变；不参与校准。术后部分属于 EFS 模型的超额风险，从中扣除（EFS 曲线不变），同时从构成中的无复发死亡扣除上述人数。情景：只计药物相关者（同表 4/1，与 2024 年正文的治疗相关死亡数相同），`config.R` 的 `ae_death_source = "drug_related"`。模型中 1 年内实际发生的因不良事件死亡占全臂：帕博利珠单抗 0.874%，安慰剂 0.249%（输入 0.894% 与 0.257%；术后风险上限起作用的周期数 0，差值为同期其他事件的竞争）。

pCR 比例：帕博利珠单抗 0.6301，安慰剂 0.5564。局部区域复发 → 远处复发 0.340/年（22/45 例，暴露 1.98 年）。术前进展后的超额死亡为进入后时间的 Weibull（形状自由；2026-10-22 第四轮，此前为常数），远处复发后的超额死亡为复发后时间的对数 logistic（形状自由，中位限定 10 至 12 个月），两者两臂共用，由校准估计（第 8 节）。

## 8. 校准（步骤 5，第四轮，2026-10-22）

### 8.1 设定

结构（用户指定，一次运行，不逐步试）：AE deaths (data) + PreProg Weibull + DR log-logistic, shapes free (common)。唯一的结构修改：术前进展后的超额死亡由常数风险改为术前进展后时间的 Weibull 分布（形状自由估计，两臂共用，由校准估计；按进入后的月数用隧道态记录）。理由：安慰剂组 KM 在约 13 个月前几乎是平的，之后才陡降（死亡累计：6 个月 0.26%，12 个月 1.28%，13 个月 1.54%，18 个月 6.15%，24 个月 8.98%），常数风险做不出这种形状；第三轮（常数风险）安慰剂组 12 个月落在区间外。
其余设定不变：远处复发后对数 logistic（形状自由、中位 10 至 12 个月、两臂共用）；因不良事件死亡（第 7 节）；带 5 年约束的 EFS 模型（第 6 节）。
校准量 4 个：术前进展 Weibull 的形状（限 0.01 至 50）与尺度（0.01 至 100 年），对数 logistic 的形状（0.01 至 50）与中位（10 至 12 个月）。目标函数不变：两臂 OS 与 2024 年 Fig. 1A 的 KM 在第 1 至 78 个月逐月的平方误差和最小（L-BFGS-B，6 个起点，目标值差 1.4e-10；`R/calibration.R`，与 `R/06_bootstrap.R` 共用）。

### 8.2 校准结果

| stage | arm | SSE_both_arms | rmse_pp | max_abs_diff_pp | gate_max_abs_diff_pp | preprog_shape | preprog_scale_years | dr_shape | dr_median_years |
|---|---|---|---|---|---|---|---|---|---|
| start value | pembro | 178.43 | 1.089 | 2.417 | 2.045 | 1.0000 | 1.0000 | 1.0000 | 0.9167 |
| start value | placebo | 178.43 | 1.050 | 2.236 | 1.936 | 1.0000 | 1.0000 | 1.0000 | 0.9167 |
| calibrated | pembro | 125.01 | 1.030 | 1.945 | 1.736 | 5.0877 | 1.0040 | 0.6991 | 0.8333 |
| calibrated | placebo | 125.01 | 0.735 | 1.583 | 1.254 | 5.0877 | 1.0040 | 0.6991 | 0.8333 |

校准值：术前进展 Weibull 形状 5.088、尺度 1.004 年（在范围内部）；对数 logistic 形状 0.699（< 1：复发后超额死亡风险从复发起单调递减），中位 10.00 个月（落在下界 10 个月）。
术前进展 Weibull 形状 5.09 意味着死亡集中在进入后约 11.2 个月附近：进入后 1 年生存 0.375，2 年生存 3.4e-15（`dr_survival_implied.csv`），即术前进展者 2 年内几乎全部死亡。

### 8.3 各时点的差与死亡来源的拆解

门槛 (a) 的逐时点表见文首「状态」。死亡来源（占全臂 %，`calibration_deaths_by_source.csv`）：

| arm | month | km_deaths | engine_deaths | from_event_free | from_ae | from_preprog | from_LRR | from_DR |
|---|---|---|---|---|---|---|---|---|
| pembro | 12 | 2.81 | 1.96 | 0.31 | 0.87 | 0.16 | 0.000 | 0.61 |
| pembro | 24 | 7.80 | 6.31 | 0.69 | 0.87 | 1.78 | 0.003 | 2.97 |
| pembro | 36 | 10.49 | 8.75 | 0.96 | 0.87 | 1.78 | 0.008 | 5.14 |
| pembro | 48 | 12.16 | 10.82 | 1.17 | 0.87 | 1.78 | 0.012 | 6.98 |
| pembro | 60 | 13.45 | 12.57 | 1.37 | 0.87 | 1.78 | 0.017 | 8.53 |
| placebo | 12 | 1.28 | 1.78 | 0.58 | 0.25 | 0.37 | 0.000 | 0.59 |
| placebo | 24 | 8.98 | 9.64 | 1.62 | 0.25 | 3.83 | 0.004 | 3.94 |
| placebo | 36 | 13.10 | 13.72 | 2.26 | 0.25 | 3.84 | 0.009 | 7.36 |
| placebo | 48 | 16.47 | 16.97 | 2.67 | 0.25 | 3.84 | 0.015 | 10.20 |
| placebo | 60 | 18.29 | 19.55 | 2.97 | 0.25 | 3.84 | 0.021 | 12.47 |

5 年 RMST（年，`calibration_rmst.csv`）：

| arm | rmst5_km | rmst5_engine | diff |
|---|---|---|---|
| pembro | 4.6079 | 4.6589 | 0.0510 |
| placebo | 4.5094 | 4.4821 | -0.0273 |
| pembro - placebo | 0.0985 | 0.1768 | 0.0783 |

模型 5 年内按死亡来源损失的 RMST（年，`calibration_rmst_by_source.csv`；RMST5 = 5 − 各来源之和；最后一行为各来源对模型两臂 RMST 差的贡献，KM 不能按来源拆分）：

| arm | event_free | ae | preprog | LRR | DR | total |
|---|---|---|---|---|---|---|
| pembro | 0.0380 | 0.0394 | 0.0652 | 0.0003 | 0.1982 | 0.3411 |
| placebo | 0.0856 | 0.0112 | 0.1391 | 0.0004 | 0.2816 | 0.5179 |
| placebo - pembro | 0.0476 | -0.0282 | 0.0739 | 0.0001 | 0.0834 | 0.1768 |

模型的两臂差 0.1768 年，比 KM 的 0.0985 年大 0.0783 年（仍在 KM 差的 bootstrap 区间内）。模型差中术前进展之后的死亡贡献 0.0739 年，远处复发后的死亡 0.0834 年，无事件状态中的死亡 0.0476 年，因不良事件死亡 -0.0282 年。第 2 至 4 年帕博利珠单抗组模型 OS 高于 KM（第 8.4 节的情景针对这一点）。

### 8.4 情景「OS 锚定」（不参与基准校准）

帕博利珠单抗组（单用与加运动）的远处复发后超额死亡风险乘以系数 k，其余参数固定在基准校准值，求 k 使模型的 5 年 RMST 两臂差等于 KM 的 0.0985 年。理由见 `docs/model_spec.md`。结果：k = 2.007；帕博利珠单抗组 5 年 RMST 由 4.6589 年降为 4.5806 年，两臂差 0.0985 年。引擎中为开关 `survival_engine(..., os_anchor = TRUE)`，只作用于帕博利珠单抗组；第 2 阶段只用于涉及帕博利珠单抗的比较。

该情景下各时点的 OS 与 KM 的差（`os_anchor_gate.csv`；安慰剂组不变）：

| arm | month | km | ci95_lo | ci95_hi | engine_base | engine_anchor | diff_anchor | inside_anchor |
|---|---|---|---|---|---|---|---|---|
| pembro | 12 | 97.19 | 96.04 | 98.35 | 98.04 | 97.61 | 0.420 | 是 |
| pembro | 24 | 92.20 | 90.34 | 94.10 | 93.69 | 92.18 | -0.024 | 是 |
| pembro | 36 | 89.51 | 87.39 | 91.68 | 91.25 | 89.12 | -0.392 | 是 |
| pembro | 48 | 87.84 | 85.58 | 90.16 | 89.18 | 86.71 | -1.136 | 是 |
| pembro | 60 | 86.55 | 84.19 | 88.98 | 87.43 | 84.76 | -1.791 | 是 |
| placebo | 12 | 98.72 | 97.61 | 99.84 | 98.22 | 98.22 | -0.500 | 是 |
| placebo | 24 | 91.02 | 88.23 | 93.90 | 90.36 | 90.36 | -0.659 | 是 |
| placebo | 36 | 86.90 | 83.62 | 90.32 | 86.28 | 86.28 | -0.625 | 是 |
| placebo | 48 | 83.53 | 79.92 | 87.30 | 83.03 | 83.03 | -0.505 | 是 |
| placebo | 60 | 81.71 | 77.95 | 85.65 | 80.45 | 80.45 | -1.254 | 是 |

### 8.5 隐含的中位生存与外部对照

模型隐含的中位生存（月，`dr_survival_implied.csv`；术前进展从 49.5 岁、远处复发从 50.5 岁计背景死亡）：

| state | median_excess_only_months | median_all_cause_months | surv_1y | surv_2y |
|---|---|---|---|---|
| PreProg | 11.2 | 11.2 | 0.375 | 3.39e-15 |
| DR | 10.0 | 10.0 | 0.468 | 0.351 |

文献：ESME 全国队列，新辅助或辅助化疗结束后 12 个月内转移复发的 TNBC 中位 OS 10.1 个月（95% CI 9.3 至 10.9），12 个月以后复发为 17.1 个月（Eur J Cancer 2023;189:112935，PMID 37385070）；IMpassion132，12 个月内复发的 PD-L1 阳性晚期 TNBC 中位 OS 安慰剂组 11.2 个月、阿替利珠单抗组 12.1 个月（Ann Oncol 2024;35:630-642，PMID 38755096）。远处复发后的中位由约束保持在此范围内（落在下界）。

### 8.6 未用于校准的曲线

与引擎的对照（`engine_checks.csv`，各曲线全部时点中差的绝对值最大者，百分点）：

| check | arm | max_abs_diff |
|---|---|---|
| DRFS vs 2022 Fig. S3 (IA4) | pembro | 1.151 |
| EFS vs 2024 Fig. 2A (IA7) | pembro | 0.633 |
| OS non-pCR vs 2024 Fig. S4 (IA7) | pembro | 4.363 |
| OS pCR vs 2024 Fig. S4 (IA7) | pembro | 0.874 |
| DRFS vs 2022 Fig. S3 (IA4) | placebo | 3.106 |
| EFS vs 2024 Fig. 2A (IA7) | placebo | 1.952 |
| OS non-pCR vs 2024 Fig. S4 (IA7) | placebo | 3.898 |
| OS pCR vs 2024 Fig. S4 (IA7) | placebo | 1.490 |

图：`fig_calibration_OS.png`（灰带为 KM 逐点 95% CI，竖线为门槛时点）、`fig_engine_checks.png`。

### 8.7 第三轮的可行性扫描（保留，只作诊断）

`R/05b_gate_feasibility.R` 保留为诊断，结构为第三轮（术前进展后常数死亡率）、门槛 (b) 为第三轮的相对误差 ≤ 20%：网格 1875 点加离网格细化，满足 (a) 的参数 0 组、两者都满足的 0 组（`calibration_gate_feasibility_*.csv`）。第四轮改用 Weibull 后不再需要。

## 9. Bootstrap（步骤 6，`R/06_bootstrap.R`）

B = 1000，随机种子 20261021（第 b 次用种子 + b），并行，耗时 107.0 分钟。每次：
1. 分层 EFS（2022 年补充材料 Fig. S4，IA4）：在各臂内连同 pCR 标签重抽样，pCR 比例与各层人数随之变动；各层在手术时点 landmark，用与基准相同的分布族重拟合并加 5 年约束（边界固定）；术前 KM 重算。
2. 术前进展的进入比例 = 报告例数 / 重抽样后的非 pCR 人数（全臂比例保持报告值）。
3. OS（2024 年 Fig. 1A，IA7）：在各臂内重抽样；所选的 OS 模型重拟合（只保存，引擎不用；RP 结点固定在基准位置）。
4. 按第 8 节的方法对重抽样后的 OS KM 重新校准 4 个参数（基准估计值加基准的 6 个起点，取最优）。
5. OS 锚定情景的 k 按重抽样后的 KM 两臂 RMST 差重新求解（k 限 0.01 至 100）。
6. 引擎在 5、10、20 年的 EFS 与 OS（臂 × pCR）。
每次都固定的数据设定：生命表、EFS 事件构成与分配比例、因不良事件死亡、局部区域复发 → 远处复发的率、术前进展例数、5 年约束的边界。拟合失败的样本换种子重抽（计入 attempts）。

结果：完成 1000 次，10 次重抽仍失败 0 次，换种子重抽的样本 0 个。校准的 optim 返回码非 0 的 24 次（0: 976，52: 24）。有参数落在边界的 945 次，其中对数 logistic 中位落在下界 10 个月的 943 次。OS 锚定的 k 在 0.01 至 100 内无解的 131 次（模型差无法降到该样本的 KM 差；该情景的分位数只用有解的样本）。5 年约束起作用的次数：EFS_pembro_pCR 132，EFS_pembro_nonpCR 116，EFS_placebo_pCR 129，EFS_placebo_nonpCR 205。

识别性：OS 只约束校准参数的组合，单个参数识别不良。术前进展 Weibull 的形状落在边界（0.01 或 50）的 82 次、尺度落在边界（0.01 或 100 年）的 132 次，对数 logistic 的形状落在边界的 41 次；对数 logistic 的中位在 943/1000 个样本中落在下界 10 个月，即 OS 数据倾向于比文献更短的复发后生存，被约束挡住。引擎的 EFS 与 OS 输出（第 10 节）的区间远比这些参数的区间窄。OS 锚定情景的区间只用 k 有解的 869 个样本；无解的样本是模型差偏大、需要更强锚定的样本，故该区间偏向锚定较弱的一侧。

参数的基准值与 bootstrap 分布（`output/phase1/bootstrap_summary.csv`；参数矩阵在 `data/bootstrap/`，一行一个样本）：

| group | quantity | base | boot_mean | boot_median | boot_lo | boot_hi | n_finite |
|---|---|---|---|---|---|---|---|
| calibration | preprog_shape | 5.0877 | 10.0425 | 4.9196 | 0.1184 | 50.0000 | 1000 |
| calibration | preprog_scale | 1.0040 | 12.7167 | 1.0039 | 0.0100 | 100.0000 | 1000 |
| calibration | dr_shape | 0.6991 | 2.6645 | 0.8195 | 0.2368 | 50.0000 | 1000 |
| calibration | dr_median | 0.8333 | 0.8516 | 0.8333 | 0.8333 | 1.0000 | 1000 |
| calibration | os_anchor_k | 2.0073 | 2.6371 | 1.6980 | 0.3890 | 10.9789 |  869 |
| calibration | sse |    NA | 316.3943 | 238.0665 | 59.2148 | 1041.1352 | 1000 |
| calibration | km_rmst5_diff |    NA | 0.1002 | 0.1020 | -0.0355 | 0.2358 | 1000 |
| calibration | engine_rmst5_diff |    NA | 0.1663 | 0.1671 | 0.0910 | 0.2371 | 1000 |
| pCR and PreProg | n_EFS_pembro_pCR |    NA | 493.4670 | 493.0000 | 465.0000 | 520.0000 | 1000 |
| pCR and PreProg | pre7_EFS_pembro_pCR | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1000 |
| pCR and PreProg | n_EFS_pembro_nonpCR |    NA | 290.5330 | 291.0000 | 264.0000 | 319.0000 | 1000 |
| pCR and PreProg | pre7_EFS_pembro_nonpCR | 0.9478 | 0.9480 | 0.9488 | 0.9215 | 0.9723 | 1000 |
| pCR and PreProg | p_pcr_pembro | 0.6301 | 0.6294 | 0.6288 | 0.5931 | 0.6633 | 1000 |
| pCR and PreProg | q_pre_pembro | 0.0483 | 0.0483 | 0.0481 | 0.0439 | 0.0530 | 1000 |
| pCR and PreProg | n_EFS_placebo_pCR |    NA | 217.0240 | 217.0000 | 197.0000 | 236.0250 | 1000 |
| pCR and PreProg | pre7_EFS_placebo_pCR | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1000 |
| pCR and PreProg | n_EFS_placebo_nonpCR |    NA | 172.9760 | 173.0000 | 153.9750 | 193.0000 | 1000 |
| pCR and PreProg | pre7_EFS_placebo_nonpCR | 0.9241 | 0.9245 | 0.9258 | 0.8808 | 0.9639 | 1000 |
| pCR and PreProg | p_pcr_placebo | 0.5564 | 0.5565 | 0.5564 | 0.5051 | 0.6052 | 1000 |
| pCR and PreProg | q_pre_placebo | 0.0867 | 0.0870 | 0.0867 | 0.0777 | 0.0974 | 1000 |

EFS 模型参数（自然尺度）：

| group | quantity | base | boot_mean | boot_median | boot_lo | boot_hi | n_finite |
|---|---|---|---|---|---|---|---|
| EFS model parameters | EFS_pembro_pCR_shape | 0.6787 | 0.7049 | 0.6930 | 0.5022 | 0.9958 | 1000 |
| EFS model parameters | EFS_pembro_pCR_scale | 178.9630 | 246.4411 | 163.5350 | 48.3296 | 949.4501 | 1000 |
| EFS model parameters | EFS_pembro_nonpCR_theta | 0.6426 | 0.6270 | 0.6426 | 0.4480 | 0.7151 | 1000 |
| EFS model parameters | EFS_pembro_nonpCR_shape | 0.8954 | 0.9195 | 0.9118 | 0.7021 | 1.2040 | 1000 |
| EFS model parameters | EFS_pembro_nonpCR_scale | 1.3566 | 1.5742 | 1.3177 | 0.8615 | 3.8925 | 1000 |
| EFS model parameters | EFS_placebo_pCR_shape | 0.7684 | 0.7963 | 0.7809 | 0.5949 | 1.0748 | 1000 |
| EFS model parameters | EFS_placebo_pCR_scale | 72.0203 | 83.8731 | 65.5822 | 27.0853 | 232.9611 | 1000 |
| EFS model parameters | EFS_placebo_nonpCR_theta | 0.5283 | 0.5165 | 0.5226 | 0.3417 | 0.6293 | 1000 |
| EFS model parameters | EFS_placebo_nonpCR_shape | 1.1970 | 1.2368 | 1.2221 | 0.9178 | 1.6449 | 1000 |
| EFS model parameters | EFS_placebo_nonpCR_scale | 1.4708 | 1.6004 | 1.4538 | 1.0276 | 3.0936 | 1000 |

文件：`boot_efs_params.csv`、`boot_efs5_binding.csv`、`boot_os_model_params.csv`、`boot_pcr_preprog.csv`、`boot_pre_surgery_km.csv`、`boot_calibration.csv`、`boot_outputs.csv`、`boot_replicates.rds`。

## 10. 生存引擎的输出（步骤 7，`R/07_engine_outputs.R`）

随机化后 5、10、20 年的 EFS 与 OS（%，基准值与 bootstrap 95% 分位区间；`engine_outputs.csv`、`engine_curves.csv`）。第 1 阶段没有运动参数，故加运动的两臂与对应的不加运动的臂相同；OS 锚定情景只改变帕博利珠单抗组的 OS（EFS 不变）。

| 终点 | 情景 | 臂 | pCR | 5 年 | 10 年 | 20 年 |
|---|---|---|---|---|---|---|
| EFS | 基准 | 单用化疗（= 化疗加运动） | 全体 | 71.1 (66.6–76.0) | 66.0 (58.0–72.1) | 58.7 (45.7–66.6) |
| EFS | 基准 | 单用化疗（= 化疗加运动） | pCR | 88.8 (83.7–92.3) | 80.9 (71.0–87.6) | 69.3 (48.7–81.1) |
| EFS | 基准 | 单用化疗（= 化疗加运动） | 非 pCR | 48.8 (43.1–57.3) | 47.3 (33.4–56.4) | 45.5 (29.6–54.1) |
| EFS | 基准 | 化疗加帕博利珠单抗（= 两者都加） | 全体 | 80.8 (77.8–83.4) | 76.8 (70.6–80.5) | 71.4 (60.4–76.8) |
| EFS | 基准 | 化疗加帕博利珠单抗（= 两者都加） | pCR | 91.7 (89.3–94.0) | 86.8 (80.4–91.0) | 79.7 (65.7–86.7) |
| EFS | 基准 | 化疗加帕博利珠单抗（= 两者都加） | 非 pCR | 62.3 (56.7–67.7) | 59.8 (48.4–66.5) | 57.4 (42.1–63.9) |
| OS | 基准 | 单用化疗（= 化疗加运动） | 全体 | 80.5 (77.1–83.5) | 72.4 (66.3–76.6) | 63.0 (53.0–69.2) |
| OS | 基准 | 单用化疗（= 化疗加运动） | pCR | 93.2 (90.3–95.2) | 85.9 (78.7–90.3) | 73.7 (58.0–82.8) |
| OS | 基准 | 单用化疗（= 化疗加运动） | 非 pCR | 64.5 (57.9–72.0) | 55.4 (44.0–63.8) | 49.5 (35.3–58.4) |
| OS | 基准 | 化疗加帕博利珠单抗（= 两者都加） | 全体 | 87.4 (84.7–89.6) | 81.4 (76.5–85.0) | 74.2 (64.4–79.0) |
| OS | 基准 | 化疗加帕博利珠单抗（= 两者都加） | pCR | 94.8 (93.1–96.0) | 90.0 (85.5–92.7) | 82.0 (70.8–87.5) |
| OS | 基准 | 化疗加帕博利珠单抗（= 两者都加） | 非 pCR | 74.9 (68.7–80.1) | 66.8 (56.9–74.1) | 60.8 (47.2–69.1) |
| OS | OS 锚定 | 化疗加帕博利珠单抗（= 两者都加） | 全体 | 84.8 (82.7–89.4) | 78.7 (74.3–84.1) | 72.0 (62.8–77.7) |
| OS | OS 锚定 | 化疗加帕博利珠单抗（= 两者都加） | pCR | 93.7 (91.6–95.8) | 88.5 (83.8–92.3) | 80.4 (69.3–87.2) |
| OS | OS 锚定 | 化疗加帕博利珠单抗（= 两者都加） | 非 pCR | 69.6 (65.3–79.0) | 62.1 (54.3–72.3) | 57.8 (45.9–66.9) |

各 bootstrap 样本的引擎由保存的参数矩阵重建，其 5、10、20 年的值与 `06_bootstrap.R` 当时算出的一致（1000 个样本，最大差 0.0e+00，`bootstrap_rebuild_check.csv`）。

图：`fig_engine_outputs.png`（实线为引擎，带为 bootstrap 95% 区间，虚线为重建的 KM）。

引擎接口：`survival_engine(arm, pcr, times, params, hr0, wane_start, wane_rate, p_pcr, nonpcr_mix, os_anchor)`，`arm` 为 chemo、exercise、pembro、both；默认参数在 `data/fits/engine_params.rds`。运动钩子 (a) 时变 HR 与 (b) pCR 比例、S-JP 混合的接口测试见 `engine_interface_test.csv`；闭式计算与逐周期递推一致（`R/test_engine_vectorized.R`）。

| test | EFS_1y | EFS_3y | EFS_5y | EFS_10y | EFS_20y | OS_1y | OS_3y | OS_5y | OS_10y | OS_20y |
|---|---|---|---|---|---|---|---|---|---|---|
| chemo base | 91.094 | 75.964 | 71.051 | 66.009 | 58.695 | 98.218 | 86.278 | 80.452 | 72.395 | 62.954 |
| nonpcr_mix with all HR = 1 | 91.094 | 75.964 | 71.051 | 66.009 | 58.695 | 98.218 | 86.278 | 80.452 | 72.395 | 62.954 |
| exercise path A with hr0 = 1 | 91.094 | 75.964 | 71.051 | 66.009 | 58.695 | 98.218 | 86.278 | 80.452 | 72.395 | 62.954 |
| S-JP (test weights) | 91.896 | 78.965 | 74.410 | 69.389 | 61.943 | 98.394 | 87.735 | 82.585 | 75.138 | 65.879 |
| S-JP + exercise path A, 6 months continued (test values) | 92.581 | 81.216 | 76.743 | 71.674 | 64.075 | 98.488 | 88.713 | 84.000 | 76.956 | 67.784 |
| exercise path B: pCR + 5 points (test value) | 91.860 | 77.850 | 73.047 | 67.690 | 59.885 | 98.330 | 87.404 | 81.890 | 73.923 | 64.162 |
| pembro base | 92.930 | 84.095 | 80.794 | 76.832 | 71.425 | 98.042 | 91.245 | 87.426 | 81.439 | 74.156 |
| pembro + S-JP (test weights) | 93.688 | 86.090 | 83.055 | 79.173 | 73.682 | 98.181 | 92.156 | 88.793 | 83.292 | 76.172 |
| chemo with os_anchor = TRUE (no effect) | 91.094 | 75.964 | 71.051 | 66.009 | 58.695 | 98.218 | 86.278 | 80.452 | 72.395 | 62.954 |
| pembro, OS anchor scenario | 92.930 | 84.095 | 80.794 | 76.832 | 71.425 | 97.609 | 89.117 | 84.761 | 78.718 | 72.043 |

## 11. 已决事项与待决事项

已决：
- 层内 HR 的较晚截点参照值：撤出门槛，改为跨分析对照（2026-10-21）。
- 准则 1：保留 95%，最初 100% 为设定错误（2026-10-21）。
- 分布族：同一层两臂同一族，依两臂合计 AIC 与 5 年外推检验选定，次优族为情景（2026-10-21）；非 pCR 层复核后维持（2026-10-22）。
- 第二原发癌：归入局部区域复发（2026-10-21）。
- 校准结构：术前进展单列、远处复发后对数 logistic（两臂共用，中位 10 至 12 个月），不用两臂分别估计的复发后死亡率（2026-10-22）。
- 校准第三轮（2026-10-22）：门槛 (a) 与 (b)；因不良事件死亡单列；对数 logistic 形状自由；EFS 加 5 年约束。
- 校准第四轮（2026-10-22）：门槛 (b) 改为 KM 差的 bootstrap 区间；术前进展后死亡改为 Weibull；新增 OS 锚定情景（不参与基准校准）。

待决：
- 若尾崎日后提供 2023-03-23 截点的分层 KM，5 年约束改为用整条曲线（2026-10-22 的决定）。

等尾崎回答：
- S-JP 的权重定义（`docs/model_spec.md` 第 2 节）。
- BRCA 检测的对象范围。
- 帕博利珠单抗组是否也加 S-JP。

