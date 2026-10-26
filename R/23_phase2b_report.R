# 23_phase2b_report.R
# Figures and output/phase2/phase2b_report.md from the results of R/22_phase2b_main.R
# (output/phase2/main/; section 7 from its plan9 part, 2026-10-26). Plan: docs/analysis_plan_phase2.md. Internal check only: the rows marked
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
# 7. section 9 of the plan (2026-10-26): scenarios of the costs after metastatic recurrence, decomposition
# of the incremental costs, net benefit for one year's patients (R/22_phase2b_main.R plan9)
SCN <- c(sc_metcost50 = "情景①（转移复发治疗费 50%）", sc_eribulin = "情景②（D05 = 艾立布林中心）")
SCX <- as.data.frame(readxl::read_excel(file.path(ROOT, "input", "params", "parameters_v10.xlsx"), sheet = "シナリオ"), stringsAsFactors = FALSE)
KX <- as.data.frame(readxl::read_excel(file.path(ROOT, "input", "params", "parameters_v10.xlsx"), sheet = "計算根拠_原", skip = 3, col_types = "text"), stringsAsFactors = FALSE)
S9 <- lapply(names(SCN), function(s) list(DC = rd(paste0(s, "_det_caps.csv")), DR = rd(paste0(s, "_det_reference.csv")), CR = rd(paste0(s, "_crossings.csv")),
                                          SM = rd(paste0(s, "_psa_caps_summary.csv")), RS = rd(paste0(s, "_psa_reference_summary.csv")),
                                          PSA = readRDS(file.path(M, paste0(s, "_psa_results.rds")))))
names(S9) <- names(SCN)
CRB <- rd("sc_base_crossings.csv"); SV <- rd("det_cost_saving_crossings.csv")
add("## 7. 补充：转移复发治疗费的情景、增量费用的分解、一年对象患者的净收益（分析计划第 9 节）", "",
    sprintf("2026-10-26 补充，依据尾崎 2026-10-26 邮件。分析计划第 9 节在计算前单独提交（5e1c0dd）。计算：`R/22_phase2b_main.R plan9`（PSA 运行时 git HEAD 为 %s；两个情景 × %d 个样本，%d 个进程，%.1f 分钟）。第 1 至 6 节的基准结果不变；用同一程序按基本值重算的上限与 E 交点与 `det_caps.csv`、`det_e_crossings.csv` 一致（脚本内核对）。结果文件以 `sc_metcost50_`、`sc_eribulin_`、`sc_base_`、`decomp_`、`cohort_value` 开头。",
            S9[[1]]$PSA$commit, length(unique(S9[[1]]$PSA$ex$rep)), S9[[1]]$PSA$workers, S9[[1]]$PSA$minutes), "")
# 7.1 scenarios
add("### 7.1 转移复发治疗费的情景", "",
    md_table(data.frame(情景 = SCN[SCX[["シナリオ"]]], param_id = SCX$param_id, `基本值（万日元/月）` = man(SCX[["基本値"]]),
                        `情景值（万日元/月）` = man(SCX[["シナリオ値"]]), 倍率 = sprintf("%.4f", SCX[["倍率（シナリオ値 ÷ 基本値）"]]), check.names = FALSE, row.names = NULL)), "",
    "值取自入力表 v10（`input/params/parameters_v10.xlsx`，工作表「シナリオ」；パラメータ工作表的「シナリオ値」列；基本值与范围不变）。PSA 用基准 PSA 的同一 1,000 个 bootstrap 样本与同一组参数抽样，被替换的参数在每个样本中乘以上表的倍率（相对不确定性同基准）。只做路径 A（基准定义）。", "")
add("#### 7.1.1 情景②的 D05：艾立布林方案的月额（入力表 v10「計算根拠_原」）", "",
    md_table(data.frame(项目 = KX[["項目"]], 值 = ifelse(is.na(suppressWarnings(as.numeric(KX[["値"]]))), KX[["値"]],
                                                       trimws(formatC(suppressWarnings(as.numeric(KX[["値"]])), format = "fg", digits = 10, big.mark = ","))),
                        单位 = KX[["単位"]], 式 = KX[["式"]], 出处 = KX[["出典・根拠"]], check.names = FALSE, row.names = NULL)), "")
