"""ESM_1_v11 = direct edit of Dr Ozaki's ESM_1.docx (v10): Table S1 Location cells and footnote a only (instruction
step 3), plus the section 8 font-size fix of the six 10-pt header lines. Pages come from the Word pagination of
manuscript_v11_BCRT.docx (word_stats JSON). Each v10 Location text must equal the expected text or the script stops.

usage: python edit_esm_v11.py <ESM_1.docx> <out.docx> <manuscript_v11_stats.json> <log.json>
"""
import hashlib, json, sys, zipfile
from lxml import etree

ESM10_SHA16 = "9c63d49303d56a4f"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def q(t):
    return "{%s}%s" % (W, t)


def ptext(el):
    return "".join(t.text or "" for t in el.iter(q("t")))


def pages(stats):
    """manuscript section -> list of (start, end) page per paragraph, keyed by name used in the Locations."""
    P = json.load(open(stats, encoding="utf-8-sig"))["paragraphs"]
    txt = [p["text"].rstrip("\r\x07") for p in P]
    pg = [(p["start_page"], p["end_page"]) for p in P]
    heads = ["Introduction", "Methods", "Study design", "Outcomes", "Exercise effect and costs",
             "Survival, costs and utilities", "Statistical analysis", "Results", "Maximum affordable cost of exercise",
             "Duration and metastatic treatment costs", "Pembrolizumab", "Sensitivity and scenario analyses",
             "Discussion", "Implications", "Limitations", "Conclusion"]
    pos = {}
    for h in heads:
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
    # statistical analysis: paragraph 1, stages (1)-(6)
    sa = [k for k in range(pos["Statistical analysis"] + 1, pos["Results"]) if txt[k].strip()]
    sec["SA_stage"] = {int(txt[k][1]): pg[k] for k in sa if txt[k].startswith("(")}
    return sec


def span(ranges):
    lo = min(a for a, _ in ranges); hi = max(b for _, b in ranges)
    return "(p. %d)" % lo if lo == hi else "(pp. %d to %d)" % (lo, hi)


