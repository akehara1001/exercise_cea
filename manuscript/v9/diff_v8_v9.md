# v8 与 v9 的逐段对照

由 `manuscript/code/compare_versions.py` 生成。v8 = `manuscript/archive/v8/`，v9 = `manuscript/v9/`。表外的每个段落与表内的每个单元格各为一项，按文档顺序用 difflib 对齐；列出全部不相同的块（两侧原文）。

## tables_v8.docx → tables_v9.docx

项数：v8 287，v9 287；相同 287；不同的块 0。

### tables：归一化比较（v8 的补充表编号换成 v9 的编号、两版都去掉文献号）

不同的块 0（原始比较 0）。

| 块 | 类型 | v8 项数 | v9 项数 | v8 首项 | v9 首项 |
|---|---|---|---|---|---|

嵌入图片（word/media）：v8 0 个、v9 0 个；sha256 相同的 0 个。

## figures_v8.docx → figures_v9.docx

项数：v8 9，v9 9；相同 9；不同的块 0。

### figures：归一化比较（v8 的补充表编号换成 v9 的编号、两版都去掉文献号）

不同的块 0（原始比较 0）。

| 块 | 类型 | v8 项数 | v9 项数 | v8 首项 | v9 首项 |
|---|---|---|---|---|---|

嵌入图片（word/media）：v8 3 个、v9 3 个；sha256 相同的 3 个。

## supplement_v8.docx → supplement_v9.docx

项数：v8 2360，v9 2360；相同 2360；不同的块 0。

### supplement：归一化比较（v8 的补充表编号换成 v9 的编号、两版都去掉文献号）

不同的块 0（原始比较 0）。

| 块 | 类型 | v8 项数 | v9 项数 | v8 首项 | v9 首项 |
|---|---|---|---|---|---|

嵌入图片（word/media）：v8 2 个、v9 2 个；sha256 相同的 2 个。

## manuscript_v8.docx → manuscript_v9.docx

项数：v8 141，v9 141；相同 134；不同的块 7。

### manuscript 块 1（改）
- v8［paragraph］The maximum affordable cost of structured exercise during neoadjuvant chemotherapy for triple-negative breast cancer in Japan: a cost-effectiveness analysis
- v9［paragraph］Cost-effectiveness of exercise added to neoadjuvant chemotherapy for triple-negative breast cancer in Japan

### manuscript 块 2（改）
- v8［paragraph］A state-transition model used KEYNOTE-522 data, including the final analysis, to simulate chemotherapy with or without pembrolizumab, each with or without exercise. The analysis took the Japanese public healthcare payer perspective over a lifetime, with discounting at 2% per year. The effect of exercise was expressed as a hazard ratio (HR) for recurrence after surgery, from 0.70 to 1.00, with alternative durations. The maximum affordable cost was the threshold of JPY 5 million per quality-adjusted life year (QALY) times the incremental QALYs, minus incremental medical costs other than the program cost.
- v9［paragraph］A state-transition model based on KEYNOTE-522 simulated chemotherapy with or without pembrolizumab, each with or without exercise. The analysis took the Japanese public healthcare payer perspective over a lifetime, with discounting at 2% per year. The exercise effect was a hazard ratio (HR) for recurrence after surgery of 0.70 to 1.00, with alternative durations. The maximum affordable cost was the threshold of JPY 5 million per quality-adjusted life year (QALY) times the incremental QALYs, minus incremental medical costs other than the program cost.

### manuscript 块 3（改）
- v8［paragraph］Added to chemotherapy plus pembrolizumab, exercise had a maximum affordable cost of JPY 2,726 thousand per patient at an HR of 0.85 (95% uncertainty interval [2,223, 3,040]). A program priced from the medical fee schedule (JPY 192,400) became cost-effective at an HR of 0.989. Medical costs avoided alone paid for it at HRs of 0.958 to 0.914, depending on metastatic treatment costs. The duration of the effect changed the maximum affordable cost more than any cost input. Pembrolizumab had an incremental cost-effectiveness ratio of JPY 2,053 thousand per QALY, and exercise would need an HR of 0.425 to match its QALY gain.
- v9［paragraph］Added to chemotherapy plus pembrolizumab, exercise had a maximum affordable cost of JPY 2,726 thousand per patient at an HR of 0.85 (95% uncertainty interval [2,223, 3,040]). Added to chemotherapy alone, it was JPY 3,443 thousand. A program priced from the medical fee schedule (JPY 192,400) became cost-effective at an HR of 0.989. Medical costs avoided alone paid for it at HRs of 0.958 to 0.914, depending on metastatic treatment costs. The duration of the effect changed the maximum affordable cost more than any cost input. Pembrolizumab cost JPY 2,053 thousand per QALY gained, and exercise would need an HR of 0.425 to match its QALY gain.

### manuscript 块 4（改）
- v8［paragraph］In Japan, the value of exercise during neoadjuvant chemotherapy depends on the size and duration of its effect on recurrence far more than on its price. Even a small effect on recurrence would pay for a program. Trials should measure recurrence and whether the effect lasts.
- v9［paragraph］In Japan, the value of exercise during neoadjuvant chemotherapy depends on the size and duration of its effect on recurrence far more than on its price. Trials should measure recurrence and whether the effect lasts.

