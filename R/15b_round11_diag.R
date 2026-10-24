# 15b_round11_diag.R
# Diagnostics after the revised round 11 (equality constraint) stopped at gate (c); not a gate, no
# structure added, nothing adopted. Uses the round-11 calibration result (data/fits/calibration_candidates.rds
# as written by 05_calibrate.R; copied to data/fits/round11/equality/) and the gate data written by 05.
#  1. engine 7-year EFS by arm x pCR status next to the reported (constrained) values and to the 04 fit
#     (the engine handles the months before surgery with the PreProg state, not with the KM alone);
#  2. k only varied over its range (0.25 to 4), the other calibrated parameters fixed: whether
#     gates (a), (b) and (c) hold at the same time (the objective is not re-optimised).
# Outputs: output/phase1/round11/equality/diag_engine_efs7.csv, diag_k_scan.csv
# Usage: Rscript R/15b_round11_diag.R [candidates.rds] [output dir] [equality constraint csv]
#   (round 12: run on the fixed engine with output/phase1/round12/round11_setting/; the gate data are
#   read from output/phase1/, so run right after 05_calibrate.R of that setting)

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R")); source(file.path(ROOT, "R", "engine.R")); source(file.path(ROOT, "R", "calibration.R"))
args <- commandArgs(trailingOnly = TRUE)
cand <- if (length(args) >= 1) args[1] else file.path(ROOT, "data", "fits", "round11", "equality", "calibration_candidates.rds")
out <- if (length(args) >= 2) args[2] else file.path(ROOT, "output", "phase1", "round11", "equality")
P1 <- readRDS(cand)$params
CON <- read.csv(if (length(args) >= 3) args[3] else file.path(out, "..", "..", "efs7_equality_constraint.csv"), stringsAsFactors = FALSE)
arm_of <- c(pembro = "pembro", placebo = "chemo")

E <- do.call(rbind, lapply(names(arm_of), function(a) do.call(rbind, lapply(c("pCR", "nonpCR"), function(s) {
  cv <- paste0("EFS_", a, "_", s)
  data.frame(arm = a, stratum = s, reported = CON$reported[CON$curve == cv], fit_04 = CON$efs_after[CON$curve == cv],
             engine = round(100 * survival_engine(arm_of[[a]], s, times = 7, params = P1)$EFS, 3))
}))))
E$engine_minus_reported <- round(E$engine - E$reported, 3)
E <- rbind(E, do.call(rbind, lapply(names(arm_of), function(a)
  data.frame(arm = a, stratum = "all", reported = NA, fit_04 = NA, engine = round(100 * survival_engine(arm_of[[a]], "all", times = 7, params = P1)$EFS, 3),
             engine_minus_reported = NA))))
write.csv(E, file.path(out, "diag_engine_efs7.csv"), row.names = FALSE)
print(E, row.names = FALSE)

G <- read.csv(file.path(ROOT, "output", "phase1", "calibration_gate.csv"))
GR <- read.csv(file.path(ROOT, "output", "phase1", "calibration_gate_rmst.csv"))
G7 <- read.csv(file.path(ROOT, "output", "phase1", "calibration_final7y.csv")); G7 <- G7[G7$gate_c, ]
months <- 0:84
scan <- do.call(rbind, lapply(c(0.25, seq(0.5, 4, by = 0.05)), function(k) {
  P <- P1; P$pembro_dr_k <- k
  os <- lapply(arm_of, function(e) 100 * survival_engine(e, "all", times = months / 12, params = P)$OS)
  efs7 <- sapply(arm_of, function(e) 100 * survival_engine(e, "all", times = 7, params = P)$EFS)
  g <- merge(G[, c("arm", "month", "ci95_lo", "ci95_hi", "ci995_lo", "ci995_hi")],
             data.frame(arm = rep(names(os), each = 5), month = rep(c(12, 24, 36, 48, 60), 2),
                        engine = unlist(lapply(os, function(v) v[c(12, 24, 36, 48, 60) + 1]))))
  a_ok <- all(g$engine >= g$ci95_lo - 1e-9 & g$engine <= g$ci95_hi + 1e-9) || all(g$engine >= g$ci995_lo - 1e-9 & g$engine <= g$ci995_hi + 1e-9)
  rd <- rmst5_monthly(os$pembro / 100) - rmst5_monthly(os$placebo / 100)
  b_ok <- rd >= GR$km_boot_ci95_lo && rd <= GR$km_boot_ci95_hi
  v7 <- c(os7_pembro = os$pembro[85], os7_placebo = os$placebo[85], efs7_pembro = efs7[["pembro"]], efs7_placebo = efs7[["placebo"]])
  c_ok <- all(v7[G7$id] >= G7$ci95_lo - 1e-9 & v7[G7$id] <= G7$ci95_hi + 1e-9)
  data.frame(k = k, os7_pembro = round(v7[["os7_pembro"]], 3), rmst5_diff = round(rd, 4), gate_a = a_ok, gate_b = b_ok, gate_c = c_ok,
             all_three = a_ok && b_ok && c_ok)
}))
write.csv(scan, file.path(out, "diag_k_scan.csv"), row.names = FALSE)
cat(sprintf("k scan (other parameters fixed at the round-11 calibration, k there %.4f): all three gates at k in [%s]\n", P1$pembro_dr_k,
            if (any(scan$all_three)) paste(range(scan$k[scan$all_three]), collapse = ", ") else "none"))
print(scan[scan$k %in% c(0.25, 0.5, 1, round(P1$pembro_dr_k / 0.05) * 0.05, 1.5, 2, 4) | scan$all_three, ], row.names = FALSE)
