# 26_recurrence_reduction.R
# Absolute reduction in recurrence with exercise (Online Resource 1, Supplementary Table S12).
# For chemotherapy plus pembrolizumab and chemotherapy alone, at recurrence hazard ratios (HRs) with exercise of
# 1.00 (reference), 0.991, 0.989, 0.966, 0.958, 0.95, 0.85 and 0.72, the cumulative proportion of the modeled cohort
#   (a) distant: with a first entry into distant recurrence (early or late) after surgery, including entry from
#       locoregional recurrence; each patient is counted once (distant recurrence is entered at most once);
#   (b) any: with a first entry into locoregional or distant recurrence after surgery (the range of the exposure,
#       the HR for locoregional and distant recurrence after surgery); locoregional recurrence followed by distant
#       recurrence is counted once, at the locoregional recurrence,
# by 5 and 7 years after randomization (model months 60 and 84; month 0 = start of neoadjuvant chemotherapy =
# randomization in KEYNOTE-522), per 100 women entering the model (both pCR strata, including those whose disease
# progressed before surgery). Progression before surgery (PreProg) is not a recurrence and is not counted.
# Output: the proportion without exercise (HR 1.00) and the absolute difference, without minus with exercise.
#
# Setting: the deterministic base case. Base parameters (data/fits/engine_params.rds; no external k, no S-JP), the
# exercise effect held for 5 years after randomization, after which 1 - HR halves every year (path_a("base") of
# R/25_four_arm.R; wane_start 5, wane_rate log 2). The HR multiplies the transitions from event-free to
# locoregional and to distant recurrence after surgery (R/engine.R). The engine is taken from econ_arm() exactly as
# in the cost model; the program cost does not enter the survival results.
#
# Method: cumulative sums of the per-cycle inflows (occupancy at the start of the cycle x transition probability)
# that the engine returns at the boundary where the entrants arrive (In_DR, In_LRR), not occupancies at month t
# (patients who die after recurrence would be lost).
#   (a) = cumsum(In_DR); In_DR holds the entries from event-free and from locoregional recurrence.
#   (b) = cumsum(In_LRR + In_DR_from_EF), where In_DR_from_EF = In_DR - (locoregional -> distant inflow), and the
#       locoregional -> distant inflow per cycle is the first difference of the locoregional balance
#       cumsum(In_LRR) - LRR - Dead_from_LRR (all who entered LRR are still there, died from LRR or moved to DR).
#   Check of (b) by an independent balance of the event-free state: 1 - EF - cumsum(In_PreProg) - Dead_from_EF -
#   Dead_from_AE (all exits from event-free that are not progression before surgery or death).
#
# Checks (the script stops if one fails): HR 1.00 difference 0 (the exercise arm at HR 1 equals the arm without
# exercise); the two computations of (b) agree; the difference rises as the HR falls; the 7-year difference is at
# least the 5-year difference; (a) <= (b) <= 1 - EFS(t) at HR 1.00; no recurrence inflow before surgery; at HRs 0.95,
# 0.85 and 0.72 the total costs and QALYs of econ_arm() equal output/phase2/main/fourarm_totals.csv (same base case
# as Table 2), when that file exists.
#
# Usage (from the repository root, after R/00_lifetable.R and R/10_read_params.R):
#   Rscript R/26_recurrence_reduction.R
# writes output/phase2/main/recurrence_reduction.csv (one row per group x HR x outcome x month) and prints the
# table and the comparison with KEYNOTE-522 (distant recurrence or distant progression as the first event).

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "."), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R")); source(file.path(ROOT, "R", "engine.R")); source(file.path(ROOT, "R", "econ.R"))
suppressPackageStartupMessages(library(survival))
OUT <- file.path(ROOT, "output", "phase2", "main"); dir.create(OUT, recursive = TRUE, showWarnings = FALSE)

# ---- read-in as in R/25_four_arm.R (lines 23-31 and the base definition of path_a)
P <- readRDS(file.path(ROOT, "data", "fits", "engine_params.rds"))
PL <- read.csv(file.path(ROOT, "data", "params_long.csv"), stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)
PD <- read.csv(file.path(ROOT, "data", "params_dist.csv"), stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)
B0 <- PL[PL$stat == "基本値", ]
stopifnot(identical(B0$param_id, PD$param_id), !anyNA(B0$value))
note_of <- setNames(B0$備考, B0$param_id)
u05_weeks <- as.numeric(sub(".*期間 ([0-9.]+) 週.*", "\\1", note_of[["U05"]]))
PV0 <- c(setNames(B0$value, B0$param_id), U05_duration_years = wk(u05_weeks))
path_a_base <- function(hr0) list(hr0 = hr0, wane_start = 5, wane_rate = log(2))

