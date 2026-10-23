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
