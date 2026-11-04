# worklog v15（2026-11-04）

## 1. 底本

底本: manuscript_v14_BCRT.docx（v14，2026-11-04 交付，sha256 前 8 位 bd741f34）。同批: tables_v14_BCRT.docx（ea0fe2b4）、ESM_1_v14.docx（02580c22）、ESM_1_v14.pdf（7fb2d73b）、Fig1〜3.tif（c13b748e、662046bf、d7926e1e）、cover_letter_v14_BCRT.docx（21ed7f1a）、worklog_v14.md（9ceb8c70）。会话开始时 9 个文件的 sha256 全部与 MANIFEST_v14.md 一致；作业树 git 状态干净（HEAD b734fea）；manuscript/ 下只有 v14（另有 archive、code、空的 _inbox）。
本版只做 v15 指示列出的删减与修正（压到词数上限以内、两条文献、v14 报告的小项）。不跑 ARS、humanizer、stop-slop；未列出的文字不改。
编辑方法: v14 的 docx 直接编辑，脚本 manuscript/code/edit_manuscript_v15.py、edit_tables_v15.py、edit_esm_v15.py（lxml 只改 word/document.xml；每条原文须在 v14 中逐字唯一命中，否则停止）。Fig1〜3.tif 与 cover letter 为 v14 的逐字节复制（cmp 确认）。三个 docx 由 Word（COM）打开确认: 修订 0、批注 0；manuscript 29 页、tables 9 页、ESM 48 页。ESM_1_v15.pdf 由 Word SaveAs2(17) 导出。

## 2. 投稿先与投稿规格（沿用 v14 第 2 节）

- 投稿先 BCRT；抄录上限 250 词；正文上限 3,500 词；Springer 数字式文献；美式拼写；"Fig."。
- 语数计法同 v14（checks_v14/word_wc14.py；Word ComputeStatistics；抄录去 4 个标签；正文 Introduction 至 Conclusion，不含 17 个标题）。
  - 做完 1a〜1n 后实测: 正文 3,470（含标题 3,511），≤ 3,480 → **备用删减未用（0 条）**。为确认另行实测: 加备 1 后 3,453、加备 1 与备 2 后 3,441（未采用）。
  - 抄录 248（含标签 252），未改。
  - 各节（不含标题）: Introduction 570、Methods 1,347、Results 674、Discussion 489、Implications 162、Limitations 191、Conclusion 37。
  - 题名页 Word count 行 → "abstract 248; main text 3,470"（1o）；"3 tables; 3 figures; 1 Online Resource" 不变。
- 偏离照旧（v11 第 2 节）: 1. 标题结构；2. 表脚注记号 a〜d；3. 题名页在 manuscript 内、表另成 tables 文件、图为 tif；4. 文献 72〜78 只在 Table 1 与 ESM。

## 3. 用语表

沿用 v14 第 3 节。本版变化: Statistical analysis (2) 不再用 "extendedly dominated"（1d: 强支配与扩展支配统称 dominated）；Table 2 脚注 a 的 "dominated" 定义未改。

## 4. 数值台帳

本版不加新数值（第 71 条的卷页是文献书目，不是结果）。v14 的表与 ESM 的数值一个不变（tables 只加 1 句脚注；ESM 只改 S4 脚注 a 的略语与 Table S1 的页码，checks_v15/regress15.py: tables 只在 v14 / v15 的数字 0；ESM 只有 CHEERS 的页码）。
删减后正文变动段落中的数字 163 个（checks_v15/numcheck15.py）: 在 fourarm_report.md、v15 tables、v15 ESM、v14 manuscript 中全部找到；只按 v15 tables 与 ESM 查找时未找到 4 个 = Limitations 第 2 段的 "2008 to 2020"（ESME 队列的诊断年，文献 [50]，1m 分段时原样移动的旧文字，不是结果数值）。
被删的数值（1h、1i、1j，均仍在表或 ESM 中）: Table 2 B 的 UI 与概率（−330、8,901、0.245、4.228、83.1、90.8）；Table S4 的 6,531、−1,911、2,565、2,785；Table S5 的 [4,545, 6,256]；Table S6 的 389 [238, 570]；Table S7 的 −437、−254；Table 3 的 [2,881, 3,785]。
改写的数值: "fell by JPY 702 thousand"（1i-3）= Table S7 的 −702 的符号反转（v13 起同样的口径）；"ranged from JPY 1,920 … to JPY 3,044"（1j）= Table S4 B 的最小与最大值。

