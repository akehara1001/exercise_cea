# AUDIT v19（2026-11-07）

本書は v19 の作業ログを兼ねる（規約第12節の順）。v19 指示＝「exercise_cea v19: 尾崎 v18 を底本に、再発の絶対差（Table S12）、題名統一、CHEERS 更新」。

開始時の宣言（規約冒頭）
1. 規約 WRITING_RULES.md を開始時に全文読んだ。改稿後にも全文を再読した（第13節の点検は本書第10節）。
2. 連鎖の段階: 初稿後の改稿（第1節の 6 に相当）。今回は指示の英文をそのまま入れる版で、humanizer も stop-slop も掛けていない（指示: humanizer は掛けない）。ARS は第1.6節の範囲（docx 直接編集、変更段落だけ）。
3. 底本: v18 一式（第2節）。作業樹 manuscript/ には作業中 v17、v18、v19 が並んだが、これは指示（v18 を組んで v19 を作り、交付後に v17 と v18 を archive へ）による。交付後は v19 だけ。

## 1. 最重要4項目（先頭で報告）

1. 版: 通過。底本 = v18 一式（manuscript = 尾崎の v18、他 = v17 交付物の逐字節コピー）。v17 以前、生成スクリプト、md、テンプレートからは作っていない（全編集は v18 docx の lxml 直接編集）。交付後、manuscript/ には v19 だけ（v17、v18 → manuscript/archive/）。
2. 表と図: 通過。本文 61 段落を走査、言及 52 件（範囲展開後）。Table 1〜3、Fig. 1〜3、Table S1〜S12、Fig. S1〜S2 の全部が地の文で番号付きで引用され、初出順は各系列 1..n、最大番号 = 実物数（3、3、12、2）。範囲（Tables S1–S12）を除いた個別引用でも全番号に地の文の引用があり、順も単調（S4 = Results 第2節、S12 = Discussion 第3段落。checks_v19/out/tfnum19.txt）。
3. 文献の真偽: 通過。DOI 61/61 が doi.org で解決（302）、著者不一致 0、年不一致 0。巻頁フラグ 10、58 は既知の検査器の偽陽性（v11 以来、Cochrane の 2016(9) 表記など）。DOI の無い 17 件: 15 件 HTTP 200、第 8 条の原網址 404（既知。2 つの Wayback 存档は 200、727,243 / 386,582 バイト = 保存済みファイルと同じ）、第 52 条は書籍。出力は v17 と逐字同（refcheck_v19.json の sha256 = refcheck_v17.json）。
4. 文献の順序: 通過。本文の初出順 1〜71 欠けなし（62 群、112 番号）。manuscript、tables、ESM の引用列は v18 と完全一致。78 件すべて引用あり（72〜78 は tables と ESM のみ、v17 以来）。

## 2. 底本と作業樹

- 指示の v18 パス（manuscript\v18\）は存在しなかった。尾崎の v18 は C:\Users\原明美\Downloads\ にあった（manuscript_v18_BCRT.docx、_track_from_v17.docx、保存 2026-11-07 20:30）。指示どおり manuscript\v18\ にコピーし、v17 の本文以外の交付物（tables、ESM docx/pdf、Fig1〜3.tif、cover letter）を逐字節コピーして版番号を v18 に改名、v18 一式を揃えた（manuscript/archive/v18/MANIFEST_v18.md）。
- 底本: manuscript_v18_BCRT.docx（v18、sha256 先頭 8 桁 d2665669）。同一式: tables_v18_BCRT.docx（8236a3ee）、ESM_1_v18.docx（642590a6）、ESM_1_v18.pdf（826fb01a）、Fig1〜3.tif（c13b748e、662046bf、d7926e1e）、cover_letter_v18_BCRT.docx（21ed7f1a）。後 5 種は MANIFEST_v17 の sha256 と一致。
- 会話開始時: manuscript/v17/ の 9 ファイルの sha256 が MANIFEST_v17 と一致。v17 の数値出所と薬価表 71 ファイルの sha256 も MANIFEST_v17 と全件一致（再計算）。
- v18 本文: 修訂 0、コメント 0（コメント部品なし、w:ins/w:del 0）。track_from_v17 は確認用で底本ではない。v17→v18 の尾崎の変更は 19 ブロック（checks_v19/out/diff_m17_m18.txt）。

## 3. 投稿先と仕様（v17 第2節を継承）

