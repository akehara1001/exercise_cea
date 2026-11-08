"""Planted-violation tests for the checks added in v19 (WRITING_RULES 13: a new check is rung once on a deliberate violation
before it is used). Writes three altered copies of manuscript_v19_BCRT.docx to <tmp_dir> (never into the work tree):
  bell_regress.docx  one word changed in Introduction paragraph 1 (not in any edit log)  -> regress19 must report UNEXPLAINED 1
  bell_tfnum/        "(Table S12)" appended to Introduction paragraph 1 (S12 cited before S1) -> tfnum19 first-mention order must fail
  bell_sec10.docx    "delve" inserted in Discussion paragraph 1                          -> sec10_19 must count 1 banned word
usage: python bell19.py <v18_dir> <v19_dir> <tmp_dir>
"""
import io, os, shutil, subprocess, sys
import docx

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))


def alter(src, dst, startswith, old, new):
    d = docx.Document(src)
    p = [p for p in d.paragraphs if p.text.startswith(startswith)]
    assert len(p) == 1
    r = [r for r in p[0].runs if old in r.text][0]
    r.text = r.text.replace(old, new, 1)
    d.save(dst)


def run(args):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True, encoding="utf-8").stdout


def main(d18, d19, tmp):
    os.makedirs(tmp, exist_ok=True)
    m19 = os.path.join(d19, "manuscript_v19_BCRT.docx")
    intro = "Triple-negative breast cancer (TNBC) recurs more often"
    # 1 regress19
    b1 = os.path.join(tmp, "bell_regress.docx")
    alter(m19, b1, intro, "recurs more often", "recurs more frequently")
    out = run([os.path.join(HERE, "regress19.py"), os.path.join(d18, "manuscript_v18_BCRT.docx"), b1,
               os.path.join(HERE, "out", "m19_log.json"), "bell"])
    un = [l for l in out.splitlines() if "UNEXPLAINED:" in l]
    print("regress19 planted change ->", un, "| fired:", un and un[0].strip() != "UNEXPLAINED: 0")
    # 2 tfnum19 (needs a full v19 directory)
    d2 = os.path.join(tmp, "bell_tfnum"); os.makedirs(d2, exist_ok=True)
    for f in os.listdir(d19):
        if f.endswith((".docx", ".tif")):
            shutil.copyfile(os.path.join(d19, f), os.path.join(d2, f))
    alter(m19, os.path.join(d2, "manuscript_v19_BCRT.docx"), intro, "diagnosis [1].", "diagnosis [1] (Table S12).")
    out = run([os.path.join(HERE, "tfnum19.py"), d2])
    ln = [l for l in out.splitlines() if l.strip().startswith("Table S ") or "ALL SERIES PASS" in l]
    print("tfnum19 planted early S12 ->", ln, "| fired:", any("ALL SERIES PASS: False" in l for l in ln))
    # 3 sec10_19
    b3 = os.path.join(tmp, "bell_sec10.docx")
    alter(m19, b3, "If exercise lowered the recurrence hazard by 5% or more, both strategies without it were dominated (Tables",
          "so the choice in Japan", "so, to delve further, the choice in Japan")
    out = run([os.path.join(HERE, "sec10_19.py"), b3])
    ln = [l for l in out.splitlines() if l.startswith("banned words")][0]
    print("sec10_19 planted 'delve' ->", ln, "| fired:", "delve" in ln)


if __name__ == "__main__":
    main(*sys.argv[1:4])
