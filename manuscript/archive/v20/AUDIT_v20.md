# AUDIT v20（2026-11-07）

本書は v20 の作業ログを兼ねる（規約第12節の順）。v20 指示＝「exercise_cea v20: v19 の仕上げ（脚注の体裁、英文の差し替え、報告に数値と文面を貼る）」。v19 以前の経緯は archive/v19/AUDIT_v19.md。

開始時の宣言
1. 規約: WRITING_RULES.md は 2026-09-27 以降更新なし（sha256 9cb3c7dd、513 行）。同日のセッション内で全文を 2 回読んだものと同一であることを確認して開始し、改稿後に全文を再読した（点検表は第8節）。
2. 連鎖の段階: 初稿後の改稿（第1節の 6 に相当）。指示の英文をそのまま入れる版で、humanizer と stop-slop は使っていない。ARS は第1.6節の範囲（docx 直接編集）。
3. 底本: v19 交付物のみ（第2節）。作業中の manuscript/ は v19 と v20、交付後は v20 だけ（v19 → archive）。

## 1. 最重要4項目

1. 版: 通過。底本 = v19 交付物（MANIFEST_v19 の 68 項目すべて sha256 一致を開始時に確認）。全編集は v19 docx の lxml 直接編集。交付後 manuscript/ は v20 だけ。
2. 表と図: 通過。本文 61 段落、言及 52 件（範囲展開後）。Table 1〜3、Fig. 1〜3、Table S1〜S12、Fig. S1〜S2 の全部が地の文で番号付きで引用、各系列の初出順 1..n、最大番号 = 実物数（3、3、12、2）。個別引用でも全番号あり（S4 = Results、S12 = Discussion 第3段落）。
3. 文献の真偽: 通過。DOI 61/61 解決（302）、著者・年の不一致 0、巻頁フラグ 10、58 は既知の偽陽性。DOI 無し 17 件: 15 件 200、第 8 条の原網址 404（存档 2 件は v19 で 200 を確認済み）、第 52 条は書籍。出力は v19 と逐字同（refcheck_v20.json の sha256 = v19 = v17）。
4. 文献の順序: 通過。初出順 1〜71 欠けなし（62 群、112 番号）。manuscript、tables、ESM の引用列は v19 と完全一致。78/78 引用あり。

## 2. 底本と裁定

- 底本: manuscript_v19_BCRT.docx（v19、sha256 先頭 8 桁 c40f9ed6）。同一式: tables_v19_BCRT.docx（3fc3f456）、ESM_1_v19.docx（9ef39de9）、cover_letter_v19_BCRT.docx（c9e56b22）、Fig1〜3.tif（c13b748e、662046bf、d7926e1e）、26_recurrence_reduction.R（4e2f2ebc）、recurrence_reduction.csv（867c0eba）。
- 指示第0節の裁定: (1) Table 3 の新脚注の記号は e、(2) 表 docx 内の引用は "(Table S12 (Online Resource 1))"、(3) S8・S11 の定義句の削除はそのまま、(4) 11 月 1 日の薬価改定は反映しない（価格日 2026-10-14 のまま）、(5) 公開フォルダは push しない。本版はこれに従った（公開フォルダは変更なし、HEAD e23e167 のまま）。

## 3. 投稿仕様と語数

- BCRT、抄録上限 250、本文上限 3,500（Word の数え方、v19 と同じ）。
- 実測（Word ComputeStatistics、checks_v19/word_wc19.py）: 抄録 249、本文 3,498（見出し込み 3,539）。節別: Introduction 588、Methods 1,402、Results 609、Discussion 459、Implications 176、Limitations 211、Conclusion 53。題名ページの Word count 行を "main text 3,498" に更新（指示の見込みどおり。v18 の記載と同じ数になったため、v18 からの比較文書ではこの行に修訂が出ない）。31 頁。

## 4. 本版で変えた箇所（変更前後は checks_v20/out/diff_*.txt、退行検査は r20_*.txt）

