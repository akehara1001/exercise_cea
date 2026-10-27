"""English labels for the input table (parameters_v10.xlsx) used in Supplementary Table S2.

Item names follow the Japanese item column. Each source text of the workbook is
mapped to a short label with reference markers (cite(); the full references are
in the reference list). Personal communications are cited without names, as
breast medical oncologists at Japanese hospitals (decision N6, 2026-10-26); the
number of experts follows the source text of the workbook.
"""
from references import cite

PC1 = "A breast medical oncologist at a Japanese hospital (personal communication, October 2026)"
PC2 = "Two breast medical oncologists at Japanese hospitals (personal communication, October 2026)"

ITEM = {
    "A01": "Paclitaxel plus carboplatin (12 weeks), drug cost",
    "A02": "Doxorubicin or epirubicin plus cyclophosphamide (4 cycles), drug cost",
    "A03": "Pembrolizumab, drug cost per dose",
    "A04": "Outpatient drug administration, per visit (fees and tests included)",
    "A05": "Supportive care (G-CSF, antiemetics), per cycle",
    "A06": "Surgery (mix of procedures)",
    "A07": "Postoperative radiotherapy, proportion treated",
    "A08": "Postoperative radiotherapy, cost per course",
    "B01": "Immune-related AE management cost: hypothyroidism",
    "B02": "Immune-related AE management cost: hyperthyroidism",
    "B03": "Immune-related AE management cost: adrenal insufficiency",
    "B04": "Immune-related AE management cost: hypophysitis",
    "B05": "Immune-related AE management cost: pneumonitis",
    "B06": "Immune-related AE management cost: colitis",
    "B07": "Immune-related AE management cost: hepatitis",
    "B08": "Immune-related AE management cost: severe skin reactions",
    "B09": "Immune-related AE management cost: type 1 diabetes",
    "B10": "Immune-related AE management cost: other serious events",
    "B11": "Febrile neutropenia management cost per event",
    "B21": "Incidence: hypothyroidism (immune-related)",
    "B22": "Incidence: hyperthyroidism (immune-related)",
    "B23": "Incidence: adrenal insufficiency (immune-related)",
    "B24": "Incidence: hypophysitis (immune-related)",
    "B25": "Incidence: pneumonitis (immune-related)",
    "B26": "Incidence: colitis (immune-related)",
    "B27": "Incidence: hepatitis (immune-related)",
    "B28": "Incidence: severe skin reactions (immune-related)",
    "B29": "Incidence: type 1 diabetes (immune-related)",
    "B30": "Incidence: other serious immune-related AEs",
    "B31": "Incidence: febrile neutropenia",
    "B32": "Incidence: any grade 3 or higher AE (scenario)",
    "B33": "Grade 3 or higher AEs of six types, events per patient",
    "C01": "Follow-up cost per year, years 1 to 2",
    "C02": "Follow-up cost per year, years 3 to 5",
    "C03": "Follow-up cost per year, year 6 onward",
    "D01": "Locoregional recurrence, initial treatment cost",
    "D02": "Locoregional recurrence, monthly cost thereafter",
    "D03": "First-line treatment of distant recurrence, monthly cost",
    "D04": "First-line treatment of distant recurrence, mean duration",
    "D05": "Second-line and later treatment, monthly cost",
    "D06": "End-of-life care, last 3 months",
    "E01": "CHALLENGE-based supervised program, total over 6 months",
    "E02": "Fee-schedule-based program, total over 6 months",
    "E03": "Remote low-cost program, total over 6 months",
    "E04": "Exercise continued after surgery, monthly cost (scenario)",
    "E05": "Exercise continued after surgery, duration (scenario)",
    "E06": "Musculoskeletal AEs, any grade, with exercise",
    "E07": "Musculoskeletal AEs, any grade, without exercise",
    "E08": "Musculoskeletal AE management cost per event",
    "E09": "Musculoskeletal AEs, grade 3 or higher, with exercise",
    "E10": "Musculoskeletal AEs, grade 3 or higher, without exercise",
    "F01": "Capecitabine use among gBRCA-negative patients without pCR",
    "F02": "Capecitabine cost, whole course",
    "F03": "gBRCA-positive proportion among patients with TNBC",
    "F04": "Olaparib use among gBRCA-positive patients without pCR",
    "F05": "Olaparib cost, whole course",
    "F06": "BRCA test cost",
    "F07": "Capecitabine HR for invasive disease or recurrence",
    "F08": "Olaparib HR for invasive disease",
    "U01": "Utility, event-free during treatment",
    "U02": "Utility, event-free after treatment",
    "U03": "Utility, locoregional recurrence",
    "U04": "Utility, distant recurrence or progression during neoadjuvant therapy",
    "U05": "Utility decrement per grade 3 or higher AE (12.5 weeks)",
}


