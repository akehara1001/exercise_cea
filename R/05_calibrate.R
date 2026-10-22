# 05_calibrate.R
# Step 5, fifth round (2026-10-22). Structure as set by the user, no stepwise trials:
#   - deaths due to adverse events: per arm, evenly over the treatment period, not calibrated
#     (engine.R, config.R); removed from the deaths without recurrence of the EFS composition;
#   - progression precluding surgery is its own state (PreProg); its excess death hazard is
#     log-logistic in time since entry (round 5; Weibull in round 4, constant in round 3), common
#     to both arms; shape and median calibrated under external constraints (calibration.R):
#     median 10-26 months, all-cause survival 5 years after entry >= 5%;
#   - excess death after distant recurrence is log-logistic in time since DR, common to both
#     arms; median an external input (10.1 months, ESME, PMID 37385070), shape calibrated;
#   - EFS models with the 5-year constraint (04_fit_models.R, efs5_constraint.csv).
# Objective (unchanged): sum over both arms of squared differences (percentage points) between
# engine OS and the KM of Schmid 2024 Fig. 1A at months 1..78.
# Gate (history in config.R and the report):
#   (a) in each arm, engine OS inside the pointwise 95% CI of the reconstructed KM (survfit
#       default, log scale) at 1, 2, 3, 4 and 5 years;
#   (b) engine 5-year RMST difference between arms (pembro - placebo) inside the bootstrap 95% CI
#       of the KM difference (B = CFG$boot_B, resampling the reconstructed IPD within arm); the
#       point difference engine - KM is reported.
# Stop (no engine default written) if the gate fails or the PreProg solution lies on the
# boundary of either external constraint.
# Scenario "OS anchor" (not part of the base calibration): k = CFG$os_anchor_k_fixed multiplies
# the DR excess hazard of the pembrolizumab arms.
# Outputs: output/phase1/calibration.csv, calibration_gate.csv, calibration_gate_rmst.csv,
#          calibration_status.csv, calibration_rmst.csv, calibration_deaths_by_source.csv,
#          ae_deaths.csv, dr_survival_implied.csv, calibration_curves.csv, engine_checks.csv,
#          os_anchor.csv, os_anchor_gate.csv,
#          fig_calibration_OS.png, fig_engine_checks.png;
#          data/fits/calibration_candidates.rds, data/fits/engine_params.rds (passed only)

source("C:/Users/原明美/Documents/ClaudeCode/exercise_cea/R/config.R")
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

P0 <- engine_params(dr = list(dist = "llogis", shape = 1, scale = DR_MEDIAN_BASE), preprog = list(dist = "llogis", shape = 1, scale = 1))
os_model <- function(P, months = g_m) lapply(arm_of, function(e) 100 * survival_engine(e, "all", times = months / 12, params = P)$OS)
set.seed(CFG$seed)                              # random restarts if optim returns code 52
cal <- calibrate_os(P0, target, g_m, DR_MEDIAN_BASE)          # calibration.R (6 starts)
best <- cal$optim; vals <- cal$starts_values; at_bound <- cal$at_bound
P1 <- cal_apply(P0, cal$par, DR_MEDIAN_BASE)
P1$os_anchor_k <- CFG$os_anchor_k_fixed
STRUCT <- "AE deaths (data) + PreProg log-logistic (constrained) + DR log-logistic, median external (common)"
constraint_bound <- at_bound[["pp_median_low"]] || at_bound[["pp_median_high"]] || at_bound[["pp_s5_at_min"]]
cat(sprintf("PreProg log-logistic shape %.4f (cap %.4f), median %.4f months; DR log-logistic shape %.4f, median %.4f months (external); SSE %.2f; starts spread %.2e; convergence %d\n",
            P1$preprog$shape, pp_shape_cap(P1$preprog$scale), 12 * P1$preprog$scale, P1$dr$shape, 12 * P1$dr$scale, best$value,
            diff(range(vals)), best$convergence))
print(round(vals, 4)); print(at_bound); print(cal$code52)

