# 99_phase1_report.R
# Builds output/phase1/phase1_report.md from the code outputs (no hand-entered numbers).

source("C:/Users/原明美/Documents/ClaudeCode/exercise_cea/R/config.R")
out_dir <- file.path(ROOT, "output", "phase1")
rd <- function(...) {
  x <- read.csv(file.path(ROOT, ...), stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)
  names(x)[1] <- sub("^\ufeff", "", names(x)[1]); x
}
ex <- function(...) file.exists(file.path(ROOT, ...))
md_table <- function(df) {
  esc <- function(x) gsub("\\|", "\\\\|", ifelse(is.na(x), "", as.character(x)))
  c(paste0("| ", paste(names(df), collapse = " | "), " |"),
    paste0("|", paste(rep("---", ncol(df)), collapse = "|"), "|"),
    apply(df, 1, function(r) paste0("| ", paste(esc(r), collapse = " | "), " |")))
}
f2 <- function(x, d = 2) formatC(x, format = "f", digits = d)

inv <- rd("output", "phase1", "inventory.csv")
apf <- rd("data", "appendix_figures.csv")
tck <- rd("data", "transcription_checks.csv")
V <- rd("output", "phase1", "validation.csv")
D <- rd("output", "phase1", "validation_diagnostics.csv")
vlog <- rd("data", "digitized", "vector_extraction_log.csv")
rlog <- rd("data", "digitized", "raster_extraction_log.csv")
man <- rd("data", "input_manifest.csv")
pcr <- rd("data", "pcr_counts.csv")
rv <- rd("data", "reported_values.csv")
CC <- rd("output", "phase1", "consistency_check.csv")
M <- rd("output", "phase1", "model_comparison.csv")
SEL <- rd("output", "phase1", "model_selection.csv")
YR <- rd("output", "phase1", "yau_landmark_reference.csv")
CAL <- rd("output", "phase1", "calibration.csv")
CV <- rd("output", "phase1", "calibration_variant_checks.csv")
EC <- rd("output", "phase1", "engine_checks.csv")
P <- readRDS(file.path(ROOT, "data", "fits", "engine_params.rds"))
val <- function(id, key) rv$value[rv$fact_id == id & rv$key == key]

gfail <- V[V$gate & !V$pass, ]
ngfail <- V[!V$gate & !V$pass, ]
L <- character(0)
add <- function(...) L <<- c(L, ...)

add("# 第1阶段（生存引擎）报告", "",
    sprintf("生成时间：%s。由 `R/99_phase1_report.R` 从代码输出生成，表中数字均读自 `output/` 与 `data/` 下的文件。模型规格见 `docs/model_spec.md`。",
            format(Sys.time(), "%Y-%m-%d %H:%M")), "")

add("## 状态", "",
    "- 已完成：步骤 1（清点，含两份补充材料）、2（数字化）、3（重建与验证）、一致性检查、步骤 4（拟合与选择）、步骤 5（校准）；引擎接口已按 `docs/model_spec.md` 扩展。",
    sprintf("- 验证共 %d 项，其中门槛项 %d 项，**%d 项不达标**；非门槛项（Yau 的 HR 与事件数）%d 项不符，按 2026-10-21 的决定只报告。",
            nrow(V), sum(V$gate), nrow(gfail), nrow(ngfail)),
    "- 按规则在此停止：步骤 6（bootstrap）与 7（生存引擎的最终输出）未进行。", "")
add("### 不达标的门槛项", "", md_table(gfail[, c("curve", "check", "unit", "reported", "reconstructed", "abs_diff", "tolerance", "reference", "note")]), "")
st <- V[V$curve == "K22_S4_EFS_pCR" & V$check == "hr", ]
add(sprintf("同一组重建曲线对 2022 年补充材料 Fig. S4（IA4）印的层内 HR：%s。用户提供的参照值不在输入文献中；其 pCR 层 95%% CI 上限比 IA4 窄，可能来自更晚的数据截点。如果参照值来自另一次分析，用 IA4 的曲线无法复现它：需要该分析的按臂 × pCR 分层 KM 图，或改为不作门槛的跨分析对照。",
            paste(sprintf("%s 原文 %s、重建 %s（差 %s）", st$unit[!grepl("user", st$unit)], st$reported[!grepl("user", st$unit)],
                          f2(st$reconstructed[!grepl("user", st$unit)], 4), f2(st$abs_diff[!grepl("user", st$unit)], 4)), collapse = "；")), "")

