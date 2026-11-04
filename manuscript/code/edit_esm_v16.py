"""ESM_1_v16 = ESM_1_v15.docx with the Table S1 (CHEERS) Locations rechecked against the v16 pagination (v16 step 3).
v16 keeps the paragraph counts that the Locations cite (Introduction 4, Outcomes 2, Discussion 7; Implications, now 2
paragraphs, and Limitations are cited as whole sections), so only pages can change. The v15 cells are first rebuilt from
the v15 pagination (edit_esm_v15.locations15) and must match ESM_1_v15 exactly. If no cell changes, the output is a byte
copy of ESM_1_v15.docx; otherwise only the changed cells are rewritten in word/document.xml.
usage: python edit_esm_v16.py <ESM_1_v15.docx> <out.docx> <m15_stats.json> <m16_stats.json> <log.json>
"""
import hashlib, json, os, shutil, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_esm_v12 import NS, q, ptext, cell  # noqa: E402
from edit_esm_v14 import pages14  # noqa: E402
from edit_esm_v15 import locations15  # noqa: E402

ESM15_SHA16 = "1955102cf2c9a793"


def main(src, dst, stats15, stats16, logpath):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == ESM15_SHA16, "ESM v15 sha256 differs"
    S15, S16 = pages14(stats15), pages14(stats16)
    assert len(S16["Introduction"]) == 4 and len(S16["Outcomes"]) == 2 and len(S16["Discussion"]) == 7
    assert len(S15["Implications"]) == 1 and len(S16["Implications"]) == 2 and len(S16["Limitations"]) == 2
    L15, L16 = locations15(S15), locations15(S16)
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    body = doc.find("w:body", NS)
    blocks = list(body)
    i1 = [i for i, b in enumerate(blocks) if b.tag == q("p") and ptext(b).startswith("Supplementary Table S1.")][0]
    i2 = [i for i, b in enumerate(blocks) if b.tag == q("p") and ptext(b).startswith("Supplementary Table S2.")][0]
    cheers = [b for b in blocks[i1:i2] if b.tag == q("tbl")]
    log, seen = [], set()
    for t in cheers:
        for tr in t.findall("w:tr", NS):
            tcs = tr.findall("w:tc", NS)
            if len(tcs) != 4 or not ptext(tcs[1]).strip().isdigit():
                continue
            n = int(ptext(tcs[1]).strip())
            tt = list(tcs[3].iter(q("t")))
            old = tt[0].text
            assert len(tt) == 1 and old == cell(*L15[n]), ("v15 cell differs from the v15 rebuild", n, old)
            tt[0].text = cell(*L16[n])
            seen.add(n)
            log.append({"step": "3", "item": n, "old": old, "new": tt[0].text, "changed": old != tt[0].text})
    assert seen == set(range(1, 29))
    nchg = sum(e["changed"] for e in log)
    if nchg == 0:
        shutil.copyfile(src, dst)
    else:
        head = xml.split(b"?>", 1)[0] + b"?>"
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
            for info in zin.infolist():
                data = zin.read(info.filename)
                if info.filename == "word/document.xml":
                    data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
                zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for e in log:
        if e["changed"]:
            print(e["item"], "|", e["old"][-45:], "=>", e["new"][-45:])
    print("changed:", nchg, "(byte copy of v15)" if nchg == 0 else "")


if __name__ == "__main__":
    main(*sys.argv[1:6])
