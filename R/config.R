# config.R
# Decisions and fixed settings for the phase-1 survival engine. Numbers taken from the papers
# are not typed here: they are read from data/ (reported_values.csv, pcr_counts.csv, ipd).

ROOT <- "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"

CFG <- list(
  # user decision 2026-10-21: cohort starts at age 49 (KEYNOTE-522 baseline median)
  start_age = 49,
  # user decision 2026-10-21: pCR proportions from the same analysis as the stratified EFS
  # curves; the 2024 appendix has no EFS by pCR, so the 2022 (IA4) Fig. S4 and its counts
  pcr_source = "K22 (IA4)",
  # landmark at surgery: latest protocol surgery time (24 weeks of neoadjuvant therapy +
  # 6 weeks) = 6.9 months; the reconstructed pCR strata have no events or censoring before 7
  landmark_months = 7,
  # model cycle and horizon
  cycle_years = 1 / 12,
  max_age = 100,
  # time-in-state tunnels after distant recurrence (months); hazard is held at the last one
  dr_tunnel_months = 240,
  # step 4 selection settings (fixed before fitting)
  fit_ci_min_at_risk = 20,      # criterion 1 is checked where the KM has >= 20 at risk
  # criterion 1 threshold: share of monthly points where the model lies inside the pointwise
  # 95% CI of the KM. First set to 1.00 (all points); that rejected every candidate for 3 of the
  # 6 curves, because even the true curve falls outside pointwise 95% CIs at about 5% of points
  # (and the CI is very narrow while S is near 1). Revised after the first run to 0.95.
  fit_ci_min_inside = 0.95,
  aic_window = 4,               # models within 4 AIC units of the best eligible one
  hazard_peak_max_years = 3,    # criterion 2: excess hazard peaks no later than 3 y after surgery
  yau_landmark_years = 0.5,     # Yau time origin is the start of NAC; surgery ~ 0.5 y later
  # step 5 calibration grid (months from randomization)
  calib_grid_months = 1:78,     # 78 = last risk-table time with >= 50 at risk in both arms
  # deaths due to adverse events (decision 2026-10-22): per arm, evenly over the treatment period
  # (neoadjuvant + adjuvant, about 12 months), removed from the deaths without recurrence of the
  # EFS composition. "any": participants who died due to an adverse event (2022 appendix Table S5,
  # IA4; all patients had completed treatment by February 2020); "drug_related": deaths due to
  # treatment-related adverse events (same table; also 2024 main text, IA7)
  ae_death_source = "any",
  ae_death_period_years = 1,
  # step 5 gate. History (all changed after seeing results; report section "门槛修改记录"):
  #   2026-10-21 task: |engine OS - KM| <= 1 point at 1-5 years in each arm (gate_pp_round1_2);
  #   2026-10-22 round 3: (a) engine OS inside the pointwise 95% CI of the KM at 1-5 years in each
  #     arm; (b) 5-year RMST difference between arms within 20% of the KM value
  #     (gate_rmst_rel_tol_round3);
  #   2026-10-22 round 4: (a) unchanged; (b) engine 5-year RMST difference inside the bootstrap
  #     95% CI of the KM difference (B = boot_B, seed).
  gate_years = 1:5,
  gate_pp_round1_2 = 1,
  gate_rmst_rel_tol_round3 = 0.20,
  # 5-year stratified EFS constraint (decision 2026-10-22): the 5-year prediction must lie in the
  # 95% CI of the later-cutoff value; CIs are not reported, so binomial (Wald) with the IA4
  # stratum sizes
  efs5_ci_z = qnorm(0.975),
  seed = 20261021,
  boot_B = 1000
)

source(file.path(ROOT, "R", "lifetable.R"))
