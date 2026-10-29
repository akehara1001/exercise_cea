import sys, docx
from docx.document import Document as _D
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

sys.stdout.reconfigure(encoding="utf-8")


def iter_block(parent):
    body = parent.element.body if isinstance(parent, _D) else parent._element
    for child in body.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, parent)
        elif child.tag == qn("w:tbl"):
            yield Table(child, parent)


def main(path, mode="p"):
    d = docx.Document(path)
    i = 0
    for b in iter_block(d):
        if isinstance(b, Paragraph):
            t = b.text
            print(f"[P{i}] ({b.style.name}) {t}")
            i += 1
        else:
            print(f"[TABLE rows={len(b.rows)}]")
            if mode == "t":
                for r, row in enumerate(b.rows):
                    cells = []
                    prev = None
                    for c in row.cells:
                        if prev is not None and c._tc is prev:
                            continue
                        prev = c._tc
                        cells.append(c.text.replace("\n", " / "))
                    print(f"  r{r}: " + " | ".join(cells))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "p")
