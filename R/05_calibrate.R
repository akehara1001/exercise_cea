# 05_calibrate.R
# Step 5, ninth round (2026-10-23, phase-2 preparation). Structure of round 8 with one change set by
# the user (survival after distant recurrence fully external, from the ESME curves), no stepwise
# trials, point estimate only (the bootstrap runs on Longleaf):
#   - deaths due to adverse events: per arm, evenly over the treatment period, not calibrated
#     (engine.R, config.R); removed from the deaths without recurrence of the EFS composition;
#   - progression precluding surgery is its own state (PreProg); excess death log-logistic in time
#     since entry, common to both arms; shape and median calibrated under external constraints
#     (calibration.R): median 10-26 months, all-cause survival 5 years after entry >= 5%;
#   - excess death after distant recurrence: log-logistic in time since DR; two sub-states by the
#     time of entry (round 8): early (DR up to CFG$dr_early_months = 18 months from randomization)
#     and late; shape and medians fully external (round 9): fits to the reconstructed ESME curves
#     (13_esme_fit.R, data/fits/esme_fits.rds); in the pembrolizumab arms multiplied by k,
#     calibrated with the two PreProg parameters (0.25 to 4);
#   - EFS models with the 5-year constraint (04_fit_models.R, efs5_constraint.csv).
# Objective: sum over both arms of squared differences (percentage points) between engine OS and
# the KM of Schmid 2024 Fig. 1A at months 1..78 (unchanged), plus (round 7) eight points of the
# KEYNOTE-522 final analysis at 7 years (data/kn522_final_7y.csv; calibration.R final7y_targets):
# OS and EFS by arm, ((engine - reported) / SE)^2 with the SE from the reported 95% CI, and OS by
# pCR status, with the binomial SE of the stratum size (IA7 pCR counts). The KM part is the same as
# an SE of 1 point per monthly point.
# Acceptance rule, fixed before this round was run (docs/acceptance_rule_round9.md, commit
# 73748f4; same as rounds 7 and 8; config.R):
#   (a) in each arm, engine OS inside the pointwise 95% CI of the reconstructed KM (survfit
#       default, log scale) at 1, 2, 3, 4 and 5 years; if not, accepted only if every point
#       outside is outside by <= 0.3 points and all 10 points are inside the Bonferroni (99.5%)
#       pointwise intervals;
#   (b) engine 5-year RMST difference between arms (pembro - placebo) inside the bootstrap 95% CI
#       of the KM difference (B = CFG$boot_B, resampling the reconstructed IPD within arm);
#   (c) in each arm, engine OS and EFS at 7 years inside the 95% CI of the final analysis. OS by
#       pCR status at 7 years is reported only (no CI; not part of the rule).
# Not accepted: no engine default is written (stop). The PreProg constraint boundaries and k at
# its bounds are reported (not part of the rule).
# Scenario "k = 1" (common post-DR mortality): for all comparisons involving pembrolizumab.
# Outputs: output/phase1/calibration.csv, calibration_gate.csv, calibration_gate_rmst.csv,
#          calibration_status.csv, calibration_rmst.csv, calibration_deaths_by_source.csv,
#          ae_deaths.csv, dr_survival_implied.csv, calibration_curves.csv, engine_checks.csv,
#          scenario_k1.csv, scenario_k1_gate.csv, scenario_k1_arm_diff.csv (between-arm OS
#          difference at 5 and 7 years), scenario_k1_arm_diff_ci.csv (95% CI of the reported
#          difference), calibration_final7y.csv (gate (c) and the other
#          7-year points), calibration_objective.csv, calibration_vs_previous.csv (rounds 6 to
#          9), dr_early_share.csv, fig_calibration_OS.png, fig_engine_checks.png;
#          data/fits/calibration_candidates.rds, data/fits/engine_params.rds (accepted only)

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
source(file.path(ROOT, "R", "calibration.R"))
suppressPackageStartupMessages({
  library(survival)
  library(ggplot2)
})
out_dir <- file.path(ROOT, "output", "phase1")
ipd <- readRDS(file.path(ROOT, "data", "ipd", "ipd_all.rds"))
km_fit <- function(d) survfit(Surv(time, status) ~ 1, data = d)
km_at <- function(d, tm) summary(km_fit(d), times = tm, extend = TRUE)$surv
arm_of <- c(pembro = "pembro", placebo = "chemo")
os_ipd <- lapply(names(arm_of), function(a) ipd[[paste0("K24_F1A_OS_", a)]]); names(os_ipd) <- names(arm_of)
g_m <- CFG$calib_grid_months
gate_m <- 12 * CFG$gate_years
target <- lapply(os_ipd, function(d) 100 * km_at(d, g_m))
X7 <- final7y_targets()                         # calibration.R: 8 points at 7 years with their SE

