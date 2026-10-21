# 99_phase1_report.R
# Builds output/phase1/phase1_report.md from the code outputs (no hand-entered numbers).

source("C:/Users/原明美/Documents/ClaudeCode/exercise_cea/R/config.R")
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
suppressPackageStartupMessages(library(survival))
out_dir <- file.path(ROOT, "output", "phase1")
rd <- function(...) {
  x <- read.csv(file.path(ROOT, ...), stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)
  names(x)[1] <- sub("^\ufeff", "", names(x)[1]); x
}
md_table <- function(df) {
  esc <- function(x) gsub("\\|", "\\\\|", ifelse(is.na(x), "", as.character(x)))
  c(paste0("| ", paste(names(df), collapse = " | "), " |"),
    paste0("|", paste(rep("---", ncol(df)), collapse = "|"), "|"),
    apply(df, 1, function(r) paste0("| ", paste(esc(r), collapse = " | "), " |")))
}
f2 <- function(x, d = 2) formatC(as.numeric(x), format = "f", digits = d)
istrue <- function(x) x %in% c(TRUE, "TRUE", "True")
# PubMed text uses non-breaking spaces in places (U+00A0), so they are normalised with the rest
abstract <- function(pmid) gsub("[\\s ]+", " ", perl = TRUE, paste(readLines(file.path(ROOT, "input", "params", "pubmed", paste0("PMID", pmid, ".txt")), encoding = "UTF-8", warn = FALSE), collapse = " "))

inv <- rd("output", "phase1", "inventory.csv")
apf <- rd("data", "appendix_figures.csv")
tck <- rd("data", "transcription_checks.csv")
V <- rd("output", "phase1", "validation.csv")
D <- rd("output", "phase1", "validation_diagnostics.csv")
vlog <- rd("data", "digitized", "vector_extraction_log.csv")
rlog <- rd("data", "digitized", "raster_extraction_log.csv")
man <- rd("data", "input_manifest.csv")
rv <- rd("data", "reported_values.csv")
us <- rd("input", "user_supplied_values.csv")
CC <- rd("output", "phase1", "consistency_check.csv")
M <- rd("output", "phase1", "model_comparison.csv")
SEL <- rd("output", "phase1", "model_selection.csv")
FAM <- rd("output", "phase1", "family_selection.csv")
YR <- rd("output", "phase1", "yau_landmark_reference.csv")
CAL <- rd("output", "phase1", "calibration.csv")
CG <- rd("output", "phase1", "calibration_gate.csv")
CS <- rd("output", "phase1", "calibration_status.csv")
CD <- rd("output", "phase1", "calibration_diagnostic.csv")
IMP <- rd("output", "phase1", "dr_survival_implied.csv")
EC <- rd("output", "phase1", "engine_checks.csv")
P <- engine_params(dr_shape = 1, dr_scale = 1)   # structure parameters (DR mortality not used here)
stop6 <- istrue(CS$stop_before_step6)

L <- character(0)
add <- function(...) L <<- c(L, ...)

add("# 第1阶段（生存引擎）报告", "",
    sprintf("生成时间：%s。由 `R/99_phase1_report.R` 从代码输出生成，表中数字均读自 `output/`、`data/` 与 `input/` 下的文件。模型规格见 `docs/model_spec.md`。",
            format(Sys.time(), "%Y-%m-%d %H:%M")), "")

# ---------------------------------------------------------------- status
gfail <- V[istrue(V$gate) & !istrue(V$pass), ]
add("## 状态", "",
    "- 已完成：步骤 1 至 4（含 2026-10-21 的修正：层内 HR 改为跨分析对照、5 年外推检验、同一层两臂同一分布族、第二原发癌归入局部区域复发）与一致性检查。",
    sprintf("- 重建与一致性的门槛项 %d 项，不达标 %d 项。", sum(istrue(V$gate)), nrow(gfail)),
    if (stop6) sprintf("- **步骤 5（校准）按 (a)、(b)、(c) 依次尝试，三步都未达到门槛（各臂 OS 在第 1 至 5 年的整年时点与 KM 差 ≤ 1 个百分点）。按规则停止，步骤 6、7 未进行。** 详见第 8 节。")
    else sprintf("- 步骤 5 采用结构 (%s)。", CS$chosen_structure), "")
