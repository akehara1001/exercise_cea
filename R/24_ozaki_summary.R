# 24_ozaki_summary.R
# Provisional results for Dr Ozaki, in Japanese (docx), from the phase-2 outputs only (the model is not
# run): output/phase2/main/det_caps.csv, psa_caps_summary.csv, det_reference.csv,
# psa_reference_summary.csv, scenario_caps.csv, scenario_reference.csv, det_yardstick.csv and
# output/phase2/phase2b_report.md (section 1.7: cost-saving crossings; section 1: programme costs;
# section 6: effect of the provisional rows).
# Outputs: output/phase2/ozaki/運動CEA_暫定結果_v2.docx, fig1_cap.png and check_v2.md (mechanical
# checks of the docx: Heading styles, bold outside label cells, non-black text, 「・」, and the source of
# every number in the text).
# Every number placed in the text goes through reg(), which records the shown string, the source and the
# raw value; the check reads the numbers back from the saved docx and requires each to be registered.
# v2 (2026-10-25, user instruction; v1 was not sent, it and check_v1.md are in output/phase2/ozaki/archive/):
# premises line 2 (published data up to the final analysis); table 1 cost per QALY as estimates only, footnote
# rewritten; figure 1 legend names the solid and the dashed line.
# v3 (2026-10-25, user instruction; v2 not sent, it and check_v2.md in archive/): table 1 caption says that the
# columns of incremental cost and QALYs carry the ranges.

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
suppressPackageStartupMessages({ library(officer); library(flextable); library(ggplot2); library(grid) })
M <- file.path(ROOT, "output", "phase2", "main")
O <- file.path(ROOT, "output", "phase2", "ozaki"); dir.create(O, showWarnings = FALSE, recursive = TRUE)
VER <- "v3"
DOCX <- file.path(O, sprintf("運動CEA_暫定結果_%s.docx", VER))
rd <- function(f) read.csv(file.path(M, f), stringsAsFactors = FALSE, encoding = "UTF-8")
DC <- rd("det_caps.csv"); SM <- rd("psa_caps_summary.csv"); DR <- rd("det_reference.csv"); RS <- rd("psa_reference_summary.csv")
SC <- rd("scenario_caps.csv"); SF <- rd("scenario_reference.csv"); YS <- rd("det_yardstick.csv")
REP <- readLines(file.path(ROOT, "output", "phase2", "phase2b_report.md"), encoding = "UTF-8")
FONT <- "Yu Mincho"; FIGFONT <- "Yu Gothic"

# ---------------------------------------------------------------- number registry
REG <- data.frame(shown = character(0), source = character(0), raw = character(0), stringsAsFactors = FALSE)
reg <- function(shown, source, raw = "") { REG[nrow(REG) + 1, ] <<- list(shown, source, as.character(raw)); shown }
minus <- function(s) sub("^-", "−", s)
num <- function(v, d) minus(formatC(v, format = "f", digits = d, big.mark = ","))
man <- function(v, src, d = 1) reg(num(v / 1e4, d), src, v)                      # yen -> 万円
pct <- function(p, src) paste0(reg(sprintf("%.1f", 100 * p), src, p), "%")
# settings and labels used in the text (not result values): registered with their source
const <- function(s, source) invisible(reg(s, source, s))

# section 1.7 of phase2b_report.md: crossings (main, base column) and programme costs
i17 <- grep("^### 1.7", REP); i2 <- grep("^## 2\\.", REP)
t17 <- REP[i17:i2][grepl("^\\| E0[123] \\|", REP[i17:i2])]
c17 <- do.call(rbind, lapply(strsplit(t17, "\\|"), function(z) trimws(z[-1])))
stopifnot(nrow(c17) == 3, identical(c17[, 1], c("E01", "E02", "E03")))
E_MAN <- setNames(as.numeric(c17[, 2]), c17[, 1])                                # 万円, as in the report
CROSS <- setNames(c17[, 3], c17[, 1])                                            # main comparison (base)
# section 6: effect of the provisional rows on the main cap (万円)
i6 <- grep("^## 6\\.", REP); t6 <- REP[i6:length(REP)][grepl("^\\| [A-Z][0-9]", REP[i6:length(REP)])]
w6 <- as.numeric(sapply(strsplit(t6, "\\|"), function(z) trimws(z[4])))
stopifnot(length(w6) == 9, max(w6) < 1)

