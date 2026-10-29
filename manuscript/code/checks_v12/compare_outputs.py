"""Compares every csv of a public run (output/phase2/main) with the file of the same name in the work tree: same
columns and rows; numeric columns by max |difference| (and relative), other columns by equality (differing
columns listed). Prints the three headline values of the manuscript from both (JPY thousand): the main and
secondary maximum affordable cost at HR 0.85 (lambda 5 million, base column) and the ICER of pembrolizumab.

usage: python compare_outputs.py <public run dir> <work tree output dir>
"""
import csv, math, os, sys
sys.stdout.reconfigure(encoding="utf-8")


def rd(p):
    return list(csv.DictReader(open(p, encoding="utf-8-sig")))


def isnum(v):
    try:
        float(v); return True
    except ValueError:
        return v in ("NA", "")


def fl(v):
    return math.nan if v in ("NA", "") else float(v)


def main(a, b):
    worst = 0.0
    bad = []
    for f in sorted(x for x in os.listdir(a) if x.endswith(".csv")):
        A, B = rd(os.path.join(a, f)), rd(os.path.join(b, f))
        assert A and list(A[0]) == list(B[0]) and len(A) == len(B), f
        num_cols = [c for c in A[0] if all(isnum(r[c]) for r in A + B)]
        txt_cols = [c for c in A[0] if c not in num_cols]
        md = mr = 0.0; nan_mis = 0
        for c in num_cols:
            for x, y in zip(A, B):
                u, v = fl(x[c]), fl(y[c])
                if math.isnan(u) or math.isnan(v):
                    nan_mis += math.isnan(u) != math.isnan(v); continue
                md = max(md, abs(u - v)); mr = max(mr, abs(u - v) / max(1.0, abs(v)))
        tdiff = [c for c in txt_cols if any(x[c] != y[c] for x, y in zip(A, B))]
        worst = max(worst, mr)
        print(f"{f}: rows {len(A)}; numeric cols {len(num_cols)} max|diff| {md:.3g} (rel {mr:.3g}); NA mismatches {nan_mis}; "
              f"text cols {len(txt_cols)} differing {tdiff or 'none'}")
        if nan_mis or mr > 1e-9:
            bad.append(f)
        for c in tdiff:
            ex = [(x[c], y[c]) for x, y in zip(A, B) if x[c] != y[c]]
            print(f"    {c}: {len(ex)} rows differ, e.g. public {ex[0][0]!r} vs work tree {ex[0][1]!r}")
    print("files with numeric differences:", bad or "none", f"(largest relative difference {worst:.3g})")
    for lab, d in (("public run", a), ("work tree", b)):
        C = rd(os.path.join(d, "det_caps.csv")); R = rd(os.path.join(d, "det_reference.csv"))
        cap = lambda comp: [float(r["cap_500"]) for r in C if r["comparison"] == comp and r["column"] == "base"
                            and r["axis"] == "hr0" and abs(float(r["x"]) - 0.85) < 1e-9][0]
        icer = [float(r["icer"]) for r in R if r["column"] == "base"][0]
        print(f"{lab}: main cap HR 0.85 {cap('main') / 1e3:,.1f}; secondary {cap('secondary') / 1e3:,.1f}; ICER {icer / 1e3:,.1f} (JPY thousand)")


if __name__ == "__main__":
    main(*sys.argv[1:3])
