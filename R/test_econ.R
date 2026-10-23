# test_econ.R
# Unit tests of the phase 2a cost and QALY layer (R/econ.R) with synthetic parameter values
# (Dr Ozaki's rows are not back yet). The survival parameters are the latest step-5 candidate
# (data/fits/calibration_candidates.rds); the tests check structure, not values.
# Output: output/phase2/econ_unit_tests.csv (test, result, the deviation or difference checked);
# no ICER is written.

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
source(file.path(ROOT, "R", "econ.R"))
suppressPackageStartupMessages(library(survival))
out_dir <- file.path(ROOT, "output", "phase2"); dir.create(out_dir, showWarnings = FALSE)
P <- readRDS(file.path(ROOT, "data", "fits", "calibration_candidates.rds"))$params
P$pembro_dr_k <- 1.5      # test value

# synthetic values (not model inputs)
ids <- c(sprintf("A%02d", 1:8), sprintf("B%02d", 1:11), paste0("B", rep(21:33, each = 2), c("P", "C")),
         "C01", "C02", "C03", sprintf("D%02d", 1:6), sprintf("E%02d", 1:5), sprintf("U%02d", 1:5))
set.seed(1)
pv <- setNames(round(runif(length(ids), 1e4, 1e6)), ids)
pv[grepl("^B[23]", ids)] <- round(runif(sum(grepl("^B[23]", ids)), 0, 0.2), 3)            # rates
pv[c("A07")] <- 0.8; pv[["D04"]] <- 8; pv[["E05"]] <- 6
pv[c("U01", "U02", "U03", "U04")] <- c(0.72, 0.80, 0.70, 0.55); pv[["U05"]] <- 0.15
pv <- c(pv, U05_duration_years = 1 / 12)
cost_ids <- setdiff(ids, c(grep("^B[23]", ids, value = TRUE), "A07", "D04", "E05", sprintf("U%02d", 1:5)))

T <- list()
add <- function(name, ok, dev) T[[length(T) + 1]] <<- data.frame(test = name, result = if (ok) "pass" else "FAIL", value = dev)

base <- lapply(setNames(ARMS, ARMS), function(a) econ_arm(a, P, pv))
# 1. all costs zero: costs are 0 and QALYs unchanged
pv0 <- pv; pv0[cost_ids] <- 0
z <- lapply(setNames(ARMS, ARMS), function(a) econ_arm(a, P, pv0))
dev <- max(sapply(ARMS, function(a) abs(z[[a]]$cost)), sapply(ARMS, function(a) abs(z[[a]]$qaly - base[[a]]$qaly)))
add("费用全为 0 时费用为 0、QALY 不变（四臂）", dev < 1e-9, dev)
# 2. all utilities 1, no AE decrement: QALY = discounted life years
pv1 <- pv; pv1[c("U01", "U02", "U03", "U04")] <- 1; pv1[["U05"]] <- 0
o <- lapply(setNames(ARMS, ARMS), function(a) econ_arm(a, P, pv1))
dev <- max(sapply(ARMS, function(a) abs(o[[a]]$qaly - o[[a]]$ly_disc)))
add("效用全为 1（不良事件效用下降为 0）时 QALY 等于折现后的生命年（四臂）", dev < 1e-12, dev)
# 3. neutral exercise (no effect, programme costs 0): exercise arms equal the non-exercise arms
pvn <- pv; pvn[sprintf("E%02d", 1:5)] <- 0
n <- lapply(setNames(ARMS, ARMS), function(a) econ_arm(a, P, pvn, settings = list(exercise_continue = TRUE)))
cmp <- function(x, y) max(abs(x$cost - y$cost), abs(x$qaly - y$qaly), abs(x$ly - y$ly), abs(x$ly_disc - y$ly_disc),
                         abs(x$cost_components - y$cost_components))
