# 第1阶段（生存引擎）报告

生成时间：2026-10-25 04:23。由 `R/99_phase1_report.R` 从代码输出生成，表中数字均读自 `output/`、`data/` 与 `input/` 下的文件。模型规格见 `docs/model_spec.md`。

## 第1阶段最终状态

**第 1 阶段结束（2026-10-25）**：结构为第十五轮，bootstrap 为提交 b06c9b9 上的 1,000 次（Longleaf，基础种子 20261023，失败 0 次；第 19.4 节）。

第 1 阶段以**第十五轮**为最终结构（AE deaths (data) + PreProg log-logistic external (ESME early-relapse fit) + DR early/late log-logistic, shape and medians external (ESME fit, common shape), k fixed at 1 (common post-DR survival)）。依据：第十五轮的规则（`docs/acceptance_rule_round15.md`，git 475f828，在计算之前单独提交）——术前进展后的超额死亡不再校准，取 ESME 早期复发拟合的同一分布（与早期远处复发相同；bootstrap 中同一次 ESME 重抽样），原来的约束（中位 10 至 26 个月、5 年存活 ≥ 5%）撤销；其余同第十四轮（k 固定为 1，分层 EFS 约束为最终分析 7 年值的等式约束，修正后的引擎）。**模型中没有任何由 OS 校准的参数，OS 只用于验证**；三道门槛都达标（第 19 节）。修改的依据：第十四轮 Longleaf 的 1,000 次 bootstrap 中术前进展的两个参数由约束而不是数据决定（中位 829 次贴 10 个月、97 次贴 26 个月，5 年存活 686 次贴 5%）；外部数据能确定的量不交给校准。第十至十四轮只作记录（第 14 至 18 节；第十轮被接受的结果是用修正前的引擎算出的），第八轮及以前见第 1 至 12 节，第九轮见第 13 节。

最终参数（第十五轮）：

| 参数 | 值 | 来源 |
|---|---|---|
| pCR 比例（帕博利珠单抗 / 安慰剂） | 0.6301 / 0.5564 | 数据（K22 (IA4)） |
| 分层 EFS 约束 | 随机化后 84 个月的分层 EFS 固定为最终分析的报告值（90.4、85.9、57.6、49.7%） | 等式约束（第十一轮修改，最终分析 J Clin Oncol 2026;44(16_suppl):507） |
| 术前进展后超额死亡：对数 logistic 中位（月） | 9.73 | 外部输入：ESME 早期复发的拟合，与早期远处复发相同（第十五轮） |
| 术前进展后超额死亡：形状 | 1.6598 | 外部输入：同上 |
| 远处复发后超额死亡：形状（早期 / 晚期） | 1.6598 / 1.6598 | 外部输入（ESME 重建个体数据的对数 logistic 拟合，共用形状） |
| 远处复发后中位：早期（月） | 9.73 | 外部输入（ESME 拟合） |
| 远处复发后中位：晚期（月） | 16.93 | 外部输入（ESME 拟合） |
| 早期远处复发的界线（随机化后月数） | 18 | 用户指定（第 8.1 节） |
| 帕博利珠单抗组远处复发后风险的倍数 k | 1 | 固定为 1（第十四轮：远处复发后生存两臂共用，全部来自 ESME） |
| 因不良事件死亡（帕博利珠单抗 / 安慰剂） | 7/783、1/389 | 数据（2022 年补充材料 Table S5） |
| 局部区域复发 → 远处复发（/年） | 0.3395 | 数据（2022 年 Table 1 脚注） |

术前进展者进入后的全死因存活（49.5 岁起的背景生存 × 超额生存）：1 年 41.3%、5 年 4.6%（第十四轮的校准值：42.5%、5.0%）。

门槛结果（接受规则 `docs/acceptance_rule_round15.md`，运行前提交）：
- (a) 按 Bonferroni 同时区间接受：10 个点中 8 个落在 KM 逐点 95% 区间内，区间外 帕博利珠单抗 24 个月、帕博利珠单抗 36 个月，超出 0.411、0.022 个百分点；全部 10 个点落在逐点 99.5% 区间内。
- (b) 达标：模型 5 年 RMST 两臂差 0.1524 年，KM 差的 bootstrap 95% 区间 -0.0381 至 0.2421 年。
- (c) 达标：7 年 OS 与 EFS 的 4 个值中 4 个落在最终分析的 95% 区间内（帕博利珠单抗 7 年 OS 83.24，报告 85.1 [82.5, 87.5]）。

情景（只报告，不参与采用判定；`R/18_round15_scenarios.R`）：「早期复发后 k（外部）」k = 1.307 同时作用于早期远处复发与帕博利珠单抗组的术前进展，门槛 (a) 满足、(b) 满足、(c) 满足；「术前进展后生存（Elmore）」中位 26 个月，门槛 (a) **不满足**、(b) 满足、(c) 满足。第 2 阶段所有涉及帕博利珠单抗的结果以「基准」与「早期复发后 k（外部）」两栏并列报告；Elmore 列入第 2 阶段的情景清单（`docs/model_spec.md` 第 6 节）。

bootstrap：第十五轮的 1,000 次在 Longleaf 上完成（结果提交 b06c9b9，运行于提交 f806079，其 `R/` 与 8dcab58 相同；基础种子 20261023；失败 0 次、重抽 0 次；没有校准参数，校准的边界标记都为 0），结果在 `data/bootstrap/`（第十四轮与第八轮的 1,000 次在 `data/bootstrap/round14/`、`round8/`）。本地参照 `output/check/bootstrap10_local.rds`（提交 bb5d7bc 生成）与 Longleaf 的核对通过。第 19.4 节。

待尾崎回答：
- 含帕博利珠单抗的组的 S-JP 数值 F01P、F04P（尾崎正向临床医生确认；结构已于 2026-10-23 决定，见第 11 节）。
- B30 的定义（第 2 阶段入力表）。
- 按 pCR 分层的 EFS 层内 HR 较晚截点值（0.65、0.72）的原始出处（第 4 节）。

## 状态

- 已完成：步骤 1 至 4（含 2026-10-21 与 2026-10-22 的修正）与一致性检查；非 pCR 层分布族已复核。
- 重建与一致性的门槛项 62 项，不达标 0 项。
- 步骤 5（校准第八轮，2026-10-22，远处复发分为早期与晚期）：按运行前确定的接受规则（`docs/acceptance_rule_round8.md`，git e0a722c；与第七轮相同）**接受**。门槛 (a)：10 个点中 9 个落在逐点 95% 区间内，区间外 1 处（安慰剂 12 个月），超出幅度 0.163 个百分点，均 ≤ 0.3 且全部 10 个点落在 Bonferroni 校正后的逐点 99.5% 区间内，按规则 (i)、(ii) 接受；门槛 (b)：模型的 5 年 RMST 两臂差 0.1175 年，落在 KM 差（0.0985 年）的 bootstrap 95% 区间 -0.0381 至 0.2421 年内。
- 门槛 (c)（第七轮新增）：模型 7 年的 OS 与 EFS 4 个值中 4 个落在最终分析报告的 95% 区间内，达标（下表）。按 pCR 分层的 7 年 OS 只报告差值（第 8.2 节）。
- 帕博利珠单抗组远处复发后死亡风险的倍数 k = 1.492（第六轮 1.428，第七轮 1.411；范围 0.25 至 4，不在边界上）。术前进展后死亡的校准值贴在约束边界上（中位 = 10 个月，5 年存活 = 5%）。
- 远处复发中早期（随机化后 18 个月以内）所占比例：随机化后 7 年内的远处复发中，帕博利珠单抗组 32.2%、安慰剂组 28.9%；到 100 岁的全部远处复发中 23.7% 与 20.1%（第 8.2 节）。
- 步骤 6（bootstrap，B = 1000，k 在每个样本中一起估计，7 年目标值在每个样本中按抽样分布抽取）与步骤 7（引擎输出，含 7 年）已完成（第 9、10 节）。
- 第 1 阶段到此结束（2026-10-23）。第 2 阶段中涉及帕博利珠单抗的结果以基准与 k = 1 两栏并列报告（`docs/model_spec.md` 第 6 节；两臂差的对照见第 8.4 节）。
- 门槛的修改经过见下一节「门槛修改记录」（全部七项）。
- 第九轮（第 2 阶段准备，2026-10-23，远处复发后生存外部锚定于 ESME 曲线）：按第九轮的规则**未被接受**（门槛 (a) 超出 0.3 个百分点的上限），见第 13 节。第十轮按判定规则 A 采用第九轮结构（门槛 (a) 改为只用 Bonferroni 同时区间后接受），见第 14 节。以上各项与第 1 至 12 节为第八轮的快照。

各时点的方向：帕博利珠单抗组模型减 KM 的差在 5 个时点中 4 个为正，安慰剂组 5 个中 2 个为负。

门槛 (a)（`calibration_gate.csv`；ci995 为 Bonferroni 校正后的逐点 99.5% 区间，outside_pp 为落在 95% 区间外的幅度）：

| arm | month | km | ci95_lo | ci95_hi | ci995_lo | ci995_hi | engine | diff | inside | outside_pp | inside_995 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pembro | 12 | 97.19 | 96.04 | 98.35 | 95.54 | 98.86 | 97.46 | 0.275 | 是 | 0.000 | 是 |
| pembro | 24 | 92.20 | 90.34 | 94.10 | 89.55 | 94.93 | 93.50 | 1.301 | 是 | 0.000 | 是 |
| pembro | 36 | 89.51 | 87.39 | 91.68 | 86.49 | 92.64 | 90.63 | 1.123 | 是 | 0.000 | 是 |
| pembro | 48 | 87.84 | 85.58 | 90.16 | 84.62 | 91.19 | 88.28 | 0.439 | 是 | 0.000 | 是 |
| pembro | 60 | 86.55 | 84.19 | 88.98 | 83.19 | 90.05 | 86.31 | -0.244 | 是 | 0.000 | 是 |
| placebo | 12 | 98.72 | 97.61 | 99.84 | 97.13 | 100.00 | 97.45 | -1.273 | **否** | 0.163 | 是 |
| placebo | 24 | 91.02 | 88.23 | 93.90 | 87.05 | 95.18 | 91.68 | 0.661 | 是 | 0.000 | 是 |
| placebo | 36 | 86.90 | 83.62 | 90.32 | 82.23 | 91.84 | 87.41 | 0.504 | 是 | 0.000 | 是 |
| placebo | 48 | 83.53 | 79.92 | 87.30 | 78.41 | 88.98 | 84.03 | 0.498 | 是 | 0.000 | 是 |
| placebo | 60 | 81.71 | 77.95 | 85.65 | 76.38 | 87.41 | 81.31 | -0.393 | 是 | 0.000 | 是 |

门槛 (b)（`calibration_gate_rmst.csv`）：

| quantity | km | km_boot_ci95_lo | km_boot_ci95_hi | boot_B | engine | engine_minus_km | pass |
|---|---|---|---|---|---|---|---|
| 5-year OS RMST difference, pembro - placebo (years) | 0.0985 | -0.0381 | 0.2421 | 1000 | 0.1175 | 0.0190 | 达标 |

门槛 (c)（`calibration_final7y.csv`；报告值为 KEYNOTE-522 最终分析，J Clin Oncol 2026;44(16_suppl):507，截点 2025-10-14；engine_k1 为情景 k = 1，只作参照）：

| id | reported | ci95_lo | ci95_hi | engine | diff | inside_ci | engine_k1 | inside_ci_k1 | source |
|---|---|---|---|---|---|---|---|---|---|
| os7_pembro | 85.1 | 82.5 | 87.5 | 83.20 | -1.90 | 是 | 84.96 | 是 | OncLive 2026-06-01 |
| os7_placebo | 77.2 | 72.7 | 81.1 | 77.17 | -0.03 | 是 | 77.17 | 是 | OncLive 2026-06-01 |
| efs7_pembro | 78.3 | 75.3 | 81.1 | 78.89 | 0.59 | 是 | 78.89 | 是 | OncLive 2026-06-01 |
| efs7_placebo | 69.8 | 65.0 | 74.2 | 68.68 | -1.12 | 是 | 68.68 | 是 | OncLive 2026-06-01 |

## 门槛修改记录

按时间列出验证与校准门槛的每次修改。第 1 至 5 项是看到结果后修改的，第 4、5 项的理由是门槛比抽样误差更严；第 6 项在看到第五轮结果之后、第六轮运行之前确定，第 7 项在第七轮运行之前确定，两者都在运行前提交到 git。第八、九轮的接受规则与第七轮相同（`docs/acceptance_rule_round8.md`、`docs/acceptance_rule_round9.md`，均在运行前提交），门槛没有修改。第 8 项是看到第九轮结果之后做出的，作为第十轮判定规则 A 的一部分在诊断之前提交，规则 A 成立后生效。

| 序号 | 日期 | 对象 | 修改前 | 修改后 | 时点 | 看到的结果 | 理由 |
|---|---|---|---|---|---|---|---|
| 1 | 2026-10-21 | Yau 2022 的重建验证 | 里程碑差 ≤ 1 个百分点、HR 差 ≤ 0.03、事件数差 ≤ 2% 三项都作门槛 | 只保留里程碑为门槛；HR 与事件数只报告 | 看到结果后修改 | Yau 有 4 项不达标（事件数 2 项、HR 2 项） | HR 的估计量与原文不同（原文为 12 个队列、含队列效应的汇总模型，使用全部随访；重建只能在 12 年内做单一 Cox）；事件数的参照值从风险表推算，原文没有报告 |
| 2 | 2026-10-21 | 拟合准则 1（选模） | 模型落在 KM 逐点 95% CI 内的月份比例 = 100% | ≥ 95% | 看到结果后修改 | 6 条曲线中 3 条没有任何候选模型通过 | 设定错误：逐点 95% 置信区间本来就预期约 5% 的点落在区间外 |
| 3 | 2026-10-21 | 按 pCR 分层的 EFS 层内 HR（较晚截点的参照值） | 与参照值的差 ≤ 0.03（门槛） | 不作门槛的跨分析对照 | 看到结果后修改 | pCR 层重建 0.722 对参照 0.65，差 0.072 | 参照值来自比 IA4 更晚的数据截点，IA4 的曲线不可能与之吻合；IA4 原文印的 0.73 与 0.70 已在 0.012 以内复现 |
| 4 | 2026-10-22 | 校准门槛 | 各臂第 1 至 5 年整年时点 OS 与 KM 的差 ≤ 1 个百分点 | (a) 各臂第 1 至 5 年整年时点落在 KM 逐点 95% CI 内；(b) 5 年 RMST 两臂差相对误差 ≤ 20% | 看到结果后修改 | 第一轮（2026-10-21）与第二轮（2026-10-22）校准都不达标 | 门槛比抽样误差更严：1 个百分点小于安慰剂组（n = 390）5 年 OS 的 Greenwood 标准误 1.96 个百分点 |
| 5 | 2026-10-22 | 校准门槛 (b) | 5 年 RMST 两臂差：模型与 KM 的相对误差 ≤ 20%（允许 0.079 至 0.118 年） | (b) 模型的 5 年 RMST 两臂差落在 KM 差的 bootstrap 95% 区间内；点估计差距照常报告 | 看到结果后修改 | 第三轮校准不达标（(a) 与 (b) 都不达标） | 门槛比抽样误差更严：允许带宽 0.039 年，远窄于 KM 差的 bootstrap 95% 区间宽度 0.280 年 |
| 6 | 2026-10-22 | 校准门槛 (a) 的接受条件 | (a) 10 个点全部落在逐点 95% CI 内 | (a) 不达标时，同时满足 (i) 每个区间外的点超出 ≤ 0.3 个百分点、(ii) 全部 10 个点落在 Bonferroni 校正后的逐点 99.5% 区间内则接受；(b) 不变 | 看到第五轮结果之后、第六轮运行之前确定（git a53afe2 提交于运行前） | 第五轮门槛 (a) 不达标（有点落在逐点 95% 区间外） | 10 个时点各按 95% 检验，即使模型正确，也有相当大的概率至少一点落在区间外（若各点独立为 40%；同一臂的各时点正相关，实际略低） |
| 7 | 2026-10-22 | 校准门槛 (c)（新增） | 只有 (a)（含例外 (i)、(ii)）与 (b) | (a)、(b) 及例外不变；新增 (c) 模型 7 年的 OS 与 EFS 各臂落在最终分析报告的 95% 置信区间内；按 pCR 分层的 7 年 OS 只报告，不作门槛 | 第七轮运行之前确定（git f811ec4 提交于运行前） | 运行前记录（`r6_vs_final7y.csv`）：第六轮模型 7 年的 OS 与 EFS 4 个值中 4 个已落在最终分析的 95% 区间内 | 最终分析提供了 7 年的成熟数据，两臂 OS 差从 5 年时的 4.9 个百分点扩大到 7.9 个百分点 |
| 8 | 2026-10-23 | 校准门槛 (a) 的接受条件 | (a) 不达标时，同时满足 (i) 每个区间外的点超出 ≤ 0.3 个百分点、(ii) 全部 10 个点落在 Bonferroni 校正后的逐点 99.5% 区间内则接受 | (a) 不达标时，只要全部 10 个点落在 Bonferroni 校正后的逐点 99.5% 区间内即接受（去掉 (i)） | 看到第九轮结果之后做出；只在第十轮判定规则 A 成立时生效（`docs/acceptance_rule_round10.md`，git e8d2134，在诊断之前提交） | 第九轮：安慰剂 12 个月超出 95% 区间 0.303 个百分点，比 0.3 的上限多 0.003 个百分点；全部 10 个点在 99.5% 区间内 | 例外规则本来就以同时区间为统计依据，0.3 个百分点的附加上限没有统计依据；超出发生在安慰剂组 12 个月，该时点只有 5 例死亡（重建个体数据） |

