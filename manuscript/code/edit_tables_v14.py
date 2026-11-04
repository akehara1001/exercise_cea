"""tables_v14 = direct edit of tables_v13_BCRT.docx by the v14 instruction step 2. Only word/document.xml is rewritten.
2a new Table 2 (two panels, footnotes a-d), inserted as its own landscape section after Table 1; its cells are built from
   the analysis outputs (half up) and must equal the strings of the instruction cell by cell; the layout copies the v13
   tables (title paragraph, Table Grid with equal columns, merged bold panel rows, merged plain group rows, plain header
   and value cells, superscript footnote marks not bold, footnote paragraphs).
2b old Table 2 -> Table 3: title number and footnote d "Table S4 (Online Resource 1)" -> "Table S5 (Online Resource 1)".
2c old Table 3 (and the section break before it) removed; it moves to the ESM (edit_esm_v14.py reads it from v13).
2d Table 1 footnote c "Table S10 (Online Resource 1)" -> "Table S11 (Online Resource 1)".

usage: python edit_tables_v14.py <tables_v13.docx> <out.docx> <project_root> <log.json>
"""
import copy, csv, hashlib, json, os, sys, zipfile
from decimal import Decimal, ROUND_HALF_UP
from lxml import etree

T13_SHA16 = "d022962f64dd85a5"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
XS = "{http://www.w3.org/XML/1998/namespace}space"
MINUS = "−"
DASH = "—"
NAME = {"chemo": "Chemotherapy alone", "exercise": "Chemotherapy plus exercise", "pembro": "Chemotherapy plus pembrolizumab",
        "both": "Chemotherapy plus pembrolizumab plus exercise"}

# ---- strings of the instruction (2a)
TITLE = ("Table 2. Costs, QALYs and cost-effectiveness of the four strategies at three recurrence hazard ratios with exercise, "
         "and the exercise effect needed to match pembrolizumab in QALYs or in net monetary benefit", "a")
HEADER = ["Strategy", "Total cost", "Total QALYs", "Comparator", "Incremental cost", "Incremental QALYs",
          "ICER (JPY 1,000 per QALY)", "Net monetary benefit relative to chemotherapy alone at JPY 5 million per QALY"]
PANEL_A = [("A. Four strategies at recurrence HRs", False), ("b", True), (" of 0.95, 0.85 and 0.72, with the fee-schedule-based program", False), ("c", True)]
PANEL_B = [("B. Pembrolizumab added to chemotherapy alone, and the exercise effect needed to match it", False), ("d", True)]
GIVEN_A = {
    0.95: [("Chemotherapy plus exercise", "12,112", "17.073", DASH, DASH, DASH, DASH, "931"),
           ("Chemotherapy alone", "12,202", "16.905", "Chemotherapy plus exercise", "91", MINUS + "0.168", "Dominated", "0"),
           ("Chemotherapy plus pembrolizumab plus exercise", "16,592", "19.194", "Chemotherapy plus exercise", "4,480", "2.121", "2,112", "7,056"),
           ("Chemotherapy plus pembrolizumab", "16,629", "19.061", "Chemotherapy plus pembrolizumab plus exercise", "37", MINUS + "0.133", "Dominated", "6,355")],
    0.85: [("Chemotherapy plus exercise", "11,525", "17.420", DASH, DASH, DASH, DASH, "3,250"),
           ("Chemotherapy alone", "12,202", "16.905", "Chemotherapy plus exercise", "677", MINUS + "0.515", "Dominated", "0"),
           ("Chemotherapy plus pembrolizumab plus exercise", "16,120", "19.466", "Chemotherapy plus exercise", "4,594", "2.047", "2,245", "8,889"),
           ("Chemotherapy plus pembrolizumab", "16,629", "19.061", "Chemotherapy plus pembrolizumab plus exercise", "509", MINUS + "0.405", "Dominated", "6,355")],
    0.72: [("Chemotherapy plus exercise", "10,723", "17.892", DASH, DASH, DASH, DASH, "6,413"),
           ("Chemotherapy alone", "12,202", "16.905", "Chemotherapy plus exercise", "1,479", MINUS + "0.987", "Dominated", "0"),
           ("Chemotherapy plus pembrolizumab plus exercise", "15,479", "19.834", "Chemotherapy plus exercise", "4,756", "1.942", "2,449", "11,368"),
           ("Chemotherapy plus pembrolizumab", "16,629", "19.061", "Chemotherapy plus pembrolizumab plus exercise", "1,150", MINUS + "0.773", "Dominated", "6,355")]}
