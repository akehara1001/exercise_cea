# worklog v12（2026-10-29）

## 1. 底本

底本: manuscript_v11_BCRT.docx（v11，2026-10-28 交付，sha256 前 8 位 58b6897a）。同批: tables_v11_BCRT.docx（d022962f）、ESM_1_v11.docx（aa0d4e94）、ESM_1_v11.pdf（52c2716f）、Fig1〜3.tif（c13b748e、662046bf、d7926e1e）、cover_letter_v11_BCRT.docx（21ed7f1a）、worklog_v11.md（ad8b4771）。会话开始时 9 个文件的 sha256 全部与 MANIFEST_v11.md 一致；作业树 git 状态干净（HEAD 06be069）。
本版是共著者交回之后的小修：不跑 ARS 起草、humanizer、stop-slop；只做指示第 1、2 步的修改与第 3 步的公开用代码，第 4 步只核对。
编辑方法: v11 的 docx 直接编辑（manuscript/code/edit_manuscript_v12.py、edit_esm_v12.py；lxml 只改 word/document.xml，其余部件逐字节照搬；每条原文须在 v11 中唯一命中，否则停止）。tables、Fig1〜3.tif、cover letter 为 v11 的逐字节复制（cmp 确认）。manuscript 与 ESM 由 Word（COM）打开确认：修订 0、批注 0。

## 2. 投稿先与投稿规格（沿用 v11 第 2 节）

- 投稿先 BCRT；抄录结构式，上限 250 词；正文上限 3,500 词；Springer 数字式文献；美式拼写；"Fig."。
- 语数计法（同 v11）: Word ComputeStatistics（逐段），抄录 = 四个结构段去掉 4 个标签；正文 = Introduction 至 Conclusion，不含标题。
  - v12: 抄录 250（含标签 254）；正文 3,244（含 16 个标题 3,279）。→ 题名页 Word count 行改为 "abstract 250; main text 3,244"（1e）。
  - 变化的来源: 1a 抄录 −2（"The analysis took" → "It took"、"per year" → "annually"）+2（"JPY 5 million" → "5 million Japanese yen (JPY)"），合计 0；1b 正文 +2；1c 分段不改词数。
- 投稿先与共著者决定的偏离（v11 第 2 节，本版照旧不动）: 1. 标题结构（Methods 5 个小标题、Results 4 个、Implications 与 Limitations 为 Discussion 下的小标题、Conclusion 大标题；二级标题斜体）；2. 表脚注记号 a〜d；3. 题名页在 manuscript 内、表另成 tables 文件、图为 tif；4. 文献 72〜78 只在 Table 1 与 ESM，不重排。

## 3. 用语表

沿用 v11 第 3 节，本版无改名。"Japanese yen (JPY)" 在抄录（1a）与 Study design 第 2 段（1b）展开；正文的初出展开仍在 Introduction 第 1 段（"398,924 Japanese yen (JPY)"，v11 既有），1b 是正文中的第二次展开（按指示）。

## 4. 数值台帳

本版不改任何结果数值。来源文件 = v9 数值台帳第 8 节的 57 个文件（清单 manuscript/code/checks_v11/out/src_sha_v9.txt），本次重算 sha256: 变动 0、缺失 0。
v11→v12 数字记号的差（manuscript/code/checks_v11/regress.py）:
- manuscript: 只在 v11: 3,242（Word count）、26（文献 65 的 Accessed 日）、"-03"（文献 65 旧网址）。只在 v12: 3,244（Word count）、2016（文献 10 的 "2016(9)"）、29（Accessed 29 Oct 2026）、03 与 661（文献 65 新网址）。全部来自指示原文或实测。抄录数值不变（"5 million" 的 5 不变）。
- tables: 与 v11 逐字节相同（数字记号 335 个一致）。
- ESM: 只在 v11: 10（第 24 项 "pp. 9 to 10"）。只在 v12: 3 ×2（第 14、15 项 "paragraph 3"）、11（第 24 项 "pp. 9 to 11"）。其余数值一致。

