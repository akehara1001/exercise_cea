"""Internal parameter sheet v7 -> v8 (2026-10-25, user instruction). Run after R/py/22_params_v7.py.
  A01, A02, A03, F05 (drug costs from list prices and labelled doses): 薬価固定 = fixed at 基本値 in the
            probabilistic analysis; the one-way range only downward, to 75% of 基本値 (price revisions in
            Japan only lower prices; no dosing beyond the labelled dose or maximum duration). F05: the
            upper bound mirrored in v7 and Ozaki's lower bound are replaced by [0.75 x 基本値, 基本値].
            Drug-cost rows where Ozaki gave a range (e.g. F02) keep his range.
  B23C, B26C, B27C, B29C (rate 0, 0 events): fixed at 0 in the probabilistic analysis; one-way upper
            bound = Clopper-Pearson 95% upper bound for 0 events (round 6: 0 events in the placebo arm
            taken as 0 for now, small effect). The values are those of v7 (checked here).
  F01P: definition as in the internal sheet (gBRCA-negative non-pCR patients); basis added to 備考
            (Ozaki's e-mail of 2026-10-25, point 2).
  B33P, B33C are not changed: the instruction (Clopper-Pearson from the KEYNOTE-522 counts) cannot be
            applied, the counts are summed events (833 events in 783 patients in the pembrolizumab arm),
            not patients; left for the user's decision (docs/model_spec.md section 8).
Writes input/params/parameters_v8.xlsx and appends section 7 to output/params_ozaki_v1_review.md
(replacing an earlier section 7, so the script can be rerun); v7 is moved to input/params/archive/
afterwards (git mv).

Usage: .venv/Scripts/python.exe -I R/py/23_params_v8.py <project_root>
"""
import sys, os, re
sys.stdout.reconfigure(encoding="utf-8")
from openpyxl import load_workbook

root = sys.argv[1]
P = lambda *a: os.path.join(root, *a)
COLS = ["param_id", "区分", "項目", "適用する群", "適用する状態", "単位", "基本値", "下限", "上限",
        "価格の年度", "出典", "出典の該当箇所", "担当", "備考"]
TAG = "【原 2026-10-25】"
DRUG = ["A01", "A02", "A03", "F05"]
ZERO = ["B23C", "B26C", "B27C", "B29C"]
NOTE_DRUG = ("幅の規則：薬価固定（確率的感度分析では基本値に固定し、一元感度分析では基本値の 75% まで下げる方向だけに動かす。"
             "日本の薬価改定は引き下げだけで、規定用量と最長投与期間を超えて投与しないため、実際の費用は減量か早期中止で下がる方向にしか動かない）。")
NOTE_ZERO = ("幅の規則：0例：PSAは固定（確率的感度分析では 0 に固定し、一元感度分析の上限は 0 例の Clopper-Pearson 95% 上限。"
             "第六ラウンドでプラセボ群の 0 例は当面 0 とすると決めた。影響は小さい）。")
NOTE_F01P = ("定義は内部表のとおり gBRCA 陰性の non-pCR 例での割合として扱う（根拠：尾崎 2026-10-25 メール第 2 点。"
             "非 gBRCA の non-pCR 例はカペシタビン、gBRCA 陽性の non-pCR 例はオラパリブ）。")
V7_MIRROR = "上限は原が設定（片側を対称に補った）。"


def col_of(ws):
    hdr = [c.value for c in ws[1]]
    assert hdr == COLS, hdr
    return {h: i + 1 for i, h in enumerate(hdr)}


def row_of(ws, pid):
    hits = [r for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value == pid]
    assert len(hits) == 1, (pid, hits)
    return hits[0]


def fmt(v):
    if v is None:
        return "（空欄）"
    if abs(v) >= 1000:
        return f"{v:,.2f}".rstrip("0").rstrip(".")
    return f"{v:.6g}"


def add_note(note, text):
    note = (note or "").rstrip()
    if TAG in note:
        return note + text
    return (note.rstrip("。") + "。" if note else "") + TAG + text


src = P("input", "params", "parameters_v7.xlsx")
if not os.path.exists(src):  # moved to archive/ after v8 was made (git mv)
    src = P("input", "params", "archive", "parameters_v7.xlsx")
