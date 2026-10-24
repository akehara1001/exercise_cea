# engine.R
# Phase-1 survival engine: cohort semi-Markov model from randomization.
#
# States: EF (event-free), PreProg (progression precluding surgery), LRR (locoregional
# recurrence, incl. second primary cancer), DR (distant recurrence, tracked by months since entry:
# semi-Markov tunnels), Dead.
# The engine splits the fitted EFS of each branch into event types and times; it does not change
# the EFS itself (round 12, 2026-10-23, docs/acceptance_rule_round12.md: events already in the
# fitted EFS are moved between times or states, never added; R/test_engine_efs_consistency.R).
# - Neoadjuvant phase [0, L): EF follows the branch KM (pre_surv) exactly. Its exits are split into
#   EF -> PreProg (share q_pre = reported progression precluding surgery / non-pCR patients of the
#   arm, at most the KM drop), EF -> death due to adverse events (the part of the treatment-period
#   AE deaths that falls before surgery, at most what is left) and other deaths; all timed by the
#   KM. The pCR branch has no exits before surgery (its KM is flat by construction). PreProg ->
#   death: background + an excess hazard in time since PreProg entry (common to both arms,
#   calibrated), tracked with tunnels like DR. (Before round 12 the background and AE deaths were
#   added on top of the KM and PreProg used q_pre instead of the KM drop.)
# - From surgery (t >= L): EF leaves with the branch EFS model (arm x pCR, landmarked at L).
#   Background death (life table) is explicit; the excess part of the EFS hazard first carries the
#   AE deaths of the treatment period after surgery and what did not fit before surgery (AE deaths
#   spread over the rest of the treatment period, PreProg entries at the earliest cycles after
#   surgery); the rest is split into EF -> LRR (local recurrence and second primary cancer),
#   EF -> DR and EF -> death by the arm's first-event composition.
# - Deaths due to adverse events: a constant rate per arm over the treatment period [0, ae_end)
#   (neoadjuvant + adjuvant, about 12 months), in both branches; not calibrated; removed from the
#   deaths without recurrence of the composition.
# - LRR -> DR at a constant rate; LRR -> death at the background rate.
# - DR -> death: background + an excess hazard in time since DR (log-logistic or Weibull;
#   common to both arms; calibrated, step 5). Round 8 (2026-10-22): with dr$late_scale, DR is two
#   sub-states by the time of entry: early (entered up to dr$early_cycles cycles from
#   randomization) with median dr$scale, late with median dr$late_scale; shape and k shared
#   (dr_state()).
# DR excess hazard of the pembrolizumab arms = common hazard x params$pembro_dr_k (round 6:
#   k estimated in the base calibration; round 13: early DR only when params$pembro_dr_k_scope is
#   "early", parameter sets without the field are "all"); scenario common_dr = TRUE sets k = 1 (common post-DR
#   mortality in all arms).
# Exercise hooks for phase 2 (no effect by default):
#   (a) hr0 / wane_start / wane_rate: time-varying HR on EF -> LRR and EF -> DR,
#       HR(t) = hr0 for t <= wane_start, 1 - (1 - hr0) * exp(-wane_rate * (t - wane_start)) after
#       (t in years from randomization; wane_rate = 0 keeps hr0 for life);
#   (b) p_pcr: replaces the arm's pCR proportion.
# Post-surgery drug scenario S-JP (docs/model_spec.md):
#   nonpcr_mix: data frame (group, weight, hr); the non-pCR branch is run once per group with
#   its excess EFS hazard (LRR, DR and excess death; not background death) multiplied by hr from
#   surgery on, and the state occupancies are mixed by weight (the HRs are not averaged).

# excess cumulative hazard after DR or PreProg as a function of time since entry (years); an
# optional multiplier k scales the hazard
dr_cumhaz <- function(dr, t) (if (is.null(dr$k)) 1 else dr$k) * switch(dr$dist,
  llogis = log1p((t / dr$scale)^dr$shape),
  weibull = (t / dr$scale)^dr$shape,
  exp = t * dr$rate)

