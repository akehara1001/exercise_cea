# 23_phase2b_report.R
# Figures and output/phase2/phase2b_report.md from the results of R/22_phase2b_main.R
# (output/phase2/main/). Plan: docs/analysis_plan_phase2.md. Internal check only: the rows marked
# 【要確認】 are provisional and the results are not for Dr Ozaki as they are.

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
suppressPackageStartupMessages(library(ggplot2))
M <- file.path(ROOT, "output", "phase2", "main")
rd <- function(f) read.csv(file.path(M, f), stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)
DC <- rd("det_caps.csv"); DR <- rd("det_reference.csv"); CR <- rd("det_e_crossings.csv"); YS <- rd("det_yardstick.csv")
SC <- rd("scenario_caps.csv"); SF <- rd("scenario_reference.csv"); OW <- rd("oneway_base.csv"); OWS <- rd("oneway_sjp.csv")
SM <- rd("psa_caps_summary.csv"); RS <- rd("psa_reference_summary.csv"); PSA <- readRDS(file.path(M, "psa_results.rds"))
PL <- read.csv(file.path(ROOT, "data", "params_long.csv"), stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)
B0 <- PL[PL$stat == "基本値", ]
E <- setNames(B0$value, B0$param_id)[c("E01", "E02", "E03")]
PROV <- B0$param_id[grepl("【要確認", B0$備考, fixed = TRUE)]

man <- function(v) formatC(v / 1e4, format = "f", digits = 1, big.mark = ",")           # yen -> 10,000 yen
yen <- function(v) formatC(v, format = "f", digits = 0, big.mark = ",")
pct <- function(v) sprintf("%.1f%%", 100 * v)
md_table <- function(df) c(paste0("| ", paste(names(df), collapse = " | "), " |"), paste0("|", paste(rep("---", ncol(df)), collapse = "|"), "|"),
                           apply(df, 1, function(r) paste0("| ", paste(ifelse(is.na(r), "", r), collapse = " | "), " |")))
lab_comp <- c(main_base = "Main: pembro + exercise vs pembro (base)", main_kext = "Main: pembro + exercise vs pembro (early-DR k external)",
              secondary_base = "Secondary: chemo + exercise vs chemo")

