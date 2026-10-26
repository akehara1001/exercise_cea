# v1 表图的回读检查（2026-10-26 15:24，`manuscript/code/make_ledger_v1.py`）

从交付的 docx 读回，不读生成脚本的中间结果。数字检查：从段落与单元格文字中抽出所有数字（与字母或连字符相连的编号如 E01、S1、EQ-5D、KEYNOTE-522 不算；“Table 2”“Fig. 3”“Supplementary Table S4”这类编号先去掉），逐个与登记表（数值行与定义/编号行）比对；反向检查登记的数值是否都出现在文档中。

### manuscript/v1/tables_v1.docx

| 项目 | 结果 | 应为 |
|---|---|---|
| paragraphs_and_cells | 304 |  |
| text_runs | 323 |  |
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
| numeric_tokens | 275 |  |
| unregistered_tokens | 0（无） | 0 |
| registered_values_not_found_in_document | 0（无） | 0 |
| sections | [('landscape', 297, 210), ('landscape', 297, 210), ('landscape', 297, 210)] | |

脚注符号（表内或题目中的上标 ↔ 脚注段落开头的符号）：

| 单位 | 表内/题目 | 脚注 | 一对一 | 顺序 |
|---|---|---|---|---|
| Table 1 | ✳ ✳✳ ✳✳✳ | ✳ ✳✳ ✳✳✳ | True | True |
| Table 2 | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | True | True |
| Table 3 | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | ✳ ✳✳ ✳✳✳ ✳✳✳✳ | True | True |

### manuscript/v1/figures_v1.docx

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

图（实测）：

| 图 | 像素 | 文件 dpi | 插入宽×高（mm） | 插入后的实际 dpi |
|---|---|---|---|---|
| Fig. 1 | 4015 x 2173 | [600.0, 600.0] | 169.97 × 91.99 | 600.0 |
| Fig. 2 | 4015 x 2456 | [600.0, 600.0] | 169.97 × 103.97 | 600.0 |
| Fig. 3 | 4015 x 3023 | [600.0, 600.0] | 169.97 × 127.97 | 600.0 |

nature-figure 的检查（导出的 PDF）：

- fig1 碰撞检查：PASS，{'fail': 0, 'warn': 0, 'contained_fill_overlays': 16, 'contained_image_overlays': 0}
- fig2 碰撞检查：PASS，{'fail': 0, 'warn': 0, 'contained_fill_overlays': 5, 'contained_image_overlays': 0}
- fig3 碰撞检查：PASS，{'fail': 0, 'warn': 0, 'contained_fill_overlays': 0, 'contained_image_overlays': 0}
- fig2 面板对齐：PASS，{'fail': 0, 'warn': 0, 'comparisons': 1, 'exemptions': 0}
- 字号下限（audit_pdf_text.py --min-pt 8）：三张图 below minimum 都为 0（见本次运行的终端输出，记录于 table_figure_plan_v1.md 第 7 节）。