stopifnot(!is.null(DR_EXT_BASE))                # data/fits/esme_fits.rds from 13_esme_fit.R
# the refit used in the bootstrap reproduces the saved ESME parameters on the original IPD
stopifnot(max(abs(esme_refit(ESME_IPD, ESME_FIT$engine$decision) - DR_EXT_BASE)) < 1e-10)
P0 <- engine_params(dr = dr_ext_spec(DR_EXT_BASE), preprog = list(dist = "llogis", shape = 1, scale = 1))
os_model <- function(P, months = g_m) lapply(arm_of, function(e) 100 * survival_engine(e, "all", times = months / 12, params = P)$OS)
set.seed(CFG$seed)                              # random restarts if optim returns code 52
cal <- calibrate_os(P0, target, g_m, DR_EXT_BASE, extra = X7)      # calibration.R (6 starts)
best <- cal$optim; vals <- cal$starts_values; at_bound <- cal$at_bound
P1 <- cal_apply(P0, cal$par, DR_EXT_BASE)
STRUCT <- sprintf("AE deaths (data) + PreProg log-logistic (constrained) + DR early/late log-logistic, shape and medians external (ESME fit, %s shape), x k in pembrolizumab arms",
                  ESME_FIT$engine$decision)
constraint_bound <- at_bound[["pp_median_low"]] || at_bound[["pp_median_high"]] || at_bound[["pp_s5_at_min"]]
cat(sprintf("PreProg log-logistic shape %.4f (cap %.4f), median %.4f months; DR log-logistic shape early %.4f / late %.4f, median early %.4f / late %.4f months (external); k %.4f; objective %.2f; starts spread %.2e; convergence %d\n",
            P1$preprog$shape, pp_shape_cap(P1$preprog$scale), 12 * P1$preprog$scale, P1$dr$shape, P1$dr$late_shape, 12 * P1$dr$scale,
            12 * P1$dr$late_scale, P1$pembro_dr_k, best$value, diff(range(vals)), best$convergence))
print(round(vals, 4)); print(at_bound); print(cal$code52)

# gate (a): pointwise 95% CI of the KM at 1-5 years, with the Bonferroni (99.5%) intervals and the
# excursion outside the 95% CI for the acceptance rule
m_g <- os_model(P1, gate_m)
G <- do.call(rbind, lapply(names(arm_of), function(a) {
  s <- summary(km_fit(os_ipd[[a]]), times = gate_m, extend = TRUE)
  sb <- summary(survfit(Surv(time, status) ~ 1, data = os_ipd[[a]], conf.int = CFG$gate_accept_simultaneous_level), times = gate_m, extend = TRUE)
  en <- m_g[[a]]
  data.frame(arm = a, month = gate_m, km = 100 * s$surv, ci95_lo = 100 * s$lower, ci95_hi = 100 * s$upper,
             ci995_lo = 100 * sb$lower, ci995_hi = 100 * sb$upper, engine = en, diff = en - 100 * s$surv,
             inside = en >= 100 * s$lower - 1e-9 & en <= 100 * s$upper + 1e-9,
             outside_pp = pmax(100 * s$lower - en, en - 100 * s$upper, 0),
             inside_995 = en >= 100 * sb$lower - 1e-9 & en <= 100 * sb$upper + 1e-9)
}))
write.csv(G, file.path(out_dir, "calibration_gate.csv"), row.names = FALSE)
pass_a_strict <- all(G$inside)
accept_a <- gate_a_accept(G)                    # calibration.R (round 10: Bonferroni intervals only)
cat("gate (a):", ifelse(pass_a_strict, "PASS", ifelse(accept_a, "outside the 95% CI but ACCEPTED by rule (i)+(ii)", "FAIL")), "\n")
print(G, row.names = FALSE)

# RMST to 5 years (years), engine vs KM, and the between-arm difference
rmst_km <- function(d) summary(survfit(Surv(time / 12, status) ~ 1, data = d), rmean = 5)$table[["rmean"]]
rmst_eng <- function(e, P = P1, common_dr = FALSE) {
  tt <- seq(0, 5, by = 1 / 120); s <- survival_engine(e, "all", times = tt, params = P, common_dr = common_dr)$OS
  sum(diff(tt) * (head(s, -1) + tail(s, -1)) / 2)
}
RM <- data.frame(arm = names(arm_of), rmst5_km = sapply(os_ipd, rmst_km), rmst5_engine = sapply(arm_of, rmst_eng))
RM$diff <- RM$rmst5_engine - RM$rmst5_km
RM <- rbind(RM, data.frame(arm = "pembro - placebo", rmst5_km = RM$rmst5_km[1] - RM$rmst5_km[2],
                           rmst5_engine = RM$rmst5_engine[1] - RM$rmst5_engine[2],
                           diff = (RM$rmst5_engine[1] - RM$rmst5_engine[2]) - (RM$rmst5_km[1] - RM$rmst5_km[2])))
write.csv(RM, file.path(out_dir, "calibration_rmst.csv"), row.names = FALSE)
print(RM, row.names = FALSE)