## 1. 输入文件

| file | bytes | pages | sha256 |
|---|---|---|---|
| NEJMoa1910549.pdf |  586012 | 12 | 918ddcc6fb4751bcb2623c347e479960e6b0aac122d582054bfc1a2fdce01019 |
| NEJMoa2112651.pdf |  634005 | 12 | d706ac0b8c8bb886472d8fe14ebed855585fec468c2b6386d5102a4e79792be2 |
| NEJMoa2409932.pdf |  653287 | 11 | c65b2cbcffe20de49c4183d1775e817286e0ae8dee0c39d4e0ede0a394475aaf |
| PIIS0923753424001078.pdf | 1024307 | 13 | 5ddc526aa6dd3c86f2138e9f3bdb70c9f5c94353880f2b9f01734e001fec75c2 |
| SOURCE.md |     916 |  1 | 81f90a4544450e515153e5266e352198680d876f9a2a4305eb9a1e17ad73cfc4 |
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

栅格图中印的数字从图像转录，与正文文字层交叉核对 19 项，不一致 0 项（`data/transcription_checks.csv`）。报告值 221 个由正则从 PDF 文字层抽取（`data/reported_values.csv`）。

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

pCR 比例：帕博利珠单抗 0.6301，安慰剂 0.5564。局部区域复发 → 远处复发 0.340/年（22/45 例，暴露 1.98 年）。术前进展后的超额死亡为进入后时间的对数 logistic（第五轮；形状与中位在外部约束下校准），远处复发后的超额死亡为复发后时间的对数 logistic，按进入时点分早期与晚期两个子状态（第八轮；中位分别为外部输入，形状共用并校准；帕博利珠单抗组另乘 k，k 一起校准），两臂共用同一规则（第 8 节）。

## 8. 校准（步骤 5，第八轮，2026-10-22）

### 8.1 设定

结构（用户指定，一次运行）：AE deaths (data) + PreProg log-logistic (constrained) + DR early/late log-logistic, medians external, shared shape, x k in pembrolizumab arms。
- 远处复发后的超额死亡（第八轮的唯一修改）：远处复发按进入时点分为两个子状态。早期：随机化后 18 个月以内的远处复发（ESME 的定义为新辅助或辅助化疗结束后 12 个月以内；模型中化疗在第 24 周〔约 5.5 个月〕结束，5.5 + 12 = 17.5 个月，取整为 18；两臂同一规则）；晚期：其余。两者都是复发后时间的对数 logistic，中位为外部输入（不参与校准）：早期 10.1 个月、晚期 17.1 个月（ESME，Grinda 等 Eur J Cancer 2023，PMID 37385070）；形状两个子状态共用，由校准估计。帕博利珠单抗组两个子状态的风险都 × k，k 与其他参数一起校准（范围 0.25 至 4）。远处复发相关的费用（D03 至 D05）两个子状态相同。
- 术前进展后的超额死亡：进入后时间的对数 logistic，两臂共用，形状与中位校准；外部约束 1：中位 10 至 26 个月（下限为 ESME 早期复发的中位 OS 10.1 个月取整；上限为 Elmore 等 Ann Surg Oncol 2021;28:5477-5485、PMID 34247335 的新辅助治疗期间局部区域进展 124 例的中位 OS 26 个月，该队列多数后来接受手术〔摘要写 104 例、89.3%，按 124 例计为 83.9%〕，比「无法手术的进展」轻，只作上界）；外部约束 2：进入后 5 年的全因存活 ≥ 5%（同一篇中位随访 71 个月时 23.4% 无病存活，向下取保守值），实现为形状的上限。术前进展两臂合计 29 例（2024 年 Table 1）。
- 其余设定不变：因不良事件死亡（第 7 节）；带 5 年约束的 EFS 模型（第 6 节）；目标函数与第七轮相同。
- 校准：目标为两臂 OS 与 2024 年 Fig. 1A 的 KM 在第 1 至 78 个月逐月的平方误差和（百分点²，不变），加上 KEYNOTE-522 最终分析的 8 个 7 年时点（第七轮新增，见下）。L-BFGS-B，6 个起点，目标值差 4.1e-11。optim 返回码 52 时加 5 个随机起点取最优；基准校准的返回码为 0。
- 7 年时点的加权：每个点加 ((模型 − 报告值) / SE)²，SE 以百分点计。两臂 7 年 OS 与 EFS 有 95% 置信区间，SE = (上限 − 下限) / (2 × 1.96)；按 pCR 分层的 7 年 OS 没有置信区间，用二项近似 SE = √(p(1 − p)/n)，n 为该层人数（2024 年 IA7 的 pCR 人数，`data/pcr_counts.csv`），不考虑删失，故偏小（权重偏大）。KM 部分不变，相当于每个逐月点的 SE 为 1 个百分点。7 年 EFS 由步骤 4 的 EFS 模型决定，不受校准量影响，两个 EFS 点在目标函数中是常数。
- 数值来源（`data/kn522_final_7y.csv`，`input/papers/SOURCE.md`）：ascopubs.org 的摘要页返回 403，未取得；两臂 7 年 OS、EFS 及其置信区间与按 pCR 分层的 OS 读自 OncLive（2026-06-01），7 年 OS 与 CancerNetwork（2026-06-01）核对一致，按 pCR 分层的 OS 与 DelveInsight 核对一致；CareNet（2026-06-02）维护中未取得。截点 2025-10-14，中位随访 93.8 个月。按 pCR 分层的 OS 在报道中没有写明时点（OncLive 写作「at median follow-up」），按用户指示作 7 年值。
- 接受规则：运行前确定（2026-10-22，`docs/acceptance_rule_round8.md`，git e0a722c 提交于第八轮运行之前），与第七轮相同：(a)、(i)、(ii)、(b)、(c)；术前进展约束与 k 的边界照常报告，不作停止条件。另外报告 5 年与 7 年的两臂 OS 差（第 8.4 节）。

7 年目标值与权重（`final7y_targets()`）：

| id | arm | pcr | endpoint | month | reported | se_pp | n | weight_basis |
|---|---|---|---|---|---|---|---|---|
| os7_pembro | pembro | all | OS | 84 | 85.1 | 1.276 |  | 95% CI |
| os7_placebo | placebo | all | OS | 84 | 77.2 | 2.143 |  | 95% CI |
| efs7_pembro | pembro | all | EFS | 84 | 78.3 | 1.480 |  | 95% CI |
| efs7_placebo | placebo | all | EFS | 84 | 69.8 | 2.347 |  | 95% CI |
| os_pcr_pembro | pembro | pCR | OS | 84 | 94.5 | 1.025 | 495 | binomial, IA7 stratum size |
| os_pcr_placebo | placebo | pCR | OS | 84 | 91.1 | 1.933 | 217 | binomial, IA7 stratum size |
| os_nonpcr_pembro | pembro | nonpCR | OS | 84 | 69.0 | 2.721 | 289 | binomial, IA7 stratum size |
| os_nonpcr_placebo | placebo | nonpCR | OS | 84 | 59.8 | 3.728 | 173 | binomial, IA7 stratum size |

概率敏感性分析中远处复发后中位的分布：早期（`dr_median_draw()`）为两项研究的中位 OS 各取对数正态分布、等权混合（与此前相同）；晚期（`dr_late_median_draw()`）为 ESME 晚期复发的对数正态分布。对数正态的均值为 log(报告的中位)，标准误 = (log 上限 − log 下限) / (2 × 1.96)。bootstrap 中每个样本两个中位各自独立抽取，再校准其余参数。

| substate | source | median | lo | hi | weight | se_log |
|---|---|---|---|---|---|---|
| 早期 | ESME early relapse (Grinda 2023, PMID 37385070, abstract) | 10.1 |  9.3 | 10.9 | 0.5 | 0.0405 |
| 早期 | IMpassion132 placebo, PD-L1-positive (Dent 2024, PMID 38755096, p.6) | 11.2 |  9.0 | 13.3 | 0.5 | 0.0996 |
| 晚期 | ESME late relapse (Grinda 2023, PMID 37385070, abstract) | 17.1 | 15.7 | 18.2 | 1.0 | 0.0377 |

IMpassion132 已用全文核对（`input/papers/PIIS0923753424001078.pdf` p.6，PD-L1 阳性人群）：安慰剂组中位 OS 11.2 个月（95% CI 9.0 至 13.3），与此前采用的值一致，分布无需修正。参考：mITT 人群安慰剂组为 9.8 个月（8.4 至 12.0），未采用（主要分析为 PD-L1 阳性人群）。ESME 读自摘要（早期 10.1 个月，9.3 至 10.9；晚期 17.1 个月，15.7 至 18.2）。

### 8.2 校准结果

| stage | arm | SSE_both_arms | rmse_pp | max_abs_diff_pp | gate_max_abs_diff_pp | preprog_shape | preprog_median_months | preprog_shape_cap | dr_shape | dr_median_months | dr_late_median_months | pembro_dr_k |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| start value | pembro | 251.43 | 1.572 | 2.800 | 2.510 | 1.0000 | 12.00 | 1.8244 | 1.0000 | 10.10 | 17.10 | 1.0000 |
| start value | placebo | 251.43 | 0.867 | 1.898 | 1.294 | 1.0000 | 12.00 | 1.8244 | 1.0000 | 10.10 | 17.10 | 1.0000 |
| calibrated | pembro | 79.25 | 0.754 | 1.671 | 1.301 | 1.6387 | 10.00 | 1.6387 | 0.8765 | 10.10 | 17.10 | 1.4918 |
| calibrated | placebo | 79.25 | 0.669 | 2.042 | 1.273 | 1.6387 | 10.00 | 1.6387 | 0.8765 | 10.10 | 17.10 | 1.4918 |

k = 1.492（在 0.25 至 4 的内部；第六轮 1.428，第七轮 1.411）。远处复发后：形状 0.876（两个子状态共用），中位早期 10.1 个月、晚期 17.1 个月（外部输入）。

与第六、七轮的比较（`calibration_vs_previous.csv`；第六、七轮的值取自提交 e530a56、d1b5517 的输出，另存为 `r6_*.csv`、`r7_*.csv`；第七轮以前远处复发后只有一个中位）：

| quantity | round6 | round7 | round8 |
|---|---|---|---|
| pembro_dr_k | 1.4277 | 1.4110 | 1.4918 |
| preprog_median_months | 11.4387 | 11.3897 | 10.0000 |
| preprog_shape | 1.7717 | 1.7671 | 1.6387 |
| preprog_shape_cap | 1.7717 | 1.7671 | 1.6387 |
| dr_shape | 0.5825 | 0.5802 | 0.8765 |
| dr_median_months_early_or_common | 10.1000 | 10.1000 | 10.1000 |
| dr_median_months_late |    NA |    NA | 17.1000 |
| rmst5_diff_engine_years | 0.1236 | 0.1250 | 0.1175 |
| km_SSE_both_arms_pp2 | 65.6135 | 65.7410 | 79.2478 |

远处复发中早期所占比例（`dr_early_share.csv`；早期 = 随机化后 18 个月以内进入；累积发生率为占全臂的百分比；远处复发的进入不受复发后死亡率影响，故基准与 k = 1 相同）：

| arm | horizon_years | dr_cum_incidence_pct | early_cum_incidence_pct | late_cum_incidence_pct | early_share |
|---|---|---|---|---|---|
| pembro |  5 | 12.89 | 4.86 | 8.03 | 0.377 |
| pembro |  7 | 15.10 | 4.86 | 10.24 | 0.322 |
| pembro | 51 | 20.54 | 4.86 | 15.68 | 0.237 |
| placebo |  5 | 18.86 | 6.29 | 12.57 | 0.333 |
| placebo |  7 | 21.76 | 6.29 | 15.47 | 0.289 |
| placebo | 51 | 31.25 | 6.29 | 24.96 | 0.201 |

（horizon_years 为随机化后的年数；51 年即到 100 岁。）

目标函数在解处的分解（`calibration_objective.csv`）：

| part | n_points | value |
|---|---|---|
| KM OS, months 1-78, both arms (pp^2) | 156 | 79.248 |
| 7-year points, OS and EFS by arm (weighted) |   4 | 2.610 |
| 7-year points, OS by pCR status (weighted) |   4 | 5.156 |
| total | 164 | 87.014 |

术前进展后：对数 logistic 形状 1.639（该中位下的上限 1.639），中位 10.00 个月。中位**贴下界 10 个月**；5 年存活**仍贴下界 5%（形状等于上限）**。进入术前进展后的全因存活：1 年 0.425，2 年 0.192，5 年 0.050（`dr_survival_implied.csv`）。

7 年各点：模型与报告值（`calibration_final7y.csv`；round6 为第六轮模型的运行前记录 `r6_vs_final7y.csv`，round7 为第七轮的校准结果 `r7_calibration_final7y.csv`；objective_term 为该点对目标函数的贡献；DRFS 不在目标函数中，只报告）：

| id | reported | ci95 | round6 | round7 | engine | diff | objective_term | inside_ci | gate_c | engine_k1 | diff_k1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| os7_pembro | 85.1 | 82.5–87.5 | 83.40 | 83.46 | 83.20 | -1.90 | 2.223 | 是 | 是 | 84.96 | -0.14 |
| os7_placebo | 77.2 | 72.7–81.1 | 77.41 | 77.43 | 77.17 | -0.03 | 0.000 | 是 | 是 | 77.17 | -0.03 |
| efs7_pembro | 78.3 | 75.3–81.1 | 78.89 | 78.89 | 78.89 | 0.59 | 0.161 | 是 | 是 | 78.89 | 0.59 |
| efs7_placebo | 69.8 | 65.0–74.2 | 68.68 | 68.68 | 68.68 | -1.12 | 0.226 | 是 | 是 | 68.68 | -1.12 |
| os_pcr_pembro | 94.5 | — | 92.19 | 92.21 | 92.23 | -2.27 | 4.889 | — | 否（只报告） | 93.08 | -1.42 |
| os_pcr_placebo | 91.1 | — | 90.49 | 90.50 | 90.63 | -0.47 | 0.058 | — | 否（只报告） | 90.63 | -0.47 |
| os_nonpcr_pembro | 69.0 | — | 68.44 | 68.56 | 67.81 | -1.19 | 0.193 | — | 否（只报告） | 71.11 | 2.11 |
| os_nonpcr_placebo | 59.8 | — | 61.00 | 61.03 | 60.27 | 0.47 | 0.016 | — | 否（只报告） | 60.27 | 0.47 |
| drfs7_pembro | 82.9 | — | 80.46 | 80.46 | 80.46 | -2.44 | — | — | 否（只报告） | 80.46 | -2.44 |
| drfs7_placebo | 74.2 | — | 70.68 | 70.68 | 70.68 | -3.52 | — | — | 否（只报告） | 70.68 | -3.52 |

记录（不作处理）：帕博利珠单抗组 pCR 层的 7 年 OS，模型 92.23%，报告值 94.5%（情景 k = 1：93.08%）。报告值没有置信区间；按该层 495 人（IA7；IA4 为 494 人）的二项近似，标准误约 1.02 个百分点；模型比报告值低 2.27 个百分点，约 2.2 个标准误（k = 1 时低 1.42 个百分点）。

### 8.3 死亡来源与 RMST

死亡来源（占全臂 %，`calibration_deaths_by_source.csv`）：

| arm | month | km_deaths | engine_deaths | from_event_free | from_ae | from_preprog | from_LRR | from_DR |
|---|---|---|---|---|---|---|---|---|
| pembro | 12 | 2.81 | 2.54 | 0.31 | 0.87 | 0.64 | 0.000 | 0.71 |
| pembro | 24 | 7.80 | 6.50 | 0.69 | 0.87 | 1.32 | 0.003 | 3.61 |
| pembro | 36 | 10.49 | 9.37 | 0.96 | 0.87 | 1.54 | 0.008 | 5.99 |
| pembro | 48 | 12.16 | 11.72 | 1.17 | 0.87 | 1.63 | 0.012 | 8.03 |
| pembro | 60 | 13.45 | 13.69 | 1.37 | 0.87 | 1.68 | 0.017 | 9.75 |
| placebo | 12 | 1.28 | 2.55 | 0.58 | 0.25 | 1.24 | 0.000 | 0.49 |
| placebo | 24 | 8.98 | 8.32 | 1.62 | 0.25 | 2.80 | 0.004 | 3.64 |
| placebo | 36 | 13.10 | 12.59 | 2.26 | 0.25 | 3.31 | 0.009 | 6.77 |
| placebo | 48 | 16.47 | 15.97 | 2.67 | 0.25 | 3.51 | 0.015 | 9.52 |
| placebo | 60 | 18.29 | 18.69 | 2.97 | 0.25 | 3.62 | 0.021 | 11.83 |

