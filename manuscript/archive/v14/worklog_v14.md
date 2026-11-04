# worklog v14（2026-11-04）

## 1. 底本

底本: manuscript_v13_BCRT.docx（v13，2026-10-29 交付，sha256 前 8 位 4178320b）。同批: tables_v13_BCRT.docx（d022962f）、ESM_1_v13.docx（ae84d2f6）、ESM_1_v13.pdf（5e1aeac6）、Fig1〜3.tif（c13b748e、662046bf、d7926e1e）、cover_letter_v13_BCRT.docx（21ed7f1a）、worklog_v13.md（bf8d88c5）。会话开始时 9 个文件的 sha256 全部与 MANIFEST_v13.md 一致；作业树 git 状态干净（HEAD 11d484b，计划第 11 节的计算提交）；manuscript/ 下只有 v13（另有 archive、code、空的 _inbox）。
本版是共著者指示的结构改稿（尾崎 2026-11-04 邮件；计算见 11d484b）：Results 改为「四组 → 运动对帕博利珠单抗 → 上乗せ」。按指示不跑 ARS 起草、humanizer、stop-slop；英文段落按指示原样插入（唯一的补字见第 5.4 节 (a)）。
编辑方法: v13 的 docx 直接编辑，脚本 manuscript/code/edit_manuscript_v14.py、edit_tables_v14.py、edit_esm_v14.py（lxml 只改 word/document.xml，其余部件逐字节照搬；每处原文须在 v13 中唯一命中，否则停止）。Fig1〜3.tif 与 cover letter 为 v13 的逐字节复制（cmp 确认）。三个 docx 由 Word（COM）打开确认: 修订 0、批注 0；manuscript 30 页、tables 9 页、ESM 48 页（v13: 28、7、46）。ESM_1_v14.pdf 由 Word SaveAs2(17) 导出。

## 2. 投稿先与投稿规格（沿用 v13 第 2 节）

- 投稿先 BCRT；抄录结构式，上限 250 词；正文上限 3,500 词；Springer 数字式文献；美式拼写；"Fig."。
- 语数计法（同 v11〜v13）: Word ComputeStatistics（逐段），抄录 = 四个结构段去掉 4 个标签；正文 = Introduction 至 Conclusion，不含标题（checks_v14/word_wc14.py = checks_v11/word_wc.py 换成 v14 的 17 个标题）。
  - v14: 抄录 248（含标签 252）；正文 3,745（含 17 个标题 3,786）。各节（不含标题）: Introduction 570、Methods 1,402、Results 790、Discussion 571、Implications 176、Limitations 199、Conclusion 37。→ 题名页 Word count 行改为 "abstract 248; main text 3,745"（1h）。"3 tables; 3 figures; 1 Online Resource" 仍成立（Table 1〜3、Fig1〜3.tif、ESM 一份）。
  - **正文 3,745 超过 BCRT 上限 3,500（超 245 词）。** 增加全部来自指示原文的段落（v13 3,242 → +503）。按规约第 1.4 节 CC 不自行删减，待用户决定（第 7 节第 1 项）。
  - 抄录（1g）: 插入指示原文后 261 词 > 250，按指示顺序删减并逐步用 Word 实测: ① 后 258、② 后 256、③ 后 251、④ 后 248 → 用到第 ④ 条（全部 4 条）。
- 投稿先与共著者决定的偏离（v11 第 2 节，本版照旧）: 1. 标题结构（Methods 5 个小标题、Results 二级标题、二级标题斜体）；2. 表脚注记号 a〜d；3. 题名页在 manuscript 内、表另成 tables 文件、图为 tif；4. 文献 72〜78 只在 Table 1 与 ESM，不重排。

## 3. 用语表（v13 沿用，本版新增）

