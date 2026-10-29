# 作业记录 v9（v9：最后的修改（Implications、D.3、D.5、标题、Abstract），2026-10-27）

## 0. 声明与底本

1. 规约：开工时读了 `Documents/ClaudeCode/WRITING_RULES.md` 全文；交付前从头到尾重读了全文（514 行，第 1–14 节），第 13 节的逐项点检见第 8 节。ARS：intro_title_rhetoric_guide.md 的题名清单与 abstract_writing_guide.md 用于本版的标题与 Abstract；writing_quality_check.md 等的诊断用于改动的段落。nature-figure：图未改，只重跑审查。
2. 段阶：v1 之后的改稿；标题与 Abstract 为用户给定的原文。
3. 底本：`manuscript/archive/v8/`：manuscript_v8.docx c0118e13、tables_v8.docx、figures_v8.docx、supplement_v8.docx（开工时作业树全部文件的 sha256 与 MANIFEST_v8 一致，git 干净）。v8 已移入 archive；作业树 `manuscript/` 下只有 v9、archive（v1 至 v8、ars_v5 至 ars_v9）、code。
4. 指示：「v9：最后的修改（Implications、D.3、D.5、标题、Abstract）」（2026-10-27）的第 0 至 4 条。
5. 做法：本文 manuscript_v9.docx 由 `archive/v8/manuscript_v8.docx` 直接编辑而成（`code/edit_manuscript_v9.py`：核对 v8 docx 的 sha256；按同一文件的文献表把上标番号还原为标记；只改指示的句子、标题与 Abstract 四段；Abstract 的标签与标题后的三个空行不动；新文与指示原文逐字比对）。`number_refs.py` 重编文献号（结果与 v8 相同）。表、图、补充材料用同一套生成代码重新生成；图的 PNG、TIFF 与 v8 逐字节相同。
6. 来源：数值来源与 v8 相同，没有新的解析输出。

产物（`manuscript/v9/`）：manuscript_v9.docx、tables_v9.docx、figures_v9.docx、supplement_v9.docx、本文件、numbers_ledger_v9.md、references_v9.md；辅助：check_v9.md、diff_v8_v9.md、MANIFEST_v9.md、figures/。ARS 的作业记录（citation audit）在交付时移入 `manuscript/archive/ars_v9/`。

投稿先与投稿仕様：投稿先未定；拼写为米式；图的表记为 Fig.；文献为 Vancouver（NLM）、本文初出顺；Abstract 的上限待投稿刊物定下后调整。

## 1. 目的与各节的对应（规约第 2.1 节）

| 目的 | Abstract | Results 的段落 | Discussion | Implications |
|---|---|---|---|---|
| 目的 1 | Objectives；Results 第 1、3–5 句；Conclusions | P1 至 P6、P11 | D.1 第 1–3 句、D.2、D.3、D.6、D.7 | 第 1 段第 1–6 句、第 2 段第 1–2 句 |
| 目的 2 | Results 第 2 句（本版新加） | P7 | D.4 第 4 句 | — |
| 目的 3 | Results 第 6 句前半 | P8、P9、P11 | D.1 第 4 句、D.5 | 第 2 段第 3 句 |
| 目的 4 | Results 第 6 句后半 | P10 | D.4 第 1–3 句 | — |

Abstract 的 Results 现在回答全部四个目的；Objectives 与 Conclusions 写目的 1。

## 2. 本版改动的段落一览（diff_v8_v9.md）

| 位置 | 改动 | 对应的指示 |
|---|---|---|
| 标题 | 「Cost-effectiveness of exercise added to neoadjuvant chemotherapy for triple-negative breast cancer in Japan」（13 词，无冒号） | 第 2 条 |
| Abstract：Methods、Results、Conclusions | 整段换成指示原文（Objectives 与 v8 相同；标签不动） | 第 3 条 |
| Discussion 第 3 段第 2 句 | 「after this regimen」→「after neoadjuvant chemotherapy with pembrolizumab」 | 第 1 条 |
| Discussion 第 5 段 | 删去最后一句（c2h_list 仍在 Introduction 第 3 段引用，文献号不变） | 第 1 条 |
| Implications 第 1 段 | 第 1 句换成两句（新引 kjeldsted2025、schmidt2025；「This analysis adds that …」一句不变） | 第 1 条 |
| 其余各段 | 一字不变；文献号与 v8 相同 | — |

## 3. 表、图与补充材料