# gate (b): engine difference inside the bootstrap 95% CI of the KM difference
set.seed(CFG$seed)
boot_d <- replicate(CFG$boot_B, {
  b <- lapply(os_ipd, function(d) d[sample.int(nrow(d), nrow(d), replace = TRUE), ])
  rmst_km(b$pembro) - rmst_km(b$placebo)
})
km_d <- RM$rmst5_km[3]; en_d <- RM$rmst5_engine[3]
GR <- data.frame(quantity = "5-year OS RMST difference, pembro - placebo (years)", km = km_d,
                 km_boot_ci95_lo = unname(quantile(boot_d, 0.025)), km_boot_ci95_hi = unname(quantile(boot_d, 0.975)),
                 boot_B = CFG$boot_B, engine = en_d, engine_minus_km = en_d - km_d, rel_error = (en_d - km_d) / km_d,
                 round3_allowed_lo = km_d * (1 - CFG$gate_rmst_rel_tol_round3), round3_allowed_hi = km_d * (1 + CFG$gate_rmst_rel_tol_round3))
GR$pass <- en_d >= GR$km_boot_ci95_lo && en_d <= GR$km_boot_ci95_hi
write.csv(GR, file.path(out_dir, "calibration_gate_rmst.csv"), row.names = FALSE)
cat("gate (b):", ifelse(GR$pass, "PASS", "FAIL"), "\n"); print(GR, row.names = FALSE)

# gate (c): engine OS and EFS at 7 years inside the 95% CI of the final analysis; OS by pCR status
# (no CI) and DRFS (not in the objective) reported. Values from survival_engine(), checked against
# point_value() used in the objective; objective_term = ((engine - reported) / SE)^2
FA <- read.csv(file.path(ROOT, "data", "kn522_final_7y.csv"), stringsAsFactors = FALSE)
fv <- function(id, col) suppressWarnings(as.numeric(FA[[col]][match(id, FA$id)]))
G7 <- rbind(X7, data.frame(id = c("drfs7_pembro", "drfs7_placebo"), arm = c("pembro", "placebo"), pcr = "all", endpoint = "DRFS", month = 84,
                           value = fv(c("drfs7_pembro", "drfs7_placebo"), "value"), se = NA, n = NA, weight_basis = "not in the objective"))
G7$ci95_lo <- fv(G7$id, "lo"); G7$ci95_hi <- fv(G7$id, "hi"); G7$source <- FA$outlet[match(G7$id, FA$id)]
eng7 <- function(arm, pcr, endpoint, common_dr) 100 * survival_engine(arm_of[[arm]], pcr, times = 7, params = P1, common_dr = common_dr)[[endpoint]]
G7$engine <- mapply(eng7, G7$arm, G7$pcr, G7$endpoint, MoreArgs = list(common_dr = FALSE))
G7$engine_k1 <- mapply(eng7, G7$arm, G7$pcr, G7$endpoint, MoreArgs = list(common_dr = TRUE))
fl1 <- cal_flows(P1); s1 <- cal_specs(cal$par, DR_EXT_BASE)
pv <- sapply(seq_len(nrow(X7)), function(i) point_value(fl1, s1, X7$arm[i], X7$pcr[i], X7$endpoint[i], X7$month[i]))
stopifnot(max(abs(pv - G7$engine[seq_len(nrow(X7))])) < 1e-8)
G7$diff <- G7$engine - G7$value; G7$diff_k1 <- G7$engine_k1 - G7$value
G7$objective_term <- (G7$diff / G7$se)^2
G7$inside_ci <- ifelse(is.na(G7$ci95_lo), NA, G7$engine >= G7$ci95_lo - 1e-9 & G7$engine <= G7$ci95_hi + 1e-9)
G7$inside_ci_k1 <- ifelse(is.na(G7$ci95_lo), NA, G7$engine_k1 >= G7$ci95_lo - 1e-9 & G7$engine_k1 <= G7$ci95_hi + 1e-9)
G7$gate_c <- G7$pcr == "all" & G7$endpoint %in% c("OS", "EFS")
write.csv(G7, file.path(out_dir, "calibration_final7y.csv"), row.names = FALSE)
pass_c <- all(G7$inside_ci[G7$gate_c])
cat("gate (c):", ifelse(pass_c, "PASS", "FAIL"), "\n")
print(transform(G7[, c("id", "value", "se", "ci95_lo", "ci95_hi", "engine", "engine_k1", "diff", "objective_term", "inside_ci", "gate_c")],
                engine = round(engine, 2), engine_k1 = round(engine_k1, 2), diff = round(diff, 2), objective_term = round(objective_term, 3)), row.names = FALSE)

# objective at the solution: KM part (months 1..78, both arms) and the 7-year points
m_cal <- os_model(P1)
OB <- data.frame(part = c("KM OS, months 1-78, both arms (pp^2)", "7-year points, OS and EFS by arm (weighted)",
                          "7-year points, OS by pCR status (weighted)", "total"),
                 n_points = c(2 * length(g_m), 4, 4, 2 * length(g_m) + 8),
                 value = c(sum((m_cal$pembro - target$pembro)^2) + sum((m_cal$placebo - target$placebo)^2),
                           sum(G7$objective_term[G7$gate_c]), sum(G7$objective_term[G7$pcr != "all"]), NA))