| 本文的名字 | 指什么 | 初出 |
|---|---|---|
| the four strategies / the four arms | 化疗 ± 帕博利珠单抗 × ± 运动的四组（指示原文两者并用: Introduction 与 Results 用 strategies，Methods 用 arms） | Introduction 第 4 段 |
| chemotherapy alone / chemotherapy plus exercise / chemotherapy plus pembrolizumab / chemotherapy plus pembrolizumab plus exercise | 四组的名字（Table 2 的 Strategy 列） | Results 第 1 节；Table 2 |
| chemotherapy with both | 两者都加的组（Results 第 1 节末句、Discussion 第 1 段，指示原文） | Results 第 1 节 |
| dominated / extendedly dominated | 强支配 / 扩展支配 | Statistical analysis (2)；Table 2 脚注 a（只定义 dominated） |
| net monetary benefit | QALY 增量 × 阈值 − 增量费用 | Outcomes 第 2 段 |
| incremental cost-effectiveness ratio (ICER) | 增量费用 ÷ 增量 QALY | Outcomes 第 2 段（v13 同段；本版在该段第一次使用处定义） |

## 4. 数值台帳

本版的新数值只来自 output/phase2/fourarm_report.md 与 main/fourarm_totals.csv、fourarm_incremental.csv、fourarm_nmb_equal.csv（11d484b），其余为 v13 的表与 ESM 中已有的值。来源文件: v13 MANIFEST 的 57 个文件 sha256 重算，只有 docs/analysis_plan_phase2.md 变更（计划第 11 节与追记，744048c、11d484b），其余 56 个一致（checks_v14/out/src_sha_v14.txt）；新增来源 fourarm_* 8 个与 R/25_four_arm.R、R/test_four_arm.R（MANIFEST_v14）。

| 位置 | 数值 | 出处 |
|---|---|---|
| Table 2 A 全部格（3 个 HR × 4 组 = 12 行） | 12,112 … 11,368 | fourarm_incremental.csv（programme E02）与 fourarm_totals.csv（dnmb_500_vs_chemo），half up；= fourarm_report.md 表 A。edit_tables_v14.py 由 csv 现算后逐格断言等于指示的字符串 |
| Table 2 B | 4,426 [−330, 8,901]；2.156 [0.245, 4.228]；2,053；83.1；90.8 | det_reference.csv（base）与 psa_reference_summary.csv（base）；= v13 Table 3 基准列（= v14 Table S4 基准列） |
| Table 2 B | 0.425、35.9 | det_yardstick.csv；= v13 Table 3 C |
| Table 2 B | 0.722、19.0；0.638、24.1 | fourarm_nmb_equal.csv（λ 500 万、750 万；hr0 轴与 pCR 轴）；= fourarm_report.md 表 B |
| Table 2 脚注 | 192,400、239,508、11,260、0.72、5 年 | Table 1（E02、E01、E03、CHALLENGE、效应持续）；脚注 c 的 status = fourarm_incremental.csv（E01: hr0 0.95 扩展支配、0.85 与 0.72 强支配；E03 同 E02） |
| Results 第 1 节 | 2,112、2,245、2,449；931、3,250、6,413、6,355 | Table 2 A |
| Results 第 2 节 | 4,426、−330、8,901、2.156、0.245、4.228、2,053、83.1%、90.8%；0.425、35.9；0.722、19.0、0.638、24.1 | Table 2 B |
| Results 第 2 节 | 6,531、−1,911 | Table S4 A（原 Table 3） |
| Sensitivity 段新句 | 3,044、2,565、2,785、1,920 | Table S4 B（原 Table 3） |
| 抄录 Results | 2,053、0.425、0.722 | Table 2 B |
| 抄录 Results | 2,726 [2,223, 3,040]、0.989、0.958〜0.914 | Table 3（原 Table 2） |
| 抄录 Results | 192,400 | Table 1 |
| Discussion 第 2 段 | 28%；more than a third | 28% = 100 × (1 − 0.72)（CHALLENGE 的 HR 0.72，Table 1、Introduction 第 2 段）；"a third" 对应 0.638（36.2% 降低，Table 2 B）。指示原文 |
| Discussion 第 3 段 | 1.1% | Table 3 "0.989 (1.1)"（v13 Discussion 第 1 段已有） |

机械核对（checks_v14/numcheck14.py → out/numcheck14.txt）: 新文字（编辑日志的新段）、新 Table 2 与脚注、S4 题名中的数字 245 个，逐个在 fourarm_report.md、v13 tables、v13 ESM、v13 manuscript 中查找（引用号除外；负号统一）: 未找到 0。
v13 原有数字（checks_v14/regress14.py）: 未变动的段落与单元格中的数字照旧。全文数字记号只在 v13 中的: manuscript 250、3,242（语数）、"2"（表号与阶段号的改号）、3,443（抄录旧 Results 句 "Added to chemotherapy alone, it was JPY 3,443 thousand"，按 1g 换掉；正文 Results 中 3,443 仍在）；tables 中原 Table 3 的值（移到 ESM S4，值不变）；ESM 中 26（页码）、2（表号）、7、9、13（页码与阶段号）。