- BCRT。抄録上限 250、本文上限 3,500 語（Word の数え方: 抄録は 4 ラベル除く、本文は Introduction〜Conclusion の見出し除く。v18 から Acknowledgments 節が無いので本文の終わりは References の前）。Springer 番号式文献、米式綴り、"Fig."。
- 実測（Word ComputeStatistics、checks_v19/word_wc19.py）: v18 = 抄録 249、本文 3,498（尾崎の記載と一致）。v19 = 抄録 249、本文 3,499（見出し込み 3,540）。節別: Introduction 588、Methods 1,402、Results 609、Discussion 460、Implications 176、Limitations 211、Conclusion 53。題名ページの Word count 行を "main text 3,499" に更新（抄録 249 は不変）。31 頁。
- 偏離（v11 以来、BCRT 構造は尾崎の決定）: 見出し構成、表脚注記号 a〜d、Conclusion 節。v18 で尾崎が加えた Methods 末尾の Claude 使用文と COI の Anthropic 記載は、指示により尾崎の判断として残す（規約第8節の例外、ユーザー承認）。

## 4. Table S12 の計算（指示第1節）

- スクリプト: R/26_recurrence_reduction.R（作業樹と exercise_cea_public に同一ファイル、sha256 4e2f2ebc）。出力: output/phase2/main/recurrence_reduction.csv（867c0eba）、検査結果 recurrence_reduction_checks.csv（d88dc07d、71 項目すべて TRUE）。
- 設定: 決定論的基本解析。engine_params.rds の基本値（外部 k なし、S-JP なし）、効果は無作為化後 5 年保持、以後 1 − HR が毎年半減（R/25_four_arm.R の path_a("base") と同じ: wane_start 5、wane_rate log 2）。エンジンは費用モデルと同じ econ_arm() から取る。プログラム費用は生存に入らない。
- 計算法: エンジンが返すサイクルごとの流入（In_DR、In_LRR = 前サイクルの占有 × 遷移確率）の累積和。(a) 遠隔再発 = cumsum(In_DR)（無事象と局所再発の両方からの流入、1 人 1 回）。(b) 再発全体 = cumsum(In_LRR + 無事象からの遠隔流入)。局所→遠隔の流入は局所状態の収支（流入累計 − 在留 − 局所からの死亡）の差分。時点 t の占有は使っていない。手術前の進行（PreProg）は数えない。第 0 月 = 無作為化、第 60 月と第 84 月で読む。分母はモデル全コホート（pCR の有無、手術前進行例を含む）、100 人あたり。
- 検算（指示の 5 項目＋追加）:
  - HR 1.00 で差 0: 通過（運動群に HR 1 を与えたエンジンが運動なし群と 1e-12 以内で一致、両群とも）。
  - HR が下がるほど差が単調に増える: 通過（両群×両アウトカム×両時点の 8 列すべて狭義単調増加）。
  - 7 年の差 ≥ 5 年の差: 通過（全 HR）。
  - HR 1.00 の累積割合 ≤ 1 − EFS(t): 通過。化学療法＋ペムブロリズマブ: 5 年 遠隔 13.13% ≤ 全体 15.55% ≤ 1 − EFS 19.53%、7 年 15.61% ≤ 17.35% ≤ 21.73%。化学療法単独: 5 年 18.11% ≤ 21.02% ≤ 27.92%、7 年 20.86% ≤ 22.79% ≤ 30.16%。
  - KEYNOTE-522 との桁: 合う（止めない）。Schmid 2022（遠隔再発または遠隔進行が初回イベント、追跡中央値 39 か月）pembrolizumab 7.7%、placebo 13.1%。モデル第 39 月・運動なしの遠隔再発（術後）: 全流入 9.85% / 14.05%、初回イベントのみ（局所→遠隔を除く、試験の数え方）7.81% / 11.62%。差の向きの説明: 局所→遠隔を含めると上がる、試験側は手術前の遠隔進行を含む（placebo 群で多い）、試験の値は追跡中央値時点の粗割合。
  - 追加: (b) の 2 通りの計算（流入の累積和と、無事象状態の収支 1 − EF − 手術前進行累計 − 無事象からの死亡 − 有害事象死亡）が全時点で 1e-12 以内で一致（最大 1.5e-15）。手術前の再発流入 0。HR 0.95、0.85、0.72 の総費用と QALY が fourarm_totals.csv（Table 2 の出所）と一致（最大相対差 4.5e-15）＝ Table 2 と同じ基本解析。
