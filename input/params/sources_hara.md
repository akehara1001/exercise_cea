# 原负责参数的来源（入力表 v2：A01 至 A03、B21P 至 B31C、U01 至 U05）

由 `R/py/11_fill_hara_params.py` 从下列文件读取后写入 `input/params/parameters_v2.xlsx`，本文件同时生成；数值不手抄。中间结果在 `data/params_hara/`。

## A. 药价（A01 至 A03）

- 薬価：厚生劳动省「薬価基準収載品目リスト及び後発医薬品に関する情報について」注射药 `tp20261014-01_02.xlsx`（https://www.mhlw.go.jp/topics/2026/04/xls/tp20261014-01_02.xlsx，令和8年4月1日适用页面上 10月14日收载品目反映版，2026-10-22 下载，sha256 161d801b4c94314c…）。令和8年度的薬価，年度内收载的新品目已反映，既有品目的薬价在年度内不变。
- 规则：有后发品的药物，基准取后发品（表中「後発品」或「★」）的最低薬価，先发品薬価作为情景；没有后发品的药物用收载品目的薬价。每次给药取覆盖剂量的最便宜小瓶组合（向上取整、不分装）。
- 排除：ドキシル（脂质体多柔比星）与アブラキサン（白蛋白结合型紫杉醇），属不同制剂。
- 体表面积 1.5552 m2：Du Bois 式，令和6年国民健康・栄养调查第2部第14表（全国补正值）女性 40 至 49 岁的平均身高 158.2 cm、平均体重 55.4 kg（e-Stat statInfId 000040502147，`NHNS_R6_2024_table14_statInfId000040502147.xlsx` 工作表 14 的 I37、L37）。参考：C2H 公的分析 C2H2409（サシツズマブ ゴビテカン，2026-02-06）的体表面积设定为 1.56 m2（p.42 表4-2-1，`sources_bsa/C2H2409_Report_sacituzumab_govitecan_v1.0_20260206.pdf`）。
- 卡铂：Calvert 式 剂量 = AUC × (CrCl + 25)；CrCl 96.0 mL/min 为 Cockcroft-Gault（49 岁、体重同上、女性 × 0.85），血清肌酐 0.62 mg/dL 取 JCCLS 共用基準範囲（2022-10-01 修订）表4 女性中间值（n = 2899，下限 0.46、上限 0.79；`sources_bsa/JCCLS_kyoyo_kijyunhani_20221001.pdf` p.21，从表格图像读取）。情景：酶法肌酐加 0.2 mg/dL 的惯例，CrCl 72.6 mL/min（此惯例本次未核对出处）。
- 方案：KEYNOTE-522（PMDA 审查报告 2022-08-10 表14，`sources_ae/PMDA_keytruda_review_20220810.pdf` p.30）：紫杉醇 80 mg/m2 每周 12 次；卡铂 AUC 1.5 每周 12 次或 AUC 5 每 3 周 4 次；AC = 多柔比星 60 mg/m2 + 环磷酰胺 600 mg/m2，EC = 表柔比星 90 mg/m2 + 环磷酰胺 600 mg/m2，每 3 周 4 次；帕博利珠单抗 200 mg 每 3 周（术前 8 次、术后 9 次）。基准按 KEYNOTE-522 的实际给药（2024 年补充材料 Table S3）：卡铂每周（帕博利珠单抗组 444 例、安慰剂组 220 例）多于每 3 周（334、167 例）；多柔比星（488、247 例）多于表柔比星（238、122 例）。

| 疗程 | 薬価 | 总额（日元） |
|---|---|---|
| A01_base_CBDCA_weekly | 基准 | 113,736 |
| A01_base_CBDCA_weekly | 先发品（情景） | 121,464 |
| A01_CBDCA_q3w | 基准 | 105,004 |
| A01_CBDCA_q3w | 先发品（情景） | 117,776 |
| A01_CBDCA_weekly_Cr+0.2 | 基准 | 97,572 |
| A01_CBDCA_weekly_Cr+0.2 | 先发品（情景） | 106,860 |
| A02_base_AC | 基准 | 33,496 |
| A02_base_AC | 先发品（情景） | 61,680 |
| A02_EC | 基准 | 86,224 |
| A02_EC | 先发品（情景） | 86,224 |
| A03_pembro_200mg | 基准 | 398,924 |
| A03_pembro_200mg | 先发品（情景） | 398,924 |

