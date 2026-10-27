# 作业记录 v7（v7：重写 Discussion、Implications、Limitations；Results 第 1 段拆段，2026-10-27）

## 0. 声明与底本

1. 规约：开工时读了 `Documents/ClaudeCode/WRITING_RULES.md` 全文；交付前从头到尾重读了全文（514 行，第 1–14 节），第 13 节的逐项点检见第 9 节。ARS：v6 中读过的 academic-paper 各文件（SKILL.md 的 Anti-Patterns 与 Quality Standards、draft_writer_agent.md、citation_compliance_agent.md、writing_quality_check.md、academic_writing_style.md、writing_judgment_framework.md、intro_title_rhetoric_guide.md）按同样的诊断用于本版改动的段落。nature-figure：图未改，只重跑审查。
2. 段阶：v1 之后的改稿（规约第 1 节第 6 步）。三节为用户给定的原文，照插；Abstract 按指示不写。
3. 底本：`manuscript/archive/v6/`：manuscript_v6.docx 7e1eed29、tables_v6.docx、figures_v6.docx、supplement_v6.docx（开工时作业树全部文件的 sha256 与 MANIFEST_v6 一致，git 干净）。v6 已移入 archive；作业树 `manuscript/` 下只有 v7、archive（v1 至 v6、ars_v5 至 ars_v7）、code。
4. 指示：「v7：重写 Discussion、Implications、Limitations；Results 第 1 段拆段」（2026-10-27）的第 0 至 4 条。
5. 做法：本文 manuscript_v7.docx 由 `archive/v6/manuscript_v6.docx` 直接编辑而成（`code/edit_manuscript_v7.py`：先核对 v6 docx 的 sha256 与 MANIFEST_v6；按同一文件的文献表把上标番号还原为标记；只删 Results 第 1 段的两句、在其后新立一段、整节替换三节；新文与指示原文逐字比对）。`number_refs.py` 重编文献号（结果与 v6 相同）。表、图、补充材料用同一套生成代码重新生成；图的 PNG、TIFF 与 v6 逐字节相同。
6. 来源：数值来源与 v6 相同，没有新的解析输出。

产物（`manuscript/v7/`）：manuscript_v7.docx、tables_v7.docx、figures_v7.docx、supplement_v7.docx、本文件、numbers_ledger_v7.md、references_v7.md；辅助：check_v7.md、diff_v6_v7.md、MANIFEST_v7.md、figures/。ARS 的作业记录（citation audit）在交付时移入 `manuscript/archive/ars_v7/`。

投稿先与投稿仕様：投稿先未定；拼写为米式；图的表记为 Fig.；文献为 Vancouver（NLM）、本文初出顺。

## 1. 目的与各节的对应（规约第 2.1 节）

目的（Introduction 第 4 段，不变）：目的 1（主）最大可负担费用及其随效应大小与持续时间的变化；目的 2 加入单用化疗时的同一费用；目的 3 帕博利珠单抗在日本的成本效果；目的 4 与帕博利珠单抗同 QALY 增益的运动效应。

| 目的 | Results 的段落 | Discussion | Implications |
|---|---|---|---|
| 目的 1 | P1 至 P6、P11 | D.1 第 1–3 句、D.2、D.3、D.6、D.7 | 第 1 段第 1–5 句、第 2 段第 1–2 句 |
| 目的 2 | P7 | D.4 第 4 句 | — |
| 目的 3 | P8、P9、P11 | D.1 第 4 句、D.5 | 第 2 段第 3 句 |
| 目的 4 | P10 | D.4 第 1–3 句 | — |

D.4 第 5、6 句（2024 年 3,451 例中 2,294 例用帕博利珠单抗 → 主比较反映多数实践）对应目的 1 的设定。Limitations 两段对应全部目的。Introduction 第 3 段的不足：第 1–3 句 → D.6；第 4 句 → D.5。对应不上的段、句：0。

