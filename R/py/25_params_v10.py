"""Internal parameter sheet v9 -> v10 (2026-10-26; docs/analysis_plan_phase2.md section 9, Ozaki's e-mail
of 2026-10-26). Scenario values only: 基本値, 下限 and 上限 of every row stay as in v9 (checked).
  sc_metcost50: D03, D03P, D05 at 50% of 基本値.
  sc_eribulin:  D05 = monthly cost of an eribulin regimen (section 9.4): eribulin mesilate 1.4 mg/m2 on
                days 1 and 8 every 3 weeks (EMBRACE), body surface area as A01/A02 (Du Bois, NHNS R6
                table 14, women 40-49), whole vials per dose (waste included), lowest generic price of
                the MHLW list (rule of A01); administration A04 (基本値) per dose; supportive care as A05:
                antiemetics by the emetic risk of the JSCO guideline 2023 (eribulin: low risk ->
                dexamethasone 6.6 mg i.v. on each day of administration), dexamethasone at the price
                used in A05; no G-CSF (A05 counts it only for AC/EC). Month = 30.4375 / 21 of a cycle.
Writes input/params/parameters_v10.xlsx: column シナリオ値 on the sheet パラメータ (readable text), sheet
シナリオ (one row per scenario x parameter; read by R/22_phase2b_main.R plan9) and sheet 計算根拠_原
(the eribulin calculation, values with the expression and source of each step). v9 is moved to
input/params/archive/ afterwards (git mv).

Usage: .venv/Scripts/python.exe -I R/py/25_params_v10.py <project_root>
"""
import sys, os, re, math, hashlib, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
from copy import copy
from openpyxl import load_workbook

root = sys.argv[1]
P = lambda *a: os.path.join(root, *a)
COLS = ["param_id", "区分", "項目", "適用する群", "適用する状態", "単位", "基本値", "下限", "上限",
        "価格の年度", "出典", "出典の該当箇所", "担当", "備考"]
SC_COL = "シナリオ値"
MAIL = "尾崎 2026-10-26 メール"
nfkc = lambda s: unicodedata.normalize("NFKC", s or "")
sha = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()

src = P("input", "params", "parameters_v9.xlsx")
if not os.path.exists(src):  # moved to archive/ after v10 was made (git mv)
    src = P("input", "params", "archive", "parameters_v9.xlsx")
wb = load_workbook(src)
ws = wb["パラメータ"]
assert [c.value for c in ws[1]] == COLS, [c.value for c in ws[1]]
cm = {h: i + 1 for i, h in enumerate(COLS)}
def row_of(pid):
    hits = [r for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value == pid]
    assert len(hits) == 1, (pid, hits)
    return hits[0]
get = lambda pid, k: ws.cell(row_of(pid), cm[k]).value
before = {ws.cell(r, 1).value: [ws.cell(r, c).value for c in range(1, len(COLS) + 1)] for r in range(2, ws.max_row + 1)}

# ---------------------------------------------------------------- inputs
# body surface area (as in R/py/11_fill_hara_params.py)
nh = [f for f in os.listdir(P("input", "params", "sources_bsa")) if f.startswith("NHNS_R6_2024_table14_")]
assert len(nh) == 1
wn = load_workbook(P("input", "params", "sources_bsa", nh[0]), read_only=True, data_only=True)["14"]
assert wn.cell(37, 1).value == "40-49歳" and wn.cell(6, 8).value == "女性"
HEIGHT, WEIGHT = float(wn.cell(37, 9).value), float(wn.cell(37, 12).value)
BSA = 0.007184 * WEIGHT ** 0.425 * HEIGHT ** 0.725
assert "体表面積 1.555 m2" in get("A01", "備考") and abs(BSA - 1.5552) < 5e-5, BSA

# MHLW price list (the file of A01-A03)
price_file = P("input", "params", "sources_price", "tp20261014-01_02.xlsx")
rows = list(load_workbook(price_file, read_only=True, data_only=True).active.iter_rows(values_only=True))
assert rows[0][2] == "成分名" and rows[0][3] == "規格" and rows[0][7] == "品名" and rows[0][12] == "薬価"
def products(ingredient):
    out = []
    for r in rows[1:]:
        if r[2] == ingredient:
            kind = "generic" if r[9] in ("後発品", "★") else ("originator" if r[10] == "先発品" else "only")
            out.append(dict(spec=nfkc(r[3]), name=nfkc(r[7]), maker=r[8], kind=kind, price=float(r[12]), transitional=r[13] or ""))
    return out
