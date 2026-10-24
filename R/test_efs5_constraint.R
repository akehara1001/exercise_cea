# test_efs5_constraint.R
# constrain_efs5 (survmodels.R) is not binding for the base fits, but it is in some bootstrap
# replicates. Check it with bounds moved to force it: the constrained fit must land on the bound,
# and its likelihood must not exceed the unconstrained maximum. At 5 years (rounds 3-10) and at 7
# years (round 11, the final analysis); and the equality constraint (target) at 7 years.
source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R"))
suppressPackageStartupMessages(library(survival))
ipd <- readRDS(file.path(ROOT, "data", "ipd", "ipd_all.rds"))
fits <- readRDS(file.path(ROOT, "data", "fits", "fits.rds"))
Lm <- CFG$landmark_months; L <- Lm / 12; a0 <- CFG$start_age + L
rows <- list()
for (cv in grep("^EFS_", names(fits$selected), value = TRUE)) {
  raw <- ipd[[sub("^EFS_", "K22_S4_EFS_pCR_", cv)]]
  pre <- summary(survfit(Surv(time, status) ~ 1, data = raw), times = Lm, extend = TRUE)$surv
  d <- raw[raw$time > Lm, ]; d <- data.frame(time = (d$time - Lm) / 12, status = d$status)
  sp <- fits$selected_unconstrained[[cv]]
  ll0 <- allcause_loglik(sp, d$time, d$status, a0)
  for (at in c(5, 7)) for (shift in c(-3, 3)) {
    v <- 100 * pre * allcause_surv(sp, at - L, a0)
    lo <- if (shift > 0) v + shift else v - 10; hi <- if (shift > 0) v + 10 else v + shift
    r <- constrain_efs5(sp, d, a0, pre, L, lo, hi, at = at)
    rows[[length(rows) + 1]] <- data.frame(curve = cv, years = at, efs5_unconstrained = round(v, 3), forced_bound = round(r$bound, 3),
      efs5_constrained = round(r$efs5, 3), on_bound = abs(r$efs5 - r$bound) < 1e-6, converged = r$converged,
      loglik_drop = round(ll0 - allcause_loglik(r$spec, d$time, d$status, a0), 4))
  }
  # equality constraint (round 11 revised): fixed at a target 1 point above or below the fit at 7
  # years, inside or outside any interval; the fit must land on the target
  for (shift in c(-1, 1)) {
    v <- 100 * pre * allcause_surv(sp, 7 - L, a0)
    r <- constrain_efs5(sp, d, a0, pre, L, -Inf, Inf, at = 7, target = v + shift)
    rows[[length(rows) + 1]] <- data.frame(curve = cv, years = 7, efs5_unconstrained = round(v, 3), forced_bound = round(r$bound, 3),
      efs5_constrained = round(r$efs5, 3), on_bound = abs(r$efs5 - r$bound) < 1e-6, converged = r$converged,
      loglik_drop = round(ll0 - allcause_loglik(r$spec, d$time, d$status, a0), 4))
  }
}
R <- do.call(rbind, rows)
print(R, row.names = FALSE)
stopifnot(all(R$on_bound), all(R$converged), all(R$loglik_drop >= -1e-6))
cat("constraint test passed\n")
