# 表与图的计划 v1（执笔第 1 步，2026-10-26）

## 0. 规约的三行声明

1. 已全文阅读 `Documents/ClaudeCode/WRITING_RULES.md`（开始时一次；交付前再读一次，对照结果见第 7 节）。
2. 处在执笔连锁的段阶 2（表与图）。段阶 1（ARS deep-research 的文献检索与注释书目）尚未做；本步按指示先定表图，所以表中的来源暂用描述性名称（试验名、数据来源名），不放文献编号，待段阶 1 之后换成编号。
3. 底本：无（v1 新建）。开工时 `manuscript/` 不存在，作业树里没有其他版本的表图、md 原稿或模板。

产物：`tables_v1.docx`（Table 1–3）、`figures_v1.docx`（Fig. 1–3，一图一页，图注在图下）、本文件、`numbers_ledger_v1.md`（每个数字的来源）、`check_v1.md`（从 docx 回读的检查）、`MANIFEST_v1.md`（sha256）。图文件在 `figures/`（PDF、SVG、PNG 与 TIFF 600 dpi）。代码在 `manuscript/code/`：`make_tables_v1.py`、`make_figures_v1.py`、`make_ledger_v1.py`（共用 `v1_common.py`、`docx_util.py`）。全部只读分析输出，不运行模型。作图后端为 Python（matplotlib，nature-figure 已存的默认）。

## 1. 目的的编号（全稿以此为轴）

| 编号 | 内容 |
|---|---|
| 目的 1（主） | 日本公共医疗支付方的立场，含帕博利珠单抗的术前化疗加结构化运动方案时，每人可负担的方案费用上限如何随运动对复发风险的效应大小（复发 HR）与持续时间变化（阈值 500 万日元/QALY） |
| 目的 2（副 a） | 同一上限，加在单用化疗上 |
| 目的 3（副 b） | 帕博利珠单抗对单用化疗的费用效果（参照） |
| 目的 4（副 c） | 运动要达到与帕博利珠单抗同等 QALY 增量所需的效应 |

主张（尾崎 2026-10-26 同意）与支撑它的表图：

| 主张的部分 | 表或图的位置 |
|---|---|
| 费用效果取决于效应的大小 | Table 2 Panel A、Fig. 2 |
| 取决于效应的持续时间 | Table 2 Panel C |
| 不取决于方案价格（上限远大于三种方案费用；上限 = 方案费用的 HR 都贴近 1） | Table 2 Panel B 第 1 行、Panel D、Fig. 2b |
| 复发风险降低几个百分点即可收回成本（转移复发治疗费情景为 4% 至 9%） | Table 2 Panel B「Medical costs avoided equal the cost of the fee-schedule-based program」（主比较 0.958）与 Panel D 两情景（0.918、0.914）；见第 6 节 D5 |
| 运动的基准 500 万日元，帕博利珠单抗另示 750 万日元 | Table 2 题目（500 万）；Table 3 Panel B（500 万与 750 万的划算概率） |

## 2. 正文表

### Table 1. Key model inputs（目的 1–4 共用；Methods 引用）

- 内容：模型设定（立场、队列、时间范围与周期、折现、价格年度、不确定性分析的样本数与 95% UI 的定义）；生存（pCR 比例、术后 EFS 的拟合与 7 年约束、远处复发后与术前进展后的生存、背景死亡、OS 只作验证）；关键费用（帕博利珠单抗、转移复发一次与二次以后、终末期、三种运动方案、运动的筋骨格系 AE）；效用；运动效应的定义与持续假设（路径 A、基准与两个替代持续、CHALLENGE 参照值、路径 B、运动 AE）；情景（早期复发后 k、转移复发治疗费 50%、艾立布林、S-JP）。全部参数放 Supplementary Table S1。
- 来源：`input/params/parameters_v10.xlsx`（工作表 パラメータ 的 G 列基本值与 N 列备考；工作表 シナリオ）；`data/pcr_counts.csv`（K22 (IA4) 行）；`data/kn522_final_7y.csv`（efs_pcr_*、efs_nonpcr_*）；`output/phase1/calibration.csv`（calibrated 行的 dr_median_months、dr_late_median_months、dr_shape）；`output/phase1/round14/kext_derivation.csv`（k_external）；`docs/model_spec.md` 与 `docs/analysis_plan_phase2.md` 的设定行；`input/papers/CHALLENGE.pdf` p.7（HR 0.72）。逐格见 numbers_ledger_v1.md 第 1 节。
- 正文引用处：Methods 的 Study background（模型与数据来源的段落，与 Fig. 1、Supplementary Table S1 同段，在 Fig. 1 之后）。

