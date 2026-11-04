"""Public-copy run v. the work tree (instruction v14 step 4): the fourarm_*.csv written by R/25_four_arm.R in a copy of
the public directory are compared column by column with those of the work tree (numbers: maximum absolute difference;
text: equality), and the three values of the instruction are read from the copy: the ICER of chemotherapy plus
pembrolizumab plus exercise against chemotherapy plus exercise at a recurrence HR of 0.85 (JPY 1,000 per QALY, half up)
and the hr0 roots of equal net benefit at JPY 5 and 7.5 million per QALY (3 decimals).
usage: python compare_pub14.py <public_copy_root> <work_tree_root>
"""
import csv, os, sys
from decimal import Decimal, ROUND_HALF_UP

sys.stdout.reconfigure(encoding="utf-8")
FILES = ["fourarm_totals.csv", "fourarm_incremental.csv", "fourarm_nmb_equal.csv", "fourarm_checks.csv", "fourarm_unit_tests.csv"]


def rd(p):
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(x):
    try:
        return float(x)
    except ValueError:
        return None


def hu(x, d):
    return f"{Decimal(repr(x)).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP):,.{d}f}"


def main(pub, wt):
    for f in FILES:
        a = rd(os.path.join(pub, "output", "phase2", "main", f)); b = rd(os.path.join(wt, "output", "phase2", "main", f))
        assert len(a) == len(b) and list(a[0]) == list(b[0]), f
        dmax, ntext, nna = 0.0, 0, 0
        for ra, rb in zip(a, b):
            for k in ra:
                if k == "detail":
                    continue
                x, y = num(ra[k]), num(rb[k])
                if x is not None and y is not None:
                    dmax = max(dmax, abs(x - y))
                elif (x is None) != (y is None):
                    nna += 1
                elif ra[k] != rb[k]:
                    ntext += 1
        print(f"{f}: rows {len(a)}, numeric max |diff| {dmax:.3g}, NA mismatches {nna}, text differences {ntext}")
    inc = rd(os.path.join(pub, "output", "phase2", "main", "fourarm_incremental.csv"))
    r = [x for x in inc if x["programme"] == "E02" and abs(float(x["hr0"]) - 0.85) < 1e-9 and x["arm"] == "both"][0]
    ne = rd(os.path.join(pub, "output", "phase2", "main", "fourarm_nmb_equal.csv"))
    root = {(float(x["lambda"]), x["axis"]): float(x["root"]) for x in ne}
    print("public copy: ICER both v. exercise at HR 0.85 =", hu(float(r["icer"]) / 1e3, 0),
          "| NMB-equal hr0 at JPY 5 million =", hu(root[(5e6, "hr0")], 3), "| at JPY 7.5 million =", hu(root[(7.5e6, "hr0")], 3))


if __name__ == "__main__":
    main(*sys.argv[1:3])
