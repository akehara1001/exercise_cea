"""Format inventory of a docx (WRITING_RULES section 8): sizes, fonts, colours, bold, spacing, styles."""
import sys, zipfile, re
from collections import Counter, defaultdict
from lxml import etree

sys.stdout.reconfigure(encoding="utf-8")
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def q(t):
    return "{%s}%s" % (W, t)


def eff(rpr, key):
    if rpr is None:
        return None
    return rpr.find("w:" + key, NS)


def main(path):
    z = zipfile.ZipFile(path)
    doc = etree.fromstring(z.read("word/document.xml"))
    styles = etree.fromstring(z.read("word/styles.xml"))
    # default run props
    dd = styles.find(".//w:docDefaults/w:rPrDefault/w:rPr", NS)
    dsz = dd.find("w:sz", NS).get(q("val")) if dd is not None and dd.find("w:sz", NS) is not None else None
    dfont = dd.find("w:rFonts", NS).attrib if dd is not None and dd.find("w:rFonts", NS) is not None else None
    print("docDefaults sz:", dsz, "fonts:", dict(dfont) if dfont else None)
    for st in styles.findall("w:style", NS):
        sid = st.get(q("styleId"))
        rpr = st.find("w:rPr", NS)
        if rpr is not None and (rpr.find("w:sz", NS) is not None or rpr.find("w:rFonts", NS) is not None or rpr.find("w:color", NS) is not None):
            sz = rpr.find("w:sz", NS)
            col = rpr.find("w:color", NS)
            print("style", sid, "sz", sz.get(q("val")) if sz is not None else None, "color", col.get(q("val")) if col is not None else None)
    body = doc.find("w:body", NS)
    paras = body.iter(q("p"))
    sizes = Counter(); fonts = Counter(); colors = Counter(); spacing = Counter(); pstyles = Counter()
    bold_runs = []
    hl = Counter()
    n_runs = 0
    in_table = set(id(p) for t in body.iter(q("tbl")) for p in t.iter(q("p")))
    for i, p in enumerate(body.iter(q("p"))):
        ppr = p.find("w:pPr", NS)
        ps = ppr.find("w:pStyle", NS).get(q("val")) if ppr is not None and ppr.find("w:pStyle", NS) is not None else "Normal"
        pstyles[ps] += 1
        sp = ppr.find("w:spacing", NS) if ppr is not None else None
        line = sp.get(q("line")) if sp is not None else None
        txt = "".join(t.text or "" for t in p.iter(q("t")))
        loc = "T" if id(p) in in_table else "B"
        if txt.strip():
            spacing[(loc, line)] += 1
        for r in p.iter(q("r")):
            rt = "".join(t.text or "" for t in r.iter(q("t")))
            if not rt:
                continue
            n_runs += 1
            rpr = r.find("w:rPr", NS)
            sz = eff(rpr, "sz"); sz = sz.get(q("val")) if sz is not None else "inherit"
            rf = eff(rpr, "rFonts"); rf = rf.get(q("ascii")) if rf is not None else "inherit"
            col = eff(rpr, "color"); col = col.get(q("val")) if col is not None else "none"
            h = eff(rpr, "highlight");
            if h is not None:
                hl[h.get(q("val"))] += 1
            sizes[(loc, sz)] += 1; fonts[(loc, rf)] += 1; colors[(loc, col)] += 1
            b = eff(rpr, "b")
            if b is not None and b.get(q("val"), "1") not in ("0", "false"):
                bold_runs.append((loc, i, rt[:60]))
    print("runs with text:", n_runs)
    print("paragraph styles:", dict(pstyles))
    print("sizes (loc, half-pt):", dict(sizes))
    print("fonts:", dict(fonts))
    print("colors:", dict(colors))
    print("highlight:", dict(hl))
    print("spacing line (nonempty paras):", dict(spacing))
    print("bold runs:", len(bold_runs))
    for b in bold_runs:
        print("   ", b)
    sect = doc.findall(".//w:sectPr", NS)
    for s in sect:
        print("sectPr lnNumType:", s.find("w:lnNumType", NS) is not None, "pgSz:", dict(s.find("w:pgSz", NS).attrib))


if __name__ == "__main__":
    main(sys.argv[1])
