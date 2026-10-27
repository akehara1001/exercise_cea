# 表与图的计划 v4（执笔第 2 步 v4：S10 的 Elmore 行与 Results 末段，2026-10-26）

## 0. 声明与底本

1. 规约：开工时读了 `Documents/ClaudeCode/WRITING_RULES.md` 第 1.2、1.6 节与第 4 节 Results；交付前从头到尾重读了全文（第 14 节），第 13 节的逐项点检见第 9 节。ARS：重读了 academic-paper/SKILL.md 的 Anti-Patterns 与 Quality Standards、agents/draft_writer_agent.md 的 Step 2、Step 3 与 Claim-Strength Ladder、references/writing_quality_check.md（A 至 F）、writing_judgment_framework.md；改写的段落（Results P10）按第 1.6 节逐项诊断（第 7 节）。academic_writing_style.md、intro_title_rhetoric_guide.md、abstract_writing_guide.md 在 v3 时读过，本版没有重读（本版只改 Results 的一段与一条表注）。
2. 段阶：段阶 2 与段阶 3 的一部分（Results），对 v3 的补充修改。段阶 1（文献）仍未做。
3. 底本：`manuscript/archive/v3/`（tables_v3.docx f11931ca、figures_v3.docx 347aa2d8、supplement_v3.docx 70d53ddf、results_v3.docx ebb8a734、table_figure_plan_v3.md c2a72388、numbers_ledger_v3.md 6936964c）与 `manuscript/code/`。v3 已移入 archive；作业树 `manuscript/` 下只有 v4、archive（v1、v2、v3）与 code。
4. 指示：「v4 的补充：S10 的 Elmore 行」（2026-10-26）。本版没有其他审阅决定；E3、E4、N5 至 N9 仍待决（第 6 节）。
5. 做法：表、图与补充材料照 v3 用同一套生成代码重新生成（v3 指示「同一套生成代码」）；Results 按规约第 1.2 节规则 2 不再用 `make_results.py` 生成，由新脚本 `edit_results.py` 直接编辑 `archive/v3/results_v3.docx`，只替换 P10 第 5 句、加入一句，其余段落一字不动（第 8 节）。
6. 来源：数值来源与 v3 相同，没有新的解析输出。`docs/model_spec.md` 在 v3 之后由并行会话改了一行（d1ec2c8，第 135 行「香港」改为「英国」）；表中引用的是该文件第 8、10、93 行，未变，显示值不受影响，sha256 已在 numbers_ledger_v4.md 第 8 节更新。

产物（`manuscript/v4/`）：tables_v4.docx、figures_v4.docx、supplement_v4.docx、results_v4.docx、本文件、numbers_ledger_v4.md；辅助：check_v4.md、diff_v3_v4.md、MANIFEST_v4.md、figures/。代码：`make_supplement.py`（S10 的 ✳✳✳ 注与 Elmore 行的核对）、`edit_results.py`（新）、`make_ledger.py`（台账与 docx 的逐字核对、Elmore 核对一节、MANIFEST 的版说明）、`common.py`（版号与 `STEP`）。

## 1. 目的与 Results 各段的对应（规约第 2.1 节；v3 沿用）

| 目的 | Results 的段落（results_v4.docx） | 开头点名的表或图 |
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

P10 的改动（本版指示）：
- 原第 5 句「Across the six scenarios in this table, the HR at which …」的范围含 Elmore 行。改为只含四个效用情景与 S-JP：「With the four utility scenarios and Japanese post-operative treatment, this cost equaled the fee-schedule-based program cost at HRs of 0.988 to 0.989 (Supplementary Table S10).」范围的两端与 v3 相同（0.988、0.989）。
- 新增一句，只写 Elmore 的参照 ICER：「With longer survival after progression during neoadjuvant therapy, the ICER of pembrolizumab was JPY 2,082 thousand per QALY (Supplementary Table S10).」（208.2 万日元/QALY = 2,082 千日元；`scenario_reference.csv`，scenario = elmore，icer = 2,081,860.29）。不写它对运动的结果。
- 规约要求稳健性内容集中在末尾一段，所以没有拆段；改后 P10 为 150 词（上限 150）。

## 2. 正文表

无改动（diff_v3_v4.md：tables 0 个块）。

