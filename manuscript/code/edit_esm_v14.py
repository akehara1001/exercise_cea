"""ESM_1_v14 = direct edit of ESM_1_v13.docx by the v14 instruction step 3. Only word/document.xml is rewritten.
3a old Table 3 of tables_v13 inserted after Supplementary Table S3 as Supplementary Table S4 (new title of the instruction;
   panel C rows and footnote d removed; panels A, B and footnotes a-c as they were), in its own landscape section.
3b old Supplementary Tables S4-S10 -> S5-S11 (titles and cross-references); references to the main tables follow 1f
   (Table 2 -> Table 3; old Table 3 -> Supplementary Table S4, the form the ESM uses for its own tables).
3c Table S1 (CHEERS) Location cells: the v13 cells are first rebuilt from the v13 pagination (edit_esm_v12.locations, as
   in v13) and must match ESM_1_v13 exactly; the v14 cells use the v14 Results headings and paragraph numbers, the stage
   numbers of the statistical analysis after 1c ((3)-(6) -> (4)-(7); old (2) = new (2) and (3)), the table numbers after
   1f, and the pages of manuscript_v14_BCRT.docx in Word (word_stats JSON). Items 19, 21, 22 and 25 carry no page (v12 rule).

usage: python edit_esm_v14.py <ESM_1_v13.docx> <tables_v13.docx> <out.docx> <m13_stats.json> <m14_stats.json> <log.json>
"""
import copy, hashlib, json, os, re, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_esm_v12 import NS, q, ptext, pages as pages_v13, locations as locations_v13, span, cell  # noqa: E402

ESM13_SHA16 = "ae84d2f68ff5ccac"
T13_SHA16 = "d022962f64dd85a5"
S4_TITLE = ("Supplementary Table S4. Incremental costs by category, QALYs and cost-effectiveness of pembrolizumab added to "
            "neoadjuvant chemotherapy, in the base case and under scenarios")
HEADS14 = ["Introduction", "Methods", "Study design", "Outcomes", "Exercise effect and costs",
           "Survival, costs and utilities", "Statistical analysis", "Results", "Four strategies compared",
           "Exercise compared with pembrolizumab", "Maximum affordable cost of exercise",
           "Duration and metastatic treatment costs", "Sensitivity and scenario analyses",
           "Discussion", "Implications", "Limitations", "Conclusion"]


def pages14(stats):
    P = json.load(open(stats, encoding="utf-8-sig"))["paragraphs"]
    txt = [p["text"].rstrip("\r\x07") for p in P]
    pg = [(p["start_page"], p["end_page"]) for p in P]
    pos = {}
    for h in HEADS14:
        k = [i for i, t in enumerate(txt) if t == h]
        assert len(k) == 1, h
        pos[h] = k[0]
    order = sorted(pos.items(), key=lambda kv: kv[1])
    sec = {}
    for j, (h, i) in enumerate(order):
        nxt = order[j + 1][1] if j + 1 < len(order) else None
        sec[h] = [pg[k] for k in range(i + 1, nxt) if txt[k].strip()] if nxt else None
    a0 = txt.index("Abstract"); i0 = txt.index("Introduction")
    sec["Abstract"] = [pg[k] for k in range(a0, i0) if txt[k].strip()]
    sec["Title page"] = [pg[k] for k in range(0, a0) if txt[k].strip()]
    for lab in ("Funding", "Competing interests", "Data availability"):
        k = [i for i, t in enumerate(txt) if t.startswith(lab + " ")]
        assert len(k) == 1, lab
        sec[lab] = [pg[k[0]]]
    sa = [k for k in range(pos["Statistical analysis"] + 1, pos["Results"]) if txt[k].strip()]
    sec["SA_stage"] = {int(txt[k][1]): pg[k] for k in sa if txt[k].startswith("(")}
    return sec


