# 第2阶段 2a 报告：费用与 QALY 层（单元测试）与原负责的参数来源

生成时间：2026-10-25 04:28。由 `R/21_phase2a_report.R` 从代码输出生成。按指示本报告不含任何 ICER 或结果数值。

## 1. 状态

- 内部入力表（`input/params/parameters_v6.xlsx`；此前各版在 `input/params/archive/`）：原负责的 40 行中已填写 40 行；尾崎负责的 39 行中已填写 0 行（`output/params_check.md`）。
- 费用与 QALY 层：`R/econ.R`（规格见 `docs/model_spec.md` 第 2、5 节）。尾崎的行尚未返回，故只用合成数值做单元测试（`R/test_econ.R`）；生存参数为第 1 阶段的引擎默认（`data/fits/engine_params.rds`，第十五轮）；k 开关的测试用测试值 k = 1.5，只检验结构。
- 已实现（2026-10-25）：运动的筋骨格系有害事象（费用：加运动的两臂 E06 × E08、不加运动的两臂 E07 × E08；效用：E09 或 E10 × U05 × 12.5 周；都在时点 0 一次计入，E09、E10 为空时不计效用损失）；S-JP 的三条曲线按 `sjp_mix()` 的权重混合，F02、F05 计入接受者（手术时点仍无事件的 non-pCR 患者 × 组权重，折现到手术时点）；F06（BRCA 检测）在时点 0 对全部患者计入四个组。
- 尚未计入：只剩尾崎负责的数值（39 行，含 E08 与 F01P、F04P）。S-JP 情景在 F01P、F04P 到之前不运行（含帕博利珠单抗的臂缺这两个值时 `econ_arm(..., sjp = TRUE)` 报错），不输出任何结果数值。

## 2. 单元测试（`output/phase2/econ_unit_tests.csv`）

| 序号 | 测试 | 结果 | 检查的差或比较值 |
|---|---|---|---|
|  1 | 费用全为 0 时费用为 0、QALY 不变（四臂） | 通过 |    0 |
|  2 | 效用全为 1（不良事件效用下降为 0）时 QALY 等于折现后的生命年（四臂） | 通过 | 3.55e-15 |
|  3 | E06 = E07 且 E09 = E10、运动效应中性、方案费用为 0 时，加运动的臂与对应的不加运动的臂完全一致 | 通过 |    0 |
|  4 | 折现率为 0 时折现后的生命年等于未折现的生命年 | 通过 |    0 |
|  5 | 只把帕博利珠单抗每次药费设为 1 日元时，费用（折现后的期望给药次数）大于 0、不超过 17，单用化疗组为 0 | 通过 |    0 |
|  6 | 只把终末期费用设为 1 日元时，费用不超过死亡比例；对象为全部死亡时不小于只计癌症死亡时 | 通过 | 0.312 |
|  7 | 远处复发一线与二线以后月额相同时，费用与一线持续期 D04 无关 | 通过 | 4.44e-15 |
|  8 | 加入运动效应（测试值 HR 0.8）后 QALY 大于单用化疗 | 通过 | 0.798 |
|  9 | 效率前沿：在答案已知的合成例中正确判定劣势与扩展劣势 | 通过 |  |
| 10 | 情景 k = 1 的开关不改变单用化疗组；k > 1（测试值 1.5）时设为 k = 1 增加帕博利珠单抗组的生命年 | 通过 |    0 |
| 11 | 不良事件效用下降的口径：基准（6 种之和，B33）与情景（任何 3 级以上，B32）的 QALY 损失之比等于两者发生率之比 | 通过 | 4.44e-16 |
| 12 | E08 = 0 时各臂费用不变（等于去掉 E06、E07 × E08 一项的费用，且与 E06、E07 无关） | 通过 |    0 |
| 13 | E09、E10 为空（未分级报告）时不计效用损失 | 通过 |    0 |
| 14 | S-JP：F03 = 0 且 F01 = 0（F01P = 0）时与不加 S-JP 完全一致（四臂） | 通过 |    0 |
| 15 | S-JP：F07 = F08 = 1 时，与不加 S-JP 相比的差只来自 F02、F05 的费用（四臂；QALY 与生命年差 ≤ 1e-12，其余费用差 ≤ 1e-6 日元） | 通过 | 2.88e-09 |
| 16 | F06（BRCA 检测）在任何两组之间的差为 0（含 S-JP） | 通过 |    0 |
| 17 | F01P、F04P 为空时含帕博利珠单抗的臂不运行 S-JP（报错），其余臂可运行 | 通过 |  |

共 17 项，通过 17 项（第 1 至 11 项为原有各项，其中第 3 项自 2026-10-25 起同时要求 E06 = E07 且 E09 = E10；第 12 至 17 项为 2026-10-25 新增）。数值一栏为检查的偏差；其中第 6、8 项为比较量之差（全部死亡对癌症死亡的终末期费用；运动对单用化疗的 QALY），只用于判断方向，不是模型结果。

## 3. 原负责的参数与来源（详见 `input/params/sources_hara.md`、`input/params/efficacy_sources.md`、`input/papers/SOURCE.md`）

