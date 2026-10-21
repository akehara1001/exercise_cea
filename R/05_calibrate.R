# 05_calibrate.R
# Step 5 (redone 2026-10-21): calibrate mortality after distant recurrence (DR) so that the engine
# reproduces the OS of both arms (Schmid 2024 Fig. 1A, reconstructed IPD).
# Gate: |engine OS - KM| <= 1 percentage point at 1, 2, 3, 4 and 5 years in each arm.
# Structures tried in order, stopping at the first that passes the gate:
#   (a) EFS events allocated to states by the reported event-type composition (engine.R) and a
#       constant excess hazard after DR, common to both arms (1 parameter);
#   (b) as (a) with the excess hazard after DR varying with time since DR (Weibull over the DR
#       tunnel states), common to both arms (2 parameters);
#   (c) as (b) with separate parameters for each arm (4 parameters).
# If none passes, the script stops before step 6 (stop_before_step6 = TRUE in calibration_status.csv).
# Objective for each structure: sum of squared differences (percentage points) between engine OS
# and the KM at months 1..78 (both arms). Starting value: median 1.5 years after DR (a starting
# point for the optimiser, not an estimate).
# Also reported, not calibrated: engine EFS by arm vs 2024 Fig. 2A, DRFS vs 2022 Fig. S3, OS by
# arm x pCR vs 2024 Fig. S4.
# Outputs: output/phase1/calibration.csv, calibration_gate.csv, calibration_status.csv,
#          calibration_curves.csv, dr_survival_implied.csv, engine_checks.csv,
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
gate_m <- c(12, 24, 36, 48, 60)
target <- lapply(names(arm_of), function(a) 100 * km_at(ipd[[paste0("K24_F1A_OS_", a)]], g_m))
names(target) <- names(arm_of)

P0 <- engine_params(dr_shape = 1, dr_scale = 1.5 / log(2))
# parameter vector -> engine parameter set for each structure
make_P <- function(struct, th) {
  P <- P0
  if (struct == "a") { P$dr_shape <- 1; P$dr_scale <- exp(th[1]) }
  if (struct == "b") { P$dr_shape <- exp(th[1]); P$dr_scale <- exp(th[2]) }
  if (struct == "c") {
    P$dr_shape <- NA; P$dr_scale <- NA
    P$dr_by_arm <- list(pembro = c(shape = exp(th[1]), scale = exp(th[2])), placebo = c(shape = exp(th[3]), scale = exp(th[4])))
  }
  P$dr_structure <- struct
  P
}
os_model <- function(P, months = g_m) lapply(arm_of, function(e) 100 * survival_engine(e, "all", times = months / 12, params = P)$OS)
sse <- function(P) { m <- os_model(P); sum((m$pembro - target$pembro)^2) + sum((m$placebo - target$placebo)^2) }
starts <- list(b = list(c(0, log(1.5 / log(2))), c(log(0.8), log(1.5)), c(log(1.5), log(3))),
               c = list(rep(c(0, log(1.5 / log(2))), 2), rep(c(log(0.8), log(1.5)), 2), rep(c(log(1.5), log(3)), 2)))
dr_median <- function(shape, scale) scale * log(2)^(1 / shape)
gate_of <- function(P) {
  m <- os_model(P, gate_m)
  do.call(rbind, lapply(names(arm_of), function(a) {
    km <- 100 * km_at(ipd[[paste0("K24_F1A_OS_", a)]], gate_m)
    data.frame(arm = a, month = gate_m, km = km, engine = m[[a]], diff = m[[a]] - km, pass = abs(m[[a]] - km) <= 1 + 1e-9)
  }))
}

res <- list(); gates <- list(); fitted <- list(); chosen <- NA
for (struct in c("a", "b", "c")) {
  obj <- function(th) sse(make_P(struct, th))
  if (struct == "a") {
    o <- optimize(obj, interval = c(log(0.02), log(50)), tol = 1e-9)
    th <- o$minimum; val <- o$objective; spread <- NA
  } else {
    opts <- lapply(starts[[struct]], function(s0) optim(s0, obj, method = "Nelder-Mead", control = list(reltol = 1e-10, maxit = 4000)))
    vals <- sapply(opts, `[[`, "value")
    th <- opts[[which.min(vals)]]$par; val <- min(vals); spread <- diff(range(vals))
  }
  P <- make_P(struct, th)
  fitted[[struct]] <- P
  G <- gate_of(P); G$structure <- struct
  gates[[struct]] <- G
  m <- os_model(P)
  dr <- if (struct == "c") P$dr_by_arm else list(pembro = c(shape = P$dr_shape, scale = P$dr_scale), placebo = c(shape = P$dr_shape, scale = P$dr_scale))
  for (a in names(arm_of)) res[[length(res) + 1]] <- data.frame(
    structure = struct, arm = a, n_par = length(th), SSE_both_arms = val, starts_spread = spread,
    rmse_pp = sqrt(mean((m[[a]] - target[[a]])^2)), max_abs_diff_pp = max(abs(m[[a]] - target[[a]])),
    gate_max_abs_diff_pp = max(abs(G$diff[G$arm == a])), gate_pass_arm = all(G$pass[G$arm == a]),
    dr_shape = dr[[a]][["shape"]], dr_scale = dr[[a]][["scale"]], dr_median_excess_years = dr_median(dr[[a]][["shape"]], dr[[a]][["scale"]]))
  cat(sprintf("structure (%s): SSE %.2f; gate %s; max gate diff %.3f (pembro) %.3f (placebo)\n", struct, val,
              ifelse(all(G$pass), "PASS", "FAIL"), max(abs(G$diff[G$arm == "pembro"])), max(abs(G$diff[G$arm == "placebo"]))))
  if (all(G$pass)) { chosen <- struct; break }
}
G0 <- gate_of(P0); m0 <- os_model(P0)
before <- do.call(rbind, lapply(names(arm_of), function(a) data.frame(
  structure = "start value", arm = a, n_par = NA, SSE_both_arms = sse(P0), starts_spread = NA,
  rmse_pp = sqrt(mean((m0[[a]] - target[[a]])^2)), max_abs_diff_pp = max(abs(m0[[a]] - target[[a]])),
  gate_max_abs_diff_pp = max(abs(G0$diff[G0$arm == a])), gate_pass_arm = all(G0$pass[G0$arm == a]),
  dr_shape = 1, dr_scale = P0$dr_scale, dr_median_excess_years = dr_median(1, P0$dr_scale))))
