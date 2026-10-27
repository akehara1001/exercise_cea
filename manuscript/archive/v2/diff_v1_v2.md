# v1 与 v2 的逐段对照

由 `manuscript/code/compare_versions.py` 生成。v1 = `manuscript/archive/v1/`，v2 = `manuscript/v2/`。表外的每个段落与表内的每个单元格各为一项，按文档顺序用 difflib 对齐；列出全部不相同的块（两侧原文）。

## tables_v1.docx → tables_v2.docx

项数：v1 302，v2 287；相同 245；不同的块 9。

### tables 块 1（改）
- v1［table 1 row 24 cell 1］Utilities
- v2［table 1 row 24 cell 1］Utilities✳✳✳

### tables 块 2（改）
- v1［table 1 row 31 cell 2］Recurrence HR✳✳✳ from 0.70 to 1.00; no effect on deaths without recurrence or on events before surgery
- v2［table 1 row 31 cell 2］Recurrence HR✳✳✳✳ from 0.70 to 1.00; no effect on deaths without recurrence or on events before surgery

### tables 块 3（改）
- v1［paragraph］✳✳✳Recurrence HR: hazard ratio for locoregional and distant recurrence after surgery in an arm with exercise, relative to the same treatment without exercise; 1.00 means no effect.
- v1［paragraph］Table 2. Maximum affordable cost of an exercise program per patient by the recurrence hazard ratio with exercise, at a willingness-to-pay threshold of JPY 5 million per QALY✳
- v1［table 2 row 1 cell 1］Recurrence HR or quantity
- v2［paragraph］✳✳✳Base case: EQ-5D values from KEYNOTE-522 with the German value set, because no report applying a Japanese value set to KEYNOTE-522 data with standard errors was found. Values from Japanese populations are used in a scenario (Supplementary Table S8).
- v2［paragraph］✳✳✳✳Recurrence HR: hazard ratio for locoregional and distant recurrence after surgery in an arm with exercise, relative to the same treatment without exercise; 1.00 means no effect.
- v2［paragraph］Table 2. Recurrence hazard ratios at which exercise breaks even, and the maximum affordable cost of an exercise program per patient under alternative effect durations and metastatic treatment costs, at a willingness-to-pay threshold of JPY 5 million per QALY✳
- v2［table 2 row 1 cell 1］Break-even point or scenario

### tables 块 4（改）
- v1［table 2 row 2 cell 1］A. Maximum affordable cost by recurrence HR✳✳, base-case effect duration
- v1［table 2 row 3 cell 1］0.70
- v1［table 2 row 3 cell 2］5,596 [4,545, 6,256]
- v1［table 2 row 3 cell 3］7,107 [5,923, 7,869]
- v1［table 2 row 4 cell 1］0.75
- v1［table 2 row 4 cell 2］4,623 [3,758, 5,164]
- v1［table 2 row 4 cell 3］5,860 [4,895, 6,473]
- v1［table 2 row 5 cell 1］0.80
- v1［table 2 row 5 cell 2］3,667 [2,983, 4,092]
- v1［table 2 row 5 cell 3］4,639 [3,879, 5,110]
- v1［table 2 row 6 cell 1］0.85
- v2［table 2 row 2 cell 1］A. Recurrence HR✳✳ (reduction in recurrence hazard, %) at which, in the base case,
- v2［table 2 row 3 cell 1］The maximum affordable cost equals the cost of the fee-schedule-based program
- v2［table 2 row 3 cell 2］0.989 (1.1)
- v2［table 2 row 3 cell 3］0.991 (0.9)
- v2［table 2 row 4 cell 1］Medical costs avoided✳✳✳ equal the cost of the CHALLENGE-based supervised program
- v2［table 2 row 4 cell 2］0.948 (5.2)
- v2［table 2 row 4 cell 3］0.958 (4.2)
- v2［table 2 row 5 cell 1］Medical costs avoided✳✳✳ equal the cost of the fee-schedule-based program
- v2［table 2 row 5 cell 2］0.958 (4.2)
- v2［table 2 row 5 cell 3］0.966 (3.4)
- v2［table 2 row 6 cell 1］Medical costs avoided✳✳✳ equal the cost of the remote low-cost program
- v2［table 2 row 6 cell 2］0.997 (0.3)
- v2［table 2 row 6 cell 3］0.998 (0.2)
- v2［table 2 row 7 cell 1］B. Maximum affordable cost under alternative effect durations✳✳✳✳
- v2［table 2 row 8 cell 1］Base case, recurrence HR 0.85

