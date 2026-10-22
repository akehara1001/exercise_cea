# 99_phase1_report.R
# Builds output/phase1/phase1_report.md from the code outputs (no hand-entered numbers).

source("C:/Users/原明美/Documents/ClaudeCode/exercise_cea/R/config.R")
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
source(file.path(ROOT, "R", "calibration.R"))
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
OA <- rd("output", "phase1", "scenario_k1.csv")
OG <- rd("output", "phase1", "scenario_k1_gate.csv")
EIT <- rd("output", "phase1", "engine_interface_test.csv")
opt <- function(...) if (file.exists(file.path(ROOT, ...))) rd(...) else NULL
BSUM <- opt("output", "phase1", "bootstrap_summary.csv")
EO <- opt("output", "phase1", "engine_outputs.csv")
RB <- opt("output", "phase1", "bootstrap_rebuild_check.csv")
BRS <- if (file.exists(file.path(ROOT, "data", "bootstrap", "boot_replicates.rds"))) readRDS(file.path(ROOT, "data", "bootstrap", "boot_replicates.rds")) else NULL
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
boot_done <- !is.null(BRS) && !is.null(EO) && "pembro_dr_k" %in% colnames(BRS$calibration)
pp_bound_txt <- function(ab) {
  x <- c(if (ab[["pp_median_low"]]) "中位 = 10 个月" else NULL, if (ab[["pp_median_high"]]) "中位 = 26 个月" else NULL,
         if (ab[["pp_s5_at_min"]]) "5 年存活 = 5%" else NULL)
  if (length(x)) paste0("贴在约束边界上（", paste(x, collapse = "，"), "）") else "不在约束边界上"
}
G_out <- CG[!istrue(CG$inside), ]
add("## 状态", "",
    "- 已完成：步骤 1 至 4（含 2026-10-21 与 2026-10-22 的修正）与一致性检查；非 pCR 层分布族已复核。",
    sprintf("- 重建与一致性的门槛项 %d 项，不达标 %d 项。", sum(istrue(V$gate)), nrow(gfail)),
    sprintf("- 步骤 5（校准第六轮，2026-10-22）：按运行前确定的接受规则（`docs/acceptance_rule_round6.md`，git a53afe2）%s。门槛 (a)：10 个点中 %d 个落在逐点 95%% 区间内%s；门槛 (b)：模型的 5 年 RMST 两臂差 %s 年，%s KM 差（%s 年）的 bootstrap 95%% 区间 %s 至 %s 年内。",
            if (stop6) "**不接受，停止**" else "**接受**", sum(istrue(CG$inside)),
            if (nrow(G_out)) sprintf("，区间外 %d 处（%s），超出幅度 %s 个百分点，均 ≤ %g 且全部 10 个点落在 Bonferroni 校正后的逐点 99.5%% 区间内%s",
                                     nrow(G_out), paste(sprintf("%s %d 个月", ifelse(G_out$arm == "pembro", "帕博利珠单抗", "安慰剂"), G_out$month), collapse = "、"),
                                     paste(f2(G_out$outside_pp, 3), collapse = "、"), CFG$gate_accept_max_outside_pp,
                                     if (istrue(CS$gate_a_accepted)) "，按规则 (i)、(ii) 接受" else "") else "",
            f2(CGR$engine, 4), if (istrue(CGR$pass)) "落在" else "不在", f2(CGR$km, 4), f2(CGR$km_boot_ci95_lo, 4), f2(CGR$km_boot_ci95_hi, 4)),
    sprintf("- 帕博利珠单抗组远处复发后死亡风险的倍数 k = %s（范围 0.25 至 4，%s）。术前进展后死亡的校准值%s。",
            f2(P$pembro_dr_k, 3), if (istrue(CS$k_at_bound)) "**贴边界**" else "不在边界上", pp_bound_txt(CANDS$at_bound)),
    if (!stop6 && boot_done) sprintf("- 步骤 6（bootstrap，B = %d，k 在每个样本中一起估计）与步骤 7（引擎输出）已完成（第 9、10 节）。", BRS$B)
    else if (!stop6) "- 步骤 6、7 尚未完成。" else NULL,
    "- 门槛的修改经过见下一节「门槛修改记录」（全部六项）。", "")
