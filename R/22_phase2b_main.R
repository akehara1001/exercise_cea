# 22_phase2b_main.R
# Phase 2 main analysis, by docs/analysis_plan_phase2.md (committed before this script was first run).
#   det: deterministic results (base, E01-E03 crossings, the yardstick), scenarios and one-way
#        sensitivity analyses;
#   psa: the 1,000 phase-1 bootstrap replicates (survival, rebuilt from the saved matrices and checked
#        against their stored outputs) with cost and utility parameters drawn from data/params_dist.csv;
#   plan9 (section 9 of the plan, 2026-10-26; not part of "all"): plan9_det = scenarios of the costs after
#        metastatic recurrence (deterministic, crossings) and the decomposition of the incremental costs;
#        plan9_psa = the scenarios over the same 1,000 replicates and parameter draws; plan9_cohort = net
#        benefit for one year's patients (from the existing results and input/params/cohort_N_jbcs2024.csv, by
#        the 9.3 addendum; the earlier cohort_value.csv and cohort_value_N.csv are superseded and not rewritten);
#        plan9 = the three. The files of det and psa are not rewritten.
#   plan10 (section 10 of the plan, deterministic): the Japanese utility scenario (sc_util_jp_*) and the break-even
#        points of the utility scenarios, Elmore and S-JP by crossings() (sc_crossings.csv).
# Usage: Rscript R/22_phase2b_main.R [det|psa|all|plan9|plan9_det|plan9_psa|plan9_cohort|plan10] [workers]
#        (default all, physical cores - 1)
# Outputs: output/phase2/main/ (csv and png)

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R")); source(file.path(ROOT, "R", "engine.R")); source(file.path(ROOT, "R", "econ.R"))
suppressPackageStartupMessages({ library(survival); library(parallel); library(ggplot2) })
args <- commandArgs(trailingOnly = TRUE)
WHAT <- if (length(args)) args[1] else "all"
N_WORKERS <- if (length(args) > 1) as.integer(args[2]) else parallel::detectCores(logical = FALSE) - 1
OUT <- file.path(ROOT, "output", "phase2", "main"); dir.create(OUT, recursive = TRUE, showWarnings = FALSE)
wcsv <- function(x, name) write.csv(x, file.path(OUT, name), row.names = FALSE, fileEncoding = "UTF-8")

P <- readRDS(file.path(ROOT, "data", "fits", "engine_params.rds"))
EXT <- readRDS(file.path(ROOT, "data", "fits", "dr_k_external.rds"))
PL <- read.csv(file.path(ROOT, "data", "params_long.csv"), stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)
PD <- read.csv(file.path(ROOT, "data", "params_dist.csv"), stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)
B0 <- PL[PL$stat == "基本値", ]
stopifnot(identical(B0$param_id, PD$param_id), !anyNA(B0$value))
note_of <- setNames(B0$備考, B0$param_id)
u05_weeks <- as.numeric(sub(".*期間 ([0-9.]+) 週.*", "\\1", note_of[["U05"]]))
PV0 <- c(setNames(B0$value, B0$param_id), U05_duration_years = wk(u05_weeks))
LAMBDA <- c(5e6, 7.5e6)
HR_GRID <- round(seq(0.70, 1.00, by = 0.025), 3)
DP_GRID <- (0:10) / 100
E_LINES <- PV0[c("E01", "E02", "E03")]
PROVISIONAL <- B0$param_id[grepl("【要確認", B0$備考, fixed = TRUE)]

# path A definitions (analysis plan section 3 and 8); wane_start in years from randomization
path_a <- function(def, hr0) switch(def,
  base = list(hr0 = hr0, wane_start = 5, wane_rate = log(2)),
  s1   = list(hr0 = hr0, delay_years = 1, wane_rate = log(2)),
  s2   = list(hr0 = hr0, wane_rate = 0),
  cont = list(hr0 = hr0, delay_years = 0, wane_rate = log(2)))          # with exercise_continue = TRUE
path_b <- function(dp) list(hr0 = 1, delta_pcr = dp)

