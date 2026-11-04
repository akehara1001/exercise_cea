# worklog v17（2026-11-04）

## 1. 底本

底本: manuscript_v16_BCRT.docx（v16，2026-11-04 交付，sha256 前 8 位 aa79255f）。同批: tables_v16_BCRT.docx（8236a3ee）、ESM_1_v16.docx（1955102c）、ESM_1_v16.pdf（c69a24fb）、Fig1〜3.tif（c13b748e、662046bf、d7926e1e）、cover_letter_v16_BCRT.docx（21ed7f1a）、worklog_v16.md。会话开始时 9 个文件的 sha256 全部与 MANIFEST_v16.md 一致；作业树 git 状态干净（HEAD c3fe44e）；manuscript/ 下只有 v16（另有 archive、code、空的 _inbox）。
本版只做 v17 指示列出的事: 文献第 8 条加内服药清单（第 1〜2 步）。不跑 ARS、humanizer、stop-slop。不重算任何数值。11/1 版注射药清单的两处降价不采用，理由见 worklog_v16 第 5.2 节（判定在第 5.3 节）。
编辑方法: v16 的 docx 直接编辑（manuscript/code/edit_manuscript_v17.py；lxml 只改 word/document.xml；原文须与 v16 第 8 条全文逐字一致）。tables_v17_BCRT.docx、Fig1〜3.tif、cover_letter_v17_BCRT.docx 为 v16 的逐字节复制。ESM_1_v17.docx: Table S1（CHEERS）页码按 v17 重核，1 格变（第 6.2 节），其余逐字节同 v16（manuscript/code/edit_esm_v17.py）。Word（COM）打开: manuscript 修订 0、批注 0、29 页；tables 修订 0、批注 0、9 页；ESM 修订 0、批注 0、48 页。ESM_1_v17.pdf 由 Word SaveAs2(17) 重新导出（48 页）。

## 2. 投稿先与投稿规格（沿用 v16 第 2 节）

- BCRT；抄录上限 250、正文上限 3,500 词；Springer 数字式文献；美式拼写；"Fig."。语数计法同 v14〜v16（checks_v14/word_wc14.py）。
- v17 实测: 正文 3,472（含 17 个标题 3,513），抄录 248（含标签 252），均与 v16 相同（第 8 条在文献表中，不计入）。各节: Introduction 569、Methods 1,350、Results 674、Discussion 489、Implications 162、Limitations 191、Conclusion 37。题名页 Word count 行 "abstract 248; main text 3,472" 不变，未改。
- 偏离照旧（v11 第 2 节）。

## 3. 用语表

沿用 v16。本版无改名。

## 4. 数值台帳

本版不改任何数值。tables 与 v16 逐字节相同；manuscript 的数字记号差只有第 8 条新加的网址中的数字；ESM 的数字记号差只有 Table S1 第 27 项的页码 26 → 27（页码，不是结果数值）（checks_v17/regress17.py）。

## 5. 文献第 8 条（第 1〜2 步）

### 5.1 来源为「薬価サーチ」的内服药（1a）
计算根据 input/params/ozaki/parameters_v1_尾崎記入案.xlsx「計算根拠_尾崎」中出处为「薬価サーチ、令和8年度薬価」或「同上」的内服药 5 行:

| 行 | 品目（计算根据的写法） | 用值 | 单位 | 用于 |
|---|---|---|---|---|
| 111 | リムパーザ150mg | 4,788 | 円/錠 | F05、D03、D03P（300 mg 1 日 2 次 = 150 mg 錠 2 錠 × 2 次） |
| 158 | カペシタビン300mg 後発品 | 46.4 | 円/錠 | F02 |
| 159 | ゼローダ300 | 107.3 | 円/錠 | F02（上限） |
| 174 | オランザピン5mg 後発品 | 14.3 | 円/錠 | A05 |
| 176 | デカドロン錠4mg | 23.4 | 円/錠 | A05（第 2〜3 日 DEX 8 mg 内服） |

