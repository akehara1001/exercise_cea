# 作业记录 v8（v8：最后的文字修改；插入标题与 Abstract，2026-10-27）

## 0. 声明与底本

1. 规约：开工时读了 `Documents/ClaudeCode/WRITING_RULES.md` 全文；交付前从头到尾重读了全文（514 行，第 1–14 节），第 13 节的逐项点检见第 9 节。ARS：academic-paper 的 abstract_writing_guide.md（结构化摘要的五要素、英文 150–250 词、摘要内无引用与未定义缩写）与 intro_title_rhetoric_guide.md 的题名清单用于本版的标题与 Abstract；writing_quality_check.md 等其余文件的诊断用于改动的段落。nature-figure：图未改，只重跑审查。
2. 段阶：v1 之后的改稿；按指示插入标题与 Abstract（规约第 1 节：Abstract 在本文完成后最后写；这次是用户给定的原文）。
3. 底本：`manuscript/archive/v7/`：manuscript_v7.docx 0f2c803f、tables_v7.docx、figures_v7.docx、supplement_v7.docx（开工时作业树全部文件的 sha256 与 MANIFEST_v7 一致，git 干净）。v7 已移入 archive；作业树 `manuscript/` 下只有 v8、archive（v1 至 v7、ars_v5 至 ars_v8）、code。
4. 指示：「v8：最后的文字修改；插入标题与 Abstract」（2026-10-27）的第 0 至 4 条，以及开工后的两项用户决定（第 4 节）。
5. 做法：本文 manuscript_v8.docx 由 `archive/v7/manuscript_v7.docx` 直接编辑而成（`code/edit_manuscript_v8.py`：核对 v7 docx 的 sha256；按同一文件的文献表把上标番号还原为标记；只改指示所列的句子；在 Introduction 之前插入标题、三个空行与 Abstract；新文与指示原文逐字比对，两项用户决定在脚本中显式套用）。`number_refs.py` 重编文献号（结果与 v7 相同）。表、图、补充材料用同一套生成代码重新生成；图的 PNG、TIFF 与 v7 逐字节相同。
6. 来源：数值来源与 v7 相同，没有新的解析输出。

产物（`manuscript/v8/`）：manuscript_v8.docx、tables_v8.docx、figures_v8.docx、supplement_v8.docx、本文件、numbers_ledger_v8.md、references_v8.md；辅助：check_v8.md、diff_v7_v8.md、MANIFEST_v8.md、figures/。ARS 的作业记录（citation audit）在交付时移入 `manuscript/archive/ars_v8/`。

投稿先与投稿仕様：投稿先未定；拼写为米式；图的表记为 Fig.；文献为 Vancouver（NLM）、本文初出顺；Abstract 的上限待投稿刊物定下后调整（指示第 3 条）。

## 1. 目的与各节的对应（规约第 2.1 节）

目的（Introduction 第 4 段，不变）：目的 1 最大可负担费用及其随效应大小与持续时间的变化；目的 2 加入单用化疗时的同一费用；目的 3 帕博利珠单抗在日本的成本效果；目的 4 与帕博利珠单抗同 QALY 增益的运动效应。

| 目的 | Abstract | Results 的段落 | Discussion | Implications |
|---|---|---|---|---|
| 目的 1 | Objectives；Results 第 1–4 句；Conclusions | P1 至 P6、P11 | D.1 第 1–3 句、D.2、D.3、D.6、D.7 | 第 1 段第 1–5 句、第 2 段第 1–2 句 |
| 目的 2 | — | P7 | D.4 第 4 句 | — |
| 目的 3 | Results 第 5 句前半 | P8、P9、P11 | D.1 第 4 句、D.5 | 第 2 段第 3 句 |
| 目的 4 | Results 第 5 句后半 | P10 | D.4 第 1–3 句 | — |

D.4 第 5 句（2024 年多数患者用帕博利珠单抗 → 主比较对实践最重要）对应目的 1 的设定。Limitations 两段对应全部目的。Abstract 的 Objectives 只写目的 1，目的 2 不在 Abstract 中（用户原文；第 6 节）。