## 2. 本版改动的段落一览（diff_v6_v7.md）

| 位置 | 改动 | 对应的指示 |
|---|---|---|
| Results 第 1 段 | 删去路径 B 的两句（「Through an effect on pCR instead, …」「An increase of 10 percentage points …」） | 第 1 条 |
| Results 第 2 段（新） | 指示的原文两句（Supplementary Table S5）；原第 2 至 10 段成为第 3 至 11 段，文字不变 | 第 1 条 |
| Discussion、Implications、Limitations | 整节替换为指示的原文：Discussion 7 段、Implications 2 段、Limitations 2 段；文献键换成番号 | 第 2 条 |
| 其余各段 | 一字不变；文献号也与 v6 相同（三节只引用已在前文出现的文献） | — |

## 3. 表、图与补充材料的改动

- Supplementary Table S1（CHEERS）：第 23 项「Results, paragraphs 1 to 9」→「paragraphs 1 to 10」，第 24 项「paragraph 10」→「paragraph 11」（Results 拆段的结果）；第 26 项的 Limitations「paragraph 1 (p. 12)」→「paragraphs 1 to 2 (pp. 11 to 12)」。其余不变。
- 表、图、补充材料的其他内容：不变（归一化比较 tables 0、figures 0、supplement 只有上面 3 格）。

## 4. 原文的核对（指示第 3 条）

### 4.1 数字（numbers_ledger_v7.md 第 1、1b 节）
- Results 第 2 段：1、389 [238, 570]、10、3,898 [2,388, 5,713] 都是 Supplementary Table S5（Panel A，主比较，500 万日元/QALY，pCR +1 与 +10 个百分点）的显示值。
- 三节的 14 个数字：Table 2 的 1.1、4.2、8.6；Table 1 的 3（CHALLENGE 的 3 年方案）；Supplementary Methods S1 的 7（7 年）；JBCS 数值文件的 2024（两处）、2,294、3,451、47%；文献摘要的 24（licata2025）、5（chan2026「5-year time horizon」）、2008 与 2020（grinda2023「diagnosed between 2008 and 2020」）。都同值同位，不一致 0，没有停下。

### 4.2 文字描述的依据（编辑脚本中断言，记录在 numbers_ledger_v7.md 第 1b 节末）
- D.2 第 2 句「one month of treatment after distant recurrence costs more than the whole exercise program」：月额 D03 1,215,933、D03P 1,458,318、D05 1,412,953 日元；艾立布林情景的 D05 245,683 日元；转移治疗费减半情景 D03 607,966、D03P 729,159、D05 706,477 日元。最低的（艾立布林情景的 D05）也高于三种方案中最贵的 E01 239,508 日元（E02 192,400、E03 11,260）。成立；艾立布林情景只高 2.6%。
- D.4 第 2 句「by more than half」：Table 3 的 HR 0.425，降低 57.5%。成立。
- L.2 第 3 句「no single cost changed the conclusion (Fig. 3)」：Fig. 3 的值所在的 S9 中，主比较 HR 0.85 上限的 42 个值最低为 2,617 千日元，是最贵方案（E01）的 10 倍以上。另查帕博利珠单抗一侧：S9 的 118 个 ICER 最高为 2,379 千日元/QALY，低于 500 万日元。成立。
- 另查了没有被要求但同样以表为依据的几句：D.3 第 1 句（持续时间使上限在 1,772 至 3,404 千日元之间变动，Fig. 3 的单因素范围为 2,617 至 2,836，转移治疗费的两个情景在 Table 2 Panel C）；D.5 第 2 句（帕博利珠单抗的 ICER 变化最大的是 S-JP 情景 +991 千日元与药价下限 −757 千日元；艾立布林情景 +732 列第三）；L.2 第 4 句（日本人群效用：上限 2,733 对 2,726，分界点相同，ICER 2,047 对 2,053）。都成立。