# gate (a): pointwise 95% CI of the KM at 1-5 years
m_g <- os_model(P1, gate_m)
G <- do.call(rbind, lapply(names(arm_of), function(a) {
  s <- summary(km_fit(os_ipd[[a]]), times = gate_m, extend = TRUE)
  data.frame(arm = a, month = gate_m, km = 100 * s$surv, ci95_lo = 100 * s$lower, ci95_hi = 100 * s$upper,
             engine = m_g[[a]], diff = m_g[[a]] - 100 * s$surv,
             inside = m_g[[a]] >= 100 * s$lower - 1e-9 & m_g[[a]] <= 100 * s$upper + 1e-9)
}))
write.csv(G, file.path(out_dir, "calibration_gate.csv"), row.names = FALSE)
cat("gate (a):", ifelse(all(G$inside), "PASS", "FAIL"), "\n"); print(G, row.names = FALSE)

# RMST to 5 years (years), engine vs KM, and the between-arm difference
rmst_km <- function(d) summary(survfit(Surv(time / 12, status) ~ 1, data = d), rmean = 5)$table[["rmean"]]
rmst_eng <- function(e, P = P1, os_anchor = FALSE) {
  tt <- seq(0, 5, by = 1 / 120); s <- survival_engine(e, "all", times = tt, params = P, os_anchor = os_anchor)$OS
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

pass_a <- all(G$inside); pass_b <- GR$pass; pass <- pass_a && pass_b && !constraint_bound
write.csv(data.frame(structure = STRUCT, gate_a_pass = pass_a, gate_b_pass = pass_b, constraint_at_bound = constraint_bound,
                     gate_pass = pass_a && pass_b, stop_before_step6 = !pass),
          file.path(out_dir, "calibration_status.csv"), row.names = FALSE)

# fit summary (start value vs calibrated)
fit_row <- function(P, stage) {
  m <- os_model(P); gg <- os_model(P, gate_m)
  do.call(rbind, lapply(names(arm_of), function(a) {
    km <- 100 * km_at(os_ipd[[a]], gate_m)
    data.frame(stage = stage, arm = a, SSE_both_arms = sum((m$pembro - target$pembro)^2) + sum((m$placebo - target$placebo)^2),
               rmse_pp = sqrt(mean((m[[a]] - target[[a]])^2)), max_abs_diff_pp = max(abs(m[[a]] - target[[a]])),
               gate_max_abs_diff_pp = max(abs(gg[[a]] - km)), preprog_shape = P$preprog$shape, preprog_median_months = 12 * P$preprog$scale,
               preprog_shape_cap = pp_shape_cap(P$preprog$scale), dr_shape = P$dr$shape, dr_median_months = 12 * P$dr$scale)
  }))
}
CAL <- rbind(fit_row(P0, "start value"), fit_row(P1, "calibrated"))
write.csv(CAL, file.path(out_dir, "calibration.csv"), row.names = FALSE)

# implied median survival after PreProg (entry ~ age 49.5) and after DR (excess-only and all-cause from age 50.5)
tt <- round(seq(0, 40, by = 1 / 1200), 8)
med <- function(S) tt[which(S <= 0.5)[1]]
S_ppx <- exp(-dr_cumhaz(P1$preprog, tt))
S_pp <- S_ppx * S_pop(PP_ENTRY_AGE, tt)
S_drx <- exp(-dr_cumhaz(P1$dr, tt))
IMP <- data.frame(state = c("PreProg", "DR"),
                  median_excess_only_months = 12 * c(med(S_ppx), med(S_drx)),
                  median_all_cause_months = 12 * c(med(S_pp), med(S_drx * S_pop(CFG$start_age + 1.5, tt))),
                  surv_1y = c(S_pp[tt == 1], (S_drx * S_pop(CFG$start_age + 1.5, tt))[tt == 1]),
                  surv_2y = c(S_pp[tt == 2], (S_drx * S_pop(CFG$start_age + 1.5, tt))[tt == 2]),
                  surv_5y = c(S_pp[tt == 5], (S_drx * S_pop(CFG$start_age + 1.5, tt))[tt == 5]))
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

# scenario "OS anchor": fixed k (round-4 value, config.R) on the DR excess hazard of the
# pembrolizumab arms
OA <- data.frame(k = P1$os_anchor_k, rmst5_pembro_anchor = rmst_eng("pembro", P1, TRUE), rmst5_pembro_base = RM$rmst5_engine[1],
                 rmst5_placebo = RM$rmst5_engine[2], km_rmst_diff = km_d)
OA$engine_rmst_diff_anchor <- OA$rmst5_pembro_anchor - OA$rmst5_placebo
write.csv(OA, file.path(out_dir, "os_anchor.csv"), row.names = FALSE)
OG <- do.call(rbind, lapply(names(arm_of), function(a) {
  s <- summary(km_fit(os_ipd[[a]]), times = gate_m, extend = TRUE)
  en <- 100 * survival_engine(arm_of[[a]], "all", times = gate_m / 12, params = P1, os_anchor = TRUE)$OS
  data.frame(arm = a, month = gate_m, km = 100 * s$surv, ci95_lo = 100 * s$lower, ci95_hi = 100 * s$upper,
             engine_base = m_g[[a]], engine_anchor = en, diff_anchor = en - 100 * s$surv,
             inside_anchor = en >= 100 * s$lower - 1e-9 & en <= 100 * s$upper + 1e-9)
}))
write.csv(OG, file.path(out_dir, "os_anchor_gate.csv"), row.names = FALSE)
cat("OS anchor k =", P1$os_anchor_k, "\n"); print(OG, row.names = FALSE)
saveRDS(list(structure = STRUCT, params = P1, optim = best, starts_values = vals, at_bound = at_bound, code52 = cal$code52,
             constraint_at_bound = constraint_bound),
        file.path(ROOT, "data", "fits", "calibration_candidates.rds"))

# diagnostic when gate (a) fails (no calibration, no change of structure): within the allowed
# region of the three calibrated parameters (PreProg median 10-26 months and 5-year survival
# >= 5%, DR shape), the smallest possible excursion of the engine OS outside the KM 95% CIs at
# 1-5 years (Nelder-Mead on transformed parameters from the six calibration starts and a grid)
if (!pass_a) {
  ci <- lapply(os_ipd, function(d) summary(km_fit(d), times = gate_m, extend = TRUE))
  fl <- cal_flows(P1)
  to_th <- function(z) c(CAL_LOWER[1] + diff(PP_MEDIAN_BOUNDS) * plogis(z[1]), plogis(z[2]), z[3])
  excursion <- function(th) {
    s <- cal_specs(th, DR_MEDIAN_BASE)
    max(sapply(names(arm_of), function(a) {
      v <- 100 * os_fast(fl[[a]], s$preprog, s$dr)[gate_m + 1]
      max(pmax(100 * ci[[a]]$lower - v, v - 100 * ci[[a]]$upper, 0))
    }))
  }
  rmst_d <- function(th) { s <- cal_specs(th, DR_MEDIAN_BASE)
    rmst5_monthly(os_fast(fl$pembro, s$preprog, s$dr)) - rmst5_monthly(os_fast(fl$placebo, s$preprog, s$dr)) }
  from_th <- function(th) c(qlogis(pmin(pmax((th[1] - CAL_LOWER[1]) / diff(PP_MEDIAN_BOUNDS), 1e-4), 1 - 1e-4)),
                            qlogis(pmin(pmax(th[2], 1e-4), 1 - 1e-4)), th[3])
  st <- c(CAL_STARTS, list(cal$par), lapply(seq(-3, 3, by = 1.5), function(z) to_th(c(z, 2, log(1)))),
          lapply(c(-2, 0, 2), function(z) to_th(c(-2, z, log(0.5)))))
  FS <- do.call(rbind, lapply(seq_along(st), function(i) {
    o <- optim(from_th(st[[i]]), function(z) excursion(to_th(z)), method = "Nelder-Mead", control = list(maxit = 2000, reltol = 1e-12))
    th <- to_th(o$par)
    data.frame(start = i, preprog_median_months = 12 * th[1], preprog_shape = th[2] * pp_shape_cap(th[1]), u = th[2],
               dr_shape = exp(th[3]), max_outside_ci_pp = o$value, rmst_diff = rmst_d(th),
               rmst_inside_boot_ci = rmst_d(th) >= GR$km_boot_ci95_lo && rmst_d(th) <= GR$km_boot_ci95_hi)
  }))
  write.csv(FS, file.path(out_dir, "calibration_gate_feasibility_r5.csv"), row.names = FALSE)
  cat("gate (a) feasibility within the constraints: smallest excursion", min(FS$max_outside_ci_pp), "pp\n")
  print(FS[order(FS$max_outside_ci_pp), ][1:3, ], row.names = FALSE)
}

if (pass) saveRDS(P1, file.path(ROOT, "data", "fits", "engine_params.rds")) else {
  cat("gate failed or constraint at bound: stop before step 6\n")
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