### 4.1 manuscript（175 段、不変 173、変更 2）
| 指示 | 位置 | 変更 |
|---|---|---|
| 1 | Discussion 第3段落 | "by about 0.14 percentage points" → "by 0.14 percentage points"（0.14 は CSV から読み、v19 の値と一致を確認） |
| 4 | 題名ページ Word count 行 | "3,499" → "3,498"（Word 実測） |
変更後の文: "If exercise reduces recurrence at all, even a small effect would make a structured program cost-effective: the fee-schedule-based program became cost-effective once it lowered the recurrence hazard by 1.1%, which cut distant recurrence at 7 years by 0.14 percentage points (Table S12)."

### 4.2 tables（Table 3 のみ。Table 1、2 不変）
- 記号 ✳ → e（指示 0(1)）。置き場所は a〜d と同じ流儀（a〜d は注記対象の語の直後: "Recurrence HR^b (reduction …)"、"Medical costs avoided^c equal …"）で、HR の値の直後（指示 1）: "0.989^e (1.1)"、"0.991^e (0.9)"、"0.958^e (4.2)"、"0.966^e (3.4)"、"Base case, recurrence HR 0.85^e"（パネル B と C の 2 行、値が行ラベルの末尾）。v19 ではセル末尾（"(1.1)" の後）だった。規約 7.2 はセル固有の脚注記号をセル末尾に置くとするが、指示（値の右上、a〜d と同じ流儀）に従った。
- 脚注 e: 指示の英文（"about" なし、"(Table S12 (Online Resource 1))"）。記号は上付き e、本文は a〜d と同じく記号の直後から始まる（指示の "e Under" の空白は置かない）。値 0.14、0.53、1.93、0.15、0.56 は recurrence_reduction.csv の diff_pp_2dp から編集スクリプトが読み、指示の文字列と一致することを assert で確認。
- 記号の対応: 題 a 1、表中 b 1・c 5・d 2・e 6、脚注 a〜e。一対一（footsym19.py）。

### 4.3 Online Resource 1（Table S12 のみ）
- 題: 指示の題を本文として入れ、番号の部分は ESM の他の 11 表と同じ形 "Supplementary Table S12. " にした（指示の "Table S12 " の形は他の表の題と不揃いになり、番号の検査も "Supplementary Table S" で数えるため）。題の最後の語 "ratio" に上付き a。
- 脚注: 指示の英文を脚注 a 一本に（表全体の脚注。ESM の他の表と同じく文字記号）。[ ] 内の "including entry after a locoregional recurrence" は残した: モデルに局所再発から遠隔再発への遷移がある（engine.R の lrr_dr rate、In_DR に LRR からの流入を含む）。末尾の略語の列 "HR, hazard ratio" に、ESM の他の脚注と同じく句点を付けた。"1 − HR" の負号は U+2212。
- v19 の脚注 b、c を削除し、8 つの列見出しの上付き b、c を外した（定義は脚注 a に移ったため）。脚注の語 "Distant recurrence"、"any recurrence" は列見出し "Distant recurrence at 5/7 years"、"Any recurrence at 5/7 years" と同じ語。
- 列、行、値は v19 のまま（72 値不変）。パネル A の題 "A. Cumulative proportion of women without exercise, %" は指示の範囲外なので変えていない（新しい題と脚注の語は "Cumulative recurrence"）。
- Table S1（CHEERS）: v19 の 28 セルを v19 の頁組みから再構築して一致を確認し、v20 の頁組み（m20_stats.json）で計算した結果、28 セルとも変化なし。PDF による独立照合: 151 段落で頁の不一致 0。
- 他の表（S8、S11 を含む）は不変。

### 4.4 cover letter
- 要約段落（第 7 段落）を指示の英文に差し替え（旧要約は残していない）。宛名、誌名、題名の段落、適合の段落、宣言の段落、推薦査読者、署名は v19 のまま。

