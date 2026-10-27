"""Resolve candidate references to PubMed records and save metadata and abstracts.

Each candidate is (key, locator): a PMID, a DOI, or a PubMed search term that must
return exactly one record. Writes pubmed_meta.json (merged with earlier runs) and
prints one line per record.
Usage: python fetch_refs.py            (all candidates in CANDIDATES)
       python fetch_refs.py key1 key2  (only these)
"""
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent
EMAIL = "akehara1001@gmail.com"
B = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

CANDIDATES = {
    # TNBC recurrence and KEYNOTE-522
    "dent2007": "Dent R[au] AND triple-negative[ti] AND patterns of recurrence[ti] AND 2007[dp]",
    "liedtke2008": "Liedtke C[au] AND triple-negative[ti] AND 2008[dp] AND J Clin Oncol[ta]",
    "licata2025": "10.1158/1078-0432.ccr-25-1478",
    "schmid2020": "10.1056/NEJMoa1910549",
    "schmid2022": "10.1056/NEJMoa2112651",
    "schmid2024": "Schmid P[au] AND overall survival[ti] AND pembrolizumab[ti] AND 2024[dp] AND N Engl J Med[ta]",
    # exercise evidence
    "courneya2025": "10.1056/NEJMoa2502760",
    "courneya2007": "Courneya KS[au] AND adjuvant chemotherapy[ti] AND 2007[dp] AND J Clin Oncol[ta] AND breast[ti]",
    "courneya2014": "10.1249/MSS.0000000000000297",
    "vanwaart2015": "van Waart H[au] AND 2015[dp] AND J Clin Oncol[ta]",
    "mijwel2018": "29139007",
    "furmaniak2016": "10.1002/14651858.CD005001.pub3",
    "campbell2019": "Campbell KL[au] AND exercise guidelines[ti] AND 2019[dp] AND Med Sci Sports Exerc[ta]",
    "cannioto2021": "Cannioto RA[au] AND 2021[dp] AND J Natl Cancer Inst[ta]",
    "sanft2023": "10.1200/JCO.23.00871",
    "kjeldsted2025": "10.1158/1078-0432.CCR-25-0416",
    "schmidt2025": "10.1016/j.jshs.2025.101064",
    "diasrato2026": "10.1007/s00520-026-11156-1",
    "deboniface2022": "10.1371/journal.pone.0274804",
    "iyengar2025": "10.1002/cncr.35575",
    # economic evaluations of exercise and headroom
    "khan2019": "10.1007/s10549-019-05235-7",
    "gublergut2021": "10.1007/s11764-021-01002-0",
    "wang2023": "10.1016/j.ypmed.2023.107491",
    "may2017": "10.1136/bmjopen-2016-012187",
    "vanwaart2018": "10.1007/s10198-017-0936-0",
    "perrier2020": "10.1007/s00520-019-05078-4",
    "ax2023": "10.1080/0284186X.2023.2200149",
    "ax2022": "10.1080/0284186X.2022.2075238",
    "chan2026": "10.1200/JCO-26-00765",
    "boudewijns2023": "10.1007/s40258-022-00774-5",
    # pembrolizumab cost-effectiveness
    "huang2023": "10.1007/s12325-022-02365-1",
    "kwong2024": "10.1007/s40487-024-00285-4",
    "favrebulle2024": "10.1007/s41669-023-00445-8",
    "pollinger2025": "10.1080/13696998.2024.2441073",
    "sugiura2023": "10.1093/jjco/hyad050",
    "kakinuma2025": "10.1007/s10388-025-01144-5",
    "taniguchi2026": "10.1016/j.vhri.2025.101555",
    "chisaki2025": "10.1007/s40261-025-01445-8",
    "tomura2025": "10.1007/s11096-024-01826-7",
    "kashiwa2024": "10.1007/s12029-024-01106-7",
    "morimoto2026": "10.1007/s41669-025-00634-7",
    # methods
    "husereau2022": "10.1136/bmj-2021-067975",
    "hasegawa2020": "Hasegawa M[au] AND cost-effectiveness[ti] AND Japan[ti] AND 2020[dp] AND Value Health[ta]",
    "shiroiwa2020": "Shiroiwa T[au] AND price adjustment[ti] AND 2020[dp]",
    "guyot2012": "10.1186/1471-2288-12-9",
    "grinda2023": "37385070",
    "elmore2021": "10.1245/s10434-021-10444-w",
    "fedele2026": "10.1007/s10549-026-08023-2",
    "ludwig2018": "Ludwig K[au] AND EQ-5D-5L[ti] AND German[ti] AND 2018[dp]",
    "iwatani2021": "10.3390/curroncol28050356",
    "shiroiwa2017": "10.1186/s12885-017-3774-7",
    "masuda2017": "10.1056/NEJMoa1612645",
    "tutt2021": "10.1056/NEJMoa2105215",
    "garber2026": "10.1016/j.annonc.2026.08.002",
    "cortes2011": "Cortes J[au] AND eribulin[ti] AND 2011[dp] AND Lancet[ta]",
    "cortes2020": "Cortes J[au] AND pembrolizumab[ti] AND 2020[dp] AND Lancet[ta] AND KEYNOTE-355[ti]",
    "miller2007": "Miller K[au] AND bevacizumab[ti] AND paclitaxel[ti] AND 2007[dp] AND N Engl J Med[ta]",
    # S1 sources
    "kuemmel2026": "41739398",
    "nusawat2026": "10.1007/s10198-026-01912-9",
    "yoshinami2025": "10.1007/s12282-025-01714-6",
    "fujisawa2021": "10.3892/mco.2021.2258",
    "andrade2026": "Andrade[au] AND 2026[dp] AND Breast Cancer Res Treat[ta] AND capecitabine[tiab]",
    "valachis2026": "Valachis A[au] AND 2026[dp] AND Br J Cancer[ta]",
}