## 5. 本版变更的段落（由生成后的 docx 读回；checks_v14/regress14.py 用编辑日志判定每个变动单元对应哪一条；输出 checks_v14/out/r14_*.txt）

### 5.1 manuscript（164 段 → 168 段；未变 138；变动块 14；不能解释的 0）
| 块 | 位置 | 指示 |
|---|---|---|
| M1 | 题名页 Word count 行 | 1h |
| M2 | 抄录 Methods 句（删 ", with alternative durations"）、抄录 Results 全换 | 1g（删减 ①〜④） |
| M3 | Introduction 第 4 段 | 1a |
| M4 | Study design 第 3 段 "Tables S1–S10" → "Tables S1–S11" | 1f |
| M5 | Outcomes 第 2 段 | 1b |
| M6 | Statistical analysis 原 (2) → 新 (2)、(3)；原 (3)〜(6) → (4)〜(7)（只改号） | 1c |
| M7 | Results 新节 Four strategies compared、Exercise compared with pembrolizumab（标题 + 各 1 段） | 1d |
| M8 | Maximum affordable cost 3 段: Table 2 → 3、S4 → S5、S5 → S6、S6 → S7 | 1f |
| M9 | Duration 3 段: Table 2 → 3、S7 → S8、S8 → S9；原 Pembrolizumab 节（标题 + 2 段）删除 | 1f、1d |
| M10 | Sensitivity 段: S9 → S10、S10 → S11，末尾追加 1 句 | 1f、1d |
| M11 | Discussion 原第 1 段 → 3 段 | 1e |
| M12 | Discussion 原第 4 段 → 新段 | 1e |
| M13 | Implications: S8 → S9、S7 → S8 | 1f |
| M14 | 图注 Fig. 2（S4 → S5）、Fig. 3（S9 → S10） | 1f |
1f 的机械替换共 17 处（out/m14_log.json）。Results、Discussion、Implications、Limitations、Conclusion 的其余段落一字不动（"Maximum affordable cost of exercise"、"Duration and metastatic treatment costs" 两节只改表号）。

### 5.2 tables（单元 289 → 309；未变 169；变动块 3；不能解释的 0）
- 2a 新 Table 2（题、表 27 行、脚注 a〜d、节分隔）插在 Table 1 的节之后。版式照 v13 的表: Table Grid、等宽 8 列（1,821 twip）、列头不加粗、面板行合并且粗体（上标记号不加粗）、HR 分组行合并不加粗、横版节。面板 B 在 8 列的格子中用合并单元格: 标签 4 列 + 值 4 列；"Exercise effect needed to match pembrolizumab" 的子表头与 3 行为 标签 4 列 + HR 2 列 + pCR 2 列。
- 2b 原 Table 2 → Table 3: 题号；脚注 d "Table S4 (Online Resource 1)" → "Table S5 (Online Resource 1)"。内容与版式不动。
- 2c 原 Table 3 及其前的节分隔删除（移入 ESM）。
- 2d Table 1 脚注 c "Table S10 (Online Resource 1)" → "Table S11 (Online Resource 1)"。

