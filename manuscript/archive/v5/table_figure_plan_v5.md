# 作业记录 v5（执笔第 3 步 v5：Results 修改；Methods、Introduction；文献（段阶 1）；S1（CHEERS）与 Supplementary Methods S1；待决事项，2026-10-27）

## 0. 声明与底本

1. 规约：开工时读了 `Documents/ClaudeCode/WRITING_RULES.md` 全文；交付前从头到尾重读了全文（514 行，第 14 节），第 13 节的逐项点检见第 9 节。ARS：academic-paper（SKILL.md 的 Anti-Patterns 与 Quality Standards、draft_writer_agent.md、writing_quality_check.md、academic_writing_style.md、writing_judgment_framework.md、intro_title_rhetoric_guide.md）、deep-research（lit-review 的检索记录）、citation_compliance_agent.md（审核报告的格式）。nature-figure：图未改，只重跑审查。
2. 段阶：段阶 1（文献）与段阶 3 的一部分（Introduction、Methods、Results 的修改）。Discussion、Implications、Limitations、Abstract 按指示不写。
3. 底本：`manuscript/archive/v4/`（tables_v4.docx a9f238b2、figures_v4.docx 9fb3a39f、supplement_v4.docx 58343716、results_v4.docx adea1932、table_figure_plan_v4.md b601b347、numbers_ledger_v4.md 9e7a00e1、MANIFEST_v4.md 6d9dde53）与 `manuscript/code/`。v4 已移入 archive；作业树 `manuscript/` 下只有 v5、archive（v1 至 v4）、code。
4. 指示：「执笔第 3 步（v5）」（2026-10-27）的第 0 至 7 条。
5. 做法：
   - 本文 manuscript_v5.docx 由 `archive/v4/results_v4.docx` 直接编辑而成（规约第 1.2 节规则 2）：`edit_manuscript.py` 在 Results 前插入 Introduction 与 Methods，并逐句修改 Results（44 处，第 4 节）；`number_refs.py` 把文献标记换成上标番号并附 References。
   - 表、图、补充材料用同一套生成代码重新生成（`make_tables.py`、`make_figures.py`、`make_supplement.py`）；图的像素与 v4 逐字节相同。
   - 文献：`refs/` 下的脚本检索、取书目、实测 DOI、撤稿筛查、原著对照（第 6 节与 references_v5.md）。
6. 来源：数值来源与 v4 相同，没有新的解析输出；新的项目文件只有文献数据（`manuscript/code/refs/`）。

产物（`manuscript/v5/`）：manuscript_v5.docx、tables_v5.docx、figures_v5.docx、supplement_v5.docx、本文件、numbers_ledger_v5.md、references_v5.md；辅助：check_v5.md、diff_v4_v5.md、MANIFEST_v5.md、figures/。ARS 的作业记录（PCR、Argument Blueprint、writer 自评、citation audit）在交付时移入 `manuscript/archive/ars_v5/`（规约第 1.5 节上书き 10）。

## 1. 目的与各节的对应（规约第 2.1 节）

目的（Introduction 第 4 段，用户给定的原文）：目的 1（主）最大可负担费用及其随效应大小与持续时间的变化；目的 2（副 a）加入单用化疗时的同一费用；目的 3（副 b）帕博利珠单抗在日本的成本效果；目的 4（副 c）与帕博利珠单抗同 QALY 增益的运动效应。

| 目的 | Introduction 的不足 | Outcome | Statistical analysis 的段阶 | Results 的段落 |
|---|---|---|---|---|
| 目的 1 | 第一 | M.OUT.1；M.OUT.2 第 1 句 | (1) 至 (6) | P1 至 P5、P10 |
| 目的 2 | 第一 | 同上（次比较） | (2)、(3) | P6 |
| 目的 3 | 第二 | M.OUT.2 第 2 句 | (2) 至 (5) | P7、P8、P10 |
| 目的 4 | 第二 | M.OUT.2 第 3 句 | (2) | P9 |

