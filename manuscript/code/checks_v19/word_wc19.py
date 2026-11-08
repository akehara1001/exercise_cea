"""Word's own counts (ComputeStatistics per paragraph, from checks_v11/word_stats.ps1 JSON) by the rule of v11-v17:
abstract = the four structured paragraphs without their labels; main text = Introduction to the end of Conclusion
without headings. = checks_v14/word_wc14.py, except that the main text ends at "References" (v18 has no
Acknowledgments section; the Figure captions after the Statements are outside the range). Prints the variants with
labels/headings and the counts per section (main text, without headings).
usage: python word_wc19.py <stats.json>
"""
import json, sys

sys.stdout.reconfigure(encoding="utf-8")
HEADS = {"Introduction", "Methods", "Results", "Discussion", "Conclusion", "Study design", "Outcomes",
         "Exercise effect and costs", "Survival, costs and utilities", "Statistical analysis",
         "Four strategies compared", "Exercise compared with pembrolizumab",
         "Maximum affordable cost of exercise", "Duration and metastatic treatment costs",
         "Sensitivity and scenario analyses", "Implications", "Limitations"}
MAJOR = ["Introduction", "Methods", "Results", "Discussion", "Implications", "Limitations", "Conclusion"]
LABELS = ("Purpose", "Methods", "Results", "Conclusion")


def main(path):
    d = json.load(open(path, encoding="utf-8-sig"))
    P = d["paragraphs"]
    txt = [p["text"].rstrip("\r\x07") for p in P]
    W = [p["words"] for p in P]
    a0 = txt.index("Abstract"); i0 = txt.index("Introduction"); end = txt.index("References")
    assert "Acknowledgments" not in txt
    ab = [k for k in range(a0 + 1, i0) if txt[k].startswith(LABELS)]
    assert len(ab) == 4
    abs_lab = sum(W[k] for k in ab)
    abs_nolab = abs_lab - 4
    body = [k for k in range(i0, end) if W[k] > 0]
    heads = [k for k in body if txt[k] in HEADS]
    assert len(heads) == len(HEADS), (len(heads), sorted(set(HEADS) - {txt[k] for k in heads}))
    main_h = sum(W[k] for k in body)
    main_nh = main_h - sum(W[k] for k in heads)
    print(f"pages {d['pages']}; abstract without labels {abs_nolab} (with labels {abs_lab}); "
          f"main text without headings {main_nh} (with {len(heads)} headings {main_h})")
    print("abstract paragraphs:", [W[k] for k in ab])
    pos = {h: txt.index(h) for h in MAJOR}
    for j, h in enumerate(MAJOR):
        stop = pos[MAJOR[j + 1]] if j + 1 < len(MAJOR) else end
        n = sum(W[k] for k in range(pos[h], stop) if k in body and k not in heads)
        print(f"  {h}: {n}")
    return abs_nolab, main_nh


if __name__ == "__main__":
    main(sys.argv[1])
