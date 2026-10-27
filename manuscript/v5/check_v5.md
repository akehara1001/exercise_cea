# v5 的回读检查（2026-10-27 00:47，`manuscript/code/make_ledger.py`）

从交付的 docx 读回。数字检查：抽出所有数字（与字母或连字符相连的编号如 E01、S1、EQ-5D、KEYNOTE-522 不算；表与图的编号与文献号的上标先去掉），逐个与登记表比对；反向检查登记的数值是否都出现在文档中。Results 另按句检查：每个数字须是该句所引表格中某一格的显示值。Introduction 与 Methods 按段检查：每个数字须登记在该段（所引文献摘要中的原文、表中的显示值、项目文件中的设定或定义）。

### manuscript/v5/manuscript_v5.docx

| 项目 | 结果 | 应为 |
|---|---|---|
| paragraphs_and_cells | 117 |  |
| text_runs | 219 |  |
| citation_runs | 51 |  |
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
| numeric_tokens | 182 |  |
| unregistered_tokens | 0（无） | 0 |
| registered_values_not_found_in_document | 0（无） | 0 |
| sections | [('portrait', 210, 297)] | |

### manuscript/v5/tables_v5.docx

| 项目 | 结果 | 应为 |
|---|---|---|
| paragraphs_and_cells | 289 |  |
| text_runs | 337 |  |
| citation_runs | 24 |  |
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

脚注符号（表内或题目中的上标 ↔ 脚注段落开头的符号；文献号的上标不计）：

| 单位 | 表内/题目 | 脚注 | 一对一 | 顺序 |
|---|---|---|---|---|
| Table 1 | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | True | True |
| Table 2 | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | True | True |
| Table 3 | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | True | True |

### manuscript/v5/figures_v5.docx

| 项目 | 结果 | 应为 |
|---|---|---|
| paragraphs_and_cells | 14 |  |
| text_runs | 14 |  |
| citation_runs | 1 |  |
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

脚注符号（表内或题目中的上标 ↔ 脚注段落开头的符号；文献号的上标不计）：

| 单位 | 表内/题目 | 脚注 | 一对一 | 顺序 |
|---|---|---|---|---|
| Fig. 1 | ✳ | ✳ | True | True |
| Fig. 2 | ✳ | ✳ | True | True |
| Fig. 3 | ✳ | ✳ | True | True |

### manuscript/v5/supplement_v5.docx

| 项目 | 结果 | 应为 |
|---|---|---|
| paragraphs_and_cells | 2390 |  |
| text_runs | 2519 |  |
| citation_runs | 126 |  |
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
| numeric_tokens | 2184 |  |
| unregistered_tokens | 0（无） | 0 |
| registered_values_not_found_in_document | 0（无） | 0 |
| sections | [('landscape', 297, 210), ('landscape', 297, 210), ('portrait', 210, 297), ('portrait', 210, 297), ('landscape', 297, 210), ('landscape', 297, 210), ('landscape', 297, 210), ('landscape', 297, 210), ('landscape', 297, 210), ('landscape', 297, 210), ('landscape', 297, 210), ('portrait', 210, 297), ('landscape', 297, 210)] | |

脚注符号（表内或题目中的上标 ↔ 脚注段落开头的符号；文献号的上标不计）：

| 单位 | 表内/题目 | 脚注 | 一对一 | 顺序 |
|---|---|---|---|---|
| Supplementary Table S1 | ✳ | ✳ | True | True |
| Supplementary Table S2 | ✳ | ✳ | True | True |
| Supplementary Fig. S1 | ✳ | ✳ | True | True |
| Supplementary Table S3 | ✳ ✳✳ ✳✳✳ | ✳ ✳✳ ✳✳✳ | True | True |
| Supplementary Table S4 | ✳ | ✳ | True | True |
| Supplementary Table S5 | ✳ | ✳ | True | True |
| Supplementary Table S6 | ✳ ✳✳ | ✳ ✳✳ | True | True |
| Supplementary Table S7 | ✳ | ✳ | True | True |
| Supplementary Table S8 | ✳ | ✳ | True | True |
| Supplementary Table S9 | ✳ | ✳ | True | True |
| Supplementary Fig. S2 | ✳ | ✳ | True | True |
| Supplementary Table S10 | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | True | True |

## 本文的结构

