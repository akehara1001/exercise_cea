"""Step 2 (vector figures): extract exact KM step coordinates, censor marks and risk tables.

Usage: python -I R/py/02_digitize_vector.py <project_root>
Writes data/digitized/<fig_id>_<arm>_curve.csv, _censor.csv, <fig_id>_risktable.csv,
and data/digitized/vector_extraction_log.csv (one row per curve).
"""
import sys, os, json, csv
sys.stdout.reconfigure(encoding="utf-8")
root = sys.argv[1]
sys.path.insert(0, os.path.join(root, "R", "py"))
import pymupdf
import kmvec

spec = json.load(open(os.path.join(root, "R", "py", "figspec.json"), encoding="utf-8"))
outdir = os.path.join(root, "data", "digitized")
os.makedirs(outdir, exist_ok=True)
log = []
for f in spec["figures"]:
    page = pymupdf.open(os.path.join(root, "input", "papers", f["pdf"]))[f["page"] - 1]
    ax = kmvec.find_axes(page, f["clip"])
    cal = kmvec.calibrate(page, f["clip"], ax)
    rt = kmvec.risk_table(page, f["clip"], ax, cal, f["row_labels"])
    with open(os.path.join(outdir, f"{f['fig_id']}_risktable.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["arm", "time", "n_risk"])
        for arm, vals in rt.items():
            for t, n in vals:
                w.writerow([arm, t, n])
    xlab = [p[1] for p in cal["xpairs"]]
    ylab = [p[1] for p in cal["ypairs"]]
    if "inset" in f:
        iax = kmvec.find_axes(page, f["inset"]["clip"])
        ical = kmvec.calibrate(page, f["inset"]["clip"], iax, y_mode="lsq", ylabel_min=f["inset"]["ylabel_min"])
        rows = []
        for arm, col in f["arms"].items():
            _, _, mv = kmvec.km_path(page, ax, cal, col)
            _, _, iv = kmvec.km_path(page, iax, ical, col)
            tmax = min(kmvec.to_data(cal, *mv[-1])[0], kmvec.to_data(ical, *iv[-1])[0])
            t = 3.0
            while t <= tmax:
                sm = kmvec.to_data(cal, 0, kmvec.curve_y_at(mv, kmvec.to_px_x(cal, t)))[1]
                si = kmvec.to_data(ical, 0, kmvec.curve_y_at(iv, kmvec.to_px_x(ical, t)))[1]
                rows.append((arm, t, round(sm, 4), round(si, 4), round(sm - si, 4)))
                t += 3.0
        with open(os.path.join(outdir, f"{f['fig_id']}_inset_check.csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["arm", "time", "surv_main", "surv_inset", "diff"])
            w.writerows(rows)
        diffs = sorted(abs(r[4]) for r in rows)
        inset_maxdiff, inset_meddiff = diffs[-1], diffs[len(diffs) // 2]
        print(f"{f['fig_id']} inset check: n={len(rows)} median|main-inset|={inset_meddiff:.4f} "
              f"max={inset_maxdiff:.4f} pct-points (max = one-step offsets at drop times)")
    else:
        inset_maxdiff = inset_meddiff = None
    for arm, col in f["arms"].items():
        idx, width, verts = kmvec.km_path(page, ax, cal, col)
        data = [kmvec.to_data(cal, x, y) for x, y in verts]
        with open(os.path.join(outdir, f"{f['fig_id']}_{arm}_curve.csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["time", "surv_pct", "x_pt", "y_pt"])
            for (t, s), (x, y) in zip(data, verts):
                w.writerow([f"{t:.5f}", f"{s:.5f}", f"{x:.3f}", f"{y:.3f}"])
        cx = kmvec.censor_marks(page, ax, col, verts, idx)
        with open(os.path.join(outdir, f"{f['fig_id']}_{arm}_censor.csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["time", "x_pt"])
            for x in cx:
                w.writerow([f"{kmvec.to_data(cal, x, 0)[0]:.5f}", f"{x:.3f}"])
        drops = sum(1 for a, b in zip(verts, verts[1:]) if abs(a[0] - b[0]) < 0.5 and b[1] > a[1] + 1e-6)
        lc = kmvec.legend_colour(page, f["clip"], ax, f["row_labels"][arm])
        legend_match = "no legend sample" if lc is None else str(kmvec.same_color(lc, col))
        if lc is not None and not kmvec.same_color(lc, col):
            raise RuntimeError(f"{f['fig_id']} {arm}: legend sample colour {lc} differs from spec {col}")
        log.append(dict(fig_id=f["fig_id"], arm=arm, pdf=f["pdf"], page=f["page"], path_index=idx,
                        legend_colour_matches_spec=legend_match,
                        line_width=round(width, 2), n_vertices=len(verts), n_drops=drops,
                        n_censor_marks=len(cx), s_first=round(data[0][1], 4),
                        t_last=round(data[-1][0], 3), s_last=round(data[-1][1], 3),
                        inset_median_abs_diff=inset_meddiff, inset_max_abs_diff=inset_maxdiff,
                        x_axis_min=min(xlab), x_axis_max=max(xlab), x_label_step=round(xlab[1] - xlab[0], 3),
                        y_axis_min=min(ylab), y_axis_max=max(ylab),
                        calib_resid_x=round(cal["resid_x"], 4), calib_resid_y=round(cal["resid_y"], 4),
                        n_xticks_labelled=len(cal["xpairs"]), n_yticks_labelled=len(cal["ypairs"]),
                        risk_times=";".join(f"{t:g}" for t, _ in rt[arm]),
                        risk_n=";".join(str(n) for _, n in rt[arm])))
        print(f"{f['fig_id']:12s} {arm:8s} verts={len(verts):4d} drops={drops:4d} censor={len(cx):4d} "
              f"last=({data[-1][0]:.2f},{data[-1][1]:.2f}) resid=({cal['resid_x']:.4f},{cal['resid_y']:.4f}) "
              f"risk={rt[arm]}")
with open(os.path.join(outdir, "vector_extraction_log.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(log[0].keys()))
    w.writeheader()
    w.writerows(log)
