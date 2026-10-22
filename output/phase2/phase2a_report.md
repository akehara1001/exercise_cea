# 第2阶段 2a 报告：费用与 QALY 层（单元测试）与原负责的参数来源

生成时间：2026-10-22 14:59。由 `R/21_phase2a_report.R` 从代码输出生成。按指示本报告不含任何 ICER 或结果数值。

## 1. 状态

- 入力表 v2（`input/params/parameters_v2.xlsx`；v1 移至 `input/params/archive/`）：原负责的 30 行已填写（另有此前已填的 F07、F08）；尾崎负责的行未动，其中已填写 0 / 36 行。
- 费用与 QALY 层：`R/econ.R`（规格见 `docs/model_spec.md` 第 5 节）。尾崎的行尚未返回，故只用合成数值做单元测试（`R/test_econ.R`）；生存参数用第 1 阶段最新的校准候选值（第五轮未通过门槛，仅供测试结构）。
- 未计入（待尾崎回答或第 2 阶段后续）：S-JP 的费用（F02、F05、F06）与混合方式；运动效应参数。

## 2. 单元测试（`output/phase2/econ_unit_tests.csv`）

| 测试 | 结果 | 检查的差或比较值 |
|---|---|---|
| 费用全为 0 时费用为 0、QALY 不变（四臂） | 通过 |    0 |
| 效用全为 1（不良事件效用下降为 0）时 QALY 等于折现后的生命年（四臂） | 通过 | 3.55e-15 |
| 运动参数为中性（无效应、费用为 0）时，加运动的臂与对应的不加运动的臂完全一致 | 通过 |    0 |
| 折现率为 0 时折现后的生命年等于未折现的生命年 | 通过 |    0 |
| 只把帕博利珠单抗每次药费设为 1 日元时，费用（折现后的期望给药次数）大于 0、不超过 17，单用化疗组为 0 | 通过 |    0 |
| 只把终末期费用设为 1 日元时，费用不超过死亡比例；对象为全部死亡时不小于只计癌症死亡时 | 通过 | 0.307 |
| 远处复发一线与二线以后月额相同时，费用与一线持续期 D04 无关 | 通过 | 7.11e-15 |
| 加入运动效应（测试值 HR 0.8）后 QALY 大于单用化疗 | 通过 | 0.785 |
| 效率前沿：在答案已知的合成例中正确判定劣势与扩展劣势 | 通过 |  |
| OS 锚定开关不改变单用化疗组，减少帕博利珠单抗组的生命年 | 通过 |    0 |

共 10 项，通过 10 项。第 6、8 项的数值为比较量之差（全部死亡对癌症死亡的终末期费用；运动对单用化疗的 QALY），只用于判断方向，不是模型结果。

## 3. 原负责的参数与来源（详见 `input/params/sources_hara.md`）

| param_id | 出典 | 该当箇所 |
|---|---|---|
| A01 | 厚生労働省 薬価基準収載品目リスト（注射薬）tp20261014-01_02.xlsx（令和8年10月14日収載品目反映版、令和8年4月1日以降の薬価） | パクリタキセル、カルボプラチンの各行（後発品の最低薬価） |
| A02 | 厚生労働省 薬価基準収載品目リスト（注射薬）tp20261014-01_02.xlsx（令和8年10月14日収載品目反映版、令和8年4月1日以降の薬価） | ドキソルビシン塩酸塩（リポソーム製剤を除く）、シクロホスファミド水和物の各行 |
| A03 | 厚生労働省 薬価基準収載品目リスト（注射薬）tp20261014-01_02.xlsx（令和8年10月14日収載品目反映版、令和8年4月1日以降の薬価） | ペムブロリズマブ（遺伝子組換え）キイトルーダ点滴静注100mg |
| B21P | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hypothyroidism） |
| B22P | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hyperthyroidism） |
| B23P | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Adrenal insufficiency） |
| B24P | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hypophysitis） |
| B25P | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Pneumonitis） |
| B26P | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.101 本文（Grade 3-4 の AEOSI） |
| B27P | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.101 本文（Grade 3-4 の AEOSI） |
| B28P | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Severe skin reaction） |
| B29P | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.100 Table 5.3.5.3.3-tnbc3: 30（画像から転記） |
| B30P | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23); EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | Table 2 の免疫介在性有害事象 Grade 3以上の総数から、表の各項目と大腸炎、肝炎の Grade 3以上を差し引いた近似 |
| B31P | Schmid P, et al. N Engl J Med 2022;386:556-67, Supplementary Appendix (IA4, data cutoff 2021-03-23) | Table S7（Grade 3-5） |
| B21C | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hypothyroidism） |
| B22C | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hyperthyroidism） |
| B23C | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Adrenal insufficiency） |
| B24C | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Hypophysitis） |
| B25C | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Pneumonitis） |
| B26C | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.97 表（全Grade、画像から転記） |
| B27C | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.97 表（全Grade、画像から転記） |
| B28C | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) | Table 2（Severe skin reaction） |
| B29C | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | p.100 Table 5.3.5.3.3-tnbc3: 30（画像から転記） |
| B30C | Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23); EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23) | Table 2 の免疫介在性有害事象 Grade 3以上の総数から、表の各項目と大腸炎、肝炎の Grade 3以上を差し引いた近似 |
| B31C | Schmid P, et al. N Engl J Med 2022;386:556-67, Supplementary Appendix (IA4, data cutoff 2021-03-23) | Table S7（Grade 3-5） |
| U01 | Favre-Bulle A, Huang M, Haiderali A, Bhadhuri A. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 |
| U02 | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 |
| U03 | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 |
| U04 | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 |
| U05 | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2（低下幅）; Methods（期間） |