### Table 2. 上限（指示中的 Table 3；目的 1、2）

- Panel A：复发 HR 0.70 至 1.00（每 0.05）的上限，两列（运动加在化疗加帕博利珠单抗上；运动加在单用化疗上），确定性值与 95% UI 在同一格。来源：`output/phase2/main/det_caps.csv`（column = base、axis = hr0、cap_500）、`psa_caps_summary.csv`（cap500_lo、cap500_hi）。
- Panel B：上限 = 费用表方案（E02）的 HR；避免的医疗费用 = E01、E02、E03 的 HR。来源：`sc_base_crossings.csv`（uniroot 连续解；与报告第 1.7 节格点插值之差 ≤ 0.00003，三位小数相同）。
- Panel C：效应持续的两个替代假设下 HR 0.85 的上限（基准持续的值即 Panel A 的 0.85 行，不重复）。来源：`scenario_caps.csv`（path_a_s1、path_a_s2）；只有确定性值（该情景未做 PSA），脚注写明。
- Panel D：两个转移复发治疗费情景下 HR 0.85 的上限（含 95% UI），以及上限 = E02 的 HR、避免的医疗费用 = E02 的 HR。来源：`sc_metcost50_*`、`sc_eribulin_*` 的 det_caps、psa_caps_summary、crossings。
- 主比较只放基准栏（指示「主比较与次比较各一列」）；「早期复发后 k（外部）」栏放 Supplementary Table S4。
- 阈值 500 万日元/QALY。费用单位千日元（JPY 1,000），精度与报告的「万日元 1 位小数」相同。
- 正文引用处：Results 第 1 段（目的 1：大小，Panel A、B 与 Fig. 2）、第 2 段（目的 1：持续时间与转移复发治疗费，Panel C、D）、目的 2 的段落（次比较列）。

**Table 3 内还是另立 Table 4：并入 Table 2，作 Panel C 与 D。** 理由（WRITING_RULES）：
1. 第 6.1 节「同じ数値は一つの表にだけ置く」：另立表时，基准情形（HR 0.85 的上限、E02 交点）要么在两表重复，要么在情景表里缺席而无法对比；并入后，情景值与同一表 Panel A、B 中只出现一次的基准值直接对照。
2. 第 7.1 节规则 6：一表可服务多个目的；Panel A 至 D 回答目的 1、2 的同一个问题（上限由效应大小、持续时间与转移复发治疗费决定），正对应主张的一句话。
3. 第 7.2 节「表は簡潔で直観的に」：读者不必在两表之间来回。代价是表变长（Panel 标题分段）。

### Table 3. 帕博利珠单抗对单用化疗（指示中的 Table 2；目的 3、4）

- Panel A：增量费用按类别（帕博利珠单抗药剂、给药、免疫相关 AE、发热性中性粒细胞减少、随访、局部区域复发、远处复发一次、二次以后、终末期、其他）与合计（合计含 95% UI）。
- Panel B：增量 QALY（含 95% UI）、ICER（只放点估计）、500 万与 750 万日元下划算的概率。
- 五个条件（列）：基准、早期复发后 k（外部）、日本的术后治疗（S-JP）、转移复发治疗费 50%、二次以后改为艾立布林。
- Panel C（目的 4，指示之外加的，理由见第 6 节 D5）：使「运动加在单用化疗上」的 QALY 增量等于帕博利珠单抗的所需效应：复发 HR 0.425、pCR 提高 35.9 个百分点（都在主轴范围之外，脚注写明）。只有基准列，其余为「—」。
- 来源：`decomp_reference.csv`（d_base、d_kext）；`det_reference.csv`、`psa_reference_summary.csv`；`scenario_reference.csv`（sjp）；`sc_metcost50_det_reference.csv`、`sc_metcost50_psa_reference_summary.csv` 与 `sc_eribulin_` 的同名文件；`det_yardstick.csv`。
- 两情景（50%、艾立布林）的类别值：分析输出只有基准与 k 外部两栏的分解。两情景只改变 D03/D03P/D05 的费用、生存不变，故类别值 = 基准类别值 × 情景倍率（入力表 v10 シナリオ工作表），其余类别不变；各类别之和与模型算出的 Δ费用之差为 5e-9、2e-9 日元（numbers_ledger_v1.md 第 1 节末）。表注写明。是否采用见第 6 节 D6。
- S-JP 栏：该情景没有做 PSA，也没有分解，类别、区间与划算概率为「—」，表注写明。
- 正文引用处：Results 中目的 3 的段落（Panel A、B）与目的 4 的段落（Panel C）。

