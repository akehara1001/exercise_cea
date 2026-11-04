# 25_four_arm.R
# Four-arm incremental analysis (chemo, chemo + exercise, chemo + pembrolizumab, all three) and the effect of exercise
# at which chemo + exercise and chemo + pembrolizumab have equal net monetary benefit, by docs/analysis_plan_phase2.md
# section 11 (committed before this script was first run). Deterministic: base parameters, base column (no external k,
# no S-JP), exercise path A base definition (or path B on the pCR axis of the break-even).
# R/22_phase2b_main.R and R/econ.R are not changed and no existing file of output/phase2/main/ is rewritten: the
# outputs begin with fourarm_ (output/phase2/main/); the report is output/phase2/fourarm_report.md (written here).
# Usage: Rscript R/25_four_arm.R          computation, checks and report
#        Rscript R/25_four_arm.R tests    runs the six unit tests R/test_*.R and R/test_four_arm.R one by one with
#                                         Rscript (fourarm_test_runs.csv) and rewrites the report
# When source()d (R/test_four_arm.R) only the definitions are made: the two parts above run when sys.nframe() == 0.

# ---- read-in: R/22_phase2b_main.R lines 19-49, unchanged
source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
source(file.path(ROOT, "R", "survmodels.R")); source(file.path(ROOT, "R", "engine.R")); source(file.path(ROOT, "R", "econ.R"))
suppressPackageStartupMessages({ library(survival); library(parallel); library(ggplot2) })
args <- commandArgs(trailingOnly = TRUE)
WHAT <- if (length(args)) args[1] else "all"
N_WORKERS <- if (length(args) > 1) as.integer(args[2]) else parallel::detectCores(logical = FALSE) - 1
OUT <- file.path(ROOT, "output", "phase2", "main"); dir.create(OUT, recursive = TRUE, showWarnings = FALSE)
wcsv <- function(x, name) write.csv(x, file.path(OUT, name), row.names = FALSE, fileEncoding = "UTF-8")

P <- readRDS(file.path(ROOT, "data", "fits", "engine_params.rds"))
EXT <- readRDS(file.path(ROOT, "data", "fits", "dr_k_external.rds"))
PL <- read.csv(file.path(ROOT, "data", "params_long.csv"), stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)
PD <- read.csv(file.path(ROOT, "data", "params_dist.csv"), stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)
B0 <- PL[PL$stat == "基本値", ]
stopifnot(identical(B0$param_id, PD$param_id), !anyNA(B0$value))
note_of <- setNames(B0$備考, B0$param_id)
u05_weeks <- as.numeric(sub(".*期間 ([0-9.]+) 週.*", "\\1", note_of[["U05"]]))
PV0 <- c(setNames(B0$value, B0$param_id), U05_duration_years = wk(u05_weeks))
LAMBDA <- c(5e6, 7.5e6)
HR_GRID <- round(seq(0.70, 1.00, by = 0.025), 3)
DP_GRID <- (0:10) / 100
E_LINES <- PV0[c("E01", "E02", "E03")]
PROVISIONAL <- B0$param_id[grepl("【要確認", B0$備考, fixed = TRUE)]

# path A definitions (analysis plan section 3 and 8); wane_start in years from randomization
path_a <- function(def, hr0) switch(def,
  base = list(hr0 = hr0, wane_start = 5, wane_rate = log(2)),
  s1   = list(hr0 = hr0, delay_years = 1, wane_rate = log(2)),
  s2   = list(hr0 = hr0, wane_rate = 0),
  cont = list(hr0 = hr0, delay_years = 0, wane_rate = log(2)))          # with exercise_continue = TRUE
path_b <- function(dp) list(hr0 = 1, delta_pcr = dp)
# ---- end of the read-in

