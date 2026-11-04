# test_four_arm.R
# Unit tests of icer_table() in R/25_four_arm.R (docs/analysis_plan_phase2.md section 11.2):
#  (a) toy data, input order shuffled, against hand calculation (status, dominated_by, comparator, increments, ICER)
#      and against the status from frontier() of R/econ.R:
#      toy 1: one strictly dominated option (dominated by an option that is itself extendedly dominated) and one
#             extendedly dominated option;
#      toy 2: an option dominated by two others, and two equal adjacent ICERs (not extended dominance: the rule is
#             "strictly higher");
#  (b) the status recomputed from output/phase2/main/fourarm_totals.csv (cost for E02, and cost_E01, cost_E03; qaly)
#      equals that in fourarm_incremental.csv (needs the outputs of Rscript R/25_four_arm.R).
# source() of R/25_four_arm.R makes the definitions only (its computation runs under Rscript).
# Output: output/phase2/main/fourarm_unit_tests.csv (test, result, detail).

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "25_four_arm.R"))
R <- list()
rec <- function(test, ok, detail = "") R[[length(R) + 1]] <<- data.frame(test = test, result = if (isTRUE(ok)) "pass" else "FAIL", detail = detail)
same_num <- function(x, y) all((is.na(x) & is.na(y)) | (!is.na(x) & !is.na(y) & abs(x - y) < 1e-12))

# toy 1, by hand. Sorted by cost: A (0, 0), B (100, 0.5), C (150, 0.4), D (300, 2).
#  strict: C is dominated by B (100 <= 150, 0.5 >= 0.4); nothing else is (A is cheapest; D has the most QALYs).
#  extended: A, B, D -> ICER B vs A = 100 / 0.5 = 200 > ICER D vs B = 200 / 1.5 = 133.3 -> B removed (between A and D);
#            A, D -> ICER D vs A = 300 / 2 = 150.
#  comparators (nearest cheaper option on the final frontier A, D): B -> A, C -> A, D -> A.
t1 <- icer_table(cost = c(300, 100, 0, 150), qaly = c(2, 0.5, 0, 0.4), arm = c("D", "B", "A", "C"))
e1 <- data.frame(arm = c("A", "B", "C", "D"), comparator = c("", "A", "A", "A"), d_cost = c(NA, 100, 150, 300), d_qaly = c(NA, 0.5, 0.4, 2),
                 icer = c(NA, 200, NA, 150), status = c("frontier", "extendedly dominated", "dominated", "frontier"), dominated_by = c("", "A/D", "B", ""),
                 stringsAsFactors = FALSE)
rec("toy1_order", identical(t1$arm, e1$arm), paste(t1$arm, collapse = ","))
rec("toy1_status", identical(t1$status, e1$status), paste(t1$status, collapse = ","))
rec("toy1_dominated_by", identical(t1$dominated_by, e1$dominated_by), paste(t1$dominated_by, collapse = ","))
rec("toy1_comparator", identical(t1$comparator, e1$comparator), paste(t1$comparator, collapse = ","))
rec("toy1_increments_icer", same_num(t1$d_cost, e1$d_cost) && same_num(t1$d_qaly, e1$d_qaly) && same_num(t1$icer, e1$icer),
    paste(signif(t1$icer, 6), collapse = ","))
fr1 <- frontier(data.frame(arm = c("D", "B", "A", "C"), cost = c(300, 100, 0, 150), qaly = c(2, 0.5, 0, 0.4)))
rec("toy1_vs_econ_frontier", identical(fr1$status[match(t1$arm, fr1$arm)], t1$status), paste(fr1$status, collapse = ","))

# toy 2, by hand. Sorted by cost: X (0, 0), Y (50, 1), Z (60, 1.2), W (100, 0.9).
#  strict: W is dominated by Y and by Z (both cheaper with more QALYs) -> "Y/Z".
#  extended: X, Y, Z -> ICER Y vs X = 50, Z vs Y = 10 / 0.2 = 50: equal, not strictly higher -> all three on the frontier.
#  comparators: Y -> X, Z -> Y, W -> Z (d_cost 40, d_qaly -0.3, no ICER).
t2 <- icer_table(cost = c(100, 60, 0, 50), qaly = c(0.9, 1.2, 0, 1), arm = c("W", "Z", "X", "Y"))
e2 <- data.frame(arm = c("X", "Y", "Z", "W"), comparator = c("", "X", "Y", "Z"), d_cost = c(NA, 50, 10, 40), d_qaly = c(NA, 1, 0.2, -0.3),
                 icer = c(NA, 50, 50, NA), status = c("frontier", "frontier", "frontier", "dominated"), dominated_by = c("", "", "", "Y/Z"),
                 stringsAsFactors = FALSE)
rec("toy2_status_dominated_by", identical(t2$arm, e2$arm) && identical(t2$status, e2$status) && identical(t2$dominated_by, e2$dominated_by),
    paste(t2$status, t2$dominated_by, collapse = ","))
rec("toy2_comparator_increments", identical(t2$comparator, e2$comparator) && same_num(t2$d_cost, e2$d_cost) && same_num(t2$d_qaly, e2$d_qaly) &&
      same_num(t2$icer, e2$icer), paste(signif(t2$d_qaly, 6), collapse = ","))
fr2 <- frontier(data.frame(arm = c("W", "Z", "X", "Y"), cost = c(100, 60, 0, 50), qaly = c(0.9, 1.2, 0, 1)))
rec("toy2_vs_econ_frontier", identical(fr2$status[match(t2$arm, fr2$arm)], t2$status), paste(fr2$status, collapse = ","))

# (b) the model results: status from fourarm_totals.csv = fourarm_incremental.csv
TOT <- read.csv(file.path(OUT, FILES[["totals"]]), stringsAsFactors = FALSE)
INC <- read.csv(file.path(OUT, FILES[["incremental"]]), stringsAsFactors = FALSE)
INC$dominated_by[is.na(INC$dominated_by)] <- ""
for (en in c("E02", "E01", "E03")) {
  ok <- TRUE; n <- 0
  for (h in unique(TOT$hr0)) {
    d <- TOT[TOT$hr0 == h, ]
    r <- icer_table(switch(en, E02 = d$cost, E01 = d$cost_E01, E03 = d$cost_E03), d$qaly, d$arm)
    s <- INC[abs(INC$hr0 - h) < 1e-12 & INC$programme == en, ]
    m <- match(r$arm, s$arm)
    ok <- ok && nrow(s) == 4 && !anyNA(m) && identical(r$status, s$status[m]) && identical(r$dominated_by, s$dominated_by[m])
    n <- n + nrow(s)
  }
  rec(sprintf("totals_vs_incremental_%s", en), ok && n == 12, sprintf("%d rows (3 hr0 x 4 arms)", n))
}

R <- do.call(rbind, R)
write.csv(R, file.path(OUT, FILES[["unit"]]), row.names = FALSE, fileEncoding = "UTF-8")
print(R, row.names = FALSE)
stopifnot(all(R$result == "pass"))
cat(sprintf("test_four_arm: %d/%d passed\n", sum(R$result == "pass"), nrow(R)))
