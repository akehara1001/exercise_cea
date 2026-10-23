# test_bootstrap_workers.R
# The bootstrap results must not depend on the number of worker processes: replicates 1-4 with the
# phase-1 seed are run with 4 and with 8 workers and must be identical; they must also equal
# replicates 1-4 of the phase-1 bootstrap (data/bootstrap/boot_replicates.rds), which checks that
# moving the replicate code to bootstrap_core.R changed nothing. Writes nothing to data/bootstrap/.
# Output: output/check/bootstrap_workers_test.csv

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
source(file.path(ROOT, "R", "calibration.R"))
source(file.path(ROOT, "R", "bootstrap_core.R"))
suppressPackageStartupMessages({
  library(survival)
  library(parallel)
})
boot_load()
BRS <- readRDS(file.path(ROOT, "data", "bootstrap", "boot_replicates.rds"))
mats <- function(RES) {
  mat <- function(f) do.call(rbind, lapply(RES, function(r) c(b = r$b, f(r))))
  list(efs = mat(function(r) flat(r$efs)), os_models = mat(function(r) flat(r$os_models)), pcr_preprog = mat(function(r) r$pcr),
       calibration = mat(function(r) c(attempts = r$attempts, r$calib)), outputs = mat(function(r) r$outputs),
       targets7 = mat(function(r) r$targets7))
}
runs <- lapply(c(w4 = 4, w8 = 8), function(w) { r <- boot_run(4, w, CFG$seed, c(5, 7, 10, 20)); cat(sprintf("%d workers: %.1f min\n", w, r$minutes)); mats(r$RES) })
cmp <- function(a, b) c(identical = identical(a, b), max_abs_diff = max(abs(a - b)))
T <- do.call(rbind, lapply(names(runs$w4), function(m) {
  ref <- BRS[[m]][BRS[[m]][, "b"] %in% 1:4, , drop = FALSE]
  data.frame(matrix = m, n_values = length(runs$w4[[m]]),
             w4_vs_w8_identical = identical(runs$w4[[m]], runs$w8[[m]]), w4_vs_w8_max_abs_diff = max(abs(runs$w4[[m]] - runs$w8[[m]])),
             w4_vs_phase1_identical = identical(unname(runs$w4[[m]]), unname(ref)) && identical(colnames(runs$w4[[m]]), colnames(ref)),
             w4_vs_phase1_max_abs_diff = max(abs(runs$w4[[m]] - ref)))
}))
dir.create(file.path(ROOT, "output", "check"), showWarnings = FALSE)
write.csv(T, file.path(ROOT, "output", "check", "bootstrap_workers_test.csv"), row.names = FALSE)
print(T, row.names = FALSE)
stopifnot(all(T$w4_vs_w8_identical), all(T$w4_vs_phase1_identical))
cat("bootstrap worker test passed\n")