dev <- max(cmp(n$exercise, n$chemo), cmp(n$both, n$pembro))
add("运动参数为中性（无效应、费用为 0）时，加运动的臂与对应的不加运动的臂完全一致", dev == 0, dev)
# 4. no discounting: discounted life years equal life years
o <- econ_arm("chemo", P, pv, settings = list(discount = 0))
add("折现率为 0 时折现后的生命年等于未折现的生命年", abs(o$ly_disc - o$ly) < 1e-12, abs(o$ly_disc - o$ly))
# 5. pembrolizumab drug cost alone (A03 = 1): expected discounted doses in (0, 17], none in the other arms
pa <- pv0; pa[["A03"]] <- 1
d_p <- econ_arm("pembro", P, pa)$cost; d_c <- econ_arm("chemo", P, pa)$cost
add("只把帕博利珠单抗每次药费设为 1 日元时，费用（折现后的期望给药次数）大于 0、不超过 17，单用化疗组为 0",
    d_p > 0 && d_p <= 17 && d_c == 0, d_c)
# 6. terminal care alone (D06 = 1): the cost is at most the share of deaths, and all deaths >= cancer deaths
pt <- pv0; pt[["D06"]] <- 1
tc <- econ_arm("chemo", P, pt)$cost; ta <- econ_arm("chemo", P, pt, settings = list(terminal_deaths = "all"))$cost
add("只把终末期费用设为 1 日元时，费用不超过死亡比例；对象为全部死亡时不小于只计癌症死亡时", tc > 0 && tc <= 1 && ta >= tc, ta - tc)
# 7. DR first-line and later lines at the same monthly cost: total does not depend on D04
pd <- pv0; pd[c("D03", "D05")] <- 1
a1 <- econ_arm("chemo", P, pd); pd2 <- pd; pd2[["D04"]] <- 20; a2 <- econ_arm("chemo", P, pd2)
add("远处复发一线与二线以后月额相同时，费用与一线持续期 D04 无关", abs(a1$cost - a2$cost) < 1e-9, abs(a1$cost - a2$cost))
# 8. exercise effect (test value hr0 = 0.8) raises QALYs relative to chemotherapy alone
ee <- econ_arm("exercise", P, pvn, exercise = list(hr0 = 0.8, delay_years = 0, wane_rate = 0, delta_pcr = 0))
add("加入运动效应（测试值 HR 0.8）后 QALY 大于单用化疗", ee$qaly > n$chemo$qaly, ee$qaly - n$chemo$qaly)
# 9. efficiency frontier on a synthetic table with known answer
ft <- frontier(data.frame(arm = c("A", "B", "C", "D", "E"), cost = c(0, 100, 150, 120, 300), qaly = c(0, 1, 1.2, 0.9, 2.0)))
st <- setNames(ft$status, ft$arm)
ok <- identical(unname(st[c("A", "B", "C", "D", "E")]), c("frontier", "frontier", "extendedly dominated", "dominated", "frontier"))
add("效率前沿：在答案已知的合成例中正确判定劣势与扩展劣势", ok, NA)
# 10. OS anchor switch changes only the pembrolizumab arms
aa <- econ_arm("chemo", P, pv, common_dr = TRUE); ab <- econ_arm("pembro", P, pv, common_dr = TRUE)
add("情景 k = 1 的开关不改变单用化疗组；k > 1（测试值 1.5）时设为 k = 1 增加帕博利珠单抗组的生命年",
    cmp(aa, base$chemo) == 0 && ab$ly > base$pembro$ly, cmp(aa, base$chemo))

# 11. AE disutility basis: base (sum of six, B33) and scenario (any grade >= 3, B32) give QALY losses
# in the ratio of the two rates
q6 <- econ_arm("pembro", P, pv)$qaly_ae_decrement; qa <- econ_arm("pembro", P, pv, settings = list(ae_disutility_basis = "any"))$qaly_ae_decrement
dev <- abs(q6 / qa - pv[["B33P"]] / pv[["B32P"]])
add("不良事件效用下降的口径：基准（6 种之和，B33）与情景（任何 3 级以上，B32）的 QALY 损失之比等于两者发生率之比", dev < 1e-12, dev)

R <- do.call(rbind, T)
write.csv(R, file.path(out_dir, "econ_unit_tests.csv"), row.names = FALSE)
print(R, row.names = FALSE)
stopifnot(all(R$result == "pass"))
cat("all econ unit tests passed\n")
