"""v17 step 1b-1c: the MHLW oral drug price lists of 14 October 2026 (tp20261014-01_01.xlsx; the MHLW address now returns
404, so the copy is the Wayback capture 20261014082215, raw bytes via the id_ form) and 1 November 2026
(tp20261101-01_01.xlsx, downloaded 2026-11-04). (1) All rows compared, keyed by the price-list code and product name:
added, removed, changed (any column). (2) Every oral product whose price was used (calculation sheet 計算根拠_尾崎, source
"薬価サーチ, 令和8年度薬価" or "同上": rows 111, 158, 159, 174, 176), looked up in both lists with the price used.
(3) For the generics (capecitabine 300 mg, olanzapine 5 mg) the price is recomputed by the rule "lowest generic price of
the same strength", by ingredient and strength in both lists. Row 210 (analgesic and poultice, 3,000 JPY) is an
assumption, not a list price, and is not compared.
Product names are compared after NFKC normalization (the lists use full-width characters).
usage: python compare_oral_lists17.py <list_1014_01.xlsx> <list_1101_01.xlsx> <out.json>
"""
import json, sys, unicodedata
import openpyxl

sys.stdout.reconfigure(encoding="utf-8")
N = lambda s: unicodedata.normalize("NFKC", str(s or "")).replace(" ", "")
# (row of 計算根拠_尾崎, parameter, product name in the list, price used in JPY per tablet)
ITEMS = [
    (111, "F05, D03, D03P", "リムパーザ錠150mg", 4788),
    (159, "F02 (upper bound)", "ゼローダ錠300", 107.3),
    (176, "A05", "デカドロン錠4mg", 23.4),
]
# (row, parameter, ingredient, strength, price used): generics, by the rule
RULE = [
    (158, "F02", "カペシタビン", "300mg1錠", 46.4),
    (174, "A05", "オランザピン", "5mg1錠", 14.3),
]


def load(path):
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    h = rows[0]
    assert h[1] == "薬価基準収載医薬品コード" and h[7] == "品名" and h[9].endswith("後発医薬品") and h[12] == "薬価", h
    out = []
    for r in rows[1:]:
        out.append({"kind": r[0], "code": r[1], "ingredient": N(r[2]), "strength": N(r[3]), "name": N(r[7]), "generic": r[9],
                    "price": r[12], "transition": r[13], "raw": [str(c) for c in r]})
    return out


def main(p1014, p1101, outpath):
    A, B = load(p1014), load(p1101)
    assert {r["kind"] for r in A} == {"内用薬"} == {r["kind"] for r in B}
    ka = {(r["code"], r["name"]): r for r in A}; kb = {(r["code"], r["name"]): r for r in B}
    added = sorted(set(kb) - set(ka)); removed = sorted(set(ka) - set(kb))
    changed = [(k, ka[k]["raw"], kb[k]["raw"]) for k in sorted(set(ka) & set(kb)) if ka[k]["raw"] != kb[k]["raw"]]
    print(f"rows: 14 Oct {len(A)}, 1 Nov {len(B)}; added {len(added)}, removed {len(removed)}, changed {len(changed)}")
    for k in added: print("  added:", k, kb[k]["price"])
    for k in removed: print("  removed:", k, ka[k]["price"])
    for k, x, y in changed:
        print("  changed:", k, [(i, x[i], y[i]) for i in range(len(x)) if x[i] != y[i]])
    table = []
    for row, use, name, used in ITEMS:
        ha = [r for r in A if r["name"] == N(name)]; hb = [r for r in B if r["name"] == N(name)]
        assert len(ha) == 1 and len(hb) == 1, (name, len(ha), len(hb))
        a, b = ha[0], hb[0]
        table.append({"row": row, "use": use, "basis": "product", "product": a["name"], "strength": a["strength"], "code": a["code"],
                      "price_used": used, "price_1014": a["price"], "price_1101": b["price"], "n_1014": 1, "n_1101": 1})
    for row, use, ing, strength, used in RULE:
        def lowest(rows):
            g = [r for r in rows if r["ingredient"] == N(ing) and r["strength"] == N(strength) and r["generic"]]
            m = min(r["price"] for r in g)
            return m, len(g), sorted(r["name"] for r in g if r["price"] == m)
        ma, mb = lowest(A), lowest(B)
        table.append({"row": row, "use": use, "basis": "lowest generic of the same strength", "product": N(ing) + " (generics)",
                      "strength": N(strength), "code": None, "price_used": used, "price_1014": ma[0], "price_1101": mb[0],
                      "n_1014": ma[1], "n_1101": mb[1], "lowest_products_1014": ma[2], "lowest_products_1101": mb[2]})
    for t in table:
        t["used_equals_1014"] = t["price_1014"] == t["price_used"]
        t["used_equals_1101"] = t["price_1101"] == t["price_used"]
    table.sort(key=lambda t: t["row"])
    print("\nrow | parameter | product | strength | basis | used | 14 Oct | 1 Nov | n generics 14 Oct/1 Nov")
    for t in table:
        print(f"  {t['row']} | {t['use']} | {t['product']} | {t['strength']} | {t['basis']} | {t['price_used']} | "
              f"{t['price_1014']} | {t['price_1101']} | {t['n_1014']}/{t['n_1101']}")
        if t.get("lowest_products_1014"):
            print("     lowest, 14 Oct:", "、".join(t["lowest_products_1014"]), "| 1 Nov same:", t["lowest_products_1014"] == t["lowest_products_1101"])
    a14 = all(t["used_equals_1014"] for t in table); a11 = all(t["used_equals_1101"] for t in table)
    print("all used = 14 Oct:", a14, "| all used = 1 Nov:", a11)
    json.dump({"rows_1014": len(A), "rows_1101": len(B), "added": [list(k) for k in added], "removed": [list(k) for k in removed],
               "changed": [[list(k), x, y] for k, x, y in changed], "items": table, "all_used_eq_1014": a14, "all_used_eq_1101": a11},
              open(outpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:4])
