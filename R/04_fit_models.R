# 04_fit_models.R
# Step 4: candidate models for each EFS curve (arm x pCR, Schmid 2022 appendix Fig. S4,
# landmarked at surgery) and each OS curve (arm, Schmid 2024 Fig. 1A, from randomization).
# Candidates: exp, Weibull, lognormal, loglogistic, Gompertz, generalised gamma; Royston-Parmar
# splines with 1-3 internal knots on the log cumulative hazard and log cumulative odds scales;
# relative-survival mixture cure models (Weibull, lognormal, loglogistic) with the Japanese
# female life table as background mortality, the cure fraction acting on excess mortality.
#
# Selection rule (fixed before fitting):
#  1. agreement with the KM: the all-cause model curve lies inside the pointwise 95% CI of the
#     KM at >= 95% of the monthly times where >= 20 are at risk (first set to 100%; see config.R);
#  2. hazard shape: the excess hazard (all-cause minus background) peaks no later than 3 years
#     after surgery (EFS) and falls from 3 to 5 and from 5 to 10 years (EFS) or from 5 to 10 and
#     10 to 20 years (OS); the all-cause hazard is not below the background hazard at 10 and 20 y;
#  3. long-term data (EFS only): conditional EFS from 5 to 10 years after surgery, S(10)/S(5),
#     compared with Yau 2022 TNBC landmarked at 0.5 years (pCR curves vs RCB-0, non-pCR curves
#     vs RCB-1 to 3 pooled). Yau reports no OS, so OS curves have no criterion 3.
#  Among models passing 1 and 2, those within 4 AIC units of the best one are kept; for EFS the
#  one closest to Yau on criterion 3 is chosen, for OS the lowest AIC. AIC/BIC use the all-cause
#  log-likelihood so that cure (relative-survival) and all-cause models are comparable.
# Outputs: output/phase1/model_comparison.csv, model_selection.csv, fig_fit_*.png,
#          fig_hazard_*.png; data/fits/fits.rds (specs of all candidates and the selection)

source("C:/Users/原明美/Documents/ClaudeCode/exercise_cea/R/config.R")
source(file.path(ROOT, "R", "survmodels.R"))
suppressPackageStartupMessages({
  library(survival)
  library(muhaz)
  library(ggplot2)
})
out_dir <- file.path(ROOT, "output", "phase1")
dir.create(file.path(ROOT, "data", "fits"), showWarnings = FALSE)
ipd <- readRDS(file.path(ROOT, "data", "ipd", "ipd_all.rds"))
L <- CFG$landmark_months / 12

landmark <- function(d, Lm) {
  d <- d[d$time > Lm, ]
  data.frame(time = (d$time - Lm) / 12, status = d$status)
}
curves <- list(
  EFS_pembro_pCR    = list(d = landmark(ipd$K22_S4_EFS_pCR_pembro_pCR, CFG$landmark_months), a0 = CFG$start_age + L, kind = "EFS", yau = "RCB0"),
  EFS_placebo_pCR   = list(d = landmark(ipd$K22_S4_EFS_pCR_placebo_pCR, CFG$landmark_months), a0 = CFG$start_age + L, kind = "EFS", yau = "RCB0"),
  EFS_pembro_nonpCR = list(d = landmark(ipd$K22_S4_EFS_pCR_pembro_nonpCR, CFG$landmark_months), a0 = CFG$start_age + L, kind = "EFS", yau = "RCB1_3"),
  EFS_placebo_nonpCR = list(d = landmark(ipd$K22_S4_EFS_pCR_placebo_nonpCR, CFG$landmark_months), a0 = CFG$start_age + L, kind = "EFS", yau = "RCB1_3"),
  OS_pembro  = list(d = data.frame(time = ipd$K24_F1A_OS_pembro$time / 12, status = ipd$K24_F1A_OS_pembro$status), a0 = CFG$start_age, kind = "OS"),
  OS_placebo = list(d = data.frame(time = ipd$K24_F1A_OS_placebo$time / 12, status = ipd$K24_F1A_OS_placebo$status), a0 = CFG$start_age, kind = "OS")
)

# external long-term data: Yau 2022 TNBC landmarked at surgery
yl <- CFG$yau_landmark_years
ylm <- function(arms) {
  d <- do.call(rbind, lapply(arms, function(a) ipd[[paste0("Y22_F4A_EFS_TNBC_", a)]]))
  d <- d[d$time > yl, ]
  data.frame(time = d$time - yl, status = d$status)
}
yau <- list(RCB0 = ylm("RCB0"), RCB1_3 = ylm(c("RCB1", "RCB2", "RCB3")))
yau_cond <- sapply(yau, function(d) {
  s <- summary(survfit(Surv(time, status) ~ 1, data = d), times = c(5, 10), extend = TRUE)$surv
  c(S5 = s[1], S10 = s[2], C5_10 = s[2] / s[1])
})

