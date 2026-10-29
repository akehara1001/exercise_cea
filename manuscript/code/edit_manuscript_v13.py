"""v13 = direct edit of manuscript_v12_BCRT.docx, instruction steps 1a-1b. Only word/document.xml is rewritten;
every other part is copied byte for byte. Each original string must occur exactly once in v12 or the script stops.

usage: python edit_manuscript_v13.py <v12.docx> <out.docx> <log.json> [--wc ABSTRACT,MAIN]
"""
import hashlib, json, sys, zipfile
from lxml import etree

V12_SHA16 = "3e2940475772e678"
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
    assert hashlib.sha256(raw).hexdigest()[:16] == V12_SHA16, "v12 sha256 differs"
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

    # 1a Study design paragraph 2 (withdraws v12 1b; the abstract definition stays)
    rep("1a", "The willingness-to-pay threshold for exercise was 5 million Japanese yen (JPY) per QALY [41,42];",
        "The willingness-to-pay threshold for exercise was JPY 5 million per QALY [41,42];")

    # 1b word count line (numbers only)
    if wc:
        a, m = wc
        rep("1b", "Word count: abstract 250; main text 3,244 (", "Word count: abstract %d; main text %s (" % (a, f"{m:,}"))

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