eri = products("エリブリンメシル酸塩")
assert {p["spec"] for p in eri} == {"1mg2mL1瓶"}, eri          # one strength only: 1 mg vials
gen = sorted([p for p in eri if p["kind"] == "generic"], key=lambda p: (p["price"], p["transitional"] != ""))
org = [p for p in eri if p["kind"] == "originator"]
assert gen and len(org) == 1
VIAL = gen[0]
dex = [p for p in products("デキサメタゾンリン酸エステルナトリウム") if p["name"] == "デキサート注射液6.6mg"]
assert len(dex) == 1

# A05: the dexamethasone price used there (Ozaki's calculation sheet, row "デキサート注6.6mg")
wo = load_workbook(P("input", "params", "ozaki", "parameters_v1_尾崎記入案.xlsx"), data_only=True)["計算根拠_尾崎"]
dex_a05 = [r[1] for r in wo.iter_rows(min_row=1, values_only=True) if r[0] == "デキサート注6.6mg"]
assert dex_a05 == [dex[0]["price"]], (dex_a05, dex[0]["price"])          # 197 yen in both
peg = [r[1] for r in wo.iter_rows(min_row=1, values_only=True) if r[0] == "ペグフィルグラスチムBS 3.6mg「ニプロ」"]
assert len(peg) == 1
A04 = float(get("A04", "基本値"))
DAYS_MONTH = [r[1] for r in wo.iter_rows(min_row=1, values_only=True) if r[0] == "1か月の日数"]
assert DAYS_MONTH == [30.4375]
MONTH = DAYS_MONTH[0] / 21

# ---------------------------------------------------------------- eribulin regimen (section 9.4)
DOSE_M2, N_ADMIN = 1.4, 2
dose = DOSE_M2 * BSA
vials = math.ceil(dose / 1.0 - 1e-9)
drug_admin = vials * VIAL["price"]
drug_cycle = N_ADMIN * drug_admin
admin_cycle = N_ADMIN * A04
supp_cycle = N_ADMIN * dex[0]["price"]
cycle = drug_cycle + admin_cycle + supp_cycle
D05_ERI = cycle * MONTH
peg_month = peg[0] * MONTH                                                  # reference only (not used)
org_month = (N_ADMIN * vials * org[0]["price"] + admin_cycle + supp_cycle) * MONTH   # reference only
print(f"BSA {BSA:.4f} m2, dose {dose:.4f} mg -> {vials} x 1 mg vials of {VIAL['name']} ({VIAL['price']:,.0f} yen)")
print(f"per cycle: drug {drug_cycle:,.0f} + administration {admin_cycle:,.0f} + supportive {supp_cycle:,.0f} = {cycle:,.0f}")
print(f"D05 (sc_eribulin) = {cycle:,.0f} x 30.4375 / 21 = {D05_ERI:,.4f} yen/month")

# ---------------------------------------------------------------- scenario values
base = {pid: float(get(pid, "基本値")) for pid in ("D03", "D03P", "D05")}
SC = [("sc_metcost50", pid, base[pid] * 0.5, 0.5,
       f"{MAIL}：転移再発の治療費（一次治療 D03、D03P と二次治療以降 D05）を基本値の 50% とするシナリオ。")
      for pid in ("D03", "D03P", "D05")]
SC.append(("sc_eribulin", "D05", D05_ERI, D05_ERI / base["D05"],
           f"{MAIL}：二次治療以降をエリブリン中心のレジメンとするシナリオ（D03、D03P は基本値のまま）。計算はシート「計算根拠_原」。"))
sc_label = {"sc_metcost50": "転移再発の治療費 50%", "sc_eribulin": "エリブリン中心"}