### 4.3 文献内容（references_v7.md 第 8 节）
三节的 23 处（句子 × 文献）都与原文段落对照，全部找到。一处报告：L.2 第 1 句的「largely before immunotherapy and antibody–drug conjugates」，grinda2023 摘要只写诊断期间 2008 至 2020 年，这一部分是由期间推出的。不构成不符，没有停下。

## 5. 按规约查的命中（指示第 3 条，原文未改）

| 项目 | 结果 |
|---|---|
| 超过 30 词的句 | 本版新文中 1 句：Results 第 2 段第 2 句 31 词。三节中 0（最长 29 词，D.1 第 1 句）。其余 6 句在未改动的 Introduction |
| 超过 150 词的段 | 0（最长 R.11 149 词；Implications 第 1 段 112、Limitations 第 1 段 124） |
| 裸用的「now」 | 0 |
| 不带日期的「current」 | 2：D.4 第 6 句「current practice」、L.2 第 2 句「current treatment」（规约第 6.3 节的时间词同类） |
| 因果用语（caused、led to、impact、improved） | 0。另有 D.6 第 3 句「drove the costs」，转述 chan2026 的「cost drivers」 |
| 未定义的术语 | 0（v6 的「break-even HR」「headroom analysis」已不在本文；新文所用的 fee-schedule-based program、main comparison、one-year net benefit 都在 Methods 定义） |
| Discussion 等与 Results 重复的数字 | 14 个中 7 个：1.1、4.2、8.6（Results 第 1、5 段）；3,451 与 2024（D.4，Results 第 6 段）；2024（D.7，同上）；5（D.6 的「5 years」与 Results 的「JPY 5 million」只是数字相同） |
| Discussion 中与 Results 的句子用词重合 0.5 以上 | 0 |

其余与规约字面的出入（报告，未改）：
- Discussion 的段首以表或图名指结果的只有 D.3（Table 2、Fig. 3）；Implications 第 2 段的第一句也名指 Table 2。
- Discussion 第 1 段答目的 1 与目的 3；目的 2、4 在 D.4。
- 节间内容相近的句：D.4 第 5 句与 Introduction 第 1 段第 5 句（2024 年 3,451 例中 2,294 例）；D.3 第 2 句与 Introduction 第 1 段第 4 句（24 个月）；D.6 第 1 句与 Introduction 第 3 段第 1 句；Implications 第 1 段第 1 句与 Introduction 第 2 段第 3 句（体能与疲劳）。
- Results 第 2 段第 2 句没有括号中的表号，以段首的「Supplementary Table S5 shows」为依据。make_ledger 的结果句检查原来只认句内引用或同段后句的引用，本版加了「段首名指该表」也算（规约第 4 节：各段开头名指表），并用植入试过（第 7 节）。

## 6. 例外与待决（沿用）

- 沿用的例外：Introduction 第 3 段（v6 的指示原文，无 First/Second，新颖性句指向 Supplementary Methods S1）；Methods 无多重比较句；I.4 的目的两句（59、47 词）；Statistical analysis 的段阶顺；Fig. 1 为模型图；E1–E3（S4、S2、S7 与 Table 1、2 的重复格）。
- 待决：N12（KEYNOTE-522 最终分析的分层 7 年 EFS 与 ESMO 2023 的值读自会议报道）、N13（tropion2025 的日期）、jbcs55（会员限定的原表未见）、CHEERS 第 1、2 项的页码待 Abstract。

## 7. 检查（check_v7.md）

