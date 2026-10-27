# v6 与 v7 的逐段对照

由 `manuscript/code/compare_versions.py` 生成。v6 = `manuscript/archive/v6/`，v7 = `manuscript/v7/`。表外的每个段落与表内的每个单元格各为一项，按文档顺序用 difflib 对齐；列出全部不相同的块（两侧原文）。

## tables_v6.docx → tables_v7.docx

项数：v6 287，v7 287；相同 287；不同的块 0。

### tables：归一化比较（v6 的补充表编号换成 v7 的编号、两版都去掉文献号）

不同的块 0（原始比较 0）。

| 块 | 类型 | v6 项数 | v7 项数 | v6 首项 | v7 首项 |
|---|---|---|---|---|---|

嵌入图片（word/media）：v6 0 个、v7 0 个；sha256 相同的 0 个。

## figures_v6.docx → figures_v7.docx

项数：v6 9，v7 9；相同 9；不同的块 0。

### figures：归一化比较（v6 的补充表编号换成 v7 的编号、两版都去掉文献号）

不同的块 0（原始比较 0）。

| 块 | 类型 | v6 项数 | v7 项数 | v6 首项 | v7 首项 |
|---|---|---|---|---|---|

嵌入图片（word/media）：v6 3 个、v7 3 个；sha256 相同的 3 个。

## supplement_v6.docx → supplement_v7.docx

项数：v6 2360，v7 2360；相同 2357；不同的块 3。

### supplement 块 1（改）
- v6［table 5 row 4 cell 4］Results, paragraphs 1 to 9 (pp. 7 to 9); Fig. 2; Tables 2 and 3
- v7［table 5 row 4 cell 4］Results, paragraphs 1 to 10 (pp. 7 to 9); Fig. 2; Tables 2 and 3

### supplement 块 2（改）
- v6［table 5 row 5 cell 4］Results, paragraph 10 (p. 9); Fig. 3; Supplementary Tables S4, S7, S9 and S10; Supplementary Fig. S2
- v7［table 5 row 5 cell 4］Results, paragraph 11 (p. 9); Fig. 3; Supplementary Tables S4, S7, S9 and S10; Supplementary Fig. S2

### supplement 块 3（改）
- v6［table 6 row 3 cell 4］Discussion, paragraphs 1 to 7 (pp. 9 to 11); Limitations, paragraph 1 (p. 12)
- v7［table 6 row 3 cell 4］Discussion, paragraphs 1 to 7 (pp. 9 to 11); Limitations, paragraphs 1 to 2 (pp. 11 to 12)

### supplement：归一化比较（v6 的补充表编号换成 v7 的编号、两版都去掉文献号）

不同的块 3（原始比较 3）。

| 块 | 类型 | v6 项数 | v7 项数 | v6 首项 | v7 首项 |
|---|---|---|---|---|---|
| N1 | replace | 1 | 1 | Results, paragraphs 1 to 9 (pp. 7 to 9); Fig. 2; Tables 2 and 3 | Results, paragraphs 1 to 10 (pp. 7 to 9); Fig. 2; Tables 2 and 3 |
| N2 | replace | 1 | 1 | Results, paragraph 10 (p. 9); Fig. 3; Supplementary Tables S4, S7, S9 and S10; Supplementa | Results, paragraph 11 (p. 9); Fig. 3; Supplementary Tables S4, S7, S9 and S10; Supplementa |
| N3 | replace | 1 | 1 | Discussion, paragraphs 1 to 7 (pp. 9 to 11); Limitations, paragraph 1 (p. 12) | Discussion, paragraphs 1 to 7 (pp. 9 to 11); Limitations, paragraphs 1 to 2 (pp. 11 to 12) |

嵌入图片（word/media）：v6 2 个、v7 2 个；sha256 相同的 2 个。

## manuscript_v6.docx → manuscript_v7.docx

项数：v6 129，v7 132；相同 119；不同的块 4。

