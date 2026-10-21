# 03_reconstruct_ipd.R
# Step 3: Guyot reconstruction of every digitized curve, cross-checked against
# IPDfromKM::getIPD, and validation against the reported values.
# Gates (task spec): milestone |diff| <= 1 percentage point; Cox HR |diff| <= 0.03;
# events |diff| <= 2% of the reported count. Yau 2022: only the milestones are gates
# (decision of 2026-10-21); its HR and event checks are reported with gate = FALSE.
# Outputs: data/ipd/<fig>_<arm>.csv, data/ipd/ipd_all.rds,
#          output/phase1/validation.csv, output/phase1/validation_diagnostics.csv

root <- "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"
source(file.path(root, "R", "guyot.R"))
suppressPackageStartupMessages({
  library(survival)
  library(IPDfromKM)
  library(jsonlite)
})

dig <- file.path(root, "data", "digitized")
ipd_dir <- file.path(root, "data", "ipd")
out_dir <- file.path(root, "output", "phase1")
dir.create(ipd_dir, showWarnings = FALSE, recursive = TRUE)
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

rv <- read.csv(file.path(root, "data", "reported_values.csv"), stringsAsFactors = FALSE, encoding = "UTF-8")
val <- function(id, key) {
  x <- rv$value[rv$fact_id == id & rv$key == key]
  if (length(x) != 1) stop("reported value missing: ", id, "/", key)
  as.numeric(x)
}
ref <- function(id) {
  r <- rv[rv$fact_id == id, ][1, ]
  sprintf("%s p%d", sub("\\.pdf$", "", r$pdf), r$page)
}

figs <- list(
  K20_F2_EFS  = list(arms = c("pembro", "placebo"), unit = "months", endpoint = "EFS"),
  K22_F1_EFS  = list(arms = c("pembro", "placebo"), unit = "months", endpoint = "EFS"),
  K22_F3_OS   = list(arms = c("pembro", "placebo"), unit = "months", endpoint = "OS"),
  K24_F1A_OS  = list(arms = c("pembro", "placebo"), unit = "months", endpoint = "OS"),
  K24_F2A_EFS = list(arms = c("pembro", "placebo"), unit = "months", endpoint = "EFS"),
  Y22_F4A_EFS_TNBC = list(arms = c("RCB0", "RCB1", "RCB2", "RCB3"), unit = "years", endpoint = "EFS"),
  K22_S3_DRFS = list(arms = c("pembro", "placebo"), unit = "months", endpoint = "DRFS"),
  K22_S4_EFS_pCR = list(arms = c("pembro_pCR", "placebo_pCR", "pembro_nonpCR", "placebo_nonpCR"), unit = "months", endpoint = "EFS"),
  K24_S4_OS_pCR = list(arms = c("pembro_pCR", "placebo_pCR", "pembro_nonpCR", "placebo_nonpCR"), unit = "months", endpoint = "OS")
)
rspec <- fromJSON(file.path(root, "R", "py", "rasterspec.json"), simplifyVector = FALSE)$figures
names(rspec) <- vapply(rspec, function(f) f$fig_id, "")
img <- function(fig) rspec[[fig]]$reported_in_image
img_ref <- function(fig) sprintf("%s p%d (printed in figure, transcribed)", sub("\\.pdf$", "", rspec[[fig]]$pdf), rspec[[fig]]$page)