def item(pid: str) -> str:
    """B21P/B21C, D03P, F01P and the like share the label of their stem."""
    return ITEM[pid] if pid in ITEM else ITEM[pid[:-1]]


ARM = {
    "全群": "All arms",
    "ペムブロリズマブを含む群": "With pembrolizumab",
    "ペムブロリズマブを含む群（運動を加えた群を含む）": "With pembrolizumab",
    "ペムブロリズマブを含まない群": "Without pembrolizumab",
    "化学療法のみの群（運動を加えた群を含む）": "Without pembrolizumab",
    "運動を含む群": "With exercise",
    "運動を含まない群": "Without exercise",
}

UNIT = {
    "ハザード比": "HR",
    "円/年": "JPY per year",
    "円/件（1コースの総額）": "JPY per course",
    "円/件": "JPY per event",
    "円/回": "JPY per administration",
    "月": "months",
    "円（6か月の総額）": "JPY per 6 months",
    "円/月": "JPY per month",
    "円（3か月の総額）": "JPY per 3 months",
    "件/人": "events per patient",
    "円（12週の総額）": "JPY per 12 weeks",
    "効用値（0から1）": "utility",
    "効用値の低下幅（期間は備考に）": "utility decrement",
    "円/人": "JPY per patient",
    "割合（0から1）": "proportion",
    "円（4サイクルの総額）": "JPY per 4 cycles",
    "円/サイクル": "JPY per cycle",
}