CAL <- rbind(before, do.call(rbind, res))
write.csv(CAL, file.path(out_dir, "calibration.csv"), row.names = FALSE)
write.csv(do.call(rbind, gates), file.path(out_dir, "calibration_gate.csv"), row.names = FALSE)
stop6 <- is.na(chosen)
write.csv(data.frame(chosen_structure = ifelse(stop6, "none", chosen), stop_before_step6 = stop6,
                     structures_tried = paste(names(gates), collapse = ",")),
          file.path(out_dir, "calibration_status.csv"), row.names = FALSE)
print(CAL, row.names = FALSE)
# the engine default is saved only when a structure passed; all structures tried are kept as
# candidates. If none passed, the outputs below describe the last structure tried (not adopted).
saveRDS(fitted, file.path(ROOT, "data", "fits", "calibration_candidates.rds"))
PE <- if (stop6) fitted[[length(fitted)]] else fitted[[chosen]]
if (stop6) {
  cat("no structure passed the gate: stop before step 6\n")
  if (file.exists(file.path(ROOT, "data", "fits", "engine_params.rds"))) file.remove(file.path(ROOT, "data", "fits", "engine_params.rds"))
} else saveRDS(PE, file.path(ROOT, "data", "fits", "engine_params.rds"))
lab <- if (stop6) paste0(PE$dr_structure, ", gate failed, not adopted") else chosen

# implied survival after DR (excess only, and all-cause from age 49 + 1.5 years)
drp <- if (identical(PE$dr_structure, "c")) PE$dr_by_arm else list(common = c(shape = PE$dr_shape, scale = PE$dr_scale))
tt <- round(seq(0, 30, by = 1 / 120), 6)
imp <- do.call(rbind, lapply(names(drp), function(k) {
  Sx <- exp(-(tt / drp[[k]][["scale"]])^drp[[k]][["shape"]])
  Sa <- Sx * S_pop(CFG$start_age + 1.5, tt)
  data.frame(structure = PE$dr_structure, parameter_set = k, median_excess_only_years = tt[which(Sx <= 0.5)[1]],
             median_all_cause_years = tt[which(Sa <= 0.5)[1]], surv_1y = Sa[tt == 1], surv_2y = Sa[tt == 2], surv_5y = Sa[tt == 5])
}))
write.csv(imp, file.path(out_dir, "dr_survival_implied.csv"), row.names = FALSE)
print(imp, row.names = FALSE)

m1 <- os_model(PE)
CC <- do.call(rbind, lapply(names(arm_of), function(a) data.frame(arm = a, month = g_m, km = target[[a]], before = m0[[a]], after = m1[[a]])))
write.csv(CC, file.path(out_dir, "calibration_curves.csv"), row.names = FALSE)

# checks against curves not used for calibration
chk <- list()
add_chk <- function(what, arm, d, eng_col, eng_arm, pcr, months) {
  km <- 100 * km_at(d, months)
  en <- 100 * survival_engine(eng_arm, pcr, times = months / 12, params = PE)[[eng_col]]
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

pd <- rbind(data.frame(CC[, c("arm", "month")], curve = "KM (2024 Fig. 1A)", os = CC$km),
            data.frame(CC[, c("arm", "month")], curve = "engine, start value", os = CC$before),
            data.frame(CC[, c("arm", "month")], curve = paste0("engine, calibrated (", lab, ")"), os = CC$after))
cols <- c("black", "grey60", "#C0392B"); names(cols) <- unique(pd$curve)
g <- ggplot(pd, aes(month, os, colour = curve, linetype = curve)) + geom_line() + facet_wrap(~arm) +
  geom_vline(xintercept = gate_m, colour = "grey85", linewidth = 0.3) +
  scale_colour_manual(values = cols) + scale_linetype_manual(values = setNames(c("solid", "22", "solid"), names(cols))) +
  labs(x = "Months from randomization", y = "OS (%)", colour = NULL, linetype = NULL,
       title = "OS calibration (mortality after distant recurrence); vertical lines: gate at 1-5 years") +
  theme_bw(base_size = 9) + theme(legend.position = "bottom")
ggsave(file.path(out_dir, "fig_calibration_OS.png"), g, width = 7, height = 3.8, dpi = 200)
pd <- rbind(data.frame(CH[, c("check", "arm", "month")], curve = "KM", v = CH$km),
            data.frame(CH[, c("check", "arm", "month")], curve = "engine", v = CH$engine))
g <- ggplot(pd, aes(month, v, colour = curve)) + geom_line() + geom_point(size = 0.8) + facet_grid(arm ~ check) +
  scale_colour_manual(values = c(KM = "black", engine = "#C0392B")) +
  labs(x = "Months from randomization", y = "%", colour = NULL, title = "Engine vs curves not used for calibration") +
  theme_bw(base_size = 8) + theme(legend.position = "bottom")
ggsave(file.path(out_dir, "fig_engine_checks.png"), g, width = 10, height = 4.5, dpi = 200)