if (stop6) {
  gs <- aggregate(cbind(max_abs_diff = abs(diff)) ~ structure + arm, data = CG, FUN = max)
  gs$failing_points <- sapply(seq_len(nrow(gs)), function(i) {
    x <- CG[CG$structure == gs$structure[i] & CG$arm == gs$arm[i] & !istrue(CG$pass), ]
    if (nrow(x) == 0) "无" else paste(sprintf("%d 个月 %s", x$month, f2(x$diff, 2)), collapse = "；")
  })
  add(md_table(transform(gs, max_abs_diff = f2(max_abs_diff, 3))), "")
}

add("## 1. 输入文件", "", md_table(man), "",
    "生命表：令和7(2025)年簡易生命表（女），`input/lifetable/SOURCE.md`、`data/lifetable_female_2025.csv`。用户提供与较晚截点的数值：`input/user_supplied_values.csv`。复发后生存的文献摘要：`input/params/pubmed/`。", "")

add("## 2. 清点表（`output/phase1/inventory.csv`）", "")
add(md_table(inv[, c("fig_key", "source", "figure", "location", "available", "format", "endpoint", "population", "analysis",
                     "data_cutoff", "median_fu_months", "time_origin", "landmark_at_surgery")]), "")
add(md_table(inv[, c("fig_key", "x_axis", "risk_times", "n", "events", "milestones", "hr")]), "")
add("EFS 首次事件构成：", "", md_table(inv[grepl("first events", inv$efs_event_composition), c("fig_key", "efs_event_composition")]), "")
add(sprintf("两份补充材料的全部图（%d 张，其中 KM 图 %d 张；2024 年补充材料没有按 pCR 分层的 EFS，故分层 EFS 与 pCR 比例都取 2022 年 IA4）：", nrow(apf), sum(istrue(apf$kaplan_meier))), "",
    md_table(apf[, c("pdf", "figure", "page", "title", "kaplan_meier", "by_pcr")]), "")
add(sprintf("栅格图中印的数字从图像转录，与正文文字层交叉核对 %d 项，不一致 %d 项（`data/transcription_checks.csv`）。报告值 %d 个由正则从 PDF 文字层抽取（`data/reported_values.csv`）。",
            nrow(tck), sum(!istrue(tck$match)), nrow(rv)), "")

add("## 3. 数字化（`data/digitized/`）", "",
    "矢量图：PyMuPDF `get_drawings()` 读取阶梯路径；x 轴用全部带标签刻度最小二乘，y 轴用 0% 与 100% 两端锚定（2024 年两图的 100% 刻度偏离等距，插图读数支持两端锚定）。",
    "", md_table(vlog[, c("fig_id", "arm", "legend_colour_matches_spec", "n_vertices", "n_censor_marks", "s_first", "t_last",
                          "calib_resid_x", "calib_resid_y", "inset_median_abs_diff")]), "",
    "栅格图：嵌入图像原生像素上的颜色分离（更高 dpi 栅格化只会插值）。线条用单调阶梯的动态规划追踪；Yau 的「+」删失标记上下对称，NEJM 补充材料的删失标记只向上延伸并在密集处连成色块，故追踪色块下沿；深色曲线的抗锯齿边缘会被分到同色系浅色曲线，浅色类在深色曲线 2 像素内的像素剔除。",
    "", md_table(rlog[, c("fig_id", "arm", "native_px", "dpi_as_placed", "column_coverage", "n_steps", "t_last", "s_last", "calib_resid_x", "calib_resid_y")]), "",
    "叠图质控：`data/digitized/qa/*_overlay.png`。", "")

