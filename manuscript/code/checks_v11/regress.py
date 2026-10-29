"""Paragraph-level regression check v10 -> v11 (body paragraphs and table cells, in document order) and the numbers
that differ. Prints every changed paragraph with a short diff.
usage: python regress.py <old.docx> <new.docx> <label>
"""
import re, sys, difflib
import docx
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding="utf-8")
NUM = re.compile(r"[−-]?\d[\d,]*(?:\.\d+)?")


def units(path):
    """document-order list of text units: body paragraphs and table-cell paragraphs (tagged)."""
    d = docx.Document(path)
    out = []
    for el in d.element.body.iterchildren():
        if el.tag == qn("w:p"):
            out.append(("P", "".join(x.text or "" for x in el.iter(qn("w:t")))))
        elif el.tag == qn("w:tbl"):
            for tr in el.iter(qn("w:tr")):
                for tc in tr.findall(qn("w:tc")):
                    for p in tc.findall(qn("w:p")):
                        out.append(("C", "".join(x.text or "" for x in p.iter(qn("w:t")))))
    return out


def nums(t):
    return [m.group(0).rstrip(",") for m in NUM.finditer(t)]


def main(a, b, label):
    A, B = units(a), units(b)
    sm = difflib.SequenceMatcher(None, [t for _, t in A], [t for _, t in B], autojunk=False)
    changed = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        changed.append((op, A[i1:i2], B[j1:j2]))
    print(f"{label}: units v10 {len(A)}, v11 {len(B)}, unchanged {sum(i2 - i1 for op, i1, i2, j1, j2 in sm.get_opcodes() if op == 'equal')}, changed blocks {len(changed)}")
    allA = [n for _, t in A for n in nums(t)]
    allB = [n for _, t in B for n in nums(t)]
    from collections import Counter
    ca, cb = Counter(allA), Counter(allB)
    print(f"  numbers: v10 {len(allA)}, v11 {len(allB)}; only in v10 {dict(ca - cb)}; only in v11 {dict(cb - ca)}")
    for k, (op, old, new) in enumerate(changed, 1):
        print(f"  [{k}] {op}: {len(old)} -> {len(new)} units")
        for _, t in old:
            print("     - " + t[:220])
        for _, t in new:
            print("     + " + t[:220])


if __name__ == "__main__":
    main(*sys.argv[1:4])