5 年 RMST（年，`calibration_rmst.csv`）：

| arm | rmst5_km | rmst5_engine | diff |
|---|---|---|---|
| pembro | 4.6079 | 4.6324 | 0.0244 |
| placebo | 4.5094 | 4.5149 | 0.0054 |
| pembro - placebo | 0.0985 | 0.1175 | 0.0190 |

模型 5 年内按死亡来源损失的 RMST（年，`calibration_rmst_by_source.csv`；最后一行为各来源对模型两臂 RMST 差的贡献）：

| arm | event_free | ae | preprog | LRR | DR | total |
|---|---|---|---|---|---|---|
| pembro | 0.0380 | 0.0394 | 0.0591 | 0.0003 | 0.2308 | 0.3676 |
| placebo | 0.0856 | 0.0112 | 0.1260 | 0.0004 | 0.2619 | 0.4851 |
| placebo - pembro | 0.0476 | -0.0282 | 0.0669 | 0.0001 | 0.0311 | 0.1175 |

### 8.4 情景「k = 1」（复发后死亡率两臂共用）

帕博利珠单抗组用 k = 1，其余参数取基准校准值；用于所有涉及帕博利珠单抗的比较，与基准并列报告（原「OS 锚定」情景已撤掉）。帕博利珠单抗组 5 年 RMST 由 4.6324 年（基准，k = 1.492）变为 4.6763 年，两臂差 0.1615 年（KM 0.0985 年）。各时点（`scenario_k1_gate.csv`）：

| arm | month | km | ci95_lo | ci95_hi | engine_base | engine_k1 | diff_k1 | inside_k1 |
|---|---|---|---|---|---|---|---|---|
| pembro | 12 | 97.19 | 96.04 | 98.35 | 97.46 | 97.66 | 0.476 | 是 |
| pembro | 24 | 92.20 | 90.34 | 94.10 | 93.50 | 94.31 | 2.107 | **否** |
| pembro | 36 | 89.51 | 87.39 | 91.68 | 90.63 | 91.81 | 2.298 | **否** |
| pembro | 48 | 87.84 | 85.58 | 90.16 | 88.28 | 89.71 | 1.870 | 是 |
| pembro | 60 | 86.55 | 84.19 | 88.98 | 86.31 | 87.91 | 1.356 | 是 |
| placebo | 12 | 98.72 | 97.61 | 99.84 | 97.45 | 97.45 | -1.273 | **否** |
| placebo | 24 | 91.02 | 88.23 | 93.90 | 91.68 | 91.68 | 0.661 | 是 |
| placebo | 36 | 86.90 | 83.62 | 90.32 | 87.41 | 87.41 | 0.504 | 是 |
| placebo | 48 | 83.53 | 79.92 | 87.30 | 84.03 | 84.03 | 0.498 | 是 |
| placebo | 60 | 81.71 | 77.95 | 85.65 | 81.31 | 81.31 | -0.393 | 是 |

两臂 OS 差（帕博利珠单抗 − 安慰剂；`scenario_k1_arm_diff.csv`）：基准（k = 1.492）、情景 k = 1 与参照值。5 年的参照值为重建 KM 的时点值与 RMST，7 年为最终分析报告的时点值（两臂差没有报告置信区间）。

| 量 | 参照 | 基准 | k = 1 | 参照值 | 基准减参照值 | k = 1 减参照值 |
|---|---|---|---|---|---|---|
| 5 年 OS 差（百分点） | 重建 KM（2024 年 Fig. 1A） | 4.99 | 6.59 | 4.85 | 0.15 | 1.75 |
| 5 年 RMST 差（年） | 重建 KM（2024 年 Fig. 1A） | 0.1175 | 0.1615 | 0.0985 | 0.0190 | 0.0630 |
| 7 年 OS 差（百分点） | 最终分析的报告值 | 6.03 | 7.79 | 7.90 | -1.87 | -0.11 |

- 5 年 OS 差（百分点）：基准 4.99，k = 1 6.59，参照值 4.85。基准高估 0.15 个百分点，k = 1 高估 1.75 个百分点。
- 5 年 RMST 差（年）：基准 0.1175，k = 1 0.1615，参照值 0.0985。基准高估 0.0190 年，k = 1 高估 0.0630 年。
- 7 年 OS 差（百分点）：基准 6.03，k = 1 7.79，参照值 7.90。基准低估 1.87 个百分点，k = 1 低估 0.11 个百分点。

偏差方向：帕博利珠单抗的 OS 获益在 5 年两者都高估（时点 OS 差与 RMST 差方向相同），在 7 年两者都低估。

报告的两臂 OS 差的不确定性（`scenario_k1_arm_diff_ci.csv`）：由各臂报告的 95% 置信区间换算——各臂标准误 = 区间宽度 ÷ 3.92，两臂差的标准误 = 两臂标准误的平方和开方（两臂独立），95% CI = 差 ± 1.96 × 标准误。5 年用 2024 年论文（IA7）报告的 5 年 OS，7 年用最终分析的 7 年 OS。

| 年 | 帕博利珠单抗 | 安慰剂 | 两臂差 | 标准误 | 95% CI | 基准 | 基准在区间内 | k = 1 | k = 1 在区间内 |
|---|---|---|---|---|---|---|---|---|---|
| 5 | 86.6 [84.0, 88.8] | 81.7 [77.5, 85.2] | 4.9 | 2.31 | [0.4, 9.4] | 4.99 | 是 | 6.59 | 是 |
| 7 | 85.1 [82.5, 87.5] | 77.2 [72.7, 81.1] | 7.9 | 2.49 | [3.0, 12.8] | 6.03 | 是 | 7.79 | 是 |

基准和 k = 1 在两个时点都落在区间内。5 年到 7 年间报告的两臂差由 4.9 扩大到 7.9 个百分点，但两个时点的 95% CI（[0.4, 9.4] 与 [3.0, 12.8]）大幅重叠，这一扩大在抽样误差范围内无法与噪声区分。因此结构不再调整，涉及帕博利珠单抗的结果按 `docs/model_spec.md` 第 6 节以基准与 k = 1 两栏并列报告。

第八轮的结构（远处复发分为早期与晚期）是在 ESME 晚期复发数据的依据下保留的，尽管 KM 部分的拟合误差（逐月平方误差和）由第七轮的 65.7 增加到 79.2。取舍的理由：(1) ESME 中晚期复发的中位 OS 为 17.1 个月，早期为 10.1 个月，校正 HR 1.92 [1.73, 2.13]，复发时点对复发后生存的影响有外部数据支持；(2) 模型中到 100 岁的远处复发，晚期占帕博利珠单抗组的 76.3%、安慰剂组的 79.9%（第 8.2 节），若一律用早期复发的中位，终生期的复发后生存会系统性偏短；(3) 拟合误差增加后三道门槛仍全部通过，拟合误差的差别不足以推翻有外部依据的结构。

### 8.5 隐含的生存与外部对照

模型隐含的生存（`dr_survival_implied.csv`；术前进展从 49.5 岁、远处复发（早期与晚期）都从 50.5 岁计背景死亡；远处复发为两臂共用的风险，即 k = 1，帕博利珠单抗组另乘 k）：

| state | median_excess_only_months | median_all_cause_months | surv_1y | surv_2y | surv_5y |
|---|---|---|---|---|---|
| PreProg | 10.0 | 10.0 | 0.425 | 0.192 | 0.050 |
| DR early | 10.1 | 10.1 | 0.462 | 0.318 | 0.172 |
| DR late | 17.1 | 17.0 | 0.576 | 0.425 | 0.248 |

### 8.6 未用于校准的曲线

与引擎的对照（`engine_checks.csv`，各曲线全部时点中差的绝对值最大者，百分点）：

| check | arm | max_abs_diff |
|---|---|---|
| DRFS vs 2022 Fig. S3 (IA4) | pembro | 1.151 |
| EFS vs 2024 Fig. 2A (IA7) | pembro | 0.633 |
| OS non-pCR vs 2024 Fig. S4 (IA7) | pembro | 3.482 |
| OS pCR vs 2024 Fig. S4 (IA7) | pembro | 1.413 |
| DRFS vs 2022 Fig. S3 (IA4) | placebo | 3.106 |
| EFS vs 2024 Fig. 2A (IA7) | placebo | 1.952 |
| OS non-pCR vs 2024 Fig. S4 (IA7) | placebo | 3.061 |
| OS pCR vs 2024 Fig. S4 (IA7) | placebo | 1.574 |

图：`round8/fig_calibration_OS.png`（灰带为 KM 逐点 95% CI，竖线为门槛时点）、`round8/fig_engine_checks.png`。

### 8.7 此前各轮

第一轮至第三轮不达标；第四轮（术前进展后 Weibull）达标后由用户改设定；第五轮（术前进展后对数 logistic 加外部约束、远处复发后中位外部输入、k 固定为情景）不达标；第六轮（k 纳入基准校准）按规则接受；第七轮（目标函数加入 7 年时点，接受规则加入 (c)）按规则接受，其 bootstrap 按用户指示中止，**已被第八轮取代**。第八轮的结构与第七轮相同，只把远处复发分为早期与晚期。此前各轮的输出可在 git 历史中取回（第五轮为提交 0abaddd，第六轮为 e530a56，第七轮为 d1b5517）。第三轮的可行性扫描 `R/05b_gate_feasibility.R` 保留为诊断。

### 8.8 乐观情景：术前进展后中位 26 个月、5 年存活 20%（`R/05s_preprog_optimistic.R`）

设定（`docs/model_spec.md` 第 6 节）：术前进展后的对数 logistic 固定为中位 26 个月、进入后 5 年全因存活 20%（形状由两者决定，为 1.6461），依据 Elmore 等的 MD Anderson 队列（第 8.1 节）；远处复发后的形状与 k 按基准的目标函数重新校准，远处复发后的中位与基准相同（早期 10.1、晚期 17.1 个月）。

结果（`scenario_preprog_optimistic.csv`）：k = 1.682（基准 1.492），远处复发后形状 1.0249（基准 0.8765）；k 与形状都不在边界上。目标函数值 206.03。

三道门槛（只作参考，不作判定；`scenario_preprog_optimistic_gate.csv`）：(a) 10 个点中 10 个落在 KM 逐点 95% 区间内（全部在区间内）；(b) 模型 5 年 RMST 两臂差 0.0833 年，落在 KM 差的 bootstrap 95% 区间 -0.0381 至 0.2421 年内；(c) 7 年 OS 与 EFS 的 4 个值中 4 个落在最终分析的 95% 区间内。

| 门槛 | 项目 | 模型 | 下限 | 上限 | 在区间内 |
|---|---|---|---|---|---|
| a | pembro 12 months | 97.939 | 96.038 | 98.354 | 是 |
| a | pembro 24 months | 93.964 | 90.340 | 94.099 | 是 |
| a | pembro 36 months | 90.821 | 87.387 | 91.684 | 是 |
| a | pembro 48 months | 88.217 | 85.579 | 90.163 | 是 |
| a | pembro 60 months | 86.063 | 84.191 | 88.978 | 是 |
| a | placebo 12 months | 98.393 | 97.608 | 99.841 | 是 |
| a | placebo 24 months | 93.160 | 88.227 | 93.904 | 是 |
| a | placebo 36 months | 88.507 | 83.616 | 90.319 | 是 |
| a | placebo 48 months | 84.700 | 79.924 | 87.303 | 是 |
| a | placebo 60 months | 81.632 | 77.948 | 85.646 | 是 |
| b | 5-year OS RMST difference (years) | 0.083 | -0.038 | 0.242 | 是 |
| c | os7_pembro | 82.754 | 82.500 | 87.500 | 是 |
| c | efs7_pembro | 78.893 | 75.300 | 81.100 | 是 |
| c | os7_placebo | 77.029 | 72.700 | 81.100 | 是 |
| c | efs7_placebo | 68.683 | 65.000 | 74.200 | 是 |

两臂 OS 差（帕博利珠单抗 − 安慰剂；`scenario_preprog_optimistic_arm_diff.csv`；基准、k = 1 与参照值同第 8.4 节）：

| 量 | 参照 | 乐观情景 | 基准 | k = 1 | 参照值 | 乐观情景减参照值 |
|---|---|---|---|---|---|---|
| 5 年 OS 差（百分点） | 重建 KM（2024 年 Fig. 1A） | 4.43 | 4.99 | 6.59 | 4.85 | -0.41 |
| 5 年 RMST 差（年） | 重建 KM（2024 年 Fig. 1A） | 0.0833 | 0.1175 | 0.1615 | 0.0985 | -0.0152 |
| 7 年 OS 差（百分点） | 最终分析的报告值 | 5.73 | 6.03 | 7.79 | 7.90 | -2.17 |

该情景的校准目标函数为 206.0，基准为 87.0；年度门槛点虽然全部在区间内，但整体拟合明显变差，数据不支持这一设定，因此只作为敏感性分析。两个时点上的得失：5 年 RMST 差更接近 KM（0.0833 对 0.0985，差 -0.0152；基准差 0.0190），7 年 OS 差离报告值更远（5.73 对 7.90，差 -2.17；基准差 -1.87）。

## 9. Bootstrap（步骤 6，`R/06_bootstrap.R`）

B = 1000，随机种子 20261021（第 b 次用种子 + b），并行，耗时 928.8 分钟。每次：
1. 分层 EFS（2022 年补充材料 Fig. S4，IA4）：在各臂内连同 pCR 标签重抽样，pCR 比例与各层人数随之变动；各层在手术时点 landmark，用与基准相同的分布族重拟合并加 5 年约束（边界固定）；术前 KM 重算。
2. 术前进展的进入比例 = 报告例数 / 重抽样后的非 pCR 人数（全臂比例保持报告值）。
3. OS（2024 年 Fig. 1A，IA7）：在各臂内重抽样；所选的 OS 模型重拟合（只保存，引擎不用；RP 结点固定在基准位置）。
4. 远处复发后的两个中位按第 8.1 节的分布各自抽样（早期：混合分布；晚期：对数正态）；8 个 7 年目标值按其抽样分布抽取（有置信区间的 4 个点：正态，均值为报告值，SD 为第 8.1 节的 SE；按 pCR 分层的 4 个点：二项，n 为该层人数，p 为报告值；权重仍用第 8.1 节的 SE）；再对重抽样后的 OS KM 与抽到的 7 年目标值校准术前进展的中位与形状、远处复发后形状与 k（基准估计值加基准的 6 个起点，取最优；返回码 52 时再加 5 个随机起点取最优）。
5. 引擎在 5、7、10、20 年的 EFS 与 OS（臂 × pCR；帕博利珠单抗组另算情景 k = 1）。
每次都固定的数据设定：生命表、EFS 事件构成与分配比例、因不良事件死亡、局部区域复发 → 远处复发的率、术前进展例数、术前进展的外部约束、5 年约束的边界。拟合失败的样本换种子重抽（计入 attempts）。

结果：完成 1000 次，10 次重抽仍失败 0 次，换种子重抽的样本 0 个。optim 返回码（最终）：0: 979，52: 21。返回码 52 而加随机起点重跑的 38 次，其中目标值改善的 0 次（最大改善 3.09e-10）。
贴边界的次数：k 贴下界 0.25 的 15 次、贴上界 4 的 148 次；术前进展中位贴 10 个月的 540 次、贴 26 个月的 120 次；5 年存活贴 5% 的 756 次；远处复发后形状贴数值边界的 51 次。5 年 EFS 约束起作用的次数：EFS_pembro_pCR 132，EFS_pembro_nonpCR 116，EFS_placebo_pCR 129，EFS_placebo_nonpCR 205。
抽到的远处复发后中位：早期中位数 10.42 个月（2.5% 至 97.5% 分位 9.29 至 13.31）；晚期中位数 17.07 个月（15.97 至 18.36）。

参数的基准值与 bootstrap 分布（`output/phase1/bootstrap_summary.csv`；参数矩阵在 `data/bootstrap/`，一行一个样本；中位为年）：

| group | quantity | base | boot_mean | boot_median | boot_lo | boot_hi | n_finite |
|---|---|---|---|---|---|---|---|
| calibration | preprog_shape | 1.6387 | 1.7100 | 1.6387 | 0.7365 | 2.7635 | 1000 |
| calibration | preprog_median | 0.8333 | 1.1592 | 0.8333 | 0.8333 | 2.1667 | 1000 |
| calibration | dr_shape | 0.8765 | 2.0884 | 0.8967 | 0.0100 | 11.4782 | 1000 |
| calibration | dr_median | 0.8417 | 0.8949 | 0.8680 | 0.7744 | 1.1089 | 1000 |
| calibration | dr_late_median | 1.4250 | 1.4245 | 1.4225 | 1.3305 | 1.5300 | 1000 |
| calibration | pembro_dr_k | 1.4918 | 1.9381 | 1.6357 | 0.4066 | 4.0000 | 1000 |
| calibration | sse |    NA | 246.0685 | 184.0502 | 68.1709 | 812.7284 | 1000 |
| calibration | km_rmst5_diff |    NA | 0.1002 | 0.1020 | -0.0355 | 0.2358 | 1000 |
| calibration | engine_rmst5_diff |    NA | 0.1091 | 0.1083 | 0.0104 | 0.2033 | 1000 |
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