add("## 4. 个体数据重建与验证（`output/phase1/validation.csv`）", "",
    "Guyot 2012 算法（`R/guyot.R`；`IPDfromKM::getIPD` 交叉核对）。重建时不输入报告的总事件数。门槛：里程碑差 ≤ 1 个百分点；Cox HR 差 ≤ 0.03；事件数差 ≤ 2%。",
    "",
    "不作门槛、只报告的项目：",
    "- Yau 2022 的 HR 与事件数（2026-10-21 的决定）。HR：原文出自 12 个队列汇总、含队列效应的模型并使用全部随访，重建数据只到 12 年、只能做单一 Cox，估计量不同。事件数：参照值是从风险表推算的 12 年累计事件数，原文没有报告。",
    sprintf("- 按 pCR 分层的 EFS 层内 HR 与较晚截点值（pCR %s [%s, %s]、non-pCR %s [%s, %s]）的跨分析对照。该参照值来自 2023-03-23 截点（中位随访 63.1 个月），比曲线所属的 IA4（2021-03-23）晚，IA4 的曲线不可能与之吻合；IA4 原文印的 0.73 与 0.70 已在 0.012 以内复现（见下表 K22_S4_EFS_pCR 的 hr 行）。出处暂记为 ESMO 2023 的会议报道（用户给出的网址现已重定向到网站首页；同一数值见 OncLive 2023-10-20 报道，引 Ann Oncol 2023;34(S2):S1256-S1257），待尾崎确认原始出处后替换。",
            us$value[us$id == "K522_EFS_HR_pCR"], us$lo[us$id == "K522_EFS_HR_pCR"], us$hi[us$id == "K522_EFS_HR_pCR"],
            us$value[us$id == "K522_EFS_HR_nonpCR"], us$lo[us$id == "K522_EFS_HR_nonpCR"], us$hi[us$id == "K522_EFS_HR_nonpCR"]), "")
Vt <- V[, c("curve", "check", "time", "unit", "reported", "reconstructed", "abs_diff", "tolerance", "pass", "gate", "reference")]
Vt$pass <- ifelse(istrue(Vt$pass), "达标", "**不达标**"); Vt$gate <- ifelse(istrue(Vt$gate), "是", "否（只报告）")
add(md_table(Vt), "")
add("诊断（不作门槛）：", "", md_table(D[, c("curve", "n", "events_guyot", "events_ipdfromkm", "max_abs_km_vs_digitized_pp",
                                         "max_abs_guyot_vs_ipdfromkm_pp", "max_abs_risk_table_diff", "censor_marks_drawn", "censored_guyot")]), "",
    "图：`fig_validation_*.png`。", "")

add("## 5. 一致性检查（`output/phase1/consistency_check.csv`）", "")
mx <- aggregate(cbind(max_abs_diff = abs(diff)) ~ arm + comparator, data = CC, FUN = max)
add(sprintf("2022 年 Fig. S4 的分层 KM 按 pCR 比例（帕博利珠单抗 %s，安慰剂 %s）加权混合，与整体 EFS 比较（3 至 %s 个月，四层在险均 ≥ 20），门槛 1 个百分点，不达标 %d 处。",
            f2(unique(CC$p_pCR[CC$arm == "pembro"]), 4), f2(unique(CC$p_pCR[CC$arm == "placebo"]), 4), max(CC$time_months), sum(!istrue(CC$pass))),
    "", md_table(transform(mx, max_abs_diff = f2(max_abs_diff, 3))), "", "图：`fig_consistency_pCR_mixture.png`。", "")

