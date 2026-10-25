# test_econ.R
# Unit tests of the phase 2a cost and QALY layer (R/econ.R) with synthetic parameter values
# (Dr Ozaki's rows are not back yet). The survival parameters are the engine default of phase 1
# (data/fits/engine_params.rds, round 15); the k-switch test uses the test value k = 1.5. The tests
# check structure, not values.
# Output: output/phase2/econ_unit_tests.csv (test, result, the deviation or difference checked);
# no ICER is written.

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
source(file.path(ROOT, "R", "econ.R"))
suppressPackageStartupMessages(library(survival))
out_dir <- file.path(ROOT, "output", "phase2"); dir.create(out_dir, showWarnings = FALSE)
P <- readRDS(file.path(ROOT, "data", "fits", "engine_params.rds"))
Pk <- P; Pk$pembro_dr_k <- 1.5      # test value, k-switch test only

# synthetic values (not model inputs)
ids <- c(sprintf("A%02d", 1:8), sprintf("B%02d", 1:11), paste0("B", rep(21:33, each = 2), c("P", "C")),
         "C01", "C02", "C03", sprintf("D%02d", 1:6), sprintf("E%02d", 1:10), "F01", "F01P", sprintf("F%02d", 2:4), "F04P",
         sprintf("F%02d", 5:8), sprintf("U%02d", 1:5))
set.seed(1)
pv <- setNames(round(runif(length(ids), 1e4, 1e6)), ids)
pv[grepl("^B[23]", ids)] <- round(runif(sum(grepl("^B[23]", ids)), 0, 0.2), 3)            # rates
pv[c("A07")] <- 0.8; pv[["D04"]] <- 8; pv[["E05"]] <- 6
pv[c("E06", "E07", "E09", "E10")] <- c(0.18, 0.11, 0.007, 0.002)                          # rates
pv[c("F01", "F01P", "F03", "F04", "F04P", "F07", "F08")] <- c(0.5, 0.4, 0.1, 0.8, 0.7, 0.58, 0.65)   # shares, HRs
pv[c("U01", "U02", "U03", "U04")] <- c(0.72, 0.80, 0.70, 0.55); pv[["U05"]] <- 0.15
pv <- c(pv, U05_duration_years = 1 / 12)
cost_ids <- setdiff(ids, c(grep("^B[23]", ids, value = TRUE), "A07", "D04", "E05", "E06", "E07", "E09", "E10",
                           "F01", "F01P", "F03", "F04", "F04P", "F07", "F08", sprintf("U%02d", 1:5)))

T <- list()
add <- function(name, ok, dev) T[[length(T) + 1]] <<- data.frame(test = name, result = if (ok) "pass" else "FAIL", value = dev)
cmp <- function(x, y) max(abs(x$cost - y$cost), abs(x$qaly - y$qaly), abs(x$ly - y$ly), abs(x$ly_disc - y$ly_disc),
                         abs(x$cost_components - y$cost_components))

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
# 3. neutral exercise (no effect, programme costs 0) and equal musculoskeletal adverse events
# (E06 = E07, E09 = E10): exercise arms equal the non-exercise arms
pvn <- pv; pvn[sprintf("E%02d", 1:5)] <- 0; pvn[["E07"]] <- pvn[["E06"]]; pvn[["E10"]] <- pvn[["E09"]]
n <- lapply(setNames(ARMS, ARMS), function(a) econ_arm(a, P, pvn, settings = list(exercise_continue = TRUE)))
dev <- max(cmp(n$exercise, n$chemo), cmp(n$both, n$pembro))
add("E06 = E07 且 E09 = E10、运动效应中性、方案费用为 0 时，加运动的臂与对应的不加运动的臂完全一致", dev == 0, dev)
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
# 10. k switch (common_dr) changes only the pembrolizumab arms (test value k = 1.5)
bk <- lapply(c(chemo = "chemo", pembro = "pembro"), function(a) econ_arm(a, Pk, pv))
aa <- econ_arm("chemo", Pk, pv, common_dr = TRUE); ab <- econ_arm("pembro", Pk, pv, common_dr = TRUE)
add("情景 k = 1 的开关不改变单用化疗组；k > 1（测试值 1.5）时设为 k = 1 增加帕博利珠单抗组的生命年",
    cmp(aa, bk$chemo) == 0 && ab$ly > bk$pembro$ly, cmp(aa, bk$chemo))
# 11. AE disutility basis: base (sum of six, B33) and scenario (any grade >= 3, B32) give QALY losses
# in the ratio of the two rates
q6 <- econ_arm("pembro", P, pv)$qaly_ae_decrement; qa <- econ_arm("pembro", P, pv, settings = list(ae_disutility_basis = "any"))$qaly_ae_decrement
dev <- abs(q6 / qa - pv[["B33P"]] / pv[["B32P"]])
add("不良事件效用下降的口径：基准（6 种之和，B33）与情景（任何 3 级以上，B32）的 QALY 损失之比等于两者发生率之比", dev < 1e-12, dev)

