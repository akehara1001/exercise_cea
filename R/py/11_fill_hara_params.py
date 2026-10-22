"""Fill the rows owned by 原 in the parameter sheet (v1 -> v2): A01-A03 drug costs, B21P-B31C
adverse event rates, U01-U05 utilities. Rows owned by 尾崎 are not touched.

Usage: .venv/Scripts/python.exe -I R/py/11_fill_hara_params.py <project_root>
Reads:
  input/params/parameters_template_v1.xlsx (moved to input/params/archive/ by the caller via git mv)
  input/params/sources_price/tp20261014-01_02.xlsx  (MHLW 薬価基準収載品目リスト, 注射薬)
  input/params/sources_bsa/NHNS_R6_2024_table14_*.xlsx (国民健康・栄養調査 令和6年 第14表)
  input/papers/*.pdf (KEYNOTE-522), input/params/sources_ae/EMA_keytruda_II0110_assessment.pdf
  input/params/sources_ae/ema_aeosi_transcribed.csv (values read from table images, with pages)
  input/params/sources_utility/utilities_selected.csv (utility values chosen, with sources)
Writes:
  input/params/parameters_v2.xlsx; data/params_hara/drug_costs.csv, drug_vials.csv,
  ae_rates.csv, hara_values.csv (everything that went into the sheet, with sources)
All numbers come from the source files read here; nothing is typed in except the regimen
(KEYNOTE-522 protocol doses, PMDA review report 表14) and the choices documented below.
"""
import sys, os, re, csv, itertools, math, glob, unicodedata, warnings
warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
from openpyxl import load_workbook
import pymupdf as fitz

root = sys.argv[1]
P = lambda *a: os.path.join(root, *a)
out_dir = P("data", "params_hara")
os.makedirs(out_dir, exist_ok=True)