## 5. 本版变更的段落（由生成后的 docx 读回；checks_v11/regress.py、regress2.py）

### manuscript（v11 163 段 → v12 164 段；未变 155；变动块 8，全部对应指示）
| 块 | 位置 | 指示 |
|---|---|---|
| M1 | 题名页 Word count 行 | 1e |
| M2 | 抄录 Methods（两句） | 1a |
| M3 | Study design 第 2 段 | 1b |
| M4 | Exercise effect and costs 第 1 段 → 第 1、2 段（原第 2 段成为第 3 段） | 1c |
| M5〜M8 | 文献 10、28、58、65 | 1d |

1c: 在 "and the effect held until it stopped." 之后分段；新第 2 段 = "In an alternative pathway, …" 与 Musculoskeletal 一句，文字一字未改（第 1 段 + 空格 + 第 2 段 = 原段落，脚本断言）。新段落为原段落的深拷贝（pPr = line 480；run = 12 pt Times New Roman），格式与前段相同；本段 166 词 → 第 1 段与第 2 段均 < 150 词。

逐段差分（原文 → 新文）:
- [M1] P unit 6: 「3,242」→「3,244」
- [M2] P unit 10: 「The analysis」→「It」; 「per year.」→「annually.」; 「JPY 5 million」→「5 million Japanese yen (JPY)」
- [M3] P unit 23: 「JPY 5 million」→「5 million Japanese yen (JPY)」
- [M4] P unit 29 → 29〜30: 「… and the effect held until it stopped. In an alternative pathway, …」→ 第 1 段「… and the effect held until it stopped.」／第 2 段「In an alternative pathway, exercise raised pCR by 0 to 10 percentage points without changing the recurrence HR; patients added to the pCR group took the event-free survival of patients with pCR given the same treatment. Musculoskeletal adverse events occurred at the rates observed in CHALLENGE [9].」
- [M5] 文献 10: 「Cochrane Database Syst Rev 9:CD005001.」→「Cochrane Database Syst Rev 2016(9):CD005001.」
- [M6] 文献 28: 「Huang M, A Fasching P, Haiderali A」→「Huang M, Fasching PA, Haiderali A」
- [M7] 文献 58: 「the current evidence?. Br J Cancer」→「the current evidence? Br J Cancer」
- [M8] 文献 65: 「https://www.pbs.gov.au/info/industry/listing/elements/pbac-meetings/psd/2023-03/pembrolizumab-earlyTNBC-keytruda-PSD-March-2023. Accessed 26 Oct 2026」→「https://www.pbs.gov.au/industry/pbac/psd/2023/03/pembrolizumab-march-2023-a661. Accessed 29 Oct 2026」

### tables
v11 的逐字节复制（tables_v11_BCRT.docx → tables_v12_BCRT.docx，只改文件名）。变动 0。

### ESM（2,404 单元，变动 5，全部对应第 2 步）
- [E1] 第 12 项: 「Methods, Exercise effect and costs, paragraph 1;」→「… paragraphs 1 to 2;」（页 pp. 6 to 7 不变）
- [E2] 第 14 项: 「… paragraph 2;」→「… paragraph 3;」（pp. 6 to 7 不变）
- [E3] 第 15 项: 「… paragraph 2;」→「… paragraph 3;」（pp. 6 to 7 不变）
- [E4] 第 17 项: 「… paragraph 1;」→「… paragraphs 1 to 2;」（pp. 6 to 8 不变）
- [E5] 第 24 项: 「(pp. 9 to 10)」→「(pp. 9 to 11)」（v12 分页: Results, Sensitivity and scenario analyses 第 1 段跨第 10〜11 页）
28 项的页码全部按 v12 重新计算（Word 对 manuscript_v12_BCRT.docx 的 Range.Information(3)）；变了的只有第 24 项。脚本先用 v11 的分页与 v11 的文字重建 v11 的 28 格，与 ESM_1_v11 逐格一致后才写 v12（edit_esm_v12.py）。第 19、21、22、25 项不加页码（第 22 项只在表中报告）。
页码的独立核对: 在 Word 导出的 manuscript PDF 中按每段首尾 6 词定位，139 段定位、页码不符 0（未定位 10 段: 文献 7 条〔DOI 或网址跨行〕、抄录 Purpose 段与 Fig. 3 图注各 1，均只有段尾未定位，且都不是 Location 引用的段落；checks_v12/pdf_pages.py）。
ESM 其余部分一字未改（regress.py: 2,399 单元未变）。

