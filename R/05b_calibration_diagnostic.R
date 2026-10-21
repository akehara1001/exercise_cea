# 05b_calibration_diagnostic.R
# Where the deaths of the first years come from in the calibrated engine (structures b and c of
# step 5), compared with the KM (Schmid 2024 Fig. 1A): background deaths, deaths after
# pre-surgery events (moved to DR), and deaths after post-surgery events.
# Output: output/phase1/calibration_diagnostic.csv

source("C:/Users/原明美/Documents/ClaudeCode/exercise_cea/R/config.R")
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
suppressPackageStartupMessages(library(survival))
ipd <- readRDS(file.path(ROOT, "data", "ipd", "ipd_all.rds"))
CAL <- read.csv(file.path(ROOT, "output", "phase1", "calibration.csv"), stringsAsFactors = FALSE)
km_at <- function(d, tm) summary(survfit(Surv(time, status) ~ 1, data = d), times = tm, extend = TRUE)$surv
P0 <- engine_params(dr_shape = 1, dr_scale = 1)
arm_of <- c(pembro = "pembro", placebo = "chemo")
months <- c(6, 12, 18, 24)

# deaths (%) by time for a parameter set; components by switching parts off
deaths <- function(P, arm, drug_hr = 1, no_pre = FALSE) {
  if (no_pre) for (b in c("pCR", "nonpCR")) P$pre_surv[[arm]][[b]]$surv[] <- 1
  e <- survival_engine(arm_of[[arm]], "all", times = months / 12, params = P, nonpcr_mix = NULL)
  if (drug_hr != 1) {
    # all post-surgery excess EFS events switched off (pCR and non-pCR) through the drug-HR hook
    pp <- P$p_pcr[[arm]]
    rb <- function(b) run_branch(P$efs[[arm]][[b]], P$pre_surv[[arm]][[b]], P$shares[[arm]], P$lrr_dr[["rate"]],
                                 P$dr_shape, P$dr_scale, P$start_age, P$L, P$cycle, P$n_cycles, P$n_tunnel, NULL, drug_hr)
    a <- rb("pCR"); n <- rb("nonpCR")
    dead <- pp * a$Dead + (1 - pp) * n$Dead
    return(100 * approx(a$time, dead, xout = months / 12)$y)
  }
  100 * e$Dead
}
out <- list()
for (st in c("b", "c")) for (arm in names(arm_of)) {
  r <- CAL[CAL$structure == st & CAL$arm == arm, ]
  if (nrow(r) == 0) next
  P <- P0; P$dr_shape <- r$dr_shape; P$dr_scale <- r$dr_scale; P$dr_by_arm <- NULL
  full <- deaths(P, arm)
  bg_pre <- deaths(P, arm, drug_hr = 0)                 # background + pre-surgery events only
  bg <- deaths(P, arm, drug_hr = 0, no_pre = TRUE)      # background only
  km <- 100 * (1 - km_at(ipd[[paste0("K24_F1A_OS_", arm)]], months))
  out[[length(out) + 1]] <- data.frame(structure = st, arm = arm, month = months, km_deaths_pct = round(km, 3),
                                       engine_deaths_pct = round(full, 3), background_pct = round(bg, 3),
                                       after_presurgery_events_pct = round(bg_pre - bg, 3),
                                       after_postsurgery_events_pct = round(full - bg_pre, 3),
                                       dr_shape = r$dr_shape, dr_scale = r$dr_scale)
}
D <- do.call(rbind, out)
write.csv(D, file.path(ROOT, "output", "phase1", "calibration_diagnostic.csv"), row.names = FALSE)
print(D, row.names = FALSE)
# pre-surgery event fraction by arm (share of the arm entering DR before surgery)
for (arm in names(arm_of)) cat(sprintf("%s: pre-surgery events %.2f%% of the arm (non-pCR branch KM at %d months)\n", arm,
                                       100 * (1 - P0$p_pcr[[arm]]) * (1 - tail(P0$pre_surv[[arm]]$nonpCR$surv, 1)), CFG$landmark_months))
