"""Internal parameter sheet v5 -> v6 (2026-10-23, user instruction; the sheet for Ozaki, v2, is not touched):
  F07, F08: 適用する群 -> 全群; a note added that the same HR is used in the arms with pembrolizumab
            (assumption; CREATE-X and OlympiA have no pembrolizumab).
  E06, E07, E09, E10: musculoskeletal adverse events of the exercise programme from CHALLENGE
            (Courneya KS, et al. N Engl J Med 2025;393:13-25, DOI 10.1056/NEJMoa2502760), read here from
            input/papers/CHALLENGE.pdf (Results, Safety, p.19) and CHALLENGE_supplement.pdf (Table S4,
            p.77): exercise group (as-treated, 428) and health-education group (461), any grade and
            grade >= 3. Intervals: Clopper-Pearson 95%, as for B21-B31 (R/py/11_fill_hara_params.py).
input/params/parameters_v5.xlsx is moved to input/params/archive/ afterwards (git mv).

Usage: .venv/Scripts/python.exe -I R/py/16_params_v6.py <project_root>
"""
import sys, os, re, math
sys.stdout.reconfigure(encoding="utf-8")
from openpyxl import load_workbook
import pymupdf as fitz

root = sys.argv[1]
P = lambda *a: os.path.join(root, *a)
COLS = ["param_id", "区分", "項目", "適用する群", "適用する状態", "単位", "基本値", "下限", "上限",
        "価格の年度", "出典", "出典の該当箇所", "担当", "備考"]


def pdf_pages(path):
    out = []
    for pg in fitz.open(path):
        t = pg.get_text().replace("­\n", "").replace("­", "")
        out.append(re.sub(r"\s+", " ", t))
    return out


def cp_ci(x, n):
    """Clopper-Pearson 95% interval by bisection on the binomial tails (as in 11_fill_hara_params.py)"""
    def cdf(k, p): return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))
    def root_(g):
        lo, hi = 0.0, 1.0
        up = g(hi) > g(lo)
        for _ in range(200):
            mid = (lo + hi) / 2
            if (g(mid) < 0) == up:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    lower = 0.0 if x == 0 else root_(lambda p: (1 - cdf(x - 1, p)) - 0.025)
    upper = 1.0 if x == n else root_(lambda p: cdf(x, p) - 0.025)
    return lower, upper


# CHALLENGE main text: as-treated sizes and musculoskeletal adverse events (Results, Safety)
main = pdf_pages(P("input", "papers", "CHALLENGE.pdf"))
sup = pdf_pages(P("input", "papers", "CHALLENGE_supplement.pdf"))
pg_main = [i for i, t in enumerate(main) if "Musculoskeletal adverse events occurred in" in t]
assert len(pg_main) == 1, pg_main
t = main[pg_main[0]]
journal_page = re.search(r"July 3, 2025 (\d+) ", t).group(1)
m = re.search(r"safety analyses included (\d+) pa ?tients who had been randomly assigned to the exercise group.*? and (\d+) patients who had been randomly assigned to the health-education group", t)
n_ex, n_he = int(m.group(1)), int(m.group(2))
m = re.search(r"Musculoskeletal adverse events occurred in (\d+) patients \(([\d.]+)%\) in the exercise group and in (\d+) \(([\d.]+)%\) in the health-education group", t)
x_ex, x_he = int(m.group(1)), int(m.group(3))
q_main = m.group(0)
# supplement Table S4: any grade and grade >= 3
pg_sup = [i for i, s in enumerate(sup) if "Table S4. Summary of acute adverse events" in s]
assert len(pg_sup) == 1, pg_sup
s = sup[pg_sup[0]]
sup_page = re.search(r"CO\.21 Supplementary Appendix (\d+)", s).group(1)
ns = re.search(r"SEP \(n.(\d+)\) HEM \(n=(\d+)\)", s)
assert (int(ns.group(1)), int(ns.group(2))) == (n_ex, n_he), ns.groups()
m = re.search(r"Musculoskeletal \(total\) (\d+) \(([\d.]+)%\) (\d+) \(([\d.]+)%\) (\d+) \(([\d.]+)%\) (\d+) \(([\d.]+)%\)", s)
s_ex, g3_ex, s_he, g3_he = int(m.group(1)), int(m.group(3)), int(m.group(5)), int(m.group(7))
q_sup = m.group(0)
assert (s_ex, s_he) == (x_ex, x_he), (s_ex, s_he, x_ex, x_he)
for x, n, pct in [(x_ex, n_ex, m.group(2)), (g3_ex, n_ex, m.group(4)), (x_he, n_he, m.group(6)), (g3_he, n_he, m.group(8))]:
    assert abs(100 * x / n - float(pct)) < 0.051, (x, n, pct)
