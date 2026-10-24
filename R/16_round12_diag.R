# 16_round12_diag.R
# Round 12 (docs/acceptance_rule_round12.md, git a1625c1): where the engine EFS departs from the
# step-4 fitted curves (KM of the branch at surgery x selected post-surgery EFS model), by source.
# For each branch (arm x pCR) and year 1, 2, 3, 5, 7, 10 the log ratio engine / fit is split into
#   A pre-surgery background deaths   (hb over [0, L), added in branch_flows())
#   B pre-surgery AE deaths           (ae_rate over [0, L), added)
#   C PreProg vs the KM drop          (log(1 - q_pre) - log KM(L): PreProg is the reported share, the
#                                      fit uses the KM drop to surgery, which holds all pre-surgery events)
#   D post-surgery background floor   (non-cure models: excess = max(dH - hb, 0), so the engine hazard
#                                      exceeds the fitted hazard where dH < hb)
#   E other (residual)
# and converted to points as fit x log term (first order; E takes the rest). Settings: round 10
# (data/fits/engine_params.rds) and round 11 revised (data/fits/round11/equality/calibration_candidates.rds).
# Environment variable ENGINE_FILE: the engine to source (default R/engine.R). The pre-fix engine is
# R/engine.R at git a1625c1; the terms A-D describe it (with the fixed engine E carries them back).
# Output (tag = ENGINE_TAG, default "fixed"): output/phase1/round12/diag_engine_vs_fit_<tag>.csv,
# diag_branch_inputs.csv
# Usage: [ENGINE_FILE=... ENGINE_TAG=prefix] Rscript R/16_round12_diag.R [label params.rds] ...

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R")); source(Sys.getenv("ENGINE_FILE", file.path(ROOT, "R", "engine.R")))
tag <- Sys.getenv("ENGINE_TAG", "fixed")
out <- file.path(ROOT, "output", "phase1", "round12"); dir.create(out, showWarnings = FALSE, recursive = TRUE)
args <- commandArgs(trailingOnly = TRUE)
sets <- if (length(args) >= 2) setNames(as.list(args[seq(2, length(args), 2)]), args[seq(1, length(args), 2)]) else
  list(round10 = file.path(ROOT, "data", "fits", "engine_params.rds"),
       round11 = file.path(ROOT, "data", "fits", "round11", "equality", "calibration_candidates.rds"))
load_P <- function(f) { x <- readRDS(f); if (!is.null(x$params)) x$params else x }
YRS <- c(1, 2, 3, 5, 7, 10)
arm_of <- c(pembro = "pembro", placebo = "chemo")
rows <- list(); inp <- list()
for (lab in names(sets)) {
  P <- load_P(sets[[lab]])
  L <- P$L; cyc <- P$cycle; a0 <- P$start_age + L
  for (a in names(arm_of)) for (b in c("pCR", "nonpCR")) {
    sp <- P$efs[[a]][[b]]; ps <- P$pre_surv[[a]][[b]]; q <- P$q_pre[[a]][[b]]; ae <- P$ae[[a]][["rate"]]
    km_L <- approx(ps$time, ps$surv, xout = L + 1e-9, method = "constant", f = 0, rule = 2)$y
    K <- round(max(YRS) / cyc); t <- (0:K) * cyc
    hb <- H_pop(P$start_age + t[-(K + 1)], cyc)
    post <- t[-(K + 1)] >= L - 1e-9
    tau0 <- pmax(t[-(K + 1)] - L, 0); tau1 <- pmax(t[-1] - L, 0)
    dH <- -log(pmax(spec_surv(sp, tau1), 1e-300)) + log(pmax(spec_surv(sp, tau0), 1e-300))
    floor_term <- if (sp$family == "cure") rep(0, K) else ifelse(post, pmax(dH, hb) - dH, 0)
    dHA <- ae * pmax(pmin(t[-1], P$ae_end) - pmin(t[-(K + 1)], P$ae_end), 0)
    eng <- 100 * survival_engine(arm_of[[a]], b, times = YRS, params = P)$EFS
    fit <- 100 * km_L * allcause_surv(sp, YRS - L, a0)
    for (i in seq_along(YRS)) {
      n <- round(YRS[i] / cyc)
      A <- -sum(hb[seq_len(n)][!post[seq_len(n)]]); B <- -sum(dHA[seq_len(n)][!post[seq_len(n)]])
      C <- log(1 - q) - log(km_L); D <- -sum(floor_term[seq_len(n)])
      d <- eng[i] - fit[i]
      pp <- fit[i] * c(A, B, C, D)
      rows[[length(rows) + 1]] <- data.frame(setting = lab, arm = a, stratum = b, year = YRS[i], fit = round(fit[i], 4), engine = round(eng[i], 4),
        diff = round(d, 4), A_pre_background = round(pp[1], 4), B_pre_ae_deaths = round(pp[2], 4), C_preprog_vs_km = round(pp[3], 4),
        D_post_background_floor = round(pp[4], 4), E_other = round(d - sum(pp), 4))
    }
    inp[[length(inp) + 1]] <- data.frame(setting = lab, arm = a, stratum = b, family = sp$family, km_at_surgery = round(km_L, 5),
      km_drop_to_surgery = round(1 - km_L, 5), q_pre = round(q, 5), ae_deaths_prob = round(P$ae[[a]][["prob"]], 5),
      ae_rate_per_year = round(ae, 5), background_cumhaz_pre = round(sum(hb[!post]), 5),
      floor_active_cycles_to_10y = sum(floor_term > 0))
  }
}
R <- do.call(rbind, rows); I <- do.call(rbind, inp)
write.csv(R, file.path(out, sprintf("diag_engine_vs_fit_%s.csv", tag)), row.names = FALSE)
write.csv(I, file.path(out, "diag_branch_inputs.csv"), row.names = FALSE)
print(I, row.names = FALSE)
print(R[R$year %in% c(1, 7, 10), ], row.names = FALSE)
cat("max |engine - fit| (points):", round(max(abs(R$diff)), 4), "; max |E_other|:", round(max(abs(R$E_other)), 4), "\n")