# ---------------------------------------------------------------- figures
fig_caps <- function(axis, xlab, file) {
  d <- DC[DC$axis == axis, ]; s <- SM[SM$axis == axis, ]
  long <- function(x, l) data.frame(series = paste(x$comparison, x$column, sep = "_"), x = x$x, lambda = l)
  det <- rbind(cbind(long(d, "lambda = 5,000,000 yen/QALY"), y = d$cap_500), cbind(long(d, "lambda = 7,500,000 yen/QALY"), y = d$cap_750))
  ps <- rbind(cbind(long(s, "lambda = 5,000,000 yen/QALY"), med = s$cap500_median, lo = s$cap500_lo, hi = s$cap500_hi),
              cbind(long(s, "lambda = 7,500,000 yen/QALY"), med = s$cap750_median, lo = s$cap750_lo, hi = s$cap750_hi))
  if (axis == "pcr") { det$x <- 100 * det$x; ps$x <- 100 * ps$x }
  det$series <- factor(lab_comp[det$series], lab_comp); ps$series <- factor(lab_comp[ps$series], lab_comp)
  g <- ggplot() +
    geom_ribbon(data = ps, aes(x, ymin = lo / 1e4, ymax = hi / 1e4), fill = "grey80") +
    geom_line(data = ps, aes(x, med / 1e4, linetype = "PSA median"), linewidth = 0.5) +
    geom_line(data = det, aes(x, y / 1e4, linetype = "Deterministic"), linewidth = 0.7) +
    geom_point(data = det, aes(x, y / 1e4), shape = 16, size = 1) +
    geom_hline(yintercept = E / 1e4, linetype = "dotted", linewidth = 0.4) +
    geom_hline(yintercept = 0, linewidth = 0.3, colour = "grey40") +
    scale_linetype_manual(values = c(Deterministic = "solid", `PSA median` = "22"), name = NULL) +
    facet_grid(series ~ lambda, labeller = labeller(series = label_wrap_gen(30))) +
    labs(x = xlab, y = "Affordable programme cost (10,000 yen)",
         caption = sprintf("Band: 95%% interval of the PSA (1,000 replicates). Dotted lines near 0: programme costs E01 %.1f, E02 %.1f, E03 %.1f (10,000 yen, base values)%s.",
                           E[1] / 1e4, E[2] / 1e4, E[3] / 1e4, if (axis == "hr0") "; crossings: fig_cap_hr0_zoom.png" else "")) +
    theme_bw(base_size = 9) + theme(legend.position = "bottom", strip.text.y = element_text(size = 7))
  if (axis == "hr0") g <- g + geom_vline(xintercept = 0.72, linetype = "longdash", linewidth = 0.3) +
    annotate("text", x = 0.725, y = Inf, label = "CHALLENGE HR 0.72\n(colon cancer, 3-year programme, DFS)", hjust = 0, vjust = 1.2, size = 2.2, lineheight = 0.9) +
    scale_x_reverse()
  ggsave(file.path(M, file), g, width = 8, height = 8, dpi = 300)
}
# hr0 near 1: where the deterministic caps cross E01-E03
fig_zoom <- function(file) {
  d <- DC[DC$axis == "hr0", ]
  det <- rbind(data.frame(series = paste(d$comparison, d$column, sep = "_"), x = d$x, lambda = "lambda = 5,000,000 yen/QALY", y = d$cap_500),
               data.frame(series = paste(d$comparison, d$column, sep = "_"), x = d$x, lambda = "lambda = 7,500,000 yen/QALY", y = d$cap_750))
  det$series <- factor(lab_comp[det$series], lab_comp)
  el <- data.frame(y = E / 1e4, lab = sprintf("%s %.1f", names(E), E / 1e4), vj = c(-0.4, 1.4, -0.4))      # E02 below its line
  g <- ggplot(det[det$x >= 0.95 - 1e-9, ], aes(x, y / 1e4, linetype = series, shape = series)) +
    geom_line(linewidth = 0.6) + geom_point(size = 1.6) +
    geom_hline(data = el, aes(yintercept = y), linetype = "dotted", linewidth = 0.4, inherit.aes = FALSE) +
    geom_text(data = el, aes(x = 0.951, y = y, label = lab, vjust = vj), hjust = 1, size = 2.5, inherit.aes = FALSE) +
    geom_hline(yintercept = 0, linewidth = 0.3, colour = "grey40") +
    scale_x_reverse() + scale_linetype_manual(values = c("solid", "longdash", "dotdash"), name = NULL) +
    scale_shape_manual(values = c(16, 1, 17), name = NULL) + facet_wrap(~lambda) +
    labs(x = "hr0 (path A, base definition)", y = "Affordable programme cost (10,000 yen)",
         caption = "Deterministic values at the grid points 0.950-1.000; crossings solved continuously in det_e_crossings.csv.") +
    theme_bw(base_size = 9) + theme(legend.position = "bottom", legend.direction = "vertical")
  ggsave(file.path(M, file), g, width = 8, height = 4.8, dpi = 300)
}
fig_zoom("fig_cap_hr0_zoom.png")
fig_caps("hr0", "Recurrence hazard ratio of exercise, hr0 (path A, base definition: held to 5 years, then half-life 1 year)", "fig_cap_hr0.png")
fig_caps("pcr", "Increase in the pCR proportion (percentage points, path B)", "fig_cap_pcr.png")

rule_tag <- function(r, pv) paste0(ifelse(r == "±25%", " [assumed range: +-25%]", ifelse(r == "片側対称", " [assumed range: mirrored]",
                                   ifelse(r == "薬価固定", " [list price: down to 75%]", ifelse(r == "0例：PSAは固定", " [0 events]", "")))),
                                   ifelse(pv, " [provisional]", ""))