## 5. 本版变更的段落（由生成后的 docx 读回；checks_v15/regress15.py 用编辑日志判定每个变动单元对应哪一条；输出 checks_v15/out/r15_*.txt）

### 5.1 manuscript（168 段 → 168 段；未变 147；变动块 17；不能解释的 0）
| 块 | 位置 | 指示 |
|---|---|---|
| M1 | 题名页 Word count 行 | 1o |
| M2 | Study design 第 1 段 | 1a |
| M3 | Study design 第 3 段（删 ", extracted from 21 to 26 October 2026"） | 1n |
| M4 | Outcomes 第 1 段末句、第 2 段整段 | 1b、1c |
| M5 | Statistical analysis (2) 第 2 句 | 1d |
| M6 | Statistical analysis (4) 第 2 句 | 1e |
| M7 | Statistical analysis (7)（删 "; these values are conditional on the HR"） | 1f |
| M8 | Four strategies compared 前两句 | 1g |
| M9 | Exercise compared with pembrolizumab 三处 | 1h |
| M10 | Maximum affordable cost 3 段四处 | 1i |
| M11 | Sensitivity 段末句 | 1j |
| M12 | Discussion 第 1 段第 2 句、第 2 段整段 | 1k |
| M13 | Discussion "Most of the value" 段删末句 | 1k |
| M14 | Discussion "The maximum affordable cost was higher without pembrolizumab" 段删除 | 1k |
| M15 | Implications（删 ", because how a change … is unknown"） | 1l |
| M16 | Limitations 句替换并在 "Survival was modeled from reconstructed data" 前分段（新段 = 原段的段落与 run 格式；文字不改） | 1m |
| M17 | 文献第 71 条 | 2 |
备用删减（1o）: 未用。Results、Discussion、Implications、Limitations 的其余句子与段落未改。
Discussion 变为 7 段；Limitations 变为 2 段；Outcomes 仍为 2 段。

### 5.2 tables（单元 309 → 309；变动块 1；不能解释的 0）
- 3a Table 2 脚注 a: "Strategies are listed in order of total cost." 之后加 "A dash marks the cheapest strategy, which has no comparator."。表的版式不动。

### 5.3 ESM（单元 2,507 → 2,507；变动块 5；不能解释的 0）
- 3b Table S4 脚注 a 的略语表: 删 "HR, hazard ratio; " 与 "pCR, pathological complete response; "。其余 ICER（表中 "ICER, JPY 1,000 per QALY" 行）、JPY（表中）、QALY（表中）、UI（脚注 a 本身的 "95% UI"）仍在使用，保留。
- 3c Table S1（CHEERS）: 先用 v14 的分页（checks_v14/out/m14_stats.json）重建 v14 的 28 格，与 ESM_1_v14 逐格一致后，按 v15 的分页（checks_v15/out/m15_stats.json）写 v15。变化 4 格: 16（页 4〜27）、24（页 10〜11）、26（Discussion 由 8 段变 7 段 → "paragraphs 1 to 7"，页 11〜14；Limitations 整体引用，2 段都在页码内）、27（p. 26）。第 4 项（Study design 第 3 段，1n 改动的句子）Location 不变。Outcomes 仍 2 段 → 第 11 项不变。第 19、21、22、25 项不加页码（v12 规则）。页码独立核对（checks_v12/pdf_pages.py，Word 导出的 manuscript PDF）: 定位 144 段、页码不符 0；未定位 10 段（抄录 Purpose 段、文献 7 条、Fig. 3 图注；段尾未定位，同 v14，都不是 Location 引用的段落）。
- 3d ESM_1_v15.pdf: Word SaveAs2(17)，48 页。