# one parameter set: the four arms as needed. Returns the rows of the exercise comparisons (dQ, dC
# without the programme cost; cap = lambda dQ - dC) and of the reference comparison.
# cols: "base" and, with Pk, "kext" for the comparisons with pembrolizumab
evaluate <- function(P, pv, Pk = NULL, sjp = FALSE, settings = list(), hr_def = "base", axes = c("hr0", "pcr"),
                     hr_grid = HR_GRID, dp_grid = DP_GRID) {
  ea <- function(arm, Px, ex = EXERCISE_NEUTRAL) econ_arm(arm, Px, pv, settings = settings, exercise = ex, sjp = sjp)
  ex_list <- c(if ("hr0" %in% axes) lapply(hr_grid, function(h) list(axis = "hr0", x = h, ex = path_a(hr_def, h))),
               if ("pcr" %in% axes) lapply(dp_grid, function(d) list(axis = "pcr", x = d, ex = path_b(d))))
  cols <- c(base = list(P), if (!is.null(Pk)) list(kext = Pk))
  ch <- ea("chemo", P)
  rows <- list(); ref <- list()
  for (cn in names(cols)) {
    pe <- ea("pembro", cols[[cn]])
    ref[[cn]] <- data.frame(column = cn, dC = pe$cost - ch$cost, dQ = pe$qaly - ch$qaly, dLY = pe$ly_disc - ch$ly_disc)
    for (e in ex_list) {
      bo <- ea("both", cols[[cn]], e$ex)
      rows[[length(rows) + 1]] <- data.frame(comparison = "main", column = cn, axis = e$axis, x = e$x,
                                             dQ = bo$qaly - pe$qaly, dC = programme_dcost(bo, pe))
      if (cn == "base") {
        xr <- ea("exercise", P, e$ex)
        rows[[length(rows) + 1]] <- data.frame(comparison = "secondary", column = "base", axis = e$axis, x = e$x,
                                               dQ = xr$qaly - ch$qaly, dC = programme_dcost(xr, ch))
      }
    }
  }
  list(ex = do.call(rbind, rows), ref = do.call(rbind, ref), q_chemo = ch$qaly)
}
add_caps <- function(d) { for (l in LAMBDA) d[[sprintf("cap_%g", l / 1e4)]] <- l * d$dQ - d$dC; d }   # cap_500 = lambda 5,000,000
# parameter set of bootstrap replicate i, rebuilt from the saved matrices (as rebuild() in R/07_engine_outputs.R);
# BR, fits and Lm are read in the psa and plan9 parts
rebuild <- function(i) {
  Pb <- P
  e <- BR$efs[i, ]; pc <- BR$pcr_preprog[i, ]; ps <- BR$pre_surv[i, ]; cb <- BR$calibration[i, ]
  for (a in c("pembro", "placebo")) {
    for (s in c("pCR", "nonpCR")) {
      cv <- paste0("EFS_", a, "_", s)
      sp <- fits$selected[[cv]]
      sp$pars <- setNames(e[paste0(cv, "_", names(sp$pars))], names(sp$pars))
      Pb$efs[[a]][[s]] <- sp
      Pb$pre_surv[[a]][[s]] <- data.frame(time = (0:Lm) / 12, surv = unname(ps[paste0("pre_surv_", a, "_", s, "_m", 0:Lm)]))
    }
    Pb$p_pcr[[a]] <- unname(pc[paste0("p_pcr_", a)])
    Pb$q_pre[[a]] <- c(pCR = 0, nonpCR = unname(pc[paste0("q_pre_", a)]))
  }
  Pb$preprog <- list(dist = "llogis", shape = unname(cb["preprog_shape"]), scale = unname(cb["preprog_median"]))
  Pb$dr <- list(dist = "llogis", shape = unname(cb["dr_shape"]), scale = unname(cb["dr_median"]),
                late_shape = unname(cb["dr_late_shape"]), late_scale = unname(cb["dr_late_median"]), early_cycles = P$dr$early_cycles)
  Pb$pembro_dr_k <- unname(cb["pembro_dr_k"])
  Pb
}
# utility value sets of the scenarios (det, plan10): U01-U05 from the notes of the input sheet (US, UK, Australia)
util_set <- function(set) {
  pat <- c(us = "米国[^0-9]*([0-9.]+)", uk = "英国[^0-9]*([0-9.]+)", au = "豪州[^0-9]*([0-9.]+)")[[set]]
  pv <- PV0
  for (u in sprintf("U%02d", 1:5)) {
    m <- regmatches(note_of[[u]], regexec(pat, note_of[[u]]))[[1]]
    stopifnot(length(m) == 2); pv[[u]] <- as.numeric(m[2])
  }
  pv
}
# break-even points in hr0 on [0.30, 1.00] by uniroot, tol 1e-6 (plan sections 9.1 and 10.2; sc_base_crossings.csv,
# Table 2 of the manuscript): cap = programme cost (lambda 5,000,000 and 7,500,000) and avoided medical costs (-dC,
# programme cost excluded) = programme cost; E01-E03 at their base values. Px: parameter set of the base column;
# Pk: that of the column "early-DR k external" of the main comparison (left out when NULL); sjp: S-JP in all arms
crossings <- function(pv, Px = P, Pk = NULL, sjp = FALSE)
  do.call(rbind, lapply(c(list(c("main", "base")), if (!is.null(Pk)) list(c("main", "kext")), list(c("secondary", "base"))), function(cc) {
    Pc <- if (cc[2] == "kext") Pk else Px
    ref <- econ_arm(if (cc[1] == "main") "pembro" else "chemo", Pc, pv, sjp = sjp)
    g <- function(h) { ex <- econ_arm(if (cc[1] == "main") "both" else "exercise", Pc, pv, exercise = path_a("base", h), sjp = sjp)
                       c(dQ = ex$qaly - ref$qaly, dC = programme_dcost(ex, ref)) }
    solve <- function(f) { lo <- f(0.30); hi <- f(1.00); if (sign(lo) != sign(hi)) uniroot(f, c(0.30, 1.00), tol = 1e-6)$root else NA_real_ }
    do.call(rbind, lapply(names(E_LINES), function(en) rbind(
      data.frame(comparison = cc[1], column = cc[2], type = "avoided_eq_programme", lambda = NA_real_, programme = en, cost = E_LINES[[en]],
                 hr0 = solve(function(h) -g(h)[["dC"]] - E_LINES[[en]])),
      do.call(rbind, lapply(LAMBDA, function(l) data.frame(comparison = cc[1], column = cc[2], type = "cap_eq_programme", lambda = l,
                 programme = en, cost = E_LINES[[en]], hr0 = solve(function(h) { v <- g(h); l * v[["dQ"]] - v[["dC"]] - E_LINES[[en]] }))))))) }))