k <- 2
for (s in names(SCN)) for (lam in c(500, 750)) {
  DC <- S9[[s]]$DC; SM <- S9[[s]]$SM
  t1 <- tab_caps("main", "base", "hr0", HRS, lam); t2 <- tab_caps("main", "kext", "hr0", HRS, lam); t3 <- tab_caps("secondary", "base", "hr0", HRS, lam)
  add(sprintf("#### 7.1.%d %s：上限（路径 A 基准定义），λ = %d 万日元/QALY", k, SCN[[s]], lam), "",
      md_table(data.frame(hr0 = t1$x, `主比较（基准）上限` = t1$cap, `P(≥E02)` = t1$p, `主比较（早期复发后 k 外部）上限` = t2$cap, `P(≥E02) ` = t2$p,
                          `次比较 上限` = t3$cap, `P(≥E02)  ` = t3$p, check.names = FALSE)), "")
  k <- k + 1
}
DC <- rd("det_caps.csv"); SM <- rd("psa_caps_summary.csv")       # tab_caps() reads DC and SM: back to the base results
add("全部格点（间隔 0.025）见 `sc_*_det_caps.csv`、`sc_*_psa_caps_summary.csv`。确定性值（PSA 中位数 [2.5%, 97.5%]），万日元；基准见第 1.1、1.2 节。", "")
cmp_lab <- function(d) ifelse(d$comparison == "main", ifelse(d$column == "base", "主比较（基准）", "主比较（早期复发后 k 外部）"), "次比较")
hr_lab <- function(v) ifelse(is.na(v), "无交点", ifelse(v < 0.70, sprintf("%.3f（主轴外）", v), sprintf("%.3f", v)))
pick <- function(d, ty, lam = NA) { d <- d[d$type == ty & (if (is.na(lam)) is.na(d$lambda) else d$lambda == lam), ]; d[order(match(d$comparison, c("main", "secondary")), match(d$column, c("base", "kext")), d$programme), ] }
b <- pick(CRB, "avoided_eq_programme"); s1 <- pick(S9$sc_metcost50$CR, "avoided_eq_programme"); s2 <- pick(S9$sc_eribulin$CR, "avoided_eq_programme")
stopifnot(identical(paste(b$comparison, b$column, b$programme), paste(s1$comparison, s1$column, s1$programme)),
          identical(paste(b$comparison, b$column, b$programme), paste(s2$comparison, s2$column, s2$programme)))
iv <- SV$hr0[match(paste(b$comparison, b$column, b$programme), paste(SV$comparison, SV$column, SV$programme))]
add(sprintf("#### 7.1.%d \"避免的医疗费用 = 方案费用\"的 hr0（确定性，uniroot 连续求解，不依赖 λ）", k), "",
    md_table(data.frame(比较 = cmp_lab(b), 方案 = b$programme, `费用（万日元）` = man(b$cost), 基准 = hr_lab(b$hr0),
                        `基准（第 1.7 节，格点插值）` = sprintf("%.3f", iv), `情景①` = hr_lab(s1$hr0), `情景②` = hr_lab(s2$hr0), check.names = FALSE)), "",
    sprintf("hr0 小于该值时，加运动的组总费用（含方案费用）更低。基准的连续解与第 1.7 节的格点插值之差最大 %.5f。", max(abs(b$hr0 - iv))), "")
k <- k + 1
xs <- do.call(rbind, lapply(c(5e6, 7.5e6), function(l) { b <- pick(CRB, "cap_eq_programme", l); s1 <- pick(S9$sc_metcost50$CR, "cap_eq_programme", l)
  s2 <- pick(S9$sc_eribulin$CR, "cap_eq_programme", l)
  data.frame(比较 = cmp_lab(b), `λ（万日元/QALY）` = l / 1e4, 方案 = b$programme, `费用（万日元）` = man(b$cost), 基准 = hr_lab(b$hr0),
             `情景①` = hr_lab(s1$hr0), `情景②` = hr_lab(s2$hr0), check.names = FALSE) }))