## 3. 图

无改动。Fig. 1–3、Supplementary Fig. S1–S2 的 PNG 与 TIFF 与 v3 逐字节相同；图注 0 个块。

## 4. 补充材料（supplement_v4.docx；编号同 v3）

编号与内容同 v3（S1、Fig. S1、S2、S4 至 S9、Fig. S2、S10；S3 与 Supplementary Methods S1 随 Methods 写）。本版只改 Supplementary Table S10 的 ✳✳✳ 注（Elmore 行），在原注后接两句：

> Progression during neoadjuvant therapy occurs before surgery and is the same with and without exercise, whereas the exercise effect on recurrence acts only after surgery. The maximum affordable costs and break-even hazard ratios for exercise therefore equal the base-case values in Table 2 at the precision shown; this scenario changes only the ICER of pembrolizumab.

- 放在原有的 ✳✳✳ 注里，没有另加符号：Elmore 行的行标签已带 ✳✳✳，一行一注，符号与脚注仍一一对应。
- 「at the precision shown」是我加的限定，原因见下面的核对。
- 核对（`make_supplement.py` 中断言；数字对照表第 4 节末）：Elmore 行的 6 个运动格与 Table 2 的基准值逐格相同（2,726；0.989 (1.1)；0.958 (4.2)；3,443；0.991 (0.9)；0.966 (3.4)）。与基准的原始差：

| 比较 | scenario_caps.csv，hr0 格点 13 个上 cap_500 的最大差 | sc_crossings.csv，分界点 9 个的最大差 |
|---|---|---|
| 主比较 | 3.1e−7 日元 | 2.2e−14 |
| 次比较 | 9.53 日元 | 1.53e−8 |

- 指示写的「差 ≤ 1.5e-8」：sc_crossings.csv 中的实测最大值是 1.53e−8（次比较，E01，λ = 500 万日元），`phase2b_report.md` 第 7.5 节按两位有效数字印为 1.5e−08。
- 次比较的差不是舍入误差。我用引擎只读检查（不改代码、不写输出）：化疗单用组 non-pCR 分支的术前进展流入有一部分落在手术后第一个周期（第 7 至 8 个月）。这个周期里，引擎把术前进展与术后复发作为同一周期内的竞争风险计算；运动降低复发的风险后，进入术前进展的比例多出 1.5e−6（0.0867052 对 0.0867067）。帕博利珠单抗组在该周期没有术前进展流入，所以主比较的差只在 1e−14 量级。这个差不改变任何显示值。所以脚注的结论句写「at the precision shown」，不写「完全相同」。
- 同一情景在 pCR 轴（路径 B，`scenario_caps.csv` axis = pcr）上会改变运动的上限（最大差：主比较 35,121 日元，次比较 62,982 日元）：运动提高 pCR 后 non-pCR 的人减少，术前进展也随之减少。S10 只列复发 HR 的结果，Elmore 的路径 B 不在任何表中；所以脚注写「the exercise effect on recurrence」，把范围限定在复发 HR。

## 5. 用语表（v3 沿用）

| 名称 | 指什么 | 初出 |
|---|---|---|
| maximum affordable cost | 上限 | Results P1；Table 2 ✳ 注 |
| recurrence hazard ratio (HR) | hr0 | Results P1 |
| 95% uncertainty interval (UI) | PSA 1,000 样本的 2.5 与 97.5 百分位 | Results P1；Table 2 ✳ 注 |
| medical costs avoided | −Δ费用（不含方案费用） | Results P1 |
| incremental medical costs other than the program cost | 与 S5「Total without the program cost」同一量 | Results P2 |
| Utility values from Japanese populations | 日本人群效用情景 | Supplementary Table S10 |
| Longer survival after progression during neoadjuvant therapy | Elmore 边界情景；Results P10 第 6 句用同一名称 | Supplementary Table S10 |
| the four utility scenarios（新） | S10 的日本人群效用与美、英、澳价值集四行 | Results P10 第 5 句 |

金额的写法：正文写「JPY 2,082 thousand」，与表中千日元的显示值同值同位。

## 6. 决定、例外与待决

### 6.1 本版照指示处理的事项
- S10 Elmore 行的脚注（第 4 节）。
- Results 末段只写 Elmore 的参照 ICER，运动的范围句不含 Elmore（第 1 节）。

