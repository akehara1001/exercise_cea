# 05r_final7y_precheck.R
# Record before round 7 (2026-10-22): the round-6 engine (data/fits/engine_params.rds, k as
# calibrated) and its scenario k = 1 at 7 years, against the KEYNOTE-522 final analysis
# (data/kn522_final_7y.csv): OS and EFS by arm (with 95% CIs), OS by pCR status, DRFS.
# Output: output/phase1/r6_vs_final7y.csv (written once, before the round-7 calibration)

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
suppressPackageStartupMessages(library(survival))
P <- readRDS(file.path(ROOT, "data", "fits", "engine_params.rds"))
FA <- read.csv(file.path(ROOT, "data", "kn522_final_7y.csv"), stringsAsFactors = FALSE)
fv <- function(id, col = "value") suppressWarnings(as.numeric(FA[[col]][FA$id == id]))
rows <- list()
for (sc in c("base", "k = 1")) for (arm in c("pembro", "chemo")) for (pc in c("all", "pCR", "nonpCR")) {
  e <- survival_engine(arm, pc, times = 7, params = P, common_dr = sc == "k = 1")
  a <- if (arm == "pembro") "pembro" else "placebo"
  add <- function(ep, model, id) rows[[length(rows) + 1]] <<- data.frame(scenario = sc, arm = a, pcr = pc, endpoint = ep, year = 7,
    model = 100 * model, reported = fv(id), ci95_lo = fv(id, "lo"), ci95_hi = fv(id, "hi"), source = FA$outlet[FA$id == id])
  if (pc == "all") {
    add("OS", e$OS, paste0("os7_", a)); add("EFS", e$EFS, paste0("efs7_", a)); add("DRFS", e$DRFS, paste0("drfs7_", a))
  } else add("OS", e$OS, paste0(if (pc == "pCR") "os_pcr_" else "os_nonpcr_", a))
}
R <- do.call(rbind, rows)
R$diff <- R$model - R$reported
R$inside_ci <- ifelse(is.na(R$ci95_lo), NA, R$model >= R$ci95_lo & R$model <= R$ci95_hi)
R$pembro_dr_k <- P$pembro_dr_k
out <- file.path(ROOT, "output", "phase1", "r6_vs_final7y.csv")
write.csv(R, out, row.names = FALSE)
print(transform(R, model = round(model, 2), diff = round(diff, 2)), row.names = FALSE)
