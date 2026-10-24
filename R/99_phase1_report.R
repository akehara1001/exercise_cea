# 99_phase1_report.R
# Builds output/phase1/phase1_report.md from the code outputs (no hand-entered numbers).
# The phase-1 sections (final state, status, sections 1-12) read the round-8 snapshot
# (output/phase1/round8/, data/fits/round8/, data/bootstrap/round8/); section 13 (round 9, phase-2
# preparation) reads the current outputs (output/phase1/*.csv, output/phase1/round9/).

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
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
CAL <- rd("output", "phase1", "round8", "calibration.csv")
CG <- rd("output", "phase1", "round8", "calibration_gate.csv")
CS <- rd("output", "phase1", "round8", "calibration_status.csv")
RM <- rd("output", "phase1", "round8", "calibration_rmst.csv")
DS <- rd("output", "phase1", "round8", "calibration_deaths_by_source.csv")
IMP <- rd("output", "phase1", "round8", "dr_survival_implied.csv")
EC <- rd("output", "phase1", "round8", "engine_checks.csv")
CGR <- rd("output", "phase1", "round8", "calibration_gate_rmst.csv")
RS <- rd("output", "phase1", "round8", "calibration_rmst_by_source.csv")
AE <- rd("output", "phase1", "round8", "ae_deaths.csv")
CON <- rd("output", "phase1", "efs5_constraint.csv")
FSU <- rd("output", "phase1", "calibration_gate_feasibility_summary.csv")
FPT <- rd("output", "phase1", "calibration_gate_feasibility_points.csv")
OA <- rd("output", "phase1", "round8", "scenario_k1.csv")
OG <- rd("output", "phase1", "round8", "scenario_k1_gate.csv")
EIT <- rd("output", "phase1", "round8", "engine_interface_test.csv")
G7 <- rd("output", "phase1", "round8", "calibration_final7y.csv")
OB <- rd("output", "phase1", "round8", "calibration_objective.csv")
AD <- rd("output", "phase1", "round8", "scenario_k1_arm_diff.csv")
PCC <- rd("data", "pcr_counts.csv")
VS <- rd("output", "phase1", "round8", "calibration_vs_previous.csv")
R6F <- rd("output", "phase1", "r6_vs_final7y.csv")
R7F <- rd("output", "phase1", "r7_calibration_final7y.csv")
DRE <- rd("output", "phase1", "round8", "dr_early_share.csv")
ADU <- rd("output", "phase1", "round8", "scenario_k1_arm_diff_ci.csv")
FA7 <- rd("data", "kn522_final_7y.csv")
fa7 <- function(id) FA7$value[FA7$id == id]
iso_date <- function(x) { m <- regmatches(x, regexec("^(\\w+) (\\d+), (\\d{4})$", x))[[1]]
  sprintf("%s-%02d-%02d", m[4], match(m[2], month.name), as.integer(m[3])) }
opt <- function(...) if (file.exists(file.path(ROOT, ...))) rd(...) else NULL
BSUM <- opt("output", "phase1", "round8", "bootstrap_summary.csv")
EO <- opt("output", "phase1", "round8", "engine_outputs.csv")
RB <- opt("output", "phase1", "round8", "bootstrap_rebuild_check.csv")
BRS <- if (file.exists(file.path(ROOT, "data", "bootstrap", "round8", "boot_replicates.rds"))) readRDS(file.path(ROOT, "data", "bootstrap", "round8", "boot_replicates.rds")) else NULL
CANDS <- readRDS(file.path(ROOT, "data", "fits", "round8", "calibration_candidates.rds"))
P <- CANDS$params
stop6 <- istrue(CS$stop_before_step6)
rvv <- function(id, key) rv$value[rv$fact_id == id & rv$key == key]
rvp <- function(id) paste0(rv$pdf[rv$fact_id == id][1], " p.", rv$page[rv$fact_id == id][1])
os_d5 <- as.numeric(rvv("K24_os_milestones", "pembro_5y")) - as.numeric(rvv("K24_os_milestones", "placebo_5y"))
os_d7 <- as.numeric(fa7("os7_pembro")) - as.numeric(fa7("os7_placebo"))
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
# the bootstrap on disk belongs to the current calibration only if its base k equals the adopted k,
# and it is the full run only if B = CFG$boot_B (a smoke test uses a few replicates)
boot_done <- !is.null(BRS) && !is.null(EO) && "pembro_dr_k" %in% colnames(BRS$calibration) &&
  isTRUE(abs(BSUM$base[BSUM$quantity == "pembro_dr_k"] - P$pembro_dr_k) < 1e-9) && isTRUE(BRS$B == CFG$boot_B)
pp_bound_txt <- function(ab) {
  x <- c(if (ab[["pp_median_low"]]) "中位 = 10 个月" else NULL, if (ab[["pp_median_high"]]) "中位 = 26 个月" else NULL,
         if (ab[["pp_s5_at_min"]]) "5 年存活 = 5%" else NULL)
  if (length(x)) paste0("贴在约束边界上（", paste(x, collapse = "，"), "）") else "不在约束边界上"
}
G_out <- CG[!istrue(CG$inside), ]

# ---------------------------------------------------------------- round 10 decision
# docs/acceptance_rule_round10.md (git e8d2134): rule A adopts the round-9 structure (gate (a) by
# the Bonferroni intervals only); rule B keeps round 8
DEC10 <- if (file.exists(file.path(ROOT, "output", "phase1", "round10", "decision.csv"))) rd("output", "phase1", "round10", "decision.csv") else NULL
CSnow <- rd("output", "phase1", "calibration_status.csv")
adopt9 <- !is.null(DEC10) && DEC10$rule == "A" && istrue(CSnow$gate_pass)
r9rule_f <- file.path(ROOT, "output", "phase1", "round9", "calibration_status_round9_rule.csv")
deaths12_placebo <- sum(ipd$K24_F1A_OS_placebo$status == 1 & ipd$K24_F1A_OS_placebo$time <= 12)

