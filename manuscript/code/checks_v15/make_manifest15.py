"""Writes manuscript/v15/MANIFEST_v15.md (every sha256 computed here): deliverables, base (v14), editing and check
scripts, the analysis source files of MANIFEST_v14 (both tables) recomputed and compared, public-directory change.
Run from the project root after worklog_v15.md is final and before v14 is moved (the base is read from manuscript/v14).
usage: python make_manifest15.py
"""
import hashlib, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
PUB = os.path.join("..", "exercise_cea_public")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def table(rows, head=("文件", "sha256")):
    return ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(r) + " |" for r in rows]


def main():
    V, B = "manuscript/v15", "manuscript/v14"
    deliv = ["manuscript_v15_BCRT.docx", "tables_v15_BCRT.docx", "ESM_1_v15.docx", "ESM_1_v15.pdf", "Fig1.tif", "Fig2.tif",
             "Fig3.tif", "cover_letter_v15_BCRT.docx", "worklog_v15.md"]
    base = ["manuscript_v14_BCRT.docx", "tables_v14_BCRT.docx", "ESM_1_v14.docx", "ESM_1_v14.pdf", "Fig1.tif", "Fig2.tif",
            "Fig3.tif", "cover_letter_v14_BCRT.docx", "worklog_v14.md", "MANIFEST_v14.md"]
    scripts = ["manuscript/code/edit_manuscript_v15.py", "manuscript/code/edit_tables_v15.py", "manuscript/code/edit_esm_v15.py",
               "R/22_phase2b_main.R"]
    d = "manuscript/code/checks_v15"
    checks = sorted(f"{d}/{f}" for f in os.listdir(d) if f.endswith(".py"))
    outs = sorted(f"{d}/out/{f}" for f in os.listdir(f"{d}/out") if os.path.isfile(f"{d}/out/{f}"))
    m14 = open(f"{B}/MANIFEST_v14.md", encoding="utf-8").read()
    src = re.findall(r"\| `([^`]+)` \| ([0-9a-f]{64}) \|", m14)
    L = ["# MANIFEST v15（2026-11-04）", "",
         "- 版本: v15（v14 的删减与修正: 正文压到 BCRT 上限以内〔3,470 词〕、文献第 71 条更新、v14 报告的小项；文献第 8 条未改）。",
         "- 交付日: 2026-11-04。",
         "- 底本: v14（2026-11-04 交付；现在 manuscript/archive/v14/，下表）。会话开始时 9 个交付物的 sha256 与 MANIFEST_v14 一致。",
         "- Fig1〜3.tif 与 cover_letter_v15_BCRT.docx = v14 的逐字节复制。ESM_1_v15.pdf 由 Word（SaveAs2, 17）从 ESM_1_v15.docx 导出（48 页）。",
         "- 数值来源: 本版不加新数值，未重算模型。MANIFEST_v14 的来源文件 sha256 重算（下表）。R/22_phase2b_main.R 只改第 112 行注释（3d）。",
         "- 文献: 78 条；第 71 条按 Crossref 与 PubMed 更新为 Ann Oncol 37:1467–1479；第 8 条未改（网址 404，同一日期的清单站内找不到，worklog_v15.md 第 6 节）。",
         "- 公开用代码: C:\\Users\\原明美\\Documents\\ClaudeCode\\exercise_cea_public\\（作业树外）；本地 git commit fbf19be（父 4a883ed）；无远程、未推送。",
         "", "## 交付物（manuscript/v15/）", ""]
    L += table([(f, sha(f"{V}/{f}")) for f in deliv])
    L += ["", "## 底本（manuscript/archive/v14/）", ""]
    L += table([(f, sha(f"{B}/{f}")) for f in base])
    L += ["", "## 编辑脚本与改动的代码", ""]
    L += table([(f, sha(f)) for f in scripts])
    L += ["", "## 核对脚本与输出（另用 checks_v11/ 的 refcheck.py、sec10.py、fmt_audit.py、word_stats.ps1、word_open_pdf.ps1、citemap.py，checks_v12/pdf_pages.py，checks_v14/ 的 word_wc14.py、acro_extract14.py、edit_esm_v14.py 的 pages14()/locations14()，均未改）", ""]
    L += table([(f, sha(f)) for f in checks + outs])
    L += ["", "## 数值来源文件（MANIFEST_v14 的两张来源表，sha256 为本版重算值；与 v14 的比较）", "",
          "| 文件 | sha256 | 与 v14 |", "|---|---|---|"]
    nchg = 0
    for p, h in src:
        now = sha(p)
        nchg += now != h
        L.append(f"| `{p}` | {now} | {'一致' if now == h else '变更'} |")
    L += ["", "## 公开目录中本版修改的文件（commit fbf19be）", ""]
    L += table([("R/22_phase2b_main.R", sha(os.path.join(PUB, "R", "22_phase2b_main.R")))])
    open(f"{V}/MANIFEST_v15.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("written; source files:", len(src), "changed:", nchg)


if __name__ == "__main__":
    main()
