"""Ozaki's reply of 2026-10-23: row changes to the parameter sheets.
  input/params/archive/parameters_template_v1.xlsx (delivered to Ozaki) -> input/params/parameters_template_v2.xlsx
  input/params/parameters_v4.xlsx (internal; then moved to archive/)    -> input/params/parameters_v5.xlsx
Same row changes in both; nothing else is touched (other rows, column widths, fills, filters).
  F01, F04: new definition (within gBRCA-negative / gBRCA-positive non-pCR patients), groups without
            pembrolizumab (exercise arms included).
  F01P, F04P (new, after F01 and F04): the same for the groups with pembrolizumab; owner 尾崎.
  F02, F05: all groups (one cost per drug; no separate pembrolizumab rows).
  F06: all groups, all patients at diagnosis.
  E06-E10 (new, after E05): musculoskeletal adverse events of the exercise programme.
Yellow (input cells G-L and N) only on rows owned by 尾崎; the new ones are F01P, F04P, E08.
E06, E07, E09, E10 (owner 原) are left blank here: CHALLENGE full text is not in input/papers.

Usage: .venv/Scripts/python.exe -I R/py/15_params_v5.py <project_root>
"""
import sys, os
from copy import copy
sys.stdout.reconfigure(encoding="utf-8")
from openpyxl import load_workbook

root = sys.argv[1]
P = lambda *a: os.path.join(root, *a)
COLS = ["param_id", "区分", "項目", "適用する群", "適用する状態", "単位", "基本値", "下限", "上限",
        "価格の年度", "出典", "出典の該当箇所", "担当", "備考"]
INPUT_COLS = ["基本値", "下限", "上限", "価格の年度", "出典", "出典の該当箇所", "備考"]
G_NO_PEMBRO = "化学療法のみの群（運動を加えた群を含む）"
G_PEMBRO = "ペムブロリズマブを含む群（運動を加えた群を含む）"
F01_ITEM = "gBRCA 陰性の non-pCR 例でのカペシタビン使用割合"
F04_ITEM = "gBRCA 陽性の non-pCR 例でのオラパリブ使用割合（カペシタビンは併用しない）"
F25_NOTE = "群によらず共通。ペムブロリズマブと併用するときに投与期間が変わる場合は備考に"
E_ROWS = [  # param_id, 項目, 適用する群, 単位, 担当
    ("E06", "筋骨格系有害事象の発現率（運動を加えた群）", "運動を含む群", "割合（0から1）", "原"),
    ("E07", "筋骨格系有害事象の発現率（運動を加えない群）", "運動を含まない群", "割合（0から1）", "原"),
    ("E08", "筋骨格系有害事象の1件あたりの管理費用", "全群", "円/件", "尾崎"),
    ("E09", "3級以上の筋骨格系有害事象の発現率（運動を加えた群）", "運動を含む群", "割合（0から1）", "原"),
    ("E10", "3級以上の筋骨格系有害事象の発現率（運動を加えない群）", "運動を含まない群", "割合（0から1）", "原"),
]
GUIDE_ROWS = [
    ("v1 との関係", "v1 に記入中の場合は、そのまま v1 でお送りください。追加した F01P、F04P、E08 だけを v2 に記入していただくか、値と出典をメールでお知らせいただければ結構です。"),
    ("F01 の定義", "F01 は gBRCA 陰性例の中での割合に定義を変えました。"),
]


def col_of(ws):
    hdr = [c.value for c in ws[1]]
    assert hdr == COLS, hdr
    return {h: i + 1 for i, h in enumerate(hdr)}


def row_of(ws, pid):
    hits = [r for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value == pid]
    assert len(hits) == 1, (pid, hits)
    return hits[0]


def copy_style(ws, src_row, dst_row):
    for c in range(1, len(COLS) + 1):
        s, d = ws.cell(src_row, c), ws.cell(dst_row, c)
        d.font, d.fill, d.border = copy(s.font), copy(s.fill), copy(s.border)
        d.alignment, d.number_format, d.protection = copy(s.alignment), s.number_format, copy(s.protection)


def insert_after(ws, pid, values, style_pid):
    """Insert one row after the row of pid; values = dict column -> value; style from style_pid's row."""
    r = row_of(ws, pid) + 1
    ws.insert_rows(r)
    copy_style(ws, row_of(ws, style_pid), r)
    for k, v in values.items():
        ws.cell(r, col_of(ws)[k]).value = v
    return r


def edit(ws, pid, **kw):
    r, cm = row_of(ws, pid), col_of(ws)
    for k, v in kw.items():
        ws.cell(r, cm[k]).value = v