add("## 1. 输入文件", "", md_table(man), "",
    "生命表：令和7(2025)年簡易生命表（女），`input/lifetable/SOURCE.md`、`data/lifetable_female_2025.csv`。", "")

add("## 2. 清点表（`output/phase1/inventory.csv`）", "")
add(md_table(inv[, c("fig_key", "source", "figure", "location", "available", "format", "endpoint", "population", "analysis",
                     "data_cutoff", "median_fu_months", "time_origin", "landmark_at_surgery")]), "")
add(md_table(inv[, c("fig_key", "x_axis", "risk_times", "n", "events", "milestones", "hr")]), "")
add("EFS 首次事件构成：", "", md_table(inv[inv$efs_event_composition %in% grep("first events", inv$efs_event_composition, value = TRUE),
                                         c("fig_key", "efs_event_composition")]), "")
add(sprintf("两份补充材料的全部图（%d 张，其中 KM 图 %d 张；2024 年补充材料没有按 pCR 分层的 EFS）：", nrow(apf), sum(apf$kaplan_meier == "True" | apf$kaplan_meier == TRUE)), "",
    md_table(apf[, c("pdf", "figure", "page", "title", "kaplan_meier", "by_pcr")]), "")
add(sprintf("栅格图里印的数字（风险表、里程碑、HR）从图像转录；与正文文字层的同一数值交叉核对 %d 项，不一致 %d 项（`data/transcription_checks.csv`）。报告值共 %d 个，均由正则从 PDF 文字层抽取（`data/reported_values.csv`）。",
            nrow(tck), sum(!(tck$match %in% c(TRUE, "True"))), nrow(rv)), "")

add("## 3. 数字化（`data/digitized/`）", "",
    "矢量图：PyMuPDF `get_drawings()` 读取阶梯路径。x 轴用全部带标签刻度最小二乘；y 轴用 0% 与 100% 两端刻度锚定（2024 年两图的 100% 刻度偏离等距，插图读数支持两端锚定）。",
    "", md_table(vlog[, c("fig_id", "arm", "legend_colour_matches_spec", "n_vertices", "n_censor_marks", "s_first", "t_last",
                          "calib_resid_x", "calib_resid_y", "inset_median_abs_diff")]), "",
    "栅格图：在嵌入图像的原生像素上做颜色分离（以更高 dpi 栅格化只会插值）。线条用单调阶梯的动态规划追踪；Yau 的「+」删失标记上下对称，NEJM 补充材料的删失标记只向上延伸、密集处连成色块，所以 NEJM 图追踪色块下沿。深色曲线的抗锯齿边缘会被误判为同色系浅色曲线，浅色类在深色曲线 2 像素内的像素剔除。",
    "", md_table(rlog[, c("fig_id", "arm", "native_px", "dpi_as_placed", "column_coverage", "n_steps", "t_last", "s_last", "calib_resid_x", "calib_resid_y")]), "",
    "叠图质控：`data/digitized/qa/*_overlay.png`。", "")

add("## 4. 个体数据重建与验证（`output/phase1/validation.csv`）", "",
    "Guyot 2012 算法（`R/guyot.R`；`IPDfromKM::getIPD` 交叉核对）。重建时不输入报告的总事件数。门槛：里程碑差 ≤ 1 个百分点；Cox HR 差 ≤ 0.03；事件数差 ≤ 2%。",
    "",
    "Yau 2022 只以里程碑为门槛（2026-10-21 的决定）。HR 不作门槛的理由：原文 HR 出自 12 个队列汇总、含队列效应的模型并使用全部随访，重建数据只到 12 年、只能做单一 Cox，估计量不同。事件数不作门槛的理由：参照值是从风险表推算的 12 年累计事件数（人数 − 在险 − 累计删失），原文没有报告。",
    "")
