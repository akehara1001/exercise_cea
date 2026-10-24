# 14_round10_decision.R
# Round 10 (2026-10-23): decide between the round-8 and round-9 structures from long-term survival
# after distant recurrence, by the rule fixed before this script was run
# (docs/acceptance_rule_round10.md, git e8d2134).
#   - survival 1, 2, 3 and 4 years after DR (12-48 months), early and late relapse: implied by
#     round 8 (data/fits/round8/engine_params.rds) and round 9 (data/fits/calibration_candidates.rds)
#     = excess log-logistic survival x background survival from age 50.5, k = 1; against the
#     ESME reconstructed KM (data/ipd/esme/esme_ipd.rds) with its pointwise 95% CI (survfit
#     default, log scale); year 4 = 48 months (the reconstruction ends at 47.98 months).
#   - rule A: round 8 outside the ESME 95% CI at year 3 or 4 in either group -> round 9 structure;
#     rule B: round 8 inside at years 3 and 4 in both groups -> round 8 stays final.
#   - reported only: mean survival after DR to the lifetime horizon (age 100) by round and group;
#     expected time in the DR state (undiscounted, lifetime) of the engine by arm, rounds 8 and 9.
# Outputs: output/phase1/round10/dr_survival_comparison.csv, mean_survival_after_dr.csv,
#          dr_time_engine.csv, decision.csv, fig_dr_survival.png

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
suppressPackageStartupMessages({
  library(survival)
  library(ggplot2)
})
out_dir <- file.path(ROOT, "output", "phase1", "round10")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
P8 <- readRDS(file.path(ROOT, "data", "fits", "round8", "engine_params.rds"))
P9 <- readRDS(file.path(ROOT, "data", "fits", "calibration_candidates.rds"))$params
esme <- readRDS(file.path(ROOT, "data", "ipd", "esme", "esme_ipd.rds"))
groups <- c(early = "early", late = "late")
entry_age <- CFG$start_age + 1.5
horizon <- 100 - entry_age

# implied all-cause survival after DR (k = 1): excess log-logistic x background from age 50.5
dr_spec <- function(P, g) if (g == "early") P$dr else dr_late_spec(P$dr)
S_impl <- function(P, g, t) exp(-dr_cumhaz(dr_spec(P, g), t)) * S_pop(entry_age, t)

# ---------------------------------------------------------------- survival at 1-4 years
yrs <- 1:4
DS <- do.call(rbind, lapply(groups, function(g) {
  km <- survfit(Surv(time, status) ~ 1, data = esme[[g]])
  s <- summary(km, times = 12 * yrs, extend = TRUE)
  data.frame(group = g, year = yrs, months = 12 * yrs,
             round8 = 100 * S_impl(P8, g, yrs), round9 = 100 * S_impl(P9, g, yrs),
             esme_km = 100 * s$surv, esme_lo = 100 * s$lower, esme_hi = 100 * s$upper, esme_n_risk = s$n.risk)
}))
DS$round8_inside <- DS$round8 >= DS$esme_lo & DS$round8 <= DS$esme_hi
DS$round9_inside <- DS$round9 >= DS$esme_lo & DS$round9 <= DS$esme_hi
DS$used_in_rule <- DS$year %in% c(3, 4)
write.csv(DS, file.path(out_dir, "dr_survival_comparison.csv"), row.names = FALSE)
print(transform(DS, round8 = round(round8, 2), round9 = round(round9, 2), esme_km = round(esme_km, 2), esme_lo = round(esme_lo, 2), esme_hi = round(esme_hi, 2)), row.names = FALSE)

# ---------------------------------------------------------------- decision
rule_pts <- DS[DS$used_in_rule, ]
rule <- if (any(!rule_pts$round8_inside)) "A" else "B"
DEC <- data.frame(rule = rule, adopted = if (rule == "A") "round 9" else "round 8",
                  round8_points_outside = paste(with(rule_pts[!rule_pts$round8_inside, ], sprintf("%s year %d", group, year)), collapse = "; "),
                  n_rule_points = nrow(rule_pts), n_round8_inside = sum(rule_pts$round8_inside), n_round9_inside = sum(rule_pts$round9_inside),
                  rule_file = "docs/acceptance_rule_round10.md", rule_commit = "e8d2134")