- 公開フォルダでの再現: exercise_cea_public の HEAD を清潔に取り出し（git archive）、00_lifetable.R → 10_read_params.R → 26 を実行、recurrence_reduction.csv が作業樹のものと逐字節一致（sha256 867c0eba）。
- 表の値（2 桁、half up、表内でそろえる。0.989 の行は 0.12〜0.20 で 0.0 に丸まらない）: Online Resource 1 Table S12（第5節）。脚注と本文に入れた 7 年遠隔再発の差: [a] HR 0.989（化学療法＋ペムブロリズマブ）0.14、[b] 0.958 0.53、[c] 0.85 1.93、[d] 0.991（化学療法単独）0.15、[e] 0.966 0.56（すべて CSV の diff_pp_2dp から編集スクリプトが読み込み、手打ちなし）。

## 5. 本版で変えた段落（変更前後は checks_v19/out/diff_*.txt、退行検査は r19_*.txt）

### 5.1 manuscript（175 段 → 175 段、不変 168、変更 7 段＋語数行。説明できない変更 0）
| 指示 | 位置 | 変更 |
|---|---|---|
| 2 | Methods, Study design 第3段落 | "Tables S1–S11" → "Tables S1–S12" |
| 4(1) | Results, Exercise compared with pembrolizumab 第1文 | 末尾に "(Table S4)"（指示の英文どおり） |
| 4(2) | Discussion 第3段落 | 2 文を指示の英文に差し替え（[a] = 0.14） |
| 4(3) | Discussion 第1段落 | "(Table 2)" → "(Tables 2 and 3)" |
| 4(4) | Methods, Exercise effect and costs 第3段落 | "its about 50 sessions" → "its roughly 50 sessions" |
| 4(5)a | Discussion 第2段落末 | 指示 a の差し替え（−7 語） |
| 4(5)b | Methods, Study design 第3段落 | 指示 b の差し替え（−5 語。a だけでは 3,504 で超過したため） |
| 4(5) | 題名ページ Word count 行 | "main text 3,498" → "3,499"（Word 実測） |
語数の経過: v18 3,498 → 指示 2、4(1)〜4(4) 適用後 +13 → a 適用で 3,504（超過）→ b 適用で 3,499（≤ 3,500）。数値、主張、表図の引用は削っていない。
題名ページ（著者、所属、責任著者、ORCID）、Statements and Declarations 以下、Methods 末尾の Claude の一文は一字も変えていない（退行検査で不変を確認）。

### 5.2 tables（指示 3。Table 1、2 は不変）
- Table 3: ✳（上付き、セル文字列の末尾）を 6 か所: パネル A「The maximum affordable cost equals … fee-schedule-based program」行の 0.989 (1.1)、0.991 (0.9)、同「Medical costs avoided equal … fee-schedule-based program」行の 0.958 (4.2)、0.966 (3.4)、パネル B と C の行ラベル "Base case, recurrence HR 0.85"。化学療法単独列の CHALLENGE 行の 0.958 (4.2) は別の分岐点なので付けない。
- 脚注 d の後に指示の文を追加（値は CSV から）: "✳ Under the base-case assumptions, recurrence HRs of 0.989, 0.958 and 0.85 with chemotherapy plus pembrolizumab correspond to absolute reductions in distant recurrence at 7 years of about 0.14, 0.53 and 1.93 percentage points, and HRs of 0.991 and 0.966 with chemotherapy alone to about 0.15 and 0.56 points (Table S12)."
- 表 docx に旧題名、"secondary/reference comparison" は無かった（全部品を検索）。

