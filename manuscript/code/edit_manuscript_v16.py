"""v16 = direct edit of manuscript_v15_BCRT.docx by the v16 instruction (2026-11-04): 1c (reference 8: two products of
the injection list differ between 14 October and 1 November 2026, so the date and address stay and the archived copy is
added; body, tables and ESM unchanged), 2a-2b (two sentences split, words as given), 3 (Implications split before
"For payers, the price of a supervised program", text unchanged, same format) and the word count line (--wc A,M).
Only word/document.xml is rewritten; every original string must occur exactly once in v15.
usage: python edit_manuscript_v16.py <v15.docx> <out.docx> <log.json> [--wc ABSTRACT,MAIN]
"""
import copy, hashlib, json, os, re, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_manuscript_v14 import NS, q, ptext, replace_in_para, set_text  # noqa: E402

V15_SHA16 = "42b4edaddd611690"
ARCHIVE = "http://web.archive.org/web/20261015005104/https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_02.xlsx"
CONFIRMED = "4 Nov 2026"
REPL = [
    ("1c ref 8", "https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_02.xlsx. Accessed 22 Oct 2026",
                 "https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_02.xlsx. Accessed 22 Oct 2026. Archived at "
                 + ARCHIVE + ". Accessed " + CONFIRMED),
    ("2a", "It compared the four strategies formed by chemotherapy with or without pembrolizumab and with or without exercise; it "
           "asked how large an effect on recurrence exercise would need to match pembrolizumab, in quality-adjusted life years "
           "(QALYs) and in net benefit; and, as its main aim, it estimated the maximum cost per patient at which exercise added to "
           "chemotherapy with pembrolizumab would be cost-effective, and how this cost depends on the size and duration of the effect "
           "of exercise on recurrence.",
           "It compared the four strategies formed by chemotherapy with or without pembrolizumab and with or without exercise, and "
           "asked how large an effect on recurrence exercise would need to match pembrolizumab, in quality-adjusted life years (QALYs) "
           "and in net benefit. Its main aim was to estimate the maximum cost per patient at which exercise added to chemotherapy with "
           "pembrolizumab would be cost-effective, and how this cost depends on the size and duration of the effect of exercise on "
           "recurrence."),
    ("2b", "Secondary outcomes were the total costs and QALYs of the four arms and the incremental cost-effectiveness ratios (ICERs) "
           "between them at recurrence HRs of 0.95, 0.85 and 0.72; the ICER of pembrolizumab against chemotherapy alone; and the "
           "exercise effect, as a recurrence HR or an increase in pCR, at which exercise added to chemotherapy alone would gain as many "
           "QALYs as pembrolizumab, or the same net monetary benefit, the QALYs gained valued at the threshold minus the incremental "
           "cost.",
           "Secondary outcomes were the total costs and QALYs of the four arms and the incremental cost-effectiveness ratios (ICERs) "
           "between them at recurrence HRs of 0.95, 0.85 and 0.72, and the ICER of pembrolizumab against chemotherapy alone. They also "
           "included the exercise effect, as a recurrence HR or an increase in pCR, at which exercise added to chemotherapy alone would "
           "gain as many QALYs as pembrolizumab, or the same net monetary benefit, the QALYs gained valued at the threshold minus the "
           "incremental cost."),
]
SPLIT_3 = "For payers, the price of a supervised program"


def main(src, dst, logpath, wc=None):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == V15_SHA16, "v15 sha256 differs"
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    body = doc.find("w:body", NS)
    log = []
    paras = lambda: [p for p in body if p.tag == q("p")]

    def find_contains(s):
        hits = [p for p in paras() if s in ptext(p)]
        assert len(hits) == 1 and ptext(hits[0]).count(s) == 1, ("original not found exactly once in v15", s[:80], len(hits))
        return hits[0]

    for step, old, new in REPL:
        p = find_contains(old)
        before = ptext(p)
        replace_in_para(p, old, new)
        log.append({"step": step, "old": old, "new": new, "para_before": before, "para_after": ptext(p)})
    # 3 Implications split
    p = find_contains(SPLIT_3)
    full = ptext(p)
    k = full.find(SPLIT_3)
    assert k > 1 and full[k - 1] == " " and full[k - 2] == "." and full.startswith("Exercise during adjuvant chemotherapy")
    part1, part2 = full[:k - 1], full[k:]
    new = copy.deepcopy(p)
    set_text(p, part1)
    set_text(new, part2)
    p.addnext(new)
    log.append({"step": "3 split", "para_before": full, "para_after": part1})
    log.append({"step": "3 split", "para_before": None, "para_after": part2})
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