FEE = "Medical fee schedule" + cite("fee2026")
PRICE = "national drug price list"
KN522 = "KEYNOTE-522 (interim analysis 4)" + cite("schmid2022")
EMA = "European Medicines Agency assessment report" + cite("ema2022")
SOURCE = {
    "A06・A08の値から構成": "Derived from inputs A06 and A08",
    "C01の値から構成": "Derived from input C01",
    "Chan KKW, et al. J Clin Oncol 2026;44:2130-9; 世界銀行PPP 2024; カナダ銀行 為替2024":
        "CHALLENGE cost-utility analysis; purchasing power parity and exchange rate" + cite("chan2026", "worldbank_ppp", "boc_fx"),
    "Nusawat C, et al. Eur J Health Econ 2026. doi:10.1007/s10198-026-01912-9（厚労省 医療保険部会2022を引用）; Ohtera S, et al. ISPOR AP 2018":
        "Published Japanese estimates" + cite("nusawat2026", "ohtera2018"),
    "Nusawat C, et al. Eur J Health Econ 2026. doi:10.1007/s10198-026-01912-9": "Published Japanese estimate" + cite("nusawat2026"),
    "Yoshinami T, et al. Breast Cancer 2025;32:857-66. doi:10.1007/s12282-025-01714-6": "Published Japanese estimate, used as a proxy" + cite("yoshinami2025"),
    "Yoshinami T, et al. Breast Cancer 2025;32:857-66. doi:10.1007/s12282-025-01714-6; Nusawat C, et al. Eur J Health Econ 2026. doi:10.1007/s10198-026-01912-9":
        "Published Japanese estimates" + cite("yoshinami2025", "nusawat2026"),
    "厚生労働省 薬価基準収載品目リスト（注射薬）tp20261014-01_02.xlsx（令和8年10月14日収載品目反映版、令和8年4月1日以降の薬価）":
        "National drug price list" + cite("price2026"),
    "春日井市民病院 入院費用概算金額; 中電病院 手術費用等概算一覧表; K476（令和8年度）; Kuemmel S, et al. Ann Surg Oncol 2026":
        "Published cost estimates of Kasugai Municipal Hospital and Chuden Hospital; medical fee schedule code K476; KEYNOTE-522 surgical outcomes"
        + cite("hosp_kasugai", "hosp_chuden", "fee2026", "kuemmel2026"),
    "Kuemmel S, et al. Ann Surg Oncol 2026;33:5550-7": "KEYNOTE-522 surgical outcomes" + cite("kuemmel2026"),
    "Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23)": KN522,
    "EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23)": EMA,
    "Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23); EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23)":
        "KEYNOTE-522 (interim analysis 4); European Medicines Agency assessment report" + cite("schmid2022", "ema2022"),
    "Schmid P, et al. N Engl J Med 2022;386:556-67, Supplementary Appendix (IA4, data cutoff 2021-03-23)":
        "KEYNOTE-522 supplementary appendix (interim analysis 4)" + cite("schmid2022"),
    "立花和之進 先生、押正徳 先生（個人的連絡、2026年10月）; Andrade MdeO, et al. Breast Cancer Res Treat 2026;216:27（Neo-Real/GBECAM 0123）; Valachis A, et al. Br J Cancer 2026;135:329-35":
        PC2 + "; real-world and expert-consensus studies" + cite("andrade2026", "valachis2026"),
    "立花和之進 先生（個人的連絡、2026年10月23日）": PC1,
    "立花和之進 先生（個人的連絡、2026年10月24日、10月23日の回答を訂正）": PC1,
    "立花和之進 先生（個人的連絡、2026年10月24日）; TROPION-Breast02（第一三共/AstraZeneca 2025年10月）; Cortes J, et al. Lancet 2020; Miller K, et al. NEJM 2007; 薬価基準 令和8年度":
        PC1 + "; trials; " + PRICE + cite("tropion2025", "cortes2020", "miller2007", "price2026"),
    "立花和之進 先生（個人的連絡、2026年10月24日）; 押正徳 先生（2026年10月24日、gBRCA陽性例の経験なし）": PC2,
    "立花和之進 先生（個人的連絡、2026年10月24日）; 薬価基準 令和8年度": PC1 + "; " + PRICE + cite("price2026"),
    "Nusawat C, et al. Eur J Health Econ 2026. doi:10.1007/s10198-026-01912-9（厚労省 医療保険部会2022を引用）; Ohtera S, et al. ISPOR AP 2018 ": None,
    "Courneya KS, et al. N Engl J Med 2025;393:13-25": "CHALLENGE trial" + cite("courneya2025"),
    "Courneya KS, et al. N Engl J Med 2025;393:13-25 (CHALLENGE, CCTG CO.21). DOI 10.1056/NEJMoa2502760": "CHALLENGE trial" + cite("courneya2025"),
    "薬価基準 令和8年度; Masuda N, et al. N Engl J Med 2017;376:2147-59": "National drug price list; CREATE-X" + cite("price2026", "masuda2017"),
    "Fujisawa F, et al. Mol Clin Oncol 2021;14:96. doi:10.3892/mco.2021.2258": "Japanese single-institution study" + cite("fujisawa2021"),
    "薬価基準 令和8年度; リムパーザ添付文書": "National drug price list; olaparib package insert" + cite("price2026", "olaparib_pi"),
    "Masuda N, et al. 2017. N Engl J Med 376:2147-59. DOI 10.1056/NEJMoa1612645": "CREATE-X" + cite("masuda2017"),
    "Garber JE, et al. 2026. Ann Oncol (online ahead of print). DOI 10.1016/j.annonc.2026.08.002": "OlympiA, updated analysis" + cite("garber2026"),
    "Favre-Bulle A, Huang M, Haiderali A, Bhadhuri A. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854":
        "KEYNOTE-522 EQ-5D-5L, German value set" + cite("favrebulle2024"),
    "Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854":
        "KEYNOTE-522 EQ-5D-5L, German value set" + cite("favrebulle2024"),
    "薬価基準 令和8年度; 日本癌治療学会 制吐薬適正使用ガイドライン2023（第3版）": "National drug price list; antiemetic guideline" + cite("price2026", "jsco2023"),
    "診療報酬点数表 令和8年度": FEE,
}
SOURCE = {k: v for k, v in SOURCE.items() if v is not None}

RANGE_RULE = {"±25%": "±25% (assumed)", "片側対称": "mirrored (assumed)", "薬価固定": "drug price, lower only", "0例：PSAは固定": "zero events, fixed in PSA"}


def source(text: str, prev: str | None) -> str:
    if text == "同上":
        return prev
    if text in SOURCE:
        return SOURCE[text]
    raise KeyError(f"source without a mapped label and reference: {text}")