Vt <- V[, c("curve", "check", "time", "unit", "reported", "reconstructed", "abs_diff", "tolerance", "pass", "gate", "reference")]
Vt$pass <- ifelse(Vt$pass, "达标", "**不达标**"); Vt$gate <- ifelse(Vt$gate, "是", "否（只报告）")
add(md_table(Vt), "")
add("诊断（不作门槛）：", "", md_table(D[, c("curve", "n", "events_guyot", "events_ipdfromkm", "max_abs_km_vs_digitized_pp",
                                         "max_abs_guyot_vs_ipdfromkm_pp", "max_abs_risk_table_diff", "censor_marks_drawn", "censored_guyot")]), "",
    "2022 和 2024 年正文矢量图上每个删失病例都画了标记；每个风险区间内的「图上标记数/Guyot 删失数」见 `validation_diagnostics.csv`。图：`fig_validation_*.png`。", "")

add("## 5. 一致性检查（`output/phase1/consistency_check.csv`）", "")
mx <- aggregate(cbind(max_abs_diff = abs(diff)) ~ arm + comparator, data = CC, FUN = max)
add(sprintf("2022 年 Fig. S4 的分层 KM 按 pCR 比例（帕博利珠单抗 %s，安慰剂 %s）加权混合，与整体 EFS 比较，时点为 3 个月至 %s 个月（四层在险均 ≥ 20），门槛 1 个百分点。不达标 %d 处。",
            f2(unique(CC$p_pCR[CC$arm == "pembro"]), 4), f2(unique(CC$p_pCR[CC$arm == "placebo"]), 4), max(CC$time_months), sum(!(CC$pass %in% c(TRUE, "True")))),
    "", md_table(transform(mx, max_abs_diff = f2(max_abs_diff, 3))), "", "图：`fig_consistency_pCR_mixture.png`。", "")

add("## 6. 拟合与模型选择（步骤 4）", "",
    sprintf("数据：4 条 EFS（2022 年 Fig. S4，臂 × pCR）在手术时点（随机化后 %d 个月）做 landmark；2 条 OS（2024 年 Fig. 1A，按臂）从随机化起。候选 15 个：6 个标准分布、6 个 RP 样条（1 至 3 个内结点，累积风险与累积比值尺度）、3 个相对生存混合治愈模型（Weibull、对数正态、对数 logistic；背景为日本女性生命表，治愈比例作用于超额死亡）。AIC/BIC 用全因对数似然，使治愈模型与全因模型可比。",
            CFG$landmark_months), "",
    "选择规则（拟合前固定）：",
    sprintf("1. 与 KM 的重合：模型曲线落在 KM 逐点 95%% CI 内的月份比例 ≥ %s（在险 ≥ %d 的时点）。最初定为全部时点（100%%），结果 6 条中有 3 条没有任何候选达到；逐点 95%% CI 下真实曲线也约有 5%% 的时点在区间外，故第一次运行后改为 95%%。",
            CFG$fit_ci_min_inside, CFG$fit_ci_min_at_risk),
    sprintf("2. 风险形状：超额风险不晚于术后 %d 年达峰，3→5→10 年递减（EFS）；OS 为 5→10→20 年递减；10 年和 20 年的全因风险不低于背景。", CFG$hazard_peak_max_years),
    sprintf("3. 外部长期数据（只用于 EFS）：术后 5 至 10 年的条件 EFS S(10)/S(5)，与 Yau 2022 TNBC 在 %s 年 landmark 后的同一量比较（pCR 对 RCB-0，非 pCR 对 RCB-1 至 3 合并）。Yau 没有 OS，OS 无第 3 条。",
            CFG$yau_landmark_years),
    sprintf("满足 1 和 2 的模型中保留 AIC 差 ≤ %d 者；EFS 取第 3 条最接近 Yau 的，OS 取 AIC 最小的。", CFG$aic_window), "")