wb = load_workbook(src)
ws = wb["パラメータ"]
cm = col_of(ws)
get = lambda pid, k: ws.cell(row_of(ws, pid), cm[k]).value
def put(pid, **kw):
    for k, v in kw.items():
        ws.cell(row_of(ws, pid), cm[k]).value = v
before = {pid: {k: get(pid, k) for k in ("基本値", "下限", "上限", "備考")} for pid in DRUG + ZERO + ["F01P", "B33P", "B33C"]}

# 1. drug costs at list price: [0.75 x 基本値, 基本値]
for pid in DRUG:
    b = get(pid, "基本値")
    assert isinstance(b, (int, float)) and b > 0, pid
    note = get(pid, "備考")
    if pid == "F05":
        assert get(pid, "担当") == "尾崎" and V7_MIRROR in note, note
        lo7, hi7 = get(pid, "下限"), get(pid, "上限")
        note = note.replace(V7_MIRROR, NOTE_DRUG + f"尾崎先生の下限（半年で中止、{fmt(lo7)} 円）と v7 で対称に補った上限（{fmt(hi7)} 円）は使わない。")
    else:
        assert get(pid, "担当") == "原" and get(pid, "下限") is None and get(pid, "上限") is None, pid
        note = add_note(note, NOTE_DRUG)
    put(pid, 下限=float(f"{0.75 * b:.15g}"), 上限=b, 備考=note)

# 2. rates 0 with 0 events: the one-way upper bound is the Clopper-Pearson upper bound for 0 events
for pid in ZERO:
    note = get(pid, "備考")
    m = re.search(r"、0/(\d+) 例", note)
    assert m and get(pid, "基本値") == 0 and get(pid, "下限") == 0, pid
    n = int(m.group(1))
    cp0 = round(1 - 0.025 ** (1 / n), 5)
    assert get(pid, "上限") == cp0, (pid, get(pid, "上限"), cp0)     # as in v7: unchanged
    extra = ""
    if "全Grade 3例を上限とし" in note:
        extra = f"上限は全Grade の 3 例（3/{n} = {3 / n:.5f}）ではなく、それより大きい 0 例の Clopper-Pearson 上限 {cp0}（v4 からの値）。"
    put(pid, 備考=add_note(note, NOTE_ZERO + extra))

# 3. F01P: basis of the definition
put("F01P", 備考=add_note(get("F01P", "備考"), NOTE_F01P))

# checks and save
for r in range(2, ws.max_row + 1):
    b, lo, hi = (ws.cell(r, cm[k]).value for k in ("基本値", "下限", "上限"))
    assert (lo is None or lo <= b) and (hi is None or b <= hi), ws.cell(r, 1).value
out = P("input", "params", "parameters_v8.xlsx")
wb.save(out)
after = {pid: {k: get(pid, k) for k in ("基本値", "下限", "上限", "備考")} for pid in before}
changed = [pid for pid in before if before[pid] != after[pid]]
assert set(changed) == set(DRUG + ZERO + ["F01P"]), changed
print(f"{os.path.basename(src)} -> {os.path.basename(out)}; changed rows: {', '.join(changed)}")
for pid in DRUG + ZERO:
    print(" ", pid, [before[pid][k] for k in ("基本値", "下限", "上限")], "->", [after[pid][k] for k in ("基本値", "下限", "上限")])

# 4. B33P, B33C: not changed; the numbers for the decision
N = {"P": 783, "C": 389}
X = {}
for arm in ("P", "C"):
    m = re.search(r"(\d+) 件 / (\d+) 例", before[f"B33{arm}"]["備考"])
    X[arm] = int(m.group(1)); assert int(m.group(2)) == N[arm], m.group(0)
assert X["P"] > N["P"]