## 2. 本版改动的段落一览（diff_v7_v8.md）

| 位置 | 改动 | 对应的指示 |
|---|---|---|
| 稿件开头 | 标题（普通段落，与正文同字号，不加粗，不用 Heading 样式）；其后三个空行，留给作者、所属与责任作者（尾崎先生填） | 第 2 条 |
| 标题之后、Introduction 之前 | Abstract：Objectives、Methods、Results、Conclusions 四个标签加粗独占一行，正文从下一行起 | 第 3 条 |
| Results 第 2 段 | 第 2 句拆成两句（指示原文） | 第 1 条 |
| Discussion 第 3 段 | 第 2、3 句换成一句（licata2025） | 第 1 条 |
| Discussion 第 4 段 | 最后两句换成一句（jbcs55） | 第 1 条 |
| Discussion 第 6 段 | 整段换成指示的原文（4 句） | 第 1 条 |
| Implications 第 1 段 | 第 1、2 句换成指示的原文（第 2 句与 v7 相同）；mijwel2018 按用户决定删去 | 第 1 条与决定 1 |
| Limitations 第 2 段 | 「Longer survival with current treatment」→「Longer survival with the treatments used in 2026」 | 第 1 条 |
| 其余各段 | 一字不变；文献号也与 v7 相同 | — |

## 3. 表、图与补充材料的改动

- Supplementary Table S1（CHEERS）：第 1 项「Title page」→「Title (p. 1)」，第 2 项「Abstract」→「Abstract, paragraphs 1 to 4 (pp. 1 to 2)」（指示第 3 条）。其余 20 项只是页码：标题与 Abstract 插在前面，本文后移一页左右（例：Introduction pp. 1 to 2 → pp. 2 to 3）。
- 表、图、补充材料的其他内容：不变（归一化比较 tables 0、figures 0；supplement 22 块都是 CHEERS 的位置格）。
- 题名不在 supplementary 与 title page 中（两者在 v7 都没有题名；title page 为尾崎担当），本版不加。

## 4. 开工后的两项用户决定（2026-10-27）

1. Implications 第 1 句：指示原文以 mijwel2018 支持「known benefits on fitness」。mijwel2018（OptiTrain，Breast Cancer Res Treat 2018;168:79-93）摘要只报告癌症相关疲劳、HRQoL 与症状；PMC5847033 全文中 fitness 一词只出现在引言、讨论与参考文献，本研究没有测体能。询问后用户选「删去 mijwel2018」。该句只引 furmaniak2016、courneya2007、vanwaart2015；mijwel2018 仍在 Introduction 第 2 段引用（疲劳），文献号不变。
2. Abstract 的三处与正文不完全一致，询问后用户只选「定义补全」：Methods 末句「minus incremental medical costs」→「minus incremental medical costs other than the program cost」（与 Methods, Outcome 的定义一致）。另两处保持原文：Results 末句「exercise would need an HR of 0.425」（Table 3 Panel C 的定义是「exercise added to chemotherapy alone」）；Abstract 中的 JPY 不展开。

## 5. 数字与文字依据的核对（numbers_ledger_v8.md 第 1、1b 节）

- 新句与 Abstract 的数字逐一按出处登记并核对：Results 第 2 段（S5 的 1、389 [238, 570]、10、3,898 [2,388, 5,713]）；D.4 的 2024（JBCS 数值文件）；D.6 的 5（chan2026「5-year time horizon」）；L.2 的 2026（Table 1 的价格年度）；Abstract 15 个数字（Table 1、2、3 的显示值，model_spec 的 2% 折现，95% 的定义）。不一致 0。
- Abstract 的 15 个数字中 14 个在本文（Introduction 至 Limitations）中同值同位；192,400（fee-schedule-based program 的费用）只在 Table 1（与 S2）中，本文散文没有（第 6 节）。编辑脚本断言：Abstract 的每个数字须在本文或表中（植入的「99」会报错，第 7 节）。
- 不印数字的文字依据（编辑脚本断言，numbers_ledger_v8.md 第 1b 节末）：沿用 v7 的三项（D.2 第 2 句、D.4 第 2 句、L.2 第 3 句）都仍成立；新加 Abstract Results 第 4 句「The duration of the effect changed the maximum affordable cost more than any cost input」：持续时间使上限在 1,772 至 3,404 千日元之间，Fig. 3 的单因素范围为 2,617 至 2,836 千日元，成立。
- D.4 新句「most patients in Japan received pembrolizumab with neoadjuvant chemotherapy in 2024」：2,294 / 3,451 = 66%（JBCS 数值文件），成立。
- 原著对照（references_v8.md 第 8 节）：本文 101 处（句 × 文献）全部有对照记录，138 条逐字段落全部找到。