Methods 中声明的推定对象都在 Results 报告（最大可负担费用 P1；两个分界 HR P1、P4；ICER P7、P8；同 QALY 的运动效应 P9；一年净收益 P5）。

## 2. Introduction（4 段，581 词）

- P1：第 II、III 期 TNBC 的复发风险；KEYNOTE-522 方案成为标准，2024 年日本 3,451 例中 2,294 例用帕博利珠单抗（JBCS 第 55 号）；一次给药 398,924 日元（200 mg = 100 mg 瓶 2 支 × 199,462 日元，药价表原文已核对）。
- P2：CHALLENGE（结肠癌，DFS 与 OS）；乳腺癌化疗期间的随机试验（体能与疲劳）；新辅助期间的 pCR 试验与 meta 分析；复发未知。
- P3（不足）：「lacks two things. First, … Second, …」。第一：运动的经济评价对试验中测得的效应计价；效应未知时可算最大可负担费用（headroom）。第二：KEYNOTE-522 方案的成本效果分析来自美国、香港、瑞士、埃及，日本的分析只涉及晚期癌，帕博利珠单抗未被指定为费用对效果评价的对象（C2H 一览 88 品目，2026-10-26）。按检索结果如实写。
- P4（目的）：用户给定的两句原文，后接新颖性句：「No economic evaluation of exercise during neoadjuvant therapy for breast cancer was identified in searches of PubMed and Europe PMC covering 2000 to 2026, last run on 26 October 2026.」与最接近的研究 Phys-Can。不用「first」。检索式与日期在 references_v5.md 第 1、2 节。
- Introduction 无方法句。

## 3. Methods（4 个小见出し 18 段，1,507 词）

- Study background：决策问题；KEYNOTE-522 型、49 岁、第 II、III 期 TNBC 开始新辅助化疗的队列；四臂；日本公的医疗支付者立场；终生；2% 折现（C2H 指南 2026）；CHEERS 2022（Supplementary Table S1）；阈值：运动为 500 万日元/QALY，理由一句（750 万日元只适用于被指定并受特别考虑的医药品等，如恶性肿瘤，运动方案不在此类；厚劳省 2026-02-13 通知 p.9、p.13）；帕博利珠单抗另按 750 万日元评价。数据截点 4 个（2021-03-23 IA4、2023-03-23 ESMO 2023、2024-03-22 OS 报告、2025-10-14 最终分析）；计划未登记。
- Outcome：第一句「The primary outcome was the maximum affordable cost of an exercise program per patient」，后接定义（阈值 × ΔQALY − 不含方案费的 Δ费用）；副次：两个分界 HR、ICER、同 QALY 的运动效应、一年净收益。
- Variables：第一句「The exposure was …」；生存、复发后生存、费用、效用、运动效应的定义与持续、pCR 路径、运动的有害事象；引 Table 1 与 Supplementary Table S2，不重复数值；德国价值集为基准的理由一句；日本人群的值为情景。
- Statistical analysis：番号段阶 (1) 至 (6)，各以目的句「To …」开头；(1) 不用 OS 拟合、只作验证，细节在 Supplementary Methods S1、Supplementary Fig. S1、Supplementary Table S3；Fig. 1 在此引用；最后一句「All analyses were performed in R version 4.5.1.」；多重比较一句。无结果数值。
- 起草后的自检与原著对照中改正的 4 处（都是改准确，不加主张）：
  - Study background 第 3 段第 1 句：截点列表加入 23 March 2023 并引 esmo2023（该截点的值用于选分布族）。
  - Variables 第 3 段第 2 句：购买力平价句只引世界银行（加拿大银行的汇率只用于上限）。
  - 段阶 (5)：「utility value sets from the United States, the United Kingdom and Australia」改为「utility values scored with the United States and United Kingdom value sets and those of the Australian reimbursement submission」（PBAC 的公开摘要未写价值集）。
  - 段阶 (5)：加目的句「To examine alternative assumptions, …」（规约第 4 节：手法名前写目的）。

## 4. Results 的修改（44 处；diff_v4_v5.md）