def get(url, as_json=True, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": f"ref-check ({EMAIL})"}), timeout=60) as r:
                b = r.read().decode("utf-8")
                return json.loads(b) if as_json else b
        except Exception:  # noqa: BLE001
            if i == tries - 1:
                raise
            time.sleep(2 + 2 * i)


def to_pmid(loc):
    if re.fullmatch(r"\d{6,9}", loc):
        return [loc]
    term = f"{loc}[doi]" if loc.startswith("10.") else loc
    s = get(B + "esearch.fcgi?" + urllib.parse.urlencode({"db": "pubmed", "term": term, "retmode": "json", "retmax": 20, "email": EMAIL}))
    return s["esearchresult"]["idlist"]


def record(pmid):
    x = get(B + "efetch.fcgi?" + urllib.parse.urlencode({"db": "pubmed", "id": pmid, "retmode": "xml", "email": EMAIL}), as_json=False)
    root = ET.fromstring(x)
    a = root.find(".//PubmedArticle")
    art = a.find(".//Article")
    j = art.find("Journal")
    au = []
    for p in art.findall("AuthorList/Author"):
        if p.find("LastName") is not None:
            au.append(p.findtext("LastName") + " " + (p.findtext("Initials") or ""))
        elif p.find("CollectiveName") is not None:
            au.append(p.findtext("CollectiveName"))
    abst = " ".join("".join(t.itertext()) for t in art.findall("Abstract/AbstractText"))
    ids = {i.get("IdType"): i.text for i in a.findall("PubmedData/ArticleIdList/ArticleId")}  # not the reference list
    pd = j.find("JournalIssue/PubDate")
    year = pd.findtext("Year") or (pd.findtext("MedlineDate") or "")[:4]
    return dict(pmid=pmid, doi=ids.get("doi", ""), pmc=ids.get("pmc", ""), authors=au, title="".join(art.find("ArticleTitle").itertext()),
                journal=j.findtext("ISOAbbreviation") or j.findtext("Title"), year=year,
                volume=j.findtext("JournalIssue/Volume") or "", issue=j.findtext("JournalIssue/Issue") or "",
                pages=art.findtext("Pagination/MedlinePgn") or "", elocation=[e.text for e in art.findall("ELocationID")],
                pubtypes=[t.text for t in art.findall("PublicationTypeList/PublicationType")], abstract=abst)


meta_p = HERE / "pubmed_meta.json"
meta = json.load(open(meta_p, encoding="utf-8")) if meta_p.exists() else {}
keys = sys.argv[1:] or list(CANDIDATES)
for k in keys:
    loc = CANDIDATES[k]
    ids = to_pmid(loc)
    time.sleep(0.35)
    if len(ids) != 1:
        print(f"{k}: {len(ids)} PubMed records for {loc!r}: {ids[:8]}")
        meta[k] = dict(locator=loc, pmid_candidates=ids)
        continue
    r = record(ids[0])
    time.sleep(0.35)
    r["locator"] = loc
    meta[k] = r
    print(f"{k}: PMID {r['pmid']} | {r['authors'][0] if r['authors'] else ''} | {r['year']} | {r['journal']} {r['volume']}({r['issue']}):{r['pages']} | doi {r['doi']} | {r['title'][:80]}")
json.dump(meta, open(meta_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