## 6. 指示第 4 条要求另报的检查（原文未改）

| 项目 | 结果 |
|---|---|
| 超过 30 词的句 | 本版新文 0（最长：L.2 第 2 句 30 词，即本版改了措辞的一句；Abstract 最长 29 词）。全文 6 句，都在未改动的 Introduction（I.3 的 33、34、44 词与 I.4 的 59、47、36 词，v6 起的用户原文） |
| 超过 150 词的段 | 0（最长 R.11 149 词；Abstract 各段 28、91、102、46 词） |
| 「current」与「now」 | 全文 0（标题、Abstract 与本文都扫过）；v7 的两处已按指示改掉一处，另一处（D.4「current practice」）随 D.4 最后两句一起换掉 |
| 各节之间重复的主张 | 见下 |

各节之间内容相近的主张（扫描本文 190 句：不同节之间实词重合 0.40 以上的 14 对多为 Methods 的定义与 Results 的同一术语；以下按内容人工列出）：
- 「多数复发发生在早期」：Introduction 第 1 段第 4 句（24 个月）与 Discussion 第 3 段第 2 句，同引 licata2025。
- 「日本多数患者用帕博利珠单抗」：Introduction 第 1 段第 5 句（3,451 例中 2,294 例）与 Discussion 第 4 段第 5 句，同引 jbcs55。
- 「运动的经济评价只针对疲劳、体能或生活质量」：Introduction 第 3 段第 1 句与 Discussion 第 6 段第 3 句，同引三篇综述。
- 「运动对体能有益」：Introduction 第 2 段第 3 句与 Implications 第 1 段第 1 句。
- 「帕博利珠单抗方案未被指定为日本费用对效果评价的对象」：Introduction 第 3 段第 4 句、Discussion 第 5 段第 3 句、Implications 第 2 段第 3 句，三处。
- 「运动效应对复发未知」：Introduction 第 2 段末句与 Limitations 第 1 段第 1 句。
- 「需要 HR 0.425」：Results 第 10 段与 Discussion 第 4 段第 2 句（Discussion 写作「more than half」，不重复数字）。
- Abstract 与本文的重复属于摘要的性质，不列。

其他报告事项（原文未改）：
- Abstract：267 词（含标签 271 词）。ARS 的英文结构化摘要标准为 150–250 词；按指示，投稿刊物定下后再按上限调整。ARS 的五要素中没有 Background（以 Objectives 开头）。Abstract 中 JPY 未展开（ARS 缩写检查报「Not defined: JPY，4 处」；用户决定保持）。192,400 只在 Table 1。Abstract 的目的只写目的 1，Results 写了目的 1、3、4，目的 2 不在 Abstract 中。
- 标题：19 词（ARS 题名清单的目安为 15 词以内）；有一个冒号（「…: a cost-effectiveness analysis」，规约第 4 节避免以冒号叠加短语）。研究设计、对象集团与设定（日本）都能从题名读出；没有缩写。
- Discussion 第 3 段第 2 句「after this regimen」：本段之内没有先行词（上一次出现方案名是 D.1 第 2 句的 chemotherapy plus pembrolizumab）。
- Implications 第 1 句：所引三篇的体能改善都是辅助化疗期间的结果，句子说的是新辅助化疗期间。

## 7. 检查（check_v8.md）