OB$value[4] <- sum(OB$value[1:3])
stopifnot(abs(OB$value[4] - best$value) < 1e-6 * max(1, best$value))
write.csv(OB, file.path(out_dir, "calibration_objective.csv"), row.names = FALSE)
print(OB, row.names = FALSE)

pass_a <- accept_a; pass_b <- GR$pass; pass <- accept_a && pass_b && pass_c
write.csv(data.frame(structure = STRUCT, gate_a_strict_pass = pass_a_strict, gate_a_accepted = accept_a, gate_b_pass = pass_b, gate_c_pass = pass_c,
                     constraint_at_bound = constraint_bound, k_at_bound = at_bound[["k_low"]] || at_bound[["k_high"]],
                     gate_pass = pass, stop_before_step6 = !pass),
          file.path(out_dir, "calibration_status.csv"), row.names = FALSE)

# fit summary (start value vs calibrated)
fit_row <- function(P, stage) {
  m <- os_model(P); gg <- os_model(P, gate_m)
  do.call(rbind, lapply(names(arm_of), function(a) {
    km <- 100 * km_at(os_ipd[[a]], gate_m)
    data.frame(stage = stage, arm = a, SSE_both_arms = sum((m$pembro - target$pembro)^2) + sum((m$placebo - target$placebo)^2),
               rmse_pp = sqrt(mean((m[[a]] - target[[a]])^2)), max_abs_diff_pp = max(abs(m[[a]] - target[[a]])),
               gate_max_abs_diff_pp = max(abs(gg[[a]] - km)), preprog_shape = P$preprog$shape, preprog_median_months = 12 * P$preprog$scale,
               preprog_shape_cap = pp_shape_cap(P$preprog$scale), dr_shape = P$dr$shape, dr_median_months = 12 * P$dr$scale,
               dr_late_shape = if (is.null(P$dr$late_shape)) P$dr$shape else P$dr$late_shape,
               dr_late_median_months = 12 * P$dr$late_scale,
               pembro_dr_k = P$pembro_dr_k)
  }))
}
CAL <- rbind(fit_row(P0, "start value"), fit_row(P1, "calibrated"))
write.csv(CAL, file.path(out_dir, "calibration.csv"), row.names = FALSE)

# round 9 vs rounds 6 to 8 (output/phase1/r6_*.csv, r7_*.csv: commits e530a56, d1b5517;
# output/phase1/round8/: commit 694b0f3); a late DR median exists from round 8, a separate late
# shape only if the ESME shapes differ (round 9)
prev <- function(cal_file, rmst_file) {
  C <- read.csv(file.path(out_dir, cal_file)); C <- C[C$stage == "calibrated", ][1, ]
  R <- read.csv(file.path(out_dir, rmst_file))
  c(C$pembro_dr_k, C$preprog_median_months, C$preprog_shape, C$preprog_shape_cap, C$dr_shape, C$dr_median_months,
    if (is.null(C$dr_late_median_months)) NA else C$dr_late_median_months, if (is.null(C$dr_late_shape)) NA else C$dr_late_shape,
    R$rmst5_engine[R$arm == "pembro - placebo"], C$SSE_both_arms)
}
VS <- data.frame(quantity = c("pembro_dr_k", "preprog_median_months", "preprog_shape", "preprog_shape_cap", "dr_shape_early_or_common",
                              "dr_median_months_early_or_common", "dr_median_months_late", "dr_shape_late", "rmst5_diff_engine_years",
                              "km_SSE_both_arms_pp2"),
                 round6 = prev("r6_calibration.csv", "r6_calibration_rmst.csv"), round7 = prev("r7_calibration.csv", "r7_calibration_rmst.csv"),
                 round8 = prev(file.path("round8", "calibration.csv"), file.path("round8", "calibration_rmst.csv")),
                 round9 = c(P1$pembro_dr_k, 12 * P1$preprog$scale, P1$preprog$shape, pp_shape_cap(P1$preprog$scale), P1$dr$shape,
                            12 * P1$dr$scale, 12 * P1$dr$late_scale, P1$dr$late_shape, RM$rmst5_engine[3], OB$value[1]))
write.csv(VS, file.path(out_dir, "calibration_vs_previous.csv"), row.names = FALSE)
if (file.exists(file.path(out_dir, "calibration_vs_r6.csv"))) file.remove(file.path(out_dir, "calibration_vs_r6.csv"))
print(VS, row.names = FALSE)