- 不变（归一化比较 tables 0、figures 0、supplement 0）。CHEERS 第 1、2 项的位置照旧：Title (p. 1)、Abstract, paragraphs 1 to 4 (pp. 1 to 2)（Word 分页实测，指示第 3 条要求确认）。

## 4. 核对

- 指示第 1 条的确认：kjeldsted2025（Neo-train，Clin Cancer Res 2025）摘要「received supervised high-intensity interval training and progressive resistance training 3 times weekly during 18 to 24 weeks of neoadjuvant chemotherapy」；schmidt2025（BENEFIT，J Sport Health Sci 2025）摘要「patients with breast cancer scheduled for NACT were randomly assigned to supervised resistance training (RT, n = 60) or aerobic training (AT, n = 60) twice weekly during NACT」。都写有新辅助化疗期间有监督的运动，相符，没有停下。
- D.3 新句：licata2025 的五项试验含 KEYNOTE-522，早期（24 个月内）复发所占比例在各试验中为 64.6% 至 82.9%，「with pembrolizumab」也成立。
- Implications 第 1 句：furmaniak2016、courneya2007、vanwaart2015 都是辅助化疗期间，句子写的也是「during adjuvant chemotherapy」（v8 报告的新辅助与辅助的错位不再存在）。
- Abstract 的 16 个数字逐一按出处登记并核对（Table 1、2、3 的显示值，model_spec 的 2% 折现，95% 的定义）：新加的 3,443 是 Table 2 Panel B 次比较的基准值（与 Results 第 7 段同值同位）。不一致 0。15 个在本文中同值同位；192,400 只在 Table 1。
- 不印数字的文字依据（编辑脚本断言，numbers_ledger_v9.md 第 1b 节末）：D.2 第 2 句、D.4 第 2 句、L.2 第 3 句、Abstract Results 第 5 句（持续时间）都仍成立。
- 原著对照（references_v9.md 第 8 节）：本文 102 处（句 × 文献）全部有对照记录，139 条逐字段落全部找到。

## 5. 指示第 4 条要求另报的检查（原文未改）

| 项目 | 结果 |
|---|---|
| 超过 30 词的句 | 本版新文 0（Abstract 最长 29 词；Implications 新两句 27、12 词）。全文 6 句，都在未改动的 Introduction（I.3 的 33、34、44 词与 I.4 的 59、47、36 词） |
| 超过 150 词的段 | 0（最长 R.11 149 词；Implications 第 1 段 119 词；Abstract 各段 28、83、107、35 词） |
| 「current」与「now」 | 全文 0 |

各节之间内容相近的主张（本文 190 句扫描；以下按内容列出，Abstract 与本文的重复不列）：
- 运动在辅助化疗期间改善体能：Introduction 第 2 段第 3 句与 Implications 第 1 句，同引 furmaniak2016、courneya2007、vanwaart2015（本版改写后两处更接近）。
- 新辅助化疗期间有监督运动的试验：Introduction 第 2 段第 5 句（未改变肿瘤大小）与 Implications 第 1 句（已实施），同引 kjeldsted2025、schmidt2025；所说的侧面不同。
- 多数复发发生在早期：Introduction 第 1 段第 4 句与 Discussion 第 3 段第 2 句，同引 licata2025。
- 日本多数患者用帕博利珠单抗：Introduction 第 1 段第 5 句与 Discussion 第 4 段第 5 句，同引 jbcs55。
- 运动的经济评价只针对疲劳、体能或生活质量：Introduction 第 3 段第 1 句与 Discussion 第 6 段第 3 句。
- 帕博利珠单抗方案未被指定为费用对效果评价的对象：Introduction 第 3 段第 4 句与 Implications 第 2 段第 3 句（v8 的三处减为两处）。
- 运动对复发的效应未知：Introduction 第 2 段末句与 Limitations 第 1 段第 1 句。
- 需要 HR 0.425：Results 第 10 段与 Discussion 第 4 段第 2 句（后者写作「more than half」）。

其他报告事项（原文未改）：
- Abstract：253 词（含标签 257 词），比 ARS 英文结构化摘要的标准（150–250 词）多 3 词；投稿刊物定下后再调整。仍以 Objectives 开头，没有 Background。JPY 未展开（v8 的决定，ARS 缩写检查报「Not defined: JPY，5 处」）。192,400 只在 Table 1。
- 标题：13 词，无冒号；研究设计（cost-effectiveness）、对象（triple-negative breast cancer、neoadjuvant chemotherapy）与设定（Japan）都能读出；最重要的概念在前 3 词；没有缩写。title page 与 supplementary 没有题名（title page 为尾崎担当）。