# one branch (arm x pCR status), in two parts: branch_flows() computes everything that does not
# depend on the excess death hazards after PreProg and DR (event-free and LRR states, flows into
# PreProg and DR, deaths from EF and LRR); branch_states() adds the PreProg and DR tunnel states.
# Calibration and the bootstrap reuse the flows while varying those hazards (os_fast()).
# hazards of leaving EF per cycle (shared with the loop in R/test_engine_vectorized.R): hbx
# background death (after surgery only; before surgery it is part of the KM exits), dHL / dHD / dHX
# to LRR, DR and death (other), dHpre to PreProg, dHA death due to adverse events. In the base case
# (hr = NULL, drug_hr = 1) the total is the KM hazard before surgery and the all-cause hazard of the
# EFS model after (non-cure models: not below background).
branch_hazards <- function(efs_spec, pre_surv, q_pre, shares, start_age, L, cycle, K, hr = NULL, drug_hr = 1,
                           ae_rate = 0, ae_end = 0) {
  t <- (0:K) * cycle
  hb <- H_pop(start_age + t[-(K + 1)], cycle)                     # background cum hazard per cycle
  # excess EF hazard per cycle after surgery
  tau0 <- pmax(t[-(K + 1)] - L, 0); tau1 <- pmax(t[-1] - L, 0)
  post <- t[-(K + 1)] >= L - 1e-9; pre <- !post
  S0 <- spec_surv(efs_spec, tau0); S1 <- spec_surv(efs_spec, tau1)
  dH <- -log(pmax(S1, 1e-300)) + log(pmax(S0, 1e-300))
  dHex <- if (efs_spec$family == "cure") dH else pmax(dH - hb, 0)
  dHex[pre] <- 0
  # before surgery: the KM hazard, split by shares of its exits (PreProg first, then AE deaths)
  # + 1e-9: k * cycle can fall a rounding error short of the KM knot at the same month
  km <- function(x) approx(pre_surv$time, pre_surv$surv, xout = pmin(x, L) + 1e-9, method = "constant", f = 0, rule = 2)$y
  km_L <- km(L); drop_L <- 1 - km_L
  dK <- ifelse(pre, -log(pmax(km(t[-1]), 1e-300) / pmax(km(t[-(K + 1)]), 1e-300)), 0)
  ae_pre <- 1 - exp(-ae_rate * min(L, ae_end))                   # AE deaths falling before surgery
  P_pre <- min(q_pre, drop_L); A_pre <- min(ae_pre, drop_L - P_pre)
  f_p <- if (drop_L > 0) P_pre / drop_L else 0; f_a <- if (drop_L > 0) A_pre / drop_L else 0
  dHpre <- f_p * dK; dHA <- f_a * dK; dHX <- (1 - f_p - f_a) * dK
  # after surgery; EF in the base case does not depend on the split, so incidences are set with it
  Hb <- ifelse(pre, dK, hb + dHex)
  EF0 <- exp(-c(0, cumsum(Hb)))[1:K]
  inc <- function(h, k) EF0[k] * (1 - exp(-Hb[k])) * h / Hb[k]    # incidence of a part h of Hb[k]
  ov <- pmax(pmin(t[-1], ae_end) - pmax(t[-(K + 1)], L), 0)        # cycle overlap with [L, ae_end)
  dHA_post <- ae_rate * ov
  M_A <- ae_pre - A_pre                                           # AE deaths moved after surgery
  if (M_A > 1e-15 && sum(ov) > 0) dHA_post <- dHA_post - log(1 - M_A / km_L) * ov / sum(ov)
  dHA_post <- pmin(dHA_post, dHex)
  dHA[post] <- dHA_post[post]
  M_P <- q_pre - P_pre                                            # PreProg entries moved after surgery
  dHpp <- numeric(K)
  if (M_P > 1e-15) for (k in which(post)) {
    room <- dHex[k] - dHA[k]
    h <- min(room, if (Hb[k] > 0) M_P * Hb[k] / (EF0[k] * (1 - exp(-Hb[k]))) else 0)
    dHpp[k] <- h; M_P <- M_P - inc(h, k)
    if (M_P <= 1e-12) break
  }
  dHpre[post] <- dHpp[post]
  rest <- ifelse(post, (dHex - dHA - dHpp) * drug_hr, 0)
  hrv <- if (is.null(hr)) rep(1, K) else hr((t[-(K + 1)] + t[-1]) / 2)
  dHX[post] <- shares[["death"]] * rest[post]
  list(t = t, post = post, hb = hb, hbx = ifelse(post, hb, 0), dHL = shares[["LRR"]] * rest * hrv, dHD = shares[["DR"]] * rest * hrv,
       dHX = dHX, dHpre = dHpre, dHA = dHA)
}

