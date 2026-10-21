# engine.R
# Phase-1 survival engine: cohort semi-Markov model from randomization.
#
# States: EF (event-free), LRR (locoregional recurrence), DR (distant recurrence, tracked by
# months since entry: semi-Markov tunnels), Dead.
# - Neoadjuvant phase [0, L): pre-surgery EFS events of the non-pCR branch (mostly progression
#   precluding surgery) move EF -> DR following the branch KM at monthly points up to L; the pCR
#   branch has none by definition.
# - From surgery (t >= L): EF leaves with the branch EFS model (arm x pCR, landmarked at L).
#   Background death (life table) is explicit; the excess part of the EFS hazard is split into
#   EF -> LRR, EF -> DR and EF -> death by the arm's first-event composition.
# - LRR -> DR at a constant rate; LRR -> death at the background rate.
# - DR -> death: background + excess Weibull hazard in time since DR (calibrated, step 5).
# Exercise hooks for phase 2 (no effect by default):
#   (a) hr0 / wane_start / wane_rate: time-varying HR on EF -> LRR and EF -> DR,
#       HR(t) = hr0 for t <= wane_start, 1 - (1 - hr0) * exp(-wane_rate * (t - wane_start)) after
#       (t in years from randomization; wane_rate = 0 keeps hr0 for life);
#   (b) p_pcr: replaces the arm's pCR proportion.

# one branch (arm x pCR status); returns state occupancy at t = 0, cycle, 2 cycles, ...
run_branch <- function(efs_spec, pre_surv, shares, lrr_dr_rate, dr_shape, dr_scale,
                       start_age, L, cycle, n_cycles, n_tunnel, hr = NULL) {
  K <- n_cycles; J <- n_tunnel
  t <- (0:K) * cycle
  hb <- H_pop(start_age + t[-(K + 1)], cycle)                     # background cum hazard per cycle
  # excess EF hazard per cycle after surgery
  tau0 <- pmax(t[-(K + 1)] - L, 0); tau1 <- pmax(t[-1] - L, 0)
  post <- t[-(K + 1)] >= L - 1e-9
  S0 <- spec_surv(efs_spec, tau0); S1 <- spec_surv(efs_spec, tau1)
  dH <- -log(pmax(S1, 1e-300)) + log(pmax(S0, 1e-300))
  dHex <- if (efs_spec$family == "cure") dH else pmax(dH - hb, 0)
  dHex[!post] <- 0
  # pre-surgery events: the branch KM before surgery (pre_surv: time in years, survival)
  pre <- !post
  # + 1e-9: k * cycle can fall a rounding error short of the KM knot at the same month
  sp <- function(x) approx(pre_surv$time, pre_surv$surv, xout = pmin(x, L) + 1e-9, method = "constant", f = 0, rule = 2)$y
  dHpre <- ifelse(pre, -log(pmax(sp(t[-1]), 1e-300) / pmax(sp(t[-(K + 1)]), 1e-300)), 0)
  hrv <- if (is.null(hr)) rep(1, K) else hr((t[-(K + 1)] + t[-1]) / 2)
  dHL <- shares[["LRR"]] * dHex * hrv
  dHD <- shares[["DR"]] * dHex * hrv + dHpre
  dHX <- shares[["death"]] * dHex
  # DR excess cumulative hazard per tunnel month
  jj <- 0:J
  dHdr <- ((jj + 1) * cycle / dr_scale)^dr_shape - (jj * cycle / dr_scale)^dr_shape
  dHdr[J + 1] <- dHdr[J]                                           # last tunnel keeps its hazard
  EF <- numeric(K + 1); LR <- numeric(K + 1); DRs <- numeric(K + 1); DE <- numeric(K + 1)
  ef <- 1; lr <- 0; dr <- numeric(J + 1); de <- 0
  EF[1] <- 1
  pLD_H <- lrr_dr_rate * cycle
  for (k in 1:K) {
    # EF
    Ht <- hb[k] + dHL[k] + dHD[k] + dHX[k]
    pe <- 1 - exp(-Ht)
    to_L <- ef * pe * dHL[k] / Ht; to_D <- ef * pe * dHD[k] / Ht; to_X <- ef * pe * (hb[k] + dHX[k]) / Ht
    # LRR
    Hl <- hb[k] + pLD_H; pl <- 1 - exp(-Hl)
    l_to_D <- lr * pl * pLD_H / Hl; l_to_X <- lr * pl * hb[k] / Hl
    # DR tunnels
    Hd <- hb[k] + dHdr
    surv_d <- dr * exp(-Hd)
    d_to_X <- sum(dr) - sum(surv_d)
    new_dr <- numeric(J + 1)
    new_dr[2:(J + 1)] <- surv_d[1:J]
    new_dr[J + 1] <- new_dr[J + 1] + surv_d[J + 1]
    new_dr[1] <- to_D + l_to_D
    ef <- ef - to_L - to_D - to_X
    lr <- lr + to_L - l_to_D - l_to_X
    dr <- new_dr
    de <- de + to_X + l_to_X + d_to_X
    EF[k + 1] <- ef; LR[k + 1] <- lr; DRs[k + 1] <- sum(dr); DE[k + 1] <- de
  }
  data.frame(time = t, EF = EF, LRR = LR, DR = DRs, Dead = DE)
}

