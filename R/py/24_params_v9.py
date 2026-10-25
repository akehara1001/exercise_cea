"""Internal parameter sheet v8 -> v9 (2026-10-25, user instruction). Run after R/py/23_params_v8.py.
  B33P, B33C: the summed counts of six grade >= 3 adverse events are treated as Poisson (events per
            patient, multiplied by the decrement per event U05; not a proportion). 下限 and 上限 = exact
            (Garwood) 95% interval of the rate, x / n with x the summed events; the probabilistic
            analysis uses a gamma distribution (R/10_read_params.R maps the unit 件/人 to gamma).
  F05: 下限 back to Ozaki's value (3,539,520 yen, stopping at half a year), 上限 = 基本値. The 薬価固定
            rule: a side Ozaki gave is kept, only a side he left blank is set by the rule. In v8 his lower
            bound was replaced by the rule's, which was an error in 原's instruction.
Corrects section 7 of output/params_ozaki_v1_review.md (7.1 and 7.4; a note at its head) and writes
input/params/parameters_v9.xlsx; v8 is moved to input/params/archive/ afterwards (git mv).
Section 7 is written by R/py/23_params_v8.py: run 23 and then 24 (24 alone on an already corrected
record stops at its checks).

Usage: .venv/Scripts/python.exe -I R/py/24_params_v9.py <project_root>
"""
import sys, os, re, math
sys.stdout.reconfigure(encoding="utf-8")
from openpyxl import load_workbook

root = sys.argv[1]
P = lambda *a: os.path.join(root, *a)
COLS = ["param_id", "区分", "項目", "適用する群", "適用する状態", "単位", "基本値", "下限", "上限",
        "価格の年度", "出典", "出典の該当箇所", "担当", "備考"]
TAG = "【原 2026-10-25】"
OZ_FILE = P("input", "params", "ozaki", "parameters_v1_尾崎記入案.xlsx")
USER_B33 = {"B33P": (0.99283, 1.13862), "B33C": (0.88599, 1.08559)}   # the instruction's values
V8_F05 = "尾崎先生の下限（半年で中止、3,539,520 円）と v7 で対称に補った上限（10,618,560 円）は使わない。"
NEW_F05 = ("下限は尾崎先生の値（半年で中止）のまま、上限だけをこの規則で基本値とした（尾崎先生が示した側はそのまま使い、示されていない側だけを規則で補う）。"
           "v7 で対称に補った上限（10,618,560 円）は使わない。v8 で尾崎先生の下限を規則の下限（5,309,280 円）に置き換えたのは原の指示の誤りで、v9 で戻した。")
V4_B33 = "下限と上限は未設定（件数の合計のため二項区間は当てはまらない）。"
NEW_B33 = ("下限と上限は Poisson の正確な 95% 信頼区間（件数を Poisson として扱う。比例ではなく 1 人あたりの件数で、件ごとの効用低下 U05 に掛けるため）。"
           "確率的感度分析はガンマ分布。")


def col_of(ws):
    hdr = [c.value for c in ws[1]]
    assert hdr == COLS, hdr
    return {h: i + 1 for i, h in enumerate(hdr)}


def row_of(ws, pid):
    hits = [r for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value == pid]
    assert len(hits) == 1, (pid, hits)
    return hits[0]


def pois_cdf(x, lam):
    """P(X <= x) for X ~ Poisson(lam), summed in log space"""
    lt = [-lam + i * math.log(lam) - math.lgamma(i + 1) for i in range(x + 1)]
    m = max(lt)
    return math.exp(m) * sum(math.exp(v - m) for v in lt)


def garwood(x, n):
    """exact 95% interval of a Poisson rate x / n (bisection on the Poisson tails)"""
    def solve(g, lo, hi):
        for _ in range(200):
            mid = (lo + hi) / 2
            if g(mid) > 0: lo = mid
            else: hi = mid
        return (lo + hi) / 2
    lower = 0.0 if x == 0 else solve(lambda l: (1 - pois_cdf(x - 1, l)) < 0.025, 0.0, 3.0 * x)   # P(X >= x) = 0.025
    upper = solve(lambda l: pois_cdf(x, l) > 0.025, 0.0, 3.0 * x + 10)                           # P(X <= x) = 0.025
    return lower / n, upper / n


def fmt(v):
    if v is None:
        return "（空欄）"
    if abs(v) >= 1000:
        return f"{v:,.2f}".rstrip("0").rstrip(".")
    return f"{v:.6g}"


src = P("input", "params", "parameters_v8.xlsx")
if not os.path.exists(src):  # moved to archive/ after v9 was made (git mv)
    src = P("input", "params", "archive", "parameters_v8.xlsx")
wb = load_workbook(src)
ws = wb["パラメータ"]
cm = col_of(ws)
get = lambda pid, k: ws.cell(row_of(ws, pid), cm[k]).value
def put(pid, **kw):
    for k, v in kw.items():
        ws.cell(row_of(ws, pid), cm[k]).value = v
before = {pid: {k: get(pid, k) for k in ("基本値", "下限", "上限", "備考")} for pid in ("B33P", "B33C", "F05")}

# B33P, B33C
b33 = {}
for pid in ("B33P", "B33C"):
    note = get(pid, "備考")
    m = re.search(r"(\d+) 件 / (\d+) 例", note)
    x, n = int(m.group(1)), int(m.group(2))
    assert get(pid, "基本値") == round(x / n, 5) and get(pid, "単位") == "件/人" and V4_B33 in note, pid
    lo, hi = (round(v, 5) for v in garwood(x, n))
    assert (lo, hi) == USER_B33[pid], (pid, lo, hi, USER_B33[pid])
    b33[pid] = (x, n, lo, hi)
    put(pid, 下限=lo, 上限=hi, 備考=note.replace(V4_B33, "") + TAG + NEW_B33)
    print(pid, f"{x} / {n}", (lo, hi))