| 类别 | 处数 | 对应的指示 |
|---|---|---|
| 补充表编号的更换（v4 → v5：S1→S2、S2→S3、S5→S6、S6→S7、S7→S8、S8→S5） | 11 | 第 1 条（按初出顺重新确认编号） |
| 连续句引同一表时只在末句引一次 | 18 | 第 2 条 |
| 估计值与 95% UI 放在同一句（P1 原第 2、3 句合并） | 1 | 第 2 条 |
| 缩写在 Introduction 或 Methods 初出时已定义，Results 不再定义 | 5 | 规约第 4 节（缩写在本文初出展开） |
| 新增：路径 B（每 1 个百分点 pCR 的上限，S5），P1 | 2 | 第 2 条 |
| 新增：术后继续运动与「效应持续到术后 1 年」的比较（S7），P3 | 1 | 第 2 条 |
| 新增：「早期复发后死亡较高」情景下主比较 HR 0.85 的上限（S4），P10 | 1 | 第 2 条 |
| P1 与 P10 的措辞压缩（不删结果） | 5 | 第 2 条（末段超限时先压缩措辞） |

新增的句（数值都在所引表中）：
- P1：「Through an effect on pCR instead, an increase of 1 percentage point gave a maximum affordable cost of JPY 389 thousand (95% UI [238, 570]). Each further point added about the same amount (Supplementary Table S5).」路径 B 的上限对 pCR 是精确线性的（每个百分点 389,880 日元），S5 不单列「每个百分点的增量」，所以写 S5 中 +1 个百分点的值，后续写「about the same amount」。
- P3：「With exercise continued after surgery, it was JPY 2,239 thousand, against JPY 1,772 thousand when the effect lasted until 1 year after surgery without continuation (Supplementary Table S7).」
- P10：「With higher mortality after early recurrence with pembrolizumab, this cost was JPY 2,691 thousand (95% UI [2,201, 2,994]; Supplementary Table S4).」

P1 改后 150 词，P10 149 词（上限 150）；其余结构、顺序与数值不变。

## 5. 表、图与补充材料

- 编号（按本文初出顺）：S1 = CHEERS 2022（Methods, Study background 初出；指示写作「S3」，按第 1 条的初出顺规则成为 S1）、S2 = 全部输入、Supplementary Methods S1、Supplementary Fig. S1、S3 = 验证值、S4 = Fig. 2 的数据、S5 = 路径 B、S6 = 费用内訳、S7 = 持续时间、S8 = 一年净收益、S9 = 一元感度、Supplementary Fig. S2、S10 = 其他情景。supplement 内的物理顺序与此一致。
- 新作：S1（CHEERS 2022 的 28 项，条目与指引文字取自 PMC8749494 的 XML；位置栏为本文的节、段与页，页码用 Word 实测）；Supplementary Methods S1（生存模型：重建、分层拟合、7 年等式约束、外部的复发后生存、术前进展、有害事象死亡、背景死亡下限；验证门槛，OS 只作验证；PSA 抽样；按 phase1_report 的最终状态与 model_spec 写，不写开发经过）。
- 文献：Table 1 与 S2 的出处栏、表注、图注、补充材料中的引用都换成文献番号（N8）。
- S10：Elmore 行的 6 个运动格写「Same as base case (Table 2)」，只留参照 ICER 的数字，脚注不变（N10）；S-JP 的参照 ICER 格写「Table 3」（E4）。
- 本版发现并修正的错误：S7、S9、S10 的脚注里输入表的编号仍是 v4 的「S1」（3 处），改为 SUPP['params']（S2）；新增检查 references_to_input_table_wrong_number（第 7 节）。
- 图：像素与 v4 逐字节相同；Fig. 2 的图注加了 CHALLENGE 的文献号。

## 6. 决定、例外与待决

