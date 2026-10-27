"""Literature searches for manuscript step 3 (stage 1 of the writing chain).

Runs each query in PubMed (NCBI E-utilities) and Europe PMC (REST API), saves the
hits (id, title, year, journal, DOI) to search_<key>.json and prints the counts.
Usage: python lit_search.py <key> [<key> ...]   (no key = all)
"""
import datetime
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
EMAIL = "akehara1001@gmail.com"

EX = '(exercise[tiab] OR "physical activity"[tiab] OR "Exercise"[mh] OR "Exercise Therapy"[mh] OR prehabilitation[tiab] OR "aerobic training"[tiab] OR "resistance training"[tiab])'
BC = '("Breast Neoplasms"[mh] OR "breast cancer"[tiab] OR "breast carcinoma"[tiab])'
NAC = '(neoadjuvant[tiab] OR preoperative[tiab] OR "Neoadjuvant Therapy"[mh])'
ECON = '("cost-effectiveness"[tiab] OR "cost effectiveness"[tiab] OR "cost-utility"[tiab] OR "cost utility"[tiab] OR "economic evaluation"[tiab] OR QALY*[tiab] OR "Cost-Benefit Analysis"[mh])'
YRS = '("2000/01/01"[dp] : "2026/12/31"[dp])'

E_EX = '(exercise OR "physical activity" OR prehabilitation OR "aerobic training" OR "resistance training")'
E_BC = '("breast cancer" OR "breast neoplasms" OR "breast carcinoma")'
E_NAC = '(neoadjuvant OR preoperative)'
E_ECON = '("cost-effectiveness" OR "cost effectiveness" OR "cost-utility" OR "cost utility" OR "economic evaluation" OR QALY OR "quality-adjusted life year")'
E_YRS = 'PUB_YEAR:[2000 TO 2026]'

Q = {
    # novelty: economic evaluation of exercise during neoadjuvant therapy for breast cancer
    "novelty": (f"{EX} AND {NAC} AND {BC} AND {ECON} AND {YRS}",
                f"{E_EX} AND {E_NAC} AND {E_BC} AND {E_ECON} AND {E_YRS}"),
    # spelling variants: (neo)adjuvant, neo-adjuvant, during treatment, any cancer
    "novelty_variants": (f"{EX} AND (cancer[tiab] OR \"Neoplasms\"[mh]) AND (\"neo adjuvant\"[tiab] OR neo-adjuvant[tiab] OR \"(neo)adjuvant\"[tiab] OR neoadjuvant[tiab] OR \"during treatment\"[tiab] OR \"during oncological treatment\"[tiab]) AND {ECON} AND {YRS}",
                         f"{E_EX} AND cancer AND (\"neo-adjuvant\" OR \"(neo)adjuvant\" OR neoadjuvant OR \"during treatment\" OR \"during oncological treatment\") AND {E_ECON} AND {E_YRS}"),
    # broader: economic evaluation of exercise during chemotherapy for breast cancer
    "novelty_chemo": (f"{EX} AND {BC} AND (chemotherapy[tiab] OR \"Antineoplastic Agents\"[mh]) AND {ECON} AND {YRS}",
                      f"{E_EX} AND {E_BC} AND chemotherapy AND {E_ECON} AND {E_YRS}"),
    # systematic reviews of economic evaluations of exercise in cancer
    "econ_reviews": (f"{EX} AND (\"Neoplasms\"[mh] OR cancer[tiab]) AND {ECON} AND (systematic[sb] OR \"systematic review\"[tiab]) AND {YRS}",
                     f"{E_EX} AND cancer AND {E_ECON} AND \"systematic review\" AND {E_YRS}"),
    # exercise during neoadjuvant chemotherapy and pathological complete response
    "nac_pcr": (f"{EX} AND {NAC} AND {BC} AND (\"pathologic complete response\"[tiab] OR \"pathological complete response\"[tiab] OR pCR[tiab] OR \"tumor response\"[tiab] OR \"tumour response\"[tiab]) AND {YRS}",
                f"{E_EX} AND {E_NAC} AND {E_BC} AND (\"pathologic complete response\" OR \"pathological complete response\" OR pCR OR \"tumor response\") AND {E_YRS}"),
    # exercise during (neo)adjuvant chemotherapy for breast cancer: randomized trials with recurrence or survival
    "chemo_rct_survival": (f"{EX} AND {BC} AND chemotherapy[tiab] AND (randomized controlled trial[pt] OR randomi*[tiab]) AND (\"disease-free\"[tiab] OR recurrence[tiab] OR \"invasive disease-free\"[tiab] OR survival[tiab]) AND {YRS}",
                           f"{E_EX} AND {E_BC} AND chemotherapy AND (randomized OR randomised) AND (\"disease-free\" OR recurrence OR survival) AND {E_YRS}"),
    # pembrolizumab for early TNBC: cost-effectiveness
    "pembro_cea": ("pembrolizumab[tiab] AND (\"triple-negative\"[tiab] OR \"triple negative\"[tiab] OR \"Triple Negative Breast Neoplasms\"[mh]) AND (early[tiab] OR neoadjuvant[tiab] OR KEYNOTE-522[tiab]) AND " + ECON,
                   "pembrolizumab AND (\"triple-negative\" OR \"triple negative\") AND (early OR neoadjuvant OR \"KEYNOTE-522\") AND " + E_ECON),
    # pembrolizumab for TNBC, any stage, cost-effectiveness (to catch analyses that do not say "early")
    "pembro_tnbc_any": ("pembrolizumab[tiab] AND (\"triple-negative\"[tiab] OR \"triple negative\"[tiab] OR TNBC[tiab]) AND " + ECON,
                        "pembrolizumab AND (\"triple-negative\" OR \"triple negative\" OR TNBC) AND " + E_ECON),
    # pembrolizumab cost-effectiveness in Japan (any indication) and breast cancer in Japan
    "pembro_japan": ("pembrolizumab[tiab] AND (Japan[tiab] OR Japanese[tiab] OR \"Japan\"[mh]) AND " + ECON,
                     "pembrolizumab AND (Japan OR Japanese) AND " + E_ECON),
    # threshold (headroom) analysis for interventions whose effect is not yet known
    "headroom": ("(headroom[tiab] AND (\"cost-effectiveness\"[tiab] OR \"cost effectiveness\"[tiab] OR \"health technology\"[tiab]))",
                 "headroom AND (\"cost-effectiveness\" OR \"health technology\")"),
    # CHALLENGE trial and structured exercise after colon cancer
    "challenge": ("(\"structured exercise\"[tiab] OR exercise[tiab]) AND (\"colon cancer\"[tiab] OR \"Colonic Neoplasms\"[mh]) AND (CHALLENGE[tiab] OR \"disease-free survival\"[tiab]) AND randomized controlled trial[pt] AND (\"2020/01/01\"[dp] : \"2026/12/31\"[dp])",
                  "(\"structured exercise\" OR exercise) AND \"colon cancer\" AND (CHALLENGE OR \"disease-free survival\") AND randomized AND PUB_YEAR:[2020 TO 2026]"),
    # recurrence risk in triple-negative breast cancer
    "tnbc_recurrence": ("(\"triple-negative\"[ti] OR \"triple negative\"[ti]) AND breast[ti] AND (recurrence[ti] OR relapse[ti] OR \"distant recurrence\"[ti] OR survival[ti]) AND (\"pattern\"[ti] OR \"outcome\"[ti] OR \"outcomes\"[ti] OR clinical[ti]) AND (\"2005/01/01\"[dp] : \"2026/12/31\"[dp])",
                        "TITLE:(\"triple-negative\" AND breast AND (recurrence OR relapse) AND (pattern OR outcome OR outcomes OR clinical)) AND PUB_YEAR:[2005 TO 2026]"),
}


