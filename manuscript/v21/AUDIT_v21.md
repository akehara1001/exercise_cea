# AUDIT v21（2026-11-07）

本書は v21 の作業ログを兼ねる。v21 指示＝「exercise_cea v21: Table S12 のパネル A の見出しの語だけ」。v20 以前の経緯は archive/v20/AUDIT_v20.md。

開始時の宣言
1. 規約: WRITING_RULES.md は sha256 9cb3c7dd（2026-09-27 以降更新なし）。同日、v20 の交付前に全文を再読したものと同一。本版の変更は Online Resource 1 の見出し 1 語句だけなので、点検表は v20 の結果を引き継ぎ、本版で影響しうる項目（版、表図の付番、体裁、退行、CHEERS）を再確認した（第5節）。
2. 連鎖の段階: 初稿後の改稿。humanizer、stop-slop は使っていない。
3. 底本: v20 交付物のみ。開始時に MANIFEST_v20 の 51 項目すべて sha256 一致。交付後の manuscript/ は v21 だけ（v20 → archive）。

## 1. 最重要4項目

1. 版: 通過。底本 = v20 交付物（51/51 一致）。v21 の ESM は v20 の docx を lxml で直接編集、他は逐字節コピー。交付後 manuscript/ は v21 だけ。
2. 表と図: 通過（本文は v20 と逐字節同一で、v20 の検査結果がそのまま当てはまる: 本文 61 段落、言及 52 件、Table 1〜3、Fig. 1〜3、Table S1〜S12、Fig. S1〜S2 がすべて地の文で引用、初出順 1..n、最大番号 = 実物数）。ESM の表の並びと題も不変。
3. 文献の真偽: 通過（文献一覧は v20 と逐字節同一。v20 の実測: DOI 61/61 解決、書誌不一致 0、既知の偽陽性 2 件、DOI 無し 17 件の扱いも同じ）。
4. 文献の順序: 通過（本文、tables、ESM の引用は v20 と同一。初出順 1〜71、78/78 引用）。

## 2. 底本

- ESM_1_v20.docx（v20、sha256 先頭 8 桁 2da3ba0f）。同一式: manuscript_v20_BCRT.docx（1e0f181a）、tables_v20_BCRT.docx（53f6ecc3）、cover_letter_v20_BCRT.docx（bfc26673）、Fig1〜3.tif（c13b748e、662046bf、d7926e1e）、26_recurrence_reduction.R（4e2f2ebc）、recurrence_reduction.csv（867c0eba）。

## 3. v20 との突き合わせ（変更は指示の 1 点だけ）

| ファイル | v20 との関係 |
|---|---|
| ESM_1_v21.docx | 変更 1 単位だけ（下記）。2,597 単位中 2,596 が不変、説明できない変更 0（regress19.py）。docx の部品で違うのは word/document.xml だけ、部品の並びも同じ |
| manuscript_v21_BCRT.docx | v20 と逐字節同一（sha256 1e0f181a） |
| tables_v21_BCRT.docx | 逐字節同一（53f6ecc3） |
| cover_letter_v21_BCRT.docx | 逐字節同一（bfc26673） |
| Fig1〜3.tif | 逐字節同一 |
| 26_recurrence_reduction.R | 逐字節同一（4e2f2ebc） |
| recurrence_reduction.csv | 逐字節同一（867c0eba） |
| ESM_1_v21.pdf | Word（SaveAs2, 17）で作り直し。49 頁（v20 と同じ）。v20 の PDF と頁ごとに文字を比べ、違うのは最終頁（第 49 頁、Table S12）だけ |
| manuscript_v21_BCRT_track_from_v18.docx | 尾崎の v18 → v21 で作り直し（Word の文書比較、語単位、修訂者 Akemi Hara）。修訂 26（挿入 12、削除 14）、挿入と削除の文字列の並びが v20 の比較文書と完全一致。本文が v20 と同一なので内容も同じ（ファイルのバイトは比較の日時が入るため異なる） |

ESM の唯一の変更（Online Resource 1、Table S12 のパネル A の見出し）:
- 変更前: "A. Cumulative proportion of women without exercise, %"
- 変更後: "A. Cumulative recurrence without exercise, %"
パネル B の見出し "B. Absolute reduction with exercise, percentage points"、題、列見出し、値、脚注は不変。見出しの書式（12 pt Times New Roman、太字、数字を含まないパネル題）は不変（fmt_audit の目録の差はこの文字列だけ）。

## 4. CHEERS（Table S1）の頁

- Table S1 の Location は本文の頁を指す。本文は v20 と同一で、Word で取り直した段落ごとの頁と語数（m21_stats.json）は v20 と完全一致（ファイルの sha256 まで同一、175 段落）。
- v21 の頁組みから 28 セルを計算し直し、v21 の ESM のセルと突き合わせて不一致 0。
- ESM の PDF 上でも Table S1 は第 5 頁から（Table S2 は第 10 頁から）で v20 と同じ。第 1〜48 頁の文字は v20 の PDF と同一。

## 5. 点検（本版で影響しうる項目）

- [x] 作業樹に最新版 v21 だけ（v20 は交付時に archive へ）
- [x] 開始時の sha256 が MANIFEST_v20 と一致（51/51）
- [x] 差分の全単位が指示に対応（ESM 1 単位、他は逐字節同一）
- [x] 意図せず戻った段落 0。名指し確認: 責任著者、補足表の脚注（Table S12 の脚注を含め不変）、題名、語数（本文 3,498、抄録 249、Word で再測定し v20 と同じ）、図の解像度（逐字節同一、600 dpi）
- [x] 数値の変更なし（表の値、本文の数値とも不変）
- [x] 変更履歴とコメント 0（Word で 4 文書を確認。頁数 manuscript 31、tables 9、ESM 49、cover letter 2）
- [x] 表と図の付番と並び（不変）
- [x] 全 run 12 pt Times New Roman、黒、太字はパネル題などのラベルのみ（ESM の目録の差は見出しの文字列だけ）
- [x] 用語: Table S12 の題、パネル A、脚注が "Cumulative recurrence" で揃った
- [x] CHEERS の頁と節（第4節）
- [x] MANIFEST_v21 を作成、v20 を archive へ移動
- その他の全項目は v20 の点検表（archive/v20/AUDIT_v20.md 第8節）のとおりで、本版で対象が変わっていない。

## 6. スクリプトと出力

編集: manuscript/code/edit_esm_v21.py（v20 の sha256 を確認し、見出しが 1 セル 1 run にあることを確かめてから word/document.xml だけを書き換え）。検査: checks_v19/diff19.py、regress19.py、word_finalize19.ps1、checks_v11/word_stats.ps1、fmt_audit.py、checks_v19/word_wc19.py。出力は manuscript/code/checks_v21/out/（checks21.txt に比較文書・CHEERS・PDF の照合結果）。sha256 は MANIFEST_v21.md。
