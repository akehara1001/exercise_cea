# 05_calibrate.R
# Step 5 (redone 2026-10-22, one structure, no stepwise trials):
#   - progression precluding surgery is its own state (PreProg); its excess death rate is
#     constant and common to both arms;
#   - excess death after distant recurrence is log-logistic in time since DR (hazard rises then
#     falls: shape > 1), common to both arms, with the median constrained to 10-12 months
#     (ESME, PMID 37385070; IMpassion132, PMID 38755096); shape estimated;
#   - deaths without recurrence follow the arms' reported EFS event composition (engine.R).
# Calibrated: PreProg excess rate, log-logistic shape, log-logistic median (within 10-12 months).
# Objective: sum over both arms of squared differences (percentage points) between engine OS and
# the KM of Schmid 2024 Fig. 1A at months 1..78.
# Gate: |engine OS - KM| <= 1 percentage point at 1, 2, 3, 4 and 5 years in each arm.
# Diagnostics (not gates): 5-year RMST by arm and the between-arm difference (engine vs KM);
# implied median survival after PreProg and after DR; deaths by source at the gate times.
# If the gate fails: calibration_status.csv says stop_before_step6 = TRUE and no engine default
# (data/fits/engine_params.rds) is written.
# Outputs: output/phase1/calibration.csv, calibration_gate.csv, calibration_status.csv,
#          calibration_rmst.csv, calibration_deaths_by_source.csv, dr_survival_implied.csv,
#          calibration_curves.csv, engine_checks.csv, fig_calibration_OS.png, fig_engine_checks.png;
#          data/fits/calibration_candidates.rds, data/fits/engine_params.rds (gate passed only)

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
gate_m <- c(12, 24, 36, 48, 60)
median_bounds <- c(10, 12) / 12
target <- lapply(names(arm_of), function(a) 100 * km_at(ipd[[paste0("K24_F1A_OS_", a)]], g_m))
names(target) <- names(arm_of)

P0 <- engine_params(dr = list(dist = "llogis", shape = 2, scale = 11 / 12), preprog_rate = 1)
make_P <- function(th) {
  P <- P0
  P$preprog_rate <- exp(th[1])
  P$dr <- list(dist = "llogis", shape = exp(th[2]), scale = th[3])
  P
}
os_model <- function(P, months = g_m) lapply(arm_of, function(e) 100 * survival_engine(e, "all", times = months / 12, params = P)$OS)
obj <- function(th) { m <- os_model(make_P(th)); sum((m$pembro - target$pembro)^2) + sum((m$placebo - target$placebo)^2) }
lower <- c(log(0.01), log(1.0001), median_bounds[1]); upper <- c(log(50), log(20), median_bounds[2])
starts <- list(c(log(1), log(2), 11 / 12), c(log(0.3), log(1.5), 10 / 12), c(log(3), log(4), 12 / 12))
opts <- lapply(starts, function(s0) optim(s0, obj, method = "L-BFGS-B", lower = lower, upper = upper, control = list(factr = 1e5, maxit = 500)))
vals <- sapply(opts, `[[`, "value")
best <- opts[[which.min(vals)]]
P1 <- make_P(best$par)
saveRDS(list(structure = "PreProg constant + DR log-logistic (common)", params = P1, optim = best, starts_values = vals),
        file.path(ROOT, "data", "fits", "calibration_candidates.rds"))
cat(sprintf("PreProg excess rate %.4f/y; DR log-logistic shape %.4f, median %.4f y (bounds %.4f-%.4f); SSE %.2f; starts spread %.2e; convergence %d\n",
            P1$preprog_rate, P1$dr$shape, P1$dr$scale, median_bounds[1], median_bounds[2], best$value, diff(range(vals)), best$convergence))

# gate
m_g <- os_model(P1, gate_m)
G <- do.call(rbind, lapply(names(arm_of), function(a) {
  km <- 100 * km_at(ipd[[paste0("K24_F1A_OS_", a)]], gate_m)
  data.frame(arm = a, month = gate_m, km = km, engine = m_g[[a]], diff = m_g[[a]] - km, pass = abs(m_g[[a]] - km) <= 1 + 1e-9)
}))
write.csv(G, file.path(out_dir, "calibration_gate.csv"), row.names = FALSE)
pass <- all(G$pass)
write.csv(data.frame(structure = "PreProg constant + DR log-logistic (common)", gate_pass = pass, stop_before_step6 = !pass),
          file.path(out_dir, "calibration_status.csv"), row.names = FALSE)
cat("gate:", ifelse(pass, "PASS", "FAIL"), "\n"); print(G, row.names = FALSE)

# fit summary (start value vs calibrated)
fit_row <- function(P, stage) {
  m <- os_model(P); gg <- os_model(P, gate_m)
  do.call(rbind, lapply(names(arm_of), function(a) {
    km <- 100 * km_at(ipd[[paste0("K24_F1A_OS_", a)]], gate_m)
    data.frame(stage = stage, arm = a, SSE_both_arms = sum((m$pembro - target$pembro)^2) + sum((m$placebo - target$placebo)^2),
               rmse_pp = sqrt(mean((m[[a]] - target[[a]])^2)), max_abs_diff_pp = max(abs(m[[a]] - target[[a]])),
               gate_max_abs_diff_pp = max(abs(gg[[a]] - km)), preprog_rate = P$preprog_rate,
               dr_shape = P$dr$shape, dr_median_years = P$dr$scale)
  }))
}
CAL <- rbind(fit_row(P0, "start value"), fit_row(P1, "calibrated"))
write.csv(CAL, file.path(out_dir, "calibration.csv"), row.names = FALSE)

