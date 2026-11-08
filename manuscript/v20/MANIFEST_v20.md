# MANIFEST v20（2026-11-07）

- 版: v20。交付日: 2026-11-07。
- 底本: v19 交付物（manuscript/archive/v19/、MANIFEST_v19.md）。
- 内容: Discussion の "about" 削除、Table 3 脚注 e（記号・位置・英文）、Table S12 の題と脚注の差し替え、cover letter の要約の差し替え、語数行 3,498。数値は不変。作業ログ兼監査 = AUDIT_v20.md。
- 数値の出所: output/phase2/main/recurrence_reduction.csv（867c0eba、v19 と同一）。他の数値の出所は MANIFEST_v17 の 71 ファイル（v19 で全件一致を確認、本版で解析の再実行なし）。
- 公開フォルダ: 変更なし（exercise_cea_public HEAD e23e167、push しない）。
- 比較文書: manuscript_v20_BCRT_track_from_v18.docx は尾崎の v18 → v20（Word の文書比較、語単位、修訂者 Akemi Hara、修訂 26）。

## 交付物（manuscript/v20/）

| ファイル | sha256 |
|---|---|
| manuscript_v20_BCRT.docx | 1e0f181a6da162c59cb8f3ccc737c3c4a09f3d5467cae6a42abfc6396a56494e |
| manuscript_v20_BCRT_track_from_v18.docx | 715a88dd3ac69202b0f7fa9fb5374dea85efeb727fbc39c80d8a74eaa0c9390b |
| tables_v20_BCRT.docx | 53f6ecc3647ab364a642d0692cb52ed4e73415a49ef2e3fce7b4832660429cb1 |
| ESM_1_v20.docx | 2da3ba0f52af85dff2861a24282abfb8d63744597c84df988c5525200628c406 |
| ESM_1_v20.pdf | d4acbce7099933972dd7a71e1fe12d692cd9a062ffc91d33dd87d2a1f677ecb8 |
| cover_letter_v20_BCRT.docx | bfc26673b8f16ea87a3856a66b7a251ea2966c6b120302044dac2ce3326c6769 |
| Fig1.tif | c13b748ed3c7d5880f81da06e5ae9c4cccf8d6285c2108c7b0be1c5c04d78543 |
| Fig2.tif | 662046bf6a3d4847b0a0992324e2cbe902981dc2dab4f16fd96d6006a5d8b3d7 |
| Fig3.tif | d7926e1e9d8664dcb69188bcc253bc98cda25bc9347927d256abe826fc54ea8a |
| 26_recurrence_reduction.R | 4e2f2ebc84b44549437480e8db7aad9653655d38144de2f6088f138d47891729 |
| recurrence_reduction.csv | 867c0eba389ab175d30dd0a6bf8dc9e03f41c873274083773dfdb29e8086c047 |
| AUDIT_v20.md | 2dea6418d22c9df15e7b9493506149b4832e2f90ca24387923a5d6d5b0f4b602 |

ESM_1_v20.pdf は Word（SaveAs2, 17）で書き出し（49 頁）。

## 底本（manuscript/archive/v19/）

| ファイル | sha256 |
|---|---|
| manuscript_v19_BCRT.docx | c40f9ed6d1796c72168580b964759f0d1ca5a453016a24efa07fd2e0215194bc |
| tables_v19_BCRT.docx | 3fc3f4561a3e1fd57fa22578b5606daa90b9c38aaced34680b98d7c2cd2f8d90 |
| ESM_1_v19.docx | 9ef39de95fb519ad646b3e5e83c487676237e8d1cbc4e1424e189c2accfd7fb2 |
| cover_letter_v19_BCRT.docx | c9e56b226a81e14ee7bee79f03ca1a36a5582d560d7b6dff9241d822c7a83631 |
| AUDIT_v19.md | 7442db755040d79ca85dfefd08d7bc3e3efdd80484bf32ed5c515ad5b107858f |

## 編集スクリプト

| ファイル | sha256 |
|---|---|
| manuscript/code/edit_manuscript_v20.py | f9f2010a82c20634882fbc0c44db6b8d48d83513306fe6b18c5d1750c1d01772 |
| manuscript/code/edit_tables_v20.py | 421f797102d6a964ebebe8f98d144516a7aadea0a139966e603d2f553d3decab |
| manuscript/code/edit_esm_v20.py | 330f8df73ea4d272b2b2570f53e7d141e27cccdfb60af1458a0a1627fc05c5e3 |
| manuscript/code/edit_cover_v20.py | 9ad20698fd1563596d9d132bf72ae47ab9c5543e8acf0ef58d7dcd31a94363ce |

