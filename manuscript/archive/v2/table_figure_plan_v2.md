# 表与图的计划 v2（执笔第 1 步，2026-10-26）

## 0. 声明

1. 开工前重读了 `Documents/ClaudeCode/WRITING_RULES.md` 第 6 至 8 节（数值、表与图、体裁）；交付前的对照见第 7 节。
2. 段阶 2（表与图）的第二版。段阶 1（文献）仍未做（D13：下一步处理）。
3. 底本：v1 的交付物（tables_v1.docx、figures_v1.docx、table_figure_plan_v1.md、numbers_ledger_v1.md）与 `manuscript/code/` 的生成代码。v1 已移到 `manuscript/archive/v1/`；作业树 `manuscript/` 下只有 v2、archive 与 code。代码去掉了文件名里的版本号（`make_tables.py`、`make_figures.py`、`make_ledger.py`、`common.py`，版本由 `common.VER` 决定），改后重新生成；新增 `compare_versions.py`（与前版逐段对照）。

产物（`manuscript/v2/`）：tables_v2.docx、figures_v2.docx、本文件、numbers_ledger_v2.md；辅助：check_v2.md（回读检查）、diff_v1_v2.md（与 v1 的逐段对照）、MANIFEST_v2.md、figures/。

## 1. 目的的编号（与 v1 相同）

| 编号 | 内容 |
|---|---|
| 目的 1（主） | 日本公共医疗支付方的立场，含帕博利珠单抗的术前化疗加结构化运动方案时，每人可负担的方案费用上限如何随运动对复发风险的效应大小（复发 HR）与持续时间变化（阈值 500 万日元/QALY） |
| 目的 2（副 a） | 同一上限，加在单用化疗上 |
| 目的 3（副 b） | 帕博利珠单抗对单用化疗的费用效果（参照） |
| 目的 4（副 c） | 运动要达到与帕博利珠单抗同等 QALY 增量所需的效应 |

主张与表图（v2）：

| 主张的部分 | 表或图的位置 |
|---|---|
| 费用效果取决于效应的大小 | Fig. 2（数值在 Supplementary Table S4） |
| 取决于效应的持续时间 | Table 2 Panel B |
| 不取决于方案价格（上限 = 方案费用的 HR 贴近 1，降低幅度约 1%） | Table 2 Panel A 第 1 行、Panel C、Fig. 2b |
| 复发风险降低几个百分点即可收回成本 | Table 2 Panel A「Medical costs avoided … fee-schedule-based program」0.958 (4.2) 与 Panel C 两情景 0.918 (8.2)、0.914 (8.6)；范围 4.2% 至 8.6% 只对主比较与 E02 成立（表注 ✳✳✳） |
| 运动的基准 500 万日元，帕博利珠单抗另示 750 万日元 | Table 2 题目；Table 3 Panel B |

## 2. 正文表

### Table 1. Key model inputs（目的 1–4；Methods 引用）

与 v1 相同，只加一条效用的脚注：效用组的标签加 ✳✳✳，脚注写明基准用 KEYNOTE-522 的 EQ-5D（德国价值集），理由是没有找到把日本价值集用于 KEYNOTE-522 并报告标准误的数据；日本人群的数值作为情景，见 Supplementary Table S8。原 ✳✳✳（复发 HR 的定义）按出现顺序改为 ✳✳✳✳。

### Table 2. 分界点与情景（目的 1、2）

