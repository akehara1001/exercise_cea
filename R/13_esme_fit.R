# 13_esme_fit.R
# Round 9 (2026-10-23): survival after distant recurrence anchored on the ESME curves (Grinda et
# al., Eur J Cancer 2023;189:112935, Fig. 3a, HAL hal-04205902; OS from the diagnosis of
# metastasis, early relapse = within 12 months of the end of neo/adjuvant chemotherapy).
#   1. Guyot reconstruction of the two digitized curves (R/py/02b_digitize_raster.py with
#      R/py/rasterspec_esme.json -> data/digitized/esme/), cross-checked against IPDfromKM, as for
#      KEYNOTE-522 (03_reconstruct_ipd.R).
#   2. Gates (user, 2026-10-23): KM median of the reconstruction within 0.5 months of the reported
#      median (10.1, 17.1); at each risk-table time, reconstructed KM within 1 percentage point of
#      the digitized curve. Not met: stop (no fit is saved).
#   3. Log-logistic fit to each curve (flexsurv; shape and median = scale, with 95% CIs) and a
#      common-shape model (group on the scale only); likelihood-ratio test of separate vs common
#      shape. Rule: separate shapes if p < 0.05, otherwise one common shape.
# The fitted log-logistic is used in the engine as the excess hazard after DR (the background
# hazard is added on top), as the ESME medians were in rounds 5-8: the OS of the cohort includes
# background deaths, a small difference over the few years after metastasis at age ~50.
# Outputs: data/ipd/esme/ESME_F3A_OS_<group>.csv, data/fits/esme_fits.rds (accepted only),
#          output/phase1/round9/esme_validation.csv, esme_diagnostics.csv, esme_fits.csv,
#          esme_shape_test.csv, fig_esme_fit.png

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "guyot.R"))
suppressPackageStartupMessages({
  library(survival)
  library(flexsurv)
  library(IPDfromKM)
  library(jsonlite)
  library(ggplot2)
})
dig <- file.path(ROOT, "data", "digitized", "esme")
ipd_dir <- file.path(ROOT, "data", "ipd", "esme")
out_dir <- file.path(ROOT, "output", "phase1", "round9")
dir.create(ipd_dir, showWarnings = FALSE, recursive = TRUE)
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
spec <- fromJSON(file.path(ROOT, "R", "py", "rasterspec_esme.json"), simplifyVector = FALSE)$figures[[1]]
fig <- spec$fig_id
groups <- c("early", "late")
rep_med <- spec$reported_in_image$median_os_months