另: 第 210 行「鎮痛薬・湿布と調剤（院外薬局）3,000 円」为【仮定】的概数，不是药价，不比对。parameters_v10.xlsx「計算根拠_原」无内服药。

### 5.2 两份内服药清单（1b）
- 11 月 1 日版: https://www.mhlw.go.jp/topics/2026/04/xls/tp20261101-01_01.xlsx（2026-11-04 下载，HTTP 200，726,965 字节，sha256 b5891578c228908434377b57ec2b9055671626cefa174e95862119e4d1f16030），存为 input/params/sources_price/tp20261101-01_01.xlsx。
- 10 月 14 日版: 原网址 https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_01.xlsx 现为 404。Wayback CDX 查到快照 1 个（20261014082215，HTTP 200）。以 id_ 形式取原始字节（http://web.archive.org/web/20261014082215id_/https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_01.xlsx，727,243 字节，sha256 21bb77b08fb9dd5fabf8776b89cfcb8db5ac3ee5316424e9b6418546e8888628），存为 input/params/sources_price/tp20261014-01_01.xlsx。条目中写的存档网址（无 id_）实测 200，内容与之逐字节相同。原文件当初未保存，无法与原件比对。
- 两版结构相同（工作表「ＨＰ用」，列同注射药清单，各 7,073 品目，区分全为「内用薬」）。全量比对（checks_v17/compare_oral_lists17.py → out/oral_compare17.txt、.json）: 增 0、删 0、变 2；2 个都是パキロビッドパック300、600 的「R8.11.1新薬価適用」降价，与本研究无关。

### 5.3 比对表（1c；后发品按「同规格最低价」重算）

| 行 | 品目 | 规格 | 依据 | 用值 | 10/14 版 | 11/1 版 | 一致 |
|---|---|---|---|---|---|---|---|
| 111 | リムパーザ錠150mg | 150mg1錠 | 品目 | 4,788 | 4,788 | 4,788 | 是 |
| 158 | カペシタビン 后发品（7 品目） | 300mg1錠 | 同规格后发品最低价 | 46.4 | 46.4 | 46.4 | 是 |
| 159 | ゼローダ錠300 | 300mg1錠 | 品目 | 107.3 | 107.3 | 107.3 | 是 |
| 174 | オランザピン 后发品（9 品目） | 5mg1錠 | 同规格后发品最低价 | 14.3 | 14.3 | 14.3 | 是 |
| 176 | デカドロン錠4mg | 4mg1錠 | 品目 | 23.4 | 23.4 | 23.4 | 是 |

最低价的品目（两版相同）: カペシタビン 300 mg = 「NK」「サワイ」「タカタ」「トーワ」「ヤクルト」「日医工」（「JG」64.8 不是最低）；オランザピン 5 mg = 一般名收载的「オランザピン5mg錠」「オランザピン5mg口腔内崩壊錠」（其余后发品 16）。用值 = 10/14 版: 5/5；用值 = 11/1 版: 5/5。

### 5.4 判定与改法（第 2 步）
**10/14 版快照存在且使用值全部一致 → (i)。** 第 8 条按指示原文改为（存档网址 = 20261014082215 的快照）:
"8. Ministry of Health, Labour and Welfare (2026) National Health Insurance drug price list and information on generic drugs: oral drugs and injections, products listed as of 14 October 2026 (in Japanese). https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_01.xlsx and https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_02.xlsx. Accessed 22 Oct 2026. Archived at http://web.archive.org/web/20261014082215/https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_01.xlsx and http://web.archive.org/web/20261015005104/https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_02.xlsx. Accessed 4 Nov 2026"
正文、表、ESM 的其他文字不动；Table S2 的 F02、F05 仍引 [8]（"[8,69]"、"[8,60]"，未动）。

## 6. 本版变更的段落（checks_v17/regress17.py；输出 out/r17_*.txt）