dir_pem <- all(CG$diff[CG$arm == "pembro"] > 0); dir_pl <- all(CG$diff[CG$arm == "placebo"] < 0)
add(sprintf("各时点的方向：帕博利珠单抗组模型减 KM 的差在 %d 个时点中 %d 个为正，安慰剂组 %d 个中 %d 个为负%s。",
            sum(CG$arm == "pembro"), sum(CG$diff[CG$arm == "pembro"] > 0), sum(CG$arm == "placebo"), sum(CG$diff[CG$arm == "placebo"] < 0),
            if (dir_pem && dir_pl) "，方向一致" else ""), "")
add("门槛 (a)（`calibration_gate.csv`；ci995 为 Bonferroni 校正后的逐点 99.5% 区间，outside_pp 为落在 95% 区间外的幅度）：", "",
    md_table(transform(CG, km = f2(km, 2), ci95_lo = f2(ci95_lo, 2), ci95_hi = f2(ci95_hi, 2), ci995_lo = f2(ci995_lo, 2), ci995_hi = f2(ci995_hi, 2),
                       engine = f2(engine, 2), diff = f2(diff, 3), inside = ifelse(istrue(inside), "是", "**否**"),
                       outside_pp = f2(outside_pp, 3), inside_995 = ifelse(istrue(inside_995), "是", "**否**"))), "",
    "门槛 (b)（`calibration_gate_rmst.csv`）：", "",
    md_table(data.frame(quantity = CGR$quantity, km = f2(CGR$km, 4), km_boot_ci95_lo = f2(CGR$km_boot_ci95_lo, 4),
                        km_boot_ci95_hi = f2(CGR$km_boot_ci95_hi, 4), boot_B = CGR$boot_B, engine = f2(CGR$engine, 4),
                        engine_minus_km = f2(CGR$engine_minus_km, 4), pass = ifelse(istrue(CGR$pass), "达标", "**不达标**"))), "")

