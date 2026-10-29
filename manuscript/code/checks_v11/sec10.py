"""WRITING_RULES section 10 / 13 counts on the abstract + main text of a BCRT manuscript docx (report only)."""
import re, sys
import docx

sys.stdout.reconfigure(encoding="utf-8")
BANNED = ["delve", "underscore", "highlight", "landscape", "leverage", "robust", "nuanced", "crucial", "pivotal",
          "notably", "importantly", "it is worth noting", "in the realm of", "a testament to", "shed light on",
          "paving the way", "multifaceted", "holistic", "comprehensive", "align with", "aligns with", "navigate",
          "tapestry", "ever-evolving", "foster", "showcase", "embark", "realm", "intricate", "cornerstone", "paradigm",
          "synergy", "streamline", "cutting-edge", "groundbreaking"]
THROAT = ["it is important to note", "it should be noted", "it is worth mentioning", "it goes without saying",
          "as a matter of fact", "when it comes to", "with that being said"]
TIME = [r"\brecently\b", r"\bcurrently\b", r"\bthe latest\b", r"\bin recent years\b", r"\bnow\b", r"\bcurrent\b"]
CONN = [r"\bMoreover\b", r"\bFurthermore\b", r"\bAdditionally\b", r"\bIn addition\b"]
CAUSAL = [r"\bcaused\b", r"\bled to\b", r"\bimpact\b"]


def sents(t):
    t = re.sub(r"\b(et al|e\.g|i\.e|Fig|vs|No)\.", lambda m: m.group(0).replace(".", "§"), t)
    return [s.replace("§", ".") for s in re.split(r"(?<=[.;?!])\s+(?=[A-Z(])", t) if s.strip()]


def main(path):
    P = [p.text for p in docx.Document(path).paragraphs]
    a0, i0, ack = P.index("Abstract"), P.index("Introduction"), P.index("Acknowledgments")
    heads = set(["Introduction", "Methods", "Results", "Discussion", "Conclusion", "Study design", "Outcomes",
                 "Exercise effect and costs", "Survival, costs and utilities", "Statistical analysis",
                 "Maximum affordable cost of exercise", "Duration and metastatic treatment costs", "Pembrolizumab",
                 "Sensitivity and scenario analyses", "Implications", "Limitations"])
    body = [t for t in P[i0:ack] if t.strip() and t not in heads]
    ab = [t for t in P[a0 + 1:i0] if t.strip()]
    txt = "\n".join(ab + body)
    low = txt.lower()
    print("paragraphs scanned:", len(ab) + len(body), "(abstract", len(ab), "+ main", len(body), ")")
    print("banned words:", {w: len(re.findall(r"\b" + re.escape(w), low)) for w in BANNED if re.findall(r"\b" + re.escape(w), low)})
    print("throat-clearing:", {w: low.count(w) for w in THROAT if w in low})
    print("bare time words:", {w: len(re.findall(w, low)) for w in TIME if re.findall(w, low)})
    print("connectives:", {w: len(re.findall(w, txt)) for w in CONN if re.findall(w, txt)})
    print("causal words:", {w: len(re.findall(w, low)) for w in CAUSAL if re.findall(w, low)})
    print("em dash —:", txt.count("—"), "| middle dot ・:", txt.count("・"), "| 'Note' paragraphs:", sum(1 for t in body if t.startswith("Note")))
    S = [(len(s.split()), s) for t in body for s in sents(t)]
    long = [x for x in S if x[0] > 30]
    print("sentences:", len(S), "| >30 words:", len(long), "| longest:", max(S)[0])
    for n, s in sorted(long, reverse=True)[:40]:
        print(f"   {n}: {s[:90]}")
    pl = [(len(t.split()), t[:60]) for t in body if len(t.split()) > 150]
    print("paragraphs >150 words:", pl)


if __name__ == "__main__":
    main(sys.argv[1])