BLOCK_LABEL = "HR %.2f"           # the block rows of panel A, as written in the instruction ("HR 0.95: ...")
GIVEN_B1 = [("Incremental cost", "4,426 [" + MINUS + "330, 8,901]"), ("Incremental QALYs", "2.156 [0.245, 4.228]"),
            ("ICER, JPY 1,000 per QALY", "2,053"),
            ("Probability cost-effective at JPY 5 million per QALY, %", "83.1"),
            ("Probability cost-effective at JPY 7.5 million per QALY, %", "90.8")]   # label as v13 Table 3 (the instruction: "at JPY 7.5 million per QALY, %")
GIVEN_B2_HEAD = ("Exercise effect needed to match pembrolizumab", "Recurrence HR", "Increase in pCR, percentage points")
GIVEN_B2 = [("In QALYs", "0.425", "35.9"), ("In net monetary benefit at JPY 5 million per QALY", "0.722", "19.0"),
            ("In net monetary benefit at JPY 7.5 million per QALY", "0.638", "24.1")]
FOOT = [
    ("a", "Modeled cohort: women aged 49 years starting neoadjuvant chemotherapy for stage II or III triple-negative breast cancer "
          "in Japan (Table 1). Costs in JPY 1,000 at fiscal year 2026 prices, discounted at 2% per year over a lifetime horizon; the "
          "strategies with exercise include the fee-schedule-based program (JPY 192,400). Strategies are listed in order of total "
          "cost. Increments are against the strategy in the comparator column: the next cheaper strategy on the frontier, or, for a "
          "dominated strategy, the strategy that dominates it. A strategy is dominated when another costs less and gives more QALYs. "
          "Net monetary benefit is the QALYs gained valued at JPY 5 million per QALY minus the incremental cost, relative to "
          "chemotherapy alone. In panel B, cells with a bracket show the deterministic estimate and the 95% UI [2.5th and 97.5th "
          "percentiles of 1,000 probabilistic sensitivity analysis samples]; probability cost-effective is the share of samples with "
          "a positive net monetary benefit. HR, hazard ratio; ICER, incremental cost-effectiveness ratio; JPY, Japanese yen; pCR, "
          "pathological complete response; QALY, quality-adjusted life year; UI, uncertainty interval."),
    ("b", "Hazard ratio for locoregional and distant recurrence after surgery in the strategies with exercise, relative to the same "
          "treatment without exercise, held for 5 years after randomization and then halving every year (Table 1); 0.72 is the "
          "CHALLENGE estimate."),
    ("c", "With the CHALLENGE-based supervised program (JPY 239,508), chemotherapy plus pembrolizumab was extendedly dominated at an "
          "HR of 0.95, because its ICER against chemotherapy plus exercise exceeded that of chemotherapy plus pembrolizumab plus "
          "exercise, and dominated at 0.85 and 0.72; with the remote low-cost program (JPY 11,260) the results were as shown."),
    ("d", "Effect at which exercise added to chemotherapy alone gives the same incremental QALYs as pembrolizumab, or the same net "
          "monetary benefit with the fee-schedule-based program, in the base case. All values except the HR of 0.722 lie outside the "
          "ranges studied: recurrence HR 0.70 to 1.00 (Table S5 (Online Resource 1)) and pCR increase 0 to 10 percentage points "
          "(Table S6 (Online Resource 1)).")]