### tables 块 5（删）
- v1［table 2 row 7 cell 1］0.90
- v1［table 2 row 7 cell 2］1,802 [1,471, 2,007]
- v1［table 2 row 7 cell 3］2,271 [1,902, 2,492]
- v1［table 2 row 8 cell 1］0.95
- v1［table 2 row 8 cell 2］893 [730, 994]
- v1［table 2 row 8 cell 3］1,124 [943, 1,232]
- v1［table 2 row 9 cell 1］1.00
- v1［table 2 row 9 cell 2］−1 [−2, 0]
- v1［table 2 row 9 cell 3］−1 [−2, 0]
- v1［table 2 row 10 cell 1］B. Recurrence HR at which, in the base case,
- v1［table 2 row 11 cell 1］The maximum affordable cost equals the cost of the fee-schedule-based program
- v1［table 2 row 11 cell 2］0.989
- v1［table 2 row 11 cell 3］0.991
- v1［table 2 row 12 cell 1］Medical costs avoided✳✳✳ equal the cost of the CHALLENGE-based supervised program
- v1［table 2 row 12 cell 2］0.948
- v1［table 2 row 12 cell 3］0.958
- v1［table 2 row 13 cell 1］Medical costs avoided✳✳✳ equal the cost of the fee-schedule-based program
- v1［table 2 row 13 cell 2］0.958
- v1［table 2 row 13 cell 3］0.966
- v1［table 2 row 14 cell 1］Medical costs avoided✳✳✳ equal the cost of the remote low-cost program
- v1［table 2 row 14 cell 2］0.997
- v1［table 2 row 14 cell 3］0.998
- v1［table 2 row 15 cell 1］C. Maximum affordable cost under alternative effect durations✳✳✳✳

### tables 块 6（改）
- v1［table 2 row 18 cell 1］D. Metastatic treatment cost scenarios✳✳✳✳
- v2［table 2 row 11 cell 1］C. Metastatic treatment cost scenarios✳✳✳✳
- v2［table 2 row 12 cell 1］Base case, recurrence HR 0.85
- v2［table 2 row 12 cell 2］2,726 [2,223, 3,040]
- v2［table 2 row 12 cell 3］3,443 [2,881, 3,785]

### tables 块 7（改）
- v1［table 2 row 21 cell 1］Recurrence HR at which the maximum affordable cost equals the cost of the fee-schedule-based program
- v1［table 2 row 21 cell 2］0.988
- v1［table 2 row 21 cell 3］0.990
- v1［table 2 row 22 cell 1］Recurrence HR at which medical costs avoided equal the cost of the fee-schedule-based program
- v1［table 2 row 22 cell 2］0.918
- v1［table 2 row 22 cell 3］0.934
- v2［table 2 row 15 cell 1］Recurrence HR (reduction in recurrence hazard, %) at which the maximum affordable cost equals the cost of the fee-schedule-based program
- v2［table 2 row 15 cell 2］0.988 (1.2)
- v2［table 2 row 15 cell 3］0.990 (1.0)
- v2［table 2 row 16 cell 1］Recurrence HR (reduction in recurrence hazard, %) at which medical costs avoided✳✳✳ equal the cost of the fee-schedule-based program
- v2［table 2 row 16 cell 2］0.918 (8.2)
- v2［table 2 row 16 cell 3］0.934 (6.6)