# ---------------------------------------------------------------- reconstruction
rt <- read.csv(file.path(dig, paste0(fig, "_risktable.csv")))
ipd <- list(); DG <- list(); V <- list()
for (g in groups) {
  cv <- read.csv(file.path(dig, sprintf("%s_%s_curve.csv", fig, g)))
  r <- rt[rt$arm == g, ]
  prep <- guyot_prepare(cv$time, cv$surv_pct / 100, r$time, r$n_risk)
  gy <- guyot(prep)
  pk <- structure(list(
    preprocessdat = data.frame(time = prep$t.S, surv = prep$S, id = seq_along(prep$t.S),
                               interval = findInterval(seq_along(prep$t.S), prep$lower)),
    intervalIndex = data.frame(interval = seq_along(prep$t.risk), lower = prep$lower, upper = prep$upper,
                               t.risk = prep$t.risk, n.risk = prep$n.risk),
    endpts = NULL, inputdat = data.frame(time = cv$time, surv = cv$surv_pct / 100)), class = "preKM")
  gi <- tryCatch(getIPD(pk, armID = 1)$IPD, error = function(e) NULL)
  d <- data.frame(group = g, time = gy$time, time_years = gy$time / 12, status = gy$status)
  ipd[[g]] <- d
  write.csv(d, file.path(ipd_dir, sprintf("%s_%s.csv", fig, g)), row.names = FALSE)
  km <- survfit(Surv(time, status) ~ 1, data = d)
  grid <- sort(unique(prep$t.S))
  s_ipd <- summary(km, times = grid, extend = TRUE)$surv
  s_dig <- vapply(grid, function(t) min(prep$S[prep$t.S <= t + 1e-9]), 0)
  s2 <- if (!is.null(gi)) summary(survfit(Surv(time, status) ~ 1, data = gi), times = grid, extend = TRUE)$surv else NA
  nr_ok <- r$time <= max(prep$t.S)
  nr <- vapply(r$time, function(t) sum(d$time >= t - 1e-9), 0)
  DG[[g]] <- data.frame(curve = g, n = nrow(d), events_guyot = sum(d$status), events_ipdfromkm = if (!is.null(gi)) sum(gi$status) else NA,
                        max_abs_km_vs_digitized_pp = 100 * max(abs(s_ipd - s_dig)),
                        max_abs_guyot_vs_ipdfromkm_pp = 100 * max(abs(s_ipd - s2)),
                        max_abs_risk_table_diff = max(abs(nr[nr_ok] - r$n_risk[nr_ok])))
  # gate 1: median
  med <- unname(summary(km)$table["median"])
  V[[length(V) + 1]] <- data.frame(curve = g, check = "median (months)", time = NA, reported = rep_med[[g]][[1]], reconstructed = med,
                                   abs_diff = abs(med - rep_med[[g]][[1]]), tolerance = 0.5, pass = abs(med - rep_med[[g]][[1]]) <= 0.5 + 1e-9)
  # gate 2: KM at the risk-table times vs the digitized curve (within the digitized range)
  tt <- r$time[nr_ok]
  s_km <- 100 * summary(km, times = tt, extend = TRUE)$surv
  s_dg <- 100 * vapply(tt, function(t) min(prep$S[prep$t.S <= t + 1e-9]), 0)
  V[[length(V) + 1]] <- data.frame(curve = g, check = "survival at risk-table time (%)", time = tt, reported = s_dg, reconstructed = s_km,
                                   abs_diff = abs(s_km - s_dg), tolerance = 1, pass = abs(s_km - s_dg) <= 1 + 1e-9)
}
V <- do.call(rbind, V); DG <- do.call(rbind, DG)
names(V)[names(V) == "reported"] <- "reference"
V$reference_source <- ifelse(V$check == "median (months)", "reported median (Fig. 3a inset, abstract)", "digitized curve")
write.csv(V, file.path(out_dir, "esme_validation.csv"), row.names = FALSE)
write.csv(DG, file.path(out_dir, "esme_diagnostics.csv"), row.names = FALSE)
print(DG, row.names = FALSE)
print(V[!V$pass | V$check == "median (months)", ], row.names = FALSE)
pass <- all(V$pass)
cat(sprintf("ESME reconstruction gates: %d/%d pass -> %s\n", sum(V$pass), nrow(V), if (pass) "PASS" else "FAIL"))
# reconstructed hazard ratio early vs late (report only; the figure prints 1.70 [1.54, 1.88])
both <- rbind(ipd$early, ipd$late); both$early <- as.integer(both$group == "early")
cx <- coxph(Surv(time, status) ~ early, data = both)
HR <- data.frame(reported = spec$reported_in_image$hr[[1]]$hr, lo = spec$reported_in_image$hr[[1]]$lo, hi = spec$reported_in_image$hr[[1]]$hi,
                 reconstructed = exp(coef(cx)), rec_lo = exp(confint(cx))[1], rec_hi = exp(confint(cx))[2])
write.csv(HR, file.path(out_dir, "esme_hr.csv"), row.names = FALSE)
print(HR, row.names = FALSE)
if (!pass) {
  if (file.exists(file.path(ROOT, "data", "fits", "esme_fits.rds"))) file.remove(file.path(ROOT, "data", "fits", "esme_fits.rds"))
  stop("ESME reconstruction did not meet the gates: stop (no fit saved)")
}
saveRDS(ipd, file.path(ipd_dir, "esme_ipd.rds"))

