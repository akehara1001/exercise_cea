"""Internal parameter sheet v6 -> v7 (2026-10-25, user instruction): Ozaki's values taken in.
Source: input/params/ozaki/parameters_v1_尾崎記入案.xlsx (sheet パラメータ; his v1 with six rows appended:
D03P, D04P, F01P, F04P, X01, X02). Cells that are formulas on his sheet 計算根拠_尾崎 are read as the
cached values (openpyxl data_only); the script stops if any cached value is missing (then recalculate
with LibreOffice headless first).
Checks (the script stops on any failure): F01, F01P, F04, F04P against his e-mail of 2026-10-25;
下限 <= 基本値 <= 上限; proportions in [0, 1]; amounts and durations positive; every row he filled
is either a row of his in v6, a new row (D03P, D04P), or mapped (X02 -> E08; X01 checked against
E06 - E07 and not entered).
Rows owned by 尾崎: 基本値 to 備考 copied from his sheet (項目 and 適用する群 stay as in v6, except
D03 and D04, now the groups without pembrolizumab). New rows D03P, D04P after D03 and D04 (groups with
pembrolizumab: no immunotherapy after recurrence). Ranges he left blank are set here
(docs/model_spec.md section 6): both blank -> 基本値 +-25% (proportions truncated to [0, 1]); one blank
-> mirrored about 基本値. Our additions to 備考 start with 【原 2026-10-25】.
Writes input/params/parameters_v7.xlsx and output/params_ozaki_v1_review.md; v6 is moved to
input/params/archive/ afterwards (git mv).

Usage: .venv/Scripts/python.exe -I R/py/22_params_v7.py <project_root>
"""
import sys, os, re
from copy import copy
sys.stdout.reconfigure(encoding="utf-8")
from openpyxl import load_workbook
from openpyxl.worksheet.cell_range import MultiCellRange

root = sys.argv[1]
P = lambda *a: os.path.join(root, *a)
COLS = ["param_id", "区分", "項目", "適用する群", "適用する状態", "単位", "基本値", "下限", "上限",
        "価格の年度", "出典", "出典の該当箇所", "担当", "備考"]
INPUT_COLS = ["基本値", "下限", "上限", "価格の年度", "出典", "出典の該当箇所", "備考"]
OZ_FILE = P("input", "params", "ozaki", "parameters_v1_尾崎記入案.xlsx")
G_NO_PEMBRO = "化学療法のみの群（運動を加えた群を含む）"
G_PEMBRO = "ペムブロリズマブを含む群（運動を加えた群を含む）"
TAG = "【原 2026-10-25】"
EMAIL = {"F01": (0.85, 0.80, 0.90), "F01P": (0.5, 0.05, 0.90), "F04": (0.9, 0.7, 1.0), "F04P": (0.9, 0.5, 1.0)}
NEW = {"D03P": "D03", "D04P": "D04"}      # new row -> the row it follows
MAP = {"X02": "E08"}                      # appended row -> internal row
CHECK_ONLY = {"X01"}                      # appended row checked against E06 - E07, not entered
NOTES = {  # our additions, besides the range and 【要確認】 notes
    "F01": "v1 の項目名は旧定義だが、値は gBRCA 陰性の non-pCR 例での割合（新定義）であることを確認済み（尾崎 2026-10-25 メール）。",
    "D03": "適用する群を化学療法のみの群に変更（ペムブロリズマブを含む群は D03P）。",
    "D04": "適用する群を化学療法のみの群に変更（ペムブロリズマブを含む群は D04P）。",
    "D05": "ペムブロリズマブの有無によらず両群共通（群別の値は D03、D04 だけ）。",
    "D03P": "尾崎先生の追加行。ペムブロリズマブを含む群では再発後に免疫療法を使わないため、化学療法のみの群（D03）と分けた。",
    "D04P": "尾崎先生の追加行。ペムブロリズマブを含む群では再発後に免疫療法を使わないため、化学療法のみの群（D04）と分けた。",
    "E08": "尾崎先生の記入案 v1 の追加行 X02（筋骨格系有害事象の1件あたり管理費用）の値。",
    "F02": "群によらず共通の値として使用（ペムブロリズマブを含む群にも同じ値）。",
    "F05": "群によらず共通の値として使用（ペムブロリズマブを含む群にも同じ値）。",
    "F06": "診断時に全例で検査する前提（全群）。",
}
PROVISIONAL = "暫定値（尾崎先生の【要確認】のまま使用）。"


