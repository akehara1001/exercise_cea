"""DOI resolution and bibliographic match for the reference list of a BCRT manuscript docx.
For each reference with a DOI: doi.org resolution (HTTP status of the first redirect) and Crossref metadata compared
field by field (first author surname, year, journal, volume, first page or article number, title similarity).
References without a DOI: the URL is requested and the HTTP status recorded.
usage: python refcheck.py <manuscript.docx> <out.json>
"""
import json, re, sys, time, unicodedata, difflib, urllib.request, urllib.error, ssl
import docx

sys.stdout.reconfigure(encoding="utf-8")
UA = {"User-Agent": "Mozilla/5.0 (reference check; academic manuscript)"}


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=timeout)


def head_status(url):
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    op = urllib.request.build_opener(NoRedirect)
    try:
        r = op.open(urllib.request.Request(url, headers=UA, method="GET"), timeout=30)
        return r.status, r.headers.get("Location")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location")
    except Exception as e:
        return str(e)[:60], None


def refs(path):
    P = [p.text for p in docx.Document(path).paragraphs]
    i = P.index("References")
    out = []
    for t in P[i + 1:]:
        m = re.match(r"^(\d+)\. (.*)$", t)
        if not m:
            break
        out.append((int(m.group(1)), m.group(2)))
    return out


def parse(text):
    d = {}
    m = re.match(r"^(.*?) \((\d{4}|n\.d\.)\) (.*)$", text)
    d["authors"], d["year"], rest = (m.group(1), m.group(2), m.group(3)) if m else ("", "", text)
    d["first_surname"] = d["authors"].split(",")[0].split(" ")[0] if d["authors"] else ""
    md = re.search(r"https://doi\.org/(\S+)$", text)
    d["doi"] = md.group(1) if md else None
    mu = re.search(r"(https?://\S+?)\.? Accessed", text)
    d["url"] = mu.group(1) if mu else None
    # journal volume:pages
    mj = re.search(r"\. ([A-Z][A-Za-z .&()-]+?) (\d+)(?: Suppl \d+)?(?:\([^)]*\))?:([A-Za-z0-9.–-]+)\. https://doi", text)
    if mj:
        d["journal"], d["volume"], d["pages"] = mj.group(1), mj.group(2), mj.group(3)
        d["title"] = rest[: rest.rfind(". " + mj.group(1) + " ")]
    else:
        d["journal"] = d["volume"] = d["pages"] = None
        d["title"] = rest.split(". https")[0]
    return d


def crossref(doi):
    for k in range(3):
        try:
            r = get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/()._-;:"))
            return json.load(r)["message"]
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2)
        except Exception:
            time.sleep(2)
    return "error"


def main(path, outp):
    import urllib.parse
    R = refs(path)
    res = []
    for n, t in R:
        d = parse(t)
        row = {"n": n, "doi": d["doi"], "url": d["url"]}
        if d["doi"]:
            st, loc = head_status("https://doi.org/" + d["doi"])
            row["doi_status"] = st
            m = crossref(d["doi"])
            if m in (None, "error"):
                row["crossref"] = m
            else:
                fam = (m.get("author") or [{}])[0].get("family", "") if m.get("author") else ""
                yrs = set()
                for k in ("published-print", "published-online", "issued", "published"):
                    if m.get(k, {}).get("date-parts"):
                        yrs.add(str(m[k]["date-parts"][0][0]))
                ctitle = (m.get("title") or [""])[0]
                cont = (m.get("container-title") or [""])[0]
                short = (m.get("short-container-title") or [""])
                vol = m.get("volume")
                page = m.get("page") or m.get("article-number")
                row.update({
                    "cr_first_author": fam, "cr_years": sorted(yrs), "cr_title": ctitle, "cr_journal": cont,
                    "cr_short": short, "cr_volume": vol, "cr_page": page,
                    "ref_first_author": d["first_surname"], "ref_year": d["year"], "ref_journal": d["journal"],
                    "ref_volume": d["volume"], "ref_pages": d["pages"], "ref_title": d["title"],
                    "title_sim": round(difflib.SequenceMatcher(None, norm(ctitle), norm(d["title"])).ratio(), 3),
                    "author_ok": norm(fam).split(" ")[-1] in norm(d["first_surname"]) or norm(d["first_surname"]) in norm(fam),
                    "year_ok": d["year"] in yrs,
                    "volume_ok": (vol is None and d["volume"] is None) or (str(vol) == str(d["volume"])),
                    "page_ok": (page is None and d["pages"] is None) or (d["pages"] is not None and page is not None and
                                norm(str(page)).split(" ")[0] == norm(d["pages"].replace("–", "-")).split(" ")[0]),
                    "update_to": [u.get("type") for u in m.get("update-to", [])] if m.get("update-to") else [],
                    "relation": list((m.get("relation") or {}).keys()),
                })
            time.sleep(0.3)
        elif d["url"]:
            st, loc = head_status(d["url"])
            row["url_status"] = st
            row["url_location"] = loc
        res.append(row)
        print(n, row.get("doi_status", row.get("url_status")), {k: row[k] for k in row if k.endswith("_ok")}, row.get("title_sim"))
    json.dump(res, open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
