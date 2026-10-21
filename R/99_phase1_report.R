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
# PubMed text uses non-breaking spaces in places, so they are normalised with the rest
abstract <- function(pmid) gsub("[\\s\\x{00A0}]+", " ", perl = TRUE,
  paste(readLines(file.path(ROOT, "input", "params", "pubmed", paste0("PMID", pmid, ".txt")), encoding = "UTF-8", warn = FALSE), collapse = " "))

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
NFR <- rd("output", "phase1", "nonpcr_family_review.csv")
YR <- rd("output", "phase1", "yau_landmark_reference.csv")
CAL <- rd("output", "phase1", "calibration.csv")
CG <- rd("output", "phase1", "calibration_gate.csv")
CS <- rd("output", "phase1", "calibration_status.csv")
RM <- rd("output", "phase1", "calibration_rmst.csv")
DS <- rd("output", "phase1", "calibration_deaths_by_source.csv")
IMP <- rd("output", "phase1", "dr_survival_implied.csv")
EC <- rd("output", "phase1", "engine_checks.csv")
CGR <- rd("output", "phase1", "calibration_gate_rmst.csv")
RS <- rd("output", "phase1", "calibration_rmst_by_source.csv")
AE <- rd("output", "phase1", "ae_deaths.csv")
CON <- rd("output", "phase1", "efs5_constraint.csv")
FSU <- rd("output", "phase1", "calibration_gate_feasibility_summary.csv")
FPT <- rd("output", "phase1", "calibration_gate_feasibility_points.csv")
CANDS <- readRDS(file.path(ROOT, "data", "fits", "calibration_candidates.rds"))
P <- CANDS$params
stop6 <- istrue(CS$stop_before_step6)
rvv <- function(id, key) rv$value[rv$fact_id == id & rv$key == key]
rvp <- function(id) paste0(rv$pdf[rv$fact_id == id][1], " p.", rv$page[rv$fact_id == id][1])
ipd <- readRDS(file.path(ROOT, "data", "ipd", "ipd_all.rds"))
se5 <- sapply(c(pembro = "pembro", placebo = "placebo"), function(a)
  100 * summary(survfit(Surv(time, status) ~ 1, data = ipd[[paste0("K24_F1A_OS_", a)]]), times = 60)$std.err)
n_os <- sapply(c(pembro = "pembro", placebo = "placebo"), function(a) nrow(ipd[[paste0("K24_F1A_OS_", a)]]))
ext_src <- "OncLive 2023-10-20 的报道与 Ann Oncol 2023;34(S2):S1256-S1257（ESMO 2023；数据截点 2023-03-23，中位随访 63.1 个月）"

L <- character(0)
add <- function(...) L <<- c(L, ...)

add("# 第1阶段（生存引擎）报告", "",
    sprintf("生成时间：%s。由 `R/99_phase1_report.R` 从代码输出生成，表中数字均读自 `output/`、`data/` 与 `input/` 下的文件。模型规格见 `docs/model_spec.md`。",
            format(Sys.time(), "%Y-%m-%d %H:%M")), "")

# ---------------------------------------------------------------- status
gfail <- V[istrue(V$gate) & !istrue(V$pass), ]
add("## 状态", "",
    "- 已完成：步骤 1 至 4（含 2026-10-21 与 2026-10-22 的修正）与一致性检查；非 pCR 层分布族已复核。",
    sprintf("- 重建与一致性的门槛项 %d 项，不达标 %d 项。", sum(istrue(V$gate)), nrow(gfail)),
    if (stop6) sprintf("- **步骤 5（校准第三轮，2026-10-22）未达到门槛：(a) 各臂 OS 在第 1 至 5 年整年时点落在重建 KM 的逐点 95%% 置信区间内——%s（区间外 %d 处）；(b) 5 年 OS 限制平均生存时间（RMST）的两臂之差，模型与 KM 的相对误差 ≤ %d%%——%s（模型 %s 年，KM %s 年，相对误差 %s%%）。按规则停止，步骤 6、7 未进行，未自行增加结构。** 各时点的差、两臂 RMST 差与死亡来源的拆解见第 8 节。",
                       if (istrue(CS$gate_a_pass)) "达标" else "不达标", sum(!istrue(CG$inside)), round(100 * CFG$gate_rmst_rel_tol),
                       if (istrue(CS$gate_b_pass)) "达标" else "不达标", f2(CGR$engine, 3), f2(CGR$km, 3), f2(100 * CGR$rel_error, 1))
    else "- 步骤 5 达标。",
    sprintf("- 在允许的参数范围内做了可行性扫描（只作诊断）：网格 %d 点加离网格的细化，没有一组参数能单独满足 (a)，也没有能同时满足 (a) 和 (b) 的参数；不达标来自结构与数据设定，不是目标函数的选择（第 8.5 节）。",
            FSU$grid_points), "")