# PSA summaries (psa and plan9): caps by comparison, column, axis and x; reference comparison by column
q <- function(v) quantile(v, c(0.5, 0.025, 0.975), names = FALSE)
caps_summary <- function(EX) {
  SM <- do.call(rbind, lapply(split(EX, list(EX$comparison, EX$column, EX$axis, EX$x), drop = TRUE), function(d) {
    data.frame(comparison = d$comparison[1], column = d$column[1], axis = d$axis[1], x = d$x[1], n = nrow(d),
               cap500_median = q(d$cap_500)[1], cap500_lo = q(d$cap_500)[2], cap500_hi = q(d$cap_500)[3],
               cap750_median = q(d$cap_750)[1], cap750_lo = q(d$cap_750)[2], cap750_hi = q(d$cap_750)[3],
               p_cap500_ge_E02 = mean(d$cap_500 >= E_LINES[["E02"]]), p_cap750_ge_E02 = mean(d$cap_750 >= E_LINES[["E02"]]))
  }))
  SM[order(SM$comparison, SM$column, SM$axis, SM$x), ]
}
ref_summary <- function(RF) do.call(rbind, lapply(split(RF, RF$column), function(d) data.frame(
  column = d$column[1], n = nrow(d), dC_median = q(d$dC)[1], dC_lo = q(d$dC)[2], dC_hi = q(d$dC)[3],
  dQ_median = q(d$dQ)[1], dQ_lo = q(d$dQ)[2], dQ_hi = q(d$dQ)[3], icer_median = q(d$icer)[1], icer_lo = q(d$icer)[2], icer_hi = q(d$icer)[3],
  p_ce_500 = mean(LAMBDA[1] * d$dQ - d$dC > 0), p_ce_750 = mean(LAMBDA[2] * d$dQ - d$dC > 0), n_dQ_le_0 = sum(d$dQ <= 0))))

# ---------------------------------------------------------------- deterministic
if (WHAT %in% c("det", "all")) {
  t0 <- Sys.time()
  PK <- params_kext(P, EXT)
  D <- evaluate(P, PV0, Pk = PK)
  wcsv(add_caps(D$ex), "det_caps.csv")
  R0 <- D$ref; R0$icer <- R0$dC / R0$dQ
  for (l in LAMBDA) R0[[sprintf("nmb_%g", l / 1e4)]] <- l * R0$dQ - R0$dC
  wcsv(R0, "det_reference.csv")
  # E01-E03 crossings in hr0 (main base, main kext, secondary), [0.30, 1.00]
  cap_at <- function(comp, col, h, l) {
    Px <- if (col == "kext") PK else P
    ex <- path_a("base", h)
    if (comp == "main") { bo <- econ_arm("both", Px, PV0, exercise = ex); pe <- econ_arm("pembro", Px, PV0) }
    else { bo <- econ_arm("exercise", P, PV0, exercise = ex); pe <- econ_arm("chemo", P, PV0) }
    programme_cap(bo, pe, l)
  }
  CR <- do.call(rbind, lapply(list(c("main", "base"), c("main", "kext"), c("secondary", "base")), function(cc)
    do.call(rbind, lapply(LAMBDA, function(l) do.call(rbind, lapply(names(E_LINES), function(en) {
      f <- function(h) cap_at(cc[1], cc[2], h, l) - E_LINES[[en]]
      lo <- f(0.30); hi <- f(1.00)
      r <- if (sign(lo) != sign(hi)) uniroot(f, c(0.30, 1.00), tol = 1e-6)$root else NA_real_
      data.frame(comparison = cc[1], column = cc[2], lambda = l, programme = en, cost = E_LINES[[en]], hr0 = r,
                 cap_at_0.30 = lo + E_LINES[[en]], cap_at_1.00 = hi + E_LINES[[en]],
                 note = if (is.na(r)) "no crossing in [0.30, 1.00]" else if (r < 0.70) "outside the main axis (hr0 < 0.70)" else "")
    }))))))
  wcsv(CR, "det_e_crossings.csv")
  # the yardstick: dQ(chemo + exercise vs chemo) = dQ(pembro vs chemo)
  target <- R0$dQ[R0$column == "base"]
  ch <- econ_arm("chemo", P, PV0)
  gA <- function(h) econ_arm("exercise", P, PV0, exercise = path_a("base", h))$qaly - ch$qaly - target
  gB <- function(d) econ_arm("exercise", P, PV0, exercise = path_b(d))$qaly - ch$qaly - target
  find_root <- function(g, lo, hi) { a <- g(lo); b <- g(hi); list(root = if (sign(a) != sign(b)) uniroot(g, c(lo, hi), tol = 1e-7)$root else NA_real_, at_lo = a + target, at_hi = b + target) }
  sa <- find_root(gA, 0.30, 1.00); sb <- find_root(gB, 0, 0.37)
  YS <- data.frame(axis = c("hr0", "pcr"), target_dQ = target, root = c(sa$root, sb$root),
                   search = c("[0.30, 1.00]", "[0, 0.37]"), dQ_at_lower_end = c(sa$at_lo, sb$at_lo), dQ_at_upper_end = c(sa$at_hi, sb$at_hi),
                   on_main_axis = c(!is.na(sa$root) && sa$root >= 0.70, !is.na(sb$root) && sb$root <= 0.10))
  wcsv(YS, "det_yardstick.csv")
  # scenarios (deterministic)
  SC <- list(
    base = list(),
    sjp = list(sjp = TRUE),
    kext = list(P = PK),
    elmore = list(P = within(P, preprog$scale <- 26 / 12)),
    utility_us = list(pv = util_set("us")), utility_uk = list(pv = util_set("uk")), utility_au = list(pv = util_set("au")),
    path_a_s1 = list(hr_def = "s1", axes = "hr0"), path_a_s2 = list(hr_def = "s2", axes = "hr0"),
    continue_s1 = list(hr_def = "cont", axes = "hr0", settings = list(exercise_continue = TRUE)))
  UV <- do.call(rbind, lapply(c("us", "uk", "au"), function(s) data.frame(set = s, param_id = sprintf("U%02d", 1:5), value = util_set(s)[sprintf("U%02d", 1:5)])))
  wcsv(UV, "scenario_utility_sets.csv")
  SR <- list(); SF <- list()
  for (n in names(SC)) {
    s <- SC[[n]]
    r <- evaluate(if (is.null(s$P)) P else s$P, if (is.null(s$pv)) PV0 else s$pv, sjp = isTRUE(s$sjp),
                  settings = if (is.null(s$settings)) list() else s$settings, hr_def = if (is.null(s$hr_def)) "base" else s$hr_def,
                  axes = if (is.null(s$axes)) c("hr0", "pcr") else s$axes)
    SR[[n]] <- data.frame(scenario = n, add_caps(r$ex))
    SF[[n]] <- data.frame(scenario = n, r$ref, icer = r$ref$dC / r$ref$dQ)
  }
  wcsv(do.call(rbind, SR), "scenario_caps.csv"); wcsv(do.call(rbind, SF), "scenario_reference.csv")
  # one-way sensitivity: main cap at hr0 = 0.85 (base path A), lambda 5,000,000; reference ICER
  ow_rows <- PD$param_id[!is.na(PD$lower) & !is.na(PD$upper)]
  one <- function(pv, sjp = FALSE) {
    ex <- path_a("base", 0.85)
    bo <- econ_arm("both", P, pv, exercise = ex, sjp = sjp); pe <- econ_arm("pembro", P, pv, sjp = sjp); ch <- econ_arm("chemo", P, pv, sjp = sjp)
    c(cap = programme_cap(bo, pe, LAMBDA[1]), icer = (pe$cost - ch$cost) / (pe$qaly - ch$qaly))
  }
  b1 <- one(PV0); b1s <- one(PV0, sjp = TRUE)
  cl <- makeCluster(N_WORKERS)
  clusterExport(cl, c("ROOT"))
  invisible(clusterEvalQ(cl, { source(file.path(ROOT, "R", "config.R")); source(file.path(ROOT, "R", "survmodels.R"))
    source(file.path(ROOT, "R", "engine.R")); source(file.path(ROOT, "R", "econ.R")); suppressPackageStartupMessages(library(survival)); NULL }))
  clusterExport(cl, c("P", "PV0", "PD", "LAMBDA", "path_a", "one"))
  OW <- do.call(rbind, parLapply(cl, ow_rows, function(id) {
    r <- PD[PD$param_id == id, ]
    o <- sapply(c(lower = r$lower, upper = r$upper), function(v) { pv <- PV0; pv[[id]] <- v; one(pv) })
    data.frame(param_id = id, low_value = r$lower, high_value = r$upper, cap_low = o["cap", "lower"], cap_high = o["cap", "upper"],
               icer_low = o["icer", "lower"], icer_high = o["icer", "upper"])
  }))
  SJP_IDS <- c("F01", "F01P", "F02", "F03", "F04", "F04P", "F05", "F06", "F07", "F08")
  OWS <- do.call(rbind, parLapply(cl, intersect(SJP_IDS, ow_rows), function(id) {
    r <- PD[PD$param_id == id, ]
    o <- sapply(c(lower = r$lower, upper = r$upper), function(v) { pv <- PV0; pv[[id]] <- v; one(pv, sjp = TRUE) })
    data.frame(param_id = id, low_value = r$lower, high_value = r$upper, cap_low = o["cap", "lower"], cap_high = o["cap", "upper"],
               icer_low = o["icer", "lower"], icer_high = o["icer", "upper"])
  }))
  stopCluster(cl)
  meta <- PD[, c("param_id", "range_rule")]; meta$provisional <- meta$param_id %in% PROVISIONAL
  meta$item <- B0$項目[match(meta$param_id, B0$param_id)]
  OW <- merge(OW, meta, by = "param_id"); OWS <- merge(OWS, meta, by = "param_id")
  OW$cap_base <- b1[["cap"]]; OW$icer_base <- b1[["icer"]]; OWS$cap_base <- b1s[["cap"]]; OWS$icer_base <- b1s[["icer"]]
  wcsv(OW, "oneway_base.csv"); wcsv(OWS, "oneway_sjp.csv")
  cat(sprintf("deterministic part: %.1f minutes\n", as.numeric(difftime(Sys.time(), t0, units = "mins"))))
}

