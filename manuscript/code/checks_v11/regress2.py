"""Changed units v10 -> v11 with word-level diffs (pairs when a block has equal counts). Markdown output.
usage: python regress2.py <old.docx> <new.docx> <label>
"""
import sys, difflib
sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])
from regress import units

sys.stdout.reconfigure(encoding="utf-8")


def wdiff(a, b):
    A, B = a.split(" "), b.split(" ")
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        out.append(f"「{' '.join(A[i1:i2])}」→「{' '.join(B[j1:j2])}」")
    return "; ".join(out)


def main(a, b, label):
    A, B = units(a), units(b)
    sm = difflib.SequenceMatcher(None, [t for _, t in A], [t for _, t in B], autojunk=False)
    k = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        k += 1
        old, new = A[i1:i2], B[j1:j2]
        if len(old) == len(new):
            for (ka, ta), (kb, tb) in zip(old, new):
                print(f"- [{label} {k}] {ka} unit {i1 + 1}: {wdiff(ta, tb)}")
        else:
            print(f"- [{label} {k}] {op} units {i1 + 1}-{i2} ({len(old)}) -> {j1 + 1}-{j2} ({len(new)}):")
            for _, t in old:
                print(f"    - old: {t}")
            for _, t in new:
                print(f"    - new: {t}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