tornado <- function(d, lo, hi, base, xlab, file, top = 20) {
  d$w <- abs(d[[hi]] - d[[lo]]); d <- d[d$w > 1e-6 * max(1, abs(base)), ]; d <- d[order(-d$w), ][seq_len(min(top, nrow(d))), ]
  d$lab <- factor(paste0(d$param_id, rule_tag(d$range_rule, d$provisional)), rev(paste0(d$param_id, rule_tag(d$range_rule, d$provisional))))
  g <- ggplot(d) +
    geom_segment(aes(y = lab, yend = lab, x = .data[[lo]] / 1e4, xend = base / 1e4), linewidth = 3, colour = "grey30") +
    geom_segment(aes(y = lab, yend = lab, x = .data[[hi]] / 1e4, xend = base / 1e4), linewidth = 3, colour = "grey75") +
    geom_vline(xintercept = base / 1e4, linewidth = 0.4) +
    labs(x = xlab, y = NULL, caption = "Dark: parameter at its lower bound; light: at its upper bound.") + theme_bw(base_size = 8)
  ggsave(file.path(M, file), g, width = 7, height = 0.25 * nrow(d) + 1.2, dpi = 300)
  d
}
TM <- tornado(OW, "cap_low", "cap_high", OW$cap_base[1], "Affordable programme cost, main comparison, hr0 = 0.85, lambda = 5,000,000 (10,000 yen)", "fig_oneway_main_cap.png")
TR <- tornado(OW, "icer_low", "icer_high", OW$icer_base[1], "ICER, pembro vs chemo (10,000 yen/QALY)", "fig_oneway_reference_icer.png")

# ---------------------------------------------------------------- report
L <- character(0); add <- function(...) L <<- c(L, ...)
cell <- function(det, med, lo, hi) sprintf("%s（%s [%s, %s]）", man(det), man(med), man(lo), man(hi))
add("# 第 2 阶段 2b 报告：主分析（内部检查用）", "",
    sprintf("生成：%s，`R/23_phase2b_report.R`；计算：`R/22_phase2b_main.R`（运行时 git HEAD 为 %s，即分析计划的提交；`econ.R` 按计划第 8 节的修改与两个脚本在运行后与结果一并提交。PSA %d 个样本，%d 个进程，%.1f 分钟）。分析计划：`docs/analysis_plan_phase2.md`（计算前提交）。结果文件：`output/phase2/main/`。",
            format(Sys.time(), "%Y-%m-%d %H:%M"), PSA$commit, length(unique(PSA$ex$rep)), PSA$workers, PSA$minutes), "",
    sprintf("**本报告只供内部检查。** 入力表 v9 中备考有【要確認】的 %d 行（%s）为暂定值，结果不直接交给尾崎（分析计划第 7 节）。依赖暂定值的程度见第 6 节。", length(PROV), paste(PROV, collapse = "、")), "",
    "金额单位：万日元（表中「确定性值（PSA 中位数 [2.5%, 97.5%]）」）。上限 = λ × ΔQALY − Δ费用（不含运动方案费用；含运动有害事象的费用与效用）。", "")
# 1. caps
tab_caps <- function(comp, col, axis, xs, lam) {
  d <- DC[DC$comparison == comp & DC$column == col & DC$axis == axis, ]; s <- SM[SM$comparison == comp & SM$column == col & SM$axis == axis, ]
  k <- if (lam == 500) "cap500" else "cap750"
  do.call(rbind, lapply(xs, function(x) {
    i <- which(abs(d$x - x) < 1e-9); j <- which(abs(s$x - x) < 1e-9)
    data.frame(x = if (axis == "hr0") sprintf("%.2f", x) else sprintf("%d", round(100 * x)),
               cap = cell(d[[paste0("cap_", lam)]][i], s[[paste0(k, "_median")]][j], s[[paste0(k, "_lo")]][j], s[[paste0(k, "_hi")]][j]),
               p = pct(s[[paste0("p_", k, "_ge_E02")]][j]), check.names = FALSE)
  }))
}
HRS <- c(0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00)
add("## 1. 主比较与次比较：可负担的方案费用上限", "",
    sprintf("运动方案费用：E01 %s、E02 %s、E03 %s 万日元（基本值；「上限 ≥ E02 的概率」用 E02 的基本值）。图：`fig_cap_hr0.png`（hr0 轴）、`fig_cap_pcr.png`（pCR 轴）。", man(E[1]), man(E[2]), man(E[3])), "")
