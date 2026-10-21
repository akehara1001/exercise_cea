# 05b_gate_feasibility.R
# Diagnostic only (no calibration, no change of structure): over a grid of the three calibrated
# parameters (PreProg excess rate, log-logistic shape, log-logistic median within 10-12 months),
# does any point meet gate (a) and gate (b) of 05_calibrate.R? Answers whether the failure comes
# from the objective (SSE over months 1-78) or from the structure and data settings.
# Output: output/phase1/calibration_gate_feasibility.csv (grid) and
#         calibration_gate_feasibility_summary.csv

source("C:/Users/原明美/Documents/ClaudeCode/exercise_cea/R/config.R")
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
suppressPackageStartupMessages({
  library(survival)
  library(parallel)
})
out_dir <- file.path(ROOT, "output", "phase1")
ipd <- readRDS(file.path(ROOT, "data", "ipd", "ipd_all.rds"))
arm_of <- c(pembro = "pembro", placebo = "chemo")
os_ipd <- lapply(names(arm_of), function(a) ipd[[paste0("K24_F1A_OS_", a)]]); names(os_ipd) <- names(arm_of)
gate_m <- 12 * CFG$gate_years
ci <- lapply(os_ipd, function(d) summary(survfit(Surv(time, status) ~ 1, data = d), times = gate_m, extend = TRUE))
rmst_km <- function(d) summary(survfit(Surv(time / 12, status) ~ 1, data = d), rmean = 5)$table[["rmean"]]
km_d <- rmst_km(os_ipd$pembro) - rmst_km(os_ipd$placebo)

grid <- expand.grid(preprog_rate = exp(seq(log(0.01), log(50), length.out = 25)),
                    dr_shape = exp(seq(log(0.05), log(20), length.out = 25)),
                    dr_median_months = c(10, 11, 12))
P0 <- engine_params(dr = list(dist = "llogis", shape = 1, scale = 11 / 12), preprog_rate = 1)
eval_point <- function(i) {
  P <- P0; P$preprog_rate <- grid$preprog_rate[i]
  P$dr <- list(dist = "llogis", shape = grid$dr_shape[i], scale = grid$dr_median_months[i] / 12)
  tt <- seq(0, 5, by = 1 / 120)
  r <- lapply(arm_of, function(e) survival_engine(e, "all", times = tt, params = P)$OS)
  rm <- sapply(r, function(s) sum(diff(tt) * (head(s, -1) + tail(s, -1)) / 2))
  idx <- match(round(gate_m / 12 * 120), round(tt * 120))
  viol <- sapply(names(arm_of), function(a) {
    s <- 100 * r[[a]][idx]
    max(pmax(100 * ci[[a]]$lower - s, s - 100 * ci[[a]]$upper, 0))
  })
  c(gate_a_max_outside_pp_pembro = viol[["pembro"]], gate_a_max_outside_pp_placebo = viol[["placebo"]],
    rmst_diff = rm[["pembro"]] - rm[["placebo"]])
}
cl <- makeCluster(min(10, detectCores() - 1))
clusterExport(cl, c("ROOT"))
invisible(clusterEvalQ(cl, {
  source(file.path(ROOT, "R", "config.R")); source(file.path(ROOT, "R", "survmodels.R")); source(file.path(ROOT, "R", "engine.R"))
  NULL
}))
clusterExport(cl, c("grid", "P0", "arm_of", "gate_m", "ci", "eval_point"))
res <- do.call(rbind, parLapply(cl, seq_len(nrow(grid)), eval_point))
stopCluster(cl)
FE <- cbind(grid, res)
FE$gate_a_pass <- FE$gate_a_max_outside_pp_pembro <= 1e-9 & FE$gate_a_max_outside_pp_placebo <= 1e-9
FE$rmst_rel_error <- (FE$rmst_diff - km_d) / km_d
FE$gate_b_pass <- abs(FE$rmst_rel_error) <= CFG$gate_rmst_rel_tol + 1e-12
write.csv(FE, file.path(out_dir, "calibration_gate_feasibility.csv"), row.names = FALSE)
SU <- data.frame(grid_points = nrow(FE), pass_a = sum(FE$gate_a_pass), pass_b = sum(FE$gate_b_pass),
                 pass_both = sum(FE$gate_a_pass & FE$gate_b_pass), km_rmst_diff = km_d,
                 min_engine_rmst_diff = min(FE$rmst_diff), min_engine_rmst_diff_given_a = if (any(FE$gate_a_pass)) min(FE$rmst_diff[FE$gate_a_pass]) else NA,
                 min_abs_rel_error = min(abs(FE$rmst_rel_error)),
                 min_gate_a_outside_pp = min(pmax(FE$gate_a_max_outside_pp_pembro, FE$gate_a_max_outside_pp_placebo)))