### manuscript 块 1（改）
- v6［paragraph］Fig. 2a shows that the maximum affordable cost of an exercise program per patient rose as the recurrence HR with exercise fell. At an HR of 0.85, exercise added to chemotherapy plus pembrolizumab had a maximum affordable cost of JPY 2,726 thousand per patient (95% UI [2,223, 3,040]; Table 2). At an HR of 0.70, it was JPY 5,596 thousand (95% UI [4,545, 6,256]; Supplementary Table S4). Table 2 (panel A) shows that the maximum affordable cost equaled the fee-schedule-based program cost at an HR of 0.989, a 1.1% reduction in the recurrence hazard. Medical costs avoided by exercise equaled the same program cost at an HR of 0.958, a 4.2% reduction (Table 2). Through an effect on pCR instead, an increase of 1 percentage point gave a maximum affordable cost of JPY 389 thousand (95% UI [238, 570]). An increase of 10 percentage points gave JPY 3,898 thousand (95% UI [2,388, 5,713]; Supplementary Table S5).
- v7［paragraph］Fig. 2a shows that the maximum affordable cost of an exercise program per patient rose as the recurrence HR with exercise fell. At an HR of 0.85, exercise added to chemotherapy plus pembrolizumab had a maximum affordable cost of JPY 2,726 thousand per patient (95% UI [2,223, 3,040]; Table 2). At an HR of 0.70, it was JPY 5,596 thousand (95% UI [4,545, 6,256]; Supplementary Table S4). Table 2 (panel A) shows that the maximum affordable cost equaled the fee-schedule-based program cost at an HR of 0.989, a 1.1% reduction in the recurrence hazard. Medical costs avoided by exercise equaled the same program cost at an HR of 0.958, a 4.2% reduction (Table 2).
- v7［paragraph］Supplementary Table S5 shows the maximum affordable cost when exercise acted through pCR instead of the recurrence HR. An increase of 1 percentage point in pCR gave JPY 389 thousand (95% UI [238, 570]), and an increase of 10 percentage points gave JPY 3,898 thousand (95% UI [2,388, 5,713]).