### 5.3 ESM（单元 2,404 → 2,507；未变 2,376；变动块 23；不能解释的 0）
- 3a Table S3 的节之后插入原 Table 3 为 Supplementary Table S4（题按指示；面板 C 的 3 行与脚注 d 删除；面板 A、B 与脚注 a〜c 原样；脚注 a〜c 中没有提到 exercise effect 的句子，不需删）。横版节（复制 S3 的节属性）。
- 3b 改号 20 处: 题 S4〜S10 → S5〜S11（7）；S7（新）脚注 b "(Table 2)" → "(Table 3)"；S8（新）脚注 "Supplementary Table S4" → S5；S10（新）脚注 "base case in Table 2" → Table 3、"base case in Table 3" → "Supplementary Table S4"；Fig. S2 图注 "(Table 3)" → "(Supplementary Table S4)"、"Supplementary Table S9" → S10；S11（新）表格 "Same as base case (Table 2)" 6 格 → Table 3、"Table 3" 1 格 → "Supplementary Table S4"；S11 脚注 a "Tables 2 and 3" → "Table 3 and Supplementary Table S4"、脚注 c "base-case values in Table 2" → Table 3。原 Table 3 在 ESM 中写成 "Supplementary Table S4"（ESM 引用自身补充表的写法）。目录: 无。
- 3c Table S1（CHEERS）Location: 先用 v13 的分页（checks_v13/out/m13_stats.json）重建 v13 的 28 格，与 ESM_1_v13 逐格一致后，按 v14 的分页（checks_v14/out/m14_stats.json，Word Range.Information(3)）写 v14。变化 8 格: 16（页 4〜28）、17（stages (1) to (3)，页 6〜8）、20（stages (4) to (6)，页 8〜9）、23（Results 两个新节各 paragraph 1 + 原两节；"Tables 2 and 3; Supplementary Tables S4 to S9"；页 9〜11）、24（"Table 3; Supplementary Tables S5, S8, S10 and S11"；页 11〜12）、26（Discussion paragraphs 1 to 8；页 12〜15）、27、28（p. 27）。第 19、21、22、25 项按 v12 规则不加页码。页码独立核对（checks_v12/pdf_pages.py，Word 导出的 manuscript PDF）: 定位 144 段、页码不符 0；未定位 10 段（抄录 Purpose 段、文献 7 条、Fig. 3 图注，段尾未定位，与 v13 同类，都不是 Location 引用的段落）。
- 3d ESM_1_v14.pdf: Word SaveAs2(17)，48 页。

### 5.4 CC 的判断（指示未写明、需要用户知道的处理）
- (a) 1b: Outcomes 第 2 段在 v13 中是 ICER 的首次定义，指示原文的第一次使用是 "the ICERs between them"（未定义）。按指示「保留首次定义的位置」，在该段第一次使用处写成 "the incremental cost-effectiveness ratios (ICERs) between them"；其后的 "the ICER of pembrolizumab" 不变。这是对指示英文的唯一补字。ICER 在此段之前（Introduction、Study design）未出现。
- (b) Table 2 面板 A 的三个分组行写成 "HR 0.95"、"HR 0.85"、"HR 0.72"（指示的分组写法 "HR 0.95：…"；HR 在面板题与脚注 a、b 中定义）。
- (c) Table 2 面板 B 第 5 行的标签写成 "Probability cost-effective at JPY 7.5 million per QALY, %"（指示写 "；at JPY 7.5 million per QALY, %"，按前一行的省略写法理解；与 v13 Table 3 的行名相同）。
- (d) CHEERS 第 17 项: v13 的 "stages (1) and (2)" 中原 (2) 被新 (2)、(3) 取代，写成 "stages (1) to (3)"；第 20 项 "(3) to (5)" 按改号写成 "(4) to (6)"。第 23、24 项的表号按 1f 的映射机械替换（第 24 项未加 S4）。
- (e) 公开代码（第 6 节）: README 的「Tables and figures」表与两处 S8 也按 1f 改号；cohort_N_jbcs2024.csv 的 source 列 4 处 S8 → S9；公开版 25 的 git_out() 在没有 .git 时返回 NA。

## 6. 第 4 步: 公开代码（exercise_cea_public，作业树外；本地 commit 4a883ed，无远程、未推送）

