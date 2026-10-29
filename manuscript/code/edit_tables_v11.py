"""tables_v11_BCRT = direct edit of Dr Ozaki's tables_v10_BCRT.docx: three text changes in Table 1 (instruction step 2).
Layout untouched; only word/document.xml is rewritten. Each original must occur exactly once or the script stops.

usage: python edit_tables_v11.py <tables_v10.docx> <out.docx> <log.json>
"""
import hashlib, json, sys, zipfile
from lxml import etree

T10_SHA16 = "2a13e2e69c4187ae"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def q(t):
    return "{%s}%s" % (W, t)


def ptext(el):
    return "".join(t.text or "" for t in el.iter(q("t")))


def main(src, dst, logpath):
    assert hashlib.sha256(open(src, "rb").read()).hexdigest()[:16] == T10_SHA16, "tables v10 sha256 differs"
    zin = zipfile.ZipFile(src)
    doc = etree.fromstring(zin.read("word/document.xml"))
    log = []

    def rep_t(old, new):
        """old must lie inside a single w:t, once in the document."""
        hits = [t for t in doc.iter(q("t")) if t.text and old in t.text]
        assert len(hits) == 1 and hits[0].text.count(old) == 1, (old, len(hits))
        t = hits[0]
        p = next(a for a in t.iterancestors() if a.tag == q("p"))
        before = ptext(p)
        t.text = t.text.replace(old, new)
        log.append({"old": old, "new": new, "para_before": before, "para_after": ptext(p)})

    rep_t("one draw of the cost and utility inputs", "one draw of the other inputs")
    rep_t("(Supplementary Methods, Online Resource 1)", "(Supplementary Methods S1, Online Resource 1)")
    # footnote d: append one sentence to its last text run
    fd = [p for p in doc.iter(q("p")) if ptext(p).startswith("dRecurrence HR: hazard ratio")]
    assert len(fd) == 1
    ts = list(fd[0].iter(q("t")))
    before = ptext(fd[0])
    assert before.endswith("1.00 means no effect.")
    ts[-1].text = ts[-1].text + " After the period in which the HR is held, the reduction in the hazard, 1 − HR, halves every year."
    ts[-1].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    log.append({"old": before, "new": ptext(fd[0])})

    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "word/document.xml":
                head = data.split(b"?>", 1)[0] + b"?>"
                data = head + etree.tostring(doc, encoding="UTF-8", xml_declaration=False)
            zout.writestr(info, data)
    json.dump(log, open(logpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for e in log:
        print(e["new"][-160:])


if __name__ == "__main__":
    main(*sys.argv[1:4])
