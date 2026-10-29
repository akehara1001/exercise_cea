# worklog v13（2026-10-29）

## 1. 底本

底本: manuscript_v12_BCRT.docx（v12，2026-10-29 交付，sha256 前 8 位 3e294047）。同批: tables_v12_BCRT.docx（d022962f）、ESM_1_v12.docx（ae84d2f6）、ESM_1_v12.pdf（8174761b）、Fig1〜3.tif（c13b748e、662046bf、d7926e1e）、cover_letter_v12_BCRT.docx（21ed7f1a）、worklog_v12.md（1eb5f8b3）。会话开始时 9 个文件的 sha256 全部与 MANIFEST_v12.md 一致；作业树 git 状态干净（HEAD 45dd2cd）；manuscript/ 下只有 v12（_inbox 空）。
本版是小修: 撤回 v12 的 1b（用户: v12 的 1b 是指示错误）、Word count 按实测，并完成 v12 停下的第 3 步公开代码。不跑 ARS 起草、humanizer、stop-slop。
编辑方法: v12 的 docx 直接编辑（manuscript/code/edit_manuscript_v13.py；lxml 只改 word/document.xml，其余部件逐字节照搬；每条原文须在 v12 中唯一命中，否则停止）。ESM 用 manuscript/code/edit_esm_v13.py 核对页码，页码无变化，所以 ESM_1_v13.docx 是 ESM_1_v12.docx 的逐字节复制。tables、Fig1〜3.tif、cover letter 为 v12 的逐字节复制（cmp 确认）。manuscript 由 Word（COM）打开确认: 修订 0、批注 0、28 页。

## 2. 投稿先与投稿规格（沿用 v12 第 2 节）

- 投稿先 BCRT；抄录结构式，上限 250 词；正文上限 3,500 词；Springer 数字式文献；美式拼写；"Fig."。
- 语数计法（同 v12）: Word ComputeStatistics（逐段），抄录 = 四个结构段去掉 4 个标签；正文 = Introduction 至 Conclusion，不含标题。
  - v13: 抄录 250（含标签 254）；正文 3,242（含 16 个标题 3,277）。→ 题名页 Word count 行改为 "abstract 250; main text 3,242"（1b），与指示的预期 3,242 一致。
  - 变化的来源: 1a 正文 −2（"5 million Japanese yen (JPY)" 5 词 → "JPY 5 million" 3 词）。抄录未改。
- 投稿先与共著者决定的偏离（v11 第 2 节，本版照旧不动）: 1. 标题结构；2. 表脚注记号 a〜d；3. 题名页在 manuscript 内、表另成 tables 文件、图为 tif；4. 文献 72〜78 只在 Table 1 与 ESM，不重排。

## 3. 用语表

沿用 v12 第 3 节，本版无改名。"Japanese yen (JPY)": 抄录中展开一次（v12 1a，保留不动）；正文中只在 Introduction 第 1 段展开一次（"398,924 Japanese yen (JPY)"），Study design 第 2 段恢复为 "JPY 5 million"（本版 1a）。

## 4. 数值台帳

本版不改任何结果数值。来源文件 = v9 数值台帳第 8 节的 57 个文件（清单 manuscript/code/checks_v11/out/src_sha_v9.txt），sha256 于本版重算: 变动 0、缺失 0（MANIFEST_v13.md）。
v12→v13 数字记号的差（checks_v11/regress.py；输出的 v10/v11 标签即旧/新）: manuscript 只在 v12: 3,244；只在 v13: 3,242（均为 Word count）。抄录与正文其他数字 1,030 个一致。tables 335 个、ESM 2,686 个数字记号一致。

## 5. 本版变更的段落（由生成后的 docx 读回；checks_v11/regress.py、regress2.py；输出在 checks_v13/out/）

### manuscript（164 段 → 164 段；未变 162；变动块 2，全部对应指示）
| 块 | 位置 | 指示 |
|---|---|---|
| M1 | 题名页 Word count 行（P unit 6） | 1b |
| M2 | Study design 第 2 段（P unit 23） | 1a |