- 新增 R/25_four_arm.R、R/test_four_arm.R（作业树 11d484b 的版本）。与作业树的差: ① 根目录缺省 "C:/Users/…/exercise_cea" → "."（两个文件各 1 行，同公开版 22）；② 报告字符串 "（尾崎 2026-11-04 邮件）" → "（2026-11-04）"；③ git_out(): 公开目录副本不是 git 仓库时 git 以非零状态结束、返回空向量，原版在写运行信息时 data.frame 行数不一致而停止 → 公开版改为返回 NA（3 行）。作业树的 25 已与结果一并提交，不改。
- README.md: 「How to run」加第 4 步（25 与 test_four_arm 的用途、前提 det、输出）；「Tables and figures of the paper」: 首句加 R/25_four_arm.R，新 Table 2 行（fourarm_*.csv、det_reference.csv、det_yardstick.csv、psa_reference_summary.csv），原 Table 2 行 → Table 3，原 Table 3 行 → Supplementary Table S4（det_yardstick.csv 移到 Table 2 行）；plan9_cohort 与「Input sheet」的 Supplementary Table S8 → S9。
- input/params/cohort_N_jbcs2024.csv: source 列 4 行 "Supplementary Table S8 of Online Resource 1" → S9（plan9_cohort 只读 item 与 value，计算不受影响；CRLF 保持）。
- 未改（报告）: R/22_phase2b_main.R 第 112 行注释 "Table 2 of the manuscript"（现为 Table 3；作业树版同样，代码注释）。
- 去名检查（checks_v13/public_name_scan.py，植入测试 4 类全部命中）: 108 个文件；尾崎、Ozaki、原明美、Akemi、立花、押、先生、「原」0；Hara 16（全部是 "character" 的一部分；新增 4 处在 25）；@ 425（全部 renv.lock，同 v13）。绝对路径与 akehara1001: 0 个文件。清单与 sha256: checks_v14/out/public_files14.txt。
- 提交: 作者 "the authors"、邮箱空（同 v13）；-c core.autocrlf=false，4 个改动文件的 blob 与文件字节一致。
- 复现（scratchpad 的公开目录副本；公开目录未写入任何输出；R_LIBS = 作业树 renv 库；日志 checks_v14/out/pub_logs/）: 00_lifetable.R、10_read_params.R（输出与作业树逐字节相同）→ 22 det（1.1 分）→ 25（0.1 分，内置核对 10/10）→ test_four_arm.R（12/12）。Rscript 退出码 127 为本机已知现象，判定按 "Execution halted" 0。fourarm_* 5 个 csv 与作业树逐列比较: 数值差 0、文字差 0；det_caps.csv、det_reference.csv、det_yardstick.csv 逐字节相同（checks_v14/out/compare_pub14.txt）。**复现的三个值: 2,245（hr0 0.85，两者都加对化疗加运动的 ICER，千日元/QALY）、0.722（λ 500 万）、0.638（λ 750 万）。**

## 7. 著者侧与用户待定的事项

1. **正文 3,745 词，超过 BCRT 上限 3,500（第 2 节）。** 抄录 248 在上限内。
2. **文献第 8 条**（厚生劳动省药价表，tp20261014-01_02.xlsx）: 网址现在返回 HTTP 404（v13 核对时 200）。**文献第 71 条**（Garber 2026，Ann Oncol）: 文献表写 "(in press)"，Crossref 现在有卷 37、页 1467–1479。两者都是 v13 交付后的外部变化；指示为「文献只核对、不修改」，本版未改。
3. Table 2 中 "—" 的意义没有脚注说明（规约第 6.2 节；脚注 a 为指示原文，"Increments are against the strategy in the comparator column" 隐含费用最低组无对照）。
4. Table S4 脚注 a 的略语表仍有 HR、pCR，但删去面板 C 后表中已不出现（指示: 脚注 a〜c 原样）。
5. 同一数值在两个表: Table 2 B 的 4,426 [−330, 8,901]、2.156 [0.245, 4.228]、2,053、83.1、90.8 与 Table S4 的基准列相同（指示的表设计）。
6. 指示原文带来的计数: 超过 150 词的段落 3（新增 Results 第 2 节 170 词）、超过 30 词的句子 47（v13 43），最长 121 词（新 Outcomes 第 2 段）；裸时间词 now（Discussion 第 3 段，v13 第 4 段的 now 移来）。
7. 目的与不足的对应: Introduction 第 3 段（不足）未改，新的目的（四组比较、与帕博利珠单抗相同所需的效应、主要目的）中前两项在第 3 段没有对应的不足项；Discussion 第 1 段只回答四组比较（目的 2、3 在第 2、3 段）。均为指示的结构，只报告。
8. v13 第 8 节第 1〜6 项照旧（公开仓库提交作者、plan9_cohort 输入、图像数、ESM 页面、文献 28 的写法、check_acronyms partial）。