抽到的 7 年目标值（%，`boot_final7y_targets.csv`）：

| group | quantity | base | boot_mean | boot_median | boot_lo | boot_hi | n_finite |
|---|---|---|---|---|---|---|---|
| 7-year targets drawn (%) | os7_pembro | 85.10 | 85.06 | 85.10 | 82.61 | 87.46 | 1000 |
| 7-year targets drawn (%) | os7_placebo | 77.20 | 77.14 | 77.21 | 72.94 | 81.47 | 1000 |
| 7-year targets drawn (%) | efs7_pembro | 78.30 | 78.39 | 78.39 | 75.48 | 81.23 | 1000 |
| 7-year targets drawn (%) | efs7_placebo | 69.80 | 69.82 | 69.77 | 65.48 | 74.31 | 1000 |
| 7-year targets drawn (%) | os_pcr_pembro | 94.50 | 94.48 | 94.55 | 92.52 | 96.36 | 1000 |
| 7-year targets drawn (%) | os_pcr_placebo | 91.10 | 91.19 | 91.24 | 87.56 | 94.93 | 1000 |
| 7-year targets drawn (%) | os_nonpcr_pembro | 69.00 | 69.01 | 69.20 | 63.67 | 74.05 | 1000 |
| 7-year targets drawn (%) | os_nonpcr_placebo | 59.80 | 59.76 | 59.54 | 52.60 | 67.05 | 1000 |

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

文件：`boot_efs_params.csv`、`boot_efs5_binding.csv`、`boot_os_model_params.csv`、`boot_pcr_preprog.csv`、`boot_pre_surgery_km.csv`、`boot_calibration.csv`、`boot_outputs.csv`、`boot_final7y_targets.csv`、`boot_replicates.rds`。

## 10. 生存引擎的输出（步骤 7，`R/07_engine_outputs.R`）

随机化后 5、7、10、20 年的 EFS 与 OS（%，基准值与 bootstrap 95% 分位区间；`engine_outputs.csv`、`engine_curves.csv`）。第 1 阶段没有运动参数，故加运动的两臂与对应的不加运动的臂相同；情景 k = 1 只改变帕博利珠单抗组的 OS（EFS 不变）。7 年的报告值见第 8.2 节。

| 终点 | 情景 | 臂 | pCR | 5 年 | 7 年 | 10 年 | 20 年 |
|---|---|---|---|---|---|---|---|
| EFS | 基准 | 单用化疗（= 化疗加运动） | 全体 | 71.1 (66.6–76.0) | 68.7 (62.6–74.2) | 66.0 (58.0–72.1) | 58.7 (45.7–66.6) |
| EFS | 基准 | 单用化疗（= 化疗加运动） | pCR | 88.8 (83.7–92.3) | 85.4 (78.4–90.2) | 80.9 (71.0–87.6) | 69.3 (48.7–81.1) |
| EFS | 基准 | 单用化疗（= 化疗加运动） | 非 pCR | 48.8 (43.1–57.3) | 47.8 (38.0–56.8) | 47.3 (33.4–56.4) | 45.5 (29.6–54.1) |
| EFS | 基准 | 化疗加帕博利珠单抗（= 两者都加） | 全体 | 80.8 (77.8–83.4) | 78.9 (74.7–82.1) | 76.8 (70.6–80.5) | 71.4 (60.4–76.8) |
| EFS | 基准 | 化疗加帕博利珠单抗（= 两者都加） | pCR | 91.7 (89.3–94.0) | 89.5 (85.8–92.6) | 86.8 (80.4–91.0) | 79.7 (65.7–86.7) |
| EFS | 基准 | 化疗加帕博利珠单抗（= 两者都加） | 非 pCR | 62.3 (56.7–67.7) | 60.7 (52.8–67.0) | 59.8 (48.4–66.5) | 57.4 (42.1–63.9) |
| OS | 基准 | 单用化疗（= 化疗加运动） | 全体 | 81.3 (78.0–84.2) | 77.2 (72.5–81.4) | 72.7 (66.3–78.4) | 62.8 (53.2–71.6) |
| OS | 基准 | 单用化疗（= 化疗加运动） | pCR | 93.6 (91.1–95.5) | 90.6 (86.4–93.5) | 86.4 (79.4–90.7) | 73.8 (59.5–83.5) |
| OS | 基准 | 单用化疗（= 化疗加运动） | 非 pCR | 65.9 (59.1–72.3) | 60.3 (51.1–69.1) | 55.6 (44.1–66.8) | 49.0 (35.8–62.6) |
| OS | 基准 | 化疗加帕博利珠单抗（= 两者都加） | 全体 | 86.3 (84.0–88.7) | 83.2 (80.2–86.2) | 79.8 (75.5–83.6) | 72.6 (63.6–78.0) |
| OS | 基准 | 化疗加帕博利珠单抗（= 两者都加） | pCR | 94.4 (92.5–95.8) | 92.2 (89.5–94.3) | 89.3 (85.0–92.2) | 80.9 (69.4–87.2) |
| OS | 基准 | 化疗加帕博利珠单抗（= 两者都加） | 非 pCR | 72.6 (67.4–78.0) | 67.8 (61.4–74.4) | 63.8 (55.4–71.9) | 58.4 (46.4–67.2) |
| OS | k = 1 | 化疗加帕博利珠单抗（= 两者都加） | 全体 | 87.9 (84.9–90.4) | 85.0 (80.8–88.6) | 81.6 (75.7–86.7) | 74.0 (64.1–81.8) |
| OS | k = 1 | 化疗加帕博利珠单抗（= 两者都加） | pCR | 95.0 (93.4–96.3) | 93.1 (90.4–95.0) | 90.3 (85.7–93.3) | 82.0 (70.5–88.2) |
| OS | k = 1 | 化疗加帕博利珠单抗（= 两者都加） | 非 pCR | 75.8 (68.8–81.2) | 71.1 (62.4–79.1) | 66.8 (56.1–77.0) | 60.3 (46.4–73.0) |

各 bootstrap 样本的引擎由保存的参数矩阵重建，其 5、7、10、20 年的值与 `06_bootstrap.R` 当时算出的一致（1000 个样本，最大差 0.0e+00，`bootstrap_rebuild_check.csv`）。

图：`round8/fig_engine_outputs.png`（实线为引擎，带为 bootstrap 95% 区间，虚线为重建的 KM，× 为最终分析的 7 年值，竖线为其 95% 置信区间）。

引擎接口：`survival_engine(arm, pcr, times, params, hr0, wane_start, wane_rate, p_pcr, nonpcr_mix, common_dr, dr_first_months)`，`arm` 为 chemo、exercise、pembro、both；默认参数在 `data/fits/engine_params.rds`。运动钩子 (a) 时变 HR 与 (b) pCR 比例、S-JP 混合与情景 k = 1 的接口测试见 `engine_interface_test.csv`；闭式计算与逐周期递推一致（`R/test_engine_vectorized.R`）。

| test | EFS_1y | EFS_3y | EFS_5y | EFS_10y | EFS_20y | OS_1y | OS_3y | OS_5y | OS_10y | OS_20y |
|---|---|---|---|---|---|---|---|---|---|---|
| chemo base | 91.094 | 75.964 | 71.051 | 66.009 | 58.695 | 97.445 | 87.407 | 81.313 | 72.698 | 62.826 |
| nonpcr_mix with all HR = 1 | 91.094 | 75.964 | 71.051 | 66.009 | 58.695 | 97.445 | 87.407 | 81.313 | 72.698 | 62.826 |
| exercise path A with hr0 = 1 | 91.094 | 75.964 | 71.051 | 66.009 | 58.695 | 97.445 | 87.407 | 81.313 | 72.698 | 62.826 |
| S-JP (test weights) | 91.896 | 78.965 | 74.410 | 69.389 | 61.943 | 97.603 | 88.784 | 83.383 | 75.450 | 65.800 |
| S-JP + exercise path A, 6 months continued (test values) | 92.581 | 81.216 | 76.743 | 71.674 | 64.075 | 97.681 | 89.705 | 84.767 | 77.289 | 67.752 |
| exercise path B: pCR + 5 points (test value) | 91.860 | 77.850 | 73.047 | 67.690 | 59.885 | 97.648 | 88.430 | 82.695 | 74.239 | 64.068 |
| pembro base | 92.930 | 84.095 | 80.794 | 76.832 | 71.425 | 97.464 | 90.633 | 86.307 | 79.846 | 72.610 |
| pembro + S-JP (test weights) | 93.688 | 86.090 | 83.055 | 79.173 | 73.682 | 97.621 | 91.689 | 87.868 | 81.921 | 74.799 |
| chemo with common_dr = TRUE (no effect) | 91.094 | 75.964 | 71.051 | 66.009 | 58.695 | 97.445 | 87.407 | 81.313 | 72.698 | 62.826 |
| pembro, scenario k = 1 | 92.930 | 84.095 | 80.794 | 76.832 | 71.425 | 97.664 | 91.807 | 87.907 | 81.621 | 74.018 |

## 11. 已决事项与待决事项

已决：
- 层内 HR 的较晚截点参照值：撤出门槛，改为跨分析对照（2026-10-21）。
- 准则 1：保留 95%，最初 100% 为设定错误（2026-10-21）。
- 分布族：同一层两臂同一族，依两臂合计 AIC 与 5 年外推检验选定，次优族为情景（2026-10-21）；非 pCR 层复核后维持（2026-10-22）。
- 第二原发癌：归入局部区域复发（2026-10-21）。
- 校准第三轮（2026-10-22）：门槛 (a) 与 (b)；因不良事件死亡单列；EFS 加 5 年约束。
- 校准第四轮（2026-10-22）：门槛 (b) 改为 KM 差的 bootstrap 区间。
- 校准第五轮（2026-10-22）：远处复发后中位改为外部输入（10.1 个月；概率敏感性分析按 ESME 与 IMpassion132 的混合分布抽样）；术前进展后死亡改为对数 logistic，加两条外部约束；返回码 52 时加随机起点。
- 校准第六轮（2026-10-22）：k 纳入基准校准（0.25 至 4）；原 OS 锚定情景撤掉，改设情景 k = 1；接受规则运行前确定；门槛修改记录保留全部六项；IMpassion132 的置信区间已用全文核对。
- 校准第七轮（2026-10-22）：加入 KEYNOTE-522 最终分析（ASCO 2026）的 7 年值（目标函数 8 个点；门槛 (c)）；接受规则运行前确定；结构不变。bootstrap 中止，已被第八轮取代。
- 校准第八轮（2026-10-22）：远处复发按进入时点分为早期（随机化后 18 个月以内）与晚期，中位分别为 ESME 的 10.1 与 17.1 个月，形状共用；接受规则与第七轮相同，运行前提交。
- S-JP（2026-10-23，尾崎的回答）：四个组都加。non-pCR 例中 gBRCA 阳性按 F04（含帕博利珠单抗的组为 F04P）的比例用奥拉帕利、不并用卡培他滨，其余不加术后治疗；gBRCA 阴性按 F01（F01P）的比例用卡培他滨。原待决的「S-JP 的权重定义」即指这一分配，已决；F01 改为 gBRCA 阴性例中的比例。F07、F08 在两类组中用同一 HR（假设）。F01P、F04P 到之前 S-JP 不运行（`docs/model_spec.md` 第 2 节）。
- BRCA 检测的对象范围（2026-10-23）：诊断时对全部患者、全部组检测（F06），不影响增量（`docs/model_spec.md` 第 2 节）。
- 运动的有害事象（2026-10-23）：筋骨格系有害事象，发生率 E06、E07（3 级以上 E09、E10）取自 CHALLENGE，费用 E08 由尾崎填写；效用只乘 3 级以上（`docs/model_spec.md` 第 3、5 节）。
- 第 2 阶段的报告方式（2026-10-22）：涉及帕博利珠单抗的结果（帕博利珠单抗对单用化疗、帕博利珠单抗加运动对帕博利珠单抗）以基准与 k = 1 两栏并列；方向一致时表述为结论稳健，不一致时分别写出两种结论，不选其一（`docs/model_spec.md` 第 6 节）。

记录（不作处理）：
- 帕博利珠单抗组 pCR 层的 7 年 OS，模型低于报告值（报告值没有置信区间；第 8.2 节）。

待决：
- 术前进展后死亡的校准值贴在约束边界上（中位 = 10 个月，5 年存活 = 5%）（第 8.2 节）。
- 若尾崎日后提供 2023-03-23 截点的分层 KM，5 年约束改为用整条曲线（2026-10-22 的决定）。

等尾崎回答：
- 含帕博利珠单抗的组的 S-JP 数值 F01P、F04P（尾崎正向临床医生确认）。
- 尾崎若已在入力表 v1 中填了 F01：定义已改为 gBRCA 阴性例中的比例，需确认该值（`output/params_check.md` 会标出）。

已填（2026-10-23）：运动的有害事象发生率 E06、E07、E09、E10（CHALLENGE 本文 p.19 与补充材料 Table S4，入力表 v6）；F07、F08 的适用组改为「全群」（内部表）。

## 12. 局限性

- 模型在 5 年和 7 年未能同时重现两臂 OS 差随时间扩大的形状；仅凭公开的汇总数据无法判别这一形状是否超出抽样误差（第 8.4 节）。
- 术前进展的人数少（两臂合计 29 例），其死亡分布主要由外部约束决定，校准值贴在约束边界上（中位 = 10 个月，5 年存活 = 5%）（第 8.2 节；乐观情景见第 8.8 节）。

## 13. 第九轮（第 2 阶段准备，2026-10-23）：远处复发后生存外部锚定于 ESME 曲线

结论：按运行前确定的接受规则（`docs/acceptance_rule_round9.md`，git 73748f4；与第七、八轮相同）**不接受，停在步骤 6 之前**。门槛 (a) **不达标**，(b) 达标，(c) 达标。按规则当时没有写出引擎默认参数，bootstrap 未运行，没有自行增加结构。此后第十轮按判定规则 A 采用第九轮结构，第九轮的校准结果不变、按新的 (a) 判定为接受（第 14 节）。

### 13.1 ESME 论文与数字化

来源：Grinda 等 Eur J Cancer 2023;189:112935（DOI 10.1016/j.ejca.2023.05.023），HAL hal-04205902 的作者稿（CC BY-NC 4.0），经 HAL 的检索 API 取得正文与补充材料（`input/papers/Grinda2023_ESME*.pdf`，不进 git；`input/papers/SOURCE.md`）。Fig. 3a（从转移诊断起的 OS，早期复发 = 新辅助或辅助化疗结束后 12 个月以内）为嵌入的栅格图（1260x630 像素），用与 KEYNOTE-522 相同的流程数字化（`R/py/02b_digitize_raster.py`，`R/py/rasterspec_esme.json`，输出 `data/digitized/esme/`）。此图没有坐标轴线（ggplot2 浅色主题），刻度取边框外的短刻度线（加权重心，亚像素）；线条为细的 JPEG 抗锯齿线，颜色中心取观测到的线条平均色。
刻度校准残差：x 0.0241 个月，y 0.0696 个百分点。数字化的列覆盖率：早期 0.908，晚期 1.000。风险表（每 4 个月，0 至 48 个月）从图像转录，0 时点人数 881 与 1045 与摘要的各组人数一致。叠图质控：`data/digitized/esme/qa/ESME_F3A_OS_overlay.png`。

### 13.2 个体数据重建与验证（`R/13_esme_fit.R`）

Guyot 算法（`R/guyot.R`），以 IPDfromKM 交叉核对；门槛（用户指定）：重建 KM 的中位与原文相差 ≤ 0.5 个月；各风险表时点重建 KM 与数字化曲线相差 ≤ 1 个百分点。结果：26 项中 26 项达标（`output/phase1/round9/esme_validation.csv`）。

| 组 | 原文中位 | 重建中位 | 差 | 达标 |
|---|---|---|---|---|
| early | 10.1 | 10.11 | 0.009 | 是 |
| late | 17.1 | 17.21 | 0.114 | 是 |

各风险表时点的最大差：早期 0.057、晚期 0.047 个百分点。诊断（`esme_diagnostics.csv`）：

| curve | n | events_guyot | events_ipdfromkm | max_abs_km_vs_digitized_pp | max_abs_guyot_vs_ipdfromkm_pp | max_abs_risk_table_diff |
|---|---|---|---|---|---|---|
| early |  881 | 768 | 767 | 0.071 | 0.095 | 0 |
| late | 1045 | 817 | 816 | 0.064 | 0.117 | 1 |

早期对晚期的 HR（只报告）：重建 1.71 [1.55, 1.89]，图中印的 1.70 [1.54, 1.88]。

### 13.3 对数 logistic 拟合与形状的检验

两条曲线分别拟合（flexsurv，时间为年；中位 = 尺度参数；95% CI 为模型的 Wald 区间）：

