# 06_bootstrap.R
# Step 6: bootstrap (B = CFG$boot_B) of the survival engine, with the structure and settings of
# step 5 (round 8, 2026-10-22; run only after step 5 has been accepted: it reads
# engine_params.rds). Each replicate:
#   1. EFS by arm x pCR (2022 appendix Fig. S4, IA4): patients resampled within arm with their pCR
#      label, so the pCR proportion and the stratum sizes vary; each stratum is landmarked at
#      surgery and the selected model (same family as the base) is refitted with the 5-year
#      constraint (fixed bounds, efs5_constraint.csv); the KM before surgery is recomputed.
#   2. PreProg entry share = reported count / resampled non-pCR size (arm-level share as reported).
#   3. OS by arm (2024 Fig. 1A, IA7): resampled within arm; the selected OS models are refitted
#      (saved only, the engine does not use them; RP knots kept at the base positions).
#   4. DR medians drawn: early from dr_median_draw() (calibration.R: equal-weight mixture of
#      lognormals from the ESME and IMpassion132 CIs), late from dr_late_median_draw() (lognormal
#      from the ESME late-relapse CI), independently; the eight 7-year points of the final analysis drawn
#      from their sampling distributions (final7y_draw: normal with the CI-based SE for OS and EFS
#      by arm, binomial with the IA7 stratum size for OS by pCR status; weights as in the base);
#      calibration as in 05_calibrate.R against the resampled OS KM and the drawn 7-year points
#      given those medians (PreProg median and shape, DR shape and k estimated together),
#      from the base estimates and the six starts of the base calibration (best of the seven); if
#      the best ends with optim code 52, five random starts are added and the best of all is kept
#      (before/after recorded).
#   5. Engine outputs at 5, 7, 10 and 20 years (EFS and OS by arm x pCR; pembrolizumab arm also
#      under the scenario k = 1).
# Fixed in every replicate (data settings): life table, EFS event composition and shares, deaths
# due to adverse events, LRR -> DR rate, PreProg counts, 5-year constraint bounds.
# A replicate whose fit fails is redrawn with another seed (counted in `attempts`).
# Outputs: data/bootstrap/boot_replicates.rds and boot_*.csv (parameter matrices and the drawn
#          7-year targets, one row per replicate); output/phase1/bootstrap_summary.csv

source("C:/Users/原明美/Documents/ClaudeCode/exercise_cea/R/config.R")
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

ipd <- readRDS(file.path(ROOT, "data", "ipd", "ipd_all.rds"))
fits <- readRDS(file.path(ROOT, "data", "fits", "fits.rds"))
SEL <- read.csv(file.path(ROOT, "output", "phase1", "model_selection.csv"), stringsAsFactors = FALSE)
P_base <- readRDS(file.path(ROOT, "data", "fits", "engine_params.rds"))     # written only when step 5 passed
cal_base <- readRDS(file.path(ROOT, "data", "fits", "calibration_candidates.rds"))
th_base <- cal_base$optim$par
X7 <- final7y_targets()
Lm <- CFG$landmark_months; L <- Lm / 12

# engine outputs at 5, 7, 10, 20 years (EFS and OS, %), by arm x pCR; pembrolizumab also under k = 1
engine_outputs <- function(P) {
  tt <- c(5, 7, 10, 20); outv <- c()
  for (arm in c("chemo", "pembro")) for (pc in c("all", "pCR", "nonpCR")) {
    e <- survival_engine(arm, pc, times = tt, params = P)
    outv[paste0(c("EFS", "OS"), "_", rep(tt, each = 2), "y_", arm, "_", pc)] <- c(rbind(100 * e$EFS, 100 * e$OS))
  }
  for (pc in c("all", "pCR", "nonpCR")) {
    outv[paste0("OS_", tt, "y_pembro_k1_", pc)] <- 100 * survival_engine("pembro", pc, times = tt, params = P, common_dr = TRUE)$OS
  }
  outv
}
flat <- function(l) unlist(lapply(names(l), function(n) setNames(l[[n]], paste0(n, "_", names(l[[n]])))))

