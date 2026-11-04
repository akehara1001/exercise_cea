"""v14 = direct edit of manuscript_v13_BCRT.docx by the v14 instruction (2026-11-04), steps 1a-1h. Only
word/document.xml is rewritten; every other part is copied byte for byte. Every paragraph acted on is found by a
string that must occur in exactly one paragraph of v13, or the script stops. The English texts of the instruction are
inserted as given (constants below); the one addition is the definition "incremental cost-effectiveness ratios (ICERs)"
at the first use of ICER in the secondary-outcomes paragraph (1b: the first definition stays in that paragraph).

Order: 1f renumbering of the tables and supplementary tables in the retained v13 text (Table 2 -> Table 3; Table S4-S10
-> S5-S11; Tables S1-S10 -> S1-S11; old Table 3 was cited only in the deleted Pembrolizumab section), then 1a-1e,
then 1g (abstract Results; --trim N applies the first N cuts of the instruction), then 1h (--wc ABSTRACT,MAIN).

usage: python edit_manuscript_v14.py <v13.docx> <out.docx> <log.json> [--trim N] [--wc ABSTRACT,MAIN]
"""
import copy, hashlib, json, re, sys, zipfile
from lxml import etree

V13_SHA16 = "4178320b77709506"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
XS = "{http://www.w3.org/XML/1998/namespace}space"

# ---- texts of the instruction (inserted as given)
T_1A = ("This study aimed to place a structured exercise program during neoadjuvant chemotherapy for stage II or III TNBC on "
        "the same cost-effectiveness scale as pembrolizumab, from the perspective of the Japanese public healthcare payer. It "
        "compared the four strategies formed by chemotherapy with or without pembrolizumab and with or without exercise; it asked "
        "how large an effect on recurrence exercise would need to match pembrolizumab, in quality-adjusted life years (QALYs) and "
        "in net benefit; and, as its main aim, it estimated the maximum cost per patient at which exercise added to chemotherapy "
        "with pembrolizumab would be cost-effective, and how this cost depends on the size and duration of the effect of exercise "
        "on recurrence. Expressing the value of an unproven program as the cost a health system can afford for each possible "
        "effect gives future trials a benchmark for their results.")
T_1B_GIVEN = ("Secondary outcomes were the total costs and QALYs of the four arms and the ICERs between them at recurrence HRs of "
              "0.95, 0.85 and 0.72; the ICER of pembrolizumab against chemotherapy alone; the exercise effect, as a recurrence HR "
              "or an increase in pCR, at which exercise added to chemotherapy alone would gain as many QALYs as pembrolizumab, or "
              "the same net monetary benefit, the QALYs gained valued at the threshold minus the incremental cost; the recurrence "
              "HRs at which the maximum affordable cost, or the medical costs avoided, equaled the cost of a program; and the "
              "one-year net benefit, the maximum affordable cost minus the program cost summed over eligible patients treated in "
              "Japan in one year.")
ICER_DEF = ("the ICERs between them", "the incremental cost-effectiveness ratios (ICERs) between them")
T_1C2 = ("(2) To compare the four arms, the model was run at recurrence HRs of 0.95, 0.85 and 0.72 with the fee-schedule-based "
         "program. Arms were ordered by total cost; an arm that cost more and gave fewer QALYs than another was dominated, an arm "
         "whose ICER against the next cheaper arm exceeded the ICER of the next more effective arm was extendedly dominated, and "
         "ICERs were calculated between the remaining arms.")
T_1C3 = ("(3) To estimate the maximum affordable cost, the model was run at recurrence HRs from 0.70 to 1.00 in steps of 0.025 "
         "and at increases in pCR from 0 to 10 percentage points in steps of 1. Break-even HRs and the exercise effects matching "
         "the QALY gain or the net monetary benefit of pembrolizumab were found numerically, over HRs from 0.30 to 1.00 and "
         "increases in pCR of up to 37 percentage points.")
H_R1 = "Four strategies compared"
T_R1 = ("Table 2 shows the four strategies at recurrence HRs with exercise of 0.95, 0.85 and 0.72, with the fee-schedule-based "
        "program. At each HR, chemotherapy plus exercise cost less and gave more QALYs than chemotherapy alone, and chemotherapy "
        "plus pembrolizumab plus exercise cost less and gave more QALYs than chemotherapy plus pembrolizumab, so both strategies "
        "without exercise were dominated. Adding pembrolizumab to chemotherapy plus exercise cost JPY 2,112 thousand per QALY at "
        "an HR of 0.95, JPY 2,245 thousand at 0.85 and JPY 2,449 thousand at 0.72. Relative to chemotherapy alone, the net "
        "monetary benefit of exercise at JPY 5 million per QALY was JPY 931 thousand at an HR of 0.95, JPY 3,250 thousand at 0.85 "
        "and JPY 6,413 thousand at 0.72, against JPY 6,355 thousand for pembrolizumab. Chemotherapy with both had the highest net "
        "monetary benefit at every HR.")