## 3. 正文图

| 图 | 目的 | 内容 | 数据来源 | 正文引用处 |
|---|---|---|---|---|
| Fig. 1 | 全部（方法） | 模型结构：术前（0 至 7 个月）→ 手术时按 pCR 分层 → 术后无事件 → 局部区域复发、远处复发（早期 ≤ 18 个月 / 晚期）→ 死亡；术前进展只在 non-pCR 层；运动 HR 作用的两条转移用粗箭头标 HR | `docs/model_spec.md` 第 1、3 节（结构，无数值结果） | Methods 的 Study background（先于 Table 1） |
| Fig. 2 | 1、2 | a：HR 0.70 至 1.00 的上限（两比较，各带 95% UI；三种方案费用的水平线；CHALLENGE HR 0.72 竖线，图注写明结肠癌、3 年方案、DFS）。b：放大 HR 0.95 至 1.00 | `det_caps.csv`、`psa_caps_summary.csv`（13 个格点，每 0.025）；方案费用 = 入力表 E01–E03 | Results 第 1 段（Table 2 之后） |
| Fig. 3 | 1 | 主比较 HR 0.85 的单因素敏感性分析（龙卷风图）。改变结果的 21 个输入全部画出（判定与 `R/23_phase2b_report.R` 相同：两端差 > 1e-6 × 基准值），按幅排序；范围按规则设定的行在标签后标 [±25%]、[mirrored]、[price] | `oneway_base.csv`（cap_low、cap_high、cap_base、range_rule） | Results 目的 1 的不确定性（第 2 或第 3 段） |

图的规格：按最终尺寸 170 mm 宽绘制（高：Fig. 1 92 mm、Fig. 2 104 mm、Fig. 3 128 mm），Arial，字号 ≥ 8 pt（PDF 实测）；黑白可分（Fig. 2：实线加实心圆 / 虚线加空心三角；区间带深灰与浅灰，各以实线、虚线描边；方案费用三种线型；Fig. 3：深灰 = 下限、浅灰 = 上限）；图内无题目；面板标签小写 a、b（规约第 7.2 节；指示写的是 A、B）。

## 4. 补充材料清单（编号按计划的正文初次引用顺序；正文写成后按实际顺序再确认）

计划的初次引用顺序：Methods（Study background）S1 → Supplementary Methods S1、Fig. S1、Table S2 → Methods（Statistical analysis 末）S3 → Results 目的 1：S4（Fig. 2 的数值）→ S5（持续）→ S6（Fig. 3 的数值）→ S7（净收益）→ 目的 3：S8（Elmore）→ 目的 4：S9（路径 B）。编号集中在 `manuscript/code/v1_common.py` 的 SUPP，表注与图注从那里读。

