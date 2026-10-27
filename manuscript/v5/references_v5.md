# 参考文献与检索记录（v5）

由 manuscript/code/make_references_doc.py 生成（2026-10-27）。本文件只读取已保存的检索结果与核对记录（manuscript/code/refs/），不重新检索。文献号是 number_refs.py 按阅读顺序（本文 → 表 → 图注 → 补充材料）编的号。

## 1. 检索

- 数据库：PubMed（NCBI E-utilities，esearch/esummary）与 Europe PMC（REST API，限题名与摘要：TITLE/ABSTRACT 字段）。
- Scopus：本环境没有 Scopus API 的配置（pybliometrics 未设置），未检索。
- 检索日：全部 12 组都在 2026-10-26 运行；年份范围见各式（新颖性的 3 组与经济评价、试验的各组为 2000–2026）。
- 脚本：manuscript/code/refs/lit_search.py；结果：manuscript/code/refs/searches/search_<key>.json（命中的 ID、题名、年、刊名、DOI）。
- 形式：Introduction 的背景检索，不是系统综述（不宣称覆盖全部文献）。新颖性句与经济评价句所依据的 4 组检索，每条命中都读了题名和摘要并记录判定（第 2 节）；其余各组按段落要陈述的内容读题名，引用的文献列在表中。

| key | 用途 | 检索日 | PubMed 命中 | Europe PMC 命中 | 其中被引用（文献号） |
|---|---|---|---|---|---|
| tnbc_recurrence | Introduction 第 1 段：TNBC 的复发模式 | 2026-10-26 | 88 | 111 | 1, 6, 50, 57 |
| challenge | Introduction 第 2 段：CHALLENGE 试验 | 2026-10-26 | 3 | 6 | 9, 46 |
| chemo_rct_survival | Introduction 第 2 段：乳腺癌化疗期间运动的随机试验与复发、生存 | 2026-10-26 | 67 | 66 | 10, 14, 19 |
| nac_pcr | Introduction 第 2 段：新辅助化疗期间运动与 pCR 的试验 | 2026-10-26 | 21 | 19 | 15, 16, 17, 18, 19 |
| econ_reviews | Introduction 第 3 段：癌症运动经济评价的系统综述 | 2026-10-26 | 27 | 17 | 20, 21, 22 |
| headroom | Introduction 第 3 段：最大可负担成本（headroom）方法 | 2026-10-26 | 44 | 40 | 26 |
| pembro_cea | Introduction 第 3 段：KEYNOTE-522 方案的成本效果分析 | 2026-10-26 | 16 | 9 | 27, 28, 29, 30 |
| pembro_tnbc_any | 同上，放宽到 TNBC 的所有场景 | 2026-10-26 | 22 | 15 | 27, 28, 29, 30, 31 |
| pembro_japan | Introduction 第 3 段：日本的帕博利珠单抗成本效果分析 | 2026-10-26 | 10 | 11 | 31, 32, 33, 34, 35, 36, 37, 66 |
| novelty | 新颖性句（Introduction 第 4 段）：乳腺癌新辅助治疗期间运动的经济评价 | 2026-10-26 | 2 | 0 | — |
| novelty_variants | 新颖性句：拼写变体（neo-adjuvant、(neo)adjuvant、during treatment），不限癌种 | 2026-10-26 | 11 | 10 | 39 |
| novelty_chemo | 新颖性句：放宽到乳腺癌化疗期间（含辅助） | 2026-10-26 | 10 | 9 | 23, 24, 25 |

检索式（原样）：

**tnbc_recurrence**

- PubMed：`("triple-negative"[ti] OR "triple negative"[ti]) AND breast[ti] AND (recurrence[ti] OR relapse[ti] OR "distant recurrence"[ti] OR survival[ti]) AND ("pattern"[ti] OR "outcome"[ti] OR "outcomes"[ti] OR clinical[ti]) AND ("2005/01/01"[dp] : "2026/12/31"[dp])`
- Europe PMC：`TITLE:("triple-negative" AND breast AND (recurrence OR relapse) AND ((TITLE:pattern OR ABSTRACT:pattern) OR (TITLE:outcome OR ABSTRACT:outcome) OR (TITLE:outcomes OR ABSTRACT:outcomes) OR (TITLE:clinical OR ABSTRACT:clinical))) AND PUB_YEAR:[2005 TO 2026]`

**challenge**

- PubMed：`("structured exercise"[tiab] OR exercise[tiab]) AND ("colon cancer"[tiab] OR "Colonic Neoplasms"[mh]) AND (CHALLENGE[tiab] OR "disease-free survival"[tiab]) AND randomized controlled trial[pt] AND ("2020/01/01"[dp] : "2026/12/31"[dp])`
- Europe PMC：`((TITLE:"structured exercise" OR ABSTRACT:"structured exercise") OR (TITLE:exercise OR ABSTRACT:exercise)) AND (TITLE:"colon cancer" OR ABSTRACT:"colon cancer") AND ((TITLE:CHALLENGE OR ABSTRACT:CHALLENGE) OR (TITLE:"disease-free survival" OR ABSTRACT:"disease-free survival")) AND (TITLE:randomized OR ABSTRACT:randomized) AND PUB_YEAR:[2020 TO 2026]`

**chemo_rct_survival**

- PubMed：`(exercise[tiab] OR "physical activity"[tiab] OR "Exercise"[mh] OR "Exercise Therapy"[mh] OR prehabilitation[tiab] OR "aerobic training"[tiab] OR "resistance training"[tiab]) AND ("Breast Neoplasms"[mh] OR "breast cancer"[tiab] OR "breast carcinoma"[tiab]) AND chemotherapy[tiab] AND (randomized controlled trial[pt] OR randomi*[tiab]) AND ("disease-free"[tiab] OR recurrence[tiab] OR "invasive disease-free"[tiab] OR survival[tiab]) AND ("2000/01/01"[dp] : "2026/12/31"[dp])`
- Europe PMC：`((TITLE:exercise OR ABSTRACT:exercise) OR (TITLE:"physical activity" OR ABSTRACT:"physical activity") OR (TITLE:prehabilitation OR ABSTRACT:prehabilitation) OR (TITLE:"aerobic training" OR ABSTRACT:"aerobic training") OR (TITLE:"resistance training" OR ABSTRACT:"resistance training")) AND ((TITLE:"breast cancer" OR ABSTRACT:"breast cancer") OR (TITLE:"breast neoplasms" OR ABSTRACT:"breast neoplasms") OR (TITLE:"breast carcinoma" OR ABSTRACT:"breast carcinoma")) AND (TITLE:chemotherapy OR ABSTRACT:chemotherapy) AND ((TITLE:randomized OR ABSTRACT:randomized) OR (TITLE:randomised OR ABSTRACT:randomised)) AND ((TITLE:"disease-free" OR ABSTRACT:"disease-free") OR (TITLE:recurrence OR ABSTRACT:recurrence) OR (TITLE:survival OR ABSTRACT:survival)) AND PUB_YEAR:[2000 TO 2026]`

**nac_pcr**

- PubMed：`(exercise[tiab] OR "physical activity"[tiab] OR "Exercise"[mh] OR "Exercise Therapy"[mh] OR prehabilitation[tiab] OR "aerobic training"[tiab] OR "resistance training"[tiab]) AND (neoadjuvant[tiab] OR preoperative[tiab] OR "Neoadjuvant Therapy"[mh]) AND ("Breast Neoplasms"[mh] OR "breast cancer"[tiab] OR "breast carcinoma"[tiab]) AND ("pathologic complete response"[tiab] OR "pathological complete response"[tiab] OR pCR[tiab] OR "tumor response"[tiab] OR "tumour response"[tiab]) AND ("2000/01/01"[dp] : "2026/12/31"[dp])`
- Europe PMC：`((TITLE:exercise OR ABSTRACT:exercise) OR (TITLE:"physical activity" OR ABSTRACT:"physical activity") OR (TITLE:prehabilitation OR ABSTRACT:prehabilitation) OR (TITLE:"aerobic training" OR ABSTRACT:"aerobic training") OR (TITLE:"resistance training" OR ABSTRACT:"resistance training")) AND ((TITLE:neoadjuvant OR ABSTRACT:neoadjuvant) OR (TITLE:preoperative OR ABSTRACT:preoperative)) AND ((TITLE:"breast cancer" OR ABSTRACT:"breast cancer") OR (TITLE:"breast neoplasms" OR ABSTRACT:"breast neoplasms") OR (TITLE:"breast carcinoma" OR ABSTRACT:"breast carcinoma")) AND ((TITLE:"pathologic complete response" OR ABSTRACT:"pathologic complete response") OR (TITLE:"pathological complete response" OR ABSTRACT:"pathological complete response") OR (TITLE:pCR OR ABSTRACT:pCR) OR (TITLE:"tumor response" OR ABSTRACT:"tumor response")) AND PUB_YEAR:[2000 TO 2026]`

**econ_reviews**

- PubMed：`(exercise[tiab] OR "physical activity"[tiab] OR "Exercise"[mh] OR "Exercise Therapy"[mh] OR prehabilitation[tiab] OR "aerobic training"[tiab] OR "resistance training"[tiab]) AND ("Neoplasms"[mh] OR cancer[tiab]) AND ("cost-effectiveness"[tiab] OR "cost effectiveness"[tiab] OR "cost-utility"[tiab] OR "cost utility"[tiab] OR "economic evaluation"[tiab] OR QALY*[tiab] OR "Cost-Benefit Analysis"[mh]) AND (systematic[sb] OR "systematic review"[tiab]) AND ("2000/01/01"[dp] : "2026/12/31"[dp])`
- Europe PMC：`((TITLE:exercise OR ABSTRACT:exercise) OR (TITLE:"physical activity" OR ABSTRACT:"physical activity") OR (TITLE:prehabilitation OR ABSTRACT:prehabilitation) OR (TITLE:"aerobic training" OR ABSTRACT:"aerobic training") OR (TITLE:"resistance training" OR ABSTRACT:"resistance training")) AND (TITLE:cancer OR ABSTRACT:cancer) AND ((TITLE:"cost-effectiveness" OR ABSTRACT:"cost-effectiveness") OR (TITLE:"cost effectiveness" OR ABSTRACT:"cost effectiveness") OR (TITLE:"cost-utility" OR ABSTRACT:"cost-utility") OR (TITLE:"cost utility" OR ABSTRACT:"cost utility") OR (TITLE:"economic evaluation" OR ABSTRACT:"economic evaluation") OR (TITLE:QALY OR ABSTRACT:QALY) OR (TITLE:"quality-adjusted life year" OR ABSTRACT:"quality-adjusted life year")) AND (TITLE:"systematic review" OR ABSTRACT:"systematic review") AND PUB_YEAR:[2000 TO 2026]`

**headroom**

- PubMed：`(headroom[tiab] AND ("cost-effectiveness"[tiab] OR "cost effectiveness"[tiab] OR "health technology"[tiab]))`
- Europe PMC：`(TITLE:headroom OR ABSTRACT:headroom) AND ((TITLE:"cost-effectiveness" OR ABSTRACT:"cost-effectiveness") OR (TITLE:"health technology" OR ABSTRACT:"health technology"))`

**pembro_cea**

- PubMed：`pembrolizumab[tiab] AND ("triple-negative"[tiab] OR "triple negative"[tiab] OR "Triple Negative Breast Neoplasms"[mh]) AND (early[tiab] OR neoadjuvant[tiab] OR KEYNOTE-522[tiab]) AND ("cost-effectiveness"[tiab] OR "cost effectiveness"[tiab] OR "cost-utility"[tiab] OR "cost utility"[tiab] OR "economic evaluation"[tiab] OR QALY*[tiab] OR "Cost-Benefit Analysis"[mh])`
- Europe PMC：`(TITLE:pembrolizumab OR ABSTRACT:pembrolizumab) AND ((TITLE:"triple-negative" OR ABSTRACT:"triple-negative") OR (TITLE:"triple negative" OR ABSTRACT:"triple negative")) AND ((TITLE:early OR ABSTRACT:early) OR (TITLE:neoadjuvant OR ABSTRACT:neoadjuvant) OR (TITLE:"KEYNOTE-522" OR ABSTRACT:"KEYNOTE-522")) AND ((TITLE:"cost-effectiveness" OR ABSTRACT:"cost-effectiveness") OR (TITLE:"cost effectiveness" OR ABSTRACT:"cost effectiveness") OR (TITLE:"cost-utility" OR ABSTRACT:"cost-utility") OR (TITLE:"cost utility" OR ABSTRACT:"cost utility") OR (TITLE:"economic evaluation" OR ABSTRACT:"economic evaluation") OR (TITLE:QALY OR ABSTRACT:QALY) OR (TITLE:"quality-adjusted life year" OR ABSTRACT:"quality-adjusted life year"))`

**pembro_tnbc_any**

- PubMed：`pembrolizumab[tiab] AND ("triple-negative"[tiab] OR "triple negative"[tiab] OR TNBC[tiab]) AND ("cost-effectiveness"[tiab] OR "cost effectiveness"[tiab] OR "cost-utility"[tiab] OR "cost utility"[tiab] OR "economic evaluation"[tiab] OR QALY*[tiab] OR "Cost-Benefit Analysis"[mh])`
- Europe PMC：`(TITLE:pembrolizumab OR ABSTRACT:pembrolizumab) AND ((TITLE:"triple-negative" OR ABSTRACT:"triple-negative") OR (TITLE:"triple negative" OR ABSTRACT:"triple negative") OR (TITLE:TNBC OR ABSTRACT:TNBC)) AND ((TITLE:"cost-effectiveness" OR ABSTRACT:"cost-effectiveness") OR (TITLE:"cost effectiveness" OR ABSTRACT:"cost effectiveness") OR (TITLE:"cost-utility" OR ABSTRACT:"cost-utility") OR (TITLE:"cost utility" OR ABSTRACT:"cost utility") OR (TITLE:"economic evaluation" OR ABSTRACT:"economic evaluation") OR (TITLE:QALY OR ABSTRACT:QALY) OR (TITLE:"quality-adjusted life year" OR ABSTRACT:"quality-adjusted life year"))`

**pembro_japan**

- PubMed：`pembrolizumab[tiab] AND (Japan[tiab] OR Japanese[tiab] OR "Japan"[mh]) AND ("cost-effectiveness"[tiab] OR "cost effectiveness"[tiab] OR "cost-utility"[tiab] OR "cost utility"[tiab] OR "economic evaluation"[tiab] OR QALY*[tiab] OR "Cost-Benefit Analysis"[mh])`
- Europe PMC：`(TITLE:pembrolizumab OR ABSTRACT:pembrolizumab) AND ((TITLE:Japan OR ABSTRACT:Japan) OR (TITLE:Japanese OR ABSTRACT:Japanese)) AND ((TITLE:"cost-effectiveness" OR ABSTRACT:"cost-effectiveness") OR (TITLE:"cost effectiveness" OR ABSTRACT:"cost effectiveness") OR (TITLE:"cost-utility" OR ABSTRACT:"cost-utility") OR (TITLE:"cost utility" OR ABSTRACT:"cost utility") OR (TITLE:"economic evaluation" OR ABSTRACT:"economic evaluation") OR (TITLE:QALY OR ABSTRACT:QALY) OR (TITLE:"quality-adjusted life year" OR ABSTRACT:"quality-adjusted life year"))`

**novelty**

