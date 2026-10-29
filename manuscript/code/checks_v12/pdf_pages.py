"""Independent page check for the ESM Table S1 Locations: finds the first and last 6 words of every manuscript
paragraph in the Word-exported PDF (line numbers removed, whitespace joined) and compares the pages with the
Word Information(3) pages in the word_stats JSON.

usage: python pdf_pages.py <manuscript.docx> <manuscript.pdf> <word_stats.json>
"""
import json, re, sys
import docx, fitz

sys.stdout.reconfigure(encoding="utf-8")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def main(dx, pdf, stats):
    P = [p.text for p in docx.Document(dx).paragraphs]
    J = json.load(open(stats, encoding="utf-8-sig"))["paragraphs"]
    assert len(P) == len(J)
    pages = []
    for pg in fitz.open(pdf):
        lines = [l for l in pg.get_text().splitlines() if not re.fullmatch(r"\s*\d+\s*", l)]
        pages.append(norm(" ".join(lines)))
    # concatenated text with page offsets, so a search continues across page breaks
    offs, allt = [], ""
    for t in pages:
        offs.append(len(allt)); allt += t + " "
    page_of = lambda k: max(i for i, o in enumerate(offs) if o <= k) + 1
    cur, n, bad, miss = 0, 0, [], 0
    for i, t in enumerate(P):
        w = norm(t).split(" ")
        if len(w) < 2:
            continue
        head, tail = " ".join(w[:6]), " ".join(w[-6:])
        a = allt.find(head, cur)
        b = allt.find(tail, a if a >= 0 else cur)
        if a < 0 or b < 0:
            miss += 1; print("   not located:", i, repr(t[:60]), "| head", a >= 0, "tail", b >= 0)
            continue
        cur = a + 1
        n += 1
        got = (page_of(a), page_of(b + len(tail) - 1))
        exp = (J[i]["start_page"], J[i]["end_page"])
        if got != exp:
            bad.append((i, t[:50], exp, got))
    print(f"paragraphs located {n}; not located {miss}; page mismatches {len(bad)}")
    for x in bad:
        print("  ", x)


if __name__ == "__main__":
    main(*sys.argv[1:4])
