# MANIFEST v19（2026-11-07）

- 版: v19。交付日: 2026-11-07。
- 底本: v18 一式（manuscript = 尾崎が v17 本文に手を入れた manuscript_v18_BCRT.docx、他 = v17 交付物の逐字節コピー。manuscript/archive/v18/MANIFEST_v18.md）。
- 内容: Supplementary Table S12（再発の絶対差）を新設し、本文・Table 3 脚注・ESM・cover letter・CHEERS を v19 指示どおり更新。題名を統一。作業ログ兼監査 = AUDIT_v19.md。
- 新しい解析出力: R/26_recurrence_reduction.R → output/phase2/main/recurrence_reduction.csv（Table S12、Table 3 脚注 ✳、Discussion 第3段落の 0.14 の出所）。他の数値の出所は MANIFEST_v17 の 71 ファイルで、sha256 を 2026-11-07 に再計算して全件一致（変更なし）。
- 公開フォルダ: exercise_cea_public にローカル commit e23e167（R/26_recurrence_reduction.R、output/phase2/main/recurrence_reduction.csv、README）。リモートなし。
- 図のファイル: Fig1〜3.tif（v17 と逐字節同。図の docx は無い。図注は manuscript 末尾）。

## 交付物（manuscript/v19/）

| ファイル | sha256 |
|---|---|
| manuscript_v19_BCRT.docx | c40f9ed6d1796c72168580b964759f0d1ca5a453016a24efa07fd2e0215194bc |
| manuscript_v19_BCRT_track_from_v18.docx | fcf6b7fbfd30fd8856b5176e57d9fa41137575815a87d47af454711c3fae6feb |
| tables_v19_BCRT.docx | 3fc3f4561a3e1fd57fa22578b5606daa90b9c38aaced34680b98d7c2cd2f8d90 |
| ESM_1_v19.docx | 9ef39de95fb519ad646b3e5e83c487676237e8d1cbc4e1424e189c2accfd7fb2 |
| ESM_1_v19.pdf | fc79cfc1a35d456255d980cc4a80057642b2349b4dd6326a4da384ed756da809 |
| Fig1.tif | c13b748ed3c7d5880f81da06e5ae9c4cccf8d6285c2108c7b0be1c5c04d78543 |
| Fig2.tif | 662046bf6a3d4847b0a0992324e2cbe902981dc2dab4f16fd96d6006a5d8b3d7 |
| Fig3.tif | d7926e1e9d8664dcb69188bcc253bc98cda25bc9347927d256abe826fc54ea8a |
| cover_letter_v19_BCRT.docx | c9e56b226a81e14ee7bee79f03ca1a36a5582d560d7b6dff9241d822c7a83631 |
| 26_recurrence_reduction.R | 4e2f2ebc84b44549437480e8db7aad9653655d38144de2f6088f138d47891729 |
| recurrence_reduction.csv | 867c0eba389ab175d30dd0a6bf8dc9e03f41c873274083773dfdb29e8086c047 |
| AUDIT_v19.md | 7442db755040d79ca85dfefd08d7bc3e3efdd80484bf32ed5c515ad5b107858f |

ESM_1_v19.pdf は Word（SaveAs2, 17）で書き出し（49 頁）。track は Word の文書比較（v18 → v19、語単位、修訂者 Akemi Hara、修訂 28）。

## 底本（manuscript/archive/v18/）

| ファイル | sha256 |
|---|---|
| manuscript_v18_BCRT.docx | d26656694a8712192a47501d2fd6c0276f59915530ffb011d4fb2083d6ec93cc |
| manuscript_v18_BCRT_track_from_v17.docx | cf7f5e9433307cad802f454b27ba84e1910a31fd372632fe3557a20bd93e2ef1 |
| tables_v18_BCRT.docx | 8236a3eee6495976fd4f07a2ed8945762fc9570f8b674cc807f610ca0c79c4e3 |
| ESM_1_v18.docx | 642590a6b691dea92f27d86d7397733cc73f6504f091acd62d62da9fcfd8775e |
| ESM_1_v18.pdf | 826fb01aec5761c150cdda802dfe707646c4ae5596b94a7e542100aed072a746 |
| Fig1.tif / Fig2.tif / Fig3.tif | = v19 と同じ |
| cover_letter_v18_BCRT.docx | 21ed7f1aa387e8b7e9e3015f97c0c44f4f50b10dd58fa334e7fdf907bd37b935 |
| MANIFEST_v18.md | 65a3682831b211d35189176a6d3845f0104b8811306901737e26bfe7f49f03f4 |