| 项目 | 结果 |
|---|---|
| headings | ['Introduction', 'Methods', 'Study background', 'Outcome', 'Variables', 'Statistical analysis', 'Results', 'References'] |
| headings_as_specified | True |
| headings_bold_normal_12pt | True |
| body_paragraphs | 32 |
| double_spacing_paragraphs | 117/117 |
| line_numbering | True |

## Results 的检查

| 项目 | 结果 |
|---|---|
| paragraphs | 10 |
| ledger_matches_docx | True |
| sentences | 47 |
| paragraph_words | [150, 58, 85, 94, 63, 69, 90, 50, 58, 149] |
| paragraphs_open_with_table_or_figure | 10 |
| sentences_without_own_reference | ['Through an effect on pCR instead, an increase of 1 percentage point gave a maximum affordable cost of JPY 389 thousand (95% UI [238, 570]).', 'Incremental medical costs other than the program cost were JPY −702 thousand per patient.', 'Second-line and later treatment of distant recurrence contributed JPY −437 thousand.', 'It was JPY 1,772 thousand when the effect lasted until 1 year after surgery, against JPY 2,726 thousand in the base case.', 'With eribulin-based later-line treatment, this HR was 0.914, an 8.6% reduction.', 'The HR at which the maximum affordable cost equaled the program cost was 0.988 with metastatic treatment costs halved and 0.987 with eribulin-based treatment.', 'At an HR of 0.95, the net benefit for one year of patients was JPY 2.68 billion (95% UI [2.22, 2.94]).', 'Its maximum affordable cost at an HR of 0.85 was JPY 3,443 thousand per patient (95% UI [2,881, 3,785]).', 'This cost equaled the cost of the fee-schedule-based program at an HR of 0.991, a 0.9% reduction in the recurrence hazard.', 'In the base case, pembrolizumab added JPY 4,426 thousand per patient in costs (95% UI [−330, 8,901]).', 'It added 2.156 QALYs (95% UI [0.245, 4.228]).', 'The pembrolizumab drug cost was JPY 6,531 thousand.', 'Second-line and later treatment of distant recurrence contributed JPY −1,911 thousand.', 'The ICER was JPY 2,053 thousand per QALY.', 'It was JPY 2,565 thousand with metastatic treatment costs halved and JPY 2,785 thousand with eribulin-based later-line treatment.', 'This required a recurrence HR of 0.425.', 'With utility values from Japanese populations, the maximum affordable cost at that HR was JPY 2,733 thousand.', 'With the four utility scenarios and Japanese post-operative treatment, this cost equaled the fee-schedule-based program cost at HRs of 0.988 to 0.989.'] |
| sentences_without_a_later_reference_to_their_table | [] |
| numbers_not_in_cited_tables | [] |
| numeric_tokens | 92 |

## Introduction 与 Methods 的数字

| 项目 | 结果 |
|---|---|
| numbers_not_registered_for_their_paragraph | [] |
| numeric_tokens | 90 |
| registered_numbers | 93 |
| registered_by_kind | {'PubMed abstract': 14, 'input/params/cohort_N_jbcs2024.csv': 5, 'table/figure registry': 38, 'definition': 14, 'manuscript/code/refs/searches/search_novelty.json': 4, 'docs/model_spec.md': 4, 'output/phase1/phase1_report.md': 2, 'input/lifetable/SOURCE.md': 2, 'manuscript/code/references.py': 1, 'docs/analysis_plan_phase2.md': 8, 'renv.lock': 1} |

## 全文（Introduction 至 Results）的写作检查

| 项目 | 结果 |
|---|---|
| banned_terms | {} |
| throat_clearing | {} |
| meta_commentary | {} |
| hedges | {} |
| methods_phrases_in_results | {} |
| bare_time_words | {} |
| causal_words | {} |
| em_dash | 0 |
| connectives_per_paragraph_max | 0 |
| sentences | 150 |
| sentences_over_30_words | [('I.4', 59, 'This study aimed to estimate, from the perspective of the Japanese pub'), ('I.4', 47, 'The secondary aims were to estimate the same cost when exercise is add')] |
| longest_sentence_words | 59 |
| paragraphs_over_150_words | {'I.4': 154} |
| words_by_section | {'Introduction': 581, 'Methods': 1507, 'Results': 866} |
| words_total | 2954 |
| sentences_joined_equal_docx | True |
| aims_sentence_with_This_study_aimed_to | True |
| gap_paragraph_First_Second | True |
| novelty_absolute_forms | 0 |
| outcome_first_sentence | True |
| variables_first_sentence | True |
| software_last_sentence | True |
| stages_numbered_1_to_6 | True |
| acronym_allow_list | {'JPY': 'Japanese yen (JPY), Introduction paragraph 1', 'TNBC': 'Triple-negative breast cancer (TNBC), Introduction paragraph 1', 'QALY': 'quality-adjusted life years (QALYs), Methods, Study background paragraph 2', 'ICER': 'incremental cost-effectiveness ratio (ICER), Methods, Outcome paragraph 2', 'PMC': 'database name Europe PMC', 'EQ': 'part of EQ-5D-5L, defined as EuroQol 5-dimension 5-level (EQ-5D-5L)'} |
| acronym_check_exit | 0 |