NCOL, COLW = 8, 1821


def q(t):
    return "{%s}%s" % (W, t)


def ptext(el):
    return "".join(t.text or "" for t in el.iter(q("t")))


def hu(x, d):
    v = Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    if v == 0:
        v = abs(v)
    s = f"{v:,.{d}f}"
    return s.replace("-", MINUS)


def read_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def computed_cells(root):
    out = os.path.join(root, "output", "phase2", "main")
    inc = [r for r in read_csv(os.path.join(out, "fourarm_incremental.csv")) if r["programme"] == "E02"]
    tot = read_csv(os.path.join(out, "fourarm_totals.csv"))
    A = {}
    for h in (0.95, 0.85, 0.72):
        rows = [r for r in inc if abs(float(r["hr0"]) - h) < 1e-9]          # in cost order (icer_table)
        assert len(rows) == 4
        A[h] = []
        for r in rows:
            t = [x for x in tot if abs(float(x["hr0"]) - h) < 1e-9 and x["arm"] == r["arm"]][0]
            na = r["d_cost"] in ("", "NA")
            icer = DASH if na else ("Dominated" if r["status"] == "dominated" else hu(float(r["icer"]) / 1e3, 0))
            assert r["status"] in ("frontier", "dominated")                 # E02: no extended dominance
            A[h].append((NAME[r["arm"]], hu(float(r["cost"]) / 1e3, 0), hu(float(r["qaly"]), 3),
                         NAME[r["comparator"]] if r["comparator"] not in ("", "NA") else DASH,
                         DASH if na else hu(float(r["d_cost"]) / 1e3, 0), DASH if na else hu(float(r["d_qaly"]), 3), icer,
                         hu(float(t["dnmb_500_vs_chemo"]) / 1e3, 0)))
    ref = [r for r in read_csv(os.path.join(out, "det_reference.csv")) if r["column"] == "base"][0]
    ps = [r for r in read_csv(os.path.join(out, "psa_reference_summary.csv")) if r["column"] == "base"][0]
    B1 = [("Incremental cost", "%s [%s, %s]" % (hu(float(ref["dC"]) / 1e3, 0), hu(float(ps["dC_lo"]) / 1e3, 0), hu(float(ps["dC_hi"]) / 1e3, 0))),
          ("Incremental QALYs", "%s [%s, %s]" % (hu(ref["dQ"], 3), hu(ps["dQ_lo"], 3), hu(ps["dQ_hi"], 3))),
          ("ICER, JPY 1,000 per QALY", hu(float(ref["icer"]) / 1e3, 0)),
          ("Probability cost-effective at JPY 5 million per QALY, %", hu(100 * float(ps["p_ce_500"]), 1)),
          ("Probability cost-effective at JPY 7.5 million per QALY, %", hu(100 * float(ps["p_ce_750"]), 1))]
    ys = {r["axis"]: float(r["root"]) for r in read_csv(os.path.join(out, "det_yardstick.csv"))}
    ne = {(float(r["lambda"]), r["axis"]): float(r["root"]) for r in read_csv(os.path.join(out, "fourarm_nmb_equal.csv"))}
    B2 = [("In QALYs", hu(ys["hr0"], 3), hu(100 * ys["pcr"], 1)),
          ("In net monetary benefit at JPY 5 million per QALY", hu(ne[(5e6, "hr0")], 3), hu(100 * ne[(5e6, "pcr")], 1)),
          ("In net monetary benefit at JPY 7.5 million per QALY", hu(ne[(7.5e6, "hr0")], 3), hu(100 * ne[(7.5e6, "pcr")], 1))]
    return A, B1, B2


