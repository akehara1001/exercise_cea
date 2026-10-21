# 99_phase1_report.R
# Builds output/phase1/phase1_report.md from the code outputs (no hand-entered numbers).
# Sections for steps that have not run yet are listed as not started.

root <- "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"
out_dir <- file.path(root, "output", "phase1")
rd <- function(...) read.csv(file.path(root, ...), stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)

inv <- rd("output", "phase1", "inventory.csv")
names(inv)[1] <- sub("^\ufeff", "", names(inv)[1])
V <- rd("output", "phase1", "validation.csv")
D <- rd("output", "phase1", "validation_diagnostics.csv")
vlog <- rd("data", "digitized", "vector_extraction_log.csv")
rlog <- rd("data", "digitized", "raster_extraction_log.csv")
man <- rd("data", "input_manifest.csv")
pcr <- rd("data", "pcr_counts.csv")
rv <- rd("data", "reported_values.csv")
val <- function(id, key) rv$value[rv$fact_id == id & rv$key == key]

md_table <- function(df) {
  esc <- function(x) gsub("\\|", "\\\\|", ifelse(is.na(x), "", as.character(x)))
  c(paste0("| ", paste(names(df), collapse = " | "), " |"),
    paste0("|", paste(rep("---", ncol(df)), collapse = "|"), "|"),
    apply(df, 1, function(r) paste0("| ", paste(esc(r), collapse = " | "), " |")))
}

fails <- V[!V$pass, ]
missing <- inv[inv$available == "no", ]
L <- character(0)
add <- function(...) L <<- c(L, ...)

add("# 第1阶段（生存引擎）报告", "",
    sprintf("生成时间：%s。本文件由 `R/99_phase1_report.R` 从代码输出生成，表中数字均读自 `output/phase1/` 与 `data/` 下的文件。",
            format(Sys.time(), "%Y-%m-%d %H:%M")), "")

add("## 状态：停在步骤 3（验证）", "",
    sprintf("- 步骤 1（清点）、2（数字化）、3（重建与验证）已完成。验证共 %d 项，%d 项不达标，全部来自 Yau 2022；按任务书规定停止，步骤 4–7 未开始。",
            nrow(V), nrow(fails)),
    sprintf("- KEYNOTE-522 的 %d 条曲线（%d 张图）全部达标。",
            length(unique(V$curve[startsWith(V$curve, "K") & V$check != "hr"])),
            length(unique(sub("_(pembro|placebo)$", "", V$curve[startsWith(V$curve, "K")])))),
    sprintf("- 另有 %d 张正文引用的补充材料 KM 图不在 `input/papers/`（%s），其中 %s 是模型核心输入（臂 × pCR 的 EFS）。",
            nrow(missing), paste(paste(missing$source, missing$figure), collapse = "；"),
            with(missing[grepl("pCR", missing$population) & missing$endpoint == "EFS", ], paste(source, figure, collapse = "、"))), "")

add("### 不达标项", "")
fd <- fails[, c("curve", "check", "time", "unit", "reported", "reconstructed", "abs_diff", "tolerance", "note")]
add(md_table(fd), "")

add("## 1. 输入文件", "", md_table(man), "",
    "生命表：令和7(2025)年簡易生命表（女），见 `input/lifetable/SOURCE.md` 与 `data/lifetable_female_2025.csv`。", "")

add("## 2. 清点表（`output/phase1/inventory.csv`）", "")
add(md_table(inv[, c("fig_key", "source", "figure", "location", "available", "format", "endpoint", "population",
                     "analysis", "data_cutoff", "median_fu_months", "time_origin", "landmark_at_surgery")]), "")
add("坐标轴、风险表时点、人数、事件数、里程碑与 HR：", "")
add(md_table(inv[, c("fig_key", "x_axis", "y_axis", "risk_times", "n", "events", "milestones", "hr")]), "")
add("EFS 首次事件构成：", "")
ec <- inv[inv$efs_event_composition != "n/a", c("fig_key", "efs_event_composition", "source_pages")]
add(md_table(ec), "")
add(sprintf("每个报告值的出处（页码与原文片段）见 `data/reported_values.csv`（%d 个值，正则从 PDF 正文抽取）。", nrow(rv)), "")

add("## 3. 数字化（`data/digitized/`）", "",
    "矢量图：PyMuPDF `get_drawings()` 直接读取阶梯路径坐标。x 轴用全部带标签刻度做最小二乘；y 轴用 0% 与 100% 两端刻度锚定（NEJM 2024 两图的 100% 刻度与 0–90% 刻度间距不一致，插图读数支持两端锚定，见 inset 列）。删失标记为同色短竖线。",
    "", md_table(vlog[, c("fig_id", "arm", "legend_colour_matches_spec", "n_vertices", "n_drops", "n_censor_marks",
                          "s_first", "t_last", "s_last", "calib_resid_x", "calib_resid_y",
                          "inset_median_abs_diff", "inset_max_abs_diff")]), "",
    sprintf("栅格图（Yau Fig. 4A）：嵌入图像为 %s，按原生像素做颜色分离（以 600 dpi 栅格化只会对该图插值，不增加信息）；线条水平用单调阶梯的动态规划追踪，以免密集删失标记把线条拉低。风险表与刻度值从图像转录（栅格无文字层），脚本检查了“人数 − 在险 − 累计删失”的单调性。",
            unique(rlog$native_px)), "",
    md_table(rlog[, c("arm", "n_pixels", "column_coverage", "n_steps", "t_last", "s_last", "calib_resid_x",
                      "calib_resid_y", "px_per_unit_x", "px_per_pct_y")]), "",
    "叠图质控：`data/digitized/qa/*_overlay.png`。", "")