- PubMed：`(exercise[tiab] OR "physical activity"[tiab] OR "Exercise"[mh] OR "Exercise Therapy"[mh] OR prehabilitation[tiab] OR "aerobic training"[tiab] OR "resistance training"[tiab]) AND (neoadjuvant[tiab] OR preoperative[tiab] OR "Neoadjuvant Therapy"[mh]) AND ("Breast Neoplasms"[mh] OR "breast cancer"[tiab] OR "breast carcinoma"[tiab]) AND ("cost-effectiveness"[tiab] OR "cost effectiveness"[tiab] OR "cost-utility"[tiab] OR "cost utility"[tiab] OR "economic evaluation"[tiab] OR QALY*[tiab] OR "Cost-Benefit Analysis"[mh]) AND ("2000/01/01"[dp] : "2026/12/31"[dp])`
- Europe PMC：`((TITLE:exercise OR ABSTRACT:exercise) OR (TITLE:"physical activity" OR ABSTRACT:"physical activity") OR (TITLE:prehabilitation OR ABSTRACT:prehabilitation) OR (TITLE:"aerobic training" OR ABSTRACT:"aerobic training") OR (TITLE:"resistance training" OR ABSTRACT:"resistance training")) AND ((TITLE:neoadjuvant OR ABSTRACT:neoadjuvant) OR (TITLE:preoperative OR ABSTRACT:preoperative)) AND ((TITLE:"breast cancer" OR ABSTRACT:"breast cancer") OR (TITLE:"breast neoplasms" OR ABSTRACT:"breast neoplasms") OR (TITLE:"breast carcinoma" OR ABSTRACT:"breast carcinoma")) AND ((TITLE:"cost-effectiveness" OR ABSTRACT:"cost-effectiveness") OR (TITLE:"cost effectiveness" OR ABSTRACT:"cost effectiveness") OR (TITLE:"cost-utility" OR ABSTRACT:"cost-utility") OR (TITLE:"cost utility" OR ABSTRACT:"cost utility") OR (TITLE:"economic evaluation" OR ABSTRACT:"economic evaluation") OR (TITLE:QALY OR ABSTRACT:QALY) OR (TITLE:"quality-adjusted life year" OR ABSTRACT:"quality-adjusted life year")) AND PUB_YEAR:[2000 TO 2026]`

**novelty_variants**

- PubMed：`(exercise[tiab] OR "physical activity"[tiab] OR "Exercise"[mh] OR "Exercise Therapy"[mh] OR prehabilitation[tiab] OR "aerobic training"[tiab] OR "resistance training"[tiab]) AND (cancer[tiab] OR "Neoplasms"[mh]) AND ("neo adjuvant"[tiab] OR neo-adjuvant[tiab] OR "(neo)adjuvant"[tiab] OR neoadjuvant[tiab] OR "during treatment"[tiab] OR "during oncological treatment"[tiab]) AND ("cost-effectiveness"[tiab] OR "cost effectiveness"[tiab] OR "cost-utility"[tiab] OR "cost utility"[tiab] OR "economic evaluation"[tiab] OR QALY*[tiab] OR "Cost-Benefit Analysis"[mh]) AND ("2000/01/01"[dp] : "2026/12/31"[dp])`
- Europe PMC：`((TITLE:exercise OR ABSTRACT:exercise) OR (TITLE:"physical activity" OR ABSTRACT:"physical activity") OR (TITLE:prehabilitation OR ABSTRACT:prehabilitation) OR (TITLE:"aerobic training" OR ABSTRACT:"aerobic training") OR (TITLE:"resistance training" OR ABSTRACT:"resistance training")) AND (TITLE:cancer OR ABSTRACT:cancer) AND ((TITLE:"neo-adjuvant" OR ABSTRACT:"neo-adjuvant") OR (TITLE:"(neo)adjuvant" OR ABSTRACT:"(neo)adjuvant") OR (TITLE:neoadjuvant OR ABSTRACT:neoadjuvant) OR (TITLE:"during treatment" OR ABSTRACT:"during treatment") OR (TITLE:"during oncological treatment" OR ABSTRACT:"during oncological treatment")) AND ((TITLE:"cost-effectiveness" OR ABSTRACT:"cost-effectiveness") OR (TITLE:"cost effectiveness" OR ABSTRACT:"cost effectiveness") OR (TITLE:"cost-utility" OR ABSTRACT:"cost-utility") OR (TITLE:"cost utility" OR ABSTRACT:"cost utility") OR (TITLE:"economic evaluation" OR ABSTRACT:"economic evaluation") OR (TITLE:QALY OR ABSTRACT:QALY) OR (TITLE:"quality-adjusted life year" OR ABSTRACT:"quality-adjusted life year")) AND PUB_YEAR:[2000 TO 2026]`

**novelty_chemo**

- PubMed：`(exercise[tiab] OR "physical activity"[tiab] OR "Exercise"[mh] OR "Exercise Therapy"[mh] OR prehabilitation[tiab] OR "aerobic training"[tiab] OR "resistance training"[tiab]) AND ("Breast Neoplasms"[mh] OR "breast cancer"[tiab] OR "breast carcinoma"[tiab]) AND (chemotherapy[tiab] OR "Antineoplastic Agents"[mh]) AND ("cost-effectiveness"[tiab] OR "cost effectiveness"[tiab] OR "cost-utility"[tiab] OR "cost utility"[tiab] OR "economic evaluation"[tiab] OR QALY*[tiab] OR "Cost-Benefit Analysis"[mh]) AND ("2000/01/01"[dp] : "2026/12/31"[dp])`
- Europe PMC：`((TITLE:exercise OR ABSTRACT:exercise) OR (TITLE:"physical activity" OR ABSTRACT:"physical activity") OR (TITLE:prehabilitation OR ABSTRACT:prehabilitation) OR (TITLE:"aerobic training" OR ABSTRACT:"aerobic training") OR (TITLE:"resistance training" OR ABSTRACT:"resistance training")) AND ((TITLE:"breast cancer" OR ABSTRACT:"breast cancer") OR (TITLE:"breast neoplasms" OR ABSTRACT:"breast neoplasms") OR (TITLE:"breast carcinoma" OR ABSTRACT:"breast carcinoma")) AND (TITLE:chemotherapy OR ABSTRACT:chemotherapy) AND ((TITLE:"cost-effectiveness" OR ABSTRACT:"cost-effectiveness") OR (TITLE:"cost effectiveness" OR ABSTRACT:"cost effectiveness") OR (TITLE:"cost-utility" OR ABSTRACT:"cost-utility") OR (TITLE:"cost utility" OR ABSTRACT:"cost utility") OR (TITLE:"economic evaluation" OR ABSTRACT:"economic evaluation") OR (TITLE:QALY OR ABSTRACT:QALY) OR (TITLE:"quality-adjusted life year" OR ABSTRACT:"quality-adjusted life year")) AND PUB_YEAR:[2000 TO 2026]`

## 2. 新颖性句与经济评价句的筛选

判定代码：C = 引用；U = 读过、未引用（理由见第 5 节）；P = 试验方案或设计论文，尚无结果；D = 其他疾病或癌种；S = 乳腺癌但不在新辅助期间（辅助、术后或转移）；E = 没有经济评价（成本效果只作为今后的课题提到）；X = 主题不符；R = 综述，范围不符或已被引用的三篇综述覆盖。两个库的同一条记录只列一次。

### novelty（PubMed 2，Europe PMC 0）

| ID | 年 | 第一作者 | 题名 | 判定 | 说明 |
|---|---|---|---|---|---|
| 41926867 | 2026 | Latif A | Feedback from wearable devices accelerates recovery after breast cancer surgery. | S,E | wearable-driven feedback after axillary surgery; observational cohort; cost-effectiveness named as future work |
| 27299796 | 2016 | VandenBussche CJ | Reflex Estrogen Receptor (ER) and Progesterone Receptor (PR) Analysis of Ductal Carcinoma In Situ (DCIS) in Breast Needle Core Biopsy Specimens: An Unnecessary Exercise That Costs the United States $35 Million/y. | X | costs of reflex ER/PR testing of DCIS; 'exercise' used figuratively |

### novelty_variants（PubMed 11，Europe PMC 10）

| ID | 年 | 第一作者 | 题名 | 判定 | 说明 |
|---|---|---|---|---|---|
| 40755583 | 2025 | Baladaniya M | Exploring the Impact of Physical Therapy on Patient Outcomes Across the Cancer Care Continuum: A Narrative Review. | R,E | narrative review of physical therapy across the cancer care continuum |
| 40681723 | 2025 | Smith-Turchyn J | Implementing exercise and self-management for women with breast cancer during treatment: results of the NEXT-BRCA randomized controlled trial. | E | NEXT-BRCA: exercise and self-management during treatment; cost-effectiveness named as future work |
| 39163116 | 2024 | Selles WL | Effectiveness of Aerobic Training for Adverse Symptoms Related to Chemotherapy During Treatment: Protocol for a Randomized Controlled Trial With Cost-Effectiveness Assessment. | P | protocol of a randomized trial of aerobic training during chemotherapy with a planned cost-effectiveness analysis |
| 37074759 | 2023 | Ax AK | Cost-effectiveness of different exercise intensities during oncological treatment in the Phys-Can RCT. | C | Phys-Can: cost-effectiveness of two exercise intensities during (neo)adjuvant treatment of breast, colorectal or prostate cancer; the nearest study named in Introduction paragraph 4; cited as [39] (ax2023) |
| 35906659 | 2022 | Hiensch AE | Design of a multinational randomized controlled trial to assess the effects of structured and individualized exercise in patients with metastatic breast cancer on fatigue and quality of life: the EFFECT study. | P,S | design of a trial of exercise in metastatic breast cancer |
| 35607981 | 2022 | Ax AK | Long-term resource utilisation and associated costs of exercise during (neo)adjuvant oncological treatment: the Phys-Can project. | U | Phys-Can: long-term resource use and costs |
| 34518245 | 2021 | Touillaud M | Connected device and therapeutic patient education to promote physical activity among women with localised breast cancer (DISCO trial): protocol for a multicentre 2×2 factorial randomised controlled trial. | P,S | protocol: connected device and education for localised breast cancer (adjuvant); planned cost-effectiveness analysis |
| 32404096 | 2020 | O'Neill L | Rehabilitation strategies following oesophagogastric and Hepatopancreaticobiliary cancer (ReStOre II): a protocol for a randomized controlled trial. | P,D | protocol: rehabilitation after oesophagogastric and hepatopancreaticobiliary cancer surgery |
| 28875575 | 2017 | Thomson ZO | Can weight gain be prevented in women receiving treatment for breast cancer? A systematic review of intervention studies. | R,E | systematic review of interventions to prevent weight gain during breast cancer treatment |
| 27299796 | 2016 | VandenBussche CJ | Reflex Estrogen Receptor (ER) and Progesterone Receptor (PR) Analysis of Ductal Carcinoma In Situ (DCIS) in Breast Needle Core Biopsy Specimens: An Unnecessary Exercise That Costs the United States $35 Million/y. | X | costs of reflex ER/PR testing of DCIS; 'exercise' used figuratively |
| 27156145 | 2016 | Heldens AF | Feasibility and preliminary effectiveness of a physical exercise training program during neoadjuvant chemoradiotherapy in individual patients with rectal cancer prior to major elective surgery. | D,E | feasibility of exercise during neoadjuvant chemoradiotherapy for rectal cancer |
| PPR1238970 | 2026 | Snooks R | Clinical and Economic Impact of a Multimodal Prehabilitation Pathway for Advanced Ovarian Cancer at a UK Specialist Centre: A Three-Tier Evaluation of Complications, Costs and Modelled QALY Outcomes. | D | preprint (not peer reviewed): economic evaluation of multimodal prehabilitation during neoadjuvant chemotherapy for advanced ovarian cancer; outside the breast-cancer bound of the novelty sentence; candidate for the Discussion |

### novelty_chemo（PubMed 10，Europe PMC 9）

| ID | 年 | 第一作者 | 题名 | 判定 | 说明 |
|---|---|---|---|---|---|
| 39163116 | 2024 | Selles WL | Effectiveness of Aerobic Training for Adverse Symptoms Related to Chemotherapy During Treatment: Protocol for a Randomized Controlled Trial With Cost-Effectiveness Assessment. | P | protocol of a randomized trial of aerobic training during chemotherapy with a planned cost-effectiveness analysis |
| 37729837 | 2023 | Samadbeik M | Mobile health interventions for cancer patient education: A scoping review. | X,R | scoping review of mobile health education for patients with cancer |
| 34518245 | 2021 | Touillaud M | Connected device and therapeutic patient education to promote physical activity among women with localised breast cancer (DISCO trial): protocol for a multicentre 2×2 factorial randomised controlled trial. | P,S | protocol: connected device and education for localised breast cancer (adjuvant); planned cost-effectiveness analysis |
| 31729566 | 2020 | Perrier L | Cost-effectiveness of an exercise and nutritional intervention versus usual nutritional care during adjuvant treatment for localized breast cancer: the PASAPAS randomized controlled trial. | C | cited as [25] (perrier2020) |
| 29086085 | 2018 | van Waart H | Cost-utility and cost-effectiveness of physical exercise during adjuvant chemotherapy. | C | cited as [24] (vanwaart2018) |
| 28875575 | 2017 | Thomson ZO | Can weight gain be prevented in women receiving treatment for breast cancer? A systematic review of intervention studies. | R,E | systematic review of interventions to prevent weight gain during breast cancer treatment |
| 28264824 | 2017 | May AM | Cost-effectiveness analysis of an 18-week exercise programme for patients with breast and colon cancer undergoing adjuvant chemotherapy: the randomised PACT study. | C | cited as [23] (may2017) |
| 25523144 | 2015 | Garattini L | Cost-effectiveness of trastuzumab in metastatic breast cancer: mainly a matter of price in the EU? | X | trastuzumab in metastatic breast cancer |
| 24096188 | 2013 | Carayol M | Adapted physical activity and diet (APAD) during adjuvant breast cancer therapy: design and implementation of a prospective randomized controlled trial. | P,S | design of the APAD trial during adjuvant therapy; planned cost-utility analysis |
| 21138561 | 2010 | van Waart H | Design of the Physical exercise during Adjuvant Chemotherapy Effectiveness Study (PACES): a randomized controlled trial to evaluate effectiveness and cost-effectiveness of physical exercise in improving physical fitness and reducing fatigue. | P,S | design of the PACES trial during adjuvant chemotherapy (its cost-utility results are cited) |
| PPR201731 | 2020 | O'Connor D | PancREatic Cancer and Individualised Supervised Exercise (PRECISE): a feasibility trial protocol for patients with resectable pancreatic ductal adenocarcinoma | P,D | feasibility protocol of supervised exercise for resectable pancreatic cancer |

### econ_reviews（PubMed 27，Europe PMC 17）

