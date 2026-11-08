"""cover_letter_v19 = direct edit of cover_letter_v18_BCRT.docx (= v17, byte copy) by the v19 instruction step 5:
  - the title in the first paragraph of the letter body -> the new title (v18 title page);
  - the summary paragraph reordered to the three questions of v18 (four strategies -> exercise against pembrolizumab ->
    exercise added to pembrolizumab). Its first sentence (background) is kept; the findings are stated as in the v18
    abstract and Discussion: dominance at a 5% or larger reduction (abstract Results, Discussion paragraph 1);
    pembrolizumab cost-effective in Japan (Discussion paragraph 1) and the HR of 0.722 to match its net benefit (abstract
    Results); 1.1% for the fee-schedule-based program (abstract Results, Discussion paragraph 3); size and duration far
    more than price (abstract Conclusion). The statement that duration mattered more than any cost input was removed
    from the v18 abstract by Dr Ozaki, so the summary follows the abstract Conclusion instead.
Other paragraphs unchanged. Only word/document.xml is rewritten.
usage: python edit_cover_v19.py <cover_letter_v18.docx> <out.docx> <log.json>
"""
import hashlib, json, os, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_manuscript_v14 import NS, q, ptext, replace_in_para, set_text  # noqa: E402

CL18_SHA16 = "21ed7f1aa387e8b7"
OLD_TITLE = "Cost-effectiveness of exercise added to neoadjuvant chemotherapy for triple-negative breast cancer in Japan"
NEW_TITLE = ("Exercise versus or in addition to pembrolizumab with neoadjuvant chemotherapy for early-stage triple-negative "
             "breast cancer: a model-based cost-effectiveness analysis in Japan")
SUM_OLD = ("Structured exercise prolonged disease-free survival after adjuvant chemotherapy for colon cancer in the CHALLENGE "
           "trial, but whether exercise during neoadjuvant chemotherapy for breast cancer reduces recurrence is unknown. Using a "
           "model based on KEYNOTE-522 and Japanese prices, we estimated the maximum cost at which an exercise program added to "
           "neoadjuvant chemotherapy for stage II or III triple-negative breast cancer would be cost-effective for each possible "
           "effect on recurrence. With chemotherapy plus pembrolizumab, a program priced from the Japanese fee schedule would be "
           "cost-effective if it lowered the recurrence hazard by 1.1%, and the duration of the effect mattered more than any "
           "cost input. Exercise could not substitute for pembrolizumab, whose cost-effectiveness in Japan we also report.")
SUM_NEW = ("Structured exercise prolonged disease-free survival after adjuvant chemotherapy for colon cancer in the CHALLENGE "
           "trial, but whether exercise during neoadjuvant chemotherapy for breast cancer reduces recurrence is unknown. Using a "
           "model based on KEYNOTE-522 and Japanese prices, we compared chemotherapy with or without pembrolizumab, each with or "
           "without exercise, for stage II or III triple-negative breast cancer. If exercise lowered the recurrence hazard by 5% "
           "or more, both strategies without it were dominated. Pembrolizumab was cost-effective in Japan, and exercise could "
           "not match the health it gained; exercise would need a recurrence hazard ratio of 0.722 to match its net benefit. "
           "Added to chemotherapy plus pembrolizumab, a program priced from the Japanese fee schedule would be cost-effective if "
           "it lowered the recurrence hazard by 1.1%. Its value depended on the size and duration of that effect far more than "
           "on its price.")


def main(src, dst, logpath):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == CL18_SHA16, "cover letter v18 sha256 differs"
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    body = doc.find("w:body", NS)
    paras = [p for p in body if p.tag == q("p")]
    log = []
    hit = [p for p in paras if OLD_TITLE in ptext(p)]
    assert len(hit) == 1
    before = ptext(hit[0]); replace_in_para(hit[0], OLD_TITLE, NEW_TITLE)
    log.append({"step": "5 title", "para_before": before, "para_after": ptext(hit[0])})
    hit = [p for p in paras if ptext(p) == SUM_OLD]
    assert len(hit) == 1
    runs = [r for r in hit[0].findall("w:r", NS) if r.find("w:t", NS) is not None]
    assert len(runs) == 1, "summary paragraph has more than one text run (formatting would be lost)"
    set_text(hit[0], SUM_NEW)
    log.append({"step": "5 summary order", "para_before": SUM_OLD, "para_after": ptext(hit[0])})
    head = xml.split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("log entries:", len(log))


if __name__ == "__main__":
    main(*sys.argv[1:4])