def locations14(S):
    st = S["SA_stage"]
    para = lambda name, *ns: [S[name][n - 1] for n in ns]
    ex1 = ("Methods, Exercise effect and costs, paragraphs 1 to 2", para("Exercise effect and costs", 1, 2))
    ex2 = ("Methods, Exercise effect and costs, paragraph 3", para("Exercise effect and costs", 3))
    L = {
        1: ("Title page", S["Title page"]),
        2: ("Abstract", S["Abstract"]),
        3: ("Introduction, paragraphs 1 to 4", para("Introduction", 1, 2, 3, 4)),
        4: ("Methods, Study design, paragraph 3", para("Study design", 3)),
        5: ("Methods, Study design, paragraph 1; Table 1", para("Study design", 1)),
        6: ("Methods, Study design, paragraphs 1 to 2", para("Study design", 1, 2)),
        7: ("Methods, Study design, paragraph 1", para("Study design", 1)),
        8: ("Methods, Study design, paragraph 2", para("Study design", 2)),
        9: ("Methods, Study design, paragraph 2", para("Study design", 2)),
        10: ("Methods, Study design, paragraph 2", para("Study design", 2)),
        11: ("Methods, Outcomes, paragraphs 1 to 2", para("Outcomes", 1, 2)),
        12: (ex1[0] + "; Methods, Survival, costs and utilities, paragraph 1; Supplementary Methods S1",
             ex1[1] + para("Survival, costs and utilities", 1)),
        13: ("Methods, Survival, costs and utilities, paragraph 2", para("Survival, costs and utilities", 2)),
        14: (ex2[0] + "; Methods, Survival, costs and utilities, paragraph 2; Table 1; Supplementary Table S2",
             ex2[1] + para("Survival, costs and utilities", 2)),
        15: (ex2[0] + "; Methods, Survival, costs and utilities, paragraph 2", ex2[1] + para("Survival, costs and utilities", 2)),
        16: ("Methods, Study design, paragraph 1; Methods, Statistical analysis, paragraph 1; Fig. 1; Supplementary Methods S1; Statements and Declarations, Data availability",
             para("Study design", 1) + para("Statistical analysis", 1) + S["Data availability"]),
        # old stage (2) is now stages (2) and (3)
        17: (ex1[0] + "; Methods, Survival, costs and utilities, paragraph 1; Methods, Statistical analysis, stages (1) to (3); Supplementary Methods S1",
             ex1[1] + para("Survival, costs and utilities", 1) + [st[1], st[2], st[3]]),
        18: ("No subgroup analyses beyond the two comparisons; Methods, Study design, paragraph 1", para("Study design", 1)),
        19: ("Not performed", None),
        # old stages (3)-(5) are now (4)-(6)
        20: ("Methods, Statistical analysis, stages (4) to (6); Supplementary Methods S1", [st[4], st[5], st[6]]),
        21: ("Not performed", None),
        22: ("Table 1; Supplementary Table S2", None),
        23: ("Results, Four strategies compared, paragraph 1; Results, Exercise compared with pembrolizumab, paragraph 1; "
             "Results, Maximum affordable cost of exercise, paragraphs 1 to 3; Results, Duration and metastatic treatment costs, paragraphs 1 to 3; "
             "Fig. 2; Tables 2 and 3; Supplementary Tables S4 to S9",
             para("Four strategies compared", 1) + para("Exercise compared with pembrolizumab", 1)
             + para("Maximum affordable cost of exercise", 1, 2, 3) + para("Duration and metastatic treatment costs", 1, 2, 3)),
        24: ("Results, Duration and metastatic treatment costs, paragraphs 1 to 2; Results, Sensitivity and scenario analyses, paragraph 1; "
             "Fig. 3; Table 3; Supplementary Tables S5, S8, S10 and S11; Supplementary Fig. S2",
             para("Duration and metastatic treatment costs", 1, 2) + para("Sensitivity and scenario analyses", 1)),
        25: ("Not applicable (item 21)", None),
        26: ("Discussion, paragraphs 1 to 8; Discussion, Implications; Discussion, Limitations",
             para("Discussion", 1, 2, 3, 4, 5, 6, 7, 8) + S["Implications"] + S["Limitations"]),
        27: ("Statements and Declarations, Funding", S["Funding"]),
        28: ("Statements and Declarations, Competing interests", S["Competing interests"]),
    }
    return L


REN = re.compile(r"Tables 2 and 3|Supplementary Table S(\d+)\b|(?<!Supplementary )\bTable (\d+)\b")


def ren_text(s):
    def f(m):
        x = m.group(0)
        if x == "Tables 2 and 3":
            return "Table 3 and Supplementary Table S4"
        if m.group(1):
            n = int(m.group(1)); return "Supplementary Table S%d" % (n + 1 if n >= 4 else n)
        n = int(m.group(2))
        return {2: "Table 3", 3: "Supplementary Table S4"}.get(n, x)
    return REN.sub(f, s)


def text_nodes(p):
    return [t for r in p.iter(q("r")) for t in r.findall("w:t", NS)]


def renumber_para(p):
    """Applies ren_text to the paragraph; every match must lie within one text node."""
    full = "".join(t.text or "" for t in text_nodes(p))
    new_full = ren_text(full)
    if new_full == full:
        return None
    for t in text_nodes(p):
        if t.text:
            t.text = ren_text(t.text)
    after = "".join(t.text or "" for t in text_nodes(p))
    assert after == new_full, ("match spans runs", full[:80])
    return full, after