add("门槛 (a)（`calibration_gate.csv`）：", "",
    md_table(transform(CG, km = f2(km, 2), ci95_lo = f2(ci95_lo, 2), ci95_hi = f2(ci95_hi, 2), engine = f2(engine, 2), diff = f2(diff, 3),
                       inside = ifelse(istrue(inside), "是", "**否**"))), "",
    "门槛 (b)（`calibration_gate_rmst.csv`；KM 差的 bootstrap 区间只报告，不作门槛）：", "",
    md_table(transform(CGR, km = f2(km, 4), km_boot_ci95_lo = f2(km_boot_ci95_lo, 4), km_boot_ci95_hi = f2(km_boot_ci95_hi, 4),
                       engine = f2(engine, 4), rel_error = f2(rel_error, 3), allowed_lo = f2(allowed_lo, 4), allowed_hi = f2(allowed_hi, 4),
                       pass = ifelse(istrue(pass), "达标", "**不达标**"))), "")

add("## 1. 输入文件", "", md_table(man), "",
    "生命表：令和7(2025)年簡易生命表（女），`input/lifetable/SOURCE.md`、`data/lifetable_female_2025.csv`。较晚截点的数值：`input/user_supplied_values.csv`。复发后生存的文献摘要：`input/params/pubmed/`。", "")

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
    sprintf("- 按 pCR 分层的 EFS 层内 HR 与较晚截点值（pCR %s [%s, %s]、non-pCR %s [%s, %s]）的跨分析对照。该参照值来自比 IA4（2021-03-23）晚的截点，IA4 的曲线不可能与之吻合；IA4 原文印的 0.73 与 0.70 已在 0.012 以内复现（下表 K22_S4_EFS_pCR 的 hr 行）。出处：%s，待尾崎确认原始出处后替换。",
            us$value[us$id == "K522_EFS_HR_pCR"], us$lo[us$id == "K522_EFS_HR_pCR"], us$hi[us$id == "K522_EFS_HR_pCR"],
            us$value[us$id == "K522_EFS_HR_nonpCR"], us$lo[us$id == "K522_EFS_HR_nonpCR"], us$hi[us$id == "K522_EFS_HR_nonpCR"], ext_src), "")
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
    "3. 10 年、20 年外推与外部长期数据：Yau 2022 TNBC 在手术时点 landmark 后的条件 EFS S(10)/S(5)（pCR 对 RCB-0，非 pCR 对 RCB-1 至 3 合并），列出供参照。",
    sprintf("选择：EFS 同一 pCR 层两臂用同一分布族。两臂都满足 1 和 2 的族中，保留两臂合计 AIC 与最优者相差 ≤ %d 的族，再取 5 年外推检验中两臂差值绝对值之和最小的族；次优者保留为情景分析。OS 按臂取满足 1 和 2 的 AIC 最小者。", CFG$aic_window), "")