逐段差分（原文 → 新文）:
- [M1] 「Word count: abstract 250; main text 3,244 (excluding …」→「Word count: abstract 250; main text 3,242 (excluding …」
- [M2] 「… The willingness-to-pay threshold for exercise was 5 million Japanese yen (JPY) per QALY [41,42]; …」→「… The willingness-to-pay threshold for exercise was JPY 5 million per QALY [41,42]; …」（该段其余文字不变；新文 = v11 的写法）

### tables
v12 的逐字节复制。变动 0。

### ESM（Table S1 页码核对；变动 0）
28 项的页码按 Word 对 manuscript_v13_BCRT.docx 的 Range.Information(3) 重新计算（checks_v13/out/m13_stats.json）。脚本先用 v12 的分页与 v12 的 Location 文字重建 v12 的 28 格，与 ESM_1_v12 逐格一致后再算 v13: 28 项全部不变（第 19、21、22、25 项按 v12 规则不加页码）。因此 ESM_1_v13.docx = ESM_1_v12.docx 的逐字节复制（edit_esm_v13.py 无变化时复制原文件）。
页码的独立核对（checks_v12/pdf_pages.py，Word 导出的 manuscript PDF 中按每段首尾 6 词定位）: 139 段定位、页码不符 0；未定位 10 段与 v12 相同（文献 7 条、抄录 Purpose 段、Fig. 3 图注，均只是段尾未定位，都不是 Location 引用的段落）。
ESM_1_v13.pdf: Word（SaveAs2, 17）由 ESM_1_v13.docx 的副本导出，46 页；与 ESM_1_v12.pdf 逐页比较文字，46 页全部相同（文件 sha256 不同，来自 PDF 的生成时刻元数据）。

## 6. 第 4 步的核对结果

### 6.1 数值
除 Word count 一行外，抄录、正文、表、ESM 的全部数值与 v12 一致（第 4 节）。来源文件 57 个 sha256 未变。

### 6.2 退行
manuscript 2 块、tables 0、ESM 0，全部对应指示（第 5 节）；对应不上的 0。名指确认: 题名（manuscript 与 ESM 未变）；责任著者占位行（尾崎，未动）；补充表脚注（ESM 逐字节相同）；表脚注（tables 逐字节相同）；语数（按 1b 改为实测）；图解像度（600 dpi，第 6.6 节）。撤回项（第 9 节）: Study design 第 2 段不再有 "5 million Japanese yen (JPY)"。

### 6.3 文献（checks_v11/refcheck.py 在 v13 上全量重跑；checks_v13/citeorder.py）
- DOI: 61/61 doi.org 解析（302）；Crossref 逐字段: 作者 0 不符、年 0 不符；卷 1 条（58）、页 2 条（10、58）为 v12 已查明的检查器假阳性（58: 问号后的题名与刊名分割；10: Crossref 只有文章号）。撤稿与关注表达标记 0（10 的 update-to new_version 为 Cochrane 新版）。78 条记录除 HTTP 状态外与 v12 的核对结果完全相同。
- 无 DOI 17 条: 16 条网址 HTTP 200；第 52 条图书（v11 已确认）。
- 初出顺: 正文（Introduction 至 Conclusion，56 段）取出引用组 61、号 110（展开后），初出顺 = 1, 2, …, 71，无缺号。manuscript（至 References）、tables、ESM 的引用序列与 v12 完全相同（61、24、126 组）。78 条全部被引用；72〜78 只在 tables 与 ESM（偏离 4）。
- 本版未增、未移、未改文献；ARS citation-check 按规约第 1.3 节不是必须项，未跑。

### 6.4 表与图编号（规约第 7.1 节第 9 条；checks_v13/tfnum.py = checks_v12/tfnum.py 只换文件名）
扫描正文 56 段，取出提及 43 个（展开后）。Table [1, 2, 3]，最大 3 = 表 3 个；Fig. [1, 2, 3]，最大 3 = Fig1〜3.tif = 图注 3；Table S [1..10]，最大 10 = ESM 补充表 10，ESM 内顺序 S1〜S10；Fig. S [1, 2]，最大 2，顺序 S1、S2。每个编号初出在地の文。Supplementary Methods S1 正文 4 处，不带 S1 0 处。

### 6.5 格式（规约第 8 节；checks_v11/fmt_audit.py，checks_v13/out/fmt_v13.txt）
manuscript: Heading 样式 0（164 段全 Normal）；176/176 run 12 pt Times New Roman、自动色；行号有（lnNumType）；非空 161 段 line=480；粗体 26 run（与 v12 相同: 题名、大标题、抄录标签、Statements 标签、图注标签）；句中粗体 0。ESM 与 tables 逐字节相同（v12: ESM 2,551/2,551、tables 349/349 run 12 pt）。需要的机械修正: 0。

### 6.6 图
Fig1.tif 4,015 × 2,173 px、600 × 600 dpi（170.0 × 92.0 mm）；Fig2.tif 4,015 × 2,456 px、600 dpi（170.0 × 104.0 mm）；Fig3.tif 4,015 × 3,023 px、600 dpi（170.0 × 128.0 mm）。RGBA。与 v12 逐字节相同。

### 6.7 第 10 节计数（只报告；checks_v11/sec10.py，checks_v13/out/sec10_v13.txt）
扫描抄录 5 段 + 正文 40 段（不含标题）、125 句: 禁用语 0、开场套话 0、接续词连发 0、因果词 0、破折号 — 0、中黒「・」0。超过 30 词的句子 43（v12 43；1a 那句由 42 词变 40 词），最长 76 词（Outcomes 第 2 段，既有）。超过 150 词的段落 2（与 v12 相同，Discussion 的两段）。裸时间词 3（currently、now、current，既有）。
check_acronyms（ARS 3.24.0，抄录与正文分别，抽出方法以 v12 的抽出文本复核一致）: 抄录 "No findings"，coverage partial，Not checked JPY、QALY；正文 partial，Not checked JPY、TNBC、QALY、ICER，Not defined PMC、CHEERS、EQ（与 v12 相同）。

## 7. 第 3 步: 公开用代码（完成）

公开目录: C:\Users\原明美\Documents\ClaudeCode\exercise_cea_public\（作业树外）。文件清单与 sha256 前 16 位、与 v12 清单的增删改: manuscript/code/checks_v13/out/public_files.txt（v12 114 个 → 105 个: 增 6、删 15、改 3、不变 96）。

### 7.1 入力表（R/py/26_public_params.py 修改后重新生成）
- 源文件 input/params/parameters_v10.xlsx sha256 5e939653（未变）→ 公开版 sha256 f0e36eff（v12 版 198f01e7）。缺省的 ESM 与 tables 路径改为 manuscript/v13/（内容与 v12 逐字节相同）。
- (a) 備考: U01〜U05 只留 22_phase2b_main.R 读取的片段，写成该解析能读的最短形式（关键词 + 值，"、" 分隔；U05 前加 "期間 12.5 週"）。值是 R 的正则从内部表取到的字符串，脚本双向断言（公开文字再解析 = 内部文字的解析）。U01〜U05 在内部表中没有幅的规则标记（rule_of 为空），也没有 "【要確認"。
  - U01 "米国 0.836、英国 0.859、豪州 0.775"；U02 "米国 0.842、英国 0.862、豪州 0.785"；U03 "米国 0.768、英国 0.800、豪州 0.693"；U04 "米国 0.639、英国 0.697、豪州 0.552"；U05 "期間 12.5 週、米国 0.034、英国 0.025、豪州 0.039"。
  - 其他行照 v12: 薬価固定 4、0例：PSAは固定 4、±25% 7、片側対称 9、无 57（U01〜U05 计在 "无" 中）。
- (b) 数据验证: 「パラメータ」M2:M82 的 1 个（担当列的列表 "尾崎,原" 与提示语）删除；「シナリオ」0 个。生成后 xlsx 的 XML 中 dataValidation 0。其余照 v12（出典、根拠、属性、批注、隐藏表、定义名称）。

### 7.2 代码与数据
- R/engine.R 第 322 行: "# S-JP subgroups of the non-pCR branch (Dr Ozaki, 2026-10-23): gBRCA carriers …" → "# S-JP subgroups of the non-pCR branch: gBRCA carriers …"（连同前面的空格删去括号，冒号接在 branch 之后；注释其余文字与代码不动）。与作业树 diff: 只有这一行。
- R/22_phase2b_main.R: 第 450 行注释与第 453 行路径 data/params_hara/ → data/params_utility/。与作业树 diff: 这两行 + v12 已改的根目录一行（第 19 行）。plan10 保留。
- data/params_utility/utility_scenarios.csv = 作业树 data/params_hara/utility_scenarios.csv 的逐字节复制（6 行: param_id、base、japan、japan_source）。params_hara 的其他 5 个文件不放。
- 图像: 删除 15 个（data/digitized/ 的 *_native.* 4 个、data/digitized/esme/ 的 1 个、qa/ 的叠加图 9 个、esme/qa/ 的 1 个），空目录 qa/ 与 esme/qa/ 一并删除。指示写 "全部 17 个"，但括号中描述的文件在公开目录与作业树中都是 15 个；按文件头检出的非文本二进制共 17 个 = 这 15 个 + input/lifetable/ 的两份厚生劳动省 PDF（life25-01_about.pdf、life25-07_female.pdf；不是图像，v12 指示要求放入 input/lifetable/），PDF 保留。公开目录的 R 脚本中检索 native、overlay、.png、.jpeg: 0 处；03_reconstruct_ipd.R 在 data/digitized/ 只读 csv（risktable、curve、censor）。
- 03_reconstruct_ipd.R 缺少的文件补入: data/reported_values.csv、R/py/rasterspec.json、input/user_supplied_values.csv（均为作业树文件的逐字节复制）。放入前去名检查（与第 7.3 节同词表，并加检 akehara1001、Users、C:/）: 3 件命中均 0；utility_scenarios.csv 同样 0。
- renv.lock 原样保留。
- README.md（英文）与 LICENSE（MIT，"Copyright (c) 2026 the authors"）新建。README 内容按 v12 指示第 3 步: 用途；R version 4.5.1 与 renv::restore()；运行顺序（00_lifetable.R → 10_read_params.R → 22_phase2b_main.R 的 det、psa、plan9_det、plan9_psa、plan10）；Table 2、Table 3、Fig. 2、Fig. 3 由哪个脚本与模式、哪些输出文件得到（按 v9 数值台帳与 make_figures.py 的读取文件）；入力表的列名为日文、param_id 对应 Online Resource 1 Supplementary Table S2 的 Code、方括号中的数字是论文的文献号、已删去个人名与作业注记且数值与论文相同；随机种子 20261023（bootstrap 样本 b 用 20261023 + b，与 ESM 一致）；完整概率分析耗时长（确定性模式本机实测 0.6〜1.5 分）。另加一句（v13）: "The curve coordinates in data/digitized/ were read from the figures of the cited publications; the figures themselves are not reproduced here." 不写作者名单。plan9_cohort 模式需要 input/params/cohort_N_jbcs2024.csv（不在放入清单），README 未列这个模式（第 8 节）。

### 7.3 去名检查（checks_v13/public_name_scan.py = checks_v12 版 + 无扩展名文件按文本读，用于 LICENSE；植入测试 csv、无扩展名、xlsx、rds 各一，全部词命中）
扫描 105 个文件（含 README.md、LICENSE）。
| 词 | 命中 | 内容 |
|---|---|---|
| 尾崎 | 0 | — |
| Ozaki | 0 | — |
| 原明美 | 0 | — |
| Hara | 12（人名 0） | "character" 的一部分: R 代码 4（00_lifetable、03、10、22 各 1）、renv.lock 8（Description、Title、Authors@R、Author 字段中的 character/Character） |
| Akemi | 0 | — |
| 立花 | 0 | — |
| 押 | 0 | — |
| 先生 | 0 | — |
| @ | 425（全部在 renv.lock，指示除外） | 包元数据: Authors@R 键名 97、Authors@R 值 210、Maintainer 106、Author 8、Contact 2、MailingList 2 |
| 「原」 | 0 | — |
akehara1001: 0（README 未写网址）。绝对路径（C:/、/Users/、Documents/ClaudeCode）: 0 个文件。

### 7.4 03_reconstruct_ipd.R 的运行（manuscript/code/checks_v13/cmp_ipd.R；日志 checks_v13/out/run03.log）
在 scratchpad 的公开目录副本中先删去 data/ipd/ 下 03 写出的 25 个文件（esme/ 的 3 个不是 03 写出的，保留），再运行 03: 正常完成（无 "Execution halted"；Rscript 退出码 127 为本机已知现象），验证 71 行、门槛 62 项、门槛不过 0、非门槛不过 5；output/phase1/validation.csv 与 validation_diagnostics.csv 和作业树逐字节相同。重建的 25 个文件与公开目录 data/ipd/ 比较: 按值 25/25 相同、逐字节 25/25 相同；ipd_all.rds 按值 identical() TRUE（24 条曲线、11,166 行）。不需要读取图像。

### 7.5 一致性（scratchpad 的新副本中运行；公开目录未写入任何输出；日志 checks_v13/out/run_*.log）
- 00_lifetable.R → data/lifetable_female_2025.csv 与作业树逐字节相同。
- 10_read_params.R → data/params_dist.csv 与作业树逐字节相同（sha256 前 16 位 3b8e10fcc27eb396）。
- 22_phase2b_main.R det（1.5 分）、plan9_det（0.6 分）、plan10（1.2 分）全部正常完成（plan9_det 内置的 sc_base 复现检查、plan10 内置的 utility_us/uk/au、elmore、sjp 对 scenario_caps.csv 与 base 对 sc_base_crossings.csv 的检查都通过）。
- 输出 23 个 csv 与作业树逐列比较（checks_v13/compare_v13.py → checks_v13/out/compare_v13.txt）: 数值列最大差 0、NA 不一致 0。文字列只有 oneway_base.csv 9 行与 oneway_sjp.csv 1 行的 provisional 列 TRUE → FALSE（指示允许）: 22 主脚本第 41 行由 備考 中的 "【要確認" 判定 provisional，公开表的 備考 不含作业注记；该列只是 oneway 输出的标签，不进入任何计算。
- 正文与表印出的值（公开运行、作业树、v13 文字三者一致，24/24）: HR 0.85 最大可承受费用 2,726（主比较）与 3,443（次比较）；帕博利珠单抗 ICER 2,053；日本效用情景 2,733（千日元，plan10）；Table 2 A 部分盈亏平衡 HR 0.989/0.991、0.948/0.958、0.958/0.966、0.997/0.998；C 部分 0.988/0.990、0.918/0.934、0.987/0.990、0.914/0.925；正文的效用情景与 S-JP 范围 0.988 to 0.989（plan10 sc_crossings.csv，Table S10）；Table 3 C 部分 0.425 与 35.9 个百分点。
- 作业树 output/phase2/main 的其余文件（psa_*、sc_*_psa_*、cohort_value*、det_cost_saving_crossings.csv、fig_*.png）来自 psa、plan9_psa、plan9_cohort 或报告脚本，不在本次范围（完整的 1,000 次概率分析按指示未重跑）。

### 7.6 git（公开目录）
git init -b main 并本地 commit 4d8e2ad（"R code, input sheet and reconstructed patient-level data of the exercise cost-effectiveness model"），105 个文件；无远程、未推送；工作区干净。
- 作者身份: 公开目录没有自己的 git 设置、本机无全局身份；作业树的身份是姓名加含 akehara1001 的 noreply 邮箱，用它会把姓名写进公开仓库的提交记录。本次只用命令行参数设为 "the authors"（与 LICENSE 一致）、邮箱空，未写入任何配置文件。推送前如需改用本人身份: git commit --amend --reset-author。
- 换行: 81 个文本文件为 CRLF（R 在 Windows 上写出）。系统级 core.autocrlf=true 会在提交时改成 LF，本次提交时用 -c core.autocrlf=false，提交内容与核对过的文件逐字节相同（105/105 个 blob 与文件字节一致）。

## 8. 著者侧与用户待定的事项

1. 公开仓库的提交作者为 "the authors"（第 7.6 节）；提交说明末尾有 Co-Authored-By 行。推送前如需更改可 amend。
2. plan9_cohort（正文 Results 的一年净效益 JPY 2.68 billion 等）需要 input/params/cohort_N_jbcs2024.csv，不在 v12 的放入清单，公开目录中不能运行；README 未列此模式。
3. 指示中的图像数 17 与实际 15 不同（第 7.2 节）；input/lifetable/ 的两份 PDF 保留。
4. ESM 第 9 页顶部只有第 28 项的一词 "requirements." 与脚注 a（v12 第 6.7 节；版式按指示未动）。
5. 文献 28 的写法 "Fasching PA" 与 Crossref、PubMed、出版社元数据的 "A. Fasching" 不同（v12 按指示）。
6. check_acronyms partial（第 6.7 节）；超过 150 词的段落 2、超过 30 词的句子 43、裸时间词 3（均既有）。
7. 目的对应（v11 第 7 节第 8 项）照旧: Statistical analysis 的 (1) 与 (6) 不对应单一目的编号；Discussion 第 1 段只直接回答目的 1 与 3。

## 9. 撤回的主张

- v12 的 1b（Study design 第 2 段的 "5 million Japanese yen (JPY)"，正文中 JPY 的第二次展开）: 用户确认为 v12 指示的错误，本版恢复为 "JPY 5 million"。以后的版本不应再出现。抄录中的展开（v12 1a）保留。

## 10. 共著者コメント台帳

本版无共著者交回的文件（底本为 CC 交付的 v12）。采否即用户指示 v13 的第 1〜3 步。

## 11. 过去意外退回的地方

规约第 1.2 节第 7 条名指的五处本版逐一确认，无退回（第 6.2 节）。本项目未记录过其他退回位置。

## 12. 文献检索的记录

沿用 v11 第 11 节（ESM Supplementary Methods S1 "Literature searches"，2026-10-26，PubMed 与 Europe PMC，2000〜2026）。本版未改新规性句。

## AUDIT（规约第 13 节；交付前再读规约全文后逐项一行）

最重要四项（先报告）:
1. 版: 通过。底本 = v12（2026-10-29 交付；9 个文件 sha256 与 MANIFEST_v12 一致）；交付后 manuscript/ 下只有 v13（v12 → archive/v12）。
2. 表与图: 通过。四系列全部在正文地の文以编号引用（56 段、43 个提及）；Supplementary Methods S1 与 CHEERS 清单（Table S1）由正文引用。
3. 文献的真伪: 通过。DOI 61/61 解析，作者与年 0 不符（卷页的 2 个标记为检查器假阳性，第 6.3 节）；无 DOI 17 条中 16 条网址 200、1 条图书已确认。
4. 文献的顺序: 通过。正文 1〜71 初出顺无缺（110 个号）；72〜78 只在 tables 与 ESM（偏离 4）。

版
- [x] 作业树只有最新版: manuscript/ 下 v13、code、archive、_inbox（空）。archive 在项目根内（项目惯例，用户指定）。
- [x] 会话开始时 sha256 与 MANIFEST_v12 一致（9/9）。
- [x] 底本 = v12，worklog 开头写了底本与 sha256。
- [x] 意外退回 0（五处名指，第 6.2 节）。
- [x] 数值与 v12 一致（Word count 除外；第 4 节）。
- [—] 模板占位: 题名页、Statements 与 cover letter 中的占位是尾崎的（第 14 节），不动、不报告。
- [x] 版本标签与作业注记 0（manuscript 只改 2 段，其余与 v12 相同；ESM、tables、cover letter 逐字节相同）。
- [x] MANIFEST_v13 写好、v12 移入 archive（交付时）。
- [x] 解析输出 57 个 sha256 不变（本版不改数值）。
- [x] 差分全部对应指示（manuscript 2 块、ESM 0、tables 0）。
- [x] 撤回主张复活 0（v12 1b 的写法已撤回，第 9 节）。
- [x] 修订与批注 0（Word COM 读 manuscript；ESM 与 v12 相同）。
- [x] 作业树无 ars/。

文献与编号
- [x] 初出顺 1〜71 无缺；未引用 0、表外号 0。
- [x] DOI 61/61 解析；书目不符 0（第 6.3 节）。
- [—] 新引用: 无。
- [—] ARS citation-check: 本版未增未移文献，未跑。
- [x] 作者名-年份式的正文引用 0（引用序列与 v12 相同）。
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
- [x] 规约外的节与项目: v12 与 v13 相同（Abstract/Keywords、Conclusion、Acknowledgments、References、Statements and Declarations 7 项、Figure captions），未增未减。
- [偏离] Methods 小标题 5 个（偏离 1）。
- [x] Heading 样式 0（164 段全 Normal）。
- [x] 全部 run 12 pt Times New Roman（manuscript 176/176；ESM、tables 逐字节同 v12）。
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
- [x] 生成 AI 记述 0（交付物只改 2 段，其余与 v12 相同；v12 扫描 0）。
- [x] ARS 作业标记 0（同上）。
- [x] ARS 默认来源的结构 0（Conclusion 为既有，规则 10）。
- [x] 美式拼写、"Fig." 统一（未变）。
- [x] 语数实测、写入题名页、在上限内（250 ≤ 250；3,242 ≤ 3,500）。

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
- [x] Methods 无数值结果（1a 只改货币写法）。
- [x] Results 无"使用了"型（未改动）。
- [x] 结果句有表或图的参照（未改动）。
- [x] 各解析的目的句（未改动）。
- [x] Introduction 末两段的形（未改动）。
- [注] 目的对应表: 照 v11 第 7 节第 8 项（第 8 节第 7 项）。
- [x] 曝露与结局名称（未改动）。
- [x] 抄录的目的与结论（未改动）。
- [x] Results 段落顺序与开头名指（未改动）。
- [x] Discussion 段首名指（未改动）。
- [注] Discussion 第 1 段只直接回答目的 1 与 3（既有）。
- [x] Discussion 与 Results 的重复（未改动）。
- [x] Discussion 引用集中在中段（未改动）。
- [x] "further research is needed" 型 0。
- [x] 临床医会改变什么（未改动）。
- [x] Implications 未改动。
- [注] check_acronyms partial（第 6.7 节）；正文 JPY 只在 Introduction 第 1 段展开。
- [x] 限界只在 Limitations（未改动）。
- [x] Outcome/Variables 第一句（未改动）。
- [x] 统计软件只写语言与版本（未改动）。
- [x] Data availability 与公开仓库: 正文写 "The R code of the model, its input file and the patient-level data reconstructed from published survival curves"；公开目录有模型 R 代码、入力表 parameters_v10.xlsx、data/ipd/（另有生命表、数字化坐标、拟合参数、bootstrap 样本与核对用数据）。去名检查人名 0；网址中的 akehara1001 是仓库所有者的账号名，提交作者不含姓名（第 7.6 节）。仓库尚未推送。
- [x] CHEERS 清单 28 项中 24 项有节、段与页（19、21、22、25 按指示不加），页码按 v13 实测，无变化。
- [x] 题名 manuscript 与 ESM 一致（未改动）。
- [x] 事前计划、缺失、多重比较（未改动）。
- [—] 选择流程图: 不适用。
- [x] 图未改动（逐字节复制）。
- [x] 图表重复（未改动）。
- [—] 著者贡献: 尾崎的占位（第 14 节）。
- [x] AI 常套语 0；破折号 0；30 词超句 43、最长 76；150 词超段 2（报告）。
- [注] 裸时间词 3 处（既有）。
- [x] 主张未变强（1a 只改货币写法，1b 为语数）。
- [—] 查读回复版: 不适用。
- [—] humanizer / stop-slop: 本版未用。