for (lam in c(500, 750)) {
  add(sprintf("### 1.%d 路径 A（hr0，基准定义），λ = %d 万日元/QALY", if (lam == 500) 1 else 2, lam), "")
  t1 <- tab_caps("main", "base", "hr0", HRS, lam); t2 <- tab_caps("main", "kext", "hr0", HRS, lam); t3 <- tab_caps("secondary", "base", "hr0", HRS, lam)
  add(md_table(data.frame(hr0 = t1$x, `主比较（基准）上限` = t1$cap, `P(≥E02)` = t1$p, `主比较（早期复发后 k 外部）上限` = t2$cap, `P(≥E02) ` = t2$p,
                          `次比较 上限` = t3$cap, `P(≥E02)  ` = t3$p, check.names = FALSE)), "")
}
for (lam in c(500, 750)) {
  add(sprintf("### 1.%d 路径 B（pCR 提高幅度，个百分点），λ = %d 万日元/QALY", if (lam == 500) 3 else 4, lam), "")
  t1 <- tab_caps("main", "base", "pcr", (0:10) / 100, lam); t2 <- tab_caps("main", "kext", "pcr", (0:10) / 100, lam); t3 <- tab_caps("secondary", "base", "pcr", (0:10) / 100, lam)
  add(md_table(data.frame(`pCR 提高` = t1$x, `主比较（基准）上限` = t1$cap, `P(≥E02)` = t1$p, `主比较（早期复发后 k 外部）上限` = t2$cap, `P(≥E02) ` = t2$p,
                          `次比较 上限` = t3$cap, `P(≥E02)  ` = t3$p, check.names = FALSE)), "")
}
CR$lab <- ifelse(is.na(CR$hr0), "[0.30, 1.00] 内无交点", ifelse(CR$hr0 < 0.70, sprintf("%.3f（在主轴范围 0.70 至 1.00 之外）", CR$hr0), sprintf("%.3f", CR$hr0)))
add("### 1.5 E01 至 E03 对应的 hr0 交点（确定性，上限 = 方案费用的 hr0；hr0 小于该值时上限高于方案费用）", "",
    md_table(data.frame(比较 = ifelse(CR$comparison == "main", ifelse(CR$column == "base", "主比较（基准）", "主比较（早期复发后 k 外部）"), "次比较"),
                        `λ（万日元/QALY）` = CR$lambda / 1e4, 方案 = CR$programme, `费用（万日元）` = man(CR$cost), hr0 = CR$lab, check.names = FALSE)), "")
# 1.6 decomposition of the cap and 1.7 cost-saving crossings (2026-10-25 addition; existing results only,
# the model is not rerun)
avoided <- function(d) -d$dC                                     # avoided medical costs, programme cost excluded
dec_tab <- function(comp, lam) {
  d <- DC[DC$comparison == comp & DC$column == "base" & DC$axis == "hr0", ]; d <- d[order(d$x), ]
  cap <- d[[paste0("cap_", lam)]]
  data.frame(hr0 = sprintf("%.3f", d$x), ΔQALY = sprintf("%.4f", d$dQ), `λ × ΔQALY` = man(lam * 1e4 * d$dQ),
             `避免的医疗费用（−Δ费用）` = man(avoided(d)), 上限 = man(cap),
             `避免的医疗费用占上限` = ifelse(cap > 0, pct(avoided(d) / cap), "－"), check.names = FALSE)
}
add("### 1.6 上限的分解（确定性，路径 A 基准定义，基准栏）", "",
    "上限 = λ × ΔQALY + 避免的医疗费用，避免的医疗费用 = −Δ费用（不含运动方案费用；含运动有害事象的费用）。金额单位：万日元。hr0 = 1.00 时上限为负（只有运动有害事象），比例不计。", "")
