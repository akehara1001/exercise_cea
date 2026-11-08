"""ESM_1_v19 = direct edit of ESM_1_v18.docx (= ESM_1_v17, byte copy) by the v19 instruction (2026-11-07):
  2   Supplementary Table S12 added after Table S11, in its own landscape section (as every ESM table): title, table and
      footnotes a-c (letters as in every ESM table; placement by WRITING_RULES 7.2: a = whole table at the last word of the
      title, b and c at the end of the column headings they define). Values from output/phase2/main/recurrence_reduction.csv
      (pct_without_2dp, diff_pp_2dp; 2 decimals in the whole table).
  2/5 cover page: "Article:" line with the new title (the ESM has no header or running head; checked in all parts).
  5   "secondary comparison" in Tables S8, S9 and S11 replaced by the main-text wording "exercise added to chemotherapy
      alone" (column headings); in the footnotes of S8 and S11 the definition "secondary comparison: exercise added to
      chemotherapy alone" is removed (the label is no longer used), in S9 "(secondary comparison)" -> "(exercise added to
      chemotherapy alone)". "reference comparison" does not occur; "main comparison" stays.
  6   Table S1 (CHEERS 2022) Location cells: the v17 cells are first rebuilt from the v17 pagination (edit_esm_v15.locations15,
      as in v17) and must equal the v18 (= v17) cells exactly; the v19 cells use the v19 pagination (Word, word_stats JSON)
      and the v19 text: item 7 adds Methods, Exercise effect and costs, paragraph 3 (the program content is described there
      again in v18); item 18 names the two treatments instead of "the two comparisons"; item 20 adds Discussion,
      Limitations, paragraph 2 (expected value of perfect information, restored in v18); item 23 adds Supplementary
      Table S12. Other items: text as in v17, pages from v19.
Only word/document.xml is rewritten (lxml).
usage: python edit_esm_v19.py <ESM_1_v18.docx> <recurrence_reduction.csv> <m17_stats.json> <m19_stats.json> <out.docx> <log.json>
"""
import copy, csv, hashlib, json, os, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_esm_v12 import NS, q, ptext, cell  # noqa: E402
from edit_esm_v14 import pages14  # noqa: E402
from edit_esm_v15 import locations15  # noqa: E402
from edit_manuscript_v19 import CSV_SHA16  # noqa: E402

ESM18_SHA16 = "642590a6b691dea9"
XS = "{http://www.w3.org/XML/1998/namespace}space"
OLD_TITLE = "Cost-effectiveness of exercise added to neoadjuvant chemotherapy for triple-negative breast cancer in Japan"
NEW_TITLE = ("Exercise versus or in addition to pembrolizumab with neoadjuvant chemotherapy for early-stage triple-negative "
             "breast cancer: a model-based cost-effectiveness analysis in Japan")
ALONE = "exercise added to chemotherapy alone"
# (location, old, new): cell texts are whole-cell matches; footnote edits are substrings of one paragraph
CELL_REPL = [
    ("S8", "Effect until 1 year after surgery: secondary comparison", "Effect until 1 year after surgery: " + ALONE, 2),
    ("S8", "No waning: secondary comparison", "No waning: " + ALONE, 2),
    ("S8", "Exercise continued after surgery: secondary comparison", "Exercise continued after surgery: " + ALONE, 2),
    ("S11", "Secondary comparison: maximum affordable cost at recurrence HR 0.85",
     "Exercise added to chemotherapy alone: maximum affordable cost at recurrence HR 0.85", 1),
    ("S11", "Secondary comparison: recurrence HR (reduction in recurrence hazard, %) at which the maximum affordable cost equals the program cost",
     "Exercise added to chemotherapy alone: recurrence HR (reduction in recurrence hazard, %) at which the maximum affordable cost equals the program cost", 1),
    ("S11", "Secondary comparison: recurrence HR (reduction in recurrence hazard, %) at which medical costs avoided equal the program cost",
     "Exercise added to chemotherapy alone: recurrence HR (reduction in recurrence hazard, %) at which medical costs avoided equal the program cost", 1),
]
FOOT_REPL = [
    ("S8", "Main comparison: exercise added to chemotherapy plus pembrolizumab; secondary comparison: exercise added to chemotherapy alone. Effect until",
     "Main comparison: exercise added to chemotherapy plus pembrolizumab. Effect until"),
    ("S9", "1,157 did not (secondary comparison);", "1,157 did not (" + ALONE + ");"),
    ("S11", "Main comparison: exercise added to chemotherapy plus pembrolizumab; secondary comparison: exercise added to chemotherapy alone; program cost:",
     "Main comparison: exercise added to chemotherapy plus pembrolizumab; program cost:"),
]