- 原 Panel A（HR 0.70 至 1.00 的上限）移到 Supplementary Table S4（D2）。题目改为「Recurrence hazard ratios at which exercise breaks even, and the maximum affordable cost …」，首列表头改为「Break-even point or scenario」。
- Panel A：基准情形的分界点。上限 = 费用表方案（E02）；避免的医疗费用 = E01、E02、E03。来源 `output/phase2/main/sc_base_crossings.csv`。
- Panel B：效应持续。首行「Base case, recurrence HR 0.85」（2,726 [2,223, 3,040]；3,443 [2,881, 3,785]，来源 `det_caps.csv`、`psa_caps_summary.csv`），其下两种替代持续（`scenario_caps.csv`，只有确定性值）。
- Panel C：转移复发治疗费。首行同上的基准行；两情景各三行（HR 0.85 的上限 [95% UI]；上限 = E02 的 HR；避免的医疗费用 = E02 的 HR）。来源 `sc_metcost50_*`、`sc_eribulin_*`。
- 所有分界点格写成「HR (降低幅度)」，如「0.958 (4.2)」，降低幅度 = 100 × (1 − HR)，由原始 HR 计算后保留 1 位小数（D5）。Panel A 的标题行与 Panel C 的行名写明「(reduction in recurrence hazard, %)」；脚注 ✳✳ 也写明。
- 脚注 ✳✳✳ 写明：避免的医疗费用 = 方案费用所需的降低幅度 4.2% 至 8.6%（基准与两个转移复发治疗费情景）只对主比较与费用表方案（E02）成立。指示原文为「4% 至 9%」；表注里的数值须以同值出现在表中（规约第 7.2 节），所以写成表中的 4.2 与 8.6（由代码取三格的最小值与最大值）。正文若要写「4% 至 9%」，按规约第 6.1 节也应写成 4.2% 至 8.6%。
- 正文引用处：Results 目的 1（Panel A、Fig. 2、S4；Panel B、C）与目的 2（次比较列）。

### Table 3. 帕博利珠单抗对单用化疗（目的 3、4）

与 v1 相同（D6 派生的类别值与脚注 ✳✳✳ 保留；D7 S-JP 栏保留）。唯一的改动：脚注 ✳✳✳✳ 原写「Table 2 (recurrence HR 0.70 to 1.00)」，HR 网格已移到 S4，改为「recurrence HR 0.70 to 1.00 (Supplementary Table S4)」（D2 的连带改动）。

## 3. 正文图

与 v1 相同（PNG 与 TIFF 与 v1 逐字节相同）。Fig. 2 的图注仍写「数值见 Supplementary Table S4」。生成代码中只改了登记说明的文字（0.70、1.00、0.95、0.85 的出处由「Table 2」改为 Table 1、S4 与 Table 2 的基准行）。

## 4. 补充材料清单（编号按计划的正文初次引用顺序）

计划的初次引用顺序：Methods（Study background）S1 → Supplementary Methods S1、Fig. S1、Table S2 → Methods（Statistical analysis 末）S3 → Results 目的 1：S4 → S5 → S6 → S7 → S8 → 目的 4：S9。编号集中在 `manuscript/code/common.py` 的 SUPP。

