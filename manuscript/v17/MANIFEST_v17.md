# MANIFEST v17（2026-11-04）

- 版本: v17（v16 的小修: 文献第 8 条加内服药清单〔10/14 版快照存在、内服药用值 5/5 一致 → 指示的 (i)〕；数值不变）。
- 交付日: 2026-11-04。
- 底本: v16（2026-11-04 交付；现在 manuscript/archive/v16/，下表）。会话开始时 9 个交付物的 sha256 与 MANIFEST_v16 一致。
- tables_v17_BCRT.docx、Fig1〜3.tif、cover_letter_v17_BCRT.docx = v16 的逐字节复制（下表 sha256 与底本相同）。ESM_1_v17.docx = v16 + Table S1 第 27 项页码 p. 26 → p. 27（第 8 条加长使 Funding 移到第 27 页；worklog_v17.md 第 6.2 节）。ESM_1_v17.pdf 由 Word（SaveAs2, 17）重新导出（48 页）。
- 数值来源: 本版不改数值，未重算模型。MANIFEST_v16 的来源文件 sha256 重算（下表）。药价表四份的 sha256 见末节。
- 文献: 78 条；第 8 条改为内服药与注射药两份清单（10/14 版）及两个 Wayback 存档网址（worklog_v17.md 第 5 节）；其余不变。
- 公开用代码: 本版无改动（exercise_cea_public，HEAD fbf19be，无远程、未推送）。

## 交付物（manuscript/v17/）

| 文件 | sha256 |
|---|---|
| manuscript_v17_BCRT.docx | 3cdc027d53f56dd208b7055895b3a5b371904c85700db898e2464a776f8bd695 |
| tables_v17_BCRT.docx | 8236a3eee6495976fd4f07a2ed8945762fc9570f8b674cc807f610ca0c79c4e3 |
| ESM_1_v17.docx | 642590a6b691dea92f27d86d7397733cc73f6504f091acd62d62da9fcfd8775e |
| ESM_1_v17.pdf | 826fb01aec5761c150cdda802dfe707646c4ae5596b94a7e542100aed072a746 |
| Fig1.tif | c13b748ed3c7d5880f81da06e5ae9c4cccf8d6285c2108c7b0be1c5c04d78543 |
| Fig2.tif | 662046bf6a3d4847b0a0992324e2cbe902981dc2dab4f16fd96d6006a5d8b3d7 |
| Fig3.tif | d7926e1e9d8664dcb69188bcc253bc98cda25bc9347927d256abe826fc54ea8a |
| cover_letter_v17_BCRT.docx | 21ed7f1aa387e8b7e9e3015f97c0c44f4f50b10dd58fa334e7fdf907bd37b935 |
| worklog_v17.md | 279689e247a6ebd2af6074ce8fde7ffa5b0d94510d973dbe0596d94a36c67797 |

## 底本（manuscript/archive/v16/）

| 文件 | sha256 |
|---|---|
| manuscript_v16_BCRT.docx | aa79255fa226e3cf435402e81759ff24cb4fb46031fa3df20b3b837f7729eb1b |
| tables_v16_BCRT.docx | 8236a3eee6495976fd4f07a2ed8945762fc9570f8b674cc807f610ca0c79c4e3 |
| ESM_1_v16.docx | 1955102cf2c9a7935e6cf243d8432204c6d48b3038287daf85fa4863c8f0201c |
| ESM_1_v16.pdf | c69a24fb266fc287267d123b3d18377698f794bf5d1cd98a5b552c4db959d61f |
| Fig1.tif | c13b748ed3c7d5880f81da06e5ae9c4cccf8d6285c2108c7b0be1c5c04d78543 |
| Fig2.tif | 662046bf6a3d4847b0a0992324e2cbe902981dc2dab4f16fd96d6006a5d8b3d7 |
| Fig3.tif | d7926e1e9d8664dcb69188bcc253bc98cda25bc9347927d256abe826fc54ea8a |
| cover_letter_v16_BCRT.docx | 21ed7f1aa387e8b7e9e3015f97c0c44f4f50b10dd58fa334e7fdf907bd37b935 |
| worklog_v16.md | a2370c632ce0c592e64831920df327f3bce480fbda65ac667480c5fc4de1d7ac |
| MANIFEST_v16.md | baf66fcf09d661189d827eca007fe77d980ec5718083afb6c2cffbdcb1a8d6d9 |

## 编辑脚本

| 文件 | sha256 |
|---|---|
| manuscript/code/edit_manuscript_v17.py | 1194ee703185879dd9e13c359500f5965b3274816b9857a683b967bf08a42051 |
| manuscript/code/edit_esm_v17.py | ced3b19051365f98b8c486422d72628d2eb6075d91eeb8dc69598117c70fb38a |