### manuscript 块 2（改）
- v6［paragraph］The value of adding a structured exercise program to neoadjuvant chemotherapy for stage II or III TNBC in Japan depends on how much and for how long the program lowers the risk of recurrence. With chemotherapy plus pembrolizumab, a program could cost up to JPY 2,726 thousand per patient at a recurrence HR of 0.85 and remain cost-effective (Table 2). The most expensive design costed in this study was JPY 239,508 (Table 1). A reduction of 1.1% in the recurrence hazard was enough for the fee-schedule-based program to be cost-effective, and a reduction of 4.2% to 8.6% was enough for it to lower total medical costs (Table 2). For patients in Japan, what remains unknown is whether exercise lowers recurrence at all, and for how long.
- v6［paragraph］Most of this value comes from distant recurrences that the program would prevent. Treatment after distant recurrence in Japan now costs JPY 1,215,933 to 1,458,318 per month in first-line treatment and JPY 1,412,953 per month in later lines (Table 1). Medical costs avoided made up JPY 702 thousand of the maximum affordable cost at an HR of 0.85 (Supplementary Table S6). Lower metastatic treatment costs reduced these savings but left the threshold for cost-effectiveness almost unchanged. With these costs halved, or with eribulin-based later-line treatment, the break-even HR was 0.988 and 0.987, while the HR at which exercise lowered total costs fell to 0.918 and 0.914 (Table 2).
- v6［paragraph］How long the effect lasts changed the result more than any single cost. If the effect faded from 1 year after surgery, the maximum affordable cost at an HR of 0.85 fell to JPY 1,772 thousand, and if it did not wane, it rose to JPY 3,404 thousand (Table 2). In the one-way analyses, no input moved this cost outside JPY 2,617 thousand to 2,836 thousand (Fig. 3). After neoadjuvant chemo-immunotherapy, most recurrences occur within 24 months of randomization6, so an effect that lasts through the first years after surgery carries most of the value. Continuing exercise after surgery raised the maximum affordable cost when the effect would otherwise have faded early (Supplementary Table S7).
- v6［paragraph］For pembrolizumab, the ICER of JPY 2,053 thousand per QALY lay below both Japanese thresholds (Table 3). Analyses of the same regimen from the United States, Hong Kong, Switzerland and Egypt28–31 found it cost-effective, with ICERs below the threshold used in each setting. In Japan, the regimen has not been designated for cost-effectiveness evaluation39. Its ICER rose to JPY 3,044 thousand per QALY when capecitabine or olaparib was added after surgery for patients without pCR, as in Japanese practice, and fell to JPY 1,296 thousand at 75% of the list price of pembrolizumab (Table 3; Supplementary Fig. S2).
- v6［paragraph］Exercise cannot stand in for pembrolizumab. To gain as many QALYs as pembrolizumab, exercise added to chemotherapy alone would need a recurrence HR of 0.425 (Table 3), a far larger effect than has been reported for exercise in other settings9,14. The maximum affordable cost was higher when exercise was added to chemotherapy alone (Table 2), because more recurrences remain for exercise to prevent without pembrolizumab. Exercise is therefore best judged as an addition to the standard regimen, which in Japan was given to 2,294 of 3,451 patients in 20247.
- v6［paragraph］Previous economic evaluations of exercise in cancer valued effects on fatigue, fitness or quality of life during or shortly after treatment20–22. The cost-utility analysis of CHALLENGE valued an effect on disease-free survival over the long term46. The structured exercise program was less costly and more effective than health education materials, and cancer recurrence or new malignancy and anticancer therapy were the major cost drivers46. Our results agree with it on the main point: once a program changes the risk of recurrence, its value reflects the cost and the loss of health that each prevented recurrence avoids, and both are large relative to the cost of the program. Headroom analysis is used to judge technologies before their effect is known27. Here it shows that an effect far smaller than a trial could detect would still pay for the program.
- v6［paragraph］In Japanese practice, the value of a given effect may be larger than modeled. In the 2024 national registry, 47% of patients treated with neoadjuvant chemotherapy had a pCR7, fewer than in either arm of KEYNOTE-522 (63.0% and 55.6%; Table 1). More patients therefore carry residual disease and the higher risk of recurrence on which exercise would act. Even at an HR of 0.95, the net benefit for one year of Japanese patients would be JPY 2.68 billion (Supplementary Table S8).
- v7［paragraph］In Japan, adding a structured exercise program to neoadjuvant chemotherapy for stage II or III TNBC would be cost-effective even if it lowered the risk of recurrence only slightly. With chemotherapy plus pembrolizumab, the fee-schedule-based program became cost-effective once it lowered the recurrence hazard by 1.1% (Table 2). How much a program could cost depended mostly on how large its effect was and how long it lasted. Pembrolizumab itself was cost-effective at both Japanese thresholds (Table 3).
- v7［paragraph］Most of the value of exercise came from the distant recurrences it would prevent. In Japan, one month of treatment after distant recurrence costs more than the whole exercise program (Table 1). The medical costs avoided alone paid for the program once the recurrence hazard fell by 4.2% to 8.6%, depending on the cost of metastatic treatment (Table 2). Cheaper metastatic treatment reduced these savings but barely moved the point at which the program became cost-effective (Table 2).
- v7［paragraph］Duration changed the maximum affordable cost more than any cost input did (Table 2; Fig. 3). Most recurrences after neoadjuvant chemo-immunotherapy occur within 24 months of randomization6. An effect that holds through the first years after surgery therefore captures most of the value. When the effect of the neoadjuvant program alone would fade early, continuing exercise after surgery raised the maximum affordable cost (Supplementary Table S7).
- v7［paragraph］Exercise cannot replace pembrolizumab. To gain as many QALYs as pembrolizumab, exercise added to chemotherapy alone would need to lower the recurrence hazard by more than half (Table 3). Trials of exercise in cancer have reported much smaller effects9,14. The maximum affordable cost was higher without pembrolizumab, because more patients relapse and the same relative effect prevents more recurrences (Table 2). In 2024, 2,294 of 3,451 patients in Japan who received neoadjuvant chemotherapy for stage II or III TNBC also received pembrolizumab7. The main comparison therefore reflects most current practice.
- v7［paragraph］Pembrolizumab added to neoadjuvant chemotherapy was cost-effective in Japan, as in analyses from the United States, Hong Kong, Switzerland and Egypt28–31. Its cost-effectiveness depended most on its price and on whether capecitabine or olaparib was added after surgery, as in Japanese practice (Table 3; Supplementary Fig. S2). The regimen has not been designated for Japan's cost-effectiveness evaluation39, and our estimate gives a reference in the meantime.
- v7［paragraph］Earlier economic evaluations of exercise in cancer valued effects on fatigue, fitness or quality of life during or shortly after treatment20–22, and their conclusions varied23–25. The cost-utility analysis of CHALLENGE valued an effect on disease-free survival over 5 years46. The program cost less and gave more health than health education, and recurrence, new cancers and their treatment drove the costs46. Our results point the same way. Each recurrence prevented avoids months of costly treatment and years of lost health, which together outweigh the cost of an exercise program.
- v7［paragraph］In Japanese practice, a given effect of exercise may be worth more than the model suggests. In the 2024 national registry, 47% of patients treated with neoadjuvant chemotherapy had a pCR7, fewer than in either arm of KEYNOTE-522 (Table 1). More patients therefore have residual disease, a higher risk of recurrence and more recurrences for exercise to prevent.