def apply(path_in, path_out, internal):
    wb = load_workbook(path_in)
    ws = wb["パラメータ"]
    cm = col_of(ws)
    n0 = ws.max_row
    owner = lambda pid: ws.cell(row_of(ws, pid), cm["担当"]).value
    oz_style, hara_style = "F01", "F07"
    assert owner(oz_style) == "尾崎" and owner(hara_style) == "原"
    yellow = ws.cell(row_of(ws, oz_style), cm["基本値"]).fill.fgColor.rgb
    for pid in ("F01", "F02", "F04", "F05", "F06"):  # rows edited here are blank in both sheets
        assert all(ws.cell(row_of(ws, pid), cm[k]).value in (None, "") for k in INPUT_COLS), pid
    edit(ws, "F01", 項目=F01_ITEM, 適用する群=G_NO_PEMBRO)
    edit(ws, "F04", 項目=F04_ITEM, 適用する群=G_NO_PEMBRO)
    edit(ws, "F02", 適用する群="全群", 備考=F25_NOTE)
    edit(ws, "F05", 適用する群="全群", 備考=F25_NOTE)
    edit(ws, "F06", 適用する群="全群", 適用する状態="診断時（全例）", 備考="診断時に全例で検査する前提")
    # bottom-up so that the rows found by param_id stay valid
    for pid, item in (("F04", F04_ITEM), ("F01", F01_ITEM)):
        src = {k: ws.cell(row_of(ws, pid), cm[k]).value for k in ("区分", "適用する状態", "単位")}
        insert_after(ws, pid, dict(param_id=pid + "P", 項目=item, 適用する群=G_PEMBRO, 担当="尾崎",
                                   備考="臨床の先生に確認中", **src), oz_style)
    e_src = {k: ws.cell(row_of(ws, "E01"), cm[k]).value for k in ("区分", "適用する状態")}
    prev = "E05"
    for pid, item, grp, unit, ow in E_ROWS:
        v = dict(param_id=pid, 項目=item, 適用する群=grp, 単位=unit, 担当=ow, **e_src)
        if internal and ow == "原":
            v["備考"] = "未記入：CHALLENGE（Courneya et al., N Engl J Med 2025）の全文が input/papers にない"
        insert_after(ws, prev, v, oz_style if ow == "尾崎" else hara_style)
        prev = pid
    n1 = ws.max_row
    assert n1 == n0 + 7
    # the validation list on 担当 and the filter cover the new rows
    for dv in ws.data_validations.dataValidation:
        if str(dv.sqref).startswith("M2:"):
            dv.sqref = __import__("openpyxl").worksheet.cell_range.MultiCellRange(f"M2:M{n1}")
    ws.auto_filter.ref = f"A1:N{n1}"
    # yellow only on 尾崎 rows
    for r in range(2, n1 + 1):
        is_oz = ws.cell(r, cm["担当"]).value == "尾崎"
        for k in INPUT_COLS:
            f = ws.cell(r, cm[k]).fill
            has_y = f.fill_type is not None and f.fgColor.rgb == yellow
            assert has_y == is_oz, (ws.cell(r, 1).value, k)
    # guide (sheet for Ozaki only): two rows after the last line of the first block
    g = wb["記入の手引き"]
    last = max(r for r in range(1, g.max_row + 1) if g.cell(r, 1).value == "確率分布")
    for i, (a, b) in enumerate([] if internal else GUIDE_ROWS):
        g.insert_rows(last + 1 + i)
        for c, v in ((1, a), (2, b)):
            s, d = g.cell(last, c), g.cell(last + 1 + i, c)
            d.value = v
            d.font, d.fill, d.border, d.alignment = copy(s.font), copy(s.fill), copy(s.border), copy(s.alignment)
    wb.save(path_out)
    ids = [ws.cell(r, 1).value for r in range(2, n1 + 1)]
    assert len(ids) == len(set(ids))
    print(f"{os.path.basename(path_in)} ({n0 - 1} rows) -> {os.path.basename(path_out)} ({n1 - 1} rows)")


apply(P("input", "params", "archive", "parameters_template_v1.xlsx"),
      P("input", "params", "parameters_template_v2.xlsx"), internal=False)
v4 = P("input", "params", "parameters_v4.xlsx")
if not os.path.exists(v4):  # moved to archive/ after v5 was made (git mv)
    v4 = P("input", "params", "archive", "parameters_v4.xlsx")
apply(v4, P("input", "params", "parameters_v5.xlsx"), internal=True)