boot_one <- function(b) {
  km_at <- function(d, tm) summary(survfit(Surv(time, status) ~ 1, data = d), times = tm, extend = TRUE)$surv
  rmst_km <- function(d) summary(survfit(Surv(time / 12, status) ~ 1, data = d), rmean = 5)$table[["rmean"]]
  cand_of <- function(id) CANDIDATES[[which(sapply(CANDIDATES, `[[`, "id") == id)]]
  one <- function() {
    P <- P_base
    efs_out <- list(); pcr_out <- c(); bind <- c()
    for (a in c("pembro", "placebo")) {
      st <- lapply(c(pCR = "pCR", nonpCR = "nonpCR"), function(s) ipd[[paste0("K22_S4_EFS_pCR_", a, "_", s)]])
      pool <- rbind(data.frame(st$pCR, stratum = "pCR"), data.frame(st$nonpCR, stratum = "nonpCR"))
      pool <- pool[sample.int(nrow(pool), nrow(pool), replace = TRUE), ]
      n_s <- c(pCR = sum(pool$stratum == "pCR"), nonpCR = sum(pool$stratum == "nonpCR"))
      P$p_pcr[[a]] <- n_s[["pCR"]] / nrow(pool)
      P$q_pre[[a]] <- c(pCR = 0, nonpCR = P$composition[[a]][["progression_precluding_surgery"]] / n_s[["nonpCR"]])
      for (s in c("pCR", "nonpCR")) {
        cv <- paste0("EFS_", a, "_", s)
        raw <- pool[pool$stratum == s, c("time", "status")]
        P$pre_surv[[a]][[s]] <- data.frame(time = (0:Lm) / 12, surv = km_at(raw, 0:Lm))
        pre <- km_at(raw, Lm)
        d <- raw[raw$time > Lm, ]; d <- data.frame(time = (d$time - Lm) / 12, status = d$status)
        a0 <- CFG$start_age + L; d$bh <- mu_pop(a0 + d$time)
        sp <- fit_candidate(cand_of(SEL$model[SEL$curve == cv]), d)$spec
        if (any(!is.finite(sp$pars))) stop("non-finite EFS fit")
        ci <- fits$efs5_ci[[cv]]
        r <- constrain_efs5(sp, d, a0, pre, L, ci[["lo"]], ci[["hi"]])
        if (!r$converged) stop("constraint did not converge")
        P$efs[[a]][[s]] <- r$spec
        efs_out[[cv]] <- r$spec$pars
        bind[[cv]] <- r$binding
        pcr_out[paste0(c("n_", "pre7_"), cv)] <- c(n_s[[s]], pre)
      }
      pcr_out[paste0(c("p_pcr_", "q_pre_"), a)] <- c(P$p_pcr[[a]], P$q_pre[[a]][["nonpCR"]])
    }
    # OS: resample, refit the selected models (saved only), targets for calibration
    os_b <- list(); os_par <- list()
    for (a in c("pembro", "placebo")) {
      d0 <- ipd[[paste0("K24_F1A_OS_", a)]]
      os_b[[a]] <- d0[sample.int(nrow(d0), nrow(d0), replace = TRUE), ]
      cv <- paste0("OS_", a)
      d <- data.frame(time = os_b[[a]]$time / 12, status = os_b[[a]]$status); d$bh <- mu_pop(CFG$start_age + d$time)
      sp0 <- fits$selected[[cv]]
      sp <- fit_candidate(cand_of(SEL$model[SEL$curve == cv]), d, knots = sp0$knots)$spec
      if (any(!is.finite(sp$pars))) stop("non-finite OS fit")
      os_par[[cv]] <- sp$pars
    }
    targets <- lapply(os_b, function(d) 100 * km_at(d, CFG$calib_grid_months))
    fl <- cal_flows(P)
    dr_med <- c(early = dr_median_draw(1), late = dr_late_median_draw(1))
    X7b <- final7y_draw(X7)
    cal <- calibrate_os(P, targets, CFG$calib_grid_months, dr_med, starts = c(list(th_base), CAL_STARTS), fl = fl, extra = X7b)
    P <- cal_apply(P, cal$par, dr_med)
    km_d <- rmst_km(os_b$pembro) - rmst_km(os_b$placebo)
    o <- cal_os(fl, cal_specs(cal$par, dr_med))
    eng_d <- rmst5_monthly(o$pembro) - rmst5_monthly(o$placebo)
    outv <- engine_outputs(P)
    list(efs = efs_out, efs_binding = bind, pcr = pcr_out, os_models = os_par,
         calib = c(preprog_shape = P$preprog$shape, preprog_median = P$preprog$scale, dr_shape = P$dr$shape, dr_median = P$dr$scale,
                   dr_late_median = P$dr$late_scale,
                   sse = cal$value, convergence = cal$convergence, cal$at_bound, cal$code52,
                   pembro_dr_k = P$pembro_dr_k, km_rmst5_diff = km_d, engine_rmst5_diff = eng_d),
         outputs = outv, pre_surv = P$pre_surv, targets7 = setNames(X7b$value, X7b$id))
  }
  for (attempt in 1:10) {
    set.seed(CFG$seed + b + 1e6 * (attempt - 1))
    r <- tryCatch(suppressWarnings(one()), error = function(e) e)
    if (!inherits(r, "error")) { r$b <- b; r$attempts <- attempt; return(r) }
  }
  list(b = b, attempts = NA, error = conditionMessage(r))
}

t0 <- Sys.time()
if (n_workers <= 1) {
  RES <- lapply(seq_len(B), boot_one)
} else {
  cl <- makeCluster(n_workers)
  clusterExport(cl, c("ROOT"))
  invisible(clusterEvalQ(cl, {
    source(file.path(ROOT, "R", "config.R")); source(file.path(ROOT, "R", "survmodels.R"))
    source(file.path(ROOT, "R", "engine.R")); source(file.path(ROOT, "R", "calibration.R"))
    suppressPackageStartupMessages(library(survival)); NULL
  }))
  clusterExport(cl, c("ipd", "fits", "SEL", "P_base", "th_base", "X7", "Lm", "L", "boot_one", "engine_outputs", "flat"))
  RES <- parLapplyLB(cl, seq_len(B), boot_one)
  stopCluster(cl)
}
el <- as.numeric(difftime(Sys.time(), t0, units = "mins"))
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
                dr_median = P_base$dr$scale, dr_late_median = P_base$dr$late_scale, pembro_dr_k = P_base$pembro_dr_k)
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