### 5.4 代码（3d）
- 作业树 R/22_phase2b_main.R 第 112 行注释 "Table 2 of the manuscript" → "Table 3 of the manuscript"（只此一行，换行符保持）。
- 公开目录同改，本地 commit fbf19be（父 4a883ed；作者 "the authors"、邮箱空；-c core.autocrlf=false，blob 与文件字节一致；无远程、未推送）。

## 6. 文献（指示第 2 步）

- 第 71 条: "Ann Oncol (in press)" → "Ann Oncol 37:1467–1479"（年 2026 不变）。依据: Crossref（api.crossref.org/works/10.1016/j.annonc.2026.08.002）卷 37、期 11、页 1467-1479、published-print 2026-11；PubMed（PMID 42636977）"2026 Nov;37(11):1467-1479"，EPub 2026 Aug 24。DOI 解析到 linkinghub.elsevier.com（脚本跳转），出版社页面 annalsofoncology.org 与 sciencedirect.com 对抓取返回 403，DOI 页本身无法读取；以 DOI 注册元数据（Crossref）与 PubMed 一致为准。格式同其他期刊条目（"刊名 卷:起–止"，en dash）。
- **第 8 条: 未改（指示: 只接受同一日期的清单）。** 厚生劳动省「薬価基準収載品目リスト及び後発医薬品に関する情報について（令和8年4月1日適用）」页面 https://www.mhlw.go.jp/topics/2026/04/tp20260401-01.html（2026-11-04 读取）: 第 2 节注射薬只挂 11 月 1 日施行分 /topics/2026/04/xls/tp20261101-01_02.xlsx（与 PDF /topics/2026/04/dl/tp20261101-01_02.pdf）；含 "1014" 的文件只剩 _03（外用薬）、_05、_06（その他），10 月 14 日施行分的 _02（注射薬）已不在站内；原网址 tp20261014-01_02.xlsx 返回 404。候选地址（只报告）:
  1. 站内更新日期的清单: https://www.mhlw.go.jp/topics/2026/04/xls/tp20261101-01_02.xlsx（11 月 1 日施行分；日期不同，按指示不接受）。
  2. 站外存档（同一文件）: http://web.archive.org/web/20261015005104/https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_02.xlsx（Wayback Machine，2026-10-15 快照，状态 200；未下载核对内容）。
- 改后重跑（checks_v11/refcheck.py → checks_v15/out/refcheck_v15.*）: DOI 61/61 由 doi.org 解析（302）；作者不符 0、年不符 0；卷页标记 10、58（v12 起已查明的检查器假阳性）；第 71 条卷、页、年与 Crossref 一致（v14 的标记消除）。无 DOI 17 条: 15 条 HTTP 200、第 8 条 404（未改）、第 52 条图书。78 条记录中除 HTTP 状态外与 v14 不同的只有第 71 条。
- 初出顺（checks_v15/citeorder15.py）: 正文 60 段、引用 60 组、109 个号（v14: 61 组、110 个号），1〜71 无缺。变化: Study design 第 1 段的 [7] 随 1a 删去（[7] 初出在 Introduction）；[28–31] 由删除的 Discussion 段移到 Discussion 第 1 段（1k）。78 条全部被引用；72〜78 只在 tables 与 ESM；tables 与 ESM 的引用序列与 v14 相同。

## 7. 第 4 步的核对结果

### 7.1 表与图编号（checks_v15/tfnum15.py；out/tfnum15.txt、cite_tf_detail15.txt）
扫描正文 60 段，取出提及 49 个（展开后）。Table [1, 2, 3]、Fig. [1, 2, 3]、Table S [1..11]、Fig. S [1, 2]，初出顺 1..n，最大号 = 实物数（3、3、11、2）；ESM 内顺序 S1〜S11、Fig. S1〜S2；Supplementary Methods S1 正文 4 处。明确引用（不计范围展开）: Table S4 2 次（Results 第 2 节 1h、Sensitivity 段 1j）、S5〜S7 各 1 次（Maximum affordable cost 节 1i）、S8 2、S9 2、S10 1、S11 2（Sensitivity 段与 Limitations 1m）、S2 2（Survival… 段与 Statistical analysis (4) 1e）、S1 1、S3 1；Fig. S1 1、Fig. S2 1。

