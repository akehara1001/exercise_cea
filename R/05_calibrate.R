# 05_calibrate.R
# Step 5: calibrate the excess mortality after distant recurrence (Weibull in time since DR,
# common to both arms) so that the engine reproduces the OS of both arms (Schmid 2024 Fig. 1A,
# reconstructed IPD). Objective: sum over both arms of squared differences (percentage points)
# between engine OS and the KM at months 1..78 (CFG$calib_grid_months).
# Starting value (pre-calibration): exponential, median 1.5 years after DR - a starting point for
# the optimiser, not an estimate.
# Variant: arm-specific DR mortality (each arm calibrated to its own OS). Rule fixed before
# running it: the arm-specific variant becomes the engine default only if it lowers the largest
# absolute difference of every OS check not used for calibration (OS by pCR, both arms; DRFS does
# not depend on DR mortality and is left out);
# otherwise the common parameters stay.
# Also reported, not calibrated: engine EFS by arm vs Schmid 2024 Fig. 2A (IA7), DRFS by arm vs
# Schmid 2022 appendix Fig. S3, OS by arm x pCR vs Schmid 2024 appendix Fig. S4.
# Outputs: output/phase1/calibration.csv, calibration_curves.csv, engine_checks.csv,
#          fig_calibration_OS.png, fig_engine_checks.png; data/fits/engine_params.rds

source("C:/Users/原明美/Documents/ClaudeCode/exercise_cea/R/config.R")
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
suppressPackageStartupMessages({
  library(survival)
  library(ggplot2)
})
out_dir <- file.path(ROOT, "output", "phase1")
ipd <- readRDS(file.path(ROOT, "data", "ipd", "ipd_all.rds"))
km_at <- function(d, tm) summary(survfit(Surv(time, status) ~ 1, data = d), times = tm, extend = TRUE)$surv
arm_of <- c(pembro = "pembro", placebo = "chemo")

g_m <- CFG$calib_grid_months
target <- lapply(names(arm_of), function(a) 100 * km_at(ipd[[paste0("K24_F1A_OS_", a)]], g_m))
names(target) <- names(arm_of)

P0 <- engine_params(dr_shape = 1, dr_scale = 1.5 / log(2))
os_model <- function(P) lapply(arm_of, function(e) 100 * survival_engine(e, "all", times = g_m / 12, params = P)$OS)
fit_stats <- function(P) {
  m <- os_model(P)
  do.call(rbind, lapply(names(arm_of), function(a) data.frame(
    arm = a, rmse_pp = sqrt(mean((m[[a]] - target[[a]])^2)), max_abs_diff_pp = max(abs(m[[a]] - target[[a]])),
    diff_36m = (m[[a]] - target[[a]])[g_m == 36], diff_60m = (m[[a]] - target[[a]])[g_m == 60],
    diff_78m = (m[[a]] - target[[a]])[g_m == 78])))
}
obj <- function(th) {
  P <- P0; P$dr_shape <- exp(th[1]); P$dr_scale <- exp(th[2])
  m <- os_model(P)
  sum((m$pembro - target$pembro)^2) + sum((m$placebo - target$placebo)^2)
}
th0 <- c(log(P0$dr_shape), log(P0$dr_scale))
starts <- list(th0, c(log(0.8), log(1.5)), c(log(1.5), log(3)))
opts <- lapply(starts, function(s) optim(s, obj, method = "Nelder-Mead", control = list(reltol = 1e-10, maxit = 2000)))
best <- opts[[which.min(sapply(opts, `[[`, "value"))]]
P1 <- P0; P1$dr_shape <- exp(best$par[1]); P1$dr_scale <- exp(best$par[2])
cat(sprintf("calibrated DR excess hazard: Weibull shape %.4f scale %.4f (median %.3f y); SSE %.2f -> %.2f; starts agree within %.4f\n",
            P1$dr_shape, P1$dr_scale, P1$dr_scale * log(2)^(1 / P1$dr_shape), obj(th0), best$value,
            diff(range(sapply(opts, `[[`, "value")))))