add(sprintf("5 年外推检验（不作门槛）：所选分层 EFS 模型外推到随机化后 5 年（术前 KM × 术后模型），与较晚截点报告的 5 年分层 EFS 比较。外部数据出处：%s。", ext_src), "")
ex5 <- M[istrue(M$selected) & grepl("^EFS", M$curve), c("curve", "model", "efs5_from_randomization", "efs5_later_cutoff", "efs5_diff")]
add(md_table(transform(ex5, efs5_from_randomization = f2(efs5_from_randomization, 2), efs5_diff = f2(efs5_diff, 2))), "")
add(sprintf("5 年约束（2026-10-22，`efs5_constraint.csv`）：所选 EFS 模型在随机化后 60 个月的预测须落在较晚截点 5 年分层 EFS 的 95%% 置信区间内。报道没有给出置信区间，故用二项近似（Wald）：p ± %s × √(p(1 − p)/n)，n 为同一次 pCR 分析（IA4）的分层人数。此近似不考虑删失，比 KM 的区间窄，即约束偏严。超出区间时在较近的边界上重新最大化似然（治愈 Weibull 由形状与尺度推出治愈比例，Weibull 由形状推出尺度）；落在区间内则参数不变。约束对非 pCR 层（%s）与 pCR 层（%s）都检查。结果：四条曲线约束前都在区间内（%d/%d），约束不起作用，参数与外推不变；bootstrap 的各次重拟合同样带此约束。约束函数在人为移动边界时都能落到边界上（`R/test_efs5_constraint.R`）。",
            f2(CFG$efs5_ci_z, 3), CON$model[grepl("nonpCR", CON$curve)][1], CON$model[grepl("_pCR", CON$curve)][1],
            sum(istrue(CON$inside_before)), nrow(CON)), "",
    md_table(CON[, c("curve", "model", "n_stratum", "efs5_later_cutoff", "ci95_lo", "ci95_hi", "efs5_before", "binding", "efs5_after",
                     "efs10_before", "efs10_after", "efs20_before", "efs20_after", "pars_before", "pars_after")]), "",
    "（efs5/10/20：随机化后 5、10、20 年的 EFS %，术前 KM × 术后模型。）", "")
add("各层的分布族比较（`family_selection.csv`，两臂都合格的族）：", "")
Ft <- FAM[istrue(FAM$eligible_both_arms), c("stratum", "model", "AIC_sum", "dAIC_sum", "within_aic_window", "efs5_diff_pembro", "efs5_diff_placebo", "efs5_abs_diff_sum", "selected", "scenario")]
add(md_table(Ft[order(Ft$stratum, Ft$dAIC_sum), ]), "")
sel_np <- NFR$model[istrue(NFR$selected)][1]
pl_bias <- NFR$efs5_diff_placebo[istrue(NFR$selected)][1]
pe_bias <- NFR$efs5_diff_pembro[istrue(NFR$selected)][1]
add(sprintf("非 pCR 层分布族复核（2026-10-22，`nonpcr_family_review.csv`）：规则为若有某族两臂 5 年差都在 1 个百分点以内、且两臂合计 AIC 与最优族相差 ≤ %d，则基准改用该族。全部候选中满足者 %d 个（两臂 5 年差都在 1 个百分点以内的族 %d 个），故维持 %s。",
            CFG$aic_window, sum(istrue(NFR$review_pass)), sum(istrue(NFR$both_arms_within_1pt)), sel_np), "",
    md_table(NFR), "",
    sprintf("偏差的方向及其影响：%s 在安慰剂非 pCR 层的 5 年 EFS 比较晚截点的报告值低 %s 个百分点（帕博利珠单抗非 pCR 层 %s 个百分点）；所有候选在安慰剂非 pCR 层都是负偏差。安慰剂（单用化疗）组的 EFS 被低估，帕博利珠单抗相对于化疗的效果因此偏向高估。",
            sel_np, f2(abs(pl_bias), 2), f2(pe_bias, 2)), "")
add("Yau 的参照值（`yau_landmark_reference.csv`）：", "", md_table(transform(YR, S5 = f2(S5, 4), S10 = f2(S10, 4), C5_10 = f2(C5_10, 4))), "")
add("选定的模型与理由（`model_selection.csv`；S5/S10/S20 为全因生存 %，EFS 为术后年数，OS 为随机化后年数）：", "",
    md_table(SEL[, c("curve", "model", "AIC", "S5", "S10", "S20", "cure_fraction", "efs5_diff", "scenario_model", "reason")]), "")
Mt <- M[istrue(M$converged), c("curve", "model", "AIC", "BIC", "c1_frac_inside_ci", "c1_max_abs_diff_pp", "c1_pass",
                               "peak_excess_haz_year", "c2_pass", "S5", "S10", "S20", "cond_5_10", "yau_cond_5_10", "efs5_diff", "selected", "scenario")]
add("全部候选（`model_comparison.csv`）：", "", md_table(Mt), "",
    "图：KM 与拟合曲线 `fig_fit_*.png`；超额风险与平滑后的 KM 风险 `fig_hazard_*.png`。", "")