# ---------------------------------------------------------------- reconstruction
ipd <- list(); diag <- list()
for (fig in names(figs)) {
  rt <- read.csv(file.path(dig, paste0(fig, "_risktable.csv")))
  for (arm in figs[[fig]]$arms) {
    cv <- read.csv(file.path(dig, sprintf("%s_%s_curve.csv", fig, arm)))
    r <- rt[rt$arm == arm, ]
    prep <- guyot_prepare(cv$time, cv$surv_pct / 100, r$time, r$n_risk)
    g <- guyot(prep)
    # cross-check: IPDfromKM's Guyot core on the same prepared points (its preprocess()
    # outlier filter is meant for hand-clicked points and is bypassed)
    pk <- structure(list(
      preprocessdat = data.frame(time = prep$t.S, surv = prep$S, id = seq_along(prep$t.S),
                                 interval = findInterval(seq_along(prep$t.S), prep$lower)),
      intervalIndex = data.frame(interval = seq_along(prep$t.risk), lower = prep$lower, upper = prep$upper,
                                 t.risk = prep$t.risk, n.risk = prep$n.risk),
      endpts = NULL, inputdat = data.frame(time = cv$time, surv = cv$surv_pct / 100)), class = "preKM")
    gi <- tryCatch(getIPD(pk, armID = 1)$IPD, error = function(e) NULL)
    key <- paste(fig, arm, sep = "_")
    tyears <- if (figs[[fig]]$unit == "months") g$time / 12 else g$time
    d <- data.frame(fig = fig, arm = arm, time = g$time, time_years = tyears, status = g$status)
    ipd[[key]] <- d
    write.csv(d, file.path(ipd_dir, paste0(key, ".csv")), row.names = FALSE)

    # diagnostics: KM of the IPD vs the digitized step function
    km <- survfit(Surv(time, status) ~ 1, data = g)
    grid <- sort(unique(c(prep$t.S)))
    s_ipd <- summary(km, times = grid, extend = TRUE)$surv
    s_dig <- vapply(grid, function(t) min(prep$S[prep$t.S <= t + 1e-9]), 0)
    # risk table reproduction
    nr <- vapply(r$time, function(t) sum(g$time >= t - 1e-9), 0)
    nr_ok <- r$time <= max(prep$t.S)
    # IPDfromKM agreement
    if (!is.null(gi)) {
      km2 <- survfit(Surv(time, status) ~ 1, data = gi)
      s2 <- summary(km2, times = grid, extend = TRUE)$surv
      ev2 <- sum(gi$status)
    } else { s2 <- NA; ev2 <- NA }
    # drawn censor marks (vector figures) vs Guyot censorings per risk interval
    cen_file <- file.path(dig, sprintf("%s_%s_censor.csv", fig, arm))
    cen_cmp <- NA
    if (file.exists(cen_file)) {
      cm <- read.csv(cen_file)$time
      br <- c(r$time[nr_ok], Inf)
      a <- table(cut(cm, br, right = FALSE))
      b <- table(cut(g$time[g$status == 0], br, right = FALSE))
      cen_cmp <- paste(sprintf("%d/%d", as.integer(a), as.integer(b)), collapse = ";")
      n_marks <- length(cm)
    } else n_marks <- NA
    diag[[key]] <- data.frame(
      curve = key, n = nrow(g), events_guyot = sum(g$status), events_ipdfromkm = ev2,
      max_abs_km_vs_digitized_pp = round(100 * max(abs(s_ipd - s_dig)), 3),
      max_abs_guyot_vs_ipdfromkm_pp = round(100 * max(abs(s_ipd - s2)), 3),
      max_abs_risk_table_diff = max(abs(nr[nr_ok] - r$n_risk[nr_ok])),
      censor_marks_drawn = n_marks, censored_guyot = sum(g$status == 0),
      censored_by_interval_marks_vs_guyot = cen_cmp)
    cat(sprintf("%-26s n=%4d events=%4d (IPDfromKM %s)  max|KM-dig|=%.3f pp  max|riskdiff|=%d\n",
                key, nrow(g), sum(g$status), ev2, 100 * max(abs(s_ipd - s_dig)), max(abs(nr[nr_ok] - r$n_risk[nr_ok]))))
  }
}
saveRDS(ipd, file.path(ipd_dir, "ipd_all.rds"))
write.csv(do.call(rbind, diag), file.path(out_dir, "validation_diagnostics.csv"), row.names = FALSE)