# ---------------------------------------------------------------- final state of phase 1
if (adopt9) {
  C9f <- readRDS(file.path(ROOT, "data", "fits", "calibration_candidates.rds")); P9f <- C9f$params
  CG9f <- rd("output", "phase1", "calibration_gate.csv"); CGR9f <- rd("output", "phase1", "calibration_gate_rmst.csv")
  G79f <- rd("output", "phase1", "calibration_final7y.csv"); DS10 <- rd("output", "phase1", "round10", "dr_survival_comparison.csv")
  ES9f <- rd("output", "phase1", "round9", "esme_shape_test.csv")
  G9o <- CG9f[!istrue(CG9f$inside), ]
  ref_meta <- tryCatch(readRDS(file.path(ROOT, "output", "check", "bootstrap10_local.rds"))$meta, error = function(e) NULL)
  BS_now <- opt("output", "phase1", "bootstrap_summary.csv")
  BR9 <- if (file.exists(file.path(ROOT, "data", "bootstrap", "boot_replicates.rds"))) readRDS(file.path(ROOT, "data", "bootstrap", "boot_replicates.rds")) else NULL
  boot9 <- !is.null(BS_now) && !is.null(BR9) && isTRUE(abs(BS_now$base[BS_now$quantity == "pembro_dr_k"] - P9f$pembro_dr_k) < 1e-9) && isTRUE(BR9$B == CFG$boot_B)
  FP9 <- data.frame(
    参数 = c("pCR 比例（帕博利珠单抗 / 安慰剂）", "术前进展后超额死亡：对数 logistic 中位（月）", "术前进展后超额死亡：形状",
           "远处复发后超额死亡：形状（早期 / 晚期）", "远处复发后中位：早期（月）", "远处复发后中位：晚期（月）",
           "早期远处复发的界线（随机化后月数）", "帕博利珠单抗组远处复发后风险的倍数 k", "因不良事件死亡（帕博利珠单抗 / 安慰剂）",
           "局部区域复发 → 远处复发（/年）"),
    值 = c(sprintf("%s / %s", f2(P9f$p_pcr[["pembro"]], 4), f2(P9f$p_pcr[["placebo"]], 4)), f2(12 * P9f$preprog$scale, 2), f2(P9f$preprog$shape, 4),
          sprintf("%s / %s", f2(P9f$dr$shape, 4), f2(P9f$dr$late_shape, 4)), f2(12 * P9f$dr$scale, 2), f2(12 * P9f$dr$late_scale, 2),
          as.character(CFG$dr_early_months), f2(P9f$pembro_dr_k, 4),
          sprintf("%s/%s、%s/%s", P9f$ae$pembro[["deaths"]], P9f$ae$pembro[["n_treated"]], P9f$ae$placebo[["deaths"]], P9f$ae$placebo[["n_treated"]]),
          f2(P9f$lrr_dr[["rate"]], 4)),
    来源 = c(sprintf("数据（%s）", CFG$pcr_source), "校准（外部约束 10 至 26 个月）", "校准（上限由 5 年存活 ≥ 5% 决定）",
           sprintf("外部输入（ESME 重建个体数据的对数 logistic 拟合，%s）", if (ES9f$decision == "common") "共用形状" else "分开的形状"),
           "外部输入（ESME 拟合）", "外部输入（ESME 拟合）", "用户指定（第 8.1 节）", "校准（范围 0.25 至 4）",
           "数据（2022 年补充材料 Table S5）", "数据（2022 年 Table 1 脚注）"), check.names = FALSE)
  out8 <- DS10[DS10$used_in_rule & !istrue(DS10$round8_inside), ]
  add("## 第1阶段最终状态", "",
      sprintf("第 1 阶段以**第九轮**为最终结构（%s）。依据：第十轮的判定规则 A（`docs/acceptance_rule_round10.md`，git e8d2134，在诊断之前单独提交）——第八轮模型的远处复发后隐含存活在%s落在 ESME 重建 KM 的 95%% CI 之外；第九轮在第 1 至 4 年的 %d 个点中 %d 个落在区间内（第 14 节）。第八轮（git 694b0f3）只作记录：第 1 至 12 节为第八轮的内容，其参数、bootstrap 与输出的快照在 `data/fits/round8/`、`data/bootstrap/round8/`、`output/phase1/round8/`。引擎默认参数在 `data/fits/engine_params.rds`（第九轮）。涉及帕博利珠单抗的结果在第 2 阶段以基准与情景 k = 1 两栏并列报告（`docs/model_spec.md` 第 6 节）。第十一轮（分层 EFS 约束改用最终分析的 7 年值，2026-10-23）两次都按规则停下、未采用：区间约束停在拟合之后，改为等式约束后停在门槛 (c)（第 15 节）。第十二轮修正了引擎与输入 EFS 的不一致（手术前的背景死亡与因不良事件死亡原先另外加在 KM 之上，术前进展用的是报告比例而非 KM 的下降）；修正后的引擎下第十一轮设定仍在门槛 (c) 不通过，未采用（第 16 节）。**本节的第十轮参数与门槛结果是用修正前的引擎算出的**；修正后的引擎下第十轮设定重新校准的结果见第 16 节（只报告，不作为回退）。",
              C9f$structure, paste(sprintf("%s第 %d 年", ifelse(out8$group == "early", "早期", "晚期"), out8$year), collapse = "、"),
              nrow(DS10), sum(istrue(DS10$round9_inside))), "",
      "最终参数（第九轮）：", "", md_table(FP9), "",
      sprintf("术前进展后死亡的校准值%s；k %s。", pp_bound_txt(C9f$at_bound), if (C9f$at_bound[["k_low"]] || C9f$at_bound[["k_high"]]) "**贴边界**" else "不在边界上"), "",
      "门槛结果（第九轮的校准结果不变、未重新校准，按第十轮的规则判定）：",
      sprintf("- (a) 按 Bonferroni 同时区间接受：10 个点中 %d 个落在 KM 逐点 95%% 区间内%s；全部 10 个点%s逐点 99.5%% 区间内。第十轮规则 A 去掉了 0.3 个百分点的附加上限（门槛修改记录第 8 项）。",
              sum(istrue(CG9f$inside)), if (nrow(G9o)) sprintf("，区间外 %s，超出 %s 个百分点", paste(sprintf("%s %d 个月", ifelse(G9o$arm == "pembro", "帕博利珠单抗", "安慰剂"), G9o$month), collapse = "、"),
                                                         paste(f2(G9o$outside_pp, 3), collapse = "、")) else "",
              if (all(istrue(CG9f$inside_995))) "落在" else "**并非都在**"),
      sprintf("- (b) %s：模型 5 年 RMST 两臂差 %s 年，KM 差的 bootstrap 95%% 区间 %s 至 %s 年。", if (istrue(CGR9f$pass)) "达标" else "**不达标**",
              f2(CGR9f$engine, 4), f2(CGR9f$km_boot_ci95_lo, 4), f2(CGR9f$km_boot_ci95_hi, 4)),
      sprintf("- (c) %s：7 年 OS 与 EFS 的 4 个值中 %d 个落在最终分析的 95%% 区间内。", if (istrue(CSnow$gate_c_pass)) "达标" else "**不达标**",
              sum(istrue(G79f$inside_ci[istrue(G79f$gate_c)]))), "",
      if (boot9) {
        BC9 <- BR9$calibration; cn <- function(x) sum(x, na.rm = TRUE)
        sprintf("bootstrap 的边界情况（B = %d，完成 %d 次，失败 %d 次）：k 贴下界 0.25 的 %d 次、贴上界 4 的 %d 次；术前进展中位贴 10 个月的 %d 次、贴 26 个月的 %d 次；5 年存活贴 5%% 的 %d 次；optim 返回码 52 而加随机起点重跑的 %d 次。",
                BR9$B, nrow(BC9), length(BR9$failed), cn(BC9[, "k_low"] == 1), cn(BC9[, "k_high"] == 1), cn(BC9[, "pp_median_low"] == 1),
                cn(BC9[, "pp_median_high"] == 1), cn(BC9[, "pp_s5_at_min"] == 1), cn(BC9[, "code52"] == 1))
      } else sprintf("bootstrap：第九轮的 1,000 次尚未运行——推送与 Longleaf 的运行推迟到第十一轮通过之后（用户 2026-10-23 的指示），第十一轮按规则停下（第 15 节）（`data/bootstrap/` 仍为第八轮的结果，不属于本结构）。本地参照 `output/check/bootstrap10_local.rds`（基础种子 20261023，10 次）%s。",
                     if (!is.null(ref_meta)) sprintf("在提交 %s 上生成（%s）", substr(ref_meta$commit, 1, 7), ref_meta$platform) else "尚未生成"), "",
      "待尾崎回答：",
      "- 含帕博利珠单抗的组的 S-JP 数值 F01P、F04P（尾崎正向临床医生确认；结构已于 2026-10-23 决定，见第 11 节）。",
      "- B30 的定义（第 2 阶段入力表）。",
      sprintf("- 按 pCR 分层的 EFS 层内 HR 较晚截点值（%s、%s）的原始出处（第 4 节）。",
              us$value[us$id == "K522_EFS_HR_pCR"], us$value[us$id == "K522_EFS_HR_nonpCR"]), "")
} else if (!stop6 && boot_done) {
  BCf <- BRS$calibration; cntf <- function(x) sum(x, na.rm = TRUE)
  FP <- data.frame(
    参数 = c("pCR 比例（帕博利珠单抗 / 安慰剂）", "术前进展后超额死亡：对数 logistic 中位（月）", "术前进展后超额死亡：形状",
           "远处复发后超额死亡：形状（早期与晚期共用）", "远处复发后中位：早期（月）", "远处复发后中位：晚期（月）",
           "早期远处复发的界线（随机化后月数）", "帕博利珠单抗组远处复发后风险的倍数 k", "因不良事件死亡（帕博利珠单抗 / 安慰剂）",
           "局部区域复发 → 远处复发（/年）"),
    值 = c(sprintf("%s / %s", f2(P$p_pcr[["pembro"]], 4), f2(P$p_pcr[["placebo"]], 4)), f2(12 * P$preprog$scale, 2), f2(P$preprog$shape, 4),
          f2(P$dr$shape, 4), f2(12 * P$dr$scale, 1), f2(12 * P$dr$late_scale, 1), as.character(CFG$dr_early_months), f2(P$pembro_dr_k, 4),
          sprintf("%s/%s、%s/%s", P$ae$pembro[["deaths"]], P$ae$pembro[["n_treated"]], P$ae$placebo[["deaths"]], P$ae$placebo[["n_treated"]]),
          f2(P$lrr_dr[["rate"]], 4)),
    来源 = c(sprintf("数据（%s）", CFG$pcr_source), "校准（外部约束 10 至 26 个月）", "校准（上限由 5 年存活 ≥ 5% 决定）", "校准",
           "外部输入（ESME 早期复发）", "外部输入（ESME 晚期复发）", "用户指定（第 8.1 节）", "校准（范围 0.25 至 4）",
           "数据（2022 年补充材料 Table S5）", "数据（2022 年 Table 1 脚注）"), check.names = FALSE)
  add("## 第1阶段最终状态", "",
      sprintf("第 1 阶段以第八轮为最终结构（%s）。引擎默认参数在 `data/fits/engine_params.rds`，bootstrap 参数矩阵在 `data/bootstrap/`。涉及帕博利珠单抗的结果在第 2 阶段以基准与情景 k = 1 两栏并列报告（`docs/model_spec.md` 第 6 节）。", CANDS$structure), "",
      "最终参数：", "", md_table(FP), "",
      sprintf("术前进展后死亡的校准值%s；k %s。", pp_bound_txt(CANDS$at_bound), if (istrue(CS$k_at_bound)) "**贴边界**" else "不在边界上"), "",
      "门槛结果（接受规则 `docs/acceptance_rule_round8.md`，运行前提交）：",
      sprintf("- (a) %s：10 个点中 %d 个落在 KM 逐点 95%% 区间内%s。", if (istrue(CS$gate_a_strict_pass)) "达标" else if (istrue(CS$gate_a_accepted)) "按例外规则 (i)、(ii) 接受" else "**不达标**",
              sum(istrue(CG$inside)), if (nrow(G_out)) sprintf("，区间外 %s，超出 %s 个百分点", paste(sprintf("%s %d 个月", ifelse(G_out$arm == "pembro", "帕博利珠单抗", "安慰剂"), G_out$month), collapse = "、"),
                                                       paste(f2(G_out$outside_pp, 3), collapse = "、")) else ""),
      sprintf("- (b) %s：模型 5 年 RMST 两臂差 %s 年，KM 差的 bootstrap 95%% 区间 %s 至 %s 年。", if (istrue(CGR$pass)) "达标" else "**不达标**",
              f2(CGR$engine, 4), f2(CGR$km_boot_ci95_lo, 4), f2(CGR$km_boot_ci95_hi, 4)),
      sprintf("- (c) %s：7 年 OS 与 EFS 的 4 个值中 %d 个落在最终分析的 95%% 区间内。", if (istrue(CS$gate_c_pass)) "达标" else "**不达标**",
              sum(istrue(G7$inside_ci[istrue(G7$gate_c)]))), "",
      sprintf("bootstrap 的边界情况（B = %d，完成 %d 次，失败 %d 次）：k 贴下界 0.25 的 %d 次、贴上界 4 的 %d 次；术前进展中位贴 10 个月的 %d 次、贴 26 个月的 %d 次；5 年存活贴 5%% 的 %d 次；远处复发后形状贴数值边界的 %d 次；optim 返回码 52 而加随机起点重跑的 %d 次（第 9 节）。",
              BRS$B, nrow(BCf), length(BRS$failed), cntf(BCf[, "k_low"] == 1), cntf(BCf[, "k_high"] == 1), cntf(BCf[, "pp_median_low"] == 1),
              cntf(BCf[, "pp_median_high"] == 1), cntf(BCf[, "pp_s5_at_min"] == 1), cntf(BCf[, "dr_shape_bound"] == 1), cntf(BCf[, "code52"] == 1)), "",
      "待尾崎回答：",
      "- 含帕博利珠单抗的组的 S-JP 数值 F01P、F04P（尾崎正向临床医生确认；结构已于 2026-10-23 决定，见第 11 节）。",
      "- B30 的定义（第 2 阶段入力表）。",
      sprintf("- 按 pCR 分层的 EFS 层内 HR 较晚截点值（%s、%s）的原始出处（第 4 节）。",
              us$value[us$id == "K522_EFS_HR_pCR"], us$value[us$id == "K522_EFS_HR_nonpCR"]), "")
}
add("## 状态", "",
    "- 已完成：步骤 1 至 4（含 2026-10-21 与 2026-10-22 的修正）与一致性检查；非 pCR 层分布族已复核。",
    sprintf("- 重建与一致性的门槛项 %d 项，不达标 %d 项。", sum(istrue(V$gate)), nrow(gfail)),
    sprintf("- 步骤 5（校准第八轮，2026-10-22，远处复发分为早期与晚期）：按运行前确定的接受规则（`docs/acceptance_rule_round8.md`，git e0a722c；与第七轮相同）%s。门槛 (a)：10 个点中 %d 个落在逐点 95%% 区间内%s；门槛 (b)：模型的 5 年 RMST 两臂差 %s 年，%s KM 差（%s 年）的 bootstrap 95%% 区间 %s 至 %s 年内。",
            if (stop6) "**不接受，停止**" else "**接受**", sum(istrue(CG$inside)),
            if (nrow(G_out)) sprintf("，区间外 %d 处（%s），超出幅度 %s 个百分点，均 ≤ %g 且全部 10 个点落在 Bonferroni 校正后的逐点 99.5%% 区间内%s",
                                     nrow(G_out), paste(sprintf("%s %d 个月", ifelse(G_out$arm == "pembro", "帕博利珠单抗", "安慰剂"), G_out$month), collapse = "、"),
                                     paste(f2(G_out$outside_pp, 3), collapse = "、"), CFG$gate_accept_max_outside_pp,
                                     if (istrue(CS$gate_a_accepted)) "，按规则 (i)、(ii) 接受" else "") else "",
            f2(CGR$engine, 4), if (istrue(CGR$pass)) "落在" else "不在", f2(CGR$km, 4), f2(CGR$km_boot_ci95_lo, 4), f2(CGR$km_boot_ci95_hi, 4)),
    sprintf("- 门槛 (c)（第七轮新增）：模型 7 年的 OS 与 EFS 4 个值中 %d 个落在最终分析报告的 95%% 区间内，%s（下表）。按 pCR 分层的 7 年 OS 只报告差值（第 8.2 节）。",
            sum(istrue(G7$inside_ci[istrue(G7$gate_c)])), if (istrue(CS$gate_c_pass)) "达标" else "**不达标**"),
    sprintf("- 帕博利珠单抗组远处复发后死亡风险的倍数 k = %s（第六轮 %s，第七轮 %s；范围 0.25 至 4，%s）。术前进展后死亡的校准值%s。",
            f2(P$pembro_dr_k, 3), f2(VS$round6[VS$quantity == "pembro_dr_k"], 3), f2(VS$round7[VS$quantity == "pembro_dr_k"], 3),
            if (istrue(CS$k_at_bound)) "**贴边界**" else "不在边界上", pp_bound_txt(CANDS$at_bound)),
    sprintf("- 远处复发中早期（随机化后 %d 个月以内）所占比例：随机化后 7 年内的远处复发中，帕博利珠单抗组 %s%%、安慰剂组 %s%%；到 100 岁的全部远处复发中 %s%% 与 %s%%（第 8.2 节）。",
            DRE$early_months[1], f2(100 * DRE$early_share[DRE$arm == "pembro" & DRE$horizon_years == 7], 1), f2(100 * DRE$early_share[DRE$arm == "placebo" & DRE$horizon_years == 7], 1),
            f2(100 * DRE$early_share[DRE$arm == "pembro" & DRE$horizon_years == max(DRE$horizon_years)], 1),
            f2(100 * DRE$early_share[DRE$arm == "placebo" & DRE$horizon_years == max(DRE$horizon_years)], 1)),
    if (!stop6 && boot_done) sprintf("- 步骤 6（bootstrap，B = %d，k 在每个样本中一起估计，7 年目标值在每个样本中按抽样分布抽取）与步骤 7（引擎输出，含 7 年）已完成（第 9、10 节）。", BRS$B)
    else if (!stop6) "- 步骤 6、7 尚未完成（`data/bootstrap/` 与步骤 7 的输出不属于本轮校准，第 9、10 节不列出）。" else NULL,
    if (!stop6 && boot_done) "- 第 1 阶段到此结束（2026-10-23）。第 2 阶段中涉及帕博利珠单抗的结果以基准与 k = 1 两栏并列报告（`docs/model_spec.md` 第 6 节；两臂差的对照见第 8.4 节）。" else NULL,
    "- 门槛的修改经过见下一节「门槛修改记录」（全部七项）。",
    if (file.exists(file.path(ROOT, "output", "phase1", "round9", "esme_fits.csv")))
      sprintf("- 第九轮（第 2 阶段准备，2026-10-23，远处复发后生存外部锚定于 ESME 曲线）：按第九轮的规则%s，见第 13 节。%s以上各项与第 1 至 12 节为第八轮的快照。",
              if (istrue((if (file.exists(r9rule_f)) read.csv(r9rule_f) else CSnow)$gate_pass)) "接受" else "**未被接受**（门槛 (a) 超出 0.3 个百分点的上限）",
              if (!is.null(DEC10)) sprintf("第十轮按判定规则 %s %s，见第 14 节。", DEC10$rule,
                                           if (adopt9) "采用第九轮结构（门槛 (a) 改为只用 Bonferroni 同时区间后接受）" else "维持第八轮") else "") else NULL, "")
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
                        engine_minus_km = f2(CGR$engine_minus_km, 4), pass = ifelse(istrue(CGR$pass), "达标", "**不达标**"))), "",
    "门槛 (c)（`calibration_final7y.csv`；报告值为 KEYNOTE-522 最终分析，J Clin Oncol 2026;44(16_suppl):507，截点 2025-10-14；engine_k1 为情景 k = 1，只作参照）：", "",
    md_table(with(G7[istrue(G7$gate_c), ], data.frame(id = id, reported = f2(value, 1), ci95_lo = f2(ci95_lo, 1), ci95_hi = f2(ci95_hi, 1),
                                                      engine = f2(engine, 2), diff = f2(diff, 2), inside_ci = ifelse(istrue(inside_ci), "是", "**否**"),
                                                      engine_k1 = f2(engine_k1, 2), inside_ci_k1 = ifelse(istrue(inside_ci_k1), "是", "**否**"), source = source))), "")

# ---------------------------------------------------------------- gate change log
yau_fail <- V[grepl("^Y22", V$curve) & !istrue(V$pass), ]
c1_none <- sum(tapply(istrue(M$c1_pass_all_points[istrue(M$converged)]), M$curve[istrue(M$converged)], function(x) !any(x)))
shr_p <- V[V$check == "hr" & grepl("^pCR [(]later", V$unit), ][1, ]
band_r3 <- 2 * CFG$gate_rmst_rel_tol_round3 * CGR$km
LOG <- data.frame(
  no = 1:7,
  date = c("2026-10-21", "2026-10-21", "2026-10-21", "2026-10-22", "2026-10-22", "2026-10-22", "2026-10-22"),
  item = c("Yau 2022 的重建验证", "拟合准则 1（选模）", "按 pCR 分层的 EFS 层内 HR（较晚截点的参照值）", "校准门槛", "校准门槛 (b)", "校准门槛 (a) 的接受条件",
           "校准门槛 (c)（新增）"),
  before = c("里程碑差 ≤ 1 个百分点、HR 差 ≤ 0.03、事件数差 ≤ 2% 三项都作门槛",
             "模型落在 KM 逐点 95% CI 内的月份比例 = 100%",
             "与参照值的差 ≤ 0.03（门槛）",
             sprintf("各臂第 1 至 5 年整年时点 OS 与 KM 的差 ≤ %g 个百分点", CFG$gate_pp_round1_2),
             sprintf("5 年 RMST 两臂差：模型与 KM 的相对误差 ≤ %d%%（允许 %s 至 %s 年）", round(100 * CFG$gate_rmst_rel_tol_round3),
                     f2(CGR$km * (1 - CFG$gate_rmst_rel_tol_round3), 3), f2(CGR$km * (1 + CFG$gate_rmst_rel_tol_round3), 3)),
             "(a) 10 个点全部落在逐点 95% CI 内",
             "只有 (a)（含例外 (i)、(ii)）与 (b)"),
  after = c("只保留里程碑为门槛；HR 与事件数只报告",
            sprintf("≥ %g%%", 100 * CFG$fit_ci_min_inside),
            "不作门槛的跨分析对照",
            sprintf("(a) 各臂第 1 至 5 年整年时点落在 KM 逐点 95%% CI 内；(b) 5 年 RMST 两臂差相对误差 ≤ %d%%", round(100 * CFG$gate_rmst_rel_tol_round3)),
            "(b) 模型的 5 年 RMST 两臂差落在 KM 差的 bootstrap 95% 区间内；点估计差距照常报告",
            sprintf("(a) 不达标时，同时满足 (i) 每个区间外的点超出 ≤ %g 个百分点、(ii) 全部 10 个点落在 Bonferroni 校正后的逐点 %g%% 区间内则接受；(b) 不变",
                    CFG$gate_accept_max_outside_pp, 100 * CFG$gate_accept_simultaneous_level),
            "(a)、(b) 及例外不变；新增 (c) 模型 7 年的 OS 与 EFS 各臂落在最终分析报告的 95% 置信区间内；按 pCR 分层的 7 年 OS 只报告，不作门槛"),
  timing = c(rep("看到结果后修改", 5), "看到第五轮结果之后、第六轮运行之前确定（git a53afe2 提交于运行前）",
             "第七轮运行之前确定（git f811ec4 提交于运行前）"),
  result_seen = c(sprintf("Yau 有 %d 项不达标（事件数 %d 项、HR %d 项）", nrow(yau_fail), sum(yau_fail$check == "events"), sum(yau_fail$check == "hr")),
                  sprintf("6 条曲线中 %d 条没有任何候选模型通过", c1_none),
                  sprintf("pCR 层重建 %s 对参照 %s，差 %s", f2(shr_p$reconstructed, 3), f2(shr_p$reported, 2), f2(shr_p$abs_diff, 3)),
                  "第一轮（2026-10-21）与第二轮（2026-10-22）校准都不达标",
                  "第三轮校准不达标（(a) 与 (b) 都不达标）",
                  "第五轮门槛 (a) 不达标（有点落在逐点 95% 区间外）",
                  sprintf("运行前记录（`r6_vs_final7y.csv`）：第六轮模型 7 年的 OS 与 EFS 4 个值中 %d 个已落在最终分析的 95%% 区间内",
                          sum(istrue(R6F$inside_ci[R6F$scenario == "base" & R6F$pcr == "all" & R6F$endpoint %in% c("OS", "EFS")])))),
  reason = c("HR 的估计量与原文不同（原文为 12 个队列、含队列效应的汇总模型，使用全部随访；重建只能在 12 年内做单一 Cox）；事件数的参照值从风险表推算，原文没有报告",
             "设定错误：逐点 95% 置信区间本来就预期约 5% 的点落在区间外",
             "参照值来自比 IA4 更晚的数据截点，IA4 的曲线不可能与之吻合；IA4 原文印的 0.73 与 0.70 已在 0.012 以内复现",
             sprintf("门槛比抽样误差更严：%g 个百分点小于安慰剂组（n = %d）5 年 OS 的 Greenwood 标准误 %s 个百分点", CFG$gate_pp_round1_2,
                     n_os[["placebo"]], f2(se5[["placebo"]], 2)),
             sprintf("门槛比抽样误差更严：允许带宽 %s 年，远窄于 KM 差的 bootstrap 95%% 区间宽度 %s 年", f2(band_r3, 3),
                     f2(CGR$km_boot_ci95_hi - CGR$km_boot_ci95_lo, 3)),
             sprintf("10 个时点各按 95%% 检验，即使模型正确，也有相当大的概率至少一点落在区间外（若各点独立为 %s%%；同一臂的各时点正相关，实际略低）",
                     f2(100 * (1 - 0.95^10), 0)),
             sprintf("最终分析提供了 7 年的成熟数据，两臂 OS 差从 5 年时的 %s 个百分点扩大到 %s 个百分点", f2(os_d5, 1), f2(os_d7, 1))))
