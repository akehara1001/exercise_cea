"""Parameter input sheet v1 (Japanese, for Dr Ozaki) and the efficacy-source note.

Usage: python -I R/py/09_make_params_template.py <project_root>
Writes input/params/parameters_template_v1.xlsx (refuses to overwrite an existing file, which
may already hold entries) and input/params/efficacy_sources.md. The hazard ratios for F07/F08
are read by regex from the PubMed abstracts saved in input/params/pubmed/.
"""
import sys, os, re
sys.stdout.reconfigure(encoding="utf-8")
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

root = sys.argv[1]
pdir = os.path.join(root, "input", "params")
out_xlsx = os.path.join(pdir, "parameters_template_v1.xlsx")
# an existing sheet may hold entries: never overwrite; v1 is archived once v2 exists
write_xlsx = not any(os.path.exists(x) for x in [out_xlsx, os.path.join(pdir, "archive", "parameters_template_v1.xlsx"),
                                                 os.path.join(pdir, "parameters_v2.xlsx")])

# ---------------------------------------------------------------- efficacy (F07, F08)
def abstract(pmid):
    t = open(os.path.join(pdir, "pubmed", f"PMID{pmid}.txt"), encoding="utf-8").read()
    return re.sub(r"\s+", " ", t)

cx = abstract("28564564")
m = re.search(r"Among patients with triple-negative disease, the rate of disease-free survival was ([\d.]+)% in the "
              r"capecitabine group versus ([\d.]+)% in the control group \(hazard ratio for recurrence, second cancer, "
              r"or death, ([\d.]+); 95% CI, ([\d.]+) to ([\d.]+)\)", cx)
F07 = dict(hr=float(m.group(3)), lo=float(m.group(4)), hi=float(m.group(5)), quote=m.group(0), pmid="28564564",
           cite="Masuda N, et al. 2017. N Engl J Med 376:2147-59. DOI 10.1056/NEJMoa1612645",
           where="Abstract, Results（TNBC サブグループ、DFS）")
ol3 = abstract("42636977")
m = re.search(r"Olaparib benefits were maintained in IDFS \(HR ([\d.]+), 95% CI ([\d.]+)-([\d.]+)\)", ol3)
F08 = dict(hr=float(m.group(1)), lo=float(m.group(2)), hi=float(m.group(3)), quote=m.group(0), pmid="42636977",
           cite="Garber JE, et al. 2026. Ann Oncol (online ahead of print). DOI 10.1016/j.annonc.2026.08.002",
           where="Abstract, Results（第3回中間解析、追跡期間中央値6.1年、IDFS）")
ol1 = abstract("34081848")
m = re.search(r"hazard ratio for invasive disease or death, ([\d.]+); 99\.5% CI, ([\d.]+) to ([\d.]+)", ol1)
F08_first = dict(hr=float(m.group(1)), lo=float(m.group(2)), hi=float(m.group(3)), quote=m.group(0))

# ---------------------------------------------------------------- rows
ALL = "全群"
PEM = "ペムブロリズマブを含む群"
NOPEM = "ペムブロリズマブを含まない群"
EX = "運動を含む群"
rows = []
def r(pid, cat, item, arm, state, unit, owner, **kw):
    rows.append(dict(param_id=pid, 区分=cat, 項目=item, 適用する群=arm, 適用する状態=state, 単位=unit, 担当=owner, **kw))

A = "A 術前と術後の全身治療"
r("A01", A, "パクリタキセル＋カルボプラチン（12週）の薬剤費", ALL, "術前治療期", "円（12週の総額）", "原")
r("A02", A, "AC または EC（4サイクル）の薬剤費", ALL, "術前治療期", "円（4サイクルの総額）", "原")
r("A03", A, "ペムブロリズマブの1回あたり薬剤費", PEM, "術前治療期と術後治療期", "円/回", "原")
r("A04", A, "外来での投与にかかる費用（加算と検査を含む、1回あたり）", ALL, "術前治療期と術後治療期", "円/回", "尾崎")
r("A05", A, "支持療法（G-CSF、制吐薬など、1サイクルあたり）", ALL, "術前治療期", "円/サイクル", "尾崎")
r("A06", A, "手術の費用（術式の構成は備考に）", ALL, "手術時", "円/件", "尾崎")
r("A07", A, "術後放射線療法の実施割合", ALL, "手術後", "割合（0から1）", "尾崎")
r("A08", A, "術後放射線療法の費用", ALL, "手術後", "円/件（1コースの総額）", "尾崎")
B = "B 有害事象"
aes = ["甲状腺機能低下症", "甲状腺機能亢進症", "副腎不全", "下垂体炎", "肺臓炎", "大腸炎", "肝炎",
       "重度の皮膚障害", "1型糖尿病", "その他の重篤なもの"]