H_R2 = "Exercise compared with pembrolizumab"
T_R2 = ("Table 2 also shows pembrolizumab against chemotherapy alone: it cost JPY 4,426 thousand more per patient (95% UI "
        "[−330, 8,901]) and added 2.156 QALYs (95% UI [0.245, 4.228]), an ICER of JPY 2,053 thousand per QALY, and it was "
        "cost-effective in 83.1% of probabilistic samples at JPY 5 million and 90.8% at JPY 7.5 million per QALY. Its drug cost "
        "of JPY 6,531 thousand was offset partly by JPY −1,911 thousand in second-line and later treatment of distant "
        "recurrence (Table S4). To gain as many QALYs as pembrolizumab, exercise added to chemotherapy alone required a recurrence "
        "HR of 0.425 or an increase in pCR of 35.9 percentage points (Table 2). To give the same net monetary benefit with the "
        "fee-schedule-based program, it required an HR of 0.722 or an increase in pCR of 19.0 percentage points at JPY 5 million "
        "per QALY, and an HR of 0.638 or an increase of 24.1 percentage points at JPY 7.5 million. Except the HR of 0.722, these "
        "values lay outside the ranges studied.")
T_SENS = ("The ICER of pembrolizumab was JPY 3,044 thousand per QALY with Japanese post-operative treatment, JPY 2,565 thousand "
          "with metastatic treatment costs halved, JPY 2,785 thousand with eribulin-based treatment and JPY 1,920 thousand with "
          "higher mortality after early recurrence with pembrolizumab (Table S4).")
T_D1 = ("At each of the three effect sizes examined, both strategies without exercise were dominated (Table 2), so the choice in "
        "Japan is not between exercise and pembrolizumab. Pembrolizumab remained cost-effective on top of exercise, and "
        "chemotherapy with both gave the most health for the money at every effect size.")
T_D2 = ("Exercise cannot replace pembrolizumab in health gained: it would need to lower the recurrence hazard by more than half, "
        "far beyond the effects reported in exercise trials [9,14]. In value for money the gap is narrower, because the program "
        "costs a small fraction of the pembrolizumab regimen. At the Japanese threshold, exercise added to chemotherapy alone "
        "would give the same net benefit as pembrolizumab with an effect the size of that in CHALLENGE, a 28% reduction in the "
        "recurrence hazard, and at the higher threshold reserved for designated products pembrolizumab keeps its lead unless "
        "exercise cuts the hazard by more than a third. The effect of pembrolizumab is established and that of exercise is not, "
        "so a payer choosing one would still choose pembrolizumab; the comparison shows how much health a cheap program could buy "
        "if its effect were confirmed.")
T_D3 = ("For patients who receive pembrolizumab, now most patients in Japan [7], the question is what a program added to their "
        "treatment may cost. Whether exercise during neoadjuvant chemotherapy for stage II or III TNBC reduces recurrence is "
        "unknown; if it does, even a small effect would make a structured program cost-effective: the fee-schedule-based program "
        "became cost-effective once it lowered the recurrence hazard by 1.1%. How much a program could cost depended mostly on "
        "how large its effect was and how long it lasted.")
T_D4 = ("The maximum affordable cost was higher without pembrolizumab, because more patients relapse and the same relative effect "
        "prevents more recurrences. Pembrolizumab itself was cost-effective in Japan, as in other countries [28–31], and its "
        "ICER depended most on its price and on post-operative capecitabine or olaparib as used in Japanese practice.")
T_ABS_R = ("At recurrence HRs of 0.95, 0.85 and 0.72, both strategies without exercise were dominated. Pembrolizumab cost JPY "
           "2,053 thousand per QALY; exercise would need an HR of 0.425 to match its QALY gain and 0.722 to match its net benefit. "
           "Added to chemotherapy plus pembrolizumab, exercise had a maximum affordable cost of JPY 2,726 thousand per patient at "
           "an HR of 0.85 (95% uncertainty interval [2,223, 3,040]). A program priced from the medical fee schedule (JPY 192,400) "
           "became cost-effective at an HR of 0.989, and medical costs avoided alone paid for it at HRs of 0.958 to 0.914, "
           "depending on metastatic treatment costs. The duration of the effect changed the maximum affordable cost more than any "
           "cost input.")
# 1g cuts, in the order of the instruction: (paragraph label, old, new)
TRIMS = [("Methods", "of 0.70 to 1.00, with alternative durations", "of 0.70 to 1.00"),
         ("Results", "JPY 2,726 thousand per patient at", "JPY 2,726 thousand at"),
         ("Results", ", depending on metastatic treatment costs", ""),
         ("Results", "The duration of the effect changed the maximum affordable cost more than any cost input.",
          "Effect duration changed the maximum affordable cost more than any cost input.")]