ARS check_acronyms.py（body 范围，Introduction 至 Results）：

```
### Acronym check (advisory; no reply needed)
Coverage: body (complete)
No findings.
```

## 表与图的首次引用（本文地の文）

| 项目 | 结果 |
|---|---|
| first_citation_order | ['Supplementary Table S1', 'Table 1', 'Supplementary Table S2', 'Fig. 1', 'Supplementary Methods S1', 'Supplementary Fig. S1', 'Supplementary Table S3', 'Fig. 2', 'Table 2', 'Table 3', 'Fig. 3', 'Supplementary Table S4', 'Supplementary Table S5', 'Supplementary Table S6', 'Supplementary Table S7', 'Supplementary Table S8', 'Supplementary Table S9', 'Supplementary Fig. S2', 'Supplementary Table S10'] |
| by_series | {'Supplementary Table': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'Table': [1, 2, 3], 'Fig.': [1, 2, 3], 'Supplementary Methods': [1], 'Supplementary Fig.': [1, 2]} |
| each_series_1_to_n_in_order | True |
| max_equals_count | {'Table': (3, 3), 'Fig.': (3, 3), 'Supplementary Table': (10, 10), 'Supplementary Fig.': (2, 2), 'Supplementary Methods': (1, 1)} |
| max_ok | True |
| supplement_physical_order | ['Supplementary Table S1', 'Supplementary Table S2', 'Supplementary Methods S1', 'Supplementary Fig. S1', 'Supplementary Table S3', 'Supplementary Table S4', 'Supplementary Table S5', 'Supplementary Table S6', 'Supplementary Table S7', 'Supplementary Table S8', 'Supplementary Table S9', 'Supplementary Fig. S2', 'Supplementary Table S10'] |
| supplement_physical_order_matches_first_citation | True |
| references_to_input_table | 10 |
| references_to_input_table_wrong_number | [] |

## 参考文献

| 项目 | 结果 |
|---|---|
| main_text_citation_runs | 51 |
| main_text_first_appearance_is_1_to_K | True |
| K_main_text | 62 |
| N_reference_list | 77 |
| list_numbered_1_to_N | True |
| list_text_equals_entries | True |
| outside_main_text_new_numbers_in_order | True |
| every_reference_cited | True |
| citations_to_numbers_beyond_list | [] |
| entries_with_doi | 61 |
| doi_resolved_at_doi_org | 61 |
| doi_problems | [] |
| entries_without_doi | ['jbcs55', 'price2026', 'c2h_list', 'c2h_guideline', 'mhlw_ce2026', 'worldbank_ppp', 'fee2026', 'lifetable2025', 'ema2022', 'pbac2023', 'tropion2025', 'boc_fx', 'jsco2023', 'hosp_kasugai', 'hosp_chuden', 'olaparib_pi'] |
| older_than_10_years | [(1, 'dent2007', 2007), (2, 'liedtke2008', 2008), (11, 'courneya2007', 2007), (12, 'vanwaart2015', 2015), (14, 'courneya2014', 2014), (49, 'guyot2012', 2012), (59, 'cortes2011', 2011), (65, 'miller2007', 2007)] |
| self_citations | [] |
| author_year_in_text | 0 |
| retracted | [] |

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
| Supplementary Table S2 & Table 1 | 26 | E2（S2 完整参数表与 Table 1；2026-10-26 决定） |
| Supplementary Table S4 & Table 2 | 6 | E1（Table 2 Panel B、C 的基准行与 S4；2026-10-26 决定） |
| Supplementary Table S7 & Table 2 | 4 | E3（S7 完整网格与 Table 2 Panel B 的 HR 0.85 两行；2026-10-26 接受，与 E1 同类） |
