# bootstrap_core.R
# One bootstrap replicate of the survival engine (structure of round 9), shared by 06_bootstrap.R
# (phase-1 bootstrap, data/bootstrap/) and 06c_bootstrap_check.R (reference results for checking
# other machines, output/check/). Steps of a replicate: see 06_bootstrap.R.
# Random numbers are set per replicate, not per worker: replicate b calls set.seed(seed + b) at its
# start (+ 1e6 per redraw after a failed fit), so the results do not depend on the number of
# worker processes or on which worker runs a replicate (checked with 4 and 8 workers, 2026-10-23).
# Requires config.R, survmodels.R, engine.R and calibration.R to be sourced.

# inputs of the replicates, put in the global environment (exported to the workers)
boot_load <- function() {
  g <- globalenv()
  g$ipd <- readRDS(file.path(ROOT, "data", "ipd", "ipd_all.rds"))
  g$fits <- readRDS(file.path(ROOT, "data", "fits", "fits.rds"))
  g$SEL <- read.csv(file.path(ROOT, "output", "phase1", "model_selection.csv"), stringsAsFactors = FALSE)
  g$P_base <- readRDS(file.path(ROOT, "data", "fits", "engine_params.rds"))     # written only when step 5 passed
  g$th_base <- readRDS(file.path(ROOT, "data", "fits", "calibration_candidates.rds"))$optim$par
  g$X7 <- final7y_targets()
  g$Lm <- CFG$landmark_months; g$L <- g$Lm / 12
  invisible(NULL)
}

# engine outputs at the years tt (EFS and OS, %), by arm x pCR; pembrolizumab also under k = 1
engine_outputs <- function(P, tt = c(5, 7, 10, 20)) {
  outv <- c()
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

boot_one <- function(b, seed = CFG$boot_seed, tt = c(5, 7, 10, 20)) {
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
        # interval constraint with fixed bounds (fits.rds written before round 11: 5-year), or round 11
        # revised: equality constraint at a value drawn from Binomial(n, p)/n (n: IA4 stratum size, p:
        # reported value), drawn here inside the replicate's random-number stream
        ci <- if (is.null(fits$efs_con_ci)) fits$efs5_ci[[cv]] else fits$efs_con_ci[[cv]]
        tgt <- if (identical(fits$efs_con_type, "equal")) 100 * rbinom(1, ci[["n"]], ci[["ref"]] / 100) / ci[["n"]] else NULL
        r <- constrain_efs5(sp, d, a0, pre, L, ci[["lo"]], ci[["hi"]], at = if (is.null(fits$efs_con_years)) 5 else fits$efs_con_years,
                            target = tgt)
        if (!r$converged) stop("constraint did not converge")
        P$efs[[a]][[s]] <- r$spec
        efs_out[[cv]] <- r$spec$pars
        bind[[cv]] <- r$binding
        pcr_out[paste0(c("n_", "pre7_"), cv)] <- c(n_s[[s]], pre)
        if (!is.null(tgt)) pcr_out[paste0("efs_target_", cv)] <- tgt
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
    dr_ext <- esme_draw()                      # round 9: ESME IPD resampled and refitted (shape and medians)
    X7b <- final7y_draw(X7)
    cal <- calibrate_os(P, targets, CFG$calib_grid_months, dr_ext, starts = c(list(th_base), CAL_STARTS), fl = fl, extra = X7b,
                        fixed = cal_fixed())                       # round 14: k fixed at CFG$pembro_dr_k_fixed
    P <- cal_apply(P, cal$par, dr_ext)
    km_d <- rmst_km(os_b$pembro) - rmst_km(os_b$placebo)
    o <- cal_os(fl, cal_specs(cal$par, dr_ext))
    eng_d <- rmst5_monthly(o$pembro) - rmst5_monthly(o$placebo)
    outv <- engine_outputs(P, tt)
    list(efs = efs_out, efs_binding = bind, pcr = pcr_out, os_models = os_par,
         calib = c(preprog_shape = P$preprog$shape, preprog_median = P$preprog$scale, dr_shape = P$dr$shape, dr_median = P$dr$scale,
                   dr_late_shape = P$dr$late_shape, dr_late_median = P$dr$late_scale,
                   sse = cal$value, convergence = cal$convergence, cal$at_bound, cal$code52,
                   pembro_dr_k = P$pembro_dr_k, km_rmst5_diff = km_d, engine_rmst5_diff = eng_d),
         outputs = outv, pre_surv = P$pre_surv, targets7 = setNames(X7b$value, X7b$id))
  }
  for (attempt in 1:10) {
    set.seed(seed + b + 1e6 * (attempt - 1))
    r <- tryCatch(suppressWarnings(one()), error = function(e) e)
    if (!inherits(r, "error")) { r$b <- b; r$attempts <- attempt; return(r) }
  }
  list(b = b, attempts = NA, error = conditionMessage(r))
}

# replicates 1..B on n_workers processes (PSOCK; serial if n_workers <= 1); returns the list of
# replicates and the minutes taken. Each worker runs with one thread for OpenMP and the BLAS
# (docs/model_spec.md section 7; RhpcBLASctl only if installed).
boot_run <- function(B, n_workers, seed = CFG$boot_seed, tt = c(5, 7, 10, 20)) {
  t0 <- Sys.time()
  if (n_workers <= 1) {
    RES <- lapply(seq_len(B), boot_one, seed = seed, tt = tt)
  } else {
    Sys.setenv(OMP_NUM_THREADS = "1")                  # inherited by the workers at start
    cl <- makeCluster(n_workers)
    on.exit(stopCluster(cl))
    clusterExport(cl, c("ROOT"))
    invisible(clusterEvalQ(cl, {
      Sys.setenv(OMP_NUM_THREADS = "1")
      if (requireNamespace("RhpcBLASctl", quietly = TRUE)) RhpcBLASctl::blas_set_num_threads(1)
      source(file.path(ROOT, "R", "config.R")); source(file.path(ROOT, "R", "survmodels.R"))
      source(file.path(ROOT, "R", "engine.R")); source(file.path(ROOT, "R", "calibration.R"))
      source(file.path(ROOT, "R", "bootstrap_core.R"))
      suppressPackageStartupMessages(library(survival)); NULL
    }))
    clusterExport(cl, c("ipd", "fits", "SEL", "P_base", "th_base", "X7", "Lm", "L"))
    RES <- parLapplyLB(cl, seq_len(B), boot_one, seed = seed, tt = tt)
  }
  list(RES = RES, minutes = as.numeric(difftime(Sys.time(), t0, units = "mins")))
}