## 核对脚本与输出（另用 checks_v11/ 的 refcheck.py、sec10.py、fmt_audit.py、word_stats.ps1、word_open_pdf.ps1、citemap.py，checks_v12/pdf_pages.py，checks_v14/ 的 word_wc14.py、acro_extract14.py，edit_esm_v14.py 的 pages14() 与 edit_esm_v15.py 的 locations15()，均未改；ARS 3.24.1 的 check_acronyms.py）

| 文件 | sha256 |
|---|---|
| manuscript/code/checks_v17/citeorder17.py | 5730138cc565931a46399232ade9810a3cf82068671825902d1e44e4380e621b |
| manuscript/code/checks_v17/compare_oral_lists17.py | 20cb58108c1837833420da0384dca608e81eca54000078efff425fba886feac1 |
| manuscript/code/checks_v17/make_manifest17.py | 8792b7e399122aea5e24c39f0a1f8c2c0a1c2db1664b16505dc35d92bb8f0bc4 |
| manuscript/code/checks_v17/regress17.py | e3400cc287d032965f442647e2dd0863436fa6bc47ae82ba3a5886cdfc1abfde |
| manuscript/code/checks_v17/tfnum17.py | afbcd7d445754e63d6a4628036bcaffae61ddea45c04d105337bada10f6de55a |
| manuscript/code/checks_v17/out/abs17.txt | 274a53bc3c6d8fb2ba19466a72cd1dc0fa6db69534746e8682a04d6a46dad217 |
| manuscript/code/checks_v17/out/acronyms_abs17.txt | 9ba96b2f1e58e113506a518682bf5725459b07cce54799f0d5802e124f5bd34b |
| manuscript/code/checks_v17/out/acronyms_body17.txt | 113829bb0f7d95fff1e5a32c1c89d080fbaf32c82ed5a26ebd3ae692a7a0e651 |
| manuscript/code/checks_v17/out/body17.txt | d5d0ae0b3f86a16df398e19ceb64d73ad967d230622f77fc92b1591083911fd8 |
| manuscript/code/checks_v17/out/bytes17.txt | 4775fafbd51a843e7d592457de6fa6c5e4587474a8f0690e7a186afc01a5e118 |
| manuscript/code/checks_v17/out/citeorder17.txt | d9c2cee1aee5ec03085504b1d233861a9b32db893daece5867bd82f80586f62e |
| manuscript/code/checks_v17/out/esm17_log.json | d7437a319e5a3145f33e60c6ba6fc187440e8a804f311a57261414185cf71172 |
| manuscript/code/checks_v17/out/fmt_esm17.txt | df1cb4c9237c684c4c57eb43bbd5355a0abf1569fa01b7ea14e86d009295f99a |
| manuscript/code/checks_v17/out/fmt_v17.txt | 008530104321368231883879827108fd3b92cce83f38235eb898cb19d9cc34aa |
| manuscript/code/checks_v17/out/m17_log.json | 7f082642e7caa7475fed876559a7f4aa4d6d4ff648d7a33f3d94c5de7208ea2d |
| manuscript/code/checks_v17/out/m17_stats.json | 7ad306131fe363f44f269dc1b42ebee2dd445e280f52b3fccc5063cc380923f4 |
| manuscript/code/checks_v17/out/oral_compare17.json | 44949fa42b5990c4a6124662f27bc4b789f5fdb1e7e9b1d6085b8b9d69976bad |
| manuscript/code/checks_v17/out/oral_compare17.txt | 09ea5e61a6bda88960b248119d73526a2fbfbdbbd9bab06d81e763bddb945136 |
| manuscript/code/checks_v17/out/pdf_pages_v17.txt | 3b063659cce5d337786cc6fbeb66e77d43b5cbcf9699b92a44c5689366c83ee9 |
| manuscript/code/checks_v17/out/r17_esm.txt | 0d28eeace1deba8a5baac813ef11807c5d8794da743691e70a8d7edc03193414 |
| manuscript/code/checks_v17/out/r17_manuscript.txt | 4b1ea654e225bef08167b6c2b3506dc29e019408a60253ceb44e6b6bde2c230d |
| manuscript/code/checks_v17/out/r17_tables.txt | 2a236ad46b67a470cdd3da6377f7f6613ec633c3c5dd0528f0b985ff8f417c4d |
| manuscript/code/checks_v17/out/ref8_urls17.txt | 53f6a513e514d8635ef8aecf8facd53ffa7f9f50ce346c88a4805321666f32af |
| manuscript/code/checks_v17/out/refcheck_v17.json | e9e076534957e320284cb01a535e0752e987c56cf30185dfbbf5bcf49cfb26a3 |
| manuscript/code/checks_v17/out/refcheck_v17.txt | 8c89af7cd2d4cea99561687a8903b60fab703daaa393db65d6ade17fff43d231 |
| manuscript/code/checks_v17/out/sec10_v17.txt | de560d23e95d2fdabbf0dc15bf6d4ab88bf3ff6430b97e7bdca790b812aeb1e5 |
| manuscript/code/checks_v17/out/tfnum17.txt | 8055fcd493c9d2bac5e7433d04a4db298d64440a44cb8e09df3f8aa8df05a0a2 |

