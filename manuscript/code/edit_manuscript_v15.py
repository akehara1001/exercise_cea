"""v15 = direct edit of manuscript_v14_BCRT.docx by the v15 instruction (2026-11-04): 1a-1n (cuts and corrections),
reference 71 (step 2; reference 8 unchanged, see worklog), backup cuts (--backup N, step 1o) and the word count line
(--wc ABSTRACT,MAIN). Only word/document.xml is rewritten. Every original string must occur exactly once in one
paragraph of v14 or the script stops. Texts of the instruction are constants below, inserted as given.

usage: python edit_manuscript_v15.py <v14.docx> <out.docx> <log.json> [--backup N] [--wc ABSTRACT,MAIN]
"""
import copy, hashlib, json, os, re, sys, zipfile
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edit_manuscript_v14 import NS, q, ptext, edit_span, replace_in_para, set_text  # noqa: E402

V14_SHA16 = "bd741f343a4e3d6e"
MINUS = "−"
EN = "–"

# (step, unique locator of the paragraph = the original string itself, original, new)
REPL = [
    ("1a", "The main comparison was exercise added to chemotherapy plus pembrolizumab against chemotherapy plus pembrolizumab; the "
           "secondary comparison was exercise added to chemotherapy alone against chemotherapy alone. Both treatments were in use in "
           "Japan in 2024 [7]. Chemotherapy plus pembrolizumab against chemotherapy alone formed the reference comparison.",
           "The main comparison was exercise added to chemotherapy plus pembrolizumab against the same treatment without exercise, the "
           "secondary comparison exercise added to chemotherapy alone, and the reference comparison chemotherapy plus pembrolizumab "
           "against chemotherapy alone."),
    ("1b", "Medical costs avoided were the incremental medical costs other than the program cost, with the sign reversed.",
           "Medical costs avoided were these incremental costs with the sign reversed."),
    ("1d", "Arms were ordered by total cost; an arm that cost more and gave fewer QALYs than another was dominated, an arm whose ICER "
           "against the next cheaper arm exceeded the ICER of the next more effective arm was extendedly dominated, and ICERs were "
           "calculated between the remaining arms.",
           "Arms were ordered by total cost; an arm that cost more and gave fewer QALYs than another, or whose ICER exceeded that of the "
           "next more effective arm, was dominated, and ICERs were calculated between the remaining arms."),
    ("1e", "Costs, durations and events per patient followed gamma distributions, proportions and utilities beta distributions, and "
           "HRs lognormal distributions; drug prices and rates based on zero events were fixed.",
           "Distributions of the other inputs are listed in Table S2."),
    ("1f", "[7]; these values are conditional on the HR.", "[7]."),
    ("1g", "Table 2 shows the four strategies at recurrence HRs with exercise of 0.95, 0.85 and 0.72, with the fee-schedule-based "
           "program. At each HR, chemotherapy plus exercise cost less and gave more QALYs than chemotherapy alone, and chemotherapy plus "
           "pembrolizumab plus exercise cost less and gave more QALYs than chemotherapy plus pembrolizumab, so both strategies without "
           "exercise were dominated.",
           "Table 2 shows the four strategies at recurrence HRs of 0.95, 0.85 and 0.72 with the fee-schedule-based program. At each HR, "
           "both strategies without exercise cost more and gave fewer QALYs than the same treatment with exercise, so they were "
           "dominated."),
    ("1h-1", "Table 2 also shows pembrolizumab against chemotherapy alone: it cost JPY 4,426 thousand more per patient (95% UI "
             "[" + MINUS + "330, 8,901]) and added 2.156 QALYs (95% UI [0.245, 4.228]), an ICER of JPY 2,053 thousand per QALY, and it "
             "was cost-effective in 83.1% of probabilistic samples at JPY 5 million and 90.8% at JPY 7.5 million per QALY.",
             "Table 2 also shows pembrolizumab against chemotherapy alone: it cost JPY 4,426 thousand more per patient and added 2.156 "
             "QALYs, an ICER of JPY 2,053 thousand per QALY."),
    ("1h-2", "Its drug cost of JPY 6,531 thousand was offset partly by JPY " + MINUS + "1,911 thousand in second-line and later "
             "treatment of distant recurrence (Table S4).",
             "Its drug cost was offset partly by savings in later-line treatment of distant recurrence (Table S4)."),
    ("1h-3", "To give the same net monetary benefit with the fee-schedule-based program, it required an HR of 0.722 or an increase in "
             "pCR of 19.0 percentage points at JPY 5 million per QALY, and an HR of 0.638 or an increase of 24.1 percentage points at "
             "JPY 7.5 million.",
             "To give the same net monetary benefit, it required an HR of 0.722 at JPY 5 million per QALY and 0.638 at JPY 7.5 million, "
             "or increases in pCR of 19.0 and 24.1 percentage points."),
    ("1i-1", "and at 0.70 it was JPY 5,596 thousand (95% UI [4,545, 6,256]; Table S5)", "and at 0.70 JPY 5,596 thousand (Table S5)"),
    ("1i-2", "Through pCR, an increase of 1 percentage point gave JPY 389 thousand (95% UI [238, 570]) and 10 points gave JPY 3,898 "
             "thousand (95% UI [2,388, 5,713]; Table S6).",
             "Through pCR, an increase of 10 percentage points gave JPY 3,898 thousand (95% UI [2,388, 5,713]; Table S6)."),
    ("1i-3", "At an HR of 0.85, incremental medical costs other than the program were JPY " + MINUS + "702 thousand per patient, of "
             "which second-line and later treatment of distant recurrence contributed JPY " + MINUS + "437 thousand and first-line "
             "treatment JPY " + MINUS + "254 thousand (Table S7).",
             "At an HR of 0.85, medical costs other than the program fell by JPY 702 thousand per patient, mostly in treatment of "
             "distant recurrence (Table S7)."),
    ("1i-4", "had a maximum affordable cost of JPY 3,443 thousand at an HR of 0.85 (95% UI [2,881, 3,785]).",
             "had a maximum affordable cost of JPY 3,443 thousand at an HR of 0.85."),
    ("1j", "The ICER of pembrolizumab was JPY 3,044 thousand per QALY with Japanese post-operative treatment, JPY 2,565 thousand with "
           "metastatic treatment costs halved, JPY 2,785 thousand with eribulin-based treatment and JPY 1,920 thousand with higher "
           "mortality after early recurrence with pembrolizumab (Table S4).",
           "The ICER of pembrolizumab ranged from JPY 1,920 thousand per QALY with higher mortality after early recurrence to JPY 3,044 "
           "thousand with Japanese post-operative treatment (Table S4)."),
    ("1k-1", "Pembrolizumab remained cost-effective on top of exercise, and chemotherapy with both gave the most health for the money "
             "at every effect size.",
             "Pembrolizumab remained cost-effective on top of exercise, as it is on its own in Japan and elsewhere [28" + EN + "31], "
             "and chemotherapy with both gave the most health for the money at every effect size."),
    ("1k-4", " Cheaper metastatic treatment reduced these savings but barely moved the point at which the program became "
             "cost-effective.", ""),
    ("1l", ", because how a change in pCR with exercise translates into fewer recurrences is unknown", ""),
    ("1m", "Several costs relied on expert input, but no single cost changed the conclusion (Fig. 3), and values from Japanese "
           "populations gave nearly the same results as the German value set.",
           "Several costs relied on expert input and utilities on a German value set, but neither changed the conclusion (Fig. 3; "
           "Table S11)."),
    ("1n", ", extracted from 21 to 26 October 2026", ""),
    ("2 ref 71", "OlympiA phase III trial. Ann Oncol (in press). https://doi.org/10.1016/j.annonc.2026.08.002",
                 "OlympiA phase III trial. Ann Oncol 37:1467" + EN + "1479. https://doi.org/10.1016/j.annonc.2026.08.002"),
]
T_1C = ("Secondary outcomes were the total costs and QALYs of the four arms and the incremental cost-effectiveness ratios (ICERs) "
        "between them at recurrence HRs of 0.95, 0.85 and 0.72; the ICER of pembrolizumab against chemotherapy alone; and the exercise "
        "effect, as a recurrence HR or an increase in pCR, at which exercise added to chemotherapy alone would gain as many QALYs as "
        "pembrolizumab, or the same net monetary benefit, the QALYs gained valued at the threshold minus the incremental cost. Further "
        "secondary outcomes were the recurrence HRs at which the maximum affordable cost, or the medical costs avoided, equaled the cost "
        "of a program, and the one-year net benefit, the maximum affordable cost minus the program cost summed over eligible patients "
        "treated in Japan in one year.")
