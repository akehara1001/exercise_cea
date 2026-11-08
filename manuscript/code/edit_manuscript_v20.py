"""v20 = direct edit of manuscript_v19_BCRT.docx by the v20 instruction (2026-11-07):
  1   Discussion paragraph 3: "by about 0.14 percentage points" -> "by 0.14 percentage points" (the value is read from
      output/phase2/main/recurrence_reduction.csv and must equal the v19 text)
  4   Word count line of the title page (--wc ABSTRACT,MAIN; Word, checks_v19/word_wc19.py)
Only word/document.xml is rewritten (lxml); each original string must occur exactly once in the body paragraphs of v19.
usage: python edit_manuscript_v20.py <v19.docx> <recurrence_reduction.csv> <out.docx> <log.json> [--wc A,M]
"""
import hashlib, json, os, re, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_manuscript_v14 import NS, q, ptext, replace_in_para  # noqa: E402
from edit_manuscript_v19 import value, CSV_SHA16  # noqa: E402

V19_SHA16 = "c40f9ed6d1796c72"


def main(src, csvpath, dst, logpath, wc=None):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == V19_SHA16, "v19 sha256 differs"
    assert hashlib.sha256(open(csvpath, "rb").read()).hexdigest()[:16] == CSV_SHA16, "recurrence_reduction.csv sha256 differs"
    a = value(csvpath, "chemo_pembro", 0.989, "distant", 84)
    old = "which cut distant recurrence at 7 years by about " + a + " percentage points (Table S12)."
    new = "which cut distant recurrence at 7 years by " + a + " percentage points (Table S12)."
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    body = doc.find("w:body", NS)
    paras = [p for p in body if p.tag == q("p")]
    log = []
    hits = [p for p in paras if old in ptext(p)]
    assert len(hits) == 1, len(hits)
    before = ptext(hits[0]); replace_in_para(hits[0], old, new)
    log.append({"step": "1", "old": old, "new": new, "para_before": before, "para_after": ptext(hits[0])})
    if wc:
        p = [x for x in paras if ptext(x).startswith("Word count: abstract ")]
        assert len(p) == 1
        before = ptext(p[0])
        m = re.match(r"Word count: abstract (\d+); main text ([\d,]+) \(", before)
        assert m and before.endswith("; 3 tables; 3 figures; 1 Online Resource")
        replace_in_para(p[0], m.group(0), "Word count: abstract %d; main text %s (" % (wc[0], f"{wc[1]:,}"))
        log.append({"step": "4 word count", "para_before": before, "para_after": ptext(p[0])})
    head = xml.split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[a] =", a, "| log entries:", len(log), "| wc:", wc)


if __name__ == "__main__":
    args = sys.argv[1:]
    wc = None
    if "--wc" in args:
        i = args.index("--wc"); wc = tuple(int(x) for x in args[i + 1].split(",")); args = args[:i] + args[i + 2:]
    main(args[0], args[1], args[2], args[3], wc)
