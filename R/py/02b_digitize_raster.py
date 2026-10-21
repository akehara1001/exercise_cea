"""Step 2 (raster figures): colour separation on the embedded image at its native resolution.

Usage: python -I R/py/02b_digitize_raster.py <project_root>
The page image is the publisher's embedded JPEG (Yau 2022 Fig. 4: 1920 x 1881 px placed at
300 dpi). Rendering the page at 600 dpi would only interpolate those pixels, so the native
image is used without resampling.
Writes data/digitized/<fig_id>_<curve>_curve.csv, <fig_id>_risktable.csv,
<fig_id>_native.jpg and data/digitized/raster_extraction_log.csv.
"""
import sys, os, json, csv
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import cv2
import pymupdf

root = sys.argv[1]
spec = json.load(open(os.path.join(root, "R", "py", "rasterspec.json"), encoding="utf-8"))
outdir = os.path.join(root, "data", "digitized")
os.makedirs(outdir, exist_ok=True)


def tick_centres(mask_1d_profile):
    """Centres of runs of True in a 1-D boolean array."""
    idx = np.where(mask_1d_profile)[0]
    if len(idx) == 0:
        return []
    runs, start = [], idx[0]
    for a, b in zip(idx, idx[1:]):
        if b != a + 1:
            runs.append((start, a))
            start = b
    runs.append((start, idx[-1]))
    return runs


