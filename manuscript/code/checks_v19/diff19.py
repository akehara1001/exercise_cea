"""Paragraph-level diff of two docx files (document-order text units incl. table cells).
usage: python diff19.py <old.docx> <new.docx> [labelA labelB]
Prints every non-equal block with old/new text; summary counts first.
"""
import sys, difflib
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
from dump19 import units

sys.stdout.reconfigure(encoding="utf-8")


def main(a, b, la="A", lb="B"):
    A = [s for k, s in units(a)]
    B = [s for k, s in units(b)]
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    ops = sm.get_opcodes()
    same = sum(i2 - i1 for op, i1, i2, j1, j2 in ops if op == "equal")
    blocks = [o for o in ops if o[0] != "equal"]
    print(f"units {la} {len(A)}, {lb} {len(B)}, unchanged {same}, changed blocks {len(blocks)}")
    for n, (op, i1, i2, j1, j2) in enumerate(blocks, 1):
        print(f"\n=== block {n}: {op} {la}[{i1}:{i2}] -> {lb}[{j1}:{j2}]")
        for i in range(i1, i2):
            print(f"  - [{i}] {A[i]}")
        for j in range(j1, j2):
            print(f"  + [{j}] {B[j]}")


if __name__ == "__main__":
    main(*sys.argv[1:])
