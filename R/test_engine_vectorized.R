# test_engine_vectorized.R
# The closed-form run_branch in engine.R must reproduce a plain cycle-by-cycle recursion of the
# same model (states EF, PreProg, LRR, DR tunnels, Dead).
source("C:/Users/原明美/Documents/ClaudeCode/exercise_cea/R/config.R")
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
suppressPackageStartupMessages(library(survival))

run_branch_loop <- function(efs_spec, pre_surv, q_pre, shares, lrr_dr_rate, dr, preprog_rate,
                            start_age, L, cycle, n_cycles, n_tunnel, hr = NULL, drug_hr = 1) {
  K <- n_cycles; J <- n_tunnel
  t <- (0:K) * cycle
  hb <- H_pop(start_age + t[-(K + 1)], cycle)
  tau0 <- pmax(t[-(K + 1)] - L, 0); tau1 <- pmax(t[-1] - L, 0)
  post <- t[-(K + 1)] >= L - 1e-9
  S0 <- spec_surv(efs_spec, tau0); S1 <- spec_surv(efs_spec, tau1)
  dH <- -log(pmax(S1, 1e-300)) + log(pmax(S0, 1e-300))
  dHex <- if (efs_spec$family == "cure") dH else pmax(dH - hb, 0)
  dHex[!post] <- 0
  dHex <- dHex * drug_hr
  km <- function(x) approx(pre_surv$time, pre_surv$surv, xout = pmin(x, L) + 1e-9, method = "constant", f = 0, rule = 2)$y
  drop_L <- 1 - km(L)
  Spre <- function(x) 1 - q_pre * (if (drop_L > 0) (1 - km(x)) / drop_L else as.numeric(x >= L))
  dHpre <- ifelse(!post, -log(pmax(Spre(t[-1]), 1e-300) / pmax(Spre(t[-(K + 1)]), 1e-300)), 0)
  hrv <- if (is.null(hr)) rep(1, K) else hr((t[-(K + 1)] + t[-1]) / 2)
  dHL <- shares[["LRR"]] * dHex * hrv; dHD <- shares[["DR"]] * dHex * hrv; dHX <- shares[["death"]] * dHex
  dHdr <- diff(dr_cumhaz(dr, (0:(J + 1)) * cycle)); dHdr[J + 1] <- dHdr[J]
  out <- matrix(0, K + 1, 5, dimnames = list(NULL, c("EF", "PreProg", "LRR", "DR", "Dead")))
  ef <- 1; pp <- 0; lr <- 0; drv <- numeric(J + 1); de <- 0
  out[1, ] <- c(1, 0, 0, 0, 0)
  for (k in 1:K) {
    Ht <- hb[k] + dHL[k] + dHD[k] + dHX[k] + dHpre[k]; pe <- 1 - exp(-Ht)
    to_L <- ef * pe * dHL[k] / Ht; to_D <- ef * pe * dHD[k] / Ht; to_P <- ef * pe * dHpre[k] / Ht; to_X <- ef * pe * (hb[k] + dHX[k]) / Ht
    Hl <- hb[k] + lrr_dr_rate * cycle; pl <- 1 - exp(-Hl)
    l_to_D <- lr * pl * lrr_dr_rate * cycle / Hl; l_to_X <- lr * pl * hb[k] / Hl
    Hp <- hb[k] + preprog_rate * cycle; p_to_X <- pp * (1 - exp(-Hp))
    surv_d <- drv * exp(-(hb[k] + dHdr)); d_to_X <- sum(drv) - sum(surv_d)
    nd <- numeric(J + 1); nd[2:(J + 1)] <- surv_d[1:J]; nd[J + 1] <- nd[J + 1] + surv_d[J + 1]; nd[1] <- to_D + l_to_D
    ef <- ef - to_L - to_D - to_P - to_X; pp <- pp + to_P - p_to_X; lr <- lr + to_L - l_to_D - l_to_X; drv <- nd
    de <- de + to_X + l_to_X + p_to_X + d_to_X
    out[k + 1, ] <- c(ef, pp, lr, sum(drv), de)
  }
  data.frame(time = t, out)
}

P <- engine_params()
hrf <- function(t) ifelse(t <= 1, 0.7, 1 - 0.3 * exp(-0.5 * (t - 1)))
cases <- expand.grid(arm = c("pembro", "placebo"), branch = c("pCR", "nonpCR"), dist = c("llogis", "weibull"),
                     shape = c(0.35, 1, 2.5), scale = c(0.3, 0.9, 3), pp = c(0.2, 2), use_hr = c(FALSE, TRUE), drug_hr = c(1, 0.6),
                     stringsAsFactors = FALSE)
worst <- 0; worst_src <- 0
for (i in seq_len(nrow(cases))) {
  cs <- cases[i, ]
  args <- list(P$efs[[cs$arm]][[cs$branch]], P$pre_surv[[cs$arm]][[cs$branch]], P$q_pre[[cs$arm]][[cs$branch]], P$shares[[cs$arm]],
               P$lrr_dr[["rate"]], list(dist = cs$dist, shape = cs$shape, scale = cs$scale), cs$pp, P$start_age, P$L, P$cycle,
               P$n_cycles, P$n_tunnel, if (cs$use_hr) hrf else NULL, cs$drug_hr)
  a <- do.call(run_branch, args); b <- do.call(run_branch_loop, args)
  cols <- c("EF", "PreProg", "LRR", "DR", "Dead")
  worst <- max(worst, max(abs(as.matrix(a[, cols]) - as.matrix(b[, cols]))))
  worst_src <- max(worst_src, max(abs(a$Dead - (a$Dead_from_EF + a$Dead_from_LRR + a$Dead_from_PreProg + a$Dead_from_DR))), min(a$Dead_from_DR) < -1e-12)
}
cat(sprintf("cases %d, max abs difference closed form vs loop: %.3e; death sources add up within %.3e\n", nrow(cases), worst, worst_src))
stopifnot(worst < 1e-10, worst_src < 1e-10)
P$dr <- list(dist = "llogis", shape = 2, scale = 0.9); P$preprog_rate <- 1
tm <- system.time(for (i in 1:20) survival_engine("chemo", "all", times = (1:78) / 12, params = P))
cat(sprintf("survival_engine: %.1f ms per call\n", 1000 * tm[["elapsed"]] / 20))