所用的小瓶（基准与情景中被选中的品目）：

| 药物 | 规格 | 品名 | 区分 | 薬価（日元） | 经过措置 |
|---|---|---|---|---|---|
| paclitaxel | 30mg5mL1瓶 | タキソール注射液30mg | originator | 1413 |  |
| paclitaxel | 30mg5mL1瓶 | パクリタキセル注射液30mg「NP」 | generic（後発品） | 1368 | R9.3.31まで |
| paclitaxel | 100mg16.7mL1瓶 | タキソール注射液100mg | originator | 4491 |  |
| paclitaxel | 100mg16.7mL1瓶 | パクリタキセル注100mg/16.7mL「NK」 | generic（★） | 4580 |  |
| carboplatin | 50mg5mL1瓶 | パラプラチン注射液50mg | originator | 1217 |  |
| carboplatin | 50mg5mL1瓶 | カルボプラチン注射液50mg「NK」 | generic（★） | 1347 |  |
| carboplatin | 150mg15mL1瓶 | カルボプラチン点滴静注液150mg「サンド」 | generic（後発品） | 2183 |  |
| carboplatin | 150mg15mL1瓶 | パラプラチン注射液150mg | originator | 3001 |  |
| carboplatin | 450mg45mL1瓶 | パラプラチン注射液450mg | originator | 7514 |  |
| carboplatin | 450mg45mL1瓶 | カルボプラチン注射液450mg「日医工」 | generic（後発品） | 4877 |  |
| doxorubicin | 50mg25mL1瓶 | ドキソルビシン塩酸塩注射液50mg「サンド」 | generic（後発品） | 2687 | R9.3.31まで |
| doxorubicin | 50mg1瓶 | アドリアシン注用50 | originator | 6210 |  |
| epirubicin | 10mg1瓶 | エピルビシン塩酸塩注射用10mg「NK」 | generic（後発品） | 1375 |  |
| epirubicin | 50mg1瓶 | エピルビシン塩酸塩注射用50mg「NK」 | generic（後発品） | 6528 |  |
| cyclophosphamide | 500mg1瓶 | 注射用エンドキサン500mg | only | 1500 |  |
| pembrolizumab | 100mg4mL1瓶 | キイトルーダ点滴静注100mg | originator | 199462 |  |

注：标有经过措置（例如「R9.3.31まで」）的品目将从薬価基準删除，令和8年度内仍为收载品目，故计入最低薬価的比较。每次给药的小瓶组合见 `data/params_hara/drug_costs.csv`，全部候选品目见 `drug_vials.csv`。

## B. 不良事件发生率（B21P 至 B31C）

- 规则：内分泌类免疫相关不良事件（甲状腺功能减退、甲状腺功能亢进、肾上腺功能不全、垂体炎、1 型糖尿病）用全部等级，其余用 3 级以上。分母为 as-treated 人群（帕博利珠单抗组 783 例，安慰剂组 389 例）。截点统一为 IA4（2021-03-23）；2024 年正文 Table 2（IA7）中同名项目的例数与 IA4 相同。
- 主要来源：Schmid P, et al. N Engl J Med 2022;386:556-67 (KEYNOTE-522, IA4, data cutoff 2021-03-23) Table 2（正文 p.564）；发热性中性粒细胞减少：Schmid P, et al. N Engl J Med 2022;386:556-67, Supplementary Appendix (IA4, data cutoff 2021-03-23) Table S7（p.27）。
- 表中没有的项目（大肠炎、肝炎、1 型糖尿病）：EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 (EMA/257879/2022; KEYNOTE-522, database cutoff 2021-03-23)（`sources_ae/EMA_keytruda_II0110_assessment.pdf`）。p.97 至 p.100 的 Table 5.3.5.3.3-tnbc3: 30 为图像，全部等级的例数从图像转记（`sources_ae/ema_aeosi_transcribed.csv`）；3 级以上的例数取 p.101 正文（只给出帕博利珠单抗组）。安慰剂组的大肠炎、肝炎 3 级以上未报告，基本值取 0，上限取全部等级的比例。
- 「その他の重篤なもの」（B30）：Table 2 免疫介导不良事件 3 级以上的总人数，减去表中各项目与大肠炎、肝炎的 3 级以上人数。总数按患者计、各项相加会有重复，故为近似；定义需与尾崎的 B10（每件费用）一致，待确认。
- 下限与上限：Clopper-Pearson 95% 置信区间。