| param_id | 出典 | 该当箇所 |
|---|---|---|
| A01 | 厚生労働省 薬価基準収載品目リスト（注射薬）tp20261014-01_02.xlsx（令和8年10月14日収載品目反映版、令和8年4月1日以降の薬価） | パクリタキセル、カルボプラチンの各行（後発品の最低薬価） |
| A02 | 厚生労働省 薬価基準収載品目リスト（注射薬）tp20261014-01_02.xlsx（令和8年10月14日収載品目反映版、令和8年4月1日以降の薬価） | ドキソルビシン塩酸塩（リポソーム製剤を除く）、シクロホスファミド水和物の各行 |
| A03 | 厚生労働省 薬価基準収載品目リスト（注射薬）tp20261014-01_02.xlsx（令和8年10月14日収載品目反映版、令和8年4月1日以降の薬価） | ペムブロリズマブ（遺伝子組換え）キイトルーダ点滴静注100mg |
| B21P | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hypothyroidism） |
| B21C | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hypothyroidism） |
| B22P | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hyperthyroidism） |
| B22C | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hyperthyroidism） |
| B23P | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Adrenal insufficiency） |
| B23C | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Adrenal insufficiency） |
| B24P | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hypophysitis） |
| B24C | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hypophysitis） |
| B25P | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Pneumonitis） |
| B25C | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Pneumonitis） |
| B26P | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.101 本文（Grade 3-4 の AEOSI） |
| B26C | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.97 表（全Grade、画像から転記） |
| B27P | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.101 本文（Grade 3-4 の AEOSI） |
| B27C | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.97 表（全Grade、画像から転記） |
| B28P | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Severe skin reaction） |
| B28C | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Severe skin reaction） |
| B29P | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.100 Table 5.3.5.3.3-tnbc3: 30（画像から転記） |
| B29C | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.100 Table 5.3.5.3.3-tnbc3: 30（画像から転記） |
| B30P | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23); EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | Table 2 の免疫介在性有害事象 Grade 3以上の総数から、表の各項目と大腸炎、肝炎の Grade 3以上を差し引いた近似 |
| B30C | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23); EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | Table 2 の免疫介在性有害事象 Grade 3以上の総数から、表の各項目と大腸炎、肝炎の Grade 3以上を差し引いた近似 |
| B31P | Schmid P, et al. N Engl J Med 2022;386:556-67, Supplementary Appendix (IA4, data cutoff 2021-03-23) | Table S7（Grade 3-5） |
| B31C | Schmid P, et al. N Engl J Med 2022;386:556-67, Supplementary Appendix (IA4, data cutoff 2021-03-23) | Table S7（Grade 3-5） |
| B32P | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Any adverse event、Grade ≥3） |
| B32C | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Any adverse event、Grade ≥3） |
| B33P | Schmid P, et al. N Engl J Med 2022;386:556-67, Supplementary Appendix (IA4, data cutoff 2021-03-23) | Table S7（Grade 3-5）の Neutropenia、Neutrophil count decreased、Anemia、Febrile neutropenia、White blood cell count decreased、Alanine aminotransferase increased |
| B33C | Schmid P, et al. N Engl J Med 2022;386:556-67, Supplementary Appendix (IA4, data cutoff 2021-03-23) | Table S7（Grade 3-5）の Neutropenia、Neutrophil count decreased、Anemia、Febrile neutropenia、White blood cell count decreased、Alanine aminotransferase increased |
| E06 | Courneya KS, et al. N Engl J Med 2025;393:13-25 (CHALLENGE, CCTG CO.21). DOI 10.1056/NEJMoa2502760 | 本文 p.19（Results の Safety）、Supplementary Appendix Table S4（p.77） |
| E07 | Courneya KS, et al. N Engl J Med 2025;393:13-25 (CHALLENGE, CCTG CO.21). DOI 10.1056/NEJMoa2502760 | 本文 p.19（Results の Safety）、Supplementary Appendix Table S4（p.77） |
| E09 | Courneya KS, et al. N Engl J Med 2025;393:13-25 (CHALLENGE, CCTG CO.21). DOI 10.1056/NEJMoa2502760 | 本文 p.19（Results の Safety）、Supplementary Appendix Table S4（p.77） |
| E10 | Courneya KS, et al. N Engl J Med 2025;393:13-25 (CHALLENGE, CCTG CO.21). DOI 10.1056/NEJMoa2502760 | 本文 p.19（Results の Safety）、Supplementary Appendix Table S4（p.77） |
| F07 | Masuda N, et al. 2017. N Engl J Med 376:2147-59. DOI 10.1056/NEJMoa1612645 | Abstract, Results（TNBC サブグループ、DFS） |
| F08 | Garber JE, et al. 2026. Ann Oncol (online ahead of print). DOI 10.1016/j.annonc.2026.08.002 | Abstract, Results（第3回中間解析、追跡期間中央値6.1年、IDFS） |
| U01 | Favre-Bulle A, Huang M, Haiderali A, Bhadhuri A. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 |
| U02 | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 |
| U03 | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 |
| U04 | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 |
| U05 | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2（低下幅）; Methods（期間） |