### 6.2 有意的例外（v3 沿用）
- E1（已决）Table 2 panel B、C 的基准行与 S4 重复。
- E2（已决）S1 与 Table 1 的基本值重复（同一来源格 26 个）。
- **E3（待确认）** S6 与 Table 2 panel B 重复 4 格。
- **E4（待确认）** S10 的 S-JP 参照 ICER 与 Table 3 的 S-JP 栏重复 1 格（3,044）。
- check_v4.md 的自动检测（同一来源格出现在两张表中）只发现上述四类。

### 6.3 待决
- **N10（新）** S10 Elmore 行的 6 个运动格显示的数与 Table 2 的基准值相同；按新脚注，这是必然的。它们取自不同的来源格（scenario = elmore），自动检测不算重复，但规约第 6.1 节「同じ数値は一つの表にだけ置く」按字面算是同一数值出现在两张表。照指示保留了数字。另一选项：这 6 格写「Same as base case (Table 2)」之类的文字，只保留 ICER 一格的数字。
- N5 至 N9：同 v3（Fig. S2 只画 20 个；S1 与 S9 出处栏的姓名与院名；S1 的位数按单位统一；出处的完整书目待换文献编号；Supplementary Methods S1 与 CHEERS 随 Methods 写）。
- E03、D02、F01P（S-JP）的暂定值在 numbers_ledger_v4.md 第 6 节标出。

## 7. 检查（重跑 v3 的全部检查，并新增两项；check_v4.md）

最重要的四项：
1. 版：`manuscript/` 下只有 v4、archive（v1、v2、v3）、code；v4 内只有本版文件。通过。
2. 表与图的引用：Results 的初次引用顺序同 v3：Fig. 2 → Table 2 → S4 → S5 → S6 → S7 → Table 3 → S8 → Fig. 3 → S9 → Fig. S2 → S10，各系列内递增。Table 1、Fig. 1、S1 至 S3、Fig. S1 由 Methods 引用，Methods 未写，这一项要等全稿。
3、4. 文献：本步无文献，不适用。

docx 回读（走查的母数：tables 289 个段落与单元格、313 个 run；figures 14、12；supplement 2,215、2,207；results 11、11）：
- 全部文字 run 为 Times New Roman 12 pt；以下各项都是 0：黑以外的文字、Heading 样式、空单元格、表外粗体（Results 的节标题除外）、含数字的单元格粗体、「・」、以 Note 开头的段落、表外的「—」。
- 横纵：tables 全横版；figures 全纵版；supplement 表为横版，两张补充图为纵版；results 纵版。
- 脚注符号：Table 1–3、Fig. 1–3、S1、S2、S4–S10、Fig. S1–S2 全部一一对应且按顺序（S10 仍为 ✳ 至 ✳✳✳✳ 四个）。
- 数字：tables 260 个、figures 30 个、supplement 2,328 个，未登记的都是 0；登记的数值都在文档中出现。
- Results：10 段 44 句 862 词（v3 为 43 句 846 词）；双倍行距 11/11 段；行号已设。以下各项都是 0：禁用语、前置套话、自我说明、推测语、方法句、裸时间词、因果语、破折号、连接词连用。
- Results 的长度：超过 30 词的句 0（最长 30）；超过 150 词的段 0（最长 150，P10）。
- Results 的引用与数字：每段以表或图开头 10/10；无表图引用的句 0；81 个数字都是所引表格中的显示值。
- ARS check_acronyms.py（body）：coverage complete，No findings（JPY、ICER、QALY 用 --allow 豁免，同 v3）。
- **新检查 1**（`make_ledger.py` 的 ledger_matches_docx）：逐句检查读的是台账，所以台账必须与 docx 逐字一致。结果 True。
- **新检查 2**（`make_supplement.py`）：Elmore 行的运动格必须等于 Table 2 的基准值，否则停止。
- 新检查的鸣响：在 docx 副本中把 P10 第 6 句的「was」改为「rose to」，检查 1 给出 False；在 Table 2 的登记表中把一格改为 0.992，`make_supplement.py` 以 AssertionError 停止，supplement_v4.docx 未被改写。测试后登记表与测试前逐字节相同。
- 改写段落的诊断（规约第 1.6 节；writing_quality_check.md A 至 F）：
  - A 标记语、B 标点（破折号、分号、冒号列举）、C 套话与自我说明、D 三项强迫与二元对比：都没有。
  - D 同义词循环：没有。「this cost」指同段第 2、4 句的 maximum affordable cost，用法同 v3 的第 2 句。
  - D 结构：第 5、6 句都以「With …」开头，两个情景并列，便于比较，保留。
  - E 句长：最长 25 词。F 缩写：见上。
  - Claim-Strength：主张没有变强。