# ---------------------------------------------------------------- text helpers
tp <- function(size = 10.5, sup = FALSE) fp_text(font.family = FONT, font.size = size, color = "black", bold = FALSE,
                                               vertical.align = if (sup) "superscript" else "baseline")
para <- function(doc, ..., size = 10.5, after = 4, align = "left") {
  parts <- list(...)
  runs <- lapply(parts, function(p) if (is.list(p)) ftext(p$t, tp(size, sup = TRUE)) else ftext(p, tp(size)))
  body_add_fpar(doc, do.call(fpar, c(runs, list(fp_p = fp_par(text.align = align, padding.bottom = after, line_spacing = 1.15)))))
}
sup <- function(s) list(t = s)
A4P <- prop_section(page_size = page_size(width = 21 / 2.54, height = 29.7 / 2.54, orient = "portrait"),
                    page_margins = page_mar(top = 1, bottom = 1, left = 1, right = 1, header = 0.5, footer = 0.5, gutter = 0), type = "nextPage")
A4L <- prop_section(page_size = page_size(width = 21 / 2.54, height = 29.7 / 2.54, orient = "landscape"),
                    page_margins = page_mar(top = 0.9, bottom = 0.9, left = 1, right = 1, header = 0.5, footer = 0.5, gutter = 0), type = "nextPage")
bd <- fp_border(color = "black", width = 0.75)
ft_style <- function(ft, label_cells) {
  ft <- font(ft, fontname = FONT, part = "all"); ft <- fontsize(ft, size = 9.5, part = "all")
  ft <- color(ft, color = "black", part = "all"); ft <- bold(ft, bold = FALSE, part = "all")
  ft <- border_remove(ft); ft <- hline_top(ft, border = bd, part = "header"); ft <- hline_bottom(ft, border = bd, part = "header")
  ft <- hline_bottom(ft, border = bd, part = "body")
  ft <- valign(ft, valign = "center", part = "all"); ft <- align(ft, align = "center", part = "all"); ft <- align(ft, j = 1, align = "left", part = "all")
  for (lc in label_cells) ft <- bold(ft, i = lc$i, j = lc$j, bold = TRUE, part = lc$part)   # label cells without numbers only
  set_table_properties(ft, layout = "fixed")
}
cellv <- function(est, lo, hi) paste0(est, " [", lo, ", ", hi, "]")

# ---------------------------------------------------------------- table 1
r_base <- DR[DR$column == "base", ]; r_kext <- DR[DR$column == "kext", ]; r_sjp <- SF[SF$scenario == "sjp" & SF$column == "base", ]
p_base <- RS[RS$column == "base", ]; p_kext <- RS[RS$column == "kext", ]
t1row <- function(lab, r, p, srcd, srcp) {
  if (is.null(p)) return(data.frame(cond = lab, dc = man(r$dC, srcd), dq = reg(sprintf("%.3f", r$dQ), srcd, r$dQ), icer = man(r$icer, srcd),
                                    p5 = "－", p7 = "－", stringsAsFactors = FALSE))
  data.frame(cond = lab,
             dc = cellv(man(r$dC, srcd), man(p$dC_lo, srcp), man(p$dC_hi, srcp)),
             dq = cellv(reg(sprintf("%.3f", r$dQ), srcd, r$dQ), reg(sprintf("%.3f", p$dQ_lo), srcp, p$dQ_lo), reg(sprintf("%.3f", p$dQ_hi), srcp, p$dQ_hi)),
             icer = man(r$icer, srcd),                                     # estimate only (v2)
             p5 = pct(p$p_ce_500, srcp), p7 = pct(p$p_ce_750, srcp), stringsAsFactors = FALSE)
}
T1 <- rbind(t1row("基本", r_base, p_base, "det_reference.csv（column = base）", "psa_reference_summary.csv（column = base）"),
            t1row("ペムブロリズマブ群の再発後の生存をやや短く置いた場合", r_kext, p_kext, "det_reference.csv（column = kext）", "psa_reference_summary.csv（column = kext）"),
            t1row("日本の術後治療を入れた場合", r_sjp, NULL, "scenario_reference.csv（scenario = sjp）", ""))
