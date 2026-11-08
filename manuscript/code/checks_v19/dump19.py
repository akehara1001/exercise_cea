"""Dump document-order text units (body paragraphs and table-cell paragraphs) of a docx with indices.
usage: python dump19.py <docx> [<out.txt>]
Each line: <index>\t<kind>\t<text>   kind = P (body paragraph) or T<t>.<r>.<c> (table cell paragraph)
"""
import sys
import docx
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding="utf-8")


def units(path):
    d = docx.Document(path)
    out = []
    t = 0
    for el in d.element.body.iterchildren():
        if el.tag == qn("w:p"):
            out.append(("P", "".join(x.text or "" for x in el.iter(qn("w:t")))))
        elif el.tag == qn("w:tbl"):
            t += 1
            for r, tr in enumerate(el.iter(qn("w:tr"))):
                for c, tc in enumerate(tr.findall(qn("w:tc"))):
                    for p in tc.findall(qn("w:p")):
                        out.append((f"T{t}.{r}.{c}", "".join(x.text or "" for x in p.iter(qn("w:t")))))
    return out


if __name__ == "__main__":
    U = units(sys.argv[1])
    lines = [f"{i}\t{k}\t{s}" for i, (k, s) in enumerate(U)]
    if len(sys.argv) > 2:
        open(sys.argv[2], "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print(f"{len(U)} units -> {sys.argv[2]}")
    else:
        print("\n".join(lines))
