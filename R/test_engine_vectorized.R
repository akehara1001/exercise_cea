# test_engine_vectorized.R
# The closed-form run_branch in engine.R must reproduce a plain cycle-by-cycle recursion of the
# same model (states EF, PreProg, LRR, DR tunnels, Dead; round 8: DR split into early and late
# sub-states by the time of entry, each with its own tunnels; round 9: the late sub-state may have
# its own shape).
source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
suppressPackageStartupMessages(library(survival))

run_branch_loop <- function(efs_spec, pre_surv, q_pre, shares, lrr_dr_rate, dr, preprog,
                            start_age, L, cycle, n_cycles, n_tunnel, hr = NULL, drug_hr = 1, ae_rate = 0, ae_end = 0) {
  K <- n_cycles; J <- n_tunnel
  t <- (0:K) * cycle
  # hazards of leaving EF: shared with engine.R (round 12: the split of the fitted EFS); this test
  # checks the recursion over states and tunnels against the closed form
  h <- branch_hazards(efs_spec, pre_surv, q_pre, shares, start_age, L, cycle, K, hr, drug_hr, ae_rate, ae_end)
  hb <- h$hb; hbx <- h$hbx; dHL <- h$dHL; dHD <- h$dHD; dHX <- h$dHX; dHpre <- h$dHpre; dHA <- h$dHA
  dHdr <- diff(dr_cumhaz(dr, (0:(J + 1)) * cycle)); dHdr[J + 1] <- dHdr[J]
  split <- !is.null(dr$late_scale)
  drl_spec <- if (split) dr_late_spec(dr) else dr                  # round 13: k_late on late DR
  dHdl <- diff(dr_cumhaz(drl_spec, (0:(J + 1)) * cycle)); dHdl[J + 1] <- dHdl[J]
  dHpp <- diff(dr_cumhaz(preprog, (0:(J + 1)) * cycle)); dHpp[J + 1] <- dHpp[J]
  out <- matrix(0, K + 1, 5, dimnames = list(NULL, c("EF", "PreProg", "LRR", "DR", "Dead")))
  ef <- 1; ppv <- numeric(J + 1); lr <- 0; drv <- numeric(J + 1); drl <- numeric(J + 1); de <- 0
  shift <- function(v, entry) { n <- numeric(J + 1); n[2:(J + 1)] <- v[1:J]; n[J + 1] <- n[J + 1] + v[J + 1]; n[1] <- entry; n }
  out[1, ] <- c(1, 0, 0, 0, 0)
  for (k in 1:K) {
    Ht <- hbx[k] + dHL[k] + dHD[k] + dHX[k] + dHpre[k] + dHA[k]; pe <- 1 - exp(-Ht); r <- if (Ht > 0) pe / Ht else 0
    to_L <- ef * r * dHL[k]; to_D <- ef * r * dHD[k]; to_P <- ef * r * dHpre[k]
    to_X <- ef * r * (hbx[k] + dHX[k] + dHA[k])
    Hl <- hb[k] + lrr_dr_rate * cycle; pl <- 1 - exp(-Hl)
    l_to_D <- lr * pl * lrr_dr_rate * cycle / Hl; l_to_X <- lr * pl * hb[k] / Hl
    surv_p <- ppv * exp(-(hb[k] + dHpp)); p_to_X <- sum(ppv) - sum(surv_p)
    surv_d <- drv * exp(-(hb[k] + dHdr)); surv_l <- drl * exp(-(hb[k] + dHdl))
    d_to_X <- sum(drv) + sum(drl) - sum(surv_d) - sum(surv_l)
    ef <- ef - to_L - to_D - to_P - to_X; lr <- lr + to_L - l_to_D - l_to_X
    early <- !split || k <= dr$early_cycles               # entrants of cycle k arrive at boundary k
    ppv <- shift(surv_p, to_P)
    drv <- shift(surv_d, if (early) to_D + l_to_D else 0); drl <- shift(surv_l, if (early) 0 else to_D + l_to_D)
    de <- de + to_X + l_to_X + p_to_X + d_to_X
    out[k + 1, ] <- c(ef, sum(ppv), lr, sum(drv) + sum(drl), de)
  }
  data.frame(time = t, out)
}

P <- engine_params()
hrf <- function(t) ifelse(t <= 1, 0.7, 1 - 0.3 * exp(-0.5 * (t - 1)))
cases <- expand.grid(arm = c("pembro", "placebo"), branch = c("pCR", "nonpCR"), dist = c("llogis", "weibull"),
                     shape = c(0.35, 1, 2.5), scale = c(0.3, 0.9, 3), pp = 1:3, use_hr = c(FALSE, TRUE), drug_hr = c(1, 0.6),
                     ae = c(0, 30), split = c(FALSE, TRUE), k_scope = c("all", "early"), stringsAsFactors = FALSE)
cases <- cases[!(cases$k_scope == "early" & !cases$split), ]
pp_specs <- list(list(dist = "exp", rate = 0.2), list(dist = "weibull", shape = 0.5, scale = 0.5), list(dist = "weibull", shape = 2.5, scale = 2))
worst <- 0; worst_src <- 0
for (i in seq_len(nrow(cases))) {
  cs <- cases[i, ]
  args <- list(P$efs[[cs$arm]][[cs$branch]], P$pre_surv[[cs$arm]][[cs$branch]], P$q_pre[[cs$arm]][[cs$branch]], P$shares[[cs$arm]],
               P$lrr_dr[["rate"]], c(list(dist = cs$dist, shape = cs$shape, scale = cs$scale, k = if (cs$drug_hr == 1) 1 else 1.7),
                                     if (cs$split) list(late_scale = 1.9 * cs$scale, late_shape = 1.3 * cs$shape, early_cycles = 18) else NULL,
                                     if (cs$k_scope == "early") list(k_late = 1) else NULL),
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
P$dr <- list(dist = "llogis", shape = 2, scale = 0.9, late_scale = 1.6, early_cycles = 18); P$preprog <- list(dist = "weibull", shape = 1.5, scale = 1)
tm <- system.time(for (i in 1:20) survival_engine("chemo", "all", times = (1:78) / 12, params = P))
cat(sprintf("survival_engine: %.1f ms per call\n", 1000 * tm[["elapsed"]] / 20))

# os_fast (cached flows, used by calibration.R and the bootstrap) must equal survival_engine OS in
# the base case, with the pembrolizumab DR multiplier k and with the scenario k = 1
P$pembro_dr_k <- 1.8
worst_fast <- 0
for (scope in c("all", "early")) for (arm in c("chemo", "pembro")) for (common in c(FALSE, TRUE)) {
  P$pembro_dr_k_scope <- scope
  dr <- P$dr; if (!common && arm == "pembro") dr <- dr_with_k(dr, P$pembro_dr_k, scope)
  a <- os_fast(arm_flows(P, arm), P$preprog, dr)
  b <- survival_engine(arm, "all", params = P, common_dr = common)$OS
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

# early DR entries: In_DR_early equals In_DR up to boundary early_cycles and 0 after
de <- max(abs(rL$In_DR_early[1:19] - rL$In_DR[1:19]), abs(rL$In_DR_early[-(1:19)]))
cat(sprintf("In_DR_early checks: max deviation %.3e\n", de))
stopifnot(de < 1e-15)
