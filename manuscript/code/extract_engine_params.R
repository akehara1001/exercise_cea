# Read-only export of the phase 1 engine parameters used in Supplementary Table S1.
# Reads data/fits/engine_params.rds (round 15, the adopted structure); computes nothing.
# Writes manuscript/code/_build/engine_params_extract.csv (quantity, arm, value).
root <- "."
args <- commandArgs(trailingOnly = TRUE)
if (length(args)) root <- args[1]
p <- readRDS(file.path(root, "data", "fits", "engine_params.rds"))
row <- function(q, arm, v) data.frame(quantity = q, arm = arm, value = unname(v))
out <- rbind(
  row("start_age", "all", p$start_age),
  row("lrr_dr_rate_per_year", "all", p$lrr_dr[["rate"]]),
  row("lrr_dr_n_local_then_distant", "all", p$lrr_dr[["n_local_then_distant"]]),
  row("lrr_dr_n_local", "all", p$lrr_dr[["n_local"]]),
  row("lrr_dr_exposure_years", "all", p$lrr_dr[["exposure_years"]]),
  row("preprog_share_nonpcr", "pembro", p$q_pre$pembro[["nonpCR"]]),
  row("preprog_share_nonpcr", "placebo", p$q_pre$placebo[["nonpCR"]]),
  row("first_event_share_LRR", "pembro", p$shares$pembro[["LRR"]]),
  row("first_event_share_DR", "pembro", p$shares$pembro[["DR"]]),
  row("first_event_share_death", "pembro", p$shares$pembro[["death"]]),
  row("first_event_share_LRR", "placebo", p$shares$placebo[["LRR"]]),
  row("first_event_share_DR", "placebo", p$shares$placebo[["DR"]]),
  row("first_event_share_death", "placebo", p$shares$placebo[["death"]]),
  row("pembro_dr_k", "pembro", p$pembro_dr_k)
)
dir.create(file.path(root, "manuscript", "code", "_build"), showWarnings = FALSE)
write.csv(out, file.path(root, "manuscript", "code", "_build", "engine_params_extract.csv"), row.names = FALSE)
print(out)