grid_h <- seq(0.02, 30, by = 0.02)
rows <- list(); fits <- list(); emp_h <- list()
for (cv in names(curves)) {
  d <- curves[[cv]]$d; a0 <- curves[[cv]]$a0
  d$bh <- mu_pop(a0 + d$time)
  km <- survfit(Surv(time, status) ~ 1, data = d)
  last_t <- max(km$time[km$n.risk >= CFG$fit_ci_min_at_risk])
  tg <- seq(1 / 12, last_t, by = 1 / 12)
  ks <- summary(km, times = tg, extend = TRUE)
  mh <- muhaz(d$time, d$status, min.time = 0, max.time = last_t)
  emp_h[[cv]] <- data.frame(curve = cv, time = mh$est.grid, haz = mh$haz.est)
  for (cand in CANDIDATES) {
    r <- tryCatch(fit_candidate(cand, d), error = function(e) NULL)
    if (is.null(r) || any(!is.finite(r$spec$pars))) {
      rows[[length(rows) + 1]] <- data.frame(curve = cv, model = cand$id, family = cand$family, converged = FALSE)
      next
    }
    sp <- r$spec
    fits[[cv]][[cand$id]] <- sp
    ll <- allcause_loglik(sp, d$time, d$status, a0)
    npar <- length(sp$pars)
    s_mod <- allcause_surv(sp, tg, a0)
    inside <- s_mod >= ks$lower - 1e-9 & s_mod <= ks$upper + 1e-9
    hx <- excess_haz(sp, grid_h, a0)
    at <- function(t) hx[which.min(abs(grid_h - t))]
    peak_t <- grid_h[which.max(hx)]
    ha <- function(t) allcause_haz(sp, t, a0)
    if (curves[[cv]]$kind == "EFS") {
      c2 <- peak_t <= CFG$hazard_peak_max_years && at(5) < at(3) && at(10) < at(5)
    } else {
      c2 <- at(10) < at(5) && at(20) <= at(10) + 1e-9
    }
    above_bg <- ha(10) >= mu_pop(a0 + 10) - 1e-9 && ha(20) >= mu_pop(a0 + 20) - 1e-9
    S <- allcause_surv(sp, c(5, 10, 20), a0)
    c3 <- if (curves[[cv]]$kind == "EFS") S[2] / S[1] else NA
    rows[[length(rows) + 1]] <- data.frame(
      curve = cv, model = cand$id, family = cand$family, converged = TRUE, n = nrow(d), events = sum(d$status),
      npar = npar, loglik = round(ll, 3), AIC = round(-2 * ll + 2 * npar, 2), BIC = round(-2 * ll + log(nrow(d)) * npar, 2),
      flexsurv_loglik = round(r$fit$loglik, 3),
      c1_frac_inside_ci = round(mean(inside), 4), c1_max_abs_diff_pp = round(100 * max(abs(s_mod - ks$surv)), 3),
      c1_pass = mean(inside) >= CFG$fit_ci_min_inside - 1e-9, c1_pass_all_points = all(inside),
      peak_excess_haz_year = peak_t, excess_haz_3y = signif(at(3), 4), excess_haz_5y = signif(at(5), 4),
      excess_haz_10y = signif(at(10), 4), excess_haz_20y = signif(at(20), 4), hazard_above_background_10_20y = above_bg,
      c2_pass = c2 && above_bg,
      S5 = round(100 * S[1], 2), S10 = round(100 * S[2], 2), S20 = round(100 * S[3], 2),
      cond_5_10 = round(c3, 4),
      yau_cond_5_10 = if (curves[[cv]]$kind == "EFS") round(yau_cond["C5_10", curves[[cv]]$yau], 4) else NA,
      c3_abs_diff = if (curves[[cv]]$kind == "EFS") round(abs(c3 - yau_cond["C5_10", curves[[cv]]$yau]), 4) else NA,
      cure_fraction = if (sp$family == "cure") round(sp$pars[["theta"]], 4) else NA)
  }
}
M <- do.call(rbind, lapply(rows, function(r) { for (nm in setdiff(names(rows[[which.max(sapply(rows, ncol))]]), names(r))) r[[nm]] <- NA; r }))

write.csv(M, file.path(out_dir, "model_comparison.csv"), row.names = FALSE)