最重要的四项：
1. 版：`manuscript/` 下只有 v8、archive（v1 至 v7、ars_v5 至 ars_v8）、code；v8 内只有本版文件；ars/ 在交付时移入 archive。通过。
2. 表与图的引用：本文 44 段（Introduction 4、Methods 18、Results 11、Discussion 7、Implications 2、Limitations 2）走查，取出的初出顺为 Supplementary Methods S1、S1、Table 1、S2、Fig. 1、Supplementary Fig. S1、S3、Fig. 2、Table 2、Table 3、Fig. 3、S4 至 S9、Supplementary Fig. S2、S10。五个系列各自 1, 2, 3, …；最大番号 = 实数；supplement 的物理顺序与初出顺一致。Abstract 不引表图。通过。
3. 文献的真伪：DOI 61 篇全部在 doi.org 实测 30x，并与 Crossref 比对；无 DOI 的 16 篇各有到源页面的核对；撤稿 0。通过。
4. 文献的顺序：本文 62 个上标 run，初出顺 1 至 62 无缺；表、图注、补充材料中新出的 63 至 77 按阅读顺序；77 篇全部被引用，表外番号 0。文献号与 v7 完全相同。通过。

docx 回读（走查的母数：manuscript 144 项 265 run、tables 289 项 337 run、figures 14 项、supplement 2,398 项 2,527 run）：
- 全部文字 run 为 Times New Roman 12 pt；黑以外的文字、Heading 样式、空单元格、表外粗体（见出し与 Abstract 标签除外）、含数字的单元格粗体、「・」、以 Note 开头的段落、表外的「—」都是 0。
- 标题：第 1 段，Normal 样式，不加粗；其后空行 3 个；19 词。
- 见出し：Abstract 的 Objectives、Methods、Results、Conclusions，以及 Introduction、Methods、Study background、Outcome、Variables、Statistical analysis、Results、Discussion、Implications、Limitations、References；双倍行距 141/141；行号已设。
- Abstract：标签顺序与格式正确，各标签之后紧接其正文；文献引用 0；超过 30 词的句 0；禁用语、因果语、裸时间词 0。
- 数字：manuscript 211 个、tables 260 个、figures 30 个、supplement 2,225 个，未登记的都是 0。标题、Abstract、Introduction、Methods 与三节的 113 个数字逐段登记（116 行）；Results 98 个数字都是所引表中的显示值；Results 每段以表或图开头 11/11；结果句无引用依据的 0。
- 三节的检查：新出文献 0；各段引用数 D.1 0、D.2 0、D.3 1、D.4 3、D.5 5、D.6 5、D.7 1、Implications 3 与 0、Limitations 0 与 1；「further research」型 0；Limitations 以外的「limitation」0；与 Results 重复的数字 6/12（1.1、4.2、8.6、2024 两处，以及 D.6 的「5 years」与 Results 的「JPY 5 million」数字相同）。
- 文体（本文）：禁用语、前置套话、自我说明、方法句、裸时间词、因果语、破折号、连接词连用都是 0；may 2 处与 suggests 1 处（推断）。语数：Introduction 565、Methods 1,494、Results 883、Discussion 509、Implications 167、Limitations 235，本文合计 3,853；Abstract 267（含标签 271）；标题 19。
- ARS check_acronyms.py：本文 coverage complete，No findings；Abstract（单独范围）coverage complete，Not defined: JPY（4 处，用户决定）。
- 原著对照：本文 101 处与散文 22 处全部有对照记录；138 条逐字段落全部找到。
- ARS citation-check（ars/citation_audit_v8.md，交付时移入 archive/ars_v8）：照合 77 篇、订正 1（mijwel2018，用户决定）、报告事项 7。
- 新检查与鸣响（规约第 13 节；植入只在 scratchpad 的副本上，交付物与 `_build` 的 sha256 在试验前后不变）：
  - make_ledger（副本）：标题加粗 → title_plain_normal_not_bold = False；Abstract 的 Results 与 Conclusions 标签对调 → labels_as_specified = False；Abstract 中加一个上标文献号 → citations_in_abstract = 1；删去一个空行 → empty_lines_after_title = 2。第一项最初使 make_ledger 在断言处中止（加粗的标题被当成见出し），已改为第 1 段固定视为标题、不进见出し的识别，改后正常报出。
  - edit_manuscript_v8.py（副本，写到 scratchpad、在写台账前停止）：在 Abstract 中植入一个本文与表中都没有的数字 99 → 断言报错 ('A.4', '99')。
  - make_supplement.py（副本）：段落图中没有标题段 → 「the manuscript has no title paragraph」。