add("## 6. 拟合与模型选择（步骤 4）", "",
    sprintf("数据：4 条 EFS（2022 年 Fig. S4，臂 × pCR）在手术时点（随机化后 %d 个月）做 landmark；2 条 OS（2024 年 Fig. 1A，按臂）从随机化起。候选 15 个：6 个标准分布、6 个 RP 样条（1 至 3 个内结点，累积风险与累积比值尺度）、3 个相对生存混合治愈模型（Weibull、对数正态、对数 logistic；背景为日本女性生命表，治愈比例作用于超额死亡）。AIC/BIC 用全因对数似然，使治愈模型与全因模型可比。",
            CFG$landmark_months), "",
    "准则：",
    sprintf("1. 与 KM 的重合：模型曲线落在 KM 逐点 95%% CI 内的月份比例 ≥ %s（在险 ≥ %d 的时点）。最初设为 100%% 是设定错误：逐点 95%% 置信区间本来就预期约 5%% 的点落在区间外；首轮运行后已修正为 95%%。",
            CFG$fit_ci_min_inside, CFG$fit_ci_min_at_risk),
    sprintf("2. 风险形状：超额风险不晚于术后 %d 年达峰，3→5→10 年递减（EFS）；OS 为 5→10→20 年递减；10 年和 20 年的全因风险不低于背景。", CFG$hazard_peak_max_years),
    "3. 10 年、20 年外推与外部长期数据：Yau 2022 TNBC 在手术时点 landmark 后的条件 EFS S(10)/S(5)（pCR 对 RCB-0，非 pCR 对 RCB-1 至 3 合并）。下表列出，供参照。",
    sprintf("选择（2026-10-21 的决定）：EFS 同一 pCR 层两臂用同一分布族。两臂都满足 1 和 2 的族中，保留两臂合计 AIC 与最优者相差 ≤ %d 的族，再取 5 年外推检验中两臂差值绝对值之和最小的族；次优者保留为情景分析。OS 按臂取满足 1 和 2 的 AIC 最小者。", CFG$aic_window), "")
add("5 年外推检验（不作门槛）：所选分层 EFS 模型外推到随机化后 5 年（术前 KM × 术后模型），与较晚截点（2023-03-23）报告的 5 年分层 EFS 比较。", "")
ex5 <- M[istrue(M$selected) & grepl("^EFS", M$curve), c("curve", "model", "efs5_from_randomization", "efs5_later_cutoff", "efs5_diff")]
add(md_table(transform(ex5, efs5_from_randomization = f2(efs5_from_randomization, 2), efs5_diff = f2(efs5_diff, 2))), "")
add("各层的分布族比较（`family_selection.csv`，两臂都合格的族）：", "")
Ft <- FAM[istrue(FAM$eligible_both_arms), c("stratum", "model", "AIC_sum", "dAIC_sum", "within_aic_window", "efs5_diff_pembro", "efs5_diff_placebo", "efs5_abs_diff_sum", "selected", "scenario")]
Ft <- Ft[order(Ft$stratum, Ft$dAIC_sum), ]
add(md_table(Ft), "")
add("Yau 的参照值（`yau_landmark_reference.csv`）：", "", md_table(transform(YR, S5 = f2(S5, 4), S10 = f2(S10, 4), C5_10 = f2(C5_10, 4))), "")
add("选定的模型与理由（`model_selection.csv`；S5/S10/S20 为全因生存 %，EFS 为术后年数，OS 为随机化后年数）：", "",
    md_table(SEL[, c("curve", "model", "AIC", "S5", "S10", "S20", "cure_fraction", "efs5_diff", "scenario_model", "reason")]), "")
Mt <- M[istrue(M$converged), c("curve", "model", "AIC", "BIC", "c1_frac_inside_ci", "c1_max_abs_diff_pp", "c1_pass",
                               "peak_excess_haz_year", "c2_pass", "S5", "S10", "S20", "cond_5_10", "yau_cond_5_10", "efs5_diff", "selected", "scenario")]
add("全部候选（`model_comparison.csv`）：", "", md_table(Mt), "",
    "图：KM 与拟合曲线 `fig_fit_*.png`；超额风险与平滑后的 KM 风险 `fig_hazard_*.png`。", "")