# arm-specific variant
obj_arm <- function(th, a) {
  P <- P0; P$dr_shape <- exp(th[1]); P$dr_scale <- exp(th[2])
  sum((100 * survival_engine(arm_of[[a]], "all", times = g_m / 12, params = P)$OS - target[[a]])^2)
}
arm_fit <- lapply(names(arm_of), function(a) {
  o <- lapply(starts, function(s) optim(s, obj_arm, a = a, method = "Nelder-Mead", control = list(reltol = 1e-10, maxit = 2000)))
  o[[which.min(sapply(o, `[[`, "value"))]]
})
names(arm_fit) <- names(arm_of)
P_arm <- lapply(names(arm_of), function(a) { P <- P0; P$dr_shape <- exp(arm_fit[[a]]$par[1]); P$dr_scale <- exp(arm_fit[[a]]$par[2]); P })
names(P_arm) <- names(arm_of)
for (a in names(arm_of)) cat(sprintf("arm-specific %s: shape %.4f scale %.4f (median %.3f y), SSE %.2f
", a, P_arm[[a]]$dr_shape,
                                     P_arm[[a]]$dr_scale, P_arm[[a]]$dr_scale * log(2)^(1 / P_arm[[a]]$dr_shape), arm_fit[[a]]$value))

before <- fit_stats(P0); before$stage <- "before (start value)"
after <- fit_stats(P1); after$stage <- "after calibration"
C <- rbind(before, after)
C$dr_shape <- rep(c(P0$dr_shape, P1$dr_shape), each = 2)
C$dr_scale <- rep(c(P0$dr_scale, P1$dr_scale), each = 2)
C$dr_median_years <- C$dr_scale * log(2)^(1 / C$dr_shape)
C$SSE_both_arms <- rep(c(obj(th0), best$value), each = 2)
write.csv(C, file.path(out_dir, "calibration.csv"), row.names = FALSE)
print(C, row.names = FALSE)

m0 <- os_model(P0); m1 <- os_model(P1)
CC <- do.call(rbind, lapply(names(arm_of), function(a) data.frame(arm = a, month = g_m, km = target[[a]], before = m0[[a]], after = m1[[a]])))
write.csv(CC, file.path(out_dir, "calibration_curves.csv"), row.names = FALSE)