add("## 7. 引擎结构", "")
comp <- do.call(rbind, lapply(names(P$composition), function(a) {
  x <- P$composition[[a]]; n_arm <- x[["n_nonpCR"]] / (1 - P$p_pcr[[a]])
  data.frame(arm = a, any_event = x[["any"]], progression_precluding_surgery = x[["progression_precluding_surgery"]],
             preprog_share_of_arm_pct = f2(100 * P$q_pre[[a]][["nonpCR"]] * (1 - P$p_pcr[[a]]), 2),
             preprog_share_of_nonpCR_pct = f2(100 * P$q_pre[[a]][["nonpCR"]], 2),
             local = x[["local"]], distant = x[["distant"]], second_primary = x[["second_primary"]], death = x[["death"]],
             second_primary_share_of_EFS_events_pct = f2(100 * x[["second_primary"]] / x[["any"]], 1),
             expected_background_deaths = f2(P$shares[[a]][["expected_background_deaths"]], 1),
             ae_deaths = P$ae[[a]][["deaths"]],
             death_without_recurrence_used = f2(x[["death"]] - P$shares[[a]][["expected_background_deaths"]] - P$ae[[a]][["deaths"]], 1),
             share_LRR = f2(P$shares[[a]][["LRR"]], 3), share_DR = f2(P$shares[[a]][["DR"]], 3), share_death = f2(P$shares[[a]][["death"]], 3))
}))
add("状态：无事件、术前进展（2026-10-22 新增）、局部区域复发（含第二原发癌）、远处复发（复发后月数的隧道态）、死亡。首发事件构成（2024 年 Table 1，IA7）与分配：无法手术的进展 → 术前进展（比例为报告例数除以该臂非 pCR 人数，时间分布按非 pCR 层术前 KM 的形状）；局部区域复发与第二原发癌 → 局部区域复发；远处复发 → 远处复发；无复发死亡 → 死亡（扣除术后无事件人时中预期的背景死亡，因背景死亡单列；2026-10-22 起再扣除单列的因不良事件死亡）。", "",
    md_table(comp), "",
    sprintf("因不良事件死亡（2026-10-22，`ae_deaths.csv`）：%s 的 Table S5（%s；IA4，数据截点 %s）中「因不良事件死亡」的人数，帕博利珠单抗组 %s/%s，安慰剂组 %s/%s（安全性分析人群）。用这一次而不用最新报告（2024 年，IA7）的理由：2024 年正文只给出治疗相关不良事件导致的死亡（%s/%s，%s），没有全部因不良事件死亡的人数；而 2022 年与 2024 年正文都写明全部患者在 %s 前完成试验治疗（%s），IA4 之后不会再有治疗期内的不良事件死亡。两臂分别设定，在治疗期（术前加术后，%s 年）内以常数风险从无事件状态发生，pCR 层与非 pCR 层用同一风险，故不随 pCR 比例改变；不参与校准。术后部分属于 EFS 模型的超额风险，从中扣除（EFS 曲线不变），同时从构成中的无复发死亡扣除上述人数。情景：只计药物相关者（同表 %s/%s，与 2024 年正文的治疗相关死亡数相同），`config.R` 的 `ae_death_source = \"drug_related\"`。模型中 1 年内实际发生的因不良事件死亡占全臂：帕博利珠单抗 %s%%，安慰剂 %s%%（输入 %s%% 与 %s%%；术后风险上限起作用的周期数 %s，差值为同期其他事件的竞争）。",
            rv$pdf[rv$fact_id == "K22A_ae_deaths"][1], paste0("p.", rv$page[rv$fact_id == "K22A_ae_deaths"][1]), rvv("K22_cutoff", "data_cutoff"),
            rvv("K22A_ae_deaths", "died_pembro"), rvv("K22A_ae_deaths", "n_astreated_pembro"),
            rvv("K22A_ae_deaths", "died_placebo"), rvv("K22A_ae_deaths", "n_astreated_placebo"),
            rvv("K24_tr_deaths", "pembro"), rvv("K24_tr_deaths", "placebo"), rvp("K24_tr_deaths"),
            rvv("K22_treatment_end", "all_completed_by"), rvp("K22_treatment_end"), f2(P$ae_end, 0),
            rvv("K22A_ae_deaths", "died_drug_related_pembro"), rvv("K22A_ae_deaths", "died_drug_related_placebo"),
            f2(AE$engine_pct_by_1y[AE$arm == "pembro"], 3), f2(AE$engine_pct_by_1y[AE$arm == "placebo"], 3),
            f2(AE$input_pct[AE$arm == "pembro"], 3), f2(AE$input_pct[AE$arm == "placebo"], 3), sum(AE$post_surgery_cycles_capped)), "",
    sprintf("pCR 比例：帕博利珠单抗 %s，安慰剂 %s。局部区域复发 → 远处复发 %s/年（%d/%d 例，暴露 %s 年）。术前进展后的超额死亡率为常数，远处复发后的超额死亡为复发后时间的对数 logistic（形状在 (0, ∞) 内自由，中位限定 10 至 12 个月），两者两臂共用，由校准估计（第 8 节）。",
            f2(P$p_pcr[["pembro"]], 4), f2(P$p_pcr[["placebo"]], 4), f2(P$lrr_dr[["rate"]], 3),
            P$lrr_dr[["n_local_then_distant"]], P$lrr_dr[["n_local"]], f2(P$lrr_dr[["exposure_years"]], 2)), "")

