"""cover_letter_v20 = direct edit of cover_letter_v19_BCRT.docx by the v20 instruction step 3: the summary paragraph is
replaced by the instruction's text (the v19 summary is not kept). Address, journal name, the first paragraph with the
title, the fit paragraph and the declarations are unchanged. Only word/document.xml is rewritten.
usage: python edit_cover_v20.py <cover_letter_v19.docx> <out.docx> <log.json>
"""
import hashlib, json, os, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_manuscript_v14 import NS, q, ptext, set_text  # noqa: E402
from edit_cover_v19 import SUM_NEW as SUM_V19  # noqa: E402

CL19_SHA16 = "c9e56b226a81e14e"
SUM_V20 = ("Pembrolizumab added to neoadjuvant chemotherapy is now standard care for stage II or III triple-negative breast "
           "cancer in Japan, at a drug cost of about JPY 400,000 per dose. Structured exercise during chemotherapy is cheap and "
           "safe, but whether it reduces recurrence is unknown. We built a state-transition model on KEYNOTE-522 and compared "
           "the four strategies formed by chemotherapy with or without pembrolizumab and with or without exercise, from the "
           "perspective of the Japanese public payer. We then asked how large an effect on recurrence exercise would need to "
           "match pembrolizumab, and how much a program added to chemotherapy plus pembrolizumab could cost and remain "
           "cost-effective. If exercise lowered the recurrence hazard by 5% or more, both strategies without it were "
           "dominated. Exercise would need to cut the recurrence hazard by more than half to match the health gained with "
           "pembrolizumab, but an effect the size of that in the CHALLENGE trial would give the same net benefit at the "
           "Japanese threshold. Added to pembrolizumab, a program priced from the medical fee schedule became cost-effective "
           "once it lowered the recurrence hazard by 1.1%, and its value depended on the size and duration of the effect far "
           "more than on its price. To our knowledge, this is the first economic evaluation of exercise during neoadjuvant "
           "therapy for breast cancer, and it places a non-drug intervention on the same cost-effectiveness scale as a drug, "
           "which Japan's formal evaluation, covering drugs and devices only, has not done.")


def main(src, dst, logpath):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == CL19_SHA16, "cover letter v19 sha256 differs"
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    paras = [p for p in doc.find("w:body", NS) if p.tag == q("p")]
    hit = [p for p in paras if ptext(p) == SUM_V19]
    assert len(hit) == 1
    assert len([r for r in hit[0].findall("w:r", NS) if r.find("w:t", NS) is not None]) == 1
    set_text(hit[0], SUM_V20)
    log = [{"step": "3 summary", "para_before": SUM_V19, "para_after": ptext(hit[0])}]
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