# RMST to 5 years (years), engine vs KM, and the between-arm difference
rmst_km <- function(d) { f <- survfit(Surv(time / 12, status) ~ 1, data = d); summary(f, rmean = 5)$table[["rmean"]] }
rmst_eng <- function(e) { tt <- seq(0, 5, by = 1 / 120); s <- survival_engine(e, "all", times = tt, params = P1)$OS; sum(diff(tt) * (head(s, -1) + tail(s, -1)) / 2) }
RM <- data.frame(arm = names(arm_of), rmst5_km = sapply(names(arm_of), function(a) rmst_km(ipd[[paste0("K24_F1A_OS_", a)]])),
                 rmst5_engine = sapply(arm_of, rmst_eng))
RM$diff <- RM$rmst5_engine - RM$rmst5_km
RM <- rbind(RM, data.frame(arm = "pembro - placebo", rmst5_km = RM$rmst5_km[1] - RM$rmst5_km[2],
                           rmst5_engine = RM$rmst5_engine[1] - RM$rmst5_engine[2],
                           diff = (RM$rmst5_engine[1] - RM$rmst5_engine[2]) - (RM$rmst5_km[1] - RM$rmst5_km[2])))
write.csv(RM, file.path(out_dir, "calibration_rmst.csv"), row.names = FALSE)
print(RM, row.names = FALSE)

# implied median survival after PreProg (entry ~ age 49.5) and after DR (excess-only and all-cause from age 50.5)
tt <- round(seq(0, 40, by = 1 / 1200), 8)
med <- function(S) tt[which(S <= 0.5)[1]]
S_pp <- exp(-P1$preprog_rate * tt) * S_pop(CFG$start_age + 0.5, tt)
S_drx <- exp(-dr_cumhaz(P1$dr, tt))
IMP <- data.frame(state = c("PreProg", "DR"),
                  median_excess_only_months = 12 * c(med(exp(-P1$preprog_rate * tt)), med(S_drx)),
                  median_all_cause_months = 12 * c(med(S_pp), med(S_drx * S_pop(CFG$start_age + 1.5, tt))),
                  surv_1y = c(S_pp[tt == 1], (S_drx * S_pop(CFG$start_age + 1.5, tt))[tt == 1]),
                  surv_2y = c(S_pp[tt == 2], (S_drx * S_pop(CFG$start_age + 1.5, tt))[tt == 2]))
write.csv(IMP, file.path(out_dir, "dr_survival_implied.csv"), row.names = FALSE)
print(IMP, row.names = FALSE)

# deaths by source at the gate times (percent of the arm)
DS <- do.call(rbind, lapply(names(arm_of), function(a) {
  e <- survival_engine(arm_of[[a]], "all", times = gate_m / 12, params = P1)
  data.frame(arm = a, month = gate_m, km_deaths = 100 * (1 - km_at(ipd[[paste0("K24_F1A_OS_", a)]], gate_m)),
             engine_deaths = 100 * e$Dead, from_event_free = 100 * e$Dead_from_EF, from_preprog = 100 * e$Dead_from_PreProg,
             from_LRR = 100 * e$Dead_from_LRR, from_DR = 100 * e$Dead_from_DR)
}))
write.csv(DS, file.path(out_dir, "calibration_deaths_by_source.csv"), row.names = FALSE)
print(DS, row.names = FALSE)

if (pass) saveRDS(P1, file.path(ROOT, "data", "fits", "engine_params.rds")) else {
  cat("gate failed: stop before step 6\n")
  if (file.exists(file.path(ROOT, "data", "fits", "engine_params.rds"))) file.remove(file.path(ROOT, "data", "fits", "engine_params.rds"))
}

# curves and checks against curves not used for calibration
m0 <- os_model(P0); m1 <- os_model(P1)
CC <- do.call(rbind, lapply(names(arm_of), function(a) data.frame(arm = a, month = g_m, km = target[[a]], before = m0[[a]], after = m1[[a]])))
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
g <- ggplot(pd, aes(month, os, colour = curve, linetype = curve)) + geom_line() + facet_wrap(~arm) +
  geom_vline(xintercept = gate_m, colour = "grey85", linewidth = 0.3) +
  scale_colour_manual(values = cols) + scale_linetype_manual(values = setNames(c("solid", "22", "solid"), names(cols))) +
  labs(x = "Months from randomization", y = "OS (%)", colour = NULL, linetype = NULL,
       title = "OS calibration; vertical lines: gate at 1-5 years") +
  theme_bw(base_size = 9) + theme(legend.position = "bottom")
ggsave(file.path(out_dir, "fig_calibration_OS.png"), g, width = 7, height = 3.8, dpi = 200)
pd <- rbind(data.frame(CH[, c("check", "arm", "month")], curve = "KM", v = CH$km),
            data.frame(CH[, c("check", "arm", "month")], curve = "engine", v = CH$engine))
g <- ggplot(pd, aes(month, v, colour = curve)) + geom_line() + geom_point(size = 0.8) + facet_grid(arm ~ check) +
  scale_colour_manual(values = c(KM = "black", engine = "#C0392B")) +
  labs(x = "Months from randomization", y = "%", colour = NULL, title = "Engine vs curves not used for calibration") +
  theme_bw(base_size = 8) + theme(legend.position = "bottom")
ggsave(file.path(out_dir, "fig_engine_checks.png"), g, width = 10, height = 4.5, dpi = 200)
