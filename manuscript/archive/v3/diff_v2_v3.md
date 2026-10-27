# v2 与 v3 的逐段对照

由 `manuscript/code/compare_versions.py` 生成。v2 = `manuscript/archive/v2/`，v3 = `manuscript/v3/`。表外的每个段落与表内的每个单元格各为一项，按文档顺序用 difflib 对齐；列出全部不相同的块（两侧原文）。

## tables_v2.docx → tables_v3.docx

项数：v2 287，v3 287；相同 285；不同的块 2。

### tables 块 1（改）
- v2［paragraph］✳✳✳Base case: EQ-5D values from KEYNOTE-522 with the German value set, because no report applying a Japanese value set to KEYNOTE-522 data with standard errors was found. Values from Japanese populations are used in a scenario (Supplementary Table S8).
- v3［paragraph］✳✳✳Base case: EQ-5D values from KEYNOTE-522 with the German value set, because no report applying a Japanese value set to KEYNOTE-522 data with standard errors was found. Values from Japanese populations are used in a scenario (Supplementary Table S10).

### tables 块 2（改）
- v2［paragraph］✳✳✳✳Effect at which exercise added to chemotherapy alone yields the same incremental QALYs as pembrolizumab in the base case. Both values lie outside the ranges studied: recurrence HR 0.70 to 1.00 (Supplementary Table S4) and pCR increase 0 to 10 percentage points (Supplementary Table S9).
- v3［paragraph］✳✳✳✳Effect at which exercise added to chemotherapy alone yields the same incremental QALYs as pembrolizumab in the base case. Both values lie outside the ranges studied: recurrence HR 0.70 to 1.00 (Supplementary Table S4) and pCR increase 0 to 10 percentage points (Supplementary Table S8).

嵌入图片（word/media）：v2 0 个、v3 0 个；sha256 相同的 0 个。

## figures_v2.docx → figures_v3.docx

项数：v2 9，v3 9；相同 8；不同的块 1。

### figures 块 1（改）
- v2［paragraph］Bars show the maximum affordable cost per patient at a willingness-to-pay threshold of JPY 5 million per QALY when one input is set to its lower bound (dark bars) or upper bound (light bars) and all other inputs keep their base-case values; the vertical line is the base-case estimate. All 21 inputs that changed the result are shown, ordered by the width of their range. Brackets mark ranges set by rule rather than taken from a source: [±25%], ±25% around the base value where no range was available; [mirrored], the missing bound mirrored where only one bound was given; [price], drug price varied downward only, to 75% of the list price. Codes in parentheses refer to Supplementary Table S1; the plotted values are listed in Supplementary Table S6.
- v3［paragraph］Bars show the maximum affordable cost per patient at a willingness-to-pay threshold of JPY 5 million per QALY when one input is set to its lower bound (dark bars) or upper bound (light bars) and all other inputs keep their base-case values; the vertical line is the base-case estimate. All 21 inputs that changed the result are shown, ordered by the width of their range. Brackets mark ranges set by rule rather than taken from a source: [±25%], ±25% around the base value where no range was available; [mirrored], the missing bound mirrored where only one bound was given; [price], drug price varied downward only, to 75% of the list price. Codes in parentheses refer to Supplementary Table S1; the plotted values are listed in Supplementary Table S9.

嵌入图片（word/media）：v2 3 个、v3 3 个；sha256 相同的 3 个。

## supplement_v3.docx

v2 中没有此文件（本版新建），不作逐段对照。

## results_v3.docx

v2 中没有此文件（本版新建），不作逐段对照。

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
| figures/figS1.pdf | — | 本版新建 |
| figures/figS1.png | — | 本版新建 |
| figures/figS1.svg | — | 本版新建 |
| figures/figS1.tiff | — | 本版新建 |
| figures/figS2.pdf | — | 本版新建 |
| figures/figS2.png | — | 本版新建 |
| figures/figS2.svg | — | 本版新建 |
| figures/figS2.tiff | — | 本版新建 |
