# 03b_validation_plots.R
# Digitized step curves vs KM of the reconstructed IPD, with the reported milestones
# (+-1 percentage point band). Output: output/phase1/fig_validation_<fig>.png

root <- Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea")
suppressPackageStartupMessages({
  library(survival)
  library(ggplot2)
})
dig <- file.path(root, "data", "digitized")
out_dir <- file.path(root, "output", "phase1")
ipd <- readRDS(file.path(root, "data", "ipd", "ipd_all.rds"))
V <- read.csv(file.path(out_dir, "validation.csv"), stringsAsFactors = FALSE)

figs <- unique(vapply(ipd, function(d) d$fig[1], ""))
for (fig in figs) {
  keys <- names(ipd)[vapply(ipd, function(d) d$fig[1] == fig, TRUE)]
  dd <- do.call(rbind, lapply(keys, function(k) {
    d <- ipd[[k]]
    cv <- read.csv(file.path(dig, sprintf("%s_%s_curve.csv", fig, d$arm[1])))
    km <- survfit(Surv(time, status) ~ 1, data = d)
    rbind(data.frame(arm = d$arm[1], source = "digitized", time = cv$time, surv = cv$surv_pct),
          data.frame(arm = d$arm[1], source = "reconstructed IPD (KM)", time = c(0, km$time), surv = 100 * c(1, km$surv)))
  }))
  ms <- V[V$check == "milestone" & startsWith(V$curve, fig), ]
  ms$arm <- sub(paste0(fig, "_"), "", ms$curve)
  unit <- if (startsWith(fig, "Y22")) "years" else "months"
  p <- ggplot(dd, aes(time, surv, colour = source, linetype = source)) +
    geom_step(linewidth = 0.5) +
    geom_errorbar(data = ms, aes(x = time, ymin = reported - 1, ymax = reported + 1), inherit.aes = FALSE,
                  width = 0, colour = "grey20", linewidth = 0.6) +
    geom_point(data = ms, aes(x = time, y = reported), inherit.aes = FALSE, shape = 21, fill = "white", size = 1.8) +
    facet_wrap(~arm, nrow = 1) +
    scale_colour_manual(values = c("digitized" = "grey55", "reconstructed IPD (KM)" = "#C0392B")) +
    scale_linetype_manual(values = c("digitized" = "solid", "reconstructed IPD (KM)" = "22")) +
    labs(title = fig, subtitle = "points: reported milestone, bar: +-1 percentage point",
         x = paste0("Time (", unit, ")"), y = "Survival (%)", colour = NULL, linetype = NULL) +
    coord_cartesian(ylim = c(max(0, min(dd$surv) - 5), 100)) +
    theme_bw(base_size = 9) + theme(legend.position = "bottom")
  ggsave(file.path(out_dir, sprintf("fig_validation_%s.png", fig)), p,
         width = 2.6 * length(keys) + 1, height = 3.4, dpi = 200)
  cat("wrote", sprintf("fig_validation_%s.png", fig), "\n")
}
