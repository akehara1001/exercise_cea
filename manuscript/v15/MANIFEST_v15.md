# MANIFEST v15（2026-11-04）

- 版本: v15（v14 的删减与修正: 正文压到 BCRT 上限以内〔3,470 词〕、文献第 71 条更新、v14 报告的小项；文献第 8 条未改）。
- 交付日: 2026-11-04。
- 底本: v14（2026-11-04 交付；现在 manuscript/archive/v14/，下表）。会话开始时 9 个交付物的 sha256 与 MANIFEST_v14 一致。
- Fig1〜3.tif 与 cover_letter_v15_BCRT.docx = v14 的逐字节复制。ESM_1_v15.pdf 由 Word（SaveAs2, 17）从 ESM_1_v15.docx 导出（48 页）。
- 数值来源: 本版不加新数值，未重算模型。MANIFEST_v14 的来源文件 sha256 重算（下表）。R/22_phase2b_main.R 只改第 112 行注释（3d）。
- 文献: 78 条；第 71 条按 Crossref 与 PubMed 更新为 Ann Oncol 37:1467–1479；第 8 条未改（网址 404，同一日期的清单站内找不到，worklog_v15.md 第 6 节）。
- 公开用代码: C:\Users\原明美\Documents\ClaudeCode\exercise_cea_public\（作业树外）；本地 git commit fbf19be（父 4a883ed）；无远程、未推送。

## 交付物（manuscript/v15/）

| 文件 | sha256 |
|---|---|
| manuscript_v15_BCRT.docx | 42b4edaddd611690a7751064179261afc9a8badf99d8bebec05594136d4e6a9d |
| tables_v15_BCRT.docx | 8236a3eee6495976fd4f07a2ed8945762fc9570f8b674cc807f610ca0c79c4e3 |
| ESM_1_v15.docx | 1955102cf2c9a7935e6cf243d8432204c6d48b3038287daf85fa4863c8f0201c |
| ESM_1_v15.pdf | bb303d3731862cf3919790e42c9ed30efda7c11f119121026657eb47e60796cf |
| Fig1.tif | c13b748ed3c7d5880f81da06e5ae9c4cccf8d6285c2108c7b0be1c5c04d78543 |
| Fig2.tif | 662046bf6a3d4847b0a0992324e2cbe902981dc2dab4f16fd96d6006a5d8b3d7 |
| Fig3.tif | d7926e1e9d8664dcb69188bcc253bc98cda25bc9347927d256abe826fc54ea8a |
| cover_letter_v15_BCRT.docx | 21ed7f1aa387e8b7e9e3015f97c0c44f4f50b10dd58fa334e7fdf907bd37b935 |
| worklog_v15.md | 96bc6543b972ae9857e5afb4f6e90ddc0c40321e5357d38a010a7cce4c5f6852 |

## 底本（manuscript/archive/v14/）

| 文件 | sha256 |
|---|---|
| manuscript_v14_BCRT.docx | bd741f343a4e3d6ecdf5ee281f10952dcffec1bd117750bcc7cc0f3ab2044790 |
| tables_v14_BCRT.docx | ea0fe2b460c132443ea0f3b87ad577a2e337861f14f9c8a822fc166625c0c712 |
| ESM_1_v14.docx | 02580c221a90f3db9c805ce1e9e8a4151ecf6345169b55bbd30958db5c6b8c15 |
| ESM_1_v14.pdf | 7fb2d73b7d893e6618aaf3e0c0314b42d4068b6423ab78eb91764fcd71f9a8f5 |
| Fig1.tif | c13b748ed3c7d5880f81da06e5ae9c4cccf8d6285c2108c7b0be1c5c04d78543 |
| Fig2.tif | 662046bf6a3d4847b0a0992324e2cbe902981dc2dab4f16fd96d6006a5d8b3d7 |
| Fig3.tif | d7926e1e9d8664dcb69188bcc253bc98cda25bc9347927d256abe826fc54ea8a |
| cover_letter_v14_BCRT.docx | 21ed7f1aa387e8b7e9e3015f97c0c44f4f50b10dd58fa334e7fdf907bd37b935 |
| worklog_v14.md | 9ceb8c704c405ab85f41e25ec03238869ad4109e8a258a22d2aa2f2409222dd5 |
| MANIFEST_v14.md | 5218a2ecd41e666651789f3a07dbcd0607f3781b06fcd58e09a04b7a0eada482 |

## 编辑脚本与改动的代码

| 文件 | sha256 |
|---|---|
| manuscript/code/edit_manuscript_v15.py | 5b601164aeb235ef2441b0ede823f013e5ee50ec39495d28fea3acae8bc6ae5c |
| manuscript/code/edit_tables_v15.py | 79584ae97d92265f19323f486c623554a6631bbf370add24fb571633d1e687a6 |
| manuscript/code/edit_esm_v15.py | c1e0cebe99044ae167c97d1085b1d09d60e0059958cb23656ad234fcf940b58d |
| R/22_phase2b_main.R | 31fa69e5f750aa700a345dace4ea8c8c87f03d8c10c285f3f10e91770c0ad317 |

