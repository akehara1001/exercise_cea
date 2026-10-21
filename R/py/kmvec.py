"""Vector extraction of Kaplan-Meier figures from publisher PDFs (PyMuPDF get_drawings).

Axis calibration uses the drawn tick marks and their numeric labels; the KM step line is
the axis-aligned path of the arm colour that starts at (0, 100%); censor marks are the
short vertical segments of the same colour that sit on that line.
"""
import re
import numpy as np
import pymupdf

NUM = re.compile(r"^-?\d+(?:\.\d+)?$")


def same_color(c1, c2, tol=0.02):
    return c1 is not None and c2 is not None and all(abs(a - b) <= tol for a, b in zip(c1, c2))


def is_dark(c):
    return c is not None and max(c) < 0.25


def line_segments(page):
    out = []
    for i, d in enumerate(page.get_drawings()):
        for it in d["items"]:
            if it[0] == "l":
                p1, p2 = it[1], it[2]
                out.append(dict(path=i, color=d.get("color"), width=d.get("width") or 0.0,
                                x1=p1.x, y1=p1.y, x2=p2.x, y2=p2.y))
    return out


def find_axes(page, clip):
    """Main axes = longest dark horizontal segment in clip + longest dark vertical one at its left end."""
    segs = [s for s in line_segments(page) if is_dark(s["color"])
            and clip[0] - 1 <= min(s["x1"], s["x2"]) and max(s["x1"], s["x2"]) <= clip[2] + 1
            and clip[1] - 1 <= min(s["y1"], s["y2"]) and max(s["y1"], s["y2"]) <= clip[3] + 1]
    hor = [s for s in segs if abs(s["y1"] - s["y2"]) < 0.05]
    xa = max(hor, key=lambda s: abs(s["x2"] - s["x1"]))
    x0, x1, ya = min(xa["x1"], xa["x2"]), max(xa["x1"], xa["x2"]), xa["y1"]
    ver = [s for s in segs if abs(s["x1"] - s["x2"]) < 0.05 and abs(s["x1"] - x0) < 1.0]
    yv = max(ver, key=lambda s: abs(s["y2"] - s["y1"]))
    return dict(x0=x0, x1=x1, y_axis_line=ya, yaxis_x=yv["x1"],
                ytop=min(yv["y1"], yv["y2"]), ybot=max(yv["y1"], yv["y2"]), segs=segs)


def calibrate(page, clip, ax, label_band=14.0, y_mode="endpoints", ylabel_min=None):
    """x: least squares over labelled ticks. y: 'endpoints' maps the lowest and highest labelled
    ticks exactly (in NEJM 2024 the 100% tick and the curve start sit 0.2 pt off the 0-90 tick
    spacing; the 2x inset agrees with the endpoint mapping), 'lsq' fits all labelled ticks."""
    words = page.get_text("words", clip=pymupdf.Rect(*clip))
    nums = [(float(w[4]), (w[0] + w[2]) / 2, (w[1] + w[3]) / 2, w[0], w[2]) for w in words if NUM.match(w[4])]
    xt = sorted({round(s["x1"], 2) for s in ax["segs"]
                 if abs(s["x1"] - s["x2"]) < 0.05 and 1.5 < abs(s["y2"] - s["y1"]) < 6
                 and abs(min(s["y1"], s["y2"]) - ax["y_axis_line"]) < 0.3
                 and ax["x0"] - 0.5 <= s["x1"] <= ax["x1"] + 0.5})
    yt = sorted({round(s["y1"], 2) for s in ax["segs"]
                 if abs(s["y1"] - s["y2"]) < 0.05 and 1.5 < abs(s["x2"] - s["x1"]) < 6
                 and abs(max(s["x1"], s["x2"]) - ax["yaxis_x"]) < 0.3
                 and ax["ytop"] - 0.5 <= s["y1"] <= ax["ybot"] + 0.5})
    xl = [n for n in nums if ax["y_axis_line"] < n[2] < ax["y_axis_line"] + label_band]
    yl = [n for n in nums if n[4] < ax["yaxis_x"] and ax["yaxis_x"] - n[4] < 15]
    xpairs, ypairs = [], []
    for t in xt:
        c = min(xl, key=lambda n: abs(n[1] - t), default=None)
        if c is not None and abs(c[1] - t) < 2.5:
            xpairs.append((t, c[0]))
    for t in yt:
        c = min(yl, key=lambda n: abs(n[2] - t), default=None)
        if c is not None and abs(c[2] - t) < 3.0:
            ypairs.append((t, c[0]))
    if ylabel_min is not None:
        ypairs = [p for p in ypairs if p[1] >= ylabel_min]
    fx = np.polyfit([p[0] for p in xpairs], [p[1] for p in xpairs], 1)
    if y_mode == "endpoints":
        lo, hi = min(ypairs, key=lambda p: p[1]), max(ypairs, key=lambda p: p[1])
        fy = np.polyfit([lo[0], hi[0]], [lo[1], hi[1]], 1)
    else:
        fy = np.polyfit([p[0] for p in ypairs], [p[1] for p in ypairs], 1)
    rx = max(abs(np.polyval(fx, p[0]) - p[1]) for p in xpairs)
    ry = max(abs(np.polyval(fy, p[0]) - p[1]) for p in ypairs)
    return dict(fx=fx, fy=fy, xpairs=xpairs, ypairs=ypairs, resid_x=rx, resid_y=ry,
                xticks_labelled=[p for p in xpairs], x_minor=len(xt) - len(xpairs))


