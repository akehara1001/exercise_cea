"""WRITING_RULES section 10 / 13 counts on the abstract + main text (report only) = checks_v11/sec10.py with the main text
ending at References (v18 has no Acknowledgments) and the Results headings of v14 onward. Also prints the counts for a
given list of paragraphs (the paragraphs changed in this version) when --changed <text file, one paragraph per line> is
given, and the sentences over 30 words in them.
usage: python sec10_19.py <manuscript.docx> [--changed <file>]
"""
import os, re, sys
import docx

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "checks_v11"))
from sec10 import BANNED, THROAT, TIME, CONN, CAUSAL, sents  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
HEADS = {"Introduction", "Methods", "Results", "Discussion", "Conclusion", "Study design", "Outcomes",
         "Exercise effect and costs", "Survival, costs and utilities", "Statistical analysis",
         "Four strategies compared", "Exercise compared with pembrolizumab",
         "Maximum affordable cost of exercise", "Duration and metastatic treatment costs",
         "Sensitivity and scenario analyses", "Implications", "Limitations"}


def report(label, ab, body):
    txt = "\n".join(ab + body)
    low = txt.lower()
    print(f"[{label}] paragraphs scanned:", len(ab) + len(body), "(abstract", len(ab), "+ main", len(body), ")")
    print("banned words:", {w: len(re.findall(r"\b" + re.escape(w), low)) for w in BANNED if re.findall(r"\b" + re.escape(w), low)})
    print("throat-clearing:", {w: low.count(w) for w in THROAT if w in low})
    print("bare time words:", {w: len(re.findall(w, low)) for w in TIME if re.findall(w, low)})
    print("connectives:", {w: len(re.findall(w, txt)) for w in CONN if re.findall(w, txt)})
    print("causal words:", {w: len(re.findall(w, low)) for w in CAUSAL if re.findall(w, low)})
    print("em dash —:", txt.count("—"), "| middle dot ・:", txt.count("・"), "| 'Note' paragraphs:", sum(1 for t in body if t.startswith("Note")))
    S = [(len(s.split()), s) for t in body for s in sents(t)]
    long = [x for x in S if x[0] > 30]
    print("sentences:", len(S), "| >30 words:", len(long), "| longest:", max(S)[0] if S else 0)
    for n, s in sorted(long, reverse=True)[:50]:
        print(f"   {n}: {s[:110]}")
    pl = [(len(t.split()), t[:60]) for t in body if len(t.split()) > 150]
    print("paragraphs >150 words:", pl)


def main(path, changed=None):
    P = [p.text for p in docx.Document(path).paragraphs]
    a0, i0, end = P.index("Abstract"), P.index("Introduction"), P.index("References")
    body = [t for t in P[i0:end] if t.strip() and t not in HEADS]
    ab = [t for t in P[a0 + 1:i0] if t.strip()]
    report("abstract + main text", ab, body)
    if changed:
        C = [l.rstrip("\n") for l in open(changed, encoding="utf-8") if l.strip()]
        report("changed paragraphs", [], C)


if __name__ == "__main__":
    a = sys.argv[1:]
    ch = None
    if "--changed" in a:
        i = a.index("--changed"); ch = a[i + 1]; a = a[:i] + a[i + 2:]
    main(a[0], ch)
