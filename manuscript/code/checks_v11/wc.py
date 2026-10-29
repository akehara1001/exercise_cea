"""Word counts of a BCRT manuscript docx by section, whitespace tokens (Word's rule)."""
import sys, docx

sys.stdout.reconfigure(encoding="utf-8")


def paras(path):
    return [p.text for p in docx.Document(path).paragraphs]


def n(t):
    return len(t.split())


def counts(path, verbose=True):
    P = paras(path)
    idx = {t.strip(): i for i, t in enumerate(P) if t.strip() in (
        "Abstract", "Introduction", "Methods", "Results", "Discussion", "Conclusion", "Acknowledgments", "References",
        "Statements and Declarations", "Figure captions")}
    a0, i0 = idx["Abstract"], idx["Introduction"]
    abstract = [t for t in P[a0 + 1:i0] if t.strip() and not t.startswith("Keywords")]
    keywords = [t for t in P[a0 + 1:i0] if t.startswith("Keywords")]
    body = [t for t in P[i0:idx["Acknowledgments"]] if t.strip()]
    heads = {"Introduction", "Methods", "Results", "Discussion", "Conclusion", "Study design", "Outcomes",
             "Exercise effect and costs", "Survival, costs and utilities", "Statistical analysis",
             "Maximum affordable cost of exercise", "Duration and metastatic treatment costs", "Pembrolizumab",
             "Sensitivity and scenario analyses", "Implications", "Limitations"}
    body_nohead = [t for t in body if t.strip() not in heads]
    labels = ("Purpose ", "Methods ", "Results ", "Conclusion ")
    abs_nolab = [t.split(" ", 1)[1] if t.startswith(labels) else t for t in abstract]
    out = {
        "abstract_with_labels": sum(map(n, abstract)),
        "abstract_without_labels": sum(map(n, abs_nolab)),
        "keywords": sum(map(n, keywords)),
        "body_with_headings": sum(map(n, body)),
        "body_without_headings": sum(map(n, body_nohead)),
        "n_body_paragraphs_nonheading": len(body_nohead),
    }
    if verbose:
        for k, v in out.items():
            print(f"{k}: {v}")
    return out


if __name__ == "__main__":
    counts(sys.argv[1])