### tables 块 8（改）
- v1［table 2 row 25 cell 1］Recurrence HR at which the maximum affordable cost equals the cost of the fee-schedule-based program
- v1［table 2 row 25 cell 2］0.987
- v1［table 2 row 25 cell 3］0.990
- v1［table 2 row 26 cell 1］Recurrence HR at which medical costs avoided equal the cost of the fee-schedule-based program
- v1［table 2 row 26 cell 2］0.914
- v1［table 2 row 26 cell 3］0.925
- v1［paragraph］✳Modeled cohort: women aged 49 years starting neoadjuvant chemotherapy for stage II or III triple-negative breast cancer in Japan (Table 1). Maximum affordable cost: the largest program cost per patient at which adding exercise remains cost-effective, equal to the threshold multiplied by the incremental QALYs minus the incremental medical costs other than the program cost (musculoskeletal adverse events of exercise included). Cells show the deterministic estimate and the 95% UI [2.5th and 97.5th percentiles of 1,000 probabilistic sensitivity analysis samples]. Costs in JPY 1,000 at fiscal year 2026 prices, discounted at 2% per year over a lifetime horizon. HR, hazard ratio; JPY, Japanese yen; QALY, quality-adjusted life year; UI, uncertainty interval.
- v1［paragraph］✳✳Hazard ratio for locoregional and distant recurrence after surgery in the arm with exercise, relative to the same treatment without exercise; 1.00 means no effect. In panels A and B the effect is held for 5 years after randomization and then halves every year (Table 1).
- v1［paragraph］✳✳✳Reduction in lifetime medical costs other than the program cost. At recurrence HRs below these values, the arm with exercise has lower total costs, program included, and more QALYs.
- v1［paragraph］✳✳✳✳At a recurrence HR of 0.85. Effect durations and cost scenarios are defined in Table 1. Panel C shows deterministic estimates only (no probabilistic analysis was run for these durations); panel D keeps the base-case effect duration.
- v2［table 2 row 19 cell 1］Recurrence HR (reduction in recurrence hazard, %) at which the maximum affordable cost equals the cost of the fee-schedule-based program
- v2［table 2 row 19 cell 2］0.987 (1.3)
- v2［table 2 row 19 cell 3］0.990 (1.0)
- v2［table 2 row 20 cell 1］Recurrence HR (reduction in recurrence hazard, %) at which medical costs avoided✳✳✳ equal the cost of the fee-schedule-based program
- v2［table 2 row 20 cell 2］0.914 (8.6)
- v2［table 2 row 20 cell 3］0.925 (7.5)
- v2［paragraph］✳Modeled cohort: women aged 49 years starting neoadjuvant chemotherapy for stage II or III triple-negative breast cancer in Japan (Table 1). Maximum affordable cost: the largest program cost per patient at which adding exercise remains cost-effective, equal to the threshold multiplied by the incremental QALYs minus the incremental medical costs other than the program cost (musculoskeletal adverse events of exercise included). Cells with a bracket show the deterministic estimate and the 95% UI [2.5th and 97.5th percentiles of 1,000 probabilistic sensitivity analysis samples]. Costs in JPY 1,000 at fiscal year 2026 prices, discounted at 2% per year over a lifetime horizon. HR, hazard ratio; JPY, Japanese yen; QALY, quality-adjusted life year; UI, uncertainty interval.
- v2［paragraph］✳✳Hazard ratio for locoregional and distant recurrence after surgery in the arm with exercise, relative to the same treatment without exercise; 1.00 means no effect. The value in parentheses is the reduction in the recurrence hazard, 100 × (1 − HR), in %. In panels A and C the effect is held for 5 years after randomization and then halves every year (Table 1).
- v2［paragraph］✳✳✳Reduction in lifetime medical costs other than the program cost. At recurrence HRs below these values, the arm with exercise has lower total costs, program included, and more QALYs. The reductions of 4.2% to 8.6% at which medical costs avoided equal the program cost (base case and both metastatic cost scenarios) hold only for exercise added to chemotherapy plus pembrolizumab with the fee-schedule-based program.
- v2［paragraph］✳✳✳✳At a recurrence HR of 0.85. The base-case row repeats the base-case estimate (Supplementary Table S4) for comparison within the panel. Effect durations and cost scenarios are defined in Table 1. The alternative effect durations show deterministic estimates only (no probabilistic analysis was run for them); panel C keeps the base-case effect duration.

### tables 块 9（改）
- v1［paragraph］✳✳✳✳Effect at which exercise added to chemotherapy alone yields the same incremental QALYs as pembrolizumab in the base case. Both values lie outside the ranges studied in Table 2 (recurrence HR 0.70 to 1.00) and Supplementary Table S9 (pCR increase 0 to 10 percentage points).
- v2［paragraph］✳✳✳✳Effect at which exercise added to chemotherapy alone yields the same incremental QALYs as pembrolizumab in the base case. Both values lie outside the ranges studied: recurrence HR 0.70 to 1.00 (Supplementary Table S4) and pCR increase 0 to 10 percentage points (Supplementary Table S9).

嵌入图片（word/media）：v1 0 个、v2 0 个；sha256 相同的 0 个。

## figures_v1.docx → figures_v2.docx

项数：v1 9，v2 9；相同 9；不同的块 0。

嵌入图片（word/media）：v1 3 个、v2 3 个；sha256 相同的 3 个。

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
