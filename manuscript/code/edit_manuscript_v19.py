"""v19 = direct edit of manuscript_v18_BCRT.docx (Dr Ozaki's revision of v17) by the v19 instruction (2026-11-07):
  2     Methods, Study design: "Tables S1–S11" -> "Tables S1–S12" (new Supplementary Table S12)
  4(1)  Results, Exercise compared with pembrolizumab, first sentence: citation of Table S4 restored (text as given)
  4(2)  Discussion paragraph 3: two sentences replaced (text as given; [a] = 7-year distant recurrence reduction at HR
        0.989 with chemotherapy plus pembrolizumab, read from output/phase2/main/recurrence_reduction.csv, 2 decimals)
  4(3)  Discussion paragraph 1: "(Table 2)" -> "(Tables 2 and 3)"
  4(4)  Methods, programs: "because its about 50 sessions" -> "because its roughly 50 sessions"
  4(5)  word-count offsets a and b in this order (--trim N applies the first N), and the Word count line of the title
        page (--wc ABSTRACT,MAIN; measured with Word, checks_v19/word_wc19.py)
Only word/document.xml is rewritten (lxml; the root keeps its namespace declarations); every other part is copied byte
for byte. Each original string must occur exactly once in the body paragraphs of v18, or the script stops.
usage: python edit_manuscript_v19.py <v18.docx> <recurrence_reduction.csv> <out.docx> <log.json> [--trim N] [--wc A,M]
"""
import csv, hashlib, json, os, re, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_manuscript_v14 import NS, q, ptext, replace_in_para  # noqa: E402

V18_SHA16 = "d26656694a8712192a47501d2fd6c0276f59915530ffb011d4fb2083d6ec93cc"[:16]
CSV_SHA16 = "867c0eba389ab175d30dd0a6bf8dc9e03f41c873274083773dfdb29e8086c047"[:16]


def value(csvpath, group, hr, outcome, month):
    rows = [r for r in csv.DictReader(open(csvpath, encoding="utf-8"))
            if r["group"] == group and abs(float(r["hr"]) - hr) < 1e-9 and r["outcome"] == outcome and int(r["month"]) == month]
    assert len(rows) == 1, (group, hr, outcome, month)
    return "%.2f" % float(rows[0]["diff_pp_2dp"])


def edits(a):
    return [
        ("2", "Supplementary Methods S1, Tables S1–S11 (including the CHEERS checklist in Table S1)",
         "Supplementary Methods S1, Tables S1–S12 (including the CHEERS checklist in Table S1)"),
        ("4(1)", "Table 2 also shows pembrolizumab against chemotherapy alone: it cost JPY 4,426 thousand more per patient and "
                 "added 2.156 QALYs, an ICER of JPY 2,053 thousand per QALY.",
         "Table 2 also shows pembrolizumab against chemotherapy alone: it cost JPY 4,426 thousand more per patient and "
         "added 2.156 QALYs, an ICER of JPY 2,053 thousand per QALY (Table S4)."),
        ("4(2)", "If exercise reduces recurrence at all, even a small effect would make a structured program cost-effective: "
                 "the fee-schedule-based program became cost-effective once it lowered the recurrence hazard by 1.1%. How much a "
                 "program could cost depended mostly on how large its effect was and how long it lasted.",
         "If exercise reduces recurrence at all, even a small effect would make a structured program cost-effective: the "
         "fee-schedule-based program became cost-effective once it lowered the recurrence hazard by 1.1%, which cut distant "
         "recurrence at 7 years by about " + a + " percentage points (Table S12). What a program could cost depended on the "
         "size and duration of its effect."),
        ("4(3)", "both strategies without it were dominated (Table 2), so the choice in Japan",
         "both strategies without it were dominated (Tables 2 and 3), so the choice in Japan"),
        ("4(4)", "because its about 50 sessions over 3 years", "because its roughly 50 sessions over 3 years"),
    ]


TRIMS = [
    ("4(5)a", "The effect of pembrolizumab is established and that of exercise is not, so the comparison shows what a cheap "
              "program could be worth if its effect were confirmed.",
     "Because the effect of exercise is unproven, the comparison shows what a cheap program could be worth if it were "
     "confirmed."),
    ("4(5)b", "The analysis plan was written before any economic computation, and each later addition before the computation "
              "it added; the plan was not registered.",
     "The analysis plan, and each later addition, was written before the corresponding computation; the plan was not "
     "registered."),
]


def main(src, csvpath, dst, logpath, trim=0, wc=None):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == V18_SHA16, "v18 sha256 differs"
    assert hashlib.sha256(open(csvpath, "rb").read()).hexdigest()[:16] == CSV_SHA16, "recurrence_reduction.csv sha256 differs"
    a = value(csvpath, "chemo_pembro", 0.989, "distant", 84)
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    body = doc.find("w:body", NS)
    paras = lambda: [p for p in body if p.tag == q("p")]
    log = []

    def find_contains(s):
        hits = [p for p in paras() if s in ptext(p)]
        assert len(hits) == 1 and ptext(hits[0]).count(s) == 1, ("original not found exactly once in v18", s[:80], len(hits))
        return hits[0]

    for step, old, new in edits(a) + TRIMS[:trim]:
        p = find_contains(old)
        before = ptext(p)
        replace_in_para(p, old, new)
        log.append({"step": step, "old": old, "new": new, "para_before": before, "para_after": ptext(p)})
    if wc:
        p = [x for x in paras() if ptext(x).startswith("Word count: abstract ")]
        assert len(p) == 1
        p = p[0]
        before = ptext(p)
        m = re.match(r"Word count: abstract (\d+); main text ([\d,]+) \(", before)
        assert m and before.endswith("; 3 tables; 3 figures; 1 Online Resource")
        replace_in_para(p, m.group(0), "Word count: abstract %d; main text %s (" % (wc[0], f"{wc[1]:,}"))
        log.append({"step": "4(5) word count", "para_before": before, "para_after": ptext(p)})
    head = xml.split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[a] =", a, "| log entries:", len(log), "| trims:", trim, "| wc:", wc)


if __name__ == "__main__":
    args = sys.argv[1:]
    trim, wc = 0, None
    if "--trim" in args:
        i = args.index("--trim"); trim = int(args[i + 1]); args = args[:i] + args[i + 2:]
    if "--wc" in args:
        i = args.index("--wc"); wc = tuple(int(x) for x in args[i + 1].split(",")); args = args[:i] + args[i + 2:]
    main(args[0], args[1], args[2], args[3], trim, wc)