### manuscript 块 3（改）
- v6［paragraph］Trials of exercise during neoadjuvant chemotherapy for TNBC should measure recurrence and follow patients long enough to show whether any effect persists after the program ends. A higher pCR would help but cannot settle the question alone. In this model, 1 percentage point more pCR was worth JPY 389 thousand per patient (Supplementary Table S5), but how a change in pCR caused by exercise would translate into fewer recurrences is unknown. Given the net benefit at stake for each year of patients in Japan (Supplementary Table S8), such trials are a sound use of research funds. For payers, the fee-schedule price of a supervised program is far below what a confirmed effect would justify, and support that keeps patients exercising after surgery, such as remote or app-based programs, would add value if it extends the effect (Supplementary Table S7). For pembrolizumab, the analysis provides a Japanese estimate for a regimen that has not been designated for cost-effectiveness evaluation.
- v7［paragraph］Clinicians already have reasons to offer exercise during chemotherapy, because trials have shown better fitness and, in some, less fatigue10–13. This analysis adds that an effect on recurrence, if present, would carry large economic value. Trials of exercise during neoadjuvant chemotherapy should record recurrence and follow patients long enough to see whether the effect lasts after the program ends. A higher pCR alone cannot settle the question, because it is unknown how a change in pCR with exercise would translate into fewer recurrences (Supplementary Table S5). Funders can weigh the cost of such trials against the net benefit for one year of Japanese patients if an effect is confirmed (Supplementary Table S8).
- v7［paragraph］For payers, the price of a supervised program is far below what a confirmed effect would justify (Table 2). Support that keeps patients exercising after surgery, such as remote programs, would add value if it extends the effect (Supplementary Table S7). For pembrolizumab, this analysis gives Japan a reference value before any formal cost-effectiveness evaluation.

### manuscript 块 4（改）
- v6［paragraph］The effect of exercise during neoadjuvant chemotherapy on recurrence is unknown, so all results for exercise are conditional on an assumed HR and duration of effect. The CHALLENGE estimate used as a reference comes from a 3-year program after adjuvant chemotherapy for colon cancer. The model credited exercise only with fewer recurrences after surgery; effects on fatigue, quality of life or completion of chemotherapy were not counted, so the maximum affordable cost may be understated. Survival was modeled from patient-level data reconstructed from published curves, and the 7-year event-free survival by pCR status came from the presentation of the final analysis rather than a full report. Survival after distant recurrence came from a French cohort treated largely before immunotherapy and antibody–drug conjugates were available, whereas treatment costs reflect regimens used in 2026. Several costs relied on clinical expert input, and ranges were set by rule where sources gave none (Fig. 3). Utilities used the German value set; values from Japanese populations gave similar results (Supplementary Table S10). The number of eligible patients came from a registry that does not capture every case.
- v7［paragraph］The effect of exercise during neoadjuvant chemotherapy on recurrence is unknown, so all results for exercise are conditional on the assumed HR and duration. The CHALLENGE estimate shown for reference comes from a 3-year program after adjuvant chemotherapy for colon cancer and may not apply to breast cancer. The model credited exercise only with fewer recurrences after surgery. Effects on fatigue, quality of life or completion of chemotherapy were not counted, so the maximum affordable cost is likely understated. Survival was modeled from data reconstructed from published curves, and the 7-year event-free survival by pCR status came from the presentation of the final analysis. Errors in these inputs would change the baseline risk of recurrence and, with it, the value of a given effect.
- v7［paragraph］Survival after distant recurrence came from a French cohort diagnosed in 2008 to 2020, largely before immunotherapy and antibody–drug conjugates50. Longer survival with current treatment would raise the costs avoided by each prevented recurrence but lower the QALYs gained, with opposite effects on the maximum affordable cost. Several costs relied on clinical expert input, and ranges were set by rule where sources gave none, but no single cost changed the conclusion (Fig. 3). Utilities came from the German value set, and values from Japanese populations gave nearly the same results (Supplementary Table S10). The registry does not capture every case, so the one-year net benefit is likely understated.