for (lam in c(500, 750)) for (comp in c("main", "secondary")) {
  add(sprintf("#### %s，λ = %d 万日元/QALY", if (comp == "main") "主比较（化疗加帕博利珠单抗再加运动对化疗加帕博利珠单抗）" else "次比较（化疗加运动对单用化疗）", lam), "",
      md_table(dec_tab(comp, lam)), "")
}
sv <- do.call(rbind, lapply(list(c("main", "base"), c("main", "kext"), c("secondary", "base")), function(cc) {
  d <- DC[DC$comparison == cc[1] & DC$column == cc[2] & DC$axis == "hr0", ]; d <- d[order(d$x), ]
  data.frame(comparison = cc[1], column = cc[2], programme = names(E), cost = unname(E),
             hr0 = sapply(E, function(e) approx(avoided(d), d$x, xout = e)$y))
}))
write.csv(sv, file.path(M, "det_cost_saving_crossings.csv"), row.names = FALSE, fileEncoding = "UTF-8")
EXp <- PSA$ex[PSA$ex$axis == "hr0", ]
ps_sv <- function(comp, col) { d <- EXp[EXp$comparison == comp & EXp$column == col, ]
  tapply(-d$dC >= E[["E02"]], d$x, mean) }
p1 <- ps_sv("main", "base"); p2 <- ps_sv("main", "kext"); p3 <- ps_sv("secondary", "base")
add("### 1.7 \"费用节约\"的交点", "",
    "避免的医疗费用等于方案费用（E01、E02、E03 的基本值）时的 hr0（确定性，路径 A 基准定义；在 hr0 格点〔间隔 0.025〕之间线性插值，不重新运行模型）。hr0 小于该值时，加运动的组总费用（含方案费用）更低且 QALY 更多（hr0 < 1 时 ΔQALY > 0）。",
    "主比较（基准栏）与次比较的值与用户由 `det_caps.csv` 独立算得的值（主比较 0.948、0.958、0.997；次比较 0.958、0.966、0.998）一致（2026-10-25 核对）。数值另存 `det_cost_saving_crossings.csv`。", "",
    md_table(data.frame(方案 = names(E), `费用（万日元）` = man(E),
                        `主比较（基准）` = sprintf("%.3f", sv$hr0[sv$comparison == "main" & sv$column == "base"]),
                        `主比较（早期复发后 k 外部）` = sprintf("%.3f", sv$hr0[sv$comparison == "main" & sv$column == "kext"]),
                        次比较 = sprintf("%.3f", sv$hr0[sv$comparison == "secondary"]), check.names = FALSE)), "",
    sprintf("PSA：每个 hr0 下避免的医疗费用 ≥ E02（基本值 %s 万日元）的样本比例（1,000 个样本；不依赖 λ）。", man(E[["E02"]])), "",
    md_table(data.frame(hr0 = sprintf("%.3f", as.numeric(names(p1))), `主比较（基准）` = pct(p1), `主比较（早期复发后 k 外部）` = pct(p2[names(p1)]),
                        次比较 = pct(p3[names(p1)]), check.names = FALSE)), "")

# 2. reference
add("## 2. 参照比较：化疗加帕博利珠单抗对单用化疗", "")
rr <- function(col) { d <- DR[DR$column == col, ]; s <- RS[RS$column == col, ]
  data.frame(栏 = if (col == "base") "基准" else "早期复发后 k（外部）", `Δ费用（万日元）` = cell(d$dC, s$dC_median, s$dC_lo, s$dC_hi),
             ΔQALY = sprintf("%.3f（%.3f [%.3f, %.3f]）", d$dQ, s$dQ_median, s$dQ_lo, s$dQ_hi),
             `ICER（万日元/QALY）` = cell(d$icer, s$icer_median, s$icer_lo, s$icer_hi),
             `P(划算), 500 万` = pct(s$p_ce_500), `P(划算), 750 万` = pct(s$p_ce_750), check.names = FALSE) }