def col_of(ws):
    hdr = [c.value for c in ws[1]]
    assert hdr == COLS, hdr
    return {h: i + 1 for i, h in enumerate(hdr)}


def rows_of(ws):
    cm = col_of(ws)
    out = {}
    for r in range(2, ws.max_row + 1):
        pid = ws.cell(r, 1).value
        if pid is None:
            continue
        assert pid not in out, pid
        out[pid] = {k: ws.cell(r, cm[k]).value for k in COLS}
    return out


def row_of(ws, pid):
    hits = [r for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value == pid]
    assert len(hits) == 1, (pid, hits)
    return hits[0]


def copy_style(ws, src_row, dst_row):
    for c in range(1, len(COLS) + 1):
        s, d = ws.cell(src_row, c), ws.cell(dst_row, c)
        d.font, d.fill, d.border = copy(s.font), copy(s.fill), copy(s.border)
        d.alignment, d.number_format, d.protection = copy(s.alignment), s.number_format, copy(s.protection)


blank = lambda v: v is None or (isinstance(v, str) and v.strip() == "")
is_prop = lambda unit: unit.startswith("割合")
is_pos = lambda unit: unit.startswith("円") or unit.startswith("月")


def fmt(v):
    if blank(v):
        return "（空欄）"
    if abs(v) >= 1000:
        return f"{v:,.2f}".rstrip("0").rstrip(".")
    return f"{v:.6g}"


# --- 1. Ozaki's sheet: cached values of the formulas ---
wv = load_workbook(OZ_FILE, data_only=True)
wf = load_workbook(OZ_FILE, data_only=False)
assert wv.sheetnames == ["パラメータ", "記入の手引き", "計算根拠_尾崎"], wv.sheetnames
n_formula, missing = {}, []
for name in wv.sheetnames:
    sf, sv = wf[name], wv[name]
    n = 0
    for row in sf.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("="):
                n += 1
                if sv[c.coordinate].value is None:
                    missing.append(f"{name}!{c.coordinate}")
    n_formula[name] = n
if missing:
    sys.exit("cached values missing (recalculate with LibreOffice headless): " + ", ".join(missing[:20]))
print("formula cells with cached values:", n_formula)
saved_by = re.search(r"<Application>(.*?)</Application>", __import__("zipfile").ZipFile(OZ_FILE).read("docProps/app.xml").decode("utf-8")).group(1)
# the formulas of パラメータ (=計算根拠_尾崎!Bn, optionally times a constant) recomputed from the cached cells
n_recomp, not_parsed = 0, []
for row in wf["パラメータ"].iter_rows():
    for c in row:
        if isinstance(c.value, str) and c.value.startswith("="):
            m = re.fullmatch(r"=計算根拠_尾崎!([A-Z]+\d+)(?:\*([\d.]+))?", c.value)
            if not m:
                not_parsed.append(c.coordinate); continue
            v = wv["計算根拠_尾崎"][m.group(1)].value * (float(m.group(2)) if m.group(2) else 1)
            assert abs(v - wv["パラメータ"][c.coordinate].value) <= 1e-9 * max(1, abs(v)), (c.coordinate, c.value)
            n_recomp += 1
print(f"saved by {saved_by}; formulas of パラメータ recomputed from the cached cells: {n_recomp}, not parsed: {not_parsed}")
oz = rows_of(wv["パラメータ"])
oz_ids = [k for k, r in oz.items() if r["担当"] == "尾崎"]
form = rows_of(wf["パラメータ"])
formula_cells = {pid: [k for k in ("基本値", "下限", "上限") if isinstance(form[pid][k], str) and form[pid][k].startswith("=")]
                 for pid in oz_ids}
assert len(oz_ids) == 42, len(oz_ids)
for pid in oz_ids:
    for k in ("基本値", "下限", "上限"):
        assert blank(oz[pid][k]) or isinstance(oz[pid][k], (int, float)), (pid, k, oz[pid][k])
    assert not blank(oz[pid]["基本値"]) and not blank(oz[pid]["出典"]), pid