### 7.2 段落 > 150 词、句子 > 60 词（checks_v11/sec10.py；out/sec10_v15.txt）
- 段落 > 150 词: 1 段 = Implications（161 词）。v14: 3 段（Results 第 2 节 170 词已由 1h 缩短；Limitations 由 1m 分为 2 段）。
- 句子 > 60 词: 3 句 = Introduction 目的段 "It compared the four strategies …"（80 词）、Outcomes 第 2 段第 1 句 "Secondary outcomes were …"（79 词）、Statistical analysis (6) "To test other assumptions …"（67 词）。v14 最长 121 词（1c 拆为两句）。
- 其他计数: 扫描抄录 5 段 + 正文 45 段、135 句；超过 30 词的句子 44（v14 47）；禁用语 0、开场套话 0、接续词连发 0、因果词 0、破折号 — 0、中黑「・」0；裸时间词 3（currently、now、current，同 v14）。

### 7.3 格式（规约第 8 节；checks_v11/fmt_audit.py → out/fmt_v15.txt）
manuscript: Heading 样式 0（168 段全 Normal）；180/180 run 12 pt Times New Roman、自动色；行号有（lnNumType）；非空 165 段 line = 480；粗体 26 run（同 v14：题名、大标题、抄录标签、Statements 标签、图注标签），句中粗体 0。1m 的新段与原段同格式（段落属性与 run 属性复制）。tables 369/369、ESM 2,660/2,660 run 12 pt TNR、自动色；表的粗体只在面板行与标签行；版式未动。
check_acronyms（ARS 3.24.0；抽出方法同 v14）: 抄录与正文的报告与 v14 逐字节相同（抄录 No findings、coverage partial；正文 partial，Not defined PMC、CHEERS、EQ）。

## 8. 著者侧与用户待定的事项

1. 文献第 8 条（第 6 节）: 站内只有 11 月 1 日施行分；同一文件只在站外存档。处理方法待用户决定。
2. v14 第 7 节的其余项: Table 2 "—" 已由 3a 说明（解决）；S4 脚注 a 的 HR、pCR 已由 3b 删除（解决）；Table 2 B 与 S4 基准列同值（指示的设计）照旧；目的与不足的对应、Discussion 第 1 段只答目的①照旧（指示的结构）。
3. v13 第 8 节第 1〜6 项照旧。

## 9. 撤回的主张

- v12 的 1b（正文 "5 million Japanese yen (JPY)"）仍为撤回（只在抄录 Methods 段）。
- v14 第 8 节列出的被替换文字未复活。
- 本版按指示删去（以后不应复活）: Study design 第 1 段 "Both treatments were in use in Japan in 2024 [7]"；Outcomes 第 1 段 "the incremental medical costs other than the program cost" 的重述；Statistical analysis (2) 的 "extendedly dominated"、(4) 的分布逐项说明（改为指向 Table S2）、(7) 的 "these values are conditional on the HR"；Results 中第 4 节列出的数值；Discussion "Cheaper metastatic treatment …" 句与 "The maximum affordable cost was higher without pembrolizumab" 段；Implications 的 "because how a change in pCR … is unknown"；Limitations 的 "values from Japanese populations gave nearly the same results as the German value set"；Study design 第 3 段的抽取日期 "extracted from 21 to 26 October 2026"。

## 10. 共著者コメント台帳

本版无共著者交回的文件。采否 = 用户的 v15 指示第 1〜5 步。

## 11. 过去意外退回的地方

规约第 1.2 节第 7 条名指的五处逐一确认，无退回: 题名（manuscript、ESM 与 v14 相同）；责任著者占位行（题名页 1〜4 行与 Statements 未动）；补充表脚注（只有 S4 脚注 a 按 3b 改）；语数（按实测）；图解像度（Fig1〜3 与 v14 逐字节相同，600 dpi）。本项目未记录过其他退回位置。