## 検査スクリプトと出力（manuscript/code/checks_v20/）

| ファイル | sha256 |
|---|---|
| tfnum20.py | 6e1f26cf280dcab51cf0baaf1f107bc76842429c651c73a19adbdf0db78e887e |
| citeorder20.py | db44cc362098f04e08aa834fb766bbc2ddcc80e33d41ba42b3de28836352cc1c |
| out/r20_manuscript.txt | 1c64e7d15e6b68bcccd96fee09e2a08826772f8b967f7c6c41217a8f3f67aeeb |
| out/r20_tables.txt | 029bcf62d53e6b866ee66c80d395ceec902dde16844ed1db6bbc6dfd2135d127 |
| out/r20_esm.txt | 0a3ce6d197db9a27c32692560d177acf03a184c54d5f194d1db15370754a3478 |
| out/r20_cover.txt | 1297b9765c3dbd49370e6356071b5dc5236017603145e30d50a2aebddff18147 |
| out/tfnum20.txt | b89238bee0f61c204c14c9acb156c1d4c4f87f1418cd161251f83657e1c23804 |
| out/citeorder20.txt | 3e4672fed6e528ecb9ff601859b7a5d7acfc8dbaf636b495636871fb68e2b319 |
| out/refcheck_v20.json | e9e076534957e320284cb01a535e0752e987c56cf30185dfbbf5bcf49cfb26a3 |
| out/refcheck_v20.txt | d4b05907ede54f0e36fd63dc86969b7e406cb0dd04a94db84f01d29a2d1bd05d |
| out/pdf_pages_v20.txt | 9409ddea09ed00a5a88de0ec58b02935817b1eb644901865df7919b338a3f9d0 |
| out/m20_stats.json | e6739ef740c640cd7078baa2817772cb15cb9407f2624e963134e11d11b9158b |
| out/m20_log.json | 0349c523548595f8c9e8d08866b7873e3df61e1c31a69421b9c33156bbe5ca1d |
| out/t20_log.json | 6ced3fa1d0f6ccec432b0f9d8be508bbcc5b71c39fbfa0450b58ab044edca14b |
| out/esm20_log.json | d0af22011c71e0263031628130d4cb0f3fce6a986fc977bb79b2db086631accd |
| out/cl20_log.json | 7f283502384fa0acfbc1848dedeaff5180cee1b91cd54524da89fc0050d43fb6 |
| out/word_finalize20.json | 18a7ed79fbbdaa09b85272f1ed4e6676f012f8abf2c657444009e2c41368450f |
| out/sec10_v20.txt | 172c7151aca445f3567f7513069b17943c6facf82f323bc0b951915c26126ba3 |
| out/fmt_m20.txt | 3c034d9d521b5d1feee05661ad67dda79cecec0e4396aebfccd0cd551b45325e |
| out/fmt_t20.txt | c14ba3a222fa854d53a70333df25267f671754674d9cd9c97301ce7c281b91c2 |
| out/fmt_esm20.txt | 53745286a6647ee6131b587e4d2ef5f2228d504bf047cc0e081792f104118ac3 |
| out/fmt_cl20.txt | edd29d57f1ad7570dd7fadafa2a2c01358896e62bf5a45ae56d27104f693223a |
| out/acronyms_body20.txt | 113829bb0f7d95fff1e5a32c1c89d080fbaf32c82ed5a26ebd3ae692a7a0e651 |
| out/acronyms_abs20.txt | 9ba96b2f1e58e113506a518682bf5725459b07cce54799f0d5802e124f5bd34b |
| out/bell20.txt | a19cb5c820a5a12640371d759affa86ef66295113cda48fcc15fc689412f2d85 |
| out/report_texts20.txt | b95f5dccee178b6c270f013bfa7ee3ea6a0c18f7e16b5273968743d9ac6f885c |
| out/diff_m19_m20.txt | 221df28134322068a9d5223bb1d4012a6e23deefd372344a4000da570940f416 |
| out/diff_t19_t20.txt | 5d1727042f3e54e5d8bdabc6877552006749300dbfe3287c85afd9921692e1a0 |
| out/diff_esm19_esm20.txt | ac990e89b3b9a102bb0db0d14525dc224bf18d31c08e1e921a092298313b6bdf |
| out/diff_cl19_cl20.txt | dd3d14e4278082a57d2fe565354e4227fae7305f00c3aa27c87e3659cc08aa27 |

## 後記
- AUDIT_v20.md の sha256 は上表に記入済み（2dea6418d22c9df15e7b9493506149b4832e2f90ca24387923a5d6d5b0f4b602）。MANIFEST_v20.md 自身の sha256 は git commit に記録。
