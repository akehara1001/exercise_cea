# 06d_reference_bounds.R
# Boundaries in the 10 reference bootstrap replicates (user instruction 2026-10-23; reported only,
# no gate; the 1,000 replicates on Longleaf are decided by the user after seeing this): every value
# of k (pembrolizumab DR hazard multiplier, range 0.25 to 4) with the number of replicates at 0.25
# and at 4, and the PreProg log-logistic median with the number at 10 and at 26 months (the
# constraint bounds). Flags as set by cal_at_bound() in calibration.R, stored in the rds.
# Usage: Rscript R/06d_reference_bounds.R [rds] [tag]
#   rds default output/check/bootstrap10_local.rds; tag (default "local") names the outputs
#   output/check/bootstrap10_bounds_<tag>.csv (per replicate) and bootstrap10_bounds_<tag>_summary.csv

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
args <- commandArgs(trailingOnly = TRUE)
src <- if (length(args) >= 1) args[1] else file.path(ROOT, "output", "check", "bootstrap10_local.rds")
tag <- if (length(args) >= 2) args[2] else "local"
x <- readRDS(src)
C <- as.data.frame(x$parameters$calibration)
per <- data.frame(b = C$b, k = round(C$pembro_dr_k, 4), k_at_0.25 = C$k_low == 1, k_at_4 = C$k_high == 1,
                  preprog_median_months = round(12 * C$preprog_median, 2), preprog_median_at_10 = C$pp_median_low == 1,
                  preprog_median_at_26 = C$pp_median_high == 1)
stopifnot(all(abs(per$k[per$k_at_4] - CFG$pembro_dr_k_bounds[2]) < 1e-3), all(abs(per$k[per$k_at_0.25] - CFG$pembro_dr_k_bounds[1]) < 1e-3),
          all(abs(per$preprog_median_months[per$preprog_median_at_10] - 10) < 0.01), all(abs(per$preprog_median_months[per$preprog_median_at_26] - 26) < 0.01))
sm <- data.frame(tag = tag, commit = substr(x$meta$commit, 1, 7), created = x$meta$created, B = nrow(per),
                 k_values = paste(format(per$k, nsmall = 3), collapse = "; "),
                 k_at_0.25 = sum(per$k_at_0.25), k_at_4 = sum(per$k_at_4),
                 k_at_4_replicates = paste(per$b[per$k_at_4], collapse = ", "),
                 preprog_median_at_10 = sum(per$preprog_median_at_10), preprog_median_at_26 = sum(per$preprog_median_at_26))
out <- file.path(ROOT, "output", "check")
write.csv(per, file.path(out, sprintf("bootstrap10_bounds_%s.csv", tag)), row.names = FALSE)
write.csv(sm, file.path(out, sprintf("bootstrap10_bounds_%s_summary.csv", tag)), row.names = FALSE)
print(per, row.names = FALSE); print(t(sm))