## 8. 撤回的主张

- v12 的 1b（Study design 第 2 段的 "5 million Japanese yen (JPY)"）仍为撤回: v14 中该写法只在抄录 Methods 段（允许），正文 Study design 第 2 段为 "JPY 5 million"。
- 本版按指示替换或删除的文字（以后不应复活）: 原 Results "Pembrolizumab" 节（标题 + 2 段，内容并入新 Results 第 2 节与 Sensitivity 段）；原 Discussion 第 1 段与第 4 段；原抄录 Results（含 "Added to chemotherapy alone, it was JPY 3,443 thousand"）；抄录 Methods 的 ", with alternative durations"；原 Table 3 面板 C 与脚注 d（移到 Table 2 B 与脚注 d）。

## 9. 共著者コメント台帳

本版无共著者交回的文件。采否 = 用户转达的尾崎 2026-11-04 邮件（v14 指示第 1〜6 步）。

## 10. 过去意外退回的地方

规约第 1.2 节第 7 条名指的五处逐一确认，无退回: 题名（manuscript、ESM 与 v13 相同）；责任著者占位行（题名页 1〜4 行与 Statements 与 v13 相同，尾崎的占位，未动）；补充表脚注（ESM 中只有改号的 6 处与新 S4，其余逐字相同）；语数（按 1h 实测）；图解像度（Fig1 4,015 × 2,173、Fig2 4,015 × 2,456、Fig3 4,015 × 3,023 px，均 600 dpi，与 v13 逐字节相同）。本项目未记录过其他退回位置。

## 11. 文献检索的记录

沿用 v11 第 11 节（ESM Supplementary Methods S1 "Literature searches"，2026-10-26，PubMed 与 Europe PMC，2000〜2026）。本版未改新规性句，未加文献。

## AUDIT（规约第 13 节；交付前再读规约全文后逐项一行）

最重要四项（先报告）:
1. 版: 通过。底本 = v13（2026-10-29 交付；9 个文件 sha256 与 MANIFEST_v13 一致）；交付后 manuscript/ 下只有 v14（v13 → archive/v13）。
2. 表与图: 通过。正文 60 段、提及 47 个（展开后）；Table 1〜3、Fig. 1〜3、Table S1〜S11、Fig. S1〜S2 全部在正文地の文以编号引用；Supplementary Methods S1 正文 4 处；CHEERS 清单 = Table S1。
3. 文献的真伪: **部分不通过（外部变化）。** DOI 61/61 由 doi.org 解析（302），作者与年不符 0；卷页标记: 10、58（v13 已查明的检查器假阳性）与 **71（新: Crossref 已有卷 37、页 1467–1479，文献表为 in press）**；无 DOI 17 条中 15 条 HTTP 200、**第 8 条 404（新）**、第 52 条图书。文献表文字与 v13 逐字相同（78 条）；按指示未改（第 7 节第 2 项）。
4. 文献的顺序: 通过。正文 1〜71 初出顺无缺（61 组、110 个号，与 v13 相同的组集合，只有 [6] 的位置随 Discussion 段落重排而后移）；72〜78 只在 tables 与 ESM（偏离 4）；78 条全部被引用。

版
- [x] 作业树只有最新版: manuscript/ 下 v14、code、archive、_inbox（空）。archive 在项目根内（项目惯例，用户指定）。
- [x] 会话开始时 sha256 与 MANIFEST_v13 一致（9/9）。
- [x] 底本 = v13，worklog 开头写了底本与 sha256。
- [x] 意外退回 0（五处名指，第 10 节）。
- [—] 数值不变的版: 不适用（本版加入新数值；v13 原有数值的保持见第 4 节）。
- [—] 模板占位: 题名页、Acknowledgments 与 Statements 的占位是尾崎的（第 14 节），不动、不报告。
- [x] 版本标签、作业注记、ARS 标记 0（四个 docx 扫描）。
- [x] MANIFEST_v14 写好、v13 移入 archive（交付时）。
- [x] 解析输出: 57 个来源中只有计划文件变更；新增 fourarm_* 的 sha256 记入 MANIFEST_v14。
- [x] 差分全部对应指示（manuscript 14 块、tables 3 块、ESM 23 块；不能解释的 0）。
- [x] 撤回主张复活 0（第 8 节）。
- [x] 修订与批注 0（Word COM，三个 docx）。
- [x] 作业树无 ars/。

