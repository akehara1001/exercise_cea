# MANIFEST v12（2026-10-29）

- 版本: v12（v11 的小修: 指示第 1 步 manuscript 1a〜1e、第 2 步 ESM Table S1 Location；结果数值不变）。
- 交付日: 2026-10-29。
- 底本: v11（2026-10-28 交付；现在 manuscript/archive/v11/，下表）。会话开始时 9 个交付物的 sha256 与 MANIFEST_v11 一致。
- tables_v12_BCRT.docx、cover_letter_v12_BCRT.docx、Fig1〜3.tif = v11 的逐字节复制（下表 sha256 与底本相同）。
- 数值来源: 第 1、2 阶段的输出与入力表 v10，未重新计算模型；来源文件 57 个，sha256 于本版重算，与 v9 数值台帳第 8 节全部一致（下表）。
- 文献: 78 条（正文 1〜71，72〜78 只在 Table 1 与 ESM）。核对结果见 worklog_v12.md 第 6.1 节。
- 公开用代码（指示第 3 步）: C:\Users\原明美\Documents\ClaudeCode\exercise_cea_public\（作业树外，114 个文件，清单与 sha256 见 manuscript/code/checks_v12/out/public_files.txt）。去名检查有人名命中，按指示停下: 无 README、LICENSE、未 git init（worklog_v12.md 第 7 节）。

## 交付物（manuscript/v12/）

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

## 底本（manuscript/archive/v11/）

| 文件 | sha256 |
|---|---|
| manuscript_v11_BCRT.docx | 58b6897ab597a714b5cb7cc7341cd5a23c9bb1cb77127074c9c5dbf063a181e3 |
| tables_v11_BCRT.docx | d022962f64dd85a5c4377294a82fbe6d56e7cc3d020f7de3805e84f71747c54a |
| ESM_1_v11.docx | aa0d4e947ced6690d64783fef62431c31f1ae5840719cab3a564a55f0bf4d207 |
| ESM_1_v11.pdf | 52c2716fe76fca7eb61d8d832596695e17f2d5690fc6ed271d0b5b21444cca97 |
| Fig1.tif | c13b748ed3c7d5880f81da06e5ae9c4cccf8d6285c2108c7b0be1c5c04d78543 |
| Fig2.tif | 662046bf6a3d4847b0a0992324e2cbe902981dc2dab4f16fd96d6006a5d8b3d7 |
| Fig3.tif | d7926e1e9d8664dcb69188bcc253bc98cda25bc9347927d256abe826fc54ea8a |
| cover_letter_v11_BCRT.docx | 21ed7f1aa387e8b7e9e3015f97c0c44f4f50b10dd58fa334e7fdf907bd37b935 |
| worklog_v11.md | ad8b47718751388cf6485d0e795fa2f226d4e4e08a22be83ed57dff027cb8ab2 |
| MANIFEST_v11.md | 86a70374013dd72f7bdffe0f2d879b88583f6201f52df9cf0ddbdf65b83c9e72 |

## 编辑脚本与公开入力表脚本

| 文件 | sha256 |
|---|---|
| manuscript/code/edit_manuscript_v12.py | 38317378e8493d319cc612373e065ddf61e64140619704110e922c01e69d0f81 |
| manuscript/code/edit_esm_v12.py | bec9ca70101e21b4e82670d16935369b8ca14543cd78aed5f932a853f9fb3476 |
| R/py/26_public_params.py | bab809e537915b6aa550b0ce80aa80223c93a003e49a574e3157a7766888aaf3 |

## 核对脚本与输出（另用 manuscript/code/checks_v11/ 的 regress.py、regress2.py、refcheck.py、fmt_audit.py、sec10.py、word_stats.ps1、word_open_pdf.ps1、word_wc.py、citemap.py，未改）

| 文件 | sha256 |
|---|---|
| manuscript/code/checks_v12/citeorder.py | 913fb998a2f8e314a4be72dc30cc85b145c8d7600b4360c15b40ea3c8fc889d7 |
| manuscript/code/checks_v12/compare_outputs.py | fcae279aee0a814141de0f2e9db8a44ff2a76686170c2f8649a8d0174a7ed65f |
| manuscript/code/checks_v12/pdf_pages.py | e00250208649c0b393b7de1283fc20a43555315217dfec2093cb9c967bf54ac8 |
| manuscript/code/checks_v12/public_name_scan.py | 3dc4885af59bd8c42f347bd3409d0945079af33c9747250e8142389fce50b4fa |
| manuscript/code/checks_v12/rds_strings.R | da7b9d08dfddf4034f1c77d864d8174c52f041676c439d5db50f389534a36936 |
| manuscript/code/checks_v12/tfnum.py | c5342b0d4b52a8e398cd40a47e3e0f7e0c7f7dd9aee20d79eea1f3a535d60681 |
| manuscript/code/checks_v12/out/citeorder.txt | bbf1192a0abeae3a8dcb47f694ef16fe321f152a782c847e5ad846628b117c24 |
| manuscript/code/checks_v12/out/compare_optionA.txt | 4fd0a25f31c545a1cd4d4442bab6d4eb887f89221d1062715aafb3facd3ddbe6 |
| manuscript/code/checks_v12/out/esm12_log.json | bda2fb2905158bd7c37785fb2cbaa7c318337c53a4c4ca055ae3a17bbfbcd445 |
| manuscript/code/checks_v12/out/fmt_v12.txt | 0d2b68d390eb4f28f24235dac33348eb1446f84ebf02d1c46f84e324dd269547 |
| manuscript/code/checks_v12/out/m12_log.json | b2b80e340c51bcb679d0e52eab9ffc362faaccec62ea1a5de1a06fad7b89b083 |
| manuscript/code/checks_v12/out/m12_stats.json | b54c11a8f358f8da950e3aa3d46c1a78e04c70708f452225ef0b5d008ef5b728 |
| manuscript/code/checks_v12/out/public_files.txt | 42c566babb486102e86209ebad65a2291dab47297f826941b5aaefeaa466f592 |
| manuscript/code/checks_v12/out/public_name_scan.txt | 54ad630e9a41ac4dd5495a74770c4c8d9e572e2855e34da8690befb2dfaf757f |
| manuscript/code/checks_v12/out/r2_esm.md | dcbaa5d4d4e0d72308047e7509729e6cde3a6727c6bcc54816c3c505c11ebbae |
| manuscript/code/checks_v12/out/r2_manuscript.md | 093ae52bf1c90e413a11c3d12e0848b1986519b3e98c347e9f69e06a1d33689e |
| manuscript/code/checks_v12/out/r_esm.txt | 24615d488c40c8be8ae38cd403ed26fbbc888a467599b7ff97152557bf59c5f9 |
| manuscript/code/checks_v12/out/r_manuscript.txt | 868644375695ace9828beca1290ca8a7c76f5fe7bf8e6b389f60f704959839bf |
| manuscript/code/checks_v12/out/refcheck_v12.json | ef1312d73d5912e2b9aaa0d64f857a96878505324cf54d1e3d8e68a5af2943f8 |
| manuscript/code/checks_v12/out/refcheck_v12.txt | 3c6f505ad318c9666ac0a827a3bf7d2dfac2ee8fe5a551b9d2847cfc4415c78c |
| manuscript/code/checks_v12/out/sec10_v12.txt | a2a37486739f5385cd0c7f56d781d79c1d57b952acf49dc50b613fb9d206fd49 |
| manuscript/code/checks_v12/out/tfnum.txt | 91b377a733dd6c59405879ea0ee5de4a79600b0ac64e12d207575be7e0ebca44 |

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
