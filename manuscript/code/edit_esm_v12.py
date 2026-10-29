"""ESM_1_v12 = direct edit of ESM_1_v11.docx: Table S1 Location cells only (instruction step 2). After the paragraph
split of Exercise effect and costs (step 1c), items 12 and 17 cite paragraphs 1 to 2 and items 14 and 15 paragraph 3;
the pages of all items are recomputed from the Word pagination of manuscript_v12_BCRT.docx (word_stats JSON).
Before editing, the v11 cells are rebuilt from the v11 texts and the v11 pagination and must match exactly.

usage: python edit_esm_v12.py <ESM_1_v11.docx> <out.docx> <manuscript_v11_stats.json> <manuscript_v12_stats.json> <log.json>
"""
import hashlib, json, sys, zipfile
from lxml import etree

ESM11_SHA16 = "aa0d4e947ced6690"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
HEADS = ["Introduction", "Methods", "Study design", "Outcomes", "Exercise effect and costs",
         "Survival, costs and utilities", "Statistical analysis", "Results", "Maximum affordable cost of exercise",
         "Duration and metastatic treatment costs", "Pembrolizumab", "Sensitivity and scenario analyses",
         "Discussion", "Implications", "Limitations", "Conclusion"]


def q(t):
    return "{%s}%s" % (W, t)


def ptext(el):
    return "".join(t.text or "" for t in el.iter(q("t")))


def pages(stats):
    """manuscript section -> list of (start, end) page per paragraph."""
    P = json.load(open(stats, encoding="utf-8-sig"))["paragraphs"]
    txt = [p["text"].rstrip("\r\x07") for p in P]
    pg = [(p["start_page"], p["end_page"]) for p in P]
    pos = {}
    for h in HEADS:
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


def span(ranges):
    lo = min(a for a, _ in ranges); hi = max(b for _, b in ranges)
    return "(p. %d)" % lo if lo == hi else "(pp. %d to %d)" % (lo, hi)


def locations(S, v12):
    """item -> (Location text, page ranges or None). v12=False gives the v11 texts and paragraph mapping."""
    st = S["SA_stage"]
    para = lambda name, *ns: [S[name][n - 1] for n in ns]
    ex1 = ("Methods, Exercise effect and costs, paragraphs 1 to 2", para("Exercise effect and costs", 1, 2)) if v12 \
        else ("Methods, Exercise effect and costs, paragraph 1", para("Exercise effect and costs", 1))
    ex2 = ("Methods, Exercise effect and costs, paragraph 3", para("Exercise effect and costs", 3)) if v12 \
        else ("Methods, Exercise effect and costs, paragraph 2", para("Exercise effect and costs", 2))
    return {
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
        15: (ex2[0] + "; Methods, Survival, costs and utilities, paragraph 2",
             ex2[1] + para("Survival, costs and utilities", 2)),
        16: ("Methods, Study design, paragraph 1; Methods, Statistical analysis, paragraph 1; Fig. 1; Supplementary Methods S1; Statements and Declarations, Data availability",
             para("Study design", 1) + para("Statistical analysis", 1) + S["Data availability"]),
        17: (ex1[0] + "; Methods, Survival, costs and utilities, paragraph 1; Methods, Statistical analysis, stages (1) and (2); Supplementary Methods S1",
             ex1[1] + para("Survival, costs and utilities", 1) + [st[1], st[2]]),
        18: ("No subgroup analyses beyond the two comparisons; Methods, Study design, paragraph 1", para("Study design", 1)),
        19: ("Not performed", None),
        20: ("Methods, Statistical analysis, stages (3) to (5); Supplementary Methods S1", [st[3], st[4], st[5]]),
        21: ("Not performed", None),
        22: ("Table 1; Supplementary Table S2", None),   # reported only in the tables (instruction: no page)
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


def cell(text, rng):
    return text if rng is None else text + " " + span(rng)


def main(src, dst, stats11, stats12, logpath):
    raw = open(src, "rb").read()
    assert hashlib.sha256(raw).hexdigest()[:16] == ESM11_SHA16, "ESM v11 sha256 differs"
    S11, S12 = pages(stats11), pages(stats12)
    assert len(S11["Exercise effect and costs"]) == 2 and len(S12["Exercise effect and costs"]) == 3
    for S in (S11, S12):
        assert len(S["Introduction"]) == 4 and len(S["Study design"]) == 3 and len(S["Outcomes"]) == 2
        assert len(S["Survival, costs and utilities"]) == 2
        assert len(S["Maximum affordable cost of exercise"]) == 3 and len(S["Duration and metastatic treatment costs"]) == 3
        assert len(S["Pembrolizumab"]) == 2 and len(S["Sensitivity and scenario analyses"]) == 1 and len(S["Discussion"]) == 6
        assert sorted(S["SA_stage"]) == [1, 2, 3, 4, 5, 6]
    L11, L12 = locations(S11, False), locations(S12, True)

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
            ts = list(tcs[3].iter(q("t")))
            assert len(ts) == 1, n
            old = ts[0].text
            assert old == cell(*L11[n]), ("v11 cell differs from v11 rebuild", n, old, cell(*L11[n]))
            new = cell(*L12[n])
            ts[0].text = new
            seen.add(n)
            log.append({"item": n, "old": old, "new": new, "changed": old != new})
    assert seen == set(range(1, 29)), sorted(seen)

    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                head = data.split(b"?>", 1)[0] + b"?>"
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for e in log:
        print(e["item"], "*" if e["changed"] else " ", "|", e["new"] if e["changed"] else "(unchanged)")
    print("changed:", sum(e["changed"] for e in log))


if __name__ == "__main__":
    main(*sys.argv[1:6])