## 6. 第 4 步的核对结果

### 6.1 文献（checks_v11/refcheck.py 在 v12 上全量重跑；checks_v12/citeorder.py）
- 1d 的 4 条（改后打开确认，2026-10-29）:
  - 10: doi.org → 302（doi.wiley.com）；Crossref volume 2016、issue 9、无页（文章号 CD005001）；PubMed PMID 27650122 vol 9、issue 9、pages CD005001、2016 Sep 21。新写法 "2016(9):CD005001" 与 Crossref 的卷号一致。Cochrane 网站对自动访问返回 412，未能打开页面。
  - 28: doi.org → 302（link.springer.com）；出版社页面 citation_author "Huang, Min"、"A. Fasching, Peter"、"Haiderali, Amin"，Adv Ther 40(3):1153–1170。Crossref 与 PubMed 都把姓登记为 "A. Fasching"；新写法 "Fasching PA" 按指示（实名 Peter A. Fasching；与同表文献 55 "Kuemmel S, Fasching PA" 一致）。
  - 58: doi.org → 302（nature.com）；出版社页面题名以 "…interpret the current evidence?" 结尾，Br J Cancer 135(3):329–335。新写法与之一致。
  - 65: 新网址 HTTP 200，页面标题 "Pembrolizumab – March 2023 | Pharmaceutical Benefits Scheme (PBS)"，"Pembrolizumab (early breast cancer) … Keytruda® … Merck Sharp & Dohme (Australia) Pty Ltd … Meeting Date: March 2023 … Public Summary Document (PSD) March 2023 PBAC Meeting"；链接的 PSD PDF（40 页）首页 "Public Summary Document - March 2023 PBAC Meeting … 6.08 PEMBROLIZUMAB … early stage triple negative breast cancer"。Accessed = 打开确认的当天 29 Oct 2026（本机日期）。
- 全量 DOI: 61/61 doi.org 解析（302）；Crossref 逐字段: 作者 0 不符、年 0 不符；卷 1 条（58）、页 2 条（10、58）为检查器的假阳性: 58 是解析器以 ". " 分隔题名与刊名，问号后去掉句点后刊名并入题名（直读为 Br J Cancer 135:329–335，与 Crossref 一致）；10 是 Crossref 只有文章号无页（v11 同）。撤稿与关注表达标记 0（relation 只有 has-review、has-preprint、is-supplemented-by；10 的 update-to new_version 是 Cochrane 新版）。
- 无 DOI 17 条: 16 条网址 HTTP 200（65 由 301 变为 200）；第 52 条图书（v11 已经 Minds 与国会图书馆确认）。
- 初出顺: 正文（Introduction 至 Conclusion，56 段）取出引用组 61、号 110（展开后），初出顺 = 1, 2, …, 71，无缺号。manuscript（至 References）、tables、ESM 的引用序列与 v11 完全相同（61、24、126 组）。78 条全部被引用；72〜78 只在 tables 与 ESM（不重排，偏离 4）。
- ARS citation-check: 本版没有增加或移动文献（只订正 4 条的书目写法），按规约第 1.3 节不是必须项，未跑；DOI 实测如上全量重跑。