### 5.3 Online Resource 1（ESM）
- 表紙: "Article: <旧題名>" → 新題名（指示 2、5）。ESM にはヘッダー部品が無く、柱の題名は存在しない（全 XML 部品を検索）。
- "secondary comparison" → 本文の言い方（指示 5）: Table S8 の列見出し 6 個（2 パネル × 3）"…: secondary comparison" → "…: exercise added to chemotherapy alone"、Table S11 の列見出し 3 個 "Secondary comparison: …" → "Exercise added to chemotherapy alone: …"、Table S9 脚注 "(secondary comparison)" → "(exercise added to chemotherapy alone)"、Table S8 と S11 の脚注 a から定義句 "secondary comparison: exercise added to chemotherapy alone" を削除（ラベルを使わなくなったため）。"reference comparison" は 0 件。"main comparison" はそのまま。
- Table S12 を Table S11 の後に追加（指示 2）。他の表と同じく独立した横版セクション。題、9 列の表（2 段見出し、パネル A = 運動なしの累積割合 %、パネル B = 運動ありの絶対差 ポイント）、脚注 a〜c（ESM の全表と同じ文字記号、置き方は規約 7.2: a は題の最後の語、b は「Distant recurrence at …」の 4 見出し、c は「Any recurrence at …」の 4 見出しの末尾）。脚注 a に、決定論的基本解析、効果は 5 年保持後に毎年半減、HR が局所と遠隔の両遷移に掛かること、術後の再発のみで手術前の進行は含まないこと、分母（100 人、pCR の有無と手術前進行例を含む）、時点の定義、略語（HR、pCR）。b、c に 2 つのアウトカムの定義。題、見出し、脚注の英文は CC が書いた（指示に英文の指定なし）。
- Table S1（CHEERS）: 第6節。

### 5.4 cover letter（指示 5）
- 題名を新題名に。要約段落を v18 の 3 つの問いの順に書き直し（背景の第 1 文は不変）: 4 群の比較（運動で再発ハザードが 5% 以上下がれば運動なしの 2 戦略は劣位）→ 運動対ペムブロリズマブ（ペムブロリズマブは日本で費用対効果あり、運動はその健康増分に届かず、純便益で並ぶには HR 0.722）→ ペムブロリズマブへの上乗せ（診療報酬ベースのプログラムは 1.1% で費用対効果あり、価値は価格より効果の大きさと持続で決まる）。文言は v18 の抄録と Discussion の記述から取った。旧要約の「持続期間がどの費用入力より効く」は尾崎が v18 抄録から外したので、抄録 Conclusion の言い方に合わせた。他の段落は不変。

### 5.5 公開フォルダ（exercise_cea_public、ローカル commit e23e167、リモートなし・未推送は従前どおり）
- R/26_recurrence_reduction.R と output/phase2/main/recurrence_reduction.csv を追加（逐字節同。commit の blob = ファイルのバイト）。
- README: 見出しを新題名に（旧見出しは旧題名の言い換え形 "Exercise during neoadjuvant chemotherapy … : cost-effectiveness model" だったので置換）、実行手順 5 と表図対応表に Supplementary Table S12 の行を追加。

## 6. Table S1（CHEERS 2022）の更新（指示 6）

方法: v18（= v17）の 28 セルを v17 の頁組み（checks_v17/out/m17_stats.json）から再構築して全件一致を確認したうえで、v19 本文の Word 頁組み（checks_v19/out/m19_stats.json）と v19 の本文で書き直した。頁は Word の PDF（SaveAs2）でも独立に照合: 151 段落で頁の不一致 0（未定位 11 段は長い URL などで、Location に使う段落ではない）。PDF 上で題名ページ pp. 1〜2、抄録 p. 3、Funding p. 28、Competing interests pp. 28〜29、Data availability p. 29 を目視確認。
v19 で題名ページが 2 頁になった（尾崎の著者・所属）ため、多くの項目で頁が 1 つずつ後ろへ動いた。

