"""Writes manuscript/v16/MANIFEST_v16.md (every sha256 computed here; = checks_v15/make_manifest15.py for v16, plus the
two price lists): deliverables, base (v15), editing and check scripts, the analysis source files of MANIFEST_v15
recomputed and compared, the price lists of step 1. Run from the project root after worklog_v16.md is final and before
v15 is moved (the base is read from manuscript/v15).
usage: python make_manifest16.py
"""
import hashlib, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def table(rows, head=("文件", "sha256")):
    return ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(r) + " |" for r in rows]


def main():
    V, B = "manuscript/v16", "manuscript/v15"
    deliv = ["manuscript_v16_BCRT.docx", "tables_v16_BCRT.docx", "ESM_1_v16.docx", "ESM_1_v16.pdf", "Fig1.tif", "Fig2.tif",
             "Fig3.tif", "cover_letter_v16_BCRT.docx", "worklog_v16.md"]
    base = ["manuscript_v15_BCRT.docx", "tables_v15_BCRT.docx", "ESM_1_v15.docx", "ESM_1_v15.pdf", "Fig1.tif", "Fig2.tif",
            "Fig3.tif", "cover_letter_v15_BCRT.docx", "worklog_v15.md", "MANIFEST_v15.md"]
    scripts = ["manuscript/code/edit_manuscript_v16.py", "manuscript/code/edit_esm_v16.py"]
    d = "manuscript/code/checks_v16"
    checks = sorted(f"{d}/{f}" for f in os.listdir(d) if f.endswith(".py"))
    outs = sorted(f"{d}/out/{f}" for f in os.listdir(f"{d}/out") if os.path.isfile(f"{d}/out/{f}"))
    m15 = open(f"{B}/MANIFEST_v15.md", encoding="utf-8").read()
    src = re.findall(r"\| `([^`]+)` \| ([0-9a-f]{64}) \|", m15)
    L = ["# MANIFEST v16（2026-11-04）", "",
         "- 版本: v16（v15 的小修: 文献第 8 条加存档网址〔两版药价表有 2 个品目不同〕、两处长句拆分、Implications 分段；数值不变）。",
         "- 交付日: 2026-11-04。",
         "- 底本: v15（2026-11-04 交付；现在 manuscript/archive/v15/，下表）。会话开始时 9 个交付物的 sha256 与 MANIFEST_v15 一致。",
         "- tables_v16_BCRT.docx、ESM_1_v16.docx、Fig1〜3.tif、cover_letter_v16_BCRT.docx = v15 的逐字节复制（下表 sha256 与底本相同）。ESM_1_v16.pdf 由 Word（SaveAs2, 17）重新导出（48 页）。",
         "- 数值来源: 本版不改数值，未重算模型。MANIFEST_v15 的来源文件 sha256 重算（下表）。药价表两版的 sha256 见末节。",
         "- 文献: 78 条；第 8 条末尾加 Wayback 存档网址（10/14 版与 11/1 版的注射药清单中トロデルビ、ダトロウェイ的药价不同，worklog_v16.md 第 5 节）；其余不变。",
         "- 公开用代码: 本版无改动（exercise_cea_public，HEAD fbf19be，无远程、未推送）。",
         "", "## 交付物（manuscript/v16/）", ""]
    L += table([(f, sha(f"{V}/{f}")) for f in deliv])
    L += ["", "## 底本（manuscript/archive/v15/）", ""]
    L += table([(f, sha(f"{B}/{f}")) for f in base])
    L += ["", "## 编辑脚本", ""]
    L += table([(f, sha(f)) for f in scripts])
    L += ["", "## 核对脚本与输出（另用 checks_v11/ 的 refcheck.py、sec10.py、fmt_audit.py、word_stats.ps1、word_open_pdf.ps1、citemap.py，checks_v12/pdf_pages.py，checks_v14/ 的 word_wc14.py、acro_extract14.py，edit_esm_v14.py 的 pages14() 与 edit_esm_v15.py 的 locations15()，均未改）", ""]
    L += table([(f, sha(f)) for f in checks + outs])
    L += ["", "## 数值来源文件（MANIFEST_v15 的来源表，sha256 为本版重算值；与 v15 的比较）", "",
          "| 文件 | sha256 | 与 v15 |", "|---|---|---|"]
    nchg = 0
    for p, h in src:
        now = sha(p)
        nchg += now != h
        L.append(f"| `{p}` | {now} | {'一致' if now == h else '变更'} |")
    L += ["", "## 药价表（第 1 步；10/14 版 = 当初保存的原文件，Wayback 存档件与之逐字节相同；11/1 版 = 2026-11-04 下载）", ""]
    L += table([(f"`input/params/sources_price/{f}`", sha(f"input/params/sources_price/{f}"))
                for f in ("tp20261014-01_02.xlsx", "tp20261101-01_02.xlsx")])
    open(f"{V}/MANIFEST_v16.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("written; source files:", len(src), "changed:", nchg)


if __name__ == "__main__":
    main()