| 编号 | 内容 | 目的 | 数据来源（文件与位置） | 正文初次引用处 |
|---|---|---|---|---|
| Supplementary Table S1 | 全部输入：基本值、范围、分布、来源、适用组；生存参数；情景值 | 全部 | `input/params/parameters_v10.xlsx`（パラメータ、シナリオ、計算根拠_原）；`data/params_dist.csv`（分布、range_rule）；`output/phase1/calibration.csv`、`data/pcr_counts.csv`、`data/kn522_final_7y.csv`、`output/phase1/ae_deaths.csv`、`output/phase1/round14/kext_derivation.csv` | Methods, Study background（与 Table 1 同段） |
| Supplementary Methods S1 | 生存模型：KEYNOTE-522 曲线的数字化与个体数据重建、分层 EFS 的分布族与 7 年等式约束、ESME 的外部拟合、引擎、验证规则（门槛 a、b、c）与 bootstrap | 全部 | `docs/model_spec.md` 第 1 节；`output/phase1/phase1_report.md`「第1阶段最终状态」与第 19 节；`docs/acceptance_rule_round15.md` | Methods, Study background（生存模型的句子） |
| Supplementary Fig. S1 | 第 1 阶段的验证：模型 OS 对重建 KM（两臂，第 1 至 5 年，95% 与 Bonferroni 区间），模型 OS、EFS 对最终分析 7 年值；分层 EFS 对重建 KM | 全部 | `output/phase1/round15/base/calibration_curves.csv`、`calibration_gate.csv`、`calibration_final7y.csv`；分层 EFS 的拟合曲线（`output/phase1/engine_curves.csv`）与重建 KM（`data/ipd/`） | Methods, Study background（与 Supplementary Methods S1 同句） |
| Supplementary Table S2 | 验证的数值：门槛 (a) 10 个点、(b) 5 年 RMST 两臂差、(c) 7 年 OS 与 EFS；bootstrap 的 OS、EFS（5、7、10、20 年） | 全部 | `output/phase1/round15/base/calibration_gate.csv`、`calibration_gate_rmst.csv`、`calibration_final7y.csv`；`output/phase1/bootstrap_summary.csv` | Methods, Study background |
| Supplementary Table S3 | CHEERS 2022 清单（各项目对应正文的页与节） | 全部 | 正文写成后填 | Methods, Statistical analysis 末句 |
| Supplementary Table S4 | Fig. 2 的数值：HR 0.700 至 1.000（每 0.025），500 万与 750 万日元，主比较（基准、早期复发后 k 外部）与次比较，上限 [95% UI] 与「上限 ≥ 费用表方案费用」的概率 | 1、2 | `output/phase2/main/det_caps.csv`、`psa_caps_summary.csv`（axis = hr0） | Results 目的 1 第 1 段（与 Fig. 2 同句） |
| Supplementary Table S5 | 效应持续与术后继续的完整表：基准、维持到术后 1 年、不衰减、术后继续（E04 × E05 计入费用），全部 HR 格点，两比较，两个阈值 | 1、2 | `output/phase2/main/scenario_caps.csv`（base、path_a_s1、path_a_s2、continue_s1） | Results 目的 1 第 2 段（持续时间） |
| Supplementary Table S6 | Fig. 3 的数值：21 个输入的下限、上限值与对应的上限 | 1 | `output/phase2/main/oneway_base.csv` | Results 目的 1（与 Fig. 3 同句） |
| Supplementary Table S7 | 一年对象患者的净收益（HR 0.95、0.90、0.85，两栏）与 N 的推算；**N 待尾崎确认，先留空**（每人值照放，乘 N 的列留空） | 1 | `output/phase2/main/cohort_value.csv`、`cohort_value_N.csv`；`input/params/cohort_N_sources.csv` | Results 目的 1 末段 |
| Supplementary Table S8 | Elmore 边界情景（术前进展后中位 26 个月；与试验第 1 至 3 年 OS 不一致）：上限与参照 ICER | 1–3 | `output/phase2/main/scenario_caps.csv`、`scenario_reference.csv`（elmore）；`output/phase1/round15/scenario_gates.csv` | Results 目的 3 的段落 |
| Supplementary Table S9 | 路径 B（pCR 提高 0 至 10 个百分点）：两比较的上限 [95% UI]、两个阈值 | 4（与 1） | `output/phase2/main/det_caps.csv`、`psa_caps_summary.csv`（axis = pcr） | Results 目的 4 的段落（与 Table 3 Panel C 同句） |

清单外、分析计划里有、尚无归宿的结果（见第 6 节 D8）：效用价值集（美、英、澳）情景、S-JP 情景的上限、S-JP 下的单因素分析（F01P 为主要项目）、参照 ICER 的单因素分析、主比较 HR 0.85 的增量费用分解（`decomp_main_hr085.csv`）。

## 5. 用语表（v1 起沿用；抄录、表、图、补充材料同名）

