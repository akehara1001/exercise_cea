# 表与图的计划 v3（执笔第 2 步：补充表与 Results，2026-10-26）

## 0. 声明与底本

1. 开工时全文重读了 `Documents/ClaudeCode/WRITING_RULES.md`；写 Results 前读了 ARS 的必读文件（academic-paper/SKILL.md 的 Anti-Patterns 与 Quality Standards、agents/draft_writer_agent.md 的写作步骤与 Claim-Strength、references/writing_quality_check.md、academic_writing_style.md、writing_judgment_framework.md、intro_title_rhetoric_guide.md、abstract_writing_guide.md）。交付前按第 4 节 Results、第 6 至 8 节、第 10 节、第 13 节逐项自查（第 7 节）。
2. 段阶：段阶 2（补齐补充表）与段阶 3 的一部分（只写 Results）。段阶 1（文献）仍未做；ARS academic-paper 的 full 模式没有跑（按指示只写 Results 一节；ARS 的写作规则以上述文件为准逐句自查）。
3. 底本：`manuscript/archive/v2/`（tables_v2.docx 4c81fa23、figures_v2.docx 1368dc38、table_figure_plan_v2.md 78272f81、numbers_ledger_v2.md 01e5894c）与 `manuscript/code/`。v2 已移入 archive；作业树 `manuscript/` 下只有 v3、archive（v1、v2）与 code。
4. 新来源：`output/phase2/main/sc_util_jp_det_caps.csv`、`sc_util_jp_det_reference.csv`、`sc_crossings.csv`（并行会话的计划第 10 节，提交 e513b7d；我读取的文件与提交内容逐字相同），以及已有的 `decomp_main_hr085.csv`、`oneway_base.csv`。第 1 阶段的生存参数由 `manuscript/code/extract_engine_params.R` 从 `data/fits/engine_params.rds` 只读导出（不计算）。

产物（`manuscript/v3/`）：tables_v3.docx、figures_v3.docx、**supplement_v3.docx（新）**、**results_v3.docx（新）**、本文件、numbers_ledger_v3.md；辅助：check_v3.md、diff_v2_v3.md、MANIFEST_v3.md、figures/（新增 figS1、figS2）。代码：`make_tables.py`、`make_figures.py`（新增补充图）、`make_supplement.py`（新）、`make_results.py`（新，只用于 v3 一次；以后的版本直接改 docx）、`make_ledger.py`（扩展）、`compare_versions.py`、`extract_engine_params.R`（新）、`param_names.py`（新）。

## 1. 目的与 Results 各段的对应（规约第 2.1 节）

| 目的 | Results 的段落（results_v3.docx） | 开头点名的表或图 |
|---|---|---|
| 目的 1（主）：效应大小 | P1 | Fig. 2a；Table 2 panel A；Supplementary Table S4 |
| 目的 1：医疗费用下降的内訳 | P2 | Supplementary Table S5 |
| 目的 1：效应持续时间 | P3 | Table 2 panel B；Supplementary Table S6 |
| 目的 1：转移复发治疗费与 4.2% 至 8.6% | P4 | Table 2 panel C |
| 目的 1：一年对象患者的净收益 | P5 | Supplementary Table S7 |
| 目的 2（副 a）：次比较 | P6 | Fig. 2、Table 2 |
| 目的 3（副 b）：帕博利珠单抗的参照 | P7、P8 | Table 3（panel A、B；各情景栏） |
| 目的 4（副 c）：同一把尺子 | P9 | Table 3 panel C；Supplementary Table S8 |
| 末段：不确定性与其他情景（规约第 4 节：稳健性的记述放在 Results 末尾一段） | P10 | Fig. 3、Supplementary Table S9、Supplementary Fig. S2、Supplementary Table S10 |

Results 不写方法、不写解释与位置、不设小标题；每段以表或图开头；每句都带表或图的引用；每个数字都能对应到所引表格的某一格（numbers_ledger_v3.md 第 1 节逐句列出）。复发风险降低幅度写 4.2% 至 8.6%，并写明只对主比较与按诊疗报酬计算的方案成立（P4 末句）。