### 4.5 その他
- Fig1〜3.tif、26_recurrence_reduction.R、recurrence_reduction.csv は v19 の逐字節コピー（作業樹の R/ と output/ のファイルとも同一）。
- manuscript_v20_BCRT_track_from_v18.docx: Word の文書比較、原本 = 尾崎の v18（archive/v18/manuscript_v18_BCRT.docx）、改訂 = v20、語単位、修訂者 Akemi Hara、修訂 26（挿入 12、削除 14）。v19 と v20 の変更をすべて含む（v19 の 8 か所、"about" の削除は v20 の文として現れる）。

## 5. 退行検査（regress19.py。出力見出しの "v18/v19" は検査器のラベル固定で、中身は v19→v20）

| 文書 | v19 単位 | v20 単位 | 不変 | 変更ブロック | 説明できない変更 |
|---|---|---|---|---|---|
| manuscript | 175 | 175 | 173 | 2 | 0 |
| tables | 310 | 310 | 303 | 5 | 0 |
| ESM | 2,599 | 2,597 | 2,587 | 3 | 0 |
| cover letter | 16 | 16 | 15 | 1 | 0 |
数値トークン: manuscript は 3,499 → 3,498 だけ。tables は "(Online Resource 1)" の 1 が増えただけ。ESM は Table S12 の旧脚注の数字（"1 − HR" の 1、"per 100"、"1.00"）が消えただけで表の値は不変。cover letter は旧要約の 0.722 が消え、新要約の 400,000 が入った。
名指し確認: 責任著者（題名ページ不変）、補足表の脚注（変わったのは Table S12 だけ、S8・S11 を含む他の脚注は不変）、題名（全文書で新題名のまま）、語数（3,498 = Word 実測）、図の解像度（Fig1〜3.tif は v17 から逐字節同、4015 px 幅、600 dpi）。意図せず戻った段落 0。
Word で開いた結果: 4 文書とも修訂 0、コメント 0。頁数 manuscript 31、tables 9、ESM 49、cover letter 2。

## 6. 数値台帳（本版で表記が変わった数値）

| 位置 | 数値 | 出所 |
|---|---|---|
| Discussion 第3段落 | 0.14 | recurrence_reduction.csv（chemo_pembro, 0.989, distant, 84, diff_pp_2dp）= Table S12 パネル B 0.989 行・化学療法＋ペムブロリズマブ・Distant recurrence at 7 years |
| Table 3 脚注 e | 0.14、0.53、1.93、0.15、0.56 | 同 CSV（0.989/0.958/0.85 chemo_pembro、0.991/0.966 chemo_alone、distant、84）= Table S12 の同セル |
| 題名ページ | 3,498 | Word 実測（checks_v20/out/m20_stats.json） |
| cover letter | about JPY 400,000 per dose | 指示の英文（本文の 398,924 円 [8] の概数） |

## 7. 用語

v19 を継承。Table S12 の用語は脚注で定義: cumulative recurrence、distant recurrence、any recurrence、absolute reduction。

## 8. WRITING_RULES.md 全項目の点検表（改稿後の再読のうえ、1 項目 1 行）

凡例: [x] 通過、[注] 通過だが注記、[偏] 記録済みの偏離、[—] 該当なし。

版
- [x] 作業樹（manuscript/）に最新版 v20 だけ（v19 は交付時に archive へ）
- [x] 開始時の sha256 が MANIFEST_v19 と一致（68/68）
- [x] 底本 = v19 交付物、本書第2節に底本名と sha256
- [x] 意図せず戻った段落 0（第5節、5 点名指し）
- [x] 数値の変更なし（表の値と推定値は v19 と同一。変わったのは "about" の削除と語数行）
- [—] テンプレートの雛形: ESM と cover letter の著者・署名・推薦査読者の欄は尾崎の担当（第14節）
- [注] 作業注記: cover letter 第 9 段落の行内 "[To be confirmed: …]" 1 件（既存、範囲外で不変）
- [x] MANIFEST_v20 を作成、v19 を archive へ移動
- [x] 解析出力は不変（recurrence_reduction.csv 867c0eba、他の出所も不変）
- [x] 差分の全単位が指示に対応（説明できない変更 0、4 文書）
- [x] 撤回した主張の復活 0
- [x] 変更履歴とコメント 0（Word で確認、track 版は別ファイル）
- [x] 作業樹に ars/ なし