add("## 4. 个体数据重建与验证（`output/phase1/validation.csv`）", "",
    "Guyot 2012 算法（`R/guyot.R`，按原文 R 代码实现；`IPDfromKM::getIPD` 用同一输入交叉核对）。重建时不输入报告总事件数，事件数检查因此不是循环验证。",
    "门槛：里程碑差 ≤ 1 个百分点；Cox HR 差 ≤ 0.03；事件数差 ≤ 2%。", "")
Vt <- V[, c("curve", "check", "time", "unit", "reported", "reconstructed", "abs_diff", "tolerance", "pass", "reference", "note")]
Vt$pass <- ifelse(Vt$pass, "达标", "**不达标**")
add(md_table(Vt), "")
add("诊断（不作门槛）：重建 KM 与数字化曲线的最大差、风险表再现、与 IPDfromKM 的差异，以及每个风险区间内“图上删失标记数/Guyot 删失数”。", "")
add(md_table(D), "")
add("图：`output/phase1/fig_validation_*.png`（灰线为数字化曲线，红虚线为重建个体数据的 KM，圆点为原文里程碑，竖线为 ±1 个百分点）。", "")

add("## 5. 需要决定的事项", "")
yf <- fails[startsWith(fails$curve, "Y22"), ]
add("1. **Yau 2022 不达标项的处理。**")
for (i in seq_len(nrow(yf)))
  add(sprintf("   - %s %s %s：原文 %s，重建 %s，差 %s（门槛 %s）。%s", yf$curve[i], yf$check[i],
              ifelse(is.na(yf$unit[i]) | yf$unit[i] == "", "", yf$unit[i]), yf$reported[i], yf$reconstructed[i],
              yf$abs_diff[i], yf$tolerance[i], yf$note[i]))
add("   - HR 两项：原文 HR 出自 12 个队列汇总、含队列效应的模型，用全部随访；重建数据只到 12 年、只能做单一 Cox，两者不是同一估计量。",
    "   - 事件数两项：参照值是由风险表推出的 12 年累计事件数（人数 − 在险 − 累计删失），差异来自 Guyot 对区间内删失均匀分布的假设；把数字化的下降惩罚改为 0.5 或 3.0，RCB-2 仍为同一事件数。",
    "   - Yau 在本模型中只用作外推的外部对照（步骤 4 的第③条），不进入模型参数。")
add(sprintf("2. **补充材料。** 需要 %s。NEJM 网站拒绝脚本下载（HTTP 403），需手动下载放入 `input/papers/`。",
            paste(paste0(missing$source, " ", missing$figure, "（", missing$endpoint, "，", missing$population, "）"), collapse = "；")))
p22 <- pcr[startsWith(pcr$source, "K22"), ]; p24 <- pcr[startsWith(pcr$source, "K24"), ]
add(sprintf("3. **pCR 比例的出处。** 正文的 pCR 亚组人数：%s 帕博利珠单抗组 %d/%d（%.1f%%）、安慰剂组 %d/%d（%.1f%%）；%s 为 %d/%d（%.1f%%）、%d/%d（%.1f%%）。“最终分析的全体 ITT 数值”取哪一版需确认。",
            p22$source, p22$pcr_pembro, p22$pcr_pembro + p22$nonpcr_pembro, 100 * p22$pcr_pembro / (p22$pcr_pembro + p22$nonpcr_pembro),
            p22$pcr_placebo, p22$pcr_placebo + p22$nonpcr_placebo, 100 * p22$pcr_placebo / (p22$pcr_placebo + p22$nonpcr_placebo),
            p24$source, p24$pcr_pembro, p24$pcr_pembro + p24$nonpcr_pembro, 100 * p24$pcr_pembro / (p24$pcr_pembro + p24$nonpcr_pembro),
            p24$pcr_placebo, p24$pcr_placebo + p24$nonpcr_placebo, 100 * p24$pcr_placebo / (p24$pcr_placebo + p24$nonpcr_placebo)))
add(sprintf("4. **队列起始年龄。** 基线表只给各臂中位数（帕博利珠单抗组 %s 岁，范围 %s；安慰剂组 %s 岁，范围 %s），没有全体中位数。",
            val("K20_age", "age_median_pembro"), val("K20_age", "age_range_pembro"),
            val("K20_age", "age_median_placebo"), val("K20_age", "age_range_placebo")), "")

add("## 6. 未开始的步骤", "",
    "步骤 4（参数与样条、治愈模型拟合）、5（远处复发后死亡率校准）、6（bootstrap B = 1000）、7（生存引擎函数）。", "")

writeLines(L, file.path(out_dir, "phase1_report.md"), useBytes = TRUE)
cat("wrote phase1_report.md:", length(L), "lines\n")