# one branch (arm x pCR status), in two parts: branch_flows() computes everything that does not
# depend on the excess death hazards after PreProg and DR (event-free and LRR states, flows into
# PreProg and DR, deaths from EF and LRR); branch_states() adds the PreProg and DR tunnel states.
# Calibration and the bootstrap reuse the flows while varying those hazards (os_fast()).
branch_flows <- function(efs_spec, pre_surv, q_pre, shares, lrr_dr_rate,
                         start_age, L, cycle, n_cycles, n_tunnel, hr = NULL, drug_hr = 1, ae_rate = 0, ae_end = 0) {
  K <- n_cycles; J <- n_tunnel
  h <- branch_hazards(efs_spec, pre_surv, q_pre, shares, start_age, L, cycle, K, hr, drug_hr, ae_rate, ae_end)
  t <- h$t; hb <- h$hb
  dHL <- h$dHL; dHD <- h$dHD; dHX <- h$dHX; dHpre <- h$dHpre; dHA <- h$dHA
  # Closed form of the cycle-by-cycle recursion (R/test_engine_vectorized.R checks it against a
  # loop). Competing hazards within a cycle; entrants of a cycle enter their state at its end.
  Ht <- h$hbx + dHL + dHD + dHX + dHpre + dHA
  EF <- c(1, exp(-cumsum(Ht)))
  efk <- EF[1:K]
  pe <- 1 - exp(-Ht)
  sh <- function(x) ifelse(Ht > 0, x / Ht, 0)                       # no exits in a cycle: Ht = 0
  to_L <- efk * pe * sh(dHL)
  to_D <- efk * pe * sh(dHD)
  to_P <- efk * pe * sh(dHpre)
  to_X <- efk * pe * sh(h$hbx + dHX)
  to_A <- efk * pe * sh(dHA)
  # first-order states: x[k+1] = x[k] exp(-H[k]) + inflow[k]
  lin <- function(inflow, H) { C <- cumsum(H); c(0, exp(-C) * cumsum(inflow * exp(C))) }
  Hl <- hb + lrr_dr_rate * cycle
  LR <- lin(to_L, Hl)
  l_to_D <- LR[1:K] * (1 - exp(-Hl)) * (lrr_dr_rate * cycle) / Hl
  l_to_X <- LR[1:K] * (1 - exp(-Hl)) * hb / Hl
  list(t = t, K = K, J = J, cycle = cycle, Bc = c(0, cumsum(hb)), EF = EF, LR = LR, to_P = to_P, to_DR = to_D + l_to_D,
       to_L = to_L, dEF = c(0, cumsum(to_X)), dAE = c(0, cumsum(to_A)), dLR = c(0, cumsum(l_to_X)))
}

# PreProg or DR at boundary m: sum over entry boundaries e <= m of inflow x background survival
# from e to m x excess survival after m - e cycles in the state (tunnel J and later keep the
# hazard of tunnel J). With max_cycles, only time in state below max_cycles cycles is counted
# (weight min(max(max_cycles - lag, 0), 1) per lag, so a fractional limit is interpolated).
tunnel_state <- function(f, inflow, spec, max_cycles = NULL) {
  K <- f$K; J <- f$J
  dHs <- diff(dr_cumhaz(spec, (0:(J + 1)) * f$cycle))
  dHs[J + 1] <- dHs[J]
  Hx <- c(0, cumsum(dHs[pmin(0:(K - 1), J) + 1]))
  kern <- exp(-Hx)
  if (!is.null(max_cycles)) kern <- kern * pmin(pmax(max_cycles - (0:K), 0), 1)
  w <- c(0, inflow) * exp(f$Bc)
  conv <- stats::filter(c(rep(0, K), w), kern, method = "convolution", sides = 1)   # causal convolution
  exp(-f$Bc) * as.vector(conv)[(K + 1):(2 * K + 1)]
}

# DR occupancy for an inflow vector (inflow[k] arrives at boundary k). Without dr$late_scale one
# tunnel_state(); with it, inflow arriving up to boundary dr$early_cycles is early (median
# dr$scale) and the rest late (median dr$late_scale, shape dr$late_shape if given, round 9),
# each with its own tunnels
dr_early_mask <- function(inflow, dr) seq_along(inflow) <= dr$early_cycles
dr_late_spec <- function(dr) modifyList(dr, list(scale = dr$late_scale, shape = if (is.null(dr$late_shape)) dr$shape else dr$late_shape,
                                                 k = if (is.null(dr$k_late)) dr$k else dr$k_late))
