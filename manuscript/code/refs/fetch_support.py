"""Source texts for checking the cited statements (claim_support.py).

Writes support_cache.json with
- crossref_abstract: the abstract text in the Crossref record of works without a PubMed abstract;
- affiliations: the author affiliations of the PubMed record (country and centre of a cohort);
- pmc: for each open-access full text used, the sha256 of the Europe PMC full-text XML. The XML itself is
  saved only to the directory given as the first argument (outside the repository) and is read from there by
  claim_support.py.
Usage: python fetch_support.py <fulltext_dir>
"""
import datetime
import hashlib
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "ref-check (mailto:akehara1001@gmail.com)"}
CROSSREF = {"kn522final2026": "10.1200/JCO.2026.44.16_suppl.507", "ohtera2018": "10.1016/j.jval.2018.07.458"}
AFFIL = ["fedele2026", "elmore2021", "grinda2023"]
PMC = {"khan2019": "PMC6548756", "gublergut2021": "PMC8521580", "favrebulle2024": "PMC10781656", "huang2023": "PMC9988745",
       "kwong2024": "PMC11333381", "iwatani2021": "PMC8535054"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
        return r.read()


out_dir = pathlib.Path(sys.argv[1])
out_dir.mkdir(parents=True, exist_ok=True)
pm = json.load(open(HERE / "pubmed_meta.json", encoding="utf-8"))
cache = {"date": datetime.date.today().isoformat(), "crossref_abstract": {}, "affiliations": {}, "pmc": {}}
for k, doi in CROSSREF.items():
    m = json.loads(get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")))["message"]
    a = m.get("abstract") or ""
    cache["crossref_abstract"][k] = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", a)).strip()
    print(k, len(cache["crossref_abstract"][k]), "characters")
    time.sleep(0.5)
ids = ",".join(pm[k]["pmid"] for k in AFFIL)
x = get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&email=akehara1001@gmail.com&id={ids}").decode("utf-8")
for art in re.findall(r"<PubmedArticle>.*?</PubmedArticle>", x, re.S):
    pmid = re.search(r"<PMID[^>]*>(\d+)", art).group(1)
    k = next(k for k in AFFIL if pm[k]["pmid"] == pmid)
    cache["affiliations"][k] = sorted(set(re.sub(r"\s+", " ", a) for a in re.findall(r"<Affiliation>(.*?)</Affiliation>", art)))
    print(k, len(cache["affiliations"][k]), "affiliations")
for k, pmc in PMC.items():
    b = get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/fullTextXML")
    (out_dir / f"{pmc}.xml").write_bytes(b)
    cache["pmc"][k] = {"pmcid": pmc, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    print(k, pmc, len(b), "bytes")
    time.sleep(0.5)
json.dump(cache, open(HERE / "support_cache.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
