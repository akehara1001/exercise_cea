"""WRITING_RULES 1.3: first-appearance order of the bracket citations in the main text (Introduction to Conclusion,
ranges expanded) must be 1, 2, 3, ... without gaps; the citation sequences of v12 (manuscript to References, tables,
ESM) are compared with v11; every reference 1-78 must be cited in the manuscript, the tables or the ESM.
Uses br_seq() of checks_v11/citemap.py.
usage: python citeorder.py <v11_dir> <v12_dir>
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


def main(d11, d12):
    m12 = f"{d12}/manuscript_v12_BCRT.docx"
    seq, npar = body_seq(m12)
    first = []
    for e in seq:
        for n in e:
            if n not in first:
                first.append(n)
    print(f"main text: paragraphs {npar}, citation groups {len(seq)}, numbers {sum(len(e) for e in seq)}; "
          f"first-appearance order == 1..{len(first)}: {first == list(range(1, len(first) + 1))}")
    for lab, a, b in (("manuscript (to References)", f"{d11}/manuscript_v11_BCRT.docx", m12),
                      ("tables", f"{d11}/tables_v11_BCRT.docx", f"{d12}/tables_v12_BCRT.docx"),
                      ("ESM", f"{d11}/ESM_1_v11.docx", f"{d12}/ESM_1_v12.docx")):
        sa = br_seq(a, stop="References" if "manuscript" in lab else None)
        sb = br_seq(b, stop="References" if "manuscript" in lab else None)
        print(f"{lab}: v12 citation sequence == v11: {sa == sb} ({len(sb)} groups)")
    cited = set(first)
    for f in (f"{d12}/tables_v12_BCRT.docx", f"{d12}/ESM_1_v12.docx"):
        for e in br_seq(f):
            cited.update(e)
    only_other = sorted(cited - set(first))
    print(f"cited anywhere: {len(cited)} of 78; missing {sorted(set(range(1, 79)) - cited)}; only in tables/ESM {only_other}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
