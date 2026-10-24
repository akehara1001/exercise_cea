# 17_round14_kext.R
# Round 14 (docs/acceptance_rule_round14.md) scenario "early-DR k (external)": k on early DR only
# (dr_with_k(..., scope = "early")), ESME shape, other parameters from the base calibration (k = 1),
# not recalibrated. k from Fedele 2026 (data/fedele2026.csv, R/py/17_fedele.py): the two groups
# (no first-line therapy within 90 days, 17 of 52, median OS 3.4 months; first-line therapy, 35 of
# 52, 12.4 months), each exponential, mixed 17/52 : 35/52; m = median of the mixture; k such that the
# pembrolizumab early-DR excess survival median equals m: S_ESME,early(m)^k = 0.5.
# Gates (a), (b), (c) as in 05_calibrate.R (data of the base run). Reported only, not for adoption.
# Outputs: output/phase1/round14/kext_derivation.csv, scenario_kext_gates.csv, data/fits/dr_k_external.rds
# Usage: Rscript R/17_round14_kext.R [base run dir] [base candidates.rds]

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R")); source(file.path(ROOT, "R", "engine.R")); source(file.path(ROOT, "R", "calibration.R"))
args <- commandArgs(trailingOnly = TRUE)
bdir <- if (length(args) >= 1) args[1] else file.path(ROOT, "output", "phase1", "round14", "base")
cand <- if (length(args) >= 2) args[2] else file.path(ROOT, "data", "fits", "round14", "base", "calibration_candidates.rds")
out <- file.path(ROOT, "output", "phase1", "round14"); dir.create(out, showWarnings = FALSE, recursive = TRUE)
P1 <- readRDS(cand)$params
stopifnot(abs(P1$pembro_dr_k - 1) < 1e-12)

FE <- read.csv(file.path(ROOT, "data", "fedele2026.csv"), stringsAsFactors = FALSE)
fv <- function(id) as.numeric(FE$value[FE$id == id]); fp <- function(id) FE$page[FE$id == id]
n1 <- fv("n_attrition"); n2 <- fv("n_no_attrition"); n <- fv("n_evaluable"); stopifnot(n1 + n2 == n)
m1 <- fv("os_median_attrition_months"); m2 <- fv("os_median_no_attrition_months")
mix_S <- function(t) (n1 / n) * 2^(-t / m1) + (n2 / n) * 2^(-t / m2)
m <- uniroot(function(t) mix_S(t) - 0.5, c(m1, m2), tol = 1e-12)$root          # months
S_esme <- function(t_months) 1 / (1 + ((t_months / 12) / P1$dr$scale)^P1$dr$shape)   # early-DR excess survival (log-logistic)
k <- log(0.5) / log(S_esme(m))
med_k <- function(kk) 12 * P1$dr$scale * (0.5^(-1 / kk) - 1)^(1 / P1$dr$shape)
stopifnot(abs(med_k(k) - m) < 1e-8)
D <- data.frame(quantity = c("n_evaluable", "n_no_first_line", "n_first_line", "os_median_no_first_line_months", "os_median_first_line_months",
                             "mixture_median_months", "esme_early_shape", "esme_early_median_months", "esme_early_excess_survival_at_m", "k_external",
                             "pembro_early_excess_median_months_at_k", "dfi_median_no_first_line_months", "dfi_median_first_line_months", "followup_median_months"),
                value = c(n, n1, n2, m1, m2, m, P1$dr$shape, 12 * P1$dr$scale, S_esme(m), k, med_k(k),
                          fv("dfi_median_attrition_months"), fv("dfi_median_no_attrition_months"), fv("followup_median_months")),
                source = c(rep(sprintf("Fedele 2026 p.%s", fp("n_evaluable")), 3), rep(sprintf("Fedele 2026 p.%s (abstract p.1)", fp("os_median_attrition_months")), 2),
                           "computed (17/52 : 35/52 mixture of exponentials)", "ESME fit (data/fits/esme_fits.rds)", "ESME fit", "computed", "computed: log(0.5) / log(S)",
                           "computed (check)", rep(sprintf("Fedele 2026 p.%s, Table 2", fp("dfi_median_attrition_months")), 2),
                           sprintf("Fedele 2026 p.%s", fp("followup_median_months"))))