def q(tag):
    return "{%s}%s" % (W, tag)


def text_nodes(p):
    return [t for r in p.iter(q("r")) for t in r.findall("w:t", NS)]


def ptext(p):
    return "".join(t.text or "" for t in text_nodes(p))


def edit_span(p, k, end, new):
    """Replace characters k..end of the paragraph text by new (k == end: insert at k). The new text goes into the first
    run overlapping the span (for an insertion, the run holding position k; at the very end, the last run)."""
    spans, pos = [], 0
    for t in text_nodes(p):
        s = t.text or ""
        spans.append((t, pos, pos + len(s)))
        pos += len(s)
    if k == end:
        for t, a, b in spans:
            if a <= k < b or (k == b == pos):
                s = t.text or ""
                t.text = s[:k - a] + new + s[k - a:]
                t.set(XS, "preserve")
                return
        raise AssertionError(("insertion point not found", k))
    first = True
    for t, a, b in spans:
        if a < end and b > k:
            s = t.text or ""
            lo, hi = max(k, a) - a, min(end, b) - a
            t.text = (s[:lo] + new + s[hi:]) if first else (s[:lo] + s[hi:])
            first = False
            t.set(XS, "preserve")
    assert not first, ("span not placed", k, end)


def replace_in_para(p, old, new):
    full = ptext(p)
    assert full.count(old) == 1, ("not unique in paragraph", old)
    k = full.find(old)
    edit_span(p, k, k + len(old), new)
    assert ptext(p) == full.replace(old, new)


def set_text(p, text):
    """Whole paragraph text replaced; the formatting of the first text run is kept, other runs removed."""
    rs = [r for r in p.findall("w:r", NS) if r.find("w:t", NS) is not None]
    assert rs, "no text run"
    for r in rs[1:]:
        p.remove(r)
    ts = rs[0].findall("w:t", NS)
    for t in ts[1:]:
        rs[0].remove(t)
    ts[0].text = text
    ts[0].set(XS, "preserve")
    assert ptext(p) == text


REN = re.compile(r"Tables S1–S10\b|\bTable S(\d+)\b|\bTable (\d+)\b")


def renumber(p):
    """1f mapping on one paragraph of v13 text; returns the list of (old, new) applied (right to left)."""
    full = ptext(p)
    done = []
    for m in reversed(list(REN.finditer(full))):
        s = m.group(0)
        if s.startswith("Tables S1"):
            new = "Tables S1–S11"
        elif m.group(1):
            n = int(m.group(1)); new = "Table S%d" % (n + 1 if n >= 4 else n)
        else:
            n = int(m.group(2))
            assert n != 3, "Table 3 outside the deleted section: " + full[:80]
            new = "Table 3" if n == 2 else s
        if new != s:
            edit_span(p, m.start(), m.end(), new)
            done.append((s, new))
    return done[::-1]