# ---------------------------------------------------------------- gate change log
yau_fail <- V[grepl("^Y22", V$curve) & !istrue(V$pass), ]
c1_none <- sum(tapply(istrue(M$c1_pass_all_points[istrue(M$converged)]), M$curve[istrue(M$converged)], function(x) !any(x)))
shr_p <- V[V$check == "hr" & grepl("^pCR [(]later", V$unit), ][1, ]
band_r3 <- 2 * CFG$gate_rmst_rel_tol_round3 * CGR$km
LOG <- data.frame(
  no = 1:6,
  date = c("2026-10-21", "2026-10-21", "2026-10-21", "2026-10-22", "2026-10-22", "2026-10-22"),
  item = c("Yau 2022 的重建验证", "拟合准则 1（选模）", "按 pCR 分层的 EFS 层内 HR（较晚截点的参照值）", "校准门槛", "校准门槛 (b)", "校准门槛 (a) 的接受条件"),
  before = c("里程碑差 ≤ 1 个百分点、HR 差 ≤ 0.03、事件数差 ≤ 2% 三项都作门槛",
             "模型落在 KM 逐点 95% CI 内的月份比例 = 100%",
             "与参照值的差 ≤ 0.03（门槛）",
             sprintf("各臂第 1 至 5 年整年时点 OS 与 KM 的差 ≤ %g 个百分点", CFG$gate_pp_round1_2),
             sprintf("5 年 RMST 两臂差：模型与 KM 的相对误差 ≤ %d%%（允许 %s 至 %s 年）", round(100 * CFG$gate_rmst_rel_tol_round3),
                     f2(CGR$km * (1 - CFG$gate_rmst_rel_tol_round3), 3), f2(CGR$km * (1 + CFG$gate_rmst_rel_tol_round3), 3)),
             "(a) 10 个点全部落在逐点 95% CI 内"),
  after = c("只保留里程碑为门槛；HR 与事件数只报告",
            sprintf("≥ %g%%", 100 * CFG$fit_ci_min_inside),
            "不作门槛的跨分析对照",
            sprintf("(a) 各臂第 1 至 5 年整年时点落在 KM 逐点 95%% CI 内；(b) 5 年 RMST 两臂差相对误差 ≤ %d%%", round(100 * CFG$gate_rmst_rel_tol_round3)),
            "(b) 模型的 5 年 RMST 两臂差落在 KM 差的 bootstrap 95% 区间内；点估计差距照常报告",
            sprintf("(a) 不达标时，同时满足 (i) 每个区间外的点超出 ≤ %g 个百分点、(ii) 全部 10 个点落在 Bonferroni 校正后的逐点 %g%% 区间内则接受；(b) 不变",
                    CFG$gate_accept_max_outside_pp, 100 * CFG$gate_accept_simultaneous_level)),
  timing = c(rep("看到结果后修改", 5), "看到第五轮结果之后、第六轮运行之前确定（git a53afe2 提交于运行前）"),
  result_seen = c(sprintf("Yau 有 %d 项不达标（事件数 %d 项、HR %d 项）", nrow(yau_fail), sum(yau_fail$check == "events"), sum(yau_fail$check == "hr")),
                  sprintf("6 条曲线中 %d 条没有任何候选模型通过", c1_none),
                  sprintf("pCR 层重建 %s 对参照 %s，差 %s", f2(shr_p$reconstructed, 3), f2(shr_p$reported, 2), f2(shr_p$abs_diff, 3)),
                  "第一轮（2026-10-21）与第二轮（2026-10-22）校准都不达标",
                  "第三轮校准不达标（(a) 与 (b) 都不达标）",
                  "第五轮门槛 (a) 不达标（有点落在逐点 95% 区间外）"),
  reason = c("HR 的估计量与原文不同（原文为 12 个队列、含队列效应的汇总模型，使用全部随访；重建只能在 12 年内做单一 Cox）；事件数的参照值从风险表推算，原文没有报告",
             "设定错误：逐点 95% 置信区间本来就预期约 5% 的点落在区间外",
             "参照值来自比 IA4 更晚的数据截点，IA4 的曲线不可能与之吻合；IA4 原文印的 0.73 与 0.70 已在 0.012 以内复现",
             sprintf("门槛比抽样误差更严：%g 个百分点小于安慰剂组（n = %d）5 年 OS 的 Greenwood 标准误 %s 个百分点", CFG$gate_pp_round1_2,
                     n_os[["placebo"]], f2(se5[["placebo"]], 2)),
             sprintf("门槛比抽样误差更严：允许带宽 %s 年，远窄于 KM 差的 bootstrap 95%% 区间宽度 %s 年", f2(band_r3, 3),
                     f2(CGR$km_boot_ci95_hi - CGR$km_boot_ci95_lo, 3)),
             sprintf("10 个时点各按 95%% 检验，即使模型正确，也有相当大的概率至少一点落在区间外（若各点独立为 %s%%；同一臂的各时点正相关，实际略低）",
                     f2(100 * (1 - 0.95^10), 0))))
add("## 门槛修改记录", "",
    "按时间列出验证与校准门槛的每次修改。第 1 至 5 项是看到结果后修改的，第 4、5 项的理由是门槛比抽样误差更严；第 6 项在看到第五轮结果之后、第六轮运行之前确定，并在运行前提交到 git。", "",
    md_table(setNames(LOG, c("序号", "日期", "对象", "修改前", "修改后", "时点", "看到的结果", "理由"))), "")

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
    sprintf("pCR 比例：帕博利珠单抗 %s，安慰剂 %s。局部区域复发 → 远处复发 %s/年（%d/%d 例，暴露 %s 年）。术前进展后的超额死亡为进入后时间的对数 logistic（第五轮；形状与中位在外部约束下校准），远处复发后的超额死亡为复发后时间的对数 logistic（中位为外部输入，形状校准；帕博利珠单抗组另乘 k，k 一起校准），形状与中位两臂共用（第 8 节）。",
            f2(P$p_pcr[["pembro"]], 4), f2(P$p_pcr[["placebo"]], 4), f2(P$lrr_dr[["rate"]], 3),
            P$lrr_dr[["n_local_then_distant"]], P$lrr_dr[["n_local"]], f2(P$lrr_dr[["exposure_years"]], 2)), "")

