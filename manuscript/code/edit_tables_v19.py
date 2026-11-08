"""tables_v19 = direct edit of tables_v18_BCRT.docx (= tables_v17, byte copy) by the v19 instruction step 3 (Dr Ozaki's
request): in Table 3, the symbol ✳ (superscript, at the end of the cell text, WRITING_RULES 7.2) where the HRs of the new
footnote appear, and the footnote sentence of the instruction after footnote d, with [a]-[e] = absolute reductions in
distant recurrence at 7 years (output/phase2/main/recurrence_reduction.csv, column diff_pp_2dp, 2 decimals):
  [a] chemotherapy plus pembrolizumab, HR 0.989   [b] same, HR 0.958   [c] same, HR 0.85
  [d] chemotherapy alone, HR 0.991                [e] same, HR 0.966
Cells marked: panel A row "The maximum affordable cost equals the cost of the fee-schedule-based program" (0.989 (1.1),
0.991 (0.9)); panel A row "Medical costs avoided equal the cost of the fee-schedule-based program" (0.958 (4.2), 0.966 (3.4));
the two row labels "Base case, recurrence HR 0.85" (panels B and C). The 0.958 of the chemotherapy-alone column in the
CHALLENGE-program row is a different break-even point and is not marked. Tables 1 and 2 are unchanged. Only
word/document.xml is rewritten.
usage: python edit_tables_v19.py <tables_v18.docx> <recurrence_reduction.csv> <out.docx> <log.json>
"""
import copy, hashlib, json, os, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_manuscript_v14 import NS, q, ptext  # noqa: E402
from edit_manuscript_v19 import value, CSV_SHA16  # noqa: E402

T18_SHA16 = "8236a3eee6495976"
STAR = "✳"   # U+2733


def footnote(v):
    return (" Under the base-case assumptions, recurrence HRs of 0.989, 0.958 and 0.85 with chemotherapy plus pembrolizumab "
            "correspond to absolute reductions in distant recurrence at 7 years of about %s, %s and %s percentage points, and "
            "HRs of 0.991 and 0.966 with chemotherapy alone to about %s and %s points (Table S12)." % tuple(v))


def add_star(tc):
    """append a superscript ✳ run after the last text run of the cell's only paragraph"""
    ps = tc.findall("w:p", NS)
    assert len(ps) == 1
    runs = [r for r in ps[0].findall("w:r", NS) if r.find("w:t", NS) is not None]
    last = runs[-1]
    new = copy.deepcopy(last)
    for t in new.findall("w:t", NS)[1:]:
        new.remove(t)
    t = new.find("w:t", NS)
    t.text = STAR
    t.attrib.pop("{http://www.w3.org/XML/1998/namespace}space", None)
    rpr = new.find("w:rPr", NS)
    assert rpr is not None and rpr.find("w:vertAlign", NS) is None
    va = etree.SubElement(rpr, q("vertAlign")); va.set(q("val"), "superscript")
    last.addnext(new)


def main(src, csvpath, dst, logpath):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == T18_SHA16, "tables v18 sha256 differs"
    assert hashlib.sha256(open(csvpath, "rb").read()).hexdigest()[:16] == CSV_SHA16, "recurrence_reduction.csv sha256 differs"
    v = [value(csvpath, "chemo_pembro", 0.989, "distant", 84), value(csvpath, "chemo_pembro", 0.958, "distant", 84),
         value(csvpath, "chemo_pembro", 0.85, "distant", 84), value(csvpath, "chemo_alone", 0.991, "distant", 84),
         value(csvpath, "chemo_alone", 0.966, "distant", 84)]
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    body = doc.find("w:body", NS)
    blocks = list(body)
    ti = [i for i, b in enumerate(blocks) if b.tag == q("tbl")]
    assert len(ti) == 3
    t3 = blocks[ti[2]]
    title = blocks[ti[2] - 1]
    assert ptext(title).startswith("Table 3. Recurrence hazard ratios at which exercise breaks even")
    log = []
    rows = t3.findall("w:tr", NS)
    lab = lambda tr: ptext(tr.findall("w:tc", NS)[0])
    targets = []
    r_cap = [tr for tr in rows if lab(tr) == "The maximum affordable cost equals the cost of the fee-schedule-based program"]
    r_av = [tr for tr in rows if lab(tr) == "Medical costs avoidedc equal the cost of the fee-schedule-based program"]  # c = footnote
    r_base = [tr for tr in rows if lab(tr) == "Base case, recurrence HR 0.85"]
    assert len(r_cap) == 1 and len(r_av) == 1 and len(r_base) == 2
    for tr, cells, expect in ((r_cap[0], (1, 2), ("0.989 (1.1)", "0.991 (0.9)")), (r_av[0], (1, 2), ("0.958 (4.2)", "0.966 (3.4)"))):
        tcs = tr.findall("w:tc", NS)
        for c, e in zip(cells, expect):
            assert ptext(tcs[c]) == e, (ptext(tcs[c]), e)
            targets.append(tcs[c])
    for tr in r_base:
        targets.append(tr.findall("w:tc", NS)[0])
    for tc in targets:
        before = ptext(tc)
        add_star(tc)
        log.append({"step": "3 symbol", "before": before, "after": ptext(tc)})
    # footnote after footnote d of Table 3
    foot = [b for b in blocks[ti[2] + 1:] if b.tag == q("p") and ptext(b)]
    assert [ptext(f)[0] for f in foot] == ["a", "b", "c", "d"], [ptext(f)[:3] for f in foot]
    fd = foot[3]
    new = copy.deepcopy(fd)
    runs = [r for r in new.findall("w:r", NS) if r.find("w:t", NS) is not None]
    assert len(runs) == 2 and runs[0].find("w:t", NS).text == "d"
    runs[0].find("w:t", NS).text = STAR
    t = runs[1].find("w:t", NS)
    t.text = footnote(v)
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    fd.addnext(new)
    log.append({"step": "3 footnote", "new": ptext(new), "values": dict(zip("abcde", v))})
    head = xml.split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("values:", dict(zip("abcde", v)), "| symbols:", len(targets))
    print(ptext(new))


if __name__ == "__main__":
    main(*sys.argv[1:5])