文献与编号
- [x] 初出顺 1〜71 无缺；未引用 0、表外号 0。
- [ ] DOI 与书目: 61/61 解析、作者与年 0 不符；第 71 条卷页与 Crossref 不一致（in press → 37:1467–1479）、第 8 条网址 404（第 7 节第 2 项，待用户决定）。
- [—] 新引用: 无（新文字中的 [9,14]、[7]、[28–31] 是原段落的既有引用，与 v13 同一主张）。
- [—] ARS citation-check: 本版未增未移文献，未跑。
- [x] 作者名-年份式的正文引用 0。
- [x] 超过 10 年 8 条、自引 0（v11 报告，文献未增减）。
- [x] 新规性句未改。
- [x] 四系列初出顺 1..n（Table [1, 2, 3]、Fig. [1, 2, 3]、Table S [1..11]、Fig. S [1, 2]）。新 Table 2 首次在 Four strategies compared；Table S4 首次明确引用在 Exercise compared with pembrolizumab（按范围规则 S1〜S11 与 v13 一样在 Study design 第 3 段 "Tables S1–S11" 初出）。
- [x] 各系列最大号 = 实物数（3、3、11、2）。
- [x] 每个表与图在正文地の文至少一次。
- [x] ESM 内顺序 S1〜S11、Fig. S1〜S2。
- [x] Supplementary Methods S1 与 CHEERS 清单由正文引用。
- [x] Fig1〜3.tif 已附，Fig. 1 起依次在正文提及。

标题与格式
- [偏离] 大标题: BCRT 结构（偏离 1）；Results 二级标题 5 个（指示 1d）。
- [x] 规约外的节与项目: v13 与 v14 相同（Abstract/Keywords、Conclusion、Acknowledgments、References、Statements and Declarations 7 项、Figure captions），未增未减。
- [偏离] Methods 小标题 5 个（偏离 1）。
- [x] Heading 样式 0（manuscript 168 段全 Normal；tables 309、ESM 2,507 段全 Normal）。
- [x] 全部 run 12 pt Times New Roman（manuscript 180/180、tables 369/369、ESM 2,660/2,660）。
- [x] 行号有（lnNumType）。
- [x] 双倍行距（manuscript 非空 165 段 line = 480）。
- [x] 句中粗体 0（粗体 26 run = 题名、大标题、抄录标签、Statements 标签、图注标签，同 v13）。
- [x] 表的列头与数值无粗体；粗体只在面板行（新 Table 2: A、B 两行）。
- [x] 非黑字 0。
- [x] 中黑「・」0（Keywords 的 "·" 为 v13 既有）。
- [x] 表页为横版（tables 3 节、ESM S4 节）。
- [偏离] 表脚注记号 a〜d；"Note" 开头 0。
- [x] 脚注记号与表内上标一一对应: Table 2 a（题）、b、c（面板 A 题）、d（面板 B 题）对脚注 a〜d；Table S4 a（题）、b、c（列头）对脚注 a〜c（面板 C 的 d 随行删除）；Table 1、3 未变。
- [x] 图 600 dpi（第 10 节）。
- [x] 前付一项一段（尾崎，未动）。
- [x] 生成 AI 记述 0。
- [x] ARS 作业标记 0。
- [x] ARS 默认来源的结构 0（Conclusion 为既有，规则 10）。
- [x] 美式拼写、"Fig." 统一。
- [ ] 语数: 实测并写入题名页；抄录 248 ≤ 250，**正文 3,745 > 3,500**（第 7 节第 1 项）。

数值
- [x] 本文与抄录的新数值全部在数值台帳（第 4 节），机械查找 245 个、未找到 0。
- [x] 表脚注数值（Table 2 脚注 a〜d）在 Table 1 或 Table 2 中。
- [注] 同一数值两表: Table 2 B 与 Table S4 基准列（指示的设计，第 7 节第 5 项）；v11 记的有意例外照旧。
- [—] n 的合计、流程图: 模型研究，不适用。
- [—] 对象者数: 不适用。
- [x] 点估计在 UI 内（4,426 ∈ [−330, 8,901]；2.156 ∈ [0.245, 4.228]）。
- [x] 同一统计量各处同值同位（Table 2 与正文、抄录: 2,053、0.425、0.722、2,726 等）。
- [—] p 值: 无。
- [x] 因果词 0（sec10）。
- [x] 负号为 −（Table 2 的 −0.168 等、正文 −330、−1,911）、千位逗号。
- [x] 小数位: Table 2 费用整数（千日元）、QALY 3 位、HR 3 位、pCR 1 位、概率 1 位。

