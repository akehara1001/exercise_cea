"""ESM_1_v20 = direct edit of ESM_1_v19.docx by the v20 instruction (2026-11-07), step 2 (Table S12 only):
  - title: the instruction's title after the label in the form of every other ESM table ("Supplementary Table S12. "),
    footnote symbol a at its last word (unchanged);
  - footnotes: the instruction's text as the single footnote a (whole table, as the other ESM tables); the bracketed
    clause is kept because the model has the locoregional -> distant transition (engine.R, lrr_dr rate; In_DR holds entries
    from LRR); the abbreviation list ends with a full stop as in the other ESM footnotes; v19 footnotes b and c removed,
    and their superscripts b and c removed from the eight column headings (the definitions are now in footnote a, whose
    words "Distant recurrence" and "any recurrence" match the headings "Distant recurrence at ..." and "Any recurrence at ...");
  - columns, rows and values unchanged (v19).
  Table S1 (CHEERS): the v19 cells are rebuilt from the v19 pagination (edit_esm_v19.locations19) and must equal ESM_1_v19;
  the v20 cells use the v20 pagination; cells are rewritten only if a page changed.
Only word/document.xml is rewritten.
usage: python edit_esm_v20.py <ESM_1_v19.docx> <m19_stats.json> <m20_stats.json> <out.docx> <log.json>
"""
import hashlib, json, os, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_esm_v12 import NS, q, ptext, cell  # noqa: E402
from edit_esm_v14 import pages14  # noqa: E402
from edit_esm_v19 import locations19, S12_TITLE as S12_TITLE_V19  # noqa: E402

ESM19_SHA16 = "9ef39de95fb519ad"
XS = "{http://www.w3.org/XML/1998/namespace}space"
S12_TITLE = ("Supplementary Table S12. Cumulative recurrence 5 and 7 years after randomization without exercise, and its "
             "absolute reduction with exercise, by recurrence hazard ratio")
S12_FOOT = ("Values are from the deterministic base case, with all inputs at their base values, the recurrence hazard ratio held "
            "for 5 years after randomization and the reduction in the hazard (1 − HR) halving every year thereafter. "
            "Cumulative recurrence is the share of the modeled cohort (women aged 49 years starting neoadjuvant chemotherapy for "
            "stage II or III triple-negative breast cancer, including those with a pathological complete response and those who "
            "progressed before surgery) with a first recurrence after surgery by 5 or 7 years after randomization (model months "
            "60 and 84), counted from the monthly transitions into the recurrence states rather than from the occupancy of those "
            "states. Distant recurrence counts the first entry into a distant recurrence state, including entry after a "
            "locoregional recurrence; any recurrence counts the first locoregional or distant recurrence. Progression before "
            "surgery is not counted. The hazard ratio applies to both the locoregional and the distant recurrence transitions. "
            "Absolute reduction is the value without exercise minus the value with exercise, in percentage points. HR, hazard "
            "ratio.")
HEADS = ["Distant recurrence at 5 years", "Distant recurrence at 7 years", "Any recurrence at 5 years", "Any recurrence at 7 years"]


def runs_t(e):
    return [r for r in e.iter(q("r")) if r.find("w:t", NS) is not None]


def is_sup(r):
    va = r.find("w:rPr/w:vertAlign", NS)
    return va is not None and va.get(q("val")) == "superscript"


def main(src, stats19, stats20, dst, logpath):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == ESM19_SHA16, "ESM v19 sha256 differs"
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    body = doc.find("w:body", NS)
    bl = list(body)
    log = []
    i = [k for k, b in enumerate(bl) if b.tag == q("p") and ptext(b) == S12_TITLE_V19 + "a"]
    assert len(i) == 1
    i = i[0]
    title, tbl = bl[i], bl[i + 1]
    assert tbl.tag == q("tbl")
    # title
    tr = runs_t(title)
    assert len(tr) == 2 and tr[0].find("w:t", NS).text == S12_TITLE_V19 and is_sup(tr[1]) and tr[1].find("w:t", NS).text == "a"
    before = ptext(title)
    tr[0].find("w:t", NS).text = S12_TITLE
    log.append({"step": "2 title", "before": before, "after": ptext(title)})
    # superscripts b and c out of the column headings
    n = 0
    for tc in tbl.iter(q("tc")):
        t = ptext(tc)
        if t[:-1] in HEADS and t[-1] in "bc":
            rs = runs_t(tc)
            assert is_sup(rs[-1]) and rs[-1].find("w:t", NS).text == t[-1]
            rs[-1].getparent().remove(rs[-1])
            n += 1
            log.append({"step": "2 heading symbol", "before": t, "after": ptext(tc)})
    assert n == 8, n
    # footnotes: a replaced, b and c removed
    feet = []
    for b in bl[i + 2:]:
        if b.tag != q("p") or b.find("w:pPr/w:sectPr", NS) is not None:
            break
        if ptext(b):
            feet.append(b)
    assert [ptext(f)[0] for f in feet] == ["a", "b", "c"], [ptext(f)[:5] for f in feet]
    fr = runs_t(feet[0])
    assert len(fr) == 2 and is_sup(fr[0]) and fr[0].find("w:t", NS).text == "a"
    before = ptext(feet[0])
    fr[1].find("w:t", NS).text = S12_FOOT
    fr[1].find("w:t", NS).set(XS, "preserve")
    log.append({"step": "2 footnote a", "before": before, "after": ptext(feet[0])})
    for f in feet[1:]:
        log.append({"step": "2 footnote removed", "before": ptext(f)})
        body.remove(f)
    # CHEERS
    S19, S20 = pages14(stats19), pages14(stats20)
    L19, L20 = locations19(S19), locations19(S20)
    s1 = [k for k, b in enumerate(list(body)) if b.tag == q("p") and ptext(b).startswith("Supplementary Table S1.")][0]
    s2 = [k for k, b in enumerate(list(body)) if b.tag == q("p") and ptext(b).startswith("Supplementary Table S2.")][0]
    cheers = [b for b in list(body)[s1:s2] if b.tag == q("tbl")]
    seen, nchg = set(), 0
    for t in cheers:
        for trw in t.findall("w:tr", NS):
            tcs = trw.findall("w:tc", NS)
            if len(tcs) != 4 or not ptext(tcs[1]).strip().isdigit():
                continue
            k = int(ptext(tcs[1]).strip())
            tt = list(tcs[3].iter(q("t")))
            assert len(tt) == 1 and tt[0].text == cell(*L19[k]), ("v19 cell differs from the v19 rebuild", k)
            new = cell(*L20[k])
            if new != tt[0].text:
                log.append({"step": "CHEERS pages", "item": k, "old": tt[0].text, "new": new}); tt[0].text = new; nchg += 1
            seen.add(k)
    assert seen == set(range(1, 29))
    head = xml.split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("heading symbols removed:", n, "| footnotes removed:", len(feet) - 1, "| CHEERS cells changed:", nchg)


if __name__ == "__main__":
    main(*sys.argv[1:6])