- 构建代码的两处适配（为空行）：word_pages.py 跳过空段落再与段落图对应；make_references_doc.py 把 number_refs.py 记录的段落序号换算为跳过空行后的序号（首次引用位置因此正确：dent2007 在 I.1、ax2023 在 I.3）。
- 图：Fig. 1–3、Fig. S1–S2 为 600 dpi（插入后实测）；字号检查 5 张都没有低于 8 pt 的字；碰撞检查 5/5 PASS；validate_figure.py 19 pass、2 warn、0 fail（像素与 v7 相同）。
- Word（COM）打开 4 个 docx 并另存为 PDF，无报错：manuscript 24 页、tables 8 页、figures 3 页、supplement 45 页；第 1、2 页目视：标题（第 1–2 行）、空行（第 3–5 行）、Abstract 的标签与正文、Introduction 的开头。

## 8. 与 v7 的逐段对照（diff_v7_v8.md）

| 文件 | 原始比较的块 | 归一化后的块 | 内容 | 对应 |
|---|---|---|---|---|
| tables | 0 | 0 | — | — |
| figures | 0 | 0 | — | — |
| supplement | 22 | 22 | CHEERS 第 1、2 项写入标题与 Abstract 的位置；其余 20 格只是页码后移 | 第 2、3 条的结果 |
| manuscript | 6 | 6 | N1 插入标题与 Abstract（9 项）；N2 Results 第 2 段；N3 Discussion 第 3、4 段；N4 Discussion 第 6 段；N5 Implications 第 1 段；N6 Limitations 第 2 段 | 第 1、2、3 条与两项决定 |

意图之外的变化：0。References：77 条逐字、逐号相同。数值：表、图、补充材料的显示值与 v7 相同。

## 9. 第 13 节的逐项点检（规约第 14 节）

title page 为尾崎担当；下表中「不适用」都是这个原因，除非另注。

