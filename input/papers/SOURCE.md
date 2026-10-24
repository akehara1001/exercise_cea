# input/papers の出所

利用者が置いたもの（2026-10-21）
- NEJMoa1910549.pdf — Schmid 2020 NEJM 382:810（本文のみ、Supplementary Appendix なし）
- NEJMoa2112651.pdf — Schmid 2022 NEJM 386:556（本文のみ）
- NEJMoa2409932.pdf — Schmid 2024 NEJM 391:1981（本文のみ）
- eScholarship UC item 0f60710w.pdf — Yau 2022 Lancet Oncol 23:149（著者稿、PMC9455620）

利用者が置いたもの（2026-10-22）
- PIIS0923753424001078.pdf — Dent R, et al. Ann Oncol 2024;35:630-642（IMpassion132、本文）

Claude が取得したもの
- Yau2022_LancetOncol_appendix_mmc1.pdf — Yau 2022 の Supplementary appendix
  https://ars.els-cdn.com/content/image/1-s2.0-S1470204521005891-mmc1.pdf（2026-10-21 取得）

NEJM の Supplementary Appendix 3 本は nejm.org がスクリプトからの取得を 403 で拒否したため未取得。
sha256 は data/input_manifest.csv。

KEYNOTE-522 最終解析（ASCO 2026、2026-10-22 追記）
- 出典：Schmid P, Cortes J, Dent RA, et al. KEYNOTE-522 final analysis. J Clin Oncol 2026;44(16_suppl):507. doi:10.1200/JCO.2026.44.16_suppl.507。データカットオフ 2025-10-14、追跡期間中央値 93.8 か月。
- 学会抄録のページ（ascopubs.org）はスクリプトからの取得が 403 で拒否されたため未取得（回避はしていない）。数値は会議報道から読み取った：
  - OncLive 2026-06-01（7 年 EFS・OS とその 95% CI、pCR 別の OS）
  - CancerNetwork 2026-06-01（7 年 DRFS、7 年 OS の照合、データカットオフ、追跡期間）
  - DelveInsight（pCR 別の OS の照合）
  - CareNet 2026-06-02 はサイトのメンテナンス中で本文を取得できなかった。
- 保存：kn522_final_analysis/（各ページの HTML、2026-10-22 取得）。値は R/py/12_final_analysis.py が正規表現で抽出し data/kn522_final_7y.csv に出典と原文つきで保存。
- 注意：pCR 別の OS（94.5% 対 91.1%、69% 対 59.8%）は報道に時点の明記がない（OncLive は "at median follow-up" と記載）。利用者の指示どおり 7 年の値として扱う。

ESME 早期再発 TNBC（2026-10-23 追記、第九轮）
- 出典：Grinda T, Antoine A, Jacot W, et al. Real-world clinical and survival outcomes of patients with early relapsed triple-negative breast cancer from the ESME national cohort. Eur J Cancer 2023;189:112935. doi:10.1016/j.ejca.2023.05.023。PMID 37385070。
- 取得元：HAL hal-04205902（著者稿、"Journal Pre-proof"、ライセンス CC BY-NC 4.0）。HAL の検索 API（api.archives-ouvertes.fr、fileMain_s と fileAnnexes_s）が示すリンクから取得。HAL のウェブページは自動アクセス対策のチャレンジを返したが、回避はしていない（API の示す /document と補足資料の /file/ リンクは PDF を直接返した）。
  - Grinda2023_ESME.pdf — 本文（https://hal.science/hal-04205902/document）、sha256 ccf06b22a4ce9eb9ed60084964c52aec83292f79890f7a6109092387e9db8a28
  - Grinda2023_ESME_suppl_mmc1.pdf — 補足資料（https://hal.science/hal-04205902/file/1-s2.0-S0959804923002769-mmc1.pdf）、sha256 5af91d819ba62edb682764dbea8791acfb6934f296c6875b697c0ec20a426be1
- 使用箇所：Fig. 3a（p.12、転移診断からの OS、早期再発／晩期再発）を R/py/02b_digitize_raster.py（R/py/rasterspec_esme.json）で数値化し data/digitized/esme/ に保存、R/13_esme_fit.R で個票を再構成。PDF は git に入れない（.gitignore）。

利用者が置いたもの（2026-10-23）
- CHALLENGE.pdf — Courneya KS, et al. Structured exercise after adjuvant chemotherapy for colon cancer. N Engl J Med 2025;393:13-25（CHALLENGE、CCTG CO.21）。DOI 10.1056/NEJMoa2502760。本文 13 ページ。sha256 cc531c2cd7d6e079d549025ef2907f8bc92e3bdcaf15d32deb44f518bf44fccb
- CHALLENGE_supplement.pdf — 同上の Supplementary Appendix（83 ページ）。sha256 965353e4512a35263a76650dffde44f348235481ffa8b5d1c6dbb1c8493ac91a
  - 使用箇所：本文 p.19（Results の Safety：as-treated 428 例と 461 例、筋骨格系有害事象 79 例と 53 例）、補足 Table S4（p.77：Musculoskeletal (total)、Any Grade と Grade ≥3）。R/py/16_params_v6.py が読み取り、入力表 v6 の E06、E07、E09、E10 に記入。
- KN522_final_ASCO2026_abstract.pdf — Schmid P, et al. Neoadjuvant pembrolizumab or placebo plus chemotherapy followed by adjuvant pembrolizumab or placebo for high-risk early-stage TNBC: Final analysis results from the phase 3 KEYNOTE-522 study. J Clin Oncol 2026;44(16_suppl):507。DOI 10.1200/JCO.2026.44.16_suppl.507（ASCO 2026 抄録、1 ページ）。sha256 533add7c3de37c72e3d5e94617f9579be1281c091345aa103445307beec18be1
  - 使用箇所：全体の 7 年 EFS と OS（95% CI）、HR、データカットオフ、追跡期間中央値（範囲）。R/py/12_final_analysis.py が読み取り、会議報道から読んだ値と一致することを確認（data/kn522_final_7y.csv の *_abstract 行）。抄録には pCR 別の値はない（pCR 別の値は引き続き会議報道による）。

利用者が置いたもの（2026-10-23、第十四轮）
- Fedele2026_BCRT.pdf — Fedele P, Rizzo A, Landriscina M, et al. Early first-line systemic anticancer therapeutic attrition after metastatic recurrence in triple-negative breast cancer following neoadjuvant chemo-immunotherapy: a multicenter real-world study. Breast Cancer Res Treat 2026;218:8。DOI 10.1007/s10549-026-08023-2。9 ページ。sha256 c9c79c715cd27dd6b0b5e4810fd664de4db9be30313ed6511b18429b4e8ade33
  - 使用箇所：p.4（転移再発 54 例中 52 例が評価可能、90 日以内に一次治療を始めなかった 17 例と始めた 35 例、無病期間の中央値 7.4 と 14.3 か月〔Table 2 も p.4〕）、p.5（再発後 OS の中央値 3.4 と 12.4 か月；抄録 p.1 も同値）、p.3（追跡期間中央値 24 か月、209 例中 54 例が転移再発）。R/py/17_fedele.py が読み取り data/fedele2026.csv に保存、R/17_round14_kext.R が第十四轮の情景「早期再発後 k（外部）」の k を計算。
  - 注意：抄録は「17 of 54 evaluable patients (32.7%)」と書くが、32.7% は 17/52 で、本文 p.4 の評価可能 52 例と一致する。52 例を用いた。
