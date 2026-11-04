"""v16 step 1a-1b: the MHLW injection price lists of 14 October 2026 (tp20261014-01_02.xlsx) and 1 November 2026
(tp20261101-01_02.xlsx). (1) All rows compared, keyed by the price-list code and product name: added, removed, changed
(any column). (2) Every injectable product whose price was used in the inputs citing reference [8] (calculation sheets:
sources_hara.md for A01-A03, 計算根拠_尾崎 for A05, D03, D03P, D05 and 計算根拠_原 for the eribulin scenario), looked
up in both lists with the price used. (3) For the rule of A01-A03 and the eribulin scenario (lowest generic price of
each strength), the lowest generic and originator prices by ingredient and strength in both lists.
Product names are compared after NFKC normalization (the lists use full-width characters).
usage: python compare_price_lists16.py <list_1014.xlsx> <list_1101.xlsx> <out.json>
"""
import json, sys, unicodedata
import openpyxl

sys.stdout.reconfigure(encoding="utf-8")
N = lambda s: unicodedata.normalize("NFKC", str(s or "")).replace(" ", "")
# (parameter rows, product name as in the calculation sheets, price used in JPY)
ITEMS = [
    ("A01", "パクリタキセル注射液30mg「NP」", 1368), ("A01", "パクリタキセル注100mg/16.7mL「NK」", 4580),
    ("A01 (originator, reference)", "タキソール注射液30mg", 1413), ("A01 (originator, reference)", "タキソール注射液100mg", 4491),
    ("A01", "カルボプラチン注射液50mg「NK」", 1347), ("A01", "カルボプラチン点滴静注液150mg「サンド」", 2183),
    ("A01", "カルボプラチン注射液450mg「日医工」", 4877),
    ("A01 (originator, reference)", "パラプラチン注射液50mg", 1217), ("A01 (originator, reference)", "パラプラチン注射液150mg", 3001),
    ("A01 (originator, reference)", "パラプラチン注射液450mg", 7514),
    ("A02", "ドキソルビシン塩酸塩注射液50mg「サンド」", 2687), ("A02 (originator, reference)", "アドリアシン注用50", 6210),
    ("A02", "エピルビシン塩酸塩注射用10mg「NK」", 1375), ("A02", "エピルビシン塩酸塩注射用50mg「NK」", 6528),
    ("A02", "注射用エンドキサン500mg", 1500),
    ("A03, D03, D03P", "キイトルーダ点滴静注100mg", 199462),
    ("A05", "ホスアプレピタント点滴静注用150mg「NK」", 4924), ("A05", "パロノセトロン静注0.75mg/2mLシリンジ「NP」", 2836),
    ("A05, scenario eribulin", "デキサート注射液6.6mg", 197), ("A05", "ペグフィルグラスチムBS皮下注3.6mg「ニプロ」", 54924),
    ("A05 (listed in the sheet)", "グラニセトロン静注液3mg「アイロム」", 652),
    ("D03", "アブラキサン点滴静注用100mg", 30878), ("D03P, D05", "トロデルビ点滴静注用200mg", 187195),
    ("D03P, D05", "エンハーツ点滴静注用100mg", 192652), ("D03, D03P, D05", "ダトロウェイ点滴静注用100mg", 311990),
    ("D03, D03P", "ベバシズマブBS点滴静注400mg「ファイザー」", 22130), ("D03, D03P", "ベバシズマブBS点滴静注100mg「ファイザー」", 5932),
    ("D05 lower bound, scenario eribulin", "エリブリンメシル酸塩静注液1mg「ニプロ」", 22997),
    ("scenario eribulin (reference)", "ハラヴェン静注1mg", 50010), ("scenario eribulin (reference)", "エリブリンメシル酸塩静注液1mg「日医工」", 23399),
]
RULE_INGREDIENTS = ["パクリタキセル", "カルボプラチン", "ドキソルビシン塩酸塩", "エピルビシン塩酸塩", "シクロホスファミド水和物",
                    "ペムブロリズマブ(遺伝子組換え)", "エリブリンメシル酸塩"]


