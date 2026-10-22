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
# the KM targets at the given months, plus (round 7) weighted squared differences at the extra
# point targets (KEYNOTE-522 final analysis, 7 years): ((engine - target) / SE)^2, SE in
# percentage points (from the reported 95% CI, or binomial with the stratum size). The KM part is
# unchanged; it is the same as weighting each monthly point with an SE of 1 point. Uses the cached
# flows of the engine (arm_flows/os_fast in engine.R), which give the same OS as survival_engine()
# in the base case.

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
# OS by pCR branch of an arm at cycle boundaries (os_fast is their mixture)
branch_os <- function(af, preprog, dr, b) { f <- af$flows[[b]]; f$EF + f$LR + tunnel_state(f, f$to_P, preprog) + tunnel_state(f, f$to_DR, dr) }
# OS and EFS (= event-free occupancy) of both arms by pCR status (all / pCR / nonpCR), each branch
# computed once; OS_all is the same expression as os_fast()
cal_curves <- function(fl, s, common_dr = FALSE) lapply(c(pembro = "pembro", placebo = "placebo"), function(a) {
  af <- fl[[a]]; dr <- s$dr; if (a == "pembro" && !common_dr) dr$k <- s$k
  ob <- lapply(c(pCR = "pCR", nonpCR = "nonpCR"), function(b) branch_os(af, s$preprog, dr, b))
  list(OS_all = af$p_pcr * ob$pCR + (1 - af$p_pcr) * ob$nonpCR, OS_pCR = ob$pCR, OS_nonpCR = ob$nonpCR,
       EFS_all = af$p_pcr * af$flows$pCR$EF + (1 - af$p_pcr) * af$flows$nonpCR$EF, EFS_pCR = af$flows$pCR$EF, EFS_nonpCR = af$flows$nonpCR$EF)
})
# engine value (percent) at one extra target point: arm (pembro / placebo), pcr (all / pCR /
# nonpCR), endpoint (OS / EFS), month
curve_point <- function(cc, arm, pcr, endpoint, month) 100 * cc[[arm]][[paste0(endpoint, "_", pcr)]][month + 1]
point_value <- function(fl, s, arm, pcr, endpoint, month, common_dr = FALSE) curve_point(cal_curves(fl, s, common_dr), arm, pcr, endpoint, month)

# extra point targets from the KEYNOTE-522 final analysis (data/kn522_final_7y.csv): 7-year OS and
# EFS by arm (SE from the 95% CI: (hi - lo) / (2 x 1.96)) and 7-year OS by pCR status (no CI:
# binomial SE sqrt(p (1 - p) / n) with the stratum size of the latest pCR counts, IA7)
final7y_targets <- function() {
  FA <- read.csv(file.path(ROOT, "data", "kn522_final_7y.csv"), stringsAsFactors = FALSE)
  pc <- read.csv(file.path(ROOT, "data", "pcr_counts.csv"), stringsAsFactors = FALSE)
  pc <- pc[pc$source == "K24 (IA7)", ]
  g <- function(id, col = "value") as.numeric(FA[[col]][FA$id == id])
  ci_row <- function(id, arm, endpoint) data.frame(id = id, arm = arm, pcr = "all", endpoint = endpoint, month = 84, value = g(id),
                                                   se = (g(id, "hi") - g(id, "lo")) / (2 * qnorm(0.975)), n = NA, weight_basis = "95% CI")
  bin_row <- function(id, arm, pcr, n) { p <- g(id) / 100
    data.frame(id = id, arm = arm, pcr = pcr, endpoint = "OS", month = 84, value = g(id), se = 100 * sqrt(p * (1 - p) / n), n = n,
               weight_basis = "binomial, IA7 stratum size") }
  rbind(ci_row("os7_pembro", "pembro", "OS"), ci_row("os7_placebo", "placebo", "OS"),
        ci_row("efs7_pembro", "pembro", "EFS"), ci_row("efs7_placebo", "placebo", "EFS"),
        bin_row("os_pcr_pembro", "pembro", "pCR", pc$pcr_pembro), bin_row("os_pcr_placebo", "placebo", "pCR", pc$pcr_placebo),
        bin_row("os_nonpcr_pembro", "pembro", "nonpCR", pc$nonpcr_pembro), bin_row("os_nonpcr_placebo", "placebo", "nonpCR", pc$nonpcr_placebo))
}
# one draw of the extra targets for a bootstrap replicate: normal with the CI-based SE, or
# binomial with the stratum size (value in percent)
final7y_draw <- function(X) {
  X$value <- ifelse(is.na(X$n), rnorm(nrow(X), X$value, X$se), 100 * rbinom(nrow(X), ifelse(is.na(X$n), 1, X$n), X$value / 100) / ifelse(is.na(X$n), 1, X$n))
  X
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
calibrate_os <- function(P, targets, months, dr_median, starts = CAL_STARTS, fl = cal_flows(P), n_random = 5, extra = NULL) {
  stopifnot(abs(P$cycle - 1 / 12) < 1e-12)
  idx <- months + 1
  obj <- function(th) {
    s <- cal_specs(th, dr_median)
    if (is.null(extra)) {
      o <- cal_os(fl, s)
      return(sum((100 * o$pembro[idx] - targets$pembro)^2) + sum((100 * o$placebo[idx] - targets$placebo)^2))
    }
    cc <- cal_curves(fl, s)
    v <- sum((100 * cc$pembro$OS_all[idx] - targets$pembro)^2) + sum((100 * cc$placebo$OS_all[idx] - targets$placebo)^2)
    for (i in seq_len(nrow(extra)))
      v <- v + ((curve_point(cc, extra$arm[i], extra$pcr[i], extra$endpoint[i], extra$month[i]) - extra$value[i]) / extra$se[i])^2
    v
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
