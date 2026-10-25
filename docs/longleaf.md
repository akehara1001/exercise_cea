# 在 Longleaf（UNC 集群）上运行

记录日期：2026-10-24（用户指示）。依据第十四轮的运行记录 `output/phase1/longleaf_bootstrap_round14.md`。

## 环境

- R：conda 环境中的 R 4.5.1（2025-06-13，x86_64-conda-linux-gnu）；包按 `renv.lock` 装入项目的 renv 库（renv 1.3.1）。
- 项目根目录用环境变量 `EXERCISE_CEA_ROOT` 指定（`docs/model_spec.md` 第 7 节）。
- 作业用 sbatch 单节点提交，PSOCK 工作进程；每个工作进程的 OpenMP 与 BLAS 线程固定为 1。

## 两处环境处理（都不改代码，也不改加载的包）

1. **RHEL 9.8 下的 renv 包库路径**：登录节点升级为 RHEL 9.8 后，renv 按操作系统版本选库目录，会去找 `renv/library/linux-rhel-9.8/`；那里是空的，项目库在 `renv/library/linux-rhel-9.7/`。在仓库外的激活脚本 `exercise_cea_env.sh` 中设 `RENV_PATHS_PREFIX=linux-rhel-9.7`，使所有节点都用 9.7 的同一个项目库。这些包是在 9.7 上用 conda 的编译器编译的，glibc 同为 2.34；第十四轮两个作业的计算节点本身都是 RHEL 9.7。
2. **1,000 次作业内关闭 renv 的 sandbox**：作业中设 `RENV_CONFIG_SANDBOX_ENABLED=FALSE`。原因是工作进程卡在 renv sandbox 的锁上：锁文件在 NFS 上排队，部分进程等了 180 秒，超过 PSOCK 的建立时限（120 秒）；第一次提交（作业 6447531）的 32 个工作进程中有 27 个没有连上主进程，没有跑任何样本。R 的系统库只有基础包，与 sandbox 中的包相同，项目库中没有重名的包，所以加载的包完全一样；关闭 sandbox 后的前 10 次与带 sandbox 运行的 `R/06c_bootstrap_check.R` 逐位相同。

## 可重现性（2026-10-25，第十五轮，`output/phase1/longleaf_bootstrap_round15.md`）

- Longleaf 内要得到逐位相同的结果，须在同一类 CPU 上运行。不同 CPU（EPYC 9654 与 EPYC 7742）上 OpenBLAS 选用的计算内核不同（Cooperlake 与 Zen），经数值优化的拟合（ESME 重拟、OS 样条）相差约 1e-10，在核对容差之内。
- 跨平台核对要在移动 `data/` 下任何文件之前、在同一个提交上运行（第十五轮的做法：先在 8dcab58 上核对，再提交第十四轮结果的移动 f806079、跑 1,000 次），因为核对只比较 `R/` 与 `data/` 内容完全相同时的结果。

## 步骤

1. `git pull`，确认工作区中 `R/` 与 `data/` 没有改动。
2. 激活环境（`exercise_cea_env.sh`）；`renv::status()` 应为一致。
3. 跨平台核对：`Rscript R/06c_bootstrap_check.R longleaf <进程数>`，10 次，与本机参照 `output/check/bootstrap10_local.rds` 逐项比较（`output/check/bootstrap10_compare_longleaf.csv`；容差 OS 与 EFS ≤ 0.05 个百分点、5 年 RMST 两臂差 ≤ 0.001 年；只比较由相同 `R/` 与 `data/` 树生成的结果）。
4. 1,000 次：`Rscript R/06_bootstrap.R 1000 <进程数>`（作业内设 `RENV_CONFIG_SANDBOX_ENABLED=FALSE`）。基础种子取 `config.R` 的 `boot_seed`（20261023，与本机参照相同；2026-10-24 起），第 b 个样本用 `set.seed(20261023 + b)`。第十四轮当时 `config.R` 只有 `seed = 20261021`，是用仓库外的包装脚本 `run_06_seed.R` 把种子设为 20261023 运行的；现在只靠仓库即可重现，不再需要包装脚本。
5. 结果（`data/bootstrap/`、`output/phase1/bootstrap_summary.csv`）与运行记录提交到仓库；作业脚本与日志留在仓库外。