| ID | 年 | 第一作者 | 题名 | 判定 | 说明 |
|---|---|---|---|---|---|
| 42799684 | 2026 | Skelly AC | Assessment and Treatment of Acute Low Back Pain (ALBP): A Systematic Review. | X | acute low back pain |
| 42366788 | 2026 | Leaviss J | Effectiveness of non-pharmacological interventions for fatigue in adults with long-term conditions: a synopsis of the EIFFEL mixed-methods evidence synthesis. | R | non-pharmacological interventions for fatigue in long-term conditions, not specific to cancer |
| 40685660 | 2025 | Davis S | Cost effectiveness of non-pharmacological interventions for fatigue in patients with long-term conditions: a systematic literature review. | R | cost-effectiveness of non-pharmacological interventions for fatigue in long-term conditions, not specific to cancer |
| 39776481 | 2024 | Kyriazakos S | Benchmarking the clinical outcomes of Healthentia SaMD in chronic disease management: a systematic literature review comparison. | X | software as a medical device in chronic disease |
| 39483606 | 2024 | Ansar M | A Systematic Review of Comparative Effectiveness of Interventions for Low Anterior Resection Syndrome: Impacts on Bowel Function and Quality of Life. | X | low anterior resection syndrome |
| 38801296 | 2024 | Khan S | A Systematic Review of Cost-Effectiveness Analyses Examining Treatments for Cachexia Syndrome. | X | treatments for cachexia |
| 38323587 | 2024 | Stiger RJ | The effectiveness of prehabilitation interventions on biopsychosocial and service outcomes pre and post upper gastrointestinal surgery: a systematic review. | R,D | prehabilitation for upper gastrointestinal cancer, effectiveness only |
| 37457987 | 2023 | Lazar DE | Web-based nutrition: a useful resource for cancer patients? | X | web-based nutrition |
| 36965520 | 2023 | Wang Y | Economic evaluation of exercise interventions for individuals with cancer: A systematic review. | C | cited as [22] (wang2023) |
| 36170564 | 2022 | Granger C | Preoperative exercise training for people with non-small cell lung cancer. | R,D | preoperative exercise for non-small cell lung cancer, effectiveness |
| 36163450 | 2023 | Gallagher A | The Cost-Effectiveness of Adjunctive Lifestyle Interventions for the Management of Cancer: A Systematic Review. | R | cost-effectiveness of adjunctive lifestyle interventions, diet included; exercise studies covered by the three cited reviews |
| 35703367 | 2022 | Kudchadkar SR | Non-pharmacological interventions for sleep promotion in hospitalized children. | X | sleep promotion in hospitalized children |
| 34694005 | 2021 | Virgara R | Interventions in outside-school hours childcare settings for promoting physical activity amongst schoolchildren aged 4 to 12 years. | X | physical activity in outside-school-hours childcare |
| 33624172 | 2021 | Gubler-Gut BE | Cost-effectiveness of physical activity interventions in cancer survivors of developed countries: a systematic review. | C | cited as [21] (gublergut2021) |
| 31221939 | 2019 | Klein PJ | Qigong and Tai Chi as Therapeutic Exercise: Survey of Systematic Reviews and Meta-Analyses Addressing Physical Health Conditions. | X | qigong and tai chi, overview of reviews |
| 30997624 | 2019 | Khan KA | Systematic review of economic evaluations of exercise and physiotherapy for patients treated for breast cancer. | C | cited as [20] (khan2019) |
| 29951414 | 2017 | Delgoshaei B | Telemedicine: A systematic review of economic evaluations. | X | telemedicine |
| 28900822 | 2018 | Treanor C | An international review and meta-analysis of prehabilitation compared to usual care for cancer patients. | R,E | meta-analysis of prehabilitation, effectiveness only |
| 28875575 | 2017 | Thomson ZO | Can weight gain be prevented in women receiving treatment for breast cancer? A systematic review of intervention studies. | R,E | systematic review of interventions to prevent weight gain during breast cancer treatment |
| 26810383 | 2016 | Dieng M | Economic evaluations of psychosocial interventions in cancer: a systematic review. | X | psychosocial interventions |
| 25757733 | 2015 | Goode AD | Telephone, print, and Web-based interventions for physical activity, diet, and weight control among cancer survivors: a systematic review. | R,E | remote physical activity, diet and weight interventions for cancer survivors, effectiveness |
| 24891269 | 2014 | Reeves MM | Weight loss intervention trials in women with breast cancer: a systematic review. | X | weight loss trials in breast cancer |
| 23074431 | 2012 | Sehatzadeh S | Influenza and pneumococcal vaccinations for patients with chronic obstructive pulmonary disease (COPD): an evidence-based review. | X | vaccination in chronic obstructive pulmonary disease |
| 19845974 | 2009 | Roine E | Cost-effectiveness of interventions based on physical exercise in the treatment of various diseases: a systematic literature review. | R | exercise interventions in various diseases, not specific to cancer |
| 19000846 | 2008 | Roux L | Cost effectiveness of community-based physical activity interventions. | X | community-based physical activity |
| 15929857 | 2005 | Stevenson M | A systematic review and economic evaluation of alendronate, etidronate, risedronate, raloxifene and teriparatide for the prevention and treatment of postmenopausal osteoporosis. | X | osteoporosis drugs |
| 10611196 | 2000 | Philips Z | Evaluation of the relative cost-effectiveness of treatments for infertility in the UK. | X | infertility treatments |
| PPR756874 | 2023 | Wale A | A rapid review exploring the effectiveness of artificial intelligence for cancer diagnosis | X | artificial intelligence for cancer diagnosis |

### 新颖性句的界限

- 位置：manuscript_v5.docx，I.4（Introduction 第 4 段）。原文：

  > No economic evaluation of exercise during neoadjuvant therapy for breast cancer was identified in searches of PubMed and Europe PMC covering 2000 to 2026, last run on 26 October 2026.
  > The nearest, Phys-Can, compared two exercise intensities during neoadjuvant or adjuvant treatment of breast, colorectal or prostate cancer[39].

- 界限：乳腺癌、新辅助治疗期间、运动、经济评价（成本效果、成本效用、QALY、Cost-Benefit Analysis[mh]）；PubMed 与 Europe PMC，2000–2026，最后运行 2026-10-26。novelty 组 2 条命中都不符合（S/E、X），放宽的 novelty_variants 与 novelty_chemo 也没有符合的记录。
- 最接近的研究：Phys-Can（ax2023）比较了两种运动强度，对象含新辅助或辅助治疗期间的乳腺癌，但不是与无运动比较，也未单独报告新辅助期间。
- 乳腺癌以外：Snooks 2026（Europe PMC 预印本 PPR1238970，未经同行评议）评价了晚期卵巢癌新辅助化疗期间多模式术前康复的成本与 QALY。它不在新颖性句的界限内（乳腺癌），本文未引用；Discussion 写到其他癌种时可作候选。
- 不用 “first” 一类的绝对说法（make_ledger 的 novelty_absolute_forms = 0）。

## 3. 文献表（Vancouver，NLM 格式）与 DOI 实测

DOI 实测：doi.org 的 HEAD 请求须返回 30x 跳转（期刊论文 refs/verify_doi.py → doi_check.json，并与 Crossref 记录比对第一作者、题名、卷、期、首页、年；会议摘要 refs/doi_head_abstracts.py → doi_head_abstracts.json）。撤稿筛查：refs/retraction_check.py（OpenAlex is_retracted 与 Crossref 的 update-to、relation）。

| 号 | key | 类型 | 首次引用 | DOI | doi.org | Crossref 比对 | 撤稿筛查 |
|---|---|---|---|---|---|---|---|
| 1 | dent2007 | journal | manuscript I.1 | 10.1158/1078-0432.CCR-06-3045 | 302 | 写法不同（issue: PubMed 15 Pt 1, Crossref 15） | OpenAlex 未撤稿 |
| 2 | liedtke2008 | journal | manuscript I.1 | 10.1200/JCO.2007.14.4147 | 302 | 一致 | OpenAlex 未撤稿 |
| 3 | schmid2020 | journal | manuscript I.1 | 10.1056/NEJMoa1910549 | 302 | 一致 | OpenAlex 未撤稿 |
| 4 | schmid2022 | journal | manuscript I.1 | 10.1056/NEJMoa2112651 | 302 | 一致 | OpenAlex 未撤稿 |
| 5 | schmid2024 | journal | manuscript I.1 | 10.1056/NEJMoa2409932 | 302 | 一致 | OpenAlex 未撤稿 |
| 6 | licata2025 | journal | manuscript I.1 | 10.1158/1078-0432.CCR-25-1478 | 302 | 一致 | OpenAlex 未撤稿 |
| 7 | jbcs55 | document/web | manuscript I.1 | — | — | — | — |
| 8 | price2026 | document/web | manuscript I.1 | — | — | — | — |
| 9 | courneya2025 | journal | manuscript I.2 | 10.1056/NEJMoa2502760 | 302 | 一致 | OpenAlex 未撤稿 |
| 10 | furmaniak2016 | journal | manuscript I.2 | 10.1002/14651858.CD005001.pub3 | 302 | 写法不同（Cochrane: PubMed volume 9 (issue) and article CD005001, Crossref volume 2016 and no page） | OpenAlex 未撤稿；Crossref new_version |
| 11 | courneya2007 | journal | manuscript I.2 | 10.1200/JCO.2006.08.2024 | 302 | 一致 | OpenAlex 未撤稿 |
| 12 | vanwaart2015 | journal | manuscript I.2 | 10.1200/JCO.2014.59.1081 | 302 | 写法不同（first author: family name with particle (van Waart)） | OpenAlex 未撤稿 |
| 13 | mijwel2018 | journal | manuscript I.2 | 10.1007/s10549-017-4571-3 | 302 | 一致 | OpenAlex 未撤稿 |
| 14 | courneya2014 | journal | manuscript I.2 | 10.1249/MSS.0000000000000297 | 302 | 一致 | OpenAlex 未撤稿 |
| 15 | sanft2023 | journal | manuscript I.2 | 10.1200/JCO.23.00871 | 302 | 一致 | OpenAlex 未撤稿 |
| 16 | kjeldsted2025 | journal | manuscript I.2 | 10.1158/1078-0432.CCR-25-0416 | 302 | 一致 | OpenAlex 未撤稿 |
| 17 | schmidt2025 | journal | manuscript I.2 | 10.1016/j.jshs.2025.101064 | 302 | 一致 | OpenAlex 未撤稿 |
| 18 | diasrato2026 | journal | manuscript I.2 | 10.1007/s00520-026-11156-1 | 302 | 写法不同（first author: two-word family name (Dias Rato); page: article number 948 (PubMed elocation, Crossref page)） | OpenAlex 未撤稿 |
| 19 | deboniface2022 | journal | manuscript I.2 | 10.1371/journal.pone.0274804 | 302 | 写法不同（first author: family name with particle (de Boniface)） | OpenAlex 未撤稿 |
| 20 | khan2019 | journal | manuscript I.3 | 10.1007/s10549-019-05235-7 | 302 | 一致 | OpenAlex 未撤稿 |
| 21 | gublergut2021 | journal | manuscript I.3 | 10.1007/s11764-021-01002-0 | 302 | 一致 | OpenAlex 未撤稿 |
| 22 | wang2023 | journal | manuscript I.3 | 10.1016/j.ypmed.2023.107491 | 302 | 一致 | OpenAlex 未撤稿 |
| 23 | may2017 | journal | manuscript I.3 | 10.1136/bmjopen-2016-012187 | 302 | 一致 | OpenAlex 未撤稿 |
| 24 | vanwaart2018 | journal | manuscript I.3 | 10.1007/s10198-017-0936-0 | 302 | 写法不同（first author: family name with particle (van Waart)） | OpenAlex 未撤稿 |
| 25 | perrier2020 | journal | manuscript I.3 | 10.1007/s00520-019-05078-4 | 302 | 一致 | OpenAlex 未撤稿 |
| 26 | boudewijns2023 | journal | manuscript I.3 | 10.1007/s40258-022-00774-5 | 302 | 一致 | OpenAlex 未撤稿 |
| 27 | huang2023 | journal | manuscript I.3 | 10.1007/s12325-022-02365-1 | 302 | 一致 | OpenAlex 未撤稿 |
| 28 | kwong2024 | journal | manuscript I.3 | 10.1007/s40487-024-00285-4 | 302 | 一致 | OpenAlex 未撤稿 |
| 29 | favrebulle2024 | journal | manuscript I.3 | 10.1007/s41669-023-00445-8 | 302 | 一致 | OpenAlex 未撤稿 |
| 30 | pollinger2025 | journal | manuscript I.3 | 10.1080/13696998.2024.2441073 | 302 | 一致 | OpenAlex 未撤稿 |
| 31 | chisaki2025 | journal | manuscript I.3 | 10.1007/s40261-025-01445-8 | 302 | 一致 | OpenAlex 未撤稿 |
| 32 | sugiura2023 | journal | manuscript I.3 | 10.1093/jjco/hyad050 | 302 | 一致 | OpenAlex 未撤稿 |
| 33 | taniguchi2026 | journal | manuscript I.3 | 10.1016/j.vhri.2025.101555 | 302 | 一致 | OpenAlex 未撤稿 |
| 34 | kakinuma2025 | journal | manuscript I.3 | 10.1007/s10388-025-01144-5 | 302 | 一致 | OpenAlex 未撤稿 |
| 35 | morimoto2026 | journal | manuscript I.3 | 10.1007/s41669-025-00634-7 | 302 | 一致 | OpenAlex 未撤稿 |
| 36 | tomura2025 | journal | manuscript I.3 | 10.1007/s11096-024-01826-7 | 302 | 一致 | OpenAlex 未撤稿 |
| 37 | kashiwa2024 | journal | manuscript I.3 | 10.1007/s12029-024-01106-7 | 302 | 一致 | OpenAlex 未撤稿 |
| 38 | c2h_list | document/web | manuscript I.3 | — | — | — | — |
| 39 | ax2023 | journal | manuscript I.4 | 10.1080/0284186X.2023.2200149 | 302 | 一致 | OpenAlex 未撤稿 |
| 40 | c2h_guideline | document/web | manuscript M.SB.2 | — | — | — | — |
| 41 | hasegawa2020 | journal | manuscript M.SB.2 | 10.1016/j.jval.2019.10.005 | 302 | 一致 | OpenAlex 未撤稿 |
| 42 | mhlw_ce2026 | document/web | manuscript M.SB.2 | — | — | — | — |
| 43 | esmo2023 | abstract | manuscript M.SB.3 | 10.1016/j.annonc.2023.10.008 | 302 | 条目取自 Crossref 记录 | OpenAlex 未撤稿 |
| 44 | kn522final2026 | abstract | manuscript M.SB.3 | 10.1200/JCO.2026.44.16_suppl.507 | 302 | 一致 | OpenAlex 未撤稿 |
| 45 | husereau2022 | journal | manuscript M.SB.3 | 10.1136/bmj-2021-067975 | 302 | 一致 | OpenAlex 未撤稿 |
| 46 | chan2026 | journal | manuscript M.VAR.3 | 10.1200/JCO-26-00765 | 302 | 一致 | OpenAlex 未撤稿 |
| 47 | worldbank_ppp | document/web | manuscript M.VAR.3 | — | — | — | — |
| 48 | fee2026 | document/web | manuscript M.VAR.3 | — | — | — | — |
| 49 | guyot2012 | journal | manuscript M.VAR.4 | 10.1186/1471-2288-12-9 | 302 | 写法不同（issue: none in PubMed, 1 in Crossref; the journal has no issues (article 9)） | OpenAlex 未撤稿 |
| 50 | grinda2023 | journal | manuscript M.VAR.4 | 10.1016/j.ejca.2023.05.023 | 302 | 一致 | OpenAlex 未撤稿 |
| 51 | lifetable2025 | document/web | manuscript M.VAR.4 | — | — | — | — |
| 52 | ema2022 | document/web | manuscript M.VAR.5 | — | — | — | — |
| 53 | ludwig2018 | journal | manuscript M.VAR.5 | 10.1007/s40273-018-0615-8 | 302 | 一致 | OpenAlex 未撤稿 |
| 54 | iwatani2021 | journal | manuscript M.VAR.5 | 10.3390/curroncol28050356 | 302 | 一致 | OpenAlex 未撤稿 |
| 55 | shiroiwa2017 | journal | manuscript M.VAR.5 | 10.1186/s12885-017-3774-7 | 302 | 一致 | OpenAlex 未撤稿 |
| 56 | pbac2023 | document/web | manuscript M.SA.6 | — | — | — | — |
| 57 | fedele2026 | journal | manuscript M.SA.6 | 10.1007/s10549-026-08023-2 | 302 | 写法不同（page: article number 8 (PubMed elocation, Crossref page)） | OpenAlex 未撤稿 |
| 58 | elmore2021 | journal | manuscript M.SA.6 | 10.1245/s10434-021-10444-w | 302 | 一致 | OpenAlex 未撤稿 |
| 59 | cortes2011 | journal | manuscript M.SA.6 | 10.1016/S0140-6736(11)60070-6 | 302 | 一致 | OpenAlex 未撤稿 |
| 60 | masuda2017 | journal | manuscript M.SA.6 | 10.1056/NEJMoa1612645 | 302 | 一致 | OpenAlex 未撤稿 |
| 61 | tutt2021 | journal | manuscript M.SA.6 | 10.1056/NEJMoa2105215 | 302 | 写法不同（title: Crossref with italic tags around BRCA1 and BRCA2） | OpenAlex 未撤稿 |
| 62 | garber2026 | journal | manuscript M.SA.6 | 10.1016/j.annonc.2026.08.002 | 302 | 一致 | OpenAlex 未撤稿 |
| 63 | tropion2025 | document/web | tables（…en mix; trials; national drug price list） | — | — | — | — |
| 64 | cortes2020 | journal | tables（…en mix; trials; national drug price list） | 10.1016/S0140-6736(20)32531-9 | 302 | 一致 | OpenAlex 未撤稿 |
| 65 | miller2007 | journal | tables（…en mix; trials; national drug price list） | 10.1056/NEJMoa072113 | 302 | 一致 | OpenAlex 未撤稿 |
| 66 | nusawat2026 | journal | tables（…Published Japanese estimates） | 10.1007/s10198-026-01912-9 | 302 | 一致 | OpenAlex 未撤稿 |
| 67 | ohtera2018 | abstract | tables（…Published Japanese estimates） | 10.1016/j.jval.2018.07.458 | 302 | 条目取自 Crossref 记录 | OpenAlex 未撤稿 |
| 68 | boc_fx | document/web | tables（…LENGE program cost; medical fee schedule） | — | — | — | — |
| 69 | jsco2023 | document/web | supplement（…al drug price list; antiemetic guideline） | — | — | — | — |
| 70 | hosp_kasugai | document/web | supplement（…code K476; KEYNOTE-522 surgical outcomes） | — | — | — | — |
| 71 | hosp_chuden | document/web | supplement（…code K476; KEYNOTE-522 surgical outcomes） | — | — | — | — |
| 72 | kuemmel2026 | journal | supplement（…code K476; KEYNOTE-522 surgical outcomes） | 10.1245/s10434-026-19121-2 | 302 | 一致 | OpenAlex 未撤稿 |
| 73 | yoshinami2025 | journal | supplement（…ished Japanese estimate, used as a proxy） | 10.1007/s12282-025-01714-6 | 302 | 一致 | OpenAlex 未撤稿 |
| 74 | andrade2026 | journal | supplement（… real-world and expert-consensus studies） | 10.1007/s10549-026-07938-0 | 302 | 写法不同（page: article number 27 (PubMed elocation, Crossref page)） | OpenAlex 未撤稿 |
| 75 | valachis2026 | journal | supplement（… real-world and expert-consensus studies） | 10.1038/s41416-026-03452-8 | 302 | 一致 | OpenAlex 未撤稿 |
| 76 | fujisawa2021 | journal | supplement（…Japanese single-institution study） | 10.3892/mco.2021.2258 | 302 | 写法不同（title: Crossref with italic tags and a non-breaking hyphen） | OpenAlex 未撤稿 |
| 77 | olaparib_pi | document/web | supplement（…drug price list; olaparib package insert） | — | — | — | — |