最重要的四项：
1. 版：`manuscript/` 下只有 v7、archive（v1 至 v6、ars_v5 至 ars_v7）、code；v7 内只有本版文件；ars/ 在交付时移入 archive。通过。
2. 表与图的引用：本文 44 段（Introduction 4、Methods 18、Results 11、Discussion 7、Implications 2、Limitations 2）走查，取出的初出顺为 Supplementary Methods S1、S1、Table 1、S2、Fig. 1、Supplementary Fig. S1、S3、Fig. 2、Table 2、Table 3、Fig. 3、S4 至 S9、Supplementary Fig. S2、S10。五个系列各自 1, 2, 3, …；最大番号 = 实数；supplement 的物理顺序与初出顺一致。通过。
3. 文献的真伪：DOI 61 篇全部在 doi.org 实测 30x，并与 Crossref 比对；无 DOI 的 16 篇各有到源页面的核对；撤稿 0。通过。
4. 文献的顺序：本文 63 个上标 run，初出顺 1 至 62 无缺；表、图注、补充材料中新出的 63 至 77 按阅读顺序；77 篇全部被引用，表外番号 0。文献号与 v6 完全相同。通过。

docx 回读（走查的母数：manuscript 132 段 258 run、tables 289 项 337 run、figures 14 项、supplement 2,398 项 2,527 run）：
- 全部文字 run 为 Times New Roman 12 pt；黑以外的文字、Heading 样式、空单元格、表外粗体（见出し除外）、含数字的单元格粗体、「・」、以 Note 开头的段落、表外的「—」都是 0。
- 见出し：Introduction、Methods、Study background、Outcome、Variables、Statistical analysis、Results、Discussion、Implications、Limitations、References；双倍行距 132/132；行号已设。
- 脚注符号：全部表与图一一对应且按顺序。
- 数字：manuscript 198 个、tables 260 个、figures 30 个、supplement 2,219 个，未登记的都是 0。Introduction、Methods 与三节的 100 个数字逐段登记（103 行）；Results 98 个数字都是所引表中的显示值；Results 每段以表或图开头 11/11；结果句无引用依据的 0。
- 三节的检查：新出文献 0；各段引用数 D.1 0、D.2 0、D.3 1、D.4 3、D.5 5、D.6 8、D.7 1、Implications 4 与 0、Limitations 0 与 1；「further research」型 0；Limitations 以外的「limitation」0。
- 文体：禁用语、前置套话、自我说明、方法句、裸时间词（recently 等 4 词）、因果语、破折号、连接词连用都是 0；may 2 处与 suggests 1 处（D.7 第 1 句、L.1 第 2 句，推断）。语数：Introduction 565、Methods 1,494、Results 884、Discussion 523、Implications 167、Limitations 232，合计 3,865。
- ARS check_acronyms.py（本文 Introduction 至 Limitations）：coverage complete，No findings。
- 原著对照（references_v7.md 第 8 节）：本文 105 处（句 × 文献）与图注、补充材料的散文 22 处全部有对照记录；142 条逐字段落全部找到。
- ARS citation-check（ars/citation_audit_v7.md，交付时移入 archive/ars_v7）：照合 77 篇、订正 0、报告事项 7。
- 新检查与鸣响（规约第 13 节；植入只在 scratchpad 的副本上，交付物与 `_build` 的 sha256 在试验前后不变）：
  - make_ledger（副本）：Results 第 2 段的段首改成不名指表 → sentences_without_a_later_reference_to_their_table 列出该段两句；D.1 加「currently offered」→ current_without_a_date 多出 D.1。
  - edit_manuscript_v7.py（副本，写出前停止）：L.2 改一词 → 「text differs from the instruction」；加入一个低于方案费用的月额 → 文字依据的断言报错；文献键的写法改回 v6（允许数字开头）→ UI「[238, 570]」被当成文献键，逐字比对报错（本版改正了这一点）。
  - make_supplement.py（副本）：CHEERS 第 24 项指向 Results 第 12 段 → 「CHEERS location not in the manuscript」。
- 图：Fig. 1–3、Fig. S1–S2 为 600 dpi（插入后实测）；字号检查 5 张都没有低于 8 pt 的字；碰撞检查 5/5 PASS；validate_figure.py 19 pass、2 warn、0 fail（像素与 v6 相同）。
- Word（COM）打开 4 个 docx 并另存为 PDF，无报错：manuscript 23 页、tables 8 页、figures 3 页、supplement 45 页。CHEERS 的页码取自同一 Word 的分页。