| param_id | 项目 | 等级 | 例数 / 分母 | 发生率 | 来源 | 位置 | 备注 |
|---|---|---|---|---|---|---|---|
| B21P | 甲状腺機能低下症 | 全Grade | 118/783 | 0.1507 | Schmid P, et al. N Engl J Med 2022;386:556-67 | Table 2（Hypothyroidism） | 甲状腺炎（全Grade 16例）は含めない |
| B22P | 甲状腺機能亢進症 | 全Grade | 41/783 | 0.0524 | Schmid P, et al. N Engl J Med 2022;386:556-67 | Table 2（Hyperthyroidism） |  |
| B23P | 副腎不全 | 全Grade | 20/783 | 0.0255 | Schmid P, et al. N Engl J Med 2022;386:556-67 | Table 2（Adrenal insufficiency） |  |
| B24P | 下垂体炎 | 全Grade | 15/783 | 0.0192 | Schmid P, et al. N Engl J Med 2022;386:556-67 | Table 2（Hypophysitis） |  |
| B25P | 肺臓炎 | Grade 3以上 | 7/783 | 0.0089 | Schmid P, et al. N Engl J Med 2022;386:556-67 | Table 2（Pneumonitis） |  |
| B26P | 大腸炎 | Grade 3以上 | 6/783 | 0.0077 | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 | p.101 本文（Grade 3-4 の AEOSI） | 全Grade は 13例（p.97 表、画像から転記） |
| B27P | 肝炎 | Grade 3以上 | 9/783 | 0.0115 | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 | p.101 本文（Grade 3-4 の AEOSI） | 全Grade は 11例（p.97 表、画像から転記） |
| B28P | 重度の皮膚障害 | Grade 3以上 | 37/783 | 0.0473 | Schmid P, et al. N Engl J Med 2022;386:556-67 | Table 2（Severe skin reaction） |  |
| B29P | 1型糖尿病 | 全Grade | 4/783 | 0.0051 | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 | p.100 Table 5.3.5.3.3-tnbc3: 30（画像から転記） |  |
| B30P | その他の重篤なもの | Grade 3以上 | 16/783 | 0.0204 | Schmid P, et al. N Engl J Med 2022;386:556-67 | Table 2 の免疫介在性有害事象 Grade 3以上の総数から、表の各項目と大腸炎、肝炎の Grade 3以上を差し引いた近似 | 患者単位の重複があるため近似値。B10 の定義と合わせて尾崎先生に確認 |
| B31P | 発熱性好中球減少症 | Grade 3以上 | 144/783 | 0.1839 | Schmid P, et al. N Engl J Med 2022;386:556-67, Supplementary Appendix | Table S7（Grade 3-5） |  |
| B21C | 甲状腺機能低下症 | 全Grade | 22/389 | 0.0566 | Schmid P, et al. N Engl J Med 2022;386:556-67 | Table 2（Hypothyroidism） | 甲状腺炎（全Grade 5例）は含めない |
| B22C | 甲状腺機能亢進症 | 全Grade | 7/389 | 0.0180 | Schmid P, et al. N Engl J Med 2022;386:556-67 | Table 2（Hyperthyroidism） |  |
| B23C | 副腎不全 | 全Grade | 0/389 | 0.0000 | Schmid P, et al. N Engl J Med 2022;386:556-67 | Table 2（Adrenal insufficiency） |  |
| B24C | 下垂体炎 | 全Grade | 1/389 | 0.0026 | Schmid P, et al. N Engl J Med 2022;386:556-67 | Table 2（Hypophysitis） |  |
| B25C | 肺臓炎 | Grade 3以上 | 2/389 | 0.0051 | Schmid P, et al. N Engl J Med 2022;386:556-67 | Table 2（Pneumonitis） |  |
| B26C | 大腸炎 | Grade 3以上 | 0/389 | 0.0000 | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 | p.97 表（全Grade、画像から転記） | プラセボ群の Grade 3以上は未報告。全Grade 3例を上限とし、基本値は0 |
| B27C | 肝炎 | Grade 3以上 | 0/389 | 0.0000 | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 | p.97 表（全Grade、画像から転記） | プラセボ群の Grade 3以上は未報告。全Grade 3例を上限とし、基本値は0 |
| B28C | 重度の皮膚障害 | Grade 3以上 | 1/389 | 0.0026 | Schmid P, et al. N Engl J Med 2022;386:556-67 | Table 2（Severe skin reaction） |  |
| B29C | 1型糖尿病 | 全Grade | 0/389 | 0.0000 | EMA. Keytruda assessment report EMEA/H/C/003820/II/0110 | p.100 Table 5.3.5.3.3-tnbc3: 30（画像から転記） |  |
| B30C | その他の重篤なもの | Grade 3以上 | 1/389 | 0.0026 | Schmid P, et al. N Engl J Med 2022;386:556-67 | Table 2 の免疫介在性有害事象 Grade 3以上の総数から、表の各項目と大腸炎、肝炎の Grade 3以上を差し引いた近似 | 患者単位の重複があるため近似値。B10 の定義と合わせて尾崎先生に確認 |
| B31C | 発熱性好中球減少症 | Grade 3以上 | 63/389 | 0.1620 | Schmid P, et al. N Engl J Med 2022;386:556-67, Supplementary Appendix | Table S7（Grade 3-5） |  |