内容
- [x] Methods 无数值结果（新 (2)、(3) 只写 HR 的取值与搜索范围）。
- [x] Results 无"使用了"型。
- [x] 结果句有表的参照（新 Results 两节各以 Table 2 开头；新句 Table S4）。
- [x] 各解析的目的句（新 (2) "To compare the four arms"、(3) "To estimate the maximum affordable cost"）。
- [注] Introduction 末两段: 最后一段为指示原文的目的；不足段未改（第 7 节第 7 项）。
- [注] 目的对应: 目的①四组比较 → Statistical analysis (2)、Results 第 1 节、Table 2 A、Discussion 第 1 段；目的②与帕博利珠单抗相同所需的效应 → (3)、Results 第 2 节、Table 2 B、Discussion 第 2 段；目的③（主要）最大可负担费用 → (3)〜(6)、Results 第 3、4 节、Table 3、Fig. 2、Discussion 第 3〜6 段；(1) 验证与 (7) 一年净收益照 v13 的注（不对应单一目的编号）。
- [x] 曝露与结局名称（未改）。
- [注] 抄录的目的（Purpose）未改（指示: 不动）；Purpose 只写主要目的。
- [x] Results 段落顺序 = 目的顺；段首名指表（新两节 Table 2）。
- [x] Discussion 段首名指: 第 1 段 (Table 2)；其余既有段照旧。
- [注] Discussion 第 1 段只回答目的①（第 7 节第 7 项）。
- [注] Discussion 与 Results 的重复: 第 1 段重述 "both strategies without exercise were dominated"（Results 第 1 节）；数值再揭 1.1%（第 3 段，v13 第 1 段已有）。
- [x] Discussion 引用分布: 第 1〜8 段 0、1、1、0、1、1、2、1 组；后半无新出文献（[28–31] 在第 6 段，v13 第 4 段同一引用）。
- [x] "further research is needed" 型 0。
- [x] 临床医会改变什么（Implications 未改）。
- [x] Implications 只改表号。
- [注] check_acronyms（ARS 3.24.0；抽出方法在 v13 上逐字节复现 v13 的两份报告）: 抄录 "No findings"，coverage partial，Not checked JPY、QALY；正文 partial，Not checked JPY、TNBC、QALY、ICER，Not defined PMC、CHEERS、EQ（与 v13 相同）。Table 2 脚注 a 再展开 HR、ICER、JPY、pCR、QALY、UI。
- [x] 限界只在 Limitations（未改）。
- [x] Outcome/Variables 第一句（未改）。
- [x] 统计软件只写语言与版本（未改）。
- [x] Data availability 与公开仓库: 文字未改；公开目录加入 25 与 test（第 6 节），去名检查人名 0。
- [x] CHEERS 清单 28 项中 24 项有节、段与页，页码按 v14 实测（Word + PDF 独立核对，不符 0）。
- [x] 题名 manuscript 与 ESM 一致（未改）。
- [x] 事前计划、缺失、多重比较（未改）。
- [—] 选择流程图: 不适用。
- [x] 图未改（逐字节复制）。
- [x] 图表重复（未改）。
- [—] 著者贡献: 尾崎的占位（第 14 节）。
- [x] AI 常套语 0、开场套话 0、接续词连发 0、破折号 — 0（manuscript）；30 词超句 47、最长 121；150 词超段 3（报告，第 7 节第 6 项）。
- [注] 裸时间词 3（currently、now、current；同 v13 的个数）。
- [x] 主张未变强: 新文字为指示原文；Discussion 第 2 段 "a payer choosing one would still choose pembrolizumab" 等为指示的措辞。
- [—] 查读回复版: 不适用。
- [—] humanizer / stop-slop: 本版未用（指示）。