### 6.1 本版照指示处理的事项
- E3：接受，与 E1 同类（S7 与 Table 2 panel B 重复 4 格）。
- E4：S10 的 S-JP 参照 ICER 格改为「Table 3」。
- N5、N7、N8：接受。
- N6：S2 的出处栏写「Two breast medical oncologists at Japanese hospitals (personal communication, October 2026)」；v4 写作单数「Clinical expert」的行写「A breast medical oncologist at a Japanese hospital (…)」（按 v4 的单复数）。院内费用的行写医院名（Kasugai Municipal Hospital、Chuden Hospital），网址在文献表的条目中（出处栏引用该条目）。
- N9：Supplementary Methods S1 与 CHEERS 随 Methods 写（第 5 节）。
- N10：S10 Elmore 行（第 5 节）。

### 6.2 有意的例外
- E1、E2、E3（已决）：S4 与 Table 2 重复 6 格、S2 与 Table 1 重复 26 格、S7 与 Table 2 重复 4 格。
- I.4 为 154 词（上限 150），目的两句为 59 词与 47 词（上限 30）：用户给定的原文，未改。目的未加番号（原文）。
- Statistical analysis 的段阶按解析种类排列（用户指定），不按目的番号（规约第 2.1 节），对应表见第 1 节。
- Fig. 1 是模型结构图，不是解析流程图（规约第 4 节：段阶 5 个以上时 Fig. 1 为流程图）：Fig. 1 由用户在前版指定为模型图。
- Methods 段阶 (1) 引用载有结果的 Supplementary Fig. S1 与 S3（指示第 3 条）。
- 段阶 (6) 不引 S8（S8 的初出在 Results P5，Methods 先引会打乱初出顺）。
- 计划未登记，未另加偏离一览（M.SB.3 写明）。
- I.3 第 6 句一句引 7 篇（日本的全部检出分析）。

### 6.3 待决
- **N11（新）**：S10 的行名「Utility value set: Australia」。PBAC 的公开摘要（PSD p.18）只写「Utilities were based on EQ-5D responses in KN-522」，未写价值集。本版 Methods 写作「those of the Australian reimbursement submission」；S10 的行名是 v4 的原文，未改。选项：改为「Utility values: Australian reimbursement submission」，或维持。
- **N12（新）**：KEYNOTE-522 最终分析按 pCR 分层的 7 年 EFS（90.4% 对 85.9%，57.6% 对 49.7%）不在摘要中，读自会议报道（OncLive、DelveInsight）；ESMO 2023（LBA18）的摘要原文未取得（403），2023-03-23 截点的值读自 OncLive。两者都引原报告的摘要。原始出处待尾崎先生确认（docs/model_spec.md 第 87 行的既有事项）。
- **N13（新）**：tropion2025 选了 2025-10-19 报告试验结果的新闻稿（参数表未写日期）；待尾崎先生确认。
- jbcs55：数值由尾崎先生提供，会员限定的原表未见。
- CHEERS 第 1、2 项的位置写「Title page」「Abstract」，无页码；Abstract 写成后补页码。
- E03、D02、F01P（S-JP）的暂定值在 numbers_ledger_v5.md 第 6 节标出（v4 沿用）。
- Discussion 的候选（不在本版）：Snooks 2026（预印本，卵巢癌新辅助化疗期间的术前康复的经济评价），见 references_v5.md 第 2 节。

## 7. 检查（check_v5.md）

最重要的四项：
1. 版：`manuscript/` 下只有 v5、archive（v1 至 v4）、code；v5 内只有本版文件；ars/ 在交付时移入 archive。通过。
2. 表与图的引用：本文 32 段（Introduction 4、Methods 18、Results 10）走查，取出的初出顺为 S1、Table 1、S2、Fig. 1、Supplementary Methods S1、Supplementary Fig. S1、S3、Fig. 2、Table 2、Table 3、Fig. 3、S4 至 S9、Supplementary Fig. S2、S10。四个系列与补充方法各自 1, 2, 3, …；最大番号 = 实数（Table 3、Fig. 3、Supplementary Table 10、Supplementary Fig. 2、Supplementary Methods 1）；supplement 的物理顺序一致。通过。
3. 文献的真伪：DOI 61 篇全部在 doi.org 实测 30x，并与 Crossref 比对（写法差异 11 篇，逐条确认为同一文献）；无 DOI 的 16 篇是文件与网页，各有到源页面的核对；撤稿 0。通过。
4. 文献的顺序：本文的上标 51 个 run，初出顺 1 至 62 无缺；表、图注、补充材料中新出的 63 至 77 按阅读顺序；77 篇全部被引用，表外番号 0。通过。

