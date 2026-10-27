"""Crossref records of the cited works that have no PubMed record (meeting abstracts).

Writes crossref_meta.json: authors (family, given), title, journal, volume, issue,
page and issued date as Crossref returns them. references.py formats these entries
from this file.
"""
import json
import pathlib
import sys
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "ref-check (mailto:akehara1001@gmail.com)"}
DOIS = {"kn522final2026": "10.1200/JCO.2026.44.16_suppl.507", "ohtera2018": "10.1016/j.jval.2018.07.458", "esmo2023": "10.1016/j.annonc.2023.10.008"}

out = {}
for k, doi in DOIS.items():
    with urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe=""), headers=UA), timeout=40) as r:
        m = json.loads(r.read())["message"]
    out[k] = dict(doi=doi, authors=[(a.get("family", ""), a.get("given", "")) for a in m.get("author", [])], title=(m.get("title") or [""])[0],
                  journal=(m.get("container-title") or [""])[0], volume=m.get("volume", ""), issue=m.get("issue", ""), page=m.get("page", ""),
                  issued=m.get("issued", {}).get("date-parts", [[None]])[0], type=m.get("type"))
    print(k, out[k]["authors"][:3], out[k]["journal"], out[k]["volume"], out[k]["issue"], out[k]["page"], out[k]["issued"])
json.dump(out, open(HERE / "crossref_meta.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