# selection
sel <- list()
M$eligible <- FALSE; M$within_aic_window <- FALSE; M$selected <- FALSE
for (cv in names(curves)) {
  i <- which(M$curve == cv & M$converged)
  M$dAIC[i] <- M$AIC[i] - min(M$AIC[i])
  el <- i[M$c1_pass[i] & M$c2_pass[i]]
  M$eligible[el] <- TRUE
  if (length(el) == 0) stop("no eligible model for ", cv, " - stop and report")
  win <- el[M$AIC[el] <= min(M$AIC[el]) + CFG$aic_window]
  M$within_aic_window[win] <- TRUE
  pick <- if (curves[[cv]]$kind == "EFS") win[order(M$c3_abs_diff[win], M$AIC[win])][1] else win[which.min(M$AIC[win])]
  M$selected[pick] <- TRUE
  n_fail1 <- sum(!M$c1_pass[i]); n_fail2 <- sum(M$c1_pass[i] & !M$c2_pass[i])
  reason <- sprintf("%d/%d converged; %d fail criterion 1 (KM 95%% CI), %d more fail criterion 2 (hazard shape / below background); %d eligible, %d within %g AIC of the best eligible (%s, AIC %.1f); ",
                    length(i), length(CANDIDATES), n_fail1, n_fail2, length(el), length(win), CFG$aic_window,
                    M$model[el][which.min(M$AIC[el])], min(M$AIC[el]))
  reason <- paste0(reason, if (curves[[cv]]$kind == "EFS")
    sprintf("chosen as closest to Yau on S(10)/S(5): model %.3f vs Yau %s %.3f", M$cond_5_10[pick], curves[[cv]]$yau, M$yau_cond_5_10[pick])
    else "chosen as lowest AIC (no external OS data for criterion 3)")
  sel[[cv]] <- data.frame(curve = cv, model = M$model[pick], family = M$family[pick], AIC = M$AIC[pick],
                          dAIC_overall = round(M$dAIC[pick], 2), S5 = M$S5[pick], S10 = M$S10[pick], S20 = M$S20[pick],
                          cure_fraction = M$cure_fraction[pick], reason = reason)
}
SEL <- do.call(rbind, sel)
write.csv(M, file.path(out_dir, "model_comparison.csv"), row.names = FALSE)
write.csv(SEL, file.path(out_dir, "model_selection.csv"), row.names = FALSE)
saveRDS(list(curves = lapply(curves, function(x) x[c("a0", "kind")]), specs = fits,
             selected = setNames(lapply(names(curves), function(cv) fits[[cv]][[SEL$model[SEL$curve == cv]]]), names(curves)),
             yau_cond = yau_cond, landmark_years = L),
        file.path(ROOT, "data", "fits", "fits.rds"))
write.csv(data.frame(group = colnames(yau_cond), t(round(yau_cond, 4))), file.path(out_dir, "yau_landmark_reference.csv"), row.names = FALSE)
print(SEL[, c("curve", "model", "AIC", "S5", "S10", "S20", "cure_fraction")], row.names = FALSE)

# figures: KM with all candidates (selected highlighted) and hazards
for (cv in names(curves)) {
  d <- curves[[cv]]$d; a0 <- curves[[cv]]$a0
  km <- survfit(Surv(time, status) ~ 1, data = d)
  kmd <- data.frame(time = c(0, km$time), surv = 100 * c(1, km$surv))
  tt <- seq(0, 20, by = 0.05)
  pm <- do.call(rbind, lapply(names(fits[[cv]]), function(m)
    data.frame(model = m, time = tt, surv = 100 * allcause_surv(fits[[cv]][[m]], tt, a0),
               selected = m == SEL$model[SEL$curve == cv])))
  xlab <- if (curves[[cv]]$kind == "EFS") "Years after surgery (landmark 7 months)" else "Years from randomization"
  g <- ggplot() +
    geom_line(data = pm[!pm$selected, ], aes(time, surv, group = model), colour = "grey75", linewidth = 0.3) +
    geom_step(data = kmd, aes(time, surv), colour = "black", linewidth = 0.5) +
    geom_line(data = pm[pm$selected, ], aes(time, surv), colour = "#C0392B", linewidth = 0.9) +
    labs(title = cv, subtitle = sprintf("black: KM; red: selected (%s); grey: other candidates", SEL$model[SEL$curve == cv]),
         x = xlab, y = paste(curves[[cv]]$kind, "(%)")) +
    coord_cartesian(ylim = c(max(0, min(pm$surv[pm$time <= 20], kmd$surv) - 5), 100)) +
    theme_bw(base_size = 9)
  ggsave(file.path(out_dir, sprintf("fig_fit_%s.png", cv)), g, width = 6, height = 4, dpi = 200)
  ph <- do.call(rbind, lapply(names(fits[[cv]]), function(m)
    data.frame(model = m, time = grid_h[grid_h <= 20], haz = excess_haz(fits[[cv]][[m]], grid_h[grid_h <= 20], a0),
               selected = m == SEL$model[SEL$curve == cv])))
  eh <- emp_h[[cv]]; eh$haz <- eh$haz - mu_pop(a0 + eh$time)
  g <- ggplot() +
    geom_line(data = ph[!ph$selected, ], aes(time, haz, group = model), colour = "grey75", linewidth = 0.3) +
    geom_line(data = eh, aes(time, haz), colour = "black", linetype = "22", linewidth = 0.6) +
    geom_line(data = ph[ph$selected, ], aes(time, haz), colour = "#C0392B", linewidth = 0.9) +
    geom_hline(yintercept = 0, colour = "grey40", linewidth = 0.3) +
    labs(title = cv, subtitle = "excess hazard (all-cause minus background); dashed: kernel-smoothed KM hazard (muhaz) minus background",
         x = xlab, y = "Excess hazard per year") +
    coord_cartesian(ylim = c(min(0, quantile(ph$haz, 0.02)), max(eh$haz, ph$haz[ph$selected]) * 1.3)) +
    theme_bw(base_size = 9)
  ggsave(file.path(out_dir, sprintf("fig_hazard_%s.png", cv)), g, width = 6, height = 4, dpi = 200)
}
cat("done\n")