add("## 8. 校准（步骤 5，第六轮，2026-10-22）", "")
el <- abstract("34247335"); es <- abstract("37385070")
e_n <- regmatches(el, regexec("Of (\\d+) patients treated with NST during the study period, (\\d+) \\(([\\d.]+)%\\) developed disease progression", el, perl = TRUE))[[1]]
e_fu <- regmatches(el, regexec("At a median live follow-up of (\\d+) months, ([\\d.]+)% were alive without disease", el, perl = TRUE))[[1]]
e_os <- regmatches(el, regexec("Median overall survival \\(OS\\) time for patients with progression was (\\d+) months", el, perl = TRUE))[[1]]
e_sx <- regmatches(el, regexec("Among patients who had surgery \\((\\d+), ([\\d.]+)%\\)", el, perl = TRUE))[[1]]
m1 <- regmatches(es, regexec("Median OS was ([\\d.]+) months \\(95% CI ([\\d.]+)-([\\d.]+)\\) in patients with early relapse versus ([\\d.]+) months \\(95% CI ([\\d.]+)-([\\d.]+)\\) in those with late relapse", es, perl = TRUE))[[1]]
imp <- function(k) rvv("IMP132_os", k); impm <- function(k) rvv("IMP132_os_mitt", k)
ab <- CANDS$at_bound
n_pp <- sum(sapply(P$composition, function(x) x[["progression_precluding_surgery"]]))
add("### 8.1 设定", "",
    sprintf("结构（用户指定，一次运行）：%s。", CANDS$structure),
    sprintf("- 远处复发后的超额死亡：对数 logistic，形状与中位两臂共用；中位为外部输入 %s 个月（ESME）。帕博利珠单抗组的风险为共用风险 × k，k 与其他参数一起校准（范围 %g 至 %g）。理由：用过帕博利珠单抗后复发，可选的有效治疗更少；在共用模型中帕博利珠单抗组各时点均偏高，第 2 年死亡偏少。",
            f2(12 * DR_MEDIAN_BASE, 1), CFG$pembro_dr_k_bounds[1], CFG$pembro_dr_k_bounds[2]),
    sprintf("- 术前进展后的超额死亡：进入后时间的对数 logistic，两臂共用，形状与中位校准；外部约束 1：中位 %g 至 %g 个月（下限为 ESME 早期复发的中位 OS %s 个月取整；上限为 Elmore 等 Ann Surg Oncol 2021;28:5477-5485、PMID 34247335 的新辅助治疗期间局部区域进展 %s 例的中位 OS %s 个月，该队列多数后来接受手术〔摘要写 %s 例、%s%%，按 %s 例计为 %s%%〕，比「无法手术的进展」轻，只作上界）；外部约束 2：进入后 5 年的全因存活 ≥ %g%%（同一篇中位随访 %s 个月时 %s%% 无病存活，向下取保守值），实现为形状的上限。",
            12 * PP_MEDIAN_BOUNDS[1], 12 * PP_MEDIAN_BOUNDS[2], m1[2], e_n[3], e_os[2], e_sx[2], e_sx[3], e_n[3],
            f2(100 * as.numeric(e_sx[2]) / as.numeric(e_n[3]), 1), 100 * PP_S5_MIN, e_fu[2], e_fu[3]),
    "- 其余设定不变：因不良事件死亡（第 7 节）；带 5 年约束的 EFS 模型（第 6 节）。",
    sprintf("- 校准：目标为两臂 OS 与 2024 年 Fig. 1A 的 KM 在第 %d 至 %d 个月逐月的平方误差和（L-BFGS-B，%d 个起点，目标值差 %s）。optim 返回码 52 时加 5 个随机起点取最优；基准校准的返回码为 %d。",
            min(CFG$calib_grid_months), max(CFG$calib_grid_months), length(CANDS$starts_values), signif(diff(range(CANDS$starts_values)), 2),
            CANDS$optim$convergence),
    "- 接受规则：运行前确定（2026-10-22，`docs/acceptance_rule_round6.md`，git a53afe2 提交于第六轮运行之前），见文首「状态」与「门槛修改记录」第 6 项。规则只含 (a)、(i)、(ii)、(b)；术前进展约束与 k 的边界照常报告，不作停止条件。", "",
    "概率敏感性分析中远处复发后中位的分布（`dr_median_draw()`）：两项研究的中位 OS 各取对数正态分布，均值为 log(报告的中位)，标准误 = (log 上限 − log 下限) / (2 × 1.96)，等权混合；bootstrap 中每个样本先抽中位，再校准其余参数。", "",
    md_table(transform(DR_MEDIAN_SOURCES, se_log = f2((log(hi) - log(lo)) / (2 * qnorm(0.975)), 4))), "",
    sprintf("IMpassion132 已用全文核对（`input/papers/PIIS0923753424001078.pdf` p.6，PD-L1 阳性人群）：安慰剂组中位 OS %s 个月（95%% CI %s 至 %s），与此前采用的值一致，分布无需修正。参考：mITT 人群安慰剂组为 %s 个月（%s 至 %s），未采用（主要分析为 PD-L1 阳性人群）。ESME 读自摘要（%s 个月，%s 至 %s）。",
            imp("median_placebo"), imp("lo_placebo"), imp("hi_placebo"), impm("median_placebo"), impm("lo_placebo"), impm("hi_placebo"), m1[2], m1[3], m1[4]), "")
