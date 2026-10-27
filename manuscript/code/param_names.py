"""English labels for the input table (parameters_v10.xlsx) used in Supplementary Table S1.

Item names follow the Japanese item column; sources translate only the Japanese
parts of the source column. Personal communications are cited without names
(whether to name the clinical experts is the authors' decision).
"""

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

FEE = "Medical fee schedule, fiscal year 2026"
PRICE = "National drug price list, fiscal year 2026"
SOURCE = {
    "A06・A08の値から構成": "Derived from inputs A06 and A08",
    "C01の値から構成": "Derived from input C01",
    "Chan KKW, et al. J Clin Oncol 2026;44:2130-9; 世界銀行PPP 2024; カナダ銀行 為替2024":
        "Chan KKW, et al. J Clin Oncol 2026;44:2130-9; World Bank purchasing power parity 2024; Bank of Canada exchange rate 2024",
    "Nusawat C, et al. Eur J Health Econ 2026. doi:10.1007/s10198-026-01912-9（厚労省 医療保険部会2022を引用）; Ohtera S, et al. ISPOR AP 2018":
        "Nusawat C, et al. Eur J Health Econ 2026. doi:10.1007/s10198-026-01912-9 (citing a 2022 Ministry of Health, Labour and Welfare committee report); Ohtera S, et al. ISPOR Asia Pacific 2018",
    "厚生労働省 薬価基準収載品目リスト（注射薬）tp20261014-01_02.xlsx（令和8年10月14日収載品目反映版、令和8年4月1日以降の薬価）":
        "Ministry of Health, Labour and Welfare. National drug price list, injections (prices from April 2026; list as of 14 October 2026)",
    "春日井市民病院 入院費用概算金額; 中電病院 手術費用等概算一覧表; K476（令和8年度）; Kuemmel S, et al. Ann Surg Oncol 2026":
        "Published cost estimates of two Japanese hospitals; medical fee schedule code K476, fiscal year 2026; Kuemmel S, et al. Ann Surg Oncol 2026",
    "立花和之進 先生、押正徳 先生（個人的連絡、2026年10月）; Andrade MdeO, et al. Breast Cancer Res Treat 2026;216:27（Neo-Real/GBECAM 0123）; Valachis A, et al. Br J Cancer 2026;135:329-35":
        "Clinical experts (personal communication, October 2026); Andrade MdeO, et al. Breast Cancer Res Treat 2026;216:27; Valachis A, et al. Br J Cancer 2026;135:329-35",
    "立花和之進 先生（個人的連絡、2026年10月23日）": "Clinical expert (personal communication, October 2026)",
    "立花和之進 先生（個人的連絡、2026年10月24日、10月23日の回答を訂正）": "Clinical expert (personal communication, October 2026)",
    "立花和之進 先生（個人的連絡、2026年10月24日）; TROPION-Breast02（第一三共/AstraZeneca 2025年10月）; Cortes J, et al. Lancet 2020; Miller K, et al. NEJM 2007; 薬価基準 令和8年度":
        "Clinical expert (personal communication, October 2026); TROPION-Breast02 (Daiichi Sankyo and AstraZeneca, October 2025); Cortes J, et al. Lancet 2020; Miller K, et al. N Engl J Med 2007; " + PRICE,
    "立花和之進 先生（個人的連絡、2026年10月24日）; 押正徳 先生（2026年10月24日、gBRCA陽性例の経験なし）": "Clinical experts (personal communication, October 2026)",
    "立花和之進 先生（個人的連絡、2026年10月24日）; 薬価基準 令和8年度": "Clinical expert (personal communication, October 2026); " + PRICE,
    "薬価基準 令和8年度; Masuda N, et al. N Engl J Med 2017;376:2147-59": PRICE + "; Masuda N, et al. N Engl J Med 2017;376:2147-59",
    "薬価基準 令和8年度; リムパーザ添付文書": PRICE + "; olaparib package insert",
    "薬価基準 令和8年度; 日本癌治療学会 制吐薬適正使用ガイドライン2023（第3版）": PRICE + "; Japan Society of Clinical Oncology antiemetic guideline 2023 (3rd edition)",
    "診療報酬点数表 令和8年度": FEE,
}

RANGE_RULE = {"±25%": "±25% (assumed)", "片側対称": "mirrored (assumed)", "薬価固定": "drug price, lower only", "0例：PSAは固定": "zero events, fixed in PSA"}


def source(text: str, prev: str | None) -> str:
    if text == "同上":
        return prev
    if text in SOURCE:
        return SOURCE[text]
    if any("぀" <= ch <= "ヿ" or "一" <= ch <= "鿿" for ch in text):
        raise KeyError(f"untranslated source: {text}")
    return text