# column シナリオ値 on パラメータ
c_new = len(COLS) + 1
ws.cell(1, c_new).value = SC_COL
ws.cell(1, c_new)._style = copy(ws.cell(1, len(COLS))._style)
ws.column_dimensions[ws.cell(1, c_new).column_letter].width = 60
for pid in ("D03", "D03P", "D05"):
    txt = "；".join(f"{s}（{sc_label[s]}）：{v:,.2f} 円/月（基本値の {100 * f:.1f}%）" for s, p, v, f, _ in SC if p == pid)
    r = row_of(pid)
    ws.cell(r, c_new).value = txt + "。分析計画第 9 節のシナリオでだけ使う（基本値と幅は変えない）。"
    ws.cell(r, c_new)._style = copy(ws.cell(r, len(COLS))._style)

# sheet シナリオ
ss = wb.create_sheet("シナリオ")
ss.append(["シナリオ", "param_id", "項目", "基本値", "シナリオ値", "倍率（シナリオ値 ÷ 基本値）", "単位", "根拠"])
for s, pid, v, f, why in SC:
    ss.append([s, pid, get(pid, "項目"), base[pid], v, f, get(pid, "単位"), why])
for col, w in zip("ABCDEFGH", (14, 9, 40, 16, 16, 14, 10, 90)):
    ss.column_dimensions[col].width = w

# sheet 計算根拠_原
ACC = "2026-10-26 取得"
akita = P("input", "params", "sources_supportive", "Akita_antiemetic_guideline_v4_202403.pdf")
AKITA = ("秋田大学医学部附属病院 制吐薬使用ガイドライン 第4版（2024年3月、日本癌治療学会 制吐薬適正使用ガイドライン 2023年10月改訂 第3版を元に作成）"
         f"https://www.hos.akita-u.ac.jp/onco/files/antiemetic-drug-guidelines-4rd-mar-2024.pdf（{ACC}、sha256 {sha(akita)[:16]}…）")
PRICE = (f"厚生労働省 薬価基準収載品目リスト（注射薬）{os.path.basename(price_file)}（令和8年10月14日収載品目反映版、"
         f"令和8年4月1日以降の薬価、sha256 {sha(price_file)[:16]}…）")
sk = wb.create_sheet("計算根拠_原")
sk.append(["計算根拠（原担当：シナリオ sc_eribulin の D05、2026-10-26）"])
sk.append(["数値は R/py/25_params_v10.py が下記の資料から計算した値（手入力なし）。式の列は計算の過程。"])
sk.append([])
sk.append(["項目", "値", "単位", "式", "出典・根拠"])
def kv(item, val, unit, expr, srcs):
    sk.append([item, val, unit, expr, srcs])
kv("用法", "1.4 mg/m2、第1・8日、3週ごと", None, None,
   "Cortes J, et al. Lancet 2011;377:914-23（EMBRACE、PMID 21376385）：eribulin mesilate 1.4 mg/m2 on days 1 and 8 of a 21-day cycle")
kv("身長（女性 40-49歳の平均）", HEIGHT, "cm", None, f"令和6年国民健康・栄養調査 第14表（{nh[0]}、I37）")
kv("体重（同）", WEIGHT, "kg", None, f"同（L37）")
kv("体表面積", round(BSA, 4), "m2", "0.007184 × 体重^0.425 × 身長^0.725（Du Bois）", "A01、A02 と同じ")
kv("1回の投与量", round(dose, 4), "mg", "1.4 × 体表面積", None)
kv("1回の瓶数（1 mg 瓶、切り上げ・残量は廃棄）", vials, "瓶", "ceil(1回の投与量 ÷ 1 mg)", f"エリブリンメシル酸塩の規格は 1mg2mL1瓶 のみ（{PRICE}）")
kv(f"エリブリン 1 mg 瓶の薬価（後発品の最低薬価：{VIAL['name']}、{VIAL['maker']}）", VIAL["price"], "円/瓶", None,
   f"{PRICE}。規則は A01 と同じ（後発品があれば後発品の最低薬価）")
for p in eri:
    if p is not VIAL:
        kv(f"参考：{p['name']}（{p['maker']}、{'後発品' if p['kind'] == 'generic' else '先発品'}）", p["price"], "円/瓶", None, "同上（使わない）")