MAIN <- sys.nframe() == 0L
HR0 <- c(0.95, 0.85, 0.72)                       # path A base definition; 0.72 = the CHALLENGE reference point
PROGRAMMES <- c("E02", "E01", "E03")             # E02 main; E01 and E03 rerun (their status as footnotes)
ARMS4 <- c("chemo", "exercise", "pembro", "both")
LABEL <- c(chemo = "化疗", exercise = "化疗 + 运动", pembro = "化疗 + 帕博利珠单抗", both = "化疗 + 帕博利珠单抗 + 运动")
FILES <- c(totals = "fourarm_totals.csv", incremental = "fourarm_incremental.csv", nmb = "fourarm_nmb_equal.csv",
           checks = "fourarm_checks.csv", run = "fourarm_run.csv", tests = "fourarm_test_runs.csv", unit = "fourarm_unit_tests.csv")
REPORT <- file.path(ROOT, "output", "phase2", "fourarm_report.md")
TOL <- 1e-6

# one arm with the programme cost given explicitly (ECON_DEFAULTS has E01); arms without exercise as in R/22
arm_run <- function(arm, hr0, programme) econ_arm(arm, P, PV0, settings = list(exercise_cost = programme),
                                                  exercise = if (has_exercise(arm)) path_a("base", hr0) else EXERCISE_NEUTRAL)

# incremental analysis with strict and extended dominance (plan 11.2); base R only.
# Returns one row per option, sorted by cost (ties: more QALYs first): comparator = the nearest cheaper option on the
# final frontier; d_cost, d_qaly against it; icer for frontier and extendedly dominated rows (blank for strictly
# dominated rows and for the cheapest frontier option); dominated_by = all strictly dominating options ("/", by cost)
# or, for extended dominance, the two options around it when it was removed.
icer_table <- function(cost, qaly, arm) {
  n <- length(cost); stopifnot(length(qaly) == n, length(arm) == n, !anyDuplicated(arm), !anyNA(cost), !anyNA(qaly))
  o <- order(cost, -qaly); cost <- cost[o]; qaly <- qaly[o]; arm <- as.character(arm[o])
  status <- rep("frontier", n); by <- rep("", n)
  for (i in seq_len(n)) {
    dom <- which(seq_len(n) != i & cost <= cost[i] & qaly >= qaly[i] & (cost < cost[i] | qaly > qaly[i]))
    if (length(dom)) { status[i] <- "dominated"; by[i] <- paste(arm[dom], collapse = "/") }
  }
  f <- which(status == "frontier")
  stopifnot(all(diff(cost[f]) > 0), all(diff(qaly[f]) > 0))   # identical options are not handled
  repeat {
    f <- which(status == "frontier")
    if (length(f) < 3) break
    ic <- diff(cost[f]) / diff(qaly[f])                         # ic[k]: option f[k + 1] against f[k]
    k <- which(ic[-length(ic)] > ic[-1])                        # the ICER of f[k + 1] above that of the next against it
    if (!length(k)) break
    j <- k[1] + 1
    status[f[j]] <- "extendedly dominated"; by[f[j]] <- paste(arm[f[j - 1]], arm[f[j + 1]], sep = "/")
  }
  f <- which(status == "frontier")
  comp <- vapply(seq_len(n), function(i) { p <- f[f < i]; if (length(p)) p[length(p)] else NA_integer_ }, integer(1))
  d_cost <- cost - cost[comp]; d_qaly <- qaly - qaly[comp]
  icer <- ifelse(is.na(comp) | status == "dominated", NA_real_, d_cost / d_qaly)
  data.frame(arm = arm, cost = cost, qaly = qaly, comparator = ifelse(is.na(comp), "", arm[comp]), d_cost = d_cost, d_qaly = d_qaly,
             icer = icer, status = status, dominated_by = by, stringsAsFactors = FALSE)
}