add("## 8. 校准（步骤 5，第三轮，2026-10-22）", "")
add("### 8.1 门槛的更换与理由", "",
    sprintf("原门槛（各臂 OS 在第 1 至 5 年整年时点与 KM 差 ≤ 1 个百分点）改为 (a) 与 (b)（2026-10-22 的决定）。理由：1 个百分点小于 5 年 OS 本身的抽样误差——重建 KM 在 60 个月的 Greenwood 标准误，安慰剂组（n = %d）为 %s 个百分点，帕博利珠单抗组（n = %d）为 %s 个百分点——要求差 ≤ 1 个百分点会迫使拟合去追随噪声。(a) 用 KM 的逐点 95%% 置信区间（survfit 默认的对数尺度），与 EFS 拟合的准则 1 一致。(b) 以 5 年 RMST 的两臂之差为对象，直接针对后续成本效用分析所需的增量生命年；允许的相对误差为 ±%d%%。KM 差的 bootstrap 95%% 区间（在各臂内对重建个体数据重抽样，B = %d）只报告，不作门槛。",
            n_os[["placebo"]], f2(se5[["placebo"]], 2), n_os[["pembro"]], f2(se5[["pembro"]], 2), round(100 * CFG$gate_rmst_rel_tol), CGR$boot_B), "")
ab <- CANDS$at_bound
add("### 8.2 设定与校准结果", "",
    sprintf("结构（用户指定，一次运行，不逐步试）：%s。校准量：术前进展后的超额死亡率（常数，两臂共用）、远处复发后对数 logistic 的形状（在 (0, ∞) 内自由估计；数值上 log 形状限在 [log 0.01, log 50]）与中位（限定 10 至 12 个月），两臂共用。数据设定（不校准）：因不良事件死亡（第 7 节）、带 5 年约束的 EFS 模型（第 6 节）。目标函数不变：两臂 OS 与 2024 年 Fig. 1A 的 KM 在第 %d 至 %d 个月逐月的平方误差和最小（L-BFGS-B，%d 个起点，目标值差 %s）。",
            CANDS$structure, min(CFG$calib_grid_months), max(CFG$calib_grid_months), length(CANDS$starts_values), signif(diff(range(CANDS$starts_values)), 2)), "",
    md_table(transform(CAL, SSE_both_arms = f2(SSE_both_arms, 2), rmse_pp = f2(rmse_pp, 3), max_abs_diff_pp = f2(max_abs_diff_pp, 3),
                       gate_max_abs_diff_pp = f2(gate_max_abs_diff_pp, 3), preprog_rate = f2(preprog_rate, 4), dr_shape = f2(dr_shape, 4),
                       dr_median_years = f2(dr_median_years, 4))), "",
    sprintf("校准值：术前进展后的超额死亡率 %s/年%s；对数 logistic 形状 %s%s（%s）；中位 %s 个月%s。",
            f2(P$preprog_rate, 4), if (ab[["preprog_rate"]]) "（落在边界）" else "",
            f2(P$dr$shape, 4), if (ab[["dr_shape"]]) "（落在边界）" else "（在范围内部）",
            if (P$dr$shape < 1) "形状 < 1：复发后超额死亡风险从复发起单调递减" else "形状 > 1：风险先升后降",
            f2(12 * P$dr$scale, 2), if (ab[["dr_median"]]) "（落在下界 10 个月）" else ""), "")
