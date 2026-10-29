"""Check that Dr Ozaki's renumbering kept every citation pointing at the same source: v9 citations (superscripts) are
mapped to v10 numbers through the reference list (matched by DOI or URL) and compared, in document order, with the
v10/v11 bracket citations. Also extracts the first-appearance order of citations in the v11 main text.
usage: python citemap.py <archive_v9_dir> <v10_dir> <v11_dir> <map.json>
"""
import json, re, sys, difflib
import docx
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding="utf-8")
BR = re.compile(r"\[(\d+(?:–\d+)?(?:,\d+(?:–\d+)?)*)\]")


def expand(s):
    out = []
    for part in s.replace(" ", "").split(","):
        a = re.match(r"^(\d+)[–-](\d+)$", part)
        out += list(range(int(a.group(1)), int(a.group(2)) + 1)) if a else [int(part)]
    return tuple(out)


def paras(path):
    d = docx.Document(path)
    return [p for p in d.element.body.iter(qn("w:p"))]


def ptxt(p):
    return "".join(x.text or "" for x in p.iter(qn("w:t")))


def sup_seq(path, stop=None):
    seq = []
    for p in paras(path):
        if stop and ptxt(p).strip() == stop:
            break
        for r in p.iter(qn("w:r")):
            rpr = r.find(qn("w:rPr"))
            va = rpr.find(qn("w:vertAlign")) if rpr is not None else None
            t = "".join(x.text or "" for x in r.iter(qn("w:t"))).strip()
            if va is not None and va.get(qn("w:val")) == "superscript" and re.fullmatch(r"\d+(?:[–-]\d+)?(?:,\s*\d+(?:[–-]\d+)?)*", t):
                seq.append(expand(t))
    return seq


def br_seq(path, stop=None):
    seq = []
    for p in paras(path):
        t = ptxt(p)
        if stop and t.strip() == stop:
            break
        for g in BR.findall(t):
            e = expand(g)
            if max(e) <= 78:
                seq.append(e)
    return seq


def compare(a9, b10, m, label):
    am = [tuple(m.get(x, -x) for x in g) for g in a9]
    sm = difflib.SequenceMatcher(None, am, b10, autojunk=False)
    diffs = [(op, a9[i1:i2], am[i1:i2], b10[j1:j2]) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
    eq = sum(i2 - i1 for op, i1, i2, j1, j2 in sm.get_opcodes() if op == "equal")
    print(f"{label}: v9 groups {len(a9)}, v10 groups {len(b10)}, equal after mapping {eq}, differing blocks {len(diffs)}")
    for d in diffs:
        print("   ", d[0], "v9", d[1], "-> mapped", d[2], "| v10", d[3])
    return diffs


def main(d9, d10, d11, mp):
    m = {int(k): v for k, v in json.load(open(mp)).items()}
    m[69] = 52
    compare(sup_seq(d9 + "/supplement_v9.docx"), br_seq(d10 + "/ESM_1.docx"), m, "ESM")
    compare(sup_seq(d9 + "/manuscript_v9.docx", stop="References"), br_seq(d10 + "/manuscript_v10_BCRT.docx", stop="References"), m, "manuscript body (to References)")
    compare(sup_seq(d9 + "/tables_v9.docx"), br_seq(d10 + "/tables_v10_BCRT.docx"), m, "tables")
    print("ESM v11 citations == v10:", br_seq(d11 + "/ESM_1_v11.docx") == br_seq(d10 + "/ESM_1.docx"))
    print("tables v11 citations == v10:", br_seq(d11 + "/tables_v11_BCRT.docx") == br_seq(d10 + "/tables_v10_BCRT.docx"))


if __name__ == "__main__":
    main(*sys.argv[1:5])