- 图：Fig. 1–3、Fig. S1–S2 都是 4015 像素宽、600 dpi，插入后实际 600 dpi；字号检查 5 张都没有低于 8 pt 的字；碰撞检查 5 张 0 fail 0 warn；Fig. 2 与 Fig. S1 面板对齐 PASS；validate_figure.py（作图代码的静态检查）19 pass、2 warn、0 fail。
- Word（COM）逐个打开 4 个 docx 并另存为 PDF，脚本无报错：tables 8 页、figures 3 页、supplement 37 页、results 3 页（与 v3 相同）。

## 8. 与 v3 的逐段对照（diff_v3_v4.md）

| 文件 | 项数（v3/v4） | 不同的块 | 内容 | 对应 |
|---|---|---|---|---|
| tables | 287/287 | 0 | — | — |
| figures | 9/9 | 0 | — | — |
| supplement | 2,186/2,186 | 1 | S10 的 ✳✳✳ 注接两句 | 指示第 1 条 |
| results | 11/11 | 1 | P10：第 5 句改写、加第 6 句 | 指示第 2 条 |
| 图文件 | — | — | PNG、TIFF 与 v3 逐字节相同 | — |

意图之外的变化：0。数值：表、图、补充材料的所有显示值与 v3 完全相同；Results 只多一个数字（2,082）。

## 9. 第 13 节的逐项点检（规约第 14 节）

本版交付物是表、图、补充材料与 Results 一节；manuscript 的其余部分（Introduction、Methods、Discussion、Implications、Limitations、Abstract）与 title page 尚未作成。下表中「不适用」都是这个原因，除非另注。