| 组 | n | 事件 | 形状 | 中位_月 | 原文中位_月 | 重建KM中位_月 |
|---|---|---|---|---|---|---|
| early |  881 | 768 | 1.605 [1.513, 1.704] | 9.74 [9.07, 10.46] | 10.1 [9.3, 10.9] | 10.11 |
| late | 1045 | 817 | 1.714 [1.619, 1.815] | 16.89 [15.87, 17.98] | 17.1 [15.7, 18.2] | 17.21 |

形状的差异：早期 1.605、晚期 1.714（比 0.936）；分开与共用形状的似然比检验 χ² = 2.43（自由度 1），p = 0.119；对数形状差的 Wald 检验 p = 0.119。规则：「差异明显」按似然比检验 p < 0.05 判断（阈值为本次的操作化，在拟合运行前写入 `R/13_esme_fit.R`），明显时分开用，否则共用一个。判定：**共用一个形状**。共用形状 1.660 [1.593, 1.730]；共用形状模型下的中位：早期 9.73 个月，晚期 16.93 个月（引擎的输入，`data/fits/esme_fits.rds`）。
拟合的对数 logistic 在引擎中作为远处复发后的超额风险（其上再加背景死亡），与第五至八轮使用 ESME 中位的方式相同；ESME 的 OS 含背景死亡，转移后数年内、约 50 岁时差别很小。图：`round9/fig_esme_fit.png`。

### 13.4 模型的修改（用户指定）与校准结果

- 远处复发后的生存（早期、晚期两个子状态）全部改为外部输入：形状与中位取自 13.3 节的拟合，不参与校准。
- 概率敏感性分析：每个 bootstrap 样本对 ESME 重建个体数据在组内重抽样并重新拟合，联合抽取形状与中位（`esme_draw()`）。
- IMpassion132 不再参与基准与抽样，改为早期复发中位的情景（11.2 个月，`dr_ext_imp132()`）。
- 校准参数只剩 k（0.25 至 4）与术前进展的两个参数（约束不变）；目标函数与第七、八轮相同。只做点估计。

校准值：k = 1.000（不在边界上）；术前进展后对数 logistic 中位 9.73 个月、形状 1.660（该中位下的上限 1.614），不在约束边界上。目标函数 157.11，其中 KM 部分 144.42（第八轮 79.25）。

与第六至八轮的比较（`calibration_vs_previous.csv`）：

| quantity | round6 | round7 | round8 | round9 |
|---|---|---|---|---|
| pembro_dr_k | 1.4277 | 1.4110 | 1.4918 | 1.5464 |
| preprog_median_months | 11.4387 | 11.3897 | 10.0000 | 10.0000 |
| preprog_shape | 1.7717 | 1.7671 | 1.6387 | 0.6055 |
| preprog_shape_cap | 1.7717 | 1.7671 | 1.6387 | 1.6387 |
| dr_shape_early_or_common | 0.5825 | 0.5802 | 0.8765 | 1.6598 |
| dr_median_months_early_or_common | 10.1000 | 10.1000 | 10.1000 | 9.7339 |
| dr_median_months_late |    NA |    NA | 17.1000 | 16.9299 |
| dr_shape_late |    NA |    NA |    NA | 1.6598 |
| rmst5_diff_engine_years | 0.1236 | 0.1250 | 0.1175 | 0.1156 |
| km_SSE_both_arms_pp2 | 65.6135 | 65.7410 | 79.2478 | 144.4206 |

门槛 (a)（`calibration_gate.csv`）：10 个点中 9 个落在逐点 95% 区间内；区间外 安慰剂 12 个月，超出 0.3030 个百分点（例外规则 (i) 的上限 0.3）；全部 10 个点落在 Bonferroni 校正后的 99.5% 区间内。

| arm | month | km | ci95_lo | ci95_hi | ci995_lo | ci995_hi | engine | diff | inside | outside_pp | inside_995 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pembro | 12 | 97.19 | 96.04 | 98.35 | 95.54 | 98.86 | 97.65 | 0.465 | 是 | 0.0000 | 是 |
| pembro | 24 | 92.20 | 90.34 | 94.10 | 89.55 | 94.93 | 93.80 | 1.600 | 是 | 0.0000 | 是 |
| pembro | 36 | 89.51 | 87.39 | 91.68 | 86.49 | 92.64 | 90.84 | 1.333 | 是 | 0.0000 | 是 |
| pembro | 48 | 87.84 | 85.58 | 90.16 | 84.62 | 91.19 | 88.24 | 0.399 | 是 | 0.0000 | 是 |
| pembro | 60 | 86.55 | 84.19 | 88.98 | 83.19 | 90.05 | 86.01 | -0.540 | 是 | 0.0000 | 是 |
| placebo | 12 | 98.72 | 97.61 | 99.84 | 97.13 | 100.00 | 97.30 | -1.413 | **否** | 0.3030 | 是 |
| placebo | 24 | 91.02 | 88.23 | 93.90 | 87.05 | 95.18 | 92.36 | 1.341 | 是 | 0.0000 | 是 |
| placebo | 36 | 86.90 | 83.62 | 90.32 | 82.23 | 91.84 | 87.88 | 0.979 | 是 | 0.0000 | 是 |
| placebo | 48 | 83.53 | 79.92 | 87.30 | 78.41 | 88.98 | 83.94 | 0.411 | 是 | 0.0000 | 是 |
| placebo | 60 | 81.71 | 77.95 | 85.65 | 76.38 | 87.41 | 80.62 | -1.088 | 是 | 0.0000 | 是 |

门槛 (b)：模型 5 年 RMST 两臂差 0.1156 年，KM 差的 bootstrap 95% 区间 -0.0381 至 0.2421 年，达标。门槛 (c)：7 年 OS 与 EFS 的 4 个值中 4 个落在最终分析的 95% 区间内。

| id | reported | ci95 | engine | inside_ci |
|---|---|---|---|---|
| os7_pembro | 85.1 | 82.5–87.5 | 82.60 | 是 |
| os7_placebo | 77.2 | 72.7–81.1 | 75.65 | 是 |
| efs7_pembro | 78.3 | 75.3–81.1 | 78.89 | 是 |
| efs7_placebo | 69.8 | 65.0–74.2 | 68.68 | 是 |

诊断（不作判定；`calibration_gate_feasibility_r9.csv`）：在约束范围内（术前进展中位 10 至 26 个月、5 年存活 ≥ 5%，k 在 0.25 至 4）以 Nelder-Mead 最小化门槛 (a) 的最大超出幅度，15 个起点中 15 个找到 10 个点全部在 95% 区间内的参数（最小超出 0.0000 个百分点），其中 5 年 RMST 两臂差也落在 (b) 的区间内的 15 个（(c) 未检查）。即本结构下存在满足 (a) 的参数，校准（最小化目标函数）的解没有落在其中。

### 13.5 两臂 OS 差（5 年与 7 年）与帕博利珠单抗 pCR 层的 7 年 OS

两臂 OS 差（帕博利珠单抗 − 安慰剂；第九轮 k = 1.546，第八轮 k = 1.492；参照值同第 8.4 节）：

| 量 | 第九轮 基准 | 第九轮 k = 1 | 第八轮 基准 | 第八轮 k = 1 | 参照值 |
|---|---|---|---|---|---|
| 5 年 OS 差（百分点） | 5.39 | 6.64 | 4.99 | 6.59 | 4.85 |
| 5 年 RMST 差（年） | 0.1156 | 0.1527 | 0.1175 | 0.1615 | 0.0985 |
| 7 年 OS 差（百分点） | 6.95 | 8.14 | 6.03 | 7.79 | 7.90 |

帕博利珠单抗组 pCR 层的 7 年 OS：第九轮模型 91.88%（k = 1：92.52%），第八轮 92.23%（k = 1：93.08%），报告值 94.5%。

## 14. 第十轮（2026-10-23）：以转移后长期存活决定采用第八轮还是第九轮结构

判定规则在任何诊断之前单独提交（`docs/acceptance_rule_round10.md`，git e8d2134）。提交前只确认了 ESME 重建数据的随访最长 47.98 个月（风险表止于 48 个月），据此经用户决定以第 4 年代替原指示的第 5 年。诊断：`R/14_round10_decision.R`，输出在 `output/phase1/round10/`。

### 14.1 远处复发后的存活比例（%）

隐含值 = 远处复发后超额生存（对数 logistic）× 背景生存（从 50.5 岁起），k = 1；第八轮：形状共用 0.8765、中位为 ESME 摘要的 10.1 与 17.1 个月；第九轮：ESME 拟合（形状 1.6598、中位 9.73 与 16.93 个月）。ESME：重建 KM 的点估计与逐点 95% CI（对数尺度）；第 4 年取 48 个月（重建数据的最后观察时点 47.98 个月的值）。第 3、4 年参与判定，第 1、2 年只报告。

| 组 | 年 | 第八轮 | 第九轮 | ESME_KM | ESME_95CI | 第八轮在CI内 | 第九轮在CI内 | 参与判定 |
|---|---|---|---|---|---|---|---|---|
| 早期 | 1 | 46.16 | 41.34 | 41.73 | [38.56, 45.17] | **否** | 是 | 否（只报告） |
| 早期 | 2 | 31.80 | 18.22 | 15.74 | [13.41, 18.46] | **否** | 是 | 否（只报告） |
| 早期 | 3 | 24.60 | 10.19 | 9.98 | [8.05, 12.37] | **否** | 是 | 是 |
| 早期 | 4 | 20.19 | 6.57 | 7.17 | [5.47, 9.39] | **否** | 是 | 是 |
| 晚期 | 1 | 57.62 | 63.82 | 64.00 | [61.15, 67.00] | **否** | 是 | 否（只报告） |
| 晚期 | 2 | 42.50 | 35.80 | 35.48 | [32.61, 38.59] | **否** | 是 | 否（只报告） |
| 晚期 | 3 | 34.08 | 22.13 | 21.18 | [18.65, 24.07] | **否** | 是 | 是 |
| 晚期 | 4 | 28.62 | 14.96 | 13.98 | [11.75, 16.64] | **否** | 是 | 是 |

图：`round10/fig_dr_survival.png`。

### 14.2 判定结果

规则 A 成立：第八轮的隐含值在早期第 3 年、早期第 4 年、晚期第 3 年、晚期第 4 年落在 ESME 的 95% CI 之外（参与判定的 4 个点中第八轮在区间内的 0 个，第九轮 4 个）。第八轮不用于终生模拟，采用第九轮结构；门槛 (a) 只用 Bonferroni 同时区间（逐点 99.5%）判定，去掉 0.3 个百分点的附加上限（门槛修改记录第 8 项）。

### 14.3 转移后的平均存活时间与远处复发状态中的停留时间

转移后的平均存活时间（年，截至终生时间范围 49.5 年，即到 100 岁；k = 1）；参考：截至 48 个月的限制平均存活时间，与 ESME 重建 KM 比较（`mean_survival_after_dr.csv`）：

| 组 | 第八轮_终生 | 第九轮_终生 | 差_第九减第八 | 第八轮_48个月 | 第九轮_48个月 | ESME_KM_48个月 |
|---|---|---|---|---|---|---|
| 早期 | 3.864 | 1.511 | -2.353 | 1.526 | 1.196 | 1.176 |
| 晚期 | 5.442 | 2.548 | -2.894 | 1.919 | 1.786 | 1.782 |

引擎中每人在远处复发状态的累计停留时间（年，折现前，终生；`dr_time_engine.csv`；第八轮与第九轮各用其校准的 k）：

| 臂 | 情景 | 第八轮 | 第九轮 | 差_年 | 差_月 | 第八轮_k | 第九轮_k |
|---|---|---|---|---|---|---|---|
| 单用化疗 | 基准 | 1.506 | 0.731 | -0.775 | -9.30 | 1.000 | 1.000 |
| 帕博利珠单抗 | 基准 | 0.494 | 0.278 | -0.217 | -2.60 | 1.492 | 1.546 |
| 帕博利珠单抗 | k = 1 | 0.991 | 0.474 | -0.516 | -6.19 | 1.000 | 1.000 |

### 14.4 采用的结构与第九轮各道门槛的最终判定

采用第九轮结构。第九轮的校准结果不变（不重新校准，`R/14b_apply_round10.R`），按第十轮的规则判定（`calibration_status.csv`；按第九轮规则的判定另存于 `round9/calibration_status_round9_rule.csv`）：(a) 按 Bonferroni 同时区间接受（10 个点中 9 个在 95% 区间内，全部 10 个点在 99.5% 区间内）；(b) 达标；(c) 达标。`data/fits/engine_params.rds` 已恢复为第九轮的值。
本地参照结果 `output/check/bootstrap10_local.rds`（基础种子 20261023，10 次）在提交 bb5d7bc 上重新生成（x86_64-w64-mingw32，2026-10-24 14:53:49 EDT）；推送与 Longleaf 的 1,000 次 bootstrap 推迟到第十一轮通过之后（用户 2026-10-23 的指示；第十一轮见第 15 节）。

## 15. 第十一轮（2026-10-23）：分层 EFS 约束改用 KEYNOTE-522 最终分析的 7 年值

规则在任何第十一轮计算之前单独提交（`docs/acceptance_rule_round11.md`，git 0ca5cfe；尾崎 2026-10-23 的指示）。唯一的改动是约束值的数据来源：由 2023-03-23 截点的 5 年分层 EFS 换成最终分析（J Clin Oncol 2026;44(16_suppl):507，截点 2025-10-14，中位随访 93.8 个月）的 7 年分层 EFS，实现方式不变（随机化后 84 个月的预测落在报告值的二项 95% 区间内，n 为 IA4 的分层人数；区间外时在较近的边界上重新最大化似然）。门槛沿用第十轮判定后的版本，分布族不变，结构为第九轮。最终分析的摘要原文未取得，数值出自会议报道（OncLive 2026-06-01，DelveInsight、CancerNetwork 对照；`data/kn522_final_7y.csv`）。规则文件的数据表中「全体 OS 的 HR」一行在提交时误读了 CancerNetwork（[0.49, 0.83] 是 DRFS 的 HR），已在文件中更正，不影响规则。

pCR 比例的核对（提交前）：按全例 pCR 率 63.0% 对 55.6% 加权，分层 7 年 EFS 合成 78.26% 与 69.83%，与全体的 78.3% 与 69.8% 一致；模型的 pCR 比例为全例值（494/784、217/390）。

### 15.1 四个格子的 7 年 EFS（不作门槛）

| 格子 | 分布族 | 报告值 | 二项95区间 | 模型 | 差 | 约束起作用 | 差在0.5以内 | AIC |
|---|---|---|---|---|---|---|---|---|
| pCR 例，帕博利珠单抗 | weibull | 90.4 | 87.80 至 93.00 | 90.08 | -0.32 | 否 | 是 | 259.71 |
| pCR 例，安慰剂 | weibull | 85.9 | 81.27 至 90.53 | 85.56 | -0.34 | 否 | 是 | 146.80 |
| non-pCR 例，帕博利珠单抗 | cure_weibull | 57.6 | 51.91 至 63.29 | 60.86 | 3.26 | 否 | **否** | 460.33 |
| non-pCR 例，安慰剂 | cure_weibull | 49.7 | 42.25 至 57.15 | 48.43 | -1.27 | 否 | **否** | 331.31 |

合计 AIC 1198.15（第十轮 1198.15）。4 条曲线在约束前都已落在区间内，约束不起作用，参数与第十轮相同（`data/fits/round11/fits.rds` 的 selected 与 `data/fits/fits.rds` 完全相同）。7 年两臂差：pCR 例模型 4.52 对报告 4.5 个百分点，non-pCR 例模型 12.43 对报告 7.9 个百分点。

### 15.2 判定

**按规则停下**：加了约束的 4 个格子中 2 个的差超过 0.5 个百分点（规则：差应在 0.5 个百分点以内，否则说明约束没起作用，停下报告）。原因是约束为区间约束：模型值落在二项区间内（半宽 2.6 至 7.5 个百分点）时参数不变，约束不把模型值固定在报告值上（规则文件提交前已写明）。没有重新校准，没有判定门槛，没有自行改变约束的实现方式。第十轮选定的结构仍为第 1 阶段的最终状态：`data/fits/fits.rds` 已恢复为第十轮的文件，`data/fits/engine_params.rds` 未改动；第十一轮的拟合存于 `data/fits/round11/`、`output/phase1/round11/`。

### 15.3 不作门槛的跨分析对照

2023-03-23 截点的 5 年分层 EFS（第十一轮起不再作约束）：

| 格子 | 模型5年 | 报告值2023 | 差 |
|---|---|---|---|
| pCR 例，帕博利珠单抗 | 92.21 | 92.2 | 0.01 |
| pCR 例，安慰剂 | 88.95 | 88.2 | 0.75 |
| non-pCR 例，帕博利珠单抗 | 62.39 | 62.6 | -0.21 |
| non-pCR 例，安慰剂 | 49.53 | 52.3 | -2.77 |

按 pCR 分层的 HR（最终分析为探索性解析）：

