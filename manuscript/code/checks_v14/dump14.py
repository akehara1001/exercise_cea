"""Dump the body of a docx: top-level paragraphs and tables in order, with indices.
usage: python dump14.py <docx> [maxchars]   (maxchars 0 = full text)
Paragraph lines: P<i> [style] <text>; table lines: T<k> r<row> | cell | cell ..."""
import sys, zipfile
from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def q(t):
    return "{%s}%s" % (W, t)


def ptext(p):
    out = []
    for node in p.iter():
        if node.tag == q("t"):
            out.append(node.text or "")
        elif node.tag == q("tab"):
            out.append("\t")
        elif node.tag == q("br"):
            out.append("\n" if node.get(q("type")) != "page" else "[PAGE]")
    return "".join(out)


def main(path, maxc=160):
    sys.stdout.reconfigure(encoding="utf-8")
    doc = etree.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    body = doc.find("w:body", NS)
    pi = ti = 0
    for el in body:
        if el.tag == q("p"):
            st = el.find("w:pPr/w:pStyle", NS)
            s = ptext(el)
            if maxc and len(s) > maxc:
                s = s[:maxc] + " …"
            sect = " [SECT]" if el.find("w:pPr/w:sectPr", NS) is not None else ""
            print(f"P{pi} [{st.get(q('val')) if st is not None else ''}]{sect} {s}")
            pi += 1
        elif el.tag == q("tbl"):
            for ri, tr in enumerate(el.findall("w:tr", NS)):
                cells = [ptext(tc) for tc in tr.findall("w:tc", NS)]
                if maxc:
                    cells = [c if len(c) <= 60 else c[:60] + "…" for c in cells]
                print(f"T{ti} r{ri} | " + " | ".join(cells))
            ti += 1


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 160)