ft1 <- flextable(T1)
ft1 <- set_header_labels(ft1, cond = "条件", dc = "増分費用（万円）", dq = "増分QALY", icer = "1QALYあたりの費用（万円）",
                         p5 = "500万円以下の確率", p7 = "750万円以下の確率")
const("1", "1QALY（単位の 1）"); const("500", "判断の基準 λ = 500万円/QALY（docs/analysis_plan_phase2.md 第 2 節、phase2b_report.md）")
const("750", "参照の基準 λ = 750万円/QALY（同上）")
ft1 <- compose(ft1, i = 1, j = "icer", part = "header", value = as_paragraph("1QALYあたりの費用（万円）", as_sup("✳")))
ft1 <- compose(ft1, i = 1, j = "p5", part = "header", value = as_paragraph("500万円以下の確率", as_sup("§")))
ft1 <- compose(ft1, i = 1, j = "p7", part = "header", value = as_paragraph("750万円以下の確率", as_sup("§")))
ft1 <- compose(ft1, i = 2, j = "cond", part = "body", value = as_paragraph("ペムブロリズマブ群の再発後の生存をやや短く置いた場合", as_sup("†")))
ft1 <- compose(ft1, i = 3, j = "cond", part = "body", value = as_paragraph("日本の術後治療を入れた場合", as_sup("‡")))
ft1 <- ft_style(ft1, list(list(i = 1, j = 1:3, part = "header"), list(i = 1:3, j = 1, part = "body")))
ft1 <- width(ft1, j = 1:6, width = c(5.4, 4.4, 3.8, 5.2, 2.6, 2.6) / 2.54)

# ---------------------------------------------------------------- figure 1
lab_main <- "ペムブロリズマブを含む治療に上乗せ"; lab_sec <- "化学療法のみに上乗せ"
fd <- function(comp) {
  d <- DC[DC$comparison == comp & DC$column == "base" & DC$axis == "hr0", ]; s <- SM[SM$comparison == comp & SM$column == "base" & SM$axis == "hr0", ]
  d <- merge(d[, c("x", "cap_500")], s[, c("x", "cap500_lo", "cap500_hi")], by = "x")
  data.frame(series = if (comp == "main") lab_main else lab_sec, x = d$x, y = d$cap_500 / 1e4, lo = d$cap500_lo / 1e4, hi = d$cap500_hi / 1e4)
}
FD <- rbind(fd("main"), fd("secondary")); FD$series <- factor(FD$series, c(lab_main, lab_sec))
EL <- data.frame(y = unname(E_MAN), lab = sprintf("想定%d  %.1f万円", 1:3, E_MAN))
base_plot <- function(d) ggplot(d, aes(x, y)) +
  geom_ribbon(aes(ymin = lo, ymax = hi, fill = series), alpha = 0.45) +
  geom_line(aes(x, lo, linetype = series), linewidth = 0.25) + geom_line(aes(x, hi, linetype = series), linewidth = 0.25) +
  geom_line(aes(linetype = series), linewidth = 0.9) +
  geom_hline(yintercept = EL$y, linetype = "dotted", linewidth = 0.4) + geom_hline(yintercept = 0, linewidth = 0.3, colour = "grey40") +
  scale_linetype_manual(values = c("solid", "longdash"), name = NULL) + scale_fill_manual(values = c("grey45", "grey80"), name = NULL) +
  scale_x_reverse() + theme_bw(base_size = 10, base_family = FIGFONT) +
  theme(legend.position = "bottom", legend.key.width = unit(1.4, "cm"), panel.grid.minor = element_blank())
gA <- base_plot(FD) + geom_vline(xintercept = 0.72, linetype = "twodash", linewidth = 0.35) +
  annotate("text", x = 0.723, y = Inf, label = "HR 0.72（参照）", hjust = 1, vjust = 1.4, size = 3.2, family = FIGFONT) +
  annotate("text", x = 0.73, y = 55, label = "点線：想定1～3の費用（Bで拡大）", hjust = 1, size = 3, family = FIGFONT) +
  scale_x_reverse(breaks = seq(0.70, 1.00, by = 0.05)) +
  labs(x = "運動による再発のリスクの低下（ハザード比 HR、右ほど低下が大きい）", y = "上限（万円）", title = "A")