add("### 8.2 校准结果", "",
    md_table(transform(CAL, SSE_both_arms = f2(SSE_both_arms, 2), rmse_pp = f2(rmse_pp, 3), max_abs_diff_pp = f2(max_abs_diff_pp, 3),
                       gate_max_abs_diff_pp = f2(gate_max_abs_diff_pp, 3), preprog_shape = f2(preprog_shape, 4),
                       preprog_median_months = f2(preprog_median_months, 2), preprog_shape_cap = f2(preprog_shape_cap, 4),
                       dr_shape = f2(dr_shape, 4), dr_median_months = f2(dr_median_months, 2), pembro_dr_k = f2(pembro_dr_k, 4))), "",
    sprintf("k = %s（%s）。远处复发后：形状 %s，中位 %s 个月（外部输入）。",
            f2(P$pembro_dr_k, 3), if (ab[["k_low"]] || ab[["k_high"]]) "**贴边界**" else "在 0.25 至 4 的内部", f2(P$dr$shape, 3), f2(12 * P$dr$scale, 1)),
    sprintf("术前进展后：对数 logistic 形状 %s（该中位下的上限 %s），中位 %s 个月。中位%s；5 年存活%s。进入术前进展后的全因存活：1 年 %s，2 年 %s，5 年 %s（`dr_survival_implied.csv`）。",
            f2(P$preprog$shape, 3), f2(pp_shape_cap(P$preprog$scale), 3), f2(12 * P$preprog$scale, 2),
            if (ab[["pp_median_low"]]) "**贴下界 10 个月**" else if (ab[["pp_median_high"]]) "**贴上界 26 个月**" else "离开边界（在 10 至 26 个月内部）",
            if (ab[["pp_s5_at_min"]]) "**仍贴下界 5%（形状等于上限）**" else "高于 5%（离开边界）",
            f2(IMP$surv_1y[IMP$state == "PreProg"], 3), f2(IMP$surv_2y[IMP$state == "PreProg"], 3), f2(IMP$surv_5y[IMP$state == "PreProg"], 3)), "")
add("### 8.3 死亡来源与 RMST", "",
    "死亡来源（占全臂 %，`calibration_deaths_by_source.csv`）：", "",
    md_table(transform(DS, km_deaths = f2(km_deaths, 2), engine_deaths = f2(engine_deaths, 2), from_event_free = f2(from_event_free, 2),
                       from_ae = f2(from_ae, 2), from_preprog = f2(from_preprog, 2), from_LRR = f2(from_LRR, 3), from_DR = f2(from_DR, 2))), "",
    "5 年 RMST（年，`calibration_rmst.csv`）：", "",
    md_table(transform(RM, rmst5_km = f2(rmst5_km, 4), rmst5_engine = f2(rmst5_engine, 4), diff = f2(diff, 4))), "",
    "模型 5 年内按死亡来源损失的 RMST（年，`calibration_rmst_by_source.csv`；最后一行为各来源对模型两臂 RMST 差的贡献）：", "",
    md_table(data.frame(arm = RS$arm, lapply(RS[, -1], function(x) f2(x, 4)), check.names = FALSE)), "")