# half-up rounding (as the manuscript) and number formats for the report
hu <- function(x, d = 0) { y <- sign(x) * floor(round(abs(x) * 10^d, 6) + 0.5) / 10^d; y[!is.na(y) & y == 0] <- 0; y }
fmt <- function(x, d = 0) ifelse(is.na(x), "—", formatC(hu(x, d), format = "f", digits = d, big.mark = ","))
git_out <- function(...) tryCatch(system2("git", c("-C", shQuote(ROOT), ...), stdout = TRUE), error = function(e) NA_character_)

# ---------------------------------------------------------------- report (from the fourarm_ files)
write_report <- function() {
  rd <- function(k) read.csv(file.path(OUT, FILES[[k]]), stringsAsFactors = FALSE, encoding = "UTF-8")
  TOT <- rd("totals"); INC <- rd("incremental"); NE <- rd("nmb"); CK <- rd("checks"); RI <- rd("run"); ri <- setNames(RI$value, RI$item)
  TR <- if (file.exists(file.path(OUT, FILES[["tests"]]))) rd("tests") else NULL
  YS <- read.csv(file.path(OUT, "det_yardstick.csv"))
  L <- character(0); add <- function(...) L <<- c(L, ...)
  st <- function(s, by) { lb <- function(x) paste(LABEL[strsplit(x, "/", fixed = TRUE)[[1]]], collapse = "、")
    ifelse(s == "dominated", sprintf("dominated（被%s支配）", vapply(by, lb, "")),
           ifelse(s == "extendedly dominated", sprintf("extendedly dominated（介于%s之间）", vapply(by, function(x) sub("、", "与", lb(x)), "")), s)) }
  add("# 运动 CEA 第 11 节：四组增量分析与净收益分界点（内部检查用）", "",
      sprintf("生成：%s，`R/25_four_arm.R`（运行时 git HEAD %s「%s」；`R/25_four_arm.R` 的 git blob %s，脚本与结果在同一提交）。依据：`docs/analysis_plan_phase2.md` 第 11 节（尾崎 2026-11-04 邮件）。计算部分运行时间 %s 分钟。",
              ri[["generated"]], ri[["head_at_run"]], ri[["head_subject"]], ri[["script_blob"]], ri[["minutes"]]), "",
      sprintf("**本报告只供内部检查。** 入力表中备考有【要確認】的 %d 行（%s）为暂定值（计划第 7 节）。", length(PROVISIONAL), paste(PROVISIONAL, collapse = "、")), "",
      "确定性计算：基准参数、基准栏（不用「早期复发后 k（外部）」，不用 S-JP）；运动效应为路径 A 基准定义（随机化后 5 年内保持 hr0，之后半衰期 1 年），两个运动组同一 hr0。运动方案费用 E02（192,400 日元，时点 0 全员）计入两个运动组的总费用。金额单位千日元（half up）。净收益 = λ × QALY − 费用。", "")
  add("## A. 四组的增量分析（方案费用 E02）", "",
      "按总费用升序。Δ与 ICER 相对「对照」列的组（费用低于该组的最近的前沿组）；被强支配的组只给 Δ，不给 ICER。", "")
  for (h in HR0) {
    d <- INC[INC$hr0 == h & INC$programme == "E02", ]; t <- TOT[TOT$hr0 == h, ]
    dn <- t$dnmb_500_vs_chemo[match(d$arm, t$arm)]
    add(sprintf("### hr0 = %.2f", h), "",
        "| 组 | 总费用（千日元） | 总 QALY | 对照 | Δ费用（千日元） | ΔQALY | ICER（千日元/QALY） | status | 相对化疗的净收益（λ 500 万，千日元） |",
        "|---|---|---|---|---|---|---|---|---|",
        sprintf("| %s | %s | %s | %s | %s | %s | %s | %s | %s |", LABEL[d$arm], fmt(d$cost / 1e3), fmt(d$qaly, 3),
                ifelse(d$comparator == "", "—", LABEL[d$comparator]), fmt(d$d_cost / 1e3), fmt(d$d_qaly, 3), fmt(d$icer / 1e3),
                st(d$status, d$dominated_by), fmt(dn / 1e3)), "")
  }
  add("## B. 分界点", "",
      "QALY 相等：「化疗 + 运动 对 化疗」的 ΔQALY = 「化疗 + 帕博利珠单抗 对 化疗」的 ΔQALY（同一把尺子，`det_yardstick.csv`）。净收益相等：λ × ΔQALY_运动 − Δ费用_运动（不含方案费用） − E02 = λ × ΔQALY_帕博利珠单抗 − Δ费用_帕博利珠单抗，即两组都计入 E02 时净收益相等；hr0 轴 [0.30, 1.00]（路径 A 基准定义），pCR 轴为 pCR 比例的提高幅度 [0, 37] 个百分点（路径 B）；`uniroot`，tol 1e-6。", "",
      "| 分界点 | λ（万日元/QALY） | hr0 | pCR 提高（个百分点） |", "|---|---|---|---|")
  ys <- function(a) YS$root[YS$axis == a]
  add(sprintf("| QALY 相等 | — | %s | %s |", fmt(ys("hr0"), 3), fmt(100 * ys("pcr"), 1)))
  for (l in LAMBDA) {
    r <- function(a) NE$root[NE$lambda == l & NE$axis == a]
    add(sprintf("| 净收益相等（E02） | %s | %s | %s |", fmt(l / 1e4), fmt(r("hr0"), 3), fmt(100 * r("pcr"), 1)))
  }
  add("", "各分界点在区间两端的 f（= 左边 − 右边，千日元）与备注：", "",
      "| λ（万日元/QALY） | 轴 | 根 | f（下端） | f（上端） | 备注 |", "|---|---|---|---|---|---|",
      sprintf("| %s | %s | %s | %s | %s | %s |", fmt(NE$lambda / 1e4), NE$axis, ifelse(NE$axis == "hr0", fmt(NE$root, 4), fmt(100 * NE$root, 2)),
              fmt(NE$f_at_lo / 1e3), fmt(NE$f_at_hi / 1e3), ifelse(is.na(NE$note) | NE$note == "", "—", NE$note)),
      "", sprintf("QALY 相等（`det_yardstick.csv`）：hr0 %s、pCR %s（主轴为 hr0 0.70–1.00、pCR 提高 0–10 个百分点）。pCR 轴的根以个百分点表示（上表为两位小数）。",
                  if (isTRUE(YS$on_main_axis[YS$axis == "hr0"])) "在主轴之内" else "在主轴之外",
                  if (isTRUE(YS$on_main_axis[YS$axis == "pcr"])) "在主轴之内" else "在主轴之外"), "")
  add("## C. 方案费用取 E01、E03 时的 status（脚注用）", "",
      sprintf("E01 %s 日元，E02 %s 日元，E03 %s 日元（基本值）。E01、E03 的总费用由 `econ_arm()` 以 `exercise_cost = \"E01\"`、`\"E03\"` 重跑得到。", fmt(E_LINES[["E01"]]), fmt(E_LINES[["E02"]]), fmt(E_LINES[["E03"]])), "",
      sprintf("| hr0 | 方案费用 | %s |", paste(LABEL[ARMS4], collapse = " | ")), paste0("|---|---|", strrep("---|", 4)))
  for (h in HR0) for (en in c("E01", "E02", "E03")) {
    d <- INC[INC$hr0 == h & INC$programme == en, ]; d <- d[match(ARMS4, d$arm), ]
    add(sprintf("| %.2f | %s%s | %s |", h, en, if (en == "E02") "（主）" else "", paste(st(d$status, d$dominated_by), collapse = " | ")))
  }
  add("", "## 核对", "", "| 核对 | 内容 | 值 | 界限 | 结果 |", "|---|---|---|---|---|",
      sprintf("| %s | %s | %s | %s | %s |", CK$check, CK$detail, trimws(formatC(CK$value, format = "g", digits = 6)), CK$limit, ifelse(CK$pass, "通过", "**不通过**")), "")
  add("### 单元测试", "")
  if (is.null(TR)) add("尚未运行（`Rscript R/25_four_arm.R tests`）。", "") else
    add(sprintf("`Rscript R/25_four_arm.R tests`（%s；运行时 `R/25_four_arm.R` 的 git blob %s，`R/test_four_arm.R` 的 git blob %s）。每个测试以 `Rscript -e \"source('R/<测试>'); cat('<完成标记>')\"` 运行。",
                TR$run_at[1], TR$script_blob[1], TR$test_blob[1]), "",
        "判定（与计划 11.4 不同，见计划 11.4 追记）：完成标记出现（测试脚本运行到最后，`stopifnot` 等未报错）且输出中没有 \"Execution halted\"。计划写的「退出码 0」在本机不能用：本机的 R 是 x64 版在 ARM64 上仿真，Rscript 正常结束后退出码也是 127（直接运行）或 255（经 `system2`），例如 `R/test_econ.R` 打印 \"all econ unit tests passed\" 后退出码 127。退出码只作记录。", "",
        "| 测试 | 完成标记 | Execution halted | 退出码 | 结果 | 时间（分钟） |", "|---|---|---|---|---|---|",
        sprintf("| `R/%s` | %s | %s | %d | %s | %s |", TR$test, ifelse(TR$completed, "有", "无"), ifelse(TR$execution_halted, "有", "无"), TR$exit_code,
                ifelse(TR$pass, "通过", "**不通过**"), fmt(TR$minutes, 1)), "",
        sprintf("合计 %d/%d 通过。", sum(TR$pass), nrow(TR)), "")
  add("## 文件", "", "`output/phase2/main/` 中：`fourarm_totals.csv`（四组的总量与净收益）、`fourarm_incremental.csv`（增量分析，programme 列 E01–E03）、`fourarm_nmb_equal.csv`（净收益分界点）、`fourarm_checks.csv`（核对）、`fourarm_run.csv`（运行信息）、`fourarm_unit_tests.csv`（`R/test_four_arm.R` 的结果）、`fourarm_test_runs.csv`（单元测试的运行记录）。")
  con <- file(REPORT, open = "w", encoding = "UTF-8"); writeLines(L, con); close(con)
}