## 核对脚本与输出（另用 checks_v11/ 的 refcheck.py、sec10.py、fmt_audit.py、word_stats.ps1、word_open_pdf.ps1、citemap.py，checks_v12/pdf_pages.py，checks_v14/ 的 word_wc14.py、acro_extract14.py、edit_esm_v14.py 的 pages14()/locations14()，均未改）

| 文件 | sha256 |
|---|---|
| manuscript/code/checks_v15/citeorder15.py | 8a6009ef4684411e83488b4c68073a42cb12971c4b51bbb656b0d812db29b8e9 |
| manuscript/code/checks_v15/make_manifest15.py | 06f434404e8eaadf45de386f02bcc8873903d9b910d6e1f3396a227a6af2e5db |
| manuscript/code/checks_v15/numcheck15.py | 2701d322f542f0b8509ae80ad12a0d53f177e0ba2bfdf23b6dadffec10a8060a |
| manuscript/code/checks_v15/regress15.py | 34f110c8f2064414b3e171e5c4c7fea535da564443a7549a44466a36a9c9fc2d |
| manuscript/code/checks_v15/tfnum15.py | 806da4f37384c8281b2bf7e3940c7085e05eb8e14036359a2cc327db39ab3095 |
| manuscript/code/checks_v15/out/acronyms_abs15.txt | 9ba96b2f1e58e113506a518682bf5725459b07cce54799f0d5802e124f5bd34b |
| manuscript/code/checks_v15/out/acronyms_body15.txt | 113829bb0f7d95fff1e5a32c1c89d080fbaf32c82ed5a26ebd3ae692a7a0e651 |
| manuscript/code/checks_v15/out/cite_tf_detail15.txt | 22ac45419273bf5d8589e8d7639ad750d3ee3d8a7f384f5cae1955bf57ea98bd |
| manuscript/code/checks_v15/out/citeorder15.txt | 812b3f0ed4180b4002e45a9dc1eba3820916cd57f897da5ff021eabe1055a024 |
| manuscript/code/checks_v15/out/esm15_log.json | 39bf955dfea7af91aaf346e03490247e4fc4e4662072ecbd5d13cbd77623a266 |
| manuscript/code/checks_v15/out/fmt_v15.txt | e752d4abd91f6ca7314f6e5d55904199f7804f7495e9dda9f93a7027783ae085 |
| manuscript/code/checks_v15/out/m15_log.json | cfdf5bad454e7a159c3a77a136a68a74d3a553013b0846fbb044c92c6cc43a8f |
| manuscript/code/checks_v15/out/m15_stats.json | 662ac1ae06af61bb75264a90cf60ea61f49848f9ff3fef78ea4873970aec0dbc |
| manuscript/code/checks_v15/out/numcheck15.txt | 4aa2e07a87eef283dc62ab4145709081c439f925778835def5fe333a78284741 |
| manuscript/code/checks_v15/out/pdf_pages_v15.txt | 0b604fb1203cf81b7cfac719c924a6b6f7dad72b3f3dbf8de612d6adc54b89ac |
| manuscript/code/checks_v15/out/r15_esm.txt | c12d496dac679141563ba0a736c6f67deea5c1844895659a4c4bba47c0ab494c |
| manuscript/code/checks_v15/out/r15_manuscript.txt | 4889b25de253ee8f4c1d915211e8d39ac01168b64235933b2304624f01fc3d0a |
| manuscript/code/checks_v15/out/r15_tables.txt | 94a2540bebbd7335467895d4f9b3e61f0b2bf217a88d620bd6410a1f300a8fb2 |
| manuscript/code/checks_v15/out/refcheck_v15.json | e9e076534957e320284cb01a535e0752e987c56cf30185dfbbf5bcf49cfb26a3 |
| manuscript/code/checks_v15/out/refcheck_v15.txt | 8c89af7cd2d4cea99561687a8903b60fab703daaa393db65d6ade17fff43d231 |
| manuscript/code/checks_v15/out/sec10_v15.txt | 9148645da93d44f311ca58a4927f76190dc635e88c8d91a59e43c960a0e243be |
| manuscript/code/checks_v15/out/t15_log.json | 6660afb2b598605d92834b1f9dd022d90b352d312442e1ca7629ecf213e93a53 |
| manuscript/code/checks_v15/out/tfnum15.txt | 21cc44dc395af29301ede79b9388ba30de71688c9c238db0209d722da031d27b |

## 数值来源文件（MANIFEST_v14 的两张来源表，sha256 为本版重算值；与 v14 的比较）

| 文件 | sha256 | 与 v14 |
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

## 公开目录中本版修改的文件（commit fbf19be）

| 文件 | sha256 |
|---|---|
| R/22_phase2b_main.R | 8c711ce6e868da7e6e7073e0fdfa2d982c722e78f1963bbcaa9fbc377e79ec2a |