条目全文：

1. Dent R, Trudeau M, Pritchard KI, Hanna WM, Kahn HK, Sawka CA, et al. Triple-negative breast cancer: clinical features and patterns of recurrence. Clin Cancer Res. 2007;13(15 Pt 1):4429-34. doi:10.1158/1078-0432.CCR-06-3045
2. Liedtke C, Mazouni C, Hess KR, André F, Tordai A, Mejia JA, et al. Response to neoadjuvant therapy and long-term survival in patients with triple-negative breast cancer. J Clin Oncol. 2008;26(8):1275-81. doi:10.1200/JCO.2007.14.4147
3. Schmid P, Cortes J, Pusztai L, McArthur H, Kümmel S, Bergh J, et al. Pembrolizumab for Early Triple-Negative Breast Cancer. N Engl J Med. 2020;382(9):810-21. doi:10.1056/NEJMoa1910549
4. Schmid P, Cortes J, Dent R, Pusztai L, McArthur H, Kümmel S, et al. Event-free Survival with Pembrolizumab in Early Triple-Negative Breast Cancer. N Engl J Med. 2022;386(6):556-67. doi:10.1056/NEJMoa2112651
5. Schmid P, Cortes J, Dent R, McArthur H, Pusztai L, Kümmel S, et al. Overall Survival with Pembrolizumab in Early-Stage Triple-Negative Breast Cancer. N Engl J Med. 2024;391(21):1981-91. doi:10.1056/NEJMoa2409932
6. Licata L, Mariani M, Viale G, Dent R, Tolaney SM, Schmid P, et al. Timing of Recurrence after Neoadjuvant Chemo-Immunotherapy in Patients with Early-Stage Triple-Negative Breast Cancer. Clin Cancer Res. 2025;31(18):3916-21. doi:10.1158/1078-0432.CCR-25-1478
7. Japanese Breast Cancer Society. Report of the National Breast Cancer Registry, No. 55: cases diagnosed in 2024 [Internet; members only]. Tokyo: Japanese Breast Cancer Society; 2026 [cited 2026 Oct 26]. Available from: https://www.jbcs.gr.jp/modules/journals/index.php?content_id=8. Japanese.
8. Ministry of Health, Labour and Welfare. National Health Insurance drug price list and information on generic drugs: injections, products listed as of 14 October 2026 [Internet]. Tokyo: Ministry of Health, Labour and Welfare; 2026 [cited 2026 Oct 22]. Available from: https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_02.xlsx. Japanese.
9. Courneya KS, Vardy JL, O'Callaghan CJ, Gill S, Friedenreich CM, Wong RKS, et al. Structured Exercise after Adjuvant Chemotherapy for Colon Cancer. N Engl J Med. 2025;393(1):13-25. doi:10.1056/NEJMoa2502760
10. Furmaniak AC, Menig M, Markes MH. Exercise for women receiving adjuvant therapy for breast cancer. Cochrane Database Syst Rev. 2016;9(9):CD005001. doi:10.1002/14651858.CD005001.pub3
11. Courneya KS, Segal RJ, Mackey JR, Gelmon K, Reid RD, Friedenreich CM, et al. Effects of aerobic and resistance exercise in breast cancer patients receiving adjuvant chemotherapy: a multicenter randomized controlled trial. J Clin Oncol. 2007;25(28):4396-404. doi:10.1200/JCO.2006.08.2024
12. van Waart H, Stuiver MM, van Harten WH, Geleijn E, Kieffer JM, Buffart LM, et al. Effect of Low-Intensity Physical Activity and Moderate- to High-Intensity Physical Exercise During Adjuvant Chemotherapy on Physical Fitness, Fatigue, and Chemotherapy Completion Rates: Results of the PACES Randomized Clinical Trial. J Clin Oncol. 2015;33(17):1918-27. doi:10.1200/JCO.2014.59.1081
13. Mijwel S, Backman M, Bolam KA, Jervaeus A, Sundberg CJ, Margolin S, et al. Adding high-intensity interval training to conventional training modalities: optimizing health-related outcomes during chemotherapy for breast cancer: the OptiTrain randomized controlled trial. Breast Cancer Res Treat. 2018;168(1):79-93. doi:10.1007/s10549-017-4571-3
14. Courneya KS, Segal RJ, McKenzie DC, Dong H, Gelmon K, Friedenreich CM, et al. Effects of exercise during adjuvant chemotherapy on breast cancer outcomes. Med Sci Sports Exerc. 2014;46(9):1744-51. doi:10.1249/MSS.0000000000000297
15. Sanft T, Harrigan M, McGowan C, Cartmel B, Zupa M, Li FY, et al. Randomized Trial of Exercise and Nutrition on Chemotherapy Completion and Pathologic Complete Response in Women With Breast Cancer: The Lifestyle, Exercise, and Nutrition Early After Diagnosis Study. J Clin Oncol. 2023;41(34):5285-95. doi:10.1200/JCO.23.00871
16. Kjeldsted E, Ammitzbøll G, Lænkholm AV, Rasic D, Ceballos SG, Jørgensen LB, et al. Effects of Supervised Exercise during Neoadjuvant Chemotherapy on Tumor Response in Patients with Breast Cancer (Neo-train): A Randomized Controlled Trial. Clin Cancer Res. 2025;31(20):4265-77. doi:10.1158/1078-0432.CCR-25-0416
17. Schmidt ME, Goldschmidt S, Kreutz C, Müller J, Schneeweiss A, May AM, et al. Effects of aerobic or resistance exercise during neoadjuvant chemotherapy on tumor response and therapy completion in women with breast cancer: The randomized controlled BENEFIT trial. J Sport Health Sci. 2025;14:101064. doi:10.1016/j.jshs.2025.101064
18. Dias Rato N, Garcia C, Pinto D, Guedes H, Joaquim A, Viamonte S, et al. Exercise and pathologic complete response to cancer treatment: a systematic review and meta-analysis. Support Care Cancer. 2026;34(10):948. doi:10.1007/s00520-026-11156-1
19. de Boniface J, Altena R, Haddad Ringborg C, Bolam KA, Wengström Y. Physical exercise during neoadjuvant chemotherapy for breast cancer as a mean to increase pathological complete response rates: Trial protocol of the randomized Neo-ACT trial. PLoS One. 2022;17(10):e0274804. doi:10.1371/journal.pone.0274804
20. Khan KA, Mazuquin B, Canaway A, Petrou S, Bruce J. Systematic review of economic evaluations of exercise and physiotherapy for patients treated for breast cancer. Breast Cancer Res Treat. 2019;176(1):37-52. doi:10.1007/s10549-019-05235-7
21. Gubler-Gut BE, Pöhlmann J, Flatz A, Schwenkglenks M, Rohrmann S. Cost-effectiveness of physical activity interventions in cancer survivors of developed countries: a systematic review. J Cancer Surviv. 2021;15(6):961-75. doi:10.1007/s11764-021-01002-0
22. Wang Y, McCarthy AL, Hayes SC, Gordon LG, Chiu V, Bailey TG, et al. Economic evaluation of exercise interventions for individuals with cancer: A systematic review. Prev Med. 2023;172:107491. doi:10.1016/j.ypmed.2023.107491
23. May AM, Bosch MJ, Velthuis MJ, van der Wall E, Steins Bisschop CN, Los M, et al. Cost-effectiveness analysis of an 18-week exercise programme for patients with breast and colon cancer undergoing adjuvant chemotherapy: the randomised PACT study. BMJ Open. 2017;7(3):e012187. doi:10.1136/bmjopen-2016-012187
24. van Waart H, van Dongen JM, van Harten WH, Stuiver MM, Huijsmans R, Hellendoorn-van Vreeswijk JAJH, et al. Cost-utility and cost-effectiveness of physical exercise during adjuvant chemotherapy. Eur J Health Econ. 2018;19(6):893-904. doi:10.1007/s10198-017-0936-0
25. Perrier L, Foucaut AM, Morelle M, Touillaud M, Kempf-Lépine AS, Heinz D, et al. Cost-effectiveness of an exercise and nutritional intervention versus usual nutritional care during adjuvant treatment for localized breast cancer: the PASAPAS randomized controlled trial. Support Care Cancer. 2020;28(6):2829-42. doi:10.1007/s00520-019-05078-4
26. Boudewijns EA, Otten TM, Gobianidze M, Ramaekers BL, van Schayck OCP, Joore MA. Headroom Analysis for Early Economic Evaluation: A Systematic Review. Appl Health Econ Health Policy. 2023;21(2):195-204. doi:10.1007/s40258-022-00774-5
27. Huang M, A Fasching P, Haiderali A, Xue W, Yang C, Pan W, et al. Cost-Effectiveness of Neoadjuvant Pembrolizumab Plus Chemotherapy Followed by Adjuvant Single-Agent Pembrolizumab for High-Risk Early-Stage Triple-Negative Breast Cancer in the United States. Adv Ther. 2023;40(3):1153-70. doi:10.1007/s12325-022-02365-1
28. Kwong A, Leung R, Chan TC, Khandelwal A, Mishra K, Huang M. Cost-effectiveness of Pembrolizumab in Combination with Chemotherapy as Neoadjuvant Treatment and Continued as a Single Agent Adjuvant Treatment for High-Risk Early-Stage Triple-Negative Breast Cancer in Hong Kong. Oncol Ther. 2024;12(3):525-47. doi:10.1007/s40487-024-00285-4
29. Favre-Bulle A, Huang M, Haiderali A, Bhadhuri A. Cost-Effectiveness of Neoadjuvant Pembrolizumab plus Chemotherapy Followed by Adjuvant Pembrolizumab in Patients with High-Risk, Early-Stage, Triple-Negative Breast Cancer in Switzerland. Pharmacoecon Open. 2024;8(1):91-101. doi:10.1007/s41669-023-00445-8
30. Pöllinger B, Haiderali A, Huang M, Akyol Ersoy B, Abdelaziz AH, Kassem L, et al. The cost-effectiveness of treatment for high-risk, early-stage, triple-negative breast cancer in Egypt: an analysis of neoadjuvant pembrolizumab plus chemotherapy followed by adjuvant single-agent pembrolizumab. J Med Econ. 2025;28(1):105-13. doi:10.1080/13696998.2024.2441073
31. Chisaki Y, Nakamura N, Komuro T, Nyuji H, Harano M, Kitada N. Cost-Effectiveness Analysis of Pembrolizumab Plus Chemotherapy Compared with Chemotherapy as First-Line Treatment for Advanced PD-L1-Positive Triple-Negative Breast Cancer from a Japanese Healthcare Perspective. Clin Drug Investig. 2025;45(6):317-26. doi:10.1007/s40261-025-01445-8
32. Sugiura K, Hiratsuka H, Oshima G, Aiko S. Cost-effectiveness analysis of pembrolizumab in patients with treatment-refractory metastatic colorectal cancer in Japan. Jpn J Clin Oncol. 2023;53(8):691-7. doi:10.1093/jjco/hyad050
33. Taniguchi S, Moriwaki K, Morimoto K, Shimozuma K. Cost-Effectiveness of Pembrolizumab as First-Line Therapy for Advanced Colorectal Cancer With High Microsatellite Instability or Mismatched Repair Deficiency in Japan. Value Health Reg Issues. 2026;54:101555. doi:10.1016/j.vhri.2025.101555
34. Kakinuma H, Takada D, Itoshima H, Kunisawa S, Moriwaki K, Honda M, et al. Cost-effectiveness analysis of pembrolizumab plus chemotherapy versus chemotherapy as first line chemotherapy for patients with unresectable advanced esophageal cancer in Japan. Esophagus. 2025;22(4):583-92. doi:10.1007/s10388-025-01144-5
35. Morimoto K, Moriwaki K, Nishikawa Y, Maeda T, Toyama M, Agatsuma N, et al. Comparative Cost-Effectiveness Analysis of Multiple First-Line Treatments for HER2-Negative Unresectable Advanced or Recurrent Gastric Cancer in Japan. Pharmacoecon Open. 2026;10(3):471-89. doi:10.1007/s41669-025-00634-7
36. Tomura K, Sakamaki H, Nawata S, Ishida H, Tanaka K, Kogo M. Cost-effectiveness analysis of first line pembrolizumab monotherapy for high programmed cell death ligand 1 expressed, advanced non-small cell lung cancer in Japan. Int J Clin Pharm. 2025;47(2):304-13. doi:10.1007/s11096-024-01826-7
37. Kashiwa M, Maeda H. Comparative Cost-Effectiveness of Gemcitabine and Cisplatin in Combination with S-1, Durvalumab, or Pembrolizumab as First-Line Triple Treatment for Advanced Biliary Tract Cancer. J Gastrointest Cancer. 2024;55(4):1569-80. doi:10.1007/s12029-024-01106-7
38. Center for Outcomes Research and Economic Evaluation for Health, National Institute of Public Health. Products designated for cost-effectiveness evaluation since fiscal year 2019 [Internet]. Wako: National Institute of Public Health; 2026 [cited 2026 Oct 26]. Available from: https://c2h.niph.go.jp/results/item.html. Japanese.
39. Ax AK, Husberg M, Johansson B, Demmelmaier I, Berntsen S, Sjövall K, et al. Cost-effectiveness of different exercise intensities during oncological treatment in the Phys-Can RCT. Acta Oncol. 2023;62(4):414-21. doi:10.1080/0284186X.2023.2200149
40. Center for Outcomes Research and Economic Evaluation for Health, National Institute of Public Health. Guideline for preparing cost-effectiveness evaluation to the Central Social Insurance Medical Council, approved on 16 January 2026 [Internet]. Wako: National Institute of Public Health; 2026 [cited 2026 Oct 26]. Available from: https://c2h.niph.go.jp/tools/guideline/guideline_en_2026.pdf.
41. Hasegawa M, Komoto S, Shiroiwa T, Fukuda T. Formal Implementation of Cost-Effectiveness Evaluations in Japan: A Unique Health Technology Assessment System. Value Health. 2020;23(1):43-51. doi:10.1016/j.jval.2019.10.005
42. Ministry of Health, Labour and Welfare. Handling of cost-effectiveness evaluation of pharmaceuticals, medical devices and regenerative medicine products: notification of 13 February 2026 [Internet]. Tokyo: Ministry of Health, Labour and Welfare; 2026 [cited 2026 Oct 26]. Available from: https://c2h.niph.go.jp/tools/system/notification_cost-effectiveness_2026.pdf. Japanese.
43. Schmid P, Cortés J, Dent RA, Pusztai L, McArthur HL, Kummel S, et al. LBA18 Pembrolizumab or placebo plus chemotherapy followed by pembrolizumab or placebo for early-stage TNBC: Updated EFS results from the phase III KEYNOTE-522 study. Ann Oncol. 2023;34 Suppl 2:S1257. doi:10.1016/j.annonc.2023.10.008
44. Schmid P, Cortes J, Dent RA, McArthur HL, Pusztai L, Kuemmel S, et al. Neoadjuvant pembrolizumab or placebo plus chemotherapy followed by adjuvant pembrolizumab or placebo for high-risk early-stage TNBC: Final analysis results from the phase 3 KEYNOTE-522 study. J Clin Oncol. 2026;44(16 Suppl):507. doi:10.1200/JCO.2026.44.16_suppl.507
45. Husereau D, Drummond M, Augustovski F, de Bekker-Grob E, Briggs AH, Carswell C, et al. Consolidated Health Economic Evaluation Reporting Standards 2022 (CHEERS 2022) statement: updated reporting guidance for health economic evaluations. BMJ. 2022;376:e067975. doi:10.1136/bmj-2021-067975
46. Chan KKW, Chu RWK, Cheung MC, Courneya KS, O'Callaghan CJ, Vardy JL, et al. Structured Exercise Program After Adjuvant Chemotherapy for Colon Cancer: A Cost-Utility Analysis of the CHALLENGE Trial. J Clin Oncol. 2026;44(22):2130-9. doi:10.1200/JCO-26-00765
47. World Bank. PPP conversion factor, GDP (LCU per international $) [Internet]. Washington, DC: World Bank; 2026 [cited 2026 Oct 26]. Available from: https://data.worldbank.org/indicator/PA.NUS.PPP.
48. Ministry of Health, Labour and Welfare. Revision of the medical fee schedule for fiscal year 2026: Ministry of Health, Labour and Welfare Notification No. 69 of 2026 [Internet]. Tokyo: Ministry of Health, Labour and Welfare; 2026 [cited 2026 Oct 26]. Available from: https://www.mhlw.go.jp/stf/newpage_67729.html. Japanese.
49. Guyot P, Ades AE, Ouwens MJ, Welton NJ. Enhanced secondary analysis of survival data: reconstructing the data from published Kaplan-Meier survival curves. BMC Med Res Methodol. 2012;12:9. doi:10.1186/1471-2288-12-9
50. Grinda T, Antoine A, Jacot W, Cottu PH, de la Motte Rouge T, Frenel JS, et al. Real-world clinical and survival outcomes of patients with early relapsed triple-negative breast cancer from the ESME national cohort. Eur J Cancer. 2023;189:112935. doi:10.1016/j.ejca.2023.05.023
51. Ministry of Health, Labour and Welfare. Abridged life tables for Japan 2025 [Internet]. Tokyo: Ministry of Health, Labour and Welfare; 2026 [cited 2026 Oct 21]. Available from: https://www.mhlw.go.jp/toukei/saikin/hw/life/life25/index.html. Japanese.
52. European Medicines Agency. Keytruda (pembrolizumab): variation assessment report, procedure no. EMEA/H/C/003820/II/0110, EMA/257879/2022 [Internet]. Amsterdam: European Medicines Agency; 2022 [cited 2026 Oct 26]. Available from: https://www.ema.europa.eu/en/documents/variation-report/keytruda-h-c-003820-ii-0110-epar-assessment-report-variation_en.pdf.
53. Ludwig K, Graf von der Schulenburg JM, Greiner W. German Value Set for the EQ-5D-5L. Pharmacoeconomics. 2018;36(6):663-74. doi:10.1007/s40273-018-0615-8
54. Iwatani T, Noto S, Tsugawa K. Changes in Health State Utility Values in Japanese Patients with End-Stage Breast Cancer. Curr Oncol. 2021;28(5):4203-12. doi:10.3390/curroncol28050356
55. Shiroiwa T, Fukuda T, Shimozuma K, Mouri M, Hagiwara Y, Kawahara T, et al. Cost-effectiveness analysis of the introduction of S-1 therapy for first-line metastatic breast cancer treatment in Japan: results from the randomized phase III SELECT BC trial. BMC Cancer. 2017;17(1):773. doi:10.1186/s12885-017-3774-7
56. Pharmaceutical Benefits Advisory Committee. Public summary document, March 2023 PBAC meeting: pembrolizumab, solution concentrate for I.V. infusion 100 mg in 4 mL vial, Keytruda, Merck Sharp & Dohme (Australia) Pty Ltd [Internet]. Canberra: Australian Government Department of Health and Aged Care; 2023 [cited 2026 Oct 26]. Available from: https://www.pbs.gov.au/info/industry/listing/elements/pbac-meetings/psd/2023-03/pembrolizumab-earlyTNBC-keytruda-PSD-March-2023.
57. Fedele P, Rizzo A, Landriscina M, Stucci LS, Inneo C, Morritti M, et al. Early first-line systemic anticancer therapeutic attrition after metastatic recurrence in triple-negative breast cancer following neoadjuvant chemo-immunotherapy: a multicenter real-world study. Breast Cancer Res Treat. 2026;218(1):8. doi:10.1007/s10549-026-08023-2
58. Elmore LC, Kuerer HM, Barcenas CH, Smith BD, Miggins MV, Lucci A, et al. Clinical Course of Breast Cancer Patients with Local-Regional Progression During Neoadjuvant Systemic Therapy. Ann Surg Oncol. 2021;28(10):5477-85. doi:10.1245/s10434-021-10444-w
59. Cortes J, O'Shaughnessy J, Loesch D, Blum JL, Vahdat LT, Petrakova K, et al. Eribulin monotherapy versus treatment of physician's choice in patients with metastatic breast cancer (EMBRACE): a phase 3 open-label randomised study. Lancet. 2011;377(9769):914-23. doi:10.1016/S0140-6736(11)60070-6
60. Masuda N, Lee SJ, Ohtani S, Im YH, Lee ES, Yokota I, et al. Adjuvant Capecitabine for Breast Cancer after Preoperative Chemotherapy. N Engl J Med. 2017;376(22):2147-59. doi:10.1056/NEJMoa1612645
61. Tutt ANJ, Garber JE, Kaufman B, Viale G, Fumagalli D, Rastogi P, et al. Adjuvant Olaparib for Patients with BRCA1- or BRCA2-Mutated Breast Cancer. N Engl J Med. 2021;384(25):2394-405. doi:10.1056/NEJMoa2105215
62. Garber JE, Cameron D, Campbell C, Yothers G, Taboada M, El-Abed S, et al. Sustained benefit of adjuvant olaparib in women with germline BRCA1- and BRCA2-associated high-risk HER2-negative early breast cancer: updated results from the OlympiA phase III trial. Ann Oncol. 2026. Epub ahead of print. doi:10.1016/j.annonc.2026.08.002
63. AstraZeneca. Datroway demonstrated an unprecedented median overall survival improvement of five months vs. chemotherapy as 1st-line treatment for patients with metastatic triple-negative breast cancer for whom immunotherapy was not an option in TROPION-Breast02 [Internet]. Cambridge: AstraZeneca; 2025 Oct 19 [cited 2026 Oct 26]. Available from: https://www.astrazeneca.com/media-centre/press-releases/2025/datroway-demonstrated-an-unprecedented-median-overall-survival-improvement-of-five-months-vs-chemotherapy-as-1st-line-treatment-for-patients-with-metastatic-triple-negative-breast-cancer-for-whom-immunotherapy-was-not-an-option-in-tropion-breast02.html.
64. Cortes J, Cescon DW, Rugo HS, Nowecki Z, Im SA, Yusof MM, et al. Pembrolizumab plus chemotherapy versus placebo plus chemotherapy for previously untreated locally recurrent inoperable or metastatic triple-negative breast cancer (KEYNOTE-355): a randomised, placebo-controlled, double-blind, phase 3 clinical trial. Lancet. 2020;396(10265):1817-28. doi:10.1016/S0140-6736(20)32531-9
65. Miller K, Wang M, Gralow J, Dickler M, Cobleigh M, Perez EA, et al. Paclitaxel plus bevacizumab versus paclitaxel alone for metastatic breast cancer. N Engl J Med. 2007;357(26):2666-76. doi:10.1056/NEJMoa072113
66. Nusawat C, Sato S, Taniguchi J, Kimura Y, Yasunaga H. Cost-effectiveness analysis of immune checkpoint inhibitors versus platinum-based doublet chemotherapy in the first-line treatment of advanced non-small-cell lung cancer with High PD-L1 expression in Japan. Eur J Health Econ. 2026. Epub ahead of print. doi:10.1007/s10198-026-01912-9
67. Ohtera S, Sakai M, Iwao T, Neff Y, Takahashi Y, Kato G, et al. Health Care Utilization and Hospital Expenditures Among Inpatients Dying of Cancer in Japan. Value Health. 2018;21 Suppl 2:S60. doi:10.1016/j.jval.2018.07.458
68. Bank of Canada. Annual exchange rates [Internet]. Ottawa: Bank of Canada; 2026 [cited 2026 Oct 26]. Available from: https://www.bankofcanada.ca/rates/exchange/annual-average-exchange-rates/.
69. Japan Society of Clinical Oncology. Guidelines for the appropriate use of antiemetics, October 2023 revision, 3rd ed. Tokyo: Kanehara Shuppan; 2023. Japanese.
70. Kasugai Municipal Hospital. Estimated hospitalization costs [Internet]. Kasugai: Kasugai Municipal Hospital; 2024 [cited 2026 Oct 26]. Available from: https://www.hospital.kasugai.aichi.jp/goriyo/nyuin/documents/nyuinhiyougaisan.pdf. Japanese.
71. Chuden Hospital. Estimated costs of surgery and other treatments [Internet]. Hiroshima: Chuden Hospital; [date unknown; cited 2026 Oct 26]. Available from: https://www.energia.co.jp/hospital/nyuuin/surgical-costs.html. Japanese.
72. Kuemmel S, Fasching PA, Schmid P, Harbeck N, Takahashi M, Untch M, et al. Surgical Outcomes After Neoadjuvant Pembrolizumab Plus Chemotherapy for Triple-Negative Breast Cancer: Results from the Randomized, Placebo-Controlled Phase 3 KEYNOTE-522 Study. Ann Surg Oncol. 2026;33(6):5550-7. doi:10.1245/s10434-026-19121-2
73. Yoshinami T, Shibata N, Tamaki K, Ishimaru K, Ito S, Nukada T, et al. Real-world evidence of febrile neutropenia-related hospitalization on patients with perioperative chemotherapy for early breast cancer in Japan. Breast Cancer. 2025;32(4):857-66. doi:10.1007/s12282-025-01714-6
74. Andrade MO, Bonadio RC, Ipiña A, Testa L, Tavares MC, Balint FC, et al. Treatment patterns and safety of adjuvant therapy after chemoimmunotherapy for early-stage triple-negative breast cancer: real-world data from the Neo-Real/GBECAM 0123 study. Breast Cancer Res Treat. 2026;216(3):27. doi:10.1007/s10549-026-07938-0
75. Valachis A, Geisler J, Karihtala P, Tuxen MK. Insights on postneoadjuvant treatment among patients with triple-negative breast cancer and residual disease after neoadjuvant therapy: can expert consensus help to interpret the current evidence? Br J Cancer. 2026;135(3):329-35. doi:10.1038/s41416-026-03452-8
76. Fujisawa F, Tamaki Y, Inoue T, Nakayama T, Yagi T, Kittaka N, et al. Prevalence of BRCA1 and BRCA2 mutations in Japanese patients with triple-negative breast cancer: A single institute retrospective study. Mol Clin Oncol. 2021;14(5):96. doi:10.3892/mco.2021.2258
77. AstraZeneca KK. Lynparza tablets 100 mg and 150 mg: package insert, revised 17 March 2026 [Internet]. Osaka: AstraZeneca KK; 2026 [cited 2026 Oct 26]. Available from: https://www.pmda.go.jp/PmdaSearch/iyakuDetail/GeneralList/4291052F1027. Japanese.