S12_TITLE = ("Supplementary Table S12. Cumulative proportion of women with distant recurrence and with any recurrence after "
             "surgery without exercise, and the absolute reduction with exercise, at 5 and 7 years after randomization by the "
             "recurrence hazard ratio with exercise")
S12_FOOT = [
    ("a", "Modeled cohort: women aged 49 years starting neoadjuvant chemotherapy for stage II or III triple-negative breast "
          "cancer in Japan (Table 1). Proportions are per 100 women entering the model, with or without pCR and including "
          "those whose disease progressed before surgery. Deterministic base case, with all inputs at their base values. The "
          "recurrence HR is held for 5 years after randomization, after which the reduction in the hazard, 1 − HR, halves every "
          "year (Table 1). The recurrence HR multiplies both the locoregional and the distant recurrence transitions after "
          "surgery. Only recurrence after surgery is counted; progression during neoadjuvant therapy, before surgery, is not. "
          "Time is counted from randomization, the start of neoadjuvant chemotherapy; 5 and 7 years are model months 60 and "
          "84. Recurrence HR 1.00: without exercise. Absolute reduction: the proportion without exercise minus the proportion "
          "with exercise. HR, hazard ratio; pCR, pathological complete response."),
    ("b", "First entry into distant recurrence, early or late, after surgery, including distant recurrence after locoregional "
          "recurrence; each woman is counted once."),
    ("c", "First entry into locoregional or distant recurrence after surgery, the recurrences on which the recurrence HR acts; "
          "distant recurrence after locoregional recurrence is not counted again."),
]
HRS_B = [0.991, 0.989, 0.966, 0.958, 0.95, 0.85, 0.72]
HR_LABEL = {1.0: "1.00", 0.991: "0.991", 0.989: "0.989", 0.966: "0.966", 0.958: "0.958", 0.95: "0.95", 0.85: "0.85", 0.72: "0.72"}
COLS = [(g, o, m) for g in ("chemo_pembro", "chemo_alone") for o in ("distant", "any") for m in (60, 84)]
GRID = [2808] + [1470] * 8                      # = 14,568 twips, the width of the other landscape ESM tables (8 x 1,821)


def locations19(S):
    L = locations15(S)
    para = lambda name, *ns: [S[name][n - 1] for n in ns]
    L[7] = ("Methods, Study design, paragraph 1; Methods, Exercise effect and costs, paragraph 3",
            para("Study design", 1) + para("Exercise effect and costs", 3))
    L[18] = ("No subgroup analyses beyond exercise added to chemotherapy alone and to chemotherapy plus pembrolizumab; "
             "Methods, Study design, paragraph 1", para("Study design", 1))
    st = S["SA_stage"]
    L[20] = ("Methods, Statistical analysis, stages (4) to (6); Supplementary Methods S1; Discussion, Limitations, paragraph 2",
             [st[4], st[5], st[6]] + para("Limitations", 2))
    t23, r23 = L[23]
    assert t23.endswith("Supplementary Tables S4 to S9")
    L[23] = (t23 + " and S12", r23)
    return L


def run_like(r, text, sup=False, bold=None):
    """copy of run r with text; superscript and bold as given"""
    n = copy.deepcopy(r)
    for t in n.findall("w:t", NS)[1:]:
        n.remove(t)
    t = n.find("w:t", NS); t.text = text; t.set(XS, "preserve")
    rpr = n.find("w:rPr", NS)
    va = rpr.find("w:vertAlign", NS)
    if sup and va is None:
        va = etree.SubElement(rpr, q("vertAlign")); va.set(q("val"), "superscript")
    if not sup and va is not None:
        rpr.remove(va)
    if bold is not None:
        b = rpr.find("w:b", NS)
        if bold:
            b.attrib.pop(q("val"), None)
        else:
            b.set(q("val"), "0")
    return n


def make_cell(tpl_tc, width, text, sup=None, span=1, vmerge=None, bold=False):
    """cell from the template cell of Table S11 (tcPr with tcW; one paragraph with an empty run and one text run)"""
    tc = copy.deepcopy(tpl_tc)
    pr = tc.find("w:tcPr", NS)
    for ch in list(pr):
        pr.remove(ch)
    w = etree.SubElement(pr, q("tcW")); w.set(q("type"), "dxa"); w.set(q("w"), str(width))
    if span > 1:
        g = etree.SubElement(pr, q("gridSpan")); g.set(q("val"), str(span))
    if vmerge is not None:
        v = etree.SubElement(pr, q("vMerge"))
        if vmerge == "restart":
            v.set(q("val"), "restart")
    p = tc.find("w:p", NS)
    runs = [r for r in p.findall("w:r", NS) if r.find("w:t", NS) is not None]
    base = runs[0]
    for r in runs:
        p.remove(r)
    if text:
        p.append(run_like(base, text, bold=bold))
    if sup:
        p.append(run_like(base, sup, sup=True, bold=False))
    return tc


