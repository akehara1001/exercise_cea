"""python-docx helpers: 12 pt Times New Roman on every run, black, no Heading styles."""
from __future__ import annotations

import re

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt

FONT = "Times New Roman"
SIZE = Pt(12)
SUP_RE = re.compile(r"\^\{(.*?)\}")


def _fonts(run) -> None:
    run.font.name = FONT
    run.font.size = SIZE
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(a), FONT)


def new_document(landscape: bool) -> Document:
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = FONT
    st.font.size = SIZE
    rpr = st.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(a), FONT)
    pf = st.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    set_page(doc.sections[0], landscape)
    return doc


def set_page(section, landscape: bool) -> None:
    if landscape:
        section.orientation = WD_ORIENT.LANDSCAPE
        section.page_width, section.page_height = Mm(297), Mm(210)
    else:
        section.orientation = WD_ORIENT.PORTRAIT
        section.page_width, section.page_height = Mm(210), Mm(297)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(section, side, Mm(20))


def add_runs(par, text: str, bold: bool = False) -> None:
    """Text with ^{...} marking superscript footnote symbols."""
    pos = 0
    for m in SUP_RE.finditer(text):
        if m.start() > pos:
            r = par.add_run(text[pos:m.start()])
            _fonts(r)
            r.bold = bold
        r = par.add_run(m.group(1))
        _fonts(r)
        r.font.superscript = True
        r.bold = False
        pos = m.end()
    if pos < len(text):
        r = par.add_run(text[pos:])
        _fonts(r)
        r.bold = bold


def para(doc_or_cell, text: str, bold: bool = False, space_after: float = 0):
    p = doc_or_cell.add_paragraph()
    add_runs(p, text, bold=bold)
    p.paragraph_format.space_after = Pt(space_after)
    return p


def page_break(doc) -> None:
    p = doc.add_paragraph()
    r = p.add_run()
    _fonts(r)
    r.add_break(WD_BREAK.PAGE)


def table(doc, rows: list[list[str]], bold_rows: set[int] = frozenset(), widths_mm=None):
    """rows[0] is the header. A row with one non-empty first cell and the rest
    empty is a group/panel label row and is merged across the table."""
    ncol = len(rows[0])
    t = doc.add_table(rows=len(rows), cols=ncol)
    t.style = doc.styles["Table Grid"]
    for i, row in enumerate(rows):
        cells = t.rows[i].cells
        if len(row) == 1:
            c = cells[0].merge(cells[-1])
            c.paragraphs[0].text = ""
            add_runs(c.paragraphs[0], row[0], bold=i in bold_rows)
            continue
        for j, txt in enumerate(row):
            cells[j].paragraphs[0].text = ""
            add_runs(cells[j].paragraphs[0], txt, bold=(i in bold_rows and j == 0))
    if widths_mm:
        for i, row in enumerate(t.rows):
            for j, w in enumerate(widths_mm):
                if j < len(row.cells):
                    row.cells[j].width = Mm(w)
    return t


def new_section(doc, landscape: bool):
    from docx.enum.section import WD_SECTION
    s = doc.add_section(WD_SECTION.NEW_PAGE)
    set_page(s, landscape)
    return s
