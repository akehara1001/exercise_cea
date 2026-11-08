"""tables_v20 = direct edit of tables_v19_BCRT.docx by the v20 instruction (2026-11-07), Table 3 only:
  0(1) footnote symbol "e" (continuing a-d) instead of ✳, in the table and in the footnote;
  1    placement as a-d (the symbol right after the term it annotates; in a-d: "Recurrence HR^b (reduction ...)",
       "Medical costs avoided^c equal ..."): right after the HR value, i.e. "0.989^e (1.1)", "0.991^e (0.9)",
       "0.958^e (4.2)", "0.966^e (3.4)" and "Base case, recurrence HR 0.85^e" (two rows; the value ends the label);
       footnote text of the instruction, without "about", with "(Table S12 (Online Resource 1))" (0(2)); the footnote begins
       with the superscript letter followed directly by the text, as footnotes a-d. Values from
       output/phase2/main/recurrence_reduction.csv (diff_pp_2dp), checked against the instruction's text.
Tables 1 and 2 unchanged. Only word/document.xml is rewritten.
usage: python edit_tables_v20.py <tables_v19.docx> <recurrence_reduction.csv> <out.docx> <log.json>
"""
import copy, hashlib, json, os, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_manuscript_v14 import NS, q, ptext  # noqa: E402
from edit_manuscript_v19 import value, CSV_SHA16  # noqa: E402

T19_SHA16 = "3fc3f4561a3e1fd5"
XS = "{http://www.w3.org/XML/1998/namespace}space"
STAR = "✳"
FOOT_V20 = ("Under the base-case assumptions, recurrence HRs of 0.989, 0.958 and 0.85 with chemotherapy plus pembrolizumab "
            "correspond to absolute reductions in distant recurrence at 7 years of %s, %s and %s percentage points, and HRs of "
            "0.991 and 0.966 with chemotherapy alone to %s and %s points (Table S12 (Online Resource 1)).")
GIVEN = ("Under the base-case assumptions, recurrence HRs of 0.989, 0.958 and 0.85 with chemotherapy plus pembrolizumab "
         "correspond to absolute reductions in distant recurrence at 7 years of 0.14, 0.53 and 1.93 percentage points, and HRs of "
         "0.991 and 0.966 with chemotherapy alone to 0.15 and 0.56 points (Table S12 (Online Resource 1)).")


def text_runs(p):
    return [r for r in p.findall("w:r", NS) if r.find("w:t", NS) is not None]


def main(src, csvpath, dst, logpath):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == T19_SHA16, "tables v19 sha256 differs"
    assert hashlib.sha256(open(csvpath, "rb").read()).hexdigest()[:16] == CSV_SHA16, "recurrence_reduction.csv sha256 differs"
    v = [value(csvpath, "chemo_pembro", 0.989, "distant", 84), value(csvpath, "chemo_pembro", 0.958, "distant", 84),
         value(csvpath, "chemo_pembro", 0.85, "distant", 84), value(csvpath, "chemo_alone", 0.991, "distant", 84),
         value(csvpath, "chemo_alone", 0.966, "distant", 84)]
    foot = FOOT_V20 % tuple(v)
    assert foot == GIVEN, "CSV values differ from the instruction's footnote"
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    body = doc.find("w:body", NS)
    blocks = list(body)
    ti = [i for i, b in enumerate(blocks) if b.tag == q("tbl")]
    t3 = blocks[ti[2]]
    assert ptext(blocks[ti[2] - 1]).startswith("Table 3. ")
    log = []
    starred = [tc for tc in t3.iter(q("tc")) if ptext(tc).endswith(STAR)]
    assert len(starred) == 6, len(starred)
    for tc in starred:
        before = ptext(tc)
        p = tc.find("w:p", NS)
        runs = text_runs(p)
        sup, txt = runs[-1], runs[-2]
        assert sup.find("w:t", NS).text == STAR and len(runs) == 2
        s = txt.find("w:t", NS).text
        if s.startswith("Base case, recurrence HR "):
            sup.find("w:t", NS).text = "e"                      # the HR value ends the label
        else:
            hr, rest = s.split(" ", 1)                          # "0.989 (1.1)" -> "0.989", "(1.1)"
            assert hr in ("0.989", "0.991", "0.958", "0.966") and rest.startswith("("), s
            txt.find("w:t", NS).text = hr
            sup.find("w:t", NS).text = "e"
            tail = copy.deepcopy(txt)
            tail.find("w:t", NS).text = " " + rest
            tail.find("w:t", NS).set(XS, "preserve")
            sup.addnext(tail)
        log.append({"step": "0(1)/1 symbol", "before": before, "after": ptext(tc)})
    feet = [b for b in blocks[ti[2] + 1:] if b.tag == q("p") and ptext(b)]
    fe = [f for f in feet if ptext(f).startswith(STAR)]
    assert len(fe) == 1
    runs = text_runs(fe[0])
    assert len(runs) == 2 and runs[0].find("w:t", NS).text == STAR
    before = ptext(fe[0])
    runs[0].find("w:t", NS).text = "e"
    runs[1].find("w:t", NS).text = foot
    runs[1].find("w:t", NS).set(XS, "preserve")
    log.append({"step": "1 footnote e", "before": before, "after": ptext(fe[0]), "values": dict(zip("abcde", v))})
    assert [ptext(f)[0] for f in feet] == ["a", "b", "c", "d", "e"]
    head = xml.split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("values:", dict(zip("abcde", v)), "| symbols:", len(starred))


if __name__ == "__main__":
    main(*sys.argv[1:5])