## 4. 文件与网页（无 DOI）及会议摘要的核对

| 号 | key | 核对 |
|---|---|---|
| 7 | jbcs55 | HTTP 200; page states 第55号2024年次症例を掲載いたしました（2026.6.16） and that the report is for members only; the values used were sent by A. Ozaki on 2026-10-26 (input/params/cohort_N_jbcs2024.csv); the original table has not been received, so the values could not be checked against the report |
| 8 | price2026 | HTTP 200 (xlsx) on 2026-10-26; file name and download date 2026-10-22 as recorded in input/params/sources_hara.md |
| 38 | c2h_list | HTTP 200; 88 products designated from fiscal year 2019 to 2026 listed; pembrolizumab (キイトルーダ) not among them (2026-10-26) |
| 40 | c2h_guideline | HTTP 200; PDF p.1 'This version was approved by CSIMC on 16th January, 2026'; p.25 'Both cost and effectiveness should be discounted at a rate of 2% per year' |
| 42 | mhlw_ce2026 | HTTP 200; PDF p.1 産情発0213第３号・保発0213第７号 令和８年２月13日; p.9 総合的評価 for products whose approved indication is a malignant tumour (ウ 悪性腫瘍), for indications without sufficient treatment and for children; p.13 thresholds 500万円/QALY, 750万円/QALY for products given consideration in the comprehensive assessment |
| 43 | esmo2023 | Crossref record (LBA18, volume 34, page S1257, issued 2023-10; no issue field); DOI resolved at doi.org (302); supplement 2 as in input/user_supplied_values.csv, which gives pages S1256-S1257 (Crossref gives S1257 only, used here)；doi.org 302（2026-10-27） |
| 44 | kn522final2026 | Crossref record; DOI resolved at doi.org (302); volume 44, issue 16_suppl, page 507；doi.org 302（2026-10-27） |
| 47 | worldbank_ppp | HTTP 200; indicator page PA.NUS.PPP |
| 48 | fee2026 | HTTP 200; page title 令和８年度診療報酬改定について, lists 診療報酬の算定方法の一部を改正する件（令和８年厚生労働省告示第69号） (2026-10-26) |
| 51 | lifetable2025 | HTTP 200; page 令和7年簡易生命表の概況; files and access date 2026-10-21 in input/lifetable/SOURCE.md; base period 1 January to 31 December 2025 (life25-01_about.pdf p.1), so published in 2026 |
| 52 | ema2022 | HTTP 200 (PDF); p.1 '22 April 2022 EMA/257879/2022 ... Assessment report Keytruda ... Procedure No. EMEA/H/C/003820/II/0110' |
| 56 | pbac2023 | HTTP 200 (page 'Pembrolizumab – March 2023'); heading from p.1 of the downloaded document (input/params/sources_utility/PBAC_PSD_pembrolizumab_early-TNBC_2023-03.pdf) |
| 63 | tropion2025 | title and date 19 October 2025 read on the page (2026-10-26); the parameter workbook names 'TROPION-Breast02 (Daiichi Sankyo/AstraZeneca, October 2025)' without a date, and this is the October 2025 release that reports the trial results (the 6 October release gives top-line results only) -- to be confirmed by A. Ozaki |
| 67 | ohtera2018 | Crossref record (volume 21, page S60, issued 2018-09; no issue field); supplement S2 from the ISPOR abstract page (Value in Health Volume 21, Supplemental S2)；doi.org 302（2026-10-27） |
| 68 | boc_fx | HTTP 200; page 'Annual exchange rates' |
| 69 | jsco2023 | Minds guideline page https://minds.jcqhc.or.jp/summary/c00828/ (HTTP 200): 制吐薬適正使用ガイドライン 2023年10月改訂 第3版, 日本癌治療学会, published by 金原出版 on 2023-10-20 |
| 70 | hosp_kasugai | HTTP 200 (PDF, sha256 7881e456…); p.1 入院費用概算金額: 乳腺悪性腫瘍手術 乳房部分切除術, 5～10 days, 300,000 yen at 30% copayment; linked from the page 入院医療費 updated 2024-09-24 |
| 71 | hosp_chuden | HTTP 200; page 手術費用等概算一覧表｜中電病院: 乳腺悪性腫瘍手術, 15 days, about 300,000 yen at 30% copayment; no date on the page |
| 77 | olaparib_pi | PMDA page: リムパーザ錠100mg／150mg, 製造販売元 アストラゼネカ株式会社, package insert PDF dated 2026年03月17日 (2026-10-26) |