add("### 8.3 各时点的差与死亡来源的拆解", "",
    "门槛 (a) 的逐时点表见文首「状态」。死亡来源（占全臂 %，`calibration_deaths_by_source.csv`）：", "",
    md_table(transform(DS, km_deaths = f2(km_deaths, 2), engine_deaths = f2(engine_deaths, 2), from_event_free = f2(from_event_free, 2),
                       from_ae = f2(from_ae, 2), from_preprog = f2(from_preprog, 2), from_LRR = f2(from_LRR, 3), from_DR = f2(from_DR, 2))), "")
x12 <- DS[DS$month == 12, ]
pre_share <- sapply(c("pembro", "placebo"), function(a) 100 * P$q_pre[[a]][["nonpCR"]] * (1 - P$p_pcr[[a]]))
gf <- CG[!istrue(CG$inside), ]
add(sprintf("区间外的时点：%s。",
            paste(sprintf("%s %d 个月（模型 %s，KM %s，95%% CI %s 至 %s）", ifelse(gf$arm == "pembro", "帕博利珠单抗", "安慰剂"), gf$month,
                          f2(gf$engine, 2), f2(gf$km, 2), f2(gf$ci95_lo, 2), f2(gf$ci95_hi, 2)), collapse = "；")),
    sprintf("12 个月：安慰剂组 KM 的死亡为 %s%%，模型为 %s%%，其中术前进展之后的死亡 %s%%（该组进入术前进展者占全臂 %s%%），单这一项已超过 KM 的全部死亡；帕博利珠单抗组 KM 为 %s%%，模型为 %s%%（因不良事件 %s%%，术前进展之后 %s%%，进入者占全臂 %s%%）。第 2 至 4 年帕博利珠单抗组的模型死亡少于 KM（OS 偏高，仍在区间内）。",
            f2(x12$km_deaths[x12$arm == "placebo"], 2), f2(x12$engine_deaths[x12$arm == "placebo"], 2), f2(x12$from_preprog[x12$arm == "placebo"], 2), f2(pre_share[["placebo"]], 2),
            f2(x12$km_deaths[x12$arm == "pembro"], 2), f2(x12$engine_deaths[x12$arm == "pembro"], 2), f2(x12$from_ae[x12$arm == "pembro"], 2),
            f2(x12$from_preprog[x12$arm == "pembro"], 2), f2(pre_share[["pembro"]], 2)), "")
add("### 8.4 两臂 RMST 差", "",
    "5 年 RMST（年，`calibration_rmst.csv`）：", "",
    md_table(transform(RM, rmst5_km = f2(rmst5_km, 4), rmst5_engine = f2(rmst5_engine, 4), diff = f2(diff, 4))), "")
rsd <- RS[RS$arm == "placebo - pembro", ]
add("模型 5 年内按死亡来源损失的 RMST（年，`calibration_rmst_by_source.csv`；RMST5 = 5 − 各来源之和，最后一行为各来源对模型两臂 RMST 差的贡献；KM 不能按来源拆分）：", "",
    md_table(data.frame(arm = RS$arm, lapply(RS[, -1], function(x) f2(x, 4)), check.names = FALSE)), "",
    sprintf("模型的两臂差 %s 年比 KM 的 %s 年大 %s 年（KM 差的 bootstrap 95%% 区间 %s 至 %s）。模型差中术前进展之后的死亡贡献 %s 年，远处复发后的死亡 %s 年，无事件状态中的死亡 %s 年，因不良事件死亡 %s 年（帕博利珠单抗组多，方向相反）。术前进展一项就与模型超出 KM 的部分相当：两臂进入术前进展的比例按报告值分别设定（全臂的 %s%% 对 %s%%），而其后的死亡率两臂共用。",
            f2(CGR$engine, 4), f2(CGR$km, 4), f2(CGR$engine - CGR$km, 4), f2(CGR$km_boot_ci95_lo, 4), f2(CGR$km_boot_ci95_hi, 4),
            f2(rsd$preprog, 4), f2(rsd$DR, 4), f2(rsd$event_free, 4), f2(rsd$ae, 4), f2(pre_share[["placebo"]], 2), f2(pre_share[["pembro"]], 2)), "")
