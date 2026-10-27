"""Results v4: direct edit of results_v3.docx (WRITING_RULES 1.2 rule 2).

Opens the previous version from manuscript/archive/<PREV>/, changes only the
sentences listed in EDITS, and saves results_<VER>.docx. The sentence ledger of
the previous version (_build/_ledger_results_<PREV>.json) is carried over: it
must match the previous docx word for word, and every number it maps must still
be shown at the same place in the current registries. New sentences take their
numbers from the registries, as in make_results.py. Writes
_build/_ledger_results.json (read by make_ledger.py) and a copy
_build/_ledger_results_<VER>.json.
"""
from __future__ import annotations

import copy
import json
import re
import sys

from docx import Document

from common import ARCHIVE_PREV, BUILD, OUT, PREV, VER

sys.stdout.reconfigure(encoding="utf-8")
if VER != "v4":
    raise SystemExit("edit_results.py holds the edits of v4 only; write the next version's edits on results_v4.docx")

REGS = {name: json.load(open(BUILD / f"_ledger_{name}.json", encoding="utf-8")) for name in ("tables", "supplement", "figures")}
base = json.load(open(BUILD / f"_ledger_results_{PREV}.json", encoding="utf-8"))


def V(reg, where, idx=0):
    rows = [x for x in REGS[reg]["rows"] if x["where"] == where]
    if len(rows) <= idx:
        raise KeyError(f"{reg}: no entry {idx} for {where!r}")
    return rows[idx]


def rng(reg, pattern):
    """Smallest and largest shown value among entries whose where matches pattern (HR-type values)."""
    rows = [x for x in REGS[reg]["rows"] if re.fullmatch(pattern, x["where"])]
    vals = sorted(rows, key=lambda x: float(x["shown"].replace("−", "-").replace(",", "")))
    return rows, vals[0], vals[-1]


# the previous docx and its ledger must agree
doc = Document(ARCHIVE_PREV / f"results_{PREV}.docx")
body = [p for p in doc.paragraphs if p.text.strip()]
assert body[0].text == "Results"
assert [p.text for p in body[1:]] == [" ".join(s["text"] for s in ps) for ps in base["paragraphs"]], "ledger of the previous version does not match its docx"
# every number of the previous version must still be shown at the same place
for u in base["used"]:
    shown = {x["shown"] for x in REGS[u["registry"]]["rows"] if x["where"] == u["where"]}
    assert u["shown"] in shown, ("value no longer in the registry", u)

# ---------------------------------------------------------------- the edits of v4
# Supplementary Table S10, Elmore row: progression during neoadjuvant therapy is the same with and
# without exercise, so the Results report only its ICER of pembrolizumab and leave it out of the
# exercise range (instruction "v4 的补充", 2026-10-26).
S10_CAP = r"Supplementary Table S10, (?!elmore,)([a-z_]+), main, cap_eq_programme"
rows, lo, hi = rng("supplement", S10_CAP)
assert sorted({re.fullmatch(S10_CAP, x["where"]).group(1) for x in rows}) == ["sjp", "utility_au", "utility_jp", "utility_uk", "utility_us"]
EDITS = {  # (paragraph, sentence) of the previous version -> new sentences in its place
    (10, 5): [("With the four utility scenarios and Japanese post-operative treatment, this cost equaled the fee-schedule-based program cost at HRs of {a} to {b} "
               "(Supplementary Table S10).",
               {"a": ("supplement", lo["where"], 0), "b": ("supplement", hi["where"], 0)}, ["Supplementary Table S10"]),
              ("With longer survival after progression during neoadjuvant therapy, the ICER of pembrolizumab was JPY {a} thousand per QALY (Supplementary Table S10).",
               {"a": ("supplement", "Supplementary Table S10, elmore, ICER", 0)}, ["Supplementary Table S10"])],
}
OLD = {(10, 5): "Across the six scenarios in this table, the HR at which the maximum affordable cost equaled the cost of the fee-schedule-based program ranged from "
                "0.988 to 0.989 (Supplementary Table S10)."}

paras, used, changed = [], [], []
for pi, ps in enumerate(base["paragraphs"], start=1):
    out = []
    for si, s in enumerate(ps, start=1):
        if (pi, si) in EDITS:
            assert s["text"] == OLD[(pi, si)], ("sentence to replace has changed", pi, si, s["text"])
            for tpl, keys, cites in EDITS[(pi, si)]:
                vals = {}
                for k, (reg, where, idx) in keys.items():
                    e = V(reg, where, idx)
                    vals[k] = e["shown"]
                    used.append(dict(paragraph=pi, sentence=len(out) + 1, placeholder=k, registry=reg, where=where, shown=e["shown"], source=e["source"], loc=e["loc"]))
                out.append(dict(text=tpl.format(**vals), cites=cites, keys=list(keys)))
            changed.append(pi)
            continue
        new_si = len(out) + 1
        for u in base["used"]:
            if u["paragraph"] == pi and u["sentence"] == si:
                used.append({**u, "sentence": new_si})
        out.append(copy.deepcopy(s))
    paras.append(out)

for pi in sorted(set(changed)):
    p = body[pi]
    assert len(p.runs) == 1, ("paragraph has more than one run; edit by hand", pi)
    p.runs[0].text = " ".join(s["text"] for s in paras[pi - 1])
doc.save(OUT / f"results_{VER}.docx")
led = {"paragraphs": paras, "used": used, "base": f"results_{PREV}.docx", "changed_paragraphs": sorted(set(changed))}
for name in ("_ledger_results.json", f"_ledger_results_{VER}.json"):
    json.dump(led, open(BUILD / name, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
words = [sum(len(s["text"].split()) for s in ps) for ps in paras]
print(f"results_{VER}.docx written from results_{PREV}.docx; changed paragraphs {sorted(set(changed))}; words {words} (total {sum(words)}); numbers {len(used)}")
for pi in sorted(set(changed)):
    for s in paras[pi - 1]:
        print(f"  P{pi}: [{len(s['text'].split())} words] {s['text']}")