| 項目 | v18（= v17）| v19 |
|---|---|---|
| 1 題名 | Title page (p. 1) | Title page (pp. 1 to 2) |
| 2 抄録 | Abstract (p. 2) | Abstract (p. 3) |
| 3 背景と目的 | Introduction, paragraphs 1 to 4 (pp. 3 to 4) | 同 (pp. 4 to 5) |
| 4 分析計画 | Study design, paragraph 3 (p. 5) | 同 (p. 6) |
| 5 対象 | Study design, paragraph 1; Table 1 (pp. 4 to 5) | 同 (pp. 5 to 6) |
| 6 設定 | Study design, paragraphs 1 to 2 (pp. 4 to 5) | 同 (pp. 5 to 6) |
| 7 比較対照 | Study design, paragraph 1 (pp. 4 to 5) | Study design, paragraph 1; Methods, Exercise effect and costs, paragraph 3 (pp. 5 to 8)（v18 で運動プログラムの内容の段落が戻ったため追加） |
| 8〜10 視点、期間、割引 | Study design, paragraph 2 (p. 5) | 同 (p. 6) |
| 11 アウトカム選択 | Outcomes, paragraphs 1 to 2 (pp. 5 to 6) | 同 (pp. 6 to 7) |
| 12 アウトカム測定 | … (pp. 6 to 7) | 同 (pp. 7 to 8) |
| 13 評価 | Survival, costs and utilities, paragraph 2 (p. 7) | 同 (pp. 8 to 9) |
| 14 費用 | Exercise effect and costs, paragraph 3; Survival…, paragraph 2; Table 1; Table S2 (pp. 6 to 7) | 同（文言不変、プログラム費用の段落 = paragraph 3）(pp. 7 to 9) |
| 15 通貨と価格年 | … paragraph 3; … paragraph 2 (pp. 6 to 7) | 同 (pp. 7 to 9) |
| 16 モデル | … Data availability (pp. 4 to 27) | 同 (pp. 5 to 29) |
| 17 解析と仮定 | … (pp. 6 to 8) | 同 (pp. 7 to 9) |
| 18 異質性 | No subgroup analyses beyond the two comparisons; … (pp. 4 to 5) | No subgroup analyses beyond exercise added to chemotherapy alone and to chemotherapy plus pembrolizumab; Methods, Study design, paragraph 1 (pp. 5 to 6)（"two comparisons" は v18 本文に無い枠組みのため本文の言い方に） |
| 19 分布 | Not performed | 不変 |
| 20 不確実性 | Statistical analysis, stages (4) to (6); Supplementary Methods S1 (pp. 8 to 9) | 同; Discussion, Limitations, paragraph 2 (pp. 9 to 15)（EVPI の一文が戻ったため） |
| 21 参画 | Not performed | 不変 |
| 22 パラメータ | Table 1; Supplementary Table S2 | 不変 |
| 23 主要結果 | … Supplementary Tables S4 to S9 (pp. 9 to 11) | … Supplementary Tables S4 to S9 and S12 (pp. 10 to 12) |
| 24 不確実性の効果 | … (pp. 10 to 11) | 同 (pp. 11 to 12) |
| 25 | Not applicable (item 21) | 不変 |
| 26 所見と限界 | Discussion, paragraphs 1 to 7; Discussion, Implications; Discussion, Limitations (pp. 11 to 14) | 同 (pp. 12 to 15) |
| 27 資金 | Statements and Declarations, Funding (p. 27) | 同 (p. 28) |
| 28 利益相反 | Statements and Declarations, Competing interests (p. 27) | 同 (pp. 28 to 29) |
変更 24 セル、不変 4（19、21、22、25）。

## 7. 退行検査（規約 1.2 規則 7。regress19.py、編集ログで各変更単位を指示に対応付け）

| 文書 | v18 単位 | v19 単位 | 不変 | 変更ブロック | 説明できない変更 |
|---|---|---|---|---|---|
| manuscript | 175 | 175 | 168 | 5 | 0 |
| tables | 309 | 310 | 303 | 5 | 0 |
| ESM | 2,507 | 2,599 | 2,470 | 36 | 0 |
| cover letter | 16 | 16 | 14 | 1 | 0 |
意図せず戻った段落 0。名指し確認: 責任著者（題名ページ不変、尾崎の記入どおり）、補足表の脚注（変わったのは S8、S9、S11 の指示 5 の語句だけ、他の脚注は不変）、題名（manuscript = 尾崎の新題名、ESM・cover letter・README を新題名に統一、旧題名の残り 0 件＝全部品検索）、語数（3,499 = Word 実測と一致）、図の解像度（Fig1〜3.tif は v17 と逐字節同、4015 px 幅、600 dpi）。v17 作業ログ第 11 節の過去に戻った箇所も同じ 5 点で、すべて戻りなし。
Word で開いた結果: 4 文書とも修訂 0、コメント 0。頁数 manuscript 31、tables 9（v17 と同）、ESM 49（v17 48 + Table S12 の 1 頁）、cover letter 2。

## 8. 数値台帳（本版で新たに入った数値）

| 位置 | 数値 | 出所 |
|---|---|---|
| Discussion 第3段落 | 0.14 | recurrence_reduction.csv（chemo_pembro, hr 0.989, distant, month 84, diff_pp_2dp）= Table S12 パネル B 0.989 行「化学療法＋ペムブロリズマブ: Distant recurrence at 7 years」 |
| Table 3 脚注 ✳ | 0.14、0.53、1.93、0.15、0.56 | 同 CSV（0.989/0.958/0.85 chemo_pembro、0.991/0.966 chemo_alone、distant、84）= Table S12 の同セル |
| Table S12 全 72 値 | 13.13〜22.79（A）、0.10〜5.24（B） | 同 CSV（pct_without_2dp、diff_pp_2dp） |
| 題名ページ | 3,499 | Word 実測（checks_v19/out/m19_stats.json） |
他の数値は v18 から不変（退行検査の数値トークン比較: manuscript で消えたのは 3,498 と S11 の 11、増えたのは 3,499、S12 の 12×2、0.14、"(Tables 2 and 3)" の 3、"(Table S4)" の 4、"7 years" の 7）。