# rows of 原 and the columns not to be changed: as in the delivered v1
tpl = rows_of(load_workbook(P("input", "params", "archive", "parameters_template_v1.xlsx"))["パラメータ"])
norm = lambda v: "" if blank(v) else str(v).strip()
hara_changed = [k for k, r in tpl.items() if r["担当"] == "原" and any(norm(r[c]) != norm(oz[k][c]) for c in INPUT_COLS)]
meta_changed = [k for k, r in tpl.items() if any(norm(r[c]) != norm(oz[k][c]) for c in COLS if c not in INPUT_COLS)]
appended = [k for k in oz if k not in tpl]
assert set(tpl) <= set(oz), sorted(set(tpl) - set(oz))
print("rows of 原 changed:", hara_changed, "; fixed columns changed:", meta_changed, "; appended:", appended)
assert not hara_changed and not meta_changed and appended == ["D03P", "D04P", "F01P", "F04P", "X01", "X02"], (hara_changed, meta_changed, appended)

# --- 2. e-mail of 2026-10-25 ---
email_rows = []
for pid, (b, lo, hi) in EMAIL.items():
    got = tuple(oz[pid][k] for k in ("基本値", "下限", "上限"))
    ok = all(abs(g - e) < 1e-12 for g, e in zip(got, (b, lo, hi)))
    email_rows.append((pid, (b, lo, hi), got, ok))
    print("e-mail", pid, (b, lo, hi), got, "ok" if ok else "MISMATCH")
if not all(r[3] for r in email_rows):
    sys.exit("Ozaki's sheet differs from his e-mail of 2026-10-25: stop and report")

# --- 3. range checks on his values ---
bad = []
for pid in oz_ids:
    r = oz[pid]; b, lo, hi = r["基本値"], r["下限"], r["上限"]
    if not blank(lo) and lo > b: bad.append(f"{pid}: 下限 > 基本値")
    if not blank(hi) and b > hi: bad.append(f"{pid}: 基本値 > 上限")
    for k, v in (("基本値", b), ("下限", lo), ("上限", hi)):
        if blank(v): continue
        if is_prop(r["単位"]) and not 0 <= v <= 1: bad.append(f"{pid}: {k} not in [0, 1]")
        if is_pos(r["単位"]) and not v > 0: bad.append(f"{pid}: {k} not positive")
if bad:
    sys.exit("range check failed: " + "; ".join(bad))
print("range checks: pass (42 rows)")

# --- 4. internal sheet v6 and the mapping ---
src = P("input", "params", "parameters_v6.xlsx")
if not os.path.exists(src):  # moved to archive/ after v7 was made (git mv)
    src = P("input", "params", "archive", "parameters_v6.xlsx")
wb = load_workbook(src)
ws = wb["パラメータ"]
cm = col_of(ws)
v6 = rows_of(ws)
v6_oz = [k for k, r in v6.items() if r["担当"] == "尾崎"]
target = {}
for pid in oz_ids:
    if pid in CHECK_ONLY:
        continue
    if pid in MAP:
        target[pid] = MAP[pid]
    elif pid in NEW:
        assert pid not in v6, pid
        target[pid] = pid
    elif pid in v6 and v6[pid]["担当"] == "尾崎":
        target[pid] = pid
    else:
        sys.exit(f"Ozaki's row {pid} is not a row of his in v6 and has no mapping: stop and report")
covered = set(target.values())
assert set(v6_oz) <= covered, sorted(set(v6_oz) - covered)
assert all(blank(v6[t][k]) for t in v6_oz for k in ("基本値", "下限", "上限")), "v6 rows of 尾崎 are expected blank"
# X01: increment E06 - E07 (CHALLENGE 18.5% vs 11.5%)
e6, e7 = v6["E06"]["基本値"], v6["E07"]["基本値"]
x01 = oz["X01"]["基本値"]
x01_ok = round(e6 - e7, 2) == x01 and f"{100 * e6:.1f}" in oz["X01"]["出典の該当箇所"] and f"{100 * e7:.1f}" in oz["X01"]["出典の該当箇所"]
print(f"X01 {x01} vs E06 - E07 = {e6} - {e7} = {e6 - e7:.5f}:", "consistent" if x01_ok else "INCONSISTENT")
if not x01_ok:
    sys.exit("X01 does not agree with E06 - E07: stop and report")