## 12. 文献检索的记录

沿用 v11 第 11 节。本版未改新规性句，未加文献；只更新第 71 条的书目。

## AUDIT（规约第 13 节；交付前再读规约全文后逐项一行）

最重要四项（先报告）:
1. 版: 通过。底本 = v14（9 个文件 sha256 与 MANIFEST_v14 一致）；交付后 manuscript/ 下只有 v15（v14 → archive/v14）。
2. 表与图: 通过。正文 60 段、提及 49 个；Table 1〜3、Fig. 1〜3、Table S1〜S11、Fig. S1〜S2 全部在正文地の文以编号引用（S4〜S11、Fig. S1〜S2 各至少 1 次明确引用）；Supplementary Methods S1 4 处；CHEERS = Table S1。
3. 文献的真伪: **第 8 条除外通过。** DOI 61/61 解析、作者与年 0 不符、第 71 条已与 Crossref 一致；卷页标记 10、58 为检查器假阳性；无 DOI 17 条中 15 条 200、第 52 条图书、**第 8 条网址 404（同一日期的清单在站内找不到，按指示未改，第 6 节）**。
4. 文献的顺序: 通过。正文 1〜71 初出顺无缺（60 组、109 个号）；72〜78 只在 tables 与 ESM；78 条全部被引用。

版
- [x] 作业树只有最新版（manuscript/ 下 v15、code、archive、_inbox 空）。
- [x] 会话开始时 sha256 与 MANIFEST_v14 一致（9/9）。
- [x] 底本 = v14，worklog 开头写了底本与 sha256。
- [x] 意外退回 0（第 11 节）。
- [x] 表与 ESM 的数值与 v14 完全一致（tables 数字差 0；ESM 只有 CHEERS 页码）；正文只删减与改写（第 4 节）。
- [—] 模板占位: 尾崎的占位（第 14 节），不动、不报告。
- [x] 版本标签、作业注记、ARS 标记 0。
- [x] MANIFEST_v15 写好、v14 移入 archive（交付时）。
- [x] 解析输出 sha256（MANIFEST_v15）: 本版未重算模型，来源文件与 v14 相同（R/22 只改注释，见 MANIFEST）。
- [x] 差分全部对应指示（manuscript 17 块、tables 1、ESM 5；不能解释的 0）。
- [x] 撤回主张复活 0（第 9 节）。
- [x] 修订与批注 0（Word COM，三个 docx）。
- [x] 作业树无 ars/。

文献与编号
- [x] 初出顺 1〜71 无缺；未引用 0、表外号 0。
- [ ] DOI 与书目: 61/61 解析、书目不符 0（第 71 条已改）；第 8 条网址 404（第 8 节第 1 项）。
- [—] 新引用: 无（Discussion 第 1 段的 [28–31] 为既有引用移位，支持同一主张: 帕博利珠单抗在各国划算）。
- [—] ARS citation-check: 未增文献；第 71 条为书目更新，按 DOI 实测核对。
- [x] 作者名-年份式的正文引用 0。
- [x] 超过 10 年 8 条、自引 0（文献未增减）。
- [x] 新规性句未改。
- [x] 四系列初出顺 1..n。
- [x] 各系列最大号 = 实物数。
- [x] 每个表与图在正文地の文至少一次。
- [x] ESM 内顺序为编号顺。
- [x] Supplementary Methods S1 与 CHEERS 清单由正文引用。
- [x] Fig1〜3.tif 已附，Fig. 1 起依次在正文提及。