### 6.2 表与图编号（规约第 7.1 节第 9 条；checks_v12/tfnum.py = checks_v11/tfnum.py 只换文件名，v11 时以植入违反鸣过）
扫描正文 56 段，取出提及 43 个（展开后）。Table [1, 2, 3]，最大 3 = 表 3 个；Fig. [1, 2, 3]，最大 3 = Fig1〜3.tif = 图注 3；Table S [1..10]，最大 10 = ESM 补充表 10，ESM 内顺序 S1〜S10；Fig. S [1, 2]，最大 2，顺序 S1、S2。每个编号初出在地の文。Supplementary Methods S1 正文 4 处，不带 S1 0 处。

### 6.3 数值
除 Word count 一行外，抄录、正文、表、ESM 的全部数值与 v11 一致（第 4 节；新出现的数字只来自指示原文与 Table S1 页码）。来源文件 57 个 sha256 未变。

### 6.4 退行
manuscript 8 块、tables 0、ESM 5 块，全部对应指示（第 5 节）；对应不上的 0。名指确认: 题名（manuscript 与 ESM 未变）；责任著者占位行（尾崎，未动）；补充表脚注（ESM 未变，Table S1 脚注 a 与 v11 相同）；表脚注（tables 逐字节相同）；语数（按 1e 改为实测）；图解像度（600 dpi，第 6.6 节）。

### 6.5 格式（规约第 8 节；checks_v11/fmt_audit.py）
manuscript: Heading 样式 0（164 段全 Normal）；176/176 run 12 pt Times New Roman、自动色；行号有；非空 161 段 line=480（新段落继承）；粗体 26 run（与 v11 相同: 题名、大标题、抄录标签、Statements 标签、图注标签）；句中粗体 0。ESM: 2,551/2,551 run 12 pt Times New Roman、自动色（未变）。需要的机械修正: 0。表的版式未动。

### 6.6 图
Fig1.tif 4,015 × 2,173 px、600 × 600 dpi（170.0 × 92.0 mm）；Fig2.tif 4,015 × 2,456 px、600 dpi（170.0 × 104.0 mm）；Fig3.tif 4,015 × 3,023 px、600 dpi（170.0 × 128.0 mm）。RGBA、LZW。与 v11 逐字节相同。

### 6.7 ESM_1_v12.pdf
Word（SaveAs2, 17）导出，46 页（与 v11 同）。与 ESM_1_v11.pdf 逐页比较文字: 第 1〜5、10〜46 页相同；第 6〜9 页只因 Table S1 的 Location 文字与其换行而变；第 6〜9 页看过图像。第 8 页末的第 28 项一行跨页: 其 Guidance 列的最后一词 "requirements." 落到第 9 页顶，第 9 页另有脚注 a（v11 第 9 页只有脚注 a）。版式按指示未动。

### 6.8 第 10 节计数（只报告）
扫描抄录 5 段 + 正文 40 段（不含标题）: 禁用语 0、开场套话 0、接续词连发 0、因果词 0、破折号 — 0、中黒「・」0。超过 30 词的句子 43（v11 43），最长 76 词（Outcomes 第 2 段，v10 既有）。超过 150 词的段落 2（v11 3；Exercise effect and costs 第 1 段因 1c 分段而消失；余下 2 段为 Discussion 段落，v10 既有）。裸时间词 3（currently、now、current，均 v10 既有）。
check_acronyms（ARS 3.24.0，本文与抄录分别）: 抄录 "No findings"，但 coverage partial、Not checked JPY 与 QALY（"Japanese yen" 的首字母拼不出 JPY）——v11 报的抄录 JPY 未定义已由 1a 解决；正文 partial，Not checked JPY、TNBC、QALY、ICER，Not defined PMC（Europe PMC）、CHEERS、EQ（与 v11 相同）。

## 7. 第 3 步: 公开用代码（停）

