# test_engine_vectorized.R
# The closed-form run_branch in engine.R must reproduce the original cycle-by-cycle recursion.
source("C:/Users/原明美/Documents/ClaudeCode/exercise_cea/R/config.R")
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
suppressPackageStartupMessages(library(survival))

# original recursion (engine.R up to 2026-10-21)
run_branch_loop <- function(efs_spec, pre_surv, shares, lrr_dr_rate, dr_shape, dr_scale,
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
  pre <- !post
  sp <- function(x) approx(pre_surv$time, pre_surv$surv, xout = pmin(x, L) + 1e-9, method = "constant", f = 0, rule = 2)$y
  dHpre <- ifelse(pre, -log(pmax(sp(t[-1]), 1e-300) / pmax(sp(t[-(K + 1)]), 1e-300)), 0)
  hrv <- if (is.null(hr)) rep(1, K) else hr((t[-(K + 1)] + t[-1]) / 2)
  dHL <- shares[["LRR"]] * dHex * hrv
  dHD <- shares[["DR"]] * dHex * hrv + dHpre
  dHX <- shares[["death"]] * dHex
  jj <- 0:J
  dHdr <- ((jj + 1) * cycle / dr_scale)^dr_shape - (jj * cycle / dr_scale)^dr_shape
  dHdr[J + 1] <- dHdr[J]
  EF <- numeric(K + 1); LR <- numeric(K + 1); DRs <- numeric(K + 1); DE <- numeric(K + 1)
  ef <- 1; lr <- 0; dr <- numeric(J + 1); de <- 0
  EF[1] <- 1
  pLD_H <- lrr_dr_rate * cycle
  for (k in 1:K) {
    Ht <- hb[k] + dHL[k] + dHD[k] + dHX[k]
    pe <- 1 - exp(-Ht)
    to_L <- ef * pe * dHL[k] / Ht; to_D <- ef * pe * dHD[k] / Ht; to_X <- ef * pe * (hb[k] + dHX[k]) / Ht
    Hl <- hb[k] + pLD_H; pl <- 1 - exp(-Hl)
    l_to_D <- lr * pl * pLD_H / Hl; l_to_X <- lr * pl * hb[k] / Hl
    Hd <- hb[k] + dHdr
    surv_d <- dr * exp(-Hd)
    d_to_X <- sum(dr) - sum(surv_d)
    new_dr <- numeric(J + 1)
    new_dr[2:(J + 1)] <- surv_d[1:J]
    new_dr[J + 1] <- new_dr[J + 1] + surv_d[J + 1]
    new_dr[1] <- to_D + l_to_D
    ef <- ef - to_L - to_D - to_X
    lr <- lr + to_L - l_to_D - l_to_X
    dr <- new_dr
    de <- de + to_X + l_to_X + d_to_X
    EF[k + 1] <- ef; LR[k + 1] <- lr; DRs[k + 1] <- sum(dr); DE[k + 1] <- de
  }
  data.frame(time = t, EF = EF, LRR = LR, DR = DRs, Dead = DE)
}

P <- engine_params(dr_shape = 1, dr_scale = 1)
hrf <- function(t) ifelse(t <= 1, 0.7, 1 - 0.3 * exp(-0.5 * (t - 1)))
cases <- expand.grid(arm = c("pembro", "placebo"), branch = c("pCR", "nonpCR"), shape = c(0.07, 0.35, 1, 2.5),
                     scale = c(0.01, 1, 3), use_hr = c(FALSE, TRUE), drug_hr = c(1, 0.6), stringsAsFactors = FALSE)
worst <- 0
for (i in seq_len(nrow(cases))) {
  cs <- cases[i, ]
  args <- list(P$efs[[cs$arm]][[cs$branch]], P$pre_surv[[cs$arm]][[cs$branch]], P$shares[[cs$arm]], P$lrr_dr[["rate"]],
               cs$shape, cs$scale, P$start_age, P$L, P$cycle, P$n_cycles, P$n_tunnel, if (cs$use_hr) hrf else NULL, cs$drug_hr)
  a <- do.call(run_branch, args); b <- do.call(run_branch_loop, args)
  worst <- max(worst, max(abs(as.matrix(a[, -1]) - as.matrix(b[, -1]))))
}
cat(sprintf("cases %d, max abs difference closed form vs loop: %.3e\n", nrow(cases), worst))
stopifnot(worst < 1e-10)
tm <- system.time(for (i in 1:20) survival_engine("chemo", "all", times = (1:78) / 12, params = P))
cat(sprintf("survival_engine: %.1f ms per call\n", 1000 * tm[["elapsed"]] / 20))