add(sprintf("#### 7.1.%d 上限 = 方案费用的 hr0（确定性，同第 1.5 节）", k), "", md_table(xs), "")
k <- k + 1
rr9 <- function(lab, DRx, RSx) do.call(rbind, lapply(c("base", "kext"), function(col) { d <- DRx[DRx$column == col, ]; s <- RSx[RSx$column == col, ]
  data.frame(情景 = lab, 栏 = if (col == "base") "基准" else "早期复发后 k（外部）", `Δ费用（万日元）` = cell(d$dC, s$dC_median, s$dC_lo, s$dC_hi),
             ΔQALY = sprintf("%.3f（%.3f [%.3f, %.3f]）", d$dQ, s$dQ_median, s$dQ_lo, s$dQ_hi), `ICER（万日元/QALY）` = cell(d$icer, s$icer_median, s$icer_lo, s$icer_hi),
             `P(划算), 500 万` = pct(s$p_ce_500), `P(划算), 750 万` = pct(s$p_ce_750), check.names = FALSE) }))
add(sprintf("#### 7.1.%d 参照比较（化疗加帕博利珠单抗对单用化疗）", k), "",
    md_table(rbind(rr9("基准（第 2 节）", DR, RS), rr9(SCN[["sc_metcost50"]], S9$sc_metcost50$DR, S9$sc_metcost50$RS),
                   rr9(SCN[["sc_eribulin"]], S9$sc_eribulin$DR, S9$sc_eribulin$RS))), "",
    "确定性值（PSA 中位数 [2.5%, 97.5%]）。转移复发的治疗费下降时，帕博利珠单抗因减少复发而避免的费用变小，Δ费用与 ICER 上升。", "")

# 7.2 decomposition
DLAB <- c(exercise_programme = "运动方案费用（E02）", exercise_ae = "运动有害事象（E06 / E07 × E08）", pembrolizumab_drug = "帕博利珠单抗药剂费（A03）",
          administration = "给药费用（A04）", immune_ae = "免疫相关不良事件（B21 至 B30 × B01 至 B10）", chemo_ae = "化疗不良事件（发热性中性粒细胞减少，B31 × B11）",
          follow_up = "随访（C01 至 C03）", lrr = "局部区域复发的治疗（D01、D02）", dr_first_line = "远处复发：一次治疗（D03 / D03P）",
          dr_later_lines = "远处复发：二次治疗以后（D05）", terminal_care = "终末期医疗（D06）", other = "其他", total = "合计（= Δ费用）",
          total_without_programme = "合计（不含方案费用）= −避免的医疗费用", total_with_E01 = "参考：方案费用取 E01 时的合计", total_with_E03 = "参考：方案费用取 E03 时的合计")
DR9 <- rd("decomp_reference.csv"); DM9 <- rd("decomp_main_hr085.csv"); DRC <- rd("decomp_reference_components.csv"); DMC <- rd("decomp_main_hr085_components.csv")
dtab <- function(d, share = TRUE) { tot <- d$d_base[d$category == "total"]
  data.frame(类别 = DLAB[d$category], `Δ费用，基准（万日元）` = man(d$d_base), `占合计（基准）` = if (share) ifelse(d$category %in% names(DLAB)[1:12], pct(d$d_base / tot), "") else "－",
             `Δ费用，早期复发后 k 外部（万日元）` = man(d$d_kext), check.names = FALSE, row.names = NULL) }
oth <- function(C) { o <- C[C$column == "base" & C$category == "other" & abs(C$d) > 0.5, ]
  if (!nrow(o)) "无（全部为 0）" else paste(sprintf("%s %s", o$component, man(o$d)), collapse = "、") }
add("### 7.2 增量费用的分解（确定性，折现后，基准参数）", "",
    "#### 7.2.1 参照比较：化疗加帕博利珠单抗对单用化疗", "", md_table(dtab(DR9)), "",
    sprintf("「其他」的内訳（基准栏，万日元，|Δ| ≥ 0.5 日元的成分）：%s。免疫相关不良事件为帕博利珠单抗组的发生率减去单用化疗组（安慰剂组）的发生率后乘以每件费用。逐成分的值见 `decomp_reference_components.csv`。",
            oth(DRC)), "",
    "#### 7.2.2 主比较：两者都加对化疗加帕博利珠单抗，hr0 = 0.85（路径 A 基准定义）", "", md_table(dtab(DM9, share = FALSE)), "",
    sprintf("「其他」的内訳（基准栏）：%s。两组都用帕博利珠单抗，不良事件的费用相同（0）；帕博利珠单抗药剂费与给药费用的差来自术后给药时点无事件者的比例（运动减少复发）。「合计（不含方案费用）」与第 1.6 节 hr0 = 0.85 的避免的医疗费用一致（脚本内核对）。",
            oth(DMC)), "")

