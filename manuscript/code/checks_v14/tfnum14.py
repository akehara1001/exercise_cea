"""WRITING_RULES 7.1 rule 9: first-mention order of Table N, Fig. N, Table SN, Fig. SN in the main text (Introduction to
Conclusion), ranges and lists expanded; maxima against the tables file, the figure files and the ESM.
usage: python tfnum14.py <v14_dir>  (= checks_v13/tfnum.py with the v14 file names)
"""
import re, sys, glob, os
import docx

sys.stdout.reconfigure(encoding="utf-8")
TOK = r"S?\d+"
LIST = rf"{TOK}(?:\s*(?:–|-|to)\s*{TOK}|(?:,\s*|,?\s+and\s+){TOK})*"
PAT = re.compile(rf"\b(Tables?|Figs?\.|Figures?)\s+({LIST})")


def expand(kind, s):
    out = []
    parts = re.split(r",\s*|,?\s+and\s+", s)
    for p in parts:
        m = re.match(rf"^({TOK})\s*(?:–|-|to)\s*({TOK})$", p)
        if m:
            a, b = m.group(1), m.group(2)
            sup = a.startswith("S")
            lo, hi = int(a.lstrip("S")), int(b.lstrip("S"))
            out += [("S" if sup else "") + str(k) for k in range(lo, hi + 1)]
        else:
            out.append(p)
    ser = "Table" if kind.startswith("Table") else "Fig"
    return [(ser + (" S" if x.startswith("S") else " "), int(x.lstrip("S"))) for x in out]


def main(d):
    P = [p.text for p in docx.Document(os.path.join(d, "manuscript_v14_BCRT.docx")).paragraphs]
    i0, i1 = P.index("Introduction"), P.index("Acknowledgments")
    body = [t for t in P[i0:i1] if t.strip()]
    mentions = []
    for t in body:
        for m in PAT.finditer(t):
            mentions += expand(m.group(1), m.group(2))
    first = {}
    for s, n in mentions:
        first.setdefault(s, [])
        if n not in first[s]:
            first[s].append(n)
    print(f"paragraphs scanned: {len(body)}; mentions extracted (expanded): {len(mentions)}")
    # actual counts
    tt = [p.text for p in docx.Document(os.path.join(d, "tables_v14_BCRT.docx")).paragraphs if re.match(r"^Table \d+\.", p.text)]
    figs = sorted(glob.glob(os.path.join(d, "Fig*.tif")))
    caps = [t for t in P[P.index("Figure captions"):] if re.match(r"^Fig\. \d+ ", t)]
    E = [p.text for p in docx.Document(os.path.join(d, "ESM_1_v14.docx")).paragraphs]
    est = [t for t in E if re.match(r"^Supplementary Table S\d+\.", t)]
    esf = [t for t in E if re.match(r"^Supplementary Fig\. S\d+\.", t)]
    actual = {"Table ": len(tt), "Fig ": len(figs), "Table S": len(est), "Fig S": len(esf)}
    print("actual:", actual, "| figure captions:", len(caps))
    for s in ("Table ", "Fig ", "Table S", "Fig S"):
        f = first.get(s, [])
        print(f"  {s.strip():8s} first-mention order {f} -> consecutive 1..n: {f == list(range(1, len(f) + 1))}; "
              f"max {max(f) if f else 0} vs actual {actual[s]}")
    # physical order in ESM
    print("ESM table order:", [int(re.match(r'^Supplementary Table S(\d+)', t).group(1)) for t in est])
    print("ESM fig order:", [int(re.match(r'^Supplementary Fig\. S(\d+)', t).group(1)) for t in esf])
    sm = [t for t in body if "Supplementary Methods" in t]
    print("Supplementary Methods mentions in main text:", sum(t.count("Supplementary Methods S1") for t in body),
          "| without S1:", sum(len(re.findall(r"Supplementary Methods(?! S1)", t)) for t in body))


if __name__ == "__main__":
    main(sys.argv[1])
