"""WRITING_RULES 7.1 rule 9: first-mention order of Table N, Fig. N, Table SN, Fig. SN in the main text (Introduction to
the end of Conclusion; v18 has no Acknowledgments, so the scan stops at References), ranges and lists expanded; maxima
against the tables file, the figure files and the ESM. Also lists, for every number, the paragraphs that cite it
individually (not only through a range), and checks that every first mention is in running text (body paragraphs only;
abstract, table footnotes, figure captions and the ESM are outside the scan).
usage: python tfnum20.py <v20_dir>   (= checks_v19/tfnum19.py with the v20 file names and the stop at References)
"""
import re, sys, glob, os
import docx

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "checks_v17"))
from tfnum17 import PAT, expand  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")


def main(d):
    P = [p.text for p in docx.Document(os.path.join(d, "manuscript_v20_BCRT.docx")).paragraphs]
    i0, i1 = P.index("Introduction"), P.index("References")
    body = [t for t in P[i0:i1] if t.strip()]
    mentions, single = [], {}
    for k, t in enumerate(body):
        for m in PAT.finditer(t):
            e = expand(m.group(1), m.group(2))
            mentions += e
            if len(e) == 1 or not re.search(r"–|-|to", m.group(2)):
                for x in e:
                    single.setdefault(x, []).append(k)
    first = {}
    for s, n in mentions:
        first.setdefault(s, [])
        if n not in first[s]:
            first[s].append(n)
    print(f"paragraphs scanned: {len(body)}; mentions extracted (expanded): {len(mentions)}")
    tt = [p.text for p in docx.Document(os.path.join(d, "tables_v20_BCRT.docx")).paragraphs if re.match(r"^Table \d+\.", p.text)]
    figs = sorted(glob.glob(os.path.join(d, "Fig*.tif")))
    caps = [t for t in P[P.index("Figure captions"):] if re.match(r"^Fig\. \d+ ", t)]
    E = [p.text for p in docx.Document(os.path.join(d, "ESM_1_v20.docx")).paragraphs]
    est = [t for t in E if re.match(r"^Supplementary Table S\d+\.", t)]
    esf = [t for t in E if re.match(r"^Supplementary Fig\. S\d+\.", t)]
    actual = {"Table ": len(tt), "Fig ": len(figs), "Table S": len(est), "Fig S": len(esf)}
    print("actual:", actual, "| figure captions:", len(caps))
    ok = True
    for s in ("Table ", "Fig ", "Table S", "Fig S"):
        f = first.get(s, [])
        good = f == list(range(1, len(f) + 1)) and (max(f) if f else 0) == actual[s]
        ok &= good
        print(f"  {s.strip():8s} first-mention order {f} -> consecutive 1..n: {f == list(range(1, len(f) + 1))}; "
              f"max {max(f) if f else 0} vs actual {actual[s]}")
    print("individual (non-range) citations, paragraph index in the scan:")
    for s in ("Table ", "Fig ", "Table S", "Fig S"):
        for n in range(1, actual[s] + 1):
            print(f"  {s.strip()} {n}: {single.get((s, n), [])}")
    print("ESM table order:", [int(re.match(r'^Supplementary Table S(\d+)', t).group(1)) for t in est])
    print("ESM fig order:", [int(re.match(r'^Supplementary Fig\. S(\d+)', t).group(1)) for t in esf])
    print("Supplementary Methods mentions in main text:", sum(t.count("Supplementary Methods S1") for t in body),
          "| without S1:", sum(len(re.findall(r"Supplementary Methods(?! S1)", t)) for t in body))
    print("ALL SERIES PASS:", ok)


if __name__ == "__main__":
    main(sys.argv[1])