# 7.3 net benefit for one year's patients
NS <- read.csv(file.path(ROOT, "input", "params", "cohort_N_sources.csv"), stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)
NV <- rd("cohort_value_N.csv"); CV <- rd("cohort_value.csv"); Nn <- NV$value[NV$factor == "N"]
st_lab <- c(found = "取得", found_mismatch = "取得（定义与公式不完全一致）", not_found = "取不到（停下）")
fmt_v <- function(f, v) ifelse(is.na(v), "－", ifelse(f == "incidence", yen(v), sprintf("%.4f", v)))
add("### 7.3 一年对象患者的净收益（主比较，λ = 500 万日元/QALY，方案费用 E02）", "",
    "#### 7.3.1 年对象人数 N 的推算（**尾崎确认待ち**）", "",
    md_table(data.frame(因子 = NS$label, 值 = fmt_v(NS$factor, NS$value), 状态 = st_lab[NS$status], 数据年份 = NS$data_year, 出处 = NS$source,
                        位置 = NS$location, 备注 = NS$note, check.names = FALSE, row.names = NULL)), "",
    if (is.na(Nn)) sprintf("N 未算出：%s 取不到，按指示停下，不自行假设。下表只报告每人的值。", paste(NS$label[NS$status == "not_found"], collapse = "、"))
    else sprintf("N = %s（%s）。%s与公式的定义差距大（见备注），N 只是暂定的量级，待尾崎确认。", yen(round(Nn)), paste(fmt_v(NS$factor, NS$value), collapse = " × "), paste(NS$label[grepl("不一致（大）", NS$note)], collapse = "、")), "")
oku <- function(v) ifelse(is.na(v), "－", formatC(v / 1e8, format = "f", digits = 1, big.mark = ","))
add("#### 7.3.2 净收益（\"如果有效\"时的条件值）", "",
    md_table(data.frame(栏 = ifelse(CV$column == "base", "基准", "早期复发后 k（外部）"), hr0 = sprintf("%.2f", CV$hr0),
                        `上限（万日元）` = man(CV$cap_det), `每人净收益 = 上限 − E02（万日元）` = cell(CV$nb_person_det, CV$nb_person_median, CV$nb_person_lo, CV$nb_person_hi),
                        N = ifelse(is.na(CV$N), "－", yen(round(CV$N))),
                        `一年对象患者的净收益（亿日元）` = ifelse(is.na(CV$N), "－", sprintf("%s（%s [%s, %s]）", oku(CV$nb_total_det), oku(CV$nb_total_median), oku(CV$nb_total_lo), oku(CV$nb_total_hi))),
                        check.names = FALSE)), "",
    "这是\"如果运动的复发风险比为该 hr0\"时的条件值，不是期望值（运动效应的大小未知，本研究不对其设分布）。确定性值（PSA 中位数 [2.5%, 97.5%]，由第 1 节的 PSA 样本计算；N 不抽样）。净收益按 λ = 500 万日元/QALY 换算 QALY，减去方案费用 E02（19.24 万日元）。", "")
add("### 7.4 不做 EVPI 的理由", "",
    sprintf("EVPI 需要假设运动效应（hr0）的分布。划算的分界点（主比较的 E02 交点 hr0 = %.3f，第 1.5 节）接近 1：hr0 = 0.95 时上限 ≥ E02 的概率为 %s，hr0 = 1.00 时为 %s（第 1.1 节）。所以 EVPI 几乎完全由所假设的分布在 hr0 ≥ 1（分界点以上）一侧放多少概率决定，反映的是这一假设而不是数据（与分析计划第 6 节不做运动效应合成分布的理由相同）。",
            CR$hr0[CR$comparison == "main" & CR$column == "base" & CR$lambda == 5e6 & CR$programme == "E02"],
            pct(SM$p_cap500_ge_E02[SM$comparison == "main" & SM$column == "base" & SM$axis == "hr0" & abs(SM$x - 0.95) < 1e-9]),
            pct(SM$p_cap500_ge_E02[SM$comparison == "main" & SM$column == "base" & SM$axis == "hr0" & abs(SM$x - 1.00) < 1e-9])), "")
writeLines(L, file.path(ROOT, "output", "phase2", "phase2b_report.md"), useBytes = TRUE)
cat("wrote phase2b_report.md:", length(L), "lines\n")
