"""Reference list of the manuscript (Vancouver, NLM style; numbered by first citation).

Journal articles are formatted from their PubMed records (refs/pubmed_meta.json,
written by refs/fetch_refs.py); every DOI was resolved at doi.org and matched with
its Crossref record (refs/doi_check.json, refs/verify_doi.py). The two meeting
abstracts without a PubMed record are formatted from Crossref
(refs/crossref_meta.json). Documents and web pages (GREY) were read at the source;
the check of each is in its "check" field. Bibliographic numbers are copied from
these files; in GREY they were transcribed from the page named in "check".

cite("a", "b") returns the marker ⟦ref:a,b⟧, which the generators place in the text
of any deliverable; number_refs.py replaces the markers by superscript numbers in
reading order (manuscript text first) and writes the list into the manuscript.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent / "refs"
PUBMED = json.load(open(HERE / "pubmed_meta.json", encoding="utf-8"))
DOICHECK = json.load(open(HERE / "doi_check.json", encoding="utf-8"))
CROSSREF = json.load(open(HERE / "crossref_meta.json", encoding="utf-8"))
MARK_RE = re.compile(r"⟦ref:([a-z0-9_,]+)⟧")

# PubMed records that are cited (candidates read but not cited stay in pubmed_meta.json
# and are listed as such in references_<VER>.md)
JOURNAL = ["dent2007", "liedtke2008", "licata2025", "schmid2020", "schmid2022", "schmid2024", "courneya2025", "courneya2007",
           "courneya2014", "vanwaart2015", "mijwel2018", "furmaniak2016", "sanft2023", "kjeldsted2025", "schmidt2025",
           "diasrato2026", "deboniface2022", "khan2019", "gublergut2021", "wang2023", "may2017", "vanwaart2018", "perrier2020",
           "ax2023", "chan2026", "boudewijns2023", "huang2023", "kwong2024", "favrebulle2024", "pollinger2025", "chisaki2025",
           "sugiura2023", "taniguchi2026", "kakinuma2025", "morimoto2026", "tomura2025", "kashiwa2024", "husereau2022",
           "hasegawa2020", "guyot2012", "grinda2023", "elmore2021", "fedele2026", "ludwig2018", "iwatani2021", "shiroiwa2017",
           "masuda2017", "tutt2021", "garber2026", "cortes2011", "cortes2020", "miller2007", "kuemmel2026", "nusawat2026",
           "yoshinami2025", "fujisawa2021", "andrade2026", "valachis2026"]
ABSTRACT = {  # meeting abstracts formatted from Crossref; issue as printed by the journal
    "kn522final2026": dict(issue="16 Suppl", check="Crossref record; DOI resolved at doi.org (302); volume 44, issue 16_suppl, page 507"),
    "ohtera2018": dict(issue="Suppl 2", check="Crossref record (volume 21, page S60, issued 2018-09; no issue field); "
                                              "supplement S2 from the ISPOR abstract page (Value in Health Volume 21, Supplemental S2)"),
    "esmo2023": dict(issue="Suppl 2", check="Crossref record (LBA18, volume 34, page S1257, issued 2023-10; no issue field); DOI resolved at "
                                            "doi.org (302); supplement 2 as in input/user_supplied_values.csv, which gives pages S1256-S1257 "
                                            "(Crossref gives S1257 only, used here)"),
}
GREY = {
    "price2026": dict(
        text="Ministry of Health, Labour and Welfare. National Health Insurance drug price list and information on generic drugs: injections, "
             "products listed as of 14 October 2026 [Internet]. Tokyo: Ministry of Health, Labour and Welfare; 2026 [cited 2026 Oct 22]. "
             "Available from: https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_02.xlsx. Japanese.",
        check="HTTP 200 (xlsx) on 2026-10-26; file name and download date 2026-10-22 as recorded in input/params/sources_hara.md"),
    "fee2026": dict(
        text="Ministry of Health, Labour and Welfare. Revision of the medical fee schedule for fiscal year 2026: Ministry of Health, Labour and "
             "Welfare Notification No. 69 of 2026 [Internet]. Tokyo: Ministry of Health, Labour and Welfare; 2026 [cited 2026 Oct 26]. "
             "Available from: https://www.mhlw.go.jp/stf/newpage_67729.html. Japanese.",
        check="HTTP 200; page title 令和８年度診療報酬改定について, lists 診療報酬の算定方法の一部を改正する件（令和８年厚生労働省告示第69号） (2026-10-26)"),
    "lifetable2025": dict(
        text="Ministry of Health, Labour and Welfare. Abridged life tables for Japan 2025 [Internet]. Tokyo: Ministry of Health, Labour and "
             "Welfare; 2026 [cited 2026 Oct 21]. Available from: https://www.mhlw.go.jp/toukei/saikin/hw/life/life25/index.html. Japanese.",
        check="HTTP 200; page 令和7年簡易生命表の概況; files and access date 2026-10-21 in input/lifetable/SOURCE.md; base period 1 January to "
              "31 December 2025 (life25-01_about.pdf p.1), so published in 2026"),
    "c2h_guideline": dict(
        text="Center for Outcomes Research and Economic Evaluation for Health, National Institute of Public Health. Guideline for preparing "
             "cost-effectiveness evaluation to the Central Social Insurance Medical Council, approved on 16 January 2026 [Internet]. Wako: "
             "National Institute of Public Health; 2026 [cited 2026 Oct 26]. Available from: https://c2h.niph.go.jp/tools/guideline/guideline_en_2026.pdf.",
        check="HTTP 200; PDF p.1 'This version was approved by CSIMC on 16th January, 2026'; p.25 'Both cost and effectiveness should be discounted "
              "at a rate of 2% per year'"),
    "mhlw_ce2026": dict(
        text="Ministry of Health, Labour and Welfare. Handling of cost-effectiveness evaluation of pharmaceuticals, medical devices and "
             "regenerative medicine products: notification of 13 February 2026 [Internet]. Tokyo: Ministry of Health, Labour and Welfare; 2026 "
             "[cited 2026 Oct 26]. Available from: https://c2h.niph.go.jp/tools/system/notification_cost-effectiveness_2026.pdf. Japanese.",
        check="HTTP 200; PDF p.1 産情発0213第３号・保発0213第７号 令和８年２月13日; p.9 総合的評価 for products whose approved indication is a "
              "malignant tumour (ウ 悪性腫瘍), for indications without sufficient treatment and for children; p.13 thresholds 500万円/QALY, "
              "750万円/QALY for products given consideration in the comprehensive assessment"),
    "c2h_list": dict(
        text="Center for Outcomes Research and Economic Evaluation for Health, National Institute of Public Health. Products designated for "
             "cost-effectiveness evaluation since fiscal year 2019 [Internet]. Wako: National Institute of Public Health; 2026 [cited 2026 Oct 26]. "
             "Available from: https://c2h.niph.go.jp/results/item.html. Japanese.",
        check="HTTP 200; 88 products designated from fiscal year 2019 to 2026 listed; pembrolizumab (キイトルーダ) not among them (2026-10-26)"),
    "jbcs55": dict(
        text="Japanese Breast Cancer Society. Report of the National Breast Cancer Registry, No. 55: cases diagnosed in 2024 [Internet; members "
             "only]. Tokyo: Japanese Breast Cancer Society; 2026 [cited 2026 Oct 26]. Available from: "
             "https://www.jbcs.gr.jp/modules/journals/index.php?content_id=8. Japanese.",
        check="HTTP 200; page states 第55号2024年次症例を掲載いたしました（2026.6.16） and that the report is for members only; the values used "
              "were sent by A. Ozaki on 2026-10-26 (input/params/cohort_N_jbcs2024.csv); the original table has not been received, so the "
              "values could not be checked against the report"),
    "ema2022": dict(
        text="European Medicines Agency. Keytruda (pembrolizumab): variation assessment report, procedure no. EMEA/H/C/003820/II/0110, "
             "EMA/257879/2022 [Internet]. Amsterdam: European Medicines Agency; 2022 [cited 2026 Oct 26]. Available from: "
             "https://www.ema.europa.eu/en/documents/variation-report/keytruda-h-c-003820-ii-0110-epar-assessment-report-variation_en.pdf.",
        check="HTTP 200 (PDF); p.1 '22 April 2022 EMA/257879/2022 ... Assessment report Keytruda ... Procedure No. EMEA/H/C/003820/II/0110'"),
    "pbac2023": dict(
        text="Pharmaceutical Benefits Advisory Committee. Public summary document, March 2023 PBAC meeting: pembrolizumab, solution concentrate "
             "for I.V. infusion 100 mg in 4 mL vial, Keytruda, Merck Sharp & Dohme (Australia) Pty Ltd [Internet]. Canberra: Australian "
             "Government Department of Health and Aged Care; 2023 [cited 2026 Oct 26]. Available from: "
             "https://www.pbs.gov.au/info/industry/listing/elements/pbac-meetings/psd/2023-03/pembrolizumab-earlyTNBC-keytruda-PSD-March-2023.",
        check="HTTP 200 (page 'Pembrolizumab – March 2023'); heading from p.1 of the downloaded document "
              "(input/params/sources_utility/PBAC_PSD_pembrolizumab_early-TNBC_2023-03.pdf)"),
    "tropion2025": dict(
        text="AstraZeneca. Datroway demonstrated an unprecedented median overall survival improvement of five months vs. chemotherapy as "
             "1st-line treatment for patients with metastatic triple-negative breast cancer for whom immunotherapy was not an option in "
             "TROPION-Breast02 [Internet]. Cambridge: AstraZeneca; 2025 Oct 19 [cited 2026 Oct 26]. Available from: "
             "https://www.astrazeneca.com/media-centre/press-releases/2025/datroway-demonstrated-an-unprecedented-median-overall-survival-"
             "improvement-of-five-months-vs-chemotherapy-as-1st-line-treatment-for-patients-with-metastatic-triple-negative-breast-cancer-"
             "for-whom-immunotherapy-was-not-an-option-in-tropion-breast02.html.",
        check="title and date 19 October 2025 read on the page (2026-10-26); the parameter workbook names 'TROPION-Breast02 (Daiichi Sankyo/"
              "AstraZeneca, October 2025)' without a date, and this is the October 2025 release that reports the trial results "
              "(the 6 October release gives top-line results only) -- to be confirmed by A. Ozaki"),
    "worldbank_ppp": dict(
        text="World Bank. PPP conversion factor, GDP (LCU per international $) [Internet]. Washington, DC: World Bank; 2026 "
             "[cited 2026 Oct 26]. Available from: https://data.worldbank.org/indicator/PA.NUS.PPP.",
        check="HTTP 200; indicator page PA.NUS.PPP"),
    "boc_fx": dict(
        text="Bank of Canada. Annual exchange rates [Internet]. Ottawa: Bank of Canada; 2026 [cited 2026 Oct 26]. Available from: "
             "https://www.bankofcanada.ca/rates/exchange/annual-average-exchange-rates/.",
        check="HTTP 200; page 'Annual exchange rates'"),
    "olaparib_pi": dict(
        text="AstraZeneca KK. Lynparza tablets 100 mg and 150 mg: package insert, revised 17 March 2026 [Internet]. Osaka: AstraZeneca KK; "
             "2026 [cited 2026 Oct 26]. Available from: https://www.pmda.go.jp/PmdaSearch/iyakuDetail/GeneralList/4291052F1027. Japanese.",
        check="PMDA page: リムパーザ錠100mg／150mg, 製造販売元 アストラゼネカ株式会社, package insert PDF dated 2026年03月17日 (2026-10-26)"),
    "jsco2023": dict(
        text="Japan Society of Clinical Oncology. Guidelines for the appropriate use of antiemetics, October 2023 revision, 3rd ed. Tokyo: "
             "Kanehara Shuppan; 2023. Japanese.",
        check="Minds guideline page https://minds.jcqhc.or.jp/summary/c00828/ (HTTP 200): 制吐薬適正使用ガイドライン 2023年10月改訂 第3版, "
              "日本癌治療学会, published by 金原出版 on 2023-10-20"),
    "hosp_kasugai": dict(
        text="Kasugai Municipal Hospital. Estimated hospitalization costs [Internet]. Kasugai: Kasugai Municipal Hospital; 2024 "
             "[cited 2026 Oct 26]. Available from: https://www.hospital.kasugai.aichi.jp/goriyo/nyuin/documents/nyuinhiyougaisan.pdf. Japanese.",
        check="HTTP 200 (PDF, sha256 7881e456…); p.1 入院費用概算金額: 乳腺悪性腫瘍手術 乳房部分切除術, 5～10 days, 300,000 yen at 30% "
              "copayment; linked from the page 入院医療費 updated 2024-09-24"),
    "hosp_chuden": dict(
        text="Chuden Hospital. Estimated costs of surgery and other treatments [Internet]. Hiroshima: Chuden Hospital; [date unknown; "
             "cited 2026 Oct 26]. Available from: https://www.energia.co.jp/hospital/nyuuin/surgical-costs.html. Japanese.",
        check="HTTP 200; page 手術費用等概算一覧表｜中電病院: 乳腺悪性腫瘍手術, 15 days, about 300,000 yen at 30% copayment; no date on the page"),
}
REFS = JOURNAL + list(ABSTRACT) + list(GREY)
assert len(REFS) == len(set(REFS))


def cite(*keys: str) -> str:
    for k in keys:
        if k not in REFS:
            raise KeyError(f"unknown reference key {k}")
    return "⟦ref:" + ",".join(keys) + "⟧"


def nlm_pages(p: str) -> str:
    """810-821 -> 810-21 (NLM drops the repeated leading digits of the last page)."""
    m = re.fullmatch(r"(\d+)-(\d+)", p or "")
    if not m:
        return p
    a, b = m.groups()
    if len(a) == len(b):
        i = 0
        while i < len(a) - 1 and a[i] == b[i]:
            i += 1
        b = b[i:]
    return f"{a}-{b}"


def authors(names: list[str]) -> str:
    names = [n.strip() for n in names if n.strip()]
    return ", ".join(names[:6]) + (", et al" if len(names) > 6 else "")


def _initials(given: str) -> str:
    return "".join(w[0] for w in re.split(r"[\s.\-]+", given) if w)


def _journal_abbrev(container: str) -> str:
    """The PubMed abbreviation used by another cited article of the same journal."""
    for k, d in DOICHECK.items():
        if d.get("cr_journal") == container and k in PUBMED and PUBMED[k].get("journal"):
            return PUBMED[k]["journal"]
    raise KeyError(container)


def _title(t: str) -> str:
    t = re.sub(r"\s+", " ", t).strip()
    return t if t.endswith((".", "?", "!")) else t + "."


def entry(key: str) -> str:
    if key in GREY:
        return GREY[key]["text"]
    if key in ABSTRACT:
        c = CROSSREF[key]
        au = authors([f"{fam} {_initials(giv)}" for fam, giv in c["authors"]])
        first, last = (c["page"].split("-") + [""])[:2]
        pg = first if last in ("", first) else c["page"]
        iss = ABSTRACT[key]["issue"]
        vol = f"{c['volume']} {iss}" if iss.startswith("Suppl") else f"{c['volume']}({iss})"  # NLM: 21 Suppl 2 / 44(16 Suppl)
        return f"{au}. {_title(c['title'])} {_journal_abbrev(c['journal'])}. {c['issued'][0]};{vol}:{pg}. doi:{c['doi']}"
    m = PUBMED[key]
    pages = m["pages"] or str(DOICHECK.get(key, {}).get("cr_page") or "")
    au = authors(m["authors"])
    head = f"{au}. {_title(m['title'])} {m['journal']}. {m['year']}"
    if not m["volume"]:
        return f"{head}. Epub ahead of print. doi:{m['doi']}"
    vol = m["volume"] + (f"({m['issue']})" if m["issue"] else "")
    return f"{head};{vol}:{nlm_pages(pages)}. doi:{m['doi']}"


def year(key: str) -> int | None:
    if key in PUBMED:
        return int(PUBMED[key]["year"])
    if key in CROSSREF:
        return int(CROSSREF[key]["issued"][0])
    m = re.search(r"; (\d{4})", GREY[key]["text"])
    return int(m.group(1)) if m else None


def superscript(nums: list[int]) -> str:
    """Sorted numbers with ranges of three or more joined by an en dash: 1,2 / 1–3 / 1,3–5."""
    nums = sorted(set(nums))
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(f"{nums[i]}–{nums[j]}" if j - i >= 2 else ",".join(str(n) for n in nums[i:j + 1]))
        i = j + 1
    return ",".join(out)


def expand(sup: str) -> list[int]:
    out = []
    for part in sup.split(","):
        if "–" in part:
            a, b = part.split("–")
            out += list(range(int(a), int(b) + 1))
        elif part:
            out.append(int(part))
    return out
