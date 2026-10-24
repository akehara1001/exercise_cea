# 15_round11_check.R
# Round 11 (docs/acceptance_rule_round11.md, committed before any round-11 computation): the
# stratified EFS constraint takes the 7-year values of the KEYNOTE-522 final analysis. After
# 04_fit_models.R (CFG$efs_constraint_years = 7; its outputs moved to output/phase1/round11/ and
# data/fits/round11/), this script applies the stop condition of the rule: in every constrained cell
# (two strata x two arms) the model 7-year EFS must be within 0.5 points of the reported value.
# Reported, not gates: total AIC; the 5-year values of the 2023-03-23 cutoff; the final-analysis
# stratified HRs next to the stratum HRs of the reconstructed IA4 data (output/phase1/validation.csv).
# Outputs (output/phase1/round11/): cells.csv, comparison_5y_2023.csv, comparison_hr.csv, status.csv

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
r11 <- file.path(ROOT, "output", "phase1", "round11")
CON <- read.csv(file.path(r11, "efs7_constraint.csv"), stringsAsFactors = FALSE)
stopifnot(nrow(CON) == 4, all(CON$constraint_years == 7))
tol_pp <- 0.5
cells <- data.frame(curve = CON$curve, model = CON$model, reported = CON$reported, ci95_lo = CON$ci95_lo, ci95_hi = CON$ci95_hi,
                    model_7y = CON$efs_after, diff = CON$diff_after, constrained = TRUE, binding = CON$binding,
                    within_0_5pp = abs(CON$diff_after) <= tol_pp, AIC = CON$AIC_after, AIC_round10 = CON$AIC_before)
write.csv(cells, file.path(r11, "cells.csv"), row.names = FALSE)

c5 <- data.frame(curve = CON$curve, model_5y = CON$efs5_after, reported_2023 = CON$efs5_later_cutoff, diff = CON$efs5_diff_later_cutoff)
write.csv(c5, file.path(r11, "comparison_5y_2023.csv"), row.names = FALSE)

FA <- read.csv(file.path(ROOT, "data", "kn522_final_7y.csv"), stringsAsFactors = FALSE)
VA <- read.csv(file.path(ROOT, "output", "phase1", "validation.csv"), stringsAsFactors = FALSE)
US <- read.csv(file.path(ROOT, "input", "user_supplied_values.csv"), stringsAsFactors = FALSE)
fa <- function(id) FA[FA$id == id, c("value", "lo", "hi", "outlet")]
ia4 <- function(st) { v <- VA$reconstructed[VA$check == "hr" & VA$unit == paste0(st, " (later cutoff, cross-analysis)")]
  stopifnot(length(v) == 1); v }
hr <- do.call(rbind, lapply(list(c("EFS", "pCR", "hr_efs_pcr"), c("EFS", "nonpCR", "hr_efs_nonpcr"),
                                 c("OS", "pCR", "hr_os_pcr"), c("OS", "nonpCR", "hr_os_nonpcr")), function(z) {
  f <- fa(z[3])
  data.frame(endpoint = z[1], stratum = z[2], final_hr = f$value, final_lo = f$lo, final_hi = f$hi, final_source = f$outlet,
             later_cutoff_hr = if (z[1] == "EFS") US$value[US$id == paste0("K522_EFS_HR_", z[2])] else NA,
             ia4_reconstructed_cox_hr = if (z[1] == "EFS") round(ia4(z[2]), 4) else NA,
             note = if (z[1] == "EFS") "IA4 (2021-03-23) reconstructed IPD, unstratified Cox; not a gate" else
               "no stratified OS curve in the model inputs; model value not computed (round 11 stopped before calibration)")
}))
hr$note[hr$endpoint == "OS" & hr$stratum == "pCR"] <- paste0(hr$note[hr$endpoint == "OS" & hr$stratum == "pCR"],
  sprintf("; OncLive prints [%s, %s]", fa("hr_os_pcr_onclive")$lo, fa("hr_os_pcr_onclive")$hi))
write.csv(hr, file.path(r11, "comparison_hr.csv"), row.names = FALSE)

pass <- all(cells$within_0_5pp[cells$constrained])
st <- data.frame(round = 11, rule = "docs/acceptance_rule_round11.md", constrained_cells = sum(cells$constrained),
                 cells_within_0_5pp = sum(cells$within_0_5pp), binding_cells = sum(cells$binding), AIC_total = sum(cells$AIC),
                 AIC_total_round10 = sum(cells$AIC_round10), constraint_check_pass = pass,
                 calibration_run = FALSE, accepted = FALSE,
                 decision = if (pass) "constraint check passed: go on to the calibration" else
                   "stop: constrained cells more than 0.5 points from the reported 7-year EFS (the interval constraint does not bind); calibration not run, round 10 stays the final state")
write.csv(st, file.path(r11, "status.csv"), row.names = FALSE)
print(cells, row.names = FALSE); print(hr[, 1:7], row.names = FALSE)
cat("round 11 constraint check:", if (pass) "PASS" else "STOP", "\n")
