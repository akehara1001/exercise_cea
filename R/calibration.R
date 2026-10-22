# calibration.R
# Calibration shared by 05_calibrate.R and 06_bootstrap.R (structure of round 6, 2026-10-22):
#   - DR excess death: log-logistic, common shape and median; median an external input (base
#     10.1 months, ESME, PMID 37385070; drawn per bootstrap replicate from dr_median_draw());
#     shape calibrated. In the pembrolizumab arms the DR excess hazard is multiplied by k,
#     calibrated with the other parameters within CFG$pembro_dr_k_bounds (0.25 to 4).
#   - PreProg excess death: log-logistic in time since entry, common to the arms; shape (> 1
#     allowed) and median calibrated under external constraints: median 10-26 months (ESME
#     10.1 rounded; Elmore et al., Ann Surg Oncol 2021, PMID 34247335, median OS 26 months) and
#     all-cause survival 5 years after entry (from age 49.5) >= 5% (same paper, 23.4% alive
#     without disease at a median follow-up of 71 months, taken conservatively). The second
#     constraint caps the shape at a value that depends on the median, so the shape is
#     parametrised as u x cap(median) with u in (0, 1]; u = 1 means the 5-year constraint binds.
# Objective: sum over both arms of squared differences (percentage points) between engine OS and
# the KM targets at the given months. Uses the cached flows of the engine (arm_flows/os_fast in
# engine.R), which give the same OS as survival_engine() in the base case.

# DR median sources, read from the source texts: ESME from the saved PubMed abstract, IMpassion132
# from the full text (data/reported_values.csv, fact IMP132_os, p.6)
.esme_txt <- gsub("[\\s\\x{00A0}]+", " ", perl = TRUE,
                  paste(readLines(file.path(ROOT, "input", "params", "pubmed", "PMID37385070.txt"), encoding = "UTF-8", warn = FALSE), collapse = " "))
.esme <- as.numeric(regmatches(.esme_txt, regexec("Median OS was ([\\d.]+) months \\(95% CI ([\\d.]+)-([\\d.]+)\\) in patients with early relapse",
                                                  .esme_txt, perl = TRUE))[[1]][2:4])
.rv <- read.csv(file.path(ROOT, "data", "reported_values.csv"), stringsAsFactors = FALSE)
.rvv <- function(id, key) as.numeric(.rv$value[.rv$fact_id == id & .rv$key == key])
DR_MEDIAN_SOURCES <- data.frame(
  source = c("ESME early relapse (Grinda 2023, PMID 37385070, abstract)", "IMpassion132 placebo, PD-L1-positive (Dent 2024, PMID 38755096, p.6)"),
  median = c(.esme[1], .rvv("IMP132_os", "median_placebo")), lo = c(.esme[2], .rvv("IMP132_os", "lo_placebo")),
  hi = c(.esme[3], .rvv("IMP132_os", "hi_placebo")), weight = c(0.5, 0.5))
DR_MEDIAN_BASE <- DR_MEDIAN_SOURCES$median[1] / 12

PP_MEDIAN_BOUNDS <- c(10, 26) / 12
PP_S5_MIN <- 0.05
PP_ENTRY_AGE <- CFG$start_age + 0.5
pp_shape_cap <- function(median) {
  sx <- PP_S5_MIN / S_pop(PP_ENTRY_AGE, 5)               # excess survival needed at 5 years
  log(1 / sx - 1) / log(5 / median)
}
# parameters: th = (PreProg median in years, u, log DR shape, log k)
CAL_LOWER <- c(PP_MEDIAN_BOUNDS[1], 1e-3, log(0.01), log(CFG$pembro_dr_k_bounds[1]))
CAL_UPPER <- c(PP_MEDIAN_BOUNDS[2], 1, log(50), log(CFG$pembro_dr_k_bounds[2]))
CAL_STARTS <- list(c(11 / 12, 0.5, log(1), log(1)), c(18 / 12, 0.9, log(0.7), log(1.5)), c(12 / 12, 0.99, log(0.5), log(2)),
                   c(24 / 12, 0.3, log(1.5), log(0.8)), c(14 / 12, 0.7, log(2), log(3)), c(10.5 / 12, 0.95, log(0.8), log(1.2)))

cal_specs <- function(th, dr_median) list(
  preprog = list(dist = "llogis", shape = th[2] * pp_shape_cap(th[1]), scale = th[1]),
  dr = list(dist = "llogis", shape = exp(th[3]), scale = dr_median),
  k = exp(th[4]))
