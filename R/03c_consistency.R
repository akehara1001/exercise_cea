# 03c_consistency.R
# Consistency of the pCR-stratified EFS (Schmid 2022 appendix Fig. S4, IA4) with the overall
# EFS by arm: mixture S_mix(t) = p * S_pCR(t) + (1 - p) * S_nonpCR(t), p = pCR proportion of
# the same analysis (IA4: pCR counts in the main-text sentence on Fig. S4).
# Compared with the overall EFS of the same cutoff (Schmid 2022 Fig. 1, IA4) and, because the
# stratified curves are from 2022, also with the 2024 overall EFS (Fig. 2A, IA7).
# Comparison times, fixed before running: every 3 months from 3 months up to the last risk-table
# time at which all four strata of Fig. S4 still have >= 20 patients at risk.
# Gate: |S_mix - S_overall| <= 1 percentage point at every time, both arms, both years.
# Outputs: output/phase1/consistency_check.csv, output/phase1/fig_consistency_pCR_mixture.png

root <- Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea")
suppressPackageStartupMessages({
  library(survival)
  library(ggplot2)
})
out_dir <- file.path(root, "output", "phase1")
ipd <- readRDS(file.path(root, "data", "ipd", "ipd_all.rds"))
pc <- read.csv(file.path(root, "data", "pcr_counts.csv"), stringsAsFactors = FALSE)
pc <- pc[startsWith(pc$source, "K22"), ]          # same analysis as the stratified curves
p <- c(pembro = pc$pcr_pembro / (pc$pcr_pembro + pc$nonpcr_pembro),
       placebo = pc$pcr_placebo / (pc$pcr_placebo + pc$nonpcr_placebo))

rt <- read.csv(file.path(root, "data", "digitized", "K22_S4_EFS_pCR_risktable.csv"))
min_at_risk <- tapply(rt$n_risk, rt$time, min)
t_max <- max(as.numeric(names(min_at_risk))[min_at_risk >= 20])
grid <- seq(3, t_max, by = 3)

km_at <- function(d, t) 100 * summary(survfit(Surv(time, status) ~ 1, data = d), times = t, extend = TRUE)$surv
res <- list()
for (arm in names(p)) {
  s_pcr <- km_at(ipd[[paste0("K22_S4_EFS_pCR_", arm, "_pCR")]], grid)
  s_non <- km_at(ipd[[paste0("K22_S4_EFS_pCR_", arm, "_nonpCR")]], grid)
  s_mix <- p[[arm]] * s_pcr + (1 - p[[arm]]) * s_non
  for (ref in c("K22_F1_EFS", "K24_F2A_EFS")) {
    s_all <- km_at(ipd[[paste0(ref, "_", arm)]], grid)
    res[[length(res) + 1]] <- data.frame(
      arm = arm, comparator = ref, time_months = grid, p_pCR = round(p[[arm]], 4),
      mixture = round(s_mix, 3), overall = round(s_all, 3), diff = round(s_mix - s_all, 3),
      pass = abs(s_mix - s_all) <= 1 + 1e-9)
  }
}
R <- do.call(rbind, res)
write.csv(R, file.path(out_dir, "consistency_check.csv"), row.names = FALSE)
cat(sprintf("grid 3..%g months (all strata >= 20 at risk); p_pCR pembro %.4f placebo %.4f\n", t_max, p[["pembro"]], p[["placebo"]]))
print(aggregate(abs(diff) ~ arm + comparator, data = R, FUN = max))
cat("failing comparisons:", sum(!R$pass), "\n")
if (any(!R$pass)) print(R[!R$pass, ], row.names = FALSE)

pd <- rbind(data.frame(R[, c("arm", "comparator", "time_months")], curve = "pCR mixture (2022 Fig. S4)", surv = R$mixture),
            data.frame(R[, c("arm", "comparator", "time_months")], curve = "overall", surv = R$overall))
pd$comparator <- factor(pd$comparator, levels = c("K22_F1_EFS", "K24_F2A_EFS"),
                        labels = c("vs 2022 Fig. 1 (IA4)", "vs 2024 Fig. 2A (IA7)"))
g <- ggplot(pd, aes(time_months, surv, colour = curve)) +
  geom_line() + geom_point(size = 1) +
  facet_grid(arm ~ comparator) +
  scale_colour_manual(values = c("overall" = "grey30", "pCR mixture (2022 Fig. S4)" = "#C0392B")) +
  labs(x = "Months from randomization", y = "EFS (%)", colour = NULL,
       title = "pCR-weighted mixture of stratified EFS vs overall EFS") +
  theme_bw(base_size = 9) + theme(legend.position = "bottom")
ggsave(file.path(out_dir, "fig_consistency_pCR_mixture.png"), g, width = 7, height = 5, dpi = 200)