# F05: Ozaki's lower bound kept
wo = load_workbook(OZ_FILE, data_only=True)["パラメータ"]
oz_lo = [r[7].value for r in wo.iter_rows(min_row=2) if r[0].value == "F05"]
assert len(oz_lo) == 1 and oz_lo[0] == 3539520, oz_lo
note = get("F05", "備考")
assert V8_F05 in note and get("F05", "上限") == get("F05", "基本値"), note
put("F05", 下限=oz_lo[0], 備考=note.replace(V8_F05, NEW_F05))

for r in range(2, ws.max_row + 1):
    b, lo, hi = (ws.cell(r, cm[k]).value for k in ("基本値", "下限", "上限"))
    assert (lo is None or lo <= b) and (hi is None or b <= hi), ws.cell(r, 1).value
out = P("input", "params", "parameters_v9.xlsx")
wb.save(out)
after = {pid: {k: get(pid, k) for k in ("基本値", "下限", "上限", "備考")} for pid in before}
print(f"{os.path.basename(src)} -> {os.path.basename(out)}")
for pid in before:
    print(" ", pid, [before[pid][k] for k in ("基本値", "下限", "上限")], "->", [after[pid][k] for k in ("基本値", "下限", "上限")])

# review record: correct section 7 (7.1 and 7.4), note at its head
rv = P("output", "params_ozaki_v1_review.md")
text = open(rv, encoding="utf-8").read()
head = "\n## 7. v8 の変更（2026-10-25、`R/py/23_params_v8.py`、`input/params/parameters_v8.xlsx`）\n"
assert text.count(head) == 1
pre, sec7 = text.split(head)
def sub(old, new):
    global sec7
    assert sec7.count(old) == 1, (old[:60], sec7.count(old))
    sec7 = sec7.replace(old, new)
note7 = ("\n> **v9 での訂正（2026-10-25、`R/py/24_params_v9.py`、`input/params/parameters_v9.xlsx`）**：F05 の下限を尾崎先生の値（3,539,520 円）に戻した。"
         "薬価固定の規則は「尾崎先生が示した側はそのまま使い、示されていない側だけを規則で補う」とした。v8 で尾崎先生の下限を規則の下限に置き換えたのは原の指示の誤り。"
         "B33P、B33C は件数を Poisson として扱い、幅を正確な 95% 信頼区間とした（7.4）。7.1 と 7.4 は v9 の値に書き直してある。\n")
sub("| F05 | オラパリブの費用（全期間） | 尾崎 | 7,079,040 [3,539,520, 10,618,560] | 7,079,040 [5,309,280, 7,079,040] | ガンマ分布（v7 で補った幅から） → 基本値に固定 |",
    "| F05 | オラパリブの費用（全期間） | 尾崎 | 7,079,040 [3,539,520, 10,618,560] | 7,079,040 [3,539,520, 7,079,040]（v9。v8 は [5,309,280, 7,079,040]） | ガンマ分布（v7 で補った幅から） → 基本値に固定 |")
sub("この規則を当てた行は次の 4 行だけ。尾崎先生が幅を示した薬剤費の行（F02 など）は尾崎先生の幅のまま。",
    "この規則を当てた行は次の 4 行だけ。尾崎先生が幅を示した薬剤費の行（F02 など）は尾崎先生の幅のまま。尾崎先生が片側だけ示した行（F05 の下限）は、示された側をそのまま使い、示されていない側だけをこの規則で補う（v9）。")
sub("F05 は v7 の上限（対称に補った 10,618,560 円）を取り消し、尾崎先生の下限（半年で中止、3,539,520 円）も規則の下限（5,309,280 円）に置き換えた。",
    "F05 は v7 の上限（対称に補った 10,618,560 円）を取り消し、上限を基本値とした。下限は尾崎先生の値（半年で中止、3,539,520 円）のまま（v9）。"
    "v8 では尾崎先生の下限を規則の下限（5,309,280 円）に置き換えていたが、原の指示の誤りで、v9 で戻した。")
old74 = sec7[sec7.index("### 7.4 B33P、B33C"):sec7.index("### 7.5")]
new74 = ("### 7.4 B33P、B33C（v9 で幅を設定）\n\n"
         "B33 は 6 種の Grade 3以上の有害事象の件数の合計で（一人が複数回数えられうる）、1 人あたりの件数として件ごとの効用低下 U05 に掛ける。比例ではないので、"
         "v8 の時点の指示（Clopper-Pearson）は当てはまらなかった（ペムブロリズマブ群は件数 833 が例数 783 を超える）。v9 で件数を Poisson として扱い、"
         "一元感度分析の幅を正確な 95% 信頼区間、確率的感度分析をガンマ分布とした。\n\n"
         "| param_id | 件数 / 例数 | 変更前（v8） | 変更後（v9） 基本値 [下限, 上限] | 確率的感度分析 |\n|---|---|---|---|---|\n"
         + "".join(f"| {pid} | {x} / {n} | {fmt(before[pid]['基本値'])} [（空欄）, （空欄）] | {fmt(after[pid]['基本値'])} [{fmt(lo)}, {fmt(hi)}] | なし → ガンマ分布 |\n"
                   for pid, (x, n, lo, hi) in b33.items()) + "\n")
sec7 = sec7.replace(old74, new74)
sub("- 上記以外の行は v7 のまま。", "- 上記以外の行は v7 のまま（v9 で変えたのは F05 の下限と B33P、B33C の幅だけ）。")
open(rv, "w", encoding="utf-8", newline="\n").write(pre + head + note7 + sec7)
print("corrected section 7 of output/params_ozaki_v1_review.md")