### 7.1 已做
- 作业树新建 R/py/26_public_params.py（用法见脚本头）。从 input/params/parameters_v10.xlsx（sha256 5e939653…）生成 C:\Users\原明美\Documents\ClaudeCode\exercise_cea_public\input\params\parameters_v10.xlsx（198f01e7…）:
  - (a) 只留「パラメータ」「シナリオ」。
  - (b) 列与顺序不变；出典 = ESM_1_v12 Table S2 B 部分同 Code 行的 Source（81/81 行都有对应 Code，B 部分 81 行无重复、无多余）；出典の該当箇所与担当清空；備考只留判定幅的标记（薬価固定 4、0例：PSAは固定 4、±25% 7〔写作 "幅の規則：±25%"〕、片側対称 9、无 57；无一行带多个标记），逐行断言公开版 rule_of 与内部表一致。
  - (c) シナリオ的根拠: sc_metcost50 = "Metastatic treatment costs halved: monthly costs of first-line and later-line treatment of distant recurrence multiplied by 0.5 (Table 1)."；sc_eribulin = "Eribulin-based later-line treatment: 245,683 per month for second-line and later treatment (EMBRACE dosing; national drug price list [8,68]; Table 1)."（取自 tables_v12 Table 1 两行，脚本断言原文）。
  - (d) 属性: creator、lastModifiedBy、title、company 均为空（docProps 只剩 created/modified 与 openpyxl 的 Application）；批注 0、隐藏表 0、定义名称只剩自动筛选的 _xlnm._FilterDatabase（指向「パラメータ」）。
- 公开目录的文件（114 个，6.5 MB；清单与 sha256 前 16 位见 checks_v12/out/public_files.txt）: R/ 10 个（config.R、lifetable.R、00_lifetable.R、guyot.R、03_reconstruct_ipd.R、survmodels.R、engine.R、econ.R、10_read_params.R、22_phase2b_main.R）；input/lifetable/ 4；input/params/parameters_v10.xlsx；data/digitized/ 66；data/ipd/ 28（含 esme/ 3）；data/fits/ 3（engine_params.rds、dr_k_external.rds、fits.rds = 22 主脚本实际读取的三件）；data/bootstrap/boot_replicates.rds（1,000 次概率分析读取）；renv.lock。未放 README、LICENSE；未 git init。
- 公开版代码: 9 个脚本只改根目录一行（Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/…") → Sys.getenv("EXERCISE_CEA_ROOT", ".")；engine.R、econ.R、survmodels.R、guyot.R、lifetable.R 无此行，内容不变）。10_read_params.R 去掉尾崎回表核对（ozaki/ 与两件模板）、記入元列与 params_check.md 报告，并把 RANGE_NOTE 的 ±25% 标记改为 "幅の規則：±25%"；分布计算部分与原文件逐字相同（diff 确认）。

### 7.2 去名检查（checks_v12/public_name_scan.py；xlsx 的 XML 成员与单元格、属性；rds 内全部字符串〔checks_v12/rds_strings.R〕；pdf 的元数据、XMP 与全文；png/jpeg 的元数据块；文本文件全文。植入测试: csv、xlsx、rds 各一，全部词命中）
扫描 114 个文件。人名命中 7 处 → 按指示停下，未自行删改:
| 文件 | 命中 | 内容 |
|---|---|---|
| input/params/parameters_v10.xlsx | 尾崎 2、原 2 | 「パラメータ」M2:M82（担当列）的数据验证: 列表 "尾崎,原" 与错误提示 "尾崎 または 原 を選んでください"（单元格与属性中 0） |
| R/engine.R 第 322 行 | Ozaki 1 | 注释 "S-JP subgroups of the non-pCR branch (Dr Ozaki, 2026-10-23)" |
| R/22_phase2b_main.R 第 450、453 行 | hara 2 | plan10 的路径 data/params_hara/utility_scenarios.csv（文件不在公开目录；plan10 不在本次复现范围） |
非人名: "hara" 在 character 中（R 代码 4、renv.lock 8）；"@" 425 处全在 renv.lock（CRAN 包的 Maintainer、Author、Authors@R 字段与联系邮箱，包元数据）。原明美、Akemi、立花、押、先生: 0。作为普通词的「原」: 0。akehara1001: 0（README 未写）。