# parameter set for the engine, built from the selected fits and the data
engine_params <- function(fits = readRDS(file.path(ROOT, "data", "fits", "fits.rds")),
                          dr_shape = NA, dr_scale = NA) {
  rv <- read.csv(file.path(ROOT, "data", "reported_values.csv"), stringsAsFactors = FALSE)
  val <- function(id, key) as.numeric(rv$value[rv$fact_id == id & rv$key == key])
  ipd <- readRDS(file.path(ROOT, "data", "ipd", "ipd_all.rds"))
  Lm <- CFG$landmark_months; L <- Lm / 12
  pc <- read.csv(file.path(ROOT, "data", "pcr_counts.csv"), stringsAsFactors = FALSE)
  pc <- pc[pc$source == CFG$pcr_source, ]
  km_at <- function(d, tm) summary(survfit(Surv(time, status) ~ 1, data = d), times = tm, extend = TRUE)$surv
  arms <- c("pembro", "placebo")
  p <- list(start_age = CFG$start_age, L = L, cycle = CFG$cycle_years,
            n_cycles = round((CFG$max_age - CFG$start_age) / CFG$cycle_years), n_tunnel = CFG$dr_tunnel_months,
            p_pcr = c(pembro = pc$pcr_pembro / (pc$pcr_pembro + pc$nonpcr_pembro),
                      placebo = pc$pcr_placebo / (pc$pcr_placebo + pc$nonpcr_placebo)),
            efs = list(), pre_surv = list(), shares = list())
  for (a in arms) {
    p$efs[[a]] <- list(pCR = fits$selected[[paste0("EFS_", a, "_pCR")]], nonpCR = fits$selected[[paste0("EFS_", a, "_nonpCR")]])
    mm <- 0:Lm
    p$pre_surv[[a]] <- lapply(c(pCR = "pCR", nonpCR = "nonpCR"), function(b)
      data.frame(time = mm / 12, surv = km_at(ipd[[paste0("K22_S4_EFS_pCR_", a, "_", b)]], mm)))
    # first-event composition after surgery (2024 Table 1, IA7): local, distant, death; second
    # primary cancers are spread over the three in proportion; progression precluding surgery is
    # the pre-surgery phase. Background deaths expected in the EF person-time after surgery are
    # removed from the death count so that only excess deaths are shared out.
    d <- ipd[[paste0("K24_F2A_EFS_", a)]]
    d <- d[d$time > Lm, ]
    e_bg <- sum(H_pop(CFG$start_age + L, (d$time - Lm) / 12))
    loc <- val("K24_efs_composition", paste0("local_", a))
    dis <- val("K24_efs_composition", paste0("distant_", a))
    dth <- max(val("K24_efs_composition", paste0("death_", a)) - e_bg, 0)
    tot <- loc + dis + dth
    p$shares[[a]] <- c(LRR = loc / tot, DR = dis / tot, death = dth / tot, expected_background_deaths = e_bg)
  }
  # LRR -> DR: 2022 Table 1 footnote, local recurrences followed by distant recurrence; exposure
  # = IA4 median follow-up minus the median time of the EFS events at IA4
  ev <- c(ipd$K22_F1_EFS_pembro$time[ipd$K22_F1_EFS_pembro$status == 1], ipd$K22_F1_EFS_placebo$time[ipd$K22_F1_EFS_placebo$status == 1])
  expo <- (val("K22_cutoff", "median_fu_months") - median(ev)) / 12
  n_ld <- val("K22_local_then_distant", "pembro") + val("K22_local_then_distant", "placebo")
  n_l <- val("K22_efs_composition", "local_pembro") + val("K22_efs_composition", "local_placebo")
  p$lrr_dr <- c(rate = -log(1 - n_ld / n_l) / expo, n_local_then_distant = n_ld, n_local = n_l, exposure_years = expo)
  p$dr_shape <- dr_shape; p$dr_scale <- dr_scale
  p
}

# exposed interface: arm = chemo | exercise | pembro | both; pcr = all | pCR | nonpCR
survival_engine <- function(arm, pcr = "all", times = NULL, params,
                            hr0 = 1, wane_start = 0, wane_rate = 0, p_pcr = NULL) {
  base <- switch(arm, chemo = "placebo", exercise = "placebo", pembro = "pembro", both = "pembro",
                 stop("arm must be chemo, exercise, pembro or both"))
  hr <- if (hr0 == 1) NULL else function(t) ifelse(t <= wane_start, hr0, 1 - (1 - hr0) * exp(-wane_rate * (t - wane_start)))
  pp <- if (is.null(p_pcr)) params$p_pcr[[base]] else p_pcr
  drp <- if (is.null(params$dr_by_arm)) c(shape = params$dr_shape, scale = params$dr_scale) else params$dr_by_arm[[base]]
  rb <- function(b) run_branch(params$efs[[base]][[b]], params$pre_surv[[base]][[b]], params$shares[[base]],
                               params$lrr_dr[["rate"]], drp[["shape"]], drp[["scale"]], params$start_age, params$L,
                               params$cycle, params$n_cycles, params$n_tunnel, hr)
  out <- switch(pcr,
    pCR = rb("pCR"),
    nonpCR = rb("nonpCR"),
    all = { a <- rb("pCR"); b <- rb("nonpCR"); r <- a; r[, -1] <- pp * a[, -1] + (1 - pp) * b[, -1]; r },
    stop("pcr must be all, pCR or nonpCR"))
  out$OS <- 1 - out$Dead; out$EFS <- out$EF; out$DRFS <- out$EF + out$LRR
  if (!is.null(times)) {
    out <- data.frame(time = times, lapply(out[, -1], function(y) approx(out$time, y, xout = times, rule = 2)$y))
  }
  out
}