def main(src, dst, logpath, trim=0, wc=None):
    raw = open(src, "rb").read()
    assert hashlib.sha256(raw).hexdigest()[:16] == V13_SHA16, "v13 sha256 differs"
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    body = doc.find("w:body", NS)
    log = []

    def paras():
        return [p for p in body if p.tag == q("p")]

    def find(start=None, contains=None, exact=None):
        P = paras()
        if exact is not None:
            hits = [p for p in P if ptext(p) == exact]
        elif start is not None:
            hits = [p for p in P if ptext(p).startswith(start)]
        else:
            hits = [p for p in P if contains in ptext(p)]
        assert len(hits) == 1, ("not unique or not found", start, contains, exact, len(hits))
        return hits[0]

    def new_after(anchor, template, text):
        p = copy.deepcopy(template)
        set_text(p, text)
        anchor.addnext(p)
        return p

    # ---- 1f: renumbering in the v13 text, after removing the Pembrolizumab section (its old Table 3 is gone)
    h_pem = find(exact="Pembrolizumab")
    p53 = find(start="Pembrolizumab added JPY 4,426 thousand per patient in costs")
    p54 = find(start="To gain as many QALYs as pembrolizumab, exercise added to chemotherapy alone required")
    assert h_pem.getnext() is p53 and p53.getnext() is p54
    for p in (h_pem, p53, p54):
        log.append({"step": "1d delete", "para_before": ptext(p), "para_after": None})
        body.remove(p)
    for p in paras():
        before = ptext(p)
        d = renumber(p)
        if d:
            log.append({"step": "1f", "changes": d, "para_before": before, "para_after": ptext(p)})

    def replace_para(step, start, text):
        p = find(start=start)
        before = ptext(p)
        set_text(p, text)
        log.append({"step": step, "para_before": before, "para_after": text})
        return p

    # ---- 1a Introduction, last paragraph
    replace_para("1a", "This study estimated, from the perspective of the Japanese public healthcare payer", T_1A)
    # ---- 1b Outcomes, paragraph 2 (ICER defined at its first use; v13 defined it in this paragraph)
    assert T_1B_GIVEN.count(ICER_DEF[0]) == 1 and T_1B_GIVEN.find(ICER_DEF[0]) < T_1B_GIVEN.find("ICER of pembrolizumab")
    replace_para("1b", "Secondary outcomes were", T_1B_GIVEN.replace(ICER_DEF[0], ICER_DEF[1]))
    # ---- 1c Statistical analysis: old (2) -> new (2) and (3); old (3)-(6) -> (4)-(7)
    p2 = replace_para("1c", "(2) To estimate the maximum affordable cost", T_1C2)
    p3 = new_after(p2, p2, T_1C3)
    log.append({"step": "1c insert", "para_before": None, "para_after": T_1C3})
    for old_n in (6, 5, 4, 3):
        p = find(start="(%d) To " % old_n) if old_n != 3 else find(start="(3) To reflect uncertainty")
        before = ptext(p)
        edit_span(p, 0, 3, "(%d)" % (old_n + 1))
        log.append({"step": "1c renumber", "para_before": before, "para_after": ptext(p)})
    # ---- 1d Results: two new sections first
    h_max = find(exact="Maximum affordable cost of exercise")
    h_res = find(exact="Results")
    body_tpl = find(start="Exercise added to chemotherapy alone had a maximum affordable cost of JPY 3,443")
    assert h_res.getnext() is h_max
    a = new_after(h_res, h_max, H_R1)
    b = new_after(a, body_tpl, T_R1)
    c = new_after(b, h_max, H_R2)
    d_ = new_after(c, body_tpl, T_R2)
    for x in (a, b, c, d_):
        log.append({"step": "1d insert", "para_before": None, "para_after": ptext(x)})
    p56 = find(start="The monthly cost of second-line and later treatment moved the maximum affordable cost")
    before = ptext(p56)
    assert before.endswith("(Fig. S2).")
    edit_span(p56, len(before), len(before), " " + T_SENS)
    log.append({"step": "1d append", "para_before": before, "para_after": ptext(p56)})
    # ---- 1e Discussion: paragraph 1 -> three paragraphs; paragraph 4 -> one
    d1 = replace_para("1e", "Whether exercise during neoadjuvant chemotherapy for stage II or III TNBC reduces recurrence is unknown. If it does",
                      T_D1)
    d2 = new_after(d1, d1, T_D2)
    d3 = new_after(d2, d1, T_D3)
    for x in (d2, d3):
        log.append({"step": "1e insert", "para_before": None, "para_after": ptext(x)})
    replace_para("1e", "Exercise cannot replace pembrolizumab: it would need", T_D4)
    # ---- 1g abstract Results (label run kept), then the cuts
    pr = find(start="Results Added to chemotherapy plus pembrolizumab")
    before = ptext(pr)
    k = len("Results ")
    edit_span(pr, k, len(before), T_ABS_R)
    assert ptext(pr) == "Results " + T_ABS_R
    log.append({"step": "1g", "para_before": before, "para_after": ptext(pr)})
    for i, (lab, old, new) in enumerate(TRIMS[:trim], 1):
        p = find(start=lab + " ") if lab != "Methods" else find(start="Methods A state-transition model")
        before = ptext(p)
        replace_in_para(p, old, new)
        log.append({"step": "1g cut %d" % i, "para_before": before, "para_after": ptext(p)})
    # ---- 1h word count line
    if wc:
        p = find(start="Word count: abstract ")
        before = ptext(p)
        m = re.match(r"Word count: abstract (\d+); main text ([\d,]+) \(", before)
        assert m and before.endswith("; 3 tables; 3 figures; 1 Online Resource")
        replace_in_para(p, m.group(0), "Word count: abstract %d; main text %s (" % (wc[0], f"{wc[1]:,}"))
        log.append({"step": "1h", "para_before": before, "para_after": ptext(p)})

    head = xml.split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("log entries:", len(log), "| trim", trim, "| wc", wc)


if __name__ == "__main__":
    a = sys.argv[1:]
    trim, wc = 0, None
    if "--trim" in a:
        i = a.index("--trim"); trim = int(a[i + 1]); a = a[:i] + a[i + 2:]
    if "--wc" in a:
        i = a.index("--wc"); wc = tuple(int(x) for x in a[i + 1].split(",")); a = a[:i] + a[i + 2:]
    main(a[0], a[1], a[2], trim, wc)