# ---------------------------------------------------------------- validation
V <- list()
addv <- function(curve, check, time, unit, reported, recon, tol, reference, note = "", gate = TRUE) {
  diff <- recon - reported
  ok <- switch(check,
               milestone = abs(diff) <= tol + 1e-9,
               milestone_diff = abs(diff) <= tol + 1e-9,
               hr = abs(diff) <= tol + 1e-9,
               events = abs(diff) <= tol * reported + 1e-9)
  V[[length(V) + 1]] <<- data.frame(curve = curve, check = check, time = time, unit = unit,
                                    reported = reported, reconstructed = round(recon, 4),
                                    abs_diff = round(abs(diff), 4),
                                    tolerance = ifelse(check == "events", sprintf("2%% (%.2f)", tol * reported), as.character(tol)),
                                    pass = ok, gate = gate, reference = reference, note = note)
}
km_at <- function(d, t) 100 * summary(survfit(Surv(time, status) ~ 1, data = d), times = t, extend = TRUE)$surv
I <- function(fig, arm) ipd[[paste(fig, arm, sep = "_")]]
hr_arm <- function(fig, pembro = "pembro", placebo = "placebo") {
  d <- rbind(I(fig, pembro), I(fig, placebo))
  d$trt <- as.integer(d$arm == pembro)
  unname(exp(coef(coxph(Surv(time, status) ~ trt, data = d, ties = "efron"))))
}

# Schmid 2020, IA2 EFS
f <- "K20_F2_EFS"
for (a in c("pembro", "placebo")) {
  addv(paste(f, a, sep = "_"), "milestone", 18, "months", val("K20_efs_18m", a), km_at(I(f, a), 18), 1, ref("K20_efs_18m"))
  addv(paste(f, a, sep = "_"), "events", NA, "", val("K20_efs_events", paste0("events_", a)), sum(I(f, a)$status), 0.02, ref("K20_efs_events"))
}
addv(f, "hr", NA, "", val("K20_efs_hr", "hr"), hr_arm(f), 0.03, ref("K20_efs_hr"),
     "reported: stratified Cox; reconstructed: unstratified Cox")

# Schmid 2022, IA4 EFS and OS
f <- "K22_F1_EFS"
for (a in c("pembro", "placebo")) {
  addv(paste(f, a, sep = "_"), "milestone", 36, "months", val("K22_efs_36m", a), km_at(I(f, a), 36), 1, ref("K22_efs_36m"))
  addv(paste(f, a, sep = "_"), "events", NA, "", val("K22_efs_events_hr", paste0("events_", a)), sum(I(f, a)$status), 0.02, ref("K22_efs_events_hr"))
}
addv(f, "hr", NA, "", val("K22_efs_events_hr", "hr"), hr_arm(f), 0.03, ref("K22_efs_events_hr"),
     "reported: stratified Cox; reconstructed: unstratified Cox")
f <- "K22_F3_OS"
for (a in c("pembro", "placebo")) {
  addv(paste(f, a, sep = "_"), "milestone", 36, "months", val("K22_os_36m", a), km_at(I(f, a), 36), 1, ref("K22_os_36m"))
  addv(paste(f, a, sep = "_"), "events", NA, "", val("K22_os_events_hr", paste0("events_", a)), sum(I(f, a)$status), 0.02, ref("K22_os_events_hr"))
}
addv(f, "hr", NA, "", val("K22_os_events_hr", "hr"), hr_arm(f), 0.03, ref("K22_os_events_hr"),
     "reported: stratified Cox; reconstructed: unstratified Cox")

# Schmid 2024, IA7 OS and EFS
f <- "K24_F1A_OS"
for (a in c("pembro", "placebo")) {
  for (y in 3:5) addv(paste(f, a, sep = "_"), "milestone", 12 * y, "months",
                      val("K24_os_milestones", sprintf("%s_%dy", a, y)), km_at(I(f, a), 12 * y), 1, ref("K24_os_milestones"))
  addv(paste(f, a, sep = "_"), "events", NA, "", val("K24_os_events", paste0("events_", a)), sum(I(f, a)$status), 0.02, ref("K24_os_events"))
}
cut_m <- 12 * val("K24_os_piecewise_hr", "cut_years")
d <- rbind(I(f, "pembro"), I(f, "placebo")); d$trt <- as.integer(d$arm == "pembro")
ds <- survSplit(Surv(time, status) ~ trt, data = d, cut = cut_m, episode = "period")
ds$trt_early <- ds$trt * (ds$period == 1); ds$trt_late <- ds$trt * (ds$period == 2)
pw <- exp(coef(coxph(Surv(tstart, time, status) ~ trt_early + trt_late, data = ds, ties = "efron")))
addv(f, "hr", cut_m, "months (before)", val("K24_os_piecewise_hr", "hr_early"), pw[["trt_early"]], 0.03, ref("K24_os_piecewise_hr"),
     "reported: unstratified piecewise Cox, as reconstructed")