add("## 7. 引擎结构参数", "")
comp <- do.call(rbind, lapply(names(P$composition), function(a) {
  x <- P$composition[[a]]
  data.frame(arm = a, any_event = x[["any"]], progression_precluding_surgery = x[["progression_precluding_surgery"]], local = x[["local"]],
             distant = x[["distant"]], second_primary = x[["second_primary"]], death = x[["death"]],
             second_primary_share_of_EFS_events_pct = f2(100 * x[["second_primary"]] / x[["any"]], 1),
             expected_background_deaths = f2(P$shares[[a]][["expected_background_deaths"]], 1),
             share_LRR = f2(P$shares[[a]][["LRR"]], 3), share_DR = f2(P$shares[[a]][["DR"]], 3), share_death = f2(P$shares[[a]][["death"]], 3))
}))
add("首发事件构成（2024 年 Table 1，IA7）与状态分配：无法手术的进展 → 远处复发（术前阶段，按非 pCR 层 KM 的形状）；局部区域复发与第二原发癌 → 局部区域复发；远处复发 → 远处复发；无复发死亡 → 死亡（扣除术后无事件人时中预期的背景死亡，因背景死亡单列）。", "",
    md_table(comp), "",
    sprintf("pCR 比例：帕博利珠单抗 %s，安慰剂 %s。局部区域复发 → 远处复发 %s/年（%d/%d 例，暴露 %s 年）。",
            f2(P$p_pcr[["pembro"]], 4), f2(P$p_pcr[["placebo"]], 4), f2(P$lrr_dr[["rate"]], 3),
            P$lrr_dr[["n_local_then_distant"]], P$lrr_dr[["n_local"]], f2(P$lrr_dr[["exposure_years"]], 2)), "")

add("## 8. 校准（步骤 5）", "",
    sprintf("目标：两臂 OS 与 2024 年 Fig. 1A 的 KM 在第 %d 至 %d 个月逐月的平方误差和最小。门槛：各臂 OS 在第 1 至 5 年的整年时点与 KM 差 ≤ 1 个百分点。顺序：(a) 事件按报告的构成分配（第 7 节），远处复发后的超额死亡率为常数、两臂共用（现有的 Weibull 隧道结构属于 (b)，所以 (a) 取不随复发后时间变化的形式）；(b) 远处复发后的超额死亡率随复发后时间变化（Weibull，隧道状态），两臂共用；(c) 同 (b)，两臂分别估计。前一步达标就停。",
            min(CFG$calib_grid_months), max(CFG$calib_grid_months)), "")
add(md_table(transform(CAL, SSE_both_arms = f2(SSE_both_arms, 2), rmse_pp = f2(rmse_pp, 3), max_abs_diff_pp = f2(max_abs_diff_pp, 3),
                       gate_max_abs_diff_pp = f2(gate_max_abs_diff_pp, 3), dr_shape = f2(dr_shape, 4), dr_scale = f2(dr_scale, 4),
                       dr_median_excess_years = f2(dr_median_excess_years, 3), starts_spread = signif(as.numeric(starts_spread), 2))), "")
add("门槛时点（`calibration_gate.csv`）：", "", md_table(transform(CG, km = f2(km, 2), engine = f2(engine, 2), diff = f2(diff, 3))), "")
add(sprintf("结果：%s", if (stop6) "三步都不达标。" else paste0("采用 (", CS$chosen_structure, ")。")), "")
d12 <- CD[CD$month == 12, ]
add("诊断（`calibration_diagnostic.csv`）：引擎在各时点的死亡（占全臂 %）按来源分解：背景死亡、术前事件（作为远处复发进入）后的死亡、术后事件后的死亡。", "",
    md_table(transform(CD[, c("structure", "arm", "month", "km_deaths_pct", "engine_deaths_pct", "background_pct", "after_presurgery_events_pct", "after_postsurgery_events_pct")])), "")
pre_share <- sapply(c("pembro", "placebo"), function(a) 100 * (1 - P$p_pcr[[a]]) * (1 - tail(P$pre_surv[[a]]$nonpCR$surv, 1)))
x <- d12[d12$structure == "c" & d12$arm == "placebo", ]
if (nrow(x) == 1)
  add(sprintf("安慰剂组 12 个月：KM 的死亡为 %s%%，结构 (c) 的引擎为 %s%%；其中术前事件（占安慰剂全臂 %s%%，按规定作为远处复发进入）之后的死亡就有 %s%%，已超过 KM 的全部死亡。只要术前进展与术后远处复发共用同一个复发后死亡率，安慰剂组第一年的 OS 就无法与 KM 吻合；帕博利珠单抗组则需要较高的早期死亡（12 个月 KM 死亡 %s%%）。",
              f2(x$km_deaths_pct, 2), f2(x$engine_deaths_pct, 2), f2(pre_share[["placebo"]], 2), f2(x$after_presurgery_events_pct, 2),
              f2(d12$km_deaths_pct[d12$structure == "c" & d12$arm == "pembro"], 2)), "")
