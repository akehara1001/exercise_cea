"""Regression check v14 -> v15 (= checks_v14/regress14.py with labels v14/v15) (WRITING_RULES 1.2 rule 7): document-order text units (body paragraphs and table-cell
paragraphs) of the two files are aligned with difflib; every unit that changed, was added or removed is matched to an entry
of the edit logs (edit_manuscript_v15 / edit_tables_v15 / edit_esm_v15), which name the instruction step. A changed unit
that no log entry explains is listed as UNEXPLAINED. Also counts the number tokens of the unchanged units (must be equal).
usage: python regress14.py <old.docx> <new.docx> <log.json> <label>
"""
import json, re, sys, difflib
from collections import Counter
import docx
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding="utf-8")
NUM = re.compile(r"[−-]?\d[\d,]*(?:\.\d+)?")


def units(path):
    d = docx.Document(path)
    out = []
    for el in d.element.body.iterchildren():
        if el.tag == qn("w:p"):
            out.append("".join(x.text or "" for x in el.iter(qn("w:t"))))
        elif el.tag == qn("w:tbl"):
            for tr in el.iter(qn("w:tr")):
                for tc in tr.findall(qn("w:tc")):
                    for p in tc.findall(qn("w:p")):
                        out.append("".join(x.text or "" for x in p.iter(qn("w:t"))))
    return out


def log_index(path):
    """text -> step, for the 'before' and 'after' sides of every log entry (rows of inserted tables as cells)."""
    L = json.load(open(path, encoding="utf-8"))
    before, after = {}, {}
    for e in L:
        st = e["step"]
        for k in ("para_before", "before", "old"):
            if e.get(k):
                before.setdefault(e[k], st)
        for k in ("para_after", "after", "new", "title"):
            if e.get(k):
                after.setdefault(e[k], st)
        for r in e.get("rows") or []:
            for c in r:
                after.setdefault(c, st)
        if e.get("row"):
            for c in e["row"]:
                before.setdefault(c, st)
        for f in e.get("footnotes") or []:
            after.setdefault(f, st)
    return before, after


def main(a, b, logpath, label):
    A, B = units(a), units(b)
    before, after = log_index(logpath)
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    ops = sm.get_opcodes()
    same = sum(i2 - i1 for op, i1, i2, j1, j2 in ops if op == "equal")
    blocks = [o for o in ops if o[0] != "equal"]
    print(f"{label}: units v14 {len(A)}, v15 {len(B)}, unchanged {same}, changed blocks {len(blocks)}")
    unexplained = 0
    steps = Counter()
    for k, (op, i1, i2, j1, j2) in enumerate(blocks, 1):
        print(f"  [{k}] {op}: {i2 - i1} -> {j2 - j1} units")
        for t in A[i1:i2]:
            st = before.get(t)
            if st is None and t == "":
                st = "empty paragraph of a removed block (section break)"
            if st is None:
                unexplained += 1; st = "UNEXPLAINED"
            steps[st] += 1
            print(f"     - [{st}] {t[:160]}")
        for t in B[j1:j2]:
            st = after.get(t)
            if st is None and t == "":
                st = "empty paragraph of an inserted block (section break or cell run)"
            if st is None:
                unexplained += 1; st = "UNEXPLAINED"
            steps[st] += 1
            print(f"     + [{st}] {t[:160]}")
    eqA = [n for op, i1, i2, j1, j2 in ops if op == "equal" for t in A[i1:i2] for n in NUM.findall(t)]
    print(f"  numbers in the unchanged units: {len(eqA)} (identical by construction)")
    allA = Counter(n.rstrip(",") for t in A for n in NUM.findall(t))
    allB = Counter(n.rstrip(",") for t in B for n in NUM.findall(t))
    print(f"  number tokens: v14 {sum(allA.values())}, v15 {sum(allB.values())}")
    print(f"  only in v14: {dict(allA - allB)}")
    print(f"  only in v15: {dict(allB - allA)}")
    print(f"  units by explanation: {dict(steps)}")
    print(f"  UNEXPLAINED: {unexplained}")
    return unexplained


if __name__ == "__main__":
    sys.exit(1 if main(*sys.argv[1:5]) else 0)
