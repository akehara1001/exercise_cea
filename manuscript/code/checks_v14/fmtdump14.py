"""Formatting dump of a docx body: per top-level paragraph and per table cell, the runs with flags
(b = bold, ^ = superscript, i = italic), paragraph properties and, for cells, gridSpan / vMerge / width.
usage: python fmtdump14.py <docx> [first_block] [last_block]"""
import sys, zipfile
from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def q(t):
    return "{%s}%s" % (W, t)


def runs(p):
    out = []
    for r in p.findall(".//w:r", NS):
        t = "".join(x.text or "" for x in r.findall("w:t", NS))
        if not t:
            continue
        rpr = r.find("w:rPr", NS)
        fl = ""
        if rpr is not None:
            b = rpr.find("w:b", NS)
            if b is not None and b.get(q("val")) not in ("0", "false"):
                fl += "b"
            va = rpr.find("w:vertAlign", NS)
            if va is not None and va.get(q("val")) == "superscript":
                fl += "^"
            if rpr.find("w:i", NS) is not None:
                fl += "i"
        out.append(f"{{{fl}}}{t}" if fl else t)
    return "".join(out)


def ppr(p):
    pp = p.find("w:pPr", NS)
    return "" if pp is None else etree.tostring(pp, encoding="unicode").replace(f'xmlns:w="{W}"', "")[:300]


def main(path, a=0, b=10 ** 9):
    sys.stdout.reconfigure(encoding="utf-8")
    body = etree.fromstring(zipfile.ZipFile(path).read("word/document.xml")).find("w:body", NS)
    for k, el in enumerate(body):
        if k < a or k > b:
            continue
        if el.tag == q("p"):
            print(f"[{k}] P {runs(el)!r}  PPR {ppr(el)}")
        elif el.tag == q("tbl"):
            tp = el.find("w:tblPr", NS)
            print(f"[{k}] TBL tblPr {etree.tostring(tp, encoding='unicode').replace(f'xmlns:w=\"{W}\"', '')[:400]}")
            g = el.find("w:tblGrid", NS)
            print("   grid", [c.get(q("w")) for c in g.findall("w:gridCol", NS)])
            for ri, tr in enumerate(el.findall("w:tr", NS)):
                cells = []
                for tc in tr.findall("w:tc", NS):
                    tcp = tc.find("w:tcPr", NS)
                    gs = tcp.find("w:gridSpan", NS) if tcp is not None else None
                    tw = tcp.find("w:tcW", NS) if tcp is not None else None
                    sp = f"<span{gs.get(q('val'))}>" if gs is not None else ""
                    w_ = f"<w{tw.get(q('w'))}>" if tw is not None else ""
                    ps = tc.findall("w:p", NS)
                    cells.append(sp + w_ + " / ".join(runs(p) for p in ps))
                trp = tr.find("w:trPr", NS)
                print(f"   r{ri}{' trPr' if trp is not None else ''} | " + " | ".join(cells))
        elif el.tag == q("sectPr"):
            print(f"[{k}] body sectPr {etree.tostring(el, encoding='unicode').replace(f'xmlns:w=\"{W}\"', '')[:400]}")


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args[0], *(int(x) for x in args[1:3]))