## 2. 正文表（v3 的改动只有补充编号）

- Table 1：✳✳✳ 注的「Supplementary Table S8」→「S10」（其他情景的新编号）。
- Table 2：无改动（✳✳✳✳ 注仍指 S4）。
- Table 3：✳✳✳✳ 注的路径 B 由「S9」→「S8」。
- 数值：与 v2 完全相同（diff_v2_v3.md：tables 只有 2 个块，都是编号）。

## 3. 图

- Fig. 1–3：PNG 与 TIFF 与 v2 逐字节相同。Fig. 3 的图注中「Supplementary Table S6」→「S9」（单因素数值表的新编号）。作图代码把龙卷风图改成通用函数（Fig. 3 与 Supplementary Fig. S2 共用），改后 Fig. 3 的像素不变。
- 新增 Supplementary Fig. S1（验证）：a 为 OS，b 为 EFS。细阶梯线 = 由 2024 年报告的曲线重建个体数据的 Kaplan–Meier（带 95% CI 的灰带），粗灰线 = 模型，点与误差棒 = 最终分析的 7 年值与 95% CI。OS 的 KM 与模型取自 `output/phase1/calibration_curves.csv`；EFS 的 KM 由 `data/ipd/K24_F2A_EFS_*.csv` 计算（log 变换的 Greenwood 95% CI，与 R survfit 的默认相同），模型取自 `output/phase1/engine_curves.csv`。图的数值在 Supplementary Table S2。
- 新增 Supplementary Fig. S2（参照 ICER 的龙卷风图，形式同 Fig. 3，范围为假定值的行加 [±25%]、[mirrored]、[price]）：改变 ICER 的输入共 59 个，图中画范围最宽的 20 个（沿用 `R/23_phase2b_report.R` 的 tornado(top = 20)），59 个全部列在 Supplementary Table S9。
- 规格：全部 170 mm 宽、Arial、≥ 8 pt、600 dpi、黑白可分；nature-figure 的检查见第 7 节。

## 4. 补充材料（supplement_v3.docx；编号按 Results 的初次引用顺序重排，全稿写完后再按实际顺序确认）

v3 的编号由 Methods（S1、Supplementary Methods S1、Fig. S1、S2、S3）与本版 Results 的初次引用顺序决定：

| v3 | 内容 | v2 的编号 | Results 中的初次引用 |
|---|---|---|---|
| Supplementary Table S1 | 完整参数表：A 生存与模型结构（基本值与 bootstrap 2.5 至 97.5 百分位）；B 81 个费用、AE、效用、运动与术后治疗的输入（基本值、范围、分布及其参数、出处） | S1 | （Methods） |
| Supplementary Fig. S1 | 验证图（OS、EFS 对重建 KM 与最终分析） | Fig. S1 | （Methods） |
| Supplementary Table S2 | 验证的数值：A 第 1 至 5 年 OS、B 5 年 RMST 两臂差、C 7 年 OS 与 EFS（含 pCR 分层 OS）、D 10 与 20 年的外推 | S2 | （Methods） |
| Supplementary Table S3 | CHEERS 2022 清单 | S3 | （Methods；本版未作，与 Methods 一同写） |
| Supplementary Methods S1 | 生存模型的构建与验证 | 同 | （Methods；本版未作） |
| Supplementary Table S4 | Fig. 2 的数值（HR 0.700 至 1.000，500 万与 750 万日元，主比较基准与早期复发后 k、次比较，[95% UI] 与「高于按诊疗报酬方案费用」的概率） | S4 | P1 |
| Supplementary Table S5 | 主比较 HR 0.85 的增量费用按类别（新，N3 之一） | — | P2 |
| Supplementary Table S6 | 效应持续与术后继续的完整表（基准见 S4） | S5 | P3 |
| Supplementary Table S7 | 一年对象患者的净收益（照 v2：JBCS 第 55 号，3,451 人 = 2,294 + 1,157；敏感性 2,900、4,000） | S7 | P5 |
| Supplementary Table S8 | 路径 B（pCR 提高 0 至 10 个百分点） | S9 | P9 |
| Supplementary Table S9 | 单因素敏感性分析的数值：改变主比较上限或参照 ICER 的 64 个输入（Fig. 3 与 Fig. S2 的数据；不改变的格为「—」） | S6 | P10 |
| Supplementary Fig. S2 | 参照 ICER 的龙卷风图（新，N3 之一） | — | P10 |
| Supplementary Table S10 | 其他情景（N1、N2）：日本人群效用（最前）、美、英、澳价值集、Elmore、S-JP；主比较与次比较的 HR 0.85 上限、上限 = E02 的 HR、避免的医疗费用 = E02 的 HR（「0.958 (4.2)」形式），以及参照 ICER | S8 | P10 |

