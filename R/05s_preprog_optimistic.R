# 05s_preprog_optimistic.R
# Scenario (docs/model_spec.md section 6, 2026-10-23): optimistic death after progression
# precluding surgery. The PreProg log-logistic is fixed at median 26 months and all-cause survival
# 20% 5 years after entry (the shape follows from the two; Elmore et al., Ann Surg Oncol 2021,
# PMID 34247335, MD Anderson cohort); k is recalibrated with the objective of 05_calibrate.R (KM
# OS months 1-78 plus the 7-year points); the DR parameters are external as in the base (round 9:
# ESME fit; in round 8 the DR shape was recalibrated here, git 694b0f3). The three
# gates are computed for reference only (no decision is taken on them). The between-arm OS
# difference at 5 and 7 years is set next to the base, the scenario k = 1 and the reference values.
# Run after 05_calibrate.R (reads engine_params.rds and its gate outputs).
# Outputs: output/phase1/scenario_preprog_optimistic.csv (parameters), ..._gate.csv (gates (a),
#          (b), (c), for reference), ..._arm_diff.csv

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
source(file.path(ROOT, "R", "calibration.R"))
suppressPackageStartupMessages(library(survival))
out_dir <- file.path(ROOT, "output", "phase1")
ipd <- readRDS(file.path(ROOT, "data", "ipd", "ipd_all.rds"))
km_at <- function(d, tm) summary(survfit(Surv(time, status) ~ 1, data = d), times = tm, extend = TRUE)$surv
arm_of <- c(pembro = "pembro", placebo = "chemo")
os_ipd <- lapply(names(arm_of), function(a) ipd[[paste0("K24_F1A_OS_", a)]]); names(os_ipd) <- names(arm_of)
g_m <- CFG$calib_grid_months
target <- lapply(os_ipd, function(d) 100 * km_at(d, g_m))
X7 <- final7y_targets()
P1 <- readRDS(file.path(ROOT, "data", "fits", "engine_params.rds"))          # base (round 8)
th1 <- readRDS(file.path(ROOT, "data", "fits", "calibration_candidates.rds"))$optim$par

# PreProg fixed: median 26 months, all-cause survival 20% at 5 years after entry (from age 49.5)
PP_OPT_MEDIAN <- 26 / 12; PP_OPT_S5 <- 0.20
shape_opt <- log(1 / (PP_OPT_S5 / S_pop(PP_ENTRY_AGE, 5)) - 1) / log(5 / PP_OPT_MEDIAN)
u_opt <- shape_opt / pp_shape_cap(PP_OPT_MEDIAN)
stopifnot(u_opt > 0, u_opt <= 1)
set.seed(CFG$seed)
cal <- calibrate_os(P1, target, g_m, DR_EXT_BASE, extra = X7, fixed = c(PP_OPT_MEDIAN, u_opt, NA),
                    starts = c(list(th1), CAL_STARTS))
PS <- cal_apply(P1, cal$par, DR_EXT_BASE)
s5 <- exp(-dr_cumhaz(PS$preprog, 5)) * S_pop(PP_ENTRY_AGE, 5)
stopifnot(abs(s5 - PP_OPT_S5) < 1e-10, abs(PS$preprog$scale - PP_OPT_MEDIAN) < 1e-12)
PAR <- data.frame(quantity = c("preprog_median_months", "preprog_shape", "preprog_allcause_surv_5y", "dr_shape", "dr_median_early_months",
                               "dr_median_late_months", "pembro_dr_k", "objective", "convergence", "k_at_bound"),
                  scenario = c(12 * PS$preprog$scale, PS$preprog$shape, s5, PS$dr$shape, 12 * PS$dr$scale, 12 * PS$dr$late_scale,
                               PS$pembro_dr_k, cal$value, cal$convergence, cal$at_bound[["k_low"]] || cal$at_bound[["k_high"]]),
                  base = c(12 * P1$preprog$scale, P1$preprog$shape, exp(-dr_cumhaz(P1$preprog, 5)) * S_pop(PP_ENTRY_AGE, 5), P1$dr$shape,
                           12 * P1$dr$scale, 12 * P1$dr$late_scale, P1$pembro_dr_k, NA, NA, NA))
write.csv(PAR, file.path(out_dir, "scenario_preprog_optimistic.csv"), row.names = FALSE)
print(PAR, row.names = FALSE)