## 5. 读过但未引用的候选

| key | PMID | 题名 | 未引用的理由 |
|---|---|---|---|
| ax2022 | 35607981 | Long-term resource utilisation and associated costs of exercise during (neo)adjuvant oncological treatment: the Phys-Can project. | Phys-Can long-term resource use and costs; the cost-effectiveness analysis of the same project (ax2023) is cited as the nearest study |
| campbell2019 | 31626055 | Exercise Guidelines for Cancer Survivors: Consensus Statement from International Multidisciplinary Roundtable. | consensus exercise guidelines for cancer survivors; the text states no guideline recommendation |
| cannioto2021 | 32239145 | Physical Activity Before, During, and After Chemotherapy for High-Risk Breast Cancer: Relationships With Survival. | observational analysis of physical activity before, during and after chemotherapy and survival; Introduction paragraph 2 reports randomized evidence only, so it was dropped in v5 |
| iyengar2025 | 39306704 | Effects of exercise therapy on chemotherapy delivery and response in primary breast cancer: A secondary analysis of a randomized trial. | secondary analysis of a phase 2 trial; pCR in a neoadjuvant subgroup of 51 tumours, 27% with exercise and 28% with usual care; Introduction paragraph 2 cites the meta-analysis for pCR (diasrato2026) |
| shiroiwa2020 | 32419677 | Cost-effectiveness evaluation for pricing medicines and devices: A new value-based price adjustment system in Japan. | Japan's value-based price adjustment system (2020); the thresholds are cited from the 2026 notification (mhlw_ce2026) |

## 6. 引用审核（ARS citation_compliance 的项目）

| 项目 | 结果 |
|---|---|
| 文献数 | 77（期刊 58、会议摘要 3、文件与网页 16）；本文首次引用 62 篇，其余 15 篇首次出现在表、图注或补充材料 |
| 孤立引用 | 引用了但不在表中 0；在表中但没有被引用 0 |
| 格式 | Vancouver（NLM）：作者 6 名后 et al、刊名用 PubMed 缩写、页码省略重复数字、DOI 置末；make_ledger 逐条比对条目文本（list_text_equals_entries） |
| 无 DOI | 16 篇，全是文件与网页：jbcs55, price2026, c2h_list, c2h_guideline, mhlw_ce2026, worldbank_ppp, fee2026, lifetable2025, ema2022, pbac2023, tropion2025, boc_fx, jsco2023, hosp_kasugai, hosp_chuden, olaparib_pi |
| DOI 实测 | 61 / 61 返回 30x |
| 自引 | 0（作者名 Ozaki A, Hara A 在 PubMed 作者列表中） |
| 近 5 年（2022–2026） | 50 / 76（66%） |
| 超过 10 年 | 8：[1] dent2007 (2007), [2] liedtke2008 (2008), [11] courneya2007 (2007), [12] vanwaart2015 (2015), [14] courneya2014 (2014), [49] guyot2012 (2012), [59] cortes2011 (2011), [65] miller2007 (2007)（TNBC 的复发与 pCR 的报告、运动试验与转移期治疗试验的原始报告、生存数据的重建方法） |
| 撤稿 | 0；Crossref 的更正、新版等记录：furmaniak2016（new_version 10.1002/14651858.cd005001.pub2） |
| PubMed 与 Crossref 的写法差异 | 11 篇，逐条读过两边的记录，都是写法不同，不是不同的文献（第 3 节 Crossref 比对一栏） |
| 正文的作者-年份式引用 | 0（make_ledger author_year_in_text） |

## 7. 备注

- esmo2023（[43]）：Crossref 记录的页码是 S1257；input/user_supplied_values.csv 写的是 S1256–S1257。条目按 Crossref 写 S1257。
- tropion2025（[63]）：参数表只写 “TROPION-Breast02 (Daiichi Sankyo/AstraZeneca, October 2025)”，没有日期；引用的是 2025-10-19 报告试验结果的新闻稿（10 月 6 日的只有顶线结果）。待尾崎先生确认。
- jbcs55（[7]）：日本乳癌学会的登记报告只对会员公开；所用数值是尾崎先生 2026-10-26 提供的（input/params/cohort_N_jbcs2024.csv），原表未收到，数值无法与报告核对。
- kwong2024（[28]）：香港的分析，效用用的是英国的 EQ-5D-5L 价值集，所以 Supplementary Table S10 写作 United Kingdom。
- huang2023（[27]）：作者名 “A Fasching P” 照 PubMed 与 Crossref 记录。
- furmaniak2016：Cochrane 综述 2016 年版（pub3）是 2009 年版（pub2）的新版本，不是撤稿。
- 医院费用（hosp_kasugai、hosp_chuden）：按待决事项 N6 写医院名与网址；临床专家只写 “two breast medical oncologists at Japanese hospitals, personal communication, October 2026”（单人的行写 “a breast medical oncologist”），不写姓名。
- kn522final2026（[44]）：摘要全文取自 Crossref 记录（support_cache.json），截点 2025-10-14、全体 7 年 EFS 与 OS 与所用值一致。按 pCR 分层的 7 年 EFS（90.4% 对 85.9%，57.6% 对 49.7%）不在摘要中，读自 ASCO 2026 报告的报道（OncLive 2026-06-01、DelveInsight；data/kn522_final_7y.csv）；报道写 “at median follow-up”，按尾崎先生的指示作为 7 年值（input/params/efficacy_sources.md 第 27 行）。引用的是该次分析的摘要；分层值的原始出处待尾崎先生确认（docs/model_spec.md 第 87 行同类事项）。
- esmo2023（[43]）：LBA18 的摘要页返回 HTTP 403，原文未取得；2023-03-23 截点的分层值读自 OncLive 2023-10-20 的报道（input/user_supplied_values.csv），原始出处待尾崎先生确认（docs/model_spec.md 第 87 行）。v5 起本文 Methods 的截点列表加入 23 March 2023，因为这些值用于选择分布族（Supplementary Methods S1）。
- pbac2023（[56]）：公开摘要（PSD）p.18 只写 “Utilities were based on EQ-5D responses in KN-522”，未写价值集。Methods 写作 “those of the Australian reimbursement submission”；Supplementary Table S10 的行名 “Utility value set: Australia” 是 v4 的原文，本版未改，列为待决事项。
- boc_fx（[68]）：加拿大银行的汇率只用于运动方案费用的上限（参数表 E01 备考：上限は為替で換算）；v5 起 Methods 的购买力平价句只引世界银行，汇率的引用留在 Table 1 与 Supplementary Table S2 的出处栏。

## 8. 引用句与原著的对照（规约第 1.3 节、第 13 节）

由 manuscript/code/refs/claim_support.py 检查（2026-10-27）：每条记录的原文段落（逐字）须出现在所示的出处中。开放获取的全文从 Europe PMC 取得（manuscript/code/refs/fetch_support.py；XML 不放进仓库，sha256 记在 support_cache.json），本次已对全文重新核对。

- 本文：82 处（句子 × 文献），全部有对照记录；图注与补充材料的散文：22 处，全部有对照记录；表与 Supplementary Table S2 的出处栏：131 处，按第 8.2 节的位置记录核对。
- 找到 119 / 119；未找到 0；未能核对 0。
- 状态：corroborated 2；ok 109；provided 4；report 4（ok = 原著中有该段；corroborated = 原著非开放获取，段落取自另一篇被引文献；report = 原著未取得，数值读自会议报道；provided = 共著者提供，原著未见）。

### 8.1 本文、图注与补充材料的散文