def main(src, t13, dst, stats13, stats14, logpath):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == ESM13_SHA16, "ESM v13 sha256 differs"
    assert hashlib.sha256(open(t13, "rb").read()).hexdigest()[:16] == T13_SHA16, "tables v13 sha256 differs"
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    body = doc.find("w:body", NS)
    blocks = list(body)
    log = []

    # ---- 3c first part: v13 cells rebuilt from the v13 pagination
    S13, S14 = pages_v13(stats13), pages14(stats14)
    L13, L14 = locations_v13(S13, True), locations14(S14)
    assert len(S14["Discussion"]) == 8 and len(S14["Four strategies compared"]) == 1 and len(S14["Exercise compared with pembrolizumab"]) == 1
    assert len(S14["Maximum affordable cost of exercise"]) == 3 and len(S14["Duration and metastatic treatment costs"]) == 3
    assert len(S14["Sensitivity and scenario analyses"]) == 1 and sorted(S14["SA_stage"]) == [1, 2, 3, 4, 5, 6, 7]
    i_s1 = [i for i, b in enumerate(blocks) if b.tag == q("p") and ptext(b).startswith("Supplementary Table S1.")]
    i_s2 = [i for i, b in enumerate(blocks) if b.tag == q("p") and ptext(b).startswith("Supplementary Table S2.")]
    assert len(i_s1) == 1 and len(i_s2) == 1
    cheers = [b for b in blocks[i_s1[0]:i_s2[0]] if b.tag == q("tbl")]
    assert len(cheers) == 7

    # ---- 3b renumbering everywhere except inside the CHEERS tables (their Location cells are rebuilt below). The
    # tables are held in the list, so their proxies are stable and "is" identifies them (id() of transient paragraph
    # proxies is not reliable in lxml).
    for p in list(body.iter(q("p"))):
        if any(a is t for a in p.iterancestors(q("tbl")) for t in cheers):
            continue
        r = renumber_para(p)
        if r:
            log.append({"step": "3b", "before": r[0], "after": r[1]})

    seen = set()
    for t in cheers:
        for tr in t.findall("w:tr", NS):
            tcs = tr.findall("w:tc", NS)
            if len(tcs) != 4 or not ptext(tcs[1]).strip().isdigit():
                continue
            n = int(ptext(tcs[1]).strip())
            ts = list(tcs[3].iter(q("t")))
            assert len(ts) == 1, n
            old = ts[0].text
            assert old == cell(*L13[n]), ("v13 cell differs from the v13 rebuild", n, old)
            ts[0].text = cell(*L14[n])
            seen.add(n)
            log.append({"step": "3c", "item": n, "old": old, "new": ts[0].text, "changed": old != ts[0].text})
    assert seen == set(range(1, 29))

    # ---- 3a old Table 3 of tables_v13 -> Supplementary Table S4, after the section of Table S3
    tdoc = etree.fromstring(zipfile.ZipFile(t13).read("word/document.xml"))
    tb = list(tdoc.find("w:body", NS))
    assert ptext(tb[14]).startswith("Table 3.") and tb[15].tag == q("tbl")
    foots = [tb[16], tb[17], tb[18]]
    assert [ptext(f)[0] for f in foots] == ["a", "b", "c"] and ptext(tb[19]).startswith("dEffect at which exercise")
    for f in foots:
        assert "exercise" not in ptext(f).lower(), "footnote mentions exercise"        # 3a: nothing to delete in a-c
    title = copy.deepcopy(tb[14])
    trs = title.findall("w:r", NS)
    assert len(trs) == 2 and ptext(trs[1]) == "a"
    trs[0].find("w:t", NS).text = S4_TITLE
    tbl = copy.deepcopy(tb[15])
    rows = tbl.findall("w:tr", NS)
    k = [i for i, tr in enumerate(rows) if ptext(tr).startswith("C. Exercise effect needed")]
    assert len(k) == 1 and len(rows) - k[0] == 3
    for tr in rows[k[0]:]:
        log.append({"step": "3a delete row", "row": [ptext(c) for c in tr.findall("w:tc", NS)]})
        tbl.remove(tr)
    blocks = list(body)
    i_s3 = [i for i, b in enumerate(blocks) if b.tag == q("p") and ptext(b).startswith("Supplementary Table S3.")][0]
    i_s5 = [i for i, b in enumerate(blocks) if b.tag == q("p") and ptext(b).startswith("Supplementary Table S5.")][0]
    sect = blocks[i_s5 - 1]
    assert sect.find("w:pPr/w:sectPr", NS) is not None and ptext(sect) == "" and i_s3 < i_s5 - 1
    assert sect.find("w:pPr/w:sectPr/w:pgSz", NS).get(q("orient")) == "landscape"
    brk = copy.deepcopy(sect)
    anchor = sect
    for el in [title, tbl] + [copy.deepcopy(f) for f in foots] + [brk]:
        anchor.addnext(el)
        anchor = el
    log.append({"step": "3a insert", "title": ptext(title), "rows": [[ptext(c) for c in tr.findall("w:tc", NS)] for tr in tbl.findall("w:tr", NS)],
                "footnotes": [ptext(f) for f in foots]})

    head = xml.split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for e in log:
        if e["step"] == "3c":
            print(e["item"], "*" if e["changed"] else " ", "|", e["new"])
        elif e["step"] == "3b":
            print("3b |", e["before"][:70], "=>", e["after"][:70])
        else:
            print(e["step"], "|", str(e.get("row") or e.get("title"))[:110])


if __name__ == "__main__":
    main(*sys.argv[1:7])
