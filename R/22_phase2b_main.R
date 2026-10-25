# 22_phase2b_main.R
# Phase 2 main analysis, by docs/analysis_plan_phase2.md (committed before this script was first run).
#   det: deterministic results (base, E01-E03 crossings, the yardstick), scenarios and one-way
#        sensitivity analyses;
#   psa: the 1,000 phase-1 bootstrap replicates (survival, rebuilt from the saved matrices and checked
#        against their stored outputs) with cost and utility parameters drawn from data/params_dist.csv.
# Usage: Rscript R/22_phase2b_main.R [det|psa|all] [workers]   (default all, physical cores - 1)
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
  util_set <- function(set) {
    pat <- c(us = "米国[^0-9]*([0-9.]+)", uk = "英国[^0-9]*([0-9.]+)", au = "豪州[^0-9]*([0-9.]+)")[[set]]
    pv <- PV0
    for (u in sprintf("U%02d", 1:5)) {
      m <- regmatches(note_of[[u]], regexec(pat, note_of[[u]]))[[1]]
      stopifnot(length(m) == 2); pv[[u]] <- as.numeric(m[2])
    }
    pv
  }
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
  # parameter set of replicate i, rebuilt from the saved matrices (as rebuild() in R/07_engine_outputs.R)
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
  q <- function(v) quantile(v, c(0.5, 0.025, 0.975), names = FALSE)
  SM <- do.call(rbind, lapply(split(EX, list(EX$comparison, EX$column, EX$axis, EX$x), drop = TRUE), function(d) {
    data.frame(comparison = d$comparison[1], column = d$column[1], axis = d$axis[1], x = d$x[1], n = nrow(d),
               cap500_median = q(d$cap_500)[1], cap500_lo = q(d$cap_500)[2], cap500_hi = q(d$cap_500)[3],
               cap750_median = q(d$cap_750)[1], cap750_lo = q(d$cap_750)[2], cap750_hi = q(d$cap_750)[3],
               p_cap500_ge_E02 = mean(d$cap_500 >= E_LINES[["E02"]]), p_cap750_ge_E02 = mean(d$cap_750 >= E_LINES[["E02"]]))
  }))
  SM <- SM[order(SM$comparison, SM$column, SM$axis, SM$x), ]
  wcsv(SM, "psa_caps_summary.csv")
  RS <- do.call(rbind, lapply(split(RF, RF$column), function(d) data.frame(
    column = d$column[1], n = nrow(d), dC_median = q(d$dC)[1], dC_lo = q(d$dC)[2], dC_hi = q(d$dC)[3],
    dQ_median = q(d$dQ)[1], dQ_lo = q(d$dQ)[2], dQ_hi = q(d$dQ)[3], icer_median = q(d$icer)[1], icer_lo = q(d$icer)[2], icer_hi = q(d$icer)[3],
    p_ce_500 = mean(LAMBDA[1] * d$dQ - d$dC > 0), p_ce_750 = mean(LAMBDA[2] * d$dQ - d$dC > 0), n_dQ_le_0 = sum(d$dQ <= 0))))
  wcsv(RS, "psa_reference_summary.csv")
  cat(sprintf("PSA: %d replicates on %d workers, %.1f minutes\n", nB, N_WORKERS, as.numeric(difftime(Sys.time(), t0, units = "mins"))))
}