# the pembrolizumab multiplier k on the DR excess hazard: scope "all" (rounds 6 to 12) on early and
# late DR; scope "early" (round 13, 2026-10-23, docs/acceptance_rule_round13.md) on early DR only,
# late DR k = 1 (k_late)
dr_with_k <- function(dr, k, scope = "all") { dr$k <- k; if (identical(scope, "early")) dr$k_late <- 1; dr }
# round 14: parameters of the scenario "early-DR k (external)" (Fedele 2026; R/17_round14_kext.R)
# from a base parameter set (k = 1): k on early DR only, other parameters unchanged
# round 15 (preprog = TRUE when PreProg comes from ESME): k also on PreProg of the pembrolizumab arms
params_kext <- function(P, ext = readRDS(file.path(ROOT, "data", "fits", "dr_k_external.rds")),
                        preprog = identical(CFG$preprog_source, "esme_early")) {
  P$pembro_dr_k <- ext$k; P$pembro_dr_k_scope <- ext$scope
  if (preprog) P$pembro_preprog_k <- ext$k
  P
}
dr_state <- function(f, inflow, dr, max_cycles = NULL) {
  if (is.null(dr$late_scale)) return(tunnel_state(f, inflow, dr, max_cycles))
  e <- dr_early_mask(inflow, dr)
  tunnel_state(f, inflow * e, dr, max_cycles) + tunnel_state(f, inflow * !e, dr_late_spec(dr), max_cycles)
}

# state occupancy, inflows (at the boundary where entrants arrive) and cumulative deaths by
# source; with dr_first_cycles, also the part of DR within that many cycles of entry (DR_first)
branch_states <- function(f, preprog, dr, dr_first_cycles = NULL) {
  PP <- tunnel_state(f, f$to_P, preprog)
  DRs <- dr_state(f, f$to_DR, dr)
  Dead <- 1 - f$EF - f$LR - PP - DRs
  dPP <- c(0, cumsum(f$to_P)) - PP
  out <- data.frame(time = f$t, EF = f$EF, PreProg = PP, LRR = f$LR, DR = DRs, Dead = Dead,
                    Dead_from_EF = f$dEF, Dead_from_AE = f$dAE, Dead_from_LRR = f$dLR, Dead_from_PreProg = dPP,
                    Dead_from_DR = Dead - f$dEF - f$dAE - f$dLR - dPP,
                    In_PreProg = c(0, f$to_P), In_LRR = c(0, f$to_L), In_DR = c(0, f$to_DR))
  if (!is.null(dr_first_cycles)) out$DR_first <- dr_state(f, f$to_DR, dr, dr_first_cycles)
  if (!is.null(dr$late_scale)) out$In_DR_early <- c(0, f$to_DR * dr_early_mask(f$to_DR, dr))
  out
}

run_branch <- function(efs_spec, pre_surv, q_pre, shares, lrr_dr_rate, dr, preprog,
                       start_age, L, cycle, n_cycles, n_tunnel, hr = NULL, drug_hr = 1, ae_rate = 0, ae_end = 0,
                       dr_first_cycles = NULL) {
  branch_states(branch_flows(efs_spec, pre_surv, q_pre, shares, lrr_dr_rate, start_age, L, cycle, n_cycles, n_tunnel,
                             hr, drug_hr, ae_rate, ae_end), preprog, dr, dr_first_cycles)
}

