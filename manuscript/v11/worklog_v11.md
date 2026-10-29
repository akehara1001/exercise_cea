# worklog v11（2026-10-28）

## 1. 底本

底本: manuscript_v10_BCRT.docx（v10，尾崎 2026-10-28 交付，sha256 前 8 位 ec20edac）。同批: tables_v10_BCRT.docx（2a13e2e6）、ESM_1.docx（9c63d493）、cover_letter_BCRT.docx（21ed7f1a）；四件 sha256 前 16 位与指示一致（ec20edacf2c278e2、2a13e2e69c4187ae、9c63d49303d56a4f、21ed7f1aa387e8b7）。ESM_1.pdf（8081215f）只作对照。
图: 尾崎未发 tif，Fig1.tif〜Fig3.tif 为 manuscript/v9/figures/fig1.tiff〜fig3.tiff 的逐字节复制（sha256 与 v9 MANIFEST 一致），之后 v9 整体 git mv 到 manuscript/archive/v9/。
本版是共著者交回之后的改稿：不跑 ARS 起草、humanizer、stop-slop；只做指示第 1〜3 步，第 5 步只核对。
编辑方法: v10 的 docx 直接编辑（manuscript/code/edit_manuscript_v11.py、edit_tables_v11.py、edit_esm_v11.py；lxml 只改 document.xml〔manuscript 另改 styles.xml 的 docDefaults 与 footer1.xml 的字号〕，其余部件逐字节照搬；每条原文须在 v10 中唯一命中，否则停止）。三份 docx 均由 Word（COM）打开确认：修订 0、批注 0。

## 2. 投稿先与投稿规格

- 投稿先: Breast Cancer Research and Treatment（BCRT；尾崎的 v10 结构）。
- 抄录: 结构式（Purpose / Methods / Results / Conclusion，粗体标签在段首），上限 250 词。正文上限 3,500 词（用户指示）。
- 文献: Springer 数字式（方括号 [n]），按初出顺；DOI 写作 https://doi.org/…。
- 拼写: 美式。图称 "Fig."。
- 语数的计法（本版确定，记录供下一版沿用）: Word 的 ComputeStatistics（逐段），抄录 = 四个结构段去掉 4 个标签；正文 = Introduction 至 Conclusion 末尾，不含小标题与大标题，不含抄录、题名页、表、图注、文献、Acknowledgments、Statements and Declarations。
  - v11: 抄录 250（含标签 254；空白分词 250）；正文 3,242（含 16 个标题 3,277）。→ 题名页 Word count 行改为 "abstract 250; main text 3,242"。
  - v10 用同一计法: 抄录 250、正文 3,014（含标题 3,049）。v10 记载的 3,022 用任何计法都无法复现（记录，不追究）。
  - 注: Word 把 "2,223–3,040"（en dash 连写）算 2 词，所以 1i 的方括号化不改变 Word 的抄录词数；空白分词下 249→250。两种计法都 ≤ 250。

### 投稿先与共著者决定的偏离（规约第 3 节、第 7.2 节；本版保留不改）

1. 标题结构: Methods 5 个小标题（Study design、Outcomes、Exercise effect and costs、Survival, costs and utilities、Statistical analysis）、Results 4 个小标题、Implications 与 Limitations 作为 Discussion 下的小标题、另有 Conclusion 大标题。二级标题是斜体（Springer 格式），不是粗体。
2. 表脚注记号 a〜d（上标小写字母），不是 ✳ 型。
3. （同一来源的结构）题名页在 manuscript 内、表另成 tables 文件、图为 tif 文件 + manuscript 末尾的 Figure captions，无 figures docx 与单独的 title page docx。
4. 文献 72〜78 只在 Table 1 与 ESM 中引用，保持排在正文引用（1〜71）之后的编号，不重排（用户决定）。

## 3. 用语表

沿用 v9（manuscript/archive/v9/table_figure_plan_v9.md、check_v9.md）与尾崎 v10 的用语，本版无改名。本版新出现的说法:
| 本文的名字 | 指什么 | 初出 |
|---|---|---|
| the reduction in the hazard, 1 − HR | 运动使复发风险降低的部分；基准下保持 5 年后每年减半 | Methods, Exercise effect and costs, 第 1 段（1e）；Table 1 脚注 d |
| stages (1)〜(6) | Statistical analysis 的编号段落（段首手写编号，非 Word 自动编号） | Methods, Statistical analysis（1g）；ESM Table S1 第 17、20 项与脚注 a |

## 4. 数值台帳