| 终点 | 层 | 最终分析 | 出处 | 截点2023 | IA4重建Cox | 备注 |
|---|---|---|---|---|---|---|
| EFS | pCR | 0.68 [0.44, 1.07] | OncLive 2026-06-01 | 0.65 | 0.722 | IA4（2021-03-23）重建个体数据，不分层 Cox；不作门槛 |
| EFS | nonpCR | 0.78 [0.59, 1.03] | OncLive 2026-06-01 | 0.72 | 0.712 | IA4（2021-03-23）重建个体数据，不分层 Cox；不作门槛 |
| OS | pCR | 0.64 [0.37, 1.14] | CancerNetwork 2026-06-01 |  |  | 模型输入中没有按 pCR 分层的 OS 曲线；模型值未计算（停在校准之前）；OncLive 印 [0.39, 1.14] |
| OS | nonpCR | 0.76 [0.55, 1.03] | OncLive 2026-06-01 |  |  | 模型输入中没有按 pCR 分层的 OS 曲线；模型值未计算（停在校准之前） |

### 15.4 未做的部分

按规则停在拟合之后：门槛结果、k、5 年与 7 年的 OS 两臂差、5 年 RMST 两臂差与第十轮的并列，以及 `bootstrap10_local.rds` 的重新生成、推送和 Longleaf 的 1,000 次 bootstrap，都没有做。

### 15.5 参照的边界报告（2026-10-23 补充，只报告不设门槛）

参照重新生成之后（门槛通过时），报告 10 次中 k 的全部值、贴下界 0.25 与上界 4 的次数，以及术前进展中位贴 10 个月与 26 个月的次数（`R/06d_reference_bounds.R`），与第十轮的参照并列；推送与 Longleaf 的 1,000 次由用户看过之后再定。第十轮的参照（提交 15dba86）：k = 4.0000、1.8764、0.5938、0.8983、0.9655、4.0000、4.0000、1.9345、1.5745、1.0924；贴 4 的 3 次（第 1、6、7 次），贴 0.25 的 0 次；术前进展中位贴 10 个月的 8 次，贴 26 个月的 1 次。第十一轮两次都停下（第 15.6 节），参照未重新生成，本轮的值尚无。

### 15.6 修改后的第十一轮：等式约束（2026-10-23）

规则修改在任何新的计算之前单独提交（`docs/acceptance_rule_round11.md` 的「修改」节，git 1996c24）：四个格子在随机化后 84 个月的 EFS 固定为报告值，在此条件下最大化似然，撤销区间约束；0.5 个百分点的检查保留；bootstrap 中每个样本的四个约束值各自从 Binomial(n, p)/n 抽取。修改记录如实写明：本修改是看到第十一轮拟合（git 974b6ef）之后做出的；理由是区间约束自第三轮以来从未起过作用，且不能保证两臂之差正确；0.5 个百分点这一条按等式约束设计，与当时的区间约束不匹配，属于指令错误。

最终分析摘要原文（`input/papers/KN522_final_ASCO2026_abstract.pdf`）与 `data/kn522_final_7y.csv` 的全体数值逐项一致（7 年 EFS 与 OS 及其 95% 置信区间、两个 HR、截点、中位随访 93.8 个月〔84.7 至 102.8〕），门槛 (c) 的取值不变；摘要不含按 pCR 分层的数值。

#### 15.6.1 拟合（`R/15_round11_check.R equal`，`round11/equality/`）

| 格子 | 报告值 | 约束前 | 约束后 | 对数似然变化 | 约束前参数 | 约束后参数 |
|---|---|---|---|---|---|---|
| pCR 例，帕博利珠单抗 | 90.4 | 90.08 | 90.40 | -0.012 | shape = 0.67867; scale = 178.96 | shape = 0.66851; scale = 198.23 |
| pCR 例，安慰剂 | 85.9 | 85.56 | 85.90 | -0.004 | shape = 0.76839; scale = 72.02 | shape = 0.75932; scale = 76.709 |
| non-pCR 例，帕博利珠单抗 | 57.6 | 60.86 | 57.60 | -0.212 | theta = 0.64257; shape = 0.89539; scale = 1.3566 | theta = 0.59614; shape = 0.84675; scale = 1.6828 |
| non-pCR 例，安慰剂 | 49.7 | 48.43 | 49.70 | -0.025 | theta = 0.52828; shape = 1.197; scale = 1.4708 | theta = 0.54268; shape = 1.2158; scale = 1.4237 |

0.5 个百分点的检查：4 个格子都在 0.5 个百分点以内（按第 4 步的拟合曲线计，差为 0）。合计对数似然变化 -0.253，合计 AIC 1198.65（第十轮 1198.15）。7 年两臂差：pCR 例 4.52 → 4.50（报告 4.5），non-pCR 例 12.43 → 7.90（报告 7.9）个百分点。

5 年值与 2023-03-23 截点报告值之差（不作门槛）：

| 格子 | 约束前 | 约束后 | 报告值2023 | 差 |
|---|---|---|---|---|
| pCR 例，帕博利珠单抗 | 92.21 | 92.44 | 92.2 | 0.24 |
| pCR 例，安慰剂 | 88.95 | 89.19 | 88.2 | 0.98 |
| non-pCR 例，帕博利珠单抗 | 62.39 | 60.08 | 62.6 | -2.52 |
| non-pCR 例，安慰剂 | 49.53 | 50.61 | 52.3 | -1.69 |

#### 15.6.2 校准与门槛（第九轮结构，`R/05_calibrate.R`）

| 项目 | 第十一轮等式约束 | 第十轮 |
|---|---|---|
| 门槛 (a)：第 1 至 5 年 10 个点 | 达标（95% 区间内 10 个） | 按 Bonferroni 同时区间接受（95% 区间内 9 个） |
| 门槛 (b)：5 年 RMST 两臂差（年） | 达标（0.1416；区间 -0.0381 至 0.2421） | 达标（0.1156） |
| 门槛 (c)：7 年 OS 帕博利珠单抗 | 82.38（82.5 至 87.5） | 82.60（82.5 至 87.5） |
| 门槛 (c)：7 年 OS 安慰剂 | 75.41（72.7 至 81.1） | 75.65（72.7 至 81.1） |
| 门槛 (c)：7 年 EFS 帕博利珠单抗 | 77.89（75.3 至 81.1） | 78.89（75.3 至 81.1） |
| 门槛 (c)：7 年 EFS 安慰剂 | 69.43（65.0 至 74.2） | 68.68（65.0 至 74.2） |
| k | 1.166 | 1.546 |
| 术前进展中位（月） | 10.00 | 10.00 |
| KM 平方误差和（百分点²） | 157.2 | 144.4 |
| 5 年 OS 两臂差（模型 / k = 1 / 报告） | 6.00 / 6.50 / 4.85 | 5.39 / 6.64 / 4.85 |
| 7 年 OS 两臂差（模型 / k = 1 / 报告） | 6.96 / 7.48 / 7.9 | 6.95 / 8.14 / 7.9 |

**按规则停下**：门槛 (c) 不达标——帕博利珠单抗 7 年 OS：模型 82.38，区间 82.5 至 87.5（低 0.12 个百分点）。没有自行增加结构，没有重新生成参照，没有运行 `R/06d_reference_bounds.R`，没有启动 Longleaf。`R/05_calibrate.R` 按设计删除了 `engine_params.rds`；之后把第十一轮的输出移到 `output/phase1/round11/equality/`、`data/fits/round11/equality/`，主目录的 `fits.rds`、`engine_params.rds`、`calibration_candidates.rds` 与校准输出恢复为第十轮的文件（与提交中的相同），`config.R` 的默认恢复为 5 年、区间约束（已接受的状态；设为 7 年、`equal` 即重现本轮）。

#### 15.6.3 诊断（不作门槛，不改结构，`R/15b_round11_diag.R`）

引擎中按 pCR 分层的 7 年 EFS 与约束值（第 4 步的拟合曲线等于约束值）：

| 臂 | 层 | 报告值 | 第4步拟合 | 引擎 | 引擎减报告值 |
|---|---|---|---|---|---|
| 帕博利珠单抗 | pCR | 90.4 | 90.40 | 89.86 | -0.54 |
| 帕博利珠单抗 | nonpCR | 57.6 | 57.60 | 57.49 | -0.11 |
| 安慰剂 | pCR | 85.9 | 85.90 | 85.71 | -0.19 |
| 安慰剂 | nonpCR | 49.7 | 49.70 | 49.01 | -0.69 |
| 帕博利珠单抗 | all |  |  | 77.89 |  |
| 安慰剂 | all |  |  | 69.43 |  |

引擎的分层 7 年 EFS 比第 4 步的拟合曲线低 0.11 至 0.69 个百分点（两格超过 0.5）。第十轮的引擎有同样大小的差（对区间约束下的拟合曲线：−0.53、−0.11、−0.19、−0.67），不是等式约束引起的。pCR 两格的差大致等于术前 7 个月内的因不良事件死亡（引擎对 pCR 层也计入，帕博利珠单抗 7/783 × 7/12 ≈ 0.52、安慰剂 1/389 × 7/12 ≈ 0.15 个百分点）；non-pCR 两格还与术前进展的处理有关（推测，未进一步查）。0.5 个百分点的检查按第 4 步的拟合曲线判定为通过；按引擎则有两格不通过。

只改 k（其余参数取本轮校准值、不重新优化）时，三道门槛同时满足的 k 为 0.70 至 1.10（校准值 1.166）。只作诊断，不作采用。

## 16. 第十二轮（2026-10-23）：修正引擎与输入 EFS 的不一致，修正后重判第十一轮

规则在任何计算之前单独提交（`docs/acceptance_rule_round12.md`，git a1625c1）。判定依据：引擎的作用是把拟合的 EFS 曲线分解到事件类型和时点上，不应改变 EFS 本身；检查为四个格子和两臂全体，引擎 EFS 与第 4 步拟合曲线在第 1、2、3、5、7、10 年的差都 ≤ 0.05 个百分点（实现的正确性检查，不是统计门槛）。修正原则：已包含在拟合 EFS 曲线中的事件只能在时点或状态之间移动，不能另外加上去。

### 16.1 诊断（修正前的引擎 = git a1625c1 的 `R/engine.R`；`R/16_round12_diag.R`）

第十一轮设定（7 年、等式约束）下引擎 EFS 与拟合曲线之差（百分点）按来源的拆解（一阶近似，余项归入「其他」；第十轮设定的同表在 `round12/diag_engine_vs_fit_prefix.csv`，大小几乎相同）：

| 格子 | 年 | 拟合 | 引擎 | 差 | A手术前背景死亡 | B手术前因不良事件死亡 | C术前进展对KM下降 | D手术后背景下限 | E其他 |
|---|---|---|---|---|---|---|---|---|---|
| 帕博利珠单抗 pCR |  1 | 98.39 | 97.81 | -0.583 | -0.070 | -0.515 | 0.000 | 0.000 | 0.002 |
| 帕博利珠单抗 pCR |  2 | 96.39 | 95.82 | -0.571 | -0.068 | -0.505 | 0.000 | 0.000 | 0.002 |
| 帕博利珠单抗 pCR |  3 | 94.88 | 94.32 | -0.562 | -0.067 | -0.497 | 0.000 | 0.000 | 0.002 |
| 帕博利珠单抗 pCR |  5 | 92.44 | 91.89 | -0.548 | -0.065 | -0.484 | 0.000 | 0.000 | 0.002 |
| 帕博利珠单抗 pCR |  7 | 90.40 | 89.86 | -0.536 | -0.064 | -0.474 | 0.000 | 0.000 | 0.002 |
| 帕博利珠单抗 pCR | 10 | 87.77 | 87.25 | -0.520 | -0.062 | -0.460 | 0.000 | 0.000 | 0.002 |
| 帕博利珠单抗 nonpCR |  1 | 84.63 | 84.47 | -0.157 | -0.060 | -0.443 | 0.346 | 0.000 | 0.000 |
| 帕博利珠单抗 nonpCR |  2 | 72.50 | 72.36 | -0.134 | -0.051 | -0.380 | 0.296 | 0.000 | 0.000 |
| 帕博利珠单抗 nonpCR |  3 | 66.12 | 66.00 | -0.123 | -0.047 | -0.346 | 0.270 | 0.000 | 0.000 |
| 帕博利珠单抗 nonpCR |  5 | 60.08 | 59.97 | -0.111 | -0.042 | -0.315 | 0.246 | 0.000 | 0.000 |
| 帕博利珠单抗 nonpCR |  7 | 57.60 | 57.49 | -0.107 | -0.041 | -0.302 | 0.235 | 0.000 | 0.000 |
| 帕博利珠单抗 nonpCR | 10 | 56.02 | 55.92 | -0.104 | -0.040 | -0.293 | 0.229 | 0.000 | 0.000 |
| 安慰剂 pCR |  1 | 98.11 | 97.90 | -0.216 | -0.069 | -0.147 | 0.000 | 0.000 | 0.000 |
| 安慰剂 pCR |  2 | 95.29 | 95.08 | -0.210 | -0.067 | -0.143 | 0.000 | 0.000 | 0.000 |
| 安慰剂 pCR |  3 | 93.02 | 92.81 | -0.205 | -0.066 | -0.140 | 0.000 | 0.000 | 0.000 |
| 安慰剂 pCR |  5 | 89.19 | 88.99 | -0.197 | -0.063 | -0.134 | 0.000 | 0.000 | 0.000 |
| 安慰剂 pCR |  7 | 85.90 | 85.71 | -0.189 | -0.061 | -0.129 | 0.000 | 0.000 | 0.000 |
| 安慰剂 pCR | 10 | 81.60 | 81.42 | -0.180 | -0.058 | -0.123 | 0.000 | 0.000 | 0.000 |
| 安慰剂 nonpCR |  1 | 83.87 | 82.71 | -1.167 | -0.059 | -0.126 | -0.990 | 0.000 | 0.008 |
| 安慰剂 nonpCR |  2 | 65.67 | 64.76 | -0.914 | -0.046 | -0.099 | -0.775 | 0.000 | 0.006 |
| 安慰剂 nonpCR |  3 | 56.27 | 55.48 | -0.783 | -0.040 | -0.085 | -0.664 | 0.000 | 0.005 |
| 安慰剂 nonpCR |  5 | 50.61 | 49.91 | -0.704 | -0.036 | -0.076 | -0.597 | 0.000 | 0.005 |
| 安慰剂 nonpCR |  7 | 49.70 | 49.01 | -0.691 | -0.035 | -0.075 | -0.587 | 0.000 | 0.005 |
| 安慰剂 nonpCR | 10 | 49.27 | 48.59 | -0.685 | -0.035 | -0.074 | -0.582 | 0.000 | 0.005 |

各层的输入：手术时点 KM 的下降 帕博利珠单抗 non-pCR 5.22%、安慰剂 non-pCR 7.59%（pCR 两层为 0：重建数据中 pCR 层手术前没有事件和删失）；术前进展的报告比例 q_pre 4.83%、8.67%；治疗期因不良事件死亡的概率 0.89%、0.26%。

| 来源 | 是否已在拟合曲线中 | 原因与代码位置 | 修正方式 |
|---|---|---|---|
| 因不良事件死亡（手术前） | 是（KM 含手术前的全部死亡） | 旧 `branch_flows()`：`dHA <- ae_rate * ...` 在 [0, ae_end) 全程计入 EF 的总风险 `Ht`，手术前未从 KM 中扣出，两层都计 | 手术前从 KM 的下降中分出（在术前进展之后，最多为余下的部分）；放不下的部分（pCR 层的全部）移到手术后、治疗期结束前，均匀地从超额风险中扣出 |
| 背景死亡（手术前） | 是（同上） | 旧 `branch_flows()`：`Ht <- hb + ...` 手术前也含背景死亡 `hb`，叠加在 KM 之上 | 手术前不另计；KM 的下降中术前进展与因不良事件死亡以外的部分为其他死亡（含背景） |
| 术前进展 | 是（无法手术的进展是 EFS 事件，在 non-pCR 层手术前的 KM 下降中） | 旧 `branch_flows()`：`Spre <- 1 - q_pre * Fpre`，以报告比例 q_pre 代替 KM 的下降（帕博利珠单抗 q < 下降、安慰剂 q > 下降） | 手术前最多为 KM 的下降、按 KM 的形状；超出的部分（安慰剂 non-pCR 8.67% − 7.59%）移到手术后最早的周期，从超额风险中扣出，总量仍为 q_pre |
| pCR 分层开始的时点 | 是（手术前的事件都在 non-pCR 层；pCR 层手术前的 KM 为 1） | 上面三项在 pCR 层的表现：手术前本无事件，引擎仍计背景死亡与因不良事件死亡（两臂 pCR 层的全部偏差） | pCR 层手术前没有离开无事件状态的事件；因不良事件死亡全部在手术后的治疗期内 |
| 背景死亡下限（手术后，非治愈模型） | 不适用（拟合风险低于背景时的外推） | `pmax(dH - hb, 0)`：10 年内不起作用（0 个周期）；pCR 层的 Weibull 拟合自第 22 年（帕博利珠单抗）、第 27 年（安慰剂）起低于背景死亡率，此后引擎以背景死亡率为下限 | 不改（不在本检查的范围；外推的问题，第 2 阶段终生模拟时要注意） |
| 其他 | — | 一阶近似的余项（≤ 0.01 个百分点） | — |

