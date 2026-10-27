# v4 的回读检查（2026-10-26 21:36，`manuscript/code/make_ledger.py`）

从交付的 docx 读回。数字检查：抽出所有数字（与字母或连字符相连的编号如 E01、S1、EQ-5D、KEYNOTE-522 不算；表与图的编号先去掉），逐个与登记表比对；反向检查登记的数值是否都出现在文档中。Results 另按句检查：每个数字须是该句所引表格中某一格的显示值。

### manuscript/v4/tables_v4.docx

| 项目 | 结果 | 应为 |
|---|---|---|
| paragraphs_and_cells | 289 |  |
| text_runs | 313 |  |
| runs_not_TNR_12pt | 0 | 0 |
| runs_non_black | 0 | 0 |
| empty_cells | 0 | 0 |
| heading_style_paragraphs | 0 | 0 |
| bold_runs_outside_tables | 0 | 0 |
| bold_runs_in_cells_with_digits | 0 | 0 |
| middle_dot | 0 | 0 |
| paragraphs_starting_Note | 0 | 0 |
| em_dash_outside_cells | 0 | 0 |
| orientation_ok | True | True |
| numeric_tokens | 260 |  |
| unregistered_tokens | 0（无） | 0 |
| registered_values_not_found_in_document | 0（无） | 0 |
| sections | [('landscape', 297, 210), ('landscape', 297, 210), ('landscape', 297, 210)] | |

脚注符号（表内或题目中的上标 ↔ 脚注段落开头的符号）：

| 单位 | 表内/题目 | 脚注 | 一对一 | 顺序 |
|---|---|---|---|---|
| Table 1 | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | True | True |
| Table 2 | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | True | True |
| Table 3 | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | True | True |

### manuscript/v4/figures_v4.docx

| 项目 | 结果 | 应为 |
|---|---|---|
| paragraphs_and_cells | 14 |  |
| text_runs | 12 |  |
| runs_not_TNR_12pt | 0 | 0 |
| runs_non_black | 0 | 0 |
| empty_cells | 0 | 0 |
| heading_style_paragraphs | 0 | 0 |
| bold_runs_outside_tables | 0 | 0 |
| bold_runs_in_cells_with_digits | 0 | 0 |
| middle_dot | 0 | 0 |
| paragraphs_starting_Note | 0 | 0 |
| em_dash_outside_cells | 0 | 0 |
| orientation_ok | True | True |
| numeric_tokens | 30 |  |
| unregistered_tokens | 0（无） | 0 |
| registered_values_not_found_in_document | 0（无） | 0 |
| sections | [('portrait', 210, 297)] | |

脚注符号（表内或题目中的上标 ↔ 脚注段落开头的符号）：

| 单位 | 表内/题目 | 脚注 | 一对一 | 顺序 |
|---|---|---|---|---|
| Fig. 1 | ✳ | ✳ | True | True |
| Fig. 2 | ✳ | ✳ | True | True |
| Fig. 3 | ✳ | ✳ | True | True |

### manuscript/v4/supplement_v4.docx

| 项目 | 结果 | 应为 |
|---|---|---|
| paragraphs_and_cells | 2215 |  |
| text_runs | 2207 |  |
| runs_not_TNR_12pt | 0 | 0 |
| runs_non_black | 0 | 0 |
| empty_cells | 0 | 0 |
| heading_style_paragraphs | 0 | 0 |
| bold_runs_outside_tables | 0 | 0 |
| bold_runs_in_cells_with_digits | 0 | 0 |
| middle_dot | 0 | 0 |
| paragraphs_starting_Note | 0 | 0 |
| em_dash_outside_cells | 0 | 0 |
| orientation_ok | True | True |
| numeric_tokens | 2328 |  |
| unregistered_tokens | 0（无） | 0 |
| registered_values_not_found_in_document | 0（无） | 0 |
| sections | [('landscape', 297, 210), ('portrait', 210, 297), ('landscape', 297, 210), ('landscape', 297, 210), ('landscape', 297, 210), ('landscape', 297, 210), ('landscape', 297, 210), ('landscape', 297, 210), ('landscape', 297, 210), ('portrait', 210, 297), ('landscape', 297, 210)] | |

脚注符号（表内或题目中的上标 ↔ 脚注段落开头的符号）：

| 单位 | 表内/题目 | 脚注 | 一对一 | 顺序 |
|---|---|---|---|---|
| Supplementary Table S1 | ✳ | ✳ | True | True |
| Supplementary Fig. S1 | ✳ | ✳ | True | True |
| Supplementary Table S2 | ✳ ✳✳ ✳✳✳ | ✳ ✳✳ ✳✳✳ | True | True |
| Supplementary Table S4 | ✳ | ✳ | True | True |
| Supplementary Table S5 | ✳ ✳✳ | ✳ ✳✳ | True | True |
| Supplementary Table S6 | ✳ | ✳ | True | True |
| Supplementary Table S7 | ✳ | ✳ | True | True |
| Supplementary Table S8 | ✳ | ✳ | True | True |
| Supplementary Table S9 | ✳ | ✳ | True | True |
| Supplementary Fig. S2 | ✳ | ✳ | True | True |
| Supplementary Table S10 | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | True | True |