## 解析出力（本版で新設）

| ファイル | sha256 |
|---|---|
| R/26_recurrence_reduction.R | 4e2f2ebc84b44549437480e8db7aad9653655d38144de2f6088f138d47891729 |
| output/phase2/main/recurrence_reduction.csv | 867c0eba389ab175d30dd0a6bf8dc9e03f41c873274083773dfdb29e8086c047 |
| output/phase2/main/recurrence_reduction_checks.csv | d88dc07d673ce90f5c24830fe7fe155d3a912fda5aecf53c9945e2da002f7bff |

## 編集スクリプト

| ファイル | sha256 |
|---|---|
| manuscript/code/edit_manuscript_v19.py | a56dd141e2746ece14dc8b413642bb0c7e0c0159ac3f06f4ee72462c297d7d88 |
| manuscript/code/edit_tables_v19.py | 78d3c1f42dbabe4f7f055b54cd39bc674066cab582b0ba639e75d453e44280ec |
| manuscript/code/edit_esm_v19.py | 2631e0baca6d9c192c0f5dc2d74dd7db3456f042c729bb9983c0af474556307b |
| manuscript/code/edit_cover_v19.py | b01451d83bfb975add8dff08e0f089727f0c10869684e5e4dbd9407dd4c327ee |

## 検査スクリプト（manuscript/code/checks_v19/）

| ファイル | sha256 |
|---|---|
| bell19.py | 4f3837724cb1ada55bb3c0726bcc286705f25e74b258637c93836d6a912f4689 |
| citeorder19.py | 3774403bbbda588bff3d457fae155b2d41c4303b7640d0d6ccbe282924389d90 |
| diff19.py | a020c1df54ae0b94cfc21a5053354a70fd951d28f4f076ca8554d30f0dbf8e17 |
| dump19.py | 699b971aaf7556807440ff6109429b53df34898d172aa3e7db8b5ff7b99fbaf1 |
| footsym19.py | d41e5f0bef1a907f8e7800e635d0f078fb33fb3032633795c35de08efb40eacd |
| grep_parts19.py | 01738ba6f462b03ee8a99eb571e99d4c3d7a11d44351fce341d3687ace9da12f |
| regress19.py | 2a3b1974329e67961e7055f3700dfe75e37703fd833710434c17d8a4fb8e0afe |
| sec10_19.py | 4ca6a0daa66818946a8ffdd0393803cf2efe30749a485d142fa9d0198c1fe28b |
| tfnum19.py | 79ac9d85e0efb169dc286e3ef8b357f0957797d3257683a4e940bb3ad8938b93 |
| word_wc19.py | 82b30c1a738873ed157c2b7aac474ca8900038f5f6c584a747961cda65c74cbb |
| word_finalize19.ps1 | 115d1cdb176a564425f85dfbee2028eeee3b0b3e37e81261488357605b4e3c4b |

## 検査の出力（manuscript/code/checks_v19/out/）