# share of distant recurrences that are early (entered up to CFG$dr_early_months from
# randomization), by arm: among all DR entries to age 100 and among those by 5 and 7 years; and
# the cumulative incidence (percent of the arm). DR entries do not depend on post-DR mortality,
# so k and the scenario k = 1 do not change them.
DRE <- do.call(rbind, lapply(names(arm_of), function(a) {
  e <- survival_engine(arm_of[[a]], "all", params = P1)
  by <- function(y) { i <- e$time <= y + 1e-9; c(early = sum(e$In_DR_early[i]), all = sum(e$In_DR[i])) }
  r <- sapply(c(5, 7, 100 - CFG$start_age), by)
  data.frame(arm = a, horizon_years = c(5, 7, 100 - CFG$start_age), dr_cum_incidence_pct = 100 * r["all", ],
             early_cum_incidence_pct = 100 * r["early", ], late_cum_incidence_pct = 100 * (r["all", ] - r["early", ]),
             early_share = r["early", ] / r["all", ], early_months = CFG$dr_early_months)
}))
write.csv(DRE, file.path(out_dir, "dr_early_share.csv"), row.names = FALSE)
print(DRE, row.names = FALSE)

# implied median survival after PreProg (entry ~ age 49.5) and after early and late DR (excess-only
# and all-cause from age 50.5 for both; common hazard, k = 1)
tt <- round(seq(0, 40, by = 1 / 1200), 8)
med <- function(S) tt[which(S <= 0.5)[1]]
S_ppx <- exp(-dr_cumhaz(P1$preprog, tt))
S_pp <- S_ppx * S_pop(PP_ENTRY_AGE, tt)
S_dex <- exp(-dr_cumhaz(P1$dr, tt))
S_dlx <- exp(-dr_cumhaz(dr_late_spec(P1$dr), tt))
S_dr_bg <- S_pop(CFG$start_age + 1.5, tt)
IMP <- data.frame(state = c("PreProg", "DR early", "DR late"),
                  median_excess_only_months = 12 * c(med(S_ppx), med(S_dex), med(S_dlx)),
                  median_all_cause_months = 12 * c(med(S_pp), med(S_dex * S_dr_bg), med(S_dlx * S_dr_bg)),
                  surv_1y = c(S_pp[tt == 1], (S_dex * S_dr_bg)[tt == 1], (S_dlx * S_dr_bg)[tt == 1]),
                  surv_2y = c(S_pp[tt == 2], (S_dex * S_dr_bg)[tt == 2], (S_dlx * S_dr_bg)[tt == 2]),
                  surv_5y = c(S_pp[tt == 5], (S_dex * S_dr_bg)[tt == 5], (S_dlx * S_dr_bg)[tt == 5]))
write.csv(IMP, file.path(out_dir, "dr_survival_implied.csv"), row.names = FALSE)
print(IMP, row.names = FALSE)

# deaths by source at the gate times (percent of the arm)
DS <- do.call(rbind, lapply(names(arm_of), function(a) {
  e <- survival_engine(arm_of[[a]], "all", times = gate_m / 12, params = P1)
  data.frame(arm = a, month = gate_m, km_deaths = 100 * (1 - km_at(os_ipd[[a]], gate_m)),
             engine_deaths = 100 * e$Dead, from_event_free = 100 * e$Dead_from_EF, from_ae = 100 * e$Dead_from_AE,
             from_preprog = 100 * e$Dead_from_PreProg, from_LRR = 100 * e$Dead_from_LRR, from_DR = 100 * e$Dead_from_DR)
}))
write.csv(DS, file.path(out_dir, "calibration_deaths_by_source.csv"), row.names = FALSE)
print(DS, row.names = FALSE)

# engine 5-year RMST lost by death source (years): RMST5 = 5 - sum of the sources; the last row
# (placebo - pembro) is each source's contribution to the engine's between-arm RMST difference
src <- c(event_free = "Dead_from_EF", ae = "Dead_from_AE", preprog = "Dead_from_PreProg", LRR = "Dead_from_LRR", DR = "Dead_from_DR")
trap <- function(x, y) sum(diff(x) * (head(y, -1) + tail(y, -1)) / 2)
RS <- do.call(rbind, lapply(names(arm_of), function(a) {
  tt5 <- seq(0, 5, by = 1 / 120); e <- survival_engine(arm_of[[a]], "all", times = tt5, params = P1)
  data.frame(arm = a, t(sapply(src, function(s) trap(tt5, e[[s]]))), total = trap(tt5, e$Dead))
}))
RS <- rbind(RS, data.frame(arm = "placebo - pembro", RS[RS$arm == "placebo", -1] - RS[RS$arm == "pembro", -1]))
write.csv(RS, file.path(out_dir, "calibration_rmst_by_source.csv"), row.names = FALSE)
print(RS, row.names = FALSE)