### 6.1 manuscript（169 段 → 169 段；未变 168；变动块 1；不能解释的 0）
| 块 | 位置 | 指示 |
|---|---|---|
| M1 | 文献第 8 条（全文按指示原文） | 2 (i) |
语数行不变（实测同 v16），未改。逐字节比较（out/bytes17.txt）: 24 个部件中只有 word/document.xml 不同；其中只有第 8 条一段不同。

### 6.2 tables、ESM
tables: v16 的逐字节复制（变动 0）。
ESM: Table S1 按 v17 重核（先用 v16 的分页重建 v16 的 28 格并与 ESM_1_v16 逐格一致）。第 8 条加长 1 行，第 10 条以后的文献与 Statements and Declarations 后移，Funding 由第 26 页移到第 27 页 → **第 27 项（Source of funding）"Statements and Declarations, Funding (p. 26)" → "(p. 27)"**；其余 27 格不变（Data availability "pp. 4 to 27" 不变；Title page 至 Conclusion 各段页码不变）。依据: 规约第 9 节与第 13 节（清单各项对应正文的页与节）；指示的「ESM 不变则逐字节复制」。逐字节比较: 27 个部件中只有 word/document.xml 不同，其中只有这一格不同。页码独立核对（checks_v12/pdf_pages.py，Word 导出的 manuscript PDF）: 定位 144 段、页码不符 0；未定位 11 段（与 v16 相同的 11 段，都不是 Location 引用的段落）；PDF 上 Funding 在第 27 页，ESM_1_v17.pdf 第 8 页为 "Funding (p. 27)"。

### 6.3 公开代码
本版无改动（exercise_cea_public 的 git 状态干净，HEAD fbf19be）；无需提交。

## 7. 第 3 步的核对结果

- 第 8 条网址各实测一次（out/ref8_urls17.txt；curl，默认 UA）: [1] tp20261014-01_01.xlsx 原址 404；[2] tp20261014-01_02.xlsx 原址 404（同 v16）；[3] 内服药存档 200（xlsx，727,243 字节，sha256 = 所存 10/14 版）；[4] 注射药存档 200（xlsx，386,582 字节，sha256 = 当初保存的原文件）。
- 文献全体（checks_v11/refcheck.py → out/refcheck_v17.*）: 输出与 v16 逐字相同。DOI 61/61 由 doi.org 解析（302）；作者不符 0、年不符 0；卷页标记 10、58（已知的检查器假阳性）；无 DOI 17 条: 15 条 HTTP 200，第 8 条检查器只测第一个网址（= 上面 [1]，404），第 52 条图书。
- 初出顺（checks_v17/citeorder17.py）: 正文 61 段、60 组、109 个号，1〜71 无缺；manuscript、tables、ESM 的引用序列与 v16 完全相同；78 条全部被引用；72〜78 只在 tables 与 ESM。
- 四系列编号（checks_v17/tfnum17.py）: 扫描正文 61 段、提及 49 个；Table [1,2,3]、Fig. [1,2,3]、Table S [1..11]、Fig. S [1,2]，初出顺 1..n，最大号 = 实物数；ESM 内顺序为编号顺；Supplementary Methods 提及 4、全带 S1。
- 与 v16 的逐字节比较: 第 6.1、6.2 节；Fig1〜3.tif、cover letter 逐字节相同。
- 词数: 正文 3,472 ≤ 3,500；抄录 248 ≤ 250（同 v16）。
- 格式（规约第 8 节；checks_v11/fmt_audit.py → out/fmt_v17.txt、fmt_esm17.txt）: manuscript 与 ESM 的输出与对 v16 重跑的输出逐行相同。manuscript: Heading 样式 0（169 段全 Normal）；181/181 run 12 pt Times New Roman、自动色；行号有；非空 166 段 line = 480；粗体 26 run（标题与标签），句中粗体 0。中黒 0；破折号: manuscript 0，tables 18、ESM 121 为空格记号 "—"（同 v16）。版本标签 0、[TO CONFIRM] 0。
- 第 10 节（checks_v11/sec10.py → out/sec10_v17.txt）: 与 v16 逐字相同（禁用语 0、开场套话 0、接续词连发 0、因果词 0；超过 30 词的句子 46、最长 67；超过 150 词的段落 0；裸时间词 3）。
- check_acronyms（ARS 3.24.1）: 抄录与正文的报告与 v16 逐字相同（partial；同既有）。

