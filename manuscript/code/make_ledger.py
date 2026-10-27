"""Read back the delivered docx files, check them against WRITING_RULES, and write
numbers_ledger_<VER>.md, check_<VER>.md and MANIFEST_<VER>.md.

Files checked: manuscript, tables, figures, supplement (each <name>_<VER>.docx).
Run after the build (make_tables.py, make_figures.py, make_supplement.py,
edit_manuscript.py (v5), number_refs.py, word_pages.py, make_supplement.py and
number_refs.py again), compare_versions.py and make_references_doc.py, and after
table_figure_plan_<VER>.md is final (the manifest hashes it).

Reference numbers are superscript runs of digits, commas and en dashes; they are
checked as citations and left out of the number checks. Footnote symbols are the
other superscript runs.
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

from common import BASE, BUILD, FIGDIR, NUM_RE, OUT, PREV, ROOT, STAR, STEP, SUPP, VER, rel, sha256
from references import CROSSREF, DOICHECK, MARK_RE, PUBMED, entry, expand, year

sys.stdout.reconfigure(encoding="utf-8")
REF_RE = re.compile(r"\b(?:Supplementary )?(?:Tables?|Figs?\.|Methods) S?\d+[a-z]?(?:\s*(?:and|to|,)\s*S?\d+)*")
UNIT_RE = re.compile(r"^(Table \d+|Fig\. \d+|Supplementary Table S\d+|Supplementary Fig\. S\d+)\.")
CIT_RE = re.compile(r"^[\d,–]+$")
ARS_ACRO = Path.home() / "Documents" / "ClaudeCode" / "academic-research-skills" / "scripts" / "check_acronyms.py"


def is_cite(r):
    return bool(r.font.superscript and r.text and CIT_RE.fullmatch(r.text))


def ptext(p):
    """Paragraph text without reference numbers."""
    return "".join(r.text for r in p.runs if not is_cite(r))


def blocks(doc):
    out = []
    for el in doc.element.body.iterchildren():
        tag = el.tag.split("}")[1]
        if tag == "p":
            p = Paragraph(el, doc)
            out.append(("p", ptext(p), p.runs, None, p))
        elif tag == "tbl":
            t = Table(el, doc)
            seen = {}  # id -> element; holding the element keeps its id from being reused
            for row in t.rows:
                for c in row.cells:
                    if id(c._tc) in seen:
                        continue
                    seen[id(c._tc)] = c._tc
                    for p in c.paragraphs:
                        out.append(("cell", ptext(p), p.runs, "".join(ptext(q) for q in c.paragraphs), p))
    return out


def tokens(text):
    return [m.group(0).rstrip(",") for m in NUM_RE.finditer(REF_RE.sub(" ", text))]


def shown_set(*ledgers):
    s = set()
    for led in ledgers:
        s |= {x["shown"] for x in led["rows"]} | {x["shown"] for x in led.get("labels", [])}
    return s


def check_doc(path, ledgers, orientation, bold_ok=lambda t: False, numbers_stop_at=None):
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
    res["bold_runs_outside_tables"] = sum(1 for k, t, rs, _, _ in bl if k == "p" and not bold_ok(t.strip()) for r in rs if r.bold and r.text.strip())
    res["bold_runs_in_cells_with_digits"] = sum(1 for k, _, rs, ct, _ in bl if k == "cell" for r in rs if r.bold and r.text.strip() and re.search(r"\d", ct))
    alltext = "\n".join(t for _, t, _, _, _ in bl)
    res["middle_dot"] = alltext.count("・")
    res["paragraphs_starting_Note"] = sum(1 for _, t, _, _, _ in bl if t.strip().lower().startswith("note"))
    res["em_dash_outside_cells"] = sum(t.count("—") for k, t, _, _, _ in bl if k == "p")
    res["citation_runs"] = sum(1 for r in runs if is_cite(r))
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
        if k == "p" and t.startswith("Supplementary Methods"):
            cur = None
        if cur is None:
            continue
        for r in rs:
            if r.font.superscript and r.text and not is_cite(r):
                cur["in"][r.text] += 1
        if k == "p" and t.startswith(STAR):
            cur["notes"][re.match(f"^{STAR}+", t).group(0)] += 1
    res["footnotes"] = [dict(unit=u["title"], symbols_in_table_or_title=sorted(set(u["in"]), key=len), symbols_in_notes=sorted(set(u["notes"]), key=len),
                             one_to_one=set(u["in"]) == set(u["notes"]) and all(v == 1 for v in u["notes"].values()),
                             in_order=sorted(set(u["notes"]), key=len) == [STAR * i for i in range(1, len(u["notes"]) + 1)]) for u in units]
    shown = shown_set(*ledgers)
    if numbers_stop_at:  # the reference list is checked against the DOI records, not the number registries
        cut = next(i for i, (k, t, _, _, _) in enumerate(bl) if k == "p" and t.strip() == numbers_stop_at)
        alltext = "\n".join(t for _, t, _, _, _ in bl[:cut])
        res["numbers_checked_up_to"] = numbers_stop_at
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
ml = json.load(open(BUILD / "_ledger_manuscript.json", encoding="utf-8"))
mm = json.load(open(BUILD / "_manuscript_map.json", encoding="utf-8"))
rf_ = json.load(open(BUILD / "_refs.json", encoding="utf-8"))
mled = {"rows": ml["rows"], "labels": []}

HEADINGS = ["Introduction", "Methods", "Study background", "Outcome", "Variables", "Statistical analysis", "Results", "References"]
rt, _ = check_doc(OUT / f"tables_{VER}.docx", [tl], "landscape")
rf, fdoc = check_doc(OUT / f"figures_{VER}.docx", [fl], "portrait")
supp_orient = ["portrait" if kind in ("figure", "methods") else "landscape" for kind in sl["order_kinds"]]
SUPP_HEAD = {"Reconstructed patient-level data", "Event-free survival after surgery", "Events before surgery, first events after surgery and deaths from adverse events",
             "Survival after recurrence and background mortality", "Validation", "Probabilistic sensitivity analysis"}
rs, sdoc = check_doc(OUT / f"supplement_{VER}.docx", [sl, sfl], supp_orient, bold_ok=lambda t: t in SUPP_HEAD)
rm, mdoc = check_doc(OUT / f"manuscript_{VER}.docx", [tl, sl, fl, sfl, mled], "portrait", bold_ok=lambda t: t in HEADINGS, numbers_stop_at="References")
rm["registered_values_not_found_in_document"] = []  # not applicable: the text cites a selection of cells

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

# ================================================================ manuscript structure
allp = [p for p in mdoc.paragraphs if p.text.strip()]
heads = [p for p in allp if p.runs and all(r.bold for r in p.runs if r.text.strip())]
M = {}
M["headings"] = [p.text for p in heads]
M["headings_as_specified"] = M["headings"] == HEADINGS
M["headings_bold_normal_12pt"] = all(p.style.name == "Normal" for p in heads)
i_res = next(i for i, p in enumerate(allp) if p.text == "Results")
i_ref = next(i for i, p in enumerate(allp) if p.text == "References")
body_ps = [p for p in allp[:i_ref] if p not in heads]  # Introduction to Results
res_ps = [p for p in allp[i_res + 1:i_ref]]
ref_ps = allp[i_ref + 1:]
ids = [o["id"] for o in mm["order"] if o["id"]]
assert len(ids) == len(body_ps), (len(ids), len(body_ps))
PID = dict(zip(ids, body_ps))
M["body_paragraphs"] = len(body_ps)
M["double_spacing_paragraphs"] = f"{sum(1 for p in allp if p.paragraph_format.line_spacing_rule == WD_LINE_SPACING.DOUBLE)}/{len(allp)}"
M["line_numbering"] = any(s._sectPr.find(qn("w:lnNumType")) is not None for s in mdoc.sections)

# ================================================================ Results-specific checks (ledger of the Results)
BANNED = ["delve", "underscore", "highlight", "landscape", "leverage", "robust", "nuanced", "crucial", "pivotal", "notably", "importantly",
          "it is worth noting", "in the realm of", "a testament to", "shed light on", "paving the way", "multifaceted", "holistic", "comprehensive",
          "align with", "navigate", "tapestry", "ever-evolving", "foster", "showcase", "embark", "realm", "intricate", "cornerstone", "paradigm",
          "synergy", "streamline", "cutting-edge", "groundbreaking"]
THROAT = ["it is important to note", "it should be noted", "it is worth mentioning", "it goes without saying", "as a matter of fact",
          "when it comes to", "with that being said", "in today's"]
META = ["this section", "the following paragraph", "we now turn", "as noted above", "described above", "see above"]
CONNECT = ["moreover", "furthermore", "additionally", "in addition"]
HEDGE = [r"\bmay\b", r"\bmight\b", r"\bappear(?:s|ed)?\b", r"\bsuggest(?:s|ed)?\b"]
METHODS = [r"\bwe used\b", r"\bwas used\b", r"\bwere used\b", r"\bwe performed\b", r"\bwas performed\b", r"\bwe conducted\b"]
TIME = [r"\brecently\b", r"\bcurrently\b", r"\bthe latest\b", r"\bin recent years\b"]
CAUSAL = [r"\bcaused\b", r"\bled to\b", r"\bimpact\b", r"\bimproved\b"]
DEF_TOKENS = {"5": "threshold JPY 5 million (Table 2 title)", "7.5": "threshold JPY 7.5 million (Table 3)", "1": "1 year after surgery (Table 1)",
              "95": "95% UI (Table 2 footnote)"}

R = {}
R["paragraphs"] = len(res_ps)
R["ledger_matches_docx"] = [p.text for p in res_ps] == [" ".join(s["text"] for s in ps) for ps in rl["paragraphs"]]
sents = [s for ps in rl["paragraphs"] for s in ps]
R["sentences"] = len(sents)
R["paragraph_words"] = [sum(len(s["text"].split()) for s in ps) for ps in rl["paragraphs"]]
R["paragraphs_open_with_table_or_figure"] = sum(1 for ps in rl["paragraphs"] if re.match(r"^(Table \d|Fig\. \d|Supplementary (Table|Fig\.) S\d)", ps[0]["text"]))


def own(t):
    return re.search(r"(Table|Tables|Fig\.) S?\d", t)


R["sentences_without_own_reference"] = [s["text"] for s in sents if not own(s["text"])]
# a sentence without its own reference is followed, in the same paragraph, by one that cites a table it relies on (instruction section 2)
orphan = []
for ps in rl["paragraphs"]:
    for i, s in enumerate(ps):
        if own(s["text"]):
            continue
        later = " ".join(x["text"] for x in ps[i + 1:])
        if not any(c in later or c.replace("Table ", "Tables ") in later for c in s["cites"]):
            orphan.append(s["text"])
R["sentences_without_a_later_reference_to_their_table"] = orphan
allrows = {"tables": tl["rows"] + tl["labels"], "supplement": sl["rows"] + sl["labels"], "figures": fl["rows"] + sfl["rows"] + fl["labels"] + sfl["labels"]}
bad = []
for pi, ps in enumerate(rl["paragraphs"], start=1):
    for si, s in enumerate(ps, start=1):
        allowed = {x["shown"] for rows in allrows.values() for x in rows if any(x["where"].startswith(c) for c in s["cites"])}
        for t in tokens(s["text"]):
            if t not in allowed and t not in DEF_TOKENS:
                bad.append((pi, si, t))
R["numbers_not_in_cited_tables"] = bad
R["numeric_tokens"] = sum(len(tokens(s["text"])) for s in sents)

# ================================================================ Introduction and Methods: numbers registered per paragraph
MI = {}
miss = []
for pid in ids:
    if pid.startswith("R."):
        continue
    reg = {r["shown"] for r in ml["rows"] if r["where"] == pid}
    for t in tokens(ptext(PID[pid])):
        if t not in reg:
            miss.append((pid, t))
MI["numbers_not_registered_for_their_paragraph"] = miss
MI["numeric_tokens"] = sum(len(tokens(ptext(PID[pid]))) for pid in ids if not pid.startswith("R."))
MI["registered_numbers"] = len(ml["rows"])
MI["registered_by_kind"] = dict(Counter("PubMed abstract" if r["source"].startswith("PubMed") else ("table/figure registry" if r["source"].startswith("_ledger")
                                         else r["source"]) for r in ml["rows"]))

# ================================================================ writing checks on the whole text (Introduction to Results)
W = {}
text = "\n".join(ptext(p) for p in body_ps)
low = text.lower()
W["banned_terms"] = {w: low.count(w) for w in BANNED if low.count(w)}
W["throat_clearing"] = {w: low.count(w) for w in THROAT if low.count(w)}
W["meta_commentary"] = {w: low.count(w) for w in META if low.count(w)}
W["hedges"] = {h: len(re.findall(h, low)) for h in HEDGE if re.findall(h, low)}
res_low = "\n".join(p.text for p in res_ps).lower()
W["methods_phrases_in_results"] = {h: len(re.findall(h, res_low)) for h in METHODS if re.findall(h, res_low)}
W["bare_time_words"] = {h: len(re.findall(h, low)) for h in TIME if re.findall(h, low)}
W["causal_words"] = {h: len(re.findall(h, low)) for h in CAUSAL if re.findall(h, low)}
W["em_dash"] = text.count("—")
W["connectives_per_paragraph_max"] = max(sum(ptext(p).lower().count(c) for c in CONNECT) for p in body_ps)
all_sents = [(x["id"], MARK_RE.sub("", s)) for x in ml["paragraphs"] for s in x["sentences"]] + \
            [(f"R.{pi}", s["text"]) for pi, ps in enumerate(rl["paragraphs"], start=1) for s in ps]
wc = [(pid, len(s.split()), s) for pid, s in all_sents]
W["sentences"] = len(wc)
W["sentences_over_30_words"] = [(pid, n, s[:70]) for pid, n, s in wc if n > 30]
W["longest_sentence_words"] = max(n for _, n, _ in wc)
pwords = defaultdict(int)
for pid, n, _ in wc:
    pwords[pid] += n
W["paragraphs_over_150_words"] = {k: v for k, v in pwords.items() if v > 150}
W["words_by_section"] = {"Introduction": sum(v for k, v in pwords.items() if k.startswith("I.")),
                         "Methods": sum(v for k, v in pwords.items() if k.startswith("M.")),
                         "Results": sum(v for k, v in pwords.items() if k.startswith("R."))}
W["words_total"] = sum(W["words_by_section"].values())
W["sentences_joined_equal_docx"] = all(MARK_RE.sub("", " ".join(x["sentences"])) == ptext(PID[x["id"]]) for x in ml["paragraphs"])
W["aims_sentence_with_This_study_aimed_to"] = ptext(PID["I.4"]).startswith("This study aimed to estimate")
W["gap_paragraph_First_Second"] = all(w in ptext(PID["I.3"]) for w in ("First,", "Second,"))
W["novelty_absolute_forms"] = len(re.findall(r"\bthe first (?:study|analysis|evaluation|report|economic)\b|\bfirst study\b|\bno (?:prior )?stud(?:y|ies) ha(?:s|ve)\b|\bno prior\b", low))
W["outcome_first_sentence"] = ptext(PID["M.OUT.1"]).startswith("The primary outcome was the maximum affordable cost of an exercise program per patient")
W["variables_first_sentence"] = ptext(PID["M.VAR.1"]).startswith("The exposure was")
W["software_last_sentence"] = ptext(PID["M.SA.8"]).rstrip().endswith("All analyses were performed in R version 4.5.1.")
W["stages_numbered_1_to_6"] = [ptext(PID[f"M.SA.{k}"])[:3] for k in range(2, 8)] == [f"({k})" for k in range(1, 7)]

# ================================================================ first citation order of tables and figures (Introduction to Results)
order = []
for m in re.finditer(r"(Supplementary Tables?|Supplementary Figs?\.|Supplementary Methods|Tables?|Figs?\.) ((?:S?\d+)(?:(?:, | and )S?\d+)*)", text):
    kind = {"Supplementary Tables": "Supplementary Table", "Supplementary Figs.": "Supplementary Fig.", "Tables": "Table", "Figs.": "Fig."}.get(m.group(1), m.group(1))
    for num in re.findall(r"S?\d+", m.group(2)):
        key = f"{kind} {num}"
        if key not in order:
            order.append(key)
F = {}
F["first_citation_order"] = order
series = defaultdict(list)
for k in order:
    series[k.rsplit(" ", 1)[0]].append(int(re.sub(r"\D", "", k.rsplit(" ", 1)[1])))
F["by_series"] = dict(series)
F["each_series_1_to_n_in_order"] = all(v == list(range(1, len(v) + 1)) for v in series.values())
tables_n = sum(1 for _, t, _, _, _ in blocks(Document(OUT / f"tables_{VER}.docx")) if re.match(r"^Table \d+\.", t))
figs_n = len(fdoc.inline_shapes)
stab_n = sum(1 for _, t, _, _, _ in blocks(sdoc) if re.match(r"^Supplementary Table S\d+\.", t))
sfig_n = len(sdoc.inline_shapes)
smeth_n = sum(1 for _, t, _, _, _ in blocks(sdoc) if re.match(r"^Supplementary Methods S\d+\.", t))
F["max_equals_count"] = {"Table": (max(series["Table"]), tables_n), "Fig.": (max(series["Fig."]), figs_n),
                         "Supplementary Table": (max(series["Supplementary Table"]), stab_n), "Supplementary Fig.": (max(series["Supplementary Fig."]), sfig_n),
                         "Supplementary Methods": (max(series["Supplementary Methods"]), smeth_n)}
F["max_ok"] = all(a == b for a, b in F["max_equals_count"].values())
phys = [re.match(r"^(Supplementary (?:Table|Fig\.|Methods) S\d+)\.", t).group(1) for _, t, _, _, _ in blocks(sdoc) if re.match(r"^Supplementary (?:Table|Fig\.|Methods) S\d+\.", t)]
F["supplement_physical_order"] = phys
F["supplement_physical_order_matches_first_citation"] = phys == [k for k in order if k.startswith("Supplementary")]
# references whose wording points to the table of all inputs (input codes, bounds, distributions, sources) must carry
# its current number, in all four documents (v5: three supplement footnotes still carried the v4 number S1)
INPUT_CTX = re.compile(r"(?:inputs? [A-F]\d{2}[A-Z]*(?: and [A-F]\d{2}[A-Z]*)?, |units of |set by rule \(|[Cc]odes (?:in parentheses )?refer to |"
                       r"distributions in |ranges, distributions and sources are listed in |interim analysis 4 \(|final analysis[\d,–]* \(|"
                       r"early-recurrence distribution \()Supplementary Table (S\d+)")
inref = []
for name, d in (("manuscript", mdoc), ("tables", Document(OUT / f"tables_{VER}.docx")), ("figures", fdoc), ("supplement", sdoc)):
    for _, t, _, _, _ in blocks(d):
        inref += [(name, m.group(1), t[max(0, m.start() - 40):m.end()]) for m in INPUT_CTX.finditer(t)]
F["references_to_input_table"] = len(inref)
F["references_to_input_table_wrong_number"] = [x for x in inref if x[1] != SUPP["params"]]

# ================================================================ references
Q = {}
main_seq = []
for p in body_ps:
    for r in p.runs:
        if is_cite(r):
            main_seq += expand(r.text)
first = []
for n in main_seq:
    if n not in first:
        first.append(n)
Q["main_text_citation_runs"] = sum(1 for p in body_ps for r in p.runs if is_cite(r))
Q["main_text_first_appearance_is_1_to_K"] = first == list(range(1, len(first) + 1))
Q["K_main_text"] = len(first)
Q["N_reference_list"] = len(ref_ps)
listed = [re.match(r"^(\d+)\. ", p.text) for p in ref_ps]
Q["list_numbered_1_to_N"] = [int(m.group(1)) for m in listed if m] == list(range(1, len(ref_ps) + 1))
Q["list_text_equals_entries"] = len(ref_ps) == len(rf_["order"]) and all(p.text == f"{rf_['numbers'][k]}. {entry(k)}" for p, k in zip(ref_ps, rf_["order"]))
rest = []
for name in ("tables", "figures", "supplement"):
    d = Document(OUT / f"{name}_{VER}.docx")
    for _, _, rs_, _, _ in blocks(d):
        for r in rs_:
            if is_cite(r):
                rest += expand(r.text)
seen_all, after = set(first), []
for n in rest:
    if n not in seen_all:
        seen_all.add(n)
        after.append(n)
Q["outside_main_text_new_numbers_in_order"] = after == list(range(len(first) + 1, len(first) + len(after) + 1))
Q["every_reference_cited"] = sorted(seen_all) == list(range(1, len(ref_ps) + 1))
Q["citations_to_numbers_beyond_list"] = sorted(n for n in main_seq + rest if n > len(ref_ps))
doi_ok, doi_bad = [], []
HEADABS = json.load(open(ROOT / "manuscript" / "code" / "refs" / "doi_head_abstracts.json", encoding="utf-8"))  # Crossref-only entries
for k in rf_["order"]:
    m = re.search(r"doi:(\S+)$", entry(k))
    if not m:
        continue
    d = DOICHECK.get(k) or HEADABS.get(k)
    if d and d.get("doi_org_status") in (301, 302, 303, 307, 308) and d.get("doi", "").lower() == m.group(1).lower():
        doi_ok.append(k)
    else:
        doi_bad.append(k)
Q["entries_with_doi"] = len(doi_ok) + len(doi_bad)
Q["doi_resolved_at_doi_org"] = len(doi_ok)
Q["doi_problems"] = doi_bad
Q["entries_without_doi"] = [k for k in rf_["order"] if "doi:" not in entry(k)]
Q["older_than_10_years"] = [(rf_["numbers"][k], k, year(k)) for k in rf_["order"] if year(k) and year(k) < dt.date.today().year - 10]
SELF = ("Ozaki A", "Hara A")
Q["self_citations"] = [k for k in rf_["order"] if k in PUBMED and any(a in PUBMED[k]["authors"] for a in SELF)]
Q["author_year_in_text"] = len(re.findall(r"\b[A-Z][a-z]+ (?:et al\.? )?\(\d{4}\)", text))
retr = json.load(open(ROOT / "manuscript" / "code" / "refs" / "retraction_check.json", encoding="utf-8"))
Q["retracted"] = [k for k in rf_["order"] if retr.get(k, {}).get("openalex_is_retracted") or any("retract" in t for t in retr.get(k, {}).get("crossref_relations", {}))]

# ARS acronym check on the plain text of the Introduction to Results (body scope). Allowed: defined at first use but not
# recognized by the checker (hyphenated or 'yen' expansions), and names (Europe PMC; EQ-5D-5L, defined as a whole)
ACRO_ALLOW = {"JPY": "Japanese yen (JPY), Introduction paragraph 1", "TNBC": "Triple-negative breast cancer (TNBC), Introduction paragraph 1",
              "QALY": "quality-adjusted life years (QALYs), Methods, Study background paragraph 2",
              "ICER": "incremental cost-effectiveness ratio (ICER), Methods, Outcome paragraph 2",
              "PMC": "database name Europe PMC", "EQ": "part of EQ-5D-5L, defined as EuroQol 5-dimension 5-level (EQ-5D-5L)"}
W["acronym_allow_list"] = ACRO_ALLOW
plain = BUILD / f"manuscript_{VER}_plain.md"
plain.write_text("\n\n".join(ptext(p) for p in body_ps) + "\n", encoding="utf-8")
try:
    acr = subprocess.run([sys.executable, str(ARS_ACRO), "--input", str(plain), "--scopes", "body", "--lang", "en",
                          "--json-out", str(BUILD / "acronyms_manuscript.json")] + [a for x in ACRO_ALLOW for a in ("--allow", x)], capture_output=True, text=True, encoding="utf-8", timeout=120)
    W["acronym_check_stdout"] = acr.stdout.strip()
    W["acronym_check_exit"] = acr.returncode
except Exception as e:  # noqa: BLE001
    W["acronym_check_stdout"] = f"did not run: {e}"
    W["acronym_check_exit"] = None


# ================================================================ same value from the same source cell in two tables
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
EXCEPTIONS = {f"Supplementary Table {SUPP['capgrid']} & Table 2": "E1（Table 2 Panel B、C 的基准行与 S4；2026-10-26 决定）",
              f"Supplementary Table {SUPP['params']} & Table 1": "E2（S2 完整参数表与 Table 1；2026-10-26 决定）",
              f"Supplementary Table {SUPP['duration']} & Table 2": "E3（S7 完整网格与 Table 2 Panel B 的 HR 0.85 两行；2026-10-26 接受，与 E1 同类）"}


# ================================================================ check_<VER>.md
def fmt_res(r):
    L = [f"### {r['file']}", "", "| 项目 | 结果 | 应为 |", "|---|---|---|"]
    for k, want in (("paragraphs_and_cells", None), ("text_runs", None), ("citation_runs", None), ("runs_not_TNR_12pt", 0), ("runs_non_black", 0),
                    ("empty_cells", 0), ("heading_style_paragraphs", 0), ("bold_runs_outside_tables", 0), ("bold_runs_in_cells_with_digits", 0),
                    ("middle_dot", 0), ("paragraphs_starting_Note", 0), ("em_dash_outside_cells", 0), ("orientation_ok", True), ("numeric_tokens", None)):
        L.append(f"| {k} | {r[k]} | {'' if want is None else want} |")
    L.append(f"| unregistered_tokens | {len(r['unregistered_tokens'])}（{', '.join(r['unregistered_tokens']) or '无'}） | 0 |")
    nf = r["registered_values_not_found_in_document"]
    L.append(f"| registered_values_not_found_in_document | {len(nf)}（{', '.join(nf) or '无'}） | 0 |")
    L.append(f"| sections | {r['sections']} | |")
    if r["footnotes"]:
        L += ["", "脚注符号（表内或题目中的上标 ↔ 脚注段落开头的符号；文献号的上标不计）：", "", "| 单位 | 表内/题目 | 脚注 | 一对一 | 顺序 |", "|---|---|---|---|---|"]
        for u in r["footnotes"]:
            L.append(f"| {u['unit']} | {' '.join(u['symbols_in_table_or_title'])} | {' '.join(u['symbols_in_notes'])} | {u['one_to_one']} | {u['in_order']} |")
    return L


def kv(title, d, skip=()):
    L = [f"## {title}", "", "| 项目 | 结果 |", "|---|---|"]
    for k, v in d.items():
        if k in skip:
            continue
        L.append(f"| {k} | {v} |")
    return L + [""]


now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
C = [f"# {VER} 的回读检查（{now}，`manuscript/code/make_ledger.py`）", "",
     "从交付的 docx 读回。数字检查：抽出所有数字（与字母或连字符相连的编号如 E01、S1、EQ-5D、KEYNOTE-522 不算；表与图的编号与文献号的上标先去掉），"
     "逐个与登记表比对；反向检查登记的数值是否都出现在文档中。Results 另按句检查：每个数字须是该句所引表格中某一格的显示值。"
     "Introduction 与 Methods 按段检查：每个数字须登记在该段（所引文献摘要中的原文、表中的显示值、项目文件中的设定或定义）。", ""]
for r in (rm, rt, rf, rs):
    C += fmt_res(r) + [""]
C += kv("本文的结构", M)
C += kv("Results 的检查", R)
C += kv("Introduction 与 Methods 的数字", MI)
C += kv("全文（Introduction 至 Results）的写作检查", W, skip=("acronym_check_stdout",))
C += ["ARS check_acronyms.py（body 范围，Introduction 至 Results）：", "", "```", W["acronym_check_stdout"], "```", ""]
C += kv("表与图的首次引用（本文地の文）", F)
C += kv("参考文献", Q)
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


# ================================================================ numbers_ledger_<VER>.md
def provisional(x):
    txt = f"{x['where']} {x['loc']}"
    if "E03" in txt:
        return "【要確認】E03"
    if "(D02)" in txt or ", D02," in txt or txt.startswith(f"Supplementary Table {SUPP['oneway']}, D02"):
        return "【要確認】D02"
    if "(F01P)" in txt or f"Supplementary Table {SUPP['other']}, sjp" in x["where"] or ", sjp" in x["where"]:
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
     "费用以千日元（JPY 1,000）显示，与第 2 阶段报告的“万日元 1 位小数”精度相同。文献号不是数值，见第 9 节。", "",
     "## 1. Results：每句所依据的表格位置", ""]
for pi, ps in enumerate(rl["paragraphs"], start=1):
    for si, s in enumerate(ps, start=1):
        L.append(f"- P{pi}.{si}　{s['text']}")
        L.append(f"  - 所引：{'、'.join(s['cites'])}；来自：{s.get('origin', '')}")
        for u in [u for u in rl["used"] if u["paragraph"] == pi and u["sentence"] == si]:
            L.append(f"  - {u['shown']} ← {u['where']}（`{u['source']}`：{u['loc']}）")
L += ["", "## 1b. Introduction 与 Methods 的数字（按段）", "", "| 段 | 显示 | 来源 | 位置 |", "|---|---|---|---|"]
for r in ml["rows"]:
    L.append(f"| {r['where']} | {r['shown']} | {r['source']} | {r['loc']} |")
L += ["", f"## 2. Table 1–3（tables_{VER}.docx）", ""] + table_rows(tl["rows"])
L += ["", "### 派生值的核对（Table 3 的“转移复发治疗费 50%”“艾立布林”两栏的类别值）", ""]
for k, v in tl["derived_check"].items():
    L.append(f"- {k}：类别之和 {v['sum_of_categories']:.6f} 日元，模型 {v['modelled_total']:.6f} 日元，差 {v['difference']:.3e} 日元")
L += ["", f"## 3. Fig. 1–3（figures_{VER}.docx）", "", "图中的线、带、柱直接由下列文件的列画出；刻度数字是标度，不登记。", ""] + table_rows(fl["rows"])
L += ["", f"## 4. 补充表（supplement_{VER}.docx）", ""] + table_rows(sl["rows"])
el = sl.get("elmore_check")
if el:
    dropped = el.get("registry_rows_dropped_N10_E4", [])
    L += ["", f"### Supplementary Table {SUPP['other']} 的 Elmore 行与 S-JP 的参照 ICER（N10、E4）", "",
          "Elmore 行的 6 个运动格与 Table 2 的基准值逐格相同（make_supplement.py 中断言），本版按 N10 显示为「Same as base case (Table 2)」："
          + "；".join(f"{a} = {b}" for a, b in el["cells_equal_to_table_2"]) + "。S-JP 的参照 ICER 按 E4 显示为「Table 3」（断言与 Table 3 的显示值相同）。"
          f"因此从登记表中移除的行 {len(dropped)} 行：" + "；".join(f"{x['where']} = {x['shown']}" for x in dropped) + "。", "",
          "| 比较 | scenario_caps.csv，hr0 格点上 cap_500 的最大绝对差（日元） | 格点数 | sc_crossings.csv，分界点 hr0 的最大绝对差 | 分界点数 |", "|---|---|---|---|---|"]
    for comp in ("main", "secondary"):
        c = el[comp]
        L.append(f"| {comp} | {c['cap_500_hr0_grid_max_abs_diff_yen']:.3g} | {c['grid_points']} | {c['crossings_hr0_max_abs_diff']:.3g} | {c['crossings']} |")
L += ["", "## 5. 补充图（supplement 中的 Supplementary Fig. S1、S2）", ""] + table_rows(sfl["rows"])
prov = [x for rows in (tl["rows"], fl["rows"], sl["rows"], sfl["rows"]) for x in rows if provisional(x)]
L += ["", "## 6. 暂定值（【要確認】）", "",
      "入力表 v10 中备考为【要確認】、并在表图中显示（或直接由其算出）的值：E03（远程低价方案费用）、D02（局部区域复发后的月额）与 F01P（S-JP 情景）。"
      f"其余【要確認】行（B03、B04、B07–B10）只在 Supplementary Table {SUPP['params']} 中作为输入列出。", "", "| 显示 | 位置 | 标记 |", "|---|---|---|"]
for x in prov:
    L.append(f"| {x['shown']} | {x['where']} | {provisional(x)} |")
L += ["", "## 7. 编号与定义中的数字（不是结果）", "", "| 显示 | 位置 | 说明 |", "|---|---|---|"]
for x in tl["labels"] + fl["labels"] + sl["labels"] + sfl["labels"]:
    L.append(f"| {x['shown']} | {x['where']} | {x['reason']} |")
SRC = sorted({x["source"] for rows in (tl["rows"], fl["rows"], sl["rows"], sfl["rows"]) for x in rows}
             | {r["source"] for r in ml["rows"] if not r["source"].startswith(("PubMed", "_ledger", "definition"))})
SRC += [f"manuscript/code/refs/{f}" for f in ("pubmed_meta.json", "doi_check.json", "crossref_meta.json", "retraction_check.json", "cheers2022_items.json")]
L += ["", "## 8. 来源文件的 sha256（生成时）", "", "| 文件 | sha256 |", "|---|---|"]
for s in SRC:
    paths = [ROOT / q.strip() for q in s.split(";")] if ";" in s else [ROOT / s.split(" (")[0]]
    for p in paths:
        L.append(f"| `{rel(p)}` | {sha256(p) if p.exists() else '（不在仓库）'} |")
L += ["", "## 9. 参考文献的编号（number_refs.py）", "",
      f"正文（Introduction 至 Results）中首次引用的 {rf_['main_text_count']} 条为 1–{rf_['main_text_count']}；只在表、图注或补充材料中引用的为其后的编号。", "",
      "| 号 | 键 | 首次引用 | 引用次数 |", "|---|---|---|---|"]
first_doc, ncit = {}, Counter()
for c in rf_["citations"]:
    for k in c["keys"]:
        first_doc.setdefault(k, c["doc"])
        ncit[k] += 1
for k in rf_["order"]:
    L.append(f"| {rf_['numbers'][k]} | {k} | {first_doc[k]} | {ncit[k]} |")
(OUT / f"numbers_ledger_{VER}.md").write_text("\n".join(L) + "\n", encoding="utf-8")

# ================================================================ MANIFEST_<VER>.md
deliv = [f"manuscript_{VER}.docx", f"tables_{VER}.docx", f"figures_{VER}.docx", f"supplement_{VER}.docx", f"table_figure_plan_{VER}.md",
         f"numbers_ledger_{VER}.md", f"references_{VER}.md", f"check_{VER}.md", f"diff_{PREV}_{VER}.md"]
figs = sorted(p.name for p in FIGDIR.iterdir() if p.suffix in (".pdf", ".png", ".tiff", ".svg"))
code_dir = ROOT / "manuscript" / "code"
code = sorted(p.relative_to(code_dir).as_posix() for p in list(code_dir.glob("*.py")) + list(code_dir.glob("*.R")) + list(code_dir.glob("*.ps1"))
              + list((code_dir / "refs").glob("*.py")) + list((code_dir / "refs").glob("*.json"))
              + list((code_dir / "refs" / "searches").glob("*.json")))
M_ = [f"# MANIFEST {VER}（{dt.date.today().isoformat()}）", "",
      f"- 版本：{VER}（{STEP}）。底本：{BASE}。Discussion、Implications、Limitations、Abstract 按指示未写。",
      f"- 数值来源：第 1、2 阶段的输出与入力表 v10；不重新计算模型。来源文件与 sha256 见 numbers_ledger_{VER}.md 第 8 节。",
      f"- 参考文献：{len(rf_['order'])} 条；书目与 DOI 的实测见 references_{VER}.md。", "",
      "| 文件 | sha256 |", "|---|---|"]
for d in deliv:
    M_.append(f"| manuscript/{VER}/{d} | {sha256(OUT / d) if (OUT / d).exists() else '（未生成）'} |")
for f in figs:
    M_.append(f"| manuscript/{VER}/figures/{f} | {sha256(FIGDIR / f)} |")
for c in code:
    M_.append(f"| manuscript/code/{c} | {sha256(code_dir / c)} |")
(OUT / f"MANIFEST_{VER}.md").write_text("\n".join(M_) + "\n", encoding="utf-8")

for name, r in (("MANUSCRIPT", rm), ("TABLES", rt), ("FIGURES", rf), ("SUPPLEMENT", rs)):
    print(name, {k: r[k] for k in ("empty_cells", "runs_not_TNR_12pt", "runs_non_black", "heading_style_paragraphs", "bold_runs_outside_tables",
                                   "bold_runs_in_cells_with_digits", "middle_dot", "paragraphs_starting_Note", "em_dash_outside_cells", "orientation_ok",
                                   "numeric_tokens", "citation_runs")},
          "unregistered", r["unregistered_tokens"], "not found", len(r["registered_values_not_found_in_document"]))
    if r["footnotes"]:
        print("  footnotes", [(u["unit"], u["one_to_one"], u["in_order"]) for u in r["footnotes"] if not (u["one_to_one"] and u["in_order"])] or "all one-to-one and in order")
print("STRUCTURE", M)
print("RESULTS", {k: v for k, v in R.items() if k not in ("sentences_without_own_reference",)})
print("INTRO/METHODS NUMBERS", MI)
print("WRITING", {k: v for k, v in W.items() if k != "acronym_check_stdout"})
print("ACRONYMS", W["acronym_check_stdout"][-800:])
print("FIRST CITATIONS", F)
print("REFERENCES", Q)
print("DUPLICATES", dict(dups))
print("PICTURES", [(p["fig"], p["effective_dpi"]) for p in pics])
