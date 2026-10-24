# 06_bootstrap.R
# Step 6: bootstrap (B = CFG$boot_B) of the survival engine, with the structure and settings of
# step 5 (round 9, 2026-10-23; run only after step 5 has been accepted: it reads
# engine_params.rds). Each replicate:
#   1. EFS by arm x pCR (2022 appendix Fig. S4, IA4): patients resampled within arm with their pCR
#      label, so the pCR proportion and the stratum sizes vary; each stratum is landmarked at
#      surgery and the selected model (same family as the base) is refitted with the 5-year
#      constraint (fixed bounds, efs5_constraint.csv); the KM before surgery is recomputed. The
#      bounds and the time come from data/fits/fits.rds (bootstrap_core.R); a fits.rds from the
#      round-11 setting (7-year values, efs7_constraint.csv) would carry its own.
#   2. PreProg entry share = reported count / resampled non-pCR size (arm-level share as reported).
#   3. OS by arm (2024 Fig. 1A, IA7): resampled within arm; the selected OS models are refitted
#      (saved only, the engine does not use them; RP knots kept at the base positions).
#   4. DR log-logistic (shape and both medians) drawn jointly: the reconstructed ESME IPD resampled
#      within each group and refitted (calibration.R esme_draw(), common or separate shape as in
#      the base); the eight 7-year points of the final analysis drawn
#      from their sampling distributions (final7y_draw: normal with the CI-based SE for OS and EFS
#      by arm, binomial with the IA7 stratum size for OS by pCR status; weights as in the base);
#      calibration as in 05_calibrate.R against the resampled OS KM and the drawn 7-year points
#      given those DR parameters (PreProg median and shape and k estimated together),
#      from the base estimates and the six starts of the base calibration (best of the seven); if
#      the best ends with optim code 52, five random starts are added and the best of all is kept
#      (before/after recorded).
#   5. Engine outputs at 5, 7, 10 and 20 years (EFS and OS by arm x pCR; pembrolizumab arm also
#      under the scenario k = 1).
# Fixed in every replicate (data settings): life table, EFS event composition and shares, deaths
# due to adverse events, LRR -> DR rate, PreProg counts, 5-year constraint bounds.
# A replicate whose fit fails is redrawn with another seed (counted in `attempts`).
# Random numbers per replicate (set.seed(CFG$seed + b)); the replicate code is in bootstrap_core.R.
# Outputs: data/bootstrap/boot_replicates.rds and boot_*.csv (parameter matrices and the drawn
#          7-year targets, one row per replicate); output/phase1/bootstrap_summary.csv

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
source(file.path(ROOT, "R", "calibration.R"))
suppressPackageStartupMessages({
  library(survival)
  library(parallel)
})
args <- commandArgs(trailingOnly = TRUE)
B <- if (length(args) >= 1) as.integer(args[1]) else CFG$boot_B
n_workers <- if (length(args) >= 2) as.integer(args[2]) else min(11, detectCores() - 1)
boot_dir <- file.path(ROOT, "data", "bootstrap")
dir.create(boot_dir, showWarnings = FALSE)

source(file.path(ROOT, "R", "bootstrap_core.R"))     # boot_load(), boot_one(), boot_run(), engine_outputs()
boot_load()
run <- boot_run(B, n_workers, CFG$seed, c(5, 7, 10, 20))
RES <- run$RES; el <- run$minutes
failed <- sapply(RES, function(r) !is.null(r$error))
cat(sprintf("B = %d, workers %d, %.1f min; failed after 10 attempts: %d\n", B, n_workers, el, sum(failed)))
R <- RES[!failed]

mat <- function(f) do.call(rbind, lapply(R, function(r) c(b = r$b, f(r))))
EFSm <- mat(function(r) flat(r$efs)); BINDm <- mat(function(r) unlist(r$efs_binding))
OSm <- mat(function(r) flat(r$os_models)); PCRm <- mat(function(r) r$pcr)
CALm <- mat(function(r) c(attempts = r$attempts, r$calib)); OUTm <- mat(function(r) r$outputs)
T7m <- mat(function(r) r$targets7)
PREm <- mat(function(r) unlist(lapply(c("pembro", "placebo"), function(a) lapply(c("pCR", "nonpCR"), function(s)
  setNames(r$pre_surv[[a]][[s]]$surv, paste0("pre_surv_", a, "_", s, "_m", 0:Lm))))))
