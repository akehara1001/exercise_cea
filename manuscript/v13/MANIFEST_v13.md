# MANIFEST v13（2026-10-29）

- 版本: v13（v12 的小修: 指示第 1 步 manuscript 1a、1b；第 2 步 ESM 页码核对，无变化；第 3 步公开代码完成；结果数值不变）。
- 交付日: 2026-10-29。
- 底本: v12（2026-10-29 交付；现在 manuscript/archive/v12/，下表）。会话开始时 9 个交付物的 sha256 与 MANIFEST_v12 一致。
- tables_v13_BCRT.docx、ESM_1_v13.docx、cover_letter_v13_BCRT.docx、Fig1〜3.tif = v12 的逐字节复制（下表 sha256 与底本相同）。ESM_1_v13.pdf 由 Word 重新导出（46 页，文字与 v12 逐页相同；sha256 因生成时刻不同而不同）。
- 数值来源: 第 1、2 阶段的输出与入力表 v10，未重新计算模型；来源文件 57 个，sha256 于本版重算，与 v9 数值台帳第 8 节全部一致（下表）。
- 文献: 78 条（正文 1〜71，72〜78 只在 Table 1 与 ESM）。核对结果见 worklog_v13.md 第 6.3 节。
- 公开用代码（指示第 3 步）: C:\Users\原明美\Documents\ClaudeCode\exercise_cea_public\（作业树外）；本地 git commit 4d8e2ad（"R code, input sheet and reconstructed patient-level data of the exercise cost-effectiveness model"）；105 个文件；无远程、未推送。清单与 sha256 见 manuscript/code/checks_v13/out/public_files.txt（worklog_v13.md 第 7 节）。

## 交付物（manuscript/v13/）

| 文件 | sha256 |
|---|---|
| manuscript_v13_BCRT.docx | 4178320b77709506683585a3876e895d09014bf9c07217bc7f3db04c21a9c2b4 |
| tables_v13_BCRT.docx | d022962f64dd85a5c4377294a82fbe6d56e7cc3d020f7de3805e84f71747c54a |
| ESM_1_v13.docx | ae84d2f68ff5ccac9fd62b1e04bbbfcc386d3bc946ca6d86fd939ead0dc89f7f |
| ESM_1_v13.pdf | 5e1aeac67dde038b2e7401234629dba85ce34b2825db6ae4337b693f1e36d13c |
| Fig1.tif | c13b748ed3c7d5880f81da06e5ae9c4cccf8d6285c2108c7b0be1c5c04d78543 |
| Fig2.tif | 662046bf6a3d4847b0a0992324e2cbe902981dc2dab4f16fd96d6006a5d8b3d7 |
| Fig3.tif | d7926e1e9d8664dcb69188bcc253bc98cda25bc9347927d256abe826fc54ea8a |
| cover_letter_v13_BCRT.docx | 21ed7f1aa387e8b7e9e3015f97c0c44f4f50b10dd58fa334e7fdf907bd37b935 |
| worklog_v13.md | bf8d88c5c77ece8bf14aca3f972ab1f853ee6ca0a2bbf045ba8e7e28220541a7 |

## 底本（manuscript/archive/v12/）

