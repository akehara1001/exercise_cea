# test_engine_vectorized.R
# The closed-form run_branch in engine.R must reproduce a plain cycle-by-cycle recursion of the
# same model (states EF, PreProg, LRR, DR tunnels, Dead).
source("C:/Users/原明美/Documents/ClaudeCode/exercise_cea/R/config.R")
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
suppressPackageStartupMessages(library(survival))

run_branch_loop <- function(efs_spec, pre_surv, q_pre, shares, lrr_dr_rate, dr, preprog,
                            start_age, L, cycle, n_cycles, n_tunnel, hr = NULL, drug_hr = 1, ae_rate = 0, ae_end = 0) {
  K <- n_cycles; J <- n_tunnel
  t <- (0:K) * cycle
  hb <- H_pop(start_age + t[-(K + 1)], cycle)
  tau0 <- pmax(t[-(K + 1)] - L, 0); tau1 <- pmax(t[-1] - L, 0)
  post <- t[-(K + 1)] >= L - 1e-9
  S0 <- spec_surv(efs_spec, tau0); S1 <- spec_surv(efs_spec, tau1)
  dH <- -log(pmax(S1, 1e-300)) + log(pmax(S0, 1e-300))
  dHex <- if (efs_spec$family == "cure") dH else pmax(dH - hb, 0)
  dHex[!post] <- 0
  dHA <- numeric(K)
  for (k in 1:K) {
    if (t[k] < ae_end) dHA[k] <- ae_rate * (min(t[k + 1], ae_end) - t[k])
    if (post[k]) { dHA[k] <- min(dHA[k], dHex[k]); dHex[k] <- dHex[k] - dHA[k] }
  }
  dHex <- dHex * drug_hr
  km <- function(x) approx(pre_surv$time, pre_surv$surv, xout = pmin(x, L) + 1e-9, method = "constant", f = 0, rule = 2)$y
  drop_L <- 1 - km(L)
  Spre <- function(x) 1 - q_pre * (if (drop_L > 0) (1 - km(x)) / drop_L else as.numeric(x >= L))
  dHpre <- ifelse(!post, -log(pmax(Spre(t[-1]), 1e-300) / pmax(Spre(t[-(K + 1)]), 1e-300)), 0)
  hrv <- if (is.null(hr)) rep(1, K) else hr((t[-(K + 1)] + t[-1]) / 2)
  dHL <- shares[["LRR"]] * dHex * hrv; dHD <- shares[["DR"]] * dHex * hrv; dHX <- shares[["death"]] * dHex
  dHdr <- diff(dr_cumhaz(dr, (0:(J + 1)) * cycle)); dHdr[J + 1] <- dHdr[J]
  dHpp <- diff(dr_cumhaz(preprog, (0:(J + 1)) * cycle)); dHpp[J + 1] <- dHpp[J]
  out <- matrix(0, K + 1, 5, dimnames = list(NULL, c("EF", "PreProg", "LRR", "DR", "Dead")))
  ef <- 1; ppv <- numeric(J + 1); lr <- 0; drv <- numeric(J + 1); de <- 0
  shift <- function(v, entry) { n <- numeric(J + 1); n[2:(J + 1)] <- v[1:J]; n[J + 1] <- n[J + 1] + v[J + 1]; n[1] <- entry; n }
  out[1, ] <- c(1, 0, 0, 0, 0)
  for (k in 1:K) {
    Ht <- hb[k] + dHL[k] + dHD[k] + dHX[k] + dHpre[k] + dHA[k]; pe <- 1 - exp(-Ht)
    to_L <- ef * pe * dHL[k] / Ht; to_D <- ef * pe * dHD[k] / Ht; to_P <- ef * pe * dHpre[k] / Ht
    to_X <- ef * pe * (hb[k] + dHX[k] + dHA[k]) / Ht
    Hl <- hb[k] + lrr_dr_rate * cycle; pl <- 1 - exp(-Hl)
    l_to_D <- lr * pl * lrr_dr_rate * cycle / Hl; l_to_X <- lr * pl * hb[k] / Hl
    surv_p <- ppv * exp(-(hb[k] + dHpp)); p_to_X <- sum(ppv) - sum(surv_p)
    surv_d <- drv * exp(-(hb[k] + dHdr)); d_to_X <- sum(drv) - sum(surv_d)
    ef <- ef - to_L - to_D - to_P - to_X; lr <- lr + to_L - l_to_D - l_to_X
    ppv <- shift(surv_p, to_P); drv <- shift(surv_d, to_D + l_to_D)
    de <- de + to_X + l_to_X + p_to_X + d_to_X
    out[k + 1, ] <- c(ef, sum(ppv), lr, sum(drv), de)
  }
  data.frame(time = t, out)
}