add(md_table(rbind(rr("base"), rr("kext"))), "",
    sprintf("确定性值（PSA 中位数 [2.5%%, 97.5%%]）。划算 = λ × ΔQALY − Δ费用 > 0（按净货币效益判断）。ΔQALY ≤ 0 的样本：基准 %d、k 外部 %d；ICER 的百分位含这些样本以及 Δ费用 < 0 的样本（ICER 为负），只作参考。阈值线 750 万日元。", RS$n_dQ_le_0[RS$column == "base"], RS$n_dQ_le_0[RS$column == "kext"]), "")
# 3. yardstick
ys <- function(a) { r <- YS[YS$axis == a, ]
  if (is.na(r$root)) sprintf("在 %s 内无解（区间两端的 ΔQALY：%.4f 与 %.4f）", r$search, r$dQ_at_lower_end, r$dQ_at_upper_end)
  else if (a == "hr0") sprintf("hr0 = %.3f%s", r$root, if (r$on_main_axis) "" else "（在主轴范围 0.70 至 1.00 之外）")
  else sprintf("提高 %.1f 个百分点%s", 100 * r$root, if (r$on_main_axis) "" else "（超过主轴范围 10 个百分点）") }
add("## 3. \"同一把尺子\"", "",
    sprintf("帕博利珠单抗对单用化疗的 ΔQALY（确定性，基准）= %.4f。使化疗加运动对单用化疗的 ΔQALY 与之相等所需的", YS$target_dQ[1]), "",
    sprintf("- 路径 A（基准定义）：%s", ys("hr0")), sprintf("- 路径 B：%s", ys("pcr")), "")
# 4. one-way
ow_tab <- function(d, lo, hi, base, f) { d$w <- abs(d[[hi]] - d[[lo]]); d <- d[d$w > 1e-6 * max(1, abs(base)), ]; d <- d[order(-d$w), ]
  data.frame(param_id = d$param_id, 项目 = d$item, 范围 = sprintf("%s 至 %s", signif(d$low_value, 4), signif(d$high_value, 4)),
             下限时 = f(d[[lo]]), 上限时 = f(d[[hi]]), 幅 = f(d$w),
             备注 = trimws(paste(ifelse(d$range_rule == "", "", paste0("range_rule：", d$range_rule)), ifelse(d$provisional, "暂定值【要確認】", ""))), check.names = FALSE) }
add("## 4. 单因素敏感性分析", "",
    sprintf("### 4.1 主比较的上限（hr0 = 0.85，基准定义，λ = 500 万日元/QALY；基准值 %s 万日元；`fig_oneway_main_cap.png`，前 20 项）", man(OW$cap_base[1])), "",
    md_table(head(ow_tab(OW, "cap_low", "cap_high", OW$cap_base[1], man), 25)), "",
    sprintf("（共 %d 行改变结果；表中列出前 25 行，全部见 `oneway_base.csv`。range_rule 不为空的行，其范围按 model_spec 第 6 节的规则设定。）", nrow(ow_tab(OW, "cap_low", "cap_high", OW$cap_base[1], man))), "",
    sprintf("### 4.2 参照比较的 ICER（基准值 %s 万日元/QALY；`fig_oneway_reference_icer.png`）", man(OW$icer_base[1])), "",
    md_table(head(ow_tab(OW, "icer_low", "icer_high", OW$icer_base[1], man), 25)), "",
    sprintf("### 4.3 S-JP 情景下 S-JP 参数的单因素分析（F01P 为主要项目；S-JP 下的基准值：主比较上限 %s 万日元，参照 ICER %s 万日元/QALY）", man(OWS$cap_base[1]), man(OWS$icer_base[1])), "",
    md_table(rbind(transform(ow_tab(OWS, "cap_low", "cap_high", OWS$cap_base[1], man), 结果 = "主比较上限"),
                   transform(ow_tab(OWS, "icer_low", "icer_high", OWS$icer_base[1], man), 结果 = "参照 ICER"))), "")