### 7.3 一致性（诊断，在 scratchpad 的副本中运行，公开目录未写入任何输出）
- 00_lifetable.R → data/lifetable_female_2025.csv 与作业树逐字节相同。
- 10_read_params.R → data/params_dist.csv 与作业树逐字节相同（全部列，含 dist、base、lower、upper、p1、p2、note、range_rule）。
- 22_phase2b_main.R det: 失败。det_caps.csv 与 det_reference.csv 的 dQ 全部 NA（72 + 2 行；dC 与作业树完全相同，最大差 0），随后 crossings 的 uniroot 报错停止（"missing value where TRUE/FALSE needed"）。原因: 22 主脚本从 data/params_long.csv 的 備考 读两样东西，按 (b) 去掉后读不到:
  1. U05 的 "期間 12.5 週"（第 35 行 u05_weeks → PV0 的 U05_duration_years；econ.R 第 132、134 行把它乘进全部有害事象的 QALY 损失）→ NA，所有 dQ 为 NA。
  2. U01〜U05 的 "米国 …、英国 …、豪州 …"（第 102〜110 行 util_set()，情景 utility_us/uk/au）→ stopifnot 失败。
  另 第 41 行 PROVISIONAL 读 "【要確認"，只影响 oneway 输出的 provisional 标签列。
- 选项 A 的诊断（不是交付物）: 在另一副本中只给 U01〜U05 的 備考 补回上述片段（U01〜U04 "シナリオ：米国 x、英国 y、豪州 z。"，U05 再加 "期間 12.5 週。"；值用 22 主脚本相同的正则从内部表取出）。结果: params_dist.csv 仍逐字节相同；det（1.5 分）与 plan9_det（0.5 分）正常完成，plan9_det 内置的 sc_base 复现检查通过；输出 20 个 csv 与作业树逐列比较，数值最大差 0（checks_v12/compare_optionA.txt）；HR 0.85 主比较 2,726.4、次比较 3,442.9、ICER 2,052.8（千日元）= 作业树；两个情景（sc_metcost50、sc_eribulin）的 det_caps、det_reference、crossings 全部一致。唯一的文字差: oneway_base.csv 与 oneway_sjp.csv 的 provisional 列 9 + 1 行由 TRUE 变 FALSE。
- 未做: README、LICENSE、git init 与 commit（停在去名检查）；完整的 1,000 次概率分析（指示不要求）。

### 7.4 另记（只报告）
- data/digitized/ 含 3 个已发表图的截取图像（K22_S3_DRFS_native.png、K22_S4_EFS_pCR_native.png、K24_S4_OS_pCR_native.jpeg）。
- 03_reconstruct_ipd.R 还读 data/reported_values.csv 与 input/user_supplied_values.csv，二者不在放入清单，公开目录中该脚本不能完整运行（22 主脚本不需要它）。
- 公开目录运行需先跑 00_lifetable.R 生成 data/lifetable_female_2025.csv（config.R 通过 lifetable.R 读取它），README 需写明顺序。

## 8. 著者侧与用户待定的事项

1. 第 3 步的去名命中 3 处（第 7.2 节）与 備考 规则 (b) 与复现的冲突（第 7.3 节）。
2. ESM 第 9 页顶部只有第 28 项的一词 "requirements." 与脚注 a（第 6.7 节）。
3. 文献 28 的写法 "Fasching PA" 与 Crossref、PubMed、出版社元数据的 "A. Fasching" 不同（按指示；实名 Peter A. Fasching）。
4. 正文中 JPY 展开两次（Introduction 第 1 段既有、Study design 第 2 段因 1b）。
5. check_acronyms partial（第 6.8 节）；超过 150 词的段落 2、超过 30 词的句子 43、裸时间词 3（均既有）。
6. 目的对应（v11 第 7 节第 8 项）照旧: Statistical analysis 的 (1) 与 (6) 不对应单一目的编号；Discussion 第 1 段只直接回答目的 1 与 3。

## 9. 撤回的主张

本版无撤回。退行对照中没有任何此前删除的内容复活。