P <- engine_params()
hrf <- function(t) ifelse(t <= 1, 0.7, 1 - 0.3 * exp(-0.5 * (t - 1)))
cases <- expand.grid(arm = c("pembro", "placebo"), branch = c("pCR", "nonpCR"), dist = c("llogis", "weibull"),
                     shape = c(0.35, 1, 2.5), scale = c(0.3, 0.9, 3), pp = 1:3, use_hr = c(FALSE, TRUE), drug_hr = c(1, 0.6),
                     ae = c(0, 30), stringsAsFactors = FALSE)
pp_specs <- list(list(dist = "exp", rate = 0.2), list(dist = "weibull", shape = 0.5, scale = 0.5), list(dist = "weibull", shape = 2.5, scale = 2))
worst <- 0; worst_src <- 0
for (i in seq_len(nrow(cases))) {
  cs <- cases[i, ]
  args <- list(P$efs[[cs$arm]][[cs$branch]], P$pre_surv[[cs$arm]][[cs$branch]], P$q_pre[[cs$arm]][[cs$branch]], P$shares[[cs$arm]],
               P$lrr_dr[["rate"]], list(dist = cs$dist, shape = cs$shape, scale = cs$scale, k = if (cs$drug_hr == 1) 1 else 1.7),
               pp_specs[[cs$pp]], P$start_age, P$L, P$cycle,
               P$n_cycles, P$n_tunnel, if (cs$use_hr) hrf else NULL, cs$drug_hr,
               cs$ae * P$ae[[cs$arm]][["rate"]], P$ae_end)
  a <- do.call(run_branch, args); b <- do.call(run_branch_loop, args)
  cols <- c("EF", "PreProg", "LRR", "DR", "Dead")
  worst <- max(worst, max(abs(as.matrix(a[, cols]) - as.matrix(b[, cols]))))
  worst_src <- max(worst_src, max(abs(a$Dead - (a$Dead_from_EF + a$Dead_from_AE + a$Dead_from_LRR + a$Dead_from_PreProg + a$Dead_from_DR))),
                   min(a$Dead_from_DR) < -1e-12, min(a$Dead_from_PreProg) < -1e-12)
}
cat(sprintf("cases %d, max abs difference closed form vs loop: %.3e; death sources add up within %.3e\n", nrow(cases), worst, worst_src))
stopifnot(worst < 1e-10, worst_src < 1e-10)
P$dr <- list(dist = "llogis", shape = 2, scale = 0.9); P$preprog <- list(dist = "weibull", shape = 1.5, scale = 1)
tm <- system.time(for (i in 1:20) survival_engine("chemo", "all", times = (1:78) / 12, params = P))
cat(sprintf("survival_engine: %.1f ms per call\n", 1000 * tm[["elapsed"]] / 20))

# os_fast (cached flows, used by calibration.R and the bootstrap) must equal survival_engine OS in
# the base case, with and without the OS anchor multiplier
P$os_anchor_k <- 1.8
worst_fast <- 0
for (arm in c("chemo", "pembro")) for (anchor in c(FALSE, TRUE)) {
  dr <- P$dr; if (anchor && arm == "pembro") dr$k <- P$os_anchor_k
  a <- os_fast(arm_flows(P, arm), P$preprog, dr)
  b <- survival_engine(arm, "all", params = P, os_anchor = anchor)$OS
  worst_fast <- max(worst_fast, max(abs(a - b)))
}
cat(sprintf("os_fast vs survival_engine: max abs difference %.3e\n", worst_fast))
stopifnot(worst_fast < 1e-12)

# DR within a number of months of entry (cost layer): between 0 and DR, equal to DR for a long limit
r0 <- survival_engine("chemo", "all", params = P, dr_first_months = 0)
r8 <- survival_engine("chemo", "all", params = P, dr_first_months = 8.5)
rL <- survival_engine("chemo", "all", params = P, dr_first_months = 12 * 60)
dev_split <- max(abs(r0$DR_first), abs(rL$DR_first - rL$DR), pmax(r8$DR_first - r8$DR, 0), pmax(-r8$DR_first, 0))
cat(sprintf("DR_first checks: max deviation %.3e\n", dev_split))
stopifnot(dev_split < 1e-12)