# parameter set for the engine, built from the selected fits and the data
engine_params <- function(fits = readRDS(file.path(ROOT, "data", "fits", "fits.rds")),
                          dr = list(dist = "llogis", shape = NA, scale = NA),
                          preprog = list(dist = "weibull", shape = NA, scale = NA)) {
  rv <- read.csv(file.path(ROOT, "data", "reported_values.csv"), stringsAsFactors = FALSE)
  val <- function(id, key) as.numeric(rv$value[rv$fact_id == id & rv$key == key])
  ipd <- readRDS(file.path(ROOT, "data", "ipd", "ipd_all.rds"))
  Lm <- CFG$landmark_months; L <- Lm / 12
  pc <- read.csv(file.path(ROOT, "data", "pcr_counts.csv"), stringsAsFactors = FALSE)
  pc <- pc[pc$source == CFG$pcr_source, ]
  km_at <- function(d, tm) summary(survfit(Surv(time, status) ~ 1, data = d), times = tm, extend = TRUE)$surv
  arms <- c("pembro", "placebo")
  n_non <- c(pembro = pc$nonpcr_pembro, placebo = pc$nonpcr_placebo)
  p <- list(start_age = CFG$start_age, L = L, cycle = CFG$cycle_years,
            n_cycles = round((CFG$max_age - CFG$start_age) / CFG$cycle_years), n_tunnel = CFG$dr_tunnel_months,
            p_pcr = c(pembro = pc$pcr_pembro / (pc$pcr_pembro + pc$nonpcr_pembro),
                      placebo = pc$pcr_placebo / (pc$pcr_placebo + pc$nonpcr_placebo)),
            efs = list(), pre_surv = list(), q_pre = list(), shares = list(), composition = list(),
            ae = list(), ae_end = CFG$ae_death_period_years, ae_source = CFG$ae_death_source)
  for (a in arms) {
    p$efs[[a]] <- list(pCR = fits$selected[[paste0("EFS_", a, "_pCR")]], nonpCR = fits$selected[[paste0("EFS_", a, "_nonpCR")]])
    mm <- 0:Lm
    p$pre_surv[[a]] <- lapply(c(pCR = "pCR", nonpCR = "nonpCR"), function(b)
      data.frame(time = mm / 12, surv = km_at(ipd[[paste0("K22_S4_EFS_pCR_", a, "_", b)]], mm)))
    # progression precluding surgery (2024 Table 1, IA7) as a share of the arm's non-pCR patients
    prog <- val("K24_efs_composition", paste0("prog_", a))
    p$q_pre[[a]] <- c(pCR = 0, nonpCR = prog / n_non[[a]])
    # first-event composition (2024 Table 1, IA7): local recurrence and second primary cancer
    # (non-distant) -> LRR; distant recurrence -> DR; death without recurrence -> death.
    # Background deaths expected in the EF person-time after surgery are removed from the death
    # count, because background mortality is modelled separately.
    d <- ipd[[paste0("K24_F2A_EFS_", a)]]
    d <- d[d$time > Lm, ]
    e_bg <- sum(H_pop(CFG$start_age + L, (d$time - Lm) / 12))
    loc <- val("K24_efs_composition", paste0("local_", a))
    sp <- val("K24_efs_composition", paste0("second_primary_", a))
    dis <- val("K24_efs_composition", paste0("distant_", a))
    # deaths due to adverse events (2022 appendix Table S5, IA4, as-treated population) are
    # modelled on their own and removed from the deaths without recurrence
    ae_key <- switch(CFG$ae_death_source, any = "died_", drug_related = "died_drug_related_")
    n_ae <- val("K22A_ae_deaths", paste0(ae_key, a)); n_at <- val("K22A_ae_deaths", paste0("n_astreated_", a))
    p$ae[[a]] <- c(deaths = n_ae, n_treated = n_at, prob = n_ae / n_at,
                   rate = -log(1 - n_ae / n_at) / CFG$ae_death_period_years)
    dth <- max(val("K24_efs_composition", paste0("death_", a)) - e_bg - n_ae, 0)
    tot <- loc + sp + dis + dth
    p$shares[[a]] <- c(LRR = (loc + sp) / tot, DR = dis / tot, death = dth / tot, expected_background_deaths = e_bg)
    p$composition[[a]] <- c(any = val("K24_efs_composition", paste0("any_", a)), progression_precluding_surgery = prog,
                            local = loc, distant = dis, second_primary = sp,
                            death = val("K24_efs_composition", paste0("death_", a)), n_nonpCR = n_non[[a]])
  }
  # LRR -> DR: 2022 Table 1 footnote, local recurrences followed by distant recurrence; exposure
  # = IA4 median follow-up minus the median time of the EFS events at IA4
  ev <- c(ipd$K22_F1_EFS_pembro$time[ipd$K22_F1_EFS_pembro$status == 1], ipd$K22_F1_EFS_placebo$time[ipd$K22_F1_EFS_placebo$status == 1])
  expo <- (val("K22_cutoff", "median_fu_months") - median(ev)) / 12
  n_ld <- val("K22_local_then_distant", "pembro") + val("K22_local_then_distant", "placebo")
  n_l <- val("K22_efs_composition", "local_pembro") + val("K22_efs_composition", "local_placebo")
  p$lrr_dr <- c(rate = -log(1 - n_ld / n_l) / expo, n_local_then_distant = n_ld, n_local = n_l, exposure_years = expo)
  p$dr <- dr
  p$preprog <- preprog
  p$pembro_dr_k <- 1
  p$pembro_dr_k_scope <- CFG$pembro_dr_k_scope
  p
}

