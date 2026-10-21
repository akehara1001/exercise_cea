"""Step 2 (raster figures): colour separation on the embedded image at its native resolution.

Usage: python -I R/py/02b_digitize_raster.py <project_root>
Each figure is the publisher's embedded image (JPEG or PNG). Rendering the page at a higher
dpi would only interpolate those pixels, so the native image is used without resampling.
Per figure (rasterspec.json):
  censor_marks: "plus" (symmetric '+', Yau) or "up" (vertical ticks above the line, NEJM)
  truncated_at_axis_max: curves drawn to the last x tick end there (Yau: 12 y)
  colour_dist_max: max RGB distance to a curve colour centre (per curve)
  fringe: {light curve: [dark curves]} - pixels of a light curve within fringe_px of a dark
          curve are its anti-aliased edge, not the light curve
Writes data/digitized/<fig_id>_<curve>_curve.csv, <fig_id>_risktable.csv, <fig_id>_native.<ext>
and data/digitized/raster_extraction_log.csv.
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


def runs(mask_1d):
    """(start, end) of runs of True in a 1-D boolean array."""
    idx = np.where(mask_1d)[0]
    if len(idx) == 0:
        return []
    out, start = [], idx[0]
    for a, b in zip(idx, idx[1:]):
        if b != a + 1:
            out.append((start, a))
            start = b
    out.append((start, idx[-1]))
    return out


def main_group(idx_bool, counts):
    """Contiguous run of True containing the maximum count."""
    best = int(np.argmax(counts))
    for a, b in runs(idx_bool):
        if a <= best <= b:
            return a, b
    raise RuntimeError("axis not found")


log = []
for f in spec["figures"]:
    doc = pymupdf.open(os.path.join(root, "input", "papers", f["pdf"]))
    page = doc[f["page"] - 1]
    xref = max(page.get_images(full=True), key=lambda im: im[2] * im[3])[0]
    info = doc.extract_image(xref)
    raw = np.frombuffer(info["image"], dtype=np.uint8)
    raw.tofile(os.path.join(outdir, f"{f['fig_id']}_native.{info['ext']}"))
    rect = page.get_image_rects(xref)[0]
    dpi = info["width"] / (rect.width / 72)
    bgr = cv2.imdecode(raw, cv2.IMREAD_COLOR)
    rgb = bgr[:, :, ::-1].astype(float)
    x0, y0, x1, y1 = f["panel_px"]
    P = rgb[y0:y1, x0:x1]
    grey = P.mean(2)
    chroma = P.max(2) - P.min(2)
    dark = (grey < 110) & (chroma < 40)

    # axes: the contiguous group of long dark columns/rows (a dashed reference line is shorter)
    col_counts, row_counts = dark.sum(0), dark.sum(1)
    ya_l, ya_r = main_group(col_counts > 0.8 * col_counts.max(), col_counts)
    xa_t, xa_b = main_group(row_counts > 0.8 * row_counts.max(), row_counts)

    # ticks: dark pixels just outside the axes
    band = dark[xa_b + 2: xa_b + 7, :].copy()
    band[:, : ya_l - 1] = False          # a y label "0" can sit left of the y axis at this height
    xt = [np.average(np.arange(a, b + 1), weights=band.sum(0)[a:b + 1]) for a, b in runs(band.sum(0) >= 3)]
    band = dark[:xa_t, ya_l - 7: ya_l - 2]
    yt = [np.average(np.arange(a, b + 1), weights=band.sum(1)[a:b + 1]) for a, b in runs(band.sum(1) >= 3)]
    yt.append(float((xa_t + xa_b) / 2))  # the 0% tick coincides with the x axis
    yt = sorted(set(round(v, 3) for v in yt), reverse=True)
    if len(xt) != len(f["x_tick_labels"]) or len(yt) != len(f["y_tick_labels"]):
        raise RuntimeError(f"{f['fig_id']}: tick count mismatch x={len(xt)} y={len(yt)}")
    fx = np.polyfit(xt, f["x_tick_labels"], 1)
    fy = np.polyfit(yt, f["y_tick_labels"], 1)
    rx = max(abs(np.polyval(fx, a) - b) for a, b in zip(xt, f["x_tick_labels"]))
    ry = max(abs(np.polyval(fy, a) - b) for a, b in zip(yt, f["y_tick_labels"]))

    # colour classification (nearest centre in RGB, saturated pixels only)
    names = list(f["curves"].keys())
    centres = np.array([f["curves"][k] for k in names], dtype=float)
    dmax = np.array([f.get("colour_dist_max", {}).get(k, 75) for k in names], dtype=float)
    d = np.sqrt(((P[:, :, None, :] - centres[None, None, :, :]) ** 2).sum(3))
    lab = d.argmin(2)
    ok = (d.min(2) < dmax[lab]) & (chroma > 50)
    for lx0, ly0, lx1, ly1 in f["exclude_px"]:
        ok[max(ly0 - y0, 0): ly1 - y0, max(lx0 - x0, 0): lx1 - x0] = False
    ok[:, : ya_r + 2] = False
    ok[xa_t - 1:, :] = False
    masks = {k: ok & (lab == i) for i, k in enumerate(names)}
    fr = f.get("fringe_px", 2)
    kern = np.ones((2 * fr + 1, 2 * fr + 1), np.uint8)
    for light, darks in f.get("fringe", {}).items():
        dk = np.zeros_like(ok)
        for k in darks:
            dk |= masks[k]
        masks[light] = masks[light] & ~cv2.dilate(dk.astype(np.uint8), kern).astype(bool)

    # risk table (transcribed from the image) and its consistency checks
    rt, times = f["risk_table"], f["risk_table_times"]
    with open(os.path.join(outdir, f"{f['fig_id']}_risktable.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["arm", "time", "n_risk", "cum_censored", "cum_events"])
        for k in names:
            n = rt[k]["n"]
            if len(n) != len(times) or any(b > a for a, b in zip(n, n[1:])):
                raise RuntimeError(f"{f['fig_id']} {k}: risk table length or monotonicity: {n}")
            cc = rt[k].get("cum_censored")
            if cc is not None:
                ev = [n[0] - a - c for a, c in zip(n, cc)]
                if any(b < a for a, b in zip(ev, ev[1:])) or ev[0] != 0:
                    raise RuntimeError(f"{f['fig_id']} {k}: risk table inconsistent: {ev}")
            for i, t in enumerate(times):
                w.writerow([k, t, n[i], "" if cc is None else cc[i], "" if cc is None else ev[i]])

    pfit_x = np.polyfit(f["x_tick_labels"], xt, 1)
    pfit_y = np.polyfit(f["y_tick_labels"], yt, 1)
    x_t0 = int(round(np.polyval(pfit_x, 0)))
    x_tmax = int(np.floor(np.polyval(pfit_x, max(f["x_tick_labels"]))))
    y_100 = float(np.polyval(pfit_y, 100))
    y_0 = float(np.polyval(pfit_y, 0))
    PEN = 1.5      # score cost of one drop; one column of line contributes about 2-3
    line_max = f.get("line_max_px", 6)   # taller column clusters contain a censor mark

    up = f["censor_marks"] == "up"
    for k in names:
        m = masks[k]
        H, W = m.shape
        if up:
            # NEJM ticks rise from the line and, where dense, merge into a solid band whose
            # bottom edge is the line: track the bottom edge of the colour mask instead
            src = m.copy()
            src[:-1] &= ~m[1:]
            src[:-2] &= ~m[2:]
            hts = [b - a + 1 for x in range(x_t0, x_tmax + 1) for a, b in runs(m[:, x]) if b - a + 1 <= line_max]
            half = (float(np.median(hts)) - 1) / 2 if hts else 0.0
        else:
            src, half = m, 0.0
        mi = src.astype(float)
        band = mi.copy()
        band[1:] += mi[:-1]
        band[:-1] += mi[1:]
        r0, r1 = int(round(y_100)), int(np.ceil(y_0))
        S = band[r0:r1 + 1, :]
        R = S.shape[0]
        # Viterbi over rows: the curve is a staircase that only moves down (survival only falls).
        # '+' marks sit symmetrically on the line and NEJM ticks only above its bottom edge, so
        # neither can pull a downward-only staircase off the tracked row: a path that followed
        # them would lose the line pixels that continue after them.
        V = np.full(R, -np.inf)
        n0 = int(np.ceil(half)) + 2 if up else 1     # bottom edge sits half a line below 100%
        V[:n0] = S[:n0, x_t0]
        bp = np.zeros((x_tmax + 1, R), dtype=np.int32)
        for x in range(x_t0 + 1, x_tmax + 1):
            pm = np.maximum.accumulate(np.concatenate(([-np.inf], V[:-1])))
            am = np.zeros(R, dtype=np.int32)
            best, bi = -np.inf, 0
            for yy in range(1, R):
                if V[yy - 1] > best:
                    best, bi = V[yy - 1], yy - 1
                am[yy] = bi
            drop = pm - PEN
            take_drop = drop > V
            V = np.where(take_drop, drop, V) + S[:, x]
            bp[x] = np.where(take_drop, am, np.arange(R))
        path = np.zeros(x_tmax + 1, dtype=np.int32)
        path[x_tmax] = int(np.argmax(V))
        for x in range(x_tmax, x_t0, -1):
            path[x - 1] = bp[x, path[x]]
        # steps = runs of constant row; sub-pixel level = median centroid of the line in the
        # columns of the step that carry no censor mark
        steps, xs0, n_clean = [], x_t0, 0
        for x in range(x_t0 + 1, x_tmax + 2):
            if x == x_tmax + 1 or path[x] != path[x - 1]:
                rr = path[xs0] + r0
                cents = []
                for xc in range(xs0, x):
                    col = m[:, xc]
                    if up:
                        hit = [(a, b) for a, b in runs(col) if abs(b - rr) <= 1]
                        if hit:
                            cents.append(hit[0][1] - half)
                        continue
                    hit = [(a, b) for a, b in runs(col) if a - 1 <= rr <= b + 1]
                    if hit and hit[0][1] - hit[0][0] + 1 <= line_max:
                        cents.append((hit[0][0] + hit[0][1]) / 2.0)
                if cents:
                    lvl = float(np.median(cents))
                    n_clean += 1
                elif up:
                    lvl = float(rr) - half
                else:
                    sub = m[rr - 1: rr + 2, xs0: x]
                    w_ = sub.sum(1)
                    lvl = float(rr - 1 + np.average(np.arange(3), weights=w_)) if w_.sum() > 0 else float(rr)
                steps.append([xs0, x - 1, lvl])
                xs0 = x
        steps[0][2] = y_100
        for j in range(1, len(steps)):
            steps[j][2] = max(steps[j][2], steps[j - 1][2])
        verts = [(steps[0][0], steps[0][2])]
        for j in range(1, len(steps)):
            verts.append((steps[j][0], steps[j - 1][2]))
            verts.append((steps[j][0], steps[j][2]))
        on_line = [m[max(path[x] + r0 - 1, 0): path[x] + r0 + 2, x].any() for x in range(x_t0, x_tmax + 1)]
        last = max(x for x, o in zip(range(x_t0, x_tmax + 1), on_line) if o)
        verts = [v for v in verts if v[0] <= last]
        verts.append((last, verts[-1][1]))
        rows = []
        for x, yv in verts:
            # pixel centre coordinates in the full image
            t = float(np.polyval(fx, x + 0.0))
            s = float(np.polyval(fy, yv + 0.0))
            rows.append((max(t, 0.0), min(s, 100.0), x + x0, yv + y0))
        # a curve drawn up to the last tick of a truncated plot runs to the truncation time; the
        # last pixel column maps to slightly less only because of pixel quantisation
        if f.get("truncated_at_axis_max", False) and x_tmax - last <= 2:
            rows[-1] = (float(max(f["x_tick_labels"])),) + rows[-1][1:]
        cover = float(np.mean(on_line[: last - x_t0 + 1]))
        with open(os.path.join(outdir, f"{f['fig_id']}_{k}_curve.csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["time", "surv_pct", "x_px", "y_px"])
            for r in rows:
                w.writerow([f"{r[0]:.5f}", f"{r[1]:.5f}", r[2], f"{r[3]:.2f}"])
        log.append(dict(fig_id=f["fig_id"], arm=k, n_pixels=int(m.sum()),
                        column_coverage=round(cover, 4), n_steps=len(steps) - 1,
                        steps_with_clean_columns=n_clean,
                        t_last=round(rows[-1][0], 4), s_last=round(rows[-1][1], 3),
                        calib_resid_x=round(rx, 4), calib_resid_y=round(ry, 4),
                        px_per_unit_x=round(1 / fx[0], 3), px_per_pct_y=round(-1 / fy[0], 3),
                        native_px=f"{info['width']}x{info['height']}", image_ext=info["ext"],
                        dpi_as_placed=round(dpi, 1)))
        print(f"{f['fig_id']} {k}: steps={len(steps) - 1} coverage={cover:.3f} "
              f"last=({rows[-1][0]:.3f},{rows[-1][1]:.2f}) resid=({rx:.4f},{ry:.4f})")

with open(os.path.join(outdir, "raster_extraction_log.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(log[0].keys()))
    w.writeheader()
    w.writerows(log)