| 编号 | 内容 | 目的 | 数据来源（文件与位置） | 正文初次引用处 |
|---|---|---|---|---|
| Supplementary Table S1 | 完整参数表：基本值、范围（下限、上限）、分布（类型与参数）、来源与位置、适用组、范围的规则（±25%、片側対称、薬価固定、0例）、暂定标记；生存参数与情景值（D9） | 全部 | `input/params/parameters_v10.xlsx`（パラメータ、シナリオ、計算根拠_原）；`data/params_dist.csv`；`output/phase1/calibration.csv`、`data/pcr_counts.csv`、`data/kn522_final_7y.csv`、`output/phase1/ae_deaths.csv`、`output/phase1/round14/kext_derivation.csv`；日本人群效用 `input/params/sources_utility/utilities_scenario_jp.csv` | Methods, Study background（与 Table 1 同段） |
| Supplementary Methods S1 | 生存模型的构建与验证 | 全部 | `docs/model_spec.md` 第 1 节；`output/phase1/phase1_report.md`「第1阶段最终状态」与第 19 节；`docs/acceptance_rule_round15.md` | Methods, Study background |
| Supplementary Fig. S1 | 模型 OS、EFS 对重建 KM 与最终分析 7 年值 | 全部 | `output/phase1/round15/base/calibration_curves.csv`、`calibration_gate.csv`、`calibration_final7y.csv`；`output/phase1/engine_curves.csv`、`data/ipd/` | Methods, Study background |
| Supplementary Table S2 | 验证的数值（门槛 a、b、c；bootstrap 的 OS、EFS） | 全部 | `output/phase1/round15/base/calibration_gate.csv`、`calibration_gate_rmst.csv`、`calibration_final7y.csv`；`output/phase1/bootstrap_summary.csv` | Methods, Study background |
| Supplementary Table S3 | CHEERS 2022 清单 | 全部 | 正文写成后填 | Methods, Statistical analysis 末句 |
| Supplementary Table S4 | Fig. 2 的数值，含 v1 Table 2 Panel A：HR 0.700 至 1.000（每 0.025），500 万与 750 万日元，主比较（基准、早期复发后 k 外部）与次比较，上限 [95% UI] 与「上限 ≥ 费用表方案费用」的概率 | 1、2 | `output/phase2/main/det_caps.csv`、`psa_caps_summary.csv`（axis = hr0） | Results 目的 1 第 1 段（与 Fig. 2 同句） |
| Supplementary Table S5 | 效应持续与术后继续的完整表 | 1、2 | `output/phase2/main/scenario_caps.csv`（base、path_a_s1、path_a_s2、continue_s1） | Results 目的 1（Table 2 Panel B 同段） |
| Supplementary Table S6 | Fig. 3 的数值 | 1 | `output/phase2/main/oneway_base.csv` | Results 目的 1（与 Fig. 3 同句） |
| Supplementary Table S7 | 一年对象患者的净收益（“如果有效”时的条件值）。主计算：N = 3,451（2024 年 TNBC〔M0〕II、III 期术前化疗例），其中术前用帕博利珠单抗的 2,294 人按主比较、其余 1,157 人按次比较；敏感性：N = 2,900 与 4,000（帕博利珠单抗比例保持 2,294/3,451，两部分按比例拆分，非整数）。HR 0.95、0.90、0.85，基准与早期复发后 k（外部）两栏，每人净收益（主、次比较）与合计 [95% UI]。来源写「Japanese Breast Cancer Society, National Breast Cancer Registry Report No. 55 (cases diagnosed in 2024, final version)」（日本乳癌学会 全国乳がん患者登録調査報告 第55号〔2024年次症例、確定版〕） | 1 | `output/phase2/main/cohort_value_jbcs2024.csv`（setting = main、sens_2023、sens_upper）；`input/params/cohort_N_jbcs2024.csv`（N 与内訳）。旧的 `cohort_value.csv`（N = 1,719）不用 | Results 目的 1 末段 |
| Supplementary Table S8 | 其他情景（D8）：效用值四个情景（日本人群、美国、英国、澳大利亚的价值集）与 Elmore 边界情景。列：主比较与次比较的 HR 0.85 上限、上限 = E02 的 HR、参照比较的 ICER。日本人群一行放最前；脚注：日本人群的来源（无事件 0.89 = Iwatani 2021，EQ-5D-5L 日本价值集，治疗中与治疗后同值；远处复发与术前进展 0.742 = Shiroiwa 2017 SELECT BC 紫杉类组），局部区域复发与 3 级以上 AE 的效用下降没有日本数值，沿用基准。早期复发后 k（外部）的上限仍在 S4 | 1–3 | 美、英、澳与 Elmore：`output/phase2/main/scenario_caps.csv`（utility_us、utility_uk、utility_au、elmore；hr0 = 0.85 的 cap_500）、`scenario_reference.csv`（icer）、`scenario_utility_sets.csv`；日本人群：`sc_util_jp_*`（**截至 2026-10-26 17:01 不存在**，见第 6 节 N1）；日本人群的值：`input/params/sources_utility/utilities_scenario_jp.csv` | Results 目的 1 末段（S7 之后） |
| Supplementary Table S9 | 路径 B（pCR 提高 0 至 10 个百分点） | 4（与 1） | `output/phase2/main/det_caps.csv`、`psa_caps_summary.csv`（axis = pcr） | Results 目的 4（与 Table 3 Panel C 同句） |

仍未归宿的结果：S-JP 情景的上限与 S-JP 下的单因素分析（F01P）、参照 ICER 的单因素分析、主比较 HR 0.85 的增量费用分解（`decomp_main_hr085.csv`）。v1 的 D8 建议并入 S6 或「其他情景」；本次决定只把效用与 Elmore 放进 S8，这些仍待定（第 6 节 N3）。

## 5. 用语表（v1 起沿用，本版新增两项）

