"""Paragraph-by-paragraph comparison of the previous and current deliverables
(WRITING_RULES 1.2 rule 7). Writes manuscript/<VER>/diff_<PREV>_<VER>.md.

Each paragraph outside tables and each table cell is one item, in document
order; items are aligned with difflib and every non-equal block is listed with
both sides. Embedded pictures and the figure files are compared by sha256.
A second, normalized comparison maps the supplementary table numbers of the
previous version to the current ones (SUPP_RENUMBER_V4_V5) and drops reference
numbers (superscript digits) from the current version, so that the blocks left
are changes of wording or content; they are listed in a summary table.
"""
from __future__ import annotations

import difflib
import hashlib
import re
import sys
import zipfile

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

from common import ARCHIVE_PREV, FIGDIR, OUT, PREV, SUPP_RENUMBER_V4_V5, VER, sha256

sys.stdout.reconfigure(encoding="utf-8")


def _txt(p, drop_cites):
    if not drop_cites:
        return p.text
    return "".join(r.text for r in p.runs if not (r.font.superscript and r.text and re.fullmatch(r"[\d,–]+", r.text)))


def renum(t):
    return re.sub(r"(?<=Supplementary Table )S\d+|(?<=Supplementary Tables )S\d+|(?<= and )S\d+(?=\))|(?<=, )S\d+(?=[,; ])",
                  lambda m: SUPP_RENUMBER_V4_V5.get(m.group(0), m.group(0)), t)


def items(path, drop_cites=False):
    doc = Document(path)
    out = []
    t_no = 0
    for el in doc.element.body.iterchildren():
        tag = el.tag.split("}")[1]
        if tag == "p":
            txt = _txt(Paragraph(el, doc), drop_cites)
            if txt.strip():
                out.append(("paragraph", txt))
        elif tag == "tbl":
            t_no += 1
            t = Table(el, doc)
            for i, row in enumerate(t.rows):
                seen = {}  # id -> element; holding the element keeps its id from being reused
                for j, c in enumerate(row.cells):
                    if id(c._tc) in seen:
                        continue
                    seen[id(c._tc)] = c._tc
                    out.append((f"table {t_no} row {i + 1} cell {j + 1}", "\n".join(_txt(q, drop_cites) for q in c.paragraphs)))
    return out


def media(path):
    with zipfile.ZipFile(path) as z:
        return {n: hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith("word/media/")}


L = [f"# {PREV} 与 {VER} 的逐段对照", "",
     f"由 `manuscript/code/compare_versions.py` 生成。{PREV} = `manuscript/archive/{PREV}/`，{VER} = `manuscript/{VER}/`。"
     "表外的每个段落与表内的每个单元格各为一项，按文档顺序用 difflib 对齐；列出全部不相同的块（两侧原文）。", ""]
summary = []
# v5: the manuscript (Introduction, Methods, Results, References) is the edited results docx of v4
PAIRS = [("tables", "tables"), ("figures", "figures"), ("supplement", "supplement"), ("results", "manuscript")]
for prev_name, name in PAIRS:
    a, b = ARCHIVE_PREV / f"{prev_name}_{PREV}.docx", OUT / f"{name}_{VER}.docx"
    if not a.exists():
        L += [f"## {name}_{VER}.docx", "", f"{PREV} 中没有此文件（本版新建），不作逐段对照。", ""]
        summary.append((name, 0, None, "new"))
        continue
    ia, ib = items(a), items(b)
    sm = difflib.SequenceMatcher(a=[t for _, t in ia], b=[t for _, t in ib], autojunk=False)
    blocks = [op for op in sm.get_opcodes() if op[0] != "equal"]
    same = sum(i2 - i1 for tag, i1, i2, _, _ in sm.get_opcodes() if tag == "equal")
    L += [f"## {prev_name}_{PREV}.docx → {name}_{VER}.docx", "",
          f"项数：{PREV} {len(ia)}，{VER} {len(ib)}；相同 {same}；不同的块 {len(blocks)}。", ""]
    for k, (tag, i1, i2, j1, j2) in enumerate(blocks, start=1):
        L.append(f"### {name} 块 {k}（{ {'replace': '改', 'delete': '删', 'insert': '增'}[tag] }）")
        for loc, t in ia[i1:i2]:
            L.append(f"- {PREV}［{loc}］{t}")
        for loc, t in ib[j1:j2]:
            L.append(f"- {VER}［{loc}］{t}")
        L.append("")
    na = [(loc, renum(t)) for loc, t in ia]
    nb = items(b, drop_cites=True)
    sm2 = difflib.SequenceMatcher(a=[t for _, t in na], b=[t for _, t in nb], autojunk=False)
    nblocks = [op for op in sm2.get_opcodes() if op[0] != "equal"]
    L += [f"### {name}：归一化比较（{PREV} 的补充表编号换成 {VER} 的编号、{VER} 去掉文献号）", "",
          f"不同的块 {len(nblocks)}（原始比较 {len(blocks)}）。", "", "| 块 | 类型 | {PREV} 项数 | {VER} 项数 | {PREV} 首项 | {VER} 首项 |".replace("{PREV}", PREV).replace("{VER}", VER), "|---|---|---|---|---|---|"]
    for k, (tag, i1, i2, j1, j2) in enumerate(nblocks, start=1):
        fa = na[i1][1][:90].replace("|", "/") if i2 > i1 else ""
        fb = nb[j1][1][:90].replace("|", "/") if j2 > j1 else ""
        L.append(f"| N{k} | {tag} | {i2 - i1} | {j2 - j1} | {fa} | {fb} |")
    L.append("")
    summary.append((name + " normalized", len(nblocks)))
    ma, mb = media(a), media(b)
    L.append(f"嵌入图片（word/media）：{PREV} {len(ma)} 个、{VER} {len(mb)} 个；sha256 相同的 {len(set(ma.values()) & set(mb.values()))} 个。")
    L.append("")
    summary.append((name, len(ia), len(ib), len(blocks)))

L += ["## 图文件", "", "| 文件 | 与前版逐字节相同 | 说明 |", "|---|---|---|"]
for f in sorted(p.name for p in FIGDIR.iterdir() if p.suffix in (".png", ".tiff", ".svg", ".pdf")):
    pa = ARCHIVE_PREV / "figures" / f
    same = pa.exists() and sha256(pa) == sha256(FIGDIR / f)
    note = ""
    if not same and f.endswith((".svg", ".pdf")):
        note = "SVG 与 PDF 内含生成时刻（SVG 另有随机的 clip-path 编号）；绘图内容以 PNG/TIFF 逐字节比较为准"
    if not pa.exists():
        note, mark = "本版新建", "—"
    else:
        mark = '是' if same else '否'
    L.append(f"| figures/{f} | {mark} | {note} |")
(OUT / f"diff_{PREV}_{VER}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print(summary)
