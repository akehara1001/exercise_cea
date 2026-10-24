# output/check

- `bootstrap10_local.rds`：参照结果（第十轮采用的第九轮结构）。由提交 15dba868cbaee61d8822b0163a10fbcf49c7c845 的 `R/06c_bootstrap_check.R` 生成（2026-10-23，本机：R 4.5.1 ucrt，x86_64-w64-mingw32，11 个进程；生成时 `R/` 与 `data/` 无未提交改动）。基础种子 20261023，10 次 bootstrap；远处复发后的参数每个样本由 ESME 重建个体数据重抽样后重新拟合。内容：`meta`（提交号、R 版本、平台、renv.lock 的 MD5 等）、`parameters`（每个样本的参数矩阵）、`outputs`（各臂〔chemo、pembro、pembro_k1〕第 1、2、3、5、7、10、20 年的 OS 与 EFS；k 不影响 EFS，pembro_k1 的 EFS 与 pembro 相同）、`rmst5_diff`（5 年 RMST 两臂差，基准）、`outputs_all`（臂 × pCR 的全部输出）。
- 此前的参照（第八轮的代码，提交 12c1f6e）在 git 历史中；Longleaf 对它的核对结果为 `bootstrap10_longleaf.rds`、`bootstrap10_compare_longleaf.csv`、`longleaf_check.md`（提交 bd10ee2 的代码）。
- 其他机器：`Rscript R/06c_bootstrap_check.R <标签>` 生成 `bootstrap10_<标签>.rds`，并与本参照逐项比较，写出 `bootstrap10_compare_<标签>.csv`。
- `bootstrap_workers_test.csv`：`R/test_bootstrap_workers.R` 第 (i) 条（同一平台内 4 个与 8 个进程逐位相同）。
- `bootstrap_crossplatform_test.csv`：同一脚本第 (ii) 条（与其他平台的结果按核对 B 的容差比较：OS 与 EFS ≤ 0.05 个百分点、5 年 RMST 两臂差 ≤ 0.001 年；只比较由相同 `R/` 与 `data/` 树生成的结果）。
- `bootstrap10_bounds_<标签>.csv`、`bootstrap10_bounds_<标签>_summary.csv`：`R/06d_reference_bounds.R` 的输出（2026-10-23 用户指示，只报告不设门槛）：10 次中 k 的全部值、贴 0.25 与贴 4 的次数，术前进展中位贴 10 个月与 26 个月的次数。`round10` = 上面第十轮的参照（15dba86）。参照重新生成后用默认标签 `local` 再跑一次，与 `round10` 并列；Longleaf 的 1,000 次由用户看过之后再定。
