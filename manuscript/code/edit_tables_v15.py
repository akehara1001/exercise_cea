"""tables_v15 = direct edit of tables_v14_BCRT.docx by the v15 instruction step 3a: one sentence added to Table 2 footnote a
after "Strategies are listed in order of total cost." Only word/document.xml is rewritten; the match must lie in one run.
usage: python edit_tables_v15.py <tables_v14.docx> <out.docx> <log.json>
"""
import hashlib, json, sys, zipfile
from lxml import etree

T14_SHA16 = "ea0fe2b460c13244"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
OLD = "Strategies are listed in order of total cost."
NEW = "Strategies are listed in order of total cost. A dash marks the cheapest strategy, which has no comparator."


def ptext(el):
    return "".join(t.text or "" for t in el.iter("{%s}t" % W))


def main(src, dst, logpath):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == T14_SHA16, "tables v14 sha256 differs"
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    hits = [p for p in doc.iter("{%s}p" % W) if OLD in ptext(p)]
    assert len(hits) == 1 and ptext(hits[0]).count(OLD) == 1 and ptext(hits[0]).startswith("aModeled cohort")
    before = ptext(hits[0])
    ts = [t for t in hits[0].iter("{%s}t" % W) if OLD in (t.text or "")]
    assert len(ts) == 1
    ts[0].text = ts[0].text.replace(OLD, NEW)
    log = [{"step": "3a", "before": before, "after": ptext(hits[0])}]
    assert log[0]["after"] == before.replace(OLD, NEW)
    head = xml.split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("3a applied")


if __name__ == "__main__":
    main(*sys.argv[1:4])