## 10. 共著者コメント台帳

本版无共著者交回的文件（底本为 CC 交付的 v11）。采否即用户指示 v12 的第 1〜3 步。

## 11. 过去意外退回的地方

规约第 1.2 节第 7 条名指的五处本版逐一确认，无退回（第 6.4 节）。本项目未记录过其他退回位置。

## 12. 文献检索的记录

沿用 v11 第 11 节（ESM Supplementary Methods S1 "Literature searches"，2026-10-26，PubMed 与 Europe PMC，2000〜2026）。本版未改新规性句。

## AUDIT（规约第 13 节；交付前再读规约全文后逐项一行）

最重要四项（先报告）:
1. 版: 通过。底本 = v11（2026-10-28 交付；9 个文件 sha256 与 MANIFEST_v11 一致）；交付后 manuscript/ 下只有 v12（v11 → archive/v11）。
2. 表与图: 通过。四系列全部在正文地の文以编号引用（56 段、43 个提及）；Supplementary Methods S1 与 CHEERS 清单（Table S1）由正文引用。
3. 文献的真伪: 通过。DOI 61/61 解析，作者与年 0 不符（卷页的 2 个标记为检查器假阳性，第 6.1 节）；无 DOI 17 条中 16 条网址 200、1 条图书已确认；1d 的 4 条打开确认。
4. 文献的顺序: 通过。正文 1〜71 初出顺无缺（110 个号）；72〜78 只在 tables 与 ESM（偏离 4）。

版
- [x] 作业树只有最新版: manuscript/ 下 v12、code、archive、_inbox（空）。archive 在项目根内（项目惯例，用户指定）。
- [x] 会话开始时 sha256 与 MANIFEST_v11 一致（9/9）。
- [x] 底本 = v11，worklog 开头写了底本与 sha256。
- [x] 意外退回 0（五处名指，第 6.4 节）。
- [x] 数值与 v11 一致（Word count 除外；第 4 节）。
- [—] 模板占位: 题名页、Statements 与 cover letter 中的占位是尾崎的（第 14 节），不动、不报告。
- [x] 版本标签 0（manuscript 161 段、ESM 2,366、tables 287、cover letter 14 段扫描）。
- [x] MANIFEST_v12 写好、v11 移入 archive（交付时）。
- [x] 解析输出 57 个 sha256 不变（本版不改数值）。
- [x] 差分全部对应指示（manuscript 8 块、ESM 5 块、tables 0）。
- [x] 撤回主张复活 0。
- [x] 修订与批注 0（Word COM 读 manuscript 与 ESM）。
- [x] 作业树无 ars/。

文献与编号
- [x] 初出顺 1〜71 无缺；未引用 0、表外号 0。
- [x] DOI 61/61 解析；书目不符 0（第 6.1 节）。
- [—] 新引用: 无。
- [—] ARS citation-check: 本版未增未移文献，未跑（第 6.1 节）。
- [x] 作者名-年份式的正文引用 0。
- [x] 超过 10 年 8 条、自引 0（v11 报告，文献未增减）。
- [x] 新规性句未改（与检索记录一致）。
- [x] 四系列初出顺 1..n。
- [x] 各系列最大号 = 实物数。
- [x] 每个表与图在正文地の文至少一次。
- [x] ESM 内顺序为编号顺。
- [x] Supplementary Methods S1 与报告规范清单由正文引用。
- [x] Fig1〜3.tif 已附，Fig. 1 起依次在正文提及。