| 正文的名称 | 指什么 | 初出 |
|---|---|---|
| maximum affordable (program) cost | 上限 = 阈值 × ΔQALY − 除方案费用以外的 Δ费用（含运动 AE） | Table 2 题目与 ✳ 注 |
| recurrence HR（recurrence hazard ratio with exercise） | hr0：作用于术后局部区域复发与远处复发的 HR；1.00 = 无效应 | Table 1 ✳✳✳ 注 |
| base-case effect duration（effect held for 5 years） | 随机化后 5 年内保持，之后半衰期 1 年 | Table 1 |
| Effect until 1 year after surgery；No waning | 路径 A 情景①、② | Table 1 |
| medical costs avoided | 避免的医疗费用（−Δ费用，不含方案费用） | Table 2 ✳✳✳ 注 |
| Exercise added to chemotherapy plus pembrolizumab | 主比较 | Table 2 列标题 |
| Exercise added to chemotherapy alone | 次比较 | Table 2 列标题 |
| pembrolizumab added to (neoadjuvant) chemotherapy | 参照比较 | Table 3 题目 |
| CHALLENGE-based supervised program；fee-schedule-based program；remote low-cost program | E01；E02；E03 | Table 1 |
| Higher mortality after early recurrence with pembrolizumab | 早期复发后 k（外部），k = 1.307 | Table 1 |
| Japanese post-operative treatment | S-JP | Table 1 |
| Metastatic treatment costs halved；Eribulin-based later-line treatment | sc_metcost50；sc_eribulin | Table 1 |
| 95% UI | PSA 1,000 个样本的 2.5 与 97.5 百分位 | Table 2 ✳ 注 |

拼写暂用美式（randomization、program、modeled），图的称呼用「Fig.」（见 D11）。

## 6. 需要你决定的事项

- **D1 表的编号与指示相反。** 指示是 Table 2 = 目的 b（参照）、Table 3 = 主目的与 a。规约第 2.1 节要求 Results 按目的编号排列（主目的先），第 7.1 节要求表号按正文初次引用的顺序；两者合起来，主目的的表必须先于参照的表出现，所以本版为 **Table 2 = 上限（指示的 Table 3）、Table 3 = 参照（指示的 Table 2）**。若想保留指示的编号，Results 须先写参照比较（与第 2.1 节的顺序冲突）。
- **D2 Table 2 Panel A 与 Fig. 2 载有同一结果。** 规约第 7.2 节：「図と表の両方に同じ結果を載せない。図にした結果の数値は supplementary の表に置き」。本版照指示两者都放（第 13 节该项监查不通过）。选项：(a) 照现状；(b) Panel A 移到 Supplementary Table S4（S4 本来就放 Fig. 2 的数值），Table 2 只留 Panel B 至 D；(c) 保留 Panel A，Fig. 2 只留 b。我的建议是 (b)。
- **D3 金额单位。** 表图用千日元（JPY 1,000），与报告的「万日元 1 位小数」精度相同（272.6 万日元 = 2,726）。若要万日元或百万日元，改 `v1_common.fk()` 一处即可；百万日元 2 位小数会降低精度（属于舍入位数，由你定）。
- **D4 舍入。** 从原始值一次四舍五入（half up）；舍入为 0 的值不带负号（HR 1.00 行的 95% UI 上端为「0」，原始值为负）。Table 1 的 D06（原值 1,120,000.5）按 half up 显示为 1,120,001。
- **D5 指示之外加的两处。** (1) Table 2 Panel D 加了两情景下「上限 = 费用表方案」与「避免的医疗费用 = 费用表方案」的 HR：主张的「4% 至 9%」（1 − 0.958 = 4.2%，1 − 0.918 = 8.2%，1 − 0.914 = 8.6%）在别处没有表可依。另外，规约第 6.1 节要求正文的数值以同值同位出现在表中：正文若写「4% 至 9%」，表里须有降低幅度（%）的列；否则正文改写 HR（0.958 至 0.914）。请定其一。此范围只对主比较、费用表方案成立（次比较 0.966 至 0.925；CHALLENGE 型方案基准 0.948，两情景不在本表）。(2) Table 3 Panel C（目的 c）：规约第 2.1 节要求每个目的至少有一个表或图。
- **D6 Table 3 两情景栏的类别值是派生值**（线性换算，与模型合计一致）。可用；若只要模型直接输出的数，两栏的类别改为「—」，只留合计。
- **D7 S-JP 栏没有 PSA 与分解**，只有合计、ΔQALY、ICER。保留此栏，或移到补充材料。
- **D8 补充材料清单外的结果**（第 4 节末）：分析计划第 6 节列为情景的「效用价值集」「S-JP」若在 Methods 中写出，就须在 Results 报告（规约第 13 节「推定対象と宣言した量」）。建议并入一张「其他情景」补充表（与 Elmore 同表），单因素的参照 ICER 与 S-JP 部分并入 S6；或 Methods 不提这些情景。
- **D9 Table 1 与 Supplementary Table S1 的重复。** 指示「全部参数放 S1」，而第 6.1 节「同じ数値は一つの表にだけ置く」。选项：S1 全列（与 Table 1 重复约 40 个值）；或 S1 对 Table 1 已列的行只写「Table 1」，其余全列。
- **D10 暂定值出现在表图中。** E03（远程低价方案 11,260 日元，【要確認】）在 Table 1、Table 2 Panel B、Fig. 2；D02（【要確認】）在 Fig. 3。其余【要確認】行（B03、B04、B07–B10、F01P）只进入模型，不在正文表图中单独显示。
- **D11 拼写与投稿刊物。** 刊物未定，暂用美式拼写与「Fig.」，定刊后按投稿规定统一。
- **D12 「早期复发后 k（外部）」在上限上只放 S4。** model_spec 第 6 节原定所有涉及帕博利珠单抗的结果两栏并列；本版按新指示（主比较一列）处理，参照比较（Table 3）仍两栏。两栏方向一致（主比较 HR 0.85：2,726 对 2,691 千日元），Results 可写一句并引用 S4。
- **D13 段阶 1（文献）未做。** Table 1 的来源栏与 Fig. 2 的 CHALLENGE 标注是描述性名称；文献编号在段阶 1 与正文起草后加。

