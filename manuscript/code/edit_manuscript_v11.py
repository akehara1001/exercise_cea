"""v11 = direct edit of Dr Ozaki's BCRT v10 docx (manuscript_v10_BCRT.docx), instruction steps 1a-1m and the
section 8 font-size fix (WRITING_RULES). Only document.xml, styles.xml and footer1.xml are rewritten; every other part
is copied byte for byte. Each original string must occur exactly once in v10 or the script stops.

usage: python edit_manuscript_v11.py <v10.docx> <out.docx> <log.json> [--wc ABSTRACT,MAIN]
"""
import copy, hashlib, json, re, sys, zipfile
from lxml import etree

V10_SHA16 = "ec20edacf2c278e2"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def q(tag):
    return "{%s}%s" % (W, tag)


def runs_t(p):
    """(run, t) pairs of the text runs of a paragraph, in order."""
    out = []
    for r in p.iter(q("r")):
        for t in r.findall("w:t", NS):
            out.append((r, t))
    return out


def ptext(p):
    return "".join(t.text or "" for _, t in runs_t(p))


def replace_in_para(p, old, new):
    """Replace one occurrence of old in the paragraph text; the match may span runs (text goes to the first run)."""
    rt = runs_t(p)
    full = "".join(t.text or "" for _, t in rt)
    k = full.find(old)
    assert k >= 0 and full.count(old) == 1, old
    end = k + len(old)
    pos = 0
    first = True
    for _, t in rt:
        s = t.text or ""
        a, b = pos, pos + len(s)
        pos = b
        if b <= k or a >= end:
            continue
        lo, hi = max(k, a) - a, min(end, b) - a
        if first:
            t.text = s[:lo] + new + s[hi:]
            first = False
        else:
            t.text = s[:lo] + s[hi:]
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")