## 6. 检查（check_v9.md）

最重要的四项：
1. 版：`manuscript/` 下只有 v9、archive（v1 至 v8、ars_v5 至 ars_v9）、code；v9 内只有本版文件；ars/ 在交付时移入 archive。通过。
2. 表与图的引用：本文 44 段走查，初出顺为 Supplementary Methods S1、S1、Table 1、S2、Fig. 1、Supplementary Fig. S1、S3、Fig. 2、Table 2、Table 3、Fig. 3、S4 至 S9、Supplementary Fig. S2、S10；五个系列各自 1, 2, 3, …；最大番号 = 实数；supplement 的物理顺序一致。通过。
3. 文献的真伪：DOI 61 篇全部在 doi.org 实测 30x，并与 Crossref 比对；无 DOI 的 16 篇各有到源页面的核对；撤稿 0。通过。
4. 文献的顺序：本文 62 个上标 run，初出顺 1 至 62 无缺；63 至 77 在表、图注与补充材料中按阅读顺序；77 篇全部被引用，表外番号 0；文献号与 v8 完全相同。通过。

docx 回读（走查的母数：manuscript 144 项 265 run、tables 289 项 337 run、figures 14 项、supplement 2,398 项 2,527 run）：
- 全部文字 run 为 Times New Roman 12 pt；黑以外的文字、Heading 样式、空单元格、表外粗体（见出し与 Abstract 标签除外）、含数字的单元格粗体、「・」、以 Note 开头的段落、表外的「—」都是 0。
- 标题：第 1 段，Normal，不加粗；其后空行 3 个。Abstract：标签顺序与格式正确，引用 0，超过 30 词的句 0。见出し与 v8 相同；双倍行距 141/141；行号已设。
- 数字：manuscript 212 个、tables 260 个、figures 30 个、supplement 2,225 个，未登记的都是 0；标题、Abstract、Introduction、Methods 与三节的 114 个数字逐段登记（117 行）；Results 98 个数字都是所引表中的显示值，未改动。
- 三节：新出文献 0；各段引用数 D.1 0、D.2 0、D.3 1、D.4 3、D.5 4、D.6 5、D.7 1、Implications 5 与 0、Limitations 0 与 1；「further research」型 0；Limitations 以外的「limitation」0；与 Results 重复的数字 6/12。
- 文体（本文）：禁用语、前置套话、自我说明、方法句、裸时间词、因果语、破折号、连接词连用都是 0。语数：Introduction 565、Methods 1,494、Results 883、Discussion 492、Implications 174、Limitations 235，本文合计 3,843；Abstract 253（含标签 257）；标题 13。
- ARS check_acronyms.py：本文 complete、No findings；Abstract（单独范围）complete、Not defined: JPY（5 处，v8 的用户决定）。
- 原著对照：本文 102 处与散文 22 处全部有对照记录；139 条逐字段落全部找到。ARS citation-check（ars/citation_audit_v9.md）：照合 77 篇、订正 0、报告事项 6。
- 植入鸣响（本版的编辑脚本；副本写到 scratchpad，交付物与 `_build` 的 sha256 在试验前后不变）：Abstract Results 改一词 → 「text differs from the instruction」；要删的 D.5 末句与 v8 不符 → 断言报错。make_ledger 等其余检查本版未改。
- 图：600 dpi；字号检查 5 张都没有低于 8 pt 的字；碰撞检查 5/5 PASS；validate_figure.py 19 pass、2 warn、0 fail（像素与 v8 相同）。
- Word（COM）打开 4 个 docx 并另存为 PDF，无报错：manuscript 24 页、tables 8 页、figures 3 页、supplement 45 页；第 1 页（标题、空行、Abstract）与 Implications 所在页（第 12 页）目视确认。

## 7. 与 v8 的逐段对照（diff_v8_v9.md）

| 文件 | 原始比较的块 | 归一化后的块 | 内容 | 对应 |
|---|---|---|---|---|
| tables | 0 | 0 | — | — |
| figures | 0 | 0 | — | — |
| supplement | 0 | 0 | — | — |
| manuscript | 7 | 7 | N1 标题；N2 至 N4 Abstract 的 Methods、Results、Conclusions；N5 Discussion 第 3 段；N6 Discussion 第 5 段；N7 Implications 第 1 段 | 第 1、2、3 条 |

意图之外的变化：0。References：77 条逐字、逐号相同。数值：表、图、补充材料的显示值与 v8 相同。

## 8. 第 13 节的逐项点检（规约第 14 节）