def main(src, csvpath, stats17, stats19, dst, logpath):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == ESM18_SHA16, "ESM v18 sha256 differs"
    assert hashlib.sha256(open(csvpath, "rb").read()).hexdigest()[:16] == CSV_SHA16, "recurrence_reduction.csv sha256 differs"
    R = list(csv.DictReader(open(csvpath, encoding="utf-8")))
    val = lambda g, hr, o, m, col: [r for r in R if r["group"] == g and abs(float(r["hr"]) - hr) < 1e-9 and r["outcome"] == o
                                    and int(r["month"]) == m][0][col]
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    body = doc.find("w:body", NS)
    log = []
    blocks = list(body)
    tstart = {}
    for i, b in enumerate(blocks):
        if b.tag == q("p") and ptext(b).startswith("Supplementary Table S"):
            tstart[ptext(b).split(".")[0].split()[-1]] = i

    def span_of(lab):                       # blocks from the title of lab to the title of the next table or figure
        i = tstart[lab]
        nxt = [j for j, b in enumerate(blocks) if j > i and b.tag == q("p") and ptext(b).startswith("Supplementary ")]
        return blocks[i:(nxt[0] if nxt else len(blocks))]

    # ---- 2/5 cover title
    p = [b for b in blocks[:6] if b.tag == q("p") and ptext(b) == "Article: " + OLD_TITLE]
    assert len(p) == 1
    ts = [t for t in p[0].iter(q("t")) if OLD_TITLE in (t.text or "")]
    assert len(ts) == 1
    ts[0].text = ts[0].text.replace(OLD_TITLE, NEW_TITLE)
    log.append({"step": "5 title", "old": "Article: " + OLD_TITLE, "new": ptext(p[0])})
    # ---- 5 secondary comparison: cells
    for lab, old, new, n_expect in CELL_REPL:
        hits = [tc for b in span_of(lab) if b.tag == q("tbl") for tc in b.iter(q("tc")) if ptext(tc) == old]
        assert len(hits) == n_expect, (lab, old, len(hits))
        for tc in hits:
            tt = list(tc.iter(q("t")))
            assert len(tt) == 1 and tt[0].text == old
            tt[0].text = new
            log.append({"step": "5 wording", "table": lab, "before": old, "after": new})
    # ---- 5 secondary comparison: footnotes
    for lab, old, new in FOOT_REPL:
        hits = [b for b in span_of(lab) if b.tag == q("p") and old in ptext(b)]
        assert len(hits) == 1, (lab, old)
        before = ptext(hits[0])
        tt = [t for t in hits[0].iter(q("t")) if old in (t.text or "")]
        assert len(tt) == 1
        tt[0].text = tt[0].text.replace(old, new)
        assert ptext(hits[0]) == before.replace(old, new)
        log.append({"step": "5 wording", "table": lab, "before": before, "after": ptext(hits[0])})
    # ---- 6 CHEERS
    S17, S19 = pages14(stats17), pages14(stats19)
    for S in (S17, S19):
        assert len(S["Introduction"]) == 4 and len(S["Study design"]) == 3 and len(S["Outcomes"]) == 2
        assert len(S["Exercise effect and costs"]) == 3 and len(S["Discussion"]) == 7
        assert len(S["Implications"]) == 2 and len(S["Limitations"]) == 2
    L17, L19 = locations15(S17), locations19(S19)
    cheers = [b for b in span_of("S1") if b.tag == q("tbl")]
    assert len(cheers) == 7
    seen = set()
    for t in cheers:
        for tr in t.findall("w:tr", NS):
            tcs = tr.findall("w:tc", NS)
            if len(tcs) != 4 or not ptext(tcs[1]).strip().isdigit():
                continue
            n = int(ptext(tcs[1]).strip())
            tt = list(tcs[3].iter(q("t")))
            assert len(tt) == 1, n
            old = tt[0].text
            assert old == cell(*L17[n]), ("v18 (= v17) cell differs from the v17 rebuild", n, old)
            tt[0].text = cell(*L19[n])
            seen.add(n)
            log.append({"step": "6 CHEERS", "item": n, "old": old, "new": tt[0].text, "changed": old != tt[0].text})
    assert seen == set(range(1, 29))
    # ---- 2 Table S12 after the last footnote of Table S11, in its own landscape section
    s11 = span_of("S11")
    s11_title, s11_tbl = s11[0], [b for b in s11 if b.tag == q("tbl")][0]
    s11_feet = [b for b in s11 if b.tag == q("p") and ptext(b) and b is not s11_title]
    s11_blank = [b for b in s11 if b.tag == q("p") and not ptext(b)][0]
    assert [ptext(f)[0] for f in s11_feet] == ["a", "b", "c", "d"]
    assert blocks[-1].tag == q("sectPr") and blocks[-1].find("w:pgSz", NS).get(q("orient")) == "landscape"
    sect_p = [b for b in blocks if b.tag == q("p") and b.find("w:pPr/w:sectPr", NS) is not None
              and b.find("w:pPr/w:sectPr/w:pgSz", NS).get(q("orient")) == "landscape"][-1]
    new_sect = copy.deepcopy(sect_p)
    # title
    title = copy.deepcopy(s11_title)
    truns = [r for r in title.findall("w:r", NS) if r.find("w:t", NS) is not None]
    assert len(truns) == 2 and truns[1].find("w:t", NS).text == "a"
    truns[0].find("w:t", NS).text = S12_TITLE
    # table
    tbl = copy.deepcopy(s11_tbl)
    for tr in tbl.findall("w:tr", NS):
        tbl.remove(tr)
    grid = tbl.find("w:tblGrid", NS)
    for gc in list(grid):
        grid.remove(gc)
    for wdt in GRID:
        gc = etree.SubElement(grid, q("gridCol")); gc.set(q("w"), str(wdt))
    tpl_tc = s11_tbl.findall("w:tr", NS)[1].findall("w:tc", NS)[0]
    tpl_tr = s11_tbl.findall("w:tr", NS)[1]

    def row(cells):
        tr = copy.deepcopy(tpl_tr)
        for tc in tr.findall("w:tc", NS):
            tr.remove(tc)
        for c in cells:
            tr.append(c)
        tbl.append(tr)

    W1, WN, WALL = GRID[0], GRID[1], sum(GRID)
    head = {"distant": "Distant recurrence at %d years", "any": "Any recurrence at %d years"}
    sup = {"distant": "b", "any": "c"}
    row([make_cell(tpl_tc, W1, "Recurrence HR", vmerge="restart"),
         make_cell(tpl_tc, 4 * WN, "Chemotherapy plus pembrolizumab", span=4),
         make_cell(tpl_tc, 4 * WN, "Chemotherapy alone", span=4)])
    row([make_cell(tpl_tc, W1, "", vmerge="continue")] +
        [make_cell(tpl_tc, WN, head[o] % (m // 12), sup=sup[o]) for g, o, m in COLS])
    row([make_cell(tpl_tc, WALL, "A. Cumulative proportion of women without exercise, %", span=9, bold=True)])
    cells_log = []
    vals = [val(g, 1.0, o, m, "pct_without_2dp") for g, o, m in COLS]
    row([make_cell(tpl_tc, W1, HR_LABEL[1.0])] + [make_cell(tpl_tc, WN, "%.2f" % float(v)) for v in vals])
    cells_log.append([HR_LABEL[1.0]] + ["%.2f" % float(v) for v in vals])
    row([make_cell(tpl_tc, WALL, "B. Absolute reduction with exercise, percentage points", span=9, bold=True)])
    for hr in HRS_B:
        vals = [val(g, hr, o, m, "diff_pp_2dp") for g, o, m in COLS]
        assert all(float(v) > 0 for v in vals), (hr, vals)
        row([make_cell(tpl_tc, W1, HR_LABEL[hr])] + [make_cell(tpl_tc, WN, "%.2f" % float(v)) for v in vals])
        cells_log.append([HR_LABEL[hr]] + ["%.2f" % float(v) for v in vals])
    # footnotes
    feet = []
    for letter, text in S12_FOOT:
        f = copy.deepcopy(s11_feet[0])
        fr = [r for r in f.findall("w:r", NS) if r.find("w:t", NS) is not None]
        assert len(fr) == 2 and fr[0].find("w:t", NS).text == "a"
        fr[0].find("w:t", NS).text = letter
        fr[1].find("w:t", NS).text = text
        fr[1].find("w:t", NS).set(XS, "preserve")
        feet.append(f)
    anchor = s11_feet[-1]
    for el in [new_sect, title, tbl, copy.deepcopy(s11_blank)] + feet:
        anchor.addnext(el)
        anchor = el
    log.append({"step": "2 Table S12", "title": ptext(title) , "rows": cells_log,
                "footnotes": [ptext(f) for f in feet],
                "header": ["Recurrence HR"] + [head[o] % (m // 12) + sup[o] for g, o, m in COLS]})
    headb = xml.split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = headb + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for e in log:
        if e["step"] == "6 CHEERS" and e["changed"]:
            print("CHEERS", e["item"], "|", e["old"], "\n      =>", e["new"])
    print("CHEERS changed:", sum(1 for e in log if e.get("changed")), "| wording edits:",
          sum(1 for e in log if e["step"] == "5 wording"), "| S12 rows:", len(cells_log))


if __name__ == "__main__":
    main(*sys.argv[1:7])