## 8. 与 v6 的逐段对照（diff_v6_v7.md）

| 文件 | 原始比较的块 | 归一化后的块 | 内容 | 对应 |
|---|---|---|---|---|
| tables | 0 | 0 | — | — |
| figures | 0 | 0 | — | — |
| supplement | 3 | 3 | CHEERS 第 23、24、26 项的位置 | 第 1、2 条的结果 |
| manuscript | 4 | 4 | N1 Results 第 1 段 → 第 1、2 段；N2 Discussion 7 段；N3 Implications 1 段 → 2 段；N4 Limitations 1 段 → 2 段 | 第 1、2 条 |

意图之外的变化：0。References：77 条逐字、逐号相同。数值：表、图、补充材料的显示值与 v6 相同。

## 9. 第 13 节的逐项点检（规约第 14 节）

Abstract 按指示不写，title page 为尾崎担当；下表中「不适用」都是这个原因，除非另注。

| 项目 | 结果 |
|---|---|
| 版：作业树只有最新版 | 通过 |
| 版：开始时 sha256 与 manifest 一致 | 通过（MANIFEST_v6 的全部文件一致；git 干净） |
| 版：底本为 v(n−1)，作业记录开头有底本与 sha256 | 通过（第 0 节；脚本也核对 manuscript_v6.docx 的 sha256） |
| 版：意图之外戻った段落 0（补充表的脚注、题名、语数、图的解像度、过去戻った箇所） | 通过（第 8 节；补充表脚注不变；图像逐字节相同；指向输入表的 10 处都是 S2） |
| 版：数值不变的版与 v(n−1) 数值完全一致 | 通过（表、图、补充材料的显示值不变；本文的新数字都在 S5、表与出处中） |
| 版：模板雏形 0；版号与作业注记 0 | 通过（[TO CONFIRM] 0 件） |
| 版：manifest 更新、旧版移入 archive | 通过 |
| 版：解析输出的 sha256 与 manifest | 通过（numbers_ledger_v7.md 第 8 节） |
| 版：差分全部对应指示 | 通过（第 2、3、8 节） |
| 版：撤回的主张 0 | 通过（v6 的三节整体替换：v6 Discussion 中 CC 补写的两句、「Medical costs avoided made up JPY 702 thousand …」「no input moved this cost outside JPY 2,617 thousand to 2,836 thousand」等句都不在 v7 的三节中；Results 中的同一数值未动） |
| 版：变更履历与注释 0；ARS 的初稿与 ars/ 0 | 通过 |
| 文献：初出顺、未引用 0、表外番号 0 | 通过 |
| 文献：DOI 解决、书目一致 | 通过（61/61） |
| 文献：新规引用全部与原著对照 | 通过，有限定（第 4.3 节；report 与 provided 的原著未见） |
| 文献：citation-check 的报告 | 通过（ars/citation_audit_v7.md） |
| 文献：著者年引用 0；10 年超与自引 | 通过；10 年超 8 篇，自引 0% |
| 文献：新规性句的检索限定 | 例外（v6 起，指向 Supplementary Methods S1） |
| 付番：四系列的初出顺、最大番号、地の文での言及；supplementary 内按编号；补充方法与报告规范从正文引用；图从 Fig. 1 依次引用 | 通过 |
| 见出し：六个大见出し、Methods 四个小见出し、规约外的节 0 | 通过 |
| 体裁：Heading 样式 0、12 pt TNR、黑字、行号、双倍行距、行内粗体 0、表的粗体、「・」、横版、✳ 脚注、符号一一对应、600 dpi | 通过 |
| 体裁：前付け | 不适用（尾崎担当） |
| 体裁：生成 AI 的记述 0、ARS 标记 0、ARS 默认的遗留 0；拼写与 Fig. 统一 | 通过 |
| 体裁：语数 | 本文 3,865 词；投稿先未定 |
| 数值：正文数值在台账、出所表中同值同位；表脚注的数值 | 通过（第 4.1 节） |
| 数值：同一数值不在两张表 | E1 至 E3 |
| 数值：分层 n、对象者数 | 3,451 与 2,294 在 Introduction、Methods、Results、Discussion、S8 一致 |
| 数值：点估计在 UI 内、p 值、因果语、负号、小数、千位逗号 | 通过（新段 389 在 [238, 570]、3,898 在 [2,388, 5,713] 内；无 p 值；因果语 0） |
| 内容：Methods 无结果；Results 无方法句、各结果句有依据、按目的顺且段首名指表图 | 通过（第 5 节末的检查调整） |
| 内容：Introduction 末两段 | 例外（v6 起） |
| 内容：目的对应表 | 通过（第 1 节） |
| 内容：Discussion 段首名指结果 | D.3 一段（第 5 节） |
| 内容：Discussion 第 1 段答各目的、Introduction 不足各一次 | 第 1 段答目的 1、3；不足两项都有回应（第 1 节） |
| 内容：Discussion 无近乎重复 Results 的段 | 通过（重合 0.5 以上的句 0；数字再揭 7/14） |
| 内容：Discussion 的引用在中段、后半无新出文献；无「further research」型 | 通过 |
| 内容：临床医生改变什么 | 有（Implications 第 1 段第 1 句：医生已有在化疗期间建议运动的理由） |
| 内容：Implications 名指结果、无更强的主张与新数字 | 无数字；各句引表 |
| 内容：用语定义、缩写（check_acronyms complete、No findings） | 通过 |
| 内容：Limitations 以外无「〜の限界」型；各限界的影响 | 通过（每个限界都写了对解释的影响：conditional、may not apply、understated、change the baseline risk、opposite effects、no single cost changed、nearly the same、understated） |
| 内容：Outcome 与 Variables 的第一句、统计软件 | 通过 |
| 内容：Ethics 等、题名、著者贡献 | 不适用（title page） |
| 内容：报告规范的清单在 supplementary，各项有页与节 | 通过（第 23、24、26 项随本版更新） |
| 内容：欠测、多重比较、事前登録 | 多重比较句按 v6 的指示删去；计划未登记一句 |
| 内容：图中无题名、面板标签、单位、不只靠颜色、≥ 8 pt；图与表无重复 | 通过 |
| 内容：AI 常套语、套话、自我说明、连接词 0；破折号、30 词与 150 词 | 0；30 词超 7 句（新文 1）；150 词超 0 |
| 内容：裸时间词 0、事实句无 may | recently 等 0；current 2 处（第 5 节） |
| 内容：主张强度未变强 | 三节为用户原文的整体替换；Results 只拆段，主张不变 |
| 内容：rebuttal-audit、humanizer、stop-slop | 不适用 |

## 10. 用语表（v6 沿用；本版的变化）

v6 中用户原文的「break-even HR」「headroom analysis」「the fee-schedule price of a supervised program」随三节替换不再出现。本版三节的用语：fee-schedule-based program、main comparison、maximum affordable cost、medical costs avoided、one-year net benefit（Methods 定义）；the 2024 national registry（JBCS 第 55 号，引 jbcs55）；health education（CHALLENGE 的对照，转述 chan2026）。其余与 v6 第 10 节相同。

## 11. 文献检索的记录

与 v6 相同（references_v7.md 第 1、2 节；新颖性句的检索式在 Supplementary Methods S1）。本版没有新检索。

## 12. 过去意图之外戻った箇所（规约第 1.2 节规则 7）

- v5 发现的补充表脚注中输入表的编号：本版名指确认，10 处都是 S2。
- 本版未发现新的戻り。v6 的「文献键正则把数字的方括号当成键」在 v6 中没有触发（v6 的新文无 UI 方括号），本版改正并加了植入试验。
