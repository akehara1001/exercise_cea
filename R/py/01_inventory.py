"""Step 1: inventory of KM figures in the three KEYNOTE-522 papers and Yau 2022.

Usage: python -I R/py/01_inventory.py <project_root>
Writes data/reported_values.csv (every reported number with page and matched text) and
output/phase1/inventory.csv. Supplementary figures that the main texts cite but that are
not in input/papers are listed with available = "no".
"""
import sys, os, json, csv
sys.stdout.reconfigure(encoding="utf-8")
root = sys.argv[1]
sys.path.insert(0, os.path.join(root, "R", "py"))
import pymupdf
import kmvec
from pdftext import PdfText
from facts import FACTS

papers = os.path.join(root, "input", "papers")
import hashlib
with open(os.path.join(root, "data", "input_manifest.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["file", "bytes", "pages", "sha256"])
    for fn in sorted(os.listdir(papers)):
        p = os.path.join(papers, fn)
        w.writerow([fn, os.path.getsize(p), len(pymupdf.open(p)), hashlib.sha256(open(p, "rb").read()).hexdigest()])
texts = {}
vals, rows = {}, []
for f in FACTS:
    if f["pdf"] not in texts:
        texts[f["pdf"]] = PdfText(os.path.join(papers, f["pdf"]))
    m, page = texts[f["pdf"]].find(f["rx"])
    if len(m.groups()) != len(f["keys"]):
        raise RuntimeError(f"{f['id']}: {len(m.groups())} groups vs {len(f['keys'])} keys")
    for k, v in zip(f["keys"], m.groups()):
        v = v.replace("−", "-")
        vals[(f["id"], k)] = v
        rows.append(dict(fact_id=f["id"], key=k, value=v, pdf=f["pdf"], page=page, matched_text=m.group(0)[:400]))
os.makedirs(os.path.join(root, "data"), exist_ok=True)
with open(os.path.join(root, "data", "reported_values.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print(f"reported values: {len(rows)} from {len(FACTS)} patterns")


def v(fid, key):
    return vals[(fid, key)]


def pg(fid):
    return next(r["page"] for r in rows if r["fact_id"] == fid)


# axis ranges and risk-table times straight from the figures
vs = json.load(open(os.path.join(root, "R", "py", "figspec.json"), encoding="utf-8"))
axinfo = {}
for f in vs["figures"]:
    page = pymupdf.open(os.path.join(papers, f["pdf"]))[f["page"] - 1]
    ax = kmvec.find_axes(page, f["clip"])
    cal = kmvec.calibrate(page, f["clip"], ax)
    rt = kmvec.risk_table(page, f["clip"], ax, cal, f["row_labels"])
    xl = [p[1] for p in cal["xpairs"]]
    yl = [p[1] for p in cal["ypairs"]]
    axinfo[f["fig_id"]] = dict(
        x_axis=f"{min(xl):g}-{max(xl):g} months (labels every {xl[1] - xl[0]:g})",
        y_axis=f"{min(yl):g}-{max(yl):g}%",
        risk_times=";".join(f"{t:g}" for t, _ in rt["pembro"]),
        n=f"pembro {rt['pembro'][0][1]}; placebo {rt['placebo'][0][1]}")
rs = json.load(open(os.path.join(root, "R", "py", "rasterspec.json"), encoding="utf-8"))
for f in rs["figures"]:
    doc = pymupdf.open(os.path.join(papers, f["pdf"]))
    pg_ = doc[f["page"] - 1]
    im = max(pg_.get_images(full=True), key=lambda im: im[2] * im[3])
    info = doc.extract_image(im[0])
    rect = pg_.get_image_rects(im[0])[0]
    raster_fmt = f"raster ({info['ext'].upper()} {info['width']}x{info['height']}, {info['width'] / (rect.width / 72):.0f} dpi as placed)"
    axinfo[f["fig_id"]] = dict(
        x_axis=f"{min(f['x_tick_labels']):g}-{max(f['x_tick_labels']):g} years",
        y_axis=f"{min(f['y_tick_labels']):g}-{max(f['y_tick_labels']):g}%",
        risk_times=";".join(f"{t:g}" for t in f["risk_table_times"]),
        n="; ".join(f"{k} {f['risk_table'][k]['n'][0]}" for k in f["curves"]))

comp22 = ("first events (pembro/placebo): progression precluding surgery {}/{}, local {}/{}, distant {}/{}, "
          "second primary {}/{}, death {}/{}; local followed by distant {}/{}").format(
    *(v("K22_efs_composition", k) for k in ["prog_pembro", "prog_placebo", "local_pembro", "local_placebo",
                                           "distant_pembro", "distant_placebo", "second_primary_pembro",
                                           "second_primary_placebo", "death_pembro", "death_placebo"]),
    v("K22_local_then_distant", "pembro"), v("K22_local_then_distant", "placebo"))
comp24 = ("first events (pembro/placebo): progression precluding surgery {}/{}, local {}/{}, distant {}/{}, "
          "second primary {}/{}, death {}/{}").format(
    *(v("K24_efs_composition", k) for k in ["prog_pembro", "prog_placebo", "local_pembro", "local_placebo",
                                           "distant_pembro", "distant_placebo", "second_primary_pembro",
                                           "second_primary_placebo", "death_pembro", "death_placebo"]))

INV = []


def add(**kw):
    INV.append(kw)


add(fig_key="K20_F2_EFS", source="Schmid 2020 NEJM 382:810", figure="Fig. 2", location="main text", available="yes",
    format="vector", endpoint="EFS", population="ITT, by arm", analysis="IA2",
    data_cutoff=v("K20_cutoff", "data_cutoff"), median_fu_months=v("K20_cutoff", "median_fu_months"),
    time_origin="randomization", landmark_at_surgery="n/a (ITT)", **axinfo["K20_F2_EFS"],
    events=f"pembro {v('K20_efs_events', 'events_pembro')}/{v('K20_efs_events', 'n_pembro')}; placebo {v('K20_efs_events', 'events_placebo')}/{v('K20_efs_events', 'n_placebo')}",
    milestones=f"18-mo EFS pembro {v('K20_efs_18m', 'pembro')}% ({v('K20_efs_18m', 'pembro_lo')}-{v('K20_efs_18m', 'pembro_hi')}), placebo {v('K20_efs_18m', 'placebo')}% ({v('K20_efs_18m_placebo_ci', 'placebo_lo')}-{v('K20_efs_18m_placebo_ci', 'placebo_hi')})",
    hr=f"{v('K20_efs_hr', 'hr')} ({v('K20_efs_hr', 'hr_lo')}-{v('K20_efs_hr', 'hr_hi')}), stratified Cox",
    efs_event_composition=f"in supplementary {v('K20_efs_event_types', 'source')} (not provided)",
    source_pages=f"text p{pg('K20_efs_events')},{pg('K20_efs_18m')}; figure p8",
    notes="superseded by IA4/IA7; censor marks merged in drawing (counts differ from N - events)")
add(fig_key="K22_F1_EFS", source="Schmid 2022 NEJM 386:556", figure="Fig. 1", location="main text", available="yes",
    format="vector", endpoint="EFS", population="ITT, by arm", analysis="IA4",
    data_cutoff=v("K22_cutoff", "data_cutoff"), median_fu_months=v("K22_cutoff", "median_fu_months"),
    time_origin=v("K22_efs_origin", "origin"), landmark_at_surgery="n/a (ITT)", **axinfo["K22_F1_EFS"],
    events=f"pembro {v('K22_efs_events_hr', 'events_pembro')}/784; placebo {v('K22_efs_events_hr', 'events_placebo')}/390",
    milestones=f"36-mo EFS pembro {v('K22_efs_36m', 'pembro')}% ({v('K22_efs_36m', 'pembro_lo')}-{v('K22_efs_36m', 'pembro_hi')}), placebo {v('K22_efs_36m', 'placebo')}% ({v('K22_efs_36m', 'placebo_lo')}-{v('K22_efs_36m', 'placebo_hi')})",
    hr=f"{v('K22_efs_events_hr', 'hr')} ({v('K22_efs_events_hr', 'hr_lo')}-{v('K22_efs_events_hr', 'hr_hi')}), stratified Cox",
    efs_event_composition=comp22, source_pages=f"text p{pg('K22_efs_events_hr')},{pg('K22_efs_36m')}; Table 1 p{pg('K22_efs_composition')}; figure p5",
    notes="")
add(fig_key="K22_F3_OS", source="Schmid 2022 NEJM 386:556", figure="Fig. 3", location="main text", available="yes",
    format="vector", endpoint="OS", population="ITT, by arm", analysis="IA4",
    data_cutoff=v("K22_cutoff", "data_cutoff"), median_fu_months=v("K22_cutoff", "median_fu_months"),
    time_origin="randomization", landmark_at_surgery="n/a (ITT)", **axinfo["K22_F3_OS"],
    events=f"deaths pembro {v('K22_os_events_hr', 'events_pembro')}/784; placebo {v('K22_os_events_hr', 'events_placebo')}/390",
    milestones=f"36-mo OS pembro {v('K22_os_36m', 'pembro')}% ({v('K22_os_36m', 'pembro_lo')}-{v('K22_os_36m', 'pembro_hi')}), placebo {v('K22_os_36m', 'placebo')}% ({v('K22_os_36m', 'placebo_lo')}-{v('K22_os_36m', 'placebo_hi')})",
    hr=f"{v('K22_os_events_hr', 'hr')} ({v('K22_os_events_hr', 'hr_lo')}-{v('K22_os_events_hr', 'hr_hi')}), stratified Cox",
    efs_event_composition="n/a", source_pages=f"text p{pg('K22_os_events_hr')}; figure p8", notes="superseded by IA7 (final OS)")
add(fig_key="K22_S3_DRFS", source="Schmid 2022 NEJM 386:556", figure=v("K22_drfs_hr", "figure"), location="supplementary appendix",
    available="no", format="unknown", endpoint="DRFS (distant progression/recurrence or death)", population="ITT, by arm", analysis="IA4",
    data_cutoff=v("K22_cutoff", "data_cutoff"), median_fu_months=v("K22_cutoff", "median_fu_months"),
    time_origin="randomization (per protocol definition)", landmark_at_surgery="n/a (ITT)",
    x_axis="", y_axis="", risk_times="", n="pembro 784; placebo 390", events="not in main text", milestones="not in main text",
    hr=f"{v('K22_drfs_hr', 'hr')} ({v('K22_drfs_hr', 'hr_lo')}-{v('K22_drfs_hr', 'hr_hi')})", efs_event_composition="n/a",
    source_pages=f"text p{pg('K22_drfs_hr')}", notes="supplementary appendix not in input/papers")
add(fig_key="K22_S4_EFS_by_pCR", source="Schmid 2022 NEJM 386:556", figure=v("K22_efs_nonpcr", "figure"), location="supplementary appendix",
    available="no", format="unknown", endpoint="EFS", population="arm x pCR (ypT0/Tis ypN0)", analysis="IA4",
    data_cutoff=v("K22_cutoff", "data_cutoff"), median_fu_months=v("K22_cutoff", "median_fu_months"),
    time_origin="randomization per EFS definition; to confirm on the figure", landmark_at_surgery="yes if origin is randomization",
    x_axis="", y_axis="", risk_times="",
    n=f"pCR: pembro {v('K22_efs_pcr', 'n_pembro')}, placebo {v('K22_efs_pcr', 'n_placebo')}; non-pCR: pembro {v('K22_efs_nonpcr', 'n_pembro')}, placebo {v('K22_efs_nonpcr', 'n_placebo')}",
    events=f"pCR: pembro {v('K22_efs_pcr', 'events_pembro')}, placebo {v('K22_efs_pcr', 'events_placebo')}; non-pCR: pembro {v('K22_efs_nonpcr', 'events_pembro')}, placebo {v('K22_efs_nonpcr', 'events_placebo')}",
    milestones="not in main text",
    hr=f"pCR {v('K22_efs_pcr', 'hr')} ({v('K22_efs_pcr', 'hr_lo')}-{v('K22_efs_pcr', 'hr_hi')}); non-pCR {v('K22_efs_nonpcr', 'hr')} ({v('K22_efs_nonpcr', 'hr_lo')}-{v('K22_efs_nonpcr', 'hr_hi')})",
    efs_event_composition="not in main text", source_pages=f"text p{pg('K22_efs_pcr')}",
    notes="core model input (EFS by arm x pCR); supplementary appendix not in input/papers")
add(fig_key="K24_F1A_OS", source="Schmid 2024 NEJM 391:1981", figure="Fig. 1A", location="main text", available="yes",
    format="vector (with 2x inset)", endpoint="OS", population="ITT, by arm", analysis="IA7 (final OS)",
    data_cutoff=v("K24_cutoff", "data_cutoff"), median_fu_months=v("K24_cutoff", "median_fu_months"),
    time_origin=v("K24_os_origin", "origin"), landmark_at_surgery="n/a (ITT)", **axinfo["K24_F1A_OS"],
    events=f"deaths pembro {v('K24_os_events', 'events_pembro')}/784; placebo {v('K24_os_events', 'events_placebo')}/390",
    milestones="; ".join(f"{y}-y OS pembro {v('K24_os_milestones', f'pembro_{y}y')}% ({v('K24_os_milestones', f'pembro_{y}y_lo')}-{v('K24_os_milestones', f'pembro_{y}y_hi')}), placebo {v('K24_os_milestones', f'placebo_{y}y')}% ({v('K24_os_milestones', f'placebo_{y}y_lo')}-{v('K24_os_milestones', f'placebo_{y}y_hi')})" for y in (3, 4, 5)),
    hr=(f"overall stratified HR not reported in main text; unstratified piecewise HR {v('K24_os_piecewise_hr', 'hr_early')} "
        f"({v('K24_os_piecewise_hr', 'hr_early_lo')}-{v('K24_os_piecewise_hr', 'hr_early_hi')}) before {v('K24_os_piecewise_hr', 'cut_years')} y, "
        f"{v('K24_os_piecewise_hr', 'hr_late')} ({v('K24_os_piecewise_hr', 'hr_late_lo')}-{v('K24_os_piecewise_hr', 'hr_late_hi')}) after; event-weighted average {v('K24_os_piecewise_hr', 'weighted_hr')}"),
    efs_event_composition="n/a", source_pages=f"text p{pg('K24_os_events')},{pg('K24_os_milestones')}; figure p5",
    notes="calibration target for OS (step 5)")
add(fig_key="K24_F2A_EFS", source="Schmid 2024 NEJM 391:1981", figure="Fig. 2A", location="main text", available="yes",
    format="vector (with 2x inset)", endpoint="EFS", population="ITT, by arm", analysis="IA7",
    data_cutoff=v("K24_cutoff", "data_cutoff"), median_fu_months=v("K24_cutoff", "median_fu_months"),
    time_origin="randomization", landmark_at_surgery="n/a (ITT)", **axinfo["K24_F2A_EFS"],
    events=f"pembro {v('K24_efs_events_hr_5y', 'events_pembro')}/784; placebo {v('K24_efs_events_hr_5y', 'events_placebo')}/390",
    milestones=f"5-y EFS pembro {v('K24_efs_events_hr_5y', 'pembro_5y')}% ({v('K24_efs_events_hr_5y', 'pembro_5y_lo')}-{v('K24_efs_events_hr_5y', 'pembro_5y_hi')}), placebo {v('K24_efs_events_hr_5y', 'placebo_5y')}% ({v('K24_efs_events_hr_5y', 'placebo_5y_lo')}-{v('K24_efs_events_hr_5y', 'placebo_5y_hi')})",
    hr=f"{v('K24_efs_events_hr_5y', 'hr')} ({v('K24_efs_events_hr_5y', 'hr_lo')}-{v('K24_efs_events_hr_5y', 'hr_hi')}), stratified Cox",
    efs_event_composition=comp24, source_pages=f"text p{pg('K24_efs_events_hr_5y')}; Table 1 p{pg('K24_efs_composition')}; figure p7",
    notes="most mature EFS by arm")
add(fig_key="K24_S4_OS_by_pCR", source="Schmid 2024 NEJM 391:1981", figure=v("K24_os_nonpcr", "figure"), location="supplementary appendix",
    available="no", format="unknown", endpoint="OS", population="arm x pCR (ypT0/Tis ypN0)", analysis="IA7",
    data_cutoff=v("K24_cutoff", "data_cutoff"), median_fu_months=v("K24_cutoff", "median_fu_months"),
    time_origin="randomization per OS definition; to confirm on the figure", landmark_at_surgery="yes if origin is randomization",
    x_axis="", y_axis="", risk_times="",
    n=f"pCR: pembro {v('K24_os_pcr', 'n_pembro')}, placebo {v('K24_os_pcr', 'n_placebo')}; non-pCR: pembro {v('K24_os_nonpcr', 'n_pembro')}, placebo {v('K24_os_nonpcr', 'n_placebo')}",
    events=f"deaths pCR: pembro {v('K24_os_pcr', 'deaths_pembro')}, placebo {v('K24_os_pcr', 'deaths_placebo')}; non-pCR: pembro {v('K24_os_nonpcr', 'deaths_pembro')}, placebo {v('K24_os_nonpcr', 'deaths_placebo')}",
    milestones=f"5-y OS difference pCR {v('K24_os_pcr', 'diff_5y')} pp ({v('K24_os_pcr', 'diff_5y_lo')} to {v('K24_os_pcr', 'diff_5y_hi')}); non-pCR {v('K24_os_nonpcr', 'diff_5y')} pp ({v('K24_os_nonpcr', 'diff_5y_lo')} to {v('K24_os_nonpcr', 'diff_5y_hi')}); arm-level 5-y values not in main text",
    hr="not reported", efs_event_composition="n/a", source_pages=f"text p{pg('K24_os_pcr')}",
    notes="supplementary appendix not in input/papers; EFS by pCR at IA7 not cited in main text")
y = "Y22_tnbc_S2"
add(fig_key="Y22_F4A_EFS_TNBC", source="Yau 2022 Lancet Oncol 23:149 (author manuscript) + appendix", figure="Fig. 4A",
    location="main text; KM estimates in appendix Table S2", available="yes", format=raster_fmt,
    endpoint=f"EFS ({v('Y22_efs_definition', 'definition')})", population="HR-negative/HER2-negative (TNBC) by RCB class",
    analysis="pooled 12 cohorts", data_cutoff="Nov 2019 (data collection)", median_fu_months="",
    time_origin=v("Y22_origin", "origin"), landmark_at_surgery="yes (origin = start of NAC)", **axinfo["Y22_F4A_EFS_TNBC"],
    events=f"TNBC total {v('Y22_events', 'events_tnbc')} (all follow-up); by class from risk table",
    milestones="; ".join(f"RCB-{c} 3/5/10-y {v(y, f'rcb{c}_3y')}/{v(y, f'rcb{c}_5y')}/{v(y, f'rcb{c}_10y')}%" for c in range(4)),
    hr="; ".join(f"RCB-{c} vs RCB-0 {v(y, f'hr_rcb{c}')} ({v(y, f'hr_rcb{c}_lo')}-{v(y, f'hr_rcb{c}_hi')})" for c in (1, 2, 3)),
    efs_event_composition="n/a", source_pages=f"text p{pg('Y22_origin')}; appendix p{pg(y)}; figure p21",
    notes=f"KM truncated at {v('Y22_truncation', 'years')} y; external data for extrapolation check (RCB-0 vs RCB-1-3)")

cols = ["fig_key", "source", "figure", "location", "available", "format", "endpoint", "population", "analysis",
        "data_cutoff", "median_fu_months", "time_origin", "landmark_at_surgery", "x_axis", "y_axis", "risk_times",
        "n", "events", "milestones", "hr", "efs_event_composition", "source_pages", "notes"]
out = os.path.join(root, "output", "phase1")
os.makedirs(out, exist_ok=True)
with open(os.path.join(out, "inventory.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader()
    for r in INV:
        w.writerow({c: r.get(c, "") for c in cols})
print(f"inventory: {len(INV)} rows ({sum(r['available'] == 'yes' for r in INV)} available)")

# pCR proportions (ITT denominators) for the model, from the pCR-subgroup sentences
pcr = [("K22 (IA4)", v("K22_efs_pcr", "n_pembro"), v("K22_efs_nonpcr", "n_pembro"), v("K22_efs_pcr", "n_placebo"), v("K22_efs_nonpcr", "n_placebo")),
       ("K24 (IA7)", v("K24_os_pcr", "n_pembro"), v("K24_os_nonpcr", "n_pembro"), v("K24_os_pcr", "n_placebo"), v("K24_os_nonpcr", "n_placebo"))]
with open(os.path.join(root, "data", "pcr_counts.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["source", "pcr_pembro", "nonpcr_pembro", "pcr_placebo", "nonpcr_placebo"])
    w.writerows(pcr)
for p in pcr:
    print(p[0], "pCR pembro", p[1], "/", int(p[1]) + int(p[2]), "placebo", p[3], "/", int(p[3]) + int(p[4]))
