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
  # user decision 2026-10-22 (round 8; rationale corrected 2026-10-23): distant recurrence entered
  # up to this many months from randomization is "early", in both arms. ESME (PMID 37385070):
  # metastasis within 12 months of the end of neo/adjuvant chemotherapy; in the model chemotherapy
  # ends at week 24 (about 5.5 months), 5.5 + 12 = 17.5, rounded to 18.
  dr_early_months = 18,
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
  #   2026-10-22 round 6, ACCEPTANCE RULE FIXED BEFORE THE RUN (user decision of 2026-10-22,
  #     committed before calibration round 6 was run):
  #     (a) engine OS inside the pointwise 95% CI of the KM at 1-5 years in each arm (10 points);
  #         if (a) fails, the calibration is still accepted only if both hold:
  #         (i) every point outside its 95% CI lies outside by <= 0.3 percentage points;
  #         (ii) all 10 points lie inside the Bonferroni simultaneous intervals (pointwise 99.5% CI,
  #              1 - 0.05 / 10; same log-scale KM interval as for (a));
  #     (b) unchanged: engine 5-year RMST difference inside the bootstrap 95% CI of the KM
  #         difference. Not accepted -> stop and report, no structure added.
  #     Reason: with 10 points each tested at 95%, at least one point falls outside with
  #     substantial probability even when the model is right.
  #     The PreProg boundaries (median 10-26 months, 5-year survival >= 5%) are reported, not part
  #     of this rule (the user's rule names only (a), (i), (ii) and (b)).
  gate_years = 1:5,
  gate_accept_max_outside_pp = 0.3,
  gate_accept_simultaneous_level = 1 - 0.05 / 10,
  # DR excess hazard of the pembrolizumab arms = common log-logistic hazard x k (round 6): k is
  # estimated in the base calibration within [0.25, 4]; scenario "k = 1" (common post-DR
  # mortality) for every comparison involving pembrolizumab
  pembro_dr_k_bounds = c(0.25, 4),
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
