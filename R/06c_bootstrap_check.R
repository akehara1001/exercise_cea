# 06c_bootstrap_check.R
# Reference results for checking other machines (2026-10-23): 10 bootstrap replicates of the
# round-8 engine (bootstrap_core.R, the same code as 06_bootstrap.R) with base seed 20261023.
# Saved per replicate: the parameters (EFS and OS model parameters, pCR and PreProg, pre-surgery
# KM, calibration incl. DR medians and k, drawn 7-year targets) and the outputs: OS and EFS at 1,
# 2, 3, 5, 7, 10 and 20 years by arm (chemo, pembro, pembro under k = 1; EFS does not depend on k)
# and the 5-year RMST difference between arms. The commit of the code, R version, platform and
# the renv.lock checksum are stored with the results.
# Usage: Rscript R/06c_bootstrap_check.R [label] [workers]
#   label "local" (default) writes output/check/bootstrap10_local.rds (the reference); any other
#   label writes bootstrap10_<label>.rds and compares it with the reference
#   (bootstrap10_compare_<label>.csv). workers default: physical cores - 1.

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
source(file.path(ROOT, "R", "calibration.R"))
source(file.path(ROOT, "R", "bootstrap_core.R"))
suppressPackageStartupMessages({
  library(survival)
  library(parallel)
})
args <- commandArgs(trailingOnly = TRUE)
label <- if (length(args) >= 1) args[1] else "local"
n_workers <- if (length(args) >= 2) as.integer(args[2]) else max(1, detectCores(logical = FALSE) - 1)
SEED <- CFG$boot_seed; B <- 10; TT <- c(1, 2, 3, 5, 7, 10, 20)       # 20261023
stopifnot(SEED == 20261023)
check_dir <- file.path(ROOT, "output", "check")
dir.create(check_dir, showWarnings = FALSE)

git <- function(...) {
  owd <- setwd(ROOT); on.exit(setwd(owd))
  tryCatch(system2("git", c(...), stdout = TRUE, stderr = FALSE), error = function(e) NA_character_)
}
commit <- git("rev-parse", "HEAD")
dirty <- git("status", "--porcelain", "--", "R", "data")

boot_load()
run <- boot_run(B, n_workers, SEED, TT)
RES <- run$RES
failed <- sapply(RES, function(r) !is.null(r$error))
stopifnot(!any(failed))
mat <- function(f) do.call(rbind, lapply(RES, function(r) c(b = r$b, f(r))))
CAL <- mat(function(r) c(attempts = r$attempts, r$calib))
OUT <- mat(function(r) r$outputs)
# outputs requested: arm-level (pcr = all) OS and EFS at the years TT
long <- do.call(rbind, lapply(seq_len(nrow(OUT)), function(i) {
  o <- OUT[i, ]
  g <- function(ep, arm) unname(o[sprintf("%s_%gy_%s_all", ep, TT, arm)])
  rbind(data.frame(b = o[["b"]], arm = "chemo", endpoint = rep(c("OS", "EFS"), each = length(TT)), year = TT,
                   value = c(g("OS", "chemo"), g("EFS", "chemo"))),
        data.frame(b = o[["b"]], arm = "pembro", endpoint = rep(c("OS", "EFS"), each = length(TT)), year = TT,
                   value = c(g("OS", "pembro"), g("EFS", "pembro"))),
        data.frame(b = o[["b"]], arm = "pembro_k1", endpoint = rep(c("OS", "EFS"), each = length(TT)), year = TT,
                   value = c(g("OS", "pembro_k1"), g("EFS", "pembro"))))
}))
REF <- list(
  meta = list(label = label, created = format(Sys.time(), "%Y-%m-%d %H:%M:%S %Z"), commit = commit,
              uncommitted_changes_in_R_or_data = dirty, seed = SEED, B = B, years = TT, workers = n_workers,
              minutes = run$minutes, R = R.version.string, platform = R.version$platform,
              renv_lock_md5 = unname(tools::md5sum(file.path(ROOT, "renv.lock"))),
              packages = sapply(c("survival", "flexsurv", "flexsurvcure", "renv"), function(p) as.character(packageVersion(p)))),
  parameters = list(efs = mat(function(r) flat(r$efs)), efs_binding = mat(function(r) unlist(r$efs_binding)),
                    os_models = mat(function(r) flat(r$os_models)), pcr_preprog = mat(function(r) r$pcr),
                    pre_surv = mat(function(r) unlist(lapply(c("pembro", "placebo"), function(a) lapply(c("pCR", "nonpCR"), function(s)
                      setNames(r$pre_surv[[a]][[s]]$surv, paste0("pre_surv_", a, "_", s, "_m", 0:Lm)))))),
                    calibration = CAL, targets7 = mat(function(r) r$targets7)),
  outputs = long,
  rmst5_diff = data.frame(b = CAL[, "b"], engine_rmst5_diff = CAL[, "engine_rmst5_diff"]),
  outputs_all = OUT)
out <- file.path(check_dir, sprintf("bootstrap10_%s.rds", label))
saveRDS(REF, out)
cat(sprintf("%s: %d replicates, %d workers, %.1f min, commit %s%s\n", out, B, n_workers, run$minutes, commit,
            if (length(dirty)) " (uncommitted changes in R/ or data/)" else ""))
print(reshape(long[long$b == 1, ], idvar = c("b", "arm", "endpoint"), timevar = "year", direction = "wide"), row.names = FALSE)

# another machine: compare with the reference
ref_file <- file.path(check_dir, "bootstrap10_local.rds")
if (label != "local" && file.exists(ref_file)) {
  L0 <- readRDS(ref_file)
  pieces <- c(L0$parameters, list(outputs_all = L0$outputs_all))
  now <- c(REF$parameters, list(outputs_all = REF$outputs_all))
  CMP <- do.call(rbind, lapply(names(pieces), function(m) {
    a <- pieces[[m]]; b <- now[[m]]
    same_shape <- identical(dim(a), dim(b)) && identical(colnames(a), colnames(b))
    data.frame(part = m, same_shape = same_shape, identical = same_shape && identical(unname(a), unname(b)),
               max_abs_diff = if (same_shape) max(abs(a - b)) else NA,
               max_rel_diff = if (same_shape) max(abs(a - b) / pmax(abs(a), 1e-12)) else NA)
  }))
  CMP <- rbind(CMP, data.frame(part = "rmst5_diff", same_shape = TRUE, identical = identical(L0$rmst5_diff, REF$rmst5_diff),
                               max_abs_diff = max(abs(L0$rmst5_diff$engine_rmst5_diff - REF$rmst5_diff$engine_rmst5_diff)),
                               max_rel_diff = NA))
  write.csv(CMP, file.path(check_dir, sprintf("bootstrap10_compare_%s.csv", label)), row.names = FALSE)
  cat(sprintf("compared with the reference (commit %s, %s):\n", L0$meta$commit, L0$meta$platform)); print(CMP, row.names = FALSE)
}