write.csv(D, file.path(out, "kext_derivation.csv"), row.names = FALSE)
saveRDS(list(k = k, scope = "early", mixture_median_months = m, inputs = D, round = 14,
             note = "scenario early-DR k (external), Fedele 2026; other parameters from the base calibration"),
        file.path(ROOT, "data", "fits", "dr_k_external.rds"))
print(D, row.names = FALSE)

# gates under the scenario (same definitions and data as 05_calibrate.R, from the base run)
P <- P1; P$pembro_dr_k <- k; P$pembro_dr_k_scope <- "early"
arm_of <- c(pembro = "pembro", placebo = "chemo")
G <- read.csv(file.path(bdir, "calibration_gate.csv")); GR <- read.csv(file.path(bdir, "calibration_gate_rmst.csv"))
G7 <- read.csv(file.path(bdir, "calibration_final7y.csv"))
months <- 0:84
os <- lapply(arm_of, function(e) 100 * survival_engine(e, "all", times = months / 12, params = P)$OS)
efs7 <- sapply(arm_of, function(e) 100 * survival_engine(e, "all", times = 7, params = P)$EFS)
ga <- merge(G[, c("arm", "month", "km", "ci95_lo", "ci95_hi", "ci995_lo", "ci995_hi")],
            data.frame(arm = rep(names(os), each = 5), month = rep(c(12, 24, 36, 48, 60), 2),
                       scenario = unlist(lapply(os, function(v) v[c(12, 24, 36, 48, 60) + 1]))))
ga$inside <- ga$scenario >= ga$ci95_lo - 1e-9 & ga$scenario <= ga$ci95_hi + 1e-9
ga$inside_995 <- ga$scenario >= ga$ci995_lo - 1e-9 & ga$scenario <= ga$ci995_hi + 1e-9
a_ok <- all(ga$inside) || all(ga$inside_995)
rd5 <- rmst5_monthly(os$pembro / 100) - rmst5_monthly(os$placebo / 100)
b_ok <- rd5 >= GR$km_boot_ci95_lo && rd5 <= GR$km_boot_ci95_hi
g7 <- G7[G7$gate_c, c("id", "value", "ci95_lo", "ci95_hi")]
g7$scenario <- c(os7_pembro = os$pembro[85], os7_placebo = os$placebo[85], efs7_pembro = efs7[["pembro"]], efs7_placebo = efs7[["placebo"]])[g7$id]
g7$inside <- g7$scenario >= g7$ci95_lo - 1e-9 & g7$scenario <= g7$ci95_hi + 1e-9
c_ok <- all(g7$inside)
S <- rbind(data.frame(item = sprintf("OS %d y %s", ga$month / 12, ga$arm), reference = ga$km, lo = ga$ci95_lo, hi = ga$ci95_hi, scenario = ga$scenario, inside = ga$inside),
           data.frame(item = g7$id, reference = g7$value, lo = g7$ci95_lo, hi = g7$ci95_hi, scenario = g7$scenario, inside = g7$inside),
           data.frame(item = "rmst5_diff_years", reference = GR$km, lo = GR$km_boot_ci95_lo, hi = GR$km_boot_ci95_hi, scenario = rd5, inside = b_ok),
           data.frame(item = c("gate_a", "gate_b", "gate_c"), reference = NA, lo = NA, hi = NA, scenario = NA, inside = c(a_ok, b_ok, c_ok)))
S$k <- k
write.csv(S, file.path(out, "scenario_kext_gates.csv"), row.names = FALSE)
print(S, row.names = FALSE)
cat(sprintf("scenario early-DR k (external): m = %.3f months, k = %.4f; gates a %s, b %s, c %s\n", m, k, a_ok, b_ok, c_ok))