# refinement off the grid (Nelder-Mead from the 5 best grid points): smallest gate (a) excursion
# (i) without and (ii) with gate (b) imposed as a penalty
to_th <- function(pr, sh, md) c(log(pr), log(sh), qlogis(min(max((md - 10) / 2, 0.005), 0.995)))
from_th <- function(th) c(preprog_rate = exp(th[1]), dr_shape = exp(th[2]), dr_median_months = 10 + 2 * plogis(th[3]))
eval_th <- function(th) {
  v <- from_th(th)
  grid <<- data.frame(preprog_rate = v[1], dr_shape = v[2], dr_median_months = v[3])
  eval_point(1)
}
f_a <- function(th) { r <- eval_th(th); max(r[1:2]) }
f_ab <- function(th) { r <- eval_th(th); max(r[1:2]) + 100 * max(abs((r[3] - km_d) / km_d) - CFG$gate_rmst_rel_tol, 0) }
grid0 <- grid
FE$amax <- pmax(FE$gate_a_max_outside_pp_pembro, FE$gate_a_max_outside_pp_placebo)
refine <- function(f, cand, label) {
  do.call(rbind, lapply(seq_len(nrow(cand)), function(i) {
    o <- optim(to_th(cand$preprog_rate[i], cand$dr_shape[i], cand$dr_median_months[i]), f, method = "Nelder-Mead",
               control = list(maxit = 400, reltol = 1e-10))
    r <- eval_th(o$par)
    data.frame(search = label, start = i, t(from_th(o$par)), gate_a_max_outside_pp_pembro = r[[1]],
               gate_a_max_outside_pp_placebo = r[[2]], rmst_diff = r[[3]], rmst_rel_error = (r[[3]] - km_d) / km_d)
  }))
}
RF <- rbind(refine(f_a, head(FE[order(FE$amax), ], 5), "gate (a) only"),
            refine(f_ab, head(FE[FE$gate_b_pass, ][order(FE$amax[FE$gate_b_pass]), ], 5), "gate (a) with gate (b) imposed"))
grid <- grid0
RF$gate_a_pass <- pmax(RF$gate_a_max_outside_pp_pembro, RF$gate_a_max_outside_pp_placebo) <= 1e-9
RF$gate_b_pass <- abs(RF$rmst_rel_error) <= CFG$gate_rmst_rel_tol + 1e-12
write.csv(RF, file.path(out_dir, "calibration_gate_feasibility_refined.csv"), row.names = FALSE)
print(RF, row.names = FALSE)
SU$refined_pass_a <- any(RF$gate_a_pass); SU$refined_pass_both <- any(RF$gate_a_pass & RF$gate_b_pass)
SU$refined_min_gate_a_outside_pp_given_b <- min(pmax(RF$gate_a_max_outside_pp_pembro, RF$gate_a_max_outside_pp_placebo)[RF$gate_b_pass])
write.csv(SU, file.path(out_dir, "calibration_gate_feasibility_summary.csv"), row.names = FALSE)
print(SU, row.names = FALSE)

# gate (a) by time point at the best refined point of each search
PT <- do.call(rbind, lapply(unique(RF$search), function(s) {
  r <- RF[RF$search == s, ]; r <- r[which.min(pmax(r$gate_a_max_outside_pp_pembro, r$gate_a_max_outside_pp_placebo)), ]
  P <- P0; P$preprog_rate <- r$preprog_rate; P$dr <- list(dist = "llogis", shape = r$dr_shape, scale = r$dr_median_months / 12)
  do.call(rbind, lapply(names(arm_of), function(a) {
    en <- 100 * survival_engine(arm_of[[a]], "all", times = gate_m / 12, params = P)$OS
    data.frame(search = s, preprog_rate = r$preprog_rate, dr_shape = r$dr_shape, dr_median_months = r$dr_median_months,
               arm = a, month = gate_m, km = 100 * ci[[a]]$surv, ci95_lo = 100 * ci[[a]]$lower, ci95_hi = 100 * ci[[a]]$upper,
               engine = en, diff = en - 100 * ci[[a]]$surv,
               inside = en >= 100 * ci[[a]]$lower - 1e-9 & en <= 100 * ci[[a]]$upper + 1e-9, rmst_diff = r$rmst_diff)
  }))
}))
write.csv(PT, file.path(out_dir, "calibration_gate_feasibility_points.csv"), row.names = FALSE)
print(PT[, c("search", "arm", "month", "ci95_lo", "ci95_hi", "engine", "inside")], row.names = FALSE)