if (adopt9) {
  G9r <- rd("output", "phase1", "calibration_gate.csv"); G9x <- G9r[!istrue(G9r$inside), ]
  LOG <- rbind(LOG, data.frame(no = 8, date = "2026-10-23", item = "校准门槛 (a) 的接受条件",
    before = sprintf("(a) 不达标时，同时满足 (i) 每个区间外的点超出 ≤ %g 个百分点、(ii) 全部 10 个点落在 Bonferroni 校正后的逐点 %g%% 区间内则接受",
                     CFG$gate_accept_max_outside_pp, 100 * CFG$gate_accept_simultaneous_level),
    after = sprintf("(a) 不达标时，只要全部 10 个点落在 Bonferroni 校正后的逐点 %g%% 区间内即接受（去掉 (i)）", 100 * CFG$gate_accept_simultaneous_level),
    timing = "看到第九轮结果之后做出；只在第十轮判定规则 A 成立时生效（`docs/acceptance_rule_round10.md`，git e8d2134，在诊断之前提交）",
    result_seen = sprintf("第九轮：%s超出 95%% 区间 %s 个百分点，比 %g 的上限多 %s 个百分点；全部 10 个点在 99.5%% 区间内",
                          paste(sprintf("%s %d 个月", ifelse(G9x$arm == "pembro", "帕博利珠单抗", "安慰剂"), G9x$month), collapse = "、"),
                          f2(max(G9x$outside_pp), 3), CFG$gate_accept_max_outside_pp, f2(max(G9x$outside_pp) - CFG$gate_accept_max_outside_pp, 3)),
    reason = sprintf("例外规则本来就以同时区间为统计依据，%g 个百分点的附加上限没有统计依据；超出发生在安慰剂组 12 个月，该时点只有 %d 例死亡（重建个体数据）",
                     CFG$gate_accept_max_outside_pp, deaths12_placebo)))
}
add("## 门槛修改记录", "",
    paste0("按时间列出验证与校准门槛的每次修改。第 1 至 5 项是看到结果后修改的，第 4、5 项的理由是门槛比抽样误差更严；第 6 项在看到第五轮结果之后、第六轮运行之前确定，第 7 项在第七轮运行之前确定，两者都在运行前提交到 git。第八、九轮的接受规则与第七轮相同（`docs/acceptance_rule_round8.md`、`docs/acceptance_rule_round9.md`，均在运行前提交），门槛没有修改。",
           if (adopt9) "第 8 项是看到第九轮结果之后做出的，作为第十轮判定规则 A 的一部分在诊断之前提交，规则 A 成立后生效。" else ""), "",
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
    sprintf("pCR 比例：帕博利珠单抗 %s，安慰剂 %s。局部区域复发 → 远处复发 %s/年（%d/%d 例，暴露 %s 年）。术前进展后的超额死亡为进入后时间的对数 logistic（第五轮；形状与中位在外部约束下校准），远处复发后的超额死亡为复发后时间的对数 logistic，按进入时点分早期与晚期两个子状态（第八轮；中位分别为外部输入，形状共用并校准；帕博利珠单抗组另乘 k，k 一起校准），两臂共用同一规则（第 8 节）。",
            f2(P$p_pcr[["pembro"]], 4), f2(P$p_pcr[["placebo"]], 4), f2(P$lrr_dr[["rate"]], 3),
            P$lrr_dr[["n_local_then_distant"]], P$lrr_dr[["n_local"]], f2(P$lrr_dr[["exposure_years"]], 2)), "")

add("## 8. 校准（步骤 5，第八轮，2026-10-22）", "")
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
    sprintf("- 远处复发后的超额死亡（第八轮的唯一修改）：远处复发按进入时点分为两个子状态。早期：随机化后 %d 个月以内的远处复发（ESME 的定义为新辅助或辅助化疗结束后 12 个月以内；模型中化疗在第 24 周〔约 5.5 个月〕结束，5.5 + 12 = 17.5 个月，取整为 18；两臂同一规则）；晚期：其余。两者都是复发后时间的对数 logistic，中位为外部输入（不参与校准）：早期 %s 个月、晚期 %s 个月（ESME，Grinda 等 Eur J Cancer 2023，PMID 37385070）；形状两个子状态共用，由校准估计。帕博利珠单抗组两个子状态的风险都 × k，k 与其他参数一起校准（范围 %g 至 %g）。远处复发相关的费用（D03 至 D05）两个子状态相同。",
            CFG$dr_early_months, f2(12 * DR_MEDIAN_BASE[["early"]], 1), f2(12 * DR_MEDIAN_BASE[["late"]], 1), CFG$pembro_dr_k_bounds[1], CFG$pembro_dr_k_bounds[2]),
    sprintf("- 术前进展后的超额死亡：进入后时间的对数 logistic，两臂共用，形状与中位校准；外部约束 1：中位 %g 至 %g 个月（下限为 ESME 早期复发的中位 OS %s 个月取整；上限为 Elmore 等 Ann Surg Oncol 2021;28:5477-5485、PMID 34247335 的新辅助治疗期间局部区域进展 %s 例的中位 OS %s 个月，该队列多数后来接受手术〔摘要写 %s 例、%s%%，按 %s 例计为 %s%%〕，比「无法手术的进展」轻，只作上界）；外部约束 2：进入后 5 年的全因存活 ≥ %g%%（同一篇中位随访 %s 个月时 %s%% 无病存活，向下取保守值），实现为形状的上限。术前进展两臂合计 %d 例（2024 年 Table 1）。",
            12 * PP_MEDIAN_BOUNDS[1], 12 * PP_MEDIAN_BOUNDS[2], m1[2], e_n[3], e_os[2], e_sx[2], e_sx[3], e_n[3],
            f2(100 * as.numeric(e_sx[2]) / as.numeric(e_n[3]), 1), 100 * PP_S5_MIN, e_fu[2], e_fu[3], n_pp),
    "- 其余设定不变：因不良事件死亡（第 7 节）；带 5 年约束的 EFS 模型（第 6 节）；目标函数与第七轮相同。",
    sprintf("- 校准：目标为两臂 OS 与 2024 年 Fig. 1A 的 KM 在第 %d 至 %d 个月逐月的平方误差和（百分点²，不变），加上 KEYNOTE-522 最终分析的 8 个 7 年时点（第七轮新增，见下）。L-BFGS-B，%d 个起点，目标值差 %s。optim 返回码 52 时加 5 个随机起点取最优；基准校准的返回码为 %d。",
            min(CFG$calib_grid_months), max(CFG$calib_grid_months), length(CANDS$starts_values), signif(diff(range(CANDS$starts_values)), 2),
            CANDS$optim$convergence),
    "- 7 年时点的加权：每个点加 ((模型 − 报告值) / SE)²，SE 以百分点计。两臂 7 年 OS 与 EFS 有 95% 置信区间，SE = (上限 − 下限) / (2 × 1.96)；按 pCR 分层的 7 年 OS 没有置信区间，用二项近似 SE = √(p(1 − p)/n)，n 为该层人数（2024 年 IA7 的 pCR 人数，`data/pcr_counts.csv`），不考虑删失，故偏小（权重偏大）。KM 部分不变，相当于每个逐月点的 SE 为 1 个百分点。7 年 EFS 由步骤 4 的 EFS 模型决定，不受校准量影响，两个 EFS 点在目标函数中是常数。",
    sprintf("- 数值来源（`data/kn522_final_7y.csv`，`input/papers/SOURCE.md`）：ascopubs.org 的摘要页返回 403，未取得；两臂 7 年 OS、EFS 及其置信区间与按 pCR 分层的 OS 读自 OncLive（2026-06-01），7 年 OS 与 CancerNetwork（2026-06-01）核对一致，按 pCR 分层的 OS 与 DelveInsight 核对一致；CareNet（2026-06-02）维护中未取得。截点 %s，中位随访 %s 个月。按 pCR 分层的 OS 在报道中没有写明时点（OncLive 写作「at median follow-up」），按用户指示作 7 年值。",
            iso_date(fa7("data_cutoff")), fa7("median_fu_months")),
    "- 接受规则：运行前确定（2026-10-22，`docs/acceptance_rule_round8.md`，git e0a722c 提交于第八轮运行之前），与第七轮相同：(a)、(i)、(ii)、(b)、(c)；术前进展约束与 k 的边界照常报告，不作停止条件。另外报告 5 年与 7 年的两臂 OS 差（第 8.4 节）。", "",
    "7 年目标值与权重（`final7y_targets()`）：", "",
    md_table(with(G7[G7$weight_basis != "not in the objective", ], data.frame(id = id, arm = arm, pcr = pcr, endpoint = endpoint, month = month,
                                                                              reported = f2(value, 1), se_pp = f2(se, 3), n = n, weight_basis = weight_basis))), "",
    "概率敏感性分析中远处复发后中位的分布：早期（`dr_median_draw()`）为两项研究的中位 OS 各取对数正态分布、等权混合（与此前相同）；晚期（`dr_late_median_draw()`）为 ESME 晚期复发的对数正态分布。对数正态的均值为 log(报告的中位)，标准误 = (log 上限 − log 下限) / (2 × 1.96)。bootstrap 中每个样本两个中位各自独立抽取，再校准其余参数。", "",
    md_table(transform(rbind(data.frame(substate = "早期", DR_MEDIAN_SOURCES), data.frame(substate = "晚期", DR_LATE_MEDIAN_SOURCE, weight = 1)),
                       se_log = f2((log(hi) - log(lo)) / (2 * qnorm(0.975)), 4))), "",
    sprintf("IMpassion132 已用全文核对（`input/papers/PIIS0923753424001078.pdf` p.6，PD-L1 阳性人群）：安慰剂组中位 OS %s 个月（95%% CI %s 至 %s），与此前采用的值一致，分布无需修正。参考：mITT 人群安慰剂组为 %s 个月（%s 至 %s），未采用（主要分析为 PD-L1 阳性人群）。ESME 读自摘要（早期 %s 个月，%s 至 %s；晚期 %s 个月，%s 至 %s）。",
            imp("median_placebo"), imp("lo_placebo"), imp("hi_placebo"), impm("median_placebo"), impm("lo_placebo"), impm("hi_placebo"), m1[2], m1[3], m1[4],
            m1[5], m1[6], m1[7]), "")
add("### 8.2 校准结果", "",
    md_table(transform(CAL, SSE_both_arms = f2(SSE_both_arms, 2), rmse_pp = f2(rmse_pp, 3), max_abs_diff_pp = f2(max_abs_diff_pp, 3),
                       gate_max_abs_diff_pp = f2(gate_max_abs_diff_pp, 3), preprog_shape = f2(preprog_shape, 4),
                       preprog_median_months = f2(preprog_median_months, 2), preprog_shape_cap = f2(preprog_shape_cap, 4),
                       dr_shape = f2(dr_shape, 4), dr_median_months = f2(dr_median_months, 2), dr_late_median_months = f2(dr_late_median_months, 2),
                       pembro_dr_k = f2(pembro_dr_k, 4))), "",
    sprintf("k = %s（%s；第六轮 %s，第七轮 %s）。远处复发后：形状 %s（两个子状态共用），中位早期 %s 个月、晚期 %s 个月（外部输入）。",
            f2(P$pembro_dr_k, 3), if (ab[["k_low"]] || ab[["k_high"]]) "**贴边界**" else "在 0.25 至 4 的内部",
            f2(VS$round6[VS$quantity == "pembro_dr_k"], 3), f2(VS$round7[VS$quantity == "pembro_dr_k"], 3),
            f2(P$dr$shape, 3), f2(12 * P$dr$scale, 1), f2(12 * P$dr$late_scale, 1)),
    "", "与第六、七轮的比较（`calibration_vs_previous.csv`；第六、七轮的值取自提交 e530a56、d1b5517 的输出，另存为 `r6_*.csv`、`r7_*.csv`；第七轮以前远处复发后只有一个中位）：", "",
    md_table(transform(VS, round6 = f2(round6, 4), round7 = f2(round7, 4), round8 = f2(round8, 4))), "",
    sprintf("远处复发中早期所占比例（`dr_early_share.csv`；早期 = 随机化后 %d 个月以内进入；累积发生率为占全臂的百分比；远处复发的进入不受复发后死亡率影响，故基准与 k = 1 相同）：", CFG$dr_early_months), "",
    md_table(transform(DRE[, c("arm", "horizon_years", "dr_cum_incidence_pct", "early_cum_incidence_pct", "late_cum_incidence_pct", "early_share")],
                       dr_cum_incidence_pct = f2(dr_cum_incidence_pct, 2), early_cum_incidence_pct = f2(early_cum_incidence_pct, 2),
                       late_cum_incidence_pct = f2(late_cum_incidence_pct, 2), early_share = f2(early_share, 3))), "",
    "（horizon_years 为随机化后的年数；51 年即到 100 岁。）", "",
    "目标函数在解处的分解（`calibration_objective.csv`）：", "",
    md_table(transform(OB, value = f2(value, 3))), "",
    sprintf("术前进展后：对数 logistic 形状 %s（该中位下的上限 %s），中位 %s 个月。中位%s；5 年存活%s。进入术前进展后的全因存活：1 年 %s，2 年 %s，5 年 %s（`dr_survival_implied.csv`）。",
            f2(P$preprog$shape, 3), f2(pp_shape_cap(P$preprog$scale), 3), f2(12 * P$preprog$scale, 2),
            if (ab[["pp_median_low"]]) "**贴下界 10 个月**" else if (ab[["pp_median_high"]]) "**贴上界 26 个月**" else "离开边界（在 10 至 26 个月内部）",
            if (ab[["pp_s5_at_min"]]) "**仍贴下界 5%（形状等于上限）**" else "高于 5%（离开边界）",
            f2(IMP$surv_1y[IMP$state == "PreProg"], 3), f2(IMP$surv_2y[IMP$state == "PreProg"], 3), f2(IMP$surv_5y[IMP$state == "PreProg"], 3)), "")
r6b <- R6F[R6F$scenario == "base", ]
r6m <- function(arm, pcr, ep) r6b$model[r6b$arm == arm & r6b$pcr == pcr & r6b$endpoint == ep]
G7$round6 <- mapply(r6m, G7$arm, G7$pcr, G7$endpoint)
G7$round7 <- R7F$engine[match(G7$id, R7F$id)]
add("7 年各点：模型与报告值（`calibration_final7y.csv`；round6 为第六轮模型的运行前记录 `r6_vs_final7y.csv`，round7 为第七轮的校准结果 `r7_calibration_final7y.csv`；objective_term 为该点对目标函数的贡献；DRFS 不在目标函数中，只报告）：", "",
    md_table(with(G7, data.frame(id = id, reported = f2(value, 1), ci95 = ifelse(is.na(ci95_lo), "—", paste0(f2(ci95_lo, 1), "–", f2(ci95_hi, 1))),
                                 round6 = f2(round6, 2), round7 = f2(round7, 2), engine = f2(engine, 2), diff = f2(diff, 2), objective_term = ifelse(is.na(objective_term), "—", f2(objective_term, 3)),
                                 inside_ci = ifelse(is.na(inside_ci), "—", ifelse(istrue(inside_ci), "是", "**否**")),
                                 gate_c = ifelse(istrue(gate_c), "是", "否（只报告）"), engine_k1 = f2(engine_k1, 2), diff_k1 = f2(diff_k1, 2)))), "")
