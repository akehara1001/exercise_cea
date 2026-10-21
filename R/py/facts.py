"""Reported values, each pulled from the normalised PDF text by a regex (no hand transcription).

Every fact records the page and the matched text so it can be checked against the source.
"""
N = r"(\d+)"
F = r"([\d.]+)"
SF = r"([−\-]?[\d.]+)"
PCT = r"\([\d.]+%?\)"
# 'pembrolizumab' is sometimes split by a stray space where a soft hyphen was
PEM = r"p ?e ?m ?b ?r ?o ?l ?i ?z ?u ?m ?a ?b"
CHEMO = r"– ?chemotherapy"
K20, K22, K24 = "NEJMoa1910549.pdf", "NEJMoa2112651.pdf", "NEJMoa2409932.pdf"
K22A, K24A = "nejmoa2112651_appendix.pdf", "nejmoa2409932_appendix.pdf"
YAU, YAUA = "eScholarship UC item 0f60710w.pdf", "Yau2022_LancetOncol_appendix_mmc1.pdf"


def g(*names):
    return list(names)


FACTS = [
    # ---- Schmid 2020 (IA2) ----
    dict(id="K20_cutoff", pdf=K20, keys=g("data_cutoff", "median_fu_months"),
         rx=r"data cutoff, (April 24, 2019); median duration of follow-up, " + F + " months"),
    dict(id="K20_age", pdf=K20, keys=g("age_median_pembro", "age_range_pembro", "age_median_placebo", "age_range_placebo"),
         rx=r"Median \(range\) — yr (\d+) \((\d+–\d+)\) (\d+) \((\d+–\d+)\)"),
    dict(id="K20_efs_events", pdf=K20, keys=g("events_pembro", "n_pembro", "events_placebo", "n_placebo"),
         rx=N + " of " + N + r" patients \([\d.]+%\) in the " + PEM + CHEMO + " group and " + N + " of " + N + " patients"),
    dict(id="K20_efs_hr", pdf=K20, keys=g("hr", "hr_lo", "hr_hi"),
         rx=r"hazard ratio, " + F + r"; 95% CI, " + F + " to " + F + r"\)"),
    dict(id="K20_efs_18m", pdf=K20, keys=g("pembro", "pembro_lo", "pembro_hi", "placebo"),
         rx=r"at 18 months who were alive .{0,200}? were " + F + r"% \(95% CI, " + F + " to " + F + r"\) in the "
            + PEM + CHEMO + " group and " + F + r"% \(95% CI,"),
    dict(id="K20_efs_18m_placebo_ci", pdf=K20, keys=g("placebo_lo", "placebo_hi"),
         rx=F + " to " + F + r"\) in the placebo" + CHEMO + r" group; the median was not reached"),
    dict(id="K20_pcr_first602", pdf=K20, keys=g("pct_pembro", "x_pembro", "n_pembro", "pct_placebo", "x_placebo", "n_placebo"),
         rx=F + r"% \(" + N + " of " + N + r" patients\) in the " + PEM + CHEMO + " group and " + F + r"% \(" + N + " of " + N + r" patients\)"),
    dict(id="K20_efs_event_types", pdf=K20, keys=g("source"),
         rx=r"The most common event was distant recurrence \((Table S5)\)"),
    # ---- Schmid 2022 (IA4) ----
    dict(id="K22_cutoff", pdf=K22, keys=g("data_cutoff", "median_fu_months", "fu_min", "fu_max"),
         rx=r"data cutoff, (March 23, 2021)\), the median duration of follow-up was " + F + r" months \(range, " + F + " to " + F + r"\)"),
    dict(id="K22_efs_origin", pdf=K22, keys=g("origin"),
         rx=r"Event-free survival, which was defined as the time from (randomization) to the date of disease progression"),
    dict(id="K22_efs_events_hr", pdf=K22, keys=g("events_pembro", "events_placebo", "hr", "hr_lo", "hr_hi"),
         rx=r"A total of " + N + r" patients \([\d.]+%\) in the " + PEM + CHEMO + " group and " + N + r" patients \([\d.]+%\) in the placebo"
            + CHEMO + r" group had an event or died \(hazard ratio, " + F + r"; 95% confi ?dence interval \[CI\], " + F + " to " + F + ";"),
    dict(id="K22_efs_36m", pdf=K22, keys=g("pembro", "pembro_lo", "pembro_hi", "placebo", "placebo_lo", "placebo_hi"),
         rx=r"The estimated event-?free survival at 36 months was " + F + r"% \(95% CI, " + F + " to " + F + r"\) in the " + PEM + CHEMO
            + " group and " + F + r"% \(95% CI, " + F + " to " + F + r"\)"),
    dict(id="K22_efs_composition", pdf=K22,
         keys=g("any_pembro", "any_placebo", "prog_pembro", "prog_placebo", "local_pembro", "local_placebo",
                "distant_pembro", "distant_placebo", "second_primary_pembro", "second_primary_placebo", "death_pembro", "death_placebo"),
         rx=r"Any first event " + N + " " + PCT + " " + N + " " + PCT + r" Progression of disease that precluded definitive surgery " + N + " " + PCT + " " + N + " " + PCT
            + r" Local recurrence\* " + N + " " + PCT + " " + N + " " + PCT + r" Distant recurrence " + N + " " + PCT + " " + N + " " + PCT
            + r" Second primary cancer† " + N + " " + PCT + " " + N + " " + PCT + r" Death " + N + " " + PCT + " " + N + " " + PCT),
    dict(id="K22_local_then_distant", pdf=K22, keys=g("pembro", "placebo"),
         rx=r"A total of " + N + r" patients in the " + PEM + CHEMO + r" group and " + N + r" in the placebo" + CHEMO
            + r" group with local recurrence had subsequent distant recurrence"),
    dict(id="K22_os_events_hr", pdf=K22, keys=g("events_pembro", "events_placebo", "hr", "hr_lo", "hr_hi"),
         rx=r"A total of " + N + r" patients \([\d.]+%\) in the " + PEM + CHEMO + " group and " + N + r" patients \([\d.]+%\) in the placebo"
            + CHEMO + r" group died \(hazard ratio, " + F + r"; 95 CI, " + F + " to " + F + r"\)"),
    dict(id="K22_os_36m", pdf=K22, keys=g("pembro", "pembro_lo", "pembro_hi", "placebo", "placebo_lo", "placebo_hi"),
         rx=r"The estimated overall survival at 36 months was " + F + r"% \(95% CI, " + F + " to " + F + r"\) in the " + PEM + CHEMO
            + " group and " + F + r"% \(95% CI, " + F + " to " + F + r"\)"),
    dict(id="K22_drfs_hr", pdf=K22, keys=g("hr", "hr_lo", "hr_hi", "figure"),
         rx=r"distant progression, distant recurrence, or death in the " + PEM + CHEMO + r" group, as compared with the placebo" + CHEMO
            + r" group, of " + F + r" \(95% CI, " + F + " to " + F + r"\) \((Fig\. S3)\)"),
    dict(id="K22_efs_pcr", pdf=K22, keys=g("events_pembro", "n_pembro", "events_placebo", "n_placebo", "hr", "hr_lo", "hr_hi"),
         rx=r"among patients with a pathological complete response, " + N + " of " + N + r" \([\d.]+%\) in the " + PEM + CHEMO
            + " group and " + N + " of " + N + r" \([\d.]+%\) in the placebo" + CHEMO + r" group had an event or died \(hazard ratio, "
            + F + r"; 95% CI, " + F + " to " + F + r"\)"),
    dict(id="K22_efs_nonpcr", pdf=K22, keys=g("events_pembro", "n_pembro", "events_placebo", "n_placebo", "hr", "hr_lo", "hr_hi", "figure"),
         rx=r"Among patients without a pathological complete response, " + N + " of " + N + r" \([\d.]+%\) in the " + PEM + CHEMO
            + " group and " + N + " of " + N + r" \([\d.]+%\) in the placebo" + CHEMO + r" group had an event or died \(hazard ratio, "
            + F + r"; 95% CI, " + F + " to " + F + r"\) \((Fig\. S4)\)"),
    # ---- Schmid 2024 (IA7, final OS) ----
    dict(id="K24_cutoff", pdf=K24, keys=g("data_cutoff", "median_fu_months", "fu_min", "fu_max"),
         rx=r"data-cutoff date, (March 22, 2024)\), the median duration of follow-up was " + F + r" months \(range, " + F + " to " + F + r"\)"),
    dict(id="K24_os_origin", pdf=K24, keys=g("origin"),
         rx=r"Overall survival, defined as the time from (randomization) to death from any cause"),
    dict(id="K24_os_events", pdf=K24, keys=g("events_pembro", "events_placebo", "p_value"),
         rx=r"including " + N + r" patients \([\d.]+%\) in the " + PEM + CHEMO + " group and " + N + r" patients \([\d.]+%\) in the placebo"
            + CHEMO + r" group \(P = " + F + r"\) \(Fig\. 1A\)"),
    dict(id="K24_os_milestones", pdf=K24,
         keys=g("pembro_3y", "pembro_3y_lo", "pembro_3y_hi", "placebo_3y", "placebo_3y_lo", "placebo_3y_hi",
                "pembro_4y", "pembro_4y_lo", "pembro_4y_hi", "placebo_4y", "placebo_4y_lo", "placebo_4y_hi",
                "pembro_5y", "pembro_5y_lo", "pembro_5y_hi", "placebo_5y", "placebo_5y_lo", "placebo_5y_hi"),
         rx=r"respectively, was " + F + r"% \(95% confidence interval \[CI\], " + F + " to " + F + r"\) and " + F + r"% \(95% CI, " + F + " to " + F
            + r"\) at 3 years, " + F + r"% \(95% CI, " + F + " to " + F + r"\) and " + F + r"% \(95% CI, " + F + " to " + F
            + r"\) at 4 years, and " + F + r"% \(95% CI, " + F + " to " + F + r"\) and " + F + r"% \(95% CI, " + F + " to " + F + r"\) at 5 years"),
    dict(id="K24_os_piecewise_hr", pdf=K24, keys=g("hr_early", "hr_early_lo", "hr_early_hi", "cut_years", "hr_late", "hr_late_lo", "hr_late_hi", "weighted_hr"),
         rx=r"unstratified piecewise hazard ratio for death was " + F + r" \(95% CI, " + F + " to " + F + r"\) before the (\d+)-year follow-up and "
            + F + r" \(95% CI, " + F + " to " + F + r"\) afterwards\. The weighted average hazard ratio with weights of number of events before and after 2-year follow-up was ([\d.]+[\d])"),
    dict(id="K24_efs_events_hr_5y", pdf=K24,
         keys=g("events_pembro", "events_placebo", "hr", "hr_lo", "hr_hi", "pembro_5y", "pembro_5y_lo", "pembro_5y_hi", "placebo_5y", "placebo_5y_lo", "placebo_5y_hi"),
         rx=r"A total of " + N + r" patients \([\d.]+%\) in the " + PEM + CHEMO + " group and " + N + r" patients \([\d.]+%\) in the placebo"
            + CHEMO + r" group had an event or died \(hazard ratio, " + F + r"; 95% CI, " + F + " to " + F + r"\) \(Fig\. 2A\)\. The estimated 5-year event-?free survival was "
            + F + r"% \(95% CI, " + F + " to " + F + r"\) in the " + PEM + CHEMO + " group and " + F + r"% \(95% CI, " + F + " to " + F + r"\)"),
    dict(id="K24_efs_composition", pdf=K24,
         keys=g("any_pembro", "any_placebo", "prog_pembro", "prog_placebo", "local_pembro", "local_placebo",
                "distant_pembro", "distant_placebo", "second_primary_pembro", "second_primary_placebo", "death_pembro", "death_placebo"),
         rx=r"Any event " + N + " " + PCT + " " + N + " " + PCT + r" Progression of disease that precluded definitive surgery " + N + " " + PCT + " " + N + " " + PCT
            + r" Local recurrence " + N + " " + PCT + " " + N + " " + PCT + r" Distant recurrence " + N + " " + PCT + " " + N + " " + PCT
            + r" Second primary cancer " + N + " " + PCT + " " + N + " " + PCT + r" Death " + N + " " + PCT + " " + N + " " + PCT),
    dict(id="K24_os_pcr", pdf=K24, keys=g("deaths_pembro", "n_pembro", "deaths_placebo", "n_placebo", "diff_5y", "diff_5y_lo", "diff_5y_hi"),
         rx=r"in the population with a pathological complete response, " + N + " of " + N + r" patients \([\d.]+%\) in the " + PEM + CHEMO
            + " group and " + N + " of " + N + r" patients \([\d.]+%\) in the placebo" + CHEMO
            + r" group had died \(absolute difference in 5-year survival, " + F + r" percentage points; 95% CI, " + SF + " to " + F + r"\)"),
    dict(id="K24_os_nonpcr", pdf=K24, keys=g("deaths_pembro", "n_pembro", "deaths_placebo", "n_placebo", "diff_5y", "diff_5y_lo", "diff_5y_hi", "figure"),
         rx=r"In the population without a pathological complete response, " + N + " of " + N + r" patients \([\d.]+%\) in the " + PEM + CHEMO
            + " group and " + N + " of " + N + r" patients \([\d.]+%\) in the placebo" + CHEMO
            + r" group had died \(absolute difference in 5-year survival, " + F + r" percentage points; 95% CI, " + SF + " to " + F + r"\) \((Fig\. S4)\)"),
    # ---- Supplementary appendices ----
    dict(id="K22A_S3_caption", pdf=K22A, keys=g("figure", "endpoint", "population", "model"),
         rx=r"(Fig\. S3)\. Kaplan-Meier Estimates of (Distant Progression- or Distant Recurrence- Free Survival) According to Treatment Group in the "
            r"(Intention-to-Treat Population)\..*?(Cox regression model with treatment as a covariate stratified by the randomization stratification factors)"),
    dict(id="K22A_S4_caption", pdf=K22A, keys=g("figure", "endpoint", "population", "model"),
         rx=r"(Fig\. S4)\. Kaplan-Meier Estimates of (Event-Free Survival by Pathological Complete Response \(ypT0/Tis ypN0\)) According to Treatment Group in the "
            r"(Intention-to-Treat Population)\..*?(Cox regression model with treatment as a covariate)\."),
    dict(id="K24A_S4_caption", pdf=K24A, keys=g("figure", "endpoint", "population"),
         rx=r"(Fig\. S4)\. Kaplan-Meier Estimates of (Overall Survival by Pathological Complete Response \(ypT0/Tis ypN0\)) According to Treatment Group in the "
            r"(Intention-to-Treat Population)\."),
    dict(id="K22A_ae_deaths", pdf=K22A,
         keys=g("n_astreated_pembro", "n_astreated_placebo", "died_pembro", "died_placebo", "died_drug_related_pembro", "died_drug_related_placebo"),
         rx=r"Table S5\. Summary of Tier 2 Adverse Events during the Combined Phases\. Participants in Population Pembrolizumab– ?Chemotherapy"
            r" \(N=(\d+)\) Placebo– ?Chemotherapy ?\( ?N=(\d+)\).*?who died (\d+) \([\d.]+\) (\d+) \([\d.]+\).*?who died due to a drug-related adverse event (\d+) \([\d.]+\) (\d+) \([\d.]+\)"),
    dict(id="K22_treatment_end", pdf=K22, keys=g("all_completed_by"),
         rx=r"All the patients completed trial treatment by (February 2020)"),
    dict(id="K24_tr_deaths", pdf=K24, keys=g("pembro", "placebo"),
         rx=r"Treatment-? ?related adverse events led to death in (\d+) patients \([\d.]+%\) and in (\d+) patient \([\d.]+%\), respectively"),
    dict(id="K24A_os_hr", pdf=K24A, keys=g("hr", "hr_lo", "hr_hi"),
         rx=r"hazard ratio for overall survival based on the protocol-specified Cox regression model is " + F + r" \(95% CI, " + F + "-" + r"([\d.]+[\d])\)"),
    # ---- Yau 2022 ----
    dict(id="Y22_origin", pdf=YAU, keys=g("origin"),
         rx=r"measured as time from (start of neoadjuvant treatment)"),
    dict(id="Y22_efs_definition", pdf=YAU, keys=g("definition"),
         rx=r"(Any locoregional recurrence, distant recurrence, or death from any cause) was considered as an event-free survival event"),
    dict(id="Y22_truncation", pdf=YAU, keys=g("years"),
         rx=r"survival times truncated at (\d+) years"),
    dict(id="Y22_events", pdf=YAU, keys=g("events_all", "events_tnbc"),
         rx=r"Event-free survival events (\d+) (\d+)"),
    dict(id="Y22_tnbc_S2", pdf=YAUA,
         keys=g("N", "n_rcb0", "rcb0_3y", "rcb0_5y", "rcb0_10y",
                "n_rcb1", "rcb1_3y", "rcb1_5y", "rcb1_10y", "hr_rcb1", "hr_rcb1_lo", "hr_rcb1_hi",
                "n_rcb2", "rcb2_3y", "rcb2_5y", "rcb2_10y", "hr_rcb2", "hr_rcb2_lo", "hr_rcb2_hi",
                "n_rcb3", "rcb3_3y", "rcb3_5y", "rcb3_10y", "hr_rcb3", "hr_rcb3_lo", "hr_rcb3_hi"),
         rx=r"HR-HER2- \((\d+)\) RCB \(continuous index\).*?RCB Class RCB-0 (\d+) \(\d+%\) (\d+)% \(\d+%-\d+%\) (\d+)% \(\d+%-\d+%\) (\d+)% \(\d+%-\d+%\) Ref"
            r".*?RCB-I (\d+) \(\d+%\) (\d+)% \(\d+%-\d+%\) (\d+)% \(\d+%-\d+%\) (\d+)% \(\d+%-\d+%\) ([\d.]+) \(([\d.]+)-([\d.]+)\)"
            r".*?RCB-II (\d+) \(\d+%\) (\d+)% \(\d+%-\d+%\) (\d+)% \(\d+%-\d+%\) (\d+)% \(\d+%-\d+%\) ([\d.]+) \(([\d.]+)-([\d.]+)\)"
            r".*?RCB-III (\d+) \(\d+%\) (\d+)% \(\d+%-\d+%\) (\d+)% \(\d+%-\d+%\) (\d+)% \(\d+%-\d+%\) ([\d.]+) \(([\d.]+)-([\d.]+)\)"),
]
