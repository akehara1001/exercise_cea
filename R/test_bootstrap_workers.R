# test_bootstrap_workers.R
# Two checks of the bootstrap (split 2026-10-23, user instruction; model code unchanged):
#   (i)  same platform: replicates 1-4 (phase-1 seed) run with 4 and with 8 worker processes must be
#        bit-for-bit identical (random numbers are set per replicate, bootstrap_core.R). Needs the
#        accepted engine (data/fits/engine_params.rds); skipped, with a message, when there is none.
#   (ii) other platform: each output/check/bootstrap10_<label>.rds (06c_bootstrap_check.R on
#        another machine) is compared with the reference bootstrap10_local.rds within the
#        tolerances of check B: OS and EFS <= 0.05 percentage points, 5-year RMST difference
#        <= 0.001 years. Floating-point results differ slightly between platforms (BLAS, libm,
#        compiler), so this comparison is not bit-for-bit. Only results produced from the same R/
#        and data/ trees are comparable (git tree hashes of the two commits); others are listed as
#        not comparable.
# Writes nothing to data/bootstrap/.
# Outputs: output/check/bootstrap_workers_test.csv (i), output/check/bootstrap_crossplatform_test.csv (ii)

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
source(file.path(ROOT, "R", "calibration.R"))
source(file.path(ROOT, "R", "bootstrap_core.R"))
suppressPackageStartupMessages({
  library(survival)
  library(parallel)
})
check_dir <- file.path(ROOT, "output", "check")
dir.create(check_dir, showWarnings = FALSE)
TOL_PP <- 0.05; TOL_RMST <- 0.001
ok_i <- TRUE; ok_ii <- TRUE

# ---------------------------------------------------------------- (i) same platform
if (file.exists(file.path(ROOT, "data", "fits", "engine_params.rds"))) {
  boot_load()
  mats <- function(RES) {
    mat <- function(f) do.call(rbind, lapply(RES, function(r) c(b = r$b, f(r))))
    list(efs = mat(function(r) flat(r$efs)), os_models = mat(function(r) flat(r$os_models)), pcr_preprog = mat(function(r) r$pcr),
         calibration = mat(function(r) c(attempts = r$attempts, r$calib)), outputs = mat(function(r) r$outputs),
         targets7 = mat(function(r) r$targets7))
  }
  runs <- lapply(c(w4 = 4, w8 = 8), function(w) { r <- boot_run(4, w, CFG$seed, c(5, 7, 10, 20)); cat(sprintf("%d workers: %.1f min\n", w, r$minutes)); mats(r$RES) })
  T1 <- do.call(rbind, lapply(names(runs$w4), function(m)
    data.frame(matrix = m, n_values = length(runs$w4[[m]]), w4_vs_w8_identical = identical(runs$w4[[m]], runs$w8[[m]]),
               w4_vs_w8_max_abs_diff = max(abs(runs$w4[[m]] - runs$w8[[m]])))))
  ok_i <- all(T1$w4_vs_w8_identical)
} else {
  T1 <- data.frame(matrix = NA, n_values = NA, w4_vs_w8_identical = NA, w4_vs_w8_max_abs_diff = NA,
                   note = "skipped: no accepted engine (data/fits/engine_params.rds)")
  cat("(i) skipped: no accepted engine (data/fits/engine_params.rds)\n")
}
write.csv(T1, file.path(check_dir, "bootstrap_workers_test.csv"), row.names = FALSE)
print(T1, row.names = FALSE)

# ---------------------------------------------------------------- (ii) other platform
git <- function(...) {
  owd <- setwd(ROOT); on.exit(setwd(owd))
  out <- tryCatch(suppressWarnings(system2("git", c(...), stdout = TRUE, stderr = FALSE)), error = function(e) character(0))
  if (length(out) == 1 && is.null(attr(out, "status"))) out else NA_character_
}
trees <- function(commit) c(R = git("rev-parse", paste0(commit, ":R")), data = git("rev-parse", paste0(commit, ":data")))
ref_file <- file.path(check_dir, "bootstrap10_local.rds")
others <- setdiff(list.files(check_dir, pattern = "^bootstrap10_.*\\.rds$"), "bootstrap10_local.rds")
T2 <- NULL
if (file.exists(ref_file) && length(others)) {
  L0 <- readRDS(ref_file); t0 <- trees(L0$meta$commit)
  for (f in others) {
    L1 <- readRDS(file.path(check_dir, f)); t1 <- trees(L1$meta$commit)
    comparable <- !anyNA(c(t0, t1)) && identical(t0, t1)
    o0 <- L0$outputs; o1 <- L1$outputs
    same_rows <- identical(o0[, c("b", "arm", "endpoint", "year")], o1[, c("b", "arm", "endpoint", "year")])
    d_os <- if (same_rows) max(abs(o0$value - o1$value)[o0$endpoint == "OS"]) else NA
    d_efs <- if (same_rows) max(abs(o0$value - o1$value)[o0$endpoint == "EFS"]) else NA
    d_rmst <- if (identical(L0$rmst5_diff$b, L1$rmst5_diff$b)) max(abs(L0$rmst5_diff$engine_rmst5_diff - L1$rmst5_diff$engine_rmst5_diff)) else NA
    pass <- if (comparable) isTRUE(d_os <= TOL_PP) && isTRUE(d_efs <= TOL_PP) && isTRUE(d_rmst <= TOL_RMST) else NA
    T2 <- rbind(T2, data.frame(file = f, platform = L1$meta$platform, commit = substr(L1$meta$commit, 1, 7),
                               reference_platform = L0$meta$platform, reference_commit = substr(L0$meta$commit, 1, 7),
                               comparable = comparable, max_abs_diff_OS_pp = d_os, max_abs_diff_EFS_pp = d_efs,
                               max_abs_diff_rmst5_years = d_rmst, tol_pp = TOL_PP, tol_rmst_years = TOL_RMST, pass = pass,
                               note = if (comparable) "" else "R/ or data/ differ between the two commits (or a commit is unknown here): not comparable"))
  }
  ok_ii <- all(T2$pass[T2$comparable] %in% TRUE)
} else {
  T2 <- data.frame(file = NA, note = "no other-platform result in output/check/")
}
write.csv(T2, file.path(check_dir, "bootstrap_crossplatform_test.csv"), row.names = FALSE)
print(T2, row.names = FALSE)
stopifnot(ok_i, ok_ii)
cat("bootstrap tests passed (", if (is.na(T1$w4_vs_w8_identical[1])) "(i) skipped" else "(i) identical", "; (ii)",
    if (is.null(T2$comparable)) "nothing to compare" else sprintf("%d comparable, %d not comparable", sum(T2$comparable %in% TRUE), sum(T2$comparable %in% FALSE)), ")\n")