saveRDS(list(B = B, seed = CFG$seed, minutes = el, failed = RES[failed], efs = EFSm, efs_binding = BINDm, os_models = OSm,
             pcr_preprog = PCRm, pre_surv = PREm, calibration = CALm, outputs = OUTm, targets7 = T7m),
        file.path(boot_dir, "boot_replicates.rds"))
write.csv(EFSm, file.path(boot_dir, "boot_efs_params.csv"), row.names = FALSE)
write.csv(BINDm, file.path(boot_dir, "boot_efs5_binding.csv"), row.names = FALSE)
write.csv(OSm, file.path(boot_dir, "boot_os_model_params.csv"), row.names = FALSE)
write.csv(PCRm, file.path(boot_dir, "boot_pcr_preprog.csv"), row.names = FALSE)
write.csv(PREm, file.path(boot_dir, "boot_pre_surgery_km.csv"), row.names = FALSE)
write.csv(CALm, file.path(boot_dir, "boot_calibration.csv"), row.names = FALSE)
write.csv(OUTm, file.path(boot_dir, "boot_outputs.csv"), row.names = FALSE)
write.csv(T7m, file.path(boot_dir, "boot_final7y_targets.csv"), row.names = FALSE)

# summary: base value and bootstrap percentile interval of each parameter and output
base_calib <- c(preprog_shape = P_base$preprog$shape, preprog_median = P_base$preprog$scale, dr_shape = P_base$dr$shape,
                dr_median = P_base$dr$scale, dr_late_shape = P_base$dr$late_shape, dr_late_median = P_base$dr$late_scale,
                pembro_dr_k = P_base$pembro_dr_k)
efs_cvs <- paste0("EFS_", rep(c("pembro", "placebo"), each = 2), "_", c("pCR", "nonpCR"))
base_efs <- flat(setNames(lapply(efs_cvs, function(cv) fits$selected[[cv]]$pars), efs_cvs))
base_pcr <- unlist(lapply(c("pembro", "placebo"), function(a) {
  v <- c(); for (s in c("pCR", "nonpCR")) v[paste0(c("pre7_"), "EFS_", a, "_", s)] <- tail(P_base$pre_surv[[a]][[s]]$surv, 1)
  c(v, setNames(c(P_base$p_pcr[[a]], P_base$q_pre[[a]][["nonpCR"]]), paste0(c("p_pcr_", "q_pre_"), a)))
}))
base_out <- engine_outputs(P_base)
summ <- function(m, group, base = NULL) {
  m <- m[, setdiff(colnames(m), "b"), drop = FALSE]
  data.frame(group = group, quantity = colnames(m),
             base = if (is.null(base)) NA else unname(base[colnames(m)]),
             boot_mean = colMeans(m, na.rm = TRUE), boot_median = apply(m, 2, median, na.rm = TRUE),
             boot_lo = apply(m, 2, quantile, 0.025, na.rm = TRUE), boot_hi = apply(m, 2, quantile, 0.975, na.rm = TRUE),
             n_finite = colSums(is.finite(m)), row.names = NULL)
}
SUM <- rbind(summ(EFSm, "EFS model parameters", base_efs),
             summ(CALm[, c("b", names(base_calib), "sse", "km_rmst5_diff", "engine_rmst5_diff"), drop = FALSE], "calibration", base_calib),
             summ(PCRm, "pCR and PreProg", base_pcr), summ(OUTm, "engine outputs (%)", base_out),
             summ(T7m, "7-year targets drawn (%)", setNames(X7$value, X7$id)))
write.csv(SUM, file.path(ROOT, "output", "phase1", "bootstrap_summary.csv"), row.names = FALSE)
cat(sprintf("replicates: %d; convergence != 0: %d; k at 0.25 / 4: %d / %d; PreProg median at 10 / 26 months: %d / %d; 5-year survival at 5%%: %d; code 52 rerun: %d (objective improved: %d); redrawn: %d; 5-year constraint binding: %s\n",
            nrow(CALm), sum(CALm[, "convergence"] != 0), sum(CALm[, "k_low"] == 1), sum(CALm[, "k_high"] == 1),
            sum(CALm[, "pp_median_low"] == 1), sum(CALm[, "pp_median_high"] == 1),
            sum(CALm[, "pp_s5_at_min"] == 1), sum(CALm[, "code52"] == 1), sum(CALm[, "value_after"] < CALm[, "value_before"] - 1e-8),
            sum(CALm[, "attempts"] > 1),
            paste(colnames(BINDm)[-1], colSums(BINDm[, -1, drop = FALSE]), sep = " ", collapse = ", ")))