fpf <- function(s) { x <- FPT[FPT$search == s & !istrue(FPT$inside), ]
  paste(sprintf("%s %d 个月（模型 %s，区间 %s 至 %s）", ifelse(x$arm == "pembro", "帕博利珠单抗", "安慰剂"), x$month,
                f2(x$engine, 2), f2(x$ci95_lo, 2), f2(x$ci95_hi, 2)), collapse = "；") }
fp1 <- FPT[FPT$search == "gate (a) only", ][1, ]; fp2 <- FPT[FPT$search == "gate (a) with gate (b) imposed", ][1, ]
exc <- function(x) max(pmax(x$ci95_lo - x$engine, x$engine - x$ci95_hi, 0))
add("### 8.5 门槛的可行性（只作诊断，`R/05b_gate_feasibility.R`）", "",
    sprintf("问题：在本结构与数据设定下，三个校准量取什么值能满足门槛？网格：术前进展超额死亡率 0.01 至 50/年与对数 logistic 形状 0.05 至 20 各 25 点（对数等距），中位 10、11、12 个月，共 %d 点；再从最好的网格点出发离网格细化（Nelder-Mead）。结果：满足 (a) 的 %d 点，满足 (b) 的 %d 点，两者都满足的 %d 点；细化后也没有满足 (a) 的参数（%s），没有两者都满足的参数（%s）。",
            FSU$grid_points, FSU$pass_a, FSU$pass_b, FSU$pass_both, if (istrue(FSU$refined_pass_a)) "有" else "无", if (istrue(FSU$refined_pass_both)) "有" else "无"),
    sprintf("- 只求 (a)：区间外最小的超出为 %s 个百分点（术前进展 %s/年，形状 %s，中位 %s 个月；RMST 差 %s 年）。仍在区间外的时点：%s。两臂朝相反方向偏离（帕博利珠单抗高于上限、安慰剂低于下限）。",
            f2(exc(FPT[FPT$search == "gate (a) only", ]), 3),
            f2(fp1$preprog_rate, 3), f2(fp1$dr_shape, 3), f2(fp1$dr_median_months, 2), f2(fp1$rmst_diff, 4), fpf("gate (a) only")),
    sprintf("- 同时要求 (b)：术前进展死亡率须降到 %s/年左右（RMST 差 %s 年）；此时区间外的时点：%s，都是帕博利珠单抗组高于上限，最大超出 %s 个百分点。",
            f2(fp2$preprog_rate, 3), f2(fp2$rmst_diff, 4), fpf("gate (a) with gate (b) imposed"), f2(exc(FPT[FPT$search == "gate (a) with gate (b) imposed", ]), 2)),
    "", "因此不达标来自结构与数据设定（两臂各自的术前进展比例、共用的死亡率、构成分配），而非目标函数的选择。按指示未改结构。", "",
    md_table(transform(FPT[, c("search", "arm", "month", "km", "ci95_lo", "ci95_hi", "engine", "diff", "inside")],
                       km = f2(km, 2), ci95_lo = f2(ci95_lo, 2), ci95_hi = f2(ci95_hi, 2), engine = f2(engine, 2), diff = f2(diff, 3),
                       inside = ifelse(istrue(inside), "是", "**否**"))), "")
es <- abstract("37385070"); ip <- abstract("38755096")
m1 <- regmatches(es, regexec("Median OS was ([\\d.]+) months \\(95% CI ([\\d.]+)-([\\d.]+)\\) in patients with early relapse versus ([\\d.]+) months \\(95% CI ([\\d.]+)-([\\d.]+)\\) in those with late relapse", es, perl = TRUE))[[1]]
m2 <- regmatches(ip, regexec("median ([\\d.]+) months with placebo versus ([\\d.]+) months with atezolizumab", ip, perl = TRUE))[[1]]
add("### 8.6 隐含的中位生存与外部对照", "",
    "模型隐含的中位生存（月，`dr_survival_implied.csv`；术前进展从 49.5 岁、远处复发从 50.5 岁计背景死亡）：", "",
    md_table(transform(IMP, median_excess_only_months = f2(median_excess_only_months, 1), median_all_cause_months = f2(median_all_cause_months, 1),
                       surv_1y = f2(surv_1y, 3), surv_2y = f2(surv_2y, 3))), "",
    sprintf("文献：ESME 全国队列，新辅助或辅助化疗结束后 12 个月内转移复发的 TNBC 中位 OS %s 个月（95%% CI %s 至 %s），12 个月以后复发为 %s 个月（Eur J Cancer 2023;189:112935，PMID 37385070）；IMpassion132，12 个月内复发的 PD-L1 阳性晚期 TNBC 中位 OS 安慰剂组 %s 个月、阿替利珠单抗组 %s 个月（Ann Oncol 2024;35:630-642，PMID 38755096）。远处复发后的中位由约束保持在此范围内。",
            m1[2], m1[3], m1[4], m1[5], m2[2], m2[3]), "")