本版不改任何结果数值。来源文件 = v9 数值台帳第 8 节所列 57 个文件，本次逐一重算 sha256: 变动 0、缺失 0（清单与哈希见 manuscript/code/checks_v11/out/src_sha_v9.txt）。
v10→v11 数值标记的差（逐段抽取的数字记号；manuscript/code/checks_v11/regress.py）:
- manuscript: 只在 v10: 3,022（Word count）。只在 v11: 3,242（Word count）；(1)〜(6) 段号与 "steps of 1"、"1 − HR" 的 1/2/3/4/5/6；2000、2026（1b）；0.30、1.00、37（1g 第 2 段）；0.85（1g 第 4 段新句中的 "at an HR of 0.85"，值来自 v10 正文与 Fig. 3）；"KEYNOTE-522" 多 1 次（1g 第 1 段）；URL 中的 202609、20260916、1001（1k、1l）。全部来自指示原文。
- 抄录: 数值完全一致（只把区间改为方括号）。
- tables: 只在 v11: "1" ×2（"Methods S1"、"1 − HR"）。其余 333 个数字记号一致。
- ESM: 变化只在 Table S1 的 Location（段落号与页码）。其余数值一致。
1g 第 2 段的 0.30〜1.00 与 37 个百分点已与代码核对: R/22_phase2b_main.R 第 121、164、176 行（uniroot 区间 [0.30, 1.00]、pCR [0, 0.37]）；"steps of 1" = DP_GRID (0:10)/100（第 39 行）。
1e 的写法已与代码核对（与指示一致，未停）: R/engine.R 第 38〜40 行注释与第 278 行 HR(t) = hr0（t ≤ wane_start），1 − (1 − hr0)·exp(−wane_rate·(t − wane_start))；R/22_phase2b_main.R 第 45 行 base = wane_start 5、wane_rate log(2)；R/econ.R 第 77 行 pp = min(p_pcr[[base]] + delta_pcr, 1) 替换该组的 pCR 比例；混合在 survival_engine 的第 298 行（pp × pCR 层 + (1 − pp) × 非 pCR 层，层取同一治疗 base），第 319 行 os_fast 为同式。

## 5. 本版变更的段落（全部由生成后的 docx 读回；manuscript/code/checks_v11/regress2.py）

### manuscript（v10 158 段 → v11 163 段；未变 139；变动块 15，全部对应指示）
| 块 | 位置 | 指示 |
|---|---|---|
| M1 | 题名页 Word count 行 | 1m |
| M2 | 抄录 Results | 1i |
| M3 | Introduction 第 2 段、第 3 段 | 1a（两处）、1b |
| M4 | Study design 第 2 段、第 3 段 | 1c、1d |
| M5 | Exercise effect and costs 第 1 段 | 1e（两处） |
| M6 | Survival, costs and utilities 第 1 段 | 1f |
| M7 | Statistical analysis 3 段 → 8 段 | 1g |
| M8〜M12 | Results 各段的 95% UI | 1i（10 处） |
| M13 | Implications | 1h |
| M14 | 文献 73 | 1k |
| M15 | Data availability | 1l |
1j: v10 正文中 "Supplementary Methods" 不带 S1 的只有 2 处，分别由 1d 与 1g 改写；1j 另外替换的处数 = 0。v11 正文 "Supplementary Methods S1" 4 处、不带 S1 0 处。
1i 的扫描: 抄录 5 段 + 正文 39 段（不含标题）中，"95% CI / UI / uncertainty interval / confidence interval" 之后接连字符、en dash 或 "to" 的写法 0 件。
格式（规约第 8 节的机械修正，文字不变）: 全部 175 个 run 的字号 10 pt（169）与 14 pt（题名 1）→ 12 pt；段落标记的 sz 一并改为 24；styles.xml docDefaults 10 pt → 12 pt（行号与空段随之 12 pt）；页脚页码 10 pt → 12 pt。结果: 页数 21 → 28。

### tables（289 单元/段，变动 3，全部对应第 2 步）
T1 Table 1 Uncertainty 行; T2 Table 1 Overall survival in KEYNOTE-522 行; T3 Table 1 脚注 d 末尾追加一句。

### ESM（2,404 单元/段，变动 25，全部对应第 3 步）
Table S1 的 Location 24 格（第 19、21、22、25 项文字与 v10 相同，故不出现在差分中）+ 脚注 a。另: 开头 6 行（Online Resource 1 至 Reference numbers…，尾崎所加）的 run 字号 10 pt → 12 pt（文字不变）。
Table S1 原已按节拆成 7 个小表（Title、Abstract、Introduction、Methods、Results、Discussion、Other relevant information），版式未动，只换 Location 文字。
页码取自 Word 对 manuscript_v11_BCRT.docx 的分页（Range.Information(3)），并与 Word 导出的 PDF 逐段文字核对，0 处不符。
第 22 项（Table 1; Supplementary Table S2）未加页码: 脚注 a 定义页码为 "the page of the manuscript file"，Table 1 在 tables 文件、S2 在 ESM，manuscript 中没有可标页的段落。待用户定。

### 逐段差分（原文 → 新文）

（以下由 regress2.py 读 v10 与 v11 docx 生成）

#### manuscript

