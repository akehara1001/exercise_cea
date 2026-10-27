"""Shared helpers for the manuscript tables and figures (manuscript step 1).

Reads the phase 1 and phase 2 outputs only; nothing here runs the model.
Every number shown in a table or figure is passed through Registry.r(), which
records the displayed string, where it is shown, the source file, the location
in that file and the raw value. The ledger (numbers_ledger_<VER>.md) is written
from the registry.
"""
from __future__ import annotations

import hashlib
import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import openpyxl
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
MAIN = ROOT / "output" / "phase2" / "main"
P1 = ROOT / "output" / "phase1"
VER = "v9"  # version written by this run; earlier versions are in manuscript/archive/
PREV = "v8"
BASE = "v8（manuscript/archive/v8/ 的交付物与同一套生成代码；本文 manuscript_v9.docx 由 manuscript_v8.docx 直接编辑而成）"
STEP = "v9：最后的修改（Implications、D.3、D.5、标题、Abstract）"
OUT = ROOT / "manuscript" / VER
ARCHIVE_PREV = ROOT / "manuscript" / "archive" / PREV
FIGDIR = OUT / "figures"
BUILD = ROOT / "manuscript" / "code" / "_build"  # registry json (intermediate, not a deliverable)
BUILD.mkdir(parents=True, exist_ok=True)
PARAMS_XLSX = ROOT / "input" / "params" / "parameters_v10.xlsx"

# Supplementary numbering by first citation in the text (Introduction, Methods,
# Results; table_figure_plan_<VER>.md section 4). Change here only; the tables,
# legends and the manuscript edit read these labels.
SUPP = {
    "cheers": "S1",            # CHEERS 2022 checklist (Methods, Study background)
    "params": "S2",            # all inputs (Methods, Variables)
    "methods_survival": "S1",  # Supplementary Methods S1: literature searches (Introduction paragraph 3, from v6), survival model, validation, PSA sampling
    "fig_validation": "S1",    # Supplementary Fig. S1: model OS/EFS vs reconstructed KM and final analysis (stage 1)
    "validation": "S3",        # Supplementary Table S3: validation values (stage 1)
    "capgrid": "S4",           # Results P1: data of Fig. 2 (HR grid, both thresholds, early-recurrence scenario)
    "pathB": "S5",             # Results P2 (v7; P1 until v6): effect on pCR (path B)
    "decomp": "S6",            # Results P2: incremental costs by category, main comparison, HR 0.85
    "duration": "S7",          # Results P3: effect duration and post-operative continuation, full grid
    "netbenefit": "S8",        # Results P5: one-year cohort net benefit (JBCS registry report no. 55)
    "oneway": "S9",            # Results P10: values of Fig. 3 and Supplementary Fig. S2
    "fig_icer": "S2",          # Supplementary Fig. S2: one-way analysis of the reference ICER (Methods stage 4)
    "other": "S10",            # Results P10: utility value sets (Japan first), Elmore, S-JP
}
# v4 -> v5 renumbering of supplementary tables (old -> new), used to carry the v4
# Results text and its ledger over to the v5 numbering
SUPP_RENUMBER_V4_V5 = {"S1": "S2", "S2": "S3", "S5": "S6", "S6": "S7", "S7": "S8", "S8": "S5"}
# previous version -> this version (compare_versions.py); v5 -> v6 and v6 -> v7 keep every supplementary number
SUPP_RENUMBER_PREV: dict[str, str] = {}

MINUS = "−"
STAR = "✳"  # footnote symbol; repeated for later footnotes


def rel(p: Path) -> str:
    p = p.resolve()
    return p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix()


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---------------------------------------------------------------- rounding

def _half_up(x: float, nd: int) -> Decimal:
    q = Decimal(1).scaleb(-nd)
    return Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP)


def fnum(x: float, nd: int, comma: bool = True) -> str:
    """Round half up once from the raw value; minus sign U+2212; no '-0'."""
    d = _half_up(x, nd)
    if d == 0:
        d = abs(d)
    s = f"{d:,.{nd}f}" if comma else f"{d:.{nd}f}"
    return s.replace("-", MINUS)


def fk(yen: float) -> str:
    """JPY to JPY 1,000 (integer), the precision of the 0.1 x 10,000 yen reports."""
    return fnum(yen / 1000.0, 0)


def fyen(yen: float) -> str:
    return fnum(yen, 0)


def pct(p: float, nd: int = 1) -> str:
    return fnum(100.0 * p, nd)


# ---------------------------------------------------------------- registry

class Registry:
    def __init__(self) -> None:
        self.rows: list[dict] = []
        self.labels: list[dict] = []

    def r(self, shown: str, where: str, source: str, loc: str, raw) -> str:
        self.rows.append(dict(shown=shown, where=where, source=source, loc=loc, raw=raw))
        return shown

    def label(self, token: str, where: str, reason: str) -> str:
        """Numbers that are names or definitions (e.g. 'KEYNOTE-522', 'Table S1')."""
        self.labels.append(dict(shown=token, where=where, reason=reason))
        return token

    def shown_set(self) -> set[str]:
        return {x["shown"] for x in self.rows} | {x["shown"] for x in self.labels}


# numeric tokens that a reader would take as a value; numbers glued to letters
# (E01, S1, EQ-5D, 2.5th) are identifiers and are not extracted
NUM_RE = re.compile(r"(?<![A-Za-z0-9.,\-−])[−]?\d[\d,]*(?:\.\d+)?(?![A-Za-z0-9]|\.\d)")


def num_tokens(text: str) -> list[str]:
    out = []
    for m in NUM_RE.finditer(text):
        t = m.group(0).rstrip(",")
        out.append(t)
    return out


# ---------------------------------------------------------------- sources

def csv(name: str, base: Path = MAIN) -> pd.DataFrame:
    return pd.read_csv(base / name)


def one(df: pd.DataFrame, **kw) -> pd.Series:
    m = pd.Series(True, index=df.index)
    for k, v in kw.items():
        if isinstance(v, float):
            m &= (df[k] - v).abs() < 1e-9
        else:
            m &= df[k] == v
    sub = df[m]
    if len(sub) != 1:
        raise ValueError(f"expected one row for {kw}, got {len(sub)}")
    return sub.iloc[0]


def loc_of(file: str, **kw) -> str:
    return file + " (" + ", ".join(f"{k} = {v}" for k, v in kw.items()) + ")"


class Params:
    """parameters_v10.xlsx, sheet パラメータ (read-only, cached values)."""

    COLS = {"base": "G", "low": "H", "high": "I", "note": "N", "item": "C", "scenario": "O"}

    def __init__(self) -> None:
        wb = openpyxl.load_workbook(PARAMS_XLSX, data_only=True)
        self.ws = wb["パラメータ"]
        self.sc = wb["シナリオ"]
        self.row = {}
        for i, r in enumerate(self.ws.iter_rows(min_row=1, values_only=True), start=1):
            if r[0]:
                self.row[r[0]] = i

    def get(self, pid: str, field: str = "base"):
        col = self.COLS[field]
        i = self.row[pid]
        return self.ws[f"{col}{i}"].value, f"{rel(PARAMS_XLSX)} sheet パラメータ cell {col}{i} ({pid})"

    def scenario(self, scen: str, pid: str):
        for i, r in enumerate(self.sc.iter_rows(min_row=1, values_only=True), start=1):
            if r[0] == scen and r[1] == pid:
                return r[4], r[5], f"{rel(PARAMS_XLSX)} sheet シナリオ row {i} ({scen}, {pid}; E = scenario value, F = multiplier)"
        raise KeyError((scen, pid))
