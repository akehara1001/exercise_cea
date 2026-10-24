# 18_round15_scenarios.R
# Round 15 (docs/acceptance_rule_round15.md): scenarios on the base of round 15 (PreProg excess death
# = ESME early-relapse fit, nothing calibrated), gates (a), (b), (c) reported only:
#   "preprog_elmore": PreProg excess death median 26 months (Elmore et al. Ann Surg Oncol
#                     2021;28:5477-5485), shape as the base;
#   "kext":           k = 1.307 (data/fits/dr_k_external.rds) on early DR and on PreProg of the
#                     pembrolizumab arms (params_kext(..., preprog = TRUE)).
# Also the survival after PreProg entry at 1 and 5 years (all-cause: excess survival x background from
# age 49.5) for the base, the scenarios and round 14.
# Gate data from the base run (output/phase1/round15/base/). Outputs: output/phase1/round15/
#   scenario_gates.csv, preprog_survival.csv
# Usage: Rscript R/18_round15_scenarios.R

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R")); source(file.path(ROOT, "R", "engine.R")); source(file.path(ROOT, "R", "calibration.R"))
out <- file.path(ROOT, "output", "phase1", "round15"); bdir <- file.path(out, "base")
P1 <- readRDS(file.path(ROOT, "data", "fits", "round15", "base", "calibration_candidates.rds"))$params
P14 <- readRDS(file.path(ROOT, "data", "fits", "round14", "base", "calibration_candidates.rds"))$params
stopifnot(abs(P1$preprog$shape - P1$dr$shape) < 1e-12, abs(P1$preprog$scale - P1$dr$scale) < 1e-12, P1$pembro_dr_k == 1)
ext <- readRDS(file.path(ROOT, "data", "fits", "dr_k_external.rds"))
sc <- list(base = P1,
           preprog_elmore = within(P1, preprog$scale <- 26 / 12),
           kext = params_kext(P1, ext, preprog = TRUE))
arm_of <- c(pembro = "pembro", placebo = "chemo")
G <- read.csv(file.path(bdir, "calibration_gate.csv")); GR <- read.csv(file.path(bdir, "calibration_gate_rmst.csv"))
G7 <- read.csv(file.path(bdir, "calibration_final7y.csv")); G7 <- G7[G7$gate_c, c("id", "value", "ci95_lo", "ci95_hi")]
gates <- function(P, lab) {
  os <- lapply(arm_of, function(e) 100 * survival_engine(e, "all", times = (0:84) / 12, params = P)$OS)
  efs7 <- sapply(arm_of, function(e) 100 * survival_engine(e, "all", times = 7, params = P)$EFS)
  ga <- merge(G[, c("arm", "month", "km", "ci95_lo", "ci95_hi", "ci995_lo", "ci995_hi")],
              data.frame(arm = rep(names(os), each = 5), month = rep(c(12, 24, 36, 48, 60), 2),
                         model = unlist(lapply(os, function(v) v[c(12, 24, 36, 48, 60) + 1]))))
  ga$inside <- ga$model >= ga$ci95_lo - 1e-9 & ga$model <= ga$ci95_hi + 1e-9
  ga$inside_995 <- ga$model >= ga$ci995_lo - 1e-9 & ga$model <= ga$ci995_hi + 1e-9
  a_ok <- all(ga$inside) || all(ga$inside_995)
  rd5 <- rmst5_monthly(os$pembro / 100) - rmst5_monthly(os$placebo / 100)
  b_ok <- rd5 >= GR$km_boot_ci95_lo && rd5 <= GR$km_boot_ci95_hi
  g7 <- G7; g7$model <- c(os7_pembro = os$pembro[85], os7_placebo = os$placebo[85], efs7_pembro = efs7[["pembro"]], efs7_placebo = efs7[["placebo"]])[g7$id]
  g7$inside <- g7$model >= g7$ci95_lo - 1e-9 & g7$model <= g7$ci95_hi + 1e-9
  c_ok <- all(g7$inside)
  rbind(data.frame(scenario = lab, item = sprintf("OS %d y %s", ga$month / 12, ga$arm), reference = ga$km, lo = ga$ci95_lo, hi = ga$ci95_hi,
                   model = ga$model, inside = ga$inside),
        data.frame(scenario = lab, item = g7$id, reference = g7$value, lo = g7$ci95_lo, hi = g7$ci95_hi, model = g7$model, inside = g7$inside),
        data.frame(scenario = lab, item = "rmst5_diff_years", reference = GR$km, lo = GR$km_boot_ci95_lo, hi = GR$km_boot_ci95_hi, model = rd5, inside = b_ok),
        data.frame(scenario = lab, item = c("gate_a", "gate_b", "gate_c"), reference = NA, lo = NA, hi = NA, model = NA, inside = c(a_ok, b_ok, c_ok)))
}
S <- do.call(rbind, lapply(names(sc), function(n) gates(sc[[n]], n)))
write.csv(S, file.path(out, "scenario_gates.csv"), row.names = FALSE)
# survival after PreProg entry (all-cause, from age 49.5 = PP_ENTRY_AGE)
pps <- function(spec, k = 1, lab) {
  ex <- function(t) exp(-k * dr_cumhaz(modifyList(spec, list(k = NULL)), t))
  data.frame(setting = lab, median_months = 12 * spec$scale, shape = spec$shape, k = k,
             surv_1y = 100 * ex(1) * S_pop(PP_ENTRY_AGE, 1), surv_5y = 100 * ex(5) * S_pop(PP_ENTRY_AGE, 5))
}
PS <- rbind(pps(P1$preprog, 1, "round 15 base (ESME early fit)"), pps(sc$preprog_elmore$preprog, 1, "round 15 scenario Elmore (median 26 months)"),
            pps(P1$preprog, ext$k, "round 15 scenario kext, pembrolizumab arms"), pps(P14$preprog, 1, "round 14 (calibrated, at the bounds)"))
write.csv(PS, file.path(out, "preprog_survival.csv"), row.names = FALSE)
print(PS, row.names = FALSE)
print(S[S$item %in% c("gate_a", "gate_b", "gate_c", "os7_pembro", "os7_placebo", "rmst5_diff_years"), ], row.names = FALSE)