- [M 1] P unit 6: 「3,022」→「3,242」
- [M 2] P unit 11: 「2,223–3,040).」→「[2,223, 3,040]).」
- [M 3] P unit 17: 「trial,」→「trial [9],」; 「[CI] 0.55–0.94) [9].」→「(CI) [0.55, 0.94]).」; 「」→「[14]」; 「0.37–1.24) [14].」→「[0.37, 1.24]).」
- [M 3] P unit 17: 「No」→「Searches of PubMed and Europe PMC covering 2000 to 2026 identified no」; 「was identified;」→「(Supplementary Methods S1);」
- [M 4] P unit 23: 「horizon.」→「horizon, to capture differences in survival.」
- [M 4] P unit 23: 「Methods,」→「Methods S1,」
- [M 5] P unit 29: 「randomization and」→「randomization; after that,」; 「effect then」→「reduction in the hazard, 1 − HR,」; 「HR.」→「HR; patients added to the pCR group took the event-free survival of patients with pCR given the same treatment.」
- [M 6] P unit 32: 「」→「The distributions, a Weibull model for patients with pCR and a Weibull mixture cure model for patients without pCR, were chosen by the fit and plausibility criteria in Supplementary Methods S1.」
- [M 7] replace units 35-37 (3) -> 35-42 (8):
    - old: The model used 1-month cycles from the start of neoadjuvant therapy to age 100 years, with the cohort split by pCR at surgery in month 7 (Fig. 1). The survival model was built without overall survival, which served only to validate the model against acceptance criteria fixed before each comparison [5,44] (Supplementary Methods; Fig. S1; Table S3).
    - old: The model was run at recurrence HRs from 0.70 to 1.00 in steps of 0.025 and at pCR increases from 0 to 10 percentage points. Break-even HRs and the exercise effect matching pembrolizumab were found numerically. Each of 1,000 probabilistic samples paired one bootstrap replicate of the survival model with one draw of cost and utility inputs, using gamma distributions for costs and durations, beta distributions for proportions and utilities and lognormal distributions for HRs; the 2.5th and 97.5th percentiles gave the 95% uncertainty interval (UI). One-way sensitivity analyses set each input to its bounds; where a source gave no range, it was ±25% or mirrored, and drug prices varied downward only, to 75% of the list price.
    - old: Scenario analyses changed one assumption at a time (Table 1): utility values from the United States, United Kingdom and Australian analyses [28,29,65]; higher excess mortality after early recurrence with pembrolizumab, from an Italian cohort [66]; longer survival after progression during neoadjuvant therapy [67]; halved costs of metastatic treatment; eribulin-based later-line treatment [68]; and post-operative capecitabine or olaparib for patients without pCR [69–71]. The one-year net benefit used the fee-schedule-based program at recurrence HRs of 0.95, 0.90 and 0.85, applying the main comparison to patients who received neoadjuvant pembrolizumab in the 2024 national registry and the secondary comparison to the others [7]; these values are conditional on the HR. Analyses were performed in R version 4.5.1.
    - new: The model used 1-month cycles from the start of neoadjuvant therapy to age 100 years, with the cohort split by pCR at surgery in month 7 (Fig. 1).
    - new: (1) To check that the model reproduced the trial, overall survival, which was not used to build the survival model, was compared with KEYNOTE-522 against acceptance criteria fixed before each comparison [5,44] (Supplementary Methods S1; Fig. S1; Table S3).
    - new: (2) To estimate the maximum affordable cost, the model was run at recurrence HRs from 0.70 to 1.00 in steps of 0.025 and at increases in pCR from 0 to 10 percentage points in steps of 1. Break-even HRs and the exercise effect matching the QALY gain of pembrolizumab were found numerically, over HRs from 0.30 to 1.00 and increases in pCR of up to 37 percentage points.
    - new: (3) To reflect uncertainty, each of 1,000 probabilistic samples paired one bootstrap replicate of the survival model with one draw of the other inputs. Costs, durations and events per patient followed gamma distributions, proportions and utilities beta distributions, and HRs lognormal distributions; drug prices and rates based on zero events were fixed. The 2.5th and 97.5th percentiles of the samples gave the 95% uncertainty interval (UI). The probability that a program was cost-effective was the share of samples in which the maximum affordable cost exceeded the program cost. For pembrolizumab, it was the share of samples with a positive net monetary benefit at each threshold.
    - new: (4) To find the inputs that move the results most, one-way sensitivity analyses set each input to its lower and upper bounds, for the maximum affordable cost in the main comparison at an HR of 0.85 and for the ICER of pembrolizumab. Where a source gave no range, the range was ±25% of the base value or the missing bound mirrored the given one; drug prices varied downward only, to 75% of the list price.
    - new: (5) To test other assumptions, scenario analyses changed one assumption at a time (Table 1): utility values from the United States, United Kingdom and Australian analyses [28,29,65]; higher excess mortality after early recurrence with pembrolizumab, from an Italian cohort [66]; longer survival after progression during neoadjuvant therapy [67]; halved costs of metastatic treatment; eribulin-based later-line treatment [68]; and post-operative capecitabine or olaparib for patients without pCR [69–71].
    - new: (6) To express the result for Japan, the one-year net benefit used the fee-schedule-based program at recurrence HRs of 0.95, 0.90 and 0.85, applying the main comparison to patients who received neoadjuvant pembrolizumab in the 2024 national registry and the secondary comparison to the others [7]; these values are conditional on the HR.
    - new: Analyses were performed in R version 4.5.1.
