"""Page of each manuscript paragraph, for the locations in the CHEERS checklist.

Runs word_pages.ps1 (Word COM, read-only) on manuscript/<VER>/manuscript_<VER>.docx and
maps Word's paragraphs to the paragraph ids of _build/_manuscript_map.json (same
order: the manuscript has no tables and no empty paragraphs). Writes
_build/_manuscript_pages.json with the start page of each id; make_supplement.py reads it.
"""
import json
import subprocess
import sys

from common import BUILD, OUT, VER

sys.stdout.reconfigure(encoding="utf-8")
raw = BUILD / "_word_pages_raw.json"
subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(BUILD.parent / "word_pages.ps1"),
                "-src", str(OUT / f"manuscript_{VER}.docx"), "-out", str(raw)], check=True, timeout=600)
w = json.loads(raw.read_text(encoding="utf-8-sig"))
mm = json.load(open(BUILD / "_manuscript_map.json", encoding="utf-8"))
paras = w["paragraphs"]
by_id = {}
for k, item in enumerate(mm["order"]):
    p = paras[k]
    head = item["text"][:20]
    assert p["text"].startswith(head[:12]), (k, p["text"][:30], head)
    if item["id"]:
        by_id[item["id"]] = p["start_page"]
json.dump(dict(pages=w["pages"], by_id=by_id, manuscript_sha256_before_numbering=mm["manuscript_sha256"]),
          open(BUILD / "_manuscript_pages.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("pages:", w["pages"], "|", ", ".join(f"{k} p.{v}" for k, v in by_id.items()))
