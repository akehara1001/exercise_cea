"""ESM_1_v15 = direct edit of ESM_1_v14.docx by the v15 instruction steps 3b-3c. Only word/document.xml is rewritten.
3b Supplementary Table S4 footnote a: HR and pCR removed from the abbreviation list (no longer used in the table; ICER,
   JPY, QALY and UI are still used in the table or in the footnote itself).
3c Table S1 (CHEERS) Location cells: the v14 cells are first rebuilt from the v14 pagination (edit_esm_v14.locations14)
   and must match ESM_1_v14 exactly; the v15 cells use the v15 pagination. Text changes follow the v15 structure only:
   Discussion has 7 paragraphs (one deleted, 1k), so item 26 cites paragraphs 1 to 7; Outcomes keeps 2 paragraphs and
   Limitations (2 paragraphs after 1m) is cited as a whole, so their texts do not change.
usage: python edit_esm_v15.py <ESM_1_v14.docx> <out.docx> <m14_stats.json> <m15_stats.json> <log.json>
"""
import hashlib, json, os, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_esm_v12 import NS, q, ptext, cell  # noqa: E402
from edit_esm_v14 import pages14, locations14  # noqa: E402

ESM14_SHA16 = "02580c221a90f3db"
FOOT_KEY = "Chemotherapy plus pembrolizumab compared with chemotherapy alone. Cells show deterministic estimates"
ABBR_OLD = "HR, hazard ratio; ICER, incremental cost-effectiveness ratio; JPY, Japanese yen; pCR, pathological complete response; QALY, quality-adjusted life year; UI, uncertainty interval."
ABBR_NEW = "ICER, incremental cost-effectiveness ratio; JPY, Japanese yen; QALY, quality-adjusted life year; UI, uncertainty interval."


def locations15(S):
    """locations14 with Discussion paragraphs 1 to 7 in item 26."""
    n = len(S["Discussion"])
    assert n == 7
    S8 = dict(S)
    S8["Discussion"] = S["Discussion"] + [S["Discussion"][-1]]      # only to evaluate the other items with locations14
    L = locations14(S8)
    L[26] = ("Discussion, paragraphs 1 to 7; Discussion, Implications; Discussion, Limitations",
             S["Discussion"] + S["Implications"] + S["Limitations"])
    return L


def main(src, dst, stats14, stats15, logpath):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == ESM14_SHA16, "ESM v14 sha256 differs"
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    body = doc.find("w:body", NS)
    log = []
    # 3b
    hits = [p for p in body.iter(q("p")) if FOOT_KEY in ptext(p)]
    assert len(hits) == 1 and ptext(hits[0]).count(ABBR_OLD) == 1
    ts = [t for t in hits[0].iter(q("t")) if ABBR_OLD in (t.text or "")]
    assert len(ts) == 1
    before = ptext(hits[0])
    ts[0].text = ts[0].text.replace(ABBR_OLD, ABBR_NEW)
    log.append({"step": "3b", "before": before, "after": ptext(hits[0])})
    # 3c
    S14, S15 = pages14(stats14), pages14(stats15)
    assert len(S14["Discussion"]) == 8 and len(S15["Outcomes"]) == 2 and len(S15["Limitations"]) == 2
    L14, L15 = locations14(S14), locations15(S15)
    blocks = list(body)
    i1 = [i for i, b in enumerate(blocks) if b.tag == q("p") and ptext(b).startswith("Supplementary Table S1.")][0]
    i2 = [i for i, b in enumerate(blocks) if b.tag == q("p") and ptext(b).startswith("Supplementary Table S2.")][0]
    cheers = [b for b in blocks[i1:i2] if b.tag == q("tbl")]
    assert len(cheers) == 7
    seen = set()
    for t in cheers:
        for tr in t.findall("w:tr", NS):
            tcs = tr.findall("w:tc", NS)
            if len(tcs) != 4 or not ptext(tcs[1]).strip().isdigit():
                continue
            n = int(ptext(tcs[1]).strip())
            tt = list(tcs[3].iter(q("t")))
            assert len(tt) == 1, n
            old = tt[0].text
            assert old == cell(*L14[n]), ("v14 cell differs from the v14 rebuild", n, old)
            tt[0].text = cell(*L15[n])
            seen.add(n)
            log.append({"step": "3c", "item": n, "old": old, "new": tt[0].text, "changed": old != tt[0].text})
    assert seen == set(range(1, 29))
    head = xml.split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for e in log:
        if e["step"] == "3c" and e["changed"]:
            print(e["item"], "|", e["old"][-45:], "=>", e["new"][-70:])
    print("3b applied; 3c changed:", sum(1 for e in log if e.get("changed")))


if __name__ == "__main__":
    main(*sys.argv[1:6])