add("### 8.4 情景「k = 1」（复发后死亡率两臂共用）", "",
    sprintf("帕博利珠单抗组用 k = 1，其余参数取基准校准值；用于所有涉及帕博利珠单抗的比较，与基准并列报告（原「OS 锚定」情景已撤掉）。帕博利珠单抗组 5 年 RMST 由 %s 年（基准，k = %s）变为 %s 年，两臂差 %s 年（KM %s 年）。各时点（`scenario_k1_gate.csv`）：",
            f2(OA$rmst5_pembro_base, 4), f2(OA$k_base, 3), f2(OA$rmst5_pembro_k1, 4), f2(OA$engine_rmst_diff_k1, 4), f2(OA$km_rmst_diff, 4)), "",
    md_table(transform(OG, km = f2(km, 2), ci95_lo = f2(ci95_lo, 2), ci95_hi = f2(ci95_hi, 2), engine_base = f2(engine_base, 2),
                       engine_k1 = f2(engine_k1, 2), diff_k1 = f2(diff_k1, 3), inside_k1 = ifelse(istrue(inside_k1), "是", "**否**"))), "")
add("### 8.5 隐含的生存与外部对照", "",
    "模型隐含的生存（`dr_survival_implied.csv`；术前进展从 49.5 岁、远处复发从 50.5 岁计背景死亡；远处复发为共用风险，帕博利珠单抗组另乘 k）：", "",
    md_table(transform(IMP, median_excess_only_months = f2(median_excess_only_months, 1), median_all_cause_months = f2(median_all_cause_months, 1),
                       surv_1y = f2(surv_1y, 3), surv_2y = f2(surv_2y, 3), surv_5y = f2(surv_5y, 3))), "")
emx <- aggregate(cbind(max_abs_diff = abs(diff)) ~ check + arm, data = EC, FUN = max)
add("### 8.6 未用于校准的曲线", "",
    "与引擎的对照（`engine_checks.csv`，各曲线全部时点中差的绝对值最大者，百分点）：", "", md_table(transform(emx, max_abs_diff = f2(max_abs_diff, 3))), "",
    "图：`fig_calibration_OS.png`（灰带为 KM 逐点 95% CI，竖线为门槛时点）、`fig_engine_checks.png`。", "")
add("### 8.7 此前各轮", "",
    "第一轮至第三轮不达标；第四轮（术前进展后 Weibull）达标后由用户改设定；第五轮（术前进展后对数 logistic 加外部约束、远处复发后中位外部输入、k 固定为情景）不达标。第四、五轮的输出可在 git 历史中取回（第五轮为提交 0abaddd）。第三轮的可行性扫描 `R/05b_gate_feasibility.R` 保留为诊断。", "")