def main(src, dst, root, logpath):
    raw = open(src, "rb").read()
    assert hashlib.sha256(raw).hexdigest()[:16] == T13_SHA16, "tables v13 sha256 differs"
    A, B1, B2 = computed_cells(root)
    for h in GIVEN_A:
        assert [tuple(r) for r in A[h]] == GIVEN_A[h], ("panel A differs from the instruction", h, A[h])
    assert B1 == GIVEN_B1, ("panel B differs", B1)
    assert [tuple(r) for r in B2] == GIVEN_B2, ("panel B effect rows differ", B2)

    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    body = doc.find("w:body", NS)
    bl = list(body)
    assert len(bl) == 21
    assert ptext(bl[0]).startswith("Table 1.") and ptext(bl[7]).startswith("Table 2.") and ptext(bl[14]).startswith("Table 3.")
    for i in (6, 13):
        assert bl[i].find("w:pPr/w:sectPr", NS) is not None and ptext(bl[i]) == ""
    # v13 v. v13 table 3 cells: panel B values of the instruction are those of v13 Table 3 (base case column)
    t3 = {ptext(tr.findall("w:tc", NS)[0]): [ptext(c) for c in tr.findall("w:tc", NS)] for tr in bl[15].findall("w:tr", NS)}
    assert t3["Total"][1] == GIVEN_B1[0][1] and t3["Incremental QALYs"][1] == GIVEN_B1[1][1]
    assert t3["ICER, JPY 1,000 per QALY"][1] == GIVEN_B1[2][1]
    assert t3["Probability cost-effective at JPY 5 million per QALY, %"][1] == GIVEN_B1[3][1]
    assert t3["Probability cost-effective at JPY 7.5 million per QALY, %"][1] == GIVEN_B1[4][1]
    assert t3["Recurrence HR with exercise added to chemotherapy alone"][1] == "0.425"
    assert t3["Increase in pCR with exercise added to chemotherapy alone, percentage points"][1] == "35.9"
    log = []

    def rep(el, old, new, step):
        full = ptext(el)
        assert full.count(old) == 1, (step, old)
        ts = [t for t in el.iter(q("t")) if old in (t.text or "")]
        assert len(ts) == 1, (step, "match spans runs")
        ts[0].text = ts[0].text.replace(old, new)
        log.append({"step": step, "before": full, "after": ptext(el)})

    # templates from v13 Table 2
    t2 = bl[8]
    rows = t2.findall("w:tr", NS)
    rpr_plain = copy.deepcopy(rows[0].find(".//w:r/w:rPr", NS))
    rpr_bold = copy.deepcopy(rows[1].findall(".//w:r", NS)[1].find("w:rPr", NS))
    rpr_sup = copy.deepcopy(rows[1].findall(".//w:r", NS)[2].find("w:rPr", NS))
    assert rpr_bold.find("w:b", NS) is not None and rpr_bold.find("w:b", NS).get(q("val")) is None
    assert rpr_sup.find("w:vertAlign", NS).get(q("val")) == "superscript"
    assert rpr_plain.find("w:b", NS).get(q("val")) == "0" and rpr_plain.find("w:vertAlign", NS) is None

    def run(text, kind):
        r = etree.Element(q("r"))
        r.append(copy.deepcopy({"plain": rpr_plain, "bold": rpr_bold, "sup": rpr_sup}[kind]))
        t = etree.SubElement(r, q("t"))
        t.text = text
        if text != text.strip():
            t.set(XS, "preserve")
        return r

    def cell(parts, span=1):
        """parts: list of (text, kind)."""
        tc = etree.Element(q("tc"))
        tcpr = etree.SubElement(tc, q("tcPr"))
        w = etree.SubElement(tcpr, q("tcW")); w.set(q("type"), "dxa"); w.set(q("w"), str(COLW * span))
        if span > 1:
            g = etree.SubElement(tcpr, q("gridSpan")); g.set(q("val"), str(span))
        p = etree.SubElement(tc, q("p"))
        etree.SubElement(p, q("r"))                      # empty first run, as in the v13 cells (python-docx)
        for text, kind in parts:
            p.append(run(text, kind))
        return tc

    def row(cells):
        tr = etree.Element(q("tr"))
        for c in cells:
            tr.append(c)
        assert sum(int(c.find("w:tcPr/w:gridSpan", NS).get(q("val"))) if c.find("w:tcPr/w:gridSpan", NS) is not None else 1
                   for c in cells) == NCOL
        return tr

    tbl = etree.Element(q("tbl"))
    tbl.append(copy.deepcopy(t2.find("w:tblPr", NS)))
    grid = etree.SubElement(tbl, q("tblGrid"))
    for _ in range(NCOL):
        g = etree.SubElement(grid, q("gridCol")); g.set(q("w"), str(COLW))
    tbl.append(row([cell([(h, "plain")]) for h in HEADER]))
    tbl.append(row([cell([(t, "sup" if s else "bold") for t, s in PANEL_A], NCOL)]))
    for h in (0.95, 0.85, 0.72):
        tbl.append(row([cell([(BLOCK_LABEL % h, "plain")], NCOL)]))
        for r in A[h]:
            tbl.append(row([cell([(x, "plain")]) for x in r]))
    tbl.append(row([cell([(t, "sup" if s else "bold") for t, s in PANEL_B], NCOL)]))
    for lab, v in B1:
        tbl.append(row([cell([(lab, "plain")], 4), cell([(v, "plain")], 4)]))
    tbl.append(row([cell([(GIVEN_B2_HEAD[0], "plain")], 4), cell([(GIVEN_B2_HEAD[1], "plain")], 2), cell([(GIVEN_B2_HEAD[2], "plain")], 2)]))
    for lab, a, b in B2:
        tbl.append(row([cell([(lab, "plain")], 4), cell([(a, "plain")], 2), cell([(b, "plain")], 2)]))

    title = copy.deepcopy(bl[7])
    trs = title.findall("w:r", NS)
    assert len(trs) == 2 and trs[1].find("w:rPr/w:vertAlign", NS) is not None
    trs[0].find("w:t", NS).text = TITLE[0]
    trs[1].find("w:t", NS).text = TITLE[1]
    foots = []
    for mark, text in FOOT:
        f = copy.deepcopy(bl[9])
        frs = f.findall("w:r", NS)
        assert len(frs) == 2 and frs[0].find("w:rPr/w:vertAlign", NS) is not None
        frs[0].find("w:t", NS).text = mark
        frs[1].find("w:t", NS).text = text
        foots.append(f)
    brk = copy.deepcopy(bl[6])
    new = [title, tbl] + foots + [brk]

    # 2d, 2b
    rep(bl[4], "Table S10 (Online Resource 1)", "Table S11 (Online Resource 1)", "2d")
    rep(bl[7], "Table 2.", "Table 3.", "2b title")
    rep(bl[12], "Table S4 (Online Resource 1)", "Table S5 (Online Resource 1)", "2b footnote d")
    # 2c: old Table 3 and the section break before it
    for el in bl[13:20]:
        if el.tag == q("p"):
            log.append({"step": "2c delete", "before": ptext(el)})
        else:
            for tr in el.findall("w:tr", NS):
                log.append({"step": "2c delete", "row": [ptext(c) for c in tr.findall("w:tc", NS)]})
        body.remove(el)
    # 2a: new Table 2 after the section break that ends Table 1
    anchor = bl[6]
    for el in new:
        anchor.addnext(el)
        anchor = el
    log.append({"step": "2a insert", "title": ptext(title), "rows": [[ptext(c) for c in tr.findall("w:tc", NS)] for tr in tbl.findall("w:tr", NS)],
                "footnotes": [ptext(f) for f in foots]})

    head = xml.split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("body blocks:", len(list(body)), "| log entries:", len(log))


if __name__ == "__main__":
    main(*sys.argv[1:5])
