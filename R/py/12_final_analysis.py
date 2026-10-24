"""KEYNOTE-522 final analysis (Schmid P, et al. J Clin Oncol 2026;44(16_suppl):507,
doi:10.1200/JCO.2026.44.16_suppl.507; data cutoff 2025-10-14): 7-year values read by regex from the
saved conference reports in input/papers/kn522_final_analysis/ (the abstract page on ascopubs.org
returned 403 and was not retrieved; CareNet was under maintenance on 2026-10-22).

Usage: .venv/Scripts/python.exe -I R/py/12_final_analysis.py <project_root>
Writes data/kn522_final_7y.csv (one row per value: id, value, lo, hi, outlet, url, file, quote).
"""
import sys, os, re, csv, html
sys.stdout.reconfigure(encoding="utf-8")
root = sys.argv[1]
d = os.path.join(root, "input", "papers", "kn522_final_analysis")
SRC = {
    "OncLive 2026-06-01": ("https://www.onclive.com/view/survival-gains-confirmed-full-keynote-522-data-set-to-redefine-treatment-standards-in-early-stage-tnbc-at-asco-2026",
                           "www.onclive.com_view_survival-gains-confirmed-full-keynote-522-data-set-to-redefine-treatment-standards-in-early-stage-tnbc-at-asco-2026.html"),
    "CancerNetwork 2026-06-01": ("https://www.cancernetwork.com/view/keynote-522-pembrolizumab-durable-efs-os-high-risk-tnbc",
                                 "www.cancernetwork.com_view_keynote-522-pembrolizumab-durable-efs-os-high-risk-tnbc.html"),
    "DelveInsight": ("https://www.delveinsight.com/asco-conference/article/pembrolizumab-keynote-522-results",
                     "www.delveinsight.com_asco-conference_article_pembrolizumab-keynote-522-results.html"),
}


def text(f):
    t = open(os.path.join(d, f), encoding="utf-8", errors="ignore").read()
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))


T = {k: text(v[1]) for k, v in SRC.items()}
F = r"([\d.]+)"
rows = []


def get(outlet, rx, ids):
    m = re.search(rx, T[outlet])
    if m is None:
        raise SystemExit(f"not found in {outlet}: {rx}")
    for i, (vid, groups) in enumerate(ids):
        g = [m.group(j) if j else "" for j in groups]
        rows.append(dict(id=vid, value=g[0], lo=g[1] if len(g) > 1 else "", hi=g[2] if len(g) > 2 else "", outlet=outlet,
                         url=SRC[outlet][0], file=SRC[outlet][1], quote=m.group(0)))


get("OncLive 2026-06-01", r"7-year event-free survival rate of " + F + r"% \(95% CI, " + F + r"%-" + F + r"%\) vs " + F + r"% \(95% CI, " + F + r"%-" + F + r"%\)",
    [("efs7_pembro", (1, 2, 3)), ("efs7_placebo", (4, 5, 6))])
get("OncLive 2026-06-01", r"The 7-year overall survival \(OS\) rates in these respective arms were " + F + r"% \(95% CI, " + F + r"%-" + F + r"%\) and " + F + r"% \(95% CI, " + F + r"%-" + F + r"%;",
    [("os7_pembro", (1, 2, 3)), ("os7_placebo", (4, 5, 6))])
get("OncLive 2026-06-01", r"OS rates for the same population of patients were " + F + r"% and " + F + r"%",
    [("os_pcr_pembro", (1,)), ("os_pcr_placebo", (2,))])
get("OncLive 2026-06-01", r"OS rates in this population of patients in each of the respective arms were " + F + r"% vs " + F + r"%",
    [("os_nonpcr_pembro", (1,)), ("os_nonpcr_placebo", (2,))])
get("CancerNetwork 2026-06-01", r"distant recurrence-free survival rate at 7 years was " + F + r"% vs " + F + r"%",
    [("drfs7_pembro", (1,)), ("drfs7_placebo", (2,))])
get("CancerNetwork 2026-06-01", r"The estimated 7-year OS rate was " + F + r"% with pembrolizumab vs " + F + r"% with placebo",
    [("os7_pembro_check", (1,)), ("os7_placebo_check", (2,))])
get("CancerNetwork 2026-06-01", r"data cutoff of (October 14, 2025), with a median follow-up of " + F + r" months",
    [("data_cutoff", (1,)), ("median_fu_months", (2,))])
get("DelveInsight", r"Patients with pCR OS " + F + r"% " + F + r"% [\d.]+ Patients without pCR EFS [\d.]+% [\d.]+% [\d.]+ Patients without pCR OS " + F + r"% " + F + r"%",
    [("os_pcr_pembro_check", (1,)), ("os_pcr_placebo_check", (2,)), ("os_nonpcr_pembro_check", (3,)), ("os_nonpcr_placebo_check", (4,))])
