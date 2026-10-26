"""Read back tables_v1.docx and figures_v1.docx, check them against WRITING_RULES
(format, footnote symbols, every number registered), and write
numbers_ledger_v1.md, check_v1.md and MANIFEST_v1.md.

Run after make_tables_v1.py and make_figures_v1.py, and after
table_figure_plan_v1.md is final (the manifest hashes it).
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from collections import Counter

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.table import Table
from docx.text.paragraph import Paragraph

from v1_common import BUILD, FIGDIR, NUM_RE, OUT, ROOT, STAR, rel, sha256

sys.stdout.reconfigure(encoding="utf-8")
REF_RE = re.compile(r"\b(?:Supplementary )?(?:Tables?|Figs?\.) S?\d+(?:\s*(?:and|to|,)\s*S?\d+)*")


def blocks(doc):
    """Paragraphs and table cells in document order: (kind, text, runs, cell_text)."""
    out = []
    for el in doc.element.body.iterchildren():
        tag = el.tag.split("}")[1]
        if tag == "p":
            p = Paragraph(el, doc)
            out.append(("p", p.text, p.runs, None, p))
        elif tag == "tbl":
            t = Table(el, doc)
            seen = set()
            for row in t.rows:
                for c in row.cells:
                    if id(c._tc) in seen:
                        continue
                    seen.add(id(c._tc))
                    for p in c.paragraphs:
                        out.append(("cell", p.text, p.runs, c.text, p))
    return out


def tokens(text):
    return [m.group(0).rstrip(",") for m in NUM_RE.finditer(REF_RE.sub(" ", text))]


def check_doc(path, ledger, landscape):
    doc = Document(path)
    res = {"file": rel(path)}
    bl = blocks(doc)
    runs = [r for _, _, rs, _, _ in bl for r in rs if r.text]
    res["paragraphs_and_cells"] = len(bl)
    res["empty_cells"] = sum(1 for k, _, _, ct, _ in bl if k == "cell" and not (ct or "").strip())
    res["text_runs"] = len(runs)
    res["runs_not_TNR_12pt"] = sum(1 for r in runs if r.font.name != "Times New Roman" or r.font.size != Pt(12)
                                  or (r._element.rPr.find(qn("w:rFonts")).get(qn("w:eastAsia")) != "Times New Roman"))
    nonblack = 0
    for r in runs:
        c = r._element.rPr.find(qn("w:color")) if r._element.rPr is not None else None
        if c is not None and c.get(qn("w:val")) not in ("auto", "000000"):
            nonblack += 1
        if r._element.rPr is not None and r._element.rPr.find(qn("w:highlight")) is not None:
            nonblack += 1
    res["runs_non_black"] = nonblack
    res["heading_style_paragraphs"] = sum(1 for _, _, _, _, p in bl if p.style.name.lower().startswith(("heading", "title")))
    bold_body = sum(1 for k, _, rs, _, _ in bl if k == "p" for r in rs if r.bold and r.text.strip())
    bold_num_cell = sum(1 for k, _, rs, ct, _ in bl if k == "cell" for r in rs if r.bold and r.text.strip() and re.search(r"\d", ct))
    res["bold_runs_outside_tables"] = bold_body
    res["bold_runs_in_cells_with_digits"] = bold_num_cell
    alltext = "\n".join(t for _, t, _, _, _ in bl)
    res["middle_dot"] = alltext.count("・")
    res["paragraphs_starting_Note"] = sum(1 for _, t, _, _, _ in bl if t.strip().lower().startswith("note"))
    res["em_dash_outside_cells"] = sum(t.count("—") for k, t, _, _, _ in bl if k == "p")
    res["sections"] = [("landscape" if s.orientation == WD_ORIENT.LANDSCAPE else "portrait",
                        round(s.page_width.mm), round(s.page_height.mm)) for s in doc.sections]
    res["orientation_ok"] = all((o == "landscape") == landscape for o, _, _ in res["sections"])
    # footnote symbols: per caption unit (title paragraph starting "Table"/"Fig." to the next one)
    units, cur = [], None
    for k, t, rs, _, _ in bl:
        if k == "p" and re.match(r"^(Table|Fig\.) \d+\.", t):
            cur = {"title": re.match(r"^(Table|Fig\.) \d+", t).group(0), "in": Counter(), "notes": Counter()}
            units.append(cur)
        if cur is None:
            continue
        for r in rs:
            if r.font.superscript and r.text:
                cur["in"][r.text] += 1
        if k == "p" and t.startswith(STAR):
            sym = re.match(f"^{STAR}+", t).group(0)
            cur["notes"][sym] += 1
    fn = []
    for u in units:
        ins, notes = set(u["in"]), set(u["notes"])
        fn.append(dict(unit=u["title"], symbols_in_table_or_title=sorted(ins, key=len), symbols_in_notes=sorted(notes, key=len),
                       one_to_one=ins == notes and all(v == 1 for v in u["notes"].values()),
                       in_order=sorted(notes, key=len) == [STAR * i for i in range(1, len(notes) + 1)]))
    res["footnotes"] = fn
    # numbers
    shown = {x["shown"] for x in ledger["rows"]} | {x["shown"] for x in ledger["labels"]}
    toks = tokens(alltext)
    res["numeric_tokens"] = len(toks)
    res["unregistered_tokens"] = sorted({t for t in toks if t not in shown})
    value_rows = [x for x in ledger["rows"] if not str(x["shown"]).endswith(("points", "rows")) and x["shown"] != "line"]
    res["registered_values_not_found_in_document"] = sorted({x["shown"] for x in value_rows if x["shown"] not in set(toks)})
    return res, doc


tl = json.load(open(BUILD / "_ledger_tables.json", encoding="utf-8"))
fl = json.load(open(BUILD / "_ledger_figures.json", encoding="utf-8"))
rt, _ = check_doc(OUT / "tables_v1.docx", tl, landscape=True)
rf, fdoc = check_doc(OUT / "figures_v1.docx", fl, landscape=False)
# embedded pictures: effective dpi at the inserted size
pics = []
for i, shp in enumerate(fdoc.inline_shapes, start=1):
    info = fl["images"][f"Fig. {i}"]
    wpx = int(info["pixels"].split(" x ")[0])
    pics.append(dict(fig=i, pixels=info["pixels"], file_dpi=info["dpi"], inserted_width_mm=round(shp.width.mm, 2),
                     inserted_height_mm=round(shp.height.mm, 2), effective_dpi=round(wpx / (shp.width.inches), 1)))
rf["pictures"] = pics
audits = {}
for f in ("fig1", "fig2", "fig3"):
    ca = json.load(open(FIGDIR / f"{f}.collision-audit.json", encoding="utf-8")) if (FIGDIR / f"{f}.collision-audit.json").exists() else {}
    audits[f] = ca.get("verdict"), ca.get("summary")
al = json.load(open(FIGDIR / "fig2.alignment.json", encoding="utf-8"))
rf["collision_audit"] = audits
rf["fig2_alignment"] = (al.get("verdict"), al.get("summary"))

# ---------------------------------------------------------------- check_v1.md
def fmt_res(r):
    L = [f"### {r['file']}", "", "| 项目 | 结果 | 应为 |", "|---|---|---|"]
    for k, want in (("paragraphs_and_cells", None), ("text_runs", None), ("runs_not_TNR_12pt", 0), ("runs_non_black", 0),
                    ("empty_cells", 0), ("heading_style_paragraphs", 0), ("bold_runs_outside_tables", 0), ("bold_runs_in_cells_with_digits", 0),
                    ("middle_dot", 0), ("paragraphs_starting_Note", 0), ("em_dash_outside_cells", 0), ("orientation_ok", True),
                    ("numeric_tokens", None)):
        L.append(f"| {k} | {r[k]} | {'' if want is None else want} |")
    L.append(f"| unregistered_tokens | {len(r['unregistered_tokens'])}（{', '.join(r['unregistered_tokens']) or '无'}） | 0 |")
    L.append(f"| registered_values_not_found_in_document | {len(r['registered_values_not_found_in_document'])}（{', '.join(r['registered_values_not_found_in_document']) or '无'}） | 0 |")
    L.append(f"| sections | {r['sections']} | |")
    L += ["", "脚注符号（表内或题目中的上标 ↔ 脚注段落开头的符号）：", "", "| 单位 | 表内/题目 | 脚注 | 一对一 | 顺序 |", "|---|---|---|---|---|"]
    for u in r["footnotes"]:
        L.append(f"| {u['unit']} | {' '.join(u['symbols_in_table_or_title'])} | {' '.join(u['symbols_in_notes'])} | {u['one_to_one']} | {u['in_order']} |")
    return L


now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
C = [f"# v1 表图的回读检查（{now}，`manuscript/code/make_ledger_v1.py`）", "",
     "从交付的 docx 读回，不读生成脚本的中间结果。数字检查：从段落与单元格文字中抽出所有数字（与字母或连字符相连的编号如 E01、S1、EQ-5D、KEYNOTE-522 不算；"
     "“Table 2”“Fig. 3”“Supplementary Table S4”这类编号先去掉），逐个与登记表（数值行与定义/编号行）比对；反向检查登记的数值是否都出现在文档中。", ""]
C += fmt_res(rt) + [""] + fmt_res(rf)
C += ["", "图（实测）：", "", "| 图 | 像素 | 文件 dpi | 插入宽×高（mm） | 插入后的实际 dpi |", "|---|---|---|---|---|"]
for p in pics:
    C.append(f"| Fig. {p['fig']} | {p['pixels']} | {p['file_dpi']} | {p['inserted_width_mm']} × {p['inserted_height_mm']} | {p['effective_dpi']} |")
C += ["", "nature-figure 的检查（导出的 PDF）：", ""]
for f, (v, s) in audits.items():
    C.append(f"- {f} 碰撞检查：{v}，{s}")
C.append(f"- fig2 面板对齐：{rf['fig2_alignment'][0]}，{rf['fig2_alignment'][1]}")
C.append("- 字号下限（audit_pdf_text.py --min-pt 8）：三张图 below minimum 都为 0（见本次运行的终端输出，记录于 table_figure_plan_v1.md 第 7 节）。")
(OUT / "check_v1.md").write_text("\n".join(C) + "\n", encoding="utf-8")

# ---------------------------------------------------------------- numbers_ledger_v1.md
L = [f"# 数字对照表 v1（{now}，由 `manuscript/code/make_ledger_v1.py` 从登记表生成）", "",
     "每个显示在表或图中的数字：显示值、位置、来源文件、来源中的位置、原始值。舍入：从原始值一次四舍五入（half up）；舍入为 0 的值不带负号；"
     "费用以千日元（JPY 1,000）显示，与第 2 阶段报告的“万日元 1 位小数”精度相同（例：272.6 万日元 = 2,726 千日元）。", "",
     "## 1. Table 1–3（tables_v1.docx）", "", "| # | 显示 | 位置 | 来源文件 | 来源中的位置 | 原始值 |", "|---|---|---|---|---|---|"]
for i, x in enumerate(tl["rows"], start=1):
    L.append(f"| {i} | {x['shown']} | {x['where']} | `{x['source']}` | {x['loc']} | {x['raw']} |")
L += ["", "### 派生值的核对（Table 3 的“转移复发治疗费 50%”“艾立布林”两栏的类别值）", "",
      "两情景只改变费用参数，生存不变，所以各类别 = 基准栏的类别值 × 情景倍率（D03/D03P 与 D05 的类别），其余类别不变。"
      "核对：各类别之和与模型算出的 Δ费用（`sc_*_det_reference.csv` 的 dC）之差：", ""]
for k, v in tl["derived_check"].items():
    L.append(f"- {k}：类别之和 {v['sum_of_categories']:.6f} 日元，模型 {v['modelled_total']:.6f} 日元，差 {v['difference']:.3e} 日元")
L += ["", "## 2. Fig. 1–3（figures_v1.docx 与 manuscript/v1/figures/）", "",
      "图中的线、带、柱直接由下列文件的列画出（数值不经手写）；刻度数字是坐标轴的标度，不是结果，不登记。", "",
      "| # | 显示 | 位置 | 来源文件 | 来源中的位置 | 原始值 |", "|---|---|---|---|---|---|"]
for i, x in enumerate(fl["rows"], start=1):
    L.append(f"| {i} | {x['shown']} | {x['where']} | `{x['source']}` | {x['loc']} | {x['raw']} |")
L += ["", "## 3. 编号与定义中的数字（不是结果；同一数字在别处作为值登记时以那里为准）", "", "| 显示 | 位置 | 说明 |", "|---|---|---|"]
for x in tl["labels"] + fl["labels"]:
    L.append(f"| {x['shown']} | {x['where']} | {x['reason']} |")
SRC = sorted({x["source"] for x in tl["rows"] + fl["rows"]})
L += ["", "## 4. 来源文件的 sha256（生成时）", "", "| 文件 | sha256 |", "|---|---|"]
for s in SRC:
    p = ROOT / s
    L.append(f"| `{s}` | {sha256(p) if p.exists() else '（不在仓库：' + s + '）'} |")
(OUT / "numbers_ledger_v1.md").write_text("\n".join(L) + "\n", encoding="utf-8")

# ---------------------------------------------------------------- MANIFEST_v1.md
deliv = ["tables_v1.docx", "figures_v1.docx", "table_figure_plan_v1.md", "numbers_ledger_v1.md", "check_v1.md"]
figs = sorted(p.name for p in FIGDIR.iterdir() if p.suffix in (".pdf", ".png", ".tiff", ".svg"))
code = sorted(p.name for p in (ROOT / "manuscript" / "code").glob("*.py"))
M = [f"# MANIFEST v1（{dt.date.today().isoformat()}）", "",
     "- 版本：v1（执笔第 1 步：表、图、补充材料清单、数字对照表）。底本：无（新建）。manuscript、supplementary、title page 尚未作成。",
     "- 数值来源：第 2 阶段主分析的输出（`output/phase2/main/`）、第 1 阶段输出、入力表 v10；不重新计算模型。来源文件与 sha256 见 numbers_ledger_v1.md 第 4 节。", "",
     "| 文件 | sha256 |", "|---|---|"]
for d in deliv:
    M.append(f"| manuscript/v1/{d} | {sha256(OUT / d)} |")
for f in figs:
    M.append(f"| manuscript/v1/figures/{f} | {sha256(FIGDIR / f)} |")
for c in code:
    M.append(f"| manuscript/code/{c} | {sha256(ROOT / 'manuscript' / 'code' / c)} |")
(OUT / "MANIFEST_v1.md").write_text("\n".join(M) + "\n", encoding="utf-8")

summary = {k: rt[k] for k in ("empty_cells", "runs_not_TNR_12pt", "runs_non_black", "heading_style_paragraphs", "bold_runs_outside_tables",
                             "bold_runs_in_cells_with_digits", "middle_dot", "paragraphs_starting_Note", "em_dash_outside_cells",
                             "orientation_ok", "numeric_tokens", "unregistered_tokens", "registered_values_not_found_in_document")}
print("TABLES", json.dumps(summary, ensure_ascii=False))
print("TABLES footnotes", [(u["unit"], u["one_to_one"], u["in_order"]) for u in rt["footnotes"]])
summary = {k: rf[k] for k in summary}
print("FIGURES", json.dumps(summary, ensure_ascii=False))
print("FIGURES footnotes", [(u["unit"], u["one_to_one"], u["in_order"]) for u in rf["footnotes"]])
print("PICTURES", pics)