kv("薬剤費（1サイクル）", drug_cycle, "円", f"{N_ADMIN} 回 × {vials} 瓶 × {VIAL['price']:,.0f}", None)
kv("投与費用（1サイクル）", admin_cycle, "円", f"{N_ADMIN} 回 × A04 基本値 {A04:,.0f}", "A04（外来での投与1回あたり）と同じ口径。尾崎先生の D05 の計算も投与1回ごとに A04 を加算")
kv("エリブリンの催吐性リスク", "軽度（催吐頻度 10〜30%）", None, None, f"{AKITA}、PDF p.6（スライド番号 5）注射抗がん薬の催吐性リスク分類；p.9（同 8）乳がん：軽度リスク エリブリン")
kv("軽度リスク（注射薬）の制吐療法", "デキサメタゾン 6.6 mg（3.3 mg）静注、Day 1", None, None, f"{AKITA}、PDF p.5（スライド番号 4）")
kv("デキサート注射液 6.6 mg の薬価", dex[0]["price"], "円/瓶", None, f"{PRICE}（後発品）。A05（尾崎先生の計算根拠「デキサート注6.6mg」）と同じ値")
kv("支持療法（1サイクル）", supp_cycle, "円", f"{N_ADMIN} 回 × {dex[0]['price']:,.0f}（投与日ごとに 6.6 mg を 1 瓶）", "A05 と同じ口径（ガイドラインの催吐性リスクで制吐薬を選ぶ）")
kv("G-CSF", 0, "円", None,
   "計上しない。A05 で G-CSF（ペグフィルグラスチム）を計上したのは AC/EC（dose-dense）だけで、A05 の下限も G-CSF なし。"
   "エリブリン単剤の発熱性好中球減少症は EMBRACE で約 5%（米国添付文書などの二次資料による。原著本文は未照合）")
kv("参考：毎サイクルにペグフィルグラスチムを加えた場合の月額の増分（使わない）", round(peg_month, 2), "円/月", f"{peg[0]:,.0f} × 30.4375 / 21", "A05 のペグフィルグラスチム BS の薬価")
kv("1サイクル（3週）の費用", cycle, "円", "薬剤費 + 投与費用 + 支持療法", None)
kv("1か月の日数", DAYS_MONTH[0], "日", None, "尾崎先生の計算根拠と同じ月換算")
kv("D05 シナリオ値（sc_eribulin）", round(D05_ERI, 4), "円/月", "1サイクルの費用 × 30.4375 / 21", None)
kv("参考：先発品（ハラヴェン）の薬価で計算した場合（使わない）", round(org_month, 2), "円/月", None, "同上の計算で瓶の薬価だけ先発品")
kv("参考：D05 の基本値（T-DXd 32%、サシツズマブ ゴビテカン 68%）", base["D05"], "円/月", None, "尾崎先生（立花先生の回答）。基本値と幅は変えない")
oz201 = [r[1] for r in wo.iter_rows(min_row=1, values_only=True) if r[0] == "D05 下限（SG後をエリブリンとした場合）"]
assert len(oz201) == 1
kv("参考：尾崎先生の計算根拠の「D05 下限（SG後をエリブリンとした場合）」（使わない）", round(oz201[0], 2), "円/月", None,
   "計算根拠_尾崎 B201：T-DXd 32% ＋ エリブリン 68%、投与費用のみ加算。T-DXd を含む構成で、本シナリオ（エリブリン中心）とは別")
for col, w in zip("ABCDE", (58, 22, 10, 40, 110)):
    sk.column_dimensions[col].width = w

# checks: 基本値, 下限, 上限 and the other 14 columns unchanged
for r in range(2, ws.max_row + 1):
    pid = ws.cell(r, 1).value
    assert [ws.cell(r, c).value for c in range(1, len(COLS) + 1)] == before[pid], pid
assert ws.max_row - 1 == len(before)
out = P("input", "params", "parameters_v10.xlsx")
wb.save(out)
print(f"{os.path.basename(src)} -> {os.path.basename(out)}: column {SC_COL}, sheets シナリオ ({len(SC)} rows) and 計算根拠_原")
for s, pid, v, f, _ in SC:
    print(f"  {s:13s} {pid:5s} {base[pid]:>16,.2f} -> {v:>16,.2f}  (x {f:.6f})")
