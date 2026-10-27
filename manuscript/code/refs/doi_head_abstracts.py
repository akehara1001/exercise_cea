"""doi.org test of the DOIs that have no PubMed record (crossref_meta.json).

verify_doi.py tests the DOIs of pubmed_meta.json and its EXTRA list; the meeting
abstracts formatted from Crossref are tested here the same way: HEAD request at
doi.org, the DOI must redirect (HTTP 30x) to a publisher URL. Writes
doi_head_abstracts.json and prints one line per DOI.
"""
import datetime
import json
import pathlib
import sys
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "ref-check (mailto:akehara1001@gmail.com)"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


opener = urllib.request.build_opener(NoRedirect)
out = {}
for k, v in json.load(open(HERE / "crossref_meta.json", encoding="utf-8")).items():
    req = urllib.request.Request("https://doi.org/" + v["doi"], headers=UA, method="HEAD")
    try:
        r = opener.open(req, timeout=40)
        status, loc = r.status, r.headers.get("Location")
    except urllib.error.HTTPError as e:
        status, loc = e.code, e.headers.get("Location")
    out[k] = dict(doi=v["doi"], doi_org_status=status, doi_org_location=loc, date=datetime.date.today().isoformat())
    print(k, v["doi"], status, loc)
json.dump(out, open(HERE / "doi_head_abstracts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