| 位置 | 文献 | 出处 | 原文段落 | 状态 | 找到 | 备注 |
|---|---|---|---|---|---|---|
| I.1 s1 | [1] dent2007 | PubMed abstract | increased likelihood of distant recurrence (hazard ratio, 2.6; 95% confidence interval, 2.0-3.5; P < 0.0001) and death (hazard ratio, 3.2; 95% confidence interval, 2.3-4.5; P < 0.001) within 5 years of diagnosis but not thereafter | ok | 是 |  |
| I.1 s2 | [2] liedtke2008 | PubMed abstract | those with pCR have excellent survival. However, patients with RD after neoadjuvant chemotherapy have significantly worse survival if they have TNBC compared with non-TNBC | ok | 是 |  |
| I.1 s3 | [3] schmid2020 | PubMed abstract | the percentage of patients with a pathological complete response was 64.8% (95% confidence interval [CI], 59.9 to 69.5) in the pembrolizumab-chemotherapy group and 51.2% (95% CI, 44.1 to 58.3) in the placebo-chemotherapy group | ok | 是 |  |
| I.1 s3 | [4] schmid2022 | PubMed abstract | resulted in significantly longer event-free survival than neoadjuvant chemotherapy alone | ok | 是 |  |
| I.1 s3 | [5] schmid2024 | PubMed abstract | resulted in a significant improvement, as compared with neoadjuvant chemotherapy alone, in overall survival | ok | 是 |  |
| I.1 s4 | [6] licata2025 | PubMed abstract | Recurrences within 24 months account for most recurrences in patients with TNBC who relapse after neoadjuvant chemo-immunotherapy. | ok | 是 |  |
| I.1 s5 | [7] jbcs55 | input/params/cohort_N_jbcs2024.csv | "nac_total","TNBC（M0）II、III 期的术前化疗例（2024 年）","3451" … "nac_pembro","其中术前用帕博利珠单抗","2294" | provided | 是 | values sent by A. Ozaki on 2026-10-26; the members-only report was not seen |
| I.1 s6 | [3] schmid2020 | PubMed abstract | the two groups then received an additional four cycles of pembrolizumab or placebo … After definitive surgery, the patients received adjuvant pembrolizumab or placebo every 3 weeks for up to nine cycles. | ok | 是 |  |
| I.1 s6 | [8] price2026 | input/params/sources_price/tp20261014-01_02.xlsx (row with all passages) | キイトルーダ点滴静注１００ｍｇ … 199462 | ok | 是 | 100 mg vial JPY 199,462; one 200 mg dose = 2 vials = JPY 398,924 |
| I.2 s1 | [9] courneya2025 | PubMed abstract | A 3-year structured exercise program initiated soon after adjuvant chemotherapy for colon cancer resulted in significantly longer disease-free survival | ok | 是 |  |
| I.2 s2 | [9] courneya2025 | PubMed abstract | hazard ratio for disease recurrence, new primary cancer, or death, 0.72; 95% confidence interval [CI], 0.55 to 0.94 | ok | 是 |  |
| I.2 s3 | [10] furmaniak2016 | PubMed abstract | physical exercise during adjuvant treatment for breast cancer probably improves physical fitness … and slightly reduces fatigue | ok | 是 |  |
| I.2 s3 | [11] courneya2007 | PubMed abstract | they did improve self-esteem, physical fitness, body composition, and chemotherapy completion rate | ok | 是 | fatigue: 'favored the exercise groups but did not reach statistical significance' |
| I.2 s3 | [12] vanwaart2015 | PubMed abstract | Onco-Move and OnTrack resulted in less decline in cardiorespiratory fitness (P < .001) … OnTrack also resulted in better outcomes for muscle strength (P = .002) and physical fatigue (P < .001) | ok | 是 |  |
| I.2 s3 | [13] mijwel2018 | PubMed abstract | 16 weeks of resistance and HIIT was effective in preventing increases in CRF | ok | 是 | CRF, cancer-related fatigue; cited for fatigue |
| I.2 s4 | [14] courneya2014 | PubMed abstract | we report an exploratory follow-up of cancer outcomes … (HR, 0.68; 95% confidence interval (CI), 0.37-1.24; log-rank, P = 0.21) | ok | 是 |  |
| I.2 s5 | [15] sanft2023 | PubMed abstract | Among 72 women who received neoadjuvant chemotherapy, women randomly assigned to intervention were more likely to have a pCR than those randomly assigned to UC (53% v 28%; P = .037) | ok | 是 |  |
| I.2 s5 | [16] kjeldsted2025 | PubMed abstract | received supervised high-intensity interval training and progressive resistance training … Although the exercise program did not affect tumor size | ok | 是 |  |
| I.2 s5 | [17] schmidt2025 | PubMed abstract | supervised resistance training … Overall, there was no significant difference in post-intervention tumor size between RT or AT and WCG. | ok | 是 |  |
| I.2 s6 | [18] diasrato2026 | PubMed abstract | Eight studies involving 504 patients with breast, esophageal, gastric, or rectal cancer were included … there were no significant differences between exercise and control groups in the rate of pCR to NACT | ok | 是 |  |
| I.2 s7 | [19] deboniface2022 | PubMed abstract | The primary endpoint is pCR … disease-free survival at 2, 5 and 10 years … In order to show an improvement in pCR of 10%, a total of 712 participants need to be included in the analysis. … The Neo-ACT has been registered at clinicaltrials.gov on January 11, 2022 | ok | 是 |  |
| I.3 s2 | [20] khan2019 | Europe PMC full text PMC6548756 (sha256 a580f2d2) | post-operative exercise versus control [ 12 , 26 ], exercise versus control during adjuvant breast cancer treatment [ 13 , 25 , 27 , 28 ] and exercise versus control following breast cancer treatment [ 29 ] … all but one study included in this systematic review measured health consequences in terms of QALYs … change in body mass index (BMI) and cardiorespiratory fitness [ 25 ] … fatigue and QALYs [ 28 ] | ok | 是 |  |
| I.3 s2 | [21] gublergut2021 | Europe PMC full text PMC8521580 (sha256 ce92594b) | OnTrack could be cost-effective for general and physical fatigue depending on willingness to pay … Cardiorespiratory fitness showed a short- and long-term increase in the low-to-moderate- and high-intensity groups [ 56 ] | ok | 是 |  |
| I.3 s2 | [22] wang2023 | PubMed abstract | Exercise interventions were found to be cost-effective in five of ten (50%) trial-based economic evaluations and in five of the six (83%) model-based economic evaluations. | ok | 是 | study designs and outcomes; the outcomes measured are shown by the full texts of khan2019 and gublergut2021 |
| I.3 s3 | [23] may2017 | PubMed abstract | the 18-week exercise programme was cost-effective for colon cancer, but not for breast cancer | ok | 是 |  |
| I.3 s3 | [24] vanwaart2018 | PubMed abstract | Depending on the decision-makers' willingness-to-pay, OnTrack could be considered cost-effective in comparison with UC. | ok | 是 |  |
| I.3 s3 | [25] perrier2020 | PubMed abstract | The 6-month exercise program was deemed to be cost-effective compared with usual care for the estimated aerobic capacity. | ok | 是 |  |
| I.3 s4 | [26] boudewijns2023 | PubMed abstract | The headroom analysis is an early economic evaluation that quantifies the highest price at which an intervention may still be cost effective. | ok | 是 |  |
| I.3 s5 | [27] huang2023 | PubMed abstract | for patients with high-risk eTNBC in the USA | ok | 是 |  |
| I.3 s5 | [28] kwong2024 | PubMed abstract | from a Hong Kong third-party payer perspective | ok | 是 |  |
| I.3 s5 | [29] favrebulle2024 | PubMed abstract | from a Swiss third-party payer perspective | ok | 是 |  |
| I.3 s5 | [30] pollinger2025 | PubMed abstract | from an Egyptian societal perspective | ok | 是 |  |
| I.3 s6 | [31] chisaki2025 | PubMed abstract | patients with PD-L1-positive inoperable or metastatic TNBC from a Japanese healthcare perspective | ok | 是 |  |
| I.3 s6 | [32] sugiura2023 | PubMed abstract | microsatellite-instability-high/mismatch repair-deficient metastatic colorectal cancer … The Japanese healthcare payer's perspective was adopted. | ok | 是 |  |
| I.3 s6 | [33] taniguchi2026 | PubMed abstract | advanced colorectal cancer with high microsatellite instability or mismatched repair deficiency in Japan | ok | 是 |  |
| I.3 s6 | [34] kakinuma2025 | PubMed abstract | advanced esophageal cancer … from a Japanese healthcare payer perspective | ok | 是 |  |
| I.3 s6 | [35] morimoto2026 | PubMed abstract | HER2-negative unresectable advanced or recurrent gastric cancer … from the Japanese healthcare payer perspective | ok | 是 |  |
| I.3 s6 | [36] tomura2025 | PubMed abstract | stage IV advanced NSCLC … in Japan | ok | 是 |  |
| I.3 s6 | [37] kashiwa2024 | PubMed abstract | advanced biliary tract cancer … from the perspective of Japanese healthcare payer | ok | 是 |  |
| I.3 s7 | [38] c2h_list | check in references.py | pembrolizumab (キイトルーダ) not among them | ok | 是 |  |
| I.4 s4 | [39] ax2023 | PubMed abstract | a six-month exercise programme of high (HI) or low-to-moderate intensity (LMI) during (neo)adjuvant oncological treatment … 189 participants with breast, colorectal, or prostate cancer | ok | 是 |  |
| M.SB.1 s2 | [3] schmid2020 | PubMed abstract | patients with previously untreated stage II or stage III triple-negative breast cancer to receive neoadjuvant therapy | ok | 是 |  |
| M.SB.1 s2 (age 49) | [3] schmid2020 | Europe PMC full text PMC9988745 (sha256 5496016c) | based on an average starting age of 49 years from KEYNOTE-522 | corroborated | 是 | the age is in the baseline table of the trial report, which is not open access; passage from the full text of huang2023 |
| M.SB.1 s5 | [7] jbcs55 | input/params/cohort_N_jbcs2024.csv | "nac_pembro","其中术前用帕博利珠单抗","2294" | provided | 是 | values sent by A. Ozaki on 2026-10-26; the members-only report was not seen |
| M.SB.2 s2 | [40] c2h_guideline | check in references.py | Both cost and effectiveness should be discounted at a rate of 2% per year | ok | 是 |  |
| M.SB.2 s3 | [41] hasegawa2020 | PubMed abstract | If the cost per quality-adjusted life-year (QALY) threshold falls below ¥5 million per QALY | ok | 是 |  |
| M.SB.2 s3 | [42] mhlw_ce2026 | check in references.py | thresholds 500万円/QALY | ok | 是 |  |
| M.SB.2 s4 | [42] mhlw_ce2026 | check in references.py | malignant tumour (ウ 悪性腫瘍) … 750万円/QALY for products given consideration in the comprehensive assessment | ok | 是 |  |
| M.SB.3 s1 | [4] schmid2022 | PubMed abstract | data cutoff, March 23, 2021 | ok | 是 |  |
| M.SB.3 s1 | [43] esmo2023 | input/user_supplied_values.csv | ESMO 2023; data cutoff 2023-03-23, median follow-up 63.1 months | report | 是 | abstract LBA18 not obtained (publisher page HTTP 403); values read in the OncLive report of the ESMO 2023 presentation (input/user_supplied_values.csv); original source to be confirmed by A. Ozaki (docs/model_spec.md line 87) |
| M.SB.3 s1 | [5] schmid2024 | PubMed abstract | At the data-cutoff date (March 22, 2024) | ok | 是 |  |
| M.SB.3 s1 | [44] kn522final2026 | Crossref abstract | At the data cutoff date (October 14, 2025) | ok | 是 |  |
| M.SB.3 s4 | [45] husereau2022 | PubMed abstract | This summary article presents the new CHEERS 2022 28-item checklist | ok | 是 |  |
| M.VAR.1 s4 | [9] courneya2025 | PubMed abstract | 0.72; 95% confidence interval [CI], 0.55 to 0.94 | ok | 是 |  |
| M.VAR.2 s5 | [9] courneya2025 | PubMed abstract | Musculoskeletal adverse events occurred more often in the exercise group than in the health-education group (in 18.5% vs. 11.5% of patients). | ok | 是 |  |
| M.VAR.3 s2 | [46] chan2026 | PubMed abstract | despite an up-front cost of $2,917 (CAD)/participant to provide the SEP … Mean costs (2024 in Canadian dollars [CAD]) | ok | 是 |  |
| M.VAR.3 s2 | [47] worldbank_ppp | check in references.py | indicator page PA.NUS.PPP | ok | 是 |  |
| M.VAR.3 s3 | [48] fee2026 | check in references.py | 令和８年度診療報酬改定について | ok | 是 |  |
| M.VAR.4 s1 | [49] guyot2012 | PubMed abstract | we propose a method which derives from the published Kaplan Meier survival curves a close approximation to the original individual patient time-to-event data | ok | 是 |  |
| M.VAR.4 s1 | [4] schmid2022 | output/phase1/phase1_report.md | / K22_S4_EFS_by_pCR / Schmid 2022 NEJM 386:556 appendix / Fig. S4 / | ok | 是 | EFS by arm and pCR status, supplementary appendix Fig. S4 |
| M.VAR.4 s2 | [44] kn522final2026 | data/kn522_final_7y.csv | EFS rates for patients who achieved pathological complete responses (pCR) at median follow-up in each arm were 90.4% for the pembrolizumab arm compared with 85.9% for the placebo arm … Patients without pCR EFS 57.6% 49.7% | report | 是 | stratified 7-year values are not in the abstract; they were read in reports of the ASCO 2026 presentation (OncLive and DelveInsight, data/kn522_final_7y.csv); the citation is to the abstract of record |
| M.VAR.4 s3 | [50] grinda2023 | PubMed abstract | Epidemio-Strategy-Medico-Economical-Metastatic Breast Cancer (ESME-MBC) database, a multicenter, national, observational cohort | ok | 是 |  |
| M.VAR.4 s3 | [50] grinda2023 | PubMed affiliations | Gustave Roussy … Villejuif, France | ok | 是 | French centres |
| M.VAR.4 s5 | [51] lifetable2025 | check in references.py | 令和7年簡易生命表の概況 | ok | 是 |  |
| M.VAR.5 s2 | [8] price2026 | check in references.py | HTTP 200 (xlsx) on 2026-10-26 | ok | 是 |  |
| M.VAR.5 s2 | [48] fee2026 | check in references.py | 令和８年度診療報酬改定について | ok | 是 |  |
| M.VAR.5 s3 | [4] schmid2022 | PubMed abstract | Adverse events occurred predominantly during the neoadjuvant phase | ok | 是 |  |
| M.VAR.5 s3 | [52] ema2022 | check in references.py | Assessment report Keytruda | ok | 是 |  |
| M.VAR.5 s4 | [29] favrebulle2024 | Europe PMC full text PMC10781656 (sha256 c5de3bef) | Health state utility values used in the base case were derived from EQ-5D-5L data collected in the KEYNOTE-522 trial … There is no EQ-5D value set for Switzerland; therefore, the model used the German value set in the base-case analysis | ok | 是 |  |
| M.VAR.5 s4 | [53] ludwig2018 | PubMed abstract | to develop a value set for EQ-5D-5L based on the societal preferences of the German population | ok | 是 |  |
| M.VAR.5 s6 | [54] iwatani2021 | Europe PMC full text PMC8535054 (sha256 6dd87098) | HSUVs calculated using the EQ-5D-5L derived from the Japanese value set | ok | 是 |  |
| M.VAR.5 s6 | [55] shiroiwa2017 | PubMed abstract | some of the randomized patients participated in an EQ-5D survey (N = 391) | ok | 是 |  |
| M.SA.2 s2 | [5] schmid2024 | PubMed abstract | Overall survival was a secondary end point. | ok | 是 |  |
| M.SA.2 s2 | [44] kn522final2026 | Crossref abstract | The 7-yr OS rate (95% CI) was 85.1% (82.5-87.5) in the pembro group vs 77.2% (72.7-81.1) in the pbo group | ok | 是 |  |
| M.SA.6 s2 | [27] huang2023 | Europe PMC full text PMC9988745 (sha256 5496016c) | US 5L value set [ 25 ] for the base case | ok | 是 |  |
| M.SA.6 s2 | [28] kwong2024 | Europe PMC full text PMC11333381 (sha256 497370a5) | Utilities based on the UK EQ-5D-5L value set were used in the base case analysis. | ok | 是 |  |
| M.SA.6 s2 | [56] pbac2023 | check in references.py | heading from p.1 of the downloaded document | ok | 是 | PSD p.18 'Utilities were based on EQ-5D responses in KN-522' (input/params/sources_utility/PBAC_PSD_pembrolizumab_early-TNBC_2023-03.pdf); the value set is not named, so the text says 'those of the Australian reimbursement submission' |
| M.SA.6 s3 | [57] fedele2026 | PubMed abstract | We conducted a retrospective multicenter analysis of 209 consecutive patients with early-stage TNBC treated with neoadjuvant chemo-immunotherapy. | ok | 是 |  |
| M.SA.6 s3 | [57] fedele2026 | PubMed affiliations | Bari, Italy | ok | 是 | Italian centres |
| M.SA.6 s4 | [58] elmore2021 | PubMed abstract | Median overall survival (OS) time for patients with progression was 26 months … identified from a prospective database | ok | 是 |  |
| M.SA.6 s4 | [58] elmore2021 | PubMed affiliations | The University of Texas MD Anderson Cancer Center, Houston, TX, USA | ok | 是 | single centre |
| M.SA.6 s5 | [59] cortes2011 | PubMed abstract | We aimed to compare overall survival of heavily pretreated patients receiving eribulin versus currently available treatments. | ok | 是 |  |
| M.SA.6 s5 | [60] masuda2017 | PubMed abstract | the addition of adjuvant capecitabine therapy was safe and effective in prolonging disease-free survival | ok | 是 |  |
| M.SA.6 s5 | [61] tutt2021 | PubMed abstract | adjuvant olaparib after completion of local treatment and neoadjuvant or adjuvant chemotherapy | ok | 是 |  |
| M.SA.6 s5 | [62] garber2026 | PubMed abstract | 1 year of adjuvant olaparib after (neo)adjuvant chemotherapy demonstrated ongoing clinically meaningful improvements | ok | 是 |  |
| M.SA.7 s2 | [7] jbcs55 | input/params/cohort_N_jbcs2024.csv | "nac_pembro","其中术前用帕博利珠单抗","2294" | provided | 是 | values sent by A. Ozaki on 2026-10-26; the members-only report was not seen |
| figures: CHALLENGE trial | [9] courneya2025 | PubMed abstract | hazard ratio for disease recurrence, new primary cancer, or death, 0.72 | ok | 是 |  |
| supplement: Checklist and guidance as published | [45] husereau2022 | PubMed abstract | This summary article presents the new CHEERS 2022 28-item checklist | ok | 是 |  |
| supplement: with a data cutoff of 23 March 2021 | [4] schmid2022 | output/phase1/phase1_report.md | / K22_S4_EFS_by_pCR / Schmid 2022 NEJM 386:556 appendix / Fig. S4 / | ok | 是 |  |
| supplement: with a data cutoff of 22 March 2024 | [5] schmid2024 | output/phase1/phase1_report.md | / K24_S4_OS_by_pCR / Schmid 2024 NEJM 391:1981 appendix / Fig. S4 / | ok | 是 | overall survival by arm: Fig. 1A of the 2024 report (phase1_report line 333) |
| supplement: algorithm of Guyot and colleagues | [49] guyot2012 | PubMed abstract | We develop an algorithm that maps from digitised curves back to KM data | ok | 是 |  |
| supplement: Japanese life table for women | [51] lifetable2025 | check in references.py | 令和7年簡易生命表の概況 | ok | 是 |  |
| supplement: reported at a later data cutoff was selected | [43] esmo2023 | input/user_supplied_values.csv | ESMO 2023; data cutoff 2023-03-23, median follow-up 63.1 months | report | 是 | abstract LBA18 not obtained (publisher page HTTP 403); values read in the OncLive report of the ESMO 2023 presentation (input/user_supplied_values.csv); original source to be confirmed by A. Ozaki (docs/model_spec.md line 87) |
| supplement: fixed at the value of the final analysis | [44] kn522final2026 | data/kn522_final_7y.csv | Patients without pCR EFS 57.6% 49.7% | report | 是 | stratified 7-year values are not in the abstract; they were read in reports of the ASCO 2026 presentation (OncLive and DelveInsight, data/kn522_final_7y.csv); the citation is to the abstract of record |
| supplement: in the proportion reported for each arm | [5] schmid2024 | docs/model_spec.md | 2024 年 Table 1 的例数除以该臂非 pCR 人数 | ok | 是 |  |
| supplement: in the proportions of the 2024 report | [5] schmid2024 | docs/model_spec.md | EFS 的超额风险按各臂首发事件构成（2024 年 Table 1）分配 | ok | 是 |  |
| supplement: to distant recurrence at a constant rate | [4] schmid2022 | docs/model_spec.md | 2022 年 Table 1 脚注的局部复发后远处复发例数 | ok | 是 |  |
| supplement: in the numbers reported for each arm | [4] schmid2022 | docs/model_spec.md | 各臂的人数取 2022 年补充材料 Table S5 | ok | 是 |  |
| supplement: Strategy and Medical Economics (ESME) cohort | [50] grinda2023 | docs/model_spec.md | ESME（Grinda 等 Eur J Cancer 2023，Fig. 3a | ok | 是 |  |
| supplement: abridged life table for Japanese women | [51] lifetable2025 | check in references.py | 令和7年簡易生命表の概況 | ok | 是 |  |
| supplement: confidence intervals of the final analysis | [44] kn522final2026 | Crossref abstract | The 7-yr EFS rate (95% CI) was 78.3% (75.3-81.1) in the pembro group vs 69.8% (65.0-74.2) in the pbo group | ok | 是 |  |
| supplement: the published curves of the 2024 report | [49] guyot2012 | PubMed abstract | We develop an algorithm that maps from digitised curves back to KM data | ok | 是 |  |
| supplement: the published curves of the 2024 report | [5] schmid2024 | output/phase1/phase1_report.md | 2 条 OS（2024 年 Fig. 1A，按臂）从随机化起 | ok | 是 |  |
| supplement: 7-year estimates of the final analysis | [44] kn522final2026 | Crossref abstract | The 7-yr OS rate (95% CI) was 85.1% (82.5-87.5) in the pembro group vs 77.2% (72.7-81.1) in the pbo group | ok | 是 |  |
| supplement: curves (overall survival, 2024 report) | [49] guyot2012 | PubMed abstract | We develop an algorithm that maps from digitised curves back to KM data | ok | 是 |  |
| supplement: curves (overall survival, 2024 report) | [5] schmid2024 | output/phase1/phase1_report.md | 2 条 OS（2024 年 Fig. 1A，按臂）从随机化起 | ok | 是 |  |
| supplement: ; final analysis | [44] kn522final2026 | Crossref abstract | At the data cutoff date (October 14, 2025) | ok | 是 |  |
| supplement: (cases diagnosed in 2024, final version) | [7] jbcs55 | input/params/cohort_N_jbcs2024.csv | 日本乳癌学会 全国乳がん患者登録調査報告 第55号（2024年次症例、確定版） | provided | 是 | values sent by A. Ozaki on 2026-10-26; the members-only report was not seen |

