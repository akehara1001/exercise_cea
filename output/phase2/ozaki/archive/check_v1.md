# 尾崎先生向け暫定結果資料 v1 の確認

対象：`output/phase2/ozaki/運動CEA_暫定結果_v1.docx`（`R/24_ozaki_summary.R` が生成、2026-10-25 20:22）。数値は `output/phase2/main/` の結果ファイルと `output/phase2/phase2b_report.md` から読み、モデルは実行していない。

## 1. 機械的な確認

| 項目 | 結果 | 基準 |
|---|---|---|
| Heading スタイルの段落 | 0 | 0 |
| 本文（表の外）の太字 run | 0 | 0 |
| 表の中で数字を含むセルの太字 run | 0 | 0 |
| 黒以外の文字色（w:color が 000000 か auto 以外、蛍光ペン） | 0 | 0 |
| 「・」を含む段落 | 0 | 0 |
| 「Note」で始まる段落 | 0 | 0 |
| 用紙 A4（全セクション） | はい（portrait 11906x16838、landscape 16838x11906、portrait 11906x16838、landscape 16838x11906） | すべて A4 |
| 本文中の数字のうち出典の登録がないもの | 0（なし） | 0 |

本文から読み取った数字 132 個（ラベル 11 個：KEYNOTE-522、表1、図1、想定1、想定2、想定3、表2、表3）。表の数値は flextable のセルの文字列も含む。

## 2. 本文の数字と出典の対照

結果の数値は表示の文字列と元の値（円、または比率）を並べた。設定と単位の数字（1QALY の 1、割引率の 2 など）は結果ファイル以外の出典（分析計画、model_spec）を示した。