docx 回读（走查的母数：manuscript 117 段、tables 287 项、figures 9 项、supplement 2,352 项）：
- 全部文字 run 为 Times New Roman 12 pt；以下各项都是 0：黑以外的文字、Heading 样式、空单元格、表外粗体（见出し除外）、含数字的单元格粗体、「・」、以 Note 开头的段落、表外的「—」。
- 见出し：Introduction、Methods、Study background、Outcome、Variables、Statistical analysis、Results、References（Normal 段落粗体 12 pt）；双倍行距 117/117；行号已设。
- 脚注符号：全部表与图一一对应且按顺序。
- 数字：manuscript 182 个、tables 260 个、figures 30 个、supplement 2,184 个，未登记的都是 0。Introduction 与 Methods 的 90 个数字逐段登记（93 行：PubMed 摘要 14、JBCS 表 5、表与图的登记 38、定义 14、检索记录 4、项目文件 17、renv.lock 1）。Results 92 个数字都是所引表中的显示值；每段以表或图开头 10/10。
- 文体：禁用语、前置套话、自我说明、推测语、方法句、裸时间词、因果语、破折号、连接词连用都是 0。超过 30 词的句：I.4 的目的两句（59、47，用户原文）；超过 150 词的段：I.4（154）。语数：Introduction 581、Methods 1,507、Results 866，合计 2,954。
- ARS check_acronyms.py（本文）：coverage complete，No findings（JPY、TNBC、QALY、ICER 在初出处定义但检查器不识别连字符形与「yen」的展开，用 --allow 豁免；PMC 与 EQ 是名称的一部分）。
- 原著对照（references_v5.md 第 8 节）：本文 82 处（句 × 文献）与图注、补充材料的散文 22 处全部有对照记录；119 条逐字段落全部在出处中找到（ok 109、corroborated 2、report 4、provided 4）；出处栏 131 处按参数表的「出典の該当箇所」逐行列出。
- 新检查与鸣响（规约第 13 节：新检查先用故意的违反鸣一次）。在 v5 的副本上植入违反，make_ledger 以副本为对象运行：
  - 本文的上标 1 与 2 互换 → main_text_first_appearance_is_1_to_K = False；
  - Introduction 第 2 段加入未登记的数「37」→ numbers_not_registered_for_their_paragraph = [('I.2', '37')]；
  - Variables 的「Supplementary Table S2」改为「S6」→ each_series_1_to_n_in_order = False；
  - 删去文献表最后一条 → N_reference_list 76、list_text_equals_entries False、every_reference_cited False、citations_to_numbers_beyond_list [77]；
  - S9 脚注的输入表编号改回 S1 → references_to_input_table_wrong_number 列出该处。
  第 4 项最初暴露了 list_text_equals_entries 的漏洞（zip 在短的一方截止，删一条仍为 True），已加条数比较。植入只在 scratchpad 的副本上，v5 本体未改。
- 原著对照的检查（claim_support.py）：段落不在出处中时 make_references_doc.py 停止；本文的（句 × 文献）与对照记录必须一一对应，否则停止。
- 图：Fig. 1–3、Fig. S1–S2 为 600 dpi（插入后实测）；字号检查 5 张都没有低于 8 pt 的字；碰撞检查 0 fail 0 warn；validate_figure.py 19 pass、2 warn、0 fail（像素与 v4 相同）。
- Word（COM）打开 4 个 docx 并另存为 PDF，无报错：manuscript 20 页、tables 8 页、figures 3 页、supplement 43 页。CHEERS 的页码取自同一 Word 的分页。