# exposed interface: arm = chemo | exercise | pembro | both; pcr = all | pCR | nonpCR
survival_engine <- function(arm, pcr = "all", times = NULL, params,
                            hr0 = 1, wane_start = 0, wane_rate = 0, p_pcr = NULL, nonpcr_mix = NULL,
                            common_dr = FALSE, dr_first_months = NULL) {
  base <- switch(arm, chemo = "placebo", exercise = "placebo", pembro = "pembro", both = "pembro",
                 stop("arm must be chemo, exercise, pembro or both"))
  dr <- params$dr
  if (base == "pembro" && !common_dr) dr <- dr_with_k(dr, params$pembro_dr_k, params$pembro_dr_k_scope)
  hr <- if (hr0 == 1) NULL else function(t) ifelse(t <= wane_start, hr0, 1 - (1 - hr0) * exp(-wane_rate * (t - wane_start)))
  pp <- if (is.null(p_pcr)) params$p_pcr[[base]] else p_pcr
  ppg <- params$preprog                                 # round 15 scenario: k also on PreProg of the pembrolizumab arms
  if (base == "pembro" && !common_dr && !is.null(params$pembro_preprog_k)) ppg$k <- params$pembro_preprog_k
  rb1 <- function(b, dhr) run_branch(params$efs[[base]][[b]], params$pre_surv[[base]][[b]], params$q_pre[[base]][[b]],
                                      params$shares[[base]], params$lrr_dr[["rate"]], dr, ppg,
                                      params$start_age, params$L, params$cycle, params$n_cycles, params$n_tunnel, hr, dhr,
                                      params$ae[[base]][["rate"]], params$ae_end,
                                      if (is.null(dr_first_months)) NULL else dr_first_months / (12 * params$cycle))
  rb <- function(b) {
    if (b == "pCR" || is.null(nonpcr_mix)) return(rb1(b, 1))
    stopifnot(abs(sum(nonpcr_mix$weight) - 1) < 1e-9, all(nonpcr_mix$weight >= 0))
    parts <- lapply(seq_len(nrow(nonpcr_mix)), function(i) rb1(b, nonpcr_mix$hr[i]))
    r <- parts[[1]]; r[, -1] <- 0
    for (i in seq_along(parts)) r[, -1] <- r[, -1] + nonpcr_mix$weight[i] * parts[[i]][, -1]
    r
  }
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

# base case only (no exercise, S-JP or pCR change): flows of both branches of an arm, and the
# arm's OS at cycle boundaries for given PreProg and DR excess hazards
arm_flows <- function(params, arm) {
  base <- switch(arm, chemo = "placebo", exercise = "placebo", pembro = "pembro", both = "pembro")
  fl <- lapply(c(pCR = "pCR", nonpCR = "nonpCR"), function(b)
    branch_flows(params$efs[[base]][[b]], params$pre_surv[[base]][[b]], params$q_pre[[base]][[b]], params$shares[[base]],
                 params$lrr_dr[["rate"]], params$start_age, params$L, params$cycle, params$n_cycles, params$n_tunnel,
                 NULL, 1, params$ae[[base]][["rate"]], params$ae_end))
  list(base = base, p_pcr = params$p_pcr[[base]], flows = fl)
}
os_fast <- function(af, preprog, dr) {
  os_b <- function(f) f$EF + f$LR + tunnel_state(f, f$to_P, preprog) + dr_state(f, f$to_DR, dr)
  af$p_pcr * os_b(af$flows$pCR) + (1 - af$p_pcr) * os_b(af$flows$nonpCR)
}

# S-JP subgroups of the non-pCR branch (Dr Ozaki, 2026-10-23): gBRCA carriers (F03) receive olaparib
# with proportion F04 (no capecitabine), the other carriers nothing; non-carriers receive capecitabine
# with proportion F01 (defined within gBRCA-negative patients). Arms with pembrolizumab pass F01P and
# F04P as F01 and F04.
sjp_mix <- function(F01, F03, F04, hr_cap, hr_ola) {
  w_o <- F03 * F04
  w_c <- (1 - F03) * F01
  data.frame(group = c("olaparib", "capecitabine", "neither"), weight = c(w_o, w_c, 1 - w_o - w_c),
             hr = c(hr_ola, hr_cap, 1))
}

# exercise path A arguments: the effect holds through the programme (surgery, or surgery +
# continuation), then after a delay decays at wane_rate per year. Path B uses p_pcr only.
exercise_args <- function(params, hr0, delay_years = 0, wane_rate = 0, continue_months = 0) {
  list(hr0 = hr0, wane_start = params$L + continue_months / 12 + delay_years, wane_rate = wane_rate)
}
