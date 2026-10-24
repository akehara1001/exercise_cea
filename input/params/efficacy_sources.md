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
- 适用的组（2026-10-23）：F07、F08 在含与不含帕博利珠单抗的组中用同一 HR，这是假设——CREATE-X 与 OlympiA 都不含帕博利珠单抗（`docs/model_spec.md` 第 2 节）。

# KEYNOTE-522 最终分析的分层 EFS（第十一轮的约束值，2026-10-23）

- 出处：Schmid P, et al. KEYNOTE-522 final analysis. J Clin Oncol 2026;44(16_suppl):507（ASCO 2026）。截点 2025-10-14，中位随访 93.8 个月。摘要原文未取得（`input/papers/SOURCE.md`），数值出自会议报道 OncLive 2026-06-01（DelveInsight、CancerNetwork 作对照），由 `R/py/12_final_analysis.py` 从保存的网页读取，写入 `data/kn522_final_7y.csv`。
- 7 年分层 EFS（第十一轮起的约束值，替代 2023-03-23 截点的 5 年值）：pCR 例帕博利珠单抗 90.4%、安慰剂 85.9%；non-pCR 例 57.6%、49.7%。报道写 "at median follow-up"，按尾崎的指示作为 7 年值；按全例 pCR 率（63.0% 对 55.6%）加权得 78.26% 与 69.83%，与全体 7 年 EFS 78.3% 与 69.8% 一致。
- 分层 HR（探索性，不作门槛的对照）：EFS pCR 0.68 [0.44, 1.07]、non-pCR 0.78 [0.59, 1.03]；OS pCR 0.64 [0.37, 1.14]（CancerNetwork；OncLive 印 [0.39, 1.14]）、non-pCR 0.76 [0.55, 1.03]。
- 本文中 EFS 的两臂差统一用 7 年值：全体 8.5 个百分点（78.3 对 69.8）、pCR 例 4.5（90.4 对 85.9）、non-pCR 例 7.9（57.6 对 49.7）。按 pCR 分层的结果是探索性解析，放补充材料。
- 2023-03-23 截点的 5 年分层 EFS（92.2/88.2、62.6/52.3）与层内 HR 0.65、0.72：第十一轮起只作不作门槛的跨分析对照（`input/user_supplied_values.csv`）。

## 不使用的来源及理由

- Pusztai L, et al. Ann Oncol 2024;35:429–436（按 RCB 分级的 EFS）：截点 2021-03-23，中位随访 39.1 个月，与现用的 IA4 曲线是同一次数据，不增加信息。
- 按 RCB 分级的 OS（第 7 次中期分析，Miami Breast Cancer Conference 2025）：早于最终分析。
- 尾崎若提供 ASCO 2026 发表幻灯片中的按 pCR 分层的曲线，另起任务处理。