gB <- base_plot(FD[FD$x >= 0.95 - 1e-9, ]) +
  geom_text(data = EL, aes(x = 0.951, y = y, label = lab), hjust = 1, vjust = c(-0.4, 1.4, -0.4), size = 3.1, family = FIGFONT, inherit.aes = FALSE) +
  coord_cartesian(ylim = c(-3, 60)) + scale_x_reverse(breaks = seq(0.95, 1.00, by = 0.01)) +
  labs(x = "運動による再発のリスクの低下（ハザード比 HR）", y = "上限（万円）", title = "B　HR 0.95～1.00 の拡大") + theme(legend.position = "none")
FIG <- file.path(O, "fig1_cap.png")
ragg::agg_png(FIG, width = 16, height = 19, units = "cm", res = 300)
grid.newpage(); pushViewport(viewport(layout = grid.layout(2, 1, heights = unit(c(0.6, 0.4), "npc"))))
print(gA, vp = viewport(layout.pos.row = 1, layout.pos.col = 1)); print(gB, vp = viewport(layout.pos.row = 2, layout.pos.col = 1))
invisible(dev.off())
FIG_NUMS <- c("目盛：0.70〜1.00（0.05 間隔）、0.95〜1.00（0.01 間隔）", sprintf("想定%d %.1f万円（phase2b_report.md 第 1.7 節）", 1:3, E_MAN), "HR 0.72（参照線）")

# ---------------------------------------------------------------- table 2
HRS <- c(0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00)
t2cell <- function(comp, h) {
  d <- DC[DC$comparison == comp & DC$column == "base" & DC$axis == "hr0" & abs(DC$x - h) < 1e-9, ]
  s <- SM[SM$comparison == comp & SM$column == "base" & SM$axis == "hr0" & abs(SM$x - h) < 1e-9, ]
  dg <- if (h == 1) 2 else 1                                          # HR 1.00: two decimals (values near 0)
  cellv(man(d$cap_500, sprintf("det_caps.csv（%s, base, hr0 = %.2f, cap_500）", comp, h), dg),
        man(s$cap500_lo, sprintf("psa_caps_summary.csv（%s, base, hr0 = %.2f, cap500_lo）", comp, h), dg),
        man(s$cap500_hi, sprintf("psa_caps_summary.csv（%s, base, hr0 = %.2f, cap500_hi）", comp, h), dg))
}
T2 <- data.frame(hr = sapply(HRS, function(h) reg(sprintf("%.2f", h), "HR の格点（det_caps.csv の x）", h)),
                 main = sapply(HRS, t2cell, comp = "main"), sec = sapply(HRS, t2cell, comp = "secondary"), stringsAsFactors = FALSE)
ft2 <- flextable(T2)
ft2 <- set_header_labels(ft2, hr = "HR", main = lab_main, sec = lab_sec)
ft2 <- compose(ft2, i = 7, j = "hr", part = "body", value = as_paragraph(T2$hr[7], as_sup("✳")))
ft2 <- ft_style(ft2, list(list(i = 1, j = 1:3, part = "header")))
ft2 <- width(ft2, j = 1:3, width = c(2.2, 7.5, 7.5) / 2.54)