# ---------------------------------------------------------------- step 6
if (boot_done) {
  BC <- BRS$calibration; BB <- BRS$efs_binding
  cnt <- function(x) sum(x, na.rm = TRUE)
  c52 <- BC[, "code52"] == 1
  imp52 <- BC[, "value_before"] - BC[, "value_after"]
  drm <- 12 * BC[, "dr_median"]
  add("## 9. Bootstrap（步骤 6，`R/06_bootstrap.R`）", "",
      sprintf("B = %d，随机种子 %d（第 b 次用种子 + b），并行，耗时 %s 分钟。每次：", BRS$B, BRS$seed, f2(BRS$minutes, 1)),
      "1. 分层 EFS（2022 年补充材料 Fig. S4，IA4）：在各臂内连同 pCR 标签重抽样，pCR 比例与各层人数随之变动；各层在手术时点 landmark，用与基准相同的分布族重拟合并加 5 年约束（边界固定）；术前 KM 重算。",
      "2. 术前进展的进入比例 = 报告例数 / 重抽样后的非 pCR 人数（全臂比例保持报告值）。",
      "3. OS（2024 年 Fig. 1A，IA7）：在各臂内重抽样；所选的 OS 模型重拟合（只保存，引擎不用；RP 结点固定在基准位置）。",
      "4. 远处复发后中位按第 8.1 节的混合分布抽样，再对重抽样后的 OS KM 校准术前进展的中位与形状、远处复发后形状与 k（基准估计值加基准的 6 个起点，取最优；返回码 52 时再加 5 个随机起点取最优）。",
      "5. 引擎在 5、10、20 年的 EFS 与 OS（臂 × pCR；帕博利珠单抗组另算情景 k = 1）。",
      "每次都固定的数据设定：生命表、EFS 事件构成与分配比例、因不良事件死亡、局部区域复发 → 远处复发的率、术前进展例数、术前进展的外部约束、5 年约束的边界。拟合失败的样本换种子重抽（计入 attempts）。", "",
      sprintf("结果：完成 %d 次，10 次重抽仍失败 %d 次，换种子重抽的样本 %d 个。optim 返回码（最终）：%s。返回码 52 而加随机起点重跑的 %d 次，其中目标值改善的 %d 次（最大改善 %s）。",
              nrow(BC), length(BRS$failed), cnt(BC[, "attempts"] > 1),
              paste(names(table(BC[, "convergence"])), table(BC[, "convergence"]), sep = ": ", collapse = "，"),
              cnt(c52), cnt(c52 & imp52 > 1e-8), if (any(c52)) formatC(max(imp52[c52]), format = "g", digits = 3) else "—"),
      sprintf("贴边界的次数：k 贴下界 0.25 的 %d 次、贴上界 4 的 %d 次；术前进展中位贴 10 个月的 %d 次、贴 26 个月的 %d 次；5 年存活贴 5%% 的 %d 次；远处复发后形状贴数值边界的 %d 次。5 年 EFS 约束起作用的次数：%s。",
              cnt(BC[, "k_low"] == 1), cnt(BC[, "k_high"] == 1), cnt(BC[, "pp_median_low"] == 1), cnt(BC[, "pp_median_high"] == 1),
              cnt(BC[, "pp_s5_at_min"] == 1), cnt(BC[, "dr_shape_bound"] == 1),
              paste(colnames(BB)[-1], colSums(BB[, -1, drop = FALSE]), sep = " ", collapse = "，")),
      sprintf("抽到的远处复发后中位：中位数 %s 个月，2.5%% 至 97.5%% 分位 %s 至 %s 个月。", f2(median(drm), 2), f2(quantile(drm, 0.025), 2), f2(quantile(drm, 0.975), 2)), "",
      "参数的基准值与 bootstrap 分布（`output/phase1/bootstrap_summary.csv`；参数矩阵在 `data/bootstrap/`，一行一个样本；中位为年）：", "",
      md_table(transform(BSUM[BSUM$group %in% c("calibration", "pCR and PreProg"), ], base = f2(base, 4), boot_mean = f2(boot_mean, 4),
                         boot_median = f2(boot_median, 4), boot_lo = f2(boot_lo, 4), boot_hi = f2(boot_hi, 4))), "",
      "EFS 模型参数（自然尺度）：", "",
      md_table(transform(BSUM[BSUM$group == "EFS model parameters", ], base = f2(base, 4), boot_mean = f2(boot_mean, 4),
                         boot_median = f2(boot_median, 4), boot_lo = f2(boot_lo, 4), boot_hi = f2(boot_hi, 4))), "",
      "文件：`boot_efs_params.csv`、`boot_efs5_binding.csv`、`boot_os_model_params.csv`、`boot_pcr_preprog.csv`、`boot_pre_surgery_km.csv`、`boot_calibration.csv`、`boot_outputs.csv`、`boot_replicates.rds`。", "")

  # ---------------------------------------------------------------- step 7
  fmt <- function(b, lo, hi) sprintf("%s (%s–%s)", f2(b, 1), f2(lo, 1), f2(hi, 1))
  EO$cell <- fmt(EO$base, EO$boot_lo, EO$boot_hi)
  W <- reshape(EO[, c("endpoint", "scenario", "arm", "pcr", "year", "cell")], idvar = c("endpoint", "scenario", "arm", "pcr"),
               timevar = "year", direction = "wide")
  names(W) <- sub("^cell\\.", "", names(W)); names(W)[names(W) %in% c("5", "10", "20")] <- paste0(names(W)[names(W) %in% c("5", "10", "20")], " 年")
  W$arm <- ifelse(W$arm == "chemo", "单用化疗（= 化疗加运动）", "化疗加帕博利珠单抗（= 两者都加）")
  W$pcr <- c(all = "全体", pCR = "pCR", nonpCR = "非 pCR")[W$pcr]
  W$scenario <- ifelse(W$scenario == "base", "基准", "k = 1")
  add("## 10. 生存引擎的输出（步骤 7，`R/07_engine_outputs.R`）", "",
      "随机化后 5、10、20 年的 EFS 与 OS（%，基准值与 bootstrap 95% 分位区间；`engine_outputs.csv`、`engine_curves.csv`）。第 1 阶段没有运动参数，故加运动的两臂与对应的不加运动的臂相同；情景 k = 1 只改变帕博利珠单抗组的 OS（EFS 不变）。", "",
      md_table(setNames(W[order(W$endpoint, W$scenario != "基准", grepl("帕博利珠单抗", W$arm), match(W$pcr, c("全体", "pCR", "非 pCR"))), ],
                        c("终点", "情景", "臂", "pCR", names(W)[-(1:4)]))), "",
      sprintf("各 bootstrap 样本的引擎由保存的参数矩阵重建，其 5、10、20 年的值与 `06_bootstrap.R` 当时算出的一致（%d 个样本，最大差 %s，`bootstrap_rebuild_check.csv`）。",
              RB$replicates, formatC(RB$max_abs_diff, format = "e", digits = 1)), "",
      "图：`fig_engine_outputs.png`（实线为引擎，带为 bootstrap 95% 区间，虚线为重建的 KM）。", "",
      "引擎接口：`survival_engine(arm, pcr, times, params, hr0, wane_start, wane_rate, p_pcr, nonpcr_mix, common_dr, dr_first_months)`，`arm` 为 chemo、exercise、pembro、both；默认参数在 `data/fits/engine_params.rds`。运动钩子 (a) 时变 HR 与 (b) pCR 比例、S-JP 混合与情景 k = 1 的接口测试见 `engine_interface_test.csv`；闭式计算与逐周期递推一致（`R/test_engine_vectorized.R`）。", "",
      md_table(EIT), "")
}

