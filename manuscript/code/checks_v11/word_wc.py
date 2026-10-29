"""Word's own counts (ComputeStatistics per paragraph, from word_stats.ps1 JSON) by the rule:
abstract = the four structured paragraphs without their labels; main text = Introduction to the end of Conclusion
without headings. Also prints the variants with labels/headings."""
import json, sys

sys.stdout.reconfigure(encoding="utf-8")
HEADS = {"Introduction", "Methods", "Results", "Discussion", "Conclusion", "Study design", "Outcomes",
         "Exercise effect and costs", "Survival, costs and utilities", "Statistical analysis",
         "Maximum affordable cost of exercise", "Duration and metastatic treatment costs", "Pembrolizumab",
         "Sensitivity and scenario analyses", "Implications", "Limitations"}
LABELS = ("Purpose", "Methods", "Results", "Conclusion")


def main(path):
    d = json.load(open(path, encoding="utf-8-sig"))
    P = d["paragraphs"]
    txt = [p["text"].rstrip("\r\x07") for p in P]
    W = [p["words"] for p in P]
    a0 = txt.index("Abstract"); i0 = txt.index("Introduction"); ack = txt.index("Acknowledgments")
    ab = [k for k in range(a0 + 1, i0) if txt[k].startswith(LABELS)]
    assert len(ab) == 4
    abs_lab = sum(W[k] for k in ab)
    abs_nolab = abs_lab - 4
    body = [k for k in range(i0, ack) if W[k] > 0]
    heads = [k for k in body if txt[k] in HEADS]
    main_h = sum(W[k] for k in body)
    main_nh = main_h - sum(W[k] for k in heads)
    print(f"pages {d['pages']}; abstract without labels {abs_nolab} (with labels {abs_lab}); "
          f"main text without headings {main_nh} (with {len(heads)} headings {main_h})")
    return abs_nolab, main_nh


if __name__ == "__main__":
    main(sys.argv[1])