# --- 5. ranges he left blank ---
filled = []   # (pid, rule, his lower, his upper, new lower, new upper)
def fill_range(pid, r):
    b, lo, hi, unit = r["基本値"], r["下限"], r["上限"], r["単位"]
    if not blank(lo) and not blank(hi):
        return lo, hi, None
    if blank(lo) and blank(hi):
        nlo, nhi, rule = b * 0.75, b * 1.25, "基本値 ±25%"
        note = "幅は原が設定（基本値 ±25%）。"
    elif blank(hi):
        nlo, nhi, rule = lo, 2 * b - lo, "上限を対称に補った"
        note = "上限は原が設定（片側を対称に補った）。"
    else:
        nlo, nhi, rule = 2 * b - hi, hi, "下限を対称に補った"
        note = "下限は原が設定（片側を対称に補った）。"
    if is_prop(unit):
        nlo, nhi = max(0.0, nlo), min(1.0, nhi)
    nlo, nhi = (float(f"{v:.15g}") for v in (nlo, nhi))   # 7.77432, not 7.774319999999999
    if is_pos(unit):
        assert nlo > 0, (pid, nlo)
    filled.append((pid, rule, lo, hi, nlo, nhi))
    return nlo, nhi, note

# --- 6. write v7 ---
yellow = ws.cell(row_of(ws, "D03"), cm["基本値"]).fill.fgColor.rgb
n0 = ws.max_row
for new_pid in ("D04P", "D03P"):  # insert, bottom-up
    after = NEW[new_pid]
    r = row_of(ws, after) + 1
    ws.insert_rows(r)
    copy_style(ws, row_of(ws, after), r)
    for k in ("区分", "項目", "適用する状態", "単位", "担当"):
        ws.cell(r, cm[k]).value = ws.cell(row_of(ws, after), cm[k]).value
    ws.cell(r, cm["param_id"]).value = new_pid
    ws.cell(r, cm["適用する群"]).value = G_PEMBRO
    for k in ("区分", "適用する状態", "単位"):
        assert ws.cell(r, cm[k]).value == oz[new_pid][k], (new_pid, k)
for pid in ("D03", "D04"):
    ws.cell(row_of(ws, pid), cm["適用する群"]).value = G_NO_PEMBRO
n1 = ws.max_row
assert n1 == n0 + 2
provisional = []
for pid, t in target.items():
    r = oz[pid]
    assert ws.cell(row_of(ws, t), cm["単位"]).value == r["単位"] or pid == "X02", (pid, t)
    lo, hi, rnote = fill_range(pid, r)
    notes = [] if blank(r["備考"]) else [r["備考"].rstrip("。") + "。"]
    add = []
    if "【要確認" in (r["備考"] or ""):
        add.append(PROVISIONAL); provisional.append(pid)
    if t in NOTES: add.append(NOTES[t])
    if rnote: add.append(rnote)
    if add: notes.append(TAG + "".join(add))
    vals = dict(基本値=r["基本値"], 下限=lo, 上限=hi, 価格の年度=r["価格の年度"], 出典=r["出典"],
                出典の該当箇所=r["出典の該当箇所"], 備考="".join(notes))
    rr = row_of(ws, t)
    for k, v in vals.items():
        ws.cell(rr, cm[k]).value = None if blank(v) else v
# the validation list on 担当 and the filter cover the new rows
for dv in ws.data_validations.dataValidation:
    if str(dv.sqref).startswith("M2:"):
        dv.sqref = MultiCellRange(f"M2:M{n1}")
ws.auto_filter.ref = f"A1:N{n1}"
for r in range(2, n1 + 1):  # yellow only on 尾崎 rows
    is_oz = ws.cell(r, cm["担当"]).value == "尾崎"
    for k in INPUT_COLS:
        f = ws.cell(r, cm[k]).fill
        assert (f.fill_type is not None and f.fgColor.rgb == yellow) == is_oz, (ws.cell(r, 1).value, k)
out = P("input", "params", "parameters_v7.xlsx")
wb.save(out)
v7 = rows_of(load_workbook(out)["パラメータ"])
v7_oz = [k for k, r in v7.items() if r["担当"] == "尾崎"]
assert all(not blank(v7[k]["基本値"]) for k in v7)
print(f"{os.path.basename(src)} ({n0 - 1} rows) -> {os.path.basename(out)} ({n1 - 1} rows; 尾崎 {len(v7_oz)}, ranges set {len(filled)})")
assert len(provisional) == 9, provisional
assert len(filled) == 17, [f[0] for f in filled]   # 18 rows without a range less X01 (not entered)

