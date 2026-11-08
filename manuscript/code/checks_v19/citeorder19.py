"""WRITING_RULES 1.3: first-appearance order of the bracket citations in the main text (Introduction to Conclusion,
ranges expanded) must be 1, 2, 3, ... without gaps; the citation sequences of v19 (manuscript to References, tables,
ESM) are compared with v18; every reference 1-78 must be cited in the manuscript, the tables or the ESM.
= checks_v17/citeorder17.py with the v18/v19 file names (body_seq stops at References; v18 has no Acknowledgments).
usage: python citeorder19.py <v18_dir> <v19_dir>
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "checks_v11"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "checks_v17"))
from citemap import br_seq  # noqa: E402
from citeorder17 import body_seq  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")


def main(d18, d19):
    m19 = f"{d19}/manuscript_v19_BCRT.docx"
    seq, npar = body_seq(m19)
    first = []
    for e in seq:
        for n in e:
            if n not in first:
                first.append(n)
    print(f"main text: paragraphs {npar}, citation groups {len(seq)}, numbers {sum(len(e) for e in seq)}; "
          f"first-appearance order == 1..{len(first)}: {first == list(range(1, len(first) + 1))}")
    for lab, a, b in (("manuscript (to References)", f"{d18}/manuscript_v18_BCRT.docx", m19),
                      ("tables", f"{d18}/tables_v18_BCRT.docx", f"{d19}/tables_v19_BCRT.docx"),
                      ("ESM", f"{d18}/ESM_1_v18.docx", f"{d19}/ESM_1_v19.docx")):
        sa = br_seq(a, stop="References" if "manuscript" in lab else None)
        sb = br_seq(b, stop="References" if "manuscript" in lab else None)
        print(f"{lab}: v19 citation sequence == v18: {sa == sb} ({len(sb)} groups)")
    cited = set(first)
    for f in (f"{d19}/tables_v19_BCRT.docx", f"{d19}/ESM_1_v19.docx"):
        for e in br_seq(f):
            cited.update(e)
    only_other = sorted(cited - set(first))
    print(f"cited anywhere: {len(cited)} of 78; missing {sorted(set(range(1, 79)) - cited)}; only in tables/ESM {only_other}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
