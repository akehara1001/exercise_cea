"""WRITING_RULES 1.3: first-appearance order of the bracket citations in the main text (Introduction to Conclusion,
ranges expanded) must be 1, 2, 3, ... without gaps; the citation sequences of v14 (manuscript to References, tables,
ESM) are compared with v13 (checks_v13/citeorder.py with the file names of v13 and v14); every reference 1-78 must be cited in the manuscript, the tables or the ESM.
Uses br_seq() of checks_v11/citemap.py.
usage: python citeorder14.py <v13_dir> <v14_dir>
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "checks_v11"))
from citemap import br_seq, paras, ptxt, BR, expand  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")


def body_seq(path):
    seq, on, npar = [], False, 0
    for p in paras(path):
        t = ptxt(p).strip()
        if t == "Introduction":
            on = True
        if t in ("Acknowledgments", "Statements and Declarations", "References"):
            break
        if on and t:
            npar += 1
            for g in BR.findall(t):
                e = expand(g)
                if max(e) <= 78:
                    seq.append(e)
    return seq, npar


def main(d12, d13):
    m13 = f"{d13}/manuscript_v14_BCRT.docx"
    seq, npar = body_seq(m13)
    first = []
    for e in seq:
        for n in e:
            if n not in first:
                first.append(n)
    print(f"main text: paragraphs {npar}, citation groups {len(seq)}, numbers {sum(len(e) for e in seq)}; "
          f"first-appearance order == 1..{len(first)}: {first == list(range(1, len(first) + 1))}")
    for lab, a, b in (("manuscript (to References)", f"{d12}/manuscript_v13_BCRT.docx", m13),
                      ("tables", f"{d12}/tables_v13_BCRT.docx", f"{d13}/tables_v14_BCRT.docx"),
                      ("ESM", f"{d12}/ESM_1_v13.docx", f"{d13}/ESM_1_v14.docx")):
        sa = br_seq(a, stop="References" if "manuscript" in lab else None)
        sb = br_seq(b, stop="References" if "manuscript" in lab else None)
        print(f"{lab}: v14 citation sequence == v13: {sa == sb} ({len(sb)} groups)")
    cited = set(first)
    for f in (f"{d13}/tables_v14_BCRT.docx", f"{d13}/ESM_1_v14.docx"):
        for e in br_seq(f):
            cited.update(e)
    only_other = sorted(cited - set(first))
    print(f"cited anywhere: {len(cited)} of 78; missing {sorted(set(range(1, 79)) - cited)}; only in tables/ESM {only_other}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