# 12. (2026-10-25) musculoskeletal AE cost: with E08 = 0 the costs of every arm are those without
# the component (base minus E06/E07 x E08), and do not depend on E06 / E07
pe0 <- pv; pe0[["E08"]] <- 0
e0 <- lapply(setNames(ARMS, ARMS), function(a) econ_arm(a, P, pe0))
pe0b <- pe0; pe0b[c("E06", "E07")] <- c(0.5, 0.01); e0b <- lapply(setNames(ARMS, ARMS), function(a) econ_arm(a, P, pe0b))
dev <- max(sapply(ARMS, function(a) abs(e0[[a]]$cost - (base[[a]]$cost - base[[a]]$cost_components[["musculoskeletal_ae_E06_E08"]]))),
           sapply(ARMS, function(a) abs(e0[[a]]$cost - e0b[[a]]$cost)))
add("E08 = 0 时各臂费用不变（等于去掉 E06、E07 × E08 一项的费用，且与 E06、E07 无关）", dev < 1e-9, dev)
# 13. musculoskeletal AE utility: blank E09 / E10 (not graded) give no utility loss
pna <- pv; pna[c("E09", "E10")] <- NA
dq <- max(sapply(ARMS, function(a) abs(econ_arm(a, P, pna)$qaly - (base[[a]]$qaly + base[[a]]$qaly_msk_ae_decrement))))
add("E09、E10 为空（未分级报告）时不计效用损失", dq < 1e-12, dq)
# 14. S-JP with F03 = 0 and F01 = F01P = 0 (nobody treated): identical to no S-JP (four arms)
ps0 <- pv; ps0[c("F03", "F01", "F01P")] <- 0
s0 <- lapply(setNames(ARMS, ARMS), function(a) econ_arm(a, P, ps0, sjp = TRUE))
b0 <- lapply(setNames(ARMS, ARMS), function(a) econ_arm(a, P, ps0))
dev <- max(sapply(ARMS, function(a) cmp(s0[[a]], b0[[a]])))
add("S-JP：F03 = 0 且 F01 = 0（F01P = 0）时与不加 S-JP 完全一致（四臂）", dev == 0, dev)
# 15. S-JP with F07 = F08 = 1 (no drug effect): survival unchanged, the cost difference is only F02 and F05
ps1 <- pv; ps1[c("F07", "F08")] <- 1
s1 <- lapply(setNames(ARMS, ARMS), function(a) econ_arm(a, P, ps1, sjp = TRUE))
b1 <- lapply(setNames(ARMS, ARMS), function(a) econ_arm(a, P, ps1))
drug <- c("sjp_capecitabine_F02", "sjp_olaparib_F05")
# the mixture of three identical curves (weights summing to 1) leaves rounding of ~1e-9 yen on costs
# of ~1e7 yen: QALY and life years within 1e-12, costs within 1e-6 yen
dq <- max(sapply(ARMS, function(a) max(abs(s1[[a]]$qaly - b1[[a]]$qaly), abs(s1[[a]]$ly - b1[[a]]$ly))))
dev <- max(sapply(ARMS, function(a) max(abs((s1[[a]]$cost - b1[[a]]$cost) - sum(s1[[a]]$cost_components[drug])),
                                       abs(s1[[a]]$cost_components[setdiff(names(s1[[a]]$cost_components), drug)] -
                                           b1[[a]]$cost_components[setdiff(names(b1[[a]]$cost_components), drug)]))))
pos <- all(sapply(ARMS, function(a) all(s1[[a]]$cost_components[drug] > 0)))
add("S-JP：F07 = F08 = 1 时，与不加 S-JP 相比的差只来自 F02、F05 的费用（四臂；QALY 与生命年差 ≤ 1e-12，其余费用差 ≤ 1e-6 日元）",
    dq < 1e-12 && dev < 1e-6 && pos, dev)
# 16. BRCA testing F06: the same in every arm, with and without S-JP (difference between any two arms 0)
f6 <- c(sapply(base, function(x) x$cost_components[["brca_test_F06"]]), sapply(s1, function(x) x$cost_components[["brca_test_F06"]]))
add("F06（BRCA 检测）在任何两组之间的差为 0（含 S-JP）", diff(range(f6)) == 0 && all(f6 == pv[["F06"]]), diff(range(f6)))
# 17. S-JP is not run without F01P / F04P (arms with pembrolizumab)
pmiss <- pv; pmiss[c("F01P", "F04P")] <- NA
stops <- sapply(c("pembro", "both"), function(a) inherits(tryCatch(econ_arm(a, P, pmiss, sjp = TRUE), error = function(e) e), "error"))
runs <- !inherits(tryCatch(econ_arm("chemo", P, pmiss, sjp = TRUE), error = function(e) e), "error")
add("F01P、F04P 为空时含帕博利珠单抗的臂不运行 S-JP（报错），其余臂可运行", all(stops) && runs, NA)

R <- do.call(rbind, T)
write.csv(R, file.path(out_dir, "econ_unit_tests.csv"), row.names = FALSE)
print(R, row.names = FALSE)
stopifnot(all(R$result == "pass"))
cat("all econ unit tests passed\n")