| 项目 | 结果 |
|---|---|
| 版：作业树只有最新版；开始时 sha256 与 manifest 一致；底本与 sha256 记在开头 | 通过 |
| 版：意图之外戻った段落 0（补充表的脚注、题名、语数、图的解像度、过去戻った箇所） | 通过（补充表脚注不变；图像逐字节相同；指向输入表的 10 处都是 S2；题名为本版新加） |
| 版：数值不变的版与 v(n−1) 数值完全一致 | 通过（表、图、补充材料的显示值不变） |
| 版：模板雏形 0；版号与作业注记 0 | 通过（[TO CONFIRM] 0 件；前付内容是空行，没有占位文字） |
| 版：manifest 更新、旧版移入 archive；解析输出的 sha256 | 通过 |
| 版：差分全部对应指示 | 通过（第 2、3、8 节） |
| 版：撤回的主张 0 | 通过（v7 的 D.3 第 2、3 句、D.4 第 5、6 句、D.6、Implications 第 1 句的旧文都不在 v8 中） |
| 版：变更履历与注释 0；ARS 的初稿与 ars/ 0 | 通过 |
| 文献：初出顺、未引用 0、表外番号 0；DOI；著者年引用 0 | 通过 |
| 文献：新规引用全部与原著对照 | 通过（第 5 节；mijwel2018 的不符经用户决定删去） |
| 文献：citation-check 的报告 | 通过（ars/citation_audit_v8.md） |
| 文献：10 年超与自引 | 10 年超 8 篇，自引 0% |
| 文献：新规性句的检索限定 | 例外（v6 起，指向 Supplementary Methods S1） |
| 付番：四系列与补充方法、最大番号、地の文、supplementary 内的顺序、图从 Fig. 1 | 通过 |
| 见出し：六个大见出し（加 Abstract 的四个标签）、Methods 四个小见出し、规约外的节 0 | 通过（Abstract 为本版按指示新加） |
| 体裁：Heading 样式 0、12 pt TNR、黑字、行号、双倍行距、行内粗体 0、表的粗体、「・」、横版、✳ 脚注、600 dpi | 通过 |
| 体裁：前付け | 不适用（尾崎担当；标题之后留了 3 个空行） |
| 体裁：生成 AI 的记述 0、ARS 标记 0；拼写与 Fig. 统一 | 通过 |
| 体裁：语数 | 本文 3,853 词，Abstract 267 词；投稿先未定 |
| 数值：本文与抄録的数值在台账、出所表中同值同位 | 通过（Abstract 的 192,400 只在 Table 1，第 6 节） |
| 数值：同一数值不在两张表 | E1 至 E3 |
| 数值：对象者数、点估计在 UI 内、p 值、因果语、负号、小数、千位逗号 | 通过 |
| 内容：Methods 无结果；Results 无方法句、各结果句有依据、按目的顺且段首名指表图 | 通过 |
| 内容：Introduction 末两段 | 例外（v6 起） |
| 内容：目的对应表 | 通过（第 1 节） |
| 内容：Abstract 的目的与结论对应本文的目的 | 部分（Abstract 的目的写目的 1；结论答目的 1；Results 含目的 3、4；目的 2 不在 Abstract 中） |
| 内容：Discussion 段首名指结果、第 1 段答各目的、不足各一次、无重复 Results 的段、引用在中段、无一般论 | 同 v7（D.3 名指表；第 1 段答目的 1、3；不足两项都有回应；重合 0.5 以上的句 0） |
| 内容：临床医生改变什么 | 有（Implications 第 1 句：在新辅助化疗期间提供运动，同时检验对复发的效应） |
| 内容：Implications 名指结果、无更强的主张与新数字 | 通过 |
| 内容：用语定义、缩写 | 本文通过；Abstract 的 JPY 未展开（用户决定） |
| 内容：Limitations 以外无「〜の限界」型；各限界的影响 | 通过 |
| 内容：Outcome 与 Variables 的第一句、统计软件 | 通过 |
| 内容：Ethics 等、著者贡献 | 不适用（title page） |
| 内容：报告规范的清单在 supplementary，各项有页与节 | 通过（第 1、2 项本版补上页码） |
| 内容：题名 | 研究设计、对象集团、设定可读出；19 词与冒号见第 6 节；supplementary 与 title page 没有题名（v7 起即无，title page 为尾崎担当） |
| 内容：欠测、多重比较、事前登録 | 多重比较句按 v6 的指示删去；计划未登记一句 |
| 内容：图（题名、面板、单位、配色、≥ 8 pt）、图与表无重复 | 通过 |
| 内容：AI 常套语、套话、自我说明、连接词 0；破折号、30 词与 150 词 | 0；30 词超 6 句（都在未改动的 Introduction）；150 词超 0 |
| 内容：裸时间词 0、事实句无 may | 通过（current 与 now 全文 0） |
| 内容：主张强度未变强 | 改动句为用户原文；「Even a small effect on recurrence would pay for a program」与 D.1 的「only slightly」同等 |
| 内容：rebuttal-audit、humanizer、stop-slop | 不适用 |

## 10. 用语表（v7 沿用；本版的变化）

本版新增：Abstract 中「hazard ratio (HR)」「quality-adjusted life year (QALY)」在 Abstract 内展开；「uncertainty interval」写全称（本文为 95% UI）；「A program priced from the medical fee schedule」指本文的 fee-schedule-based program；「the treatments used in 2026」（Limitations）替代 v7 的「current treatment」。其余与 v6、v7 相同。

## 11. 文献检索的记录

与 v6、v7 相同（references_v8.md 第 1、2 节；新颖性句的检索式在 Supplementary Methods S1）。本版只为核对 mijwel2018 取了其 PMC 全文（PMC5847033，Europe PMC；XML 不放入仓库），没有新检索。

## 12. 过去意图之外戻った箇所（规约第 1.2 节规则 7）

- v5 发现的补充表脚注中输入表的编号：本版名指确认，10 处都是 S2。
- 本版未发现新的戻り。