def to_data(cal, x, y):
    return float(np.polyval(cal["fx"], x)), float(np.polyval(cal["fy"], y))


def to_px_y(cal, yd):
    a, b = cal["fy"]
    return (yd - b) / a


def to_px_x(cal, xd):
    a, b = cal["fx"]
    return (xd - b) / a


def km_path(page, ax, cal, color, tol_start=1.5):
    """Return list of (x_px, y_px) vertices of the step path that starts at (0, 100%)."""
    x00, y100 = to_px_x(cal, 0.0), to_px_y(cal, 100.0)
    best = None
    for i, d in enumerate(page.get_drawings()):
        if not same_color(d.get("color"), color):
            continue
        its = d["items"]
        if len(its) < 10 or any(it[0] != "l" for it in its):
            continue
        p0 = its[0][1]
        if abs(p0.x - x00) > tol_start or abs(p0.y - y100) > tol_start:
            continue
        # steps are axis-aligned; a few drops are drawn as short diagonals (|dx| < 0.5 pt) when
        # two event times fall within one rendering unit
        axis_aligned = all(abs(it[1].x - it[2].x) < 0.5 or abs(it[1].y - it[2].y) < 0.05 for it in its)
        if not axis_aligned:
            continue
        if best is None or len(its) > len(best[1]):
            best = (i, its, d.get("width"))
    if best is None:
        raise RuntimeError(f"no KM path for colour {color}")
    i, its, w = best
    pts = [(its[0][1].x, its[0][1].y)] + [(it[2].x, it[2].y) for it in its]
    # drop consecutive duplicates
    out = [pts[0]]
    for p in pts[1:]:
        if abs(p[0] - out[-1][0]) > 1e-6 or abs(p[1] - out[-1][1]) > 1e-6:
            out.append(p)
    return i, w, out


def curve_y_at(verts, x):
    """y (px) of the step curve at x (right-continuous: after a drop at x the lower value)."""
    y = verts[0][1]
    for vx, vy in verts:
        if vx <= x + 1e-6:
            y = vy
        else:
            break
    return y


def censor_marks(page, ax, color, verts, km_path_idx, max_gap=2.5):
    xs = []
    xmax = max(v[0] for v in verts)
    for s in line_segments(page):
        if s["path"] == km_path_idx or not same_color(s["color"], color):
            continue
        if abs(s["x1"] - s["x2"]) > 0.05:
            continue
        L = abs(s["y2"] - s["y1"])
        if not (1.5 < L < 6.0):
            continue
        x = s["x1"]
        if x < ax["x0"] - 0.5 or x > xmax + 0.5:
            continue
        ylo, yhi = min(s["y1"], s["y2"]), max(s["y1"], s["y2"])
        # the curve level just before and after x (marks can sit on a drop)
        ys = [curve_y_at(verts, x - 0.01), curve_y_at(verts, x)]
        if any(ylo - max_gap <= yc <= yhi + max_gap for yc in ys):
            xs.append(x)
    return sorted(xs)


def legend_colour(page, clip, ax, label_rx):
    """Colour of the legend sample line drawn just left of a legend label inside the plot,
    or None when the figure labels its curves without sample lines."""
    words = [w for w in page.get_text("words", clip=pymupdf.Rect(*clip))
             if re.search(label_rx, w[4]) and w[3] < ax["y_axis_line"]]
    for w in words:
        yc = (w[1] + w[3]) / 2
        for d in page.get_drawings():
            c, r = d.get("color"), d["rect"]
            if c is None or max(c) - min(c) < 0.2 or len(d["items"]) > 3 or r.width < 5:
                continue
            if abs((r.y0 + r.y1) / 2 - yc) < 3 and 0 <= w[0] - r.x1 < 30:
                return tuple(c)
    return None


def risk_table(page, clip, ax, cal, row_labels, label_dx=4.0):
    """row_labels: dict arm -> regex matching the row label words (joined)."""
    words = [w for w in page.get_text("words", clip=pymupdf.Rect(*clip)) if w[1] > ax["y_axis_line"] + 2]
    tick_x = [(px, lab) for px, lab in cal["xpairs"]]
    out = {}
    for arm, rx in row_labels.items():
        labs = [w for w in words if not NUM.match(w[4]) and re.search(rx, w[4])]
        if len(labs) != 1:
            raise RuntimeError(f"risk-table row label for {arm}: {len(labs)} matches")
        yc = (labs[0][1] + labs[0][3]) / 2
        vals = []
        for w in words:
            if not NUM.match(w[4]) or abs((w[1] + w[3]) / 2 - yc) > 2.5 or w[0] < labs[0][2]:
                continue
            xc = (w[0] + w[2]) / 2
            px, lab = min(tick_x, key=lambda t: abs(t[0] - xc))
            if abs(px - xc) < label_dx:
                vals.append((lab, int(float(w[4]))))
        out[arm] = sorted(vals)
    return out