log = []
for f in spec["figures"]:
    doc = pymupdf.open(os.path.join(root, "input", "papers", f["pdf"]))
    page = doc[f["page"] - 1]
    xref = max(page.get_images(full=True), key=lambda im: im[2] * im[3])[0]
    info = doc.extract_image(xref)
    raw = np.frombuffer(info["image"], dtype=np.uint8)
    raw.tofile(os.path.join(outdir, f"{f['fig_id']}_native.{info['ext']}"))
    bgr = cv2.imdecode(raw, cv2.IMREAD_COLOR)
    rgb = bgr[:, :, ::-1].astype(float)
    x0, y0, x1, y1 = f["panel_px"]
    P = rgb[y0:y1, x0:x1]
    grey = P.mean(2)
    chroma = P.max(2) - P.min(2)
    dark = (grey < 110) & (chroma < 40)

    # axes: longest dark column / row inside the panel
    col_counts = dark.sum(0)
    row_counts = dark.sum(1)
    yaxis_cols = np.where(col_counts > 0.8 * col_counts.max())[0]
    xaxis_rows = np.where(row_counts > 0.8 * row_counts.max())[0]
    yaxis_c = yaxis_cols.mean()
    xaxis_r = xaxis_rows.mean()
    ya_l, ya_r = yaxis_cols.min(), yaxis_cols.max()
    xa_t, xa_b = xaxis_rows.min(), xaxis_rows.max()

    # x ticks: dark pixels in the rows just below the x axis
    band = dark[xa_b + 2: xa_b + 7, :].copy()
    band[:, : ya_l - 1] = False          # the y label "0" sits left of the y axis at this height
    xr = tick_centres(band.sum(0) >= 3)
    # weighted centre of each tick run
    xt = [np.average(np.arange(a, b + 1), weights=band.sum(0)[a:b + 1]) for a, b in xr]
    band = dark[:, ya_l - 7: ya_l - 2]
    yr = tick_centres(band.sum(1) >= 3)
    yt = [np.average(np.arange(a, b + 1), weights=band.sum(1)[a:b + 1]) for a, b in yr]
    if len(xt) != len(f["x_tick_labels"]) or len(yt) != len(f["y_tick_labels"]):
        raise RuntimeError(f"tick count mismatch x={len(xt)} y={len(yt)}")
    fx = np.polyfit(xt, f["x_tick_labels"], 1)
    fy = np.polyfit(sorted(yt, reverse=True), f["y_tick_labels"], 1)
    rx = max(abs(np.polyval(fx, a) - b) for a, b in zip(xt, f["x_tick_labels"]))
    ry = max(abs(np.polyval(fy, a) - b) for a, b in zip(sorted(yt, reverse=True), f["y_tick_labels"]))

    # colour classification (nearest centre in RGB, saturated pixels only)
    names = list(f["curves"].keys())
    centres = np.array([f["curves"][k] for k in names], dtype=float)
    d = np.sqrt(((P[:, :, None, :] - centres[None, None, :, :]) ** 2).sum(3))
    lab = d.argmin(2)
    ok = (d.min(2) < 75) & (chroma > 50)
    lx0, ly0, lx1, ly1 = f["legend_px"]
    ok[ly0 - y0: ly1 - y0, lx0 - x0: lx1 - x0] = False
    ok[:, : int(ya_r) + 2] = False
    ok[int(xa_t) - 1:, :] = False

    # risk table consistency
    rt = f["risk_table"]
    times = f["risk_table_times"]
    with open(os.path.join(outdir, f"{f['fig_id']}_risktable.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["arm", "time", "n_risk", "cum_censored", "cum_events"])
        for k in names:
            N = rt[k]["n"][0]
            ev = [N - n - c for n, c in zip(rt[k]["n"], rt[k]["cum_censored"])]
            if any(b < a for a, b in zip(ev, ev[1:])) or ev[0] != 0:
                raise RuntimeError(f"risk table inconsistent for {k}: {ev}")
            for t, n, c, e in zip(times, rt[k]["n"], rt[k]["cum_censored"], ev):
                w.writerow([k, t, n, c, e])

    for ci, k in enumerate(names):
        m = ok & (lab == ci)
        # keep horizontal line pixels (drop vertical drop segments and the vertical arm of '+')
        hm = m.copy()
        hm[:, 1:-1] = m[:, 1:-1] & m[:, :-2] & m[:, 2:]
        H, W = hm.shape
        level = np.full(W, np.nan)
        for x in range(W):
            ys = np.where(hm[:, x])[0]
            if len(ys) == 0:
                continue
            # split into clusters; the curve is the lowest cluster (right-continuous at drops)
            cl = tick_centres(np.isin(np.arange(H), ys))
            a, b = cl[-1]
            level[x] = (a + b) / 2.0
        # the plot is truncated at the last x tick; '+' arms of marks there poke past it
        x_tmax = int(np.floor(np.polyval(np.poly1d(np.polyfit(f["x_tick_labels"], xt, 1)), max(f["x_tick_labels"]))))
        level[x_tmax + 1:] = np.nan
        xs = np.where(~np.isnan(level))[0]
        first, last = xs.min(), xs.max()
        # start of curve: 100% at time 0 (curves overlap at the top before the first drops)
        x_t0 = int(round(np.polyval(np.poly1d(np.polyfit(f["x_tick_labels"], xt, 1)), 0)))
        y_100 = float(np.polyval(np.poly1d(np.polyfit(f["y_tick_labels"], sorted(yt, reverse=True), 1)), 100))
        lev = level.copy()
        lev[x_t0] = y_100 if np.isnan(lev[x_t0]) else min(lev[x_t0], y_100)
        # forward fill gaps, then enforce monotone non-increasing survival (y px non-decreasing)
        cur = y_100
        for x in range(x_t0, last + 1):
            if not np.isnan(lev[x]):
                cur = max(cur, lev[x])
            lev[x] = cur
        # vertices of the step function
        verts = [(x_t0, lev[x_t0])]
        for x in range(x_t0 + 1, last + 1):
            if lev[x] > lev[x - 1] + 1e-9:
                verts.append((x, lev[x - 1]))
                verts.append((x, lev[x]))
        verts.append((last, lev[last]))
        rows = []
        for x, yv in verts:
            # pixel centre coordinates in the full image
            t = float(np.polyval(fx, x + 0.0))
            s = float(np.polyval(fy, yv + 0.0))
            rows.append((max(t, 0.0), min(s, 100.0), x + x0, yv + y0))
        with open(os.path.join(outdir, f"{f['fig_id']}_{k}_curve.csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["time", "surv_pct", "x_px", "y_px"])
            for r in rows:
                w.writerow([f"{r[0]:.5f}", f"{r[1]:.5f}", r[2], f"{r[3]:.2f}"])
        cover = np.mean(~np.isnan(level[x_t0:last + 1]))
        log.append(dict(fig_id=f["fig_id"], arm=k, n_pixels=int(m.sum()), n_line_pixels=int(hm.sum()),
                        column_coverage=round(float(cover), 4), n_steps=(len(verts) - 2) // 2,
                        t_last=round(rows[-1][0], 4), s_last=round(rows[-1][1], 3),
                        calib_resid_x=round(rx, 4), calib_resid_y=round(ry, 4),
                        px_per_unit_x=round(1 / fx[0], 3), px_per_pct_y=round(-1 / fy[0], 3),
                        native_px=f"{info['width']}x{info['height']}", image_ext=info["ext"]))
        print(f"{f['fig_id']} {k}: steps={(len(verts) - 2) // 2} coverage={cover:.3f} "
              f"last=({rows[-1][0]:.3f},{rows[-1][1]:.2f}) resid=({rx:.4f},{ry:.4f})")

with open(os.path.join(outdir, "raster_extraction_log.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(log[0].keys()))
    w.writeheader()
    w.writerows(log)
