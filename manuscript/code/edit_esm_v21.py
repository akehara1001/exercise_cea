"""ESM_1_v21 = direct edit of ESM_1_v20.docx by the v21 instruction (2026-11-07): one change only, the panel A heading of
Supplementary Table S12 "A. Cumulative proportion of women without exercise, %" -> "A. Cumulative recurrence without
exercise, %" (the word of the title and the footnote). Panel B unchanged. The heading must occur in exactly one cell, in
one text run. Only word/document.xml is rewritten.
usage: python edit_esm_v21.py <ESM_1_v20.docx> <out.docx> <log.json>
"""
import hashlib, json, os, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_esm_v12 import NS, q, ptext  # noqa: E402

ESM20_SHA16 = "2da3ba0f52af85df"
OLD = "A. Cumulative proportion of women without exercise, %"
NEW = "A. Cumulative recurrence without exercise, %"


def main(src, dst, logpath):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == ESM20_SHA16, "ESM v20 sha256 differs"
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    hits = [tc for tc in doc.iter(q("tc")) if ptext(tc) == OLD]
    assert len(hits) == 1, len(hits)
    tt = [t for t in hits[0].iter(q("t")) if t.text]
    assert len(tt) == 1 and tt[0].text == OLD
    tt[0].text = NEW
    log = [{"step": "panel A heading", "before": OLD, "after": ptext(hits[0])}]
    head = xml.split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("changed cells:", len(log))


if __name__ == "__main__":
    main(*sys.argv[1:4])