for i, ae in enumerate(aes, start=1):
    r(f"B{i:02d}", B, f"免疫関連有害事象の1件あたり管理費用（{ae}）", ALL, "術前治療期と術後治療期", "円/件", "尾崎")
r("B11", B, "発熱性好中球減少症の1件あたり管理費用", ALL, "術前治療期", "円/件", "尾崎")
for i, ae in enumerate(aes + ["発熱性好中球減少症"], start=21):
    name = f"免疫関連有害事象（{ae}）の発現率" if i <= 30 else f"{ae}の発現率"
    r(f"B{i}P", B, name, PEM, "術前治療期と術後治療期", "割合（0から1）", "原",
      備考=f"B{i - 20:02d} に対応（KEYNOTE-522 のペムブロリズマブ群）")
    r(f"B{i}C", B, name, NOPEM, "術前治療期と術後治療期", "割合（0から1）", "原",
      備考=f"B{i - 20:02d} に対応（KEYNOTE-522 のプラセボ群）")
C = "C 経過観察"
r("C01", C, "1〜2年目の年間費用", ALL, "無事件", "円/年", "尾崎")
r("C02", C, "3〜5年目の年間費用", ALL, "無事件", "円/年", "尾崎")
r("C03", C, "6年目以降の年間費用", ALL, "無事件", "円/年", "尾崎")
D = "D 再発後"
r("D01", D, "局所領域再発の治療（一時費用）", ALL, "局所領域再発", "円/件", "尾崎")
r("D02", D, "局所領域再発後の月額", ALL, "局所領域再発", "円/月", "尾崎")
r("D03", D, "遠隔再発の一次治療の月額（レジメンの構成と割合は備考に）", ALL, "遠隔再発", "円/月", "尾崎")
r("D04", D, "一次治療の平均継続期間（月）", ALL, "遠隔再発", "月", "尾崎")
r("D05", D, "二次治療以降の月額", ALL, "遠隔再発", "円/月", "尾崎")
r("D06", D, "死亡前3か月の終末期医療費", ALL, "死亡前3か月", "円（3か月の総額）", "尾崎")
E = "E 運動プログラム"
r("E01", E, "想定1 CHALLENGE 相当の円換算（NAC中6か月の総額）", EX, "術前治療期", "円（6か月の総額）", "尾崎")
r("E02", E, "想定2 リハビリの点数に準じた額（NAC中6か月の総額）", EX, "術前治療期", "円（6か月の総額）", "尾崎")
r("E03", E, "想定3 遠隔指導の低価格版（NAC中6か月の総額）", EX, "術前治療期", "円（6か月の総額）", "尾崎")
r("E04", E, "術後も続ける場合の月額", EX, "手術後", "円/月", "尾崎")
r("E05", E, "術後も続ける期間（月）", EX, "手術後", "月", "尾崎")
F = "F 日本の術後治療シナリオ"
r("F01", F, "化学療法のみの群の non-pCR 例でのカペシタビン使用割合", NOPEM, "non-pCR 例の術後", "割合（0から1）", "尾崎")
r("F02", F, "カペシタビンの費用（全期間）", NOPEM, "non-pCR 例の術後", "円/人", "尾崎")
r("F03", F, "TNBC での gBRCA 陽性割合", ALL, "診断時", "割合（0から1）", "尾崎")
r("F04", F, "gBRCA 陽性例でのオラパリブ使用割合", NOPEM, "non-pCR 例の術後", "割合（0から1）", "尾崎")
r("F05", F, "オラパリブの費用（全期間）", NOPEM, "non-pCR 例の術後", "円/人", "尾崎")
r("F06", F, "BRCA 検査の費用", ALL, "診断時", "円/件", "尾崎")
r("F07", F, "カペシタビンの HR", NOPEM, "non-pCR 例の術後", "ハザード比", "原",
  基本値=F07["hr"], 下限=F07["lo"], 上限=F07["hi"], 出典=F07["cite"], 出典の該当箇所=F07["where"],
  備考="CREATE-X の TNBC サブグループ。下限と上限は95%信頼区間")