### manuscript：归一化比较（v6 的补充表编号换成 v7 的编号、两版都去掉文献号）

不同的块 4（原始比较 4）。

| 块 | 类型 | v6 项数 | v7 项数 | v6 首项 | v7 首项 |
|---|---|---|---|---|---|
| N1 | replace | 1 | 2 | Fig. 2a shows that the maximum affordable cost of an exercise program per patient rose as  | Fig. 2a shows that the maximum affordable cost of an exercise program per patient rose as  |
| N2 | replace | 7 | 7 | The value of adding a structured exercise program to neoadjuvant chemotherapy for stage II | In Japan, adding a structured exercise program to neoadjuvant chemotherapy for stage II or |
| N3 | replace | 1 | 2 | Trials of exercise during neoadjuvant chemotherapy for TNBC should measure recurrence and  | Clinicians already have reasons to offer exercise during chemotherapy, because trials have |
| N4 | replace | 1 | 2 | The effect of exercise during neoadjuvant chemotherapy on recurrence is unknown, so all re | The effect of exercise during neoadjuvant chemotherapy on recurrence is unknown, so all re |

嵌入图片（word/media）：v6 0 个、v7 0 个；sha256 相同的 0 个。

## 图文件

| 文件 | 与前版逐字节相同 | 说明 |
|---|---|---|
| figures/fig1.pdf | 否 | SVG 与 PDF 内含生成时刻（SVG 另有随机的 clip-path 编号）；绘图内容以 PNG/TIFF 逐字节比较为准 |
| figures/fig1.png | 是 |  |
| figures/fig1.svg | 否 | SVG 与 PDF 内含生成时刻（SVG 另有随机的 clip-path 编号）；绘图内容以 PNG/TIFF 逐字节比较为准 |
| figures/fig1.tiff | 是 |  |
| figures/fig2.pdf | 否 | SVG 与 PDF 内含生成时刻（SVG 另有随机的 clip-path 编号）；绘图内容以 PNG/TIFF 逐字节比较为准 |
| figures/fig2.png | 是 |  |
| figures/fig2.svg | 否 | SVG 与 PDF 内含生成时刻（SVG 另有随机的 clip-path 编号）；绘图内容以 PNG/TIFF 逐字节比较为准 |
| figures/fig2.tiff | 是 |  |
| figures/fig3.pdf | 否 | SVG 与 PDF 内含生成时刻（SVG 另有随机的 clip-path 编号）；绘图内容以 PNG/TIFF 逐字节比较为准 |
| figures/fig3.png | 是 |  |
| figures/fig3.svg | 否 | SVG 与 PDF 内含生成时刻（SVG 另有随机的 clip-path 编号）；绘图内容以 PNG/TIFF 逐字节比较为准 |
| figures/fig3.tiff | 是 |  |
| figures/figS1.pdf | 否 | SVG 与 PDF 内含生成时刻（SVG 另有随机的 clip-path 编号）；绘图内容以 PNG/TIFF 逐字节比较为准 |
| figures/figS1.png | 是 |  |
| figures/figS1.svg | 否 | SVG 与 PDF 内含生成时刻（SVG 另有随机的 clip-path 编号）；绘图内容以 PNG/TIFF 逐字节比较为准 |
| figures/figS1.tiff | 是 |  |
| figures/figS2.pdf | 否 | SVG 与 PDF 内含生成时刻（SVG 另有随机的 clip-path 编号）；绘图内容以 PNG/TIFF 逐字节比较为准 |
| figures/figS2.png | 是 |  |
| figures/figS2.svg | 否 | SVG 与 PDF 内含生成时刻（SVG 另有随机的 clip-path 编号）；绘图内容以 PNG/TIFF 逐字节比较为准 |
| figures/figS2.tiff | 是 |  |