# gates, for reference: the KM intervals of 05_calibrate.R (calibration_gate.csv,
# calibration_gate_rmst.csv) and the final-analysis CIs
eng <- function(arm, pcr, t, ep, P = PS, cd = FALSE) 100 * survival_engine(arm_of[[arm]], pcr, times = t, params = P, common_dr = cd)[[ep]]
CG <- read.csv(file.path(out_dir, "calibration_gate.csv"))
CG$engine <- mapply(function(a, m) eng(a, "all", m / 12, "OS"), CG$arm, CG$month)
CG$inside <- CG$engine >= CG$ci95_lo - 1e-9 & CG$engine <= CG$ci95_hi + 1e-9
CG$outside_pp <- pmax(CG$ci95_lo - CG$engine, CG$engine - CG$ci95_hi, 0)
CG$inside_995 <- CG$engine >= CG$ci995_lo - 1e-9 & CG$engine <= CG$ci995_hi + 1e-9
acc_a <- gate_a_accept(CG)
rmst_eng <- function(e, P, cd = FALSE) {
  tt <- seq(0, 5, by = 1 / 120); s <- survival_engine(e, "all", times = tt, params = P, common_dr = cd)$OS
  sum(diff(tt) * (head(s, -1) + tail(s, -1)) / 2)
}
GR <- read.csv(file.path(out_dir, "calibration_gate_rmst.csv"))
rd_s <- rmst_eng("pembro", PS) - rmst_eng("chemo", PS)
FA <- read.csv(file.path(ROOT, "data", "kn522_final_7y.csv"), stringsAsFactors = FALSE)
fv <- function(id, col) suppressWarnings(as.numeric(FA[[col]][FA$id == id]))
c7 <- expand.grid(endpoint = c("OS", "EFS"), arm = c("pembro", "placebo"), stringsAsFactors = FALSE)
c7$id <- paste0(tolower(c7$endpoint), "7_", c7$arm)
c7$engine <- mapply(function(a, ep) eng(a, "all", 7, ep), c7$arm, c7$endpoint)
c7$lo <- sapply(c7$id, fv, col = "lo"); c7$hi <- sapply(c7$id, fv, col = "hi")
c7$inside <- c7$engine >= c7$lo - 1e-9 & c7$engine <= c7$hi + 1e-9
GT <- rbind(data.frame(gate = "a", item = sprintf("%s %d months", CG$arm, CG$month), engine = CG$engine, lo = CG$ci95_lo, hi = CG$ci95_hi,
                       inside = CG$inside, outside_pp = CG$outside_pp, inside_995 = CG$inside_995),
            data.frame(gate = "b", item = "5-year OS RMST difference (years)", engine = rd_s, lo = GR$km_boot_ci95_lo, hi = GR$km_boot_ci95_hi,
                       inside = rd_s >= GR$km_boot_ci95_lo & rd_s <= GR$km_boot_ci95_hi, outside_pp = NA, inside_995 = NA),
            data.frame(gate = "c", item = c7$id, engine = c7$engine, lo = c7$lo, hi = c7$hi, inside = c7$inside, outside_pp = NA, inside_995 = NA))
GT$gate_result <- c(a = if (all(CG$inside)) "inside" else if (acc_a) "accepted by (i)+(ii)" else "not met",
                    b = if (GT$inside[GT$gate == "b"]) "inside" else "not met",
                    c = if (all(c7$inside)) "inside" else "not met")[GT$gate]
write.csv(GT, file.path(out_dir, "scenario_preprog_optimistic_gate.csv"), row.names = FALSE)
print(GT, row.names = FALSE)

# between-arm OS difference (pembro - placebo) at 5 and 7 years: scenario next to the base, k = 1
# and the reference (scenario_k1_arm_diff.csv of 05_calibrate.R)
AD <- read.csv(file.path(out_dir, "scenario_k1_arm_diff.csv"), stringsAsFactors = FALSE)
AO <- data.frame(quantity = AD$quantity, reference = AD$reference,
                 optimistic = c(eng("pembro", "all", 5, "OS") - eng("placebo", "all", 5, "OS"), rd_s,
                                eng("pembro", "all", 7, "OS") - eng("placebo", "all", 7, "OS")),
                 base = AD$base, k1 = AD$k1, reported = AD$reported)
AO$optimistic_minus_reported <- AO$optimistic - AO$reported
AO$k_optimistic <- PS$pembro_dr_k
write.csv(AO, file.path(out_dir, "scenario_preprog_optimistic_arm_diff.csv"), row.names = FALSE)
print(AO, row.names = FALSE)