## U. 效用值（U01 至 U05）

优先顺序：KEYNOTE-522 的 EQ-5D 效用值 → 日本人群研究（日本的价值组）→ 其他费用效用分析。

| param_id | 值 | 标准误 | 下限 | 上限 | 层级 | 来源 | 位置 | 原文 | 文件 |
|---|---|---|---|---|---|---|---|---|---|
| U01 | 0.889 | 0.004 | 0.8812 | 0.8968 | 1 KEYNOTE-522 EQ-5D-5L（ドイツの価値セット） | Favre-Bulle A, Huang M, Haiderali A, Bhadhuri A. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 | Event-free on treatment / 0.889 (0.004) / KEYNOTE-522 (cut-off date: 23 March 2021) | sources_utility/FavreBulle2024_PharmacoeconOpen_suppl_MOESM1.docx |
| U02 | 0.887 | 0.005 | 0.8772 | 0.8968 | 1 KEYNOTE-522 EQ-5D-5L（ドイツの価値セット） | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 | Event-free off treatment / 0.887 (0.005) | sources_utility/FavreBulle2024_PharmacoeconOpen_suppl_MOESM1.docx |
| U03 | 0.830 | 0.022 | 0.7869 | 0.8731 | 1 KEYNOTE-522 EQ-5D-5L（ドイツの価値セット） | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 | Locoregional recurrence / 0.830 (0.022) | sources_utility/FavreBulle2024_PharmacoeconOpen_suppl_MOESM1.docx |
| U04 | 0.735 | 0.018 | 0.6997 | 0.7703 | 1 KEYNOTE-522 EQ-5D-5L（ドイツの価値セット） | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2 | Distant metastasis / 0.735 (0.0180) | sources_utility/FavreBulle2024_PharmacoeconOpen_suppl_MOESM1.docx |
| U05 | 0.022 | 0.0189 | 0 | 0.059 | 1 KEYNOTE-522 EQ-5D-5L（ドイツの価値セット） | Favre-Bulle A, et al. Pharmacoecon Open 2024;8(1):91-101. DOI 10.1007/s41669-023-00445-8, PMID 37999854 | Supplementary Table S2（低下幅）; Methods（期間） | Grade 3+ AE utility decrement / -0.022 (0.0189); A mean duration of 12.5 weeks was applied to all grade 3+ AEs based on pooled data from the KEYNOTE-522 trial | sources_utility/FavreBulle2024_PharmacoeconOpen_suppl_MOESM1.docx; sources_utility/FavreBulle2024_PharmacoeconOpen_PMC10781656.xml |