add("## 11. 已决事项与待决事项", "",
    "已决：",
    "- 层内 HR 的较晚截点参照值：撤出门槛，改为跨分析对照（2026-10-21）。",
    "- 准则 1：保留 95%，最初 100% 为设定错误（2026-10-21）。",
    "- 分布族：同一层两臂同一族，依两臂合计 AIC 与 5 年外推检验选定，次优族为情景（2026-10-21）；非 pCR 层复核后维持（2026-10-22）。",
    "- 第二原发癌：归入局部区域复发（2026-10-21）。",
    "- 校准第三轮（2026-10-22）：门槛 (a) 与 (b)；因不良事件死亡单列；EFS 加 5 年约束。",
    "- 校准第四轮（2026-10-22）：门槛 (b) 改为 KM 差的 bootstrap 区间。",
    "- 校准第五轮（2026-10-22）：远处复发后中位改为外部输入（10.1 个月；概率敏感性分析按 ESME 与 IMpassion132 的混合分布抽样）；术前进展后死亡改为对数 logistic，加两条外部约束；返回码 52 时加随机起点。",
    "- 校准第六轮（2026-10-22）：k 纳入基准校准（0.25 至 4）；原 OS 锚定情景撤掉，改设情景 k = 1；接受规则运行前确定；门槛修改记录保留全部六项；IMpassion132 的置信区间已用全文核对。",
    "",
    "待决：",
    if (stop6) "- **校准第六轮未被接受**（第 8 节）。按指示未自行增加结构，处理方向待定。" else NULL,
    if (CANDS$at_bound[["pp_s5_at_min"]]) "- 术前进展后死亡的校准值仍贴在「5 年存活 ≥ 5%」的约束上（第 8.2 节）。" else NULL,
    "- 若尾崎日后提供 2023-03-23 截点的分层 KM，5 年约束改为用整条曲线（2026-10-22 的决定）。",
    "",
    "等尾崎回答：",
    "- S-JP 的权重定义（`docs/model_spec.md` 第 2 节）。",
    "- BRCA 检测的对象范围。",
    "- 帕博利珠单抗组是否也加 S-JP。", "")

add("## 12. 局限性", "",
    sprintf("- 术前进展的人数少（两臂合计 %d 例，2024 年 Table 1），其后的死亡分布主要由外部约束决定（第 8.1 节）。", n_pp), "")

writeLines(L, file.path(out_dir, "phase1_report.md"), useBytes = TRUE)
cat("wrote phase1_report.md:", length(L), "lines\n")