HRS <- c(1.00, 0.991, 0.989, 0.966, 0.958, 0.95, 0.85, 0.72)
GROUPS <- list(chemo_pembro = c(without = "pembro", with = "both"), chemo_alone = c(without = "chemo", with = "exercise"))
MONTHS <- c(60, 84)
TOL <- 1e-12

run <- function(arm, hr0) econ_arm(arm, P, PV0, settings = list(exercise_cost = "E02"),
                                   exercise = if (has_exercise(arm)) path_a_base(hr0) else EXERCISE_NEUTRAL)

# cumulative first entries (per person) at each cycle boundary from the engine table e
cum_entries <- function(e) {
  lrr_bal <- cumsum(e$In_LRR) - e$LRR - e$Dead_from_LRR             # cumulative LRR -> DR
  l_to_d <- c(0, diff(lrr_bal))
  dr_from_ef <- e$In_DR - l_to_d
  any_flow <- cumsum(e$In_LRR + dr_from_ef)
  any_ef <- 1 - e$EF - cumsum(e$In_PreProg) - e$Dead_from_EF - e$Dead_from_AE
  list(distant = cumsum(e$In_DR), any = any_flow, any_check = any_ef, efs = e$EF, time = e$time,
       distant_first = cumsum(dr_from_ef),                              # distant recurrence as the first event (diagnostic)
       min_l_to_d = min(l_to_d), min_dr_from_ef = min(dr_from_ef),
       pre_inflow = sum((e$In_DR + e$In_LRR)[e$time < P$L - 1e-9]))
}
at_month <- function(x, time, m) { i <- which(abs(time * 12 - m) < 1e-6); stopifnot(length(i) == 1); x[i] }

rows <- list(); checks <- list(); cmp <- list()
chk <- function(name, ok, detail = "") { checks[[length(checks) + 1]] <<- data.frame(check = name, pass = ok, detail = detail); if (!ok) stop("check failed: ", name, " ", detail) }

for (g in names(GROUPS)) {
  arms <- GROUPS[[g]]
  r0 <- run(arms[["without"]], 1)
  c0 <- cum_entries(r0$engine)
  # exercise arm at HR 1 equals the arm without exercise
  c1 <- cum_entries(run(arms[["with"]], 1)$engine)
  chk(paste(g, "HR 1 exercise arm = arm without exercise"),
      max(abs(c1$distant - c0$distant), abs(c1$any - c0$any)) < TOL)
  for (hr in HRS) {
    ce <- if (hr == 1) c0 else cum_entries(run(arms[["with"]], hr)$engine)
    chk(sprintf("%s HR %.3f two computations of any recurrence agree", g, hr), max(abs(ce$any - ce$any_check)) < 1e-12,
        sprintf("max |diff| %.2e", max(abs(ce$any - ce$any_check))))
    chk(sprintf("%s HR %.3f inflows not negative", g, hr), ce$min_l_to_d > -1e-15 && ce$min_dr_from_ef > -1e-15)
    chk(sprintf("%s HR %.3f no recurrence inflow before surgery", g, hr), abs(ce$pre_inflow) < 1e-15)
    for (o in c("distant", "any")) for (m in MONTHS) {
      p0 <- at_month(c0[[o]], c0$time, m); p1 <- at_month(ce[[o]], ce$time, m)
      rows[[length(rows) + 1]] <- data.frame(group = g, arm_without = arms[["without"]], arm_with = arms[["with"]], hr = hr,
                                             outcome = o, month = m, years = m / 12,
                                             pct_without = 100 * p0, pct_with = 100 * p1, diff_pp = 100 * (p0 - p1))
    }
  }
  # HR 1.00 against 1 - EFS(t) and (a) <= (b)
  for (m in MONTHS) {
    a <- at_month(c0$distant, c0$time, m); b <- at_month(c0$any, c0$time, m); f <- 1 - at_month(c0$efs, c0$time, m)
    chk(sprintf("%s month %d distant <= any <= 1 - EFS", g, m), a <= b + 1e-15 && b <= f + 1e-15,
        sprintf("distant %.4f%%, any %.4f%%, 1 - EFS %.4f%%", 100 * a, 100 * b, 100 * f))
  }
  # comparison with KEYNOTE-522 (Schmid 2022, distant recurrence or distant progression as first event, median
  # follow-up 39 months): model distant recurrence after surgery at 39 months without exercise, all entries and
  # first events only (entries from event-free, as the trial counted first events)
  cmp[[g]] <- 100 * c(all = at_month(c0$distant, c0$time, 39), first = at_month(c0$distant_first, c0$time, 39))
}
R <- do.call(rbind, rows)

