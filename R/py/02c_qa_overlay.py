"""QA overlays: digitized step vertices drawn back onto the source figure.

Usage: python -I R/py/02c_qa_overlay.py <project_root>
Writes data/digitized/qa/<fig_id>_overlay.png (vector figures rendered at 300 dpi; raster
figures on the native embedded image). Extracted points are drawn in black.
"""
import sys, os, json, csv
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import cv2
import pymupdf

root = sys.argv[1]
dd = os.path.join(root, "data", "digitized")
qa = os.path.join(dd, "qa")
os.makedirs(qa, exist_ok=True)


def read_curve(path, xcol, ycol):
    with open(path, encoding="utf-8") as fh:
        r = csv.DictReader(fh)
        return [(float(row[xcol]), float(row[ycol])) for row in r]


def save(img, path):
    ok, buf = cv2.imencode(".png", img)
    buf.tofile(path)


vs = json.load(open(os.path.join(root, "R", "py", "figspec.json"), encoding="utf-8"))
dpi = 300
for f in vs["figures"]:
    page = pymupdf.open(os.path.join(root, "input", "papers", f["pdf"]))[f["page"] - 1]
    clip = pymupdf.Rect(*f["clip"])
    pix = page.get_pixmap(dpi=dpi, clip=clip)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3][:, :, ::-1].copy()
    sc = dpi / 72.0
    for arm in f["arms"]:
        pts = read_curve(os.path.join(dd, f"{f['fig_id']}_{arm}_curve.csv"), "x_pt", "y_pt")
        P = np.array([[(x - clip.x0) * sc, (y - clip.y0) * sc] for x, y in pts], dtype=np.int32)
        cv2.polylines(img, [P.reshape(-1, 1, 2)], False, (0, 0, 0), 1, cv2.LINE_AA)
        for x, y in P:
            cv2.circle(img, (int(x), int(y)), 2, (0, 0, 0), -1)
    save(img, os.path.join(qa, f"{f['fig_id']}_overlay.png"))
    print("wrote", f"{f['fig_id']}_overlay.png")

rs = json.load(open(os.path.join(root, "R", "py", "rasterspec.json"), encoding="utf-8"))
for f in rs["figures"]:
    path = [p for p in os.listdir(dd) if p.startswith(f"{f['fig_id']}_native.")][0]
    img = cv2.imdecode(np.fromfile(os.path.join(dd, path), dtype=np.uint8), cv2.IMREAD_COLOR)
    x0, y0, x1, y1 = f["panel_px"]
    for k in f["curves"]:
        pts = read_curve(os.path.join(dd, f"{f['fig_id']}_{k}_curve.csv"), "x_px", "y_px")
        P = np.array([[x, y] for x, y in pts], dtype=np.int32)
        cv2.polylines(img, [P.reshape(-1, 1, 2)], False, (0, 0, 0), 1, cv2.LINE_AA)
    save(img[y0:y1, x0:x1], os.path.join(qa, f"{f['fig_id']}_overlay.png"))
    print("wrote", f"{f['fig_id']}_overlay.png")