print(f"CHALLENGE: as-treated {n_ex} / {n_he}; musculoskeletal any grade {x_ex} / {x_he}; grade >= 3 {g3_ex} / {g3_he}; "
      f"main text p.{journal_page} (PDF page {pg_main[0] + 1}), Table S4 p.{sup_page} (PDF page {pg_sup[0] + 1})")
print("  main:", q_main); print("  S4:", q_sup)

SRC = "Courneya KS, et al. N Engl J Med 2025;393:13-25 (CHALLENGE, CCTG CO.21). DOI 10.1056/NEJMoa2502760"
WHERE = f"本文 p.{journal_page}（Results の Safety）、Supplementary Appendix Table S4（p.{sup_page}）"
DUR = ("CHALLENGE の介入は 3 年（有害事象は無作為化後 36 か月まで観察）、本モデルは NAC 中の 6 か月。報告値をそのまま使うため、"
       "運動群の有害事象を過大に見積もる（運動に不利な方向）。")
HE = f"健康教育群には運動群に割り付けられたが一度も参加しなかった 17 例を含む（as-treated、計 {n_he} 例）。"
rows = {
    "E06": (x_ex, n_ex, "全Grade", "Table S4 の Musculoskeletal (total)、Any Grade の欄（本文と同値）", ""),
    "E07": (x_he, n_he, "全Grade", "Table S4 の Musculoskeletal (total)、Any Grade の欄（本文と同値）", HE),
    "E09": (g3_ex, n_ex, "Grade 3以上", "Table S4 の Musculoskeletal (total)、Grade ≥3 の欄（表の注：1% 以上の重篤な有害事象を掲載する欄。筋骨格系は特に関心のある有害事象として掲載）", ""),
    "E10": (g3_he, n_he, "Grade 3以上", "Table S4 の Musculoskeletal (total)、Grade ≥3 の欄（表の注：1% 以上の重篤な有害事象を掲載する欄。筋骨格系は特に関心のある有害事象として掲載）", HE),
}
F_NOTE = "ペムブロリズマブを含む群にも同じ値を当てる（仮定。CREATE-X と OlympiA はペムブロリズマブを含まない）"

src = P("input", "params", "parameters_v5.xlsx")
if not os.path.exists(src):  # moved to archive/ after v6 was made (git mv)
    src = P("input", "params", "archive", "parameters_v5.xlsx")
wb = load_workbook(src)
ws = wb["パラメータ"]
hdr = [c.value for c in ws[1]]
assert hdr == COLS, hdr
cm = {h: i + 1 for i, h in enumerate(hdr)}
def row_of(pid):
    hits = [r for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value == pid]
    assert len(hits) == 1, (pid, hits)
    return hits[0]
def put(pid, **kw):
    r = row_of(pid)
    for k, v in kw.items():
        ws.cell(r, cm[k]).value = v
for pid in ("F07", "F08"):
    note = ws.cell(row_of(pid), cm["備考"]).value or ""
    assert F_NOTE not in note
    put(pid, 適用する群="全群", 備考=(note.rstrip("。") + "。" if note else "") + F_NOTE + "。")
for pid, (x, n, grade, where_s4, extra) in rows.items():
    assert ws.cell(row_of(pid), cm["担当"]).value == "原"
    lo, hi = cp_ci(x, n)
    put(pid, 基本値=round(x / n, 5), 下限=round(lo, 5), 上限=round(hi, 5), 出典=SRC, 出典の該当箇所=WHERE,
        備考=f"{grade}、{x}/{n} 例（as-treated）。下限と上限は Clopper-Pearson 95%信頼区間。{where_s4}。{extra}{DUR}")
    print(pid, round(x / n, 5), round(lo, 5), round(hi, 5))
out = P("input", "params", "parameters_v6.xlsx")
wb.save(out)
print(os.path.basename(src), "->", os.path.basename(out))
