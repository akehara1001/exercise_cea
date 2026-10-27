"""Literature record of the manuscript (references_<VER>.md).

Reads the saved searches (refs/searches/*.json), the reference data (refs/*.json),
references.py and the numbering written by number_refs.py (_build/_refs.json); does
not search or fetch anything. Sections: searches, screening of the searches behind
the novelty sentence and the economic-evaluation sentence, the numbered list with
the DOI and retraction checks, documents and web pages, candidates read but not
cited, the citation audit, and notes.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from collections import Counter

from common import BUILD, OUT, ROOT, SUPP, VER
from references import ABSTRACT, CROSSREF, DOICHECK, GREY, JOURNAL, MARK_RE, PUBMED, entry, year

sys.stdout.reconfigure(encoding="utf-8")
REFS = ROOT / "manuscript" / "code" / "refs"
rf = json.load(open(BUILD / "_refs.json", encoding="utf-8"))
mm = json.load(open(BUILD / "_manuscript_map.json", encoding="utf-8"))
retr = json.load(open(REFS / "retraction_check.json", encoding="utf-8"))
headabs = json.load(open(REFS / "doi_head_abstracts.json", encoding="utf-8"))
NUM = rf["numbers"]
BYPMID = {v["pmid"]: k for k, v in PUBMED.items()}

# purpose of each search and the paragraph whose statement it supports
PURPOSE = {
    "tnbc_recurrence": "Introduction 第 1 段：TNBC 的复发模式",
    "challenge": "Introduction 第 2 段：CHALLENGE 试验",
    "chemo_rct_survival": "Introduction 第 2 段：乳腺癌化疗期间运动的随机试验与复发、生存",
    "nac_pcr": "Introduction 第 2 段：新辅助化疗期间运动与 pCR 的试验",
    "econ_reviews": "Introduction 第 3 段：癌症运动经济评价的系统综述",
    "headroom": "Introduction 第 3 段：最大可负担成本（headroom）方法",
    "pembro_cea": "Introduction 第 3 段：KEYNOTE-522 方案的成本效果分析",
    "pembro_tnbc_any": "同上，放宽到 TNBC 的所有场景",
    "pembro_japan": "Introduction 第 3 段：日本的帕博利珠单抗成本效果分析",
    "novelty": "新颖性句（Introduction 第 3 段；v6 起检索式写在 Supplementary Methods S1）：乳腺癌新辅助治疗期间运动的经济评价",
    "novelty_variants": "新颖性句：拼写变体（neo-adjuvant、(neo)adjuvant、during treatment），不限癌种",
    "novelty_chemo": "新颖性句：放宽到乳腺癌化疗期间（含辅助）",
}
ORDER = ["tnbc_recurrence", "challenge", "chemo_rct_survival", "nac_pcr", "econ_reviews", "headroom", "pembro_cea", "pembro_tnbc_any",
         "pembro_japan", "novelty", "novelty_variants", "novelty_chemo"]
SCREENED = ["novelty", "novelty_variants", "novelty_chemo", "econ_reviews"]

# screening of every hit of the searches in SCREENED (title and abstract read); code: C cited, U read and not cited,
# P protocol or design without results, D other disease or cancer type, S setting other than neoadjuvant breast cancer,
# E no economic evaluation, X topic outside the question, R review outside the question or covered by the cited reviews
CODES = {"C": "引用", "U": "读过、未引用（理由见第 5 节）", "P": "试验方案或设计论文，尚无结果", "D": "其他疾病或癌种",
         "S": "乳腺癌但不在新辅助期间（辅助、术后或转移）", "E": "没有经济评价（成本效果只作为今后的课题提到）",
         "X": "主题不符", "R": "综述，范围不符或已被引用的三篇综述覆盖"}
SCREEN = {
    "41926867": ("S,E", "wearable-driven feedback after axillary surgery; observational cohort; cost-effectiveness named as future work"),
    "27299796": ("X", "costs of reflex ER/PR testing of DCIS; 'exercise' used figuratively"),
    "40755583": ("R,E", "narrative review of physical therapy across the cancer care continuum"),
    "40681723": ("E", "NEXT-BRCA: exercise and self-management during treatment; cost-effectiveness named as future work"),
    "39163116": ("P", "protocol of a randomized trial of aerobic training during chemotherapy with a planned cost-effectiveness analysis"),
    "37074759": ("C", "Phys-Can: cost-effectiveness of two exercise intensities during (neo)adjuvant treatment of breast, colorectal or prostate "
                      "cancer; the nearest study named in Introduction paragraph 3"),
    "35906659": ("P,S", "design of a trial of exercise in metastatic breast cancer"),
    "35607981": ("U", "Phys-Can: long-term resource use and costs"),
    "34518245": ("P,S", "protocol: connected device and education for localised breast cancer (adjuvant); planned cost-effectiveness analysis"),
    "32404096": ("P,D", "protocol: rehabilitation after oesophagogastric and hepatopancreaticobiliary cancer surgery"),
    "28875575": ("R,E", "systematic review of interventions to prevent weight gain during breast cancer treatment"),
    "27156145": ("D,E", "feasibility of exercise during neoadjuvant chemoradiotherapy for rectal cancer"),
    "PPR1238970": ("D", "preprint (not peer reviewed): economic evaluation of multimodal prehabilitation during neoadjuvant chemotherapy for "
                        "advanced ovarian cancer; outside the breast-cancer bound of the novelty sentence; candidate for the Discussion"),
    "37729837": ("X,R", "scoping review of mobile health education for patients with cancer"),
    "31729566": ("C", ""), "29086085": ("C", ""), "28264824": ("C", ""),
    "25523144": ("X", "trastuzumab in metastatic breast cancer"),
    "24096188": ("P,S", "design of the APAD trial during adjuvant therapy; planned cost-utility analysis"),
    "21138561": ("P,S", "design of the PACES trial during adjuvant chemotherapy (its cost-utility results are cited)"),
    "PPR201731": ("P,D", "feasibility protocol of supervised exercise for resectable pancreatic cancer"),
    "42799684": ("X", "acute low back pain"),
    "42366788": ("R", "non-pharmacological interventions for fatigue in long-term conditions, not specific to cancer"),
    "40685660": ("R", "cost-effectiveness of non-pharmacological interventions for fatigue in long-term conditions, not specific to cancer"),
    "39776481": ("X", "software as a medical device in chronic disease"),
    "39483606": ("X", "low anterior resection syndrome"),
    "38801296": ("X", "treatments for cachexia"),
    "38323587": ("R,D", "prehabilitation for upper gastrointestinal cancer, effectiveness only"),
    "37457987": ("X", "web-based nutrition"),
    "36965520": ("C", ""), "33624172": ("C", ""), "30997624": ("C", ""),
    "36170564": ("R,D", "preoperative exercise for non-small cell lung cancer, effectiveness"),
    "36163450": ("R", "cost-effectiveness of adjunctive lifestyle interventions, diet included; exercise studies covered by the three cited reviews"),
    "35703367": ("X", "sleep promotion in hospitalized children"),
    "34694005": ("X", "physical activity in outside-school-hours childcare"),
    "31221939": ("X", "qigong and tai chi, overview of reviews"),
    "29951414": ("X", "telemedicine"),
    "28900822": ("R,E", "meta-analysis of prehabilitation, effectiveness only"),
    "26810383": ("X", "psychosocial interventions"),
    "25757733": ("R,E", "remote physical activity, diet and weight interventions for cancer survivors, effectiveness"),
    "24891269": ("X", "weight loss trials in breast cancer"),
    "23074431": ("X", "vaccination in chronic obstructive pulmonary disease"),
    "19845974": ("R", "exercise interventions in various diseases, not specific to cancer"),
    "19000846": ("X", "community-based physical activity"),
    "15929857": ("X", "osteoporosis drugs"),
    "10611196": ("X", "infertility treatments"),
    "PPR756874": ("X", "artificial intelligence for cancer diagnosis"),
}
NOT_CITED = {
    "ax2022": "Phys-Can long-term resource use and costs; the cost-effectiveness analysis of the same project (ax2023) is cited as the nearest study",
    "campbell2019": "consensus exercise guidelines for cancer survivors; the text states no guideline recommendation",
    "cannioto2021": "observational analysis of physical activity before, during and after chemotherapy and survival; Introduction paragraph 2 "
                    "reports randomized evidence only, so it was dropped in v5",
    "iyengar2025": "secondary analysis of a phase 2 trial; pCR in a neoadjuvant subgroup of 51 tumours, 27% with exercise and 28% with usual "
                   "care; Introduction paragraph 2 cites the meta-analysis for pCR (diasrato2026)",
    "shiroiwa2020": "Japan's value-based price adjustment system (2020); the thresholds are cited from the 2026 notification (mhlw_ce2026)",
}

# fields where verify_doi.py found PubMed and Crossref different; each was read on both records (2026-10-27) and the
# difference is one of notation, not of the work cited. The entry follows PubMed.
MISMATCH = {
    "dent2007": "issue: PubMed 15 Pt 1, Crossref 15",
    "furmaniak2016": "Cochrane: PubMed volume 9 (issue) and article CD005001, Crossref volume 2016 and no page",
    "vanwaart2015": "first author: family name with particle (van Waart)",
    "diasrato2026": "first author: two-word family name (Dias Rato); page: article number 948 (PubMed elocation, Crossref page)",
    "deboniface2022": "first author: family name with particle (de Boniface)",
    "vanwaart2018": "first author: family name with particle (van Waart)",
    "guyot2012": "issue: none in PubMed, 1 in Crossref; the journal has no issues (article 9)",
    "fedele2026": "page: article number 8 (PubMed elocation, Crossref page)",
    "tutt2021": "title: Crossref with italic tags around BRCA1 and BRCA2",
    "andrade2026": "page: article number 27 (PubMed elocation, Crossref page)",
    "fujisawa2021": "title: Crossref with italic tags and a non-breaking hyphen",
}


def md(t):
    return str(t).replace("|", "/").replace("\n", " ")


def shown(t):
    """Text with markers replaced by the reference numbers in square brackets."""
    return MARK_RE.sub(lambda m: "[" + ",".join(str(NUM[k]) for k in m.group(1).split(",")) + "]", t)


searches = {k: json.load(open(REFS / "searches" / f"search_{k}.json", encoding="utf-8")) for k in ORDER}
assert sorted(searches) == sorted(p.stem.removeprefix("search_") for p in (REFS / "searches").glob("search_*.json"))

L = [f"# 参考文献与检索记录（{VER}）", "",
     f"由 manuscript/code/make_references_doc.py 生成（{dt.date.today().isoformat()}）。本文件只读取已保存的检索结果与核对记录"
     "（manuscript/code/refs/），不重新检索。文献号是 number_refs.py 按阅读顺序（本文 → 表 → 图注 → 补充材料）编的号。", ""]

# ---------------------------------------------------------------- 1 searches
L += ["## 1. 检索", "",
      "- 数据库：PubMed（NCBI E-utilities，esearch/esummary）与 Europe PMC（REST API，限题名与摘要：TITLE/ABSTRACT 字段）。",
      "- Scopus：本环境没有 Scopus API 的配置（pybliometrics 未设置），未检索。",
      "- 检索日：全部 12 组都在 2026-10-26 运行；年份范围见各式（新颖性的 3 组与经济评价、试验的各组为 2000–2026）。",
      "- 脚本：manuscript/code/refs/lit_search.py；结果：manuscript/code/refs/searches/search_<key>.json（命中的 ID、题名、年、刊名、DOI）。",
      "- 形式：Introduction 的背景检索，不是系统综述（不宣称覆盖全部文献）。新颖性句与经济评价句所依据的 4 组检索，每条命中都读了题名和摘要并记录判定（第 2 节）；"
      "其余各组按段落要陈述的内容读题名，引用的文献列在表中。", "",
      "| key | 用途 | 检索日 | PubMed 命中 | Europe PMC 命中 | 其中被引用（文献号） |", "|---|---|---|---|---|---|"]
for k in ORDER:
    s = searches[k]
    ids = {h.get("pmid") for db in ("pubmed", "europepmc") for h in s[db]["hits"] if h.get("pmid")}
    cited = sorted(NUM[BYPMID[i]] for i in ids if i in BYPMID and BYPMID[i] in NUM)
    L.append(f"| {k} | {PURPOSE[k]} | {s['date']} | {s['pubmed']['count']} | {s['europepmc']['count']} | {', '.join(map(str, cited)) or '—'} |")
L += ["", "检索式（原样）：", ""]
for k in ORDER:
    s = searches[k]
    L += [f"**{k}**", "", f"- PubMed：`{s['pubmed']['query']}`", f"- Europe PMC：`{s['europepmc']['query']}`", ""]

# ---------------------------------------------------------------- 2 screening
L += ["## 2. 新颖性句与经济评价句的筛选", "",
      "判定代码：" + "；".join(f"{c} = {v}" for c, v in CODES.items()) + "。两个库的同一条记录只列一次。", ""]
missing = []
for k in SCREENED:
    s = searches[k]
    L += [f"### {k}（PubMed {s['pubmed']['count']}，Europe PMC {s['europepmc']['count']}）", "",
          "| ID | 年 | 第一作者 | 题名 | 判定 | 说明 |", "|---|---|---|---|---|---|"]
    seen = set()
    for db in ("pubmed", "europepmc"):
        for h in s[db]["hits"]:
            hid = h.get("pmid") or h.get("id")
            if hid in seen:
                continue
            seen.add(hid)
            if hid not in SCREEN:
                missing.append((k, hid, h["title"]))
                continue
            code, note = SCREEN[hid]
            key = BYPMID.get(hid)
            if "C" in code:
                assert key in NUM, (hid, key)
                note = (note + "; " if note else "") + f"cited as [{NUM[key]}] ({key})"
            elif key:
                assert key not in NUM, (hid, key)
            L.append(f"| {hid} | {h['year']} | {md(h.get('first_author', ''))} | {md(h['title'])} | {code} | {md(note)} |")
    L.append("")
if missing:
    raise SystemExit(f"hits without a screening decision: {missing}")

nov = [o for o in mm["order"] if o["id"] and "No economic evaluation of exercise" in o["text"]]
assert len(nov) == 1
nov_sents = [x for x in re.split(r"(?<=[.⟧])\s+(?=[A-Z])", nov[0]["text"]) if "No economic evaluation" in x or x.startswith("The nearest")]
L += ["### 新颖性句的界限", "",
      f"- 位置：manuscript_{VER}.docx，{nov[0]['id']}（Introduction 第 3 段）。原文：", ""] + [f"  > {shown(x)}" for x in nov_sents] + ["",
      "- 界限：乳腺癌、新辅助治疗期间、运动、经济评价（成本效果、成本效用、QALY、Cost-Benefit Analysis[mh]）；PubMed 与 Europe PMC，2000–2026，"
      "最后运行 2026-10-26。novelty 组 2 条命中都不符合（S/E、X），放宽的 novelty_variants 与 novelty_chemo 也没有符合的记录。"
      f"v6 起本文的新颖性句只引 Supplementary Methods {SUPP['methods_survival']}；该节的 Literature searches 小节写数据库、出版年范围、检索日与三组检索式原文"
      "（novelty、novelty_variants、novelty_chemo，与本节第 1 节同一文件）。",
      "- 最接近的研究：Phys-Can（ax2023）比较了两种运动强度，对象含新辅助或辅助治疗期间的乳腺癌，但不是与无运动比较，也未单独报告新辅助期间。",
      "- 乳腺癌以外：Snooks 2026（Europe PMC 预印本 PPR1238970，未经同行评议）评价了晚期卵巢癌新辅助化疗期间多模式术前康复的成本与 QALY。"
      "它不在新颖性句的界限内（乳腺癌），本文未引用；Discussion 写到其他癌种时可作候选。",
      "- 不用 “first” 一类的绝对说法（make_ledger 的 novelty_absolute_forms = 0）。", ""]

# ---------------------------------------------------------------- 3 numbered list
first_loc = {}
order_ids = mm["order"]
# number_refs.py counts every paragraph; the map skips the empty lines left for the front matter (v8)
from docx import Document  # noqa: E402
_nonempty = [i for i, p in enumerate(Document(OUT / f"manuscript_{VER}.docx").paragraphs) if p.text.strip()]
pi2order = {pi: k for k, pi in enumerate(_nonempty)}
for c in rf["citations"]:
    for k in c["keys"]:
        if k in first_loc:
            continue
        if c["doc"] == "manuscript":
            o = order_ids[pi2order[c["paragraph"]]]
            assert MARK_RE.search(o["text"]) and k in o["text"], (k, c["paragraph"])
            first_loc[k] = f"manuscript {o['id']}"
        else:
            first_loc[k] = f"{c['doc']}（…{md(c['before'][-40:])}）"
assert set(first_loc) == set(NUM)


def kind(k):
    return "journal" if k in JOURNAL else "abstract" if k in ABSTRACT else "document/web"


def doi_cells(k):
    m = re.search(r"doi:(\S+)$", entry(k))
    if not m:
        return "—", "—", "—"
    d = DOICHECK.get(k) or headabs.get(k)
    st = f"{d['doi_org_status']}" if d else "未测"
    if k in DOICHECK and "checks" in DOICHECK[k]:
        bad = [f for f, ok in DOICHECK[k]["checks"].items() if not ok]
        if bad and k not in MISMATCH:
            raise SystemExit(f"{k}: PubMed and Crossref differ in {bad}, not reviewed")
        cr = "一致" if not bad else "写法不同（" + MISMATCH[k] + "）"
    elif k in CROSSREF:
        cr = "条目取自 Crossref 记录"
    else:
        cr = "—"
    return m.group(1), st, cr


def retr_cell(k):
    r = retr.get(k)
    if not r:
        return "—"
    rel = [t for t in r["crossref_relations"] if r["crossref_relations"][t]]
    upd = [u["type"] for u in r["crossref_update_to"]]
    s = "OpenAlex 未撤稿" if r["openalex_is_retracted"] is False else f"OpenAlex is_retracted={r['openalex_is_retracted']}"
    if rel or upd:
        s += "；Crossref " + ", ".join(rel + upd)
    return s


L += ["## 3. 文献表（Vancouver，NLM 格式）与 DOI 实测", "",
      "DOI 实测：doi.org 的 HEAD 请求须返回 30x 跳转（期刊论文 refs/verify_doi.py → doi_check.json，并与 Crossref 记录比对第一作者、题名、卷、期、首页、年；"
      "会议摘要 refs/doi_head_abstracts.py → doi_head_abstracts.json）。撤稿筛查：refs/retraction_check.py（OpenAlex is_retracted 与 Crossref 的 "
      "update-to、relation）。", "",
      "| 号 | key | 类型 | 首次引用 | DOI | doi.org | Crossref 比对 | 撤稿筛查 |", "|---|---|---|---|---|---|---|---|"]
for k in rf["order"]:
    doi, st, cr = doi_cells(k)
    L.append(f"| {NUM[k]} | {k} | {kind(k)} | {first_loc[k]} | {doi} | {st} | {cr} | {retr_cell(k)} |")
L += ["", "条目全文：", ""] + [f"{NUM[k]}. {entry(k)}" for k in rf["order"]] + [""]

# ---------------------------------------------------------------- 4 grey and abstracts
L += ["## 4. 文件与网页（无 DOI）及会议摘要的核对", "", "| 号 | key | 核对 |", "|---|---|---|"]
for k in rf["order"]:
    if k in GREY:
        L.append(f"| {NUM[k]} | {k} | {md(GREY[k]['check'])} |")
    elif k in ABSTRACT:
        L.append(f"| {NUM[k]} | {k} | {md(ABSTRACT[k]['check'])}；doi.org {headabs[k]['doi_org_status']}（{headabs[k]['date']}） |")
L.append("")

# ---------------------------------------------------------------- 5 read, not cited
nc = sorted(set(PUBMED) - set(JOURNAL))
assert nc == sorted(NOT_CITED), (nc, sorted(NOT_CITED))
L += ["## 5. 读过但未引用的候选", "", "| key | PMID | 题名 | 未引用的理由 |", "|---|---|---|---|"]
for k in nc:
    L.append(f"| {k} | {PUBMED[k]['pmid']} | {md(PUBMED[k]['title'])} | {md(NOT_CITED[k])} |")
L.append("")

# ---------------------------------------------------------------- 6 audit
yrs = {k: year(k) for k in rf["order"]}
this = dt.date.today().year
recent = [k for k, y in yrs.items() if y and y >= this - 4]
old = [(NUM[k], k, y) for k, y in yrs.items() if y and y < this - 10]
cnt = Counter(kind(k) for k in rf["order"])
nodoi = [k for k in rf["order"] if "doi:" not in entry(k)]
listed = set(NUM)
cited = {k for c in rf["citations"] for k in c["keys"]}
SELF = ("Ozaki A", "Hara A")
selfc = [k for k in rf["order"] if k in PUBMED and any(a in PUBMED[k]["authors"] for a in SELF)]
retracted = [k for k in rf["order"] if retr.get(k, {}).get("openalex_is_retracted")
             or any("retract" in t for t, v in retr.get(k, {}).get("crossref_relations", {}).items() if v)]
L += ["## 6. 引用审核（ARS citation_compliance 的项目）", "", "| 项目 | 结果 |", "|---|---|",
      f"| 文献数 | {len(rf['order'])}（期刊 {cnt['journal']}、会议摘要 {cnt['abstract']}、文件与网页 {cnt['document/web']}）；本文首次引用 {rf['main_text_count']} 篇，"
      f"其余 {len(rf['order']) - rf['main_text_count']} 篇首次出现在表、图注或补充材料 |",
      f"| 孤立引用 | 引用了但不在表中 {len(cited - listed)}；在表中但没有被引用 {len(listed - cited)} |",
      "| 格式 | Vancouver（NLM）：作者 6 名后 et al、刊名用 PubMed 缩写、页码省略重复数字、DOI 置末；make_ledger 逐条比对条目文本（list_text_equals_entries） |",
      f"| 无 DOI | {len(nodoi)} 篇，全是文件与网页：{', '.join(nodoi)} |",
      f"| DOI 实测 | {sum(1 for k in rf['order'] if doi_cells(k)[1] not in ('—', '未测'))} / {sum(1 for k in rf['order'] if doi_cells(k)[0] != '—')} 返回 30x |",
      f"| 自引 | {len(selfc)}（作者名 {', '.join(SELF)} 在 PubMed 作者列表中） |",
      f"| 近 5 年（{this - 4}–{this}） | {len(recent)} / {sum(1 for y in yrs.values() if y)}（{100 * len(recent) / sum(1 for y in yrs.values() if y):.0f}%） |",
      f"| 超过 10 年 | {len(old)}：" + ", ".join(f"[{n}] {k} ({y})" for n, k, y in sorted(old)) + "（TNBC 的复发与 pCR 的报告、运动试验与转移期治疗试验的原始报告、"
      "生存数据的重建方法） |",
      f"| 撤稿 | {len(retracted)}；Crossref 的更正、新版等记录：" + ", ".join(sorted(
          f"{k}（{', '.join([u['type'] + ' ' + u['doi'] for u in retr[k]['crossref_update_to']] + [t for t, v in retr[k]['crossref_relations'].items() if v])}）"
          for k in rf['order'] if k in retr and (retr[k]['crossref_update_to'] or any(retr[k]['crossref_relations'].values())))) + " |",
      f"| PubMed 与 Crossref 的写法差异 | {len(MISMATCH)} 篇，逐条读过两边的记录，都是写法不同，不是不同的文献（第 3 节 Crossref 比对一栏） |",
      "| 正文的作者-年份式引用 | 0（make_ledger author_year_in_text） |", ""]

# ---------------------------------------------------------------- 7 notes
L += ["## 7. 备注", "",
      f"- esmo2023（[{NUM['esmo2023']}]）：Crossref 记录的页码是 S1257；input/user_supplied_values.csv 写的是 S1256–S1257。条目按 Crossref 写 S1257。",
      f"- tropion2025（[{NUM['tropion2025']}]）：参数表只写 “TROPION-Breast02 (Daiichi Sankyo/AstraZeneca, October 2025)”，没有日期；"
      "引用的是 2025-10-19 报告试验结果的新闻稿（10 月 6 日的只有顶线结果）。待尾崎先生确认。",
      f"- jbcs55（[{NUM['jbcs55']}]）：日本乳癌学会的登记报告只对会员公开；所用数值是尾崎先生 2026-10-26 提供的（input/params/cohort_N_jbcs2024.csv），"
      "原表未收到，数值无法与报告核对。",
      f"- kwong2024（[{NUM['kwong2024']}]）：香港的分析，效用用的是英国的 EQ-5D-5L 价值集，所以 Supplementary Table {SUPP['other']} 写作 United Kingdom。",
      f"- huang2023（[{NUM['huang2023']}]）：作者名 “A Fasching P” 照 PubMed 与 Crossref 记录。",
      "- furmaniak2016：Cochrane 综述 2016 年版（pub3）是 2009 年版（pub2）的新版本，不是撤稿。",
      "- 医院费用（hosp_kasugai、hosp_chuden）：按待决事项 N6 写医院名与网址；临床专家只写 “two breast medical oncologists at Japanese hospitals, "
      "personal communication, October 2026”（单人的行写 “a breast medical oncologist”），不写姓名。",
      f"- kn522final2026（[{NUM['kn522final2026']}]）：摘要全文取自 Crossref 记录（support_cache.json），截点 2025-10-14、全体 7 年 EFS 与 OS 与所用值一致。"
      "按 pCR 分层的 7 年 EFS（90.4% 对 85.9%，57.6% 对 49.7%）不在摘要中，读自 ASCO 2026 报告的报道（OncLive 2026-06-01、DelveInsight；"
      "data/kn522_final_7y.csv）；报道写 “at median follow-up”，按尾崎先生的指示作为 7 年值（input/params/efficacy_sources.md 第 27 行）。"
      "引用的是该次分析的摘要；分层值的原始出处待尾崎先生确认（docs/model_spec.md 第 87 行同类事项）。",
      f"- esmo2023（[{NUM['esmo2023']}]）：LBA18 的摘要页返回 HTTP 403，原文未取得；2023-03-23 截点的分层值读自 OncLive 2023-10-20 的报道"
      "（input/user_supplied_values.csv），原始出处待尾崎先生确认（docs/model_spec.md 第 87 行）。v5 起本文 Methods 的截点列表加入 23 March 2023，"
      "因为这些值用于选择分布族（Supplementary Methods S1）。",
      f"- pbac2023（[{NUM['pbac2023']}]）：公开摘要（PSD）p.18 只写 “Utilities were based on EQ-5D responses in KN-522”，未写价值集。"
      f"Methods 写作 “those of the Australian reimbursement submission”；Supplementary Table {SUPP['other']} 的行名 v6 起按 N11 的决定改为 "
      "“Australian reimbursement submission”（v4、v5 为 “Utility value set: Australia”）。",
      f"- boc_fx（[{NUM['boc_fx']}]）：加拿大银行的汇率只用于运动方案费用的上限（参数表 E01 备考：上限は為替で換算）；"
      "v5 起 Methods 的购买力平价句只引世界银行，汇率的引用留在 Table 1 与 Supplementary Table S2 的出处栏。", ""]

# ---------------------------------------------------------------- 8 cited statements and the passages of the sources
sys.path.insert(0, str(REFS))
import claim_support  # noqa: E402
import openpyxl  # noqa: E402
from param_names import SOURCE, source  # noqa: E402

FULLTEXT = sys.argv[1] if len(sys.argv) > 1 else None
res = claim_support.check(FULLTEXT)
ml = json.load(open(BUILD / "_ledger_manuscript.json", encoding="utf-8"))
need = {(f"{x['id']} s{i + 1}", k) for x in ml["paragraphs"] for i, t in enumerate(x["sentences"])
        for m in MARK_RE.finditer(t) for k in m.group(1).split(",")}
have = {(re.sub(r" \(.*\)$", "", r["loc"]), r["key"]) for r in res if re.match(r"^(?:I|M|R|D|IMP|L)\.", r["loc"])}
assert need == have, ("manuscript citations without a passage", sorted(need - have), "passages without a citation", sorted(have - need))
labels = [MARK_RE.sub("", v) for v in SOURCE.values()] + list(claim_support.PANEL_A) + ["KEYNOTE-522 population"]
prose = [r for r in res if r["loc"].startswith(("supplement:", "figures:"))]
uncovered, n_cells = [], 0
for c in rf["citations"]:
    if c["doc"] == "manuscript":
        continue
    if c["doc"] == "tables" or any(c["before"] in lab for lab in labels):
        n_cells += 1
        continue
    for k in c["keys"]:
        if not any(r["loc"].split(": ", 1)[0] == c["doc"] and r["key"] == k
                   and (r["loc"].split(": ", 1)[1] in c["before"] or c["before"] in r["loc"].split(": ", 1)[1]) for r in prose):
            uncovered.append((c["doc"], k, c["before"]))
if uncovered:
    raise SystemExit(f"citations in legends or supplement prose without a passage: {uncovered}")
st = Counter(r["status"] for r in res)
L += ["## 8. 引用句与原著的对照（规约第 1.3 节、第 13 节）", "",
      f"由 manuscript/code/refs/claim_support.py 检查（{dt.date.today().isoformat()}）：每条记录的原文段落（逐字）须出现在所示的出处中。"
      "开放获取的全文从 Europe PMC 取得（manuscript/code/refs/fetch_support.py；XML 不放进仓库，sha256 记在 support_cache.json），"
      f"本次{'已' if FULLTEXT else '未'}对全文重新核对。", "",
      f"- 本文：{len(need)} 处（句子 × 文献），全部有对照记录；图注与补充材料的散文：{len(prose)} 处，全部有对照记录；"
      f"表与 Supplementary Table {SUPP['params']} 的出处栏：{n_cells} 处，按第 8.2 节的位置记录核对。",
      f"- 找到 {sum(1 for r in res if r['found'] is True)} / {len(res)}；未找到 {sum(1 for r in res if r['found'] is False)}；"
      f"未能核对 {sum(1 for r in res if r['found'] is None)}。",
      "- 状态：" + "；".join(f"{k} {v}" for k, v in sorted(st.items())) +
      "（ok = 原著中有该段；corroborated = 原著非开放获取，段落取自另一篇被引文献；report = 原著未取得，数值读自会议报道；provided = 共著者提供，原著未见）。", "",
      "### 8.1 本文、图注与补充材料的散文", "", "| 位置 | 文献 | 出处 | 原文段落 | 状态 | 找到 | 备注 |", "|---|---|---|---|---|---|---|"]
for r in res:
    if r["loc"].startswith("S2 Panel A"):
        continue
    L.append(f"| {r['loc']} | [{NUM[r['key']]}] {r['key']} | {md(r['where'])} | {md(' … '.join(r['quotes']))} | {r['status']} | "
             f"{'是' if r['found'] else '否' if r['found'] is False else '未核对'} | {md(r['note'])} |")
L += ["", f"### 8.2 出处栏（Table 1 与 Supplementary Table {SUPP['params']}）", "",
      f"Table 1 的出处栏汇总 Supplementary Table {SUPP['params']} 的出处，文献相同。Panel A（生存）按下表的项目文件记录核对；"
      "Panel B 按参数表 input/params/parameters_v10.xlsx 的「出典」与「出典の該当箇所」两列（原著中的位置）逐行列出。", "",
      "| Panel A 的出处 | 文献 | 记录位置的文件 | 记录 | 找到 |", "|---|---|---|---|---|"]
for r in res:
    if r["loc"].startswith("S2 Panel A") and r["src"].startswith("file:"):
        L.append(f"| {md(r['loc'].split(': ', 1)[1])} | {', '.join(f'[{NUM[k]}]' for k in r['key'].split(','))} | {md(r['where'])} | "
                 f"{md(r['quotes'][0])} | {'是' if r['found'] else '否'} |")
L += ["", "| param_id | 文献 | 出典 | 出典の該当箇所 |", "|---|---|---|---|"]
ws = openpyxl.load_workbook(ROOT / "input" / "params" / "parameters_v10.xlsx", read_only=True, data_only=True)["パラメータ"]
prev = None
for r in ws.iter_rows(min_row=2, values_only=True):
    if not r[0]:
        continue
    lab = source(r[10], prev)
    prev = lab
    ks = [k for m in MARK_RE.finditer(lab) for k in m.group(1).split(",")]
    if ks:
        L.append(f"| {r[0]} | {', '.join(f'[{NUM[k]}]' for k in ks)} | {md(r[10])} | {md(r[11] or '')} |")
L.append("")
if any(r["found"] is False for r in res):
    raise SystemExit("passages not found: " + str([(r["loc"], r["key"]) for r in res if r["found"] is False]))

# ---------------------------------------------------------------- 9 the two sentences completed by CC (v6, instruction section 5)
if ml.get("cc"):
    sent_of = {x["id"]: x["sentences"] for x in ml["paragraphs"]}
    L += ["## 9. Discussion 中 CC 补写的两句与所依据的摘要原句", "",
          "指示第 5 条的「[CC: …]」两处：只写各文献摘要中有的内容，不加数字。下列原句逐字取自 PubMed 摘要（与第 8.1 节同一记录）。", ""]
    for pid, si in (("D.4", 2), ("D.6", 3)):
        s = sent_of[pid][si - 1]
        assert MARK_RE.sub("", ml["cc"][pid]).lstrip(". ").split(" [")[0][:40] in s, (pid, s)
        L += [f"### {pid} 第 {si} 句", "", f"- 本文：{shown(s)}", "- 依据："]
        for r in res:
            if r["loc"] == f"{pid} s{si}":
                L += [f"  - [{NUM[r['key']]}] {r['key']}（{r['where']}；找到：{'是' if r['found'] else '否'}）"] + [f"    > {q}" for q in r["quotes"]]
        L.append("")

(OUT / f"references_{VER}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print(f"references_{VER}.md written: {len(rf['order'])} references, {sum(len(searches[k]['pubmed']['hits']) for k in SCREENED)} PubMed hits screened")