r("F08", F, "オラパリブの HR", NOPEM, "non-pCR 例の術後", "ハザード比", "原",
  基本値=F08["hr"], 下限=F08["lo"], 上限=F08["hi"], 出典=F08["cite"], 出典の該当箇所=F08["where"],
  備考=(f"OlympiA の全体集団（ホルモン受容体陽性を含む）。下限と上限は95%信頼区間。初回解析では HR {F08_first['hr']}"
        f"（99.5%信頼区間 {F08_first['lo']} から {F08_first['hi']}、PMID 34081848）"))
U = "U 効用値"
r("U01", U, "無事件（治療中）", ALL, "無事件（治療中）", "効用値（0から1）", "原")
r("U02", U, "無事件（治療終了後）", ALL, "無事件（治療終了後）", "効用値（0から1）", "原")
r("U03", U, "局所領域再発", ALL, "局所領域再発", "効用値（0から1）", "原")
r("U04", U, "遠隔再発", ALL, "遠隔再発", "効用値（0から1）", "原")
r("U05", U, "重篤な有害事象による一時的な低下", ALL, "有害事象の発現時", "効用値の低下幅（期間は備考に）", "原")

cols = ["param_id", "区分", "項目", "適用する群", "適用する状態", "単位", "基本値", "下限", "上限", "価格の年度",
        "出典", "出典の該当箇所", "担当", "備考"]

guide = [
    ("この表について", "経済評価モデルに入れる費用、割合、効用値などを1行1項目で集める表です。"),
    ("記入する行", "担当が尾崎の行だけを記入してください。担当が原の行はこちらで記入します。"),
    ("記入する欄", "基本値、下限、上限、価格の年度、出典、出典の該当箇所、備考の各欄です。param_id から単位までの欄と担当の欄は変えないでください。"),
    ("金額", "金額は円で記入してください。"),
    ("価格の年度", "価格は令和8年度の薬価基準と診療報酬を基本とし、用いた年度を価格の年度の欄に書いてください。"),
    ("点数で書く場合", "診療報酬の点数をもとにした場合は、区分番号を出典の該当箇所の欄に書いてください（基本値は円に換算して記入）。"),
    ("下限と上限", "分からなければ空欄でかまいません。こちらで幅を置きます。"),
    ("出典", "文献なら著者、年、誌名、DOI を、点数表なら区分番号を書いてください。"),
    ("分からない項目", "空欄のままにして、備考の欄に一言書いてください。"),
    ("確率分布", "確率分布はこちらで設定します（費用はガンマ分布、割合と効用値はベータ分布、ハザード比は対数正規分布。パラメータは下限と上限から求めます）。記入は不要です。"),
]
col_help = [
    ("param_id", "項目の番号です。"), ("区分", "項目のまとまりです。"), ("項目", "記入していただく内容です。"),
    ("適用する群", "その値を使う群です。"), ("適用する状態", "その値を使うモデル上の時期または状態です。"),
    ("単位", "基本値、下限、上限の単位です。"), ("基本値", "モデルで用いる値です。"),
    ("下限", "幅の下側の値です（分からなければ空欄）。"), ("上限", "幅の上側の値です（分からなければ空欄）。"),
    ("価格の年度", "価格の根拠とした年度です（例 令和8年度）。"), ("出典", "根拠となる文献または点数表です。"),
    ("出典の該当箇所", "表番号、ページ、区分番号などです。"), ("担当", "記入する人です（尾崎 または 原）。"),
    ("備考", "補足、前提、分からない理由などです。"),
]

# no middle dots anywhere
for txt in [str(v) for row in rows for v in row.values()] + cols + [x for g in guide for x in g] + [x for g in col_help for x in g]:
    if "・" in txt or "･" in txt:
        raise ValueError(f"middle dot in: {txt}")

if not write_xlsx:
    print(f"{out_xlsx} exists; not overwritten")
wb = Workbook()
ws = wb.active
ws.title = "パラメータ"
ws.append(cols)
for row in rows:
    ws.append([row.get(c, None) for c in cols])
thin = Side(style="thin", color="BFBFBF")
hdr_fill = PatternFill("solid", fgColor="DDEBF7")
ozaki_fill = PatternFill("solid", fgColor="FFF2CC")
for c in ws[1]:
    c.font = Font(bold=True)
    c.fill = hdr_fill
    c.alignment = Alignment(vertical="center", wrap_text=True)