| 文件 | sha256 |
|---|---|
| manuscript_v12_BCRT.docx | 3e2940475772e678e213c23c1843ec478f1c9f7271d4f0b301acd4a085b1e39f |
| tables_v12_BCRT.docx | d022962f64dd85a5c4377294a82fbe6d56e7cc3d020f7de3805e84f71747c54a |
| ESM_1_v12.docx | ae84d2f68ff5ccac9fd62b1e04bbbfcc386d3bc946ca6d86fd939ead0dc89f7f |
| ESM_1_v12.pdf | 8174761bc204c40a3f58fb8cb07a1a26f64b3c07a531d79089baa173a8f78ec7 |
| Fig1.tif | c13b748ed3c7d5880f81da06e5ae9c4cccf8d6285c2108c7b0be1c5c04d78543 |
| Fig2.tif | 662046bf6a3d4847b0a0992324e2cbe902981dc2dab4f16fd96d6006a5d8b3d7 |
| Fig3.tif | d7926e1e9d8664dcb69188bcc253bc98cda25bc9347927d256abe826fc54ea8a |
| cover_letter_v12_BCRT.docx | 21ed7f1aa387e8b7e9e3015f97c0c44f4f50b10dd58fa334e7fdf907bd37b935 |
| worklog_v12.md | 1eb5f8b3a0fc41d84fb04d1f34e74e23ed583157b37a41223afbf285838998dd |
| MANIFEST_v12.md | d8603ce234ff59a9febef5bf85b3255b2fecf871e9ab05239cf5b4a9c8cca454 |

## 编辑脚本与公开入力表脚本

| 文件 | sha256 |
|---|---|
| manuscript/code/edit_manuscript_v13.py | 891b5a6431aad9be8e9a80caf5276603e762c394caea672030d3c5d152ea26a6 |
| manuscript/code/edit_esm_v13.py | b6b285bdf3d22867eb85171c4172f8c7ce98276c169aaba75b411c91712a3f8c |
| R/py/26_public_params.py | 1d9c478d5ca3041323da11a4b9445ca98d34be83150b0d02f1ea698e3cc0c2cc |

## 公开目录中本版新增或修改的文件

| 文件 | sha256 |
|---|---|
| README.md | 01a621838886f869a368f5015fece6a3d5425f33f3c00a1df9ec14d732842870 |
| LICENSE | d961790572a7e0572c5144a973334f30dbf856c6ff00db04f1dc427254815f4f |
| input/params/parameters_v10.xlsx | f0e36eff915824638dfbcb248500ec9f05d4a439d042e95bd9444026a576007d |
| R/engine.R | 5366f404314696c2761adf5978bd93b5ddf9ca9dc0df8fd47185a772c72b52ce |
| R/22_phase2b_main.R | a9b9787756ab56c31488610d845f1cee4428d9c82b8820d5d850cd8adb2a3728 |
| data/params_utility/utility_scenarios.csv | 84db7722a657933a5d62007b8f49d5317b91316c1af663531e50cb3b5aa36da0 |
| data/reported_values.csv | 7d8a8cff70d896108e6d2319f27e299a009285414d5523d65c0530e3949eddb9 |
| R/py/rasterspec.json | 894262b76decb7d81a3f08d51ff3ffca891c848317abc86303eff538619461cf |
| input/user_supplied_values.csv | 0b59998e85118b699c6316dd698b916ef69379502b4ffeaf265265c9194cd5e6 |

## 核对脚本与输出（另用 manuscript/code/checks_v11/ 的 regress.py、regress2.py、refcheck.py、fmt_audit.py、sec10.py、word_stats.ps1、word_open_pdf.ps1、word_wc.py、citemap.py，checks_v12/ 的 pdf_pages.py、compare_outputs.py，未改）