### manuscript 块 5（改）
- v8［paragraph］Duration changed the maximum affordable cost more than any cost input did (Table 2; Fig. 3). Because most recurrences after this regimen occur early6, an effect that holds through the first years after surgery captures most of the value. When the effect of the neoadjuvant program alone would fade early, continuing exercise after surgery raised the maximum affordable cost (Supplementary Table S7).
- v9［paragraph］Duration changed the maximum affordable cost more than any cost input did (Table 2; Fig. 3). Because most recurrences after neoadjuvant chemotherapy with pembrolizumab occur early6, an effect that holds through the first years after surgery captures most of the value. When the effect of the neoadjuvant program alone would fade early, continuing exercise after surgery raised the maximum affordable cost (Supplementary Table S7).

### manuscript 块 6（改）
- v8［paragraph］Pembrolizumab added to neoadjuvant chemotherapy was cost-effective in Japan, as in analyses from the United States, Hong Kong, Switzerland and Egypt28–31. Its cost-effectiveness depended most on its price and on whether capecitabine or olaparib was added after surgery, as in Japanese practice (Table 3; Supplementary Fig. S2). The regimen has not been designated for Japan's cost-effectiveness evaluation39, and our estimate gives a reference in the meantime.
- v9［paragraph］Pembrolizumab added to neoadjuvant chemotherapy was cost-effective in Japan, as in analyses from the United States, Hong Kong, Switzerland and Egypt28–31. Its cost-effectiveness depended most on its price and on whether capecitabine or olaparib was added after surgery, as in Japanese practice (Table 3; Supplementary Fig. S2).

### manuscript 块 7（改）
- v8［paragraph］Clinicians can offer exercise during neoadjuvant chemotherapy for its known benefits on fitness10–12 while its effect on recurrence is tested. This analysis adds that an effect on recurrence, if present, would carry large economic value. Trials of exercise during neoadjuvant chemotherapy should record recurrence and follow patients long enough to see whether the effect lasts after the program ends. A higher pCR alone cannot settle the question, because it is unknown how a change in pCR with exercise would translate into fewer recurrences (Supplementary Table S5). Funders can weigh the cost of such trials against the net benefit for one year of Japanese patients if an effect is confirmed (Supplementary Table S8).
- v9［paragraph］Exercise during adjuvant chemotherapy improves fitness10–12, and trials have delivered supervised exercise during neoadjuvant chemotherapy16,17. Clinicians can therefore offer it while its effect on recurrence is tested. This analysis adds that an effect on recurrence, if present, would carry large economic value. Trials of exercise during neoadjuvant chemotherapy should record recurrence and follow patients long enough to see whether the effect lasts after the program ends. A higher pCR alone cannot settle the question, because it is unknown how a change in pCR with exercise would translate into fewer recurrences (Supplementary Table S5). Funders can weigh the cost of such trials against the net benefit for one year of Japanese patients if an effect is confirmed (Supplementary Table S8).

### manuscript：归一化比较（v8 的补充表编号换成 v9 的编号、两版都去掉文献号）

不同的块 7（原始比较 7）。

| 块 | 类型 | v8 项数 | v9 项数 | v8 首项 | v9 首项 |
|---|---|---|---|---|---|
| N1 | replace | 1 | 1 | The maximum affordable cost of structured exercise during neoadjuvant chemotherapy for tri | Cost-effectiveness of exercise added to neoadjuvant chemotherapy for triple-negative breas |
| N2 | replace | 1 | 1 | A state-transition model used KEYNOTE-522 data, including the final analysis, to simulate  | A state-transition model based on KEYNOTE-522 simulated chemotherapy with or without pembr |
| N3 | replace | 1 | 1 | Added to chemotherapy plus pembrolizumab, exercise had a maximum affordable cost of JPY 2, | Added to chemotherapy plus pembrolizumab, exercise had a maximum affordable cost of JPY 2, |
| N4 | replace | 1 | 1 | In Japan, the value of exercise during neoadjuvant chemotherapy depends on the size and du | In Japan, the value of exercise during neoadjuvant chemotherapy depends on the size and du |
| N5 | replace | 1 | 1 | Duration changed the maximum affordable cost more than any cost input did (Table 2; Fig. 3 | Duration changed the maximum affordable cost more than any cost input did (Table 2; Fig. 3 |
| N6 | replace | 1 | 1 | Pembrolizumab added to neoadjuvant chemotherapy was cost-effective in Japan, as in analyse | Pembrolizumab added to neoadjuvant chemotherapy was cost-effective in Japan, as in analyse |
| N7 | replace | 1 | 1 | Clinicians can offer exercise during neoadjuvant chemotherapy for its known benefits on fi | Exercise during adjuvant chemotherapy improves fitness, and trials have delivered supervis |

嵌入图片（word/media）：v8 0 个、v9 0 个；sha256 相同的 0 个。

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