# round 11 (2026-10-23): stratified EFS by pCR status (the constraint values; OncLive writes "at
# median follow-up", taken as 7-year values by instruction) and the exploratory stratified HRs
get("OncLive 2026-06-01", r"EFS rates for patients who achieved pathological complete responses \(pCR\) at median follow-up in each arm were " + F +
    r"% for the pembrolizumab arm compared with " + F + r"% for the placebo arm \(HR, " + F + r"; 95% CI, " + F + r"-" + F + r"\)",
    [("efs_pcr_pembro", (1,)), ("efs_pcr_placebo", (2,)), ("hr_efs_pcr", (3, 4, 5))])
get("OncLive 2026-06-01", r"EFS rates among patients who did not achieve pCR were " + F + r"% in the pembrolizumab arm and " + F +
    r"% in the placebo arm \(HR, " + F + r"; 95% CI, " + F + r"-" + F + r"\)",
    [("efs_nonpcr_pembro", (1,)), ("efs_nonpcr_placebo", (2,)), ("hr_efs_nonpcr", (3, 4, 5))])
get("OncLive 2026-06-01", r"OS rates for the same population of patients were [\d.]+% and [\d.]+% \(HR, " + F + r"; 95% CI, " + F + r"-" + F + r"\)",
    [("hr_os_pcr_onclive", (1, 2, 3))])
get("OncLive 2026-06-01", r"OS rates in this population of patients in each of the respective arms were [\d.]+% vs [\d.]+% \(HR, " + F + r"; 95% CI, " + F + r"-" + F + r"\)",
    [("hr_os_nonpcr", (1, 2, 3))])
get("OncLive 2026-06-01", r"69\.8% \(95% CI, 65\.0%-74\.2%\) with neoadjuvant placebo plus chemotherapy followed by surgery and adjuvant placebo \(HR, " + F + r"; 95% CI, " + F + r"-" + F + r"\)",
    [("hr_efs_all", (1, 2, 3))])
get("OncLive 2026-06-01", r"77\.2% \(95% CI, 72\.7%-81\.1%; HR, " + F + r"; 95% CI, " + F + r"-" + F + r"\)",
    [("hr_os_all_onclive", (1, 2, 3))])
get("CancerNetwork 2026-06-01", r"among patients who achieved pCR, the OS HR was " + F + r" \(95% CI, " + F + r"–" + F + r"\), and among those who did not, the HR was " + F + r" \(95% CI, " + F + r"–" + F + r"\)",
    [("hr_os_pcr", (1, 2, 3)), ("hr_os_nonpcr_check", (4, 5, 6))])
get("CancerNetwork 2026-06-01", r"\(90 of 390\) of patients in the pembrolizumab and placebo arms, respectively \(HR, " + F + r"; 95% CI, " + F + r"–" + F + r"\)",
    [("hr_os_all", (1, 2, 3))])
get("CancerNetwork 2026-06-01", r"distant recurrence-free survival rate at 7 years was [\d.]+% vs [\d.]+% \(HR, " + F + r"; 95% CI, " + F + r"–" + F + r"\)",
    [("hr_drfs_all", (1, 2, 3))])
get("DelveInsight", r"Patients with pCR EFS " + F + r"% " + F + r"% " + F + r" Patients with pCR OS [\d.]+% [\d.]+% " + F + r" Patients without pCR EFS " + F + r"% " + F + r"% " + F,
    [("efs_pcr_pembro_check", (1,)), ("efs_pcr_placebo_check", (2,)), ("hr_efs_pcr_check", (3,)), ("hr_os_pcr_check", (4,)),
     ("efs_nonpcr_pembro_check", (5,)), ("efs_nonpcr_placebo_check", (6,)), ("hr_efs_nonpcr_check", (7,))])
out = os.path.join(root, "data", "kn522_final_7y.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
v = {r["id"]: r["value"] for r in rows}
for k in ["os7_pembro", "os7_placebo"]:
    assert float(v[k]) == float(v[k + "_check"]), k
for k in ["os_pcr_pembro", "os_pcr_placebo", "os_nonpcr_pembro", "os_nonpcr_placebo",
          "efs_pcr_pembro", "efs_pcr_placebo", "efs_nonpcr_pembro", "efs_nonpcr_placebo", "hr_efs_pcr", "hr_efs_nonpcr", "hr_os_pcr"]:
    assert float(v[k]) == float(v[k + "_check"]), k
hv = {r["id"]: (r["value"], r["lo"], r["hi"]) for r in rows}
assert hv["hr_os_nonpcr"] == hv["hr_os_nonpcr_check"]
assert hv["hr_os_all"] == hv["hr_os_all_onclive"]
# the OS HR for the pCR stratum: CancerNetwork 0.64 [0.37, 1.14] (the value used) vs OncLive [0.39, 1.14]
print("OS HR pCR, CancerNetwork / OncLive:", hv["hr_os_pcr"], hv["hr_os_pcr_onclive"])
print("OS HR all, CancerNetwork / OncLive:", hv["hr_os_all"], hv["hr_os_all_onclive"])
for r in rows:
    print(r["id"], r["value"], r["lo"], r["hi"], r["outlet"])
