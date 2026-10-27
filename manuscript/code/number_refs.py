"""Number the reference markers and write the four deliverable docx files.

Reads the marked files written by the generators (_build/manuscript_marked.docx,
tables_marked.docx, figures_marked.docx, supplement_marked.docx). A reference gets
its number at its first citation, reading the manuscript text first (Introduction,
Methods, Results), then the tables, the figure legends and the supplement, each in
document order (paragraphs and table cells as they appear). So the numbers in the
manuscript text run 1, 2, 3, ... without gaps, and references cited only in tables,
legends or the supplement follow. Each marker becomes a superscript run; the
reference list is appended to the manuscript under the heading "References".
Writes manuscript/<VER>/{manuscript,tables,figures,supplement}_<VER>.docx and
_build/_refs.json.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

from common import BUILD, OUT, VER
from references import MARK_RE, REFS, entry, superscript

sys.stdout.reconfigure(encoding="utf-8")
FILES = [("manuscript", BUILD / "manuscript_marked.docx"), ("tables", BUILD / "tables_marked.docx"),
         ("figures", BUILD / "figures_marked.docx"), ("supplement", BUILD / "supplement_marked.docx")]


def paragraphs(doc):
    """Body paragraphs and table-cell paragraphs in document order."""
    for el in doc.element.body.iterchildren():
        tag = el.tag.split("}")[1]
        if tag == "p":
            yield Paragraph(el, doc)
        elif tag == "tbl":
            seen = {}  # id -> element; holding the element keeps its id from being reused
            for row in Table(el, doc).rows:
                for c in row.cells:
                    if id(c._tc) in seen:
                        continue
                    seen[id(c._tc)] = c._tc
                    yield from c.paragraphs


num: dict[str, int] = {}
cites = []
docs = {}
for name, path in FILES:
    doc = Document(path)
    docs[name] = doc
    for pi, p in enumerate(paragraphs(doc)):
        if "⟦" not in p.text:
            continue
        for r in list(p.runs):
            t = r.text
            if "⟦" not in t:
                continue
            assert t.count("⟦") == t.count("⟧"), ("marker split across runs", t)
            pieces, pos = [], 0
            for m in MARK_RE.finditer(t):
                keys = m.group(1).split(",")
                for k in keys:
                    assert k in REFS, k
                    if k not in num:
                        num[k] = len(num) + 1
                nums = [num[k] for k in keys]
                pieces += [(t[pos:m.start()], False), (superscript(nums), True)]
                cites.append(dict(doc=name, paragraph=pi, keys=keys, numbers=nums, shown=superscript(nums), before=t[max(0, m.start() - 40):m.start()]))
                pos = m.end()
            pieces.append((t[pos:], False))
            anchor = r._r
            for text, sup in pieces:
                if not text:
                    continue
                nr = copy.deepcopy(r._r)
                for x in nr.findall(qn("w:t")):
                    nr.remove(x)
                tel = nr.makeelement(qn("w:t"), {})
                tel.text = text
                tel.set(qn("xml:space"), "preserve")
                nr.append(tel)
                rpr = nr.find(qn("w:rPr"))
                if rpr is None:
                    rpr = nr.makeelement(qn("w:rPr"), {})
                    nr.insert(0, rpr)
                va = rpr.find(qn("w:vertAlign"))
                if sup:
                    if va is None:
                        va = rpr.makeelement(qn("w:vertAlign"), {})
                        rpr.append(va)
                    va.set(qn("w:val"), "superscript")
                elif va is not None:
                    rpr.remove(va)
                anchor.addnext(nr)
                anchor = nr
            r._r.getparent().remove(r._r)
        assert "⟦" not in p.text and "⟧" not in p.text
    if name == "manuscript":
        main_count = len(num)

unused = [k for k in REFS if k not in num]
assert not unused, ("references never cited", unused)

# reference list at the end of the manuscript, in the formatting of the existing heading and body paragraphs
ms = docs["manuscript"]
body = [p for p in ms.paragraphs if p.text.strip()]
head = next(p for p in body if p.text == "Results")
last = body[-1]


def clone(src, text):
    el = copy.deepcopy(src._p)
    runs = el.findall(qn("w:r"))
    for x in runs[1:]:
        el.remove(x)
    t = runs[0].find(qn("w:t"))
    t.text = text
    t.set(qn("xml:space"), "preserve")
    return el


anchor = last._p
order = sorted(num, key=num.get)
for el in [clone(head, "References")] + [clone(last, f"{num[k]}. {entry(k)}") for k in order]:
    anchor.addnext(el)
    anchor = el

for name, _ in FILES:
    docs[name].save(OUT / f"{name}_{VER}.docx")
json.dump(dict(order=order, numbers=num, main_text_count=main_count, citations=cites,
               entries={k: entry(k) for k in order},
               manuscript_sha256=hashlib.sha256((OUT / f"manuscript_{VER}.docx").read_bytes()).hexdigest()),
          open(BUILD / "_refs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(num)} references: {main_count} first cited in the manuscript text, {len(num) - main_count} only in tables, legends or the supplement;",
      len(cites), "citations")
for name in ("tables", "figures", "supplement"):
    new = sorted({n for c in cites if c["doc"] == name for n in c["numbers"] if n > main_count})
    print(f"  first cited in {name}: {new}")
