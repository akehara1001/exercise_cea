"""Read back the delivered docx files, check them against WRITING_RULES, and write
numbers_ledger_<VER>.md, check_<VER>.md and MANIFEST_<VER>.md.

Files checked: tables, figures, supplement, results (each <name>_<VER>.docx).
Run after make_tables.py, make_figures.py, make_supplement.py, make_results.py and
compare_versions.py, and after table_figure_plan_<VER>.md is final (the manifest
hashes it).
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.table import Table
from docx.text.paragraph import Paragraph

from common import BASE, BUILD, FIGDIR, NUM_RE, OUT, PREV, ROOT, STAR, VER, rel, sha256

sys.stdout.reconfigure(encoding="utf-8")
REF_RE = re.compile(r"\b(?:Supplementary )?(?:Tables?|Figs?\.) S?\d+[a-z]?(?:\s*(?:and|to|,)\s*S?\d+)*")
UNIT_RE = re.compile(r"^(Table \d+|Fig\. \d+|Supplementary Table S\d+|Supplementary Fig\. S\d+)\.")
ARS_ACRO = Path.home() / "Documents" / "ClaudeCode" / "academic-research-skills" / "scripts" / "check_acronyms.py"


def blocks(doc):
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


def shown_set(*ledgers):
    s = set()
    for led in ledgers:
        s |= {x["shown"] for x in led["rows"]} | {x["shown"] for x in led.get("labels", [])}
    return s


def check_doc(path, ledgers, orientation):
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
        rpr = r._element.rPr
        c = rpr.find(qn("w:color")) if rpr is not None else None
        if c is not None and c.get(qn("w:val")) not in ("auto", "000000"):
            nonblack += 1
        if rpr is not None and rpr.find(qn("w:highlight")) is not None:
            nonblack += 1
    res["runs_non_black"] = nonblack
    res["heading_style_paragraphs"] = sum(1 for _, _, _, _, p in bl if p.style.name.lower().startswith(("heading", "title")))
    res["bold_runs_outside_tables"] = sum(1 for k, t, rs, _, _ in bl if k == "p" and t.strip() != "Results" for r in rs if r.bold and r.text.strip())
    res["bold_runs_in_cells_with_digits"] = sum(1 for k, _, rs, ct, _ in bl if k == "cell" for r in rs if r.bold and r.text.strip() and re.search(r"\d", ct))
    alltext = "\n".join(t for _, t, _, _, _ in bl)
    res["middle_dot"] = alltext.count("・")
    res["paragraphs_starting_Note"] = sum(1 for _, t, _, _, _ in bl if t.strip().lower().startswith("note"))
    res["em_dash_outside_cells"] = sum(t.count("—") for k, t, _, _, _ in bl if k == "p")
    secs = [("landscape" if s.orientation == WD_ORIENT.LANDSCAPE else "portrait", round(s.page_width.mm), round(s.page_height.mm)) for s in doc.sections]
    res["sections"] = secs
    if isinstance(orientation, list):
        res["orientation_ok"] = [o for o, _, _ in secs] == orientation
    else:
        res["orientation_ok"] = all(o == orientation for o, _, _ in secs)
    units, cur = [], None
    for k, t, rs, _, _ in bl:
        m = UNIT_RE.match(t) if k == "p" else None
        if m:
            cur = {"title": m.group(1), "in": Counter(), "notes": Counter()}
            units.append(cur)
        if cur is None:
            continue
        for r in rs:
            if r.font.superscript and r.text:
                cur["in"][r.text] += 1
        if k == "p" and t.startswith(STAR):
            cur["notes"][re.match(f"^{STAR}+", t).group(0)] += 1
    res["footnotes"] = [dict(unit=u["title"], symbols_in_table_or_title=sorted(set(u["in"]), key=len), symbols_in_notes=sorted(set(u["notes"]), key=len),
                             one_to_one=set(u["in"]) == set(u["notes"]) and all(v == 1 for v in u["notes"].values()),
                             in_order=sorted(set(u["notes"]), key=len) == [STAR * i for i in range(1, len(u["notes"]) + 1)]) for u in units]
    shown = shown_set(*ledgers)
    toks = tokens(alltext)
    res["numeric_tokens"] = len(toks)
    res["unregistered_tokens"] = sorted({t for t in toks if t not in shown})
    vals = [x for led in ledgers for x in led["rows"] if not str(x["shown"]).endswith(("points", "rows")) and x["shown"] not in ("line", "curves")]
    res["registered_values_not_found_in_document"] = sorted({x["shown"] for x in vals if x["shown"] not in set(toks)})
    return res, doc


tl = json.load(open(BUILD / "_ledger_tables.json", encoding="utf-8"))
fl = json.load(open(BUILD / "_ledger_figures.json", encoding="utf-8"))
sl = json.load(open(BUILD / "_ledger_supplement.json", encoding="utf-8"))
sfl = json.load(open(BUILD / "_ledger_suppfigs.json", encoding="utf-8"))
rl = json.load(open(BUILD / "_ledger_results.json", encoding="utf-8"))

rt, _ = check_doc(OUT / f"tables_{VER}.docx", [tl], "landscape")
rf, fdoc = check_doc(OUT / f"figures_{VER}.docx", [fl], "portrait")
supp_orient = []
for kind in sl["order_kinds"]:
    supp_orient.append("portrait" if kind == "figure" else "landscape")
rs, sdoc = check_doc(OUT / f"supplement_{VER}.docx", [sl, sfl], supp_orient)
rr, rdoc = check_doc(OUT / f"results_{VER}.docx", [tl, sl, fl, sfl], "portrait")
rr["registered_values_not_found_in_document"] = []  # not applicable: the Results cite a selection of cells

pics = []
for i, shp in enumerate(fdoc.inline_shapes, start=1):
    info = fl["images"][f"Fig. {i}"]
    wpx = int(info["pixels"].split(" x ")[0])
    pics.append(dict(fig=f"Fig. {i}", pixels=info["pixels"], file_dpi=info["dpi"], inserted_width_mm=round(shp.width.mm, 2),
                     inserted_height_mm=round(shp.height.mm, 2), effective_dpi=round(wpx / shp.width.inches, 1)))
for name, shp in zip(("Supplementary Fig. S1", "Supplementary Fig. S2"), sdoc.inline_shapes):
    info = sfl["images"][name]
    wpx = int(info["pixels"].split(" x ")[0])
    pics.append(dict(fig=name, pixels=info["pixels"], file_dpi=info["dpi"], inserted_width_mm=round(shp.width.mm, 2),
                     inserted_height_mm=round(shp.height.mm, 2), effective_dpi=round(wpx / shp.width.inches, 1)))
audits = {}
for f in ("fig1", "fig2", "fig3", "figS1", "figS2"):
    p = FIGDIR / f"{f}.collision-audit.json"
    ca = json.load(open(p, encoding="utf-8")) if p.exists() else {}
    audits[f] = (ca.get("verdict"), ca.get("summary"))
align = {f: (lambda d: (d.get("verdict"), d.get("summary")))(json.load(open(FIGDIR / f"{f}.alignment.json", encoding="utf-8"))) for f in ("fig2", "figS1")}

# ---------------------------------------------------------------- Results-specific checks
BANNED = ["delve", "underscore", "highlight", "landscape", "leverage", "robust", "nuanced", "crucial", "pivotal", "notably", "importantly",
          "it is worth noting", "in the realm of", "a testament to", "shed light on", "paving the way", "multifaceted", "holistic", "comprehensive",
          "align with", "navigate", "tapestry", "ever-evolving", "foster", "showcase", "embark", "realm", "intricate", "cornerstone", "paradigm",
          "synergy", "streamline", "cutting-edge", "groundbreaking"]
THROAT = ["it is important to note", "it should be noted", "it is worth mentioning", "it goes without saying", "as a matter of fact",
          "when it comes to", "with that being said", "in today's"]
META = ["this section", "the following paragraph", "we now turn", "as noted above"]
CONNECT = ["moreover", "furthermore", "additionally", "in addition"]
HEDGE = [r"\bmay\b", r"\bmight\b", r"\bappear(?:s|ed)?\b", r"\bsuggest(?:s|ed)?\b"]
METHODS = [r"\bwe used\b", r"\bwas used\b", r"\bwere used\b", r"\bwe performed\b", r"\bwas performed\b", r"\bwe conducted\b"]
TIME = [r"\brecently\b", r"\bcurrently\b", r"\bthe latest\b", r"\bin recent years\b"]
CAUSAL = [r"\bcaused\b", r"\bled to\b", r"\bimpact\b", r"\bimproved\b"]
DEF_TOKENS = {"5": "threshold JPY 5 million (Table 2 title)", "7.5": "threshold JPY 7.5 million (Table 3)", "1": "1 year after surgery (Table 1)",
              "95": "95% UI (Table 2 footnote)"}

body = [p for p in rdoc.paragraphs if p.text.strip()]
heading = body[0]
paras = body[1:]
R = {}
R["heading_is_Results_bold_normal"] = heading.text == "Results" and all(r.bold for r in heading.runs) and heading.style.name == "Normal"
R["paragraphs"] = len(paras)
R["double_spacing_paragraphs"] = sum(1 for p in [heading] + paras if p.paragraph_format.line_spacing_rule == WD_LINE_SPACING.DOUBLE)
R["line_numbering"] = any(s._sectPr.find(qn("w:lnNumType")) is not None for s in rdoc.sections)
text = "\n".join(p.text for p in paras)
low = text.lower()
R["banned_terms"] = {w: low.count(w) for w in BANNED if low.count(w)}
R["throat_clearing"] = {w: low.count(w) for w in THROAT if low.count(w)}
R["meta_commentary"] = {w: low.count(w) for w in META if low.count(w)}
R["hedges"] = {h: len(re.findall(h, low)) for h in HEDGE if re.findall(h, low)}
R["methods_phrases"] = {h: len(re.findall(h, low)) for h in METHODS if re.findall(h, low)}
R["bare_time_words"] = {h: len(re.findall(h, low)) for h in TIME if re.findall(h, low)}
R["causal_words"] = {h: len(re.findall(h, low)) for h in CAUSAL if re.findall(h, low)}
R["em_dash"] = text.count("—")
R["connectives_per_paragraph_max"] = max(sum(p.text.lower().count(c) for c in CONNECT) for p in paras)
sents = [s for sents in rl["paragraphs"] for s in sents]
wc = [len(s["text"].split()) for s in sents]
R["sentences"] = len(sents)
R["sentences_over_30_words"] = sum(1 for w in wc if w > 30)
R["longest_sentence_words"] = max(wc)
pw = [sum(len(s["text"].split()) for s in ps) for ps in rl["paragraphs"]]
R["paragraph_words"] = pw
R["paragraphs_over_150_words"] = sum(1 for w in pw if w > 150)
R["words_total"] = sum(pw)
R["paragraphs_open_with_table_or_figure"] = sum(1 for ps in rl["paragraphs"] if re.match(r"^(Table \d|Fig\. \d|Supplementary (Table|Fig\.) S\d)", ps[0]["text"]))
R["sentences_without_table_or_figure_reference"] = [s["text"] for s in sents if not re.search(r"(Table|Tables|Fig\.) S?\d", s["text"])]
# numbers: every token of a sentence must be a value shown in a table the sentence cites (or a definitional token)
allrows = {"tables": tl["rows"] + tl["labels"], "supplement": sl["rows"] + sl["labels"], "figures": fl["rows"] + sfl["rows"] + fl["labels"] + sfl["labels"]}
bad = []
for pi, ps in enumerate(rl["paragraphs"], start=1):
    for si, s in enumerate(ps, start=1):
        cited = s["cites"]
        allowed = {x["shown"] for rows in allrows.values() for x in rows if any(x["where"].startswith(c) for c in cited)}
        for t in tokens(s["text"]):
            if t not in allowed and t not in DEF_TOKENS:
                bad.append((pi, si, t))
R["numbers_not_in_cited_tables"] = bad
R["numeric_tokens"] = sum(len(tokens(s["text"])) for s in sents)
order = []
for m in re.finditer(r"(Supplementary Tables?|Supplementary Fig\.|Table|Fig\.) (S?\d+)(?:\s*and\s*(S?\d+))?", text):
    kind = m.group(1).replace("Tables", "Table")
    for num in (m.group(2), m.group(3)):
        if num:
            key = f"{kind} {num}"
            if key not in order:
                order.append(key)
R["first_citation_order"] = order
series = defaultdict(list)
for k in order:
    series[k.rsplit(" ", 1)[0]].append(int(re.sub(r"\D", "", k.rsplit(" ", 1)[1])))
R["first_citation_order_by_series"] = dict(series)
R["first_citation_in_order"] = all(v == sorted(v) for v in series.values())
# ARS acronym check on the plain text
plain = BUILD / f"results_{VER}_plain.md"
plain.write_text("\n\n".join(p.text for p in paras) + "\n", encoding="utf-8")
try:
    acr = subprocess.run([sys.executable, str(ARS_ACRO), "--input", str(plain), "--scopes", "body", "--lang", "en",
                          "--json-out", str(BUILD / "acronyms_results.json"), "--allow", "JPY", "--allow", "ICER", "--allow", "QALY"], capture_output=True, text=True, encoding="utf-8", timeout=120)
    R["acronym_check_stdout"] = acr.stdout.strip()
    R["acronym_check_exit"] = acr.returncode
except Exception as e:  # noqa: BLE001
    R["acronym_check_stdout"] = f"did not run: {e}"
    R["acronym_check_exit"] = None

# ---------------------------------------------------------------- same value from the same source cell in two tables
def norm_loc(src, loc):
    m = re.search(r"cell [A-Z]+\d+", loc)
    if m:
        return (Path(src).name, m.group(0))
    loc = re.sub(r"\[derived.*?\]", "", loc).replace(", column = base", "")
    loc = re.sub(r"\d+\.\d+", lambda k: repr(round(float(k.group(0)), 6)), loc)
    return (Path(src).name, re.sub(r"\s+", " ", loc).strip())


owners = defaultdict(set)
for reg, rows in (("tables", tl["rows"]), ("supplement", sl["rows"])):
    for x in rows:
        if x["shown"] in ("see file", "curves", "line") or str(x["shown"]).endswith(("points", "rows")):
            continue
        tab = re.match(r"^(Table \d+|Supplementary Table S\d+)", x["where"])
        if tab:
            owners[norm_loc(x["source"], x["loc"])].add(tab.group(1))
dups = Counter()
for k, tabs in owners.items():
    if len(tabs) > 1:
        dups[" & ".join(sorted(tabs))] += 1
EXCEPTIONS = {"Supplementary Table S4 & Table 2": "E1（Table 2 Panel B、C 的基准行与 S4；2026-10-26 决定）",
              "Supplementary Table S1 & Table 1": "E2（S1 完整参数表与 Table 1；2026-10-26 决定）",
              "Supplementary Table S6 & Table 2": "E3（S6 完整网格与 Table 2 Panel B 的 HR 0.85 两行；待确认）",
              "Supplementary Table S10 & Table 3": "E4（S10 的 S-JP 参照 ICER 与 Table 3 的 S-JP 栏；待确认）"}

# ---------------------------------------------------------------- check_<VER>.md
def fmt_res(r):
    L = [f"### {r['file']}", "", "| 项目 | 结果 | 应为 |", "|---|---|---|"]
    for k, want in (("paragraphs_and_cells", None), ("text_runs", None), ("runs_not_TNR_12pt", 0), ("runs_non_black", 0),
                    ("empty_cells", 0), ("heading_style_paragraphs", 0), ("bold_runs_outside_tables", 0), ("bold_runs_in_cells_with_digits", 0),
                    ("middle_dot", 0), ("paragraphs_starting_Note", 0), ("em_dash_outside_cells", 0), ("orientation_ok", True), ("numeric_tokens", None)):
        L.append(f"| {k} | {r[k]} | {'' if want is None else want} |")
    L.append(f"| unregistered_tokens | {len(r['unregistered_tokens'])}（{', '.join(r['unregistered_tokens']) or '无'}） | 0 |")
    nf = r["registered_values_not_found_in_document"]
    L.append(f"| registered_values_not_found_in_document | {len(nf)}（{', '.join(nf) or '无'}） | 0 |")
    L.append(f"| sections | {r['sections']} | |")
    if r["footnotes"]:
        L += ["", "脚注符号（表内或题目中的上标 ↔ 脚注段落开头的符号）：", "", "| 单位 | 表内/题目 | 脚注 | 一对一 | 顺序 |", "|---|---|---|---|---|"]
        for u in r["footnotes"]:
            L.append(f"| {u['unit']} | {' '.join(u['symbols_in_table_or_title'])} | {' '.join(u['symbols_in_notes'])} | {u['one_to_one']} | {u['in_order']} |")
    return L


now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
C = [f"# {VER} 的回读检查（{now}，`manuscript/code/make_ledger.py`）", "",
     "从交付的 docx 读回。数字检查：抽出所有数字（与字母或连字符相连的编号如 E01、S1、EQ-5D、KEYNOTE-522 不算；表与图的编号先去掉），"
     "逐个与登记表比对；反向检查登记的数值是否都出现在文档中。Results 另按句检查：每个数字须是该句所引表格中某一格的显示值。", ""]
for r in (rt, rf, rs, rr):
    C += fmt_res(r) + [""]
C += ["## Results 的检查", "", "| 项目 | 结果 |", "|---|---|"]
for k, v in R.items():
    if k in ("acronym_check_stdout",):
        continue
    C.append(f"| {k} | {v} |")
C += ["", "ARS check_acronyms.py（body 范围）：", "", "```", R["acronym_check_stdout"], "```", ""]
C += ["## 图（实测）", "", "| 图 | 像素 | 文件 dpi | 插入宽×高（mm） | 插入后的实际 dpi |", "|---|---|---|---|---|"]
for p in pics:
    C.append(f"| {p['fig']} | {p['pixels']} | {p['file_dpi']} | {p['inserted_width_mm']} × {p['inserted_height_mm']} | {p['effective_dpi']} |")
C += ["", "nature-figure 的检查（导出的 PDF）：", ""]
for f, (v, s) in audits.items():
    C.append(f"- {f} 碰撞检查：{v}，{s}")
for f, (v, s) in align.items():
    C.append(f"- {f} 面板对齐：{v}，{s}")
C += ["", "## 同一来源格出现在两张表中（规约第 6.1 节）", "", "| 表 | 格数 | 归类 |", "|---|---|---|"]
for k, n in sorted(dups.items()):
    C.append(f"| {k} | {n} | {EXCEPTIONS.get(k, '未登记的重复')} |")
(OUT / f"check_{VER}.md").write_text("\n".join(C) + "\n", encoding="utf-8")

# ---------------------------------------------------------------- numbers_ledger_<VER>.md
def provisional(x):
    txt = f"{x['where']} {x['loc']}"
    if "E03" in txt:
        return "【要確認】E03"
    if "(D02)" in txt or ", D02," in txt or txt.startswith("Supplementary Table S9, D02"):
        return "【要確認】D02"
    if "(F01P)" in txt or "Supplementary Table S10, sjp" in x["where"] or ", sjp" in x["where"]:
        return "【要確認】S-JP 依赖 F01P"
    if x["source"].endswith("oneway_base.csv") and x["where"].startswith("Fig. 3, bars"):
        return "【要確認】含 D02 的一行"
    return ""


def table_rows(rows):
    out = ["| # | 显示 | 位置 | 来源文件 | 来源中的位置 | 原始值 | 暂定 |", "|---|---|---|---|---|---|---|"]
    for i, x in enumerate(rows, start=1):
        out.append(f"| {i} | {x['shown']} | {x['where']} | `{x['source']}` | {x['loc']} | {x['raw']} | {provisional(x)} |")
    return out


L = [f"# 数字对照表 {VER}（{now}，由 `manuscript/code/make_ledger.py` 从登记表生成）", "",
     "每个显示的数字：显示值、位置、来源文件、来源中的位置、原始值。舍入：从原始值一次四舍五入（half up）；舍入为 0 的值不带负号；"
     "费用以千日元（JPY 1,000）显示，与第 2 阶段报告的“万日元 1 位小数”精度相同。", "",
     "## 1. Results：每句所依据的表格位置", ""]
for pi, ps in enumerate(rl["paragraphs"], start=1):
    for si, s in enumerate(ps, start=1):
        L.append(f"- P{pi}.{si}　{s['text']}")
        L.append(f"  - 所引：{'、'.join(s['cites'])}")
        for u in [u for u in rl["used"] if u["paragraph"] == pi and u["sentence"] == si]:
            L.append(f"  - {u['shown']} ← {u['where']}（`{u['source']}`：{u['loc']}）")
L += ["", f"## 2. Table 1–3（tables_{VER}.docx）", ""] + table_rows(tl["rows"])
L += ["", "### 派生值的核对（Table 3 的“转移复发治疗费 50%”“艾立布林”两栏的类别值）", ""]
for k, v in tl["derived_check"].items():
    L.append(f"- {k}：类别之和 {v['sum_of_categories']:.6f} 日元，模型 {v['modelled_total']:.6f} 日元，差 {v['difference']:.3e} 日元")
L += ["", f"## 3. Fig. 1–3（figures_{VER}.docx）", "", "图中的线、带、柱直接由下列文件的列画出；刻度数字是标度，不登记。", ""] + table_rows(fl["rows"])
L += ["", f"## 4. 补充表（supplement_{VER}.docx）", ""] + table_rows(sl["rows"])
L += ["", "## 5. 补充图（supplement 中的 Supplementary Fig. S1、S2）", ""] + table_rows(sfl["rows"])
prov = [x for rows in (tl["rows"], fl["rows"], sl["rows"], sfl["rows"]) for x in rows if provisional(x)]
L += ["", "## 6. 暂定值（【要確認】）", "",
      "入力表 v10 中备考为【要確認】、并在表图中显示（或直接由其算出）的值：E03（远程低价方案费用）、D02（局部区域复发后的月额）与 F01P（S-JP 情景）。"
      "其余【要確認】行（B03、B04、B07–B10）只在 Supplementary Table S1 中作为输入列出。", "", "| 显示 | 位置 | 标记 |", "|---|---|---|"]
for x in prov:
    L.append(f"| {x['shown']} | {x['where']} | {provisional(x)} |")
L += ["", "## 7. 编号与定义中的数字（不是结果）", "", "| 显示 | 位置 | 说明 |", "|---|---|---|"]
for x in tl["labels"] + fl["labels"] + sl["labels"] + sfl["labels"]:
    L.append(f"| {x['shown']} | {x['where']} | {x['reason']} |")
SRC = sorted({x["source"] for rows in (tl["rows"], fl["rows"], sl["rows"], sfl["rows"]) for x in rows})
L += ["", "## 8. 来源文件的 sha256（生成时）", "", "| 文件 | sha256 |", "|---|---|"]
for s in SRC:
    paths = [ROOT / q.strip() for q in s.split(";")] if ";" in s else [ROOT / s.split(" (")[0]]
    for p in paths:
        L.append(f"| `{rel(p)}` | {sha256(p) if p.exists() else '（不在仓库）'} |")
(OUT / f"numbers_ledger_{VER}.md").write_text("\n".join(L) + "\n", encoding="utf-8")

# ---------------------------------------------------------------- MANIFEST_<VER>.md
deliv = [f"tables_{VER}.docx", f"figures_{VER}.docx", f"supplement_{VER}.docx", f"results_{VER}.docx", f"table_figure_plan_{VER}.md",
         f"numbers_ledger_{VER}.md", f"check_{VER}.md", f"diff_{PREV}_{VER}.md"]
figs = sorted(p.name for p in FIGDIR.iterdir() if p.suffix in (".pdf", ".png", ".tiff", ".svg"))
code = sorted(p.name for p in (ROOT / "manuscript" / "code").iterdir() if p.suffix in (".py", ".R"))
M = [f"# MANIFEST {VER}（{dt.date.today().isoformat()}）", "",
     f"- 版本：{VER}（执笔第 2 步：补充表与 Results）。底本：{BASE}。Introduction、Methods、Discussion、Abstract 与 title page 尚未作成。",
     f"- 数值来源：第 1、2 阶段的输出与入力表 v10；不重新计算模型。来源文件与 sha256 见 numbers_ledger_{VER}.md 第 8 节。", "",
     "| 文件 | sha256 |", "|---|---|"]
for d in deliv:
    M.append(f"| manuscript/{VER}/{d} | {sha256(OUT / d)} |")
for f in figs:
    M.append(f"| manuscript/{VER}/figures/{f} | {sha256(FIGDIR / f)} |")
for c in code:
    M.append(f"| manuscript/code/{c} | {sha256(ROOT / 'manuscript' / 'code' / c)} |")
(OUT / f"MANIFEST_{VER}.md").write_text("\n".join(M) + "\n", encoding="utf-8")

for name, r in (("TABLES", rt), ("FIGURES", rf), ("SUPPLEMENT", rs), ("RESULTS", rr)):
    print(name, {k: r[k] for k in ("empty_cells", "runs_not_TNR_12pt", "runs_non_black", "heading_style_paragraphs", "bold_runs_outside_tables",
                                   "bold_runs_in_cells_with_digits", "middle_dot", "paragraphs_starting_Note", "em_dash_outside_cells", "orientation_ok", "numeric_tokens")},
          "unregistered", r["unregistered_tokens"], "not found", len(r["registered_values_not_found_in_document"]))
    if r["footnotes"]:
        print("  footnotes", [(u["unit"], u["one_to_one"], u["in_order"]) for u in r["footnotes"]])
print("RESULTS checks", {k: v for k, v in R.items() if k != "acronym_check_stdout"})
print("ACRONYMS", R["acronym_check_stdout"][-600:])
print("DUPLICATES", dict(dups))
print("PICTURES", [(p["fig"], p["effective_dpi"]) for p in pics])
