"""Second pass for the citation check: author lists against Crossref (surnames and initials of the listed authors),
retraction/correction markers (update-to, updated-by, relation), format rules of the Springer basic style
(DOI as https://doi.org/, no period after DOI/URL, 'et al' after the listed authors, double punctuation),
currency and self-citation counts.
usage: python refcheck2.py <manuscript.docx> <out.json>
"""
import json, re, sys, time, unicodedata, urllib.request, urllib.parse
import docx

sys.stdout.reconfigure(encoding="utf-8")
UA = {"User-Agent": "Mozilla/5.0 (reference check; academic manuscript)"}


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


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


def cr(doi):
    for _ in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(
                "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/()._-;:"), headers=UA), timeout=30)
            return json.load(r)["message"]
        except Exception:
            time.sleep(2)
    return None


def main(path, outp):
    R = refs(path)
    res = []
    years = {}
    fmt = []
    for n, t in R:
        m = re.match(r"^(.*?) \((\d{4}|n\.d\.)\) ", t)
        auth = m.group(1) if m else ""
        years[n] = m.group(2) if m else None
        etal = auth.endswith(" et al")
        names = [a.strip() for a in auth.replace(" et al", "").split(", ") if a.strip()]
        if re.search(r"https://doi\.org/\S+\.$", t) or re.search(r"https?://\S+\.$", t) and "Accessed" not in t:
            fmt.append((n, "period after DOI/URL"))
        if re.search(r"[?!]\.", t):
            fmt.append((n, "double punctuation (?. or !.)"))
        if "dx.doi.org" in t:
            fmt.append((n, "dx.doi.org"))
        if etal and len(names) != 6:
            fmt.append((n, f"et al after {len(names)} authors"))
        md = re.search(r"https://doi\.org/(\S+)$", t)
        row = {"n": n, "listed": names, "et_al": etal}
        if md:
            msg = cr(md.group(1))
            if msg:
                ca = msg.get("author") or []
                fams = [norm(a.get("family", a.get("name", ""))) for a in ca]
                row["cr_n_authors"] = len(ca)
                row["cr_first6"] = [(a.get("family", a.get("name", "")), a.get("given", "")) for a in ca[:6]]
                mism = []
                for k, nm in enumerate(names[:len(ca)]):
                    sur = norm(nm.rsplit(" ", 1)[0]) if " " in nm else norm(nm)
                    if k < len(fams) and not (sur == fams[k] or sur.replace("-", " ") == fams[k].replace("-", " ")):
                        mism.append((k + 1, nm, ca[k].get("family", ""), ca[k].get("given", "")))
                row["author_mismatch"] = mism
                if not etal and len(ca) and len(names) != len(ca):
                    row["count_note"] = f"listed {len(names)} without et al, Crossref {len(ca)}"
                if etal and len(ca) <= 6:
                    row["count_note"] = f"et al but Crossref has {len(ca)} authors"
                row["update_to"] = [u.get("type") for u in msg.get("update-to", [])]
                row["updated_by"] = [u.get("type") for u in msg.get("updated-by", [])] if msg.get("updated-by") else []
                row["relation"] = sorted((msg.get("relation") or {}).keys())
            time.sleep(0.3)
        res.append(row)
    json.dump({"rows": res, "format": fmt, "years": years}, open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("format flags:", fmt)
    for r in res:
        if r.get("author_mismatch") or r.get("count_note") or r.get("updated_by") or any(u for u in r.get("update_to", [])):
            print(r["n"], "mismatch:", r.get("author_mismatch"), "|", r.get("count_note", ""), "| update_to:", r.get("update_to"), "updated_by:", r.get("updated_by"))
    ys = [int(y) for y in years.values() if y and y.isdigit()]
    print("years: n", len(ys), "| >10 years old (<=2015):", sum(1 for y in ys if y <= 2015),
          "| 2021-2026:", sum(1 for y in ys if y >= 2021), "of", len(R))
    allt = " ".join(t for _, t in R)
    print("self-citation probe (Ozaki/Hara in author fields):", sum(1 for _, t in R if re.search(r"\b(Ozaki|Hara) [A-Z]+\b", t.split(" (")[0])))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