# ---------------------------------------------------------------- PSA
if (WHAT %in% c("psa", "all")) {
  t0 <- Sys.time()
  BR <- readRDS(file.path(ROOT, "data", "bootstrap", "boot_replicates.rds"))
  fits <- readRDS(file.path(ROOT, "data", "fits", "fits.rds"))
  Lm <- CFG$landmark_months
  nB <- nrow(BR$calibration); stopifnot(nB == 1000)
  # cost and utility parameters: drawn once here, replicate 1..1000, rows in the order of params_dist.csv
  set.seed(CFG$boot_seed)
  DRAW <- matrix(NA_real_, nB, nrow(PD), dimnames = list(NULL, PD$param_id))
  for (b in seq_len(nB)) for (j in seq_len(nrow(PD))) {
    DRAW[b, j] <- switch(PD$dist[j], gamma = rgamma(1, shape = PD$p1[j], scale = PD$p2[j]), beta = rbeta(1, PD$p1[j], PD$p2[j]),
                         lognormal = rlnorm(1, PD$p1[j], PD$p2[j]), fixed = PD$base[j], stop("no distribution for ", PD$param_id[j]))
  }
  saveRDS(DRAW, file.path(OUT, "psa_parameter_draws.rds"))
  one_rep <- function(i) {
    Pb <- rebuild(i)
    o <- BR$outputs[i, ]                                   # check of the rebuild against the stored outputs
    chk <- c(100 * survival_engine("chemo", "all", times = c(5, 10), params = Pb)$OS - unlist(o[c("OS_5y_chemo_all", "OS_10y_chemo_all")]),
             100 * survival_engine("pembro", "all", times = c(5, 10), params = Pb)$OS - unlist(o[c("OS_5y_pembro_all", "OS_10y_pembro_all")]))
    pv <- c(DRAW[i, ], U05_duration_years = PV0[["U05_duration_years"]])
    r <- evaluate(Pb, pv, Pk = params_kext(Pb, EXT))
    list(ex = data.frame(rep = i, r$ex), ref = data.frame(rep = i, r$ref), rebuild_dev = max(abs(chk)))
  }
  Sys.setenv(OMP_NUM_THREADS = "1")
  cl <- makeCluster(N_WORKERS)
  clusterExport(cl, c("ROOT"))
  invisible(clusterEvalQ(cl, { Sys.setenv(OMP_NUM_THREADS = "1"); if (requireNamespace("RhpcBLASctl", quietly = TRUE)) RhpcBLASctl::blas_set_num_threads(1)
    source(file.path(ROOT, "R", "config.R")); source(file.path(ROOT, "R", "survmodels.R"))
    source(file.path(ROOT, "R", "engine.R")); source(file.path(ROOT, "R", "econ.R")); suppressPackageStartupMessages(library(survival)); NULL }))
  clusterExport(cl, c("P", "EXT", "PV0", "BR", "fits", "Lm", "DRAW", "rebuild", "evaluate", "path_a", "path_b", "HR_GRID", "DP_GRID", "LAMBDA"))
  RES <- parLapplyLB(cl, seq_len(nB), one_rep)
  stopCluster(cl)
  dev <- max(sapply(RES, `[[`, "rebuild_dev"))
  cat(sprintf("rebuild check: max |OS difference| %.2e points over %d replicates\n", dev, nB))
  stopifnot(dev < 1e-8)
  EX <- add_caps(do.call(rbind, lapply(RES, `[[`, "ex"))); RF <- do.call(rbind, lapply(RES, `[[`, "ref"))
  RF$icer <- RF$dC / RF$dQ
  saveRDS(list(ex = EX, ref = RF, minutes = as.numeric(difftime(Sys.time(), t0, units = "mins")), workers = N_WORKERS,
               commit = system2("git", c("-C", shQuote(ROOT), "rev-parse", "--short", "HEAD"), stdout = TRUE)),
          file.path(OUT, "psa_results.rds"))
  wcsv(caps_summary(EX), "psa_caps_summary.csv")
  wcsv(ref_summary(RF), "psa_reference_summary.csv")
  cat(sprintf("PSA: %d replicates on %d workers, %.1f minutes\n", nB, N_WORKERS, as.numeric(difftime(Sys.time(), t0, units = "mins"))))
}