### manuscript/v4/results_v4.docx

| 项目 | 结果 | 应为 |
|---|---|---|
| paragraphs_and_cells | 11 |  |
| text_runs | 11 |  |
| runs_not_TNR_12pt | 0 | 0 |
| runs_non_black | 0 | 0 |
| empty_cells | 0 | 0 |
| heading_style_paragraphs | 0 | 0 |
| bold_runs_outside_tables | 0 | 0 |
| bold_runs_in_cells_with_digits | 0 | 0 |
| middle_dot | 0 | 0 |
| paragraphs_starting_Note | 0 | 0 |
| em_dash_outside_cells | 0 | 0 |
| orientation_ok | True | True |
| numeric_tokens | 81 |  |
| unregistered_tokens | 0（无） | 0 |
| registered_values_not_found_in_document | 0（无） | 0 |
| sections | [('portrait', 210, 297)] | |

## Results 的检查

| 项目 | 结果 |
|---|---|
| heading_is_Results_bold_normal | True |
| paragraphs | 10 |
| ledger_matches_docx | True |
| double_spacing_paragraphs | 11 |
| line_numbering | True |
| banned_terms | {} |
| throat_clearing | {} |
| meta_commentary | {} |
| hedges | {} |
| methods_phrases | {} |
| bare_time_words | {} |
| causal_words | {} |
| em_dash | 0 |
| connectives_per_paragraph_max | 0 |
| sentences | 44 |
| sentences_over_30_words | 0 |
| longest_sentence_words | 30 |
| paragraph_words | [128, 64, 62, 98, 66, 73, 106, 52, 63, 150] |
| paragraphs_over_150_words | 0 |
| words_total | 862 |
| paragraphs_open_with_table_or_figure | 10 |
| sentences_without_table_or_figure_reference | [] |
| numbers_not_in_cited_tables | [] |
| numeric_tokens | 81 |
| first_citation_order | ['Fig. 2', 'Table 2', 'Supplementary Table S4', 'Supplementary Table S5', 'Supplementary Table S6', 'Supplementary Table S7', 'Table 3', 'Supplementary Table S8', 'Fig. 3', 'Supplementary Table S9', 'Supplementary Fig. S2', 'Supplementary Table S10'] |
| first_citation_order_by_series | {'Fig.': [2, 3], 'Table': [2, 3], 'Supplementary Table': [4, 5, 6, 7, 8, 9, 10], 'Supplementary Fig.': [2]} |
| first_citation_in_order | True |
| acronym_check_exit | 0 |

ARS check_acronyms.py（body 范围）：

```
### Acronym check (advisory; no reply needed)
Coverage: body (complete)
No findings.
```

## 图（实测）

| 图 | 像素 | 文件 dpi | 插入宽×高（mm） | 插入后的实际 dpi |
|---|---|---|---|---|
| Fig. 1 | 4015 x 2173 | [600.0, 600.0] | 169.97 × 91.99 | 600.0 |
| Fig. 2 | 4015 x 2456 | [600.0, 600.0] | 169.97 × 103.97 | 600.0 |
| Fig. 3 | 4015 x 3023 | [600.0, 600.0] | 169.97 × 127.97 | 600.0 |
| Supplementary Fig. S1 | 4015 x 2267 | [600.0, 600.0] | 169.97 × 95.97 | 600.0 |
| Supplementary Fig. S2 | 4015 x 3023 | [600.0, 600.0] | 169.97 × 127.97 | 600.0 |

nature-figure 的检查（导出的 PDF）：

- fig1 碰撞检查：PASS，{'fail': 0, 'warn': 0, 'contained_fill_overlays': 16, 'contained_image_overlays': 0}
- fig2 碰撞检查：PASS，{'fail': 0, 'warn': 0, 'contained_fill_overlays': 5, 'contained_image_overlays': 0}
- fig3 碰撞检查：PASS，{'fail': 0, 'warn': 0, 'contained_fill_overlays': 0, 'contained_image_overlays': 0}
- figS1 碰撞检查：PASS，{'fail': 0, 'warn': 0, 'contained_fill_overlays': 0, 'contained_image_overlays': 0}
- figS2 碰撞检查：PASS，{'fail': 0, 'warn': 0, 'contained_fill_overlays': 0, 'contained_image_overlays': 0}
- fig2 面板对齐：PASS，{'fail': 0, 'warn': 0, 'comparisons': 1, 'exemptions': 0}
- figS1 面板对齐：PASS，{'fail': 0, 'warn': 0, 'comparisons': 1, 'exemptions': 0}

## 同一来源格出现在两张表中（规约第 6.1 节）

| 表 | 格数 | 归类 |
|---|---|---|
| Supplementary Table S1 & Table 1 | 26 | E2（S1 完整参数表与 Table 1；2026-10-26 决定） |
| Supplementary Table S10 & Table 3 | 1 | E4（S10 的 S-JP 参照 ICER 与 Table 3 的 S-JP 栏；待确认） |
| Supplementary Table S4 & Table 2 | 6 | E1（Table 2 Panel B、C 的基准行与 S4；2026-10-26 决定） |
| Supplementary Table S6 & Table 2 | 4 | E3（S6 完整网格与 Table 2 Panel B 的 HR 0.85 两行；待确认） |