| 文件 | sha256 |
|---|---|
| manuscript/code/checks_v13/citeorder.py | 55cc7502727c901eea1ab290e3d0cb2f61b7f07013ed9476b048039ea1849338 |
| manuscript/code/checks_v13/cmp_ipd.R | af68504a463a5bf4277b8908ed08254209adca1310c5396b2ef3a60e50063fb0 |
| manuscript/code/checks_v13/compare_v13.py | ff394967ccb90c385e5a96f0d4fdbd1cd7a7afb3fd309e0361d1979c378330ed |
| manuscript/code/checks_v13/public_files.py | 5824c916eec33fb2e7a8cf2c9d46348e7a6613f5dbbd1c3427eebf1b99f91b19 |
| manuscript/code/checks_v13/public_name_scan.py | ab9bcbbf8d1db251cfbf3903f918c4acc6dc806e8472e715216cfcb46cf7d6c7 |
| manuscript/code/checks_v13/rds_strings.R | da7b9d08dfddf4034f1c77d864d8174c52f041676c439d5db50f389534a36936 |
| manuscript/code/checks_v13/tfnum.py | fc730e7d16308e1bdcd03ec37f0c281d88cb3cda2ef11884978634f425dadbda |
| manuscript/code/checks_v13/out/acronyms_abs13.txt | 9ba96b2f1e58e113506a518682bf5725459b07cce54799f0d5802e124f5bd34b |
| manuscript/code/checks_v13/out/acronyms_body13.txt | 113829bb0f7d95fff1e5a32c1c89d080fbaf32c82ed5a26ebd3ae692a7a0e651 |
| manuscript/code/checks_v13/out/citeorder.txt | 342926c288a0b8d273917e3e4fe6b34814e770121eadd9debf48e95dd7dc71d8 |
| manuscript/code/checks_v13/out/cmp_ipd.txt | 11bb5eba84b5dab095ca8a0a02510d993bd2279432b3a11983fa7aed3b49f4dc |
| manuscript/code/checks_v13/out/compare_v13.txt | 9499bd496b46751f50aa61a2882f36f536f28fc06ddb961f26a2b26b7b1917ac |
| manuscript/code/checks_v13/out/esm13_log.json | a10e2ed8b7bb5beda2300ebc774324c7d3338d27132f63384512786b295046a0 |
| manuscript/code/checks_v13/out/fmt_v13.txt | 5c4a0e164474b0b449e38ac34cbd19a31ed64a82af7ce457e338bfdfe44e803e |
| manuscript/code/checks_v13/out/m13_log.json | 2b6332f6276729772c50fa4922ae8b667119cc9bed608018f9d444bb75b11f14 |
| manuscript/code/checks_v13/out/m13_stats.json | 2915cc1879bfa67d5837ca732f64d9b7ceefd9e334e8c6b069139b1ba8f22984 |
| manuscript/code/checks_v13/out/pdf_pages_v13.txt | 048ea75c2ce2eb26d27dfeb1c9b9b23f3432d55020355741807bdaf465668157 |
| manuscript/code/checks_v13/out/public_files.txt | f58f7d761c9e72376532a9af2931e4c6710b7269f594e49c0cc634814c084c17 |
| manuscript/code/checks_v13/out/public_name_scan.txt | a1a147b4fd8c611d95533ec3191394caef690ce296f019e90c34fca6446d07e9 |
| manuscript/code/checks_v13/out/r2_manuscript.md | 96b4e33d2a756888f23ba12d313eb3ddd93fc4bfdab9fe85d489211a1953d79e |
| manuscript/code/checks_v13/out/r_esm.txt | 56d754c8f6c61294a55994ef1df09aff94ebf5a21eb00a13d648052ff0ed67a1 |
| manuscript/code/checks_v13/out/r_manuscript.txt | 0b1bcbe3ce5fa4749135506dd12521042e0c41d4b0bd6525d027c78753ec3ddf |
| manuscript/code/checks_v13/out/r_tables.txt | 1605a301a2d2d3480b2ff764ca3435401478a5836710f41295802e660c7e8684 |
| manuscript/code/checks_v13/out/refcheck_v13.json | ef1312d73d5912e2b9aaa0d64f857a96878505324cf54d1e3d8e68a5af2943f8 |
| manuscript/code/checks_v13/out/refcheck_v13.txt | 3c6f505ad318c9666ac0a827a3bf7d2dfac2ee8fe5a551b9d2847cfc4415c78c |
| manuscript/code/checks_v13/out/run03.log | f52577bec7682b673a2c9e1d851478b20de4b1a901243064c3173abf08532149 |
| manuscript/code/checks_v13/out/run_00_lifetable.log | a7e27658c44c14af4d746f7ed24066dd1d71e95675d7a454fe020814ddd583b7 |
| manuscript/code/checks_v13/out/run_10_read_params.log | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| manuscript/code/checks_v13/out/run_det.log | 366b47e45b572a12638d775d1bdd00dd26ebb3b8865754b3e8b21ced22b39cdb |
| manuscript/code/checks_v13/out/run_plan10.log | e858c658f26753bd0b5f29b3feec287ee7518cb554c01cc5126a5afec4095a15 |
| manuscript/code/checks_v13/out/run_plan9_det.log | 088d8b0a95a2673eeea0838b1034a1907e6f449157942ba2857cf7fea38925d0 |
| manuscript/code/checks_v13/out/sec10_v13.txt | 386f7f79215fba4a779a427b898f4fbc94ad65de3ee42fc08ddbe6778a73af74 |
| manuscript/code/checks_v13/out/tfnum.txt | 91b377a733dd6c59405879ea0ee5de4a79600b0ac64e12d207575be7e0ebca44 |

