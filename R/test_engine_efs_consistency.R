# test_engine_efs_consistency.R
# Round 12 (docs/acceptance_rule_round12.md): the engine splits the fitted EFS into event types and
# times and must not change the EFS itself. Check (implementation correctness, not a statistical
# gate): for the four cells (arm x pCR status) and both arms overall, engine EFS minus the step-4
# fitted curve at years 1, 2, 3, 5, 7 and 10 is within 0.05 points. Fitted curve of a cell: KM of
# the branch at surgery x the selected post-surgery EFS model (all-cause); overall: the two cells
# weighted by the pCR proportion of the parameters. Also (moved, not dropped): PreProg entries of a
# branch equal q_pre; AE deaths are reported next to the treatment-period probability.
# Settings: every parameter file found among data/fits/engine_params.rds (engine default),
# data/fits/round11/equality/calibration_candidates.rds (round 11, 7 years, equality) and
# data/fits/round10/engine_params.rds (round 10, kept when round 11 is adopted).
# Output: output/phase1/engine_efs_consistency_test.csv

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R")); source(file.path(ROOT, "R", "engine.R"))
files <- c(engine_default = file.path(ROOT, "data", "fits", "engine_params.rds"),
           round11_equality = file.path(ROOT, "data", "fits", "round11", "equality", "calibration_candidates.rds"),
           round10 = file.path(ROOT, "data", "fits", "round10", "engine_params.rds"))
files <- files[file.exists(files)]
stopifnot(length(files) > 0)
YRS <- c(1, 2, 3, 5, 7, 10); TOL <- 0.05
arm_of <- c(pembro = "pembro", placebo = "chemo")
rows <- list()
for (lab in names(files)) {
  x <- readRDS(files[[lab]]); P <- if (!is.null(x$params)) x$params else x
  a0 <- P$start_age + P$L
  fit_cell <- function(a, b) {
    ps <- P$pre_surv[[a]][[b]]
    km_L <- approx(ps$time, ps$surv, xout = P$L + 1e-9, method = "constant", f = 0, rule = 2)$y
    100 * km_L * allcause_surv(P$efs[[a]][[b]], YRS - P$L, a0)
  }
  for (a in names(arm_of)) {
    for (b in c("pCR", "nonpCR", "all")) {
      fit <- if (b == "all") P$p_pcr[[a]] * fit_cell(a, "pCR") + (1 - P$p_pcr[[a]]) * fit_cell(a, "nonpCR") else fit_cell(a, b)
      e <- survival_engine(arm_of[[a]], b, times = YRS, params = P)
      rows[[length(rows) + 1]] <- data.frame(setting = lab, arm = a, stratum = b, year = YRS, fit = fit, engine = 100 * e$EFS,
                                             diff = 100 * e$EFS - fit, pass = abs(100 * e$EFS - fit) <= TOL)
    }
    for (b in c("pCR", "nonpCR")) {                       # conservation of the moved events (lifetime run)
      r <- survival_engine(arm_of[[a]], b, params = P)
      q <- P$q_pre[[a]][[b]]
      stopifnot(abs(sum(r$In_PreProg) - q) < 1e-8)
      rows[[length(rows) + 1]] <- data.frame(setting = lab, arm = a, stratum = b, year = NA,
                                             fit = 100 * P$ae[[a]][["prob"]], engine = 100 * max(r$Dead_from_AE),
                                             diff = 100 * (max(r$Dead_from_AE) - P$ae[[a]][["prob"]]), pass = NA)
    }
  }
}
R <- do.call(rbind, rows)
R$check <- ifelse(is.na(R$year), "AE deaths over life vs treatment-period probability (report)", "EFS engine - fit (points)")
write.csv(R, file.path(ROOT, "output", "phase1", "engine_efs_consistency_test.csv"), row.names = FALSE)
E <- R[!is.na(R$year), ]
print(aggregate(abs(diff) ~ setting + arm + stratum, data = E, FUN = max), row.names = FALSE)
print(R[is.na(R$year), c("setting", "arm", "stratum", "fit", "engine", "diff")], row.names = FALSE)
if (!all(E$pass)) stop(sprintf("engine EFS differs from the fitted curve by more than %.2f points (max %.4f)", TOL, max(abs(E$diff))))
cat(sprintf("engine EFS consistency passed: %d settings, max |engine - fit| %.2e points\n", length(files), max(abs(E$diff))))
