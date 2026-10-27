# 作业记录 v6（执笔第 4 步 v6：Introduction、Methods、Results 的修改；插入 Discussion、Implications、Limitations，2026-10-27）

## 0. 声明与底本

1. 规约：开工时读了 `Documents/ClaudeCode/WRITING_RULES.md` 全文；交付前从头到尾重读了全文（514 行，第 1–14 节），第 13 节的逐项点检见第 9 节。ARS：academic-paper 的 SKILL.md（Anti-Patterns、Quality Standards）、draft_writer_agent.md（Step 1–3、Quality Gates）、citation_compliance_agent.md（检查清单与报告格式）、writing_quality_check.md、academic_writing_style.md（Medicine / Health 与时制表）、writing_judgment_framework.md、intro_title_rhetoric_guide.md。nature-figure：图未改，只重跑审查。
2. 段阶：v1 之后的改稿（规约第 1 节第 6 步，ARS 按第 1.6 节使用）。Discussion、Implications、Limitations 是用户给定的原文，照插；Abstract 按指示不写。
3. 底本：`manuscript/archive/v5/`：manuscript_v5.docx 3bc70868、tables_v5.docx e8365200、figures_v5.docx e1ea15eb、supplement_v5.docx 76ddc2ed（开工时作业树全部文件的 sha256 与 MANIFEST_v5 一致，git 干净）。v5 已移入 archive；作业树 `manuscript/` 下只有 v6、archive（v1 至 v5、ars_v5、ars_v6）、code。
4. 指示：「执笔第 4 步（v6）」（2026-10-27）的第 0 至 6 条。
5. 做法：
   - 本文 manuscript_v6.docx 由 `archive/v5/manuscript_v5.docx` 直接编辑而成（规约第 1.2 节规则 2）：`code/edit_manuscript_v6.py` 打开 v5 的 docx（先核对其 sha256 与 MANIFEST_v5 一致），按同一文件的文献表把上标番号还原为文献标记，只改指示所列的句子，在 Results 之后插入三节；`number_refs.py` 按阅读顺序重编文献号并重写 References。v5 的 docx、段落图与台账三者先互相核对一致才开始编辑。
   - 用户原文以常量存于脚本中，插入的文本与之逐字比对（CC 补写的两处除外，见第 4 节）。
   - 表、图、补充材料用同一套生成代码重新生成（与 v3 至 v5 相同）；图的 PNG、TIFF 与 v5 逐字节相同。
6. 来源：数值来源与 v5 相同，没有新的解析输出；Discussion 的数字全部取自表、图、补充材料的显示值，另有所引文献摘要与 JBCS 数值文件（第 5 节）。

产物（`manuscript/v6/`）：manuscript_v6.docx、tables_v6.docx、figures_v6.docx、supplement_v6.docx、本文件、numbers_ledger_v6.md、references_v6.md；辅助：check_v6.md、diff_v5_v6.md、MANIFEST_v6.md、figures/。ARS 的作业记录（citation audit）在交付时移入 `manuscript/archive/ars_v6/`。

投稿先与投稿仕様：投稿先未定；拼写为米式；图的表记为 Fig.；文献为 Vancouver（NLM）、本文初出顺。

## 1. 目的与各节的对应（规约第 2.1 节）

目的（Introduction 第 4 段，用户原文）：目的 1（主）最大可负担费用及其随效应大小与持续时间的变化；目的 2（副 a）加入单用化疗时的同一费用；目的 3（副 b）帕博利珠单抗在日本的成本效果；目的 4（副 c）与帕博利珠单抗同 QALY 增益的运动效应。

