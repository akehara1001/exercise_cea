"""Retraction screening of every cited DOI (ARS citation_compliance_agent, section 5).

For each DOI in doi_check.json and crossref_meta.json: Crossref 'update-to' and
'relation' entries (corrections, retractions, expressions of concern) and the
OpenAlex 'is_retracted' flag. Writes retraction_check.json and prints one line per DOI.
"""
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "ref-check (mailto:akehara1001@gmail.com)"}


def get(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return json.loads(r.read())
        except Exception:  # noqa: BLE001
            time.sleep(2 + i)
    return None


dois = {k: v["doi"] for k, v in json.load(open(HERE / "doi_check.json", encoding="utf-8")).items()}
dois.update({k: v["doi"] for k, v in json.load(open(HERE / "crossref_meta.json", encoding="utf-8")).items()})
out = {}
for k, doi in sorted(dois.items()):
    cr = get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe=""))
    m = cr["message"] if cr else {}
    upd = [dict(type=u.get("type"), doi=u.get("DOI")) for u in m.get("update-to", [])]
    rel = {t: [x.get("id") for x in v] for t, v in m.get("relation", {}).items() if t in ("is-retracted-by", "has-retraction", "is-corrected-by", "has-correction", "has-expression-of-concern")}
    oa = get("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi, safe="/"))
    out[k] = dict(doi=doi, crossref_ok=bool(cr), crossref_update_to=upd, crossref_relations=rel,
                  openalex_ok=bool(oa), openalex_is_retracted=(oa or {}).get("is_retracted"))
    print(k, doi, "| CR", "ok" if cr else "FAIL", upd or "", rel or "", "| OpenAlex retracted:", out[k]["openalex_is_retracted"])
    time.sleep(0.2)
json.dump(out, open(HERE / "retraction_check.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("retracted (OpenAlex):", [k for k, v in out.items() if v["openalex_is_retracted"]], "| Crossref retraction relations:",
      [k for k, v in out.items() if any("retract" in t for t in v["crossref_relations"])])
