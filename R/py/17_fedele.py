"""Fedele et al. Breast Cancer Res Treat 2026;218:8 (DOI 10.1007/s10549-026-08023-2): recurrence after
neoadjuvant chemo-immunotherapy for TNBC (Italian multicentre, retrospective). Values for the round-14
scenario "early-DR k (external)" (docs/acceptance_rule_round14.md), read by regex from
input/papers/Fedele2026_BCRT.pdf (placed by the user, 2026-10-23), with the printed page.

Usage: .venv/Scripts/python.exe -I R/py/17_fedele.py <project_root>
Writes data/fedele2026.csv (id, value, page, quote).
"""
import sys, os, re, csv
sys.stdout.reconfigure(encoding="utf-8")
import pymupdf as fitz

root = sys.argv[1]
pages = []
for pg in fitz.open(os.path.join(root, "input", "papers", "Fedele2026_BCRT.pdf")):
    t = pg.get_text().replace("­\n", "").replace("­", "")
    pages.append(re.sub(r"\s+", " ", t))
F = r"([\d.]+)"
rows = []


def get(rx, ids, where="body"):
    hits = [(i, m) for i, t in enumerate(pages) for m in [re.search(rx, t)] if m]
    if not hits:
        raise SystemExit(f"not found: {rx}")
    i, m = hits[0] if where == "body" else hits[0]
    printed = re.search(r"Page (\d) of 9", pages[i])
    page = printed.group(1) if printed else str(i + 1)
    for vid, g in ids:
        rows.append(dict(id=vid, value=m.group(g), page=page, quote=m.group(0)))


get(r"metastatic recur ?rence was documented in " + F + r" of " + F + r" patients", [("n_recurrence", 1), ("n_cohort", 2)])
get(r"After a median follow-up of " + F + r" months, metastatic recur", [("followup_median_months", 1)])
get(r"Among the " + F + r" patients with metastatic recurrence, " + F + r" were evaluable", [("n_recurrence_check", 1), ("n_evaluable", 2)])
get(r"attrition occurred in " + F + r" patients \(([\d.]+)%\), while " + F + r" patients \(([\d.]+)%\) initiated systemic therapy",
    [("n_attrition", 1), ("pct_attrition", 2), ("n_no_attrition", 3), ("pct_no_attrition", 4)])
get(r"shorter disease- ?free interval compared with those who initiated treatment \(median " + F + r" vs\. " + F + r" months",
    [("dfi_median_attrition_months", 1), ("dfi_median_no_attrition_months", 2)])
get(r"within 90 days \(" + F + r" vs\. " + F + r" months, respectively\)", [("os_median_attrition_months", 1), ("os_median_no_attrition_months", 2)])
get(r"Median overall survival from metastatic recurrence was " + F + r" months in the attrition group compared with " + F + r" months",
    [("os_median_attrition_months_abstract", 1), ("os_median_no_attrition_months_abstract", 2)])
v = {r["id"]: float(r["value"]) for r in rows}
assert v["n_recurrence"] == v["n_recurrence_check"]
assert v["n_attrition"] + v["n_no_attrition"] == v["n_evaluable"]
assert abs(100 * v["n_attrition"] / v["n_evaluable"] - v["pct_attrition"]) < 0.051
assert v["os_median_attrition_months"] == v["os_median_attrition_months_abstract"]
assert v["os_median_no_attrition_months"] == v["os_median_no_attrition_months_abstract"]
out = os.path.join(root, "data", "fedele2026.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["id", "value", "page", "quote"])
    w.writeheader(); w.writerows(rows)
for r in rows:
    print(r["id"], r["value"], "p." + r["page"])