标题与格式
- [偏离] 大标题: BCRT 结构（第 2 节偏离 1）。
- [x] 规约外的节与项目: v11 与 v12 相同（Abstract/Keywords、Conclusion、Acknowledgments、References、Statements and Declarations 7 项、Figure captions），未增未减。
- [偏离] Methods 小标题 5 个（偏离 1）。
- [x] Heading 样式 0。
- [x] 全部 run 12 pt Times New Roman（manuscript 176/176、ESM 2,551/2,551、tables 未变 349/349）。
- [x] 行号有。
- [x] 双倍行距（非空 161 段）。
- [x] 句中粗体 0。
- [x] 表的列头与数值无粗体（tables 未变）。
- [x] 非黑字 0。
- [x] 中黒「・」0。
- [x] 表页为横版（未变）。
- [偏离] 表脚注记号 a〜d；"Note" 开头 0。
- [x] 脚注记号与表内上标一一对应（tables 未变，v11 已核）。
- [x] 图 600 dpi（第 6.6 节）。
- [x] 前付一项一段（尾崎，未动）。
- [x] 生成 AI 记述 0（四件 docx 扫描）。
- [x] ARS 作业标记 0（同上）。
- [x] ARS 默认来源的结构 0（Conclusion 为既有，规则 10）。
- [x] 美式拼写、"Fig." 统一（未变）。
- [x] 语数实测、写入题名页、在上限内（250 ≤ 250；3,244 ≤ 3,500）。

数值
- [x] 无新增结果数值；来源台帐 57 文件未变。
- [x] 表脚注数值未变（tables 逐字节相同）。
- [x] 同一数值两表重复: 未改动（v11 记的有意例外照旧）。
- [—] n 的合计、流程图: 模型研究，不适用。
- [—] 对象者数: 不适用。
- [x] 点估计在 UI 内（未改动）。
- [x] 同一统计量各处同值（未改动）。
- [—] p 值: 无。
- [x] 因果词 0（sec10）。
- [x] 负号与千位逗号（未改动；新文无负数）。
- [x] 小数位与舍入（未改动）。

内容
- [x] Methods 无数值结果（1b、1c 未加结果）。
- [x] Results 无"使用了"型（未改动）。
- [x] 结果句有表或图的参照（未改动）。
- [x] 各解析的目的句（未改动）。
- [x] Introduction 末两段的形（未改动）。
- [注] 目的对应表: 照 v11 第 7 节第 8 项（第 8 节第 6 项）。
- [x] 曝露与结局名称（未改动）；1c 分段后 Exercise effect and costs 第 1 段 = 曝露与持续时间，第 2 段 = pCR 途径与有害事象。
- [x] 抄录的目的与结论（1a 只改方法句的写法与 JPY 的展开）。
- [x] Results 段落顺序与开头名指（未改动）。
- [x] Discussion 段首名指（未改动）。
- [注] Discussion 第 1 段只直接回答目的 1 与 3（既有）。
- [x] Discussion 与 Results 的重复（未改动）。
- [x] Discussion 引用集中在中段（未改动）。
- [x] "further research is needed" 型 0。
- [x] 临床医会改变什么（未改动）。
- [x] Implications 未改动。
- [注] check_acronyms partial（第 6.8 节）；抄录 JPY 已展开。
- [x] 限界只在 Limitations（未改动）。
- [x] Outcome/Variables 第一句（未改动）。
- [x] 统计软件只写语言与版本（未改动）。
- [注] Data availability 与公开仓库的一致: 公开目录的内容（R 代码、入力表、重建的患者级数据）与 1l 的文字对应，但第 3 步停在去名检查，仓库尚未建立。
- [x] CHEERS 清单 28 项中 24 项有节、段与页（19、21、22、25 按指示不加），页码按 v12 实测。
- [x] 题名 manuscript 与 ESM 一致（未改动）。
- [x] 事前计划、缺失、多重比较（未改动）。
- [—] 选择流程图: 不适用。
- [x] 图未改动（逐字节复制）。
- [x] 图表重复（未改动）。
- [—] 著者贡献: 尾崎的占位（第 14 节）。
- [x] AI 常套语 0；破折号 0；30 词超句 43、最长 76；150 词超段 2（报告）。
- [注] 裸时间词 3 处（既有）。
- [x] 主张未变强（1a、1b 为写法与略语展开，1c 为分段，1d 为书目）。
- [—] 查读回复版: 不适用。
- [—] humanizer / stop-slop: 本版未用。