# ---------------------------------------------------------------- table 3
t3 <- function(sc, comp) {
  d <- SC[SC$scenario == sc & SC$comparison == comp & SC$column == "base" & SC$axis == "hr0" & abs(SC$x - 0.85) < 1e-9, ]
  stopifnot(nrow(d) == 1); man(d$cap_500, sprintf("scenario_caps.csv（scenario = %s, %s, hr0 = 0.85, cap_500）", sc, comp))
}
SCN <- c(base = "基本（5年間効果が続き、その後薄れる）", path_a_s1 = "手術後1年で薄れ始める", path_a_s2 = "ずっと続く", continue_s1 = "術後も運動を続ける")
T3 <- data.frame(cond = unname(SCN), main = sapply(names(SCN), t3, comp = "main"), sec = sapply(names(SCN), t3, comp = "secondary"), stringsAsFactors = FALSE)
const("5", "効果が続く期間 5 年（docs/analysis_plan_phase2.md 第 3 節）"); const("0.85", "HR 0.85（表 3 の条件、analysis_plan 第 6 節）")
ft3 <- flextable(T3)
ft3 <- set_header_labels(ft3, cond = "効果の続き方", main = lab_main, sec = lab_sec)
ft3 <- compose(ft3, i = 1, j = "cond", part = "body", value = as_paragraph("基本（5年間効果が続き、その後薄れる", as_sup("✳"), "）"))
ft3 <- compose(ft3, i = 4, j = "cond", part = "body", value = as_paragraph("術後も運動を続ける", as_sup("†")))
ft3 <- ft_style(ft3, list(list(i = 1, j = 1:3, part = "header")))   # body labels not bold: rows 1-2 contain digits, kept uniform
ft3 <- width(ft3, j = 1:3, width = c(7, 7.5, 7.5) / 2.54)

# ---------------------------------------------------------------- yardstick
ya <- YS[YS$axis == "hr0", ]; yb <- YS[YS$axis == "pcr", ]
YS_HR <- reg(sprintf("%.3f", ya$root), "det_yardstick.csv（axis = hr0, root）", ya$root)
YS_RED <- reg(sprintf("%.0f", 100 * (1 - ya$root) + 1e-9), "1 − det_yardstick.csv の hr0 root（57.5% を四捨五入）", 100 * (1 - ya$root))
YS_PCR <- reg(sprintf("%.1f", 100 * yb$root), "det_yardstick.csv（axis = pcr, root × 100）", 100 * yb$root)

# ---------------------------------------------------------------- document
doc <- read_docx()
doc <- para(doc, "術前化学療法中の運動プログラムとペムブロリズマブの費用効用分析（暫定結果）", size = 14, after = 12)
doc <- para(doc, "比較は", const("4", "比較した群の数（4 群）"), "群：化学療法のみ、運動を追加、ペムブロリズマブを追加、両方を追加。")
doc <- para(doc, "生存のデータは KEYNOTE-522 試験の公表データ（最終解析まで）に基づいて推計した。")
doc <- para(doc, "公的医療の立場で、費用と効果を年", const("2", "割引率 年 2%（docs/model_spec.md 第 5 節）"), "%で割り引き、生涯にわたり計算した。")
doc <- para(doc, "判断の基準は1QALYあたり500万円（参照として750万円）とした。")
doc <- para(doc, "入力値の", const("9", "【要確認】の 9 行（phase2b_report.md 冒頭と第 6 節）"), "項目は確認中の暫定値だが、主要な結果への影響は",
            const("1", "phase2b_report.md 第 6 節：主比較の上限への影響の最大が 0.0 万円（1 万円未満）"), "万円未満。")
doc <- body_end_block_section(doc, block_section(A4P))
# table 1 (landscape)
doc <- para(doc, "表1　ペムブロリズマブの費用対効果（化学療法のみとの比較）。増分費用と増分QALYの欄は推定値 [不確かさを反映した範囲]。範囲は",
            const("2.5", "PSA の 2.5 パーセンタイル（psa_reference_summary.csv、phase2b_report.md）"), "%から",
            const("97.5", "PSA の 97.5 パーセンタイル（同上）"), "%。", after = 6)
doc <- body_add_flextable(doc, ft1, align = "left")
doc <- para(doc, sup("✳"), "1QALYあたりの費用は、費用が減る場合や QALY が減る場合を含むと範囲の解釈が難しいため、推定値のみ示す。不確かさは右の",
            const("2", "表1の右の確率の列数（2 列）"), "列の確率で示した。", size = 9, after = 1)