def wcsv(name, rows):
    with open(os.path.join(out_dir, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def pdf_text(path, page):
    return " ".join(fitz.open(path)[page - 1].get_text().split())


# ---------------------------------------------------------------- body size, creatinine
nh = glob.glob(P("input", "params", "sources_bsa", "NHNS_R6_2024_table14_*.xlsx"))[0]
ws = load_workbook(nh, read_only=True, data_only=True)["14"]
assert ws.cell(37, 1).value == "40-49歳" and ws.cell(6, 8).value == "女性"
HEIGHT, WEIGHT = float(ws.cell(37, 9).value), float(ws.cell(37, 12).value)
BSA = 0.007184 * WEIGHT ** 0.425 * HEIGHT ** 0.725                       # Du Bois
AGE = 49
SCR = 0.62     # JCCLS 共用基準範囲 女性 中間値 (表4, PDF p.21, read from the table image)
CRCL = (140 - AGE) * WEIGHT / (72 * SCR) * 0.85                           # Cockcroft-Gault, female
CRCL_ADJ = (140 - AGE) * WEIGHT / (72 * (SCR + 0.2)) * 0.85               # scenario: enzymatic Cr + 0.2

# ---------------------------------------------------------------- price list
price_file = P("input", "params", "sources_price", "tp20261014-01_02.xlsx")
pl = load_workbook(price_file, read_only=True, data_only=True).active
rows = list(pl.iter_rows(values_only=True))
hdr = rows[0]
assert hdr[2] == "成分名" and hdr[3] == "規格" and hdr[7] == "品名" and hdr[12] == "薬価"


def mg_of(spec):
    s = unicodedata.normalize("NFKC", spec)
    m = re.match(r"([\d.]+)mg", s)
    return float(m.group(1))


def products(ingredient, exclude_names=()):
    out = []
    for r in rows[1:]:
        if r[2] == ingredient and not any(x in (r[7] or "") for x in exclude_names):
            kind = "generic" if r[9] in ("後発品", "★") else ("originator" if r[10] == "先発品" else "only")
            out.append(dict(ingredient=ingredient, code=r[1], spec=unicodedata.normalize("NFKC", r[3]), mg=mg_of(r[3]),
                            name=unicodedata.normalize("NFKC", r[7]), maker=r[8], kind=kind, flag_generic=r[9] or "",
                            price=float(r[12]), transitional=r[13] or ""))
    return out


DRUGS = {
    "paclitaxel": products("パクリタキセル", exclude_names=("アブラキサン",)),     # nab-paclitaxel is another product
    "carboplatin": products("カルボプラチン"),
    "doxorubicin": products("ドキソルビシン塩酸塩", exclude_names=("ドキシル",)),  # liposomal doxorubicin excluded
    "epirubicin": products("エピルビシン塩酸塩"),
    "cyclophosphamide": products("シクロホスファミド水和物"),
    "pembrolizumab": products("ペムブロリズマブ（遺伝子組換え）"),
}
vial_rows = [dict(drug=d, **p) for d, ps in DRUGS.items() for p in ps]
wcsv("drug_vials.csv", vial_rows)


def price_table(drug, which):
    """lowest price per strength: which = 'base' (lowest generic where a generic exists, else the
    listed product) or 'originator' (先発品 where listed, else the base price)."""
    ps = DRUGS[drug]
    out = {}
    for mg in sorted({p["mg"] for p in ps}):
        cands = [p for p in ps if p["mg"] == mg]
        gen = [p for p in cands if p["kind"] == "generic"]
        org = [p for p in cands if p["kind"] == "originator"]
        key = lambda p: (p["price"], p["transitional"] != "")      # ties: prefer products not being delisted
        if which == "originator" and org:
            pick = min(org, key=key)
        elif gen:
            pick = min(gen, key=key)
        else:
            pick = min(cands, key=key)
        out[mg] = pick
    return out


def cheapest_vials(dose, table):
    """cheapest combination of vials covering the dose (no vial sharing); ties: less waste"""
    sizes = sorted(table)
    best = None
    rng = [range(0, int(math.ceil(dose / s)) + 1) for s in sizes]
    for counts in itertools.product(*rng):
        mg = sum(c * s for c, s in zip(counts, sizes))
        if mg + 1e-9 < dose:
            continue
        cost = sum(c * table[s]["price"] for c, s in zip(counts, sizes))
        key = (cost, mg)
        if best is None or key < best[0]:
            best = (key, counts)
    (cost, mg), counts = best
    combo = " + ".join(f"{c}x{s:g}mg({table[s]['name']} {table[s]['price']:g}円)" for c, s in zip(counts, sizes) if c)
    return cost, mg, combo


def course(name, items, which):
    """items: (drug, dose_mg, n_admin); returns total cost and detail rows"""
    total, det = 0.0, []
    for drug, dose, n in items:
        cost, mg, combo = cheapest_vials(dose, price_table(drug, which))
        total += cost * n
        det.append(dict(course=name, prices=which, drug=drug, dose_mg=round(dose, 2), vial_mg=mg, cost_per_admin=cost,
                        n_admin=n, cost=cost * n, vials=combo))
    return total, det


auc_w = lambda auc, crcl: auc * (crcl + 25)                               # Calvert
REG = {
    # KEYNOTE-522 (PMDA review report 表14): PTX 80 mg/m2 weekly x12; CBDCA AUC 1.5 weekly x12 or
    # AUC 5 q3w x4; AC = ADM 60 mg/m2 + CPA 600 mg/m2 q3w x4; EC = EPI 90 mg/m2 + CPA 600 mg/m2 q3w x4
    "A01_base_CBDCA_weekly": [("paclitaxel", 80 * BSA, 12), ("carboplatin", auc_w(1.5, CRCL), 12)],
    "A01_CBDCA_q3w": [("paclitaxel", 80 * BSA, 12), ("carboplatin", auc_w(5, CRCL), 4)],
    "A01_CBDCA_weekly_Cr+0.2": [("paclitaxel", 80 * BSA, 12), ("carboplatin", auc_w(1.5, CRCL_ADJ), 12)],
    "A02_base_AC": [("doxorubicin", 60 * BSA, 4), ("cyclophosphamide", 600 * BSA, 4)],
    "A02_EC": [("epirubicin", 90 * BSA, 4), ("cyclophosphamide", 600 * BSA, 4)],
    "A03_pembro_200mg": [("pembrolizumab", 200, 1)],
}
costs, details = [], []
for name, items in REG.items():
    for which in ("base", "originator"):
        tot, det = course(name, items, which)
        costs.append(dict(course=name, prices=which, total_yen=tot))
        details += det
wcsv("drug_costs.csv", details)
C = {(c["course"], c["prices"]): c["total_yen"] for c in costs}

# KEYNOTE-522 drug exposure (2024 appendix Table S3): which carboplatin schedule and anthracycline
t = pdf_text(P("input", "papers", "nejmoa2409932_appendix.pdf"), 20)
ex = {k: re.search(rx, t).groups() for k, rx in {
    "cbdca_weekly": r"Carboplatin \(weekly\) n (\d+) (\d+)", "cbdca_q3w": r"Carboplatin \(Q3W\) n (\d+) (\d+)",
    "doxorubicin": r"Doxorubicin \(Q3W\) n (\d+) (\d+)", "epirubicin": r"Epirubicin \(Q3W\) n (\d+) (\d+)"}.items()}

# ---------------------------------------------------------------- adverse events
N = {"P": 783, "C": 389}
t2 = pdf_text(P("input", "papers", "NEJMoa2112651.pdf"), 9)
assert "Table 2. Adverse Events in the Combined Neoadjuvant and Adjuvant Phases (As-Treated Population)" in t2
assert "Pembrolizumab–Chemotherapy (N = 783) Placebo–Chemotherapy (N = 389)" in t2
cell = r"(\d+)(?: \([\d.]+\))?"
def t2row(label):
    m = re.search(re.escape(label) + r"‡? " + " ".join([cell] * 4), t2)
    return dict(zip(["P_any", "P_g3", "C_any", "C_g3"], map(int, m.groups()))), m.group(0)
T2 = {k: t2row(k) for k in ["Immune-mediated adverse event", "Hypothyroidism", "Severe skin reaction", "Hyperthyroidism",
                            "Adrenal insufficiency", "Pneumonitis", "Thyroiditis", "Hypophysitis"]}
s7 = pdf_text(P("input", "papers", "nejmoa2112651_appendix.pdf"), 28)
assert s7.startswith("27 Table S7. Grade 3-5 Adverse Events")
m = re.search(r"Febrile neutropenia (\d+) \(([\d.]+)\) (\d+) \(([\d.]+)\)", s7)
FN = dict(P_g3=int(m.group(1)), C_g3=int(m.group(3))), m.group(0)
ema = P("input", "params", "sources_ae", "EMA_keytruda_II0110_assessment.pdf")
e101 = pdf_text(ema, 101)
EMA_G34 = {k: int(re.search(k + r" \(n=(\d+) \[", e101).group(1)) for k in ["hepatitis", "colitis", "pneumonitis", "nephritis", "pancreatitis"]}
TR = {}
with open(P("input", "params", "sources_ae", "ema_aeosi_transcribed.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        TR[r["category"]] = r

def rate(n, arm): return n / N[arm]
other_g3 = {arm: T2["Immune-mediated adverse event"][0][f"{arm}_g3"] - sum(
    T2[k][0][f"{arm}_g3"] for k in ["Hypothyroidism", "Severe skin reaction", "Hyperthyroidism", "Adrenal insufficiency",
                                    "Pneumonitis", "Thyroiditis", "Hypophysitis"]) - (
    (EMA_G34["colitis"] + EMA_G34["hepatitis"]) if arm == "P" else 0) for arm in ("P", "C")}

SRC_T2 = "Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23)"
SRC_S7 = "Schmid P, et al. N Engl J Med 2022;386:556-67, Supplementary Appendix (IA4, data cutoff 2021-03-23)"
SRC_EMA = "EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23)"
AE = []
def add_ae(i, label, arm, n, grade, src, where, note=""):
    AE.append(dict(param_id=f"B{i}{arm}", item=label, arm=arm, n=n, N=N[arm], rate=rate(n, arm), grade=grade,
                   source=src, where=where, note=note))
for arm in ("P", "C"):
    a = "P" if arm == "P" else "C"
    add_ae(21, "甲状腺機能低下症", arm, T2["Hypothyroidism"][0][f"{a}_any"], "全Grade", SRC_T2, "Table 2（Hypothyroidism）",
           f"甲状腺炎（全Grade {T2['Thyroiditis'][0][f'{a}_any']}例）は含めない")
    add_ae(22, "甲状腺機能亢進症", arm, T2["Hyperthyroidism"][0][f"{a}_any"], "全Grade", SRC_T2, "Table 2（Hyperthyroidism）")
    add_ae(23, "副腎不全", arm, T2["Adrenal insufficiency"][0][f"{a}_any"], "全Grade", SRC_T2, "Table 2（Adrenal insufficiency）")
    add_ae(24, "下垂体炎", arm, T2["Hypophysitis"][0][f"{a}_any"], "全Grade", SRC_T2, "Table 2（Hypophysitis）")
    add_ae(25, "肺臓炎", arm, T2["Pneumonitis"][0][f"{a}_g3"], "Grade 3以上", SRC_T2, "Table 2（Pneumonitis）")
    if arm == "P":
        add_ae(26, "大腸炎", arm, EMA_G34["colitis"], "Grade 3以上", SRC_EMA, "p.101 本文（Grade 3-4 の AEOSI）",
               f"全Grade は {TR['colitis']['P_any']}例（p.{TR['colitis']['page']} 表、画像から転記）")
        add_ae(27, "肝炎", arm, EMA_G34["hepatitis"], "Grade 3以上", SRC_EMA, "p.101 本文（Grade 3-4 の AEOSI）",
               f"全Grade は {TR['hepatitis']['P_any']}例（p.{TR['hepatitis']['page']} 表、画像から転記）")
    else:
        add_ae(26, "大腸炎", arm, 0, "Grade 3以上", SRC_EMA, f"p.{TR['colitis']['page']} 表（全Grade、画像から転記）",
               f"プラセボ群の Grade 3以上は未報告。全Grade {TR['colitis']['C_any']}例を上限とし、基本値は0")
        add_ae(27, "肝炎", arm, 0, "Grade 3以上", SRC_EMA, f"p.{TR['hepatitis']['page']} 表（全Grade、画像から転記）",
               f"プラセボ群の Grade 3以上は未報告。全Grade {TR['hepatitis']['C_any']}例を上限とし、基本値は0")
    add_ae(28, "重度の皮膚障害", arm, T2["Severe skin reaction"][0][f"{a}_g3"], "Grade 3以上", SRC_T2, "Table 2（Severe skin reaction）")
    add_ae(29, "1型糖尿病", arm, int(TR["type1_diabetes"][f"{a}_any"]), "全Grade", SRC_EMA,
           f"p.{TR['type1_diabetes']['page']} Table 5.3.5.3.3-tnbc3: 30（画像から転記）")
    add_ae(30, "その他の重篤なもの", arm, max(other_g3[arm], 0), "Grade 3以上", SRC_T2 + "; " + SRC_EMA,
           "Table 2 の免疫介在性有害事象 Grade 3以上の総数から、表の各項目と大腸炎、肝炎の Grade 3以上を差し引いた近似",
           "患者単位の重複があるため近似値。B10 の定義と合わせて尾崎先生に確認")
    add_ae(31, "発熱性好中球減少症", arm, FN[0][f"{a}_g3"], "Grade 3以上", SRC_S7, "Table S7（Grade 3-5）")
wcsv("ae_rates.csv", AE)

# ---------------------------------------------------------------- utilities
UT = {}
ut_file = P("input", "params", "sources_utility", "utilities_selected.csv")
if os.path.exists(ut_file):
    with open(ut_file, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            v, se = float(r["value"]), float(r["se"])
            r["lower"] = round(max(v - 1.96 * se, 0), 4)                       # decrement (U05) truncated at 0
            r["upper"] = round(min(v + 1.96 * se, 1), 4)
            UT[r["param_id"]] = r
else:
    print("utilities_selected.csv not found: U rows left empty")

# ---------------------------------------------------------------- fill the sheet
src_v1 = P("input", "params", "parameters_template_v1.xlsx")
if not os.path.exists(src_v1):
    src_v1 = P("input", "params", "archive", "parameters_template_v1.xlsx")
wb = load_workbook(src_v1)
sh = wb["パラメータ"]
cols = [c.value for c in sh[1]]
ci = {c: i + 1 for i, c in enumerate(cols)}
row_of = {sh.cell(r, 1).value: r for r in range(2, sh.max_row + 1)}
filled = []


def put(pid, **kw):
    r = row_of[pid]
    assert sh.cell(r, ci["担当"]).value == "原", pid
    for k, v in kw.items():
        sh.cell(r, ci[k]).value = v
    filled.append(dict(param_id=pid, **{k: v for k, v in kw.items()}))


price_src = f"厚生労働省 薬価基準収載品目リスト（注射薬）{os.path.basename(price_file)}（令和8年10月14日収載品目反映版、令和8年4月1日以降の薬価）"
body = (f"体表面積 {BSA:.3f} m2（Du Bois、令和6年国民健康・栄養調査 第14表 女性40-49歳の平均身長 {HEIGHT:g} cm、平均体重 {WEIGHT:g} kg）。"
        f"1回ごとに瓶単位で切り上げ、分割使用なし。")
det = lambda course_, w: "；".join(d["vials"] + f" x{d['n_admin']}回" for d in details if d["course"] == course_ and d["prices"] == w)
put("A01", 基本値=round(C[("A01_base_CBDCA_weekly", "base")]), 価格の年度="令和8年度", 出典=price_src,
    出典の該当箇所="パクリタキセル、カルボプラチンの各行（後発品の最低薬価）",
    備考=(f"{body} PTX 80 mg/m2 毎週12回、CBDCA AUC 1.5 毎週12回（Calvert式、CrCl {CRCL:.1f} mL/min は Cockcroft-Gault、49歳、"
          f"血清Cr {SCR} mg/dL＝JCCLS共用基準範囲の女性中間値）。KEYNOTE-522 ではカルボプラチン毎週投与が多数"
          f"（ペムブロリズマブ群 {ex['cbdca_weekly'][0]} 例対 3週毎 {ex['cbdca_q3w'][0]} 例、2024年補足 Table S3）。"
          f"内訳：{det('A01_base_CBDCA_weekly', 'base')}。シナリオ：先発品の薬価 {C[('A01_base_CBDCA_weekly', 'originator')]:,.0f} 円；"
          f"CBDCA AUC 5 3週毎4回 {C[('A01_CBDCA_q3w', 'base')]:,.0f} 円；Cr に 0.2 を加える慣行 {C[('A01_CBDCA_weekly_Cr+0.2', 'base')]:,.0f} 円。"
          "薬価は固定（確率的感度分析で動かさない）。"))
put("A02", 基本値=round(C[("A02_base_AC", "base")]), 価格の年度="令和8年度", 出典=price_src,
    出典の該当箇所="ドキソルビシン塩酸塩（リポソーム製剤を除く）、シクロホスファミド水和物の各行",
    備考=(f"{body} AC（ADM 60 mg/m2 + CPA 600 mg/m2、3週毎4回）。KEYNOTE-522 ではドキソルビシンが多数"
          f"（ペムブロリズマブ群 {ex['doxorubicin'][0]} 例対エピルビシン {ex['epirubicin'][0]} 例、2024年補足 Table S3）。"
          f"内訳：{det('A02_base_AC', 'base')}。シクロホスファミドは後発品なし。シナリオ：先発品の薬価 {C[('A02_base_AC', 'originator')]:,.0f} 円；"
          f"EC（EPI 90 mg/m2、後発品のみ収載）{C[('A02_EC', 'base')]:,.0f} 円。薬価は固定。"))
put("A03", 基本値=round(C[("A03_pembro_200mg", "base")]), 価格の年度="令和8年度", 出典=price_src,
    出典の該当箇所="ペムブロリズマブ（遺伝子組換え）キイトルーダ点滴静注100mg",
    備考=f"200 mg（100 mg 瓶 x2）を3週毎、術前8回、術後9回。後発品なし。薬価は固定。")
def cp_ci(x, n):
    """Clopper-Pearson 95% interval by bisection on the binomial tails"""
    def cdf(k, p): return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))
    def root(g):                    # g monotone on [0, 1] with a sign change
        lo, hi = 0.0, 1.0
        up = g(hi) > g(lo)
        for _ in range(200):
            mid = (lo + hi) / 2
            if (g(mid) < 0) == up:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    lower = 0.0 if x == 0 else root(lambda p: (1 - cdf(x - 1, p)) - 0.025)   # P(X >= x) = 0.025
    upper = 1.0 if x == n else root(lambda p: cdf(x, p) - 0.025)             # P(X <= x) = 0.025
    return lower, upper
for a in AE:
    lo, hi = cp_ci(a["n"], a["N"])
    if a["param_id"] in ("B26C", "B27C"):
        hi = max(hi, int(TR["colitis" if a["param_id"] == "B26C" else "hepatitis"]["C_any"]) / a["N"])
    put(a["param_id"], 基本値=round(a["rate"], 5), 下限=round(lo, 5), 上限=round(hi, 5),
        出典=a["source"], 出典の該当箇所=a["where"],
        備考=f"{a['grade']}、{a['n']}/{a['N']} 例（as-treated）。下限と上限は Clopper-Pearson 95%信頼区間。" + (a["note"] + "。" if a["note"] else ""))
for pid in [p for p in ["U01", "U02", "U03", "U04", "U05"] if p in UT]:
    u = UT[pid]
    put(pid, 基本値=float(u["value"]), 下限=u["lower"], 上限=u["upper"], 出典=u["citation"], 出典の該当箇所=u["location"], 備考=u["note"])
out_xlsx = P("input", "params", "parameters_v2.xlsx")
wb.save(out_xlsx)
wcsv("hara_values.csv", [{k: ("" if v is None else v) for k, v in dict(param_id=f["param_id"], 基本値=f.get("基本値"), 下限=f.get("下限"),
                                                                     上限=f.get("上限"), 出典=f.get("出典"), 出典の該当箇所=f.get("出典の該当箇所"),
                                                                     備考=f.get("備考")).items()} for f in filled])
# ---------------------------------------------------------------- sources_hara.md
import hashlib
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
used = {(d["drug"], v.strip()) for d in details for v in re.findall(r"\d+x[\d.]+mg\(([^)]*)\)", d["vials"])}
M = ["# 原负责参数的来源（入力表 v2：A01 至 A03、B21P 至 B31C、U01 至 U05）", "",
     "由 `R/py/11_fill_hara_params.py` 从下列文件读取后写入 `input/params/parameters_v2.xlsx`，本文件同时生成；数值不手抄。中间结果在 `data/params_hara/`。", "",
     "## A. 药价（A01 至 A03）", "",
     f"- 薬価：厚生劳动省「薬価基準収載品目リスト及び後発医薬品に関する情報について」注射药 `{os.path.basename(price_file)}`"
     f"（https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_02.xlsx，令和8年4月1日适用页面上 10月14日收载品目反映版，2026-10-22 下载，sha256 {sha(price_file)[:16]}…）。令和8年度的薬価，年度内收载的新品目已反映，既有品目的薬价在年度内不变。",
     "- 规则：有后发品的药物，基准取后发品（表中「後発品」或「★」）的最低薬価，先发品薬価作为情景；没有后发品的药物用收载品目的薬价。每次给药取覆盖剂量的最便宜小瓶组合（向上取整、不分装）。",
     "- 排除：ドキシル（脂质体多柔比星）与アブラキサン（白蛋白结合型紫杉醇），属不同制剂。",
     f"- 体表面积 {BSA:.4f} m2：Du Bois 式，令和6年国民健康・栄养调查第2部第14表（全国补正值）女性 40 至 49 岁的平均身高 {HEIGHT:g} cm、平均体重 {WEIGHT:g} kg"
     f"（e-Stat statInfId 000040502147，`{os.path.basename(nh)}` 工作表 14 的 I37、L37）。参考：C2H 公的分析 C2H2409（サシツズマブ ゴビテカン，2026-02-06）的体表面积设定为 1.56 m2（p.42 表4-2-1，`sources_bsa/C2H2409_Report_sacituzumab_govitecan_v1.0_20260206.pdf`）。",
     f"- 卡铂：Calvert 式 剂量 = AUC × (CrCl + 25)；CrCl {CRCL:.1f} mL/min 为 Cockcroft-Gault（49 岁、体重同上、女性 × 0.85），血清肌酐 {SCR} mg/dL 取 JCCLS 共用基準範囲（2022-10-01 修订）表4 女性中间值（n = 2899，下限 0.46、上限 0.79；`sources_bsa/JCCLS_kyoyo_kijyunhani_20221001.pdf` p.21，从表格图像读取）。情景：酶法肌酐加 0.2 mg/dL 的惯例，CrCl {CRCL_ADJ:.1f} mL/min（此惯例本次未核对出处）。",
     f"- 方案：KEYNOTE-522（PMDA 审查报告 2022-08-10 表14，`sources_ae/PMDA_keytruda_review_20220810.pdf` p.30）：紫杉醇 80 mg/m2 每周 12 次；卡铂 AUC 1.5 每周 12 次或 AUC 5 每 3 周 4 次；AC = 多柔比星 60 mg/m2 + 环磷酰胺 600 mg/m2，EC = 表柔比星 90 mg/m2 + 环磷酰胺 600 mg/m2，每 3 周 4 次；帕博利珠单抗 200 mg 每 3 周（术前 8 次、术后 9 次）。"
     f"基准按 KEYNOTE-522 的实际给药（2024 年补充材料 Table S3）：卡铂每周（帕博利珠单抗组 {ex['cbdca_weekly'][0]} 例、安慰剂组 {ex['cbdca_weekly'][1]} 例）多于每 3 周（{ex['cbdca_q3w'][0]}、{ex['cbdca_q3w'][1]} 例）；多柔比星（{ex['doxorubicin'][0]}、{ex['doxorubicin'][1]} 例）多于表柔比星（{ex['epirubicin'][0]}、{ex['epirubicin'][1]} 例）。", "",
     "| 疗程 | 薬価 | 总额（日元） |", "|---|---|---|"]
M += [f"| {c['course']} | {'先发品（情景）' if c['prices'] == 'originator' else '基准'} | {c['total_yen']:,.0f} |" for c in costs]
M += ["", "所用的小瓶（基准与情景中被选中的品目）：", "", "| 药物 | 规格 | 品名 | 区分 | 薬価（日元） | 经过措置 |", "|---|---|---|---|---|---|"]
for v in vial_rows:
    if (v["drug"], f"{v['name']} {v['price']:g}円") in used:
        M.append(f"| {v['drug']} | {v['spec']} | {v['name']} | {v['kind']}{('（' + v['flag_generic'] + '）') if v['flag_generic'] else ''} | {v['price']:g} | {v['transitional']} |")
M += ["", "注：标有经过措置（例如「R9.3.31まで」）的品目将从薬価基準删除，令和8年度内仍为收载品目，故计入最低薬価的比较。每次给药的小瓶组合见 `data/params_hara/drug_costs.csv`，全部候选品目见 `drug_vials.csv`。", "",
      "## B. 不良事件发生率（B21P 至 B31C）", "",
      "- 规则：内分泌类免疫相关不良事件（甲状腺功能减退、甲状腺功能亢进、肾上腺功能不全、垂体炎、1 型糖尿病）用全部等级，其余用 3 级以上。分母为 as-treated 人群（帕博利珠单抗组 783 例，安慰剂组 389 例）。截点统一为 IA4（2021-03-23）；2024 年正文 Table 2（IA7）中同名项目的例数与 IA4 相同。",
      f"- 主要来源：{SRC_T2} Table 2（正文 p.564）；发热性中性粒细胞减少：{SRC_S7} Table S7（p.27）。",
      f"- 表中没有的项目（大肠炎、肝炎、1 型糖尿病）：{SRC_EMA}（`sources_ae/EMA_keytruda_II0110_assessment.pdf`）。p.97 至 p.100 的 Table 5.3.5.3.3-tnbc3: 30 为图像，全部等级的例数从图像转记（`sources_ae/ema_aeosi_transcribed.csv`）；3 级以上的例数取 p.101 正文（只给出帕博利珠单抗组）。安慰剂组的大肠炎、肝炎 3 级以上未报告，基本值取 0，上限取全部等级的比例。",
      "- 「その他の重篤なもの」（B30）：Table 2 免疫介导不良事件 3 级以上的总人数，减去表中各项目与大肠炎、肝炎的 3 级以上人数。总数按患者计、各项相加会有重复，故为近似；定义需与尾崎的 B10（每件费用）一致，待确认。",
      "- 下限与上限：Clopper-Pearson 95% 置信区间。", "",
      "| param_id | 项目 | 等级 | 例数 / 分母 | 发生率 | 来源 | 位置 | 备注 |", "|---|---|---|---|---|---|---|---|"]
M += [f"| {a['param_id']} | {a['item']} | {a['grade']} | {a['n']}/{a['N']} | {a['rate']:.4f} | {a['source'].split(' (')[0]} | {a['where']} | {a['note']} |" for a in AE]
M += ["", "## U. 效用值（U01 至 U05）", "", "优先顺序：KEYNOTE-522 的 EQ-5D 效用值 → 日本人群研究（日本的价值组）→ 其他费用效用分析。", ""]
if UT:
    M += ["| param_id | 值 | 标准误 | 下限 | 上限 | 层级 | 来源 | 位置 | 原文 | 文件 |", "|---|---|---|---|---|---|---|---|---|---|"]
    M += [f"| {u['param_id']} | {u['value']} | {u['se']} | {u['lower']} | {u['upper']} | {u['tier']} | {u['citation']} | {u['location']} | {u['quote'].replace('|', '/')} | {u['file']} |" for u in UT.values()]
    M += ["", "下限与上限由本脚本按 基本值 ± 1.96 × 标准误 计算（来源只给出标准误）；U05 的下限截于 0。U05 的持续期间："
          + UT["U05"]["duration_weeks"] + " 周（同一来源）。",
          "检索范围与未采用的来源：KEYNOTE-522 的 HRQoL 论文（Dent 2024 JNCI，PMID 38913881）只报告 EQ-5D VAS；NICE TA851 的效用值全部涂黑；CADTH PC0279 的药物经济学评估页面无法取得（reCAPTCHA、403），未绕过；日本没有帕博利珠单抗的 C2H 费用效果评价。日本人群（日本的价值组）的数值只作对照：Iwatani 2021 Curr Oncol（PMID 34677274）原发乳腺癌 0.89 至 0.90；Shiroiwa 2017 BMC Cancer（PMID 29149882）转移乳腺癌一线 0.742 至 0.764；局部区域复发没有日本人的数值。保存的文件在 `input/params/sources_utility/` 与 `input/params/pubmed/`。"]
    M += ["", "选择理由与说明：", ""] + [f"- {u['param_id']}：{u['note']}" for u in UT.values()]
else:
    M += ["（未填写）"]
M += ["", "## 待确认事项", "",
      "- B30「その他の重篤なもの」的定义需与尾崎的 B10（每件费用）一致；现值为近似（见 B 节）。",
      "- 安慰剂组大肠炎、肝炎的 3 级以上例数未报告，基本值取 0（上限为全部等级的比例）。",
      "- U05：来源的分析把效用下降乘以全部 3 级以上不良事件的发生（件数），本模型按规格乘以 B25 至 B28、B30、B31 的发生率之和，两者对象不同。",
      "- 卡铂的情景「酶法肌酐加 0.2 mg/dL」的出处本次未核对。",
      "- 效用值用的是外国的价值组（基准为德国）；没有把日本的价值组用于 KEYNOTE-522 的数值。"]
with open(P("input", "params", "sources_hara.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(M) + "\n")

print(f"BSA {BSA:.4f} m2, CrCl {CRCL:.1f} mL/min (Cr+0.2: {CRCL_ADJ:.1f})")
for c in costs:
    print(f"{c['course']:28s} {c['prices']:10s} {c['total_yen']:>12,.0f}")
print("exposure", ex)
for a in AE:
    print(a["param_id"], a["n"], a["N"], round(a["rate"], 4), a["grade"])
print("filled rows:", len(filled), "->", out_xlsx)