def main(src, dst, stats, logpath):
    raw = open(src, "rb").read()
    assert hashlib.sha256(raw).hexdigest()[:16] == ESM10_SHA16, "ESM v10 sha256 differs"
    S = pages(stats)
    m, r, st = S, S, S["SA_stage"]
    para = lambda name, *ns: [S[name][n - 1] for n in ns]
    loc = {
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
        12: ("Methods, Exercise effect and costs, paragraph 1; Methods, Survival, costs and utilities, paragraph 1; Supplementary Methods S1",
             para("Exercise effect and costs", 1) + para("Survival, costs and utilities", 1)),
        13: ("Methods, Survival, costs and utilities, paragraph 2", para("Survival, costs and utilities", 2)),
        14: ("Methods, Exercise effect and costs, paragraph 2; Methods, Survival, costs and utilities, paragraph 2; Table 1; Supplementary Table S2",
             para("Exercise effect and costs", 2) + para("Survival, costs and utilities", 2)),
        15: ("Methods, Exercise effect and costs, paragraph 2; Methods, Survival, costs and utilities, paragraph 2",
             para("Exercise effect and costs", 2) + para("Survival, costs and utilities", 2)),
        16: ("Methods, Study design, paragraph 1; Methods, Statistical analysis, paragraph 1; Fig. 1; Supplementary Methods S1; Statements and Declarations, Data availability",
             para("Study design", 1) + para("Statistical analysis", 1) + S["Data availability"]),
        17: ("Methods, Exercise effect and costs, paragraph 1; Methods, Survival, costs and utilities, paragraph 1; Methods, Statistical analysis, stages (1) and (2); Supplementary Methods S1",
             para("Exercise effect and costs", 1) + para("Survival, costs and utilities", 1) + [st[1], st[2]]),
        18: ("No subgroup analyses beyond the two comparisons; Methods, Study design, paragraph 1", para("Study design", 1)),
        19: ("Not performed", None),
        20: ("Methods, Statistical analysis, stages (3) to (5); Supplementary Methods S1", [st[3], st[4], st[5]]),
        21: ("Not performed", None),
        22: ("Table 1; Supplementary Table S2", None),   # no manuscript paragraph to page (Table 1 is in the tables file)
        23: ("Results, Maximum affordable cost of exercise, paragraphs 1 to 3; Results, Duration and metastatic treatment costs, paragraphs 1 to 3; Results, Pembrolizumab, paragraphs 1 to 2; Fig. 2; Tables 2 and 3; Supplementary Tables S4 to S8",
             para("Maximum affordable cost of exercise", 1, 2, 3) + para("Duration and metastatic treatment costs", 1, 2, 3) + para("Pembrolizumab", 1, 2)),
        24: ("Results, Duration and metastatic treatment costs, paragraphs 1 to 2; Results, Sensitivity and scenario analyses, paragraph 1; Fig. 3; Table 2; Supplementary Tables S4, S7, S9 and S10; Supplementary Fig. S2",
             para("Duration and metastatic treatment costs", 1, 2) + para("Sensitivity and scenario analyses", 1)),
        25: ("Not applicable (item 21)", None),
        26: ("Discussion, paragraphs 1 to 6; Discussion, Implications; Discussion, Limitations",
             para("Discussion", 1, 2, 3, 4, 5, 6) + S["Implications"] + S["Limitations"]),
        27: ("Statements and Declarations, Funding", S["Funding"]),
        28: ("Statements and Declarations, Competing interests", S["Competing interests"]),
    }
    # section paragraph counts the Locations assume
    assert len(S["Introduction"]) == 4 and len(S["Study design"]) == 3 and len(S["Outcomes"]) == 2
    assert len(S["Exercise effect and costs"]) == 2 and len(S["Survival, costs and utilities"]) == 2
    assert len(S["Maximum affordable cost of exercise"]) == 3 and len(S["Duration and metastatic treatment costs"]) == 3
    assert len(S["Pembrolizumab"]) == 2 and len(S["Sensitivity and scenario analyses"]) == 1 and len(S["Discussion"]) == 6
    assert sorted(st) == [1, 2, 3, 4, 5, 6]

    zin = zipfile.ZipFile(src)
    doc = etree.fromstring(zin.read("word/document.xml"))
    body = doc.find("w:body", NS)
    blocks = list(body)
    i_s1 = [i for i, b in enumerate(blocks) if b.tag == q("p") and ptext(b).startswith("Supplementary Table S1.")]
    i_s2 = [i for i, b in enumerate(blocks) if b.tag == q("p") and ptext(b).startswith("Supplementary Table S2.")]
    assert len(i_s1) == 1 and len(i_s2) == 1
    tbls = [b for b in blocks[i_s1[0]:i_s2[0]] if b.tag == q("tbl")]
    assert [ptext(t.find("w:tr", NS)) for t in tbls] == ["Title", "Abstract", "Introduction", "Methods", "Results",
                                                        "Discussion", "Other relevant information"]
    log = []
    seen = set()
    for t in tbls:
        for tr in t.findall("w:tr", NS):
            tcs = tr.findall("w:tc", NS)
            if len(tcs) != 4:
                continue
            item = ptext(tcs[1]).strip()
            if not item.isdigit():
                continue
            n = int(item)
            text, rng = loc[n]
            new = text if rng is None else text + " " + span(rng)
            ts = list(tcs[3].iter(q("t")))
            assert len(ts) == 1, n
            old = ts[0].text
            ts[0].text = new
            seen.add(n)
            log.append({"item": n, "old": old, "new": new})
    assert seen == set(range(1, 29)), sorted(seen)
    # footnote a
    old_a = "the paragraph within the section or subsection and the page of the manuscript file"
    new_a = "the paragraph within the section or subsection (or the numbered stage of the statistical analysis) and the page of the manuscript file"
    hits = [t for t in doc.iter(q("t")) if t.text and old_a in t.text]
    assert len(hits) == 1
    before = hits[0].text
    hits[0].text = before.replace(old_a, new_a)
    log.append({"footnote_a_old": before, "footnote_a_new": hits[0].text})
    # section 8: the six 10-pt header runs (Online Resource 1 ... Reference numbers ...) to 12 pt
    nfix = []
    for rr in doc.iter(q("r")):
        rpr = rr.find("w:rPr", NS)
        if rpr is None:
            continue
        for el in rpr:
            if el.tag in (q("sz"), q("szCs")) and el.get(q("val")) == "20":
                el.set(q("val"), "24")
                nfix.append(ptext(rr)[:40])
    log.append({"fmt_runs_10pt_to_12pt": nfix})

    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                head = data.split(b"?>", 1)[0] + b"?>"
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for e in log[:28]:
        print(e["item"], "|", e["new"])
    print("fmt runs fixed:", len(nfix))


if __name__ == "__main__":
    main(*sys.argv[1:5])