## 9. 用語表

v17 を継承。新出の名前: distant recurrence（術後に遠隔再発状態へ初めて入ること、局所再発経由を含む）、any recurrence（術後に局所または遠隔再発へ初めて入ること）、absolute reduction（運動なし − 運動あり、ポイント）。いずれも Table S12 の脚注で定義。"exercise added to chemotherapy alone"、"pembrolizumab against chemotherapy alone" は本文と ESM で同じ言い方に統一（"secondary comparison" 0 件、"reference comparison" 0 件）。

## 10. WRITING_RULES.md 全項目の点検表（改稿後の再読のうえ、1 項目 1 行）

凡例: [x] 通過、[注] 通過だが注記、[偏] 記録済みの偏離、[—] 該当なし。

版
- [x] 作業樹（manuscript/）に最新版 v19 だけ（v17、v18 は交付時に archive へ。生成スクリプト出力、md、テンプレートなし）
- [x] セッション開始時の sha256 が MANIFEST_v17 と一致（9/9、出所 71/71）
- [x] 底本 = v18 交付物、本書冒頭に底本名と sha256
- [x] 意図せず戻った段落 0（第7節、5 点名指し）
- [注] 数値を変えた版: 新規数値は Table S12 と、その値を引く Table 3 脚注・Discussion の 1 か所だけ。既存数値の変更 0（第8節）
- [—] テンプレートの雛形: ESM の Authors/Corresponding author と cover letter の署名・推薦査読者は尾崎の担当（第14節、報告しない）
- [注] 版ラベルと作業注記 0。[TO CONFIRM] 型: cover letter 第 8 段落の行内の "[To be confirmed: …]" 1 件（v17 以前からある既存、今回の指示の範囲外で不変）
- [x] MANIFEST_v19 を作成、v17 と v18 を archive に移動
- [x] 解析出力: 新出力 recurrence_reduction.csv（と checks）の sha256 を manifest に記載、既存出力 71 件は不変
- [x] 差分の全単位が指示に対応（説明できない変更 0、4 文書）
- [x] 撤回した主張の復活 0（v12〜v17 の撤回項目は本文に無い）
- [x] 変更履歴とコメント 0（Word で確認。track 版は別ファイル）
- [x] 作業樹に ars/ なし

参考文献と付番
- [x] 文献番号の初出順 1〜71 欠けなし、未引用 0（78/78）
- [x] DOI 61/61 解決、書誌不一致 0（巻頁フラグ 2 件は既知の偽陽性）、未解決 0
- [—] 新規の文献引用なし（KEYNOTE-522 2022 との照合は検算のみで本文に入れていない）
- [—] 文献の追加・移動なし（citation-check 不要）
- [x] 著者名と年の本文引用 0
- [x] 10 年超の文献 8 件（1、2、11、12、14、49、68、75）、自著引用 0（v18 の著者 9 名で照合）。報告のみ
- [x] 新規性の文は不変（PubMed と Europe PMC、2000〜2026）
- [x] 四系列の初出順 1..n（Table、Fig.、Table S 1..12、Fig. S）
- [x] 各系列の最大番号 = 実物数（3、3、12、2）
- [x] 全表図に地の文の言及（個別引用でも全番号あり）
- [x] ESM 内の並びが番号順（表 1..12、図 1..2）
- [x] Supplementary Methods S1 の言及 4 件、CHEERS（Table S1）を Methods から引用
- [x] 図 1〜3 添付、本文で順に言及