# ---------------------------------------------------------------- log-logistic fits (time in years)
fit1 <- lapply(ipd, function(d) flexsurvreg(Surv(time_years, status) ~ 1, data = d, dist = "llogis"))
both$group <- factor(both$group, levels = groups)
fit_common <- flexsurvreg(Surv(time_years, status) ~ group, data = both, dist = "llogis")
fit_sep <- flexsurvreg(Surv(time_years, status) ~ group, anc = list(shape = ~ group), data = both, dist = "llogis")
FT <- do.call(rbind, lapply(groups, function(g) {
  r <- fit1[[g]]$res
  data.frame(group = g, n = nrow(ipd[[g]]), events = sum(ipd[[g]]$status),
             shape = r["shape", "est"], shape_lo = r["shape", "L95%"], shape_hi = r["shape", "U95%"],
             median_months = 12 * r["scale", "est"], median_lo = 12 * r["scale", "L95%"], median_hi = 12 * r["scale", "U95%"],
             reported_median = rep_med[[g]][[1]], reported_lo = rep_med[[g]][[2]], reported_hi = rep_med[[g]][[3]],
             km_median_reconstructed = unname(summary(survfit(Surv(time, status) ~ 1, data = ipd[[g]]))$table["median"]),
             loglik = fit1[[g]]$loglik, AIC = fit1[[g]]$AIC)
}))
# common shape: medians per group from the scale covariate
cs <- fit_common$res
med_c <- c(early = cs["scale", "est"], late = cs["scale", "est"] * exp(cs["grouplate", "est"]))
lrt <- 2 * (fit_sep$loglik - fit_common$loglik)
p_lrt <- pchisq(lrt, df = 1, lower.tail = FALSE)
# Wald test on the log-shape difference from the separate fits
ls <- sapply(fit1, function(f) log(f$res["shape", "est"]))
ls_se <- sapply(fit1, function(f) sqrt(f$cov["shape", "shape"]))   # cov of log(shape)
z <- unname((ls["early"] - ls["late"]) / sqrt(sum(ls_se^2)))
p_wald <- 2 * pnorm(-abs(z))
separate <- p_lrt < 0.05
ST <- data.frame(shape_early = FT$shape[1], shape_late = FT$shape[2], shape_ratio_early_late = FT$shape[1] / FT$shape[2],
                 common_shape = cs["shape", "est"], common_shape_lo = cs["shape", "L95%"], common_shape_hi = cs["shape", "U95%"],
                 common_median_early_months = 12 * med_c[["early"]], common_median_late_months = 12 * med_c[["late"]],
                 loglik_separate = fit_sep$loglik, loglik_common = fit_common$loglik, lrt_chisq = lrt, lrt_df = 1, p_lrt = p_lrt,
                 wald_z_log_shape = z, p_wald = p_wald, rule = "separate shapes if p_lrt < 0.05",
                 decision = if (separate) "separate" else "common")
write.csv(FT, file.path(out_dir, "esme_fits.csv"), row.names = FALSE)
write.csv(ST, file.path(out_dir, "esme_shape_test.csv"), row.names = FALSE)
print(FT, row.names = FALSE); print(ST, row.names = FALSE)

# parameters for the engine (years): separate fits, or the common-shape model
EP <- if (separate) {
  list(decision = "separate", shape_early = FT$shape[1], shape_late = FT$shape[2],
       median_early = FT$median_months[1] / 12, median_late = FT$median_months[2] / 12)
} else {
  list(decision = "common", shape_early = cs["shape", "est"], shape_late = cs["shape", "est"],
       median_early = med_c[["early"]], median_late = med_c[["late"]])
}
saveRDS(list(engine = EP, fits = FT, shape_test = ST, validation = V, source = spec$label), file.path(ROOT, "data", "fits", "esme_fits.rds"))
cat(sprintf("engine DR parameters (%s): shape early %.4f / late %.4f, median early %.3f / late %.3f months\n",
            EP$decision, EP$shape_early, EP$shape_late, 12 * EP$median_early, 12 * EP$median_late))

# figure: reconstructed KM and the fitted log-logistic curves
tg <- seq(0, 4, by = 1 / 48)
pl <- do.call(rbind, lapply(groups, function(g) {
  k <- survfit(Surv(time_years, status) ~ 1, data = ipd[[g]])
  sh <- if (g == "early") EP$shape_early else EP$shape_late; md <- if (g == "early") EP$median_early else EP$median_late
  rbind(data.frame(group = g, curve = "KM (reconstructed)", t = c(0, k$time), s = c(1, k$surv)),
        data.frame(group = g, curve = "log-logistic (engine)", t = tg, s = 1 / (1 + (tg / md)^sh)))
}))
p <- ggplot(pl, aes(12 * t, 100 * s, colour = group, linetype = curve)) + geom_step(data = pl[pl$curve != "log-logistic (engine)", ]) +
  geom_line(data = pl[pl$curve == "log-logistic (engine)", ]) + scale_colour_manual(values = c(early = "#F8766D", late = "#00BFC4")) +
  coord_cartesian(xlim = c(0, 48)) + labs(x = "Months from diagnosis of metastasis", y = "OS (%)", colour = NULL, linetype = NULL,
                                          title = sprintf("ESME Fig. 3a: reconstructed KM and log-logistic (%s shape)", EP$decision)) +
  theme_bw(base_size = 9) + theme(legend.position = "bottom")
ggsave(file.path(out_dir, "fig_esme_fit.png"), p, width = 6.5, height = 4, dpi = 200)