doc <- para(doc, sup("§"), "1QALYあたりの費用がその基準以下となる（費用対効果がよいと判断される）確率。", size = 9, after = 1)
doc <- para(doc, sup("†"), "ペムブロリズマブ群で、治療開始から早い時期の遠隔再発の後の死亡リスクを、化学療法の時代のデータより高く置いた（外部の研究による）。", size = 9, after = 1)
doc <- para(doc, sup("‡"), "術前化学療法で病理学的完全奏効が得られなかった例に、日本で使われている術後治療（カペシタビン、gBRCA 陽性例ではオラパリブ）を加えた。この条件では不確かさを反映した範囲と確率を計算していない（－）。", size = 9, after = 1)
doc <- body_end_block_section(doc, block_section(A4L))
# figure 1 (portrait)
doc <- para(doc, "図1　1人あたりかけてよい運動プログラム費用の上限（1QALYあたり500万円の基準）", after = 4)
doc <- body_add_img(doc, src = FIG, width = 16 / 2.54, height = 19 / 2.54)
doc <- para(doc, "上限は、運動プログラムを加えても1QALYあたり500万円の基準を満たす、1人あたりのプログラム費用の上限。実線はペムブロリズマブを含む治療に上乗せ、破線は化学療法のみに上乗せした場合の推定値、帯は不確かさを反映した範囲（",
            "2.5", "%から", "97.5", "%）。点線は想定1、想定2、想定3の運動プログラムの費用。横軸は、運動によって再発のリスクを何%下げるかをハザード比（HR）で示す。", size = 9, after = 2)
doc <- para(doc, "HR 0.72 の線は参照として示した、結腸癌の CHALLENGE 試験（", const("3", "CHALLENGE の介入期間 3 年（docs/analysis_plan_phase2.md 第 3 節）"),
            "年間のプログラム、無病生存期間）のハザード比。", size = 9, after = 2)
const("0.72", "CHALLENGE のハザード比（docs/analysis_plan_phase2.md 第 3 節）")
const("0.95", "図 1B の拡大範囲"); const("1.00", "HR の上端（効果なし）")
doc <- body_end_block_section(doc, block_section(A4P))
# tables 2 and 3, yardstick (landscape, the last section)
doc <- para(doc, "表2　HR 別の、1人あたりかけてよい運動プログラム費用の上限（万円、1QALYあたり500万円の基準）。各欄は推定値 [不確かさを反映した範囲（2.5%から97.5%）]。", after = 6)
doc <- body_add_flextable(doc, ft2, align = "left")
doc <- para(doc, sup("✳"), "HR 1.00 は効果がない場合で、運動の有害事象の分だけ上限がわずかに負になる（この行だけ小数第2位まで示す）。", size = 9, after = 2)
const("2", "小数第 2 位（表示の桁）")
ecost <- function(e) reg(sprintf("%.1f", E_MAN[[e]]), sprintf("phase2b_report.md 第 1.7 節（%s の費用、万円）", e), E_MAN[[e]])
ecross <- function(e) reg(CROSS[[e]], sprintf("phase2b_report.md 第 1.7 節（%s、主比較の基準の欄）", e), CROSS[[e]])
doc <- para(doc, "医療費の削減だけでプログラム費用をまかなえる HR（ペムブロリズマブを含む治療に上乗せする場合）：想定1（", ecost("E01"), "万円）は",
            ecross("E01"), "、想定2（", ecost("E02"), "万円）は", ecross("E02"), "、想定3（", ecost("E03"), "万円）は", ecross("E03"),
            "。HR がこれより小さければ、プログラム費用を含めても費用が減り、QALY は増える。", after = 12)
doc <- body_add_break(doc)                                              # table 3 on its own page, not split
doc <- para(doc, "表3　結果を最も動かす仮定：効果の続き方（HR 0.85、1QALYあたり500万円の基準、推定値、万円）", after = 6)
doc <- body_add_flextable(doc, ft3, align = "left")
doc <- para(doc, sup("✳"), "薄れる：効果（1 − HR）が", const("1", "半減期 1 年（docs/analysis_plan_phase2.md 第 3 節）"), "年ごとに半分になる。", size = 9, after = 1)
doc <- para(doc, sup("†"), "手術後も月", const("1", "術後の指導 月 1 回（入力表 E04 の備考）"), "回の指導を続け（その費用を含む）、続けている間は効果が保たれ、その後薄れる。手術後1年で薄れ始める条件と比べる。", size = 9, after = 12)
doc <- para(doc, "同じ物差しで見ると：運動でペムブロリズマブと同じ QALY の増分を得るには、再発のリスクを HR ", YS_HR, "（約", YS_RED,
            "%低下）まで下げるか、病理学的完全奏効（pCR）の割合を", YS_PCR, "ポイント上げる必要がある。いずれも図と表の範囲（HR ",
            const("0.70", "HR の主軸の下端（analysis_plan 第 3 節）"), "まで、pCR は", const("10", "pCR の主軸の上端 10 ポイント（analysis_plan 第 3 節）"),
            "ポイントまで）を超える。")