# 5. review record, section 7
rv = P("output", "params_ozaki_v1_review.md")
text = open(rv, encoding="utf-8").read()
text = text.split("\n## 7. v8 の変更")[0].rstrip("\n") + "\n"
item = lambda pid: get(pid, "項目")
rng = lambda d: f"{fmt(d['基本値'])} [{fmt(d['下限'])}, {fmt(d['上限'])}]"
L = ["", "## 7. v8 の変更（2026-10-25、`R/py/23_params_v8.py`、`input/params/parameters_v8.xlsx`）", "",
     "### 7.1 薬価と規定用量で計算した薬剤費（薬価固定）", "",
     "確率的感度分析では基本値に固定し、一元感度分析では基本値の 75% まで下げる方向だけに動かす。理由：日本の薬価改定は引き下げだけで、"
     "規定用量（または最長投与期間）を超えて投与しないため、実際の費用は減量か早期中止で下がる方向にしか動かない。"
     "この規則を当てた行は次の 4 行だけ。尾崎先生が幅を示した薬剤費の行（F02 など）は尾崎先生の幅のまま。", "",
     "| param_id | 項目 | 担当 | 変更前 基本値 [下限, 上限] | 変更後 基本値 [下限, 上限] | 確率的感度分析 |", "|---|---|---|---|---|---|"]
for pid in DRUG:
    psa_before = "ガンマ分布（v7 で補った幅から）" if pid == "F05" else "なし（幅未設定）"
    L.append(f"| {pid} | {item(pid)} | {get(pid, '担当')} | {rng(before[pid])} | {rng(after[pid])} | {psa_before} → 基本値に固定 |")
L += ["", f"F05 は v7 の上限（対称に補った {fmt(before['F05']['上限'])} 円）を取り消し、尾崎先生の下限（半年で中止、{fmt(before['F05']['下限'])} 円）も"
      f"規則の下限（{fmt(after['F05']['下限'])} 円）に置き換えた。", "",
      "### 7.2 基本値が 0 の発現率（0例：PSAは固定）", "",
      "確率的感度分析では 0 に固定し、一元感度分析の上限は 0 例の Clopper-Pearson 95% 上限。第六ラウンドで、プラセボ群の 0 例は当面 0 とし影響は小さいと決めている。"
      "値は v7 と同じ（上限 0.00944 は v4 から 0 例の Clopper-Pearson 上限）。変わったのは確率的感度分析の扱い（v7 ではベータ分布にできない行として残っていた）と備考。", "",
      "| param_id | 項目 | 基本値 [下限, 上限]（v7 と v8 で同じ） | 確率的感度分析 |", "|---|---|---|---|"]
for pid in ZERO:
    L.append(f"| {pid} | {item(pid)} | {rng(after[pid])} | ベータ分布にできない（v7）→ 0 に固定 |")
L += ["", "B26C、B27C の備考にある「全Grade 3例を上限とし」は、実際の上限（0 例の Clopper-Pearson 上限 0.00944）が全Grade の 3/389 = 0.00771 より大きいため使われていなかった。v8 の備考にその旨を足した。", "",
      "### 7.3 F01P の定義", "",
      "値（0.5 [0.05, 0.90]、暫定値）と定義は変えていない。内部表の定義（gBRCA 陰性の non-pCR 例でのカペシタビン使用割合）で扱う根拠として、"
      "尾崎 2026-10-25 メール第 2 点（非 gBRCA の non-pCR 例はカペシタビン、gBRCA 陽性の non-pCR 例はオラパリブ）を備考に足した。", "",
      "### 7.4 B33P、B33C（変更していない、裁定待ち）", "",
      f"指示は「KEYNOTE-522 の例数から Clopper-Pearson で 95% 区間」だが、B33 は 6 種の Grade 3以上の有害事象の件数の合計で、"
      f"ペムブロリズマブ群は {X['P']} 件 / {N['P']} 例（{X['P'] / N['P']:.5f} 件/人）と件数が例数を超える。二項分布の区間は定義できない"
      f"（v4 でも「件数の合計のため二項区間は当てはまらない」として未設定にしていた）。化学療法群（{X['C']} 件 / {N['C']} 例）は計算はできるが、同じ理由で意味が違う。"
      "どちらも v7 のまま（幅なし、分布なし）。", "",
      "### 7.5 この版でしていないこと", "",
      "- 経済評価の結果は計算していない（ICER なし）。",
      "- 上記以外の行は v7 のまま。"]
open(rv, "w", encoding="utf-8", newline="\n").write(text + "\n".join(L) + "\n")
print("appended section 7 to output/params_ozaki_v1_review.md")
