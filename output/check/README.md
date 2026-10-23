# output/check

- `bootstrap10_local.rds`：参照结果。由提交 12c1f6e7ac1f9c4a43814ef10dd8c7afc6b46c6f 的 `R/06c_bootstrap_check.R` 生成（2026-10-23，本机：R 4.5.1 ucrt，x86_64-w64-mingw32，11 个进程）。基础种子 20261023，第八轮设定，10 次 bootstrap。内容：`meta`（提交号、R 版本、平台、renv.lock 的 MD5 等）、`parameters`（每个样本的参数矩阵）、`outputs`（各臂〔chemo、pembro、pembro_k1〕第 1、2、3、5、7、10、20 年的 OS 与 EFS；k 不影响 EFS，pembro_k1 的 EFS 与 pembro 相同）、`rmst5_diff`（5 年 RMST 两臂差，基准）、`outputs_all`（臂 × pCR 的全部输出）。
- 其他机器：`Rscript R/06c_bootstrap_check.R <标签>` 生成 `bootstrap10_<标签>.rds`，并与本参照逐项比较，写出 `bootstrap10_compare_<标签>.csv`。
- `bootstrap_workers_test.csv`：`R/test_bootstrap_workers.R` 的结果（4 个与 8 个进程完全相同，且与第 1 阶段 bootstrap 的第 1 至 4 个样本完全相同）。