# deaths due to adverse events: input vs what the engine realises (after surgery the AE hazard is
# capped by the EFS-model excess hazard of the cycle)
ae_capped <- function(a) sum(sapply(c("pCR", "nonpCR"), function(b) {
  sp <- P1$efs[[a]][[b]]; t <- seq(0, P1$ae_end, by = P1$cycle); K <- length(t) - 1
  hb <- H_pop(P1$start_age + t[-(K + 1)], P1$cycle); post <- t[-(K + 1)] >= P1$L - 1e-9
  dH <- -log(spec_surv(sp, pmax(t[-1] - P1$L, 0))) + log(spec_surv(sp, pmax(t[-(K + 1)] - P1$L, 0)))
  dHex <- if (sp$family == "cure") dH else pmax(dH - hb, 0)
  sum(post & dHex < P1$ae[[a]][["rate"]] * P1$cycle)
}))
AE <- do.call(rbind, lapply(names(arm_of), function(a) {
  e <- survival_engine(arm_of[[a]], "all", times = c(CFG$landmark_months, 12) / 12, params = P1)
  data.frame(arm = a, source = P1$ae_source, deaths = P1$ae[[a]][["deaths"]], n_treated = P1$ae[[a]][["n_treated"]],
             input_pct = 100 * P1$ae[[a]][["prob"]], period_years = P1$ae_end,
             engine_pct_by_surgery = 100 * e$Dead_from_AE[1], engine_pct_by_1y = 100 * e$Dead_from_AE[2],
             post_surgery_cycles_capped = ae_capped(a),
             composition_deaths = P1$composition[[a]][["death"]],
             expected_background_deaths = P1$shares[[a]][["expected_background_deaths"]],
             deaths_without_recurrence_used = P1$composition[[a]][["death"]] - P1$shares[[a]][["expected_background_deaths"]] - P1$ae[[a]][["deaths"]],
             share_death = P1$shares[[a]][["death"]], share_LRR = P1$shares[[a]][["LRR"]], share_DR = P1$shares[[a]][["DR"]])
}))
write.csv(AE, file.path(out_dir, "ae_deaths.csv"), row.names = FALSE)
print(AE, row.names = FALSE)

# scenario "k = 1" (common post-DR mortality, other parameters as calibrated): only the
# pembrolizumab arms change
OA <- data.frame(k_base = P1$pembro_dr_k, rmst5_pembro_k1 = rmst_eng("pembro", P1, TRUE), rmst5_pembro_base = RM$rmst5_engine[1],
                 rmst5_placebo = RM$rmst5_engine[2], km_rmst_diff = km_d)
OA$engine_rmst_diff_k1 <- OA$rmst5_pembro_k1 - OA$rmst5_placebo
write.csv(OA, file.path(out_dir, "scenario_k1.csv"), row.names = FALSE)
OG <- do.call(rbind, lapply(names(arm_of), function(a) {
  s <- summary(km_fit(os_ipd[[a]]), times = gate_m, extend = TRUE)
  en <- 100 * survival_engine(arm_of[[a]], "all", times = gate_m / 12, params = P1, common_dr = TRUE)$OS
  data.frame(arm = a, month = gate_m, km = 100 * s$surv, ci95_lo = 100 * s$lower, ci95_hi = 100 * s$upper,
             engine_base = m_g[[a]], engine_k1 = en, diff_k1 = en - 100 * s$surv,
             inside_k1 = en >= 100 * s$lower - 1e-9 & en <= 100 * s$upper + 1e-9)
}))
write.csv(OG, file.path(out_dir, "scenario_k1_gate.csv"), row.names = FALSE)
for (f in c("os_anchor.csv", "os_anchor_gate.csv")) if (file.exists(file.path(out_dir, f))) file.remove(file.path(out_dir, f))
cat("scenario k = 1:\n"); print(OG, row.names = FALSE)
# between-arm OS difference (pembro - placebo) at 5 and 7 years: base, scenario k = 1 and the
# reference (5 years: reconstructed KM, OS and RMST; 7 years: the final analysis)
og5 <- function(col, a) OG[[col]][OG$arm == a & OG$month == 60]
g7d <- function(col) G7[[col]][G7$id == "os7_pembro"] - G7[[col]][G7$id == "os7_placebo"]
AD <- data.frame(quantity = c("OS at 5 years (points)", "RMST to 5 years (years)", "OS at 7 years (points)"),
                 reference = c("reconstructed KM (2024 Fig. 1A)", "reconstructed KM (2024 Fig. 1A)", "final analysis (reported)"),
                 base = c(og5("engine_base", "pembro") - og5("engine_base", "placebo"), RM$rmst5_engine[3], g7d("engine")),
                 k1 = c(og5("engine_k1", "pembro") - og5("engine_k1", "placebo"), OA$engine_rmst_diff_k1, g7d("engine_k1")),
                 reported = c(og5("km", "pembro") - og5("km", "placebo"), km_d, g7d("value")))