addv(f, "hr", cut_m, "months (after)", val("K24_os_piecewise_hr", "hr_late"), pw[["trt_late"]], 0.03, ref("K24_os_piecewise_hr"),
     "reported: unstratified piecewise Cox, as reconstructed")
addv(f, "hr", NA, "overall", val("K24A_os_hr", "hr"), hr_arm(f), 0.03, ref("K24A_os_hr"),
     "reported: protocol-specified stratified Cox (appendix); reconstructed: unstratified Cox")
f <- "K24_F2A_EFS"
for (a in c("pembro", "placebo")) {
  addv(paste(f, a, sep = "_"), "milestone", 60, "months", val("K24_efs_events_hr_5y", paste0(a, "_5y")), km_at(I(f, a), 60), 1, ref("K24_efs_events_hr_5y"))
  addv(paste(f, a, sep = "_"), "events", NA, "", val("K24_efs_events_hr_5y", paste0("events_", a)), sum(I(f, a)$status), 0.02, ref("K24_efs_events_hr_5y"))
}
addv(f, "hr", NA, "", val("K24_efs_events_hr_5y", "hr"), hr_arm(f), 0.03, ref("K24_efs_events_hr_5y"),
     "reported: stratified Cox; reconstructed: unstratified Cox")

# Yau 2022 TNBC by RCB class (reported KM estimates are whole percentages)
f <- "Y22_F4A_EFS_TNBC"
yrt <- read.csv(file.path(dig, paste0(f, "_risktable.csv")))
for (c in 0:3) {
  a <- paste0("RCB", c)
  for (y in c(3, 5, 10)) addv(paste(f, a, sep = "_"), "milestone", y, "years",
                              val("Y22_tnbc_S2", sprintf("rcb%d_%dy", c, y)), km_at(I(f, a), y), 1, ref("Y22_tnbc_S2"),
                              "reported value rounded to whole %")
  ev12 <- yrt$cum_events[yrt$arm == a & yrt$time == 12]
  addv(paste(f, a, sep = "_"), "events", 12, "years (cumulative)", ev12, sum(I(f, a)$status), 0.02,
       "figure risk table: N - at risk - censored at 12 y",
       "not a gate: reference derived from the published risk table, not reported in the paper", gate = FALSE)
}
d <- do.call(rbind, lapply(paste0("RCB", 0:3), function(a) I(f, a)))
d$rcb <- factor(d$arm, levels = paste0("RCB", 0:3))
hy <- exp(coef(coxph(Surv(time, status) ~ rcb, data = d, ties = "efron")))
for (c in 1:3) addv(f, "hr", NA, sprintf("RCB-%d vs RCB-0", c), val("Y22_tnbc_S2", sprintf("hr_rcb%d", c)),
                    hy[[sprintf("rcbRCB%d", c)]], 0.03, ref("Y22_tnbc_S2"),
                    "not a gate: reported = pooled 12-cohort model with cohort effects on all follow-up; reconstructed = single Cox on curves truncated at 12 y",
                    gate = FALSE)

# Schmid 2022 appendix Fig. S3, DRFS by arm (events not reported)
f <- "K22_S3_DRFS"
for (a in c("pembro", "placebo"))
  addv(paste(f, a, sep = "_"), "milestone", img(f)$milestones$time, "months", img(f)$milestones[[a]],
       km_at(I(f, a), img(f)$milestones$time), 1, img_ref(f))
addv(f, "hr", NA, "", val("K22_drfs_hr", "hr"), hr_arm(f), 0.03, ref("K22_drfs_hr"),
     "reported: stratified Cox; reconstructed: unstratified Cox")