# ---------------------------------------------------------------- computation
if (MAIN && WHAT == "all") {
  t0 <- Sys.time()
  head_at_run <- git_out("rev-parse", "--short", "HEAD")
  if (file.exists(file.path(OUT, FILES[["tests"]]))) file.remove(file.path(OUT, FILES[["tests"]]))   # stale test record
  CK <- list(); chk <- function(check, detail, value, limit, pass) CK[[length(CK) + 1]] <<- data.frame(check = check, detail = detail, value = value, limit = limit, pass = pass)
  E02 <- PV0[["E02"]]

  # 11.1 totals of the four arms (E02; E01 and E03 by rerunning econ_arm())
  RUNS <- list()
  for (h in HR0) for (a in ARMS4) for (en in PROGRAMMES) RUNS[[paste(h, a, en)]] <- arm_run(a, h, en)
  run_of <- function(h, a, en = "E02") RUNS[[paste(h, a, en)]]
  TOT <- do.call(rbind, lapply(HR0, function(h) do.call(rbind, lapply(ARMS4, function(a) {
    r <- run_of(h, a); r1 <- run_of(h, a, "E01"); r3 <- run_of(h, a, "E03")
    stopifnot(identical(r$qaly, r1$qaly), identical(r$qaly, r3$qaly), identical(r$ly_disc, r1$ly_disc), identical(r$ly_disc, r3$ly_disc))
    data.frame(hr0 = h, arm = a, cost = r$cost, qaly = r$qaly, ly_disc = r$ly_disc, cost_E01 = r1$cost, cost_E03 = r3$cost)
  }))))
  for (l in LAMBDA) TOT[[sprintf("nmb_%g", l / 1e4)]] <- l * TOT$qaly - TOT$cost
  ich <- match(paste(TOT$hr0, "chemo"), paste(TOT$hr0, TOT$arm))
  TOT$dnmb_500_vs_chemo <- TOT$nmb_500 - TOT$nmb_500[ich]; TOT$dnmb_750_vs_chemo <- TOT$nmb_750 - TOT$nmb_750[ich]
  wcsv(TOT, FILES[["totals"]])
  ex <- has_exercise(TOT$arm)
  for (en in c("E01", "E03")) {
    dev <- max(abs((TOT[[paste0("cost_", en)]] - TOT$cost) - ifelse(ex, PV0[[en]] - E02, 0)))
    chk(sprintf("programme_%s", en), sprintf("cost_%s − cost：运动两组 = %s − E02，其余两组 = 0（12 行）", en, en), dev, "1e-06", dev <= TOL)
  }

  # 11.2 incremental analysis: three hr0 x three programme costs
  INC <- do.call(rbind, lapply(HR0, function(h) do.call(rbind, lapply(PROGRAMMES, function(en) {
    d <- TOT[TOT$hr0 == h, ]
    data.frame(hr0 = h, programme = en, icer_table(switch(en, E02 = d$cost, E01 = d$cost_E01, E03 = d$cost_E03), d$qaly, d$arm))
  }))))
  wcsv(INC, FILES[["incremental"]])

  # 11.3 net-benefit break-even: chemo + exercise (E02) against chemo + pembrolizumab; reference from det_reference.csv
  REF <- read.csv(file.path(OUT, "det_reference.csv")); rb <- REF[REF$column == "base", ]; stopifnot(nrow(rb) == 1)
  chm <- run_of(HR0[1], "chemo"); pem <- run_of(HR0[1], "pembro")
  gx <- function(exr) { xr <- econ_arm("exercise", P, PV0, settings = list(exercise_cost = "E02"), exercise = exr)
                        c(dQ = xr$qaly - chm$qaly, dC = programme_dcost(xr, chm)) }
  f_nmb <- function(l, axis) function(x) { v <- gx(if (axis == "hr0") path_a("base", x) else path_b(x))
                                           l * v[["dQ"]] - v[["dC"]] - E02 - (l * rb$dQ - rb$dC) }
  roots <- function() {
    # solve(): R/22_phase2b_main.R line 121, unchanged (hr0 axis); solve_pcr(): the same body on [0, 0.37]
    solve <- function(f) { lo <- f(0.30); hi <- f(1.00); if (sign(lo) != sign(hi)) uniroot(f, c(0.30, 1.00), tol = 1e-6)$root else NA_real_ }
    solve_pcr <- function(f) { lo <- f(0); hi <- f(0.37); if (sign(lo) != sign(hi)) uniroot(f, c(0, 0.37), tol = 1e-6)$root else NA_real_ }
    NE <- do.call(rbind, lapply(LAMBDA, function(l) do.call(rbind, lapply(c("hr0", "pcr"), function(axis) {
      f <- f_nmb(l, axis); ends <- if (axis == "hr0") c(0.30, 1.00) else c(0, 0.37)
      r <- if (axis == "hr0") solve(f) else solve_pcr(f)
      lo <- f(ends[1]); hi <- f(ends[2])
      note <- if (is.na(r)) sprintf("no root in [%s, %s]: f %s at both ends", format(ends[1]), format(ends[2]), if (lo > 0) "> 0" else "< 0") else
        if (axis == "hr0" && r < 0.70) "outside the main axis (hr0 < 0.70)" else if (axis == "pcr" && r > 0.10) "outside the main axis (pCR gain > 10 points)" else ""
      data.frame(lambda = l, axis = axis, root = r, f_at_lo = lo, f_at_hi = hi, note = note)
    }))))
    # yardstick by the same solve(): dQ(chemo + exercise vs chemo) = dQ(pembro vs chemo)
    list(NE = NE, ys = solve(function(h) gx(path_a("base", h))[["dQ"]] - rb$dQ))
  }
  RT <- roots(); NE <- RT$NE
  wcsv(NE, FILES[["nmb"]])

  # expected values written before the computation (plan 11.3)
  DC <- read.csv(file.path(OUT, "det_caps.csv"))
  dcs <- DC[DC$comparison == "secondary" & DC$column == "base" & DC$axis == "hr0", ]
  c70 <- dcs$cap_500[abs(dcs$x - 0.70) < 1e-9]; c725 <- dcs$cap_500[abs(dcs$x - 0.725) < 1e-9]; stopifnot(length(c70) == 1, length(c725) == 1)
  need <- rb$nmb_500 + E02                                   # secondary cap at which the two net benefits are equal
  h_lin <- 0.70 + 0.025 * (c70 - need) / (c70 - c725)
  r500 <- NE$root[NE$lambda == 5e6 & NE$axis == "hr0"]; r750 <- NE$root[NE$lambda == 7.5e6 & NE$axis == "hr0"]
  chk("expected_hr0_500", sprintf("λ 500 万的 hr0 根（det_caps.csv 次比较 hr0 0.700、0.725 的 cap_500 线性内插 = %.4f）", h_lin), r500, "[0.700, 0.725]",
      !is.na(r500) && r500 >= 0.700 && r500 <= 0.725)
  chk("expected_hr0_750", "λ 750 万的 hr0 根", r750, "< 0.70", !is.na(r750) && r750 < 0.70)

  # 11.4 consistency with the committed results, from the written totals
  T2 <- read.csv(file.path(OUT, FILES[["totals"]]))
  for (h in c(0.95, 0.85)) for (cmp in c("secondary", "main")) {
    a <- if (cmp == "secondary") c("exercise", "chemo") else c("both", "pembro")
    x <- T2[abs(T2$hr0 - h) < 1e-9 & T2$arm == a[1], ]; y <- T2[abs(T2$hr0 - h) < 1e-9 & T2$arm == a[2], ]
    b <- DC[DC$comparison == cmp & DC$column == "base" & DC$axis == "hr0" & abs(DC$x - h) < 1e-9, ]; stopifnot(nrow(b) == 1, nrow(x) == 1, nrow(y) == 1)
    dQ <- x$qaly - y$qaly; dC <- (x$cost - E02) - y$cost
    chk(sprintf("det_caps_%s_%.2f", cmp, h), sprintf("%s 对 %s（hr0 %.2f）的 dQ、dC（减 E02）对 det_caps.csv %s/base：最大绝对差", a[1], a[2], h, cmp),
        max(abs(dQ - b$dQ), abs(dC - b$dC)), "1e-06", max(abs(dQ - b$dQ), abs(dC - b$dC)) <= TOL)
  }
  dev_ref <- max(sapply(HR0, function(h) { x <- T2[abs(T2$hr0 - h) < 1e-9 & T2$arm == "pembro", ]; y <- T2[abs(T2$hr0 - h) < 1e-9 & T2$arm == "chemo", ]
    max(abs((x$cost - y$cost) - rb$dC), abs((x$qaly - y$qaly) - rb$dQ)) }))
  chk("det_reference", "pembro 对 chemo 的 dC、dQ（三个 hr0 的行）对 det_reference.csv base：最大绝对差", dev_ref, "1e-06", dev_ref <= TOL)
  YS <- read.csv(file.path(OUT, "det_yardstick.csv")); ys0 <- YS$root[YS$axis == "hr0"]
  chk("yardstick_hr0", sprintf("solve() 解 dQ_sec(hr0) = dQ_ref（det_yardstick.csv：%.6f，tol 1e-7）", ys0), RT$ys, "0.4248（4 位小数）",
      identical(sprintf("%.4f", RT$ys), "0.4248") && identical(sprintf("%.4f", ys0), "0.4248"))
  CK <- do.call(rbind, CK)
  wcsv(CK, FILES[["checks"]])

  minutes <- as.numeric(difftime(Sys.time(), t0, units = "mins"))
  RI <- data.frame(item = c("generated", "head_at_run", "head_subject", "script_blob", "test_blob", "minutes", "r_version", "econ_arm_runs_totals"),
                   value = c(format(Sys.time(), "%Y-%m-%d %H:%M %Z"), head_at_run, git_out("log", "-1", "--format=%s"), git_out("hash-object", "R/25_four_arm.R"),
                             git_out("hash-object", "R/test_four_arm.R"), sprintf("%.1f", minutes), R.version.string, length(RUNS)))
  wcsv(RI, FILES[["run"]])
  write_report()
  cat(sprintf("four-arm analysis: %.1f minutes; checks %d/%d passed\n", minutes, sum(CK$pass), nrow(CK)))
  print(NE)
  if (!all(CK$pass)) stop("check(s) failed: ", paste(CK$check[!CK$pass], collapse = ", "), " (see ", FILES[["checks"]], "); stop and report")
}