### 16.2 修正与测试

`R/engine.R`：新增 `branch_hazards()`（离开无事件状态的各项风险），`branch_flows()` 与 `R/test_engine_vectorized.R` 的逐周期递推共用；手术前的无事件比例严格等于该层的 KM，手术后的全死因风险等于 EFS 模型（非治愈模型不低于背景）；手术前放不下的事件移到手术后，不另外加。新增单元测试 `R/test_engine_efs_consistency.R`（输出 `output/phase1/engine_efs_consistency_test.csv`），已纳入全部单元测试。

结果：第十轮设定与第十一轮设定都达标，四个格子与两臂全体在 6 个时点的最大差 4.3e-14 个百分点；术前进展的进入量每层都等于 q_pre；终生的因不良事件死亡与治疗期的概率之差最大 0.046 个百分点（只报告）。其他单元测试（向量化 3,456 例、接口、费用层、约束）都通过；接口测试与费用层测试的数值因引擎改变而改变。

### 16.3 校准与门槛（`R/16b_round12_calibrate.sh`）

| 项目 | 第十一轮设定（修正后引擎） | 第十一轮（修正前引擎） | 第十轮设定（修正后引擎，只报告） | 第十轮（修正前引擎，已接受） |
|---|---|---|---|---|
| 门槛 (a) | 达标（95% 区间内 10 个） | 达标（95% 区间内 10 个） | 达标（95% 区间内 10 个） | 按 Bonferroni 同时区间接受（95% 区间内 9 个） |
| 门槛 (b)：5 年 RMST 两臂差（年） | 达标（0.1268） | 达标（0.1416） | 达标（0.1248） | 达标（0.1156） |
| 门槛 (c) | **不达标** | **不达标** | 达标 | 达标 |
| 7 年 OS 帕博利珠单抗（报告 85.1） | 82.34（82.5 至 87.5） **区间外** | 82.38（82.5 至 87.5） **区间外** | 82.65（82.5 至 87.5） | 82.60（82.5 至 87.5） |
| 7 年 OS 安慰剂（报告 77.2） | 75.81（72.7 至 81.1） | 75.41（72.7 至 81.1） | 75.32（72.7 至 81.1） | 75.65（72.7 至 81.1） |
| 7 年 EFS 帕博利珠单抗（报告 78.3） | 78.27（75.3 至 81.1） | 77.89（75.3 至 81.1） | 79.27（75.3 至 81.1） | 78.89（75.3 至 81.1） |
| 7 年 EFS 安慰剂（报告 69.8） | 69.84（65.0 至 74.2） | 69.43（65.0 至 74.2） | 69.09（65.0 至 74.2） | 68.68（65.0 至 74.2） |
| k | 1.333 | 1.166 | 1.528 | 1.546 |
| 术前进展中位（月） | 10.00 | 10.00 | 10.00 | 10.00 |
| KM 平方误差和（百分点²） | 154.6 | 157.2 | 144.7 | 144.4 |

### 16.4 判定

**第十一轮设定按规则停下**：门槛 (c) 不达标——帕博利珠单抗 7 年 OS 模型 82.34，区间 82.5 至 87.5（低 0.16 个百分点）。门槛与第十一轮完全相同，没有放宽，没有手动指定 k，没有自行改结构或目标函数。第十轮设定在修正后的引擎下三道门槛都达标，但按规则只报告，不作为回退选项（其 non-pCR 层 7 年两臂差有已知偏差：模型 12.43 对报告 7.9 个百分点）。

诊断（不作门槛，`R/15b_round11_diag.R`，修正后的引擎）：引擎中按 pCR 分层的 7 年 EFS 与约束值完全相同；只改 k（其余参数取本轮校准值、不重新优化）时三道门槛同时满足的 k 为 0.80 至 1.25（校准值 1.333）。

### 16.5 状态

主目录（`data/fits/fits.rds`、`engine_params.rds`、`calibration_candidates.rds` 与校准输出）仍为第十轮的文件，**这些是用修正前的引擎算出的**；`config.R` 的默认仍为 5 年、区间约束（设 `EXERCISE_CEA_EFS_CONSTRAINT=7,equal` 即重现第十一轮设定）。引擎的修正已提交。两种设定在修正后引擎下的产物在 `output/phase1/round12/`、`data/fits/round12/`。本地参照 `output/check/bootstrap10_local.rds` 是修正前的引擎生成的，未重新生成；没有运行 `R/06d_reference_bounds.R`；没有启动 Longleaf。

## 17. 第十三轮（2026-10-23）：k 只作用于早期远处复发

规则在任何计算之前单独提交（`docs/acceptance_rule_round13.md`，git 8f979c2）。唯一的改动：帕博利珠单抗组远处复发后风险的倍数 k 只作用于早期远处复发（随机化后 18 个月以内进入），晚期远处复发两臂都取 k = 1；参数个数不变，k 的范围仍为 0.25 至 4；设定沿用第十一轮（7 年、等式约束）与修正后的引擎（git 4c67d2e）；门槛与第十一轮完全相同；情景 k = 1 不变。修改记录如实写明：本修改是看到第十二轮结果（git 3f4be26）之后做出的；数据上的理由是单一 k 无法同时满足第 1 至 5 年与第 7 年（帕博利珠单抗组需要早期较高、后期较低的复发后死亡）；临床上的理由是 k 的依据（用过帕博利珠单抗后再复发时有效治疗较少）适用于治疗期间或结束后不久的复发，KEYNOTE-355 允许距治愈性治疗结束 6 个月以上的复发者再用帕博利珠单抗加化疗，术后帕博利珠单抗约在随机化后 12.5 个月结束，18 个月大致相当于结束后 6 个月。

实现：`R/engine.R` 的 `dr_with_k()`（范围 `"early"` 时晚期子状态取 k = 1，`dr_late_spec()` 读 `k_late`），引擎（`survival_engine()`）与校准（`cal_os()`、`cal_curves()`）共用；范围存于参数（`pembro_dr_k_scope`；没有此字段的旧参数按「全部」处理，第十二轮的结果可原样重现）；`config.R` 的 `pembro_dr_k_scope`（默认仍为 `"all"`，环境变量 `EXERCISE_CEA_DR_K_SCOPE` 覆盖）。`R/test_engine_vectorized.R` 加入范围 `"early"` 的情形。

### 17.1 校准结果（与第十二轮——第十一轮设定、修正后的引擎——并列）

| 项目 | 第十三轮 | 第十二轮 |
|---|---|---|
| 门槛 (a) | 达标 | 达标 |
| 门槛 (b) | 达标 | 达标 |
| 门槛 (c) | 达标 | **不达标** |
| k（范围 0.25 至 4） | **4.000（贴上界）** | 1.333 |
| OS 第 1 年 帕博利珠单抗（KM 97.19，95% 区间 96.04 至 98.35） | 97.50 | 97.95 |
| OS 第 2 年 帕博利珠单抗（KM 92.20，95% 区间 90.34 至 94.10） | 92.74 | 94.04 |
| OS 第 3 年 帕博利珠单抗（KM 89.51，95% 区间 87.39 至 91.68） | 90.84 | 91.05 |
| OS 第 4 年 帕博利珠单抗（KM 87.84，95% 区间 85.58 至 90.16） | 88.73 | 88.40 |
| OS 第 5 年 帕博利珠单抗（KM 86.55，95% 区间 84.19 至 88.98） | 86.65 | 86.06 |
| OS 第 1 年 安慰剂（KM 98.72，95% 区间 97.61 至 99.84） | 97.97 | 97.97 |
| OS 第 2 年 安慰剂（KM 91.02，95% 区间 88.23 至 93.90） | 92.25 | 92.25 |
| OS 第 3 年 安慰剂（KM 86.90，95% 区间 83.62 至 90.32） | 87.62 | 87.62 |
| OS 第 4 年 安慰剂（KM 83.53，95% 区间 79.92 至 87.30） | 83.73 | 83.73 |
| OS 第 5 年 安慰剂（KM 81.71，95% 区间 77.95 至 85.65） | 80.53 | 80.53 |
| OS 第 7 年 帕博利珠单抗（报告 85.1，82.5 至 87.5） | 83.08 | 82.34 **区间外** |
| OS 第 7 年 安慰剂（报告 77.2，72.7 至 81.1） | 75.81 | 75.81 |
| EFS 第 7 年 帕博利珠单抗（报告 78.3，75.3 至 81.1） | 78.27 | 78.27 |
| EFS 第 7 年 安慰剂（报告 69.8，65.0 至 74.2） | 69.84 | 69.84 |
| 5 年 RMST 两臂差（年；KM 0.0985，区间 -0.0381 至 0.2421） | 0.1130 | 0.1268 |
| 远处复发中早期的比例，至 7 年 帕博利珠单抗（早期 / 全部，累积发生 %） | 29.7%（4.64 / 15.61） | 29.7%（4.64 / 15.61） |
| 远处复发中早期的比例，至 7 年 安慰剂 | 28.3%（5.90 / 20.86） | 28.3%（5.90 / 20.86） |
| 远处复发中早期的比例，终生 帕博利珠单抗 | 21.8%（4.64 / 21.26） | 21.8%（4.64 / 21.26） |
| 远处复发中早期的比例，终生 安慰剂 | 19.8%（5.90 / 29.82） | 19.8%（5.90 / 29.82） |
| 术前进展的中位（月） | 10.00（贴下界） | 10.00（贴下界） |
| KM 平方误差和（百分点²） | 90.1 | 154.6 |

### 17.2 判定

三道门槛都达标，但 **k = 4.000，贴在上界 4**。按规则（k 贴在边界上，即使门槛通过也停下报告）停下，未采用；没有自行增加结构或改变 k 的范围，没有重新生成参照，没有启动 Longleaf。主目录仍为第十轮的文件（用修正前的引擎算出），`config.R` 的默认仍为第十轮的设定（设 `EXERCISE_CEA_EFS_CONSTRAINT=7,equal` 与 `EXERCISE_CEA_DR_K_SCOPE=early` 即重现本轮）；本轮的产物在 `output/phase1/round13/round13/`、`data/fits/round13/round13/`。

### 17.3 诊断（不作门槛，`R/15b_round11_diag.R`）

只改 k（其余参数取本轮校准值、不重新优化）时，三道门槛同时满足的 k 为 0.80 至 4.00；k 约 1.5 以上时帕博利珠单抗组 7 年 OS 几乎不再随 k 变化（k = 1.5、2、4 时分别为 83.11、83.09、83.08），k 主要改变第 1 至 3 年的死亡时点。按校准值 k = 4.00，帕博利珠单抗组早期远处复发后超额生存的中位约为 3.6 个月（k = 1 时为 ESME 的 9.7 个月）。

## 18. 第十四轮（2026-10-23）：基准取 k = 1，早期复发后 k 改为外部情景

先补两项（与采用哪一轮无关，git 91e8741）：`docs/model_spec.md` 第 1 节的「外推」（pCR 层 Weibull 拟合的全死因风险在帕博利珠单抗组第 22 年、安慰剂组第 27 年起低于背景死亡率，此后以背景死亡率作下限）与第 8 节的待决事项（术前进展的中位在第五轮以后各轮都贴在下界 10 个月，放到第 2 阶段作情景分析）。

规则在任何计算之前单独提交（`docs/acceptance_rule_round14.md`，git 13325b6）：基准 k 固定为 1、不参与校准，远处复发后生存两臂共用、全部来自 ESME 的外部拟合；其余沿用第十三轮（7 年等式约束、修正后的引擎）；校准只剩术前进展的两个参数；门槛 (a)、(b)、(c) 不变。原来的情景 k = 1 并入基准。修改记录如实写明：本修改是看到第十三轮结果（git 01a8c13）之后做出的；第十三轮的 k 贴上界 4，对应早期远处复发后超额生存中位约 3.6 个月（ESME 9.7 个月），而接受新辅助化疗加免疫治疗后复发的真实世界队列（Fedele 2026）两组合成约 7.9 个月，校准出的 k 吸收的是与复发后生存无关的偏差；k 在第六轮引入时补偿的两处偏差已在第十一、十二轮修正；外部数据能确定的量不交给校准。实现：`config.R` 的 `pembro_dr_k_fixed = 1`，`calibration.R` 的 `cal_fixed()`（`05_calibrate.R` 与 bootstrap 共用）。

### 18.1 基准的校准与门槛（与第十三、十二轮并列）

| 项目 | 第十四轮基准 | 第十三轮 | 第十二轮 |
|---|---|---|---|
| 门槛 (a) | 按 Bonferroni 同时区间接受 | 达标 | 达标 |
| 门槛 (b) | 达标 | 达标 | 达标 |
| 门槛 (c) | 达标 | 达标 | **不达标** |
| OS 第 1 年 帕博利珠单抗（KM 97.19，95% 区间 96.04 至 98.35） | 98.02 | 97.50 | 97.95 |
| OS 第 2 年 帕博利珠单抗（KM 92.20，95% 区间 90.34 至 94.10） | 94.53 *（95% 区间外）* | 92.74 | 94.04 |
| OS 第 3 年 帕博利珠单抗（KM 89.51，95% 区间 87.39 至 91.68） | 91.72 *（95% 区间外）* | 90.84 | 91.05 |
| OS 第 4 年 帕博利珠单抗（KM 87.84，95% 区间 85.58 至 90.16） | 89.22 | 88.73 | 88.40 |
| OS 第 5 年 帕博利珠单抗（KM 86.55，95% 区间 84.19 至 88.98） | 86.96 | 86.65 | 86.06 |
| OS 第 1 年 安慰剂（KM 98.72，95% 区间 97.61 至 99.84） | 97.97 | 97.97 | 97.97 |
| OS 第 2 年 安慰剂（KM 91.02，95% 区间 88.23 至 93.90） | 92.25 | 92.25 | 92.25 |
| OS 第 3 年 安慰剂（KM 86.90，95% 区间 83.62 至 90.32） | 87.62 | 87.62 | 87.62 |
| OS 第 4 年 安慰剂（KM 83.53，95% 区间 79.92 至 87.30） | 83.73 | 83.73 | 83.73 |
| OS 第 5 年 安慰剂（KM 81.71，95% 区间 77.95 至 85.65） | 80.53 | 80.53 | 80.53 |
| OS 第 7 年 帕博利珠单抗（报告 85.1，82.5 至 87.5） | 83.24 | 83.08 | 82.34 **区间外** |
| OS 第 7 年 安慰剂（报告 77.2，72.7 至 81.1） | 75.81 | 75.81 | 75.81 |
| EFS 第 7 年 帕博利珠单抗（报告 78.3，75.3 至 81.1） | 78.27 | 78.27 | 78.27 |
| EFS 第 7 年 安慰剂（报告 69.8，65.0 至 74.2） | 69.84 | 69.84 | 69.84 |
| 5 年 RMST 两臂差（年；KM 0.0985，区间 -0.0381 至 0.2421） | 0.1517 | 0.1130 | 0.1268 |
| 术前进展的中位（月；下界 10） | 10.00 | 10.00 | 10.00 |
| k | 1.000 | 4.000 | 1.333 |
| KM 平方误差和（百分点²） | 192.3 | 90.1 | 154.6 |

判定：三道门槛都达标——(a) 按 Bonferroni 同时区间接受（帕博利珠单抗第 2、3 年高于 95% 区间上限，10 个点都在 99.5% 区间内），(b) 达标，(c) 4 个值都在区间内。**采用第十四轮**（`config.R` 默认改为第十四轮，主目录换成第十四轮的文件，第十轮的校准输出另存于 `output/phase1/round10/final_state/`）。术前进展的中位仍贴下界 10 个月（`docs/model_spec.md` 第 8 节的待决事项）；KM 平方误差和 192.3，大于第十三轮（k = 4）与第十二轮。

### 18.2 情景「早期复发后 k（外部）」（只报告，不参与采用判定；`R/17_round14_kext.R`）

| 量 | 值 | 来源 |
|---|---|---|
| 可评估例数 | 52 | Fedele 2026 p.4 |
| 90 天内未开始一线治疗（例） | 17 | Fedele 2026 p.4 |
| 开始一线治疗（例） | 35 | Fedele 2026 p.4 |
| 中位 OS，未开始（月） | 3.4 | Fedele 2026 p.5 (abstract p.1) |
| 中位 OS，开始（月） | 12.4 | Fedele 2026 p.5 (abstract p.1) |
| 两组指数分布按 17/52、35/52 混合后的中位 m（月） | 7.850 | computed (17/52 : 35/52 mixture of exponentials) |
| ESME 早期远处复发：形状 | 1.6598 | ESME fit (data/fits/esme_fits.rds) |
| ESME 早期远处复发：中位（月） | 9.734 | ESME fit |
| ESME 早期的超额生存 S(m) | 0.5883 | computed |
| k = log(0.5) / log(S(m)) | 1.3067 | computed: log(0.5) / log(S) |
| 检验：k 下的超额生存中位（月） | 7.850 | computed (check) |
| 无病间隔中位，未开始 / 开始（月；从手术算起） | 7.4 / 14.3 | Fedele 2026 p.4, Table 2 |
| 随访中位（月） | 24 | Fedele 2026 p.3 |

