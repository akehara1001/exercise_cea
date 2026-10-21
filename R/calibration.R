# calibration.R
# Calibration shared by 05_calibrate.R and 06_bootstrap.R (structure of round 4, 2026-10-22):
# PreProg excess death Weibull (shape, scale), DR excess death log-logistic (shape, median in
# 10-12 months), both common to the arms. Objective: sum over both arms of squared differences
# (percentage points) between engine OS and the KM targets at the given months.
# Uses the cached flows of the engine (arm_flows/os_fast in engine.R), which give the same OS as
# survival_engine() in the base case (checked in R/test_engine_vectorized.R).

CAL_MEDIAN_BOUNDS <- c(10, 12) / 12
# PreProg Weibull shape in [0.01, 50] and scale in [0.01, 100] years; log-logistic shape in
# [0.01, 50]; median 10-12 months
CAL_LOWER <- c(log(0.01), log(0.01), log(0.01), CAL_MEDIAN_BOUNDS[1])
CAL_UPPER <- c(log(50), log(100), log(50), CAL_MEDIAN_BOUNDS[2])
CAL_STARTS <- list(c(log(1), log(1), log(1), 11 / 12), c(log(2), log(1.5), log(0.7), 10 / 12), c(log(4), log(1.2), log(1), 11 / 12),
                   c(log(0.5), log(0.5), log(0.5), 12 / 12), c(log(3), log(3), log(2), 10 / 12), c(log(1.5), log(0.8), log(0.7), 11 / 12))

cal_specs <- function(th) list(preprog = list(dist = "weibull", shape = exp(th[1]), scale = exp(th[2])),
                               dr = list(dist = "llogis", shape = exp(th[3]), scale = th[4]))
cal_apply <- function(P, th) { s <- cal_specs(th); P$preprog <- s$preprog; P$dr <- s$dr; P }

# flows of both arms (pembro, chemo = placebo) for parameter set P
cal_flows <- function(P) list(pembro = arm_flows(P, "pembro"), placebo = arm_flows(P, "chemo"))

# targets: list(pembro =, placebo =) in percent at `months` (whole months; cycle must be 1 month)
calibrate_os <- function(P, targets, months, starts = CAL_STARTS, fl = cal_flows(P)) {
  stopifnot(abs(P$cycle - 1 / 12) < 1e-12)
  idx <- months + 1
  obj <- function(th) {
    s <- cal_specs(th)
    sum((100 * os_fast(fl$pembro, s$preprog, s$dr)[idx] - targets$pembro)^2) +
      sum((100 * os_fast(fl$placebo, s$preprog, s$dr)[idx] - targets$placebo)^2)
  }
  opts <- lapply(starts, function(s0) optim(s0, obj, method = "L-BFGS-B", lower = CAL_LOWER, upper = CAL_UPPER,
                                            control = list(factr = 1e5, maxit = 500)))
  vals <- sapply(opts, `[[`, "value")
  best <- opts[[which.min(vals)]]
  ab <- function(j) best$par[j] <= CAL_LOWER[j] + 1e-6 || best$par[j] >= CAL_UPPER[j] - 1e-6
  list(par = best$par, value = best$value, convergence = best$convergence, starts_values = vals, optim = best,
       at_bound = c(preprog_shape = ab(1), preprog_scale = ab(2), dr_shape = ab(3), dr_median = ab(4)))
}

# 5-year RMST (years) from OS at monthly boundaries 0..60 (trapezoid)
rmst5_monthly <- function(os) { s <- os[1:61]; sum((head(s, -1) + tail(s, -1)) / 2) / 12 }

# OS anchor: k on the DR excess hazard of the pembrolizumab arm so that the engine's 5-year RMST
# difference (pembro - placebo) equals `target_diff`; NA when no k in [0.01, 100] reaches it
solve_os_anchor <- function(P, target_diff, fl = cal_flows(P)) {
  rm_pl <- rmst5_monthly(os_fast(fl$placebo, P$preprog, P$dr))
  gap <- function(lk) { dr <- P$dr; dr$k <- exp(lk); rmst5_monthly(os_fast(fl$pembro, P$preprog, dr)) - rm_pl - target_diff }
  g <- c(gap(log(0.01)), gap(log(100)))
  if (sign(g[1]) == sign(g[2])) return(NA_real_)
  exp(uniroot(gap, log(c(0.01, 100)), tol = 1e-12)$root)
}