标题与格式
- [偏离] 大标题: BCRT 结构（偏离 1）；Results 二级标题 5 个（v14）。
- [x] 规约外的节与项目: v14 与 v15 相同，未增未减。
- [偏离] Methods 小标题 5 个（偏离 1）。
- [x] Heading 样式 0。
- [x] 全部 run 12 pt Times New Roman（manuscript 180/180、tables 369/369、ESM 2,660/2,660）。
- [x] 行号有。
- [x] 双倍行距（非空 165 段）。
- [x] 句中粗体 0。
- [x] 表的列头与数值无粗体。
- [x] 非黑字 0。
- [x] 中黒「・」0。
- [x] 表页为横版（未动）。
- [偏离] 表脚注记号 a〜d；"Note" 开头 0。
- [x] 脚注记号与表内上标一一对应（Table 2、S4 的记号未变；S4 a〜c）。
- [x] 图 600 dpi（逐字节同 v14）。
- [x] 前付一项一段（尾崎，未动）。
- [x] 生成 AI 记述 0。
- [x] ARS 作业标记 0。
- [x] ARS 默认来源的结构 0（Conclusion 为既有）。
- [x] 美式拼写、"Fig." 统一。
- [x] 语数: 抄录 248 ≤ 250，正文 3,470 ≤ 3,500（目标 ≤ 3,480），写入题名页。

数值
- [x] 正文数字在数值台帳内（163 个，表或 ESM 中可找到，2008/2020 为文献年份）。
- [x] 表脚注数值（未改）。
- [注] 同一数值两表: Table 2 B 与 Table S4 基准列（指示的设计，照旧）。
- [—] n 的合计、流程图: 不适用。
- [—] 对象者数: 不适用。
- [x] 点估计在 UI 内（未改）。
- [x] 同一统计量各处同值（正文 2,053、0.722、0.638、3,443 等与表一致）。
- [—] p 值: 无。
- [x] 因果词 0。
- [x] 负号与千位逗号（本版正文去掉了负数；702 为 "fell by" 的正数写法）。
- [x] 小数位（未改）。

内容
- [x] Methods 无数值结果。
- [x] Results 无"使用了"型。
- [x] 结果句有表的参照（1h 第二处仍引 Table S4；1i 仍引 S5、S6、S7；1j 引 S4）。
- [x] 各解析的目的句（未改）。
- [注] Introduction 末两段（未改；v14 的注照旧）。
- [注] 目的对应: v14 的对应表照旧；Discussion 删除 1 段后，第 4〜5 段（Most of the value、Duration）与第 6、7 段对应目的③。
- [x] 曝露与结局名称（未改）。
- [注] 抄录未改。
- [x] Results 段落顺序与段首名指（新 1g 仍以 Table 2 开头）。
- [x] Discussion 段首名指（第 1 段 Table 2）。
- [注] Discussion 第 1 段只回答目的①（照旧）。
- [x] Discussion 与 Results 的重复: 第 1 段重述 dominated（照旧）；第 2 段已去掉 28% 的数值表述（1k）。
- [x] Discussion 引用分布: 第 1〜7 段 1、1、1、0、1、2、1 组；后半无新出文献。
- [x] "further research is needed" 型 0。
- [x] 临床医会改变什么（Implications 未改主体）。
- [x] Implications 只删一个从句（1l）。
- [注] check_acronyms partial（同 v14）。
- [x] 限界只在 Limitations；1m 的新句保留影响句（"neither changed the conclusion"）。
- [x] Outcome/Variables 第一句（未改）。
- [x] 统计软件只写语言与版本（未改）。
- [x] Data availability 与公开仓库（未改；公开目录只改 R/22 注释）。
- [x] CHEERS 清单页码按 v15 实测（Word + PDF 独立核对，不符 0）。
- [x] 题名一致（未改）。
- [x] 事前计划、缺失、多重比较（未改）。
- [—] 选择流程图: 不适用。
- [x] 图未改。
- [x] 图表重复（未改）。
- [—] 著者贡献: 尾崎的占位。
- [x] AI 常套语 0；破折号 0；30 词超句 44、最长 80；150 词超段 1（第 7.2 节）。
- [注] 裸时间词 3（同 v14）。
- [x] 主张未变强（删减与指示原文；1k 第 1 段加的 "as it is on its own in Japan and elsewhere [28–31]" 为原 Discussion 段的既有主张移位）。
- [—] 查读回复版: 不适用。
- [—] humanizer / stop-slop: 未用（指示）。
