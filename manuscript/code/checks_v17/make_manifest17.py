"""Writes manuscript/v17/MANIFEST_v17.md (every sha256 computed here; = checks_v16/make_manifest16.py for v17, plus the
two oral drug price lists): deliverables, base (v16), editing and check scripts, the analysis source files of MANIFEST_v16
recomputed and compared (the price-list rows of MANIFEST_v16 are listed in their own section), the four price lists.
Run from the project root after worklog_v17.md is final and before v16 is moved (the base is read from manuscript/v16).
usage: python make_manifest17.py
"""
import hashlib, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def table(rows, head=("文件", "sha256")):
    return ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(r) + " |" for r in rows]


def main():
    V, B = "manuscript/v17", "manuscript/v16"
    deliv = ["manuscript_v17_BCRT.docx", "tables_v17_BCRT.docx", "ESM_1_v17.docx", "ESM_1_v17.pdf", "Fig1.tif", "Fig2.tif",
             "Fig3.tif", "cover_letter_v17_BCRT.docx", "worklog_v17.md"]
    base = ["manuscript_v16_BCRT.docx", "tables_v16_BCRT.docx", "ESM_1_v16.docx", "ESM_1_v16.pdf", "Fig1.tif", "Fig2.tif",
            "Fig3.tif", "cover_letter_v16_BCRT.docx", "worklog_v16.md", "MANIFEST_v16.md"]
    scripts = ["manuscript/code/edit_manuscript_v17.py", "manuscript/code/edit_esm_v17.py"]
    d = "manuscript/code/checks_v17"
    checks = sorted(f"{d}/{f}" for f in os.listdir(d) if f.endswith(".py"))
    outs = sorted(f"{d}/out/{f}" for f in os.listdir(f"{d}/out") if os.path.isfile(f"{d}/out/{f}"))
    m16 = open(f"{B}/MANIFEST_v16.md", encoding="utf-8").read()
    src = [(p, h) for p, h in re.findall(r"\| `([^`]+)` \| ([0-9a-f]{64}) \|", m16) if "/sources_price/" not in p]
    L = ["# MANIFEST v17（2026-11-04）", "",
         "- 版本: v17（v16 的小修: 文献第 8 条加内服药清单〔10/14 版快照存在、内服药用值 5/5 一致 → 指示的 (i)〕；数值不变）。",
         "- 交付日: 2026-11-04。",
         "- 底本: v16（2026-11-04 交付；现在 manuscript/archive/v16/，下表）。会话开始时 9 个交付物的 sha256 与 MANIFEST_v16 一致。",
         "- tables_v17_BCRT.docx、Fig1〜3.tif、cover_letter_v17_BCRT.docx = v16 的逐字节复制（下表 sha256 与底本相同）。"
         "ESM_1_v17.docx = v16 + Table S1 第 27 项页码 p. 26 → p. 27（第 8 条加长使 Funding 移到第 27 页；worklog_v17.md 第 6.2 节）。"
         "ESM_1_v17.pdf 由 Word（SaveAs2, 17）重新导出（48 页）。",
         "- 数值来源: 本版不改数值，未重算模型。MANIFEST_v16 的来源文件 sha256 重算（下表）。药价表四份的 sha256 见末节。",
         "- 文献: 78 条；第 8 条改为内服药与注射药两份清单（10/14 版）及两个 Wayback 存档网址（worklog_v17.md 第 5 节）；其余不变。",
         "- 公开用代码: 本版无改动（exercise_cea_public，HEAD fbf19be，无远程、未推送）。",
         "", "## 交付物（manuscript/v17/）", ""]
    L += table([(f, sha(f"{V}/{f}")) for f in deliv])
    L += ["", "## 底本（manuscript/archive/v16/）", ""]
    L += table([(f, sha(f"{B}/{f}")) for f in base])
    L += ["", "## 编辑脚本", ""]
    L += table([(f, sha(f)) for f in scripts])
    L += ["", "## 核对脚本与输出（另用 checks_v11/ 的 refcheck.py、sec10.py、fmt_audit.py、word_stats.ps1、word_open_pdf.ps1、citemap.py，"
          "checks_v12/pdf_pages.py，checks_v14/ 的 word_wc14.py、acro_extract14.py，edit_esm_v14.py 的 pages14() 与 edit_esm_v15.py 的 "
          "locations15()，均未改；ARS 3.24.1 的 check_acronyms.py）", ""]
    L += table([(f, sha(f)) for f in checks + outs])
    L += ["", "## 数值来源文件（MANIFEST_v16 的来源表，sha256 为本版重算值；与 v16 的比较）", "",
          "| 文件 | sha256 | 与 v16 |", "|---|---|---|"]
    nchg = 0
    for p, h in src:
        now = sha(p)
        nchg += now != h
        L.append(f"| `{p}` | {now} | {'一致' if now == h else '变更'} |")
    L += ["", "## 药价表（_01 = 内服药、_02 = 注射药。10/14 版 _02 = 当初保存的原文件，Wayback 存档件与之逐字节相同；"
          "10/14 版 _01 = Wayback 快照 20261014082215 的原始字节〔原网址现 404〕；11/1 版 = 2026-11-04 下载）", ""]
    L += table([(f"`input/params/sources_price/{f}`", sha(f"input/params/sources_price/{f}"))
                for f in ("tp20261014-01_01.xlsx", "tp20261014-01_02.xlsx", "tp20261101-01_01.xlsx", "tp20261101-01_02.xlsx")])
    open(f"{V}/MANIFEST_v17.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("written; source files:", len(src), "changed:", nchg)


if __name__ == "__main__":
    main()
