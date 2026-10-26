"""Figures 1 to 3 of the manuscript, v1 (Python / matplotlib), and figures_v1.docx.

Reads the phase 2 outputs and the parameter workbook; does not run the model.
Each figure is drawn at its final size (170 mm wide) so that every glyph is at
least 8 pt as printed. Exports PDF (for the audits), PNG and TIFF at 600 dpi.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch
from PIL import Image

from docx.shared import Mm
from docx_util import new_document, page_break, para
from v1_common import BUILD, FIGDIR, OUT, ROOT, STAR, SUPP, Params, Registry, csv, fnum, rel

sys.stdout.reconfigure(encoding="utf-8")
SKILL = Path.home() / ".claude" / "skills" / "nature-figure" / "scripts"
sys.path.insert(0, str(SKILL))
from audit_panel_alignment import require_matplotlib_panel_alignment  # noqa: E402

REG = Registry()
PR = Params()
MM = 1 / 25.4
FS = 8  # final-size font floor (WRITING_RULES section 7.2)
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial"],
    "font.size": FS,
    "axes.labelsize": FS,
    "xtick.labelsize": FS,
    "ytick.labelsize": FS,
    "legend.fontsize": FS,
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "legend.frameon": False,
    "text.color": "black",
    "axes.labelcolor": "black",
    "xtick.color": "black",
    "ytick.color": "black",
})
FIGDIR.mkdir(parents=True, exist_ok=True)
ARM_MAIN = "Exercise added to chemotherapy plus pembrolizumab"
ARM_SEC = "Exercise added to chemotherapy alone"
PROG = {"E01": "CHALLENGE-based supervised program", "E02": "Fee-schedule-based program", "E03": "Remote low-cost program"}
PROG_LS = {"E01": (0, (6, 2)), "E02": (0, (5, 1.5, 1, 1.5)), "E03": (0, (1, 1.5))}
AP = "docs/analysis_plan_phase2.md"
MS = "docs/model_spec.md"


def line_of(path, needle):
    for i, ln in enumerate((ROOT / path).read_text(encoding="utf-8").splitlines(), start=1):
        if needle in ln:
            return f"{path} line {i}"
    raise ValueError(needle)


def export(fig, stem):
    """Fixed final size (no tight bounding box), so the inserted size equals the drawn size."""
    base = FIGDIR / stem
    fig.savefig(f"{base}.pdf")
    fig.savefig(f"{base}.svg")
    fig.savefig(f"{base}.png", dpi=600)
    fig.savefig(f"{base}.tiff", dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)
    return Path(f"{base}.pdf"), Path(f"{base}.png"), Path(f"{base}.tiff")


# ================================================================ Fig. 1  model structure
def fig1():
    W, H = 170, 92
    fig = plt.figure(figsize=(W * MM, H * MM))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    m7 = REG.label("7", "Fig. 1, box text", "surgery at month 7 (" + line_of(MS, "手术时点（landmark）为随机化后 7 个月") + ")")
    m18 = REG.label("18", "Fig. 1, box text", "early distant recurrence within 18 months of randomization (" + line_of(MS, "随机化后 18 个月以内的远处复发") + ")")
    boxes = {
        "nac": (3, 40, 36, 20, f"Neoadjuvant therapy\nand surgery\n(months 0 to {m7})"),
        "pcr": (50, 60, 22, 10, "pCR"),
        "npcr": (50, 30, 22, 10, "No pCR"),
        "ef": (84, 40, 30, 20, "Event-free\nafter surgery"),
        "lrr": (122, 68, 36, 16, "Locoregional\nrecurrence"),
        "dr": (122, 38, 36, 24, f"Distant recurrence\nearly (within {m18} months\nof randomization)\nor late"),
        "pp": (3, 6, 36, 16, "Progression during\nneoadjuvant therapy"),
        "death": (122, 6, 36, 16, "Death"),
    }
    for k, (x, y, w, h, txt) in boxes.items():
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.5",
                                    fc="white" if k != "death" else "0.88", ec="black", lw=0.8))
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=FS, linespacing=1.15)

    def c(k, side):
        x, y, w, h, _ = boxes[k]
        return {"l": (x, y + h / 2), "r": (x + w, y + h / 2), "t": (x + w / 2, y + h), "b": (x + w / 2, y),
                "tr": (x + w * 0.8, y + h), "br": (x + w * 0.8, y)}[side]

    def arrow(p, q, rad=0.0, lw=0.8, ls="-"):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=8, lw=lw, color="black",
                                     linestyle=ls, connectionstyle=f"arc3,rad={rad}", shrinkA=1, shrinkB=1))

    arrow(c("nac", "r"), c("pcr", "l"))
    arrow(c("nac", "r"), c("npcr", "l"))
    arrow(c("pcr", "r"), c("ef", "l"))
    arrow(c("npcr", "r"), c("ef", "l"))
    arrow(c("nac", "b"), c("pp", "t"))
    arrow(c("pp", "r"), c("death", "l"))
    arrow((114, 58), (122, 72), lw=1.6)
    arrow(c("ef", "r"), c("dr", "l"), lw=1.6)
    arrow(c("ef", "b"), (126, 22))
    arrow(c("lrr", "b"), c("dr", "t"))
    arrow(c("dr", "b"), c("death", "t"))
    arrow(c("lrr", "r"), c("death", "r"), rad=-0.28)
    ax.text(114.5, 67, "HR", ha="center", va="center", fontsize=FS, fontweight="bold")
    ax.text(118, 53.2, "HR", ha="center", va="center", fontsize=FS, fontweight="bold")
    ax.text(44.5, 50, "Surgery", ha="center", va="center", fontsize=FS, rotation=90, rotation_mode="anchor")
    ax.text(23, 31, "No pCR only", ha="left", va="center", fontsize=FS)
    ax.text(104, 26, "Death without\nrecurrence", ha="right", va="center", fontsize=FS)
    return export(fig, "fig1")


# ================================================================ Fig. 2  cap by HR
def series(comp):
    dc = csv("det_caps.csv")
    ps = csv("psa_caps_summary.csv")
    d = dc[(dc.comparison == comp) & (dc.column == "base") & (dc.axis == "hr0")].sort_values("x")
    p = ps[(ps.comparison == comp) & (ps.column == "base") & (ps.axis == "hr0")].sort_values("x")
    assert np.allclose(d.x.values, p.x.values) and len(d) == 13
    assert ((p.cap500_lo.values <= d.cap_500.values) & (d.cap_500.values <= p.cap500_hi.values)).all()
    for col, f in (("cap_500", "det_caps.csv"), ):
        REG.r(f"{len(d)} points", f"Fig. 2, line, {comp}", "output/phase2/main/det_caps.csv",
              f"comparison = {comp}, column = base, axis = hr0, x = 0.700 to 1.000 by 0.025, cap_500 / 1,000", "see file")
    REG.r(f"{len(p)} points", f"Fig. 2, band, {comp}", "output/phase2/main/psa_caps_summary.csv",
          f"comparison = {comp}, column = base, axis = hr0, x = 0.700 to 1.000 by 0.025, cap500_lo and cap500_hi / 1,000", "see file")
    return d.x.values, d.cap_500.values / 1e3, p.cap500_lo.values / 1e3, p.cap500_hi.values / 1e3


def fig2():
    W, H = 170, 104
    fig, axs = plt.subplots(1, 2, figsize=(W * MM, H * MM))
    fig.subplots_adjust(left=0.085, right=0.985, bottom=0.30, top=0.96, wspace=0.28)
    xm, ym, lm, hm = series("main")
    xs, ysec, ls_, hs = series("secondary")
    e = {}
    for pid in ("E01", "E02", "E03"):
        v, loc = PR.get(pid)
        REG.r("line", f"Fig. 2, horizontal line {pid}", "input/params/parameters_v10.xlsx", loc + " / 1,000", v)
        e[pid] = v / 1e3
    hr_ref = REG.label("0.72", "Fig. 2a, vertical line label", "CHALLENGE DFS HR (input/papers/CHALLENGE.pdf p.7; " + line_of(AP, "图中标出 0.72") + ")")
    assert np.allclose(xm, xs)
    for i, ax in enumerate(axs):
        k = xm >= (0.70 if i == 0 else 0.95) - 1e-9  # draw only the visible range (no clipped geometry in the PDF)
        ax.fill_between(xs[k], ls_[k], hs[k], color="0.90", lw=0, zorder=1)
        ax.fill_between(xm[k], lm[k], hm[k], color="0.62", alpha=0.6, lw=0, zorder=1.5)
        for lo, hi, st in ((lm, hm, "-"), (ls_, hs, "--")):
            ax.plot(xm[k], lo[k], color="0.3", lw=0.5, ls=st, zorder=2)
            ax.plot(xm[k], hi[k], color="0.3", lw=0.5, ls=st, zorder=2)
        ax.plot(xm[k], ym[k], color="black", lw=1.2, ls="-", marker="o", ms=3.2, zorder=4)
        ax.plot(xs[k], ysec[k], color="black", lw=1.2, ls="--", marker="^", ms=3.6, mfc="white", mew=0.8, zorder=4)
        for pid in ("E01", "E02", "E03"):
            ax.axhline(e[pid], color="black", lw=0.7, ls=PROG_LS[pid], zorder=3)
        ax.axhline(0, color="0.5", lw=0.5, zorder=0)
        ax.set_xlabel("Recurrence hazard ratio with exercise")
    a, b = axs
    a.set_xlim(0.695, 1.005)
    a.set_xticks(np.round(np.arange(0.70, 1.0001, 0.05), 2))
    a.set_xticklabels([f"{t:.2f}" for t in a.get_xticks()])
    a.set_ylim(-250, 8000)
    a.set_yticks(range(0, 8001, 1000))
    a.set_yticklabels([f"{t:,}" for t in range(0, 8001, 1000)])
    a.set_ylabel("Maximum affordable program cost (JPY 1,000)")
    a.axvline(0.72, color="black", lw=0.7, ls=(0, (1, 1.5)), zorder=3)
    a.text(0.7245, 1300, f"CHALLENGE\nHR {hr_ref}", ha="left", va="center", fontsize=FS)
    b.set_xlim(0.9495, 1.0005)
    b.set_xticks(np.round(np.arange(0.95, 1.0001, 0.01), 2))
    b.set_xticklabels([f"{t:.2f}" for t in b.get_xticks()])
    b.set_ylim(-40, 1300)
    b.set_yticks(range(0, 1301, 200))
    b.set_yticklabels([f"{t:,}" for t in range(0, 1301, 200)])
    short = {"E01": "CHALLENGE-based", "E02": "Fee-schedule-based", "E03": "Remote low-cost"}
    for pid, dy, va in (("E01", 10, "bottom"), ("E02", -10, "top"), ("E03", 10, "bottom")):
        b.text(0.9505, e[pid] + dy, short[pid], ha="left", va=va, fontsize=FS)
    from matplotlib.legend_handler import HandlerTuple
    band_m = Patch(facecolor="0.62", alpha=0.6, edgecolor="0.3", lw=0.5)
    band_s = Patch(facecolor="0.90", edgecolor="0.3", lw=0.5, ls="--")
    line_m = Line2D([], [], color="black", lw=1.2, ls="-", marker="o", ms=3.2)
    line_s = Line2D([], [], color="black", lw=1.2, ls="--", marker="^", ms=3.6, mfc="white", mew=0.8)
    blank = Line2D([], [], color="none")
    handles = [(band_m, line_m), (band_s, line_s), blank] + \
              [Line2D([], [], color="black", lw=0.7, ls=PROG_LS[pid]) for pid in ("E01", "E02", "E03")]
    labels = [ARM_MAIN, ARM_SEC, ""] + [PROG[p] for p in ("E01", "E02", "E03")]
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, 0.005), ncol=2, handlelength=3.0,
               handler_map={tuple: HandlerTuple(ndivide=None, pad=0)}, columnspacing=1.6, labelspacing=0.45)
    for ax, lab in zip(axs, "ab"):
        ax.text(-0.17 if lab == "a" else -0.17, 1.0, lab, transform=ax.transAxes, fontsize=FS + 1, fontweight="bold", ha="left", va="bottom")
    REG.label("95", "Fig. 2 legend", "95% UI")
    fig.canvas.draw()
    require_matplotlib_panel_alignment(fig, json_out=FIGDIR / "fig2.alignment.json", tolerance_pt=1.5, gutter_tolerance_pt=1.5, strict=True)
    return export(fig, "fig2")


# ================================================================ Fig. 3  tornado
EN = {
    "D05": "Second-line and later treatment, monthly cost",
    "D03P": "First-line treatment, monthly cost, with pembrolizumab",
    "U02": "Utility, event-free after treatment",
    "U04": "Utility, distant recurrence",
    "U03": "Utility, locoregional recurrence",
    "D06": "End-of-life care cost",
    "C03": "Follow-up cost per year, year 6 onward",
    "D01": "Locoregional recurrence, initial cost",
    "A03": "Pembrolizumab cost per dose",
    "D04P": "First-line treatment duration, with pembrolizumab",
    "E06": "Musculoskeletal AEs, any grade, with exercise",
    "C02": "Follow-up cost per year, years 3 to 5",
    "E07": "Musculoskeletal AEs, any grade, without exercise",
    "E09": "Musculoskeletal AEs, grade 3 or higher, with exercise",
    "D02": "Locoregional recurrence, monthly cost",
    "U05": "Utility decrement, grade 3 or higher AE",
    "E08": "Musculoskeletal AE, cost per event",
    "E10": "Musculoskeletal AEs, grade 3 or higher, without exercise",
    "C01": "Follow-up cost per year, years 1 to 2",
    "A04": "Drug administration cost per visit",
    "U01": "Utility, event-free during treatment",
}
RULE_TAG = {"±25%": "[±25%]", "片側対称": "[mirrored]", "薬価固定": "[price]"}


def fig3():
    ow = csv("oneway_base.csv")
    base = float(ow.cap_base.iloc[0])
    ow = ow.assign(w=(ow.cap_high - ow.cap_low).abs())
    sel = ow[ow.w > 1e-6 * max(1, abs(base))].sort_values("w", ascending=False)
    n_rows = len(sel)
    if set(sel.param_id) != set(EN):
        raise ValueError(f"label table does not match the rows that change the result: {sorted(set(sel.param_id) ^ set(EN))}")
    REG.r(str(n_rows), "Fig. 3 legend (number of inputs shown)", "output/phase2/main/oneway_base.csv",
          "rows with |cap_high - cap_low| > 1e-6 x cap_base (same rule as R/23_phase2b_report.R tornado())", n_rows)
    REG.r(f"{n_rows} rows", "Fig. 3, bars", "output/phase2/main/oneway_base.csv", "param_id, cap_low, cap_high, cap_base / 1,000", "see file")
    W, H = 170, 128
    fig, ax = plt.subplots(figsize=(W * MM, H * MM))
    fig.subplots_adjust(left=0.50, right=0.975, bottom=0.10, top=0.985)
    y = np.arange(n_rows)[::-1]
    labels = []
    for yi, (_, r) in zip(y, sel.iterrows()):
        b0 = base / 1e3
        for v, fc, ec in ((r.cap_low / 1e3, "0.25", "black"), (r.cap_high / 1e3, "0.85", "black")):
            ax.barh(yi + (0.19 if fc == "0.25" else -0.19), v - b0, left=b0, height=0.36, color=fc, edgecolor=ec, lw=0.4)
        tag = RULE_TAG.get(r.range_rule, "") if isinstance(r.range_rule, str) else ""
        labels.append(f"{EN[r.param_id]} ({r.param_id})" + (f" {tag}" if tag else ""))
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.tick_params(axis="y", length=0)
    ax.axvline(base / 1e3, color="black", lw=0.8)
    ax.set_xlim(2600, 2850)
    ax.set_xticks(range(2600, 2851, 50))
    ax.set_xticklabels([f"{t:,}" for t in range(2600, 2851, 50)])
    ax.set_xlabel("Maximum affordable program cost (JPY 1,000)")
    ax.set_ylim(-0.7, n_rows - 0.3)
    handles = [Patch(facecolor="0.25", edgecolor="black", lw=0.4, label="Input at its lower bound"),
               Patch(facecolor="0.85", edgecolor="black", lw=0.4, label="Input at its upper bound")]
    ax.legend(handles=handles, loc="lower right", borderaxespad=0.2)
    for tok, why in (("25", "±25% range rule (docs/model_spec.md section 6)"),):
        REG.label(tok, "Fig. 3, labels", why)
    fig.canvas.draw()
    return export(fig, "fig3")


p1, p2, p3 = fig1(), fig2(), fig3()

# ================================================================ figures_v1.docx
S1 = STAR
cap = {
    1: ["Fig. 1. Structure of the state-transition " + "model^{" + S1 + "}",
        "All four arms (chemotherapy alone, chemotherapy plus exercise, chemotherapy plus pembrolizumab, and chemotherapy plus pembrolizumab plus exercise) "
        "share this structure, in 1-month cycles from the start of neoadjuvant therapy at age 49 years to age 100 years. "
        "At surgery (month 7) the cohort is split by pCR, and event-free survival after surgery is modeled separately for each stratum. "
        "Progression that precludes surgery occurs only in patients without pCR. Distant recurrence is early (within 18 months of randomization) or late, "
        "each with tunnel states by months since recurrence. In the arms with exercise, the two transitions marked HR (thick arrows) are multiplied by the recurrence hazard ratio with exercise. "
        "Background mortality applies in every state alive.",
        f"{S1}HR, hazard ratio; pCR, pathological complete response."],
    2: ["Fig. 2. Maximum affordable cost of an exercise program per patient by the recurrence hazard ratio with " + "exercise^{" + S1 + "}",
        "(a) Recurrence hazard ratio from 0.70 to 1.00. (b) The same results enlarged for hazard ratios from 0.95 to 1.00. "
        "Lines show deterministic estimates at a willingness-to-pay threshold of JPY 5 million per QALY for exercise added to chemotherapy plus pembrolizumab "
        "(solid line, circles) and to chemotherapy alone (dashed line, triangles); the dark and light grey bands, edged by thin solid and dashed lines, show their 95% UIs. "
        "Horizontal lines mark the costs of the three program designs in Table 1; exercise is cost-effective wherever a curve lies above the line of the program. "
        "The dotted vertical line in (a) marks the hazard ratio of 0.72 for disease-free survival with a 3-year exercise program in colon cancer (CHALLENGE trial). "
        f"The effect is held for 5 years after randomization and then halves every year. The plotted values are listed in Supplementary Table {SUPP['capgrid']}.",
        f"{S1}Modeled cohort: women aged 49 years starting neoadjuvant chemotherapy for stage II or III triple-negative breast cancer in Japan (Table 1). Costs in JPY 1,000 at fiscal year 2026 prices, discounted at 2% per year over a lifetime horizon. "
        "95% UI: 2.5th and 97.5th percentiles of 1,000 probabilistic sensitivity analysis samples. "
        "HR, hazard ratio; JPY, Japanese yen; QALY, quality-adjusted life year; UI, uncertainty interval."],
    3: ["Fig. 3. One-way sensitivity analysis of the maximum affordable program cost for exercise added to chemotherapy plus pembrolizumab at a recurrence hazard ratio of " + "0.85^{" + S1 + "}",
        "Bars show the maximum affordable cost per patient at a willingness-to-pay threshold of JPY 5 million per QALY when one input is set to its lower bound (dark bars) "
        "or upper bound (light bars) and all other inputs keep their base-case values; the vertical line is the base-case estimate. "
        "All 21 inputs that changed the result are shown, ordered by the width of their range. "
        "Brackets mark ranges set by rule rather than taken from a source: [±25%], ±25% around the base value where no range was available; [mirrored], the missing bound mirrored where only one bound was given; "
        "[price], drug price varied downward only, to 75% of the list price. "
        f"Codes in parentheses refer to Supplementary Table {SUPP['params']}; the plotted values are listed in Supplementary Table {SUPP['oneway']}.",
        f"{S1}Modeled cohort: women aged 49 years starting neoadjuvant chemotherapy for stage II or III triple-negative breast cancer in Japan (Table 1). Costs in JPY 1,000 at fiscal year 2026 prices, discounted at 2% per year over a lifetime horizon. AE, adverse event; JPY, Japanese yen; QALY, quality-adjusted life year."],
}
for tok, why in (("1", "1-month cycles (Table 1)"), ("49", "starting age (Table 1)"), ("100", "time horizon (Table 1)"), ("7", "surgery month (Table 1)"),
                 ("18", "early recurrence cut-off (Table 1)"), ("0.70", "HR range (Table 2)"), ("1.00", "HR range (Table 2)"), ("0.95", "zoom range (Table 2 row)"),
                 ("5", "threshold JPY 5 million / 5-year effect duration (Table 1)"), ("95", "95% UI"), ("0.72", "CHALLENGE HR (Table 1)"), ("3", "3-year CHALLENGE program (Table 1)"),
                 ("2026", "price year"), ("2", "discount rate"), ("2.5", "UI percentile"), ("97.5", "UI percentile"), ("1,000", "PSA samples / JPY 1,000 unit"),
                 ("0.85", "HR of the one-way analysis (Table 2 row)"), ("25", "range rule ±25% (docs/model_spec.md section 6)"),
                 ("75", "drug-price rule: lower bound 0.75 x base (docs/model_spec.md section 6)")):
    REG.label(tok, "figure legends", why)
REG.r("21", "Fig. 3 legend", "output/phase2/main/oneway_base.csv", "number of rows that change the result (see Fig. 3 bars)", 21)

doc = new_document(landscape=False)
img_info = {}
for i, (pdf, png, tif) in enumerate((p1, p2, p3), start=1):
    if i > 1:
        page_break(doc)
    im = Image.open(png)
    wpx, hpx = im.size
    dpi = im.info.get("dpi", (None, None))
    width_mm = wpx / 600 * 25.4
    doc.add_paragraph().add_run().add_picture(str(png), width=Mm(width_mm))
    img_info[f"Fig. {i}"] = dict(png=rel(png), pixels=f"{wpx} x {hpx}", dpi=[round(float(x), 1) for x in dpi] if dpi[0] else None,
                                 inserted_width_mm=round(width_mm, 2), height_mm=round(hpx / 600 * 25.4, 2),
                                 tiff_pixels="x".join(map(str, Image.open(tif).size)))
    for j, t in enumerate(cap[i]):
        para(doc, t, space_after=0)
doc.save(OUT / "figures_v1.docx")
json.dump({"rows": REG.rows, "labels": REG.labels, "images": img_info},
          open(BUILD / "_ledger_figures.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(img_info, indent=1))