| ファイル | sha256 |
|---|---|
| r19_manuscript.txt | 7b5acda4878a51937157e4acd3cd00dc7f35af9a5cf39074691635612d71a2b2 |
| r19_tables.txt | 4ed22cff1cf633a098f9041f01c89512d6016204655c99c8cc22762daa0b5a67 |
| r19_esm.txt | 3bc25d50de6863ebcf5043592266e7053d9c39881f9007aceadebe7fc0665970 |
| r19_cover.txt | 6f2e7ae9154f4c7c8134690dc90277786d115fddc27b5f71668e7fcef693cb76 |
| tfnum19.txt | b89238bee0f61c204c14c9acb156c1d4c4f87f1418cd161251f83657e1c23804 |
| citeorder19.txt | b7e2762345ea2a598fe86d18bc7bbe4b55e5489d06dc6c45b2184c7b600f0c73 |
| refcheck_v19.json | e9e076534957e320284cb01a535e0752e987c56cf30185dfbbf5bcf49cfb26a3 |
| refcheck_v19.txt | d4b05907ede54f0e36fd63dc86969b7e406cb0dd04a94db84f01d29a2d1bd05d |
| pdf_pages_v19.txt | 9409ddea09ed00a5a88de0ec58b02935817b1eb644901865df7919b338a3f9d0 |
| m18_stats.json | e12461b7e7301693f65e426897f9725e9e5c4cc25d2570d4d26bd5d83a5c01d0 |
| m19_stats.json | c9b1f051e6e5864e7ad2b55085d02e7c904166c9779d7544fccceeee635b1041 |
| m19_log.json | ab63f8729e8c8a3c447507bdd6cc5fbe84099a95c71e5b5e1a5c18070f58b90e |
| t19_log.json | 5714de51be0a48492b989b8c05c36d2796ef02e4c370d54f45acbdda2edc3545 |
| esm19_log.json | 076ca0335390a1dd0522b8978cc70ca120f98e7eda42cdf2e8205cb1ca573ffc |
| cl19_log.json | 626e99de32d6799cbea6d8c685a9901e8ba63c769dd623dd44441ffe6ba1f92e |
| sec10_v18.txt | c57cb2990042a0209190ed63afbb8145069daa8fd8a6071e982ba5c3c636ebae |
| sec10_v19.txt | e69237dff80aaa641d737a95135006cdfaec6b6e5f38cfd55305d65dc149cd5f |
| fmt_m19.txt | 3c034d9d521b5d1feee05661ad67dda79cecec0e4396aebfccd0cd551b45325e |
| fmt_t19.txt | 9953460df9103811f726b0265c705733d0de9cf18539dc7e95fb540b82132135 |
| fmt_esm19.txt | deb21b016b2bba0bf451698cfb7b80be021e78f4f857fd96c4469179483aa9a4 |
| fmt_cl19.txt | edd29d57f1ad7570dd7fadafa2a2c01358896e62bf5a45ae56d27104f693223a |
| acronyms_body19.txt | 113829bb0f7d95fff1e5a32c1c89d080fbaf32c82ed5a26ebd3ae692a7a0e651 |
| acronyms_abs19.txt | 9ba96b2f1e58e113506a518682bf5725459b07cce54799f0d5802e124f5bd34b |
| footsym19.txt | f47b96539418e37e9108c4ad991418921664b532ca9a0e3d77d6806df9ee8ded |
| bell19.txt | 0cb9e146ed721267fa2cc28106a5dff5e2af70e9b22399c0dc557e27c25f9c27 |
| bell26.txt | 99f4cca3936832f039c9de6bd1a867fbe33b16b1de071122b07d5424e5e68729 |
| diff_m18_m19.txt | b033ac4c19d88b5cfeb7c7956ed5ecf16611489f13d2cca19f0b3e20f60bf7e6 |
| diff_t18_t19.txt | bb42bc851c69c48ba76ef48ea2f9dc251c2b6bafbefbe11551fa8673038d5ad5 |
| diff_esm18_esm19.txt | eee8ddf28e3956dbea8cb40d27346934fe67dece352a4288828f3ba5972bf43d |
| diff_cl18_cl19.txt | c61eab4306786f5697e59c93d59b61923a278419b26bbb33b009ed27a8f26b0b |
| diff_m17_m18.txt | 5a49676dd081a4b4815135148e1feafc15b6c8f04e84111cf3a628d1199190eb |

## 後記
- AUDIT_v19.md の sha256 は上表に記入済み（7442db755040d79ca85dfefd08d7bc3e3efdd80484bf32ed5c515ad5b107858f）。MANIFEST_v19.md 自身の sha256 は git commit に記録。