### 8.2 出处栏（Table 1 与 Supplementary Table S2）

Table 1 的出处栏汇总 Supplementary Table S2 的出处，文献相同。Panel A（生存）按下表的项目文件记录核对；Panel B 按参数表 input/params/parameters_v10.xlsx 的「出典」与「出典の該当箇所」两列（原著中的位置）逐行列出。

| Panel A 的出处 | 文献 | 记录位置的文件 | 记录 | 找到 |
|---|---|---|---|---|
| KEYNOTE-522 (interim analysis 4) | [4] | docs/model_spec.md | 2022 年补充材料 Fig. S4（IA4）的 494/784 与 217/390 | 是 |
| KEYNOTE-522 final analysis | [44] | data/kn522_final_7y.csv | efs_pcr_pembro,90.4 | 是 |
| Fitted to reconstructed KEYNOTE-522 data (interim analysis 4) | [49], [4] | output/phase1/phase1_report.md | / K22_S4_EFS_by_pCR / Schmid 2022 NEJM 386:556 appendix / Fig. S4 / | 是 |
| KEYNOTE-522 (2024 report) | [5] | docs/model_spec.md | 2024 年 Table 1 | 是 |
| KEYNOTE-522 (2022 report) | [4] | docs/model_spec.md | 2022 年 Table 1 脚注的局部复发后远处复发例数 | 是 |
| ESME cohort, reconstructed overall survival | [50], [49] | docs/model_spec.md | ESME（Grinda 等 Eur J Cancer 2023，Fig. 3a | 是 |
| ESME cohort | [50] | docs/model_spec.md | ESME（Grinda 等 Eur J Cancer 2023，Fig. 3a | 是 |
| Abridged life table (2025) | [51] | docs/model_spec.md | 令和7年简易生命表 | 是 |
| Italian real-world cohort after neoadjuvant pembrolizumab | [57] | docs/model_spec.md | Fedele | 是 |
| Single-center cohort with locoregional progression during neoadjuvant therapy | [58] | docs/model_spec.md | Elmore | 是 |

| param_id | 文献 | 出典 | 出典の該当箇所 |
|---|---|---|---|
| A01 | [8] | 厚生労働省 薬価基準収載品目リスト（注射薬）tp20261014-01_02.xlsx（令和8年10月14日収載品目反映版、令和8年4月1日以降の薬価） | パクリタキセル、カルボプラチンの各行（後発品の最低薬価） |
| A02 | [8] | 厚生労働省 薬価基準収載品目リスト（注射薬）tp20261014-01_02.xlsx（令和8年10月14日収載品目反映版、令和8年4月1日以降の薬価） | ドキソルビシン塩酸塩（リポソーム製剤を除く）、シクロホスファミド水和物の各行 |
| A03 | [8] | 厚生労働省 薬価基準収載品目リスト（注射薬）tp20261014-01_02.xlsx（令和8年10月14日収載品目反映版、令和8年4月1日以降の薬価） | ペムブロリズマブ（遺伝子組換え）キイトルーダ点滴静注100mg |
| A04 | [48] | 診療報酬点数表 令和8年度 | B001-2-12, G004, G020, D005, D007, D400, D026 |
| A05 | [8], [69] | 薬価基準 令和8年度; 日本癌治療学会 制吐薬適正使用ガイドライン2023（第3版） | 計算根拠_尾崎 A05（追加・修正） |
| A06 | [70], [71], [48], [72] | 春日井市民病院 入院費用概算金額; 中電病院 手術費用等概算一覧表; K476（令和8年度）; Kuemmel S, et al. Ann Surg Oncol 2026 | 乳房部分切除術 3割負担30万円（在院5〜10日） |
| A07 | [72] | Kuemmel S, et al. Ann Surg Oncol 2026;33:5550-7 | 抄録（術式割合、リンパ節のpCR 76.7%対69.9%） |
| A08 | [48] | 診療報酬点数表 令和8年度 | M001 2イ（41,500点、一連）, M000 1, 専任加算 |
| B01 | [66] | Nusawat C, et al. Eur J Health Econ 2026. doi:10.1007/s10198-026-01912-9 | Table 1（DPCデータ、1ドル150円で換算） |
| B02 | [66] | Nusawat C, et al. Eur J Health Econ 2026. doi:10.1007/s10198-026-01912-9 | Table 1（DPCデータ、1ドル150円で換算） |
| B03 | [73] | Yoshinami T, et al. Breast Cancer 2025;32:857-66. doi:10.1007/s12282-025-01714-6 | 代理値 |
| B04 | [73] | Yoshinami T, et al. Breast Cancer 2025;32:857-66. doi:10.1007/s12282-025-01714-6 | 代理値 |
| B05 | [66] | Nusawat C, et al. Eur J Health Econ 2026. doi:10.1007/s10198-026-01912-9 | Table 1（DPCデータ、1ドル150円で換算） |
| B06 | [66] | Nusawat C, et al. Eur J Health Econ 2026. doi:10.1007/s10198-026-01912-9 | Table 1（DPCデータ、1ドル150円で換算） |
| B07 | [66] | Nusawat C, et al. Eur J Health Econ 2026. doi:10.1007/s10198-026-01912-9 | Table 1（DPCデータ、1ドル150円で換算）（大腸炎の値を代用） |
| B08 | [73], [66] | Yoshinami T, et al. Breast Cancer 2025;32:857-66. doi:10.1007/s12282-025-01714-6; Nusawat C, et al. Eur J Health Econ 2026. doi:10.1007/s10198-026-01912-9 | 代理値; Table 1（皮疹） |
| B09 | [73] | Yoshinami T, et al. Breast Cancer 2025;32:857-66. doi:10.1007/s12282-025-01714-6 | 代理値 |
| B10 | [73] | Yoshinami T, et al. Breast Cancer 2025;32:857-66. doi:10.1007/s12282-025-01714-6 | 代理値 |
| B11 | [73] | Yoshinami T, et al. Breast Cancer 2025;32:857-66. doi:10.1007/s12282-025-01714-6 | Abstract、Results（平均236,000円、中央値189,000円、在院中央値6日） |
| B21P | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hypothyroidism） |
| B21C | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hypothyroidism） |
| B22P | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hyperthyroidism） |
| B22C | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hyperthyroidism） |
| B23P | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Adrenal insufficiency） |
| B23C | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Adrenal insufficiency） |
| B24P | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hypophysitis） |
| B24C | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hypophysitis） |
| B25P | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Pneumonitis） |
| B25C | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Pneumonitis） |
| B26P | [52] | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.101 本文（Grade 3-4 の AEOSI） |
| B26C | [52] | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.97 表（全Grade、画像から転記） |
| B27P | [52] | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.101 本文（Grade 3-4 の AEOSI） |
| B27C | [52] | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.97 表（全Grade、画像から転記） |
| B28P | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Severe skin reaction） |
| B28C | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Severe skin reaction） |
| B29P | [52] | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.100 Table 5.3.5.3.3-tnbc3: 30（画像から転記） |
| B29C | [52] | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.100 Table 5.3.5.3.3-tnbc3: 30（画像から転記） |
| B30P | [4], [52] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23); EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | Table 2 の免疫介在性有害事象 Grade 3以上の総数から、表の各項目と大腸炎、肝炎の Grade 3以上を差し引いた近似 |
| B30C | [4], [52] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23); EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | Table 2 の免疫介在性有害事象 Grade 3以上の総数から、表の各項目と大腸炎、肝炎の Grade 3以上を差し引いた近似 |
| B31P | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67, Supplementary Appendix (IA4, data cutoff 2021-03-23) | Table S7（Grade 3-5） |
| B31C | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67, Supplementary Appendix (IA4, data cutoff 2021-03-23) | Table S7（Grade 3-5） |
| B32P | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Any adverse event、Grade ≥3） |
| B32C | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Any adverse event、Grade ≥3） |
| B33P | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67, Supplementary Appendix (IA4, data cutoff 2021-03-23) | Table S7（Grade 3-5）の Neutropenia、Neutrophil count decreased、Anemia、Febrile neutropenia、White blood cell count decreased、Alanine aminotransferase increased |
| B33C | [4] | Schmid P, et al. N Engl J Med 2022;386:556-67, Supplementary Appendix (IA4, data cutoff 2021-03-23) | Table S7（Grade 3-5）の Neutropenia、Neutrophil count decreased、Anemia、Febrile neutropenia、White blood cell count decreased、Alanine aminotransferase increased |
| C01 | [48] | 診療報酬点数表 令和8年度 | A002, D007, D400, D009, D026, E001, E002, D215 |
| C02 | [48] | 同上 | 同上 |
| C03 | [48] | 同上 | 同上 |
| D03 | [63], [64], [65], [8] | 立花和之進 先生（個人的連絡、2026年10月24日）; TROPION-Breast02（第一三共/AstraZeneca 2025年10月）; Cortes J, et al. Lancet 2020; Miller K, et al. NEJM 2007; 薬価基準 令和8年度 | 計算根拠_尾崎（追加：立花先生の回答） |
| D03P | [63], [64], [65], [8] | 立花和之進 先生（個人的連絡、2026年10月24日）; TROPION-Breast02（第一三共/AstraZeneca 2025年10月）; Cortes J, et al. Lancet 2020; Miller K, et al. NEJM 2007; 薬価基準 令和8年度 | 計算根拠_尾崎（追加：立花先生の回答） |
| D04 | [63], [64], [65], [8] | 立花和之進 先生（個人的連絡、2026年10月24日）; TROPION-Breast02（第一三共/AstraZeneca 2025年10月）; Cortes J, et al. Lancet 2020; Miller K, et al. NEJM 2007; 薬価基準 令和8年度 | PFS中央値（オラパリブ7.0、ペムブロリズマブ＋化学療法9.7、ダトロウェイ10.8、ベバシズマブ＋PTX 11.8か月）を加重 |
| D04P | [63], [64], [65], [8] | 立花和之進 先生（個人的連絡、2026年10月24日）; TROPION-Breast02（第一三共/AstraZeneca 2025年10月）; Cortes J, et al. Lancet 2020; Miller K, et al. NEJM 2007; 薬価基準 令和8年度 | PFS中央値で加重 |
| D05 | [8] | 立花和之進 先生（個人的連絡、2026年10月24日）; 薬価基準 令和8年度 | 二次治療以降の選択 |
| D06 | [66], [67] | Nusawat C, et al. Eur J Health Econ 2026. doi:10.1007/s10198-026-01912-9（厚労省 医療保険部会2022を引用）; Ohtera S, et al. ISPOR AP 2018 | Table 1; 抄録 |
| E01 | [46], [47], [68] | Chan KKW, et al. J Clin Oncol 2026;44:2130-9; 世界銀行PPP 2024; カナダ銀行 為替2024 | 本文（プログラム費用2,917カナダドル） |
| E02 | [48] | 診療報酬点数表 令和8年度 | H002 運動器リハビリテーション料(I) 185点 |
| E03 | [48] | 診療報酬点数表 令和8年度 | H002, A001（オンライン再診） |
| E04 | [48] | 診療報酬点数表 令和8年度 | H002, A001 |
| E05 | [9] | Courneya KS, et al. N Engl J Med 2025;393:13-25 | プログラム期間（3年） |
| E06 | [9] | Courneya KS, et al. N Engl J Med 2025;393:13-25 (CHALLENGE, CCTG CO.21). DOI 10.1056/NEJMoa2502760 | 本文 p.19（Results の Safety）、Supplementary Appendix Table S4（p.77） |
| E07 | [9] | Courneya KS, et al. N Engl J Med 2025;393:13-25 (CHALLENGE, CCTG CO.21). DOI 10.1056/NEJMoa2502760 | 本文 p.19（Results の Safety）、Supplementary Appendix Table S4（p.77） |
| E08 | [48] | 診療報酬点数表 令和8年度 | A000, E001 1イ, E002 1ロ, F400 3, A002 |
| E09 | [9] | Courneya KS, et al. N Engl J Med 2025;393:13-25 (CHALLENGE, CCTG CO.21). DOI 10.1056/NEJMoa2502760 | 本文 p.19（Results の Safety）、Supplementary Appendix Table S4（p.77） |
| E10 | [9] | Courneya KS, et al. N Engl J Med 2025;393:13-25 (CHALLENGE, CCTG CO.21). DOI 10.1056/NEJMoa2502760 | 本文 p.19（Results の Safety）、Supplementary Appendix Table S4（p.77） |
| F01P | [74], [75] | 立花和之進 先生、押正徳 先生（個人的連絡、2026年10月）; Andrade MdeO, et al. Breast Cancer Res Treat 2026;216:27（Neo-Real/GBECAM 0123）; Valachis A, et al. Br J Cancer 2026;135:329-35 | 施設の実感（8〜9割／1例のみ）; Neo-Real：gBRCA陰性の残存病変207例でペムブロリズマブ＋カペシタビン57.5%; 北欧Delphi：RCB2〜3で74% |
| F02 | [8], [60] | 薬価基準 令和8年度; Masuda N, et al. N Engl J Med 2017;376:2147-59 | CREATE-X の用法（1,250mg/m2 1日2回、14日投与7日休薬） |
| F03 | [76] | Fujisawa F, et al. Mol Clin Oncol 2021;14:96. doi:10.3892/mco.2021.2258 | 13/65（20.0%） |
| F05 | [8], [77] | 薬価基準 令和8年度; リムパーザ添付文書 | 術後は1回300mg 1日2回、投与期間1年まで |
| F06 | [48] | 診療報酬点数表 令和8年度 | D006-18（20,200点）＋判断料100点 |
| F07 | [60] | Masuda N, et al. 2017. N Engl J Med 376:2147-59. DOI 10.1056/NEJMoa1612645 | Abstract, Results（TNBC サブグループ、DFS） |
| F08 | [62] | Garber JE, et al. 2026. Ann Oncol (online ahead of print). DOI 10.1016/j.annonc.2026.08.002 | Abstract, Results（第3回中間解析、追跡期間中央値6.1年、IDFS） |
| U01 | [29] | Favre-Bulle A, Huang M, Haiderali A, Bhadhuri A. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 |
| U02 | [29] | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 |
| U03 | [29] | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 |
| U04 | [29] | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 |
| U05 | [29] | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2（低下幅）; Methods（期間） |