es <- abstract("37385070"); ip <- abstract("38755096")
m1 <- regmatches(es, regexec("Median OS was ([\\d.]+) months \\(95% CI ([\\d.]+)-([\\d.]+)\\) in patients with early relapse versus ([\\d.]+) months \\(95% CI ([\\d.]+)-([\\d.]+)\\) in those with late relapse", es, perl = TRUE))[[1]]
m2 <- regmatches(ip, regexec("median ([\\d.]+) months with placebo versus ([\\d.]+) months with atezolizumab", ip, perl = TRUE))[[1]]
add("模型隐含的远处复发后生存（`dr_survival_implied.csv`，最后尝试的结构；中位为年）：", "", md_table(transform(IMP, surv_1y = f2(surv_1y, 3), surv_2y = f2(surv_2y, 3), surv_5y = f2(surv_5y, 3))), "",
    sprintf("文献对照：法国 ESME 全国队列，新辅助或辅助化疗结束后 12 个月内转移复发的 TNBC，中位 OS %s 个月（95%% CI %s 至 %s），12 个月以后复发为 %s 个月（Eur J Cancer 2023;189:112935，PMID 37385070）。IMpassion132，12 个月内复发的 PD-L1 阳性晚期 TNBC，中位 OS 安慰剂组 %s 个月、阿替利珠单抗组 %s 个月（Ann Oncol 2024;35:630-642，PMID 38755096）。模型隐含的中位明显短于这些值（结构 (b) 共用参数约 %s 年；结构 (c) 帕博利珠单抗臂的参数退化），说明校准得到的是吸收了结构偏差的有效参数。",
            m1[2], m1[3], m1[4], m1[5], m2[2], m2[3],
            f2(CAL$dr_median_excess_years[CAL$structure == "b"][1], 2)), "")
emx <- aggregate(cbind(max_abs_diff = abs(diff)) ~ check + arm, data = EC, FUN = max)
add(sprintf("未用于校准的曲线与引擎的对照（最后尝试的结构，`engine_checks.csv`）："), "", md_table(transform(emx, max_abs_diff = f2(max_abs_diff, 3))), "",
    "图：`fig_calibration_OS.png`（灰竖线为门槛时点）、`fig_engine_checks.png`。", "")

add("## 9. 已决事项与待决事项", "",
    "已决（2026-10-21）：",
    "- 层内 HR 的较晚截点参照值：撤出门槛，改为跨分析对照（第 4 节）。",
    "- 准则 1：保留 95%，最初 100% 为设定错误（第 6 节）。",
    "- 分布族：同一层两臂同一族，依两臂合计 AIC 与 5 年外推检验选定，次优族为情景（第 6 节）。",
    "- 第二原发癌：归入局部区域复发（第 7 节）。",
    "- 校准：按 (a)(b)(c) 依次尝试，加门槛（第 8 节）。",
    "",
    "待决：",
    "- **校准未达标后的处理**（第 8 节）。可选方向：（1）术前无法手术的进展与术后远处复发分开，给前者单独的死亡率或状态；（2）远处复发后的超额死亡率改用先升后降的形状（如对数 logistic），与文献的中位约 10 至 12 个月相符；（3）接受 (c)，在报告中写明安慰剂组 12 个月的偏差；（4）调整第 1 年的门槛。",
    "",
    "等尾崎回答：",
    "- S-JP 的权重定义（`docs/model_spec.md` 第 2 节）。",
    "- BRCA 检测的对象范围。",
    "- 帕博利珠单抗组是否也加 S-JP。", "")
add("## 10. 未进行的步骤", "", "步骤 6（bootstrap，B = 1000，含选定的校准结构）与步骤 7（生存引擎的最终输出：5、10、20 年 EFS 与 OS 等）。引擎已改为闭式计算（与逐周期递推一致，`R/test_engine_vectorized.R`），每次调用约 20 毫秒，可在校准结构确定后进行 bootstrap。", "")

writeLines(L, file.path(out_dir, "phase1_report.md"), useBytes = TRUE)
cat("wrote phase1_report.md:", length(L), "lines\n")