## 8. 与 v4 的逐段对照（diff_v4_v5.md）

原始比较之外，另做归一化比较（v4 的补充表编号换成 v5 的编号、v5 去掉文献号），剩下的块都是措辞或内容的变化：

| 文件 | 归一化后的块 | 内容 | 对应 |
|---|---|---|---|
| tables | 7 | Table 1 出处栏的措辞（引文献号后改为「KEYNOTE-522 (interim analysis 4)」「Abridged life table (2025)」「KEYNOTE-522 reports」等） | 指示第 5 条、N8 |
| figures | 0 | — | — |
| supplement | 95 | N1 插入 S1（CHEERS）；N2 至 N90 S2 出处栏（完整书目换成文献号，专家与医院的写法）；N91 插入 Supplementary Methods S1；N92、N93 路径 B 的表由 S8 的位置移到 S5（内容 172 项相同）；N94 Elmore 行 6 格；N95 S-JP 的参照 ICER 格 | 第 1、5、6 条，N6、N8、N9、N10、E4 |
| manuscript | 2 | 插入 Introduction 与 Methods；Results 10 段（第 4 节）与 References | 第 2 至 5 条 |

S7、S9、S10 的三条脚注在原始比较中只差输入表的编号（v4 的 S1 → v5 的 S2），归一化后与 v4 一致。意图之外的变化：0。数值：表、图、补充材料的显示值与 v4 相同，只有 N10 与 E4 的 7 格按指示由数字改为文字。

## 9. 第 13 节的逐项点检（规约第 14 节）

本版交付物是 manuscript（Introduction、Methods、Results、References）、tables、figures、supplementary；Discussion、Implications、Limitations、Abstract 按指示不写，title page 为尾崎担当。下表中「不适用」都是这个原因，除非另注。