## 数值来源文件（v9 数值台帳第 8 节的清单，sha256 为本版重算值）

| 文件 | sha256 | 与 v9 台帳 |
|---|---|---|
| `data/ipd/K24_F2A_EFS_pembro.csv` | 55c68dee37923aeea2aa44c7098a9307cf643c456fafbc193614aaef2ad903d8 | 一致 |
| `data/ipd/K24_F2A_EFS_placebo.csv` | c11b24f5ea47fc1651054fba33f71fa4e2232a068c99d32b5025eca1dbf0568f | 一致 |
| `data/kn522_final_7y.csv` | 0f40a51bb51c1d412e7e6ee578c3cd98631980df61d8a1e12e3d193aafe3258a | 一致 |
| `data/lifetable_female_2025.csv` | 213403bd92ac2669014a8b4edfba3210ed334c51031bf92e1a7bb87049fed733 | 一致 |
| `data/params_dist.csv` | 3b8e10fcc27eb396dd7c3738dedd22f4ba6a1abe2ae60e14d7cf22841960b8b2 | 一致 |
| `data/pcr_counts.csv` | 0d8cf779b0ffd827981d87e926ddc74b4483ab54ca02b5c1c47ebe88f9d030c1 | 一致 |
| `docs/analysis_plan_phase2.md` | 7d386c574d7933de88cd1749f1b53ef64ccf8b6188acb6de03205f66ade9c41a | 一致 |
| `docs/model_spec.md` | cb734ba8237fa77c54054866861a6a6b0026036be81a9b023bdd8c408b30e0a9 | 一致 |
| `input/lifetable/SOURCE.md` | fdd7eda82464824d8c9d80c544b7802adf54300f1addc0f80005eccee2d6d5e9 | 一致 |
| `input/papers/CHALLENGE.pdf` | cc531c2cd7d6e079d549025ef2907f8bc92e3bdcaf15d32deb44f518bf44fccb | 一致 |
| `input/params/cohort_N_jbcs2024.csv` | 8dd976c1e47643e612feb0ee866e58f0a5cfd59347f1f4fb362b5fdc01d71f10 | 一致 |
| `input/params/parameters_v10.xlsx` | 5e9396531d92fc8d8b0a0cbcf59aafcc6307676be5b48f8e09965088aae34510 | 一致 |
| `input/params/sources_utility/utilities_scenario_jp.csv` | 59c1ac7f4de93e67fcd7b04b5e605eb71d2f38987f6a0623eb32889c98180448 | 一致 |
| `manuscript/code/_build/engine_params_extract.csv` | 7aef325510f7d6241f17b9bc8bc34517a7d352667375d2752dc0679c4142a089 | 一致 |
| `manuscript/code/references.py` | 78ebb37a6c90008ba0ffd8f1b0e6c26e79b5ca026cff1940f89f1bbc410a2b24 | 一致 |
| `output/phase1/ae_deaths.csv` | 5de37965c1bd5f3d8a0b18631694d31fc67048a427b23a2fe4296418ed16d7c8 | 一致 |
| `output/phase1/bootstrap_summary.csv` | c120a8caad3d1fcf4760df8c252dd86c1a9cf6aff42827b5a1e753e401ec2a6f | 一致 |
| `output/phase1/calibration.csv` | d40cc1e71dff4acdbc7c76a514bed19a02d5b01a2cc7d4540cb2487b7de087bf | 一致 |
| `output/phase1/calibration_curves.csv` | 9c7d8c8de5d83b54d5482859724b00117213cbaa4d87a81a6130d315356f12c9 | 一致 |
| `output/phase1/calibration_final7y.csv` | 6b605ef7539af833981969e7dcba9a293f3329a06f64a623098ea8bfe7d400f7 | 一致 |
| `output/phase1/calibration_gate.csv` | bbe3cf8cc4898e8b235c50092d8f28d98f982384e3d385333f04f09cc00eb505 | 一致 |
| `output/phase1/calibration_gate_rmst.csv` | 25f95c894458658ec473a5c23bdae4a9d3d98f8289befee1cb01f44e22f82e22 | 一致 |
| `output/phase1/engine_curves.csv` | fafcc2eaa939739c68c5fc06214d6f591b5bd65c0a81e553b081ced7f23f8ff5 | 一致 |
| `output/phase1/phase1_report.md` | 40850b28d3f5f88484e841f07d9aeccdf7533e0cdfe163cecfdb10a5ec502b7c | 一致 |
| `output/phase1/round14/kext_derivation.csv` | df9012d396ccc2f18190571cfff1021210914cbfd48c476f96fdb125b5b43d1a | 一致 |
| `output/phase1/round15/preprog_survival.csv` | d4a23c547d3f46be3c67277d834420d160976dd1c51064fee5430bf2f5c240f2 | 一致 |
| `output/phase2/main/cohort_value_jbcs2024.csv` | d0689d50db6cddfa6bf102f2cd9e67a3162bef50eda8d43ec2faf7f347699c4a | 一致 |
| `output/phase2/main/decomp_main_hr085.csv` | be47f4f12d860e2b763b671d9ea27853e873c56ebe8cae4c6517f162456063d3 | 一致 |
| `output/phase2/main/decomp_reference.csv` | 35dfc9294341a9dbf7c8855bb014d7226986a4b075d92cff440245822fb853ee | 一致 |
| `output/phase2/main/det_caps.csv` | 0f63eeecb6e2fc78ea12024bc1b54e822d5265bc02cfe702d47073e201eac0ef | 一致 |
| `output/phase2/main/det_reference.csv` | 4b431ed1b804112adb2d1da256c89f9432f880c66df9b19cb2016cc6b7fccb44 | 一致 |
| `output/phase2/main/det_yardstick.csv` | 68ad2c46a7b232d20cc29bc6055c6b5bfb186280a97ee63a78fef528357fb9aa | 一致 |
| `output/phase2/main/oneway_base.csv` | 432601b43420909daccc9bc6d282f1a6134b7706861309fa326db122e918dae1 | 一致 |
| `output/phase2/main/psa_caps_summary.csv` | 417e9f3832c97f3802209c847e157b92d30f7ddca2b38ab4402845d81cfae1ad | 一致 |
| `output/phase2/main/psa_reference_summary.csv` | 68028e245ffab5387dd565ce0be02903d30b626bb72798696fef0f89e6b89173 | 一致 |
| `output/phase2/main/sc_base_crossings.csv` | c8665b64726aac059ae3e23403d6b56550c018b3f0857da3abf92d7d22eebf9c | 一致 |
| `output/phase2/main/sc_crossings.csv` | accdcc8331e664e9c7ef09cc1dc0ea3a7d1f4a44214bea8166008eda13678963 | 一致 |
| `output/phase2/main/sc_eribulin_crossings.csv` | c1b0cdc1a209ebd91338e120a9636697ea36e35ed75cfda322f4f18ca324b4f1 | 一致 |
| `output/phase2/main/sc_eribulin_det_caps.csv` | bfae73d45d1229b812c220cfff6d6097b1f547e6cbab6f873bedf5cc7f016414 | 一致 |
| `output/phase2/main/sc_eribulin_det_reference.csv` | 5486010df2d8647857dcdb9ab3bddb72ebbbd3296fa2ed5503e42ae8793d0f4b | 一致 |
| `output/phase2/main/sc_eribulin_psa_caps_summary.csv` | f8f313e178925831a15cdf1f4aaa56222481f276c7550573e27bcf14e04e818c | 一致 |
| `output/phase2/main/sc_eribulin_psa_reference_summary.csv` | 65f8a8d01381c829fe380c029cfcd970f8725f7cba8488bc336f14d185f439a5 | 一致 |
| `output/phase2/main/sc_metcost50_crossings.csv` | d0c243cad7eb453a0c49242d9478ffc1f34a804bec312aca08a004b9f791fd89 | 一致 |
| `output/phase2/main/sc_metcost50_det_caps.csv` | 09e07587396981745468156061d11ae849d5679ce4768e1219b8a292c18ddfed | 一致 |
| `output/phase2/main/sc_metcost50_det_reference.csv` | f46bf1c938f39bf36f2bce9214af9ba6b4ba3231a561ae1b2046b2e8a4b66399 | 一致 |
| `output/phase2/main/sc_metcost50_psa_caps_summary.csv` | f908cb86ff31e4f9275ad4f4f349f952214087a99d717e42068d9eaa5b5516e3 | 一致 |
| `output/phase2/main/sc_metcost50_psa_reference_summary.csv` | aab4b3b45d535e646671255835a2edd80b3b2991099b4b10e95b2209180e0231 | 一致 |
| `output/phase2/main/sc_util_jp_det_caps.csv` | a3d81057b579f4cc55f95d5bfb9dd4bcbc1de7c1330b12bc89db04073b21ef4d | 一致 |
| `output/phase2/main/sc_util_jp_det_reference.csv` | 53c2b36636efa103e4e8b5e853d6df30056479ff1a70a1d19f132344db35aa4e | 一致 |
| `output/phase2/main/scenario_caps.csv` | a5489cb0c9301be9b1d32f511c462e89071cc2ee896cd6d38d3a04bae350a71e | 一致 |
| `output/phase2/main/scenario_reference.csv` | eb3ad8dfc8f2e9bf988ce5506c286b452f457e6889977cdefc314d1e5d9f354f | 一致 |
| `renv.lock` | d5ae0360b232bbaa1d4da047c73382229a1d6704b474a3815f85a32a585279b5 | 一致 |
| `manuscript/code/refs/pubmed_meta.json` | 36b2238c6caebd28a31062cdb09d1e165fe0bfabd83df378e74727e612e821f9 | 一致 |
| `manuscript/code/refs/doi_check.json` | b3a3db4dc88361464e0911e76bf2435c73eceefdcca7fb5f025be5f40289bae1 | 一致 |
| `manuscript/code/refs/crossref_meta.json` | 0d3fa0473da9613560084d177d8fbcc8c023313a95df0b0c6f05ff4d80b14d00 | 一致 |
| `manuscript/code/refs/retraction_check.json` | cccdbb0f676a1ef8de58d51fb32c6f75cacd414e4c8a31a60cffd7e0ac704eb5 | 一致 |
| `manuscript/code/refs/cheers2022_items.json` | e155de0840844ed21d69a27b7dd52c758ce200d33b645667f3e3790cda38fec7 | 一致 |