## 数值来源文件（MANIFEST_v16 的来源表，sha256 为本版重算值；与 v16 的比较）

| 文件 | sha256 | 与 v16 |
|---|---|---|
| `data/ipd/K24_F2A_EFS_pembro.csv` | 55c68dee37923aeea2aa44c7098a9307cf643c456fafbc193614aaef2ad903d8 | 一致 |
| `data/ipd/K24_F2A_EFS_placebo.csv` | c11b24f5ea47fc1651054fba33f71fa4e2232a068c99d32b5025eca1dbf0568f | 一致 |
| `data/kn522_final_7y.csv` | 0f40a51bb51c1d412e7e6ee578c3cd98631980df61d8a1e12e3d193aafe3258a | 一致 |
| `data/lifetable_female_2025.csv` | 213403bd92ac2669014a8b4edfba3210ed334c51031bf92e1a7bb87049fed733 | 一致 |
| `data/params_dist.csv` | 3b8e10fcc27eb396dd7c3738dedd22f4ba6a1abe2ae60e14d7cf22841960b8b2 | 一致 |
| `data/pcr_counts.csv` | 0d8cf779b0ffd827981d87e926ddc74b4483ab54ca02b5c1c47ebe88f9d030c1 | 一致 |
| `docs/analysis_plan_phase2.md` | fcf1ad39107d6662119c82b365ac15eb56efdbb5aa4a74d6f147a2007a27ee5f | 一致 |
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
| `output/phase2/fourarm_report.md` | 3c9a6160293d9c7eb2d2bff6831e94b6129c5ea02c54ec7556bfb06daa87270e | 一致 |
| `output/phase2/main/fourarm_totals.csv` | 32183682a038cac57615701a6e501d8269800d061896b6636fab31a89611b567 | 一致 |
| `output/phase2/main/fourarm_incremental.csv` | 430e3c58d351069dbcaf862b37f237f2ecddae1abcff53352f52a1c8e54aa84c | 一致 |
| `output/phase2/main/fourarm_nmb_equal.csv` | 5f6671dfccb10b894fad80c85c0f44394e7900a7dc319f5fb0009d020f9fb353 | 一致 |
| `output/phase2/main/fourarm_checks.csv` | 4828dcbb186d4018f4f5de3fe7dc4046fd5cad744e4bf72ab86238b5c75ccbda | 一致 |
| `output/phase2/main/fourarm_run.csv` | e2abad573ef49445b6583d9cc60664654ed12e7d2447b010e9e3ff3af850a7df | 一致 |
| `output/phase2/main/fourarm_test_runs.csv` | ab623cc9ea0329bb4eb66fbc3c3f0aa144f8a89046b91e27a02c05262869050d | 一致 |
| `output/phase2/main/fourarm_unit_tests.csv` | 6748be69055eea66569d84b7446bf821d88318d752f2d1f572c81b68b8fe0781 | 一致 |
| `R/25_four_arm.R` | 552f3e6487b3670ffcfd5833861dc9919acfed037b0d47f974bfb563cefc128c | 一致 |
| `R/test_four_arm.R` | 79ae13e24b34cb96b733eddf38d4105e90d15e988b19aa18372f053b41b2d40d | 一致 |

## 药价表（_01 = 内服药、_02 = 注射药。10/14 版 _02 = 当初保存的原文件，Wayback 存档件与之逐字节相同；10/14 版 _01 = Wayback 快照 20261014082215 的原始字节〔原网址现 404〕；11/1 版 = 2026-11-04 下载）

| 文件 | sha256 |
|---|---|
| `input/params/sources_price/tp20261014-01_01.xlsx` | 21bb77b08fb9dd5fabf8776b89cfcb8db5ac3ee5316424e9b6418546e8888628 |
| `input/params/sources_price/tp20261014-01_02.xlsx` | 161d801b4c94314c725eb19daf06af8834d7fc66c8aa4c503566ac818363a4bb |
| `input/params/sources_price/tp20261101-01_01.xlsx` | b5891578c228908434377b57ec2b9055671626cefa174e95862119e4d1f16030 |
| `input/params/sources_price/tp20261101-01_02.xlsx` | 198dac81e6141f9a06e9ba8509b727b9e875276a7da8122aa3df803045e21662 |