# --- 7. review record ---
L = ["# 尾崎先生の記入案 v1 の取り込み（2026-10-25）", "",
     f"対象：`input/params/ozaki/{os.path.basename(OZ_FILE)}`（シート パラメータ、記入の手引き、計算根拠_尾崎）。"
     f"取り込み先：`input/params/parameters_v7.xlsx`（{n1 - 1} 行、底本 v6 は `input/params/archive/`）。`R/py/22_params_v7.py` が生成。", "",
     "## 0. 読み取り", "",
     f"- パラメータの数式は計算根拠_尾崎のセルを参照している。数式セルはパラメータ {n_formula['パラメータ']}、計算根拠_尾崎 {n_formula['計算根拠_尾崎']}、"
     "すべてに計算済みの値（キャッシュ）があり、それを読んだ（openpyxl の data_only）。LibreOffice での再計算は不要だった。"
     f"ファイルの最終保存は {saved_by.split('$')[0]}（キャッシュはその計算結果）。パラメータの数式 {n_recomp} 個は、参照先の計算根拠_尾崎のキャッシュ値から計算し直して一致した"
     + ("" if not not_parsed else f"（形の違う {len(not_parsed)} 個は照合していない：{'、'.join(not_parsed)}）") + "。",
     f"- 担当が尾崎の行は {len(oz_ids)} 行（v1 の 36 行と末尾の追加 6 行：D03P、D04P、F01P、F04P、X01、X02）。"
     "交付した v1（`input/params/archive/parameters_template_v1.xlsx`）と比べて、担当が原の行と、param_id から単位までの欄と担当の欄に変更はない。",
     "- 範囲の確認：下限 ≦ 基本値 ≦ 上限、割合は 0 から 1、金額と期間は正。42 行すべて満たす。", "",
     "## 1. メール（尾崎 2026-10-25）との照合", "",
     "| param_id | メール（基本値 [下限, 上限]） | 記入案 | 一致 |", "|---|---|---|---|"]
for pid, e, g, ok in email_rows:
    L.append(f"| {pid} | {fmt(e[0])} [{fmt(e[1])}, {fmt(e[2])}] | {fmt(g[0])} [{fmt(g[1])}, {fmt(g[2])}] | {'一致' if ok else '不一致'} |")
L += ["", "F01：v1 の項目名は旧定義（化学療法のみの群の non-pCR 例）だが、メールで gBRCA 陰性の non-pCR 例での割合（新定義）と明記されている。"
      "`output/params_check.md` の「確認が必要」の印は外し、確認済み（根拠：尾崎 2026-10-25 メール）とした。", "",
      "## 2. 追加行の扱い", "",
      f"- X01（運動による筋骨格系有害事象の発現率の増分 {fmt(x01)}）：CHALLENGE の E06 − E07 = {e6} − {e7} = {e6 - e7:.5f}（{100 * e6:.1f}% − {100 * e7:.1f}%）と一致"
      "（小数 2 桁で一致、出典の該当箇所の 18.5% 対 11.5% も一致）。内部表は E06、E07（3 級以上は E09、E10）で群別に計上するので、X01 の行は設けない。",
      f"- X02（筋骨格系有害事象の1件あたり管理費用 {fmt(oz['X02']['基本値'])} 円、下限 {fmt(oz['X02']['下限'])} 円）：内部表の E08 に入れた。上限は空欄のため対称に補った（第 4 節）。",
      "- D03P、D04P：v7 に新設（ペムブロリズマブを含む群の遠隔再発の一次治療の月額と平均継続期間。ペムブロリズマブを含む群では再発後に免疫療法を使わないため）。"
      f"D03、D04 の適用する群は「{G_NO_PEMBRO}」に変更、D05 は両群共通のまま。",
      "- F01P、F04P：v6 に既にある行（ペムブロリズマブを含む群）に入れた。",
      "- A06：尾崎先生が 10 割に換算した 100 万円（備考に記載）をそのまま使う。", "",
      "## 3. 【要確認】の 9 行（暫定値として使う）", "",
      "v7 の備考に「" + TAG + PROVISIONAL + "」と書いた。", "",
      "| param_id | 項目 | 基本値 | 尾崎先生の【要確認】 |", "|---|---|---|---|"]
