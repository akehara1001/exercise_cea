"""Public input sheet (2026-10-29, manuscript v12 instruction step 3; v13 step 3): from
input/params/parameters_v10.xlsx, writes <public_root>/input/params/parameters_v10.xlsx (same file name, so the code
paths stay) without personal names and working notes.
  (a) only the sheets パラメータ and シナリオ are kept (記入の手引き and 計算根拠_原 are deleted).
  (b) パラメータ: columns and their order unchanged (R/10_read_params.R checks the names). param_id, 区分, 項目,
      適用する群, 適用する状態, 単位, 基本値, 下限, 上限, 価格の年度 and シナリオ値 as they are. 出典 = the Source of the
      row with the same Code in Supplementary Table S2, part B, of Online Resource 1 (English, with the reference
      numbers); the script stops if a param_id has no such row. 出典の該当箇所 and 担当 emptied. 備考 = only the one
      marker that rule_of() in R/10_read_params.R needs for the range rule (the first in RANGE_NOTE order where
      there are several), with "幅は原が設定（基本値 ±25%）" written as "幅の規則：±25%"; all other text removed.
      U01-U05 (v13): 備考 = only what R/22_phase2b_main.R reads from it, "期間 <n> 週" (U05; line 35) and the US, UK
      and Australian utility values (util_set()), as "[期間 <n> 週、]米国 <x>、英国 <y>、豪州 <z>"; these rows carry no
      range marker. The values are the strings the R patterns take from the internal note (checked both ways).
  (c) シナリオ: column 根拠 of sc_metcost50 and sc_eribulin = one English sentence in the words of Table 1 of the
      tables file; the other columns unchanged.
  (d) workbook properties (creator, last modified by, company, title) emptied; comments, hidden sheets and defined
      names that point to a deleted sheet removed; all data validations removed (v13; the 担当 list on M2:M82).
The range rule given by the public 備考 is checked against the internal sheet for every row.

Usage: .venv/Scripts/python.exe -I R/py/26_public_params.py <project_root> <public_root> [<ESM docx> <tables docx>]
       (default: manuscript/v13/ESM_1_v13.docx and manuscript/v13/tables_v13_BCRT.docx)
"""
import sys, os, re, zipfile, hashlib
import xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding="utf-8")
from openpyxl import load_workbook

root, pub = sys.argv[1], sys.argv[2]
P = lambda *a: os.path.join(root, *a)
esm = sys.argv[3] if len(sys.argv) > 3 else P("manuscript", "v13", "ESM_1_v13.docx")
tables = sys.argv[4] if len(sys.argv) > 4 else P("manuscript", "v13", "tables_v13_BCRT.docx")
COLS = ["param_id", "区分", "項目", "適用する群", "適用する状態", "単位", "基本値", "下限", "上限",
        "価格の年度", "出典", "出典の該当箇所", "担当", "備考", "シナリオ値"]
# as in R/10_read_params.R (first match wins); the public sheet carries the value on the right
RANGE_NOTE = [("薬価固定", "幅の規則：薬価固定", "幅の規則：薬価固定"),
              ("0例：PSAは固定", "幅の規則：0例：PSAは固定", "幅の規則：0例：PSAは固定"),
              ("±25%", "幅は原が設定（基本値 ±25%）", "幅の規則：±25%"),
              ("片側対称", "片側を対称に補った", "片側を対称に補った")]
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
sha = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()


def docx_body(path):
    return ET.fromstring(zipfile.ZipFile(path).read("word/document.xml")).find(W + "body")


def text(el):
    return "".join(t.text or "" for t in el.iter(W + "t"))


def rows_of(tbl):
    out = []
    for tr in tbl.findall(W + "tr"):
        out.append([text(tc) for tc in tr.findall(W + "tc")])
    return out


def rule_of(note, k):   # k = 1: internal marker, 2: public marker
    for name, *m in RANGE_NOTE:
        if m[k - 1] in (note or ""):
            return name
    return ""


# the parts of 備考 that R/22_phase2b_main.R reads (as its patterns: sub(".*期間 ([0-9.]+) 週.*") and regexec())
def u_parts(note, pid):
    out = {}
    if pid == "U05":
        m = re.match(r".*期間 ([0-9.]+) 週", note or "", re.S)
        assert m, (pid, "期間")
        out["期間"] = m.group(1)
    for k in ("米国", "英国", "豪州"):
        m = re.search(k + r"[^0-9]*([0-9.]+)", note or "")
        assert m, (pid, k)
        out[k] = m.group(1)
    return out


def u_note(parts):
    head = f"期間 {parts['期間']} 週、" if "期間" in parts else ""
    return head + "、".join(f"{k} {parts[k]}" for k in ("米国", "英国", "豪州"))


# Supplementary Table S2, part B: Code -> Source
blocks = list(docx_body(esm))
i2 = [i for i, b in enumerate(blocks) if b.tag == W + "p" and text(b).startswith("Supplementary Table S2.")]
i3 = [i for i, b in enumerate(blocks) if b.tag == W + "p" and text(b).startswith("Supplementary Table S3.")]
assert len(i2) == 1 and len(i3) == 1
tb = [b for b in blocks[i2[0]:i3[0]] if b.tag == W + "tbl"]
assert len(tb) == 2
R = rows_of(tb[1])
assert R[0][0].startswith("B. ") and R[1] == ["Code", "Input", "Arms", "Unit", "Base case", "Range", "Distribution", "Source"], R[:2]
SRC = {}
for r in R[2:]:
    assert len(r) == 8 and r[0] not in SRC, r
    SRC[r[0]] = r[7]