doc <- body_set_default_section(doc, A4L)
print(doc, target = DOCX)
cat("wrote", DOCX, "\n")

# ---------------------------------------------------------------- mechanical checks
tmp <- file.path(tempdir(), "ozaki_docx"); unlink(tmp, recursive = TRUE); unzip(DOCX, exdir = tmp)
X <- xml2::read_xml(file.path(tmp, "word", "document.xml")); ns <- xml2::xml_ns(X)
pstyles <- xml2::xml_attr(xml2::xml_find_all(X, ".//w:pStyle", ns), "val")
n_heading <- sum(grepl("heading|見出し", pstyles, ignore.case = TRUE))
runs_b <- xml2::xml_find_all(X, ".//w:r[w:rPr/w:b[not(@w:val='0' or @w:val='false')]]", ns)
in_tc <- vapply(runs_b, function(r) !inherits(xml2::xml_find_first(r, "ancestor::w:tc", ns), "xml_missing"), logical(1))
cell_txt <- sapply(runs_b, function(r) { tc <- xml2::xml_find_first(r, "ancestor::w:tc", ns); if (inherits(tc, "xml_missing")) "" else xml2::xml_text(tc) })
n_bold_body <- sum(!in_tc); n_bold_numcell <- sum(in_tc & grepl("[0-9]", cell_txt))
cols <- xml2::xml_attr(xml2::xml_find_all(X, ".//w:color", ns), "val")
n_nonblack <- sum(!(toupper(cols) %in% c("000000", "AUTO"))) + length(xml2::xml_find_all(X, ".//w:highlight", ns))
ptext <- sapply(xml2::xml_find_all(X, ".//w:p", ns), function(p) paste(xml2::xml_text(xml2::xml_find_all(p, ".//w:t", ns)), collapse = ""))
n_dot <- sum(grepl("・", ptext, fixed = TRUE)); n_note <- sum(grepl("^\\s*Note", ptext))
sect <- xml2::xml_find_all(X, ".//w:sectPr/w:pgSz", ns)
pg <- data.frame(w = as.numeric(xml2::xml_attr(sect, "w")), h = as.numeric(xml2::xml_attr(sect, "h")), orient = xml2::xml_attr(sect, "orient"))
a4 <- all(abs(pmin(pg$w, pg$h) - 11906) <= 2 & abs(pmax(pg$w, pg$h) - 16838) <= 2)
# numbers in the text: labels first (trial name, 表/図/想定 numbers), then every number must be registered
txt <- paste(ptext, collapse = "\n")
labels <- regmatches(txt, gregexpr("KEYNOTE-522|表[0-9]|図[0-9]|想定[0-9]", txt))[[1]]
rest <- gsub("KEYNOTE-522|表[0-9]|図[0-9]|想定[0-9]", " ", txt)
toks <- regmatches(rest, gregexpr("[−-]?[0-9][0-9,]*(\\.[0-9]+)?", rest))[[1]]
toks <- gsub("^-", "−", toks)
unreg <- setdiff(unique(toks), REG$shown)
L <- c(sprintf("# 尾崎先生向け暫定結果資料 %s の確認", VER), "",
       sprintf("対象：`output/phase2/ozaki/%s`（`R/24_ozaki_summary.R` が生成、%s）。数値は `output/phase2/main/` の結果ファイルと `output/phase2/phase2b_report.md` から読み、モデルは実行していない。",
               basename(DOCX), format(Sys.time(), "%Y-%m-%d %H:%M")), "",
       "## 1. 機械的な確認", "",
       "| 項目 | 結果 | 基準 |", "|---|---|---|",
       sprintf("| Heading スタイルの段落 | %d | 0 |", n_heading),
       sprintf("| 本文（表の外）の太字 run | %d | 0 |", n_bold_body),
       sprintf("| 表の中で数字を含むセルの太字 run | %d | 0 |", n_bold_numcell),
       sprintf("| 黒以外の文字色（w:color が 000000 か auto 以外、蛍光ペン） | %d | 0 |", n_nonblack),
       sprintf("| 「・」を含む段落 | %d | 0 |", n_dot),
       sprintf("| 「Note」で始まる段落 | %d | 0 |", n_note),
       sprintf("| 用紙 A4（全セクション） | %s（%s） | すべて A4 |", if (a4) "はい" else "いいえ", paste(sprintf("%s %gx%g", ifelse(is.na(pg$orient), "portrait", pg$orient), pg$w, pg$h), collapse = "、")),
       sprintf("| 本文中の数字のうち出典の登録がないもの | %d（%s） | 0 |", length(unreg), if (length(unreg)) paste(unreg, collapse = "、") else "なし"),
       "", sprintf("本文から読み取った数字 %d 個（ラベル %d 個：%s）。表の数値は flextable のセルの文字列も含む。", length(toks), length(labels), paste(unique(labels), collapse = "、")), "",
       "## 2. 本文の数字と出典の対照", "",
       "結果の数値は表示の文字列と元の値（円、または比率）を並べた。設定と単位の数字（1QALY の 1、割引率の 2 など）は結果ファイル以外の出典（分析計画、model_spec）を示した。", "",
       "| 表示 | 出典 | 元の値 |", "|---|---|---|",
       apply(unique(REG), 1, function(r) sprintf("| %s | %s | %s |", r[["shown"]], r[["source"]], r[["raw"]])), "",
       "## 3. 図1の中の数字（画像のため本文からは読み取れない）", "",
       paste0("- ", FIG_NUMS), "- 線と帯は det_caps.csv（cap_500）と psa_caps_summary.csv（cap500_lo、cap500_hi）を R でそのまま描いた（`fig1_cap.png`）。", "",
       "## 4. 指示からの変更", "",
       sprintf("- 同じ物差しの「再発のリスクを約 57%% 下げる」は、1 − %s = %.1f%% を四捨五入して約 %s%% とした。", sprintf("%.4f", ya$root), 100 * (1 - ya$root), YS_RED),
       "- 「日本の術後治療を入れた場合」は確定的な計算だけで、不確かさの範囲と確率はない（－、表1の脚注‡）。",
       "- 表2の HR 1.00 の行は値が 0 に近いため小数第 2 位まで示した（脚注✳）。", "",
       "## 5. v1 からの変更（v2、2026-10-25。v1 は未送付、`archive/` に移した）", "",
       "- 前提の第 2 行：「生存のデータは KEYNOTE-522 試験の公表データ（最終解析まで）に基づいて推計した。」",
       "- 表1：「1QALYあたりの費用（万円）」の列は推定値だけにした（範囲を外した）。脚注✳を「1QALYあたりの費用は、費用が減る場合や QALY が減る場合を含むと範囲の解釈が難しいため、推定値のみ示す。不確かさは右の2列の確率で示した。」に替えた（✳ は列の見出しの右上のまま）。",
       "- 図1の図注：「実線はペムブロリズマブを含む治療に上乗せ、破線は化学療法のみに上乗せした場合の推定値」。", "",
       "## 6. v2 からの変更（v3、2026-10-25。v2 は未送付、`archive/` に移した）", "",
       "- 表1の見出し：「各欄は推定値 [不確かさを反映した範囲]」を「増分費用と増分QALYの欄は推定値 [不確かさを反映した範囲]」に替えた。ほかは v2 のまま。")
writeLines(L, file.path(O, sprintf("check_%s.md", VER)), useBytes = TRUE)
cat(sprintf("checks: heading %d, bold body %d, bold numeric cells %d, non-black %d, middle dots %d, Note %d, A4 %s, unregistered numbers %d\n",
            n_heading, n_bold_body, n_bold_numcell, n_nonblack, n_dot, n_note, a4, length(unreg)))
stopifnot(n_heading == 0, n_bold_body == 0, n_bold_numcell == 0, n_nonblack == 0, n_dot == 0, n_note == 0, a4, length(unreg) == 0)