for (g in names(GROUPS)) for (o in c("distant", "any")) {
  s <- R[R$group == g & R$outcome == o, ]
  chk(sprintf("%s %s HR 1.00 difference 0", g, o), all(s$diff_pp[s$hr == 1] == 0))
  for (m in MONTHS) {
    d <- s$diff_pp[s$month == m][order(-s$hr[s$month == m])]
    chk(sprintf("%s %s month %d difference rises as HR falls", g, o, m), all(diff(d) > 0), paste(sprintf("%.4f", d), collapse = " "))
  }
  d5 <- s$diff_pp[s$month == 60][order(-s$hr[s$month == 60])]; d7 <- s$diff_pp[s$month == 84][order(-s$hr[s$month == 84])]
  chk(sprintf("%s %s 7-year difference >= 5-year difference", g, o), all(d7 >= d5 - 1e-12))
}

# same base case as Table 2: total costs and QALYs at HRs 0.95, 0.85 and 0.72 against fourarm_totals.csv
ft_path <- file.path(OUT, "fourarm_totals.csv")
if (file.exists(ft_path)) {
  ft <- read.csv(ft_path, stringsAsFactors = FALSE)
  dev <- 0
  for (hr in c(0.95, 0.85, 0.72)) for (a in c("exercise", "both")) {
    r <- run(a, hr); f <- ft[abs(ft$hr0 - hr) < 1e-9 & ft$arm == a, ]
    dev <- max(dev, abs(r$cost - f$cost) / f$cost, abs(r$qaly - f$qaly) / f$qaly)
  }
  chk("costs and QALYs equal fourarm_totals.csv (HR 0.95, 0.85, 0.72)", dev < 1e-9, sprintf("max relative deviation %.2e", dev))
} else {
  checks[[length(checks) + 1]] <- data.frame(check = "costs and QALYs equal fourarm_totals.csv", pass = NA, detail = "file not present; not checked")
}

hu <- function(x, d) { y <- sign(x) * floor(round(abs(x) * 10^d, 6) + 0.5) / 10^d; y[y == 0] <- 0; y }
R$pct_without_2dp <- hu(R$pct_without, 2); R$diff_pp_2dp <- hu(R$diff_pp, 2)
write.csv(R, file.path(OUT, "recurrence_reduction.csv"), row.names = FALSE, fileEncoding = "UTF-8")
CH <- do.call(rbind, checks)
write.csv(CH, file.path(OUT, "recurrence_reduction_checks.csv"), row.names = FALSE, fileEncoding = "UTF-8")

cat("Without exercise (HR 1.00), cumulative % per 100 women:\n")
w <- R[R$hr == 1, c("group", "outcome", "month", "pct_without")]; w$pct_without <- sprintf("%.2f", w$pct_without); print(w, row.names = FALSE)
cat("\nAbsolute reduction with exercise, percentage points (2 decimals, half up):\n")
for (g in names(GROUPS)) {
  s <- R[R$group == g, ]
  cat(g, "\n")
  for (hr in HRS) {
    z <- s[s$hr == hr, ]
    cat(sprintf("  HR %.3f  distant 5y %.2f  7y %.2f | any 5y %.2f  7y %.2f\n", hr,
                z$diff_pp_2dp[z$outcome == "distant" & z$month == 60], z$diff_pp_2dp[z$outcome == "distant" & z$month == 84],
                z$diff_pp_2dp[z$outcome == "any" & z$month == 60], z$diff_pp_2dp[z$outcome == "any" & z$month == 84]))
  }
}
cat(sprintf(paste0("\nKEYNOTE-522 (Schmid 2022): distant recurrence or progression as first event 7.7%% (pembrolizumab), 13.1%% (placebo), median follow-up 39 months.\n",
                   "Model, distant recurrence after surgery at month 39 without exercise: %.2f%% (chemotherapy plus pembrolizumab), %.2f%% (chemotherapy alone);\n",
                   "as the first event only (excluding locoregional -> distant): %.2f%%, %.2f%%.\n"),
            cmp$chemo_pembro[["all"]], cmp$chemo_alone[["all"]], cmp$chemo_pembro[["first"]], cmp$chemo_alone[["first"]]))
cat(sprintf("\nchecks: %d run, %d passed, %d not run\n", nrow(CH), sum(CH$pass %in% TRUE), sum(is.na(CH$pass))))
cat("26_recurrence_reduction.R finished\n")