def main(src, dst, logpath, wc=None):
    raw = open(src, "rb").read()
    assert hashlib.sha256(raw).hexdigest()[:16] == V10_SHA16, "v10 sha256 differs"
    zin = zipfile.ZipFile(src)
    doc = etree.fromstring(zin.read("word/document.xml"))
    body = doc.find("w:body", NS)
    P = [p for p in body if p.tag == q("p")]
    log = []

    def find_unique(old):
        hits = [p for p in P if old in ptext(p)]
        assert len(hits) == 1 and ptext(hits[0]).count(old) == 1, ("not unique or not found", old, len(hits))
        return hits[0]

    def rep(step, old, new):
        p = find_unique(old)
        before = ptext(p)
        replace_in_para(p, old, new)
        after = ptext(p)
        assert after == before.replace(old, new)
        log.append({"step": step, "old": old, "new": new, "para_before": before, "para_after": after})

    # 1a Introduction paragraph 2
    rep("1a", "In the CHALLENGE trial, structured exercise for 3 years after adjuvant chemotherapy for colon cancer prolonged disease-free survival, with a hazard ratio (HR) of 0.72 (95% confidence interval [CI] 0.55–0.94) [9].",
        "In the CHALLENGE trial [9], structured exercise for 3 years after adjuvant chemotherapy for colon cancer prolonged disease-free survival, with a hazard ratio (HR) of 0.72 (95% confidence interval (CI) [0.55, 0.94]).")
    rep("1a", "and an exploratory follow-up of one trial found an HR for disease-free survival of 0.68 (95% CI 0.37–1.24) [14].",
        "and an exploratory follow-up of one trial [14] found an HR for disease-free survival of 0.68 (95% CI [0.37, 1.24]).")
    # 1b Introduction paragraph 3
    rep("1b", "No economic evaluation of exercise during neoadjuvant therapy for breast cancer was identified; the nearest,",
        "Searches of PubMed and Europe PMC covering 2000 to 2026 identified no economic evaluation of exercise during neoadjuvant therapy for breast cancer (Supplementary Methods S1); the nearest,")
    # 1c, 1d Study design
    rep("1c", "The analysis took the Japanese public healthcare payer perspective and a lifetime horizon.",
        "The analysis took the Japanese public healthcare payer perspective and a lifetime horizon, to capture differences in survival.")
    rep("1d", "Supplementary Methods, Tables S1–S10", "Supplementary Methods S1, Tables S1–S10")
    # 1e Exercise effect and costs paragraph 1
    rep("1e", "In the base case, the HR held for 5 years after randomization and the effect then halved every year.",
        "In the base case, the HR held for 5 years after randomization; after that, the reduction in the hazard, 1 − HR, halved every year.")
    rep("1e", "In an alternative pathway, exercise raised pCR by 0 to 10 percentage points without changing the recurrence HR.",
        "In an alternative pathway, exercise raised pCR by 0 to 10 percentage points without changing the recurrence HR; patients added to the pCR group took the event-free survival of patients with pCR given the same treatment.")
    # 1f Survival, costs and utilities paragraph 1
    s44 = "with 7-year values in each stratum fixed at those of the final analysis [44]."
    rep("1f", s44, s44 + " The distributions, a Weibull model for patients with pCR and a Weibull mixture cure model for patients without pCR, were chosen by the fit and plausibility criteria in Supplementary Methods S1.")

    # 1g Statistical analysis: all paragraphs under the subheading replaced by 8 paragraphs
    ih = [i for i, p in enumerate(P) if ptext(p) == "Statistical analysis"]
    ir = [i for i, p in enumerate(P) if ptext(p) == "Results"]
    assert len(ih) == 1 and len(ir) == 1
    old_ps = P[ih[0] + 1:ir[0]]
    old_txt = [ptext(p) for p in old_ps]
    assert old_txt[0].startswith("The model used 1-month cycles") and old_txt[-1].endswith("Analyses were performed in R version 4.5.1."), old_txt
    assert len(old_ps) == 3
    new_paras = [
        "The model used 1-month cycles from the start of neoadjuvant therapy to age 100 years, with the cohort split by pCR at surgery in month 7 (Fig. 1).",
        "(1) To check that the model reproduced the trial, overall survival, which was not used to build the survival model, was compared with KEYNOTE-522 against acceptance criteria fixed before each comparison [5,44] (Supplementary Methods S1; Fig. S1; Table S3).",
        "(2) To estimate the maximum affordable cost, the model was run at recurrence HRs from 0.70 to 1.00 in steps of 0.025 and at increases in pCR from 0 to 10 percentage points in steps of 1. Break-even HRs and the exercise effect matching the QALY gain of pembrolizumab were found numerically, over HRs from 0.30 to 1.00 and increases in pCR of up to 37 percentage points.",
        "(3) To reflect uncertainty, each of 1,000 probabilistic samples paired one bootstrap replicate of the survival model with one draw of the other inputs. Costs, durations and events per patient followed gamma distributions, proportions and utilities beta distributions, and HRs lognormal distributions; drug prices and rates based on zero events were fixed. The 2.5th and 97.5th percentiles of the samples gave the 95% uncertainty interval (UI). The probability that a program was cost-effective was the share of samples in which the maximum affordable cost exceeded the program cost. For pembrolizumab, it was the share of samples with a positive net monetary benefit at each threshold.",
        "(4) To find the inputs that move the results most, one-way sensitivity analyses set each input to its lower and upper bounds, for the maximum affordable cost in the main comparison at an HR of 0.85 and for the ICER of pembrolizumab. Where a source gave no range, the range was ±25% of the base value or the missing bound mirrored the given one; drug prices varied downward only, to 75% of the list price.",
        "(5) To test other assumptions, scenario analyses changed one assumption at a time (Table 1): utility values from the United States, United Kingdom and Australian analyses [28,29,65]; higher excess mortality after early recurrence with pembrolizumab, from an Italian cohort [66]; longer survival after progression during neoadjuvant therapy [67]; halved costs of metastatic treatment; eribulin-based later-line treatment [68]; and post-operative capecitabine or olaparib for patients without pCR [69–71].",
        "(6) To express the result for Japan, the one-year net benefit used the fee-schedule-based program at recurrence HRs of 0.95, 0.90 and 0.85, applying the main comparison to patients who received neoadjuvant pembrolizumab in the 2024 national registry and the secondary comparison to the others [7]; these values are conditional on the HR.",
        "Analyses were performed in R version 4.5.1.",
    ]
    tmpl = old_ps[0]
    assert len(runs_t(tmpl)) == 1
    anchor = old_ps[0]
    built = []
    for txt in new_paras:
        np_ = copy.deepcopy(tmpl)
        (_, t), = runs_t(np_)
        t.text = txt
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        anchor.addprevious(np_)
        built.append(np_)
    for p in old_ps:
        body.remove(p)
    log.append({"step": "1g", "old_paragraphs": old_txt, "new_paragraphs": [ptext(p) for p in built]})
    P = [p for p in body if p.tag == q("p")]

    # 1h Implications
    rep("1h", "For pembrolizumab, this analysis gives Japan a reference value before any formal evaluation.",
        "For pembrolizumab, this analysis gives Japan a reference value before any formal evaluation of its perioperative indication.")
    # 1i intervals in square brackets (abstract and text)
    for old, new in [
        ("(95% uncertainty interval 2,223–3,040)", "(95% uncertainty interval [2,223, 3,040])"),
        ("(95% UI 2,223–3,040; Table 2)", "(95% UI [2,223, 3,040]; Table 2)"),
        ("(95% UI 4,545–6,256; Table S4)", "(95% UI [4,545, 6,256]; Table S4)"),
        ("(95% UI 238–570)", "(95% UI [238, 570])"),
        ("(95% UI 2,388–5,713; Table S5)", "(95% UI [2,388, 5,713]; Table S5)"),
        ("(95% UI 2,881–3,785)", "(95% UI [2,881, 3,785])"),
        ("(95% UI 2.22–2.94)", "(95% UI [2.22, 2.94])"),
        ("(95% UI 8.15–10.36; Table S8)", "(95% UI [8.15, 10.36]; Table S8)"),
        ("(95% UI −330 to 8,901)", "(95% UI [−330, 8,901])"),
        ("(95% UI 0.245–4.228)", "(95% UI [0.245, 4.228])"),
        ("(95% UI 2,201–2,994)", "(95% UI [2,201, 2,994])"),
    ]:
        rep("1i", old, new)
    # 1j remaining "Supplementary Methods" without S1 in the text
    n1j = 0
    for p in P:
        tx = ptext(p)
        for m in list(re.finditer(r"Supplementary Methods(?! S1)", tx)):
            n1j += 1
    log.append({"step": "1j", "remaining_without_S1_before_fix": n1j})
    assert n1j == 0, "1j: occurrences left; handle explicitly"
    # 1k reference 73
    rep("1k", "[URL to be added]. Accessed 28 Oct 2026",
        "https://www.daiichisankyo.com/files/news/pressrelease/pdf/202609/20260916_E.pdf. Accessed 28 Oct 2026")
    # 1l Data availability
    rep("1l", "[To be confirmed: The model code is available from the corresponding author on reasonable request.]",
        "The R code of the model, its input file and the patient-level data reconstructed from published survival curves are available at https://github.com/akehara1001/exercise-cea-tnbc.")
    # 1m word count line (numbers only)
    if wc:
        a, m = wc
        rep("1m", "Word count: abstract 250; main text 3,022 (", "Word count: abstract %d; main text %s (" % (a, f"{m:,}"))

    # section 8: every run, paragraph mark and footer at 12 pt (sz 24)
    nsz = {"20": 0, "28": 0, "other": 0}
    for el in doc.iter(q("sz"), q("szCs")):
        v = el.get(q("val"))
        nsz[v if v in nsz else "other"] += 1
        el.set(q("val"), "24")
    log.append({"step": "fmt", "document_sz_elements_set_to_24": nsz})

    styles = etree.fromstring(zin.read("word/styles.xml"))
    dd = styles.find("w:docDefaults/w:rPrDefault/w:rPr", NS)
    for el in dd:
        if el.tag in (q("sz"), q("szCs")):
            assert el.get(q("val")) == "20"
            el.set(q("val"), "24")
    footer = etree.fromstring(zin.read("word/footer1.xml"))
    nf = 0
    for el in footer.iter(q("sz"), q("szCs")):
        el.set(q("val"), "24"); nf += 1
    log.append({"step": "fmt", "docDefaults_sz": "20->24", "footer_sz_elements": nf})

    def ser(root, orig):
        head = orig.split(b"?>", 1)[0] + b"?>"
        return head + etree.tostring(root, encoding="UTF-8", xml_declaration=False)

    repl = {"word/document.xml": doc, "word/styles.xml": styles, "word/footer1.xml": footer}
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename in repl:
                data = ser(repl[info.filename], data)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("edits:", len(log))


if __name__ == "__main__":
    a = sys.argv[1:]
    wc = None
    if "--wc" in a:
        i = a.index("--wc")
        wc = tuple(int(x) for x in a[i + 1].split(","))
        a = a[:i] + a[i + 2:]
    main(a[0], a[1], a[2], wc)
