# test_engine_interface.R
# Checks that the engine interface supports the phase-2 scenarios (docs/model_spec.md). The
# weights and HRs below are test inputs only, not model inputs.
source("C:/Users/原明美/Documents/ClaudeCode/exercise_cea/R/config.R")
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
suppressPackageStartupMessages(library(survival))
# engine default if a calibration passed its gate; otherwise the step-5 candidate, for the test only
ep <- file.path(ROOT, "data", "fits", "engine_params.rds")
P <- if (file.exists(ep)) readRDS(ep) else readRDS(file.path(ROOT, "data", "fits", "calibration_candidates.rds"))$params
cat("parameters:", if (file.exists(ep)) "engine default" else "calibration candidate (gate failed), not adopted", "\n")
tt <- c(1, 3, 5, 10, 20)
row <- function(name, r) data.frame(test = name, t(setNames(round(100 * r$EFS, 3), paste0("EFS_", tt, "y"))),
                                    t(setNames(round(100 * r$OS, 3), paste0("OS_", tt, "y"))), check.names = FALSE)
base <- survival_engine("chemo", "all", tt, P)
same1 <- survival_engine("chemo", "all", tt, P, nonpcr_mix = data.frame(group = c("a", "b"), weight = c(0.3, 0.7), hr = c(1, 1)))
ex1 <- do.call(survival_engine, c(list("exercise", "all", tt, P), exercise_args(P, hr0 = 1, delay_years = 1, wane_rate = 0.5)))
mix <- sjp_mix(F01 = 0.5, F03 = 0.1, F04 = 0.8, hr_cap = 0.58, hr_ola = 0.65)
sjp <- survival_engine("chemo", "all", tt, P, nonpcr_mix = mix)
sjp_ex <- do.call(survival_engine, c(list("exercise", "all", tt, P, nonpcr_mix = mix),
                                     exercise_args(P, hr0 = 0.8, delay_years = 0.5, wane_rate = 0.5, continue_months = 6)))
pathB <- survival_engine("exercise", "all", tt, P, p_pcr = P$p_pcr[["placebo"]] + 0.05)
pem_sjp <- survival_engine("pembro", "all", tt, P, nonpcr_mix = mix)
pem <- survival_engine("pembro", "all", tt, P)
# scenario k = 1 (common post-DR mortality): acts on the pembrolizumab arms only, OS only
chemo_k1 <- survival_engine("chemo", "all", tt, P, common_dr = TRUE)
pem_k1 <- survival_engine("pembro", "all", tt, P, common_dr = TRUE)
out <- rbind(row("chemo base", base), row("nonpcr_mix with all HR = 1", same1), row("exercise path A with hr0 = 1", ex1),
             row("S-JP (test weights)", sjp), row("S-JP + exercise path A, 6 months continued (test values)", sjp_ex),
             row("exercise path B: pCR + 5 points (test value)", pathB), row("pembro base", pem), row("pembro + S-JP (test weights)", pem_sjp),
             row("chemo with common_dr = TRUE (no effect)", chemo_k1), row("pembro, scenario k = 1", pem_k1))
stopifnot(max(abs(same1[, -1] - base[, -1])) < 1e-12, max(abs(ex1[, -1] - base[, -1])) < 1e-12,
          all(sjp$EFS >= base$EFS - 1e-12), all(pathB$EFS >= base$EFS - 1e-12),
          max(abs(chemo_k1[, -1] - base[, -1])) < 1e-12, max(abs(pem_k1$EFS - pem$EFS)) < 1e-12,
          P$pembro_dr_k <= 1 || all(pem_k1$OS[-1] > pem$OS[-1]))
write.csv(out, file.path(ROOT, "output", "phase1", "engine_interface_test.csv"), row.names = FALSE)
print(out, row.names = FALSE)
cat("S-JP test weights:\n"); print(mix)
