"""WRITING_RULES 7.2 / 13: footnote symbols of a table. For each table (title paragraph, table, footnote paragraphs up to
the next title or section break), counts the superscript symbol runs in the title and in the table cells, and the leading
superscript symbol of each footnote paragraph; every symbol must occur on both sides (one footnote per symbol).
usage: python footsym19.py <docx> <title prefix> [<title prefix> ...]
"""
import sys, zipfile
from collections import Counter
from lxml import etree

sys.stdout.reconfigure(encoding="utf-8")
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
q = lambda t: "{%s}%s" % (W, t)


def ptext(e):
    return "".join(t.text or "" for t in e.iter(q("t")))


def sup_runs(e):
    out = []
    for r in e.iter(q("r")):
        va = r.find("w:rPr/w:vertAlign", {"w": W})
        t = "".join(x.text or "" for x in r.findall(q("t")))
        if va is not None and va.get(q("val")) == "superscript" and t:
            out.append(t)
    return out


def main(path, prefixes):
    body = etree.fromstring(zipfile.ZipFile(path).read("word/document.xml")).find(q("body"))
    bl = list(body)
    ok_all = True
    for pre in prefixes:
        i = [k for k, b in enumerate(bl) if b.tag == q("p") and ptext(b).startswith(pre)]
        assert len(i) == 1, pre
        i = i[0]
        title = bl[i]
        j = i + 1
        assert bl[j].tag == q("tbl")
        tbls = []
        while bl[j].tag == q("tbl") or (bl[j].tag == q("p") and not ptext(bl[j]) and j + 1 < len(bl) and bl[j + 1].tag == q("tbl")):
            if bl[j].tag == q("tbl"):
                tbls.append(bl[j])
            j += 1
        j -= 1
        tbl = etree.Element(q("tbl"))
        for t in tbls:
            tbl.append(etree.fromstring(etree.tostring(t)))
        feet = []
        for b in bl[j + 1:]:
            if b.tag != q("p") or b.find("w:pPr/w:sectPr", {"w": W}) is not None:
                break
            t = ptext(b)
            if t.startswith(("Table ", "Supplementary ")):
                break
            if t:
                feet.append(b)
        in_title = Counter(sup_runs(title)); in_tbl = Counter(sup_runs(tbl))
        lead = []
        for f in feet:
            s = sup_runs(f)
            first_run = [r for r in f.iter(q("r")) if "".join(x.text or "" for x in r.findall(q("t")))][0]
            lead.append("".join(x.text or "" for x in first_run.findall(q("t"))) if s and s[0] == "".join(x.text or "" for x in first_run.findall(q("t"))) else None)
        used = set(in_title) | set(in_tbl)
        ok = None not in lead and set(lead) == used and len(lead) == len(set(lead))
        ok_all &= ok
        print(f"{pre[:40]:40s} | tables {len(tbls)} | title {dict(in_title)} | table {dict(in_tbl)} | footnotes {lead} | one-to-one: {ok}")
    print("ALL ONE-TO-ONE:", ok_all)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
