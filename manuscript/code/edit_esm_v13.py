"""ESM_1_v13 = ESM_1_v12.docx with the Table S1 page numbers rechecked against the Word pagination of
manuscript_v13_BCRT.docx (instruction step 2). Location texts and paragraph mapping are those of v12
(edit_esm_v12.locations with v12=True). The v12 cells are first rebuilt from the v12 pagination and must match
ESM_1_v12 exactly. If no page changes, the output is a byte copy of ESM_1_v12.docx; otherwise only the changed
cells are rewritten in word/document.xml.

usage: python edit_esm_v13.py <ESM_1_v12.docx> <out.docx> <manuscript_v12_stats.json> <manuscript_v13_stats.json> <log.json>
"""
import hashlib, json, os, shutil, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_esm_v12 import NS, q, ptext, pages, locations, cell  # noqa: E402

ESM12_SHA16 = "ae84d2f68ff5ccac"


def main(src, dst, stats12, stats13, logpath):
    raw = open(src, "rb").read()
    assert hashlib.sha256(raw).hexdigest()[:16] == ESM12_SHA16, "ESM v12 sha256 differs"
    S12, S13 = pages(stats12), pages(stats13)
    for S in (S12, S13):
        assert len(S["Exercise effect and costs"]) == 3
        assert len(S["Introduction"]) == 4 and len(S["Study design"]) == 3 and len(S["Outcomes"]) == 2
        assert len(S["Survival, costs and utilities"]) == 2
        assert len(S["Maximum affordable cost of exercise"]) == 3 and len(S["Duration and metastatic treatment costs"]) == 3
        assert len(S["Pembrolizumab"]) == 2 and len(S["Sensitivity and scenario analyses"]) == 1 and len(S["Discussion"]) == 6
        assert sorted(S["SA_stage"]) == [1, 2, 3, 4, 5, 6]
    L12, L13 = locations(S12, True), locations(S13, True)

    zin = zipfile.ZipFile(src)
    doc = etree.fromstring(zin.read("word/document.xml"))
    body = doc.find("w:body", NS)
    blocks = list(body)
    i_s1 = [i for i, b in enumerate(blocks) if b.tag == q("p") and ptext(b).startswith("Supplementary Table S1.")]
    i_s2 = [i for i, b in enumerate(blocks) if b.tag == q("p") and ptext(b).startswith("Supplementary Table S2.")]
    assert len(i_s1) == 1 and len(i_s2) == 1
    tbls = [b for b in blocks[i_s1[0]:i_s2[0]] if b.tag == q("tbl")]
    log = []
    seen = set()
    for t in tbls:
        for tr in t.findall("w:tr", NS):
            tcs = tr.findall("w:tc", NS)
            if len(tcs) != 4:
                continue
            item = ptext(tcs[1]).strip()
            if not item.isdigit():
                continue
            n = int(item)
            ts = list(tcs[3].iter(q("t")))
            assert len(ts) == 1, n
            old = ts[0].text
            assert old == cell(*L12[n]), ("v12 cell differs from v12 rebuild", n, old, cell(*L12[n]))
            new = cell(*L13[n])
            ts[0].text = new
            seen.add(n)
            log.append({"item": n, "old": old, "new": new, "changed": old != new})
    assert seen == set(range(1, 29)), sorted(seen)
    nchg = sum(e["changed"] for e in log)

    if nchg == 0:
        shutil.copyfile(src, dst)
    else:
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
            for info in zin.infolist():
                data = zin.read(info.filename)
                if info.filename == "word/document.xml":
                    head = data.split(b"?>", 1)[0] + b"?>"
                    data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
                zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for e in log:
        print(e["item"], "*" if e["changed"] else " ", "|", e["new"])
    print("changed:", nchg, "(byte copy of v12)" if nchg == 0 else "")


if __name__ == "__main__":
    main(*sys.argv[1:6])