S7：尾崎的原表到了以后只补出处存档，不改数值（照指示）。

## 5. 用语表（v2 沿用；本版新增）

| 名称 | 指什么 | 初出 |
|---|---|---|
| maximum affordable cost | 上限 | Results P1；Table 2 ✳ 注 |
| recurrence hazard ratio (HR) | hr0 | Results P1 |
| 95% uncertainty interval (UI) | PSA 1,000 样本的 2.5 与 97.5 百分位 | Results P1；Table 2 ✳ 注 |
| medical costs avoided | −Δ费用（不含方案费用） | Results P1 |
| incremental medical costs other than the program cost（新） | 与 S5「Total without the program cost」同一量；正文用负值与表一致（−702） | Results P2 |
| Utility values from Japanese populations（新） | 日本人群效用情景（U01、U02 = 0.89，U04 = 0.742，其余沿用基准） | Supplementary Table S10 |
| Longer survival after progression during neoadjuvant therapy（新） | Elmore 边界情景 | Supplementary Table S10 |

金额的写法：正文写「JPY 2,726 thousand」，与表中千日元的显示值同值同位；负的增量费用照表写「JPY −702 thousand」。

## 6. 决定、例外与待决

### 6.1 本版照指示处理的事项
- N1、N2：S10 照规格作成；日本人群一行在最前；分界点与 Table 2 同法（`sc_crossings.csv` 的 uniroot 解；脚本核对其基准行与 `sc_base_crossings.csv` 一致）。
- N3：主比较 HR 0.85 的费用分解 = 新 S5；参照 ICER 的单因素 = 新 Supplementary Fig. S2。
- 补充编号暂定：已按本版 Results 的初次引用顺序重排（上表），全稿写完后再按实际顺序确认。

### 6.2 有意的例外（审核记录）

- E1（已决）Table 2 panel B、C 的基准行与 S4 重复。
- E2（已决）S1 与 Table 1 的基本值重复（check_v3.md：同一来源格 26 个）。
- **E3（新，待确认）S6 与 Table 2 panel B 重复 4 格**：S6 是效应持续的完整网格，其 HR 0.850 行的两种替代持续（主、次比较）与 Table 2 panel B 相同。理由同 E1（完整网格与面板内比较各需其值）。另一选项：S6 去掉 HR 0.850 行（网格出现空行）。
- **E4（新，待确认）S10 的 S-JP 参照 ICER 与 Table 3 的 S-JP 栏重复 1 格**（3,044）：S10 的规格要求列出参照 ICER。另一选项：S10 的 S-JP 一行的 ICER 写「Table 3」。
- check_v3.md 的自动检测（同一来源格出现在两张表中）只发现上述四类，没有其他重复。

### 6.3 新的待决
- **N5** Supplementary Fig. S2 只画 59 个中的 20 个（沿用分析报告的规则）；要全部画出则需一整页的高度（约 59 行）。
- **N6** S1 与 S9 的出处栏：个人通信不写姓名（写「Clinical expert (personal communication, October 2026)」），两家医院的费用概算写为「Published cost estimates of two Japanese hospitals」。是否写出姓名与医院名由你与尾崎定。
- **N7** S1 的数字位数：按单位统一（日元整数；效用与每人件数 3 位；HR 与月数 2 位；比例 5 位；分布参数 4 位有效数字；生存参数与 bootstrap 范围 4 位有效数字）。规约第 6.2 节要求「表ごとに桁を揃える」，S1 混有多种单位，无法全表一致；如需改，在 `make_supplement.py` 的 `fval()` 与 `sig4()` 一处改。
- **N8** S1 与 S9 的出处栏写的是完整的书目（著者、刊名、卷页、DOI）；文献编号在段阶 1 之后替换。
- **N9** Supplementary Methods S1 与 Table S3（CHEERS）随 Methods 一起写；本版 supplement 中没有这两项。
- E03、D02、F01P（S-JP）的暂定值在 numbers_ledger_v3.md 第 6 节标出。

