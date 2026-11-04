"""Number ledger of the v14 changes (instruction step 5, WRITING_RULES 6.1): every number in the new or replaced text of
the manuscript (edit log), in the new Table 2 and its footnotes, and in the title of Supplementary Table S4, is looked up
in the sources in this order: output/phase2/fourarm_report.md, the v13 tables, the v13 ESM, the v13 manuscript. Citation
groups ([9,14], [28-31]) are reference numbers, not values, and are left out. A number found in none is listed as
NOT FOUND (to be explained, e.g. derived). Output: one line per number with its paragraph and its first source.
usage: python numcheck14.py <project_root>
"""
import json, os, re, sys
import docx
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding="utf-8")
NUM = re.compile(r"(?<![\w.])[−-]?\d[\d,]*(?:\.\d+)?")
CITE = re.compile(r"\[\d+(?:[,–]\d+)*\]")


def doc_text(path):
    d = docx.Document(path)
    return "\n".join("".join(x.text or "" for x in p.iter(qn("w:t"))) for p in d.element.body.iter(qn("w:p")))


def tokens(s):
    s = CITE.sub(" ", s)
    return [m.group(0).rstrip(",") for m in NUM.finditer(s)]


def main(root):
    M = os.path.join(root, "manuscript")
    src = [("fourarm_report.md", open(os.path.join(root, "output", "phase2", "fourarm_report.md"), encoding="utf-8").read()),
           ("tables_v13", doc_text(os.path.join(M, "v13", "tables_v13_BCRT.docx"))),
           ("ESM_1_v13", doc_text(os.path.join(M, "v13", "ESM_1_v13.docx"))),
           ("manuscript_v13", doc_text(os.path.join(M, "v13", "manuscript_v13_BCRT.docx")))]
    src = [(n, CITE.sub(" ", t).replace("−", "-")) for n, t in src]   # one minus sign (the report writes "-")
    items = []
    for e in json.load(open(os.path.join(M, "code", "checks_v14", "out", "m14_log.json"), encoding="utf-8")):
        st = e["step"]
        if st in ("1f", "1c renumber", "1d delete", "1h") or not e.get("para_after"):
            continue
        txt = e["para_after"]
        if st == "1d append":
            txt = txt[len(e["para_before"]):]
        items.append((st, txt))
    for e in json.load(open(os.path.join(M, "code", "checks_v14", "out", "t14_log.json"), encoding="utf-8")):
        if e["step"] == "2a insert":
            items.append(("2a title", e["title"]))
            for r in e["rows"]:
                items.append(("2a row", " | ".join(r)))
            for f in e["footnotes"]:
                items.append(("2a footnote", f))
    for e in json.load(open(os.path.join(M, "code", "checks_v14", "out", "esm14_log.json"), encoding="utf-8")):
        if e["step"] == "3a insert":
            items.append(("3a title", e["title"]))
    seen_final = {}
    nf = 0; n = 0
    for st, txt in items:
        for tok in tokens(txt):
            n += 1
            pat = re.compile(r"(?<![\w.,])" + re.escape(tok.replace("−", "-")) + r"(?![\d]|,\d|\.\d)")
            where = next((name for name, t in src if pat.search(t)), None)
            if where is None:
                nf += 1
            print(f"{st:12s} | {tok:>12s} | {where or 'NOT FOUND'} | {txt[:70]}")
    print(f"numbers checked: {n}; not found in the sources: {nf}")


if __name__ == "__main__":
    main(sys.argv[1])