| 表示 | 出典 | 元の値 |
|---|---|---|
| 442.6 | det_reference.csv（column = base） | 4426444.21182148 |
| −33.0 | psa_reference_summary.csv（column = base） | -330227.688151215 |
| 890.1 | psa_reference_summary.csv（column = base） | 8901031.51910191 |
| 2.156 | det_reference.csv（column = base） | 2.15634301985791 |
| 0.245 | psa_reference_summary.csv（column = base） | 0.245084978196081 |
| 4.228 | psa_reference_summary.csv（column = base） | 4.22838927384795 |
| 205.3 | det_reference.csv（column = base） | 2052755.1373126 |
| −29.8 | psa_reference_summary.csv（column = base） | -297708.52576844 |
| 1,902.3 | psa_reference_summary.csv（column = base） | 19023489.085204 |
| 83.1 | psa_reference_summary.csv（column = base） | 0.831 |
| 90.8 | psa_reference_summary.csv（column = base） | 0.908 |
| 410.2 | det_reference.csv（column = kext） | 4101859.38763142 |
| −74.4 | psa_reference_summary.csv（column = kext） | -744288.681675664 |
| 855.8 | psa_reference_summary.csv（column = kext） | 8558249.78597497 |
| 2.137 | det_reference.csv（column = kext） | 2.13682523039882 |
| 0.230 | psa_reference_summary.csv（column = kext） | 0.22966161874911 |
| 4.207 | psa_reference_summary.csv（column = kext） | 4.20734642632207 |
| 192.0 | det_reference.csv（column = kext） | 1919604.52791258 |
| −38.9 | psa_reference_summary.csv（column = kext） | -388912.100541957 |
| 1,846.4 | psa_reference_summary.csv（column = kext） | 18464125.2948277 |
| 84.4 | psa_reference_summary.csv（column = kext） | 0.844 |
| 91.1 | psa_reference_summary.csv（column = kext） | 0.911 |
| 499.0 | scenario_reference.csv（scenario = sjp） | 4989524.20858509 |
| 1.639 | scenario_reference.csv（scenario = sjp） | 1.63888097707382 |
| 304.4 | scenario_reference.csv（scenario = sjp） | 3044470.14663246 |
| 1 | 1QALY（単位の 1） | 1 |
| 500 | 判断の基準 λ = 500万円/QALY（docs/analysis_plan_phase2.md 第 2 節、phase2b_report.md） | 500 |
| 750 | 参照の基準 λ = 750万円/QALY（同上） | 750 |
| 0.70 | HR の格点（det_caps.csv の x） | 0.7 |
| 0.75 | HR の格点（det_caps.csv の x） | 0.75 |
| 0.80 | HR の格点（det_caps.csv の x） | 0.8 |
| 0.85 | HR の格点（det_caps.csv の x） | 0.85 |
| 0.90 | HR の格点（det_caps.csv の x） | 0.9 |
| 0.95 | HR の格点（det_caps.csv の x） | 0.95 |
| 1.00 | HR の格点（det_caps.csv の x） | 1 |
| 559.6 | det_caps.csv（main, base, hr0 = 0.70, cap_500） | 5595776.10847557 |
| 454.5 | psa_caps_summary.csv（main, base, hr0 = 0.70, cap500_lo） | 4545499.30391027 |
| 625.6 | psa_caps_summary.csv（main, base, hr0 = 0.70, cap500_hi） | 6256345.34624927 |
| 462.3 | det_caps.csv（main, base, hr0 = 0.75, cap_500） | 4622953.57814769 |
| 375.8 | psa_caps_summary.csv（main, base, hr0 = 0.75, cap500_lo） | 3758428.54595357 |
| 516.4 | psa_caps_summary.csv（main, base, hr0 = 0.75, cap500_hi） | 5163753.85987483 |
| 366.7 | det_caps.csv（main, base, hr0 = 0.80, cap_500） | 3666609.71795855 |
| 298.3 | psa_caps_summary.csv（main, base, hr0 = 0.80, cap500_lo） | 2983165.14833969 |
| 409.2 | psa_caps_summary.csv（main, base, hr0 = 0.80, cap500_hi） | 4091635.99176277 |
| 272.6 | det_caps.csv（main, base, hr0 = 0.85, cap_500） | 2726400.8870362 |
| 222.3 | psa_caps_summary.csv（main, base, hr0 = 0.85, cap500_lo） | 2222889.94969549 |
| 304.0 | psa_caps_summary.csv（main, base, hr0 = 0.85, cap500_hi） | 3039571.6727006 |
| 180.2 | det_caps.csv（main, base, hr0 = 0.90, cap_500） | 1801990.91184234 |
| 147.1 | psa_caps_summary.csv（main, base, hr0 = 0.90, cap500_lo） | 1471094.57758093 |
| 200.7 | psa_caps_summary.csv（main, base, hr0 = 0.90, cap500_hi） | 2007047.17040087 |
| 89.3 | det_caps.csv（main, base, hr0 = 0.95, cap_500） | 893050.922566834 |
| 73.0 | psa_caps_summary.csv（main, base, hr0 = 0.95, cap500_lo） | 730429.179444587 |
| 99.4 | psa_caps_summary.csv（main, base, hr0 = 0.95, cap500_hi） | 993777.720192172 |
| −0.07 | det_caps.csv（main, base, hr0 = 1.00, cap_500） | -740.806878935912 |
| −0.15 | psa_caps_summary.csv（main, base, hr0 = 1.00, cap500_lo） | -1542.24790409717 |
| −0.02 | psa_caps_summary.csv（main, base, hr0 = 1.00, cap500_hi） | -220.922133505826 |
| 710.7 | det_caps.csv（secondary, base, hr0 = 0.70, cap_500） | 7106810.66807256 |
| 592.3 | psa_caps_summary.csv（secondary, base, hr0 = 0.70, cap500_lo） | 5923067.31247807 |
| 786.9 | psa_caps_summary.csv（secondary, base, hr0 = 0.70, cap500_hi） | 7868859.01713853 |
| 586.0 | det_caps.csv（secondary, base, hr0 = 0.75, cap_500） | 5860005.5604669 |
| 489.5 | psa_caps_summary.csv（secondary, base, hr0 = 0.75, cap500_lo） | 4894905.22185895 |
| 647.3 | psa_caps_summary.csv（secondary, base, hr0 = 0.75, cap500_hi） | 6473355.81223986 |
| 463.9 | det_caps.csv（secondary, base, hr0 = 0.80, cap_500） | 4638912.2827981 |
| 387.9 | psa_caps_summary.csv（secondary, base, hr0 = 0.80, cap500_lo） | 3879138.85297923 |
| 511.0 | psa_caps_summary.csv（secondary, base, hr0 = 0.80, cap500_hi） | 5109701.34161143 |
| 344.3 | det_caps.csv（secondary, base, hr0 = 0.85, cap_500） | 3442898.84929941 |
| 288.1 | psa_caps_summary.csv（secondary, base, hr0 = 0.85, cap500_lo） | 2880585.1480882 |
| 378.5 | psa_caps_summary.csv（secondary, base, hr0 = 0.85, cap500_hi） | 3785042.45783867 |
| 227.1 | det_caps.csv（secondary, base, hr0 = 0.90, cap_500） | 2271349.53861421 |
| 190.2 | psa_caps_summary.csv（secondary, base, hr0 = 0.90, cap500_lo） | 1902118.14956824 |
| 249.2 | psa_caps_summary.csv（secondary, base, hr0 = 0.90, cap500_hi） | 2492170.50682024 |
| 112.4 | det_caps.csv（secondary, base, hr0 = 0.95, cap_500） | 1123664.47042199 |
| 94.3 | psa_caps_summary.csv（secondary, base, hr0 = 0.95, cap500_lo） | 943241.898366675 |
| 123.2 | psa_caps_summary.csv（secondary, base, hr0 = 0.95, cap500_hi） | 1232205.07904342 |
| −0.07 | det_caps.csv（secondary, base, hr0 = 1.00, cap_500） | -740.806878934049 |
| −0.15 | psa_caps_summary.csv（secondary, base, hr0 = 1.00, cap500_lo） | -1542.24790409722 |
| −0.02 | psa_caps_summary.csv（secondary, base, hr0 = 1.00, cap500_hi） | -220.922133503963 |
| 272.6 | scenario_caps.csv（scenario = base, main, hr0 = 0.85, cap_500） | 2726400.8870362 |
| 177.2 | scenario_caps.csv（scenario = path_a_s1, main, hr0 = 0.85, cap_500） | 1772364.98201127 |
| 340.4 | scenario_caps.csv（scenario = path_a_s2, main, hr0 = 0.85, cap_500） | 3403938.77458484 |
| 223.9 | scenario_caps.csv（scenario = continue_s1, main, hr0 = 0.85, cap_500） | 2238868.41647028 |
| 344.3 | scenario_caps.csv（scenario = base, secondary, hr0 = 0.85, cap_500） | 3442898.84929941 |
| 227.9 | scenario_caps.csv（scenario = path_a_s1, secondary, hr0 = 0.85, cap_500） | 2279438.16744623 |
| 442.0 | scenario_caps.csv（scenario = path_a_s2, secondary, hr0 = 0.85, cap_500） | 4419672.68859316 |
| 295.4 | scenario_caps.csv（scenario = continue_s1, secondary, hr0 = 0.85, cap_500） | 2954336.80323356 |
| 5 | 効果が続く期間 5 年（docs/analysis_plan_phase2.md 第 3 節） | 5 |
| 0.85 | HR 0.85（表 3 の条件、analysis_plan 第 6 節） | 0.85 |
| 0.425 | det_yardstick.csv（axis = hr0, root） | 0.424844086027943 |
| 58 | 1 − det_yardstick.csv の hr0 root（57.5% を四捨五入） | 57.5155913972057 |
| 35.9 | det_yardstick.csv（axis = pcr, root × 100） | 35.8556422277975 |
| 4 | 比較した群の数（4 群） | 4 |
| 2 | 割引率 年 2%（docs/model_spec.md 第 5 節） | 2 |
| 9 | 【要確認】の 9 行（phase2b_report.md 冒頭と第 6 節） | 9 |
| 1 | phase2b_report.md 第 6 節：主比較の上限への影響の最大が 0.0 万円（1 万円未満） | 1 |
| 2.5 | PSA の 2.5 パーセンタイル（psa_reference_summary.csv、phase2b_report.md） | 2.5 |
| 97.5 | PSA の 97.5 パーセンタイル（同上） | 97.5 |
| 3 | CHALLENGE の介入期間 3 年（docs/analysis_plan_phase2.md 第 3 節） | 3 |
| 0.72 | CHALLENGE のハザード比（docs/analysis_plan_phase2.md 第 3 節） | 0.72 |
| 0.95 | 図 1B の拡大範囲 | 0.95 |
| 1.00 | HR の上端（効果なし） | 1.00 |
| 2 | 小数第 2 位（表示の桁） | 2 |
| 24.0 | phase2b_report.md 第 1.7 節（E01 の費用、万円） | 24 |
| 0.948 | phase2b_report.md 第 1.7 節（E01、主比較の基準の欄） | 0.948 |
| 19.2 | phase2b_report.md 第 1.7 節（E02 の費用、万円） | 19.2 |
| 0.958 | phase2b_report.md 第 1.7 節（E02、主比較の基準の欄） | 0.958 |
| 1.1 | phase2b_report.md 第 1.7 節（E03 の費用、万円） | 1.1 |
| 0.997 | phase2b_report.md 第 1.7 節（E03、主比較の基準の欄） | 0.997 |
| 1 | 半減期 1 年（docs/analysis_plan_phase2.md 第 3 節） | 1 |
| 1 | 術後の指導 月 1 回（入力表 E04 の備考） | 1 |
| 0.70 | HR の主軸の下端（analysis_plan 第 3 節） | 0.70 |
| 10 | pCR の主軸の上端 10 ポイント（analysis_plan 第 3 節） | 10 |

## 3. 図1の中の数字（画像のため本文からは読み取れない）

- 目盛：0.70〜1.00（0.05 間隔）、0.95〜1.00（0.01 間隔）
- 想定1 24.0万円（phase2b_report.md 第 1.7 節）
- 想定2 19.2万円（phase2b_report.md 第 1.7 節）
- 想定3 1.1万円（phase2b_report.md 第 1.7 節）
- HR 0.72（参照線）
- 線と帯は det_caps.csv（cap_500）と psa_caps_summary.csv（cap500_lo、cap500_hi）を R でそのまま描いた（`fig1_cap.png`）。

## 4. 指示からの変更

- 同じ物差しの「再発のリスクを約 57% 下げる」は、1 − 0.4248 = 57.5% を四捨五入して約 58% とした。
- 「日本の術後治療を入れた場合」は確定的な計算だけで、不確かさの範囲と確率はない（－、表1の脚注‡）。
- 表2の HR 1.00 の行は値が 0 に近いため小数第 2 位まで示した（脚注✳）。