# Schmid 2022 appendix Fig. S4, EFS by arm x pCR
f <- "K22_S4_EFS_pCR"
for (a in figs[[f]]$arms)
  addv(paste(f, a, sep = "_"), "milestone", img(f)$milestones$time, "months", img(f)$milestones[[a]],
       km_at(I(f, a), img(f)$milestones$time), 1, img_ref(f))
for (arm in c("pembro", "placebo")) {
  addv(paste(f, arm, "pCR", sep = "_"), "events", NA, "", val("K22_efs_pcr", paste0("events_", arm)),
       sum(I(f, paste0(arm, "_pCR"))$status), 0.02, ref("K22_efs_pcr"))
  addv(paste(f, arm, "nonpCR", sep = "_"), "events", NA, "", val("K22_efs_nonpcr", paste0("events_", arm)),
       sum(I(f, paste0(arm, "_nonpCR"))$status), 0.02, ref("K22_efs_nonpcr"))
}
addv(f, "hr", NA, "pCR", val("K22_efs_pcr", "hr"), hr_arm(f, "pembro_pCR", "placebo_pCR"), 0.03, ref("K22_efs_pcr"),
     "reported: unstratified Cox (appendix caption), as reconstructed")
addv(f, "hr", NA, "non-pCR", val("K22_efs_nonpcr", "hr"), hr_arm(f, "pembro_nonpCR", "placebo_nonpCR"), 0.03, ref("K22_efs_nonpcr"),
     "reported: unstratified Cox (appendix caption), as reconstructed")

# stratum HRs supplied by the user (2026-10-21), compared with the same reconstructed curves
us <- read.csv(file.path(root, "input", "user_supplied_values.csv"), stringsAsFactors = FALSE)
for (st in c("pCR", "nonpCR")) {
  u <- us[us$stratum == st, ]
  addv(f, "hr", NA, paste0(st, " (user-supplied reference)"), u$hr, hr_arm(f, paste0("pembro_", st), paste0("placebo_", st)), 0.03,
       "input/user_supplied_values.csv", paste0("reference ", u$hr, " [", u$lo, ", ", u$hi, "]: ", u$source))
}

# Schmid 2024 appendix Fig. S4, OS by arm x pCR (only deaths and 5-y differences are reported)
f <- "K24_S4_OS_pCR"
for (arm in c("pembro", "placebo")) {
  addv(paste(f, arm, "pCR", sep = "_"), "events", NA, "", val("K24_os_pcr", paste0("deaths_", arm)),
       sum(I(f, paste0(arm, "_pCR"))$status), 0.02, ref("K24_os_pcr"))
  addv(paste(f, arm, "nonpCR", sep = "_"), "events", NA, "", val("K24_os_nonpcr", paste0("deaths_", arm)),
       sum(I(f, paste0(arm, "_nonpCR"))$status), 0.02, ref("K24_os_nonpcr"))
}
addv(paste(f, "pCR", sep = "_"), "milestone_diff", 60, "months (pembro - placebo)", val("K24_os_pcr", "diff_5y"),
     km_at(I(f, "pembro_pCR"), 60) - km_at(I(f, "placebo_pCR"), 60), 1, ref("K24_os_pcr"),
     "difference in 5-y OS between arms; the arm-level 5-y values are not reported")
addv(paste(f, "nonpCR", sep = "_"), "milestone_diff", 60, "months (pembro - placebo)", val("K24_os_nonpcr", "diff_5y"),
     km_at(I(f, "pembro_nonpCR"), 60) - km_at(I(f, "placebo_nonpCR"), 60), 1, ref("K24_os_nonpcr"),
     "difference in 5-y OS between arms; the arm-level 5-y values are not reported")

V <- do.call(rbind, V)
write.csv(V, file.path(out_dir, "validation.csv"), row.names = FALSE)
cat("\nvalidation rows:", nrow(V), " gated:", sum(V$gate), " failing gates:", sum(V$gate & !V$pass),
    " failing non-gate checks:", sum(!V$gate & !V$pass), "\n")
print(V[, c("curve", "check", "time", "reported", "reconstructed", "abs_diff", "pass", "gate")], row.names = FALSE)
