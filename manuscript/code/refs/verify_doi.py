"""Resolve every DOI in pubmed_meta.json (and EXTRA) at doi.org and Crossref, and compare
first author, year, journal, volume, issue and first page with the PubMed record.

doi.org: HEAD request, the DOI must redirect (HTTP 30x) to a publisher URL.
Crossref: /works/<doi> metadata. Writes doi_check.json and prints one line per DOI.
"""
import json
import pathlib
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "ref-check (mailto:akehara1001@gmail.com)"}
EXTRA = {
    # meeting abstract of the KEYNOTE-522 final analysis (7-year values), not in PubMed
    "kn522final2026": "10.1200/JCO.2026.44.16_suppl.507",
}


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)


def resolve(doi):
    url = "https://doi.org/" + urllib.parse.quote(doi, safe="/()._;:-")
    req = urllib.request.Request(url, method="HEAD", headers=UA)

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    op = urllib.request.build_opener(NoRedirect)
    try:
        r = op.open(req, timeout=30)
        return r.status, r.headers.get("Location", "")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location", "")


def crossref(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return json.loads(r.read())["message"]
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2)
        except Exception:  # noqa: BLE001
            time.sleep(2)
    return None


meta = json.load(open(HERE / "pubmed_meta.json", encoding="utf-8"))
items = {k: v["doi"] for k, v in meta.items() if v.get("doi")}
items.update(EXTRA)
out = {}
for k, doi in items.items():
    st, loc = resolve(doi)
    cr = crossref(doi)
    time.sleep(0.3)
    rec = dict(doi=doi, doi_org_status=st, doi_org_location=loc)
    if cr:
        a0 = (cr.get("author") or [{}])[0]
        yr = None
        for f in ("published-print", "published-online", "issued"):
            if cr.get(f, {}).get("date-parts"):
                yr = cr[f]["date-parts"][0][0]
                break
        rec.update(cr_title=(cr.get("title") or [""])[0], cr_first_author=a0.get("family", a0.get("name", "")),
                   cr_year=yr, cr_issued=cr.get("issued", {}).get("date-parts", [[None]])[0],
                   cr_journal=(cr.get("container-title") or [""])[0], cr_short=(cr.get("short-container-title") or [""])[0],
                   cr_volume=cr.get("volume", ""), cr_issue=cr.get("issue", ""), cr_page=cr.get("page", cr.get("article-number", "")),
                   cr_type=cr.get("type"), cr_updates=[u.get("type") for u in cr.get("update-to", [])] + [u.get("type") for u in cr.get("relation", {}).get("is-retracted-by", [])])
    m = meta.get(k)
    checks = {}
    if m and cr:
        checks["first_author"] = norm(m["authors"][0].split(" ")[0]) == norm(rec["cr_first_author"]) if m["authors"] else None
        checks["title"] = norm(m["title"]).rstrip()[:40] == norm(rec["cr_title"])[:40]
        checks["volume"] = (m["volume"] or "") == (rec["cr_volume"] or "")
        checks["issue"] = norm(m["issue"]) == norm(rec["cr_issue"]) if m["issue"] or rec["cr_issue"] else True
        pg = (m["pages"] or "").split("-")[0]
        checks["first_page"] = norm(pg) == norm(str(rec["cr_page"]).split("-")[0]) if pg or rec["cr_page"] else True
        checks["year_any"] = str(m["year"]) in {str(x) for x in [rec["cr_year"]] + [rec["cr_issued"][0] if rec["cr_issued"] else None]}
    rec["checks"] = checks
    out[k] = rec
    flag = "OK" if (st in (301, 302, 303, 307, 308) and cr and all(v in (True, None) for v in checks.values())) else "CHECK"
    print(f"{flag} {k}: doi.org {st} | CR {rec.get('cr_first_author','-')} {rec.get('cr_year','-')} {rec.get('cr_short') or rec.get('cr_journal','-')} "
          f"{rec.get('cr_volume','')}({rec.get('cr_issue','')}):{rec.get('cr_page','')} | {checks}")
json.dump(out, open(HERE / "doi_check.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