def load(path):
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    h = rows[0]
    assert h[1] == "薬価基準収載医薬品コード" and h[7] == "品名" and h[12] == "薬価", h
    out = []
    for r in rows[1:]:
        out.append({"code": r[1], "ingredient": N(r[2]), "strength": N(r[3]), "name": N(r[7]), "maker": r[8], "generic": r[9],
                    "originator": r[10], "orig_with_generic": r[11], "price": r[12], "transition": r[13], "raw": [str(c) for c in r]})
    return out


def find(rows, name):
    n = N(name)
    hits = [r for r in rows if r["name"] == n]
    if not hits:
        hits = [r for r in rows if n in r["name"]]
    return hits


def main(p1014, p1101, outpath):
    A, B = load(p1014), load(p1101)
    ka = {(r["code"], r["name"]): r for r in A}; kb = {(r["code"], r["name"]): r for r in B}
    added = sorted(set(kb) - set(ka)); removed = sorted(set(ka) - set(kb))
    changed = [(k, ka[k]["raw"], kb[k]["raw"]) for k in sorted(set(ka) & set(kb)) if ka[k]["raw"] != kb[k]["raw"]]
    print(f"rows: 14 Oct {len(A)}, 1 Nov {len(B)}; added {len(added)}, removed {len(removed)}, changed {len(changed)}")
    for k in added: print("  added:", k, kb[k]["price"])
    for k in removed: print("  removed:", k, ka[k]["price"])
    for k, x, y in changed:
        diff = [(i, x[i], y[i]) for i in range(len(x)) if x[i] != y[i]]
        print("  changed:", k, diff)
    table = []
    for use, name, used in ITEMS:
        ha, hb = find(A, name), find(B, name)
        assert len(ha) == 1 and len(hb) == 1, (name, len(ha), len(hb))
        a, b = ha[0], hb[0]
        table.append({"use": use, "product": a["name"], "strength": a["strength"], "code": a["code"], "price_used": used,
                      "price_1014": a["price"], "price_1101": b["price"], "same": a["price"] == b["price"],
                      "used_equals_1014": a["price"] == used})
    print("\nproducts used | strength | used | 14 Oct | 1 Nov | same")
    for t in table:
        print(f"  {t['use']} | {t['product']} | {t['strength']} | {t['price_used']} | {t['price_1014']} | {t['price_1101']} | {t['same']}")
    print("all used products: 14 Oct = used:", all(t["used_equals_1014"] for t in table), "| 14 Oct = 1 Nov:", all(t["same"] for t in table))
    rule = []
    for ing in RULE_INGREDIENTS:
        for strength in sorted({r["strength"] for r in A + B if r["ingredient"] == N(ing)}):
            def mins(rows):
                g = [r["price"] for r in rows if r["ingredient"] == N(ing) and r["strength"] == strength and r["generic"]]
                o = [r["price"] for r in rows if r["ingredient"] == N(ing) and r["strength"] == strength and not r["generic"]]
                return (min(g) if g else None, min(o) if o else None, len([r for r in rows if r["ingredient"] == N(ing) and r["strength"] == strength]))
            ma, mb = mins(A), mins(B)
            rule.append({"ingredient": N(ing), "strength": strength, "min_generic_1014": ma[0], "min_generic_1101": mb[0],
                         "min_nongeneric_1014": ma[1], "min_nongeneric_1101": mb[1], "n_1014": ma[2], "n_1101": mb[2], "same": ma == mb})
    print("\nrule check (lowest generic / lowest non-generic, number of products) by ingredient and strength")
    for r in rule:
        print(f"  {r['ingredient']} {r['strength']}: 14 Oct {r['min_generic_1014']}/{r['min_nongeneric_1014']} (n {r['n_1014']}) | "
              f"1 Nov {r['min_generic_1101']}/{r['min_nongeneric_1101']} (n {r['n_1101']}) | same {r['same']}")
    print("rule check, all same:", all(r["same"] for r in rule))
    json.dump({"rows_1014": len(A), "rows_1101": len(B), "added": [list(k) for k in added], "removed": [list(k) for k in removed],
               "changed": [[list(k), x, y] for k, x, y in changed], "products": table, "rule": rule},
              open(outpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:4])