## 8. 著者侧与用户待定的事项

1. 模型中 D03、D03P、D05 的月额用的是 10/14 版药价；2026 年 11 月 1 日起戈沙妥珠单抗与德达妥珠单抗降价约 11%（worklog_v16 第 5.2 节）。本版按指示不改数值；是否按 11/1 版重算由用户决定。
2. v16 第 8 节第 2 项（口服药不在第 8 条中）已由本版解决。
3. 只报告: 第 8 条的 "Accessed 22 Oct 2026" 按指示原文也覆盖内服药清单；内服药的用值当时取自「薬価サーチ」（令和8年度薬価），与 10/14 版内服药清单逐项一致（第 5.3 节）。
4. v16 第 8 节的其余事项照旧。

## 9. 撤回的主张

v12〜v16 列出的撤回与删除项未复活（退行检查）。本版无新撤回。

## 10. 共著者コメント台帳

本版无共著者交回的文件。采否 = 用户的 v17 指示第 1〜4 步。

## 11. 过去意外退回的地方

五处名指确认，无退回: 题名、责任著者占位行（题名页、Statements 未动）、补充表脚注（ESM 只变 Table S1 第 27 项一格）、语数（实测同 v16）、图解像度（逐字节同 v16，600 dpi）。

## 12. 文献检索的记录

沿用 v11 第 11 节。本版未加文献；第 8 条加内服药清单与其存档网址。

## AUDIT（规约第 13 节；交付前再读规约全文后逐项一行）

最重要四项（先报告）:
1. 版: 通过。底本 = v16（9 个文件 sha256 与 MANIFEST_v16 一致）；交付后 manuscript/ 下只有 v17（v16 → archive/v16）。
2. 表与图: 通过。正文 61 段、提及 49 个；全部表与图（补充含）在正文地の文以编号引用。
3. 文献的真伪: 通过（第 8 条按指示处理）。DOI 61/61 解析、书目不符 0；第 8 条两个原网址 404，两个存档网址 200（内容与所存文件逐字节相同）；无 DOI 的其余 15 条 200、第 52 条图书。
4. 文献的顺序: 通过。1〜71 初出顺无缺；72〜78 只在 tables 与 ESM。

版
- [x] 作业树只有最新版。
- [x] 会话开始时 sha256 与 MANIFEST_v16 一致（9/9）。
- [x] 底本 = v16，worklog 开头写了底本与 sha256。
- [x] 意外退回 0。
- [x] 数值不变（tables 逐字节同 v16；manuscript 只有第 8 条网址；ESM 只有 CHEERS 页码 26 → 27）。
- [—] 模板占位: 尾崎的占位，不动、不报告。
- [x] 版本标签、作业注记、ARS 标记 0。
- [x] MANIFEST_v17 写好、v16 移入 archive（交付时）。
- [x] 解析输出未变（未重算）。
- [x] 差分全部对应指示（manuscript 1 块 = 2 (i)；ESM 1 格 = 页码重核；不能解释的 0）。
- [x] 撤回主张复活 0。
- [x] 修订与批注 0。
- [x] 作业树无 ars/。