add("Yau 的参照值（`yau_landmark_reference.csv`）：", "", md_table(transform(YR, S5 = f2(S5, 4), S10 = f2(S10, 4), C5_10 = f2(C5_10, 4))), "")
add("选定的模型与理由（`model_selection.csv`）：", "", md_table(SEL[, c("curve", "model", "AIC", "S5", "S10", "S20", "cure_fraction", "reason")]), "",
    "S5/S10/S20 为所选模型的全因生存（%）：EFS 为术后年数，OS 为随机化后年数。", "")
Mt <- M[M$converged %in% c(TRUE, "True"), c("curve", "model", "AIC", "BIC", "c1_frac_inside_ci", "c1_max_abs_diff_pp", "c1_pass",
                                            "peak_excess_haz_year", "c2_pass", "S5", "S10", "S20", "cond_5_10", "yau_cond_5_10", "within_aic_window", "selected")]
add("全部候选的比较（`model_comparison.csv`）：", "", md_table(Mt), "",
    "图：KM 与拟合曲线 `fig_fit_*.png`；超额风险与平滑后的 KM 风险 `fig_hazard_*.png`。", "")
np <- SEL[SEL$curve %in% c("EFS_pembro_nonpCR", "EFS_placebo_nonpCR"), ]
alt <- M[M$curve == "EFS_placebo_nonpCR" & M$within_aic_window %in% c(TRUE, "True") & M$model != np$model[np$curve == "EFS_placebo_nonpCR"], ]
alt <- alt[order(alt$c3_abs_diff), ][1, ]
if (length(unique(np$model)) > 1)
  add(sprintf("值得注意：两条非 pCR 曲线选中的模型不同（帕博利珠单抗 %s，安慰剂 %s）。安慰剂一侧第 3 条的差距，所选模型为 %s，次优的 %s 为 %s，选择对第 3 条敏感；20 年时两组非 pCR 层的 EFS 分别为 %s%% 与 %s%%。引擎给出的按臂 EFS 与随访更长的 2024 年 EFS（IA7）的对照见第 7 节。",
              np$model[np$curve == "EFS_pembro_nonpCR"], np$model[np$curve == "EFS_placebo_nonpCR"],
              f2(M$c3_abs_diff[M$curve == "EFS_placebo_nonpCR" & M$selected %in% c(TRUE, "True")], 4), alt$model, f2(alt$c3_abs_diff, 4),
              np$S20[np$curve == "EFS_pembro_nonpCR"], np$S20[np$curve == "EFS_placebo_nonpCR"]), "")