emx <- aggregate(cbind(max_abs_diff = abs(diff)) ~ check + arm, data = EC, FUN = max)
add("### 8.7 未用于校准的曲线", "",
    "与引擎的对照（`engine_checks.csv`，各曲线全部时点中差的绝对值最大者，百分点）：", "", md_table(transform(emx, max_abs_diff = f2(max_abs_diff, 3))), "",
    "图：`fig_calibration_OS.png`（灰带为 KM 逐点 95% CI，竖线为门槛时点）、`fig_engine_checks.png`。", "")

add("## 9. 已决事项与待决事项", "",
    "已决：",
    "- 层内 HR 的较晚截点参照值：撤出门槛，改为跨分析对照（2026-10-21）。",
    "- 准则 1：保留 95%，最初 100% 为设定错误（2026-10-21）。",
    "- 分布族：同一层两臂同一族，依两臂合计 AIC 与 5 年外推检验选定，次优族为情景（2026-10-21）；非 pCR 层复核后维持（2026-10-22）。",
    "- 第二原发癌：归入局部区域复发（2026-10-21）。",
    "- 校准结构：术前进展单列（常数死亡率，两臂共用），远处复发后对数 logistic（两臂共用，中位 10 至 12 个月），不用两臂分别估计的复发后死亡率（2026-10-22）。",
    "- 校准第三轮（2026-10-22）：门槛改为 (a) KM 逐点 95% CI 与 (b) 5 年 RMST 两臂差相对误差 ≤ 20%；因不良事件死亡单列（数据设定，不校准）；对数 logistic 形状不再限定 > 1；非 pCR 层（及 pCR 层）EFS 加 5 年约束；术前进展的设定不变。",
    "",
    "待决：",
    if (stop6) sprintf("- **校准第三轮仍未达门槛**（第 8 节）：(a) 区间外 %d 处，(b) 模型 RMST 差 %s 年对 KM %s 年。可行性扫描显示本结构下没有参数能满足 (a)，更没有能同时满足 (a)、(b) 的参数；模型多出的 RMST 差主要来自术前进展（两臂进入比例按报告值分别设定、其后死亡率共用）。按指示未自行增加结构，处理方向待定。",
                       sum(!istrue(CG$inside)), f2(CGR$engine, 3), f2(CGR$km, 3)) else NULL,
    "- 若尾崎日后提供 2023-03-23 截点的分层 KM，5 年约束改为用整条曲线（2026-10-22 的决定）。",
    "",
    "等尾崎回答：",
    "- S-JP 的权重定义（`docs/model_spec.md` 第 2 节）。",
    "- BRCA 检测的对象范围。",
    "- 帕博利珠单抗组是否也加 S-JP。", "")
add("## 10. 未进行的步骤", "", "步骤 6（bootstrap，B = 1000：各臂 × pCR 层与 OS 的个体数据重抽样，重拟合选定的分布族并带 5 年约束，因不良事件死亡按设定，每次重新校准术前进展死亡率与对数 logistic）与步骤 7（生存引擎的最终输出：5、10、20 年 EFS 与 OS 等）。5 年约束函数已就绪并经测试（`R/test_efs5_constraint.R`）。引擎为闭式计算（与逐周期递推一致，`R/test_engine_vectorized.R`）。", "")

writeLines(L, file.path(out_dir, "phase1_report.md"), useBytes = TRUE)
cat("wrote phase1_report.md:", length(L), "lines\n")
