# 疗效 HR 来源（入力表 F07、F08）

由 `R/py/09_make_params_template.py` 从 `input/params/pubmed/` 中保存的 PubMed 摘要用正则抽取后写入入力表。摘要于 2026-10-21 经 NCBI E-utilities（efetch）取得。

## F07 卡培他滨（CREATE-X，TNBC 亚组）

- PMID：28564564
- 文献：Masuda N, et al. 2017. N Engl J Med 376:2147-59. DOI 10.1056/NEJMoa1612645
- 终点：DFS（复发、第二癌或死亡）
- HR 0.58，95% CI 0.39 至 0.87
- 摘要原文：“Among patients with triple-negative disease, the rate of disease-free survival was 69.8% in the capecitabine group versus 56.1% in the control group (hazard ratio for recurrence, second cancer, or death, 0.58; 95% CI, 0.39 to 0.87)”

## F08 奥拉帕利（OlympiA，iDFS）

- PMID：42636977（第三次中期分析，中位随访 6.1 年，在线先行发表）
- 文献：Garber JE, et al. 2026. Ann Oncol (online ahead of print). DOI 10.1016/j.annonc.2026.08.002
- 终点：iDFS，分层 Cox 模型
- HR 0.65，95% CI 0.53 至 0.78
- 摘要原文：“Olaparib benefits were maintained in IDFS (HR 0.65, 95% CI 0.53-0.78)”
- 选用理由：任务要求记录 95% CI；首次分析（PMID 34081848，Tutt 2021 NEJM）摘要只给出 99.5% CI：HR 0.58（99.5% CI 0.41 至 0.82）。第二次中期分析（PMID 36228963，Geyer 2022 Ann Oncol）摘要未给出 iDFS HR。
- 注意：OlympiA 全体人群含激素受体阳性患者，摘要中没有 TNBC 单独的 HR；入组为 gBRCA 致病变异且高危的 HER2 阴性早期乳腺癌，新辅助后 non-pCR 只是其中一部分。