見出しと体裁
- [偏] 大見出しと小見出しは BCRT 構造（v11 以来の偏離、v18 で不変）
- [x] 規約外の節と項目: v18 の構成をそのまま（v18 で尾崎が Acknowledgments を削除、Statements の記入。v19 で追加・削除 0）
- [偏] Methods 小見出しは BCRT 構造（同上）
- [x] Heading スタイル 0（175 段すべて Normal）
- [x] 全 run 12 pt Times New Roman（manuscript 223 run、tables 377、ESM 2,761、cover letter。新規 run もすべて 12 pt TNR）
- [x] 行番号あり（sectPr lnNumType）
- [x] 本文段落の行間 480（双倍）172/172
- [x] 本文の行内太字 0（太字は見出し、ラベル、題名のみ。v18 と同一）
- [x] 表の列見出しと数値セルに太字 0。新規の太字は Table S12 の数字を含まないパネル題 2 つだけ
- [x] 黒以外の文字 0
- [x] 中黒「・」0
- [x] 表は横版（Table S12 も横版セクション）
- [偏] 脚注記号は文字 a〜d（BCRT 偏離）。Table 3 の新脚注だけ指示の英文どおり ✳。"Note" 始まり 0
- [x] 脚注記号の一対一: Table 1 a〜d、Table 2 a〜d、Table 3 a〜d と ✳（表中 ✳ 6、脚注 1）、S8・S9 a、S11 a〜d、S12 a（題）、b ×4、c ×4 と脚注 a〜c。片側だけの記号 0（footsym19.txt）
- [x] 図 4015 × 2173/2456/3023 px、600 dpi（v17 と逐字節同）
- [x] 前付けは尾崎の記入どおり（不変）
- [注] 生成 AI の記述: Methods 末尾と COI の Claude/Anthropic の記載は尾崎の判断として指示で残す（ユーザー承認の例外）。CC が足した記述 0
- [x] ARS のマーカー 0
- [x] ARS 既定に由来する構造 0（Conclusion は BCRT 構造で v18 にあるもの）
- [x] 米式綴り、"Fig." 統一
- [x] 語数を節ごとに実測、題名ページと一致、上限内（249 ≤ 250、3,499 ≤ 3,500）

数値
- [x] 本文の新規数値 0.14 は Table S12 に同値・同桁
- [x] Table 3 の新脚注の数値は Table S12 に同値・同桁
- [注] 同じ数値が二つの表: Table 3 脚注 ✳ の 5 値は Table S12 の値（指示による引用。規約 7.2 の「脚注の数値は表にある数値」に従う）。従前からの Table 2 B と S4 の重複は照旧
- [—] n の合計、流れ図: 該当なし
- [—] 対象者数: 該当なし（モデル）
- [x] 点推定と UI（不変）
- [x] 同じ統計量は同値（0.989、0.958、0.85、0.991、0.966 の表記は Table 3 と S12 と本文で同じ）
- [—] p 値なし
- [x] 因果語 0（sec10: caused、led to、impact 0）
- [x] Table S12 は空セル 0（縦結合の見出しセルのみ）、要約統計量なし
- [x] 負号（新規なし）、1 未満の先頭 0（0.10 など）、千位カンマ（新規なし）
- [x] Table S12 は全値 2 桁でそろえた

内容
- [x] Methods に数値結果 0（変更は語句と S12 の範囲だけ）
- [x] Results に「〜を用いた」型 0（変更は "(Table S4)" の追加だけ）
- [x] 結果文に表図の参照（Table S4 の引用を戻した）
- [x] 各解析の目的文（不変）
- [注] Introduction 末 2 段: v14 以来の注（不足の列挙段落の形）照旧
- [注] 目的対応表: v17 を継承（今回は目的・段落構成とも不変）
- [x] 曝露とアウトカムの名前（不変）
- [x] 抄録（不変、尾崎 v18）
- [x] Results の段落順と段首の表図名指し（不変）
- [x] Discussion 段首（第1段落の引用が "(Tables 2 and 3)" に）
- [注] Discussion 第1段落は目的①中心（従前どおり）
- [x] Discussion と Results の重複（新しい文は Results に無い 7 年遠隔再発の差を Table S12 で示すもの）
- [x] Discussion の引用分布（新出文献 0）
- [x] "further research is needed" 型 0
- [x] 臨床医が何を変えるか（不変）
- [x] Implications（不変）
- [注] check_acronyms（ARS 3.24.1）: 本文・抄録とも v18 と逐字同の報告（partial: PMC、CHEERS、EQ の既知 3 件、Not checked 4 件）。Table S12 の脚注で HR、pCR を再展開
- [x] 限界は Limitations のみ（不変）
- [x] Outcome/Variables の第一文（不変）
- [x] 統計ソフト（不変）
- [x] Data availability と公開フォルダの一致（新スクリプトと CSV を公開フォルダに追加）
- [x] CHEERS の各項目に v19 の頁と節（第6節、PDF で独立照合）
- [x] 題名: manuscript（尾崎）、ESM、cover letter、README が新題名で一致。旧題名の残り 0
- [x] 事前計画、欠測、多重比較（事前計画の文は指示 b で短縮、内容不変）
- [—] 選定の流れ図: 該当なし
- [x] 図は不変
- [x] 図と表の重複（新規なし）
- [—] 著者の貢献: 尾崎の記入（不変）
- [注] AI 常套語 0、前置き 0、接続語連発 0、挿入句のダッシュ 0（本文）。30 語超の文 48（v18 46 + 指示の 2 文: Discussion 第3段落 43 語、第1段落 31 語）、最長 67（既存）。150 語超の段落 1（Introduction 第3段落 162 語、v18 で尾崎が文を追加したもの）
- [注] 裸の時間語: currently 1、now 1、current 1（v17 以来の既存）。may/appeared の誤用なし
- [x] 主張の強さ: 強くなった文 0（"How much … depended mostly on" → "What … depended on the size and duration of its effect" は指示の文）
- [—] 査読対応の版ではない
- [—] humanizer、stop-slop は使っていない

