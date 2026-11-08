"""Regression check v18 -> v19 (WRITING_RULES 1.2 rule 7) = checks_v17/regress17.py with the v19 log fields: document-order
text units (body paragraphs and table-cell paragraphs) of the two files are aligned with difflib; every unit that changed,
was added or removed is matched to an entry of the edit logs (edit_*_v19.py), which name the instruction step. A changed
unit that no log entry explains is listed as UNEXPLAINED. Number tokens of the whole files are compared.
usage: python regress19.py <old.docx> <new.docx> <log.json> <label>
"""
import json, os, re, sys, difflib
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "checks_v17"))
from regress17 import units  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
NUM = re.compile(r"[−-]?\d[\d,]*(?:\.\d+)?")


def log_index(path):
    L = json.load(open(path, encoding="utf-8"))
    before, after = {}, {}
    for e in L:
        st = e["step"]
        for k in ("para_before", "before", "old"):
            if isinstance(e.get(k), str):
                before.setdefault(e[k], st)
        for k in ("para_after", "after", "new", "title"):
            if isinstance(e.get(k), str):
                after.setdefault(e[k], st)
        for r in e.get("rows") or []:
            for c in r:
                after.setdefault(c, st)
        for k in ("footnotes", "header"):
            for f in e.get(k) or []:
                after.setdefault(f, st)
    return before, after


def main(a, b, logpath, label):
    A, B = units(a), units(b)
    before, after = log_index(logpath)
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    ops = sm.get_opcodes()
    same = sum(i2 - i1 for op, i1, i2, j1, j2 in ops if op == "equal")
    blocks = [o for o in ops if o[0] != "equal"]
    print(f"{label}: units v18 {len(A)}, v19 {len(B)}, unchanged {same}, changed blocks {len(blocks)}")
    unexplained = 0
    steps = Counter()
    fixed = {"Chemotherapy plus pembrolizumab": "2 Table S12", "Chemotherapy alone": "2 Table S12",
             "A. Cumulative proportion of women without exercise, %": "2 Table S12",
             "B. Absolute reduction with exercise, percentage points": "2 Table S12"}
    for k, (op, i1, i2, j1, j2) in enumerate(blocks, 1):
        print(f"  [{k}] {op}: {i2 - i1} -> {j2 - j1} units")
        for t in A[i1:i2]:
            st = before.get(t)
            if st is None:
                unexplained += 1; st = "UNEXPLAINED"
            steps[st] += 1
            print(f"     - [{st}] {t[:160]}")
        for t in B[j1:j2]:
            st = after.get(t) or fixed.get(t) or ("2 Table S12" if t == "Recurrence HR" and "ESM" in label else None)
            if st is None and t == "":
                st = "empty paragraph of an inserted block (section break, merged cell or spacer)"
            if st is None:
                unexplained += 1; st = "UNEXPLAINED"
            steps[st] += 1
            print(f"     + [{st}] {t[:160]}")
    allA = Counter(n.rstrip(",") for t in A for n in NUM.findall(t))
    allB = Counter(n.rstrip(",") for t in B for n in NUM.findall(t))
    print(f"  number tokens: v18 {sum(allA.values())}, v19 {sum(allB.values())}")
    print(f"  only in v18: {dict(allA - allB)}")
    print(f"  only in v19: {dict(allB - allA)}")
    print(f"  units by explanation: {dict(steps)}")
    print(f"  UNEXPLAINED: {unexplained}")
    return unexplained


if __name__ == "__main__":
    sys.exit(1 if main(*sys.argv[1:5]) else 0)