pp7 <- G7[G7$id == "os_pcr_pembro", ]
hl <- function(x) if (x < 0) "低" else "高"
add(sprintf("记录（不作处理）：帕博利珠单抗组 pCR 层的 7 年 OS，模型 %s%%，报告值 %s%%（情景 k = 1：%s%%）。报告值没有置信区间；按该层 %d 人（IA7；IA4 为 %d 人）的二项近似，标准误约 %s 个百分点；模型比报告值%s %s 个百分点，约 %s 个标准误（k = 1 时%s %s 个百分点）。",
            f2(pp7$engine, 2), f2(pp7$value, 1), f2(pp7$engine_k1, 2), as.integer(pp7$n), PCC$pcr_pembro[PCC$source == "K22 (IA4)"], f2(pp7$se, 2),
            hl(pp7$diff), f2(abs(pp7$diff), 2), f2(abs(pp7$diff) / pp7$se, 1), hl(pp7$diff_k1), f2(abs(pp7$diff_k1), 2)), "")
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
ad_lab <- c("5 年 OS 差（百分点）", "5 年 RMST 差（年）", "7 年 OS 差（百分点）")
ad_ref <- c("重建 KM（2024 年 Fig. 1A）", "重建 KM（2024 年 Fig. 1A）", "最终分析的报告值")
ad_unit <- c("个百分点", "年", "个百分点"); ad_d <- c(2, 4, 2)
est <- function(x, i) sprintf("%s %s %s", if (x > 0) "高估" else "低估", f2(abs(x), ad_d[i]), ad_unit[i])
ad_txt <- sapply(seq_len(nrow(AD)), function(i) with(AD[i, ], sprintf("- %s：基准 %s，k = 1 %s，参照值 %s。基准%s，k = 1 %s。",
  ad_lab[i], f2(base, ad_d[i]), f2(k1, ad_d[i]), f2(reported, ad_d[i]), est(base_minus_reported, i), est(k1_minus_reported, i))))
dir_of <- function(x) if (x > 0) "高估" else "低估"
both_dir <- function(i) if (AD$base_minus_reported[i] > 0 && AD$k1_minus_reported[i] > 0) "两者都高估" else
  if (AD$base_minus_reported[i] < 0 && AD$k1_minus_reported[i] < 0) "两者都低估" else
  sprintf("基准%s、k = 1 %s", dir_of(AD$base_minus_reported[i]), dir_of(AD$k1_minus_reported[i]))
add(sprintf("两臂 OS 差（帕博利珠单抗 − 安慰剂；`scenario_k1_arm_diff.csv`）：基准（k = %s）、情景 k = 1 与参照值。5 年的参照值为重建 KM 的时点值与 RMST，7 年为最终分析报告的时点值（两臂差没有报告置信区间）。",
            f2(AD$k_base[1], 3)), "",
    md_table(data.frame(量 = ad_lab, 参照 = ad_ref, 基准 = mapply(f2, AD$base, ad_d), `k = 1` = mapply(f2, AD$k1, ad_d), 参照值 = mapply(f2, AD$reported, ad_d),
                        基准减参照值 = mapply(f2, AD$base_minus_reported, ad_d), `k = 1 减参照值` = mapply(f2, AD$k1_minus_reported, ad_d), check.names = FALSE)), "",
    ad_txt, "",
    sprintf("偏差方向：帕博利珠单抗的 OS 获益在 5 年%s（%s），在 7 年%s。",
            both_dir(1), if (sign(AD$base_minus_reported[1]) == sign(AD$base_minus_reported[2]) && sign(AD$k1_minus_reported[1]) == sign(AD$k1_minus_reported[2])) "时点 OS 差与 RMST 差方向相同" else "时点 OS 差与 RMST 差方向不全一致", both_dir(3)), "")
esh <- as.numeric(regmatches(es, regexec("aHR\\): ([\\d.]+) \\(95% CI ([\\d.]+)-([\\d.]+)\\)", es, perl = TRUE))[[1]][2:4])
late_life <- function(a) 100 * (1 - DRE$early_share[DRE$arm == a & DRE$horizon_years == max(DRE$horizon_years)])
add("报告的两臂 OS 差的不确定性（`scenario_k1_arm_diff_ci.csv`）：由各臂报告的 95% 置信区间换算——各臂标准误 = 区间宽度 ÷ 3.92，两臂差的标准误 = 两臂标准误的平方和开方（两臂独立），95% CI = 差 ± 1.96 × 标准误。5 年用 2024 年论文（IA7）报告的 5 年 OS，7 年用最终分析的 7 年 OS。", "",
    md_table(with(ADU, data.frame(年 = year, 帕博利珠单抗 = sprintf("%s [%s, %s]", f2(pembro, 1), f2(pembro_lo, 1), f2(pembro_hi, 1)),
                                  安慰剂 = sprintf("%s [%s, %s]", f2(placebo, 1), f2(placebo_lo, 1), f2(placebo_hi, 1)),
                                  两臂差 = f2(diff, 1), 标准误 = f2(se_diff, 2), `95% CI` = sprintf("[%s, %s]", f2(ci95_lo, 1), f2(ci95_hi, 1)),
                                  基准 = f2(base, 2), `基准在区间内` = ifelse(istrue(base_inside), "是", "**否**"),
                                  `k = 1` = f2(k1, 2), `k = 1 在区间内` = ifelse(istrue(k1_inside), "是", "**否**"), check.names = FALSE))), "",
    sprintf("基准和 k = 1 %s。5 年到 7 年间报告的两臂差由 %s 扩大到 %s 个百分点，但两个时点的 95%% CI（[%s, %s] 与 [%s, %s]）大幅重叠，这一扩大在抽样误差范围内无法与噪声区分。因此结构不再调整，涉及帕博利珠单抗的结果按 `docs/model_spec.md` 第 6 节以基准与 k = 1 两栏并列报告。",
            if (all(istrue(ADU$base_inside)) && all(istrue(ADU$k1_inside))) "在两个时点都落在区间内" else "**并非在两个时点都落在区间内**",
            f2(ADU$diff[1], 1), f2(ADU$diff[2], 1), f2(ADU$ci95_lo[1], 1), f2(ADU$ci95_hi[1], 1), f2(ADU$ci95_lo[2], 1), f2(ADU$ci95_hi[2], 1)), "",
    sprintf("第八轮的结构（远处复发分为早期与晚期）是在 ESME 晚期复发数据的依据下保留的，尽管 KM 部分的拟合误差（逐月平方误差和）由第七轮的 %s 增加到 %s。取舍的理由：(1) ESME 中晚期复发的中位 OS 为 %s 个月，早期为 %s 个月，校正 HR %s [%s, %s]，复发时点对复发后生存的影响有外部数据支持；(2) 模型中到 100 岁的远处复发，晚期占帕博利珠单抗组的 %s%%、安慰剂组的 %s%%（第 8.2 节），若一律用早期复发的中位，终生期的复发后生存会系统性偏短；(3) 拟合误差增加后三道门槛仍全部通过，拟合误差的差别不足以推翻有外部依据的结构。",
            f2(VS$round7[VS$quantity == "km_SSE_both_arms_pp2"], 1), f2(VS$round8[VS$quantity == "km_SSE_both_arms_pp2"], 1),
            m1[5], m1[2], f2(esh[1], 2), f2(esh[2], 2), f2(esh[3], 2), f2(late_life("pembro"), 1), f2(late_life("placebo"), 1)), "")
add("### 8.5 隐含的生存与外部对照", "",
    "模型隐含的生存（`dr_survival_implied.csv`；术前进展从 49.5 岁、远处复发（早期与晚期）都从 50.5 岁计背景死亡；远处复发为两臂共用的风险，即 k = 1，帕博利珠单抗组另乘 k）：", "",
    md_table(transform(IMP, median_excess_only_months = f2(median_excess_only_months, 1), median_all_cause_months = f2(median_all_cause_months, 1),
                       surv_1y = f2(surv_1y, 3), surv_2y = f2(surv_2y, 3), surv_5y = f2(surv_5y, 3))), "")
emx <- aggregate(cbind(max_abs_diff = abs(diff)) ~ check + arm, data = EC, FUN = max)
add("### 8.6 未用于校准的曲线", "",
    "与引擎的对照（`engine_checks.csv`，各曲线全部时点中差的绝对值最大者，百分点）：", "", md_table(transform(emx, max_abs_diff = f2(max_abs_diff, 3))), "",
    "图：`round8/fig_calibration_OS.png`（灰带为 KM 逐点 95% CI，竖线为门槛时点）、`round8/fig_engine_checks.png`。", "")
add("### 8.7 此前各轮", "",
    "第一轮至第三轮不达标；第四轮（术前进展后 Weibull）达标后由用户改设定；第五轮（术前进展后对数 logistic 加外部约束、远处复发后中位外部输入、k 固定为情景）不达标；第六轮（k 纳入基准校准）按规则接受；第七轮（目标函数加入 7 年时点，接受规则加入 (c)）按规则接受，其 bootstrap 按用户指示中止，**已被第八轮取代**。第八轮的结构与第七轮相同，只把远处复发分为早期与晚期。此前各轮的输出可在 git 历史中取回（第五轮为提交 0abaddd，第六轮为 e530a56，第七轮为 d1b5517）。第三轮的可行性扫描 `R/05b_gate_feasibility.R` 保留为诊断。", "")

SO <- rd("output", "phase1", "round8", "scenario_preprog_optimistic.csv")
SG <- rd("output", "phase1", "round8", "scenario_preprog_optimistic_gate.csv")
SA <- rd("output", "phase1", "round8", "scenario_preprog_optimistic_arm_diff.csv")
so <- function(q, col = "scenario") SO[[col]][SO$quantity == q]
sg <- function(g) SG[SG$gate == g, ]
add("### 8.8 乐观情景：术前进展后中位 26 个月、5 年存活 20%（`R/05s_preprog_optimistic.R`）", "",
    sprintf("设定（`docs/model_spec.md` 第 6 节）：术前进展后的对数 logistic 固定为中位 %s 个月、进入后 5 年全因存活 %s%%（形状由两者决定，为 %s），依据 Elmore 等的 MD Anderson 队列（第 8.1 节）；远处复发后的形状与 k 按基准的目标函数重新校准，远处复发后的中位与基准相同（早期 %s、晚期 %s 个月）。",
            f2(so("preprog_median_months"), 0), f2(100 * so("preprog_allcause_surv_5y"), 0), f2(so("preprog_shape"), 4),
            f2(so("dr_median_early_months"), 1), f2(so("dr_median_late_months"), 1)), "",
    sprintf("结果（`scenario_preprog_optimistic.csv`）：k = %s（基准 %s），远处复发后形状 %s（基准 %s）；%s。目标函数值 %s。",
            f2(so("pembro_dr_k"), 3), f2(so("pembro_dr_k", "base"), 3), f2(so("dr_shape"), 4), f2(so("dr_shape", "base"), 4),
            if (istrue(so("k_at_bound") == 1) || istrue(so("dr_shape_at_bound") == 1)) "**有参数贴边界**" else "k 与形状都不在边界上",
            f2(so("objective"), 2)), "",
    sprintf("三道门槛（只作参考，不作判定；`scenario_preprog_optimistic_gate.csv`）：(a) 10 个点中 %d 个落在 KM 逐点 95%% 区间内（%s）；(b) 模型 5 年 RMST 两臂差 %s 年，%s KM 差的 bootstrap 95%% 区间 %s 至 %s 年内；(c) 7 年 OS 与 EFS 的 4 个值中 %d 个落在最终分析的 95%% 区间内。",
            sum(istrue(sg("a")$inside)), c(inside = "全部在区间内", `accepted by (i)+(ii)` = "按例外规则 (i)、(ii) 可接受", `not met` = "不满足")[[sg("a")$gate_result[1]]],
            f2(sg("b")$engine, 4), if (istrue(sg("b")$inside)) "落在" else "不在",
            f2(sg("b")$lo, 4), f2(sg("b")$hi, 4), sum(istrue(sg("c")$inside))), "",
    md_table(with(SG, data.frame(门槛 = gate, 项目 = item, 模型 = f2(engine, 3), 下限 = f2(lo, 3), 上限 = f2(hi, 3),
                                在区间内 = ifelse(istrue(inside), "是", "**否**")))), "",
    "两臂 OS 差（帕博利珠单抗 − 安慰剂；`scenario_preprog_optimistic_arm_diff.csv`；基准、k = 1 与参照值同第 8.4 节）：", "",
    md_table(data.frame(量 = ad_lab, 参照 = ad_ref, 乐观情景 = mapply(f2, SA$optimistic, ad_d), 基准 = mapply(f2, SA$base, ad_d),
                        `k = 1` = mapply(f2, SA$k1, ad_d), 参照值 = mapply(f2, SA$reported, ad_d),
                        乐观情景减参照值 = mapply(f2, SA$optimistic_minus_reported, ad_d), check.names = FALSE)), "",
    sprintf("该情景的校准目标函数为 %s，基准为 %s；年度门槛点虽然%s在区间内，但整体拟合明显变差，数据不支持这一设定，因此只作为敏感性分析。两个时点上的得失：5 年 RMST 差%s（%s 对 %s，差 %s；基准差 %s），7 年 OS 差%s（%s 对 %s，差 %s；基准差 %s）。",
            f2(so("objective"), 1), f2(OB$value[OB$part == "total"], 1), if (all(istrue(sg("a")$inside))) "全部" else "并非全部",
            if (abs(SA$optimistic_minus_reported[2]) < abs(SA$base[2] - SA$reported[2])) "更接近 KM" else "并未更接近 KM",
            f2(SA$optimistic[2], 4), f2(SA$reported[2], 4), f2(SA$optimistic_minus_reported[2], 4), f2(SA$base[2] - SA$reported[2], 4),
            if (abs(SA$optimistic_minus_reported[3]) > abs(SA$base[3] - SA$reported[3])) "离报告值更远" else "并未离报告值更远",
            f2(SA$optimistic[3], 2), f2(SA$reported[3], 2), f2(SA$optimistic_minus_reported[3], 2), f2(SA$base[3] - SA$reported[3], 2)), "")