下限与上限由本脚本按 基本值 ± 1.96 × 标准误 计算（来源只给出标准误）；U05 的下限截于 0。U05 的持续期间：12.5 周（同一来源）。
检索范围与未采用的来源：KEYNOTE-522 的 HRQoL 论文（Dent 2024 JNCI，PMID 38913881）只报告 EQ-5D VAS；NICE TA851 的效用值全部涂黑；CADTH PC0279 的药物经济学评估页面无法取得（reCAPTCHA、403），未绕过；日本没有帕博利珠单抗的 C2H 费用效果评价。日本人群（日本的价值组）的数值只作对照：Iwatani 2021 Curr Oncol（PMID 34677274）原发乳腺癌 0.89 至 0.90；Shiroiwa 2017 BMC Cancer（PMID 29149882）转移乳腺癌一线 0.742 至 0.764；局部区域复发没有日本人的数值。保存的文件在 `input/params/sources_utility/` 与 `input/params/pubmed/`。

选择理由与说明：

- U01：KEYNOTE-522 の EQ-5D（データカットオフ 2021-03-23、両群併合）。日本の価値セットを KEYNOTE-522 に適用した報告はなく、標準誤差を示した唯一の公表値（スイスの費用効用分析、ドイツの価値セット）を基本とした。シナリオ：米国の価値セット 0.836（Huang 2023 Adv Ther、Table 1）、英国 0.859（Kwong 2024 Oncol Ther、Table 2）、豪州 PBAC 0.775（PSD 2023年3月、Table 10）。日本人の参考値：原発乳癌 0.89〜0.90（Iwatani 2021 Curr Oncol、日本の価値セット）。NICE の ERG によれば治療中の値は Grade 3 以上の有害事象のない患者のもの（U05 との二重計上を避けるため）。下限と上限は基本値 ± 1.96 × 標準誤差。
- U02：出典は U01 と同じ。シナリオ：米国 0.842、英国 0.862、豪州 0.785。日本人の参考値：原発乳癌 0.89〜0.90（Iwatani 2021）。下限と上限は基本値 ± 1.96 × 標準誤差。
- U03：出典は U01 と同じ。シナリオ：米国 0.768、英国 0.800、豪州 0.693。局所領域再発の日本人の値は見つからなかった。下限と上限は基本値 ± 1.96 × 標準誤差。
- U04：出典は U01 と同じ。モデルでは術前進展の状態にも用いる。シナリオ：米国 0.639、英国 0.697、豪州 0.552。日本人の参考値：転移乳癌一次治療 0.742〜0.764（Shiroiwa 2017 BMC Cancer、SELECT BC、日本の価値セット）。NICE の ERG は KEYNOTE-522 で転移後の回答が少ないことを指摘。下限と上限は基本値 ± 1.96 × 標準誤差。
- U05：Grade 3 以上の有害事象 1 件あたりの低下幅（表では -0.022）。期間 12.5 週（同論文、KEYNOTE-522 の併合データ。香港の分析も 12.53 週）。シナリオ：米国 0.034、英国 0.025、豪州 0.039。下限は 0 で切り、上限は基本値 + 1.96 × 標準誤差。各国の分析は Grade 3 以上の有害事象全体の発現（件数）に掛けており、本モデルの B25 から B28、B30、B31 の合計に掛ける仕様とは対象が異なる（要確認）。

## 待确认事项

- B30「その他の重篤なもの」的定义需与尾崎的 B10（每件费用）一致；现值为近似（见 B 节）。
- 安慰剂组大肠炎、肝炎的 3 级以上例数未报告，基本值取 0（上限为全部等级的比例）。
- U05：来源的分析把效用下降乘以全部 3 级以上不良事件的发生（件数），本模型按规格乘以 B25 至 B28、B30、B31 的发生率之和，两者对象不同。
- 卡铂的情景「酶法肌酐加 0.2 mg/dL」的出处本次未核对。
- 效用值用的是外国的价值组（基准为德国）；没有把日本的价值组用于 KEYNOTE-522 的数值。