# 5. scenarios
sc_lab <- c(base = "基准", sjp = "S-JP", kext = "早期复发后 k（外部）", elmore = "术前进展后生存（Elmore；边界情景，与试验第 1 至 3 年的 OS 不一致）",
            utility_us = "效用：美国价值集", utility_uk = "效用：英国价值集", utility_au = "效用：澳大利亚价值集",
            path_a_s1 = "路径 A 情景①（维持到手术后 1 年，之后半衰期 1 年）", path_a_s2 = "路径 A 情景②（不衰减）",
            continue_s1 = "术后继续（情景①下，维持到继续期间 E05 结束，之后半衰期 1 年；费用加 E04 × E05）")
scap <- function(n, comp, axis, x) { d <- SC[SC$scenario == n & SC$comparison == comp & SC$column == "base" & SC$axis == axis & abs(SC$x - x) < 1e-9, ]
  if (nrow(d)) man(d$cap_500) else "－" }
add("## 5. 情景（确定性，λ = 500 万日元/QALY）", "",
    md_table(data.frame(情景 = sc_lab[names(sc_lab)],
                        `主比较 hr0 0.85` = sapply(names(sc_lab), scap, comp = "main", axis = "hr0", x = 0.85),
                        `主比较 hr0 0.70` = sapply(names(sc_lab), scap, comp = "main", axis = "hr0", x = 0.70),
                        `主比较 pCR +5` = sapply(names(sc_lab), scap, comp = "main", axis = "pcr", x = 0.05),
                        `次比较 hr0 0.85` = sapply(names(sc_lab), scap, comp = "secondary", axis = "hr0", x = 0.85),
                        `次比较 pCR +5` = sapply(names(sc_lab), scap, comp = "secondary", axis = "pcr", x = 0.05),
                        `参照 ICER（万日元/QALY）` = sapply(names(sc_lab), function(n) { d <- SF[SF$scenario == n & SF$column == "base", ]; man(d$icer) }),
                        check.names = FALSE, row.names = NULL)), "",
    "上限的单位为万日元。路径 A 的情景①②与术后继续只改变运动臂，参照 ICER 与基准相同；它们没有 pCR 轴（－）。全部格点见 `scenario_caps.csv`、`scenario_reference.csv`；效用的价值集见 `scenario_utility_sets.csv`。", "")
# 6. provisional values
pv_rows <- function(d, lo, hi, base) { d <- d[d$provisional, ]; d$w <- abs(d[[hi]] - d[[lo]]); d[order(-d$w), ] }
pm <- pv_rows(OW, "cap_low", "cap_high", OW$cap_base[1]); pr <- pv_rows(OW, "icer_low", "icer_high", OW$icer_base[1])
add("## 6. 依赖暂定值（【要確認】）的程度", "",
    sprintf("【要確認】的 %d 行：%s。在单因素敏感性分析中（各行在其范围内变动），它们对主比较上限（hr0 = 0.85，λ = 500 万）与参照 ICER 的影响：", length(PROV), paste(PROV, collapse = "、")), "",
    md_table(data.frame(param_id = pm$param_id, 项目 = pm$item, `主比较上限的幅（万日元）` = man(pm$w),
                        `参照 ICER 的幅（万日元/QALY）` = man(abs(pr$icer_high - pr$icer_low)[match(pm$param_id, pr$param_id)]), check.names = FALSE)), "",
    "F01P 只在 S-JP 情景中起作用（第 4.3 节）；E03 只是一条水平线（方案费用），不进入上限的计算。其余结果都含这些暂定值（基本值），PSA 中按其范围抽样。", "")
writeLines(L, file.path(ROOT, "output", "phase2", "phase2b_report.md"), useBytes = TRUE)
cat("wrote phase2b_report.md:", length(L), "lines\n")