新しく足した検査の空打ち（規約13、checks_v19/out/bell19.txt、bell26.txt、footsym19.txt）
- regress19: 本文に 1 語の無断変更を仕込む → UNEXPLAINED 2（変更前と変更後）。鳴った。
- tfnum19: Introduction 第1段落に "(Table S12)" を仕込む → Table S の初出順 [12, 1, …] で不合格。鳴った。
- sec10_19: "delve" を仕込む → 1 件。鳴った。
- footsym19: Table S12 の脚注 c を消す → 一対一 False。鳴った。
- R/26 の一致検査: 局所→遠隔を二重に数える誤った式 → 収支との差 7.4e-02（許容 1e-12）で検出。正しい式は 1.5e-15。占有で数えた場合は第 84 月で 10.83 ポイント過小（指示が占有を禁じた理由の確認）。
- word_wc19: v18 で尾崎の記載 249/3,498 を再現して検証。

## 11. 著者側・ユーザー判断に残す事項

1. Table 3 の新脚注の記号は指示の英文どおり ✳。同じ表の他の脚注は文字 a〜d（BCRT 偏離）なので、文字にそろえるなら "e" になる。
2. 同脚注の "(Table S12)" も指示どおり。tables docx の他の箇所は "(Table S5 (Online Resource 1))" の形。
3. Table S12 の題、列見出し、脚注 a〜c の英文と、cover letter の要約の書き直しは CC の文（指示に英文の指定なし）。第5.3、5.4節。
4. v17 から持ち越し（今回の範囲外）: 2026-11-01 の薬価改定（トロデルビ、ダトロウェイ約 11% 引き下げ）を反映して再計算するか。
5. 公開フォルダは従前どおりローカル commit のみ（リモートなし）。Data availability の GitHub URL への公開は未実施。

## 12. 撤回した主張、共著者コメント台帳、過去に戻った箇所、文献検索

- 撤回した主張: v12〜v17 の撤回・削除項目の復活 0。v18 で尾崎が外した文（Results の Table S4 の 2 文目「Its drug cost was offset …」、Sensitivity の ICER 範囲の文、抄録の「Effect duration changed …」など）は v19 でも戻していない（Table S4 は指示 4(1) の括弧引用だけ）。
- 共著者コメント台帳: v18 docx にコメント 0、修訂 0（尾崎の変更は確定済みの本文として受領）。採否 = ユーザーの v19 指示。
- 過去に戻った箇所: 第7節の 5 点、戻りなし。
- 文献検索: v11 第11節を継承。本版で文献の追加なし。

## 13. 検査と編集のスクリプト

編集: manuscript/code/edit_manuscript_v19.py、edit_tables_v19.py、edit_esm_v19.py、edit_cover_v19.py（いずれも v18 の sha256 を確認してから word/document.xml だけを lxml で書き換え、元の文字列が 1 か所でなければ停止）。検査: manuscript/code/checks_v19/（dump19、diff19、regress19、tfnum19、citeorder19、sec10_19、word_wc19、footsym19、grep_parts19、bell19、word_finalize19.ps1）と既存の checks_v11/fmt_audit.py、refcheck.py、checks_v12/pdf_pages.py、checks_v11/word_stats.ps1、ARS 3.24.1 check_acronyms.py。出力は checks_v19/out/。ファイルごとの sha256 は MANIFEST_v19.md。