write.csv(DEC, file.path(out_dir, "decision.csv"), row.names = FALSE)
cat(sprintf("rule %s -> adopt %s (round 8 outside at: %s)\n", rule, DEC$adopted, if (nzchar(DEC$round8_points_outside)) DEC$round8_points_outside else "none"))

# ---------------------------------------------------------------- mean survival after DR
tt <- seq(0, horizon, by = 1 / 120)
trap <- function(x, y) sum(diff(x) * (head(y, -1) + tail(y, -1)) / 2)
t48 <- tt[tt <= 4 + 1e-9]
MS <- do.call(rbind, lapply(groups, function(g) {
  km <- survfit(Surv(time / 12, status) ~ 1, data = esme[[g]])
  data.frame(group = g,
             round8_mean_lifetime_years = trap(tt, S_impl(P8, g, tt)), round9_mean_lifetime_years = trap(tt, S_impl(P9, g, tt)),
             round8_rmst48_years = trap(t48, S_impl(P8, g, t48)), round9_rmst48_years = trap(t48, S_impl(P9, g, t48)),
             esme_km_rmst48_years = summary(km, rmean = max(esme[[g]]$time) / 12)$table[["rmean"]],
             esme_km_rmst_horizon_years = max(esme[[g]]$time) / 12, horizon_years = horizon)
}))
MS$diff_mean_lifetime_years <- MS$round9_mean_lifetime_years - MS$round8_mean_lifetime_years
write.csv(MS, file.path(out_dir, "mean_survival_after_dr.csv"), row.names = FALSE)
print(MS, row.names = FALSE)

# ---------------------------------------------------------------- engine: time in DR (undiscounted)
dr_time <- function(P, arm, cd = FALSE) { e <- survival_engine(arm, "all", params = P, common_dr = cd); trap(e$time, e$DR) }
DT <- do.call(rbind, lapply(list(c("chemo", FALSE), c("pembro", FALSE), c("pembro", TRUE)), function(a) {
  cd <- as.logical(a[2])
  data.frame(arm = a[1], scenario = if (cd) "k = 1" else "base", round8_years = dr_time(P8, a[1], cd), round9_years = dr_time(P9, a[1], cd),
             round8_k = if (a[1] == "pembro" && !cd) P8$pembro_dr_k else 1, round9_k = if (a[1] == "pembro" && !cd) P9$pembro_dr_k else 1)
}))
DT$diff_years <- DT$round9_years - DT$round8_years
DT$diff_months <- 12 * DT$diff_years
write.csv(DT, file.path(out_dir, "dr_time_engine.csv"), row.names = FALSE)
print(DT, row.names = FALSE)

# ---------------------------------------------------------------- figure
tg <- seq(0, 5, by = 1 / 48)
pl <- do.call(rbind, lapply(groups, function(g) {
  km <- survfit(Surv(time, status) ~ 1, data = esme[[g]])
  rbind(data.frame(group = g, curve = "ESME KM (reconstructed)", t = c(0, km$time) / 12, s = 100 * c(1, km$surv)),
        data.frame(group = g, curve = "round 8 implied", t = tg, s = 100 * S_impl(P8, g, tg)),
        data.frame(group = g, curve = "round 9 implied", t = tg, s = 100 * S_impl(P9, g, tg)))
}))
p <- ggplot() + geom_step(data = pl[pl$curve == "ESME KM (reconstructed)", ], aes(12 * t, s, colour = curve)) +
  geom_line(data = pl[pl$curve != "ESME KM (reconstructed)", ], aes(12 * t, s, colour = curve)) +
  geom_errorbar(data = DS, aes(x = months, ymin = esme_lo, ymax = esme_hi), width = 1.2, colour = "grey30") +
  facet_wrap(~group) + scale_colour_manual(values = c("ESME KM (reconstructed)" = "black", "round 8 implied" = "#C0392B", "round 9 implied" = "#2E86C1")) +
  labs(x = "Months after distant recurrence", y = "Survival (%)", colour = NULL, title = "Survival after DR: rounds 8 and 9 (k = 1) vs ESME, bars: 95% CI at 12-48 months") +
  theme_bw(base_size = 9) + theme(legend.position = "bottom")
ggsave(file.path(out_dir, "fig_dr_survival.png"), p, width = 8, height = 4, dpi = 200)