## 7. 检查（重跑 v1、v2 的全部检查并加 Results 的检查；check_v3.md）

最重要的四项：
1. 版：`manuscript/` 下只有 v3、archive（v1、v2）、code；v3 内只有本版文件。通过。
2. 表与图的引用：Results 中 Table 2、3，Fig. 2、3，Supplementary Table S4 至 S10，Supplementary Fig. S2 都在地の文中初次引用，顺序为 Fig. 2 → Table 2 → S4 → S5 → S6 → S7 → Table 3 → S8 → Fig. 3 → S9 → Fig. S2 → S10（各系列内递增）。Table 1、Fig. 1、S1 至 S3、Fig. S1 由 Methods 引用（未写），这一项待全稿。
3、4. 文献：本步无文献，不适用。

docx 回读（4 个文件，走查的段落与单元格数见 check_v3.md）：
- 全部文字 run 为 Times New Roman 12 pt；黑以外 0；Heading 样式 0；空单元格 0；表外粗体 0（Results 的节标题除外）；含数字的单元格粗体 0；「・」0；以 Note 开头 0；表外「—」0。
- 横纵：tables 全横版；figures 全纵版；supplement 表为横版、两张补充图为纵版（11 节与预期顺序一致）；results 纵版。
- 脚注符号：Table 1–3、Fig. 1–3、S1、S2、S4–S10、Fig. S1–S2 全部一一对应且按顺序。
- 数字：tables 260 个、figures 30 个、supplement 2,328 个，未登记 0；登记的数值都在文档中出现。
- Results：10 段 43 句 846 词；双倍行距 11/11 段；行号已设；禁用语、前置套话、自我说明、推测语（may、appear、suggest）、方法句、裸时间词、因果语、破折号、连接词连用都为 0；超过 30 词的句 0（最长 30）；超过 150 词的段 0（最长 134）；每段以表或图开头 10/10；无表图引用的句 0；80 个数字全部是所引表格中的显示值；ARS check_acronyms.py（body）coverage complete、No findings（JPY、ICER、QALY 以 --allow 列为标准缩写，因为其展开形式脚本按首字母无法匹配）。
- 新检查的鸣响：在 Results 副本中植入 robust、破折号、may、appeared、Moreover/Furthermore、无引用句、不在表中的数字 1,234、单倍行距，全部被检出。
- 图：Fig. 1–3、Fig. S1–S2 都是 4015 像素宽、600 dpi，插入后实际 600 dpi；字号下限 8 pt 检查 5 张都为 0 个低于；碰撞检查 5 张 0 fail 0 warn；Fig. 2 与 Fig. S1 面板对齐 PASS。
- Word（COM）打开 4 个 docx 并转 PDF：tables 8 页、figures 3 页、supplement 37 页、results 3 页，无修复提示。
- 规约第 6.1 节的重复：只有 E1 至 E4。

## 8. 与 v2 的逐段对照（diff_v2_v3.md）

| 文件 | 不同的块 | 内容 | 对应 |
|---|---|---|---|
| tables | 2 | Table 1 ✳✳✳ 注 S8→S10；Table 3 ✳✳✳✳ 注 S9→S8 | 补充编号重排（6.1） |
| figures | 1 | Fig. 3 图注 S6→S9 | 补充编号重排（6.1） |
| supplement、results | — | 本版新建 | 指示第 1、2 节 |
| 图文件 | — | Fig. 1–3 的 PNG、TIFF 与 v2 逐字节相同；figS1、figS2 新建 | — |

意图之外的变化：0。Table 1–3 与 Fig. 1–3 的数值与 v2 完全相同。