title page 为尾崎担当；「不适用」都是这个原因，除非另注。

| 项目 | 结果 |
|---|---|
| 版：作业树只有最新版；开始时 sha256 与 manifest 一致；底本与 sha256 记在开头 | 通过 |
| 版：意图之外戻った段落 0（补充表的脚注、题名、语数、图的解像度、过去戻った箇所） | 通过（补充材料 0 差；图像逐字节相同；指向输入表的 10 处都是 S2；题名按指示更换） |
| 版：数值不变的版与 v(n−1) 数值完全一致 | 通过（表、图、补充材料不变） |
| 版：模板雏形 0；版号与作业注记 0；manifest 更新、旧版移入 archive；解析输出的 sha256 | 通过 |
| 版：差分全部对应指示 | 通过（第 2、7 节） |
| 版：撤回的主张 0 | 通过（v8 的旧标题、旧 Abstract、D.5 末句、Implications 旧第 1 句都不在 v9 中） |
| 版：变更履历与注释 0；ARS 的初稿与 ars/ 0 | 通过 |
| 文献：初出顺、未引用 0、表外番号 0；DOI；著者年引用 0；新规引用与原著对照；citation-check | 通过 |
| 文献：10 年超与自引 | 10 年超 8 篇，自引 0% |
| 文献：新规性句的检索限定 | 例外（v6 起，指向 Supplementary Methods S1） |
| 付番：四系列与补充方法、最大番号、地の文、supplementary 内的顺序、图从 Fig. 1 | 通过 |
| 见出し：六个大见出し与 Abstract 的四个标签、Methods 四个小见出し、规约外的节 0 | 通过 |
| 体裁：Heading 样式 0、12 pt TNR、黑字、行号、双倍行距、行内粗体 0、表的粗体、「・」、横版、✳ 脚注、600 dpi | 通过 |
| 体裁：前付け | 不适用（尾崎担当；标题之后的 3 个空行不动） |
| 体裁：生成 AI 的记述 0、ARS 标记 0；拼写与 Fig. 统一；语数 | 通过；本文 3,843 词，Abstract 253 词；投稿先未定 |
| 数值：本文与抄録的数值同值同位；表脚注的数值 | 通过（Abstract 的 192,400 只在 Table 1） |
| 数值：同一数值不在两张表 | E1 至 E3 |
| 数值：对象者数、点估计在 UI 内、p 值、因果语、负号、小数、千位逗号 | 通过 |
| 内容：Methods、Results 的各项 | 通过（未改动） |
| 内容：Introduction 末两段 | 例外（v6 起） |
| 内容：目的对应表 | 通过（第 1 节） |
| 内容：Abstract 的目的与结论对应本文的目的 | Objectives 与 Conclusions 写目的 1；Results 回答目的 1–4 |
| 内容：Discussion 各项 | 同 v8（D.3 名指表；第 1 段答目的 1、3；重合 0.5 以上的句 0） |
| 内容：临床医生改变什么 | 有（Implications 第 2 句：在检验对复发的效应期间即可提供运动） |
| 内容：Implications 名指结果、无更强的主张与新数字 | 通过 |
| 内容：用语定义、缩写 | 本文通过；Abstract 的 JPY 未展开（v8 的用户决定） |
| 内容：Limitations | 通过（未改动） |
| 内容：报告规范的清单 | 通过（CHEERS 第 1、2 项的页码确认） |
| 内容：题名 | 研究设计、对象、设定可读出；13 词；无冒号 |
| 内容：欠测、多重比较、事前登録 | 多重比较句按 v6 的指示删去；计划未登记一句 |
| 内容：图、图与表无重复 | 通过 |
| 内容：AI 常套语、套话、自我说明、连接词 0；破折号、30 词与 150 词 | 0；30 词超 6 句（Introduction，未改动）；150 词超 0 |
| 内容：裸时间词 0、事实句无 may | 通过 |
| 内容：主张强度未变强 | 通过（Abstract 删去「Even a small effect on recurrence would pay for a program」；Implications 新句把体能的依据限定在辅助化疗期间） |
| 内容：rebuttal-audit、humanizer、stop-slop | 不适用 |

## 9. 用语表、文献检索、戻り

- 用语：Abstract 的「The exercise effect」指本文的 recurrence HR with exercise；其余与 v8 相同。
- 文献检索：与 v6 至 v8 相同；本版没有新检索。
- 过去意图之外戻った箇所：v5 发现的补充表脚注中输入表的编号，本版名指确认，10 处都是 S2。本版未发现新的戻り。