# Table 1 of the tables file: the two scenario rows
T1 = rows_of([b for b in docx_body(tables) if b.tag == W + "tbl"][0])
def t1_row(label):
    hits = [r for r in T1 if r and r[0] == label]
    assert len(hits) == 1, label
    return hits[0]
m50 = t1_row("Metastatic treatment costs halved")
eri = t1_row("Eribulin-based later-line treatment")
assert m50[1:] == ["Monthly costs of first-line and later-line treatment of distant recurrence multiplied by 0.5", "—"], m50
assert eri[1:] == ["245,683 per month for second-line and later treatment", "EMBRACE dosing; national drug price list [8,68]"], eri
BASIS = {"sc_metcost50": f"{m50[0]}: {m50[1][0].lower()}{m50[1][1:]} (Table 1).",
         "sc_eribulin": f"{eri[0]}: {eri[1]} ({eri[2]}; Table 1)."}

src = P("input", "params", "parameters_v10.xlsx")
wb = load_workbook(src)
assert wb.sheetnames == ["パラメータ", "記入の手引き", "シナリオ", "計算根拠_原"], wb.sheetnames
# (a) and (d): deleted and hidden sheets, defined names pointing to them
drop = ["記入の手引き", "計算根拠_原"] + [ws.title for ws in wb.worksheets if ws.sheet_state != "visible"]
for name in list(wb.defined_names):
    if any(d in (wb.defined_names[name].attr_text or "") for d in drop):
        del wb.defined_names[name]
for ws in wb.worksheets:
    for name in list(ws.defined_names):
        if any(d in (ws.defined_names[name].attr_text or "") for d in drop):
            del ws.defined_names[name]
for d in dict.fromkeys(drop):
    del wb[d]
assert wb.sheetnames == ["パラメータ", "シナリオ"], wb.sheetnames

# (b) パラメータ
ws = wb["パラメータ"]
assert [c.value for c in ws[1]] == COLS, [c.value for c in ws[1]]
cm = {h: i + 1 for i, h in enumerate(COLS)}
n_rule = {}
U_IDS = [f"U0{i}" for i in range(1, 6)]
U_NOTES = {}
for r in range(2, ws.max_row + 1):
    pid = ws.cell(r, cm["param_id"]).value
    if pid is None:
        assert all(ws.cell(r, c).value is None for c in range(1, len(COLS) + 1)), r
        continue
    if pid not in SRC:
        sys.exit(f"STOP: param_id {pid} has no row in Supplementary Table S2, part B")
    ws.cell(r, cm["出典"]).value = SRC[pid]
    ws.cell(r, cm["出典の該当箇所"]).value = None
    ws.cell(r, cm["担当"]).value = None
    note = ws.cell(r, cm["備考"]).value
    rule = rule_of(note, 1)
    pub_note = dict((n, m2) for n, _, m2 in RANGE_NOTE).get(rule)
    if pid in U_IDS:
        assert rule == "" and "【要確認" not in (note or ""), pid
        parts = u_parts(note, pid)
        pub_note = u_note(parts)
        assert u_parts(pub_note, pid) == parts, pid
        U_NOTES[pid] = pub_note
    ws.cell(r, cm["備考"]).value = pub_note
    assert rule_of(pub_note, 2) == rule, pid
    n_rule[rule or "(none)"] = n_rule.get(rule or "(none)", 0) + 1
ids = [ws.cell(r, 1).value for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value]
assert sorted(ids) == sorted(SRC), "param_id and Table S2 part B differ"
assert sorted(U_NOTES) == U_IDS, sorted(U_NOTES)

# (c) シナリオ
sc = wb["シナリオ"]
hdr = [c.value for c in sc[1]]
assert hdr == ["シナリオ", "param_id", "項目", "基本値", "シナリオ値", "倍率（シナリオ値 ÷ 基本値）", "単位", "根拠"], hdr
for r in range(2, sc.max_row + 1):
    s = sc.cell(r, 1).value
    assert s in BASIS, s
    sc.cell(r, 8).value = BASIS[s]

# (d) comments, data validations and properties
n_comments = 0
n_dv = {}
for w in wb.worksheets:
    for row in w.iter_rows():
        for c in row:
            if c.comment is not None:
                c.comment = None; n_comments += 1
    n_dv[w.title] = [str(dv.sqref) for dv in w.data_validations.dataValidation]
    w.data_validations.dataValidation = []
p = wb.properties
p.creator = p.lastModifiedBy = p.title = None
p.subject = p.description = p.keywords = p.category = None
if hasattr(wb, "company"):
    wb.company = None

out = os.path.join(pub, "input", "params", "parameters_v10.xlsx")
os.makedirs(os.path.dirname(out), exist_ok=True)
wb.save(out)
print(f"source {src} sha256 {sha(src)[:16]}; Table S2 part B rows {len(SRC)}; rows {len(ids)}; "
      f"range markers {n_rule}; comments removed {n_comments}; data validations removed {n_dv}; sheets {wb.sheetnames}")
print("備考 U01-U05:", U_NOTES)
print("根拠:", BASIS)
print(f"written {out} sha256 {sha(out)[:16]}")