# ---------------------------------------------------------------- plan9 (docs/analysis_plan_phase2.md section 9)
if (WHAT %in% c("plan9", "plan9_det", "plan9_psa", "plan9_cohort")) {
  t0 <- Sys.time()
  PK <- params_kext(P, EXT)
  # scenario values from the internal sheet v10 (sheet シナリオ, R/py/25_params_v10.py); 基本値 must be the
  # current ones; a scenario multiplies its parameters by シナリオ値 / 基本値 (deterministic and each PSA draw)
  suppressPackageStartupMessages(library(readxl))
  SCX <- as.data.frame(read_excel(file.path(ROOT, "input", "params", "parameters_v10.xlsx"), sheet = "シナリオ"), stringsAsFactors = FALSE)
  stopifnot(identical(names(SCX)[1:6], c("シナリオ", "param_id", "項目", "基本値", "シナリオ値", "倍率（シナリオ値 ÷ 基本値）")))
  stopifnot(all(abs(SCX[["基本値"]] - PV0[SCX$param_id]) <= 1e-9 * PV0[SCX$param_id]))
  SCN <- c("sc_metcost50", "sc_eribulin"); stopifnot(setequal(SCX[["シナリオ"]], SCN))
  fac <- lapply(setNames(SCN, SCN), function(s) { d <- SCX[SCX[["シナリオ"]] == s, ]; setNames(d[["シナリオ値"]] / d[["基本値"]], d$param_id) })
  scale_pv <- function(pv, f) { pv[names(f)] <- pv[names(f)] * f; pv }
  PVS <- c(list(sc_base = PV0), lapply(fac, function(f) scale_pv(PV0, f)))
  for (s in SCN) { d <- SCX[SCX[["シナリオ"]] == s, ]; stopifnot(max(abs(PVS[[s]][d$param_id] - d[["シナリオ値"]])) < 1e-6) }
}
if (WHAT %in% c("plan9", "plan9_det")) {
  # 9.1 deterministic caps and reference comparison (path A, base definition; hr0 axis only)
  DC0 <- read.csv(file.path(OUT, "det_caps.csv"))
  for (s in names(PVS)) {
    D <- evaluate(P, PVS[[s]], Pk = PK, axes = "hr0")
    X <- add_caps(D$ex); R0 <- D$ref; R0$icer <- R0$dC / R0$dQ
    for (l in LAMBDA) R0[[sprintf("nmb_%g", l / 1e4)]] <- l * R0$dQ - R0$dC
    if (s == "sc_base") {                      # the same code on the base values reproduces det_caps.csv and det_reference.csv
      b <- DC0[DC0$axis == "hr0", ]; m <- match(paste(X$comparison, X$column, X$x), paste(b$comparison, b$column, b$x))
      stopifnot(!anyNA(m), max(abs(X$cap_500 - b$cap_500[m]), abs(X$cap_750 - b$cap_750[m])) < 1e-6)
      r0 <- read.csv(file.path(OUT, "det_reference.csv")); stopifnot(max(abs(R0$icer - r0$icer[match(R0$column, r0$column)])) < 1e-6)
    } else { wcsv(X, paste0(s, "_det_caps.csv")); wcsv(R0, paste0(s, "_det_reference.csv")) }
  }
  cl <- makeCluster(min(N_WORKERS, length(PVS)))
  clusterExport(cl, c("ROOT"))
  invisible(clusterEvalQ(cl, { source(file.path(ROOT, "R", "config.R")); source(file.path(ROOT, "R", "survmodels.R"))
    source(file.path(ROOT, "R", "engine.R")); source(file.path(ROOT, "R", "econ.R")); suppressPackageStartupMessages(library(survival)); NULL }))
  clusterExport(cl, c("P", "PK", "E_LINES", "LAMBDA", "path_a", "crossings"))
  CRS <- parLapply(cl, PVS, function(pv) crossings(pv, P, PK))
  stopCluster(cl)
  CR0 <- read.csv(file.path(OUT, "det_e_crossings.csv"))
  b <- CRS$sc_base[CRS$sc_base$type == "cap_eq_programme", ]
  m <- match(paste(b$comparison, b$column, b$lambda, b$programme), paste(CR0$comparison, CR0$column, CR0$lambda, CR0$programme))
  stopifnot(!anyNA(m), max(abs(b$hr0 - CR0$hr0[m])) < 1e-9)          # same as det_e_crossings.csv
  for (s in names(PVS)) wcsv(CRS[[s]], paste0(s, "_crossings.csv"))

  # 9.2 decomposition of the incremental costs (deterministic, discounted, base values); adverse_events_B
  # split into immune-related (B21-B30 x B01-B10) and febrile neutropenia (B31 x B11)
  cat9 <- c(pembro_A03 = "pembrolizumab_drug", administration_A04 = "administration", ae_immune_B01_B10 = "immune_ae",
            ae_fn_B11 = "chemo_ae", follow_up_C = "follow_up", lrr_entry_D01 = "lrr", lrr_monthly_D02 = "lrr",
            dr_first_line_D03 = "dr_first_line", dr_later_lines_D05 = "dr_later_lines", terminal_D06 = "terminal_care",
            exercise_programme_E = "exercise_programme", musculoskeletal_ae_E06_E08 = "exercise_ae")
  comps <- function(r, pv) {
    cc <- r$cost_components; sfx <- if (has_pembro(r$arm)) "P" else "C"
    im <- sum(sapply(21:30, function(i) pv[[paste0("B", i, sfx)]] * pv[[sprintf("B%02d", i - 20)]])); fn <- pv[[paste0("B31", sfx)]] * pv[["B11"]]
    stopifnot(abs(im + fn - cc[["adverse_events_B"]]) < 1e-6)
    out <- c(cc[names(cc) != "adverse_events_B"], ae_immune_B01_B10 = im, ae_fn_B11 = fn)
    stopifnot(abs(sum(out) - r$cost) < 1e-6); out
  }
  decomp <- function(a, b, comparison, pv) {           # b minus a, by component, with the categories of section 9.2
    ca <- comps(a, pv); cb <- comps(b, pv); stopifnot(identical(names(ca), names(cb)))
    own <- if (comparison == "main") c("exercise_programme", "exercise_ae") else character(0)   # rows of their own in the main comparison
    k <- ifelse(names(ca) %in% names(cat9), cat9[names(ca)], "other")
    k[k %in% c("exercise_programme", "exercise_ae") & !(k %in% own)] <- "other"
    data.frame(component = names(ca), category = unname(k), a = unname(ca), b = unname(cb), d = unname(cb - ca))
  }
  ORD <- c("exercise_programme", "exercise_ae", "pembrolizumab_drug", "administration", "immune_ae", "chemo_ae", "follow_up", "lrr",
           "dr_first_line", "dr_later_lines", "terminal_care", "other")
  by_cat <- function(d) { s <- tapply(d$d, factor(d$category, ORD), sum); s <- s[!is.na(s)]
    data.frame(category = c(names(s), "total"), d = c(unname(s), sum(d$d))) }
  ch <- econ_arm("chemo", P, PV0)
  DEC <- list(); DEM <- list()
  for (cn in c("base", "kext")) {
    Px <- if (cn == "kext") PK else P
    pe <- econ_arm("pembro", Px, PV0)
    r <- decomp(ch, pe, "reference", PV0); stopifnot(abs(sum(r$d) - (pe$cost - ch$cost)) < 1e-6)
    DEC[[cn]] <- data.frame(column = cn, r)
    bo <- econ_arm("both", Px, PV0, settings = list(exercise_cost = "E02"), exercise = path_a("base", 0.85))
    m <- decomp(pe, bo, "main", PV0); stopifnot(abs(sum(m$d) - (bo$cost - pe$cost)) < 1e-6)
    dcx <- DC0$dC[DC0$comparison == "main" & DC0$column == cn & DC0$axis == "hr0" & abs(DC0$x - 0.85) < 1e-9]
    stopifnot(length(dcx) == 1, abs(sum(m$d[m$category != "exercise_programme"]) - dcx) < 1e-6)   # = -(avoided medical costs, report 1.6)
    DEM[[cn]] <- data.frame(column = cn, m)
  }
  wide <- function(L) {
    w <- Reduce(function(x, y) merge(x, y, by = "category", sort = FALSE),
                lapply(names(L), function(cn) setNames(by_cat(L[[cn]]), c("category", paste0("d_", cn)))))
    w[match(c(intersect(ORD, w$category), "total"), w$category), ]
  }
  DR9 <- wide(DEC); DM9 <- wide(DEM)
  tot <- DM9[DM9$category == "total", c("d_base", "d_kext")]
  DM9 <- rbind(DM9, data.frame(category = c("total_without_programme", "total_with_E01", "total_with_E03"),
                               d_base = tot$d_base + c(0, PV0[["E01"]], PV0[["E03"]]) - PV0[["E02"]],
                               d_kext = tot$d_kext + c(0, PV0[["E01"]], PV0[["E03"]]) - PV0[["E02"]]))
  wcsv(DR9, "decomp_reference.csv"); wcsv(do.call(rbind, DEC), "decomp_reference_components.csv")
  wcsv(DM9, "decomp_main_hr085.csv"); wcsv(do.call(rbind, DEM), "decomp_main_hr085_components.csv")
  cat(sprintf("plan9 deterministic part: %.1f minutes\n", as.numeric(difftime(Sys.time(), t0, units = "mins"))))
}
if (WHAT %in% c("plan9", "plan9_psa")) {
  # 9.1 PSA of the two scenarios: the same 1,000 replicates and the same parameter draws as the base PSA
  t1 <- Sys.time()
  BR <- readRDS(file.path(ROOT, "data", "bootstrap", "boot_replicates.rds"))
  fits <- readRDS(file.path(ROOT, "data", "fits", "fits.rds"))
  Lm <- CFG$landmark_months
  nB <- nrow(BR$calibration); stopifnot(nB == 1000)
  DRAW <- readRDS(file.path(OUT, "psa_parameter_draws.rds")); stopifnot(nrow(DRAW) == nB, identical(colnames(DRAW), PD$param_id))
  one_rep9 <- function(i) {
    Pb <- rebuild(i)
    o <- BR$outputs[i, ]                                   # check of the rebuild against the stored outputs
    chk <- c(100 * survival_engine("chemo", "all", times = c(5, 10), params = Pb)$OS - unlist(o[c("OS_5y_chemo_all", "OS_10y_chemo_all")]),
             100 * survival_engine("pembro", "all", times = c(5, 10), params = Pb)$OS - unlist(o[c("OS_5y_pembro_all", "OS_10y_pembro_all")]))
    pv <- c(DRAW[i, ], U05_duration_years = PV0[["U05_duration_years"]])
    Pk <- params_kext(Pb, EXT)
    r <- lapply(SCN, function(s) { e <- evaluate(Pb, scale_pv(pv, fac[[s]]), Pk = Pk, axes = "hr0")
      list(ex = data.frame(scenario = s, rep = i, e$ex), ref = data.frame(scenario = s, rep = i, e$ref)) })
    list(ex = do.call(rbind, lapply(r, `[[`, "ex")), ref = do.call(rbind, lapply(r, `[[`, "ref")), rebuild_dev = max(abs(chk)))
  }
  Sys.setenv(OMP_NUM_THREADS = "1")
  cl <- makeCluster(N_WORKERS)
  clusterExport(cl, c("ROOT"))
  invisible(clusterEvalQ(cl, { Sys.setenv(OMP_NUM_THREADS = "1"); if (requireNamespace("RhpcBLASctl", quietly = TRUE)) RhpcBLASctl::blas_set_num_threads(1)
    source(file.path(ROOT, "R", "config.R")); source(file.path(ROOT, "R", "survmodels.R"))
    source(file.path(ROOT, "R", "engine.R")); source(file.path(ROOT, "R", "econ.R")); suppressPackageStartupMessages(library(survival)); NULL }))
  clusterExport(cl, c("P", "EXT", "PV0", "BR", "fits", "Lm", "DRAW", "rebuild", "evaluate", "path_a", "path_b", "HR_GRID", "DP_GRID", "LAMBDA",
                      "SCN", "fac", "scale_pv"))
  RES <- parLapplyLB(cl, seq_len(nB), one_rep9)
  stopCluster(cl)
  dev <- max(sapply(RES, `[[`, "rebuild_dev"))
  cat(sprintf("rebuild check: max |OS difference| %.2e points over %d replicates\n", dev, nB))
  stopifnot(dev < 1e-8)
  EXA <- add_caps(do.call(rbind, lapply(RES, `[[`, "ex"))); RFA <- do.call(rbind, lapply(RES, `[[`, "ref")); RFA$icer <- RFA$dC / RFA$dQ
  mins <- as.numeric(difftime(Sys.time(), t1, units = "mins"))
  for (s in SCN) {
    EX <- EXA[EXA$scenario == s, names(EXA) != "scenario"]; RF <- RFA[RFA$scenario == s, names(RFA) != "scenario"]
    saveRDS(list(ex = EX, ref = RF, minutes = mins, workers = N_WORKERS, scenario = s, factors = fac[[s]],
                 commit = system2("git", c("-C", shQuote(ROOT), "rev-parse", "--short", "HEAD"), stdout = TRUE)),
            file.path(OUT, paste0(s, "_psa_results.rds")))
    wcsv(caps_summary(EX), paste0(s, "_psa_caps_summary.csv")); wcsv(ref_summary(RF), paste0(s, "_psa_reference_summary.csv"))
  }
  cat(sprintf("plan9 PSA: 2 scenarios x %d replicates on %d workers, %.1f minutes\n", nB, N_WORKERS, mins))
}
if (WHAT %in% c("plan9", "plan9_cohort")) {
  # 9.3 net benefit for one year's patients, by the addendum of 2026-10-26 (it withdraws N = 1,719 from four factors;
  # their files cohort_value.csv and cohort_value_N.csv, from 6704e54, are kept and marked as superseded): N from
  # the JBCS registry report no. 55 (input/params/cohort_N_jbcs2024.csv). The patients with pembrolizumab by the
  # main comparison, the rest by the secondary; net benefit per person = cap (lambda 5,000,000) - E02; hr0 0.95,
  # 0.90, 0.85; conditional on the effect. PSA: the two parts added within each replicate of psa_results.rds
  # (N not sampled). Sensitivity: N 2,900 and 4,000 at the same share of pembrolizumab.
  NJ <- read.csv(file.path(ROOT, "input", "params", "cohort_N_jbcs2024.csv"), stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)
  nv <- setNames(NJ$value, NJ$item)
  stopifnot(nv[["nac_stage2"]] + nv[["nac_stage3"]] == nv[["nac_total"]])
  share <- nv[["nac_pembro"]] / nv[["nac_total"]]
  NS <- data.frame(setting = c("main", "sens_2023", "sens_upper"), N = c(nv[["nac_total"]], nv[["sens_N_2023"]], nv[["sens_N_upper"]]))
  NS$n_pembro <- NS$N * share; NS$n_other <- NS$N - NS$n_pembro
  DC0 <- read.csv(file.path(OUT, "det_caps.csv")); PS <- readRDS(file.path(OUT, "psa_results.rds"))$ex
  nb_det <- function(comp, cn, h) { d <- DC0[DC0$comparison == comp & DC0$column == cn & DC0$axis == "hr0" & abs(DC0$x - h) < 1e-9, ]
    stopifnot(nrow(d) == 1); d$cap_500 - PV0[["E02"]] }
  nb_psa <- function(comp, cn, h) { p <- PS[PS$comparison == comp & PS$column == cn & PS$axis == "hr0" & abs(PS$x - h) < 1e-9, ]
    stopifnot(nrow(p) == 1000, identical(sort(p$rep), 1:1000)); p <- p[order(p$rep), ]; p$cap_500 - PV0[["E02"]] }   # by replicate
  CJ <- do.call(rbind, lapply(seq_len(nrow(NS)), function(i) do.call(rbind, lapply(c("base", "kext"), function(cn) do.call(rbind, lapply(c(0.95, 0.90, 0.85), function(h) {
    m <- nb_det("main", cn, h); s <- nb_det("secondary", "base", h)
    qq <- q(NS$n_pembro[i] * nb_psa("main", cn, h) + NS$n_other[i] * nb_psa("secondary", "base", h))
    data.frame(setting = NS$setting[i], N = NS$N[i], n_pembro = NS$n_pembro[i], n_other = NS$n_other[i], column = cn, hr0 = h, lambda = LAMBDA[1],
               programme = "E02", programme_cost = PV0[["E02"]], nb_person_main_det = m, nb_person_secondary_det = s,
               total_pembro_det = NS$n_pembro[i] * m, total_other_det = NS$n_other[i] * s, total_det = NS$n_pembro[i] * m + NS$n_other[i] * s,
               total_median = qq[1], total_lo = qq[2], total_hi = qq[3])
  }))))))
  wcsv(CJ, "cohort_value_jbcs2024.csv")
}