cal_apply <- function(P, th, dr_median) {
  s <- cal_specs(th, dr_median); P$preprog <- s$preprog; P$dr <- s$dr; P$pembro_dr_k <- s$k; P
}

# flows of both arms (pembro, chemo = placebo) for parameter set P
cal_flows <- function(P) list(pembro = arm_flows(P, "pembro"), placebo = arm_flows(P, "chemo"))
# OS of both arms at cycle boundaries; common_dr = TRUE is the scenario k = 1
cal_os <- function(fl, s, common_dr = FALSE) {
  drp <- s$dr; if (!common_dr) drp$k <- s$k
  list(pembro = os_fast(fl$pembro, s$preprog, drp), placebo = os_fast(fl$placebo, s$preprog, s$dr))
}

# boundary flags of a solution: constraint 1 (median at 10 or 26 months), constraint 2 (5-year
# survival at 5%), and the numerical bounds of u, the DR shape and k
cal_at_bound <- function(th) c(pp_median_low = th[1] <= CAL_LOWER[1] + 1e-6, pp_median_high = th[1] >= CAL_UPPER[1] - 1e-6,
                               pp_s5_at_min = th[2] >= 1 - 1e-6, pp_u_low = th[2] <= CAL_LOWER[2] + 1e-9,
                               dr_shape_bound = th[3] <= CAL_LOWER[3] + 1e-6 || th[3] >= CAL_UPPER[3] - 1e-6,
                               k_low = th[4] <= CAL_LOWER[4] + 1e-6, k_high = th[4] >= CAL_UPPER[4] - 1e-6)

# targets: list(pembro =, placebo =) in percent at `months` (whole months; cycle must be 1 month).
# If the best start ends with optim code 52 (L-BFGS-B line-search failure), five random starts are
# run and the best of all is kept; the before/after values are returned.
calibrate_os <- function(P, targets, months, dr_median, starts = CAL_STARTS, fl = cal_flows(P), n_random = 5) {
  stopifnot(abs(P$cycle - 1 / 12) < 1e-12)
  idx <- months + 1
  obj <- function(th) {
    o <- cal_os(fl, cal_specs(th, dr_median))
    sum((100 * o$pembro[idx] - targets$pembro)^2) + sum((100 * o$placebo[idx] - targets$placebo)^2)
  }
  run <- function(st) lapply(st, function(s0) optim(s0, obj, method = "L-BFGS-B", lower = CAL_LOWER, upper = CAL_UPPER,
                                                    control = list(factr = 1e5, maxit = 500)))
  opts <- run(starts)
  vals <- sapply(opts, `[[`, "value")
  best <- opts[[which.min(vals)]]
  c52 <- c(code52 = best$convergence == 52, value_before = best$value, value_after = best$value, max_abs_par_change = 0)
  if (best$convergence == 52) {
    rs <- lapply(seq_len(n_random), function(i) runif(length(CAL_LOWER), CAL_LOWER, CAL_UPPER))
    ro <- run(rs)
    rv <- sapply(ro, `[[`, "value")
    if (min(rv) < best$value) {
      nb <- ro[[which.min(rv)]]
      c52[c("value_after", "max_abs_par_change")] <- c(nb$value, max(abs(nb$par - best$par)))
      best <- nb
    }
  }
  list(par = best$par, value = best$value, convergence = best$convergence, starts_values = vals, optim = best,
       at_bound = cal_at_bound(best$par), code52 = c52)
}

# 5-year RMST (years) from OS at monthly boundaries 0..60 (trapezoid)
rmst5_monthly <- function(os) { s <- os[1:61]; sum((head(s, -1) + tail(s, -1)) / 2) / 12 }

# DR median for the probabilistic analysis (decision 2026-10-22): equal-weight mixture of two
# lognormal distributions for the median OS after early relapse, one per study (DR_MEDIAN_SOURCES),
# each centred on the reported median with the log-scale SE from its 95% CI,
# SE = (log hi - log lo) / (2 x 1.96). The IMpassion132 CI was checked against the full text on
# 2026-10-22 (p.6).
dr_median_draw <- function(n = 1) {
  s <- DR_MEDIAN_SOURCES
  i <- sample.int(nrow(s), n, replace = TRUE, prob = s$weight)
  se <- (log(s$hi) - log(s$lo)) / (2 * qnorm(0.975))
  exp(rnorm(n, log(s$median[i]), se[i])) / 12          # years
}