# ---------------------------------------------------------------- unit tests (plan 11.4)
if (MAIN && WHAT == "tests") {
  rs <- file.path(R.home("bin"), if (.Platform$OS.type == "windows") "Rscript.exe" else "Rscript")
  tests <- c(sort(setdiff(list.files(file.path(ROOT, "R"), "^test_.*\\.R$"), "test_four_arm.R")), "test_four_arm.R")
  stopifnot(length(tests) == 7)
  owd <- setwd(ROOT)                                    # renv is activated by .Rprofile in the project root
  run_at <- format(Sys.time(), "%Y-%m-%d %H:%M %Z")
  # Judgement (11.4 addendum after the first run): on this machine (x64 R emulated on ARM64) Rscript returns 127 or 255
  # after finishing normally, so the exit code carries no information. A test passes when a completion mark, printed
  # after source() of the test returns, is in the output and "Execution halted" is not; the exit code is recorded only.
  MARK <- "__FOURARM_TEST_COMPLETED__"
  TR <- do.call(rbind, lapply(tests, function(f) {
    t1 <- Sys.time()
    out <- suppressWarnings(system2(rs, c("-e", shQuote(sprintf("source('R/%s'); cat('%s', fill = TRUE)", f, MARK))), stdout = TRUE, stderr = TRUE))
    code <- attr(out, "status"); if (is.null(code)) code <- 0L
    halted <- any(grepl("Execution halted", out, fixed = TRUE)); done <- any(trimws(out) == MARK)
    if (!done || halted) { cat("----", f, "\n"); cat(tail(out, 40), sep = "\n") }
    cat(sprintf("%s: completed %s, halted %s, exit %d, %.1f minutes\n", f, done, halted, code, as.numeric(difftime(Sys.time(), t1, units = "mins"))))
    data.frame(test = f, completed = done, execution_halted = halted, exit_code = as.integer(code), pass = done && !halted,
               minutes = as.numeric(difftime(Sys.time(), t1, units = "mins")))
  }))
  setwd(owd)
  TR$run_at <- run_at; TR$script_blob <- git_out("hash-object", "R/25_four_arm.R"); TR$test_blob <- git_out("hash-object", "R/test_four_arm.R")
  wcsv(TR, FILES[["tests"]])
  write_report()
  if (!all(TR$pass)) stop("unit test(s) failed: ", paste(TR$test[!TR$pass], collapse = ", "))
  cat(sprintf("unit tests: %d/%d passed\n", sum(TR$pass), nrow(TR)))
}
if (MAIN && !WHAT %in% c("all", "tests")) stop("usage: Rscript R/25_four_arm.R [tests]")
