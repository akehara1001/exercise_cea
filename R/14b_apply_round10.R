# 14b_apply_round10.R
# Round 10 (2026-10-23): apply the decision of 14_round10_decision.R (docs/acceptance_rule_round10.md,
# git e8d2134) without recalibrating.
#   Rule A: the round-9 calibration (data/fits/calibration_candidates.rds and the round-9 gate
#   tables in output/phase1/) is judged again with gate (a) by the Bonferroni 99.5% intervals only
#   (calibration.R gate_a_accept(), config.R gate_accept_use_max_outside = FALSE); (b) and (c) as
#   computed in round 9. If accepted, data/fits/engine_params.rds is restored to the round-9
#   parameters. The status under the round-9 rule is kept in
#   output/phase1/round9/calibration_status_round9_rule.csv.
#   Rule B: nothing is changed here (round 8 stays final; the round-9 code changes are removed by
#   hand from the working tree).
# Outputs: output/phase1/calibration_status.csv (round-10 judgment), data/fits/engine_params.rds

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
source(file.path(ROOT, "R", "calibration.R"))
out_dir <- file.path(ROOT, "output", "phase1")
DEC <- read.csv(file.path(out_dir, "round10", "decision.csv"), stringsAsFactors = FALSE)
if (DEC$rule != "A") stop("rule B: round 8 stays final; nothing to apply here")

keep <- file.path(out_dir, "round9", "calibration_status_round9_rule.csv")
if (!file.exists(keep)) invisible(file.copy(file.path(out_dir, "calibration_status.csv"), keep))
S9 <- read.csv(keep, stringsAsFactors = FALSE)
G <- read.csv(file.path(out_dir, "calibration_gate.csv"), stringsAsFactors = FALSE)
GR <- read.csv(file.path(out_dir, "calibration_gate_rmst.csv"), stringsAsFactors = FALSE)
G7 <- read.csv(file.path(out_dir, "calibration_final7y.csv"), stringsAsFactors = FALSE)
cand <- readRDS(file.path(ROOT, "data", "fits", "calibration_candidates.rds"))
stopifnot(identical(cand$structure, S9$structure))   # the gate tables belong to this calibration

accept_a <- gate_a_accept(G)
pass_b <- isTRUE(GR$pass); pass_c <- all(G7$inside_ci[G7$gate_c])
pass <- accept_a && pass_b && pass_c
ST <- data.frame(structure = S9$structure, gate_a_strict_pass = all(G$inside), gate_a_accepted = accept_a, gate_b_pass = pass_b,
                 gate_c_pass = pass_c, constraint_at_bound = S9$constraint_at_bound, k_at_bound = S9$k_at_bound,
                 gate_pass = pass, stop_before_step6 = !pass,
                 rule = "round 10, rule A (docs/acceptance_rule_round10.md): gate (a) by the Bonferroni 99.5% intervals only; round-9 calibration not rerun")
write.csv(ST, file.path(out_dir, "calibration_status.csv"), row.names = FALSE)
print(ST, row.names = FALSE)
if (pass) {
  saveRDS(cand$params, file.path(ROOT, "data", "fits", "engine_params.rds"))
  cat("accepted under the round-10 rule: data/fits/engine_params.rds restored to the round-9 parameters\n")
} else cat("not accepted under the round-10 rule\n")