AD$base_minus_reported <- AD$base - AD$reported; AD$k1_minus_reported <- AD$k1 - AD$reported
AD$k_base <- P1$pembro_dr_k
write.csv(AD, file.path(out_dir, "scenario_k1_arm_diff.csv"), row.names = FALSE)
print(AD, row.names = FALSE)
# uncertainty of the reported between-arm OS difference at 5 years (2024 paper, IA7) and 7 years
# (final analysis): SE of each arm = CI width / 3.92, SE of the difference = sqrt(SE1^2 + SE2^2)
# (arms independent), 95% CI = difference +- 1.96 SE; base and k = 1 checked against it
rvf <- read.csv(file.path(ROOT, "data", "reported_values.csv"), stringsAsFactors = FALSE)
r5 <- function(key) as.numeric(rvf$value[rvf$fact_id == "K24_os_milestones" & rvf$key == key])
f7 <- function(id, col) G7[[col]][G7$id == id]
ADU <- data.frame(year = c(5, 7), source = c("2024 paper (IA7), 5-year OS", "final analysis, 7-year OS"),
                  pembro = c(r5("pembro_5y"), f7("os7_pembro", "value")), pembro_lo = c(r5("pembro_5y_lo"), f7("os7_pembro", "ci95_lo")),
                  pembro_hi = c(r5("pembro_5y_hi"), f7("os7_pembro", "ci95_hi")),
                  placebo = c(r5("placebo_5y"), f7("os7_placebo", "value")), placebo_lo = c(r5("placebo_5y_lo"), f7("os7_placebo", "ci95_lo")),
                  placebo_hi = c(r5("placebo_5y_hi"), f7("os7_placebo", "ci95_hi")))
ADU$se_pembro <- (ADU$pembro_hi - ADU$pembro_lo) / 3.92; ADU$se_placebo <- (ADU$placebo_hi - ADU$placebo_lo) / 3.92
ADU$diff <- ADU$pembro - ADU$placebo; ADU$se_diff <- sqrt(ADU$se_pembro^2 + ADU$se_placebo^2)
ADU$ci95_lo <- ADU$diff - qnorm(0.975) * ADU$se_diff; ADU$ci95_hi <- ADU$diff + qnorm(0.975) * ADU$se_diff
ADU$base <- AD$base[c(1, 3)]; ADU$k1 <- AD$k1[c(1, 3)]
ADU$base_inside <- ADU$base >= ADU$ci95_lo & ADU$base <= ADU$ci95_hi; ADU$k1_inside <- ADU$k1 >= ADU$ci95_lo & ADU$k1 <= ADU$ci95_hi
write.csv(ADU, file.path(out_dir, "scenario_k1_arm_diff_ci.csv"), row.names = FALSE)
print(ADU, row.names = FALSE)
saveRDS(list(structure = STRUCT, params = P1, optim = best, starts_values = vals, at_bound = at_bound, code52 = cal$code52,
             constraint_at_bound = constraint_bound),
        file.path(ROOT, "data", "fits", "calibration_candidates.rds"))

# diagnostic when the calibration is not accepted (no calibration, no change of structure):
# within the allowed region of the three calibrated parameters (PreProg median 10-26 months and
# 5-year survival >= 5%, k in [0.25, 4]), the smallest possible excursion of the engine OS
# outside the KM 95% CIs at 1-5 years (Nelder-Mead on transformed parameters)
if (!pass_a) {
  ci <- lapply(os_ipd, function(d) summary(km_fit(d), times = gate_m, extend = TRUE))
  fl <- cal_flows(P1)
  kb <- log(CFG$pembro_dr_k_bounds)
  to_th <- function(z) c(CAL_LOWER[1] + diff(PP_MEDIAN_BOUNDS) * plogis(z[1]), plogis(z[2]), kb[1] + diff(kb) * plogis(z[3]))
  excursion <- function(th) {
    o <- cal_os(fl, cal_specs(th, DR_EXT_BASE))
    max(sapply(names(arm_of), function(a) {
      v <- 100 * o[[a]][gate_m + 1]
      max(pmax(100 * ci[[a]]$lower - v, v - 100 * ci[[a]]$upper, 0))
    }))
  }
  rmst_d <- function(th) { o <- cal_os(fl, cal_specs(th, DR_EXT_BASE)); rmst5_monthly(o$pembro) - rmst5_monthly(o$placebo) }
  q <- function(x) qlogis(pmin(pmax(x, 1e-4), 1 - 1e-4))
  from_th <- function(th) c(q((th[1] - CAL_LOWER[1]) / diff(PP_MEDIAN_BOUNDS)), q(th[2]), q((th[3] - kb[1]) / diff(kb)))
  st <- c(CAL_STARTS, list(cal$par), lapply(seq(-3, 3, by = 1.5), function(z) to_th(c(z, 2, 0))),
          lapply(c(-2, 0, 2), function(z) to_th(c(-2, 2, z))))
  FS <- do.call(rbind, lapply(seq_along(st), function(i) {
    o <- optim(from_th(st[[i]]), function(z) excursion(to_th(z)), method = "Nelder-Mead", control = list(maxit = 4000, reltol = 1e-12))
    th <- to_th(o$par)
    data.frame(start = i, preprog_median_months = 12 * th[1], preprog_shape = th[2] * pp_shape_cap(th[1]), u = th[2],
               k = exp(th[3]), max_outside_ci_pp = o$value, rmst_diff = rmst_d(th),
               rmst_inside_boot_ci = rmst_d(th) >= GR$km_boot_ci95_lo && rmst_d(th) <= GR$km_boot_ci95_hi)
  }))
  write.csv(FS, file.path(out_dir, "calibration_gate_feasibility_r9.csv"), row.names = FALSE)
  cat("gate (a) feasibility within the constraints: smallest excursion", min(FS$max_outside_ci_pp), "pp\n")
  print(FS[order(FS$max_outside_ci_pp), ][1:3, ], row.names = FALSE)
}