文献与编号
- [x] 初出顺 1〜71 无缺；未引用 0。
- [x] DOI 61/61、书目不符 0；第 8 条见上。
- [x] 新引用: 无新文献；第 8 条新加的内服药清单与比对表并列确认（第 5.3 节，用值 5/5 一致）。
- [—] ARS citation-check: 未增未移文献。
- [x] 作者名-年份式的正文引用 0。
- [x] 超过 10 年 8 条、自引 0（未增减）。
- [x] 新规性句未改。
- [x] 四系列初出顺 1..n。
- [x] 各系列最大号 = 实物数。
- [x] 每个表与图在正文地の文至少一次。
- [x] ESM 内顺序为编号顺。
- [x] Supplementary Methods S1 与 CHEERS 清单由正文引用。
- [x] Fig1〜3 已附、依次提及。

标题与格式
- [偏离] 大标题与 Methods 小标题: BCRT 结构（偏离 1）。
- [x] 规约外的节与项目: 与 v16 相同。
- [x] Heading 样式 0。
- [x] 全部 run 12 pt Times New Roman。
- [x] 行号有。
- [x] 双倍行距。
- [x] 句中粗体 0。
- [x] 表的列头与数值无粗体（tables 逐字节同 v16）。
- [x] 非黑字 0。
- [x] 中黒 0。
- [x] 表页为横版（未动）。
- [偏离] 表脚注记号 a〜d；"Note" 开头 0。
- [x] 脚注记号一一对应（未动）。
- [x] 图 600 dpi（逐字节同 v16）。
- [x] 前付一项一段（尾崎，未动）。
- [x] 生成 AI 记述 0。
- [x] ARS 作业标记 0。
- [x] ARS 默认来源的结构 0。
- [x] 美式拼写、"Fig." 统一。
- [x] 语数实测、与题名页一致、在上限内（248 ≤ 250；3,472 ≤ 3,500）。

数值
- [x] 正文与抄录的数值与 v16 相同。
- [x] 表脚注数值（未动）。
- [注] 同一数值两表: Table 2 B 与 Table S4（指示的设计，照旧）。
- [—] n 的合计、流程图: 不适用。
- [—] 对象者数: 不适用。
- [x] 点估计在 UI 内（未动）。
- [x] 同一统计量各处同值（未动）。
- [—] p 值: 无。
- [x] 因果词 0。
- [x] 负号、千位逗号（未动）。
- [x] 小数位（未动）。

内容
- [x] Methods 无数值结果。
- [x] Results 无"使用了"型（未动）。
- [x] 结果句有表的参照（未动）。
- [x] 各解析的目的句（未动）。
- [注] Introduction 末两段: v14 起的注照旧。
- [注] 目的对应: 照 v16。
- [x] 曝露与结局名称（未动）。
- [x] 抄录（未动）。
- [x] Results 段落顺序与段首名指（未动）。
- [x] Discussion 段首名指（未动）。
- [注] Discussion 第 1 段只答目的①（照旧）。
- [x] Discussion 与 Results 的重复（未动）。
- [x] Discussion 引用分布（未动）。
- [x] "further research is needed" 型 0。
- [x] 临床医会改变什么（未动）。
- [x] Implications 2 段（未动）。
- [注] check_acronyms partial（同 v16）。
- [x] 限界只在 Limitations（未动）。
- [x] Outcome/Variables 第一句（未动）。
- [x] 统计软件（未动）。
- [x] Data availability 与公开仓库（未动）。
- [x] CHEERS 页码按 v17 实测（Word + PDF 独立核对，不符 0；第 27 项 p. 26 → p. 27，其余 27 格不变）。
- [x] 题名一致（未动）。
- [x] 事前计划、缺失、多重比较（未动）。
- [—] 选择流程图: 不适用。
- [x] 图未改。
- [x] 图表重复（未动）。
- [—] 著者贡献: 尾崎的占位。
- [x] AI 常套语 0；破折号 0（正文）；30 词超句 46、最长 67；150 词超段 0。
- [注] 裸时间词 3（同 v16）。
- [x] 主张未变强（正文未动）。
- [—] 查读回复版: 不适用。
- [—] humanizer / stop-slop: 未用。