| 项目 | 结果 |
|---|---|
| 版：作业树只有最新版 | 通过（manuscript/ 下 v4、archive、code） |
| 版：开始时 sha256 与 manifest 一致 | 通过（v3 的 numbers_ledger 第 8 节 48 个来源文件：47 个一致，1 个是 docs/model_spec.md，由并行会话改了未引用的一行，见第 0 节第 6 条） |
| 版：底本为 v(n−1)，作业记录开头有底本与 sha256 | 通过（第 0 节第 3 条） |
| 版：意图之外戻った段落 0 | 通过（第 8 节；补充表的脚注逐条比较，只有 S10 ✳✳✳ 一条变化） |
| 版：数值不变的版与 v(n−1) 数值完全一致 | 表、图、补充材料通过；Results 照指示加了一个数字 |
| 版：模板雏形 0 | 通过（交付物中没有 [name]、[affiliation]、[email]） |
| 版：版号与作业注记 0、[TO CONFIRM] | 通过（docx 中无版号；[TO CONFIRM] 0 件） |
| 版：manifest 更新、旧版移入 archive | 通过 |
| 版：解析输出的 sha256 与 manifest | 通过（numbers_ledger_v4.md 第 8 节） |
| 版：差分全部对应指示 | 通过（第 8 节） |
| 版：撤回的主张 0 | 不适用（无撤回记录） |
| 版：变更履历与注释 0 | 通过（python-docx 生成，无 w:ins、w:del、comments） |
| 版：ARS 的 Markdown 初稿与 ars/ 0 | 通过（无 ars/） |
| 文献：初出顺、DOI、原著核对、citation-check、无著者年引用、10 年以上与自引比例、新规性限定 | 不适用（段阶 1 未做；S1 与 S9 出处栏的书目见 N8） |
| 付番：四个系列的初出顺 | Results 内通过（第 7 节）；全稿待 Methods |
| 付番：最大编号与实数一致 | Table 3、Fig. 3、Supplementary Table S10、Supplementary Fig. S2：通过；S3 与 Supplementary Methods S1 未作 |
| 付番：所有表图在地の文中被引用 | Table 1、Fig. 1、S1、S2、Fig. S1 待 Methods |
| 付番：supplementary 内按编号排列 | 通过（S1、Fig. S1、S2、S4 至 S10、Fig. S2 的物理顺序与编号一致；S3 缺） |
| 付番：补充方法与报告规范从正文引用 | 不适用（未作，N9） |
| 付番：图附上且从 Fig. 1 依次引用 | Fig. 1 待 Methods |
| 见出し：六个大见出し、Methods 四个小见出し | 不适用（只有 Results；Results 无小见出し） |
| 见出し：规约外的节与项目 | 通过（v3 与 v4 都只有「Results」一节，无前付け） |
| 体裁：Heading 样式 0、12 pt TNR、黑字 | 通过（第 7 节） |
| 体裁：行号、双倍行距、行内粗体 0 | 通过 |
| 体裁：表的列见出しと数値セル粗体 0 | 通过 |
| 体裁：「・」0、表为横版、✳ 脚注、Note 0、符号一一对应 | 通过 |
| 体裁：图 600 dpi 实测 | 通过（4015 像素宽，插入后 600 dpi） |
| 体裁：前付け | 不适用（title page 为尾崎担当） |
| 体裁：生成 AI 的记述 0、ARS 标记 0、ARS 默认的遗留 0 | 通过 |
| 体裁：拼写统一（米式）、Fig. 统一 | 通过 |
| 体裁：语数 | Results 862 词；投稿先未定，不比较上限 |
| 数值：正文数值在台账、出所表中同值同位 | 通过（81 个） |
| 数值：表脚注的数值在表或图中 | 通过（S10 新脚注中无新数字） |
| 数值：同一数值不在两张表 | E1 至 E4 与 N10（第 6 节） |
| 数值：分层 n 之和、百分率之和、流程图 | 不适用（无分层计数表与流程图）；S7 的 N：2,294 + 1,157 = 3,451，与表头一致 |
| 数值：对象者数一致 | 不适用（模型队列） |
| 数值：点估计在 CI 内、CI 与 p | 通过（本版从登记表实测：tables 16 组、supplement 180 组「点估计 [2.5, 97.5 百分位]」，点估计都在区间内；无 p 值） |
| 数值：同一统计量同值同位 | 通过 |
| 数值：p 值表记、trend 型用语 | 不适用（无 p 值） |
| 数值：因果语 0 | 通过（Results 0；新脚注中「changes」描述模型设定，不是观察研究的因果主张） |
| 数值：要约统计量的形、空セル 0 | 通过 |
| 数值：负号、前导 0、千位逗号 | 通过（U+2212；0.988；2,082） |
| 数值：小数位按表统一、百分率舍入一致 | 通过（S1 按单位，N7） |
| 内容：Methods 无数值结果 | 不适用 |
| 内容：Results 无方法句、各结果句有表图引用 | 通过 |
| 内容：各解析有目的句、Introduction 末两段、目的对应表 | 第 1 节的对应表通过；其余不适用 |
| 内容：Results 段落按目的顺序、段首点名表图 | 通过 |
| 内容：Discussion、Implications、Limitations、Abstract 各项 | 不适用 |
| 内容：用语定义与一致 | 通过（第 5 节） |
| 内容：缩写（正文初出展开、表图脚注再展开、check_acronyms） | 通过（Results complete、No findings；S10 脚注列出 HR、ICER、JPY、QALY） |
| 内容：统计软件、Ethics 等、报告规范、题名、欠测、多重比较、流程图 | 不适用 |
| 内容：图中无题名、面板标签、单位、不只靠颜色、≥ 8 pt | 通过 |
| 内容：图与表无同一结果重复 | 通过（图的数值在 S4、S9、S2，按规约放补充表） |
| 内容：著者贡献 | 不适用（尾崎担当） |
| 内容：AI 常套语、套话、自我说明、连接词连用 0；破折号、30 词与 150 词 | 通过（第 7 节） |
| 内容：裸时间词 0、事实句无 may | 通过 |
| 内容：主张强度未变强 | 通过 |
| 内容：rebuttal-audit、humanizer、stop-slop | 不适用（非查读对应版；humanizer 与 stop-slop 在全稿初稿后） |
