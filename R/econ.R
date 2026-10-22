# econ.R
# Phase 2a: cost and QALY layer on the survival engine (docs/model_spec.md, section 5).
# Lifetime horizon (to age 100), start age 49, costs and effects discounted at 2% a year
# (d(t) = 1.02^-t, t in years from randomization). State occupancies are integrated on the
# engine's monthly grid by the trapezoid rule; no separate half-cycle correction.
#
# pv: named numeric vector of parameter values by param_id (A01..U05, as in the input sheet).
# Costs:
#   - treatment by schedule (events at administration times, weighted by the event-free
#     occupancy then): A01 paclitaxel + carboplatin over weeks 0-11 (A01/12 per week), A02 AC/EC
#     at weeks 12, 15, 18, 21 (A02/4 each), A03 pembrolizumab per dose (neoadjuvant weeks 0, 3,
#     ..., 21; adjuvant 9 doses every 3 weeks from surgery), A04 per outpatient administration
#     visit, A05 per neoadjuvant 3-week cycle, A06 surgery and A07 x A08 radiotherapy at surgery;
#   - adverse events: sum of rate x cost per case (B21-B31 x B01-B11, P rates for the
#     pembrolizumab arms, C rates otherwise), once at the start of treatment;
#   - follow-up of event-free patients, annual cost by years since surgery (C01: years 1-2,
#     C02: years 3-5, C03: year 6 on);
#   - LRR: one-time D01 on entry, then D02 a month while in LRR;
#   - DR: D03 a month for the first D04 months after entry (time-in-state tunnels), then D05 a
#     month until death;
#   - terminal care D06 (total for the last 3 months of life): each death is given D06/3 in its
#     month and in each of the two preceding months (deaths from DR and PreProg by default;
#     setting terminal_deaths = "all" for all deaths). This is the cohort equivalent of a
#     3-month tunnel before death;
#   - exercise programme (exercise arms): the chosen 6-month total (E01, E02 or E03) spread over
#     months 0-6 while event-free; continuation after surgery E04 a month for E05 months.
# Utilities: event-free U01 on treatment (to surgery in the arms without pembrolizumab, to the end
# of adjuvant pembrolizumab in the others) and U02 after; LRR U03; DR and PreProg U04; severe
# adverse events: decrement U05 for pv[["U05_duration_years"]] years, applied to the summed rate
# of the grade >= 3 events (B25-B28, B30, B31), once at the start.

ECON_DEFAULTS <- list(discount = 0.02, exercise_cost = "E01", exercise_continue = FALSE, terminal_deaths = "cancer",
                      neo_doses = 8, adj_doses = 9)
ARMS <- c("chemo", "exercise", "pembro", "both")
has_pembro <- function(arm) arm %in% c("pembro", "both")
has_exercise <- function(arm) arm %in% c("exercise", "both")
wk <- function(w) w * 7 / 365.25

# exercise effect (phase 2 inputs; neutral by default): hr0, delay_years, wane_rate on recurrence
# (engine path A) and delta_pcr on the pCR proportion (path B)
EXERCISE_NEUTRAL <- list(hr0 = 1, delay_years = 0, wane_rate = 0, delta_pcr = 0)