| 正文的名称 | 指什么 | 初出 |
|---|---|---|
| maximum affordable (program) cost | 上限 = 阈值 × ΔQALY − 除方案费用以外的 Δ费用（含运动 AE） | Table 2 ✳ 注 |
| recurrence HR | hr0：作用于术后局部区域复发与远处复发的 HR；1.00 = 无效应 | Table 1 ✳✳✳✳ 注 |
| reduction in recurrence hazard (%)（新） | 100 × (1 − recurrence HR) | Table 2 Panel A 标题行与 ✳✳ 注 |
| break-even（新） | 两种分界点的总称：上限 = 方案费用；避免的医疗费用 = 方案费用 | Table 2 题目与首列表头 |
| base-case effect duration；Effect until 1 year after surgery；No waning | 路径 A 的基准与情景①、② | Table 1 |
| medical costs avoided | 避免的医疗费用（−Δ费用，不含方案费用） | Table 2 ✳✳✳ 注 |
| Exercise added to chemotherapy plus pembrolizumab；Exercise added to chemotherapy alone | 主比较；次比较 | Table 2 列标题 |
| CHALLENGE-based supervised program；fee-schedule-based program；remote low-cost program | E01；E02；E03 | Table 1 |
| Higher mortality after early recurrence with pembrolizumab；Japanese post-operative treatment；Metastatic treatment costs halved；Eribulin-based later-line treatment | 早期复发后 k（外部）；S-JP；sc_metcost50；sc_eribulin | Table 1 |
| 95% UI | PSA 1,000 个样本的 2.5 与 97.5 百分位 | Table 1 Uncertainty 行 |

拼写暂用美式（D11），图的称呼「Fig.」。

## 6. 决定与审核记录

### 6.1 v1 的待决事项（2026-10-26 审阅）

| 项 | 决定 | 本版的处理 |
|---|---|---|
| D1 | 表号照 v1 | 不变 |
| D2 | (b) | 原 Panel A → S4；Table 2 重编为 A、B、C；B、C 各加基准行 |
| D3 | 千日元 | 不变 |
| D4 | 照 v1 | 不变（half up；舍入为 0 不带负号） |
| D5 | 分界点格写「HR (降低幅度 %)」 | 全部 16 个分界点格；脚注写明范围的适用条件 |
| D6 | 采用派生的类别值 | 不变，脚注 ✳✳✳ 保留 |
| D7 | S-JP 栏保留 | 不变 |
| D8 | 新设「其他情景」补充表 | S8（第 4 节）；日本人群一行的数据待生成（N1） |
| D9 | S1 为完整参数表 | 第 4 节；有意的例外 E2 |
| D10 | 照 v1；对照表标暂定 | numbers_ledger_v2.md 加「暂定」列与「暂定值」小节（E03 的 7 项、D02 的 Fig. 3 一行） |
| D11 | 美式拼写 | 不变 |
| D12 | 照 v1 | 不变 |
| D13 | 文献下一步 | 不变 |

### 6.2 有意的例外（审核记录）

- **E1　Table 2 Panel B、C 的基准行与 Supplementary Table S4 重复**（2,726 [2,223, 3,040]；3,443 [2,881, 3,785]），且在 Table 2 内出现两次（B、C 各一）。违反规约第 6.1 节「同じ数値は一つの表にだけ置く」。理由（2026-10-26 审阅的决定）：情景值必须与基准值在同一表内比较。表注 ✳✳✳✳ 写明该行重复 S4 的基准估计。
- **E2　Supplementary Table S1 与 Table 1 的基本值重复。** 违反同一节。理由（同日决定）：S1 增加了 Table 1 没有的范围与分布，且 CHEERS 2022 要求完整的参数表。
- 两项以外，正文表之间、表与图之间的重复为 0（v1 的 Table 2 Panel A 与 Fig. 2 的重复已由 D2 消除）。

### 6.3 新出现的待办

- **N1　日本人群效用情景的结果（`sc_util_jp_*`）不存在。** 截至 2026-10-26 17:01，`output/phase2/main/` 中没有以 sc_util_jp 开头的文件，`scenario_caps.csv`、`scenario_reference.csv` 也只有 utility_us、utility_uk、utility_au（与已提交的 1a33658 相同）。S8 的日本人群一行待该计算完成后取数；本步只定规格，不重算模型。
- **N2　S8 要的「上限 = E02 的 HR」对效用价值集与 Elmore 情景不在现有输出中**（`sc_*_crossings.csv` 只有转移复发治疗费的两个情景与基准；其余情景只有 HR 格点上的上限）。选项：(a) 在生成 sc_util_jp 的同一次计算中，对 S8 的全部情景用 uniroot 求交点（与 `sc_base_crossings.csv` 同法）；(b) 由 0.025 格点线性插值（报告第 1.7 节用过此法，与 uniroot 的差 ≤ 0.00003），在表注中写明。建议 (a)。
- **N3　S-JP 的上限与单因素分析、参照 ICER 的单因素分析、主比较的费用分解**仍无归宿（第 4 节末）。若 Methods 写到这些分析，就须在 Results 报告。
- **N4　S7 的出处原表尚未收到**（`cohort_N_jbcs2024.csv` 备注：会员限定资料，原表待尾崎提供）。