参考文献と付番
- [x] 初出順 1〜71 欠けなし、未引用 0（78/78）
- [x] DOI 61/61 解決、書誌不一致 0、未解決 0
- [—] 新規の文献引用なし
- [—] 文献の追加・移動なし
- [x] 著者名と年の本文引用 0
- [x] 10 年超の文献 8 件、自著引用 0（不変、報告のみ）
- [注] 新規性: 本文の文は不変（PubMed と Europe PMC、2000〜2026 の範囲で限定）。cover letter の "To our knowledge, this is the first economic evaluation …" はユーザーの英文（絶対形をユーザーが自ら書いたもの）
- [x] 四系列の初出順 1..n
- [x] 各系列の最大番号 = 実物数
- [x] 全表図に地の文の言及
- [x] ESM 内の並びが番号順
- [x] Supplementary Methods S1 と CHEERS の引用あり
- [x] 図 1〜3 添付、順に言及

見出しと体裁
- [偏] 大見出しと Methods 小見出しは BCRT 構造（v11 以来）
- [x] 規約外の節と項目: v19 と同じ（追加・削除 0）
- [x] Heading スタイル 0
- [x] 全 run 12 pt Times New Roman（manuscript 223、tables 381、ESM 2,749、cover letter。増減した run もすべて 12 pt TNR）
- [x] 行番号あり、本文の行間 480（v19 と同じ目録）
- [x] 本文の行内太字 0
- [x] 表の列見出しと数値セルに太字 0（Table S12 の太字は数字を含まないパネル題 2 つ）
- [x] 黒以外の文字 0
- [x] 中黒 0
- [x] 表は横版
- [偏] 脚注記号は文字（BCRT 偏離）。Table 3 は a〜e、Table S12 は a。"Note" 始まり 0
- [注] 記号の一対一: Table 1〜3、S8、S9、S11、S12 で片側だけの記号 0。Table 3 の e はセル末尾ではなく HR の値の直後（指示による）
- [x] 図 600 dpi（逐字節同）
- [x] 前付けは尾崎の記入どおり
- [注] 生成 AI の記述: Methods 末尾と COI の記載は尾崎の判断として残す（ユーザー承認の例外）。CC が足した記述 0
- [x] ARS のマーカー 0
- [x] ARS 既定由来の構造 0
- [x] 米式綴り、"Fig."
- [x] 語数（249 ≤ 250、3,498 ≤ 3,500）を節別に実測、題名ページと一致

数値
- [x] 本文の 0.14 は Table S12 に同値・同桁
- [x] Table 3 脚注 e の数値は Table S12 に同値・同桁（"about" を外し 2 桁で一致）
- [注] 同じ数値が二つの表: Table 3 脚注 e の 5 値は Table S12 の値の引用（指示による）。Table 2 B と S4 の重複は従前どおり
- [—] n、流れ図、対象者数: 該当なし
- [x] 点推定と UI（不変）
- [x] 同じ統計量は同値
- [—] p 値なし
- [x] 因果語 0
- [x] Table S12 の空セル 0（縦結合の見出しのみ）
- [x] 負号 U+2212、先頭 0、千位カンマ
- [x] Table S12 の値は 2 桁でそろう