- [M 8] P unit 40: 「2,223–3,040;」→「[2,223, 3,040];」; 「4,545–6,256;」→「[4,545, 6,256];」; 「238–570)」→「[238, 570])」; 「2,388–5,713;」→「[2,388, 5,713];」
- [M 9] P unit 42: 「2,881–3,785).」→「[2,881, 3,785]).」
- [M 10] P unit 46: 「2.22–2.94);」→「[2.22, 2.94]);」; 「8.15–10.36;」→「[8.15, 10.36];」
- [M 11] P unit 48: 「−330 to 8,901)」→「[−330, 8,901])」; 「0.245–4.228),」→「[0.245, 4.228]),」
- [M 12] P unit 51: 「2,201–2,994),」→「[2,201, 2,994]),」
- [M 13] P unit 60: 「evaluation.」→「evaluation of its perioperative indication.」
- [M 14] P unit 140: 「[URL to be added].」→「https://www.daiichisankyo.com/files/news/pressrelease/pdf/202609/20260916_E.pdf.」
- [M 15] P unit 150: 「[To be confirmed:」→「」; 「model」→「R」; 「is」→「of the model, its input file and the patient-level data reconstructed from published survival curves are」; 「from the corresponding author on reasonable request.]」→「at https://github.com/akehara1001/exercise-cea-tnbc.」

#### tables

- [T 1] C unit 22: 「cost and utility」→「other」
- [T 2] C unit 44: 「Methods,」→「Methods S1,」
- [T 3] P unit 116: 「」→「After the period in which the HR is held, the reduction in the hazard, 1 − HR, halves every year.」

#### ESM