Fedele 2026：Breast Cancer Res Treat 2026;218:8，DOI 10.1007/s10549-026-08023-2（意大利多中心回顾性，新辅助化疗加免疫治疗后的 209 例中 54 例转移复发，可评估 52 例；摘要写作「17 of 54 evaluable」，32.7% 对应 17/52，按正文 p.4 的 52 例计）。这是近似：该队列的无病间隔从手术算起，两组中位为 7.4 与 14.3 个月，按本模型的定义是早期与晚期复发的混合，这里只用于早期复发，所以这个情景偏温和；随访中位 24 个月。k 只作用于早期远处复发，晚期 k = 1；其余参数取基准的校准值。

| 项目 | 参照值 | 区间 | 情景 | 在区间内 |
|---|---|---|---|---|
| OS 1 y pembro | 97.189 | 96.038 至 98.354 | 97.953 | 是 |
| OS 2 y pembro | 92.200 | 90.340 至 94.099 | 94.100 | **否** |
| OS 3 y pembro | 89.510 | 87.387 至 91.684 | 91.371 | 是 |
| OS 4 y pembro | 87.841 | 85.579 至 90.163 | 88.975 | 是 |
| OS 5 y pembro | 86.552 | 84.191 至 88.978 | 86.782 | 是 |
| OS 1 y placebo | 98.718 | 97.608 至 99.841 | 97.973 | 是 |
| OS 2 y placebo | 91.021 | 88.227 至 93.904 | 92.246 | 是 |
| OS 3 y placebo | 86.903 | 83.616 至 90.319 | 87.617 | 是 |
| OS 4 y placebo | 83.532 | 79.924 至 87.303 | 83.732 | 是 |
| OS 5 y placebo | 81.706 | 77.948 至 85.646 | 80.529 | 是 |
| os7_pembro | 85.100 | 82.500 至 87.500 | 83.141 | 是 |
| os7_placebo | 77.200 | 72.700 至 81.100 | 75.814 | 是 |
| efs7_pembro | 78.300 | 75.300 至 81.100 | 78.267 | 是 |
| efs7_placebo | 69.800 | 65.000 至 74.200 | 69.842 | 是 |
| rmst5_diff_years | 0.098 | -0.038 至 0.242 | 0.140 | 是 |

情景的门槛：(a) 满足、(b) 满足、(c) 满足（k = 1.307）。

### 18.3 本地参照与边界报告

第十四轮的本地参照（基础种子 20261023，10 次）在提交 e90fa6c 上生成（x86_64-w64-mingw32，2026-10-24 09:07:36 EDT；`R/` 与 `data/` 无未提交改动；`output/check/bootstrap10_bounds_round14*.csv`）。`R/06d_reference_bounds.R`：k 不再校准，10 次都为 1.000、1.000、1.000、1.000、1.000、1.000、1.000、1.000、1.000、1.000；术前进展中位贴 10 个月的 10 次、贴 26 个月的 0 次（第十轮的参照：8 次与 1 次）。之后 Longleaf 的跨平台核对通过、1,000 次 bootstrap 完成（git 48f4ee8，`output/phase1/longleaf_bootstrap_round14.md`，`data/bootstrap/`）：术前进展中位 829 次贴 10 个月、97 次贴 26 个月，5 年存活 686 次贴 5%，115 次形状约 0.002；这促成了第十五轮（第 19 节）。

## 19. 第十五轮（2026-10-24）：术前进展后的生存改为外部输入，不再校准；OS 只用于验证

先做（与本轮判定无关，git f94fa55）：`config.R` 新增 bootstrap 的基础种子 `boot_seed = 20261023`（与本机参照相同；`06_bootstrap.R`、`06c_bootstrap_check.R` 与 `bootstrap_core.R` 的默认），1,000 次只靠仓库即可重现；`seed = 20261021` 仍用于校准与门槛 (b) 的 KM 差 bootstrap 区间，不变。新建 `docs/longleaf.md`，记录 Longleaf 环境的两处处理（RHEL 9.8 下 renv 包库路径指回 9.7 的包库；1,000 次作业内关闭 renv 的 sandbox），两处都不改代码，也不改加载的包。

规则在任何计算之前单独提交（`docs/acceptance_rule_round15.md`，git 475f828）：唯一的改动是术前进展后的超额死亡不再校准，取 ESME 早期复发拟合的同一分布（形状 1.6598、中位 9.73 个月；bootstrap 中与早期远处复发使用同一次 ESME 重抽样），原来的约束撤销；模型中不再有任何由 OS 校准的参数；门槛不变。修改记录如实写明：本修改是看到第十四轮 Longleaf bootstrap（git 48f4ee8）之后做出的；1,000 次中术前进展中位 829 次贴 10 个月、97 次贴 26 个月，115 次形状约 0.002，5 年存活 686 次贴 5%，这两个参数由约束而不是数据决定，实际在吸收极少数早期死亡的噪声；依据第十四轮的原则（外部数据能确定的量不交给校准），化疗期间进展属于化疗耐药，最接近的外部数据是化疗结束后 12 个月内的复发（ESME），也是原来约束的下界；「早期复发后 k（外部）」扩及帕博利珠单抗组的术前进展，理由是在免疫治疗期间进展比治疗结束后复发更符合免疫治疗耐药。实现：`config.R` 的 `preprog_source`（`"esme_early"`），`calibration.R` 的 `cal_specs()`、`cal_fixed()`（没有自由参数时 `calibrate_os()` 只运行引擎），引擎的 `pembro_preprog_k`（情景用）。

### 19.1 结果（与第十四轮并列）

| 项目 | 第十五轮基准 | 第十四轮 |
|---|---|---|
| 门槛 (a) | 按 Bonferroni 同时区间接受 | 按 Bonferroni 同时区间接受 |
| 门槛 (b) | 达标 | 达标 |
| 门槛 (c) | 达标 | 达标 |
| OS 第 1 年 帕博利珠单抗（KM 97.19，95% 区间 96.04 至 98.35） | 98.00 | 98.02 |
| OS 第 2 年 帕博利珠单抗（KM 92.20，95% 区间 90.34 至 94.10） | 94.51 *（95% 区间外）* | 94.53 *（95% 区间外）* |
| OS 第 3 年 帕博利珠单抗（KM 89.51，95% 区间 87.39 至 91.68） | 91.71 *（95% 区间外）* | 91.72 *（95% 区间外）* |
| OS 第 4 年 帕博利珠单抗（KM 87.84，95% 区间 85.58 至 90.16） | 89.21 | 89.22 |
| OS 第 5 年 帕博利珠单抗（KM 86.55，95% 区间 84.19 至 88.98） | 86.95 | 86.96 |
| OS 第 1 年 安慰剂（KM 98.72，95% 区间 97.61 至 99.84） | 97.95 | 97.97 |
| OS 第 2 年 安慰剂（KM 91.02，95% 区间 88.23 至 93.90） | 92.20 | 92.25 |
| OS 第 3 年 安慰剂（KM 86.90，95% 区间 83.62 至 90.32） | 87.59 | 87.62 |
| OS 第 4 年 安慰剂（KM 83.53，95% 区间 79.92 至 87.30） | 83.71 | 83.73 |
| OS 第 5 年 安慰剂（KM 81.71，95% 区间 77.95 至 85.65） | 80.51 | 80.53 |
| OS 第 7 年 帕博利珠单抗（报告 85.1，82.5 至 87.5） | 83.24 | 83.24 |
| OS 第 7 年 安慰剂（报告 77.2，72.7 至 81.1） | 75.80 | 75.81 |
| EFS 第 7 年 帕博利珠单抗（报告 78.3，75.3 至 81.1） | 78.27 | 78.27 |
| EFS 第 7 年 安慰剂（报告 69.8，65.0 至 74.2） | 69.84 | 69.84 |
| 5 年 RMST 两臂差（年；KM 0.0985，区间 -0.0381 至 0.2421） | 0.1524 | 0.1517 |
| 术前进展后超额死亡：中位（月）/ 形状 | 9.73 / 1.6598 | 10.00 / 1.6387 |
| KM 平方误差和（百分点²；只报告） | 189.0 | 192.3 |
| 术前进展者进入后 1 年存活（全死因，%） | 41.3 | 42.5 |
| 术前进展者进入后 5 年存活（全死因，%） | 4.6 | 5.0 |

判定：三道门槛都达标。**采用第十五轮**（`config.R` 默认改为第十五轮，主目录换成第十五轮的文件）。

### 19.2 情景（只报告，不参与判定；`R/18_round15_scenarios.R`）

| 情景 | 门槛a | 门槛b | 门槛c | 帕博利珠单抗7年OS | RMST两臂差 | 在95区间外的点 |
|---|---|---|---|---|---|---|
| 基准 | 满足 | 满足 | 满足 | 83.24 | 0.1524 | OS 2 y pembro 94.51（90.34 至 94.10）；OS 3 y pembro 91.71（87.39 至 91.68） |
| 术前进展后生存（Elmore，中位 26 个月） | **不满足** | 满足 | 满足 | 83.43 | 0.1276 | OS 1 y pembro 98.47（96.04 至 98.35）；OS 2 y pembro 95.18（90.34 至 94.10）；OS 3 y pembro 92.24（87.39 至 91.68） |
| 早期复发后 k（外部，k = 1.307，含帕博利珠单抗组的术前进展） | 满足 | 满足 | 满足 | 83.10 | 0.1356 | 无 |

| 设定 | 中位月 | 形状 | k | 进入后1年存活 | 进入后5年存活 |
|---|---|---|---|---|---|
| 第十五轮基准（ESME 早期拟合） | 9.73 | 1.6598 | 1.000 | 41.3 | 4.6 |
| 情景 Elmore（中位 26 个月） | 26.00 | 1.6598 | 1.000 | 78.2 | 19.8 |
| 情景 k 外部（帕博利珠单抗组） | 9.73 | 1.6598 | 1.307 | 31.5 | 1.8 |
| 第十四轮（校准值，贴约束边界） | 10.00 | 1.6387 | 1.000 | 42.5 | 5.0 |

### 19.3 本地参照与边界报告

本地参照 `output/check/bootstrap10_local.rds`（基础种子 20261023，10 次）在提交 bb5d7bc 上重新生成（x86_64-w64-mingw32，2026-10-24 14:53:49 EDT；`R/` 与 `data/` 无未提交改动：是）。`R/06d_reference_bounds.R`：没有任何校准参数——k 10 次都为 1；术前进展的中位为各样本 ESME 重抽样的早期复发拟合值（9.41、9.62、9.39、9.79、9.56、10.18、10.00、9.92、9.62、9.82 个月），贴 10 个月或 26 个月的标记都为否（约束已撤销）。Longleaf 的 1,000 次 bootstrap 未启动。

### 19.4 Longleaf 的 1,000 次 bootstrap（2026-10-25，`output/phase1/longleaf_bootstrap_round15.md`）

- 跨平台核对（提交 8dcab58，在移动 `data/` 下任何文件之前；10 次，与本机参照 bb5d7bc 比较，`output/check/bootstrap10_compare_longleaf.csv`）：通过。臂 × pCR 的全部输出最大差 9.9e-08 个百分点，5 年 RMST 两臂差最大差 5.1e-10 年（容差 0.05 个百分点与 0.001 年）；EFS 约束是否起作用、pCR 与术前进展、术前 KM、7 年目标的抽取值逐位相同。
- 1,000 次：结果提交 b06c9b9，运行于提交 f806079（`R/` 与 8dcab58 相同；`data/` 只差把第十四轮的 1,000 次原样移到 `data/bootstrap/round14/`，bootstrap 不读该目录）。`Rscript R/06_bootstrap.R 1000 32`，基础种子取 `config.R` 的 `boot_seed`（20261023），没有用包装脚本。完成 1000 次、失败 0 次、重抽 0 次；收敛码不为 0 的 0 次（没有自由参数，`calibrate_os()` 只运行引擎）；`boot_run()` 用 0.54 分钟（节点 AMD EPYC 9654，32 个工作进程）。
- 前 10 次与本机参照逐项一致：第 5、7、10、20 年臂 × pCR 的输出最大差 8.3e-08 个百分点（由仓库中的 `data/bootstrap/boot_replicates.rds` 与 `output/check/bootstrap10_local.rds` 算出）。Longleaf 内与同一类 CPU 上的 06c 逐位相同；与另一类 CPU（EPYC 7742）上的核对相差约 1e-10，原因是 OpenBLAS 按 CPU 选择的计算内核不同（`docs/longleaf.md`）。
- 边界：校准的 6 个边界标记在 1,000 次中合计 0 个（没有校准参数）。术前进展后的形状与中位在每个样本中都与同一样本的早期远处复发相同（最大差 0）。远处复发与术前进展的参数都是 ESME 重抽样后的无约束拟合值，没有贴边界：

| 参数 | 基准 | bootstrap中位数_2.5至97.5百分位_最小至最大 |
|---|---|---|
| 术前进展后中位（月） | 9.7339 | 9.7273（9.1000 至 10.4310；8.6263 至 10.9072） |
| 早期远处复发后中位（月） | 9.7339 | 9.7273（9.1000 至 10.4310；8.6263 至 10.9072） |
| 晚期远处复发后中位（月） | 16.9299 | 16.9611（15.8813 至 18.0074；14.9050 至 18.8208） |
| 形状（三者共用） | 1.6598 | 1.6634（1.5902 至 1.7357；1.5545 至 1.7819） |

- EFS 的治愈比例：非 pCR 层的治愈 Weibull 模型中，治愈比例 θ 在 4 个样本中为 0（< 1e-8；b = 250 为帕博利珠单抗 non-pCR、b = 590 为帕博利珠单抗 non-pCR、b = 888 为化疗 non-pCR、b = 982 为帕博利珠单抗 non-pCR）。这是参数空间的自然边界（7 年等式约束下 θ 由约束与另外两个参数决定，实现上要求 θ > 0，θ 只能趋近 0），不是人为约束，不作处理；这 4 个样本在该层实际上是不含治愈部分的 Weibull，7 年值仍满足等式约束。1,000 个样本（含为 0 的 4 个）中 θ 的 1% 分位为 0.26（帕博利珠单抗 non-pCR）与 0.40（化疗 non-pCR），基准为 0.596 与 0.543；分位数用全部样本计算，因为这 4 个样本按决定属正常样本、不作处理，去掉后再算分位数与此矛盾，并使分布偏高（2026-10-25 更正）。EFS 的拟合在第十四轮与本轮之间没有改动，1,000 个样本的 EFS 参数与第十四轮逐位相同，所以第十四轮的 1,000 次同样包含这 4 个样本。

- 各臂 OS 与 EFS（%，pCR 不分层；基准为 `data/fits/engine_params.rds` 的引擎输出，bootstrap 为 1,000 次的中位数与 2.5、97.5 百分位；`output/phase1/bootstrap_summary.csv`。第 1、2、3 年由重建的参数组算出，见 Longleaf 报告第 5 节）：

| 终点 | 年 | 化疗基准 | 化疗bootstrap中位数 | 化疗2.5至97.5 | 帕博利珠单抗基准 | 帕博利珠单抗bootstrap中位数 | 帕博利珠单抗2.5至97.5 |
|---|---|---|---|---|---|---|---|
| OS |  5 | 80.51 | 80.77 | 78.05 至 83.34 | 86.95 | 87.00 | 85.26 至 88.58 |
| OS |  7 | 75.80 | 75.99 | 72.53 至 79.29 | 83.24 | 83.27 | 81.34 至 85.32 |
| OS | 10 | 71.13 | 71.16 | 66.59 至 75.28 | 79.28 | 79.19 | 76.48 至 81.97 |
| OS | 20 | 61.74 | 61.35 | 52.27 至 68.00 | 71.65 | 71.18 | 65.17 至 75.97 |
| EFS |  5 | 72.08 | 72.36 | 68.21 至 76.23 | 80.47 | 80.55 | 78.28 至 83.05 |
| EFS |  7 | 69.84 | 69.94 | 65.10 至 74.25 | 78.27 | 78.25 | 75.35 至 81.21 |
| EFS | 10 | 67.26 | 67.09 | 61.06 至 72.13 | 76.03 | 75.92 | 71.99 至 79.67 |
| EFS | 20 | 60.12 | 59.70 | 48.36 至 67.13 | 70.73 | 70.13 | 62.63 至 75.53 |

- 5 年 RMST 两臂差（年，帕博利珠单抗 − 化疗，引擎）：基准 0.1524，bootstrap 中位数 0.1449（2.5 至 97.5 百分位 0.0552 至 0.2469），均值 0.1461；参考：同一差值的 KM 值（各样本重抽的 OS 个体数据）中位数 0.1002（-0.0327 至 0.2322）。
- 每个样本的参数组都能从 `boot_replicates.rds` 重建（`R/07_engine_outputs.R` 的 `rebuild()`；重算的 60,000 个输出与保存值逐位相同），两个情景都可以在重建的参数组上换算：「早期复发后 k（外部）」用固定的 k = 1.307（`params_kext()`），「术前进展后生存（Elmore）」只把中位改为 26 个月、形状与其余参数沿用各样本自己的值（`docs/model_spec.md` 第 6 节的决定）。没有另跑两个情景的 bootstrap。