for pid in provisional:
    t = target[pid]
    m = re.search(r"【要確認[^】]*】[^【]*", oz[pid]["備考"]).group(0).strip()
    L.append(f"| {pid} | {v7[t]['項目']} | {fmt(oz[pid]['基本値'])} | {m} |")
L += ["", "## 4. 幅が未設定の 18 行", "",
      "記入の手引きの約束（下限と上限は分からなければ空欄、こちらで設定）に従い、尾崎先生に問い合わせずに補った。"
      "両方空欄は基本値 ±25% を 95% 区間とし（割合は 0 から 1 で切る。該当は F03 で切る必要はなかった）、片側だけ空欄は基本値に対して対称に補った。"
      "一元感度分析の図表ではこれらの行に「範囲は仮定値」と注記する（`docs/model_spec.md` 第 6 節）。X01 はモデルに入れないので補っていない。", "",
      "| param_id | 項目 | 単位 | 基本値 | 下限（記入案） | 上限（記入案） | 下限（v7） | 上限（v7） | 規則 |", "|---|---|---|---|---|---|---|---|---|"]
order = [p for p in oz_ids if p in {f[0] for f in filled} or p in CHECK_ONLY]
fd = {f[0]: f for f in filled}
for pid in order:
    r = oz[pid]
    if pid in CHECK_ONLY:
        L.append(f"| {pid} | {r['項目']} | {r['単位']} | {fmt(r['基本値'])} | {fmt(r['下限'])} | {fmt(r['上限'])} | － | － | モデルに入れない（第 2 節） |")
        continue
    _, rule, lo, hi, nlo, nhi = fd[pid]
    t = target[pid]
    name = v7[t]["項目"] + (f"（内部表 {t}）" if t != pid else "")
    L.append(f"| {pid} | {name} | {r['単位']} | {fmt(r['基本値'])} | {fmt(lo)} | {fmt(hi)} | {fmt(nlo)} | {fmt(nhi)} | {rule} |")
f5 = fd["F05"]
L += ["", f"所見（値は変えていない）：F05（オラパリブの費用）は基本値 {fmt(oz['F05']['基本値'])} 円が添付文書上の最大投与期間 1 年分で、"
      f"上限を対称に補った {fmt(f5[5])} 円はその {f5[5] / oz['F05']['基本値']:.2f} 倍、投与期間の上限を超える額になる。規則どおりに置いた。", "",
      "## 5. 尾崎先生の各行（値と出典の一覧）", "",
      "表示は丸めてある（内部表には元の値）。v7 の欄は第 4 節で補った後の値。数式の欄は記入案のパラメータのシートで計算根拠_尾崎を参照していたもの。", "",
      "| param_id | 内部表 | 項目（v7） | 単位 | 基本値 | 下限（記入案） | 上限（記入案） | 下限（v7） | 上限（v7） | 数式 | 出典 | 出典の該当箇所 |",
      "|---|---|---|---|---|---|---|---|---|---|---|---|"]
esc = lambda s: "" if blank(s) else str(s).replace("|", "\\|").replace("\n", " ")
for pid in oz_ids:
    r = oz[pid]; t = target.get(pid)
    item = v7[t]["項目"] if t else r["項目"]
    v7lo, v7hi = (v7[t]["下限"], v7[t]["上限"]) if t else (None, None)
    L.append(f"| {pid} | {t or '（入れない）'} | {esc(item)} | {esc(r['単位'])} | {fmt(r['基本値'])} | {fmt(r['下限'])} | {fmt(r['上限'])} | "
             f"{'－' if not t else fmt(v7lo)} | {'－' if not t else fmt(v7hi)} | {'、'.join(formula_cells[pid]) or '－'} | {esc(r['出典'])} | {esc(r['出典の該当箇所'])} |")
L += ["", "### 備考（記入案のまま）", ""]
for pid in oz_ids:
    L.append(f"- {pid}：{esc(oz[pid]['備考']) or '（空欄）'}")
L += ["", "## 6. この取り込みでしていないこと", "",
      "- 経済評価の結果は計算していない（ICER なし）。",
      "- 尾崎先生の値は変えていない（第 4 節の幅の補いと備考への追記だけ）。"]
with open(P("output", "params_ozaki_v1_review.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L) + "\n")
print("wrote output/params_ozaki_v1_review.md")