def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": f"lit-search ({EMAIL})"}), timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            if i == tries - 1:
                raise
            time.sleep(2 + 2 * i)


def pubmed(term):
    b = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    s = get(b + "esearch.fcgi?" + urllib.parse.urlencode({"db": "pubmed", "term": term, "retmax": 500, "retmode": "json", "email": EMAIL}))
    ids = s["esearchresult"]["idlist"]
    count = int(s["esearchresult"]["count"])
    out = []
    for k in range(0, len(ids), 150):
        time.sleep(0.4)
        sm = get(b + "esummary.fcgi?" + urllib.parse.urlencode({"db": "pubmed", "id": ",".join(ids[k:k + 150]), "retmode": "json", "email": EMAIL}))
        for i in ids[k:k + 150]:
            d = sm["result"].get(i, {})
            doi = next((a["value"] for a in d.get("articleids", []) if a.get("idtype") == "doi"), "")
            out.append(dict(pmid=i, title=d.get("title", ""), year=d.get("pubdate", "")[:4], journal=d.get("source", ""), doi=doi,
                            first_author=(d.get("authors") or [{}])[0].get("name", ""), pubtype=d.get("pubtype", [])))
    return count, out


def ta(q):
    """Europe PMC: restrict a boolean query to title and abstract.

    Each quoted phrase or bare word inside the query is turned into (TITLE:x OR ABSTRACT:x);
    field-qualified parts (PUB_YEAR:, TITLE:) are left as they are."""
    import re
    def rep(m):
        t = m.group(0)
        if t in ("AND", "OR", "NOT"):
            return t
        return f"(TITLE:{t} OR ABSTRACT:{t})"
    parts = re.split(r"(PUB_YEAR:\[[^\]]*\]|TITLE:\([^)]*\))", q)
    out = []
    for i, part in enumerate(parts):
        out.append(part if i % 2 else re.sub(r'"[^"]+"|[A-Za-z][A-Za-z0-9\-]*', rep, part))
    return "".join(out)


def europepmc(q):
    q = ta(q)
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode({"query": q, "format": "json", "pageSize": 500, "resultType": "lite"})
    d = get(url)
    out = [dict(id=r.get("id"), src=r.get("source"), pmid=r.get("pmid", ""), title=r.get("title", ""), year=r.get("pubYear", ""), journal=r.get("journalTitle", ""),
                doi=r.get("doi", ""), first_author=r.get("authorString", "").split(",")[0], pubtype=r.get("pubType", "")) for r in d.get("resultList", {}).get("result", [])]
    return int(d.get("hitCount", 0)), out


keys = sys.argv[1:] or list(Q)
for key in keys:
    pq, eq = Q[key]
    today = datetime.date.today().isoformat()
    pc, ph = pubmed(pq)
    ec, eh = europepmc(eq)
    json.dump(dict(key=key, date=today, pubmed=dict(query=pq, count=pc, hits=ph), europepmc=dict(query=ta(eq), count=ec, hits=eh)),
              open(HERE / "searches" / f"search_{key}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{key}: {today} PubMed {pc}, Europe PMC {ec}")