| 目的 | Introduction 的不足（v6 第 3 段） | Statistical analysis 的段阶 | Results 的段落 | Discussion 的段落 | Implications 的句 |
|---|---|---|---|---|---|
| 目的 1 | 第 1–3 句（运动的经济评价只对试验中测得的效应计价；新辅助期间的经济评价未检出；效应未知时可算最大可负担费用） | (1) 至 (6) | P1 至 P5、P10 | D.1、D.2、D.3、D.6、D.7 | 第 1–5 句 |
| 目的 2 | 同上 | (2)、(3) | P6 | D.5 第 3 句 | — |
| 目的 3 | 第 4 句（KEYNOTE-522 方案的分析不来自日本，日本未指定为费用对效果评价的对象） | (2) 至 (5) | P7、P8、P10 | D.4 | 第 6 句 |
| 目的 4 | 同上 | (2) | P9 | D.5 第 1、2、4 句 | — |

Limitations 的 8 句：第 1–3 句与第 6 句对应目的 1；第 4、5、7 句对应全部目的（生存模型与效用）；第 8 句对应目的 1 的一年净收益。对应不上的段、句：0。

## 2. 本版改动的段落一览（diff_v5_v6.md；规约第 12 节第 5 项）

| 位置 | 改动 | 对应的指示 |
|---|---|---|
| Introduction 第 1 段第 1 句 | 「is confined to the first 5 years」→「is concentrated in the first 5 years」 | 第 1 条 |
| Introduction 第 3 段 | 整段换成指示的原文（4 句）；文献键换成番号 | 第 1 条 |
| Introduction 第 4 段 | 保留目的两句；删去检索句与 Phys-Can 句；末尾加指示的一句 | 第 1 条 |
| Methods, Statistical analysis 末段 | 删去多重比较句，只留「All analyses were performed in R version 4.5.1.」 | 第 2 条 |
| Results 第 1 段末句 | 「Each further point added about the same amount (Supplementary Table S5).」→「An increase of 10 percentage points gave JPY 3,898 thousand (95% UI [2,388, 5,713]; Supplementary Table S5).」（S5 路径 B、主比较、500 万日元/QALY、pCR +10 个百分点） | 第 3 条 |
| Results 第 5 段第 1 句 | 「the 3,451 patients a year in Japan who would be eligible」→「the 3,451 patients registered in 2024 who received neoadjuvant chemotherapy for stage II or III TNBC」 | 第 3 条 |
| Results 之后 | 插入 Discussion（7 段）、Implications（1 段）、Limitations（1 段），大见出し各一，无小见出し | 第 5 条 |
| References | 77 条不变（条目文本逐字相同）；ax2023 由 39 号移到 26 号，原 26–38 号顺延（Phys-Can 句移入第 3 段的结果） | 第 1、5 条（按初出顺重排） |
| 本文其余各段 | 只有文献号随之变化（Methods 中引 huang2023、kwong2024 等的句） | 同上 |

## 3. 表、图与补充材料的改动