- [ESM 1] C unit 42: 「」→「page」
- [ESM 2] C unit 52: 「Abstract, paragraphs 1 to 4 (pp. 1 to」→「Abstract (p.」
- [ESM 3] C unit 62: 「2」→「3」; 「3)」→「4)」
- [ESM 4] C unit 72: 「background,」→「design,」; 「4)」→「5)」
- [ESM 5] C unit 76: 「background,」→「design,」; 「1 (p. 3);」→「1;」; 「」→「(pp. 4 to 5)」
- [ESM 6] C unit 80: 「background,」→「design,」; 「3」→「4」; 「4)」→「5)」
- [ESM 7] C unit 84: 「background,」→「design,」; 「(p. 3)」→「(pp. 4 to 5)」
- [ESM 8] C unit 88: 「background,」→「design,」; 「4)」→「5)」
- [ESM 9] C unit 92: 「background,」→「design,」; 「4)」→「5)」
- [ESM 10] C unit 96: 「background,」→「design,」; 「4)」→「5)」
- [ESM 11] C unit 100: 「Outcome,」→「Outcomes,」; 「4」→「5」; 「5)」→「6)」
- [ESM 12] C unit 104: 「Variables,」→「Exercise effect and costs,」; 「4 (p. 6);」→「1;」; 「Variables,」→「Survival, costs and utilities,」; 「5 (p. 6);」→「1;」; 「」→「(pp. 6 to 7)」
- [ESM 13] C unit 108: 「Variables,」→「Survival, costs and utilities,」; 「5」→「2」; 「6)」→「7)」
- [ESM 14] C unit 112: 「Variables,」→「Exercise effect and costs,」; 「3 (p. 5);」→「2;」; 「Variables,」→「Survival, costs and utilities,」; 「5 (p. 6);」→「2;」; 「」→「(pp. 6 to 7)」
- [ESM 15] C unit 116: 「Variables,」→「Exercise effect and costs,」; 「3 (p. 5);」→「2;」; 「Variables,」→「Survival, costs and utilities,」; 「5 (p. 6)」→「2 (pp. 6 to 7)」
- [ESM 16] C unit 120: 「」→「Methods, Study design, paragraph 1;」; 「paragraphs 1 to 2 (p. 6);」→「paragraph 1;」; 「S1」→「S1; Statements and Declarations, Data availability (pp. 4 to 26)」
- [ESM 17] C unit 124: 「」→「Methods, Exercise effect and costs, paragraph 1; Methods, Survival, costs and utilities, paragraph 1;」; 「paragraphs 2 to 3 (p. 6);」→「stages (1) and (2);」; 「」→「(pp. 6 to 8)」
- [ESM 18] C unit 128: 「background,」→「design,」; 「(p. 3)」→「(pp. 4 to 5)」
- [ESM 19] C unit 136: 「paragraphs 4」→「stages (3)」; 「6 (p. 7);」→「(5);」; 「」→「(p. 8)」
- [ESM 20] C unit 154: 「」→「Maximum affordable cost of exercise,」; 「10 (pp. 8」→「3; Results, Duration and metastatic treatment costs, paragraphs 1」; 「10);」→「3; Results, Pembrolizumab, paragraphs 1 to 2;」; 「3」→「3; Supplementary Tables S4 to S8 (pp. 9 to 10)」
- [ESM 21] C unit 158: 「」→「Duration and metastatic treatment costs, paragraphs 1 to 2; Results, Sensitivity and scenario analyses,」; 「11 (p. 10);」→「1;」; 「」→「Table 2;」; 「」→「(pp. 9 to 10)」
- [ESM 22] C unit 172: 「7」→「6; Discussion, Implications; Discussion, Limitations」; 「10 to 12); Limitations, paragraphs 1 to 2 (pp. 12」→「11」
- [ESM 23] C unit 182: 「Title page」→「Statements and Declarations, Funding (p. 26)」
- [ESM 24] C unit 186: 「Title page」→「Statements and Declarations, Competing interests (p. 26)」
- [ESM 25] P unit 188: 「」→「(or the numbered stage of the statistical analysis)」

## 6. 第 5 步的核对结果

### 6.1 文献（全 78 条；manuscript/code/checks_v11/refcheck.py、refcheck2.py、citemap.py）
- DOI 实测: 有 DOI 61 条，doi.org 全部解析（HTTP 302）；Crossref 元数据逐字段比对（第一作者、年、卷、首页/文章号、题名）: 不一致 0。格式层面的差 4 条，均不是书目错误: 第 10 条 Cochrane 写作 "9:CD005001"（Crossref 卷=2016、无页）；第 59、70 条题名差在 Crossref 的斜体标签与连字符；第 71、76 条在印（Crossref 无卷页）。
- 作者列表逐名比对（前 6 名）: 第 9 条撇号字形（' 对 ’）；第 28 条第 2 作者写作 "A Fasching P"——Crossref（family "A. Fasching"）与 PubMed（PMID 36648737，"A Fasching P"）都是这样登记，文献表与两处记录一致，实名为 Peter A. Fasching，按惯例可写 "Fasching PA"（只报告）。
- 撤稿与更正: 61 条中 retraction / expression of concern 标记 0。第 2 条 updated-by "new_edition"（JCO 2023 年重刊，10.1200/jco.22.02572），第 10 条 update-to "new_version"（本版取代旧版 Cochrane 综述），均非撤稿。
- 无 DOI 17 条: 16 条网址可访问（第 65 条 301 跳转到 https://www.pbs.gov.au/industry/listing/elements/pbac-meetings/psd/2023-03/pembrolizumab-earlyTNBC-keytruda-PSD-March-2023）；页面标题或 PDF 首页与文献表题名一致（第 51 条页面为 Shift_JIS，标题乱码但即令和 7 年简易生命表概况；第 72 条本轮一次 403、首轮 200）。第 52 条图书经 Minds 与国立国会図書館登录确认（日本癌治療学会、金原出版、2023 年 10 月、第 3 版）。
- 文献 73（1k）: 打开 PDF 确认标题 "Enhertu® and Datroway® Approved in Japan for Two New First-Line Indications for Patients with Metastatic Breast Cancer"，日期 "Tokyo – (September 16, 2026)"。
- 尾崎重编号的核对: v9 文献表与 v10 按 DOI/URL 对应（76 条对上；v9 第 69 条止吐指南 = v10 第 52 条；v10 第 73 条为新增）。把 v9 的引用按此映射后与 v10 逐个比较: ESM 126 组中 124 组一致，余 2 处是 [73,66]→[56,76] 的升序重排与 [8,72–75] 加入新文献 73；tables 24 组中 23 组一致，余 1 处同为 [8,72–75]；正文 5 处差异全部来自尾崎的句子改写（合并句、新增 [52–60] 与 [48] 等），引用指向的文献不变。v11 的 ESM 与 tables 引用序列与 v10 完全相同。
- 初出顺: 正文（Introduction 至 Conclusion，55 段）取出引用号 110 个（范围展开后），去重 71 个，初出顺 = 1, 2, …, 71，无缺号。文献 72〜78 只在 Table 1 与 ESM 中出现，正文 0 次；图注只引 [9]。78 条全部至少被引用一次，未被引用 0、表外编号 0。72〜78 按用户决定不重排（见第 2 节偏离 4）。
- ARS citation-check（academic-paper citation-check 模式，citation_compliance_agent 的清单；按规约 1.4 与指示不做自动更正）:
  | 项目 | 结果 |
  |---|---|
  | 核对的文献条目 | 78（DOI 61 + 无 DOI 17） |
  | 正文引用组 / 号（展开后） | 61 组 / 110 号（另: Table 1 24 组、ESM 126 组、图注 1 组） |
  | 孤立的正文引用 / 孤立的文献 | 0 / 0 |
  | 缺 DOI（有 DOI 而未写） | 0 |
  | DOI 格式（https://doi.org/、末尾无句点） | 61/61 合格 |
  | 订正 | 0 |
  | 未解决（书目与来源不符） | 0 |
  | 待人工确认的格式项 | 4: 第 10 条 Cochrane 卷号写法；第 28 条作者名按来源登记；第 58 条 "evidence?." 的问号后句点；第 65 条网址已迁移（301） |
  | 发表超过 10 年（2015 年及以前） | 8 条（n.d. 1 条另计）；2021〜2026 年 56/78 |
  | 自引 | 著者未填，文献作者中无 Ozaki / Hara: 0 |
  | 题名大小写 | 照原刊（Title Case 与 sentence case 混在），Springer 基本格式允许，未改 |

### 6.2 表与图编号（规约第 7.1 节第 9 条；checks_v11/tfnum.py）
扫描正文 55 段（Introduction 至 Conclusion，不含标题），取出提及 43 个（范围与列举已展开）。
- Table: 初出 [1, 2, 3]，最大 3 = tables 文件中的表 3 个。
- Fig.: 初出 [1, 2, 3]，最大 3 = Fig1〜3.tif 3 个 = Figure captions 3 条。
- Table S: 初出 [1, …, 10]（Study design 第 3 段 "Tables S1–S10" 一次全部初出），最大 10 = ESM 补充表 10 个，ESM 内物理顺序 S1〜S10。
- Fig. S: 初出 [1, 2]，最大 2 = ESM 补充图 2 个，顺序 S1、S2。
- 每个编号的初出都在正文地の文。Supplementary Methods S1: 正文 4 处（Introduction 第 3 段为初出），不带 S1 0 处。
- 检查器用植入违反的文本鸣过一次（Table 2 先于 Table 1、Tables S3–S4 先于 S1 → 报 False；引用 [1][3–4][2] → 报 False）。

### 6.3 数值
除 Word count 一行外，抄录、正文、表、ESM 的结果数值与 v10 完全一致；新增的数字记号全部来自指示原文或 Table S1 的页码（见第 4 节）。来源文件 57 个 sha256 未变。替代性核对（第 4 步停下，未在公开目录重跑）: 现有输出 output/phase2/main/det_caps.csv（sha256 0f63eeec…，000a3b7）HR 0.85 主比较 2,726,400.9 日元、次比较 3,442,898.8 日元；det_reference.csv（4b431ed1…）ICER 2,052,755.1 日元/QALY → 2,726 / 3,443 / 2,053（千日元），与 v11 一致。

### 6.4 退行
manuscript 15 块、tables 3 块、ESM 25 块，全部对应指示（第 5 节）；无法对应的变动 0。名指确认: 题名（manuscript P0 与 ESM 第 2 行，v10 与 v11 相同）；责任著者占位行（尾崎，未动）；补充表脚注（ESM 中只改 Table S1 脚注 a，其余逐字相同）；表脚注（只追加 Table 1 脚注 d，按指示）；语数（按 1m 改为实测）；图的解像度（600 dpi，见第 6.6 节）。

### 6.5 格式（规约第 8 节；checks_v11/fmt_audit.py）
v10 底本的检查结果与修正:
| 项目 | v10 | 处理 | v11 |
|---|---|---|---|
| Heading 样式 | 0（158 段全 Normal） | — | 0（163 段全 Normal） |
| 字号 | manuscript 169 run 10 pt、题名 14 pt；docDefaults 10 pt；页脚 10 pt；ESM 开头 6 行 10 pt；tables 全 12 pt | 全部改 12 pt（文字不变） | manuscript 175/175、tables 349/349、ESM 2,551/2,551 为 12 pt |
| 字体 | 全部 Times New Roman | — | 同 |
| 颜色 | 全部自动色 | — | 同（未使用的 Heading 样式定义带色，未被引用） |
| 行号 | 有（lnNumType countBy=1，无 start） | — | 有 |
| 双倍行距 | 非空 155 段 line=480 | — | 非空 160 段 line=480（新段落继承） |
| 句中粗体 | 0 | — | 0。粗体 26 run = 题名 1、大标题 10、抄录标签 5（含 Keywords）、Statements 标签 7、图注标签 "Fig. 1〜3" 3；后两类是 BCRT 的段首标签，规约第 8 节字面不在允许之列，作为投稿先格式保留 |
| 表 | 横版、单倍行距、列头与数值无粗体 | 不动 | 同 |
二级标题为斜体非粗体: 归入第 2 节偏离 1，不改。

### 6.6 图
Fig1.tif 4,015 × 2,173 px，600 × 600 dpi（170.0 × 92.0 mm）；Fig2.tif 4,015 × 2,456 px，600 dpi（170.0 × 104.0 mm）；Fig3.tif 4,015 × 3,023 px，600 dpi（170.0 × 128.0 mm）。RGBA、LZW。与 v9 逐字节相同。

### 6.7 ESM_1_v11.pdf
Word（SaveAs2, 17）导出，46 页，逐页看过。与同一 Word 导出的 v10（45 页）相比，多出的 1 页来自 Table S1: Location 变长后表格占满第 8 页，脚注 a 单独落在第 9 页。版式按指示未动，留待用户决定。另有两处 v10 已有的分页: Table S3 的 "D. Model extrapolation" 表头在第 26 页底、表身在第 27 页；Table S10 的脚注单独在第 46 页。尾崎的 ESM_1.pdf（48 页，19:25）早于 ESM_1.docx（20:56），分页不同，未作逐页比较。

## 7. 著者侧与用户待定的事项

1. 第 4 步（公开用代码）在开始前停下: input/params/parameters_v10.xlsx 含人名（"尾崎" 81 格、"原" 80 格且工作表名为「計算根拠_原」、"先生" 35 格；邮箱 0；文件属性 creator 有值）。未建 exercise_cea_public\、未复制任何文件、未 git init。另外 Data availability（1l）写明公开 "its input file"，与规约第 9 节"公开范围与仓库一致、不得出现可识别个人的信息"相关，需在公开前决定输入表的去名方式。
2. ESM Table S1 第 22 项未加页码（理由见第 5 节）。
3. ESM 第 9 页只有 Table S1 的脚注 a（第 6.7 节）。
4. 文献格式待确认 4 项（第 6.1 节表）。
5. 抄录内 "JPY" 未定义（ARS check_acronyms 对抄录报 Not defined；v9 以来的既有事项，本版未改）。
6. 正文的 check_acronyms 为 partial: JPY、TNBC、QALY、ICER 未被检查器识别（正文均有定义）；报 "PMC"（1b 的 "Europe PMC"，数据库名）、CHEERS 与 EQ（定义带 "2022" 与 "-5D-5L" 后缀）。
7. 第 10 节计数（只报告，本版不改）: 禁用语 0、开场套话 0、元评论 0、破折号 — 0、中黑「・」0（Keywords 分隔符 "·" U+00B7 5 处，BCRT 格式）；超过 30 词的句子 43（v10 37；新增来自 1b、1e、1f、1g 的指示原文），最长 76 词（Outcomes 第 2 段，v10 既有）；超过 150 词的段落 3（v10 2；新增 Exercise effect and costs 第 1 段 166 词，因 1e）；裸时间词 currently 1（Implications）、now 1（Discussion 第 4 段）、current 1（Limitations），均为 v10 既有。
8. 目的对应（规约第 2.1 节）: Statistical analysis 的 (1) 验证与 (6) 一年净收益不对应单一目的编号（v10 已有同样内容，本版只加编号）；Discussion 第 1 段回答目的 1 与 3，目的 2 与 4 在第 4 段回答（v10 既有）。

## 8. 撤回的主张

本版无撤回。退行对照中没有任何此前删除的内容复活。

## 9. 共著者コメント台帳

v10（尾崎）为干净的 docx: 修订 0、批注 0。本版的采否即用户的指示 1a〜3。

## 10. 过去意外退回的地方

规约第 1.2 节第 7 条名指的五处（责任著者占位、补充表脚注、题名、语数、图解像度）本版逐一确认，无退回（第 6.4 节）。本项目未记录过其他退回位置。

## 11. 文献检索的记录

ESM Supplementary Methods S1 "Literature searches": 2026-10-26，PubMed（题名摘要词与 MeSH）与 Europe PMC（题名摘要词），各限 2000〜2026 年，三组检索式原文在 ESM。1b 的新规性句 "Searches of PubMed and Europe PMC covering 2000 to 2026 identified no economic evaluation …" 与此一致，并引用 Supplementary Methods S1；未用 "the first" 型绝对说法。

## AUDIT（规约第 13 节，交付前再读规约后逐项一行）

最重要四项（先报告）:
1. 版: 通过。底本 = 尾崎 2026-10-28 交付的 v10（sha256 前 16 位四件一致）；交付后 manuscript/ 下只有 v11（v10 → archive/v10、v9 → archive/v9）。
2. 表与图: 通过。四系列全部在正文地の文以编号引用（55 段、43 个提及）；Supplementary Methods S1 与 CHEERS 清单（Table S1）由正文引用。
3. 文献的真伪: 通过。DOI 61/61 解析、书目一致；无 DOI 17 条按网页/出版社确认。
4. 文献的顺序: 通过。正文 1〜71 初出顺无缺（110 个号）；72〜78 只在 Table 1 与 ESM（用户决定不重排）。

版
- [x] 作业树只有最新版: manuscript/ 下 v11、code、archive、_inbox（空）。archive 在项目根内（manuscript/archive，按用户指定；规约要求根外，沿用项目惯例）。code/ 有 v1 时代的生成脚本（make_*.py 等），本版未运行。
- [x] 会话开始时 sha256: v10 无 MANIFEST，按指示的 sha256 前 16 位核对，一致。
- [x] 底本 = v(n−1)，worklog 开头写了底本与 sha256。
- [x] 意外退回 0（第 6.4 节，五处名指）。
- [x] 数值与 v10 一致（Word count 除外；第 6.3 节）。
- [—] 模板占位（[name] 等）: 题名页与 Statements 的占位是尾崎的（第 14 节），不动、不报告。
- [x] 交付物无版本标签与作业注记（版本号只在文件名）。
- [x] MANIFEST 更新、v10 移入 archive（交付时）。
- [x] 解析输出 57 个 sha256 与 v9 台帐一致。
- [x] 差分全部对应指示（43 块）；格式修正对应第 5 步。
- [x] 撤回主张复活 0。
- [x] 修订与批注 0（Word COM 读三份 docx）。
- [x] 作业树无 ars/（ars_v5〜v9 在 archive）。

文献与编号
- [x] 初出顺 1〜71 无缺；未引用 0、表外号 0。
- [x] DOI 61/61 解析、书目一致；解析失败 0。
- [x] 新引用: 无（[9]、[14] 只移位置；文献 73 补 URL 并核对标题与日期）。
- [x] ARS citation-check: 核对 78、订正 0、未解决 0、待确认 4（第 6.1 节）。
- [x] 作者名-年份式的正文引用 0。
- [x] 超过 10 年 8 条；自引 0（报告）。
- [x] 新规性句以检索范围限定，与检索记录一致；无绝对说法。
- [x] 四系列初出顺 1..n。
- [x] 各系列最大号 = 实物数。
- [x] 每个表与图在正文地の文至少一次。
- [x] ESM 内顺序为编号顺。
- [x] Supplementary Methods S1 与报告规范清单由正文引用。
- [x] Fig1〜3.tif 已附，Fig. 1 起依次在正文提及。

标题与格式
- [偏离] 大标题: BCRT 结构（Introduction、Methods、Results、Discussion、Conclusion 等），投稿先与共著者决定（第 2 节）。
- [x] 规约外的节与项目: v10 与 v11 相同（Abstract/Keywords、Conclusion、Acknowledgments、References、Statements and Declarations 的 7 项、Figure captions），未增未减。
- [偏离] Methods 小标题: 5 个（第 2 节）。
- [x] Heading 样式 0。
- [x] 全部 run 12 pt Times New Roman（修正后；第 6.5 节）。
- [x] 行号有。
- [x] 双倍行距（非空 160 段）。
- [x] 句中粗体 0（段首标签另述，第 6.5 节）。
- [x] 表的列头与数值无粗体（tables 粗体 13 run 全是面板与分组标签）。
- [x] 非黑字 0。
- [x] 中黒「・」0。
- [x] 表页为横版。
- [偏离] 表脚注记号 a〜d（非 ✳）；"Note" 开头 0。
- [x] 脚注记号与表内上标一一对应: Table 1〜3 各 a（题名）+ b、c、d（表内）。
- [x] 图 600 dpi，实测见第 6.6 节。
- [x] 前付一项一段（尾崎）。
- [x] 生成 AI 记述 0（manuscript 163 段、tables 326、ESM 2,509、cover letter 16 单元扫描）。
- [x] ARS 作业标记 0（同上）。
- [x] ARS 默认来源的结构 0（Conclusion 为 v10 已有，按第 1.2 节规则 10 保留）。
- [x] 美式拼写统一（英式只在文献原题与 CHEERS 清单原文）；只用 "Fig."。
- [x] 语数按节实测、写入题名页、在上限内（250 ≤ 250；3,242 ≤ 3,500）。

数值
- [x] 正文与抄录数值无新增结果数值，来源台帐沿用 v9 第 8 节（57 文件未变）。
- [x] 表脚注数值未变（Table 1 脚注 d 的新句不含结果数值，"1 − HR" 是式）。
- [x] 同一数值两表重复: 未改动（v10 既有的 Table 2 B/C 首行为 v2 起的有意例外 E1）。
- [—] n 的合计、流程图: 本研究为模型研究，无选择流程；未改动。
- [—] 对象者数: 不适用（模型队列）。
- [x] 点估计在 UI 内（未改动数值）。
- [x] 同一统计量各处同值同位（未改动）。
- [—] p 值: 无。
- [x] 因果词 caused / led to / impact 0。
- [x] 负号为 −（U+2212），新文 "1 − HR"、"[−330, 8,901]" 亦同。
- [x] 小数位与百分比舍入未改动。

内容
- [x] Methods 无数值结果（新增 8 段为设定与检索范围）。
- [x] Results 无"使用了"型（未改动段落）。
- [x] 结果句有表或图的参照（未改动）。
- [x] 每个解析段有目的句: 新 (1)〜(6) 均以 "To …" 开头。
- [x] Introduction 末两段的形（v10 既有，未改）。
- [注] 目的对应表: (1) 与 (6) 不对应单一目的编号（第 7 节第 8 项）。
- [x] 曝露与结局名称与目的一致（未改）；段落顺序 (2) 目的 1/2/4 → (3)〜(5) 不确定性 → (6) 日本的一年净收益。
- [x] 抄录的目的与结论与本文对应（未改）。
- [x] Results 段落顺序与开头名指（未改）。
- [x] Discussion 段首名指（未改）。
- [注] Discussion 第 1 段只直接回答目的 1 与 3（v10 既有）。
- [x] Discussion 与 Results 的重复（未改）。
- [x] Discussion 引用集中在中段（未改）。
- [x] "further research is needed" 型 0。
- [x] 临床医会改变什么的句子（Implications 第 1 句，未改）。
- [x] Implications 无新数值；1h 是限定范围的补充，主张未变强。
- [注] 用语与略语: check_acronyms partial（第 7 节第 5、6 项）。
- [x] 限界只在 Limitations（未改）。
- [x] Outcome/Variables 第一句（BCRT 的 Outcomes 与 Exercise effect and costs 第一句，未改）。
- [x] 统计软件只写语言与版本（"Analyses were performed in R version 4.5.1."）。
- [注] Data availability 只在 manuscript；内容与公开仓库的一致性取决于第 4 步（停）。
- [x] CHEERS 清单在 ESM，28 项中 24 项有节、段与页（19、21、25 按指示不加；22 待定）。
- [x] 题名 manuscript 与 ESM 一致。
- [x] 事前计划与未登记的一句在 Study design 第 3 段（未改）；缺失与多重比较对模型研究不适用。
- [—] 选择流程图: 不适用。
- [x] 图未改动（v9 交付时的检查: 无图内题名、面板标签、单位、线型区分、≥ 8 pt）。
- [x] 图表重复未改动。
- [—] 著者贡献: 尾崎的占位（第 14 节）。
- [x] AI 常套语 0；破折号 0；30 词超句 43、最长 76；150 词超段 3（报告）。
- [注] 裸时间词 3 处（v10 既有）。
- [x] 主张未变强（1c 加理由、1h 缩小范围、1e/1f/1g 为方法描述）。
- [—] 查读回复版: 不适用。
- [—] humanizer / stop-slop: 本版未用。
