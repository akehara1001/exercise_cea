"""Instruction v13 step 3, consistency: the csv outputs of det, plan9_det and plan10 of a run of the public directory
against the work tree (checks_v12/compare_outputs.py: same columns and rows, numeric max |difference|, text columns),
then the values the v13 manuscript and tables print, taken from the public run and from the work tree, rounded as
printed and compared with the printed strings: the maximum affordable costs at HR 0.85 (main, secondary, Japanese
utility scenario), the ICER of pembrolizumab, the break-even HRs of Table 2 (panels A and C) and of the Results text,
the range over the utility scenarios and S-JP (Table S10), and the QALY-matching HR and pCR increase of Table 3.

usage: python compare_v13.py <public run output dir> <work tree output dir>
"""
import csv, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "checks_v12"))
from compare_outputs import main as compare_all  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")


def rd(d, f):
    return list(csv.DictReader(open(os.path.join(d, f), encoding="utf-8-sig")))


def cap(d, f, comp, scen=None):
    R = [r for r in rd(d, f) if r["comparison"] == comp and r["column"] == "base" and r["axis"] == "hr0"
         and abs(float(r["x"]) - 0.85) < 1e-9 and (scen is None or r.get("scenario") == scen)]
    assert len(R) == 1, (f, comp, scen, len(R))
    return float(R[0]["cap_500"])


def cross(d, f, comp, typ, prog, scen=None):
    R = [r for r in rd(d, f) if r["comparison"] == comp and r["column"] == "base" and r["type"] == typ
         and r["programme"] == prog and (r["lambda"] == "NA" if typ == "avoided_eq_programme" else float(r["lambda"]) == 5e6)
         and (scen is None or r["scenario"] == scen)]
    assert len(R) == 1, (f, comp, typ, prog, scen, len(R))
    return float(R[0]["hr0"])


def values(d):
    V = {}
    V["cap main HR 0.85 (JPY 1,000)"] = (f"{cap(d, 'det_caps.csv', 'main') / 1e3:,.0f}", "2,726")
    V["cap secondary HR 0.85"] = (f"{cap(d, 'det_caps.csv', 'secondary') / 1e3:,.0f}", "3,443")
    V["cap main HR 0.85, Japanese utilities (plan10)"] = (f"{cap(d, 'sc_util_jp_det_caps.csv', 'main', 'utility_jp') / 1e3:,.0f}", "2,733")
    icer = [float(r["icer"]) for r in rd(d, "det_reference.csv") if r["column"] == "base"]
    assert len(icer) == 1
    V["ICER pembrolizumab (JPY 1,000 per QALY)"] = (f"{icer[0] / 1e3:,.0f}", "2,053")
    T2 = [("main", "cap_eq_programme", "E02", "0.989"), ("secondary", "cap_eq_programme", "E02", "0.991"),
          ("main", "avoided_eq_programme", "E01", "0.948"), ("secondary", "avoided_eq_programme", "E01", "0.958"),
          ("main", "avoided_eq_programme", "E02", "0.958"), ("secondary", "avoided_eq_programme", "E02", "0.966"),
          ("main", "avoided_eq_programme", "E03", "0.997"), ("secondary", "avoided_eq_programme", "E03", "0.998")]
    for comp, typ, prog, txt in T2:
        V[f"Table 2A {comp} {typ} {prog}"] = (f"{cross(d, 'sc_base_crossings.csv', comp, typ, prog):.3f}", txt)
    T2C = [("sc_metcost50", "main", "cap_eq_programme", "0.988"), ("sc_metcost50", "secondary", "cap_eq_programme", "0.990"),
           ("sc_metcost50", "main", "avoided_eq_programme", "0.918"), ("sc_metcost50", "secondary", "avoided_eq_programme", "0.934"),
           ("sc_eribulin", "main", "cap_eq_programme", "0.987"), ("sc_eribulin", "secondary", "cap_eq_programme", "0.990"),
           ("sc_eribulin", "main", "avoided_eq_programme", "0.914"), ("sc_eribulin", "secondary", "avoided_eq_programme", "0.925")]
    for s, comp, typ, txt in T2C:
        V[f"Table 2C {s} {comp} {typ} E02"] = (f"{cross(d, s + '_crossings.csv', comp, typ, 'E02'):.3f}", txt)
    sc = ["utility_jp", "utility_us", "utility_uk", "utility_au", "sjp"]
    h = [cross(d, "sc_crossings.csv", "main", "cap_eq_programme", "E02", s) for s in sc]
    V["Results: utility scenarios and S-JP, cap = fee-schedule program (main), range (plan10)"] = (
        f"{min(h):.3f} to {max(h):.3f}", "0.988 to 0.989")
    hb = cross(d, "sc_crossings.csv", "main", "cap_eq_programme", "E02", "base")
    V["plan10 base row = sc_base_crossings (main, cap, E02)"] = (f"{hb:.3f}", "0.989")
    Y = {r["axis"]: float(r["root"]) for r in rd(d, "det_yardstick.csv")}
    V["Table 3C recurrence HR matching pembrolizumab QALYs"] = (f"{Y['hr0']:.3f}", "0.425")
    V["Table 3C pCR increase (percentage points)"] = (f"{100 * Y['pcr']:.1f}", "35.9")
    return V


def main(pub, work):
    compare_all(pub, work)
    VP, VW = values(pub), values(work)
    print("\nvalue | public run | work tree | v13 text | all equal")
    bad = 0
    for k in VP:
        ok = VP[k][0] == VW[k][0] == VP[k][1]
        bad += not ok
        print(f"{k} | {VP[k][0]} | {VW[k][0]} | {VP[k][1]} | {ok}")
    print(f"values checked {len(VP)}; not equal {bad}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