## 7. 交付前的检查（规约第 13 节中与表图有关的项目；全文监查在 manuscript 交付时做）

最重要的四项：
1. 版：作业树 `manuscript/` 只有 v1；无旧版、无 md 原稿、无模板。通过。
2. 表与图的正文引用：正文未写，无法检查；第 2 至 4 节已为每个表、图、补充项目定好初次引用的位置。待正文。
3. 文献的真伪、4. 文献的顺序：本步无文献。不适用。

交付前重读了规约第 6 至 8 节（表、图、体裁），据此改了两处：Table 2、3 表头左上的空格补上列名（第 6.2 节「空のセルを残さない」）；表注中「1,000 个 PSA 样本」在任何表中都没有值，于是在 Table 1 加「Uncertainty」行（第 7.2 节「表の脚注に書く数値も…」）。

从 docx 回读（`check_v1.md`；检查器先用植入违规的副本鸣响过：字体、颜色、粗体、中黑、Note、破折号、未登记数字、孤立脚注都被检出）：
- tables_v1.docx：全部文字 run 为 Times New Roman 12 pt；黑以外 0；Heading 样式 0；空单元格 0；表外粗体 0；含数字的单元格粗体 0；「・」0；以 Note 开头 0；表外的「—」0；三个 section 都是 A4 横版；脚注符号与表内或题目的上标一一对应，按 ✳、✳✳、✳✳✳、✳✳✳✳ 的顺序（Table 1 三个，Table 2、3 各四个）；抽出数字 275 个，未登记 0，登记的数值在文档中找不到的 0。
- figures_v1.docx：同上各项 0；A4 纵版；三个图注的 ✳ 一一对应；抽出数字 30 个，未登记 0。
- Word（COM）打开两个 docx 并转 PDF：tables 7 页、figures 3 页，无修复提示。
- 图：PNG 4015 像素宽、600 dpi，插入宽 169.97 mm（实际 600 dpi）；TIFF 同像素。nature-figure：`validate_figure.py` 0 fail（2 warn：字号由 rcParams 统一设定、宽度由变量给出，非问题）；`audit_pdf_text.py --min-pt 8` 三图低于 8 pt 的文字 0；`audit_figure_collisions.py` 三图 0 fail、0 warn；Fig. 2 面板对齐 PASS。
- 已知不通过：第 7.2 节「図と表に同じ結果」= Table 2 Panel A 与 Fig. 2（D2）。
- 表的版式（列宽等）按规约第 7.2 节由你处理，未调整。