## 7. 交付前的检查（重跑 v1 的全部检查）

最重要的四项：
1. 版：`manuscript/` 下只有 v2、archive（v1）与 code；v2 内只有本版文件。通过。
2. 表与图的正文引用：正文未写；第 2 至 4 节为每个表、图、补充项目定了初次引用处。待正文。
3. 文献的真伪、4. 文献的顺序：本步无文献。不适用。

从 docx 回读（`check_v2.md`）：
- tables_v2.docx：全部文字 run 为 Times New Roman 12 pt；黑以外 0；Heading 样式 0；空单元格 0；表外粗体 0；含数字的单元格粗体 0；「・」0；以 Note 开头 0；表外的「—」0；三个 section 都是 A4 横版；脚注符号与表内或题目的上标一一对应且按顺序（Table 1 四个，Table 2 四个，Table 3 四个）；抽出数字 260 个，未登记 0，登记的数值在文档中找不到的 0。
- figures_v2.docx：同上各项 0；A4 纵版；三个图注的 ✳ 一一对应；抽出数字 30 个，未登记 0。
- 图：PNG 4015 像素宽、600 dpi，插入宽 169.97 mm（实际 600 dpi）；`audit_pdf_text.py --min-pt 8` 三图低于 8 pt 的文字 0；`audit_figure_collisions.py` 三图 0 fail、0 warn；Fig. 2 面板对齐 PASS；`validate_figure.py` 0 fail（2 warn，同 v1）。
- Word（COM）打开并转 PDF：tables 8 页、figures 3 页，无修复提示。
- 规约第 7.2 节「図と表に同じ結果」：v1 的不通过项已消除。第 6.1 节的重复只有第 6.2 节的两项有意例外。
- 表的版式（列宽等）由你处理，未调整。

## 8. 与 v1 的逐段对照（`diff_v1_v2.md`）

tables：v1 302 项、v2 287 项（表外段落与表内单元格各为一项），不同的块 9 个。figures：9 项全部相同，嵌入的 3 张图片 sha256 相同；PNG、TIFF 与 v1 逐字节相同，SVG、PDF 只差生成时刻（SVG 另有随机的 clip-path 编号，归一化后无差）。

| 块 | 内容 | 对应的决定 |
|---|---|---|
| 1 | Table 1「Utilities」加 ✳✳✳ | 第 3 节（效用脚注） |
| 2 | Table 1「Recurrence HR」的 ✳✳✳ → ✳✳✳✳ | 第 3 节的连带改动（脚注按出现顺序编号） |
| 3 | Table 1 新增效用脚注、复发 HR 脚注改号；Table 2 题目与首列表头 | 第 3 节；D2 |
| 4 | Table 2 原 Panel A 的网格行删除；新 Panel A（分界点，带降低幅度）；Panel B 标题与基准行 | D2、D5 |
| 5 | 原 Panel A 其余网格行与原 Panel B（无降低幅度的分界点）删除 | D2（网格移 S4）；D5（同一分界点改为带降低幅度的格，在块 4） |
| 6 | 原 Panel D → Panel C，加基准行 | D2 |
| 7、8 | Panel C 的分界点格加降低幅度、行名加「(reduction in recurrence hazard, %)」与 ✳✳✳；Table 2 的四条脚注改写（「Cells with a bracket」、降低幅度的定义、4.2% 至 8.6% 的适用条件、基准行重复 S4） | D5；D2 |
| 9 | Table 3 脚注 ✳✳✳✳ 的「Table 2」→「Supplementary Table S4」 | D2 的连带改动 |

意图之外的变化：0。Table 1 除块 1 至 3 之外、Table 3 除块 9 之外、Table 2 的数值（各格的估计值与区间、分界点的 HR）都与 v1 相同；新增的数值只有 16 个降低幅度与两行基准行（重复值，E1）。