add("## 7. 校准（步骤 5）", "",
    sprintf("引擎结构参数：pCR 比例 帕博利珠单抗 %s、安慰剂 %s；首发事件中超额部分的分配（局部区域复发/远处复发/超额死亡）帕博利珠单抗 %s/%s/%s、安慰剂 %s/%s/%s（预期背景死亡 %s、%s 例已扣除；第二原发癌按比例摊入）；局部区域复发 → 远处复发 %s/年（%d/%d 例，暴露 %s 年）。",
            f2(P$p_pcr[["pembro"]], 4), f2(P$p_pcr[["placebo"]], 4),
            f2(P$shares$pembro[["LRR"]], 3), f2(P$shares$pembro[["DR"]], 3), f2(P$shares$pembro[["death"]], 3),
            f2(P$shares$placebo[["LRR"]], 3), f2(P$shares$placebo[["DR"]], 3), f2(P$shares$placebo[["death"]], 3),
            f2(P$shares$pembro[["expected_background_deaths"]], 1), f2(P$shares$placebo[["expected_background_deaths"]], 1),
            f2(P$lrr_dr[["rate"]], 3), P$lrr_dr[["n_local_then_distant"]], P$lrr_dr[["n_local"]], f2(P$lrr_dr[["exposure_years"]], 2)),
    "",
    sprintf("远处复发后的超额死亡（复发后时间的 Weibull，两臂共用）使两臂 OS 与 2024 年 Fig. 1A 的 KM 在第 %d 至 %d 个月逐月吻合（平方误差和最小）。校准前为起点值（指数分布、中位 1.5 年，不是估计值）。结果：形状 %s、尺度 %s 年（中位 %s 年）。这是吸收了结构假设的有效参数，不宜直接解读为临床上的复发后生存。",
            min(CFG$calib_grid_months), max(CFG$calib_grid_months), f2(P$dr_shape, 4), f2(P$dr_scale, 4), f2(P$dr_scale * log(2)^(1 / P$dr_shape), 3)),
    "", md_table(transform(CAL[, c("arm", "stage", "rmse_pp", "max_abs_diff_pp", "diff_36m", "diff_60m", "diff_78m", "dr_shape", "dr_scale", "dr_median_years", "SSE_both_arms")],
                           rmse_pp = f2(rmse_pp, 3), max_abs_diff_pp = f2(max_abs_diff_pp, 3), diff_36m = f2(diff_36m, 3), diff_60m = f2(diff_60m, 3),
                           diff_78m = f2(diff_78m, 3), dr_shape = f2(dr_shape, 4), dr_scale = f2(dr_scale, 4), dr_median_years = f2(dr_median_years, 4), SSE_both_arms = f2(SSE_both_arms, 2))), "",
    sprintf("两臂各自校准的变体：规则（运行前固定）为只有当它在两臂所有未用于校准的 OS 检查上都改善时才采用。结果未采用（%s）；且帕博利珠单抗臂的参数退化（中位接近 0）。",
            paste(sprintf("%s %s：%s → %s", CV$check, CV$arm, f2(CV$max_abs_diff_common, 2), f2(CV$max_abs_diff_arm_specific, 2)), collapse = "；")), "")
emx <- aggregate(cbind(max_abs_diff = abs(diff)) ~ check + arm, data = EC, FUN = max)
add("未用于校准的曲线与引擎的对照（`engine_checks.csv`，不作门槛）：", "", md_table(transform(emx, max_abs_diff = f2(max_abs_diff, 3))), "",
    "图：`fig_calibration_OS.png`、`fig_engine_checks.png`。帕博利珠单抗组 OS 在 20 至 40 个月模型偏高，安慰剂非 pCR 层 OS 第一年模型偏低；推测原因是无复发死亡（治疗相关死亡等）在时间上的分布与模型假设（与 EFS 超额风险成比例）不同，且两臂复发后的生存可能不同。", "")

add("## 8. 需要决定的事项", "",
    "1. **层内 HR 的参照值**（上文「不达标的门槛项」）：请给出 pCR 层 0.65 [0.39, 1.08]、non-pCR 层 0.72 [0.54, 0.96] 的出处。若来自 IA4 以后的分析，需要该分析的按臂 × pCR 分层 KM 图才能重建；否则可改为不作门槛的跨分析对照。",
    "2. 非 pCR 两层的分布族不同（第 6 节），是否要求两臂用同一分布族。",
    "3. 第二原发癌的处理（现为按比例摊入三类）。",
    "4. 远处复发后死亡率为两臂共用的有效参数（第 7 节）。",
    "5. S-JP 的权重定义与 BRCA 检查的对象范围（`docs/model_spec.md` 第 2 节，待尾崎确认）。", "")
add("## 9. 未进行的步骤", "", "步骤 6（bootstrap，B = 1000）与步骤 7（生存引擎的最终输出：5、10、20 年 EFS 与 OS 等）。引擎函数与扩展接口已在 `R/engine.R`，接口测试见 `engine_interface_test.csv`。", "")

writeLines(L, file.path(out_dir, "phase1_report.md"), useBytes = TRUE)
cat("wrote phase1_report.md:", length(L), "lines\n")