if (pass) saveRDS(P1, file.path(ROOT, "data", "fits", "engine_params.rds")) else {
  cat("not accepted under the round-9 rule: stop before step 6\n")
  if (file.exists(file.path(ROOT, "data", "fits", "engine_params.rds"))) file.remove(file.path(ROOT, "data", "fits", "engine_params.rds"))
}

# curves and checks against curves not used for calibration
m0 <- os_model(P0); m1 <- os_model(P1)
CC <- do.call(rbind, lapply(names(arm_of), function(a) {
  s <- summary(km_fit(os_ipd[[a]]), times = g_m, extend = TRUE)
  data.frame(arm = a, month = g_m, km = target[[a]], km_lo = 100 * s$lower, km_hi = 100 * s$upper, before = m0[[a]], after = m1[[a]])
}))
write.csv(CC, file.path(out_dir, "calibration_curves.csv"), row.names = FALSE)
chk <- list()
add_chk <- function(what, arm, d, eng_col, eng_arm, pcr, months) {
  km <- 100 * km_at(d, months)
  en <- 100 * survival_engine(eng_arm, pcr, times = months / 12, params = P1)[[eng_col]]
  chk[[length(chk) + 1]] <<- data.frame(check = what, arm = arm, month = months, km = km, engine = en, diff = en - km)
}
for (a in names(arm_of)) {
  add_chk("EFS vs 2024 Fig. 2A (IA7)", a, ipd[[paste0("K24_F2A_EFS_", a)]], "EFS", arm_of[[a]], "all", seq(6, 78, 6))
  add_chk("DRFS vs 2022 Fig. S3 (IA4)", a, ipd[[paste0("K22_S3_DRFS_", a)]], "DRFS", arm_of[[a]], "all", seq(6, 42, 6))
  add_chk("OS pCR vs 2024 Fig. S4 (IA7)", a, ipd[[paste0("K24_S4_OS_pCR_", a, "_pCR")]], "OS", arm_of[[a]], "pCR", seq(6, 78, 6))
  add_chk("OS non-pCR vs 2024 Fig. S4 (IA7)", a, ipd[[paste0("K24_S4_OS_pCR_", a, "_nonpCR")]], "OS", arm_of[[a]], "nonpCR", seq(6, 78, 6))
}
CH <- do.call(rbind, chk)
write.csv(CH, file.path(out_dir, "engine_checks.csv"), row.names = FALSE)
print(aggregate(cbind(max_abs_diff = abs(diff)) ~ check + arm, data = CH, FUN = max))

lab <- if (pass) "engine, calibrated" else "engine, calibrated (gate failed, not adopted)"
pd <- rbind(data.frame(CC[, c("arm", "month")], curve = "KM (2024 Fig. 1A)", os = CC$km),
            data.frame(CC[, c("arm", "month")], curve = "engine, start value", os = CC$before),
            data.frame(CC[, c("arm", "month")], curve = lab, os = CC$after))
cols <- c("black", "grey60", "#C0392B"); names(cols) <- unique(pd$curve)
g <- ggplot(pd, aes(month, os, colour = curve, linetype = curve)) +
  geom_ribbon(data = CC, aes(x = month, ymin = km_lo, ymax = km_hi), inherit.aes = FALSE, fill = "grey88") +
  geom_line() + facet_wrap(~arm) +
  geom_vline(xintercept = gate_m, colour = "grey80", linewidth = 0.3) +
  scale_colour_manual(values = cols) + scale_linetype_manual(values = setNames(c("solid", "22", "solid"), names(cols))) +
  labs(x = "Months from randomization", y = "OS (%)", colour = NULL, linetype = NULL,
       title = "OS calibration; band: KM pointwise 95% CI; vertical lines: gate (a) at 1-5 years") +
  theme_bw(base_size = 9) + theme(legend.position = "bottom")
ggsave(file.path(out_dir, "fig_calibration_OS.png"), g, width = 7, height = 3.8, dpi = 200)
pd <- rbind(data.frame(CH[, c("check", "arm", "month")], curve = "KM", v = CH$km),
            data.frame(CH[, c("check", "arm", "month")], curve = "engine", v = CH$engine))
g <- ggplot(pd, aes(month, v, colour = curve)) + geom_line() + geom_point(size = 0.8) + facet_grid(arm ~ check) +
  scale_colour_manual(values = c(KM = "black", engine = "#C0392B")) +
  labs(x = "Months from randomization", y = "%", colour = NULL, title = "Engine vs curves not used for calibration") +
  theme_bw(base_size = 8) + theme(legend.position = "bottom")
ggsave(file.path(out_dir, "fig_engine_checks.png"), g, width = 10, height = 4.5, dpi = 200)