| 项目 | 结果 |
|---|---|
| 版：作业树只有最新版 | 通过（manuscript/ 下 v5、archive、code；ars/ 交付时移入 archive） |
| 版：开始时 sha256 与 manifest 一致 | 通过（MANIFEST_v4 的 4 个 docx 与 archive/v4 的文件一致：a9f238b2、9fb3a39f、58343716、adea1932） |
| 版：底本为 v(n−1)，作业记录开头有底本与 sha256 | 通过（第 0 节第 3 条） |
| 版：意图之外戻った段落 0（补充表的脚注、题名、语数、图的解像度、过去戻った箇所） | 通过（第 8 节；补充表的脚注逐条比较；图像逐字节相同；题名与语数属 title page，不适用） |
| 版：数值不变的版与 v(n−1) 数值完全一致 | 通过（第 8 节；Results 照指示加 3 个结果，见第 4 节） |
| 版：模板雏形 0 | 通过 |
| 版：版号与作业注记 0、[TO CONFIRM] | 通过（docx 中无版号；[TO CONFIRM] 0 件） |
| 版：manifest 更新、旧版移入 archive | 通过 |
| 版：解析输出的 sha256 与 manifest | 通过（numbers_ledger_v5.md 第 8 节） |
| 版：差分全部对应指示 | 通过（第 8 节） |
| 版：撤回的主张 0 | 通过（v5 删去的主张：Methods 草稿中「utility value sets from … Australia」与 PPP 句的汇率引用，均未进入交付物） |
| 版：变更履历与注释 0 | 通过（python-docx 生成，无 w:ins、w:del、comments） |
| 版：ARS 的 Markdown 初稿与 ars/ 0 | 通过（不出 Markdown 初稿；ars/ 的作业记录移入 archive/ars_v5/） |
| 文献：初出顺、未引用 0、表外番号 0 | 通过（第 7 节第 4 条） |
| 文献：DOI 解决、书目一致 | 通过（61/61；写法差异 11 篇已逐条确认；解决不了的 0） |
| 文献：新规引用全部与原著对照 | 通过，有限定（119 条段落全部找到；report 4 条与 provided 4 条的原著未见，列为待决 N12 与 jbcs55） |
| 文献：citation-check 的报告 | 通过（ars/citation_audit_v5.md：照合 77 篇、订正 5 处、未解决 7 项） |
| 文献：著者年引用 0 | 通过 |
| 文献：10 年超与自引的比例（报告） | 10 年超 8 篇；自引 0% |
| 文献：新规性句的检索限定 | 通过（PubMed 与 Europe PMC，2000–2026，2026-10-26；与 references_v5.md 第 1 节一致；无绝对形） |
| 付番：四系列的初出顺、最大番号、地の文での言及 | 通过（第 7 节第 2 条） |
| 付番：supplementary 内按编号排列 | 通过 |
| 付番：补充方法与报告规范从正文引用 | 通过（Supplementary Methods S1 从段阶 (1) 与 (3)；S1 从 Study background） |
| 付番：图附上且从 Fig. 1 依次引用 | 通过（Fig. 1 在 Statistical analysis 第 1 段） |
| 见出し：六个大见出し | 本版只有 Introduction、Methods、Results 与 References（其余三节按指示不写）；References 是文献表的标题 |
| 见出し：Methods 四个小见出し | 通过 |
| 见出し：规约外的节与项目 | 通过（v4 只有 Results；未加 Acknowledgements 等） |
| 体裁：Heading 样式 0、12 pt TNR、黑字、行号、双倍行距、行内粗体 0 | 通过 |
| 体裁：表的列见出しと数値セル粗体 0、「・」0、横版、✳ 脚注、Note 0、符号一一对应 | 通过 |
| 体裁：图 600 dpi 实测 | 通过 |
| 体裁：前付け | 不适用（尾崎担当） |
| 体裁：生成 AI 的记述 0、ARS 标记 0、ARS 默认的遗留 0 | 通过 |
| 体裁：拼写统一（米式）、Fig. 统一 | 通过 |
| 体裁：语数 | 本文 2,954 词（第 7 节）；投稿先未定 |
| 数值：正文数值在台账、出所表中同值同位 | 通过（Results 92 个；Introduction 与 Methods 90 个逐段登记） |
| 数值：表脚注的数值在表或图中 | 通过 |
| 数值：同一数值不在两张表 | E1 至 E3（第 6.2 节）；N10 与 E4 按指示改为文字 |
| 数值：分层 n 之和、百分率之和、流程图 | 不适用（无分层计数表与流程图）；S8：2,294 + 1,157 = 3,451 |
| 数值：对象者数一致 | 3,451 与 2,294 在 Introduction、Methods、S8 一致 |
| 数值：点估计在 CI 内、CI 与 p | 通过（UI 的格式同 v4；无 p 值） |
| 数值：同一统计量同值同位 | 通过 |
| 数值：p 值表记、trend 型用语 | 不适用（无 p 值）；trend 型 0 |
| 数值：因果语 0 | 通过（模型研究；「effect of exercise」是模型中的假设参数，Methods 定义为曝露） |
| 数值：要约统计量的形、空セル 0 | 通过 |
| 数值：负号、前导 0、千位逗号 | 通过 |
| 数值：小数位按表统一、百分率舍入一致 | 通过 |
| 内容：Methods 无数值结果 | 通过（Methods 的数字都是设定、输入或日期；结果的值 0） |
| 内容：Results 无方法句、各结果句有表图引用 | 通过 |
| 内容：各解析有目的句；推定对象都在 Results | 通过（段阶 (1) 至 (6) 各以「To …」开头；第 1 节） |
| 内容：Introduction 末两段（不足的列举 → 目的） | 通过（第一、第二；目的为用户原文，未番号化） |
| 内容：目的对应表 | 通过（第 1 节；ars/argument_blueprint_v5.md） |
| 内容：Methods 的曝露与アウトカムの名前与目的一致、段阶顺 | 名前一致；段阶顺为用户指定（第 6.2 节） |
| 内容：Abstract、Discussion、Implications、Limitations 各项 | 不适用 |
| 内容：用语定义与一致 | 通过（第 10 节） |
| 内容：缩写（正文初出展开、表图脚注再展开、check_acronyms） | 通过（complete、No findings） |
| 内容：Limitations 以外无「〜の限界」型 | 通过 |
| 内容：Outcome 与 Variables 的第一句 | 通过 |
| 内容：统计软件只写语言与版本 | 通过（R version 4.5.1） |
| 内容：Ethics、Data availability、Funding、COI | 不适用（title page 为尾崎担当；模型研究） |
| 内容：报告规范的清单在 supplementary，各项有页与节 | 通过（S1；第 1、2 项待 Abstract 与 title page） |
| 内容：题名 | 不适用（title page） |
| 内容：欠测、多重比较、事前登録 | 多重比较一句、计划未登记一句；欠测：模型研究，无个体数据的欠测，按规约「欠測が無かったという記録は書かない」不写 |
| 内容：选定流程图 | 不适用（无对象选定） |
| 内容：图中无题名、面板标签、单位、不只靠颜色、≥ 8 pt | 通过 |
| 内容：图与表无同一结果重复 | 通过 |
| 内容：著者贡献 | 不适用（尾崎担当） |
| 内容：AI 常套语、套话、自我说明、连接词连用 0；破折号、30 词与 150 词 | 通过（第 7 节；例外 I.4） |
| 内容：裸时间词 0、事实句无 may | 通过 |
| 内容：主张强度未变强 | 通过（Results 的改动不改主张；Methods 的 3 处改正都是弱化或准确化） |
| 内容：rebuttal-audit、humanizer、stop-slop | 不适用（非查读对应版；humanizer 在全稿初稿完成后一次） |