widths = dict(param_id=9, 区分=22, 項目=46, 適用する群=22, 適用する状態=20, 単位=22, 基本値=12, 下限=10, 上限=10,
              価格の年度=12, 出典=36, 出典の該当箇所=24, 担当=8, 備考=40)
for i, c in enumerate(cols, start=1):
    ws.column_dimensions[ws.cell(1, i).column_letter].width = widths[c]
owner_col = cols.index("担当") + 1
for rr in range(2, ws.max_row + 1):
    for cc in range(1, len(cols) + 1):
        cell = ws.cell(rr, cc)
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        cell.border = Border(top=thin, bottom=thin, left=thin, right=thin)
    if ws.cell(rr, owner_col).value == "尾崎":
        for cc in range(cols.index("基本値") + 1, len(cols) + 1):
            if cc != owner_col:
                ws.cell(rr, cc).fill = ozaki_fill
ws.freeze_panes = "D2"
dv = DataValidation(type="list", formula1='"尾崎,原"', allow_blank=False, showDropDown=False)
dv.error = "尾崎 または 原 を選んでください"
dv.errorTitle = "担当"
ws.add_data_validation(dv)
col_letter = ws.cell(1, owner_col).column_letter
dv.add(f"{col_letter}2:{col_letter}{ws.max_row}")
ws.auto_filter.ref = f"A1:{ws.cell(1, len(cols)).column_letter}{ws.max_row}"

g = wb.create_sheet("記入の手引き")
g.append(["記入の手引き", ""])
g["A1"].font = Font(bold=True, size=12)
g.append(["", ""])
for k, v in guide:
    g.append([k, v])
g.append(["", ""])
g.append(["各欄の意味", ""])
g.cell(g.max_row, 1).font = Font(bold=True)
for k, v in col_help:
    g.append([k, v])
g.append(["", ""])
g.append(["色", "黄色の欄が尾崎先生に記入をお願いする欄です。"])
g.column_dimensions["A"].width = 18
g.column_dimensions["B"].width = 100
for rr in range(1, g.max_row + 1):
    for cc in (1, 2):
        g.cell(rr, cc).alignment = Alignment(vertical="top", wrap_text=True)
    if g.cell(rr, 1).value in [k for k, _ in guide]:
        g.cell(rr, 1).font = Font(bold=True)
if write_xlsx:
    wb.save(out_xlsx)
    print(f"wrote {out_xlsx}: {len(rows)} rows ({sum(r['担当'] == '尾崎' for r in rows)} 尾崎, {sum(r['担当'] == '原' for r in rows)} 原)")

# ---------------------------------------------------------------- efficacy_sources.md
md = f"""# 疗效 HR 来源（入力表 F07、F08）

由 `R/py/09_make_params_template.py` 从 `input/params/pubmed/` 中保存的 PubMed 摘要用正则抽取后写入入力表。摘要于 2026-10-21 经 NCBI E-utilities（efetch）取得。

## F07 卡培他滨（CREATE-X，TNBC 亚组）

- PMID：{F07['pmid']}
- 文献：{F07['cite']}
- 终点：DFS（复发、第二癌或死亡）
- HR {F07['hr']}，95% CI {F07['lo']} 至 {F07['hi']}
- 摘要原文：“{F07['quote']}”

## F08 奥拉帕利（OlympiA，iDFS）

- PMID：{F08['pmid']}（第三次中期分析，中位随访 6.1 年，在线先行发表）
- 文献：{F08['cite']}
- 终点：iDFS，分层 Cox 模型
- HR {F08['hr']}，95% CI {F08['lo']} 至 {F08['hi']}
- 摘要原文：“{F08['quote']}”
- 选用理由：任务要求记录 95% CI；首次分析（PMID 34081848，Tutt 2021 NEJM）摘要只给出 99.5% CI：HR {F08_first['hr']}（99.5% CI {F08_first['lo']} 至 {F08_first['hi']}）。第二次中期分析（PMID 36228963，Geyer 2022 Ann Oncol）摘要未给出 iDFS HR。
- 注意：OlympiA 全体人群含激素受体阳性患者，摘要中没有 TNBC 单独的 HR；入组为 gBRCA 致病变异且高危的 HER2 阴性早期乳腺癌，新辅助后 non-pCR 只是其中一部分。
"""
open(os.path.join(pdir, "efficacy_sources.md"), "w", encoding="utf-8").write(md)
print("wrote efficacy_sources.md")
