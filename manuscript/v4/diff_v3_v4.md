# v3 与 v4 的逐段对照

由 `manuscript/code/compare_versions.py` 生成。v3 = `manuscript/archive/v3/`，v4 = `manuscript/v4/`。表外的每个段落与表内的每个单元格各为一项，按文档顺序用 difflib 对齐；列出全部不相同的块（两侧原文）。

## tables_v3.docx → tables_v4.docx

项数：v3 287，v4 287；相同 287；不同的块 0。

嵌入图片（word/media）：v3 0 个、v4 0 个；sha256 相同的 0 个。

## figures_v3.docx → figures_v4.docx

项数：v3 9，v4 9；相同 9；不同的块 0。

嵌入图片（word/media）：v3 3 个、v4 3 个；sha256 相同的 3 个。

## supplement_v3.docx → supplement_v4.docx

项数：v3 2186，v4 2186；相同 2185；不同的块 1。

### supplement 块 1（改）
- v3［paragraph］✳✳✳Median survival of 26 months after progression during neoadjuvant therapy instead of the early-recurrence distribution (Supplementary Table S1); this scenario did not reproduce trial overall survival in years 1 to 3.
- v4［paragraph］✳✳✳Median survival of 26 months after progression during neoadjuvant therapy instead of the early-recurrence distribution (Supplementary Table S1); this scenario did not reproduce trial overall survival in years 1 to 3. Progression during neoadjuvant therapy occurs before surgery and is the same with and without exercise, whereas the exercise effect on recurrence acts only after surgery. The maximum affordable costs and break-even hazard ratios for exercise therefore equal the base-case values in Table 2 at the precision shown; this scenario changes only the ICER of pembrolizumab.

嵌入图片（word/media）：v3 2 个、v4 2 个；sha256 相同的 2 个。

## results_v3.docx → results_v4.docx

项数：v3 11，v4 11；相同 10；不同的块 1。

### results 块 1（改）
- v3［paragraph］Fig. 3 shows the one-way sensitivity analysis of the maximum affordable cost for exercise added to chemotherapy plus pembrolizumab at an HR of 0.85 (Supplementary Table S9). The monthly cost of second-line and later treatment moved this cost most, from JPY 2,617 thousand at its lower bound to JPY 2,836 thousand at its upper bound (Fig. 3). Supplementary Fig. S2 shows that the pembrolizumab drug cost moved the ICER most, to JPY 1,296 thousand per QALY at its lower bound. Supplementary Table S10 shows that, with utility values from Japanese populations, the maximum affordable cost at an HR of 0.85 was JPY 2,733 thousand. Across the six scenarios in this table, the HR at which the maximum affordable cost equaled the cost of the fee-schedule-based program ranged from 0.988 to 0.989 (Supplementary Table S10).
- v4［paragraph］Fig. 3 shows the one-way sensitivity analysis of the maximum affordable cost for exercise added to chemotherapy plus pembrolizumab at an HR of 0.85 (Supplementary Table S9). The monthly cost of second-line and later treatment moved this cost most, from JPY 2,617 thousand at its lower bound to JPY 2,836 thousand at its upper bound (Fig. 3). Supplementary Fig. S2 shows that the pembrolizumab drug cost moved the ICER most, to JPY 1,296 thousand per QALY at its lower bound. Supplementary Table S10 shows that, with utility values from Japanese populations, the maximum affordable cost at an HR of 0.85 was JPY 2,733 thousand. With the four utility scenarios and Japanese post-operative treatment, this cost equaled the fee-schedule-based program cost at HRs of 0.988 to 0.989 (Supplementary Table S10). With longer survival after progression during neoadjuvant therapy, the ICER of pembrolizumab was JPY 2,082 thousand per QALY (Supplementary Table S10).

嵌入图片（word/media）：v3 0 个、v4 0 个；sha256 相同的 0 个。

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