## 10. 用语表（v4 沿用，加本版的新语）

| 名称 | 指什么 | 初出 |
|---|---|---|
| maximum affordable cost | 上限（阈值 × ΔQALY − 不含方案费的 Δ医疗费） | Methods, Outcome 第 1 句 |
| recurrence HR with exercise（recurrence HR） | hr0 | Methods, Variables 第 1 句 |
| medical costs avoided | −Δ医疗费（不含方案费） | Methods, Outcome 第 4 句 |
| 95% uncertainty interval (UI) | PSA 1,000 样本的 2.5 与 97.5 百分位 | Methods, Statistical analysis 段阶 (3) |
| main / secondary / reference comparison | 运动 + 化疗 + 帕博利珠单抗 对 化疗 + 帕博利珠单抗 / 运动 + 化疗 对 化疗 / 化疗 + 帕博利珠单抗 对 化疗 | Methods, Study background 第 1 段 |
| fee-schedule-based program、CHALLENGE-based supervised program、remote low-cost program | 三种方案 | Methods, Variables 第 3 段 |
| higher mortality after early recurrence with pembrolizumab | k 外部（早期复发后 k）情景 | Methods, Statistical analysis 段阶 (5) |
| longer survival after progression during neoadjuvant therapy | Elmore 情景 | 同上 |
| one-year net benefit | 一年队列净收益 | Methods, Outcome 第 2 段 |
| Utility values from Japanese populations、the four utility scenarios | 日本人群效用情景；与美、英、澳三行合称 | Methods 段阶 (5)；Results P10 |

金额的写法：正文写「JPY 2,082 thousand」，与表中千日元的显示值同值同位；阈值写「JPY 5 million per QALY」。拼写：米式；图的表记：Fig.

## 11. 文献检索的记录

见 references_v5.md 第 1 节（数据库、检索式原文、年范围、检索日、命中数）与第 2 节（新颖性句与经济评价句所依据的 4 组检索的全部命中的判定）。Scopus：本环境未配置，未检索。

## 12. 过去意图之外戻った箇所（规约第 1.2 节规则 7）

- v5 发现：补充表脚注中输入表的编号（3 处）在编号变更时未随之更新（硬编码的「Supplementary Table S1」）。已改为从 SUPP 取值，并加检查 references_to_input_table_wrong_number；以后每版名指确认。
