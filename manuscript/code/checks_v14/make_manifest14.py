"""Writes manuscript/v14/MANIFEST_v14.md: deliverables, base (v13), editing and check scripts, analysis source files
(the 57 files of MANIFEST_v13 recomputed, and the new four-arm outputs), public-directory changes. Every sha256 is computed
here. Run from the project root after worklog_v14.md is final and before v13 is moved (the base is read from manuscript/v13).
usage: python make_manifest14.py
"""
import hashlib, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
PUB = os.path.join("..", "exercise_cea_public")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def table(rows, head=("文件", "sha256")):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return out


def main():
    V = "manuscript/v14"
    deliv = ["manuscript_v14_BCRT.docx", "tables_v14_BCRT.docx", "ESM_1_v14.docx", "ESM_1_v14.pdf", "Fig1.tif", "Fig2.tif",
             "Fig3.tif", "cover_letter_v14_BCRT.docx", "worklog_v14.md"]
    base = ["manuscript_v13_BCRT.docx", "tables_v13_BCRT.docx", "ESM_1_v13.docx", "ESM_1_v13.pdf", "Fig1.tif", "Fig2.tif",
            "Fig3.tif", "cover_letter_v13_BCRT.docx", "worklog_v13.md", "MANIFEST_v13.md"]
    scripts = ["manuscript/code/edit_manuscript_v14.py", "manuscript/code/edit_tables_v14.py", "manuscript/code/edit_esm_v14.py"]
    checks = sorted("manuscript/code/checks_v14/" + f for f in os.listdir("manuscript/code/checks_v14") if f.endswith(".py"))
    outs = sorted("manuscript/code/checks_v14/out/" + f for f in os.listdir("manuscript/code/checks_v14/out")
                  if os.path.isfile("manuscript/code/checks_v14/out/" + f))
    plogs = sorted("manuscript/code/checks_v14/out/pub_logs/" + f for f in os.listdir("manuscript/code/checks_v14/out/pub_logs"))
    man13 = open("manuscript/v13/MANIFEST_v13.md", encoding="utf-8").read().split("## 数值来源文件")[1]
    src = re.findall(r"\| `([^`]+)` \| ([0-9a-f]{64}) \|", man13)
    new_src = ["output/phase2/fourarm_report.md"] + ["output/phase2/main/fourarm_%s.csv" % k for k in
               ("totals", "incremental", "nmb_equal", "checks", "run", "test_runs", "unit_tests")] + ["R/25_four_arm.R", "R/test_four_arm.R"]
    pub = ["R/25_four_arm.R", "R/test_four_arm.R", "README.md", "input/params/cohort_N_jbcs2024.csv"]
    L = ["# MANIFEST v14（2026-11-04）", "",
         "- 版本: v14（共著者指示的结构改稿: Results 改为「四组 → 运动对帕博利珠单抗 → 上乗せ」；尾崎 2026-11-04 邮件；计算见 commit 11d484b）。",
         "- 交付日: 2026-11-04。",
         "- 底本: v13（2026-10-29 交付；现在 manuscript/archive/v13/，下表）。会话开始时 9 个交付物的 sha256 与 MANIFEST_v13 一致。",
         "- Fig1〜3.tif 与 cover_letter_v14_BCRT.docx = v13 的逐字节复制（下表 sha256 与底本相同）。ESM_1_v14.pdf 由 Word（SaveAs2, 17）从 ESM_1_v14.docx 导出（48 页）。",
         "- 数值来源: 新数值来自 output/phase2/fourarm_report.md 与 main/fourarm_*.csv（11d484b）；其余为 v13 的表与 ESM 中的值。v13 MANIFEST 的 57 个来源文件 sha256 重算: 变更 1（docs/analysis_plan_phase2.md，计划第 11 节），其余一致（下表）。",
         "- 文献: 78 条，文字与 v13 相同（正文 1〜71，72〜78 只在 Table 1 与 ESM）。核对结果见 worklog_v14.md 第 7 节第 2 项与 AUDIT（第 8 条网址 404、第 71 条 Crossref 已有卷页）。",
         "- 公开用代码: C:\\Users\\原明美\\Documents\\ClaudeCode\\exercise_cea_public\\（作业树外）；本地 git commit 4a883ed（父 9b02039）；108 个文件；无远程、未推送。",
         "", "## 交付物（manuscript/v14/）", ""]
    L += table([(f, sha(os.path.join(V, f))) for f in deliv])
    L += ["", "## 底本（manuscript/archive/v13/）", ""]
    L += table([(f, sha(os.path.join("manuscript/v13", f))) for f in base])
    L += ["", "## 编辑脚本", ""]
    L += table([(f, sha(f)) for f in scripts])
    L += ["", "## 核对脚本与输出（另用 checks_v11/ 的 refcheck.py、sec10.py、fmt_audit.py、word_stats.ps1、word_open_pdf.ps1、citemap.py，checks_v12/pdf_pages.py，checks_v13/public_name_scan.py，edit_esm_v12.py 的 pages()/locations()，均未改）", ""]
    L += table([(f, sha(f)) for f in checks + outs + plogs])
    L += ["", "## 数值来源文件（v13 MANIFEST 的 57 个，sha256 为本版重算值；与 v13 的比较）", "",
          "| 文件 | sha256 | 与 v13 |", "|---|---|---|"]
    for p, h in src:
        now = sha(p)
        L.append(f"| `{p}` | {now} | {'一致' if now == h else '变更'} |")
    L += ["", "## 本版新增的数值来源（11d484b）", ""]
    L += table([(f"`{p}`", sha(p)) for p in new_src])
    L += ["", "## 公开目录中本版新增或修改的文件（commit 4a883ed）", ""]
    L += table([(p, sha(os.path.join(PUB, p))) for p in pub])
    open(os.path.join(V, "MANIFEST_v14.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("written; source files changed:", sum(sha(p) != h for p, h in src), "of", len(src))


if __name__ == "__main__":
    main()