- Supplementary Table S10：行名「Utility value set: Australia」→「Australian reimbursement submission」（N11，指示第 4 条；照指示原文，整个行名换掉）。
- Supplementary Methods S1：新加小节「Literature searches」（指示第 1 条：检索的数据库、期间、日期与检索式移入）。内容：三组检索（novelty、novelty_variants、novelty_chemo，即 v5 新颖性句所依据的检索）在 PubMed 与 Europe PMC 的运行日（2026-10-26）、出版年范围（2000–2026）、各组检索的范围一句、「每条记录读了题名和摘要」一句，以及 6 条检索式原文（取自 refs/searches/*.json，未手打）。标题改为「Supplementary Methods S1. Literature searches, survival model, validation and probabilistic sampling」。原有 16 段逐字不变（与 v5 逐段比对）。
- 补充材料的物理顺序：Supplementary Methods S1 的初出移到 Introduction 第 3 段（在 Methods 引 S1 CHEERS 之前），按第 7.1 节规则 8（物理顺序与本文初出顺一致）移到补充材料最前（第 1 页起，纵版）。编号不变。
- Supplementary Table S1（CHEERS）：第 26 项（Study findings, limitations, generalisability, and current knowledge）的位置由「Discussion; Limitations」改为段落与页码（Discussion, paragraphs 1 to 7 (pp. 9 to 11); Limitations, paragraph 1 (p. 12)）；第 11 项的页码随本文分页由 pp. 3 to 4 变为 p. 3。其余各项不变。第 1、2 项仍为「Title page」「Abstract」。
- 表与图：内容不变（归一化比较 0 块）；只有文献号随重排变化。

## 4. 插入的三节与 CC 补写的两句

- 原文照插：Discussion 7 段、Implications、Limitations 的每一句都由脚本与指示原文逐字比对（文献键 → 番号；只有两处 CC）。比对用植入的一词之差试过会报错（第 7 节）。
- D.4 第 2 句（指示：按四篇摘要各自的结论补一句）：「Analyses of the same regimen from the United States, Hong Kong, Switzerland and Egypt[28–31] found it cost-effective, with ICERs below the threshold used in each setting.」四篇摘要的结论都是「划算」，ICER 都低于各自使用的阈值（美国：低于所有常用的支付意愿阈值；香港：低于 3 倍人均 GDP；瑞士：低于 10 万瑞士法郎/QALY；埃及：低于 2022 年埃及的阈值）。不加数字。依据的原句在 references_v6.md 第 9 节。
- D.6 第 3 句（指示：按摘要补一句其结论）：「The structured exercise program was less costly and more effective than health education materials, and cancer recurrence or new malignancy and anticancer therapy were the major cost drivers[46].」依据：chan2026 摘要「The SEP was less costly and more effective than HEM.」「Major cost drivers were cancer recurrence or new malignancy and anticancer therapy.」。句末加引了 chan2026，使该句的出处可以追溯。

## 5. Discussion、Implications、Limitations 的数字核对（numbers_ledger_v6.md 第 1b 节）

41 个数字逐一按出处登记并核对：表的显示值 24 个，补充材料（含 Fig. 3 与 Supplementary Fig. S2 的值所在的 S9、补充方法与图注的定义）11 个，JBCS 数值文件 5 个（2,294、3,451、2024 两处、47%），所引文献摘要 1 个（licata2025 的 24 个月）。不一致：0，没有停下。需要说明的三处：
- D.2 的 702：Supplementary Table S6 显示的是增量医疗费 −702；文中为「Medical costs avoided」，按 Methods（Outcome）的定义是其符号反转，同值同位。
- D.3「no input moved this cost outside JPY 2,617 thousand to 2,836 thousand (Fig. 3)」：Fig. 3 的值所在的 Supplementary Table S9 中，主比较 HR 0.85 上限的全部 42 个值（21 个输入 × 下限、上限）最小为 D05 下限 2,617、最大为 D05 上限 2,836，句子成立。
- D.7 的 47%：不在表、图与补充材料中，取自 JBCS 第 55 号的数值文件（input/params/cohort_N_jbcs2024.csv 的 pcr_registry = 0.47，术前化疗例，含未用帕博利珠单抗者），与 Introduction 中引自文献的数字同样处理。

Limitations 第 5 句「a French cohort treated largely before immunotherapy and antibody–drug conjugates were available」无引文；grinda2023 摘要写「All ESME patients diagnosed between 2008 and 2020」，内容相符（报告事项，第 6 节）。

## 6. 决定、例外与报告事项

### 6.1 本版照指示处理、与规约字面不同的地方
- Introduction 第 3 段不再是「First, … Second, …」的不足列举（规约第 4 节的固定形）；新颖性句不写数据库与期间，指向 Supplementary Methods S1（规约第 4 节要求在句中限定）。第 4 句 44 词，一句引 12 篇。
- Methods 不再有多重比较的一句（规约第 4 节、第 13 节）。
- 三节为用户原文，下列写作检查的命中没有改（第 7 节的数字）：超过 30 词的句（Discussion 7、Implications 2、Limitations 2）；超过 150 词的段（Implications 158、Limitations 182）；裸的「now」（D.2 第 2 句）；因果语「caused by」（Implications 第 3 句，指模型外的假设机制）；Discussion 中 41 个数字有 27 个也出现在 Results，D.7 第 4 句与 Results 第 5 段第 2 句的用词重合 0.59；只有 D.4 的第一句名指表；Discussion 第 1 段只答目的 1（目的 2–4 在 D.4、D.5）；D.3 第 4 句与 Introduction 第 1 段第 4 句、D.6 第 1 句与 Introduction 第 3 段第 1 句内容相近；「break-even HR」（D.2）与「headroom analysis」（D.6）在本文中没有以这个名称定义；Limitations 第 2、4、5、6、8 句没有写对解释的影响；Implications 没有写临床医生在诊疗中改变什么（写的是试验、支付方与帕博利珠单抗）；「such trials are a sound use of research funds」没有对应的信息价值分析。
- Results 第 1 段：新句写成 17 词，段落 156 词（v5 为 150 词）。不动其余句子就压不到 150 词以内（规约第 1.4 节：不做指示外的改动）。

### 6.2 沿用的例外（v5 已报告）
- E1、E2、E3：S4 与 Table 2 重复 6 格、S2 与 Table 1 重复 26 格、S7 与 Table 2 重复 4 格。
- I.4 的目的两句（59 词、47 词）为用户原文；Statistical analysis 的段阶按用户指定的解析种类排列；Fig. 1 为模型结构图。

### 6.3 待决（沿用）
- N12：KEYNOTE-522 最终分析按 pCR 分层的 7 年 EFS 与 ESMO 2023 的值读自会议报道（摘要无，LBA18 原文 403）。待尾崎先生确认原始出处。Limitations 第 4 句的「came from the presentation of the final analysis rather than a full report」写的就是这一点。
- N13：tropion2025 的日期（2025-10-19 的新闻稿）待尾崎先生确认。
- jbcs55：数值由尾崎先生提供，会员限定的原表未见（D.5、D.7 也引用）。
- CHEERS 第 1、2 项的页码待 Abstract。

## 7. 检查（check_v6.md）

最重要的四项：
1. 版：`manuscript/` 下只有 v6、archive（v1 至 v5、ars_v5、ars_v6）、code；v6 内只有本版文件；ars/ 在交付时移入 archive。通过。
2. 表与图的引用：本文 41 段（Introduction 4、Methods 18、Results 10、Discussion 7、Implications 1、Limitations 1）走查，取出的初出顺为 Supplementary Methods S1、S1、Table 1、S2、Fig. 1、Supplementary Fig. S1、S3、Fig. 2、Table 2、Table 3、Fig. 3、S4 至 S9、Supplementary Fig. S2、S10。五个系列各自 1, 2, 3, …；最大番号 = 实数（Table 3、Fig. 3、Supplementary Table 10、Supplementary Fig. 2、Supplementary Methods 1）；supplement 的物理顺序与初出顺一致。通过。
3. 文献的真伪：DOI 61 篇全部在 doi.org 实测 30x，并与 Crossref 比对（写法差异 11 篇，逐条确认为同一文献）；无 DOI 的 16 篇是文件与网页，各有到源页面的核对；撤稿 0。通过。
4. 文献的顺序：本文 61 个上标 run，初出顺 1 至 62 无缺；表、图注、补充材料中新出的 63 至 77 按阅读顺序；77 篇全部被引用，表外番号 0。通过。

docx 回读（走查的母数：manuscript 129 段 251 run、tables 289 项 337 run、figures 14 项、supplement 2,398 项 2,527 run）：
- 全部文字 run 为 Times New Roman 12 pt；以下都是 0：黑以外的文字、Heading 样式、空单元格、表外粗体（见出し除外）、含数字的单元格粗体、「・」、以 Note 开头的段落、表外的「—」。
- 见出し：Introduction、Methods、Study background、Outcome、Variables、Statistical analysis、Results、Discussion、Implications、Limitations、References（Normal 段落粗体 12 pt）；双倍行距 129/129；行号已设。
- 脚注符号：全部表与图一一对应且按顺序。
- 数字：manuscript 225 个、tables 260 个、figures 30 个、supplement 2,217 个，未登记的都是 0。Introduction、Methods、Discussion、Implications、Limitations 的 127 个数字逐段登记（130 行）；Results 98 个数字都是所引表中的显示值；Results 每段以表或图开头 10/10。
- Discussion 等的检查：新出文献 0（Discussion 只引已在前文出现的文献）；各段引用数 D.1 0、D.2 0、D.3 1、D.4 5、D.5 3、D.6 6、D.7 1、Implications 0、Limitations 0；「further research」型 0；Limitations 以外的「limitation」0。
- 文体：禁用语、前置套话、自我说明、方法句、裸时间词（recently 等 4 词）、破折号、连接词连用都是 0；may 2 处（D.7、Limitations 的推断）；caused 1 处（Implications）。超过 30 词的句 17 个（最长 59 词，I.4 目的句）；超过 150 词的段 3 个（R.1 156、IMP.1 158、L.1 182）。语数：Introduction 565、Methods 1,494、Results 877、Discussion 755、Implications 158、Limitations 182，合计 4,031。
- ARS check_acronyms.py（本文 Introduction 至 Limitations）：coverage complete，No findings。
- 原著对照（references_v6.md 第 8、9 节）：本文 98 处（句 × 文献）与图注、补充材料的散文 22 处全部有对照记录；135 条逐字段落全部找到；CC 两句的依据原句列在第 9 节。
- ARS citation-check（ars/citation_audit_v6.md，交付时移入 archive/ars_v6）：照合 77 篇、订正 0、报告事项 6（第 6 节与该文件）。
- 新检查与鸣响（规约第 13 节）。植入只在 scratchpad 的副本上，交付物与 `_build` 的 sha256 在试验前后不变：
  - make_ledger（副本）：Discussion 的引用改成 63 号 → references_first_cited_in_Discussion_Implications_Limitations = [63]；D.1 末尾加「Further research is needed.」→ further_research_phrases 报 2 项；D.2 加「limitation」→ limitation_words_outside_Limitations = [D.2]；见出し「Limitations」改为「Limitation」→ headings_as_specified = False。
  - edit_manuscript_v6.py（副本，在写出之前停止）：D.5 改一词 → 「text differs from the instruction」；702 → 701（符号反转的核对）、47 → 48（JBCS 比例的核对）、D.1 的 2,726 → 2,762（表值的核对）都报错。
  - make_references_doc.py（副本）：删去 D.4 第 2 句 huang2023 的对照记录 → 「manuscript citations without a passage」。
  - make_supplement.py（副本）：CHEERS 第 26 项指向 Discussion 第 8 段 → 「CHEERS location not in the manuscript」。
- 图：Fig. 1–3、Fig. S1–S2 为 600 dpi（插入后实测）；字号检查 5 张都没有低于 8 pt 的字；碰撞检查 5/5 PASS（0 fail 0 warn）；validate_figure.py 19 pass、2 warn、0 fail（像素与 v5 相同）。
- Word（COM）打开 4 个 docx 并另存为 PDF，无报错：manuscript 23 页、tables 8 页、figures 3 页、supplement 45 页。CHEERS 的页码取自同一 Word 的分页。

## 8. 与 v5 的逐段对照（diff_v5_v6.md）

原始比较之外，另做归一化比较（两版都去掉文献号），剩下的块都是措辞或内容的变化：

| 文件 | 归一化后的块 | 内容 | 对应 |
|---|---|---|---|
| tables | 0 | — | — |
| figures | 0 | — | — |
| supplement | 5 | N1、N4 Supplementary Methods S1 移到最前、加检索小节、改标题（原 16 段逐字不变）；N2 CHEERS 第 11 项页码；N3 CHEERS 第 26 项；N5 S10 行名 | 指示第 1、4、5、6 条 |
| manuscript | 7 | N1 I.1；N2 I.3、I.4；N3 Methods 末段；N4 R.1；N5 R.5；N6 三节的插入；N7 References 26–39 号的顺序 | 指示第 1、2、3、5 条 |

意图之外的变化：0。数值：表、图、补充材料的显示值与 v5 相同；本文新增的数字只在新句与插入的三节中（第 5 节）。

## 9. 第 13 节的逐项点检（规约第 14 节）

本版交付物是 manuscript（Introduction 至 Limitations、References）、tables、figures、supplementary；Abstract 按指示不写，title page 为尾崎担当。下表中「不适用」都是这个原因，除非另注。

| 项目 | 结果 |
|---|---|
| 版：作业树只有最新版 | 通过（manuscript/ 下 v6、archive、code；ars/ 交付时移入 archive） |
| 版：开始时 sha256 与 manifest 一致 | 通过（MANIFEST_v5 的全部文件一致；git 干净） |
| 版：底本为 v(n−1)，作业记录开头有底本与 sha256 | 通过（第 0 节第 3 条；脚本也核对 manuscript_v5.docx 的 sha256） |
| 版：意图之外戻った段落 0（补充表的脚注、题名、语数、图的解像度、过去戻った箇所） | 通过（第 8 节；补充表脚注逐条不变；图像逐字节相同；补充脚注中输入表的编号 10 处都是 S2；题名与语数属 title page） |
| 版：数值不变的版与 v(n−1) 数值完全一致 | 通过（表、图、补充材料的显示值不变；本文新数字见第 5 节） |
| 版：模板雏形 0 | 通过 |
| 版：版号与作业注记 0、[TO CONFIRM] | 通过（docx 中无版号；[TO CONFIRM] 0 件） |
| 版：manifest 更新、旧版移入 archive | 通过 |
| 版：解析输出的 sha256 与 manifest | 通过（numbers_ledger_v6.md 第 8 节） |
| 版：差分全部对应指示 | 通过（第 2、3、8 节） |
| 版：撤回的主张 0 | 通过（v6 删去的：I.3 的「lacks two things」与「Without a Japanese estimate for pembrolizumab, there is no reference against which the cost and health gain of exercise can be judged.」、I.4 句中的检索范围、Methods 的多重比较句；都不在 v6 本文中） |
| 版：变更履历与注释 0 | 通过（python-docx 生成，无 w:ins、w:del、comments） |
| 版：ARS 的 Markdown 初稿与 ars/ 0 | 通过（不出 Markdown 初稿；ars/ 移入 archive/ars_v6/） |
| 文献：初出顺、未引用 0、表外番号 0 | 通过（第 7 节第 4 条） |
| 文献：DOI 解决、书目一致 | 通过（61/61；写法差异 11 篇已逐条确认；解决不了的 0） |
| 文献：新规引用全部与原著对照 | 通过，有限定（135 条段落全部找到；report 与 provided 的原著未见，列为待决 N12 与 jbcs55） |
| 文献：citation-check 的报告 | 通过（ars/citation_audit_v6.md：照合 77 篇、订正 0、报告事项 6） |
| 文献：著者年引用 0 | 通过 |
| 文献：10 年超与自引的比例（报告） | 10 年超 8 篇；自引 0% |
| 文献：新规性句的检索限定 | 例外（指示第 1 条：句中只引 Supplementary Methods S1，数据库、期间、日期与检索式在该节，与 references_v6.md 第 1 节一致；无绝对形） |
| 付番：四系列的初出顺、最大番号、地の文での言及 | 通过（第 7 节第 2 条） |
| 付番：supplementary 内按编号排列 | 通过（Supplementary Methods S1 移到最前） |
| 付番：补充方法与报告规范从正文引用 | 通过（Supplementary Methods S1 从 Introduction 第 3 段与段阶 (1)、(3)；S1 从 Study background） |
| 付番：图附上且从 Fig. 1 依次引用 | 通过 |
| 见出し：六个大见出し | 通过（加上文献表的 References） |
| 见出し：规约外的节与项目 | 通过（v5 与 v6 都没有 Acknowledgements 等） |
| 见出し：Methods 四个小见出し | 通过 |
| 体裁：Heading 样式 0、12 pt TNR、黑字、行号、双倍行距、行内粗体 0 | 通过 |
| 体裁：表的列见出しと数値セル粗体 0、「・」0、横版、✳ 脚注、Note 0、符号一一对应 | 通过 |
| 体裁：图 600 dpi 实测 | 通过 |
| 体裁：前付け | 不适用（尾崎担当） |
| 体裁：生成 AI 的记述 0、ARS 标记 0、ARS 默认的遗留 0 | 通过 |
| 体裁：拼写统一（米式）、Fig. 统一 | 通过 |
| 体裁：语数 | 本文 4,031 词（第 7 节）；投稿先未定 |
| 数值：正文数值在台账、出所表中同值同位 | 通过（第 5 节；702 为定义上的符号反转） |
| 数值：表脚注的数值在表或图中 | 通过 |
| 数值：同一数值不在两张表 | E1 至 E3（第 6.2 节） |
| 数值：分层 n 之和、百分率之和、流程图 | 不适用（无分层计数表与流程图）；S8：2,294 + 1,157 = 3,451 |
| 数值：对象者数一致 | 3,451 与 2,294 在 Introduction、Methods、Results、Discussion、S8 一致 |
| 数值：点估计在 CI 内、CI 与 p | 通过（新句 3,898 在 [2,388, 5,713] 内；无 p 值） |
| 数值：同一统计量同值同位 | 通过 |
| 数值：p 值表记、trend 型用语 | 不适用（无 p 值）；trend 型 0 |
| 数值：因果语 | 「caused by」1 处（Implications，用户原文，指假设的机制；第 6.1 节） |
| 数值：要约统计量的形、空セル 0 | 通过 |
| 数值：负号、前导 0、千位逗号 | 通过 |
| 数值：小数位按表统一、百分率舍入一致 | 通过 |
| 内容：Methods 无数值结果 | 通过 |
| 内容：Results 无方法句、各结果句有表图引用 | 通过 |
| 内容：各解析有目的句；推定对象都在 Results | 通过 |
| 内容：Introduction 末两段（不足的列举 → 目的） | 例外（指示第 1 条，第 6.1 节） |
| 内容：目的对应表 | 通过（第 1 节） |
| 内容：Methods 的曝露与アウトカムの名前与目的一致、段阶顺 | 名前一致；段阶顺为用户指定（第 6.2 节） |
| 内容：Abstract 的目的与结论 | 不适用（未写） |
| 内容：Results 按目的顺、每段以表图开头 | 通过 |
| 内容：Discussion 每段开头名指结果、无 Results 以外的所见 | 只有 D.4 以表开头；Results 以外的所见：D.7 的登记 pCR 47%（JBCS，非本研究的结果）（第 6.1 节） |
| 内容：Discussion 第 1 段答各目的、Introduction 不足各一次 | 第 1 段只答目的 1（第 6.1 节）；不足：第 1–3 句 → D.6，第 4 句 → D.4 |
| 内容：Discussion 无近乎重复 Results 的段 | 无整段重复；数字再揭 27/41，D.7 第 4 句重合 0.59（第 6.1 节） |
| 内容：Discussion 的引用集中在中段、后半无新出文献 | 新出 0；各段引用数见第 7 节 |
| 内容：Discussion 后半无一般论与无法导出的推测 | 「further research」型 0 |
| 内容：临床医生改变什么 | 无此类句（第 6.1 节） |
| 内容：Implications 名指结果、无更强的主张与新数字 | 无新数字；「a sound use of research funds」（第 6.1 节） |
| 内容：用语定义与一致 | 「break-even HR」「headroom analysis」未以此名定义（第 6.1 节、第 10 节） |
| 内容：缩写（正文初出展开、表图脚注再展开、check_acronyms） | 通过（complete、No findings） |
| 内容：Limitations 以外无「〜の限界」型；各限界的影响 | 前者通过；后者 5 句无影响句（第 6.1 节） |
| 内容：Outcome 与 Variables 的第一句 | 通过 |
| 内容：统计软件只写语言与版本 | 通过（R version 4.5.1） |
| 内容：Ethics、Data availability、Funding、COI | 不适用（title page 为尾崎担当；模型研究） |
| 内容：报告规范的清单在 supplementary，各项有页与节 | 通过（S1；第 26 项本版起有段与页；第 1、2 项待 Abstract 与 title page） |
| 内容：题名 | 不适用（title page） |
| 内容：欠测、多重比较、事前登録 | 多重比较句按指示删去（第 6.1 节）；计划未登记一句；欠测：模型研究，无个体数据的欠测，按规约不写 |
| 内容：选定流程图 | 不适用（无对象选定） |
| 内容：图中无题名、面板标签、单位、不只靠颜色、≥ 8 pt | 通过 |
| 内容：图与表无同一结果重复 | 通过 |
| 内容：著者贡献 | 不适用（尾崎担当） |
| 内容：AI 常套语、套话、自我说明、连接词连用 0；破折号、30 词与 150 词 | 前四项 0；破折号 0；超过 30 词的句 17、超过 150 词的段 3（第 7 节） |
| 内容：裸时间词 0、事实句无 may | recently 等 0；「now」1 处（D.2，第 6.1 节）；may 只在推断 |
| 内容：主张强度未变强 | 通过（I.1「confined to」→「concentrated in」为弱化；其余改动不改主张） |
| 内容：rebuttal-audit、humanizer、stop-slop | 不适用（非查读对应版；humanizer 在全稿初稿完成后一次） |

## 10. 用语表（v5 沿用，加本版的新语）

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
| Utility values from Japanese populations、the four utility scenarios | 日本人群效用情景；与美、英及澳洲报销申请的三行合称 | Methods 段阶 (5)；Results P10 |
| break-even HR（v6，用户原文） | 最大可负担费用 = 方案费用 的 HR（Methods 写作「the HR at which the maximum affordable cost equaled the cost of a program」） | Discussion 第 2 段（本文未以此名定义） |
| headroom analysis（v6，用户原文） | 最大可负担费用的分析（Introduction 第 3 段第 3 句描述其概念） | Discussion 第 6 段（本文未以此名定义） |
| the standard regimen（v6） | 化疗 + 帕博利珠单抗 | Discussion 第 5 段 |
| the 2024 national registry（v6） | JBCS 全国乳癌患者登记第 55 号（2024 年病例） | Discussion 第 7 段 |
| the fee-schedule price of a supervised program（v6） | fee-schedule-based program 的费用 | Implications 第 5 句 |

金额的写法：正文写「JPY 2,726 thousand」，与表中千日元的显示值同值同位；阈值写「JPY 5 million per QALY」；一年净收益写「JPY 2.68 billion」（S8 的显示）。拼写：米式；图的表记：Fig.

## 11. 文献检索的记录

见 references_v6.md 第 1 节（数据库、检索式原文、年范围、检索日、命中数）与第 2 节（新颖性句与经济评价句所依据的 4 组检索的全部命中的判定）。本版起，新颖性句所依据的三组检索的数据库、出版年范围、检索日与检索式原文也写在 Supplementary Methods S1 的 Literature searches 小节（同一 JSON 文件）。Scopus：本环境未配置，未检索。本版没有新检索。

## 12. 过去意图之外戻った箇所（规约第 1.2 节规则 7）

- v5 发现：补充表脚注中输入表的编号（3 处）在编号变更时未随之更新。本版名指确认：补充材料与本文中指向输入表的 10 处都是 S2（make_ledger 的 references_to_input_table_wrong_number = []）。
- 本版未发现新的戻り。
