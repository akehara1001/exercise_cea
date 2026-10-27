"""Each cited statement next to the passage of the source that supports it (rules 1.3 and 13).

CLAIMS holds, for every citation in the text of the manuscript (paragraph id and sentence number, as in
_build/_ledger_manuscript.json) and in the prose of the figure legends and the supplement (located by the text
before the marker), the cited work, the passage and where the passage was read:
- abstract: the PubMed abstract (pubmed_meta.json);
- crossref: the abstract in the Crossref record (support_cache.json);
- pmc:<id>: the Europe PMC full-text XML (read from the directory passed to check(); sha256 in support_cache.json);
- affil: the author affiliations of the PubMed record (support_cache.json);
- check: the check of a document or web page in references.py (GREY or ABSTRACT);
- file:<path>: a project file in which the location in the source was recorded when the value was read
  (for values read from figures, tables and appendices of articles that are not open access).
status: ok, the passage is in the source; corroborated, the passage is in another cited work because the cited original is
not open access; report, the value was read in a report of a conference presentation
because the original was not available; provided, the value was provided by a co-author and the original was not seen.
Source cells of tables (the Source column of Table 1 and Supplementary Table S2) are listed by
make_references_doc.py from the parameter workbook (出典, 出典の該当箇所) and PANEL_A below.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def C(loc, key, src, *quotes, status="ok", note=""):
    return dict(loc=loc, key=key, src=src, quotes=list(quotes), status=status, note=note)


KN7 = "data/kn522_final_7y.csv"
USV = "input/user_supplied_values.csv"
MS = "docs/model_spec.md"
P1R = "output/phase1/phase1_report.md"
JB = "input/params/cohort_N_jbcs2024.csv"
REP_KN = ("stratified 7-year values are not in the abstract; they were read in reports of the ASCO 2026 presentation "
          "(OncLive and DelveInsight, data/kn522_final_7y.csv); the citation is to the abstract of record")
REP_ESMO = ("abstract LBA18 not obtained (publisher page HTTP 403); values read in the OncLive report of the ESMO 2023 "
            "presentation (input/user_supplied_values.csv); original source to be confirmed by A. Ozaki (docs/model_spec.md line 87)")
PROV = "values sent by A. Ozaki on 2026-10-26; the members-only report was not seen"

CLAIMS = [
    # ---------------------------------------------------------------- Introduction
    C("I.1 s1", "dent2007", "abstract", "increased likelihood of distant recurrence (hazard ratio, 2.6; 95% confidence interval, 2.0-3.5; P < 0.0001) and "
      "death (hazard ratio, 3.2; 95% confidence interval, 2.3-4.5; P < 0.001) within 5 years of diagnosis but not thereafter"),
    C("I.1 s2", "liedtke2008", "abstract", "those with pCR have excellent survival. However, patients with RD after neoadjuvant chemotherapy have "
      "significantly worse survival if they have TNBC compared with non-TNBC"),
    C("I.1 s3", "schmid2020", "abstract", "the percentage of patients with a pathological complete response was 64.8% (95% confidence interval [CI], "
      "59.9 to 69.5) in the pembrolizumab-chemotherapy group and 51.2% (95% CI, 44.1 to 58.3) in the placebo-chemotherapy group"),
    C("I.1 s3", "schmid2022", "abstract", "resulted in significantly longer event-free survival than neoadjuvant chemotherapy alone"),
    C("I.1 s3", "schmid2024", "abstract", "resulted in a significant improvement, as compared with neoadjuvant chemotherapy alone, in overall survival"),
    C("I.1 s4", "licata2025", "abstract", "Recurrences within 24 months account for most recurrences in patients with TNBC who relapse after neoadjuvant "
      "chemo-immunotherapy."),
    C("I.1 s5", "jbcs55", f"file:{JB}", '"nac_total","TNBC（M0）II、III 期的术前化疗例（2024 年）","3451"', '"nac_pembro","其中术前用帕博利珠单抗","2294"',
      status="provided", note=PROV),
    C("I.1 s6", "schmid2020", "abstract", "the two groups then received an additional four cycles of pembrolizumab or placebo",
      "After definitive surgery, the patients received adjuvant pembrolizumab or placebo every 3 weeks for up to nine cycles."),
    C("I.1 s6", "price2026", "xlsx:input/params/sources_price/tp20261014-01_02.xlsx", "キイトルーダ点滴静注１００ｍｇ", "199462",
      note="100 mg vial JPY 199,462; one 200 mg dose = 2 vials = JPY 398,924"),
    C("I.2 s1", "courneya2025", "abstract", "A 3-year structured exercise program initiated soon after adjuvant chemotherapy for colon cancer resulted in "
      "significantly longer disease-free survival"),
    C("I.2 s2", "courneya2025", "abstract", "hazard ratio for disease recurrence, new primary cancer, or death, 0.72; 95% confidence interval [CI], 0.55 to 0.94"),
    C("I.2 s3", "furmaniak2016", "abstract", "physical exercise during adjuvant treatment for breast cancer probably improves physical fitness",
      "and slightly reduces fatigue"),
    C("I.2 s3", "courneya2007", "abstract", "they did improve self-esteem, physical fitness, body composition, and chemotherapy completion rate",
      note="fatigue: 'favored the exercise groups but did not reach statistical significance'"),
    C("I.2 s3", "vanwaart2015", "abstract", "Onco-Move and OnTrack resulted in less decline in cardiorespiratory fitness (P < .001)",
      "OnTrack also resulted in better outcomes for muscle strength (P = .002) and physical fatigue (P < .001)"),
    C("I.2 s3", "mijwel2018", "abstract", "16 weeks of resistance and HIIT was effective in preventing increases in CRF",
      note="CRF, cancer-related fatigue; cited for fatigue"),
    C("I.2 s4", "courneya2014", "abstract", "we report an exploratory follow-up of cancer outcomes",
      "(HR, 0.68; 95% confidence interval (CI), 0.37-1.24; log-rank, P = 0.21)"),
    C("I.2 s5", "sanft2023", "abstract", "Among 72 women who received neoadjuvant chemotherapy, women randomly assigned to intervention were more likely "
      "to have a pCR than those randomly assigned to UC (53% v 28%; P = .037)"),
    C("I.2 s5", "kjeldsted2025", "abstract", "received supervised high-intensity interval training and progressive resistance training",
      "Although the exercise program did not affect tumor size"),
    C("I.2 s5", "schmidt2025", "abstract", "supervised resistance training",
      "Overall, there was no significant difference in post-intervention tumor size between RT or AT and WCG."),
    C("I.2 s6", "diasrato2026", "abstract", "Eight studies involving 504 patients with breast, esophageal, gastric, or rectal cancer were included",
      "there were no significant differences between exercise and control groups in the rate of pCR to NACT"),
    C("I.2 s7", "deboniface2022", "abstract", "The primary endpoint is pCR", "disease-free survival at 2, 5 and 10 years",
      "In order to show an improvement in pCR of 10%, a total of 712 participants need to be included in the analysis.",
      "The Neo-ACT has been registered at clinicaltrials.gov on January 11, 2022"),
    # v6: paragraph 3 replaced by the user's text (four sentences); the Phys-Can sentence moved here from paragraph 4
    C("I.3 s1", "khan2019", "pmc:PMC6548756", "post-operative exercise versus control [ 12 , 26 ], exercise versus control during adjuvant breast cancer "
      "treatment [ 13 , 25 , 27 , 28 ] and exercise versus control following breast cancer treatment [ 29 ]",
      "all but one study included in this systematic review measured health consequences in terms of QALYs",
      "change in body mass index (BMI) and cardiorespiratory fitness [ 25 ]", "fatigue and QALYs [ 28 ]"),
    C("I.3 s1", "gublergut2021", "pmc:PMC8521580", "OnTrack could be cost-effective for general and physical fatigue depending on willingness to pay",
      "Cardiorespiratory fitness showed a short- and long-term increase in the low-to-moderate- and high-intensity groups [ 56 ]"),
    C("I.3 s1", "wang2023", "abstract", "Exercise interventions were found to be cost-effective in five of ten (50%) trial-based economic evaluations "
      "and in five of the six (83%) model-based economic evaluations.",
      note="study designs and outcomes; the outcomes measured are shown by the full texts of khan2019 and gublergut2021"),
    C("I.3 s1", "may2017", "abstract", "the 18-week exercise programme was cost-effective for colon cancer, but not for breast cancer"),
    C("I.3 s1", "vanwaart2018", "abstract", "Depending on the decision-makers' willingness-to-pay, OnTrack could be considered cost-effective in comparison with UC."),
    C("I.3 s1", "perrier2020", "abstract", "The 6-month exercise program was deemed to be cost-effective compared with usual care for the estimated aerobic capacity."),
    C("I.3 s2", "ax2023", "abstract", "a six-month exercise programme of high (HI) or low-to-moderate intensity (LMI) during (neo)adjuvant oncological treatment",
      "189 participants with breast, colorectal, or prostate cancer"),
    C("I.3 s3", "boudewijns2023", "abstract", "The headroom analysis is an early economic evaluation that quantifies the highest price at which an "
      "intervention may still be cost effective."),
    C("I.3 s4", "huang2023", "abstract", "for patients with high-risk eTNBC in the USA"),
    C("I.3 s4", "kwong2024", "abstract", "from a Hong Kong third-party payer perspective"),
    C("I.3 s4", "favrebulle2024", "abstract", "from a Swiss third-party payer perspective"),
    C("I.3 s4", "pollinger2025", "abstract", "from an Egyptian societal perspective"),
    C("I.3 s4", "chisaki2025", "abstract", "patients with PD-L1-positive inoperable or metastatic TNBC from a Japanese healthcare perspective"),
    C("I.3 s4", "sugiura2023", "abstract", "microsatellite-instability-high/mismatch repair-deficient metastatic colorectal cancer",
      "The Japanese healthcare payer's perspective was adopted."),
    C("I.3 s4", "taniguchi2026", "abstract", "advanced colorectal cancer with high microsatellite instability or mismatched repair deficiency in Japan"),
    C("I.3 s4", "kakinuma2025", "abstract", "advanced esophageal cancer", "from a Japanese healthcare payer perspective"),
    C("I.3 s4", "morimoto2026", "abstract", "HER2-negative unresectable advanced or recurrent gastric cancer", "from the Japanese healthcare payer perspective"),
    C("I.3 s4", "tomura2025", "abstract", "stage IV advanced NSCLC", "in Japan"),
    C("I.3 s4", "kashiwa2024", "abstract", "advanced biliary tract cancer", "from the perspective of Japanese healthcare payer"),
    C("I.3 s4", "c2h_list", "check", "pembrolizumab (キイトルーダ) not among them"),
    # ---------------------------------------------------------------- Methods
    C("M.SB.1 s2", "schmid2020", "abstract", "patients with previously untreated stage II or stage III triple-negative breast cancer to receive neoadjuvant therapy"),
    C("M.SB.1 s2 (age 49)", "schmid2020", "pmc:PMC9988745", "based on an average starting age of 49 years from KEYNOTE-522", status="corroborated",
      note="the age is in the baseline table of the trial report, which is not open access; passage from the full text of huang2023"),
    C("M.SB.1 s5", "jbcs55", f"file:{JB}", '"nac_pembro","其中术前用帕博利珠单抗","2294"', status="provided", note=PROV),
    C("M.SB.2 s2", "c2h_guideline", "check", "Both cost and effectiveness should be discounted at a rate of 2% per year"),
    C("M.SB.2 s3", "hasegawa2020", "abstract", "If the cost per quality-adjusted life-year (QALY) threshold falls below ¥5 million per QALY"),
    C("M.SB.2 s3", "mhlw_ce2026", "check", "thresholds 500万円/QALY"),
    C("M.SB.2 s4", "mhlw_ce2026", "check", "malignant tumour (ウ 悪性腫瘍)", "750万円/QALY for products given consideration in the comprehensive assessment"),
    C("M.SB.3 s1", "schmid2022", "abstract", "data cutoff, March 23, 2021"),
    C("M.SB.3 s1", "esmo2023", f"file:{USV}", "ESMO 2023; data cutoff 2023-03-23, median follow-up 63.1 months", status="report", note=REP_ESMO),
    C("M.SB.3 s1", "schmid2024", "abstract", "At the data-cutoff date (March 22, 2024)"),
    C("M.SB.3 s1", "kn522final2026", "crossref", "At the data cutoff date (October 14, 2025)"),
    C("M.SB.3 s4", "husereau2022", "abstract", "This summary article presents the new CHEERS 2022 28-item checklist"),
    C("M.VAR.1 s4", "courneya2025", "abstract", "0.72; 95% confidence interval [CI], 0.55 to 0.94"),
    C("M.VAR.2 s5", "courneya2025", "abstract", "Musculoskeletal adverse events occurred more often in the exercise group than in the health-education group "
      "(in 18.5% vs. 11.5% of patients)."),
    C("M.VAR.3 s2", "chan2026", "abstract", "despite an up-front cost of $2,917 (CAD)/participant to provide the SEP", "Mean costs (2024 in Canadian dollars [CAD])"),
    C("M.VAR.3 s2", "worldbank_ppp", "check", "indicator page PA.NUS.PPP"),
    C("M.VAR.3 s3", "fee2026", "check", "令和８年度診療報酬改定について"),
    C("M.VAR.4 s1", "guyot2012", "abstract", "we propose a method which derives from the published Kaplan Meier survival curves a close approximation to the "
      "original individual patient time-to-event data"),
    C("M.VAR.4 s1", "schmid2022", f"file:{P1R}", "| K22_S4_EFS_by_pCR | Schmid 2022 NEJM 386:556 appendix | Fig. S4 |",
      note="EFS by arm and pCR status, supplementary appendix Fig. S4"),
    C("M.VAR.4 s2", "kn522final2026", f"file:{KN7}", "EFS rates for patients who achieved pathological complete responses (pCR) at median follow-up "
      "in each arm were 90.4% for the pembrolizumab arm compared with 85.9% for the placebo arm", "Patients without pCR EFS 57.6% 49.7%",
      status="report", note=REP_KN),
    C("M.VAR.4 s3", "grinda2023", "abstract", "Epidemio-Strategy-Medico-Economical-Metastatic Breast Cancer (ESME-MBC) database, a multicenter, national, observational cohort"),
    C("M.VAR.4 s3", "grinda2023", "affil", "Gustave Roussy", "Villejuif, France", note="French centres"),
    C("M.VAR.4 s5", "lifetable2025", "check", "令和7年簡易生命表の概況"),
    C("M.VAR.5 s2", "price2026", "check", "HTTP 200 (xlsx) on 2026-10-26"),
    C("M.VAR.5 s2", "fee2026", "check", "令和８年度診療報酬改定について"),
    C("M.VAR.5 s3", "schmid2022", "abstract", "Adverse events occurred predominantly during the neoadjuvant phase"),
    C("M.VAR.5 s3", "ema2022", "check", "Assessment report Keytruda"),
    C("M.VAR.5 s4", "favrebulle2024", "pmc:PMC10781656", "Health state utility values used in the base case were derived from EQ-5D-5L data collected in the KEYNOTE-522 trial",
      "There is no EQ-5D value set for Switzerland; therefore, the model used the German value set in the base-case analysis"),
    C("M.VAR.5 s4", "ludwig2018", "abstract", "to develop a value set for EQ-5D-5L based on the societal preferences of the German population"),
    C("M.VAR.5 s6", "iwatani2021", "pmc:PMC8535054", "HSUVs calculated using the EQ-5D-5L derived from the Japanese value set"),
    C("M.VAR.5 s6", "shiroiwa2017", "abstract", "some of the randomized patients participated in an EQ-5D survey (N = 391)"),
    C("M.SA.2 s2", "schmid2024", "abstract", "Overall survival was a secondary end point."),
    C("M.SA.2 s2", "kn522final2026", "crossref", "The 7-yr OS rate (95% CI) was 85.1% (82.5-87.5) in the pembro group vs 77.2% (72.7-81.1) in the pbo group"),
    C("M.SA.6 s2", "huang2023", "pmc:PMC9988745", "US 5L value set [ 25 ] for the base case"),
    C("M.SA.6 s2", "kwong2024", "pmc:PMC11333381", "Utilities based on the UK EQ-5D-5L value set were used in the base case analysis."),
    C("M.SA.6 s2", "pbac2023", "check", "heading from p.1 of the downloaded document",
      note="PSD p.18 'Utilities were based on EQ-5D responses in KN-522' (input/params/sources_utility/PBAC_PSD_pembrolizumab_early-TNBC_2023-03.pdf); "
           "the value set is not named, so the text says 'those of the Australian reimbursement submission'"),
    C("M.SA.6 s3", "fedele2026", "abstract", "We conducted a retrospective multicenter analysis of 209 consecutive patients with early-stage TNBC treated "
      "with neoadjuvant chemo-immunotherapy."),
    C("M.SA.6 s3", "fedele2026", "affil", "Bari, Italy", note="Italian centres"),
    C("M.SA.6 s4", "elmore2021", "abstract", "Median overall survival (OS) time for patients with progression was 26 months", "identified from a prospective database"),
    C("M.SA.6 s4", "elmore2021", "affil", "The University of Texas MD Anderson Cancer Center, Houston, TX, USA", note="single centre"),
    C("M.SA.6 s5", "cortes2011", "abstract", "We aimed to compare overall survival of heavily pretreated patients receiving eribulin versus currently available treatments."),
    C("M.SA.6 s5", "masuda2017", "abstract", "the addition of adjuvant capecitabine therapy was safe and effective in prolonging disease-free survival"),
    C("M.SA.6 s5", "tutt2021", "abstract", "adjuvant olaparib after completion of local treatment and neoadjuvant or adjuvant chemotherapy"),
    C("M.SA.6 s5", "garber2026", "abstract", "1 year of adjuvant olaparib after (neo)adjuvant chemotherapy demonstrated ongoing clinically meaningful improvements"),
    C("M.SA.7 s2", "jbcs55", f"file:{JB}", '"nac_pembro","其中术前用帕博利珠单抗","2294"', status="provided", note=PROV),
    # ---------------------------------------------------------------- Discussion, Implications, Limitations (v7; text of the user)
    C("D.3 s2", "licata2025", "abstract", "Recurrences within 24 months account for most recurrences in patients with TNBC who relapse after neoadjuvant "
      "chemo-immunotherapy."),
    C("D.4 s3", "courneya2025", "abstract", "0.72; 95% confidence interval [CI], 0.55 to 0.94"),
    C("D.4 s3", "courneya2014", "abstract", "(HR, 0.68; 95% confidence interval (CI), 0.37-1.24; log-rank, P = 0.21)",
      note="exploratory follow-up of one trial; the text calls both 'much smaller' than the HR of 0.425 of Table 3"),
    C("D.4 s5", "jbcs55", f"file:{JB}", '"nac_total","TNBC（M0）II、III 期的术前化疗例（2024 年）","3451"', '"nac_pembro","其中术前用帕博利珠单抗","2294"',
      status="provided", note=PROV),
    C("D.5 s1", "huang2023", "abstract", "The incremental cost per QALY gained was $27,285, which is lower than all commonly cited US willingness-to-pay thresholds.",
      "is considered a cost-effective option for high-risk eTNBC in the USA"),
    C("D.5 s1", "kwong2024", "abstract", "which were lower than the World Health Organization (WHO) cost-effectiveness threshold of three times gross domestic "
      "product (GDP) per capita for Hong Kong", "pembrolizumab + chemotherapy represents a cost-effective proposition"),
    C("D.5 s1", "favrebulle2024", "abstract", "Base-case results estimated an ICER of 14,114 Swiss francs (CHF)/QALY",
      "was cost-effective versus chemotherapy alone in patients with high-risk, early-stage TNBC in Switzerland"),
    C("D.5 s1", "pollinger2025", "abstract", "both of which were lower than the 2022 Egyptian cost-effectiveness threshold",
      "In Egypt, pembrolizumab + chemotherapy/pembrolizumab is a cost-effective treatment"),
    C("D.5 s3", "c2h_list", "check", "pembrolizumab (キイトルーダ) not among them"),
    # v8: paragraph 6 replaced by the user's text
    C("D.6 s1", "chan2026", "abstract", "demonstrated that a 3-year structured exercise program (SEP) improved disease-free and overall survival",
      "This prespecified economic evaluation used prospectively collected data from all trial participants",
      "Major cost drivers were cancer recurrence or new malignancy and anticancer therapy."),
    C("D.6 s2", "chan2026", "abstract", "included direct health care costs over a 5-year time horizon", "versus health education materials (HEM)",
      "The SEP was less costly and more effective than HEM.", "Major cost drivers were cancer recurrence or new malignancy and anticancer therapy."),
    C("D.6 s3", "khan2019", "pmc:PMC6548756", "exercise versus control during adjuvant breast cancer treatment [ 13 , 25 , 27 , 28 ] and exercise versus "
      "control following breast cancer treatment [ 29 ]", "change in body mass index (BMI) and cardiorespiratory fitness [ 25 ]", "fatigue and QALYs [ 28 ]"),
    C("D.6 s3", "gublergut2021", "pmc:PMC8521580", "OnTrack could be cost-effective for general and physical fatigue depending on willingness to pay",
      "Cardiorespiratory fitness showed a short- and long-term increase in the low-to-moderate- and high-intensity groups [ 56 ]"),
    C("D.6 s3", "wang2023", "abstract", "Exercise interventions were found to be cost-effective in five of ten (50%) trial-based economic evaluations "
      "and in five of the six (83%) model-based economic evaluations.",
      note="the reviews contain evaluations of effects on fatigue, fitness or quality of life (full texts of khan2019 and gublergut2021); "
           "the sentence refers to those evaluations, not to every evaluation in the reviews"),
    C("D.7 s2", "jbcs55", f"file:{JB}", '"pcr_registry","登录中术前化疗例的 pCR（ypT0/is N0，2024 年）","0.47"', status="provided", note=PROV),
    # v8: fitness only; mijwel2018 (no fitness outcome) removed by the user's decision of 2026-10-27
    C("IMP.1 s1", "furmaniak2016", "abstract", "physical exercise during adjuvant treatment for breast cancer probably improves physical fitness",
      note="the trials of the review were during adjuvant treatment; the sentence applies them to neoadjuvant chemotherapy"),
    C("IMP.1 s1", "courneya2007", "abstract", "breast cancer patients initiating adjuvant chemotherapy",
      "they did improve self-esteem, physical fitness, body composition, and chemotherapy completion rate",
      note="adjuvant chemotherapy; the sentence applies the result to neoadjuvant chemotherapy"),
    C("IMP.1 s1", "vanwaart2015", "abstract", "patients undergoing adjuvant chemotherapy for breast cancer",
      "Onco-Move and OnTrack resulted in less decline in cardiorespiratory fitness (P < .001)",
      note="adjuvant chemotherapy; the sentence applies the result to neoadjuvant chemotherapy"),
    C("L.2 s1", "grinda2023", "abstract", "All ESME patients diagnosed between 2008 and 2020",
      note="the abstract gives the period of diagnosis; 'largely before immunotherapy and antibody-drug conjugates' is inferred from that period "
           "and is not stated in the abstract"),
    # ---------------------------------------------------------------- figure legends and supplement (located by the text before the marker)
    C("figures: CHALLENGE trial", "courneya2025", "abstract", "hazard ratio for disease recurrence, new primary cancer, or death, 0.72"),
    C("S2 Panel A source: KEYNOTE-522 population", "schmid2020", "pmc:PMC9988745", "based on an average starting age of 49 years from KEYNOTE-522",
      status="corroborated", note="starting age; baseline table of the trial report not open access; passage from the full text of huang2023"),
    C("supplement: Checklist and guidance as published", "husereau2022", "abstract", "This summary article presents the new CHEERS 2022 28-item checklist"),
    C("supplement: with a data cutoff of 23 March 2021", "schmid2022", f"file:{P1R}", "| K22_S4_EFS_by_pCR | Schmid 2022 NEJM 386:556 appendix | Fig. S4 |"),
    C("supplement: with a data cutoff of 22 March 2024", "schmid2024", f"file:{P1R}", "| K24_S4_OS_by_pCR | Schmid 2024 NEJM 391:1981 appendix | Fig. S4 |",
      note="overall survival by arm: Fig. 1A of the 2024 report (phase1_report line 333)"),
    C("supplement: algorithm of Guyot and colleagues", "guyot2012", "abstract", "We develop an algorithm that maps from digitised curves back to KM data"),
    C("supplement: Japanese life table for women", "lifetable2025", "check", "令和7年簡易生命表の概況"),
    C("supplement: reported at a later data cutoff was selected", "esmo2023", f"file:{USV}", "ESMO 2023; data cutoff 2023-03-23, median follow-up 63.1 months",
      status="report", note=REP_ESMO),
    C("supplement: fixed at the value of the final analysis", "kn522final2026", f"file:{KN7}", "Patients without pCR EFS 57.6% 49.7%", status="report", note=REP_KN),
    C("supplement: in the proportion reported for each arm", "schmid2024", f"file:{MS}", "2024 年 Table 1 的例数除以该臂非 pCR 人数"),
    C("supplement: in the proportions of the 2024 report", "schmid2024", f"file:{MS}", "EFS 的超额风险按各臂首发事件构成（2024 年 Table 1）分配"),
    C("supplement: to distant recurrence at a constant rate", "schmid2022", f"file:{MS}", "2022 年 Table 1 脚注的局部复发后远处复发例数"),
    C("supplement: in the numbers reported for each arm", "schmid2022", f"file:{MS}", "各臂的人数取 2022 年补充材料 Table S5"),
    C("supplement: Strategy and Medical Economics (ESME) cohort", "grinda2023", f"file:{MS}", "ESME（Grinda 等 Eur J Cancer 2023，Fig. 3a"),
    C("supplement: abridged life table for Japanese women", "lifetable2025", "check", "令和7年簡易生命表の概況"),
    C("supplement: confidence intervals of the final analysis", "kn522final2026", "crossref",
      "The 7-yr EFS rate (95% CI) was 78.3% (75.3-81.1) in the pembro group vs 69.8% (65.0-74.2) in the pbo group"),
    C("supplement: the published curves of the 2024 report", "guyot2012", "abstract", "We develop an algorithm that maps from digitised curves back to KM data"),
    C("supplement: the published curves of the 2024 report", "schmid2024", f"file:{P1R}", "2 条 OS（2024 年 Fig. 1A，按臂）从随机化起"),
    C("supplement: 7-year estimates of the final analysis", "kn522final2026", "crossref",
      "The 7-yr OS rate (95% CI) was 85.1% (82.5-87.5) in the pembro group vs 77.2% (72.7-81.1) in the pbo group"),
    C("supplement: curves (overall survival, 2024 report)", "guyot2012", "abstract", "We develop an algorithm that maps from digitised curves back to KM data"),
    C("supplement: curves (overall survival, 2024 report)", "schmid2024", f"file:{P1R}", "2 条 OS（2024 年 Fig. 1A，按臂）从随机化起"),
    C("supplement: ; final analysis", "kn522final2026", "crossref", "At the data cutoff date (October 14, 2025)"),
    C("supplement: (cases diagnosed in 2024, final version)", "jbcs55", f"file:{JB}", "日本乳癌学会 全国乳がん患者登録調査報告 第55号（2024年次症例、確定版）",
      status="provided", note=PROV),
]

# Source cells of Supplementary Table S2, Panel A (survival inputs): label -> (keys, project file, passage recording the location)
PANEL_A = {
    "KEYNOTE-522 (interim analysis 4)": (["schmid2022"], MS, "2022 年补充材料 Fig. S4（IA4）的 494/784 与 217/390"),
    "KEYNOTE-522 final analysis": (["kn522final2026"], KN7, "efs_pcr_pembro,90.4"),
    "Fitted to reconstructed KEYNOTE-522 data (interim analysis 4)": (["guyot2012", "schmid2022"], P1R, "| K22_S4_EFS_by_pCR | Schmid 2022 NEJM 386:556 appendix | Fig. S4 |"),
    "KEYNOTE-522 (2024 report)": (["schmid2024"], MS, "2024 年 Table 1"),
    "KEYNOTE-522 (2022 report)": (["schmid2022"], MS, "2022 年 Table 1 脚注的局部复发后远处复发例数"),
    "ESME cohort, reconstructed overall survival": (["grinda2023", "guyot2012"], MS, "ESME（Grinda 等 Eur J Cancer 2023，Fig. 3a"),
    "ESME cohort": (["grinda2023"], MS, "ESME（Grinda 等 Eur J Cancer 2023，Fig. 3a"),
    "Abridged life table (2025)": (["lifetable2025"], MS, "令和7年简易生命表"),
    "Italian real-world cohort after neoadjuvant pembrolizumab": (["fedele2026"], MS, "Fedele"),
    "Single-center cohort with locoregional progression during neoadjuvant therapy": (["elmore2021"], MS, "Elmore"),
}


def norm(t):
    return re.sub(r"\s+", " ", t).strip()


def _source_text(c, fulltext_dir, cache):
    from references import ABSTRACT, GREY, PUBMED  # noqa: PLC0415
    s = c["src"]
    if s == "abstract":
        return PUBMED[c["key"]]["abstract"], "PubMed abstract"
    if s == "crossref":
        return cache["crossref_abstract"][c["key"]], "Crossref abstract"
    if s == "affil":
        return " | ".join(cache["affiliations"][c["key"]]), "PubMed affiliations"
    if s == "check":
        return (GREY.get(c["key"]) or ABSTRACT.get(c["key"]))["check"], "check in references.py"
    if s.startswith("pmc:"):
        pmc = s[4:]
        info = next(v for v in cache["pmc"].values() if v["pmcid"] == pmc)
        p = Path(fulltext_dir or "") / f"{pmc}.xml"
        if not fulltext_dir or not p.exists():
            return None, f"{pmc} full text not available in this run"
        b = p.read_bytes()
        if hashlib.sha256(b).hexdigest() != info["sha256"]:
            return None, f"{pmc} full text differs from the recorded sha256"
        return re.sub(r"<[^>]+>", " ", b.decode("utf-8")), f"Europe PMC full text {pmc} (sha256 {info['sha256'][:8]})"
    if s.startswith("file:"):
        return (ROOT / s[5:]).read_text(encoding="utf-8"), s[5:]
    if s.startswith("xlsx:"):
        import openpyxl  # noqa: PLC0415
        wb = openpyxl.load_workbook(ROOT / s[5:], read_only=True, data_only=True)
        rows = [" | ".join(str(x) for x in r if x is not None) for ws in wb.worksheets for r in ws.iter_rows(values_only=True)
                if r and all(q in " | ".join(str(x) for x in r if x is not None) for q in c["quotes"])]
        return "\n".join(rows), s[5:] + " (row with all passages)"
    raise ValueError(s)


def check(fulltext_dir=None):
    """Return the claims with found (True/False/None) and where the passage was looked for."""
    cache = json.load(open(HERE / "support_cache.json", encoding="utf-8"))
    out = []
    for c in CLAIMS:
        text, where = _source_text(c, fulltext_dir, cache)
        found = None if text is None else all(norm(q) in norm(text) for q in c["quotes"])
        out.append(dict(c, found=found, where=where))
    for label, (keys, path, needle) in PANEL_A.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        out.append(dict(loc=f"S2 Panel A source: {label}", key=",".join(keys), src=f"file:{path}", quotes=[needle], status="ok", note="",
                        found=norm(needle) in norm(text), where=path))
    return out