econ_arm <- function(arm, P, pv, settings = ECON_DEFAULTS, exercise = EXERCISE_NEUTRAL, os_anchor = FALSE, nonpcr_mix = NULL) {
  s <- modifyList(ECON_DEFAULTS, settings)
  base <- if (has_pembro(arm)) "pembro" else "placebo"
  cont_m <- if (has_exercise(arm) && isTRUE(s$exercise_continue)) pv[["E05"]] else 0
  ex <- if (has_exercise(arm)) exercise_args(P, exercise$hr0, exercise$delay_years, exercise$wane_rate, cont_m) else
    list(hr0 = 1, wane_start = 0, wane_rate = 0)
  pp <- if (has_exercise(arm) && exercise$delta_pcr != 0) P$p_pcr[[base]] + exercise$delta_pcr else NULL
  e <- survival_engine(arm, "all", times = NULL, params = P, hr0 = ex$hr0, wane_start = ex$wane_start, wane_rate = ex$wane_rate,
                       p_pcr = pp, nonpcr_mix = nonpcr_mix, os_anchor = os_anchor, dr_first_months = pv[["D04"]])
  t <- e$time; cyc <- P$cycle; L <- P$L
  d <- (1 + s$discount)^(-t)
  trap <- function(y) sum(cyc * (head(y, -1) + tail(y, -1)) / 2)          # integral over the grid
  at <- function(col, tt) approx(t, e[[col]], xout = tt, rule = 2)$y      # occupancy at event times
  dsc <- function(tt) (1 + s$discount)^(-tt)
  ev <- function(tt, unit) sum(unit * at("EF", tt) * dsc(tt))             # event costs, event-free patients
  # treatment schedule
  t_ptx <- wk(0:11); t_ac <- wk(c(12, 15, 18, 21)); t_neo <- wk(seq(0, 21, by = 3))
  t_adj <- L + wk(3 * (0:(s$adj_doses - 1)))
  visits <- c(t_ptx, t_ac, if (has_pembro(arm)) t_adj)
  cost <- c(
    chemo_A01 = ev(t_ptx, pv[["A01"]] / 12),
    chemo_A02 = ev(t_ac, pv[["A02"]] / 4),
    pembro_A03 = if (has_pembro(arm)) ev(c(t_neo, t_adj), pv[["A03"]]) else 0,
    administration_A04 = ev(visits, pv[["A04"]]),
    supportive_A05 = ev(t_neo, pv[["A05"]]),
    surgery_A06 = ev(L, pv[["A06"]]),
    radiotherapy_A07_A08 = ev(L, pv[["A07"]] * pv[["A08"]]))
  # adverse events, once at the start
  sfx <- if (has_pembro(arm)) "P" else "C"
  cost[["adverse_events_B"]] <- sum(sapply(21:31, function(i) pv[[paste0("B", i, sfx)]] * pv[[sprintf("B%02d", i - 20)]]))
  # follow-up of event-free patients by years since surgery
  band <- ifelse(t < L, 0, ifelse(t < L + 2, pv[["C01"]], ifelse(t < L + 5, pv[["C02"]], pv[["C03"]])))
  cost[["follow_up_C"]] <- trap(band * e$EF * d)
  # recurrence
  cost[["lrr_entry_D01"]] <- sum(pv[["D01"]] * e$In_LRR * d)
  cost[["lrr_monthly_D02"]] <- trap(12 * pv[["D02"]] * e$LRR * d)
  cost[["dr_first_line_D03"]] <- trap(12 * pv[["D03"]] * e$DR_first * d)
  cost[["dr_later_lines_D05"]] <- trap(12 * pv[["D05"]] * (e$DR - e$DR_first) * d)
  # terminal care: D06 / 3 in the month of death and each of the two months before
  dead_cum <- if (s$terminal_deaths == "all") e$Dead else e$Dead_from_DR + e$Dead_from_PreProg
  dd <- diff(dead_cum)                                                     # deaths in cycle k (t[k] to t[k+1])
  tmid <- head(t, -1) + cyc / 2
  cost[["terminal_D06"]] <- sum(sapply(0:2, function(j) sum(pv[["D06"]] / 3 * dd * dsc(pmax(tmid - j * cyc, 0)))))
  # exercise programme
  cost[["exercise_E"]] <- if (has_exercise(arm)) {
    prog <- trap(ifelse(t < 0.5, pv[[s$exercise_cost]] / 0.5, 0) * e$EF * d)
    contn <- if (isTRUE(s$exercise_continue)) trap(ifelse(t >= L & t < L + pv[["E05"]] / 12, 12 * pv[["E04"]], 0) * e$EF * d) else 0
    prog + contn
  } else 0
  # utilities
  t_on <- if (has_pembro(arm)) L + wk(3 * s$adj_doses) else L
  u_ef <- ifelse(t < t_on, pv[["U01"]], pv[["U02"]])
  qaly_states <- trap((e$EF * u_ef + e$LRR * pv[["U03"]] + (e$DR + e$PreProg) * pv[["U04"]]) * d)
  sev <- sum(sapply(c(25:28, 30, 31), function(i) pv[[paste0("B", i, sfx)]]))
  qaly_ae <- sev * pv[["U05"]] * pv[["U05_duration_years"]]
  os <- 1 - e$Dead
  list(arm = arm, cost = sum(cost), cost_components = cost, qaly = qaly_states - qaly_ae, qaly_ae_decrement = qaly_ae,
       ly = trap(os), ly_disc = trap(os * d), engine = e)
}

econ_all <- function(P, pv, settings = ECON_DEFAULTS, exercise = EXERCISE_NEUTRAL, os_anchor = FALSE, arms = ARMS) {
  R <- lapply(arms, function(a) econ_arm(a, P, pv, settings, exercise, os_anchor))
  names(R) <- arms
  data.frame(arm = arms, cost = sapply(R, `[[`, "cost"), qaly = sapply(R, `[[`, "qaly"), ly = sapply(R, `[[`, "ly"),
             ly_disc = sapply(R, `[[`, "ly_disc"), row.names = NULL)
}

# increments and ICERs against a reference arm
increments <- function(tab, ref = "chemo") {
  r <- tab[tab$arm == ref, ]
  out <- tab
  out$d_cost <- tab$cost - r$cost; out$d_qaly <- tab$qaly - r$qaly; out$d_ly <- tab$ly_disc - r$ly_disc
  out$icer <- ifelse(tab$arm == ref, NA, out$d_cost / out$d_qaly)
  out
}

# efficiency frontier: drop strictly dominated options (higher or equal cost and fewer or equal
# QALYs than another, not identical), then extendedly dominated ones (ICERs must increase along
# the frontier); returns the table with status and frontier ICERs
frontier <- function(tab) {
  tab <- tab[order(tab$cost, -tab$qaly), ]
  tab$status <- "frontier"
  for (i in seq_len(nrow(tab))) for (j in seq_len(nrow(tab))) {
    if (i != j && tab$cost[j] <= tab$cost[i] && tab$qaly[j] >= tab$qaly[i] && (tab$cost[j] < tab$cost[i] || tab$qaly[j] > tab$qaly[i]))
      tab$status[i] <- "dominated"
  }
  repeat {
    f <- which(tab$status == "frontier")
    if (length(f) < 3) break
    ic <- diff(tab$cost[f]) / diff(tab$qaly[f])
    k <- which(diff(ic) < 0)
    if (!length(k)) break
    tab$status[f[k[1] + 1]] <- "extendedly dominated"
  }
  f <- which(tab$status == "frontier")
  tab$frontier_icer <- NA_real_
  if (length(f) > 1) tab$frontier_icer[f[-1]] <- diff(tab$cost[f]) / diff(tab$qaly[f])
  tab
}