# checks against curves that were not used for calibration
run_checks <- function(Pfor) {
chk <- list()
add_chk <- function(what, arm, d, eng_col, eng_arm, pcr, months) {
  km <- 100 * km_at(d, months)
  en <- 100 * survival_engine(eng_arm, pcr, times = months / 12, params = Pfor(arm))[[eng_col]]
  chk[[length(chk) + 1]] <<- data.frame(check = what, arm = arm, month = months, km = km, engine = en, diff = en - km)
}
for (a in names(arm_of)) {
  add_chk("EFS vs 2024 Fig. 2A (IA7)", a, ipd[[paste0("K24_F2A_EFS_", a)]], "EFS", arm_of[[a]], "all", seq(6, 78, 6))
  add_chk("DRFS vs 2022 Fig. S3 (IA4)", a, ipd[[paste0("K22_S3_DRFS_", a)]], "DRFS", arm_of[[a]], "all", seq(6, 42, 6))
  add_chk("OS pCR vs 2024 Fig. S4 (IA7)", a, ipd[[paste0("K24_S4_OS_pCR_", a, "_pCR")]], "OS", arm_of[[a]], "pCR", seq(6, 78, 6))
  add_chk("OS non-pCR vs 2024 Fig. S4 (IA7)", a, ipd[[paste0("K24_S4_OS_pCR_", a, "_nonpCR")]], "OS", arm_of[[a]], "nonpCR", seq(6, 78, 6))
}
do.call(rbind, chk)
}
CH_c <- run_checks(function(a) P1)
CH_a <- run_checks(function(a) P_arm[[a]])
mx <- function(CH) aggregate(cbind(max_abs_diff = abs(diff)) ~ check + arm, data = CH[grepl("^OS", CH$check), ], FUN = max)
cmp <- merge(mx(CH_c), mx(CH_a), by = c("check", "arm"), suffixes = c("_common", "_arm_specific"))
use_arm <- all(cmp$max_abs_diff_arm_specific < cmp$max_abs_diff_common)
cat("arm-specific DR mortality improves every out-of-sample check in both arms:", use_arm, "
")
print(cmp, row.names = FALSE)
write.csv(cmp, file.path(out_dir, "calibration_variant_checks.csv"), row.names = FALSE)
CH <- if (use_arm) CH_a else CH_c
write.csv(CH, file.path(out_dir, "engine_checks.csv"), row.names = FALSE)
print(aggregate(cbind(max_abs_diff = abs(diff)) ~ check + arm, data = CH, FUN = max))
# engine default parameters (common or arm-specific, by the rule above)
PE <- P1
PE$dr_by_arm <- if (use_arm) lapply(P_arm, function(P) c(shape = P$dr_shape, scale = P$dr_scale)) else NULL
PE$dr_variant <- if (use_arm) "arm-specific" else "common"
saveRDS(PE, file.path(ROOT, "data", "fits", "engine_params.rds"))
va <- do.call(rbind, lapply(names(arm_of), function(a) { s <- fit_stats(P_arm[[a]]); s <- s[s$arm == a, ]
  s$stage <- "arm-specific calibration"; s$dr_shape <- P_arm[[a]]$dr_shape; s$dr_scale <- P_arm[[a]]$dr_scale
  s$dr_median_years <- s$dr_scale * log(2)^(1 / s$dr_shape); s$SSE_both_arms <- arm_fit$pembro$value + arm_fit$placebo$value; s }))
write.csv(rbind(read.csv(file.path(out_dir, "calibration.csv")), va), file.path(out_dir, "calibration.csv"), row.names = FALSE)

pd <- rbind(data.frame(CC[, c("arm", "month")], curve = "KM (2024 Fig. 1A)", os = CC$km),
            data.frame(CC[, c("arm", "month")], curve = "engine, before", os = CC$before),
            data.frame(CC[, c("arm", "month")], curve = "engine, calibrated", os = CC$after))
g <- ggplot(pd, aes(month, os, colour = curve, linetype = curve)) + geom_line() + facet_wrap(~arm) +
  scale_colour_manual(values = c("KM (2024 Fig. 1A)" = "black", "engine, before" = "grey60", "engine, calibrated" = "#C0392B")) +
  scale_linetype_manual(values = c("KM (2024 Fig. 1A)" = "solid", "engine, before" = "22", "engine, calibrated" = "solid")) +
  labs(x = "Months from randomization", y = "OS (%)", colour = NULL, linetype = NULL, title = "OS calibration (distant-recurrence mortality)") +
  theme_bw(base_size = 9) + theme(legend.position = "bottom")
ggsave(file.path(out_dir, "fig_calibration_OS.png"), g, width = 7, height = 3.8, dpi = 200)
pd <- rbind(data.frame(CH[, c("check", "arm", "month")], curve = "KM", v = CH$km),
            data.frame(CH[, c("check", "arm", "month")], curve = "engine", v = CH$engine))
g <- ggplot(pd, aes(month, v, colour = curve)) + geom_line() + geom_point(size = 0.8) + facet_grid(arm ~ check) +
  scale_colour_manual(values = c(KM = "black", engine = "#C0392B")) +
  labs(x = "Months from randomization", y = "%", colour = NULL, title = "Engine vs curves not used for calibration") +
  theme_bw(base_size = 8) + theme(legend.position = "bottom")
ggsave(file.path(out_dir, "fig_engine_checks.png"), g, width = 10, height = 4.5, dpi = 200)
