"""v17 = direct edit of manuscript_v16_BCRT.docx by the v17 instruction (2026-11-04): step 2 (i) (reference 8: the oral
drug list of 14 October 2026 exists as a Wayback capture and all five oral prices used equal it, checks_v17/
compare_oral_lists17.py; the oral list and its archived copy are added, text as given in the instruction) and the word
count line (--wc A,M). Body, tables and ESM unchanged. Only word/document.xml is rewritten; the original string must
occur exactly once in v16.
usage: python edit_manuscript_v17.py <v16.docx> <out.docx> <log.json> [--wc ABSTRACT,MAIN]
"""
import hashlib, json, os, re, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_manuscript_v14 import NS, q, ptext, replace_in_para  # noqa: E402

V16_SHA16 = "aa79255fa226e3cf"
ORAL_ARCHIVE = "http://web.archive.org/web/20261014082215/https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_01.xlsx"
REF8_OLD = ("Ministry of Health, Labour and Welfare (2026) National Health Insurance drug price list and information on generic "
            "drugs: injections, products listed as of 14 October 2026 (in Japanese). "
            "https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_02.xlsx. Accessed 22 Oct 2026. Archived at "
            "http://web.archive.org/web/20261015005104/https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_02.xlsx. "
            "Accessed 4 Nov 2026")
REF8_NEW = ("Ministry of Health, Labour and Welfare (2026) National Health Insurance drug price list and information on generic "
            "drugs: oral drugs and injections, products listed as of 14 October 2026 (in Japanese). "
            "https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_01.xlsx and "
            "https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_02.xlsx. Accessed 22 Oct 2026. Archived at "
            + ORAL_ARCHIVE + " and "
            "http://web.archive.org/web/20261015005104/https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_02.xlsx. "
            "Accessed 4 Nov 2026")
REPL = [("2 (i) ref 8", REF8_OLD, REF8_NEW)]


def main(src, dst, logpath, wc=None):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == V16_SHA16, "v16 sha256 differs"
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    body = doc.find("w:body", NS)
    log = []
    paras = lambda: [p for p in body if p.tag == q("p")]

    def find_contains(s):
        hits = [p for p in paras() if s in ptext(p)]
        assert len(hits) == 1 and ptext(hits[0]).count(s) == 1, ("original not found exactly once in v16", s[:80], len(hits))
        return hits[0]

    for step, old, new in REPL:
        p = find_contains(old)
        before = ptext(p)
        assert before == "8. " + old, "reference 8 paragraph is not exactly the v16 text"
        replace_in_para(p, old, new)
        log.append({"step": step, "old": old, "new": new, "para_before": before, "para_after": ptext(p)})
    if wc:
        p = [x for x in paras() if ptext(x).startswith("Word count: abstract ")][0]
        before = ptext(p)
        m = re.match(r"Word count: abstract (\d+); main text ([\d,]+) \(", before)
        assert m and before.endswith("; 3 tables; 3 figures; 1 Online Resource")
        replace_in_para(p, m.group(0), "Word count: abstract %d; main text %s (" % (wc[0], f"{wc[1]:,}"))
        log.append({"step": "word count", "para_before": before, "para_after": ptext(p)})
    head = xml.split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("log entries:", len(log), "| wc", wc)


if __name__ == "__main__":
    a = sys.argv[1:]
    wc = None
    if "--wc" in a:
        i = a.index("--wc"); wc = tuple(int(x) for x in a[i + 1].split(",")); a = a[:i] + a[i + 2:]
    main(a[0], a[1], a[2], wc)