# ---------------------------------------------------------------- plan10 (docs/analysis_plan_phase2.md section 10)
if (WHAT == "plan10") {
  # 10.1 Japanese utility scenario (data/params_hara/utility_scenarios.csv, column japan; U03 and U05 as the base),
  # as the other utility sets of the det part: caps on both axes (base column) and the reference ICER
  t0 <- Sys.time()
  UJ <- read.csv(file.path(ROOT, "data", "params_hara", "utility_scenarios.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")
  stopifnot(identical(UJ$param_id, sprintf("U%02d", 1:5)), max(abs(UJ$base - PV0[UJ$param_id])) < 1e-9)
  pv_jp <- PV0; pv_jp[UJ$param_id] <- UJ$japan
  r <- evaluate(P, pv_jp)
  wcsv(data.frame(scenario = "utility_jp", add_caps(r$ex)), "sc_util_jp_det_caps.csv")
  wcsv(data.frame(scenario = "utility_jp", r$ref, icer = r$ref$dC / r$ref$dQ), "sc_util_jp_det_reference.csv")
  # 10.2 break-even points by crossings() (the method of sc_base_crossings.csv); the base again as a check, and the
  # other scenarios checked against scenario_caps.csv and scenario_reference.csv (same definitions as the det part)
  SC10 <- list(base = list(), utility_jp = list(pv = pv_jp), utility_us = list(pv = util_set("us")), utility_uk = list(pv = util_set("uk")),
               utility_au = list(pv = util_set("au")), elmore = list(P = within(P, preprog$scale <- 26 / 12)), sjp = list(sjp = TRUE))
  SC0 <- read.csv(file.path(OUT, "scenario_caps.csv")); SF0 <- read.csv(file.path(OUT, "scenario_reference.csv"))
  for (n in c("utility_us", "utility_uk", "utility_au", "elmore", "sjp")) {
    s <- SC10[[n]]
    r <- evaluate(if (is.null(s$P)) P else s$P, if (is.null(s$pv)) PV0 else s$pv, sjp = isTRUE(s$sjp))
    X <- add_caps(r$ex); b <- SC0[SC0$scenario == n, ]
    m <- match(paste(X$comparison, X$column, X$axis, X$x), paste(b$comparison, b$column, b$axis, b$x))
    stopifnot(!anyNA(m), nrow(b) == nrow(X), max(abs(X$cap_500 - b$cap_500[m]), abs(X$cap_750 - b$cap_750[m])) < 1e-6,
              abs(r$ref$dC / r$ref$dQ - SF0$icer[SF0$scenario == n & SF0$column == "base"]) < 1e-6)
  }
  cl <- makeCluster(min(N_WORKERS, length(SC10)))
  clusterExport(cl, c("ROOT"))
  invisible(clusterEvalQ(cl, { source(file.path(ROOT, "R", "config.R")); source(file.path(ROOT, "R", "survmodels.R"))
    source(file.path(ROOT, "R", "engine.R")); source(file.path(ROOT, "R", "econ.R")); suppressPackageStartupMessages(library(survival)); NULL }))
  clusterExport(cl, c("P", "PV0", "E_LINES", "LAMBDA", "path_a", "crossings"))
  CX <- parLapply(cl, SC10, function(s) crossings(if (is.null(s$pv)) PV0 else s$pv, if (is.null(s$P)) P else s$P, sjp = isTRUE(s$sjp)))
  stopCluster(cl)
  CX <- do.call(rbind, lapply(names(CX), function(n) data.frame(scenario = n, CX[[n]])))
  B0X <- read.csv(file.path(OUT, "sc_base_crossings.csv")); B0X <- B0X[B0X$column == "base", ]; b <- CX[CX$scenario == "base", ]
  m <- match(paste(b$comparison, b$column, b$type, b$lambda, b$programme), paste(B0X$comparison, B0X$column, B0X$type, B0X$lambda, B0X$programme))
  stopifnot(!anyNA(m), nrow(b) == nrow(B0X), max(abs(b$hr0 - B0X$hr0[m])) < 1e-9)   # same as sc_base_crossings.csv
  wcsv(CX, "sc_crossings.csv")
  cat(sprintf("plan10: %.1f minutes\n", as.numeric(difftime(Sys.time(), t0, units = "mins"))))
}