T_1K2 = ("Exercise cannot replace pembrolizumab in health gained: it would need to lower the recurrence hazard by more than half, far "
         "beyond the effects reported in exercise trials [9,14]. In value for money the gap is narrower, because the program costs a "
         "small fraction of the pembrolizumab regimen: at the Japanese threshold, an effect the size of that in CHALLENGE would give the "
         "same net benefit as pembrolizumab, and at the higher threshold pembrolizumab keeps its lead unless exercise cuts the hazard by "
         "more than a third. The effect of pembrolizumab is established and that of exercise is not, so the comparison shows what a "
         "cheap program could be worth if its effect were confirmed.")
SPLIT_1M = "Survival was modeled from reconstructed data"
BACKUP = [("1o backup 1", " For pembrolizumab, this analysis gives Japan a reference value before any formal evaluation of its "
                          "perioperative indication.", ""),
          ("1o backup 2", " Chemotherapy with both had the highest net monetary benefit at every HR.", "")]


def main(src, dst, logpath, backup=0, wc=None):
    raw = open(src, "rb").read()
    assert hashlib.sha256(raw).hexdigest()[:16] == V14_SHA16, "v14 sha256 differs"
    zin = zipfile.ZipFile(src)
    xml = zin.read("word/document.xml")
    doc = etree.fromstring(xml)
    body = doc.find("w:body", NS)
    log = []

    def paras():
        return [p for p in body if p.tag == q("p")]

    def find_contains(s):
        hits = [p for p in paras() if s in ptext(p)]
        assert len(hits) == 1 and ptext(hits[0]).count(s) == 1, ("original not found exactly once in v14", s[:80], len(hits))
        return hits[0]

    def rep(step, old, new):
        p = find_contains(old)
        before = ptext(p)
        replace_in_para(p, old, new)
        log.append({"step": step, "old": old, "new": new, "para_before": before, "para_after": ptext(p)})

    for step, old, new in REPL:
        rep(step, old, new)
    # 1c Outcomes paragraph 2, whole paragraph
    p = [x for x in paras() if ptext(x).startswith("Secondary outcomes were the total costs and QALYs of the four arms")]
    assert len(p) == 1
    before = ptext(p[0]); set_text(p[0], T_1C)
    log.append({"step": "1c", "para_before": before, "para_after": T_1C})
    # 1k Discussion paragraph 2, whole paragraph; paragraph "The maximum affordable cost was higher without pembrolizumab" deleted
    p = [x for x in paras() if ptext(x).startswith("Exercise cannot replace pembrolizumab in health gained:")]
    assert len(p) == 1
    before = ptext(p[0]); set_text(p[0], T_1K2)
    log.append({"step": "1k-2", "para_before": before, "para_after": T_1K2})
    p = [x for x in paras() if ptext(x).startswith("The maximum affordable cost was higher without pembrolizumab,")]
    assert len(p) == 1
    log.append({"step": "1k-3 delete", "para_before": ptext(p[0]), "para_after": None})
    body.remove(p[0])
    # 1m Limitations: new paragraph from "Survival was modeled from reconstructed data" (text unchanged, same format)
    p = find_contains(SPLIT_1M)
    full = ptext(p)
    k = full.find(SPLIT_1M)
    assert k > 0 and full[k - 1] == " " and full[k - 2] == "."
    part1, part2 = full[:k - 1], full[k:]
    new = copy.deepcopy(p)
    set_text(p, part1)            # the paragraph is a single run (asserted by set_text through ptext)
    set_text(new, part2)
    p.addnext(new)
    log.append({"step": "1m split", "para_before": full, "para_after": part1})
    log.append({"step": "1m split", "para_before": None, "para_after": part2})
    # 1o backup cuts
    for step, old, new_ in BACKUP[:backup]:
        rep(step, old, new_)
    # 1o word count line
    if wc:
        p = [x for x in paras() if ptext(x).startswith("Word count: abstract ")]
        assert len(p) == 1
        before = ptext(p[0])
        m = re.match(r"Word count: abstract (\d+); main text ([\d,]+) \(", before)
        assert m and before.endswith("; 3 tables; 3 figures; 1 Online Resource")
        replace_in_para(p[0], m.group(0), "Word count: abstract %d; main text %s (" % (wc[0], f"{wc[1]:,}"))
        log.append({"step": "1o word count", "para_before": before, "para_after": ptext(p[0])})

    head = xml.split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("log entries:", len(log), "| backup", backup, "| wc", wc)


if __name__ == "__main__":
    a = sys.argv[1:]
    backup, wc = 0, None
    if "--backup" in a:
        i = a.index("--backup"); backup = int(a[i + 1]); a = a[:i] + a[i + 2:]
    if "--wc" in a:
        i = a.index("--wc"); wc = tuple(int(x) for x in a[i + 1].split(",")); a = a[:i] + a[i + 2:]
    main(a[0], a[1], a[2], backup, wc)
