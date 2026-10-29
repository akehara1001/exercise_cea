"""v12 = direct edit of manuscript_v11_BCRT.docx, instruction steps 1a-1e. Only word/document.xml is rewritten;
every other part is copied byte for byte. Each original string must occur exactly once in v11 or the script stops.

usage: python edit_manuscript_v12.py <v11.docx> <out.docx> <log.json> [--wc ABSTRACT,MAIN]
"""
import copy, hashlib, json, sys, zipfile
from lxml import etree

V11_SHA16 = "58b6897ab597a714"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
XS = "{http://www.w3.org/XML/1998/namespace}space"


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
        t.set(XS, "preserve")


def main(src, dst, logpath, wc=None):
    raw = open(src, "rb").read()
    assert hashlib.sha256(raw).hexdigest()[:16] == V11_SHA16, "v11 sha256 differs"
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

    # 1a Abstract, Methods
    rep("1a", "The analysis took the Japanese payer perspective over a lifetime, discounting at 2% per year.",
        "It took the Japanese payer perspective over a lifetime, discounting at 2% annually.")
    rep("1a", "The maximum affordable cost was the threshold of JPY 5 million per quality-adjusted life year (QALY)",
        "The maximum affordable cost was the threshold of 5 million Japanese yen (JPY) per quality-adjusted life year (QALY)")
    # 1b Study design paragraph 2
    rep("1b", "The willingness-to-pay threshold for exercise was JPY 5 million per QALY [41,42];",
        "The willingness-to-pay threshold for exercise was 5 million Japanese yen (JPY) per QALY [41,42];")

    # 1c Exercise effect and costs paragraph 1 split after "and the effect held until it stopped."
    ih = [i for i, p in enumerate(P) if ptext(p) == "Exercise effect and costs"]
    assert len(ih) == 1
    p1 = P[ih[0] + 1]
    full = ptext(p1)
    cut = "and the effect held until it stopped. "
    assert full.startswith("The exposure was the recurrence HR with exercise:") and full.count(cut) == 1
    k = full.index(cut) + len(cut) - 1
    first, second = full[:k], full[k + 1:]
    assert second.startswith("In an alternative pathway, ") and second.endswith(
        "Musculoskeletal adverse events occurred at the rates observed in CHALLENGE [9].")
    assert ptext(P[ih[0] + 2]).startswith("Three programs were costed")
    rt = runs_t(p1)
    assert len(rt) == 1
    p2 = copy.deepcopy(p1)
    rt[0][1].text = first
    (_, t2), = runs_t(p2)
    t2.text = second
    t2.set(XS, "preserve")
    p1.addnext(p2)
    assert ptext(p1) + " " + ptext(p2) == full
    log.append({"step": "1c", "para_before": full, "para_1_after": ptext(p1), "para_2_after": ptext(p2)})
    P = [p for p in body if p.tag == q("p")]

    # 1d references 10, 28, 58, 65
    rep("1d", "Cochrane Database Syst Rev 9:CD005001", "Cochrane Database Syst Rev 2016(9):CD005001")
    rep("1d", "Huang M, A Fasching P, Haiderali A", "Huang M, Fasching PA, Haiderali A")
    rep("1d", "the current evidence?. Br J Cancer", "the current evidence? Br J Cancer")
    rep("1d", "https://www.pbs.gov.au/info/industry/listing/elements/pbac-meetings/psd/2023-03/pembrolizumab-earlyTNBC-keytruda-PSD-March-2023. Accessed 26 Oct 2026",
        "https://www.pbs.gov.au/industry/pbac/psd/2023/03/pembrolizumab-march-2023-a661. Accessed 29 Oct 2026")

    # 1e word count line (numbers only)
    if wc:
        a, m = wc
        rep("1e", "Word count: abstract 250; main text 3,242 (", "Word count: abstract %d; main text %s (" % (a, f"{m:,}"))

    head = zin.read("word/document.xml").split(b"?>", 1)[0] + b"?>"
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
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