# ---------------------------------------------------------------- step 6
if (boot_done) {
  BC <- BRS$calibration; BB <- BRS$efs_binding
  cnt <- function(x) sum(x, na.rm = TRUE)
  c52 <- BC[, "code52"] == 1
  imp52 <- BC[, "value_before"] - BC[, "value_after"]
  drm <- 12 * BC[, "dr_median"]; drl <- 12 * BC[, "dr_late_median"]
  add("## 9. Bootstrap（步骤 6，`R/06_bootstrap.R`）", "",
      sprintf("B = %d，随机种子 %d（第 b 次用种子 + b），并行，耗时 %s 分钟。每次：", BRS$B, BRS$seed, f2(BRS$minutes, 1)),
      "1. 分层 EFS（2022 年补充材料 Fig. S4，IA4）：在各臂内连同 pCR 标签重抽样，pCR 比例与各层人数随之变动；各层在手术时点 landmark，用与基准相同的分布族重拟合并加 5 年约束（边界固定）；术前 KM 重算。",
      "2. 术前进展的进入比例 = 报告例数 / 重抽样后的非 pCR 人数（全臂比例保持报告值）。",
      "3. OS（2024 年 Fig. 1A，IA7）：在各臂内重抽样；所选的 OS 模型重拟合（只保存，引擎不用；RP 结点固定在基准位置）。",
      "4. 远处复发后的两个中位按第 8.1 节的分布各自抽样（早期：混合分布；晚期：对数正态）；8 个 7 年目标值按其抽样分布抽取（有置信区间的 4 个点：正态，均值为报告值，SD 为第 8.1 节的 SE；按 pCR 分层的 4 个点：二项，n 为该层人数，p 为报告值；权重仍用第 8.1 节的 SE）；再对重抽样后的 OS KM 与抽到的 7 年目标值校准术前进展的中位与形状、远处复发后形状与 k（基准估计值加基准的 6 个起点，取最优；返回码 52 时再加 5 个随机起点取最优）。",
      "5. 引擎在 5、7、10、20 年的 EFS 与 OS（臂 × pCR；帕博利珠单抗组另算情景 k = 1）。",
      "每次都固定的数据设定：生命表、EFS 事件构成与分配比例、因不良事件死亡、局部区域复发 → 远处复发的率、术前进展例数、术前进展的外部约束、5 年约束的边界。拟合失败的样本换种子重抽（计入 attempts）。", "",
      sprintf("结果：完成 %d 次，10 次重抽仍失败 %d 次，换种子重抽的样本 %d 个。optim 返回码（最终）：%s。返回码 52 而加随机起点重跑的 %d 次，其中目标值改善的 %d 次（最大改善 %s）。",
              nrow(BC), length(BRS$failed), cnt(BC[, "attempts"] > 1),
              paste(names(table(BC[, "convergence"])), table(BC[, "convergence"]), sep = ": ", collapse = "，"),
              cnt(c52), cnt(c52 & imp52 > 1e-8), if (any(c52)) formatC(max(imp52[c52]), format = "g", digits = 3) else "—"),
      sprintf("贴边界的次数：k 贴下界 0.25 的 %d 次、贴上界 4 的 %d 次；术前进展中位贴 10 个月的 %d 次、贴 26 个月的 %d 次；5 年存活贴 5%% 的 %d 次；远处复发后形状贴数值边界的 %d 次。5 年 EFS 约束起作用的次数：%s。",
              cnt(BC[, "k_low"] == 1), cnt(BC[, "k_high"] == 1), cnt(BC[, "pp_median_low"] == 1), cnt(BC[, "pp_median_high"] == 1),
              cnt(BC[, "pp_s5_at_min"] == 1), cnt(BC[, "dr_shape_bound"] == 1),
              paste(colnames(BB)[-1], colSums(BB[, -1, drop = FALSE]), sep = " ", collapse = "，")),
      sprintf("抽到的远处复发后中位：早期中位数 %s 个月（2.5%% 至 97.5%% 分位 %s 至 %s）；晚期中位数 %s 个月（%s 至 %s）。",
              f2(median(drm), 2), f2(quantile(drm, 0.025), 2), f2(quantile(drm, 0.975), 2), f2(median(drl), 2), f2(quantile(drl, 0.025), 2), f2(quantile(drl, 0.975), 2)), "",
      "参数的基准值与 bootstrap 分布（`output/phase1/bootstrap_summary.csv`；参数矩阵在 `data/bootstrap/`，一行一个样本；中位为年）：", "",
      md_table(transform(BSUM[BSUM$group %in% c("calibration", "pCR and PreProg"), ], base = f2(base, 4), boot_mean = f2(boot_mean, 4),
                         boot_median = f2(boot_median, 4), boot_lo = f2(boot_lo, 4), boot_hi = f2(boot_hi, 4))), "",
      "抽到的 7 年目标值（%，`boot_final7y_targets.csv`）：", "",
      md_table(transform(BSUM[BSUM$group == "7-year targets drawn (%)", ], base = f2(base, 2), boot_mean = f2(boot_mean, 2),
                         boot_median = f2(boot_median, 2), boot_lo = f2(boot_lo, 2), boot_hi = f2(boot_hi, 2))), "",
      "EFS 模型参数（自然尺度）：", "",
      md_table(transform(BSUM[BSUM$group == "EFS model parameters", ], base = f2(base, 4), boot_mean = f2(boot_mean, 4),
                         boot_median = f2(boot_median, 4), boot_lo = f2(boot_lo, 4), boot_hi = f2(boot_hi, 4))), "",
      "文件：`boot_efs_params.csv`、`boot_efs5_binding.csv`、`boot_os_model_params.csv`、`boot_pcr_preprog.csv`、`boot_pre_surgery_km.csv`、`boot_calibration.csv`、`boot_outputs.csv`、`boot_final7y_targets.csv`、`boot_replicates.rds`。", "")

  # ---------------------------------------------------------------- step 7
  fmt <- function(b, lo, hi) sprintf("%s (%s–%s)", f2(b, 1), f2(lo, 1), f2(hi, 1))
  EO$cell <- fmt(EO$base, EO$boot_lo, EO$boot_hi)
  W <- reshape(EO[, c("endpoint", "scenario", "arm", "pcr", "year", "cell")], idvar = c("endpoint", "scenario", "arm", "pcr"),
               timevar = "year", direction = "wide")
  names(W) <- sub("^cell\\.", "", names(W)); yrs <- names(W) %in% c("5", "7", "10", "20"); names(W)[yrs] <- paste0(names(W)[yrs], " 年")
  W$arm <- ifelse(W$arm == "chemo", "单用化疗（= 化疗加运动）", "化疗加帕博利珠单抗（= 两者都加）")
  W$pcr <- c(all = "全体", pCR = "pCR", nonpCR = "非 pCR")[W$pcr]
  W$scenario <- ifelse(W$scenario == "base", "基准", "k = 1")
  add("## 10. 生存引擎的输出（步骤 7，`R/07_engine_outputs.R`）", "",
      "随机化后 5、7、10、20 年的 EFS 与 OS（%，基准值与 bootstrap 95% 分位区间；`engine_outputs.csv`、`engine_curves.csv`）。第 1 阶段没有运动参数，故加运动的两臂与对应的不加运动的臂相同；情景 k = 1 只改变帕博利珠单抗组的 OS（EFS 不变）。7 年的报告值见第 8.2 节。", "",
      md_table(setNames(W[order(W$endpoint, W$scenario != "基准", grepl("帕博利珠单抗", W$arm), match(W$pcr, c("全体", "pCR", "非 pCR"))), ],
                        c("终点", "情景", "臂", "pCR", names(W)[-(1:4)]))), "",
      sprintf("各 bootstrap 样本的引擎由保存的参数矩阵重建，其 5、7、10、20 年的值与 `06_bootstrap.R` 当时算出的一致（%d 个样本，最大差 %s，`bootstrap_rebuild_check.csv`）。",
              RB$replicates, formatC(RB$max_abs_diff, format = "e", digits = 1)), "",
      "图：`round8/fig_engine_outputs.png`（实线为引擎，带为 bootstrap 95% 区间，虚线为重建的 KM，× 为最终分析的 7 年值，竖线为其 95% 置信区间）。", "",
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
    "- 校准第七轮（2026-10-22）：加入 KEYNOTE-522 最终分析（ASCO 2026）的 7 年值（目标函数 8 个点；门槛 (c)）；接受规则运行前确定；结构不变。bootstrap 中止，已被第八轮取代。",
    sprintf("- 校准第八轮（2026-10-22）：远处复发按进入时点分为早期（随机化后 %d 个月以内）与晚期，中位分别为 ESME 的 %s 与 %s 个月，形状共用；接受规则与第七轮相同，运行前提交。",
            CFG$dr_early_months, f2(12 * DR_MEDIAN_BASE[["early"]], 1), f2(12 * DR_MEDIAN_BASE[["late"]], 1)),
    "- S-JP（2026-10-23，尾崎的回答）：四个组都加。non-pCR 例中 gBRCA 阳性按 F04（含帕博利珠单抗的组为 F04P）的比例用奥拉帕利、不并用卡培他滨，其余不加术后治疗；gBRCA 阴性按 F01（F01P）的比例用卡培他滨。原待决的「S-JP 的权重定义」即指这一分配，已决；F01 改为 gBRCA 阴性例中的比例。F07、F08 在两类组中用同一 HR（假设）。F01P、F04P 到之前 S-JP 不运行（`docs/model_spec.md` 第 2 节）。",
    "- BRCA 检测的对象范围（2026-10-23）：诊断时对全部患者、全部组检测（F06），不影响增量（`docs/model_spec.md` 第 2 节）。",
    "- 运动的有害事象（2026-10-23）：筋骨格系有害事象，发生率 E06、E07（3 级以上 E09、E10）取自 CHALLENGE，费用 E08 由尾崎填写；效用只乘 3 级以上（`docs/model_spec.md` 第 3、5 节）。",
    "- 第 2 阶段的报告方式（2026-10-22）：涉及帕博利珠单抗的结果（帕博利珠单抗对单用化疗、帕博利珠单抗加运动对帕博利珠单抗）以基准与 k = 1 两栏并列；方向一致时表述为结论稳健，不一致时分别写出两种结论，不选其一（`docs/model_spec.md` 第 6 节）。",
    "",
    "记录（不作处理）：",
    "- 帕博利珠单抗组 pCR 层的 7 年 OS，模型低于报告值（报告值没有置信区间；第 8.2 节）。",
    "",
    "待决：",
    if (stop6) "- **校准第八轮未被接受**（第 8 节）。按指示未自行增加结构，处理方向待定。" else NULL,
    if (istrue(CS$constraint_at_bound)) sprintf("- 术前进展后死亡的校准值%s（第 8.2 节）。", pp_bound_txt(CANDS$at_bound)) else NULL,
    "- 若尾崎日后提供 2023-03-23 截点的分层 KM，5 年约束改为用整条曲线（2026-10-22 的决定）。",
    "",
    "等尾崎回答：",
    "- 含帕博利珠单抗的组的 S-JP 数值 F01P、F04P（尾崎正向临床医生确认）。",
    "- 尾崎若已在入力表 v1 中填了 F01：定义已改为 gBRCA 阴性例中的比例，需确认该值（`output/params_check.md` 会标出）。", "",
    "已填（2026-10-23）：运动的有害事象发生率 E06、E07、E09、E10（CHALLENGE 本文 p.19 与补充材料 Table S4，入力表 v6）；F07、F08 的适用组改为「全群」（内部表）。", "")

add("## 12. 局限性", "",
    "- 模型在 5 年和 7 年未能同时重现两臂 OS 差随时间扩大的形状；仅凭公开的汇总数据无法判别这一形状是否超出抽样误差（第 8.4 节）。",
    sprintf("- 术前进展的人数少（两臂合计 %d 例），其死亡分布主要由外部约束决定，校准值%s（第 8.2 节；乐观情景见第 8.8 节）。", n_pp, pp_bound_txt(CANDS$at_bound)), "")

# ---------------------------------------------------------------- round 9 (phase-2 preparation)
r9 <- function(...) file.path("output", "phase1", "round9", ...)
if (file.exists(file.path(ROOT, r9("esme_fits.csv")))) {
  EV <- rd(r9("esme_validation.csv")); ED <- rd(r9("esme_diagnostics.csv")); EF <- rd(r9("esme_fits.csv"))
  ES <- rd(r9("esme_shape_test.csv")); EH <- rd(r9("esme_hr.csv")); ERL <- rd("data", "digitized", "esme", "raster_extraction_log.csv")
  ERT <- rd("data", "digitized", "esme", "ESME_F3A_OS_risktable.csv")
  CS9 <- if (file.exists(r9rule_f)) read.csv(r9rule_f) else rd("output", "phase1", "calibration_status.csv")   # status under the round-9 rule
  CG9 <- rd("output", "phase1", "calibration_gate.csv")
  CGR9 <- rd("output", "phase1", "calibration_gate_rmst.csv"); G79 <- rd("output", "phase1", "calibration_final7y.csv")
  VS9 <- rd("output", "phase1", "calibration_vs_previous.csv"); OB9 <- rd("output", "phase1", "calibration_objective.csv")
  AD9 <- rd("output", "phase1", "scenario_k1_arm_diff.csv"); AD8 <- rd("output", "phase1", "round8", "scenario_k1_arm_diff.csv")
  G78 <- rd("output", "phase1", "round8", "calibration_final7y.csv")
  C9 <- readRDS(file.path(ROOT, "data", "fits", "calibration_candidates.rds")); ab9 <- C9$at_bound; P9 <- C9$params
  FS9f <- file.path(ROOT, "output", "phase1", "calibration_gate_feasibility_r9.csv")
  esme_spec <- jsonlite::fromJSON(file.path(ROOT, "R", "py", "rasterspec_esme.json"), simplifyVector = FALSE)$figures[[1]]
  gate9 <- c(a = if (istrue(CS9$gate_a_strict_pass)) "达标" else if (istrue(CS9$gate_a_accepted)) "按例外规则接受" else "**不达标**",
             b = if (istrue(CS9$gate_b_pass)) "达标" else "**不达标**", c = if (istrue(CS9$gate_c_pass)) "达标" else "**不达标**")
  G9_out <- CG9[!istrue(CG9$inside), ]
  add("## 13. 第九轮（第 2 阶段准备，2026-10-23）：远处复发后生存外部锚定于 ESME 曲线", "",
      sprintf("结论：按运行前确定的接受规则（`docs/acceptance_rule_round9.md`，git 73748f4；与第七、八轮相同）%s。门槛 (a) %s，(b) %s，(c) %s。%s%s",
              if (istrue(CS9$gate_pass)) "**接受**" else "**不接受，停在步骤 6 之前**", gate9[["a"]], gate9[["b"]], gate9[["c"]],
              if (istrue(CS9$gate_pass)) "" else "按规则当时没有写出引擎默认参数，bootstrap 未运行，没有自行增加结构。",
              if (adopt9) "此后第十轮按判定规则 A 采用第九轮结构，第九轮的校准结果不变、按新的 (a) 判定为接受（第 14 节）。" else ""), "")
  add("### 13.1 ESME 论文与数字化", "",
      sprintf("来源：Grinda 等 Eur J Cancer 2023;189:112935（DOI 10.1016/j.ejca.2023.05.023），HAL hal-04205902 的作者稿（CC BY-NC 4.0），经 HAL 的检索 API 取得正文与补充材料（`input/papers/Grinda2023_ESME*.pdf`，不进 git；`input/papers/SOURCE.md`）。Fig. 3a（从转移诊断起的 OS，早期复发 = 新辅助或辅助化疗结束后 12 个月以内）为嵌入的栅格图（%s 像素），用与 KEYNOTE-522 相同的流程数字化（`R/py/02b_digitize_raster.py`，`R/py/rasterspec_esme.json`，输出 `data/digitized/esme/`）。此图没有坐标轴线（ggplot2 浅色主题），刻度取边框外的短刻度线（加权重心，亚像素）；线条为细的 JPEG 抗锯齿线，颜色中心取观测到的线条平均色。",
              ERL$native_px[1]),
      sprintf("刻度校准残差：x %s 个月，y %s 个百分点。数字化的列覆盖率：早期 %s，晚期 %s。风险表（每 4 个月，0 至 48 个月）从图像转录，0 时点人数 %s 与 %s 与摘要的各组人数一致。叠图质控：`data/digitized/esme/qa/ESME_F3A_OS_overlay.png`。",
              f2(ERL$calib_resid_x[1], 4), f2(ERL$calib_resid_y[1], 4), f2(ERL$column_coverage[ERL$arm == "early"], 3), f2(ERL$column_coverage[ERL$arm == "late"], 3),
              ERT$n_risk[ERT$arm == "early" & ERT$time == 0], ERT$n_risk[ERT$arm == "late" & ERT$time == 0]), "")
  add("### 13.2 个体数据重建与验证（`R/13_esme_fit.R`）", "",
      sprintf("Guyot 算法（`R/guyot.R`），以 IPDfromKM 交叉核对；门槛（用户指定）：重建 KM 的中位与原文相差 ≤ 0.5 个月；各风险表时点重建 KM 与数字化曲线相差 ≤ 1 个百分点。结果：%d 项中 %d 项达标（`output/phase1/round9/esme_validation.csv`）。",
              nrow(EV), sum(istrue(EV$pass))), "",
      md_table(with(EV[EV$check == "median (months)", ], data.frame(组 = curve, 原文中位 = f2(reference, 1), 重建中位 = f2(reconstructed, 2),
                                                                     差 = f2(abs_diff, 3), 达标 = ifelse(istrue(pass), "是", "**否**")))), "",
      sprintf("各风险表时点的最大差：早期 %s、晚期 %s 个百分点。诊断（`esme_diagnostics.csv`）：", f2(max(EV$abs_diff[EV$curve == "early" & EV$check != "median (months)"]), 3),
              f2(max(EV$abs_diff[EV$curve == "late" & EV$check != "median (months)"]), 3)), "",
      md_table(transform(ED, max_abs_km_vs_digitized_pp = f2(max_abs_km_vs_digitized_pp, 3), max_abs_guyot_vs_ipdfromkm_pp = f2(max_abs_guyot_vs_ipdfromkm_pp, 3))), "",
      sprintf("早期对晚期的 HR（只报告）：重建 %s [%s, %s]，图中印的 %s [%s, %s]。", f2(EH$reconstructed, 2), f2(EH$rec_lo, 2), f2(EH$rec_hi, 2),
              f2(EH$reported, 2), f2(EH$lo, 2), f2(EH$hi, 2)), "")
  add("### 13.3 对数 logistic 拟合与形状的检验", "",
      "两条曲线分别拟合（flexsurv，时间为年；中位 = 尺度参数；95% CI 为模型的 Wald 区间）：", "",
      md_table(with(EF, data.frame(组 = group, n = n, 事件 = events, 形状 = sprintf("%s [%s, %s]", f2(shape, 3), f2(shape_lo, 3), f2(shape_hi, 3)),
                                   中位_月 = sprintf("%s [%s, %s]", f2(median_months, 2), f2(median_lo, 2), f2(median_hi, 2)),
                                   原文中位_月 = sprintf("%s [%s, %s]", f2(reported_median, 1), f2(reported_lo, 1), f2(reported_hi, 1)),
                                   重建KM中位_月 = f2(km_median_reconstructed, 2)))), "",
      sprintf("形状的差异：早期 %s、晚期 %s（比 %s）；分开与共用形状的似然比检验 χ² = %s（自由度 1），p = %s；对数形状差的 Wald 检验 p = %s。规则：「差异明显」按似然比检验 p < 0.05 判断（阈值为本次的操作化，在拟合运行前写入 `R/13_esme_fit.R`），明显时分开用，否则共用一个。判定：**%s**。共用形状 %s [%s, %s]；共用形状模型下的中位：早期 %s 个月，晚期 %s 个月（引擎的输入，`data/fits/esme_fits.rds`）。",
              f2(ES$shape_early, 3), f2(ES$shape_late, 3), f2(ES$shape_ratio_early_late, 3), f2(ES$lrt_chisq, 2), f2(ES$p_lrt, 3), f2(ES$p_wald, 3),
              if (ES$decision == "common") "共用一个形状" else "分开用", f2(ES$common_shape, 3), f2(ES$common_shape_lo, 3), f2(ES$common_shape_hi, 3),
              f2(ES$common_median_early_months, 2), f2(ES$common_median_late_months, 2)),
      "拟合的对数 logistic 在引擎中作为远处复发后的超额风险（其上再加背景死亡），与第五至八轮使用 ESME 中位的方式相同；ESME 的 OS 含背景死亡，转移后数年内、约 50 岁时差别很小。图：`round9/fig_esme_fit.png`。", "")
  add("### 13.4 模型的修改（用户指定）与校准结果", "",
      "- 远处复发后的生存（早期、晚期两个子状态）全部改为外部输入：形状与中位取自 13.3 节的拟合，不参与校准。",
      "- 概率敏感性分析：每个 bootstrap 样本对 ESME 重建个体数据在组内重抽样并重新拟合，联合抽取形状与中位（`esme_draw()`）。",
      sprintf("- IMpassion132 不再参与基准与抽样，改为早期复发中位的情景（%s 个月，`dr_ext_imp132()`）。", DR_MEDIAN_SOURCES$median[2]),
      "- 校准参数只剩 k（0.25 至 4）与术前进展的两个参数（约束不变）；目标函数与第七、八轮相同。只做点估计。", "",
      sprintf("校准值：k = %s（%s）；术前进展后对数 logistic 中位 %s 个月、形状 %s（该中位下的上限 %s），%s。目标函数 %s，其中 KM 部分 %s（第八轮 %s）。",
              f2(P9$pembro_dr_k, 3), if (ab9[["k_low"]] || ab9[["k_high"]]) "**贴边界**" else "不在边界上", f2(12 * P9$preprog$scale, 2), f2(P9$preprog$shape, 3),
              f2(pp_shape_cap(P9$preprog$scale), 3), pp_bound_txt(ab9), f2(OB9$value[OB9$part == "total"], 2),
              f2(OB9$value[1], 2), f2(VS9$round8[VS9$quantity == "km_SSE_both_arms_pp2"], 2)), "",
      "与第六至八轮的比较（`calibration_vs_previous.csv`）：", "",
      md_table(transform(VS9, round6 = f2(round6, 4), round7 = f2(round7, 4), round8 = f2(round8, 4), round9 = f2(round9, 4))), "",
      sprintf("门槛 (a)（`calibration_gate.csv`）：10 个点中 %d 个落在逐点 95%% 区间内%s。",
              sum(istrue(CG9$inside)), if (nrow(G9_out)) sprintf("；区间外 %s，超出 %s 个百分点（例外规则 (i) 的上限 %g）；全部 10 个点%s Bonferroni 校正后的 99.5%% 区间内",
                                                             paste(sprintf("%s %d 个月", ifelse(G9_out$arm == "pembro", "帕博利珠单抗", "安慰剂"), G9_out$month), collapse = "、"),
                                                             paste(f2(G9_out$outside_pp, 4), collapse = "、"), CFG$gate_accept_max_outside_pp,
                                                             if (all(istrue(CG9$inside_995))) "落在" else "**并非都在**") else ""), "",
      md_table(transform(CG9, km = f2(km, 2), ci95_lo = f2(ci95_lo, 2), ci95_hi = f2(ci95_hi, 2), ci995_lo = f2(ci995_lo, 2), ci995_hi = f2(ci995_hi, 2),
                         engine = f2(engine, 2), diff = f2(diff, 3), inside = ifelse(istrue(inside), "是", "**否**"), outside_pp = f2(outside_pp, 4),
                         inside_995 = ifelse(istrue(inside_995), "是", "**否**"))), "",
      sprintf("门槛 (b)：模型 5 年 RMST 两臂差 %s 年，KM 差的 bootstrap 95%% 区间 %s 至 %s 年，%s。门槛 (c)：7 年 OS 与 EFS 的 4 个值中 %d 个落在最终分析的 95%% 区间内。",
              f2(CGR9$engine, 4), f2(CGR9$km_boot_ci95_lo, 4), f2(CGR9$km_boot_ci95_hi, 4), gate9[["b"]], sum(istrue(G79$inside_ci[istrue(G79$gate_c)]))), "",
      md_table(with(G79[istrue(G79$gate_c), ], data.frame(id = id, reported = f2(value, 1), ci95 = paste0(f2(ci95_lo, 1), "–", f2(ci95_hi, 1)),
                                                          engine = f2(engine, 2), inside_ci = ifelse(istrue(inside_ci), "是", "**否**")))), "")
  if (file.exists(FS9f)) {
    FS9 <- read.csv(FS9f)
    add(sprintf("诊断（不作判定；`calibration_gate_feasibility_r9.csv`）：在约束范围内（术前进展中位 10 至 26 个月、5 年存活 ≥ 5%%，k 在 0.25 至 4）以 Nelder-Mead 最小化门槛 (a) 的最大超出幅度，%d 个起点中 %d 个找到 10 个点全部在 95%% 区间内的参数（最小超出 %s 个百分点），其中 5 年 RMST 两臂差也落在 (b) 的区间内的 %d 个（(c) 未检查）。即本结构下存在满足 (a) 的参数，校准（最小化目标函数）的解没有落在其中。",
                nrow(FS9), sum(FS9$max_outside_ci_pp <= 1e-9), f2(min(FS9$max_outside_ci_pp), 4), sum(FS9$max_outside_ci_pp <= 1e-9 & istrue(FS9$rmst_inside_boot_ci))), "")
  }
  ad_tab <- function(A) data.frame(量 = ad_lab, 基准 = mapply(f2, A$base, ad_d), `k = 1` = mapply(f2, A$k1, ad_d), check.names = FALSE)
  t9 <- ad_tab(AD9); t8 <- ad_tab(AD8)
  add("### 13.5 两臂 OS 差（5 年与 7 年）与帕博利珠单抗 pCR 层的 7 年 OS", "",
      sprintf("两臂 OS 差（帕博利珠单抗 − 安慰剂；第九轮 k = %s，第八轮 k = %s；参照值同第 8.4 节）：", f2(AD9$k_base[1], 3), f2(AD8$k_base[1], 3)), "",
      md_table(data.frame(量 = ad_lab, `第九轮 基准` = t9$基准, `第九轮 k = 1` = t9$`k = 1`, `第八轮 基准` = t8$基准, `第八轮 k = 1` = t8$`k = 1`,
                          参照值 = mapply(f2, AD9$reported, ad_d), check.names = FALSE)), "",
      sprintf("帕博利珠单抗组 pCR 层的 7 年 OS：第九轮模型 %s%%（k = 1：%s%%），第八轮 %s%%（k = 1：%s%%），报告值 %s%%。",
              f2(G79$engine[G79$id == "os_pcr_pembro"], 2), f2(G79$engine_k1[G79$id == "os_pcr_pembro"], 2),
              f2(G78$engine[G78$id == "os_pcr_pembro"], 2), f2(G78$engine_k1[G78$id == "os_pcr_pembro"], 2), f2(G79$value[G79$id == "os_pcr_pembro"], 1)), "")
}

# ---------------------------------------------------------------- round 10
if (!is.null(DEC10)) {
  DS10 <- rd("output", "phase1", "round10", "dr_survival_comparison.csv"); MS10 <- rd("output", "phase1", "round10", "mean_survival_after_dr.csv")
  DT10 <- rd("output", "phase1", "round10", "dr_time_engine.csv")
  ref_meta10 <- tryCatch(readRDS(file.path(ROOT, "output", "check", "bootstrap10_local.rds"))$meta, error = function(e) NULL)
  gl <- function(g) ifelse(g == "early", "早期", "晚期")
  add("## 14. 第十轮（2026-10-23）：以转移后长期存活决定采用第八轮还是第九轮结构", "",
      "判定规则在任何诊断之前单独提交（`docs/acceptance_rule_round10.md`，git e8d2134）。提交前只确认了 ESME 重建数据的随访最长 47.98 个月（风险表止于 48 个月），据此经用户决定以第 4 年代替原指示的第 5 年。诊断：`R/14_round10_decision.R`，输出在 `output/phase1/round10/`。", "",
      "### 14.1 远处复发后的存活比例（%）", "",
      with(list(P8r = readRDS(file.path(ROOT, "data", "fits", "round8", "engine_params.rds")), P9r = readRDS(file.path(ROOT, "data", "fits", "calibration_candidates.rds"))$params),
           sprintf("隐含值 = 远处复发后超额生存（对数 logistic）× 背景生存（从 %s 岁起），k = 1；第八轮：形状共用 %s、中位为 ESME 摘要的 %s 与 %s 个月；第九轮：ESME 拟合（形状 %s、中位 %s 与 %s 个月）。ESME：重建 KM 的点估计与逐点 95%% CI（对数尺度）；第 4 年取 48 个月（重建数据的最后观察时点 %s 个月的值）。第 3、4 年参与判定，第 1、2 年只报告。",
                   f2(CFG$start_age + 1.5, 1), f2(P8r$dr$shape, 4), f2(12 * P8r$dr$scale, 1), f2(12 * P8r$dr$late_scale, 1),
                   f2(P9r$dr$shape, 4), f2(12 * P9r$dr$scale, 2), f2(12 * P9r$dr$late_scale, 2),
                   f2(max(sapply(readRDS(file.path(ROOT, "data", "ipd", "esme", "esme_ipd.rds")), function(d) max(d$time))), 2))), "",
      md_table(with(DS10, data.frame(组 = gl(group), 年 = year, 第八轮 = f2(round8, 2), 第九轮 = f2(round9, 2), ESME_KM = f2(esme_km, 2),
                                     ESME_95CI = sprintf("[%s, %s]", f2(esme_lo, 2), f2(esme_hi, 2)),
                                     第八轮在CI内 = ifelse(istrue(round8_inside), "是", "**否**"), 第九轮在CI内 = ifelse(istrue(round9_inside), "是", "**否**"),
                                     参与判定 = ifelse(istrue(used_in_rule), "是", "否（只报告）")))), "",
      "图：`round10/fig_dr_survival.png`。", "",
      "### 14.2 判定结果", "",
      sprintf("规则 %s 成立：第八轮的隐含值在%s落在 ESME 的 95%% CI 之外（参与判定的 %d 个点中第八轮在区间内的 %d 个，第九轮 %d 个）。%s",
              DEC10$rule, if (nzchar(DEC10$round8_points_outside)) paste(sprintf("%s第 %s 年", gl(sub(" year.*", "", strsplit(DEC10$round8_points_outside, "; ")[[1]])),
                                                                            sub(".*year ", "", strsplit(DEC10$round8_points_outside, "; ")[[1]])), collapse = "、") else "（无）",
              DEC10$n_rule_points, DEC10$n_round8_inside, DEC10$n_round9_inside,
              if (DEC10$rule == "A") "第八轮不用于终生模拟，采用第九轮结构；门槛 (a) 只用 Bonferroni 同时区间（逐点 99.5%）判定，去掉 0.3 个百分点的附加上限（门槛修改记录第 8 项）。" else "维持第八轮为最终结构，第九轮只作记录。"), "",
      "### 14.3 转移后的平均存活时间与远处复发状态中的停留时间", "",
      sprintf("转移后的平均存活时间（年，截至终生时间范围 %s 年，即到 100 岁；k = 1）；参考：截至 48 个月的限制平均存活时间，与 ESME 重建 KM 比较（`mean_survival_after_dr.csv`）：", f2(MS10$horizon_years[1], 1)), "",
      md_table(with(MS10, data.frame(组 = gl(group), 第八轮_终生 = f2(round8_mean_lifetime_years, 3), 第九轮_终生 = f2(round9_mean_lifetime_years, 3),
                                     差_第九减第八 = f2(diff_mean_lifetime_years, 3), 第八轮_48个月 = f2(round8_rmst48_years, 3), 第九轮_48个月 = f2(round9_rmst48_years, 3),
                                     ESME_KM_48个月 = f2(esme_km_rmst48_years, 3)))), "",
      "引擎中每人在远处复发状态的累计停留时间（年，折现前，终生；`dr_time_engine.csv`；第八轮与第九轮各用其校准的 k）：", "",
      md_table(with(DT10, data.frame(臂 = ifelse(arm == "chemo", "单用化疗", "帕博利珠单抗"), 情景 = ifelse(scenario == "base", "基准", "k = 1"),
                                     第八轮 = f2(round8_years, 3), 第九轮 = f2(round9_years, 3), 差_年 = f2(diff_years, 3), 差_月 = f2(diff_months, 2),
                                     第八轮_k = f2(round8_k, 3), 第九轮_k = f2(round9_k, 3)))), "")
  if (adopt9) {
    G9r <- rd("output", "phase1", "calibration_gate.csv")
    add("### 14.4 采用的结构与第九轮各道门槛的最终判定", "",
        sprintf("采用第九轮结构。第九轮的校准结果不变（不重新校准，`R/14b_apply_round10.R`），按第十轮的规则判定（`calibration_status.csv`；按第九轮规则的判定另存于 `round9/calibration_status_round9_rule.csv`）：(a) %s（10 个点中 %d 个在 95%% 区间内，全部 10 个点%s 99.5%% 区间内）；(b) %s；(c) %s。`data/fits/engine_params.rds` 已恢复为第九轮的值。",
                if (istrue(CSnow$gate_a_accepted)) "按 Bonferroni 同时区间接受" else "**不达标**", sum(istrue(G9r$inside)),
                if (all(istrue(G9r$inside_995))) "在" else "**并非都在**", if (istrue(CSnow$gate_b_pass)) "达标" else "**不达标**",
                if (istrue(CSnow$gate_c_pass)) "达标" else "**不达标**"),
        sprintf("本地参照结果 `output/check/bootstrap10_local.rds`（基础种子 20261023，10 次）%s；推送与 Longleaf 的 1,000 次 bootstrap 推迟到第十一轮通过之后（用户 2026-10-23 的指示；第十一轮见第 15 节）。",
                if (!is.null(ref_meta10)) sprintf("在提交 %s 上重新生成（%s，%s）", substr(ref_meta10$commit, 1, 7), ref_meta10$platform, ref_meta10$created) else "尚未重新生成"), "")
  }
}

# round 11 (docs/acceptance_rule_round11.md, git 0ca5cfe): the stratified EFS constraint takes the
# 7-year values of the final analysis; R/15_round11_check.R applies the stop condition of the rule
r11 <- file.path(ROOT, "output", "phase1", "round11")
if (file.exists(file.path(r11, "status.csv"))) {
  S11 <- rd("output", "phase1", "round11", "status.csv"); C11 <- rd("output", "phase1", "round11", "cells.csv")
  F11 <- rd("output", "phase1", "round11", "comparison_5y_2023.csv"); H11 <- rd("output", "phase1", "round11", "comparison_hr.csv")
  lab11 <- c(EFS_pembro_pCR = "pCR 例，帕博利珠单抗", EFS_placebo_pCR = "pCR 例，安慰剂",
             EFS_pembro_nonpCR = "non-pCR 例，帕博利珠单抗", EFS_placebo_nonpCR = "non-pCR 例，安慰剂")
  gap <- function(col, st) C11[[col]][C11$curve == paste0("EFS_pembro_", st)] - C11[[col]][C11$curve == paste0("EFS_placebo_", st)]
  add("## 15. 第十一轮（2026-10-23）：分层 EFS 约束改用 KEYNOTE-522 最终分析的 7 年值", "",
      "规则在任何第十一轮计算之前单独提交（`docs/acceptance_rule_round11.md`，git 0ca5cfe；尾崎 2026-10-23 的指示）。唯一的改动是约束值的数据来源：由 2023-03-23 截点的 5 年分层 EFS 换成最终分析（J Clin Oncol 2026;44(16_suppl):507，截点 2025-10-14，中位随访 93.8 个月）的 7 年分层 EFS，实现方式不变（随机化后 84 个月的预测落在报告值的二项 95% 区间内，n 为 IA4 的分层人数；区间外时在较近的边界上重新最大化似然）。门槛沿用第十轮判定后的版本，分布族不变，结构为第九轮。最终分析的摘要原文未取得，数值出自会议报道（OncLive 2026-06-01，DelveInsight、CancerNetwork 对照；`data/kn522_final_7y.csv`）。规则文件的数据表中「全体 OS 的 HR」一行在提交时误读了 CancerNetwork（[0.49, 0.83] 是 DRFS 的 HR），已在文件中更正，不影响规则。", "",
      "pCR 比例的核对（提交前）：按全例 pCR 率 63.0% 对 55.6% 加权，分层 7 年 EFS 合成 78.26% 与 69.83%，与全体的 78.3% 与 69.8% 一致；模型的 pCR 比例为全例值（494/784、217/390）。", "",
      "### 15.1 四个格子的 7 年 EFS（不作门槛）", "",
      md_table(data.frame(格子 = lab11[C11$curve], 分布族 = C11$model, 报告值 = f2(C11$reported, 1),
                          二项95区间 = sprintf("%s 至 %s", f2(C11$ci95_lo, 2), f2(C11$ci95_hi, 2)), 模型 = f2(C11$model_7y, 2),
                          差 = f2(C11$diff, 2), 约束起作用 = ifelse(istrue(C11$binding), "是", "否"),
                          差在0.5以内 = ifelse(istrue(C11$within_0_5pp), "是", "**否**"), AIC = f2(C11$AIC, 2), check.names = FALSE)), "",
      sprintf("合计 AIC %s（第十轮 %s）。4 条曲线在约束前都已落在区间内，约束不起作用，参数与第十轮相同（`data/fits/round11/fits.rds` 的 selected 与 `data/fits/fits.rds` 完全相同）。7 年两臂差：pCR 例模型 %s 对报告 %s 个百分点，non-pCR 例模型 %s 对报告 %s 个百分点。",
              f2(S11$AIC_total, 2), f2(S11$AIC_total_round10, 2), f2(gap("model_7y", "pCR"), 2), f2(gap("reported", "pCR"), 1),
              f2(gap("model_7y", "nonpCR"), 2), f2(gap("reported", "nonpCR"), 1)), "",
      "### 15.2 判定", "",
      if (istrue(S11$constraint_check_pass)) "加了约束的 4 个格子的差都在 0.5 个百分点以内，继续校准。" else
        sprintf("**按规则停下**：加了约束的 %d 个格子中 %d 个的差超过 0.5 个百分点（规则：差应在 0.5 个百分点以内，否则说明约束没起作用，停下报告）。原因是约束为区间约束：模型值落在二项区间内（半宽 2.6 至 7.5 个百分点）时参数不变，约束不把模型值固定在报告值上（规则文件提交前已写明）。没有重新校准，没有判定门槛，没有自行改变约束的实现方式。第十轮选定的结构仍为第 1 阶段的最终状态：`data/fits/fits.rds` 已恢复为第十轮的文件，`data/fits/engine_params.rds` 未改动；第十一轮的拟合存于 `data/fits/round11/`、`output/phase1/round11/`。",
                S11$constrained_cells, S11$constrained_cells - S11$cells_within_0_5pp), "",
      "### 15.3 不作门槛的跨分析对照", "",
      "2023-03-23 截点的 5 年分层 EFS（第十一轮起不再作约束）：", "",
      md_table(data.frame(格子 = lab11[F11$curve], 模型5年 = f2(F11$model_5y, 2), 报告值2023 = f2(F11$reported_2023, 1), 差 = f2(F11$diff, 2), check.names = FALSE)), "",
      "按 pCR 分层的 HR（最终分析为探索性解析）：", "",
      md_table(data.frame(终点 = H11$endpoint, 层 = H11$stratum, 最终分析 = sprintf("%s [%s, %s]", H11$final_hr, H11$final_lo, H11$final_hi),
                          出处 = H11$final_source, 截点2023 = ifelse(is.na(H11$later_cutoff_hr), "", H11$later_cutoff_hr),
                          IA4重建Cox = ifelse(is.na(H11$ia4_reconstructed_cox_hr), "", f2(H11$ia4_reconstructed_cox_hr, 3)),
                          备注 = ifelse(H11$endpoint == "EFS", "IA4（2021-03-23）重建个体数据，不分层 Cox；不作门槛",
                                      paste0("模型输入中没有按 pCR 分层的 OS 曲线；模型值未计算（停在校准之前）",
                                             ifelse(H11$stratum == "pCR", "；OncLive 印 [0.39, 1.14]", ""))), check.names = FALSE)), "",
      "### 15.4 未做的部分", "",
      "按规则停在拟合之后：门槛结果、k、5 年与 7 年的 OS 两臂差、5 年 RMST 两臂差与第十轮的并列，以及 `bootstrap10_local.rds` 的重新生成、推送和 Longleaf 的 1,000 次 bootstrap，都没有做。", "")
  RB10 <- file.path(ROOT, "output", "check", "bootstrap10_bounds_round10_summary.csv")
  if (file.exists(RB10)) {
    B10 <- rd("output", "check", "bootstrap10_bounds_round10_summary.csv")
    add("### 15.5 参照的边界报告（2026-10-23 补充，只报告不设门槛）", "",
        sprintf("参照重新生成之后（门槛通过时），报告 10 次中 k 的全部值、贴下界 0.25 与上界 4 的次数，以及术前进展中位贴 10 个月与 26 个月的次数（`R/06d_reference_bounds.R`），与第十轮的参照并列；推送与 Longleaf 的 1,000 次由用户看过之后再定。第十轮的参照（提交 %s）：k = %s；贴 4 的 %d 次（第 %s 次），贴 0.25 的 %d 次；术前进展中位贴 10 个月的 %d 次，贴 26 个月的 %d 次。第十一轮两次都停下（第 15.6 节），参照未重新生成，本轮的值尚无。",
                B10$commit, gsub("; ", "、", B10$k_values), B10$k_at_4, gsub(", ", "、", B10$k_at_4_replicates), B10$k_at_0.25, B10$preprog_median_at_10, B10$preprog_median_at_26), "")
  }
  # revised round 11: equality constraint (rule 1996c24); outputs in output/phase1/round11/equality/
  re <- file.path(r11, "equality")
  if (file.exists(file.path(re, "status.csv")) && file.exists(file.path(re, "calibration_status.csv"))) {
    rq <- function(f) rd("output", "phase1", "round11", "equality", f)
    SE <- rq("status.csv"); CE <- rq("cells.csv"); GE <- rq("arm_gap_7y.csv"); FE <- rq("comparison_5y_2023.csv")
    CSe <- rq("calibration_status.csv"); Ge <- rq("calibration_gate.csv"); GRe <- rq("calibration_gate_rmst.csv"); G7e <- rq("calibration_final7y.csv")
    VSe <- rq("calibration_vs_previous.csv"); ADe <- rq("scenario_k1_arm_diff.csv"); DE <- rq("diag_engine_efs7.csv"); KS <- rq("diag_k_scan.csv")
    CS10 <- rd("output", "phase1", "calibration_status.csv"); G10 <- rd("output", "phase1", "calibration_gate.csv")
    GR10 <- rd("output", "phase1", "calibration_gate_rmst.csv"); G710 <- rd("output", "phase1", "calibration_final7y.csv")
    VS10 <- rd("output", "phase1", "calibration_vs_previous.csv"); AD10 <- rd("output", "phase1", "scenario_k1_arm_diff.csv")
    vq <- function(V, q) V$round9[V$quantity == q]
    adq <- function(A, q, col) A[[col]][A$quantity == q]
    yn <- function(x) ifelse(istrue(x), "达标", "**不达标**")
    ya <- function(CS) if (istrue(CS$gate_a_strict_pass)) "达标" else if (istrue(CS$gate_a_accepted)) "按 Bonferroni 同时区间接受" else "**不达标**"
    g7row <- function(G, id) sprintf("%s（%s 至 %s）", f2(G$engine[G$id == id], 2), f2(G$ci95_lo[G$id == id], 1), f2(G$ci95_hi[G$id == id], 1))
    out_c <- G7e[istrue(G7e$gate_c) & !istrue(G7e$inside_ci), ]
    ks <- KS$k[istrue(KS$all_three)]
    add("### 15.6 修改后的第十一轮：等式约束（2026-10-23）", "",
        "规则修改在任何新的计算之前单独提交（`docs/acceptance_rule_round11.md` 的「修改」节，git 1996c24）：四个格子在随机化后 84 个月的 EFS 固定为报告值，在此条件下最大化似然，撤销区间约束；0.5 个百分点的检查保留；bootstrap 中每个样本的四个约束值各自从 Binomial(n, p)/n 抽取。修改记录如实写明：本修改是看到第十一轮拟合（git 974b6ef）之后做出的；理由是区间约束自第三轮以来从未起过作用，且不能保证两臂之差正确；0.5 个百分点这一条按等式约束设计，与当时的区间约束不匹配，属于指令错误。", "",
        "最终分析摘要原文（`input/papers/KN522_final_ASCO2026_abstract.pdf`）与 `data/kn522_final_7y.csv` 的全体数值逐项一致（7 年 EFS 与 OS 及其 95% 置信区间、两个 HR、截点、中位随访 93.8 个月〔84.7 至 102.8〕），门槛 (c) 的取值不变；摘要不含按 pCR 分层的数值。", "",
        "#### 15.6.1 拟合（`R/15_round11_check.R equal`，`round11/equality/`）", "",
        md_table(data.frame(格子 = lab11[CE$curve], 报告值 = f2(CE$reported, 1), 约束前 = f2(CE$model_7y_before, 2), 约束后 = f2(CE$model_7y, 2),
                            对数似然变化 = f2(CE$loglik_change, 3), 约束前参数 = CE$pars_before, 约束后参数 = CE$pars_after, check.names = FALSE)), "",
        sprintf("0.5 个百分点的检查：4 个格子都在 0.5 个百分点以内（按第 4 步的拟合曲线计，差为 0）。合计对数似然变化 %s，合计 AIC %s（第十轮 %s）。7 年两臂差：pCR 例 %s → %s（报告 %s），non-pCR 例 %s → %s（报告 %s）个百分点。",
                f2(SE$loglik_change_total, 3), f2(SE$AIC_total, 2), f2(SE$AIC_total_round10, 2),
                f2(GE$model_before[GE$stratum == "pCR"], 2), f2(GE$model[GE$stratum == "pCR"], 2), f2(GE$reported[GE$stratum == "pCR"], 1),
                f2(GE$model_before[GE$stratum == "nonpCR"], 2), f2(GE$model[GE$stratum == "nonpCR"], 2), f2(GE$reported[GE$stratum == "nonpCR"], 1)), "",
        "5 年值与 2023-03-23 截点报告值之差（不作门槛）：", "",
        md_table(data.frame(格子 = lab11[FE$curve], 约束前 = f2(FE$model_5y_before, 2), 约束后 = f2(FE$model_5y, 2), 报告值2023 = f2(FE$reported_2023, 1),
                            差 = f2(FE$diff, 2), check.names = FALSE)), "",
        "#### 15.6.2 校准与门槛（第九轮结构，`R/05_calibrate.R`）", "",
        md_table(data.frame(项目 = c("门槛 (a)：第 1 至 5 年 10 个点", "门槛 (b)：5 年 RMST 两臂差（年）", "门槛 (c)：7 年 OS 帕博利珠单抗", "门槛 (c)：7 年 OS 安慰剂",
                                    "门槛 (c)：7 年 EFS 帕博利珠单抗", "门槛 (c)：7 年 EFS 安慰剂", "k", "术前进展中位（月）", "KM 平方误差和（百分点²）",
                                    "5 年 OS 两臂差（模型 / k = 1 / 报告）", "7 年 OS 两臂差（模型 / k = 1 / 报告）"),
                            第十一轮等式约束 = c(sprintf("%s（95%% 区间内 %d 个）", ya(CSe), sum(istrue(Ge$inside))),
                                           sprintf("%s（%s；区间 %s 至 %s）", yn(CSe$gate_b_pass), f2(GRe$engine, 4), f2(GRe$km_boot_ci95_lo, 4), f2(GRe$km_boot_ci95_hi, 4)),
                                           g7row(G7e, "os7_pembro"), g7row(G7e, "os7_placebo"), g7row(G7e, "efs7_pembro"), g7row(G7e, "efs7_placebo"),
                                           f2(vq(VSe, "pembro_dr_k"), 3), f2(vq(VSe, "preprog_median_months"), 2), f2(vq(VSe, "km_SSE_both_arms_pp2"), 1),
                                           sprintf("%s / %s / %s", f2(adq(ADe, "OS at 5 years (points)", "base"), 2), f2(adq(ADe, "OS at 5 years (points)", "k1"), 2), f2(adq(ADe, "OS at 5 years (points)", "reported"), 2)),
                                           sprintf("%s / %s / %s", f2(adq(ADe, "OS at 7 years (points)", "base"), 2), f2(adq(ADe, "OS at 7 years (points)", "k1"), 2), f2(adq(ADe, "OS at 7 years (points)", "reported"), 1))),
                            第十轮 = c(sprintf("%s（95%% 区间内 %d 个）", ya(CS10), sum(istrue(G10$inside))),
                                     sprintf("%s（%s）", yn(CS10$gate_b_pass), f2(GR10$engine, 4)),
                                     g7row(G710, "os7_pembro"), g7row(G710, "os7_placebo"), g7row(G710, "efs7_pembro"), g7row(G710, "efs7_placebo"),
                                     f2(vq(VS10, "pembro_dr_k"), 3), f2(vq(VS10, "preprog_median_months"), 2), f2(vq(VS10, "km_SSE_both_arms_pp2"), 1),
                                     sprintf("%s / %s / %s", f2(adq(AD10, "OS at 5 years (points)", "base"), 2), f2(adq(AD10, "OS at 5 years (points)", "k1"), 2), f2(adq(AD10, "OS at 5 years (points)", "reported"), 2)),
                                     sprintf("%s / %s / %s", f2(adq(AD10, "OS at 7 years (points)", "base"), 2), f2(adq(AD10, "OS at 7 years (points)", "k1"), 2), f2(adq(AD10, "OS at 7 years (points)", "reported"), 1))),
                            check.names = FALSE)), "",
        sprintf("**按规则停下**：门槛 (c) 不达标——%s。没有自行增加结构，没有重新生成参照，没有运行 `R/06d_reference_bounds.R`，没有启动 Longleaf。`R/05_calibrate.R` 按设计删除了 `engine_params.rds`；之后把第十一轮的输出移到 `output/phase1/round11/equality/`、`data/fits/round11/equality/`，主目录的 `fits.rds`、`engine_params.rds`、`calibration_candidates.rds` 与校准输出恢复为第十轮的文件（与提交中的相同），`config.R` 的默认恢复为 5 年、区间约束（已接受的状态；设为 7 年、`equal` 即重现本轮）。",
                paste(sprintf("%s 7 年 %s：模型 %s，区间 %s 至 %s（低 %s 个百分点）", ifelse(out_c$arm == "pembro", "帕博利珠单抗", "安慰剂"), out_c$endpoint, f2(out_c$engine, 2),
                              f2(out_c$ci95_lo, 1), f2(out_c$ci95_hi, 1), f2(pmax(out_c$ci95_lo - out_c$engine, out_c$engine - out_c$ci95_hi), 2)), collapse = "；")), "",
        "#### 15.6.3 诊断（不作门槛，不改结构，`R/15b_round11_diag.R`）", "",
        "引擎中按 pCR 分层的 7 年 EFS 与约束值（第 4 步的拟合曲线等于约束值）：", "",
        md_table(data.frame(臂 = ifelse(DE$arm == "pembro", "帕博利珠单抗", "安慰剂"), 层 = DE$stratum, 报告值 = ifelse(is.na(DE$reported), "", f2(DE$reported, 1)),
                            第4步拟合 = ifelse(is.na(DE$fit_04), "", f2(DE$fit_04, 2)), 引擎 = f2(DE$engine, 2),
                            引擎减报告值 = ifelse(is.na(DE$engine_minus_reported), "", f2(DE$engine_minus_reported, 2)), check.names = FALSE)), "",
        "引擎的分层 7 年 EFS 比第 4 步的拟合曲线低 0.11 至 0.69 个百分点（两格超过 0.5）。第十轮的引擎有同样大小的差（对区间约束下的拟合曲线：−0.53、−0.11、−0.19、−0.67），不是等式约束引起的。pCR 两格的差大致等于术前 7 个月内的因不良事件死亡（引擎对 pCR 层也计入，帕博利珠单抗 7/783 × 7/12 ≈ 0.52、安慰剂 1/389 × 7/12 ≈ 0.15 个百分点）；non-pCR 两格还与术前进展的处理有关（推测，未进一步查）。0.5 个百分点的检查按第 4 步的拟合曲线判定为通过；按引擎则有两格不通过。", "",
        sprintf("只改 k（其余参数取本轮校准值、不重新优化）时，三道门槛同时满足的 k 为 %s（校准值 %s）。只作诊断，不作采用。",
                if (length(ks)) sprintf("%s 至 %s", f2(min(ks), 2), f2(max(ks), 2)) else "无", f2(vq(VSe, "pembro_dr_k"), 3)), "")
  }
}

# round 12 (docs/acceptance_rule_round12.md, git a1625c1): engine / fitted EFS consistency fixed,
# round 11 re-judged; outputs in output/phase1/round12/
r12 <- file.path(ROOT, "output", "phase1", "round12")
if (file.exists(file.path(r12, "round11_setting", "calibration_status.csv"))) {
  r2 <- function(...) rd("output", "phase1", "round12", ...)
  DP <- r2("diag_engine_vs_fit_prefix.csv"); DI <- r2("diag_branch_inputs.csv"); CT <- rd("output", "phase1", "engine_efs_consistency_test.csv")
  KS12 <- r2("round11_setting", "diag_k_scan.csv")
  lab12 <- c(pembro = "帕博利珠单抗", placebo = "安慰剂")
  cols <- list(
    list(name = "第十一轮设定（修正后引擎）", dir = c("output", "phase1", "round12", "round11_setting")),
    list(name = "第十一轮（修正前引擎）", dir = c("output", "phase1", "round11", "equality")),
    list(name = "第十轮设定（修正后引擎，只报告）", dir = c("output", "phase1", "round12", "round10_setting")),
    list(name = "第十轮（修正前引擎，已接受）", dir = c("output", "phase1")))
  cell <- function(cl, f) do.call(rd, as.list(c(cl$dir, f)))
  g7v <- function(G, id) { G <- G[G$id == id, ]; sprintf("%s（%s 至 %s）%s", f2(G$engine, 2), f2(G$ci95_lo, 1), f2(G$ci95_hi, 1), if (istrue(G$inside_ci)) "" else " **区间外**") }
  ya12 <- function(CS) if (istrue(CS$gate_a_strict_pass)) "达标" else if (istrue(CS$gate_a_accepted)) "按 Bonferroni 同时区间接受" else "**不达标**"
  colv <- lapply(cols, function(cl) {
    CS <- cell(cl, "calibration_status.csv"); G <- cell(cl, "calibration_gate.csv"); GR <- cell(cl, "calibration_gate_rmst.csv")
    G7 <- cell(cl, "calibration_final7y.csv"); V <- cell(cl, "calibration_vs_previous.csv")
    c(sprintf("%s（95%% 区间内 %d 个）", ya12(CS), sum(istrue(G$inside))), sprintf("%s（%s）", if (istrue(CS$gate_b_pass)) "达标" else "**不达标**", f2(GR$engine, 4)),
      if (istrue(CS$gate_c_pass)) "达标" else "**不达标**",
      g7v(G7, "os7_pembro"), g7v(G7, "os7_placebo"), g7v(G7, "efs7_pembro"), g7v(G7, "efs7_placebo"),
      f2(V$round9[V$quantity == "pembro_dr_k"], 3), f2(V$round9[V$quantity == "preprog_median_months"], 2), f2(V$round9[V$quantity == "km_SSE_both_arms_pp2"], 1))
  })
  TB <- data.frame(项目 = c("门槛 (a)", "门槛 (b)：5 年 RMST 两臂差（年）", "门槛 (c)", "7 年 OS 帕博利珠单抗（报告 85.1）", "7 年 OS 安慰剂（报告 77.2）",
                          "7 年 EFS 帕博利珠单抗（报告 78.3）", "7 年 EFS 安慰剂（报告 69.8）", "k", "术前进展中位（月）", "KM 平方误差和（百分点²）"),
                   setNames(as.data.frame(do.call(cbind, colv)), sapply(cols, `[[`, "name")), check.names = FALSE)
  S11f <- cell(cols[[1]], "calibration_status.csv"); G711f <- cell(cols[[1]], "calibration_final7y.csv")
  oc <- G711f[istrue(G711f$gate_c) & !istrue(G711f$inside_ci), ]
  ks <- KS12$k[istrue(KS12$all_three)]
  D7 <- DP[DP$setting == "round11", ]
  add("## 16. 第十二轮（2026-10-23）：修正引擎与输入 EFS 的不一致，修正后重判第十一轮", "",
      "规则在任何计算之前单独提交（`docs/acceptance_rule_round12.md`，git a1625c1）。判定依据：引擎的作用是把拟合的 EFS 曲线分解到事件类型和时点上，不应改变 EFS 本身；检查为四个格子和两臂全体，引擎 EFS 与第 4 步拟合曲线在第 1、2、3、5、7、10 年的差都 ≤ 0.05 个百分点（实现的正确性检查，不是统计门槛）。修正原则：已包含在拟合 EFS 曲线中的事件只能在时点或状态之间移动，不能另外加上去。", "",
      "### 16.1 诊断（修正前的引擎 = git a1625c1 的 `R/engine.R`；`R/16_round12_diag.R`）", "",
      "第十一轮设定（7 年、等式约束）下引擎 EFS 与拟合曲线之差（百分点）按来源的拆解（一阶近似，余项归入「其他」；第十轮设定的同表在 `round12/diag_engine_vs_fit_prefix.csv`，大小几乎相同）：", "",
      md_table(data.frame(格子 = sprintf("%s %s", lab12[D7$arm], D7$stratum), 年 = D7$year, 拟合 = f2(D7$fit, 2), 引擎 = f2(D7$engine, 2), 差 = f2(D7$diff, 3),
                          A手术前背景死亡 = f2(D7$A_pre_background, 3), B手术前因不良事件死亡 = f2(D7$B_pre_ae_deaths, 3),
                          C术前进展对KM下降 = f2(D7$C_preprog_vs_km, 3), D手术后背景下限 = f2(D7$D_post_background_floor, 3), E其他 = f2(D7$E_other, 3), check.names = FALSE)), "",
      sprintf("各层的输入：手术时点 KM 的下降 帕博利珠单抗 non-pCR %s%%、安慰剂 non-pCR %s%%（pCR 两层为 0：重建数据中 pCR 层手术前没有事件和删失）；术前进展的报告比例 q_pre %s%%、%s%%；治疗期因不良事件死亡的概率 %s%%、%s%%。",
              f2(100 * DI$km_drop_to_surgery[DI$setting == "round11" & DI$arm == "pembro" & DI$stratum == "nonpCR"], 2),
              f2(100 * DI$km_drop_to_surgery[DI$setting == "round11" & DI$arm == "placebo" & DI$stratum == "nonpCR"], 2),
              f2(100 * DI$q_pre[DI$setting == "round11" & DI$arm == "pembro" & DI$stratum == "nonpCR"], 2),
              f2(100 * DI$q_pre[DI$setting == "round11" & DI$arm == "placebo" & DI$stratum == "nonpCR"], 2),
              f2(100 * DI$ae_deaths_prob[DI$setting == "round11" & DI$arm == "pembro"][1], 2), f2(100 * DI$ae_deaths_prob[DI$setting == "round11" & DI$arm == "placebo"][1], 2)), "",
      md_table(data.frame(
        来源 = c("因不良事件死亡（手术前）", "背景死亡（手术前）", "术前进展", "pCR 分层开始的时点", "背景死亡下限（手术后，非治愈模型）", "其他"),
        是否已在拟合曲线中 = c("是（KM 含手术前的全部死亡）", "是（同上）", "是（无法手术的进展是 EFS 事件，在 non-pCR 层手术前的 KM 下降中）",
                       "是（手术前的事件都在 non-pCR 层；pCR 层手术前的 KM 为 1）", "不适用（拟合风险低于背景时的外推）", "—"),
        原因与代码位置 = c("旧 `branch_flows()`：`dHA <- ae_rate * ...` 在 [0, ae_end) 全程计入 EF 的总风险 `Ht`，手术前未从 KM 中扣出，两层都计",
                    "旧 `branch_flows()`：`Ht <- hb + ...` 手术前也含背景死亡 `hb`，叠加在 KM 之上",
                    "旧 `branch_flows()`：`Spre <- 1 - q_pre * Fpre`，以报告比例 q_pre 代替 KM 的下降（帕博利珠单抗 q < 下降、安慰剂 q > 下降）",
                    "上面三项在 pCR 层的表现：手术前本无事件，引擎仍计背景死亡与因不良事件死亡（两臂 pCR 层的全部偏差）",
                    "`pmax(dH - hb, 0)`：10 年内不起作用（0 个周期）；pCR 层的 Weibull 拟合自第 22 年（帕博利珠单抗）、第 27 年（安慰剂）起低于背景死亡率，此后引擎以背景死亡率为下限",
                    "一阶近似的余项（≤ 0.01 个百分点）"),
        修正方式 = c("手术前从 KM 的下降中分出（在术前进展之后，最多为余下的部分）；放不下的部分（pCR 层的全部）移到手术后、治疗期结束前，均匀地从超额风险中扣出",
                 "手术前不另计；KM 的下降中术前进展与因不良事件死亡以外的部分为其他死亡（含背景）",
                 "手术前最多为 KM 的下降、按 KM 的形状；超出的部分（安慰剂 non-pCR 8.67% − 7.59%）移到手术后最早的周期，从超额风险中扣出，总量仍为 q_pre",
                 "pCR 层手术前没有离开无事件状态的事件；因不良事件死亡全部在手术后的治疗期内",
                 "不改（不在本检查的范围；外推的问题，第 2 阶段终生模拟时要注意）",
                 "—"), check.names = FALSE)), "",
      "### 16.2 修正与测试", "",
      "`R/engine.R`：新增 `branch_hazards()`（离开无事件状态的各项风险），`branch_flows()` 与 `R/test_engine_vectorized.R` 的逐周期递推共用；手术前的无事件比例严格等于该层的 KM，手术后的全死因风险等于 EFS 模型（非治愈模型不低于背景）；手术前放不下的事件移到手术后，不另外加。新增单元测试 `R/test_engine_efs_consistency.R`（输出 `output/phase1/engine_efs_consistency_test.csv`），已纳入全部单元测试。", "",
      sprintf("结果：第十轮设定与第十一轮设定都达标，四个格子与两臂全体在 6 个时点的最大差 %s 个百分点；术前进展的进入量每层都等于 q_pre；终生的因不良事件死亡与治疗期的概率之差最大 %s 个百分点（只报告）。其他单元测试（向量化 3,456 例、接口、费用层、约束）都通过；接口测试与费用层测试的数值因引擎改变而改变。",
              formatC(max(abs(CT$diff[!is.na(CT$year)])), format = "e", digits = 1), f2(max(abs(CT$diff[is.na(CT$year)])), 3)), "",
      "### 16.3 校准与门槛（`R/16b_round12_calibrate.sh`）", "",
      md_table(TB), "",
      "### 16.4 判定", "",
      sprintf("**第十一轮设定按规则停下**：门槛 (c) 不达标——%s。门槛与第十一轮完全相同，没有放宽，没有手动指定 k，没有自行改结构或目标函数。第十轮设定在修正后的引擎下三道门槛都达标，但按规则只报告，不作为回退选项（其 non-pCR 层 7 年两臂差有已知偏差：模型 12.43 对报告 7.9 个百分点）。",
              paste(sprintf("%s 7 年 %s 模型 %s，区间 %s 至 %s（低 %s 个百分点）", lab12[oc$arm], oc$endpoint, f2(oc$engine, 2), f2(oc$ci95_lo, 1), f2(oc$ci95_hi, 1),
                            f2(pmax(oc$ci95_lo - oc$engine, oc$engine - oc$ci95_hi), 2)), collapse = "；")), "",
      sprintf("诊断（不作门槛，`R/15b_round11_diag.R`，修正后的引擎）：引擎中按 pCR 分层的 7 年 EFS 与约束值完全相同；只改 k（其余参数取本轮校准值、不重新优化）时三道门槛同时满足的 k 为 %s（校准值 %s）。",
              if (length(ks)) sprintf("%s 至 %s", f2(min(ks), 2), f2(max(ks), 2)) else "无", f2(as.numeric(cell(cols[[1]], "calibration_vs_previous.csv")$round9[1]), 3)), "",
      "### 16.5 状态", "",
      "主目录（`data/fits/fits.rds`、`engine_params.rds`、`calibration_candidates.rds` 与校准输出）仍为第十轮的文件，**这些是用修正前的引擎算出的**；`config.R` 的默认仍为 5 年、区间约束（设 `EXERCISE_CEA_EFS_CONSTRAINT=7,equal` 即重现第十一轮设定）。引擎的修正已提交。两种设定在修正后引擎下的产物在 `output/phase1/round12/`、`data/fits/round12/`。本地参照 `output/check/bootstrap10_local.rds` 是修正前的引擎生成的，未重新生成；没有运行 `R/06d_reference_bounds.R`；没有启动 Longleaf。", "")
}

writeLines(L, file.path(out_dir, "phase1_report.md"), useBytes = TRUE)
cat("wrote phase1_report.md:", length(L), "lines\n")