内容
- [x] Methods に数値結果 0（不変）
- [x] Results に「〜を用いた」型 0（不変）
- [x] 結果文に表図の参照（不変）
- [x] 各解析の目的文（不変）
- [注] Introduction 末 2 段: 従前の注どおり
- [注] 目的対応表: v17 を継承（構成不変）
- [x] 曝露とアウトカムの名前（不変）
- [x] 抄録（不変）
- [x] Results の段落順と段首の名指し（不変）
- [x] Discussion 段首（不変）
- [注] Discussion 第1段落は目的①中心（従前どおり）
- [x] Discussion と Results の重複（変更は "about" の削除だけ）
- [x] Discussion の引用分布（不変）
- [x] "further research is needed" 型 0
- [x] 臨床医が何を変えるか（不変）
- [x] Implications（不変）
- [注] check_acronyms（ARS 3.24.1）: 本文・抄録とも v19 と逐字同（partial: PMC、CHEERS、EQ の既知 3 件）
- [x] 限界は Limitations のみ
- [x] Outcome/Variables の第一文（不変）
- [x] 統計ソフト（不変）
- [x] Data availability と公開フォルダ（不変、一致）
- [x] CHEERS の頁と節（v20 の頁組みで 28 セル不変、PDF で独立照合）
- [x] 題名の一致（manuscript、ESM、cover letter、README）
- [x] 事前計画、欠測、多重比較（不変）
- [—] 選定の流れ図: 該当なし
- [x] 図は不変
- [x] 図と表の重複（新規なし）
- [—] 著者の貢献: 尾崎の記入
- [注] AI 常套語 0、前置き 0、接続語連発 0、挿入句のダッシュ 0（本文）。30 語超の文 48（v19 と同数。Discussion 第3段落の文は 43 → 42 語）、最長 67。150 語超の段落 1（Introduction 第3段落、v18 から）
- [注] 裸の時間語 currently 1、now 1、current 1（既存）
- [x] 主張の強さ: 強くなった文 0（"about" を外したのは Table S12 の値と同じ桁にするため。値の意味は同じ）
- [—] 査読対応の版ではない
- [—] humanizer、stop-slop は使っていない

新しく足した検査の空打ち（checks_v20/out/bell20.txt）
- tfnum20（tfnum19 の v20 名版）: Introduction 第1段落に "(Table S12)" を仕込む → Table S の初出順 [12, 1, …] で不合格。鳴った。
- citeorder20（citeorder19 の v20 名版）: 同じ段落に "[1,50]" を仕込む → 初出順 False。鳴った。
- 他の検査器は v19 で空打ち済みのものをそのまま使用（regress19、footsym19、sec10_19、word_wc19）。

## 9. 著者側・ユーザー判断に残す事項

- Table S12 の題の番号部分を "Supplementary Table S12." の形にした（第4.3節）。指示どおり "Table S12 " にするなら他の 11 表と形が揃わない。
- Table S12 パネル A の題 "Cumulative proportion of women without exercise, %" は、新しい題と脚注の語 "Cumulative recurrence" とは別の言い方のまま（指示の範囲外）。
- v17 から持ち越していた 11 月 1 日の薬価改定は、裁定 (4) により反映しないことで決着。

## 10. 撤回した主張、共著者コメント台帳、過去に戻った箇所、文献検索

- 撤回した主張: 復活 0（v18 で尾崎が外した文と v19 の cover letter 旧要約は戻していない）。
- 共著者コメント台帳: 本版に共著者の戻しなし。採否 = ユーザーの v20 指示。
- 過去に戻った箇所: 第5節の 5 点、戻りなし。
- 文献検索: v11 第11節を継承。追加なし。

## 11. スクリプト

編集: manuscript/code/edit_manuscript_v20.py、edit_tables_v20.py、edit_esm_v20.py、edit_cover_v20.py（v19 の sha256 を確認してから word/document.xml だけを lxml で書き換え、元の文字列が 1 か所でなければ停止）。検査: checks_v20/（tfnum20、citeorder20）と checks_v19/（regress19、diff19、footsym19、sec10_19、word_wc19、word_finalize19.ps1）、checks_v11（fmt_audit、refcheck、word_stats.ps1）、checks_v12/pdf_pages.py、ARS 3.24.1 check_acronyms.py。出力は checks_v20/out/。sha256 は MANIFEST_v20.md。
