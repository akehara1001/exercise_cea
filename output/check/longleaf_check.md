# Longleaf 一致性核对（2026-10-23）

## 结论

- **核对 A（引擎）：通过。** 用 `data/` 中保存的 1,000 个样本的参数矩阵，在 Longleaf 上重算步骤 7。与仓库中第 1 阶段的输出相比，最大绝对差为 1.21e-13（标准：< 1e-10）。
- **核对 B（bootstrap）：通过。** 基础种子 20261023，第八轮设定，10 次。
  - 各臂各时点 OS 与 EFS 的差值，绝对值最大为 1.90e-6 个百分点（标准：≤ 0.05）。
  - 5 年 RMST 两臂差的差值，绝对值最大为 1.81e-8 年（标准：≤ 0.001）。
- **单元测试：5 个中 4 个通过。** `test_bootstrap_workers.R` 退出码为 1：
  - 4 个与 8 个进程的结果完全相同，这一项成立；
  - 但与本机第 1 阶段 bootstrap 的第 1 至 4 个样本不是逐位相同（最大差 2.8e-6），见第 3 节。
- 没有修改模型代码、测试代码和 `renv.lock`。

## 1. 环境

| 项目 | Longleaf | 本机（参照结果） |
|---|---|---|
| 提交 | bd10ee2（运行时 `R/` 与 `data/` 无未提交改动） | 12c1f6e |
| R | 4.5.1 (2025-06-13)，conda-forge `r-base` 4.5.1 | 4.5.1 (2025-06-13 ucrt) |
| 平台 | x86_64-conda-linux-gnu（RHEL 9.7） | x86_64-w64-mingw32 |
| BLAS/LAPACK | OpenBLAS 0.3.34（pthreads 版），LAPACK 3.12.0 | （rds 中未记录） |
| 编译器 | conda-forge gcc / g++ / gfortran 15.3.0 | — |
| survival / flexsurv / flexsurvcure / renv | 3.8.3 / 2.3.2 / 1.3.3 / 1.3.1 | 相同 |
| `renv.lock` 的 MD5 | 38e44703… | fc622ab8… |

- 从 12c1f6e 到 bd10ee2，`R/`、`data/`、`renv.lock` 和 `renv/` 都没有改动。
- `renv.lock` 的 MD5 不同只是换行符造成的，内容相同。本机工作区的文件是 CRLF；把仓库中的 `renv.lock` 转为 CRLF 后，MD5 正好是 fc622ab8…。

**conda 环境**：`/users/y/i/yihanzh/conda/envs/r451`，全部来自 conda-forge。

- 内容：`r-base=4.5.1`、`compilers`、`make`、`pkg-config`、`libcurl`、`openssl`、`libxml2`。
- 另外补装了 `zlib` 1.3.2。原因：data.table 与 png 从源码编译需要 `zlib.h` 和 `libz.so`，第一次 restore 因缺少它们而失败。

**激活脚本**：`/users/y/i/yihanzh/exercise_cea_env.sh`。它加载 `anaconda/2024.02` 模块、激活 r451，并设置以下环境变量：

- `OMP_NUM_THREADS=1`
- `OPENBLAS_NUM_THREADS=1`
- `EXERCISE_CEA_ROOT=/users/y/i/yihanzh/exercise_cea`

### 包

**`renv::restore()`**：在计算节点上运行，全部从源码编译。设置了 `RENV_CONFIG_PPM_ENABLED=FALSE`，不用 Posit 为系统 R 编译的 RHEL 9 二进制包。

- `renv.lock` 中的 71 个包全部按锁定版本装入项目库，并且全部可以加载；`renv::status()` 显示一致。
- 与 `renv.lock` 不一致的包：无。
- 安装失败：只发生在第一次。data.table 与 png 因缺少 zlib 编译失败，依赖它们的 mstate、flexsurv、flexsurvcure、readbitmap、IPDfromKM 随之未装。补装 zlib 后重跑，全部成功。

**项目代码用到的包**：`renv::dependencies("R")` 找到以下包，都在 `renv.lock` 中：

- flexsurv、flexsurvcure、ggplot2、IPDfromKM、jsonlite、muhaz、readxl、RhpcBLASctl、survival；
- 以及基础包 parallel、stats、tools。

它们的递归依赖（Depends、Imports、LinkingTo）加上它们本身共 70 个包，再加 renv，正好是 `renv.lock` 中的 71 个，没有缺的。

**推荐包**：conda 的 R 不自带推荐包，这里用到的都由 renv 装入项目库。

| 包 | 项目代码如何用到 | renv.lock | 安装版本 | 可加载 |
|---|---|---|---|---|
| survival | 直接（`library(survival)`） | 3.8-3 | 3.8-3 | 是 |
| MASS | 经依赖 | 7.3-65 | 7.3-65 | 是 |
| Matrix | 经依赖 | 1.7-3 | 1.7-3 | 是 |
| lattice | 经依赖 | 0.22-7 | 0.22-7 | 是 |
| nlme | 经依赖 | 3.1-168 | 3.1-168 | 是 |
| boot | 经依赖 | 1.3-31 | 1.3-31 | 是 |
| mgcv | 经依赖 | 1.9-3 | 1.9-3 | 是 |
| class、cluster、codetools、foreign、KernSmooth、nnet、rpart、spatial | 不用（不在依赖闭包中） | 无 | 未装 | — |

- 补装的推荐包：无。`renv.lock` 未改动。
- **RhpcBLASctl** 0.23-42：在 `renv.lock` 中，restore 后可以加载，`blas_get_num_procs()` 为 1。

## 2. 作业设定

**线程**：每个 R 进程（主进程和 PSOCK 工作进程）启动时，都把线程数固定为 1。

- **做法**：用环境变量 `R_PROFILE_USER` 指定一个启动文件。它先执行项目的 `.Rprofile`（激活 renv），然后：
  - 设置 `OMP_NUM_THREADS=1`；
  - 调用 `RhpcBLASctl::blas_set_num_threads(1)` 和 `omp_set_num_threads(1)`；
  - 记录每个进程的设定。
- **为什么这样做**：`07_engine_outputs.R` 的工作进程自己不设线程数，用这种方式补上，不需要改代码。`06c_bootstrap_check.R` 的工作进程还会按 `bootstrap_core.R` 的 `boot_run()` 再设一次。
- **记录结果**：核对 A 的 12 个进程、核对 B 的 11 个进程，全部是 `OMP_NUM_THREADS=1`、`OPENBLAS_NUM_THREADS=1`、`blas_get_num_procs()=1`。每个进程最多 2 个线程。

| 作业 | 内容 | 分区（sacct） | CPU | 内存 | 时限 | 用时 | 峰值内存（MaxRSS） | 节点 |
|---|---|---|---:|---:|---:|---:|---:|---|
| 6295045 | 核对 A：`Rscript R/07_engine_outputs.R` | hov | 12 | 16G | 1:00:00 | 0:07:17 | 4.3 GiB | c130503（AMD EPYC 7702） |
| 6295046 | 核对 B：`Rscript R/06c_bootstrap_check.R longleaf 10` | hov | 11 | 24G | 4:00:00 | 0:02:11 | 3.9 GiB | c0316（Intel Xeon Gold 6140） |
| 6295044 | 单元测试（`R/test_*.R`，依次运行） | hov | 9 | 16G | 3:00:00 | 0:06:45 | 3.2 GiB | c151401 |
| 6294495、6294863 | `renv::restore()`（srun；第二次在补装 zlib 后） | hov | 8 | 16G | 3:00:00 / 2:00:00 | 0:05:03 / 0:02:30 | — | c151409 / c0301 |

- 提交时写的分区是 `-p general`，sacct 记录的实际分区是 hov。
- CPU 数的依据：
  - 核对 A：步骤 7 的进程数是 min(11, detectCores() − 1) = 11，再加主进程；
  - 核对 B：10 个工作进程（每个跑 1 个样本），再加主进程；
  - 单元测试：worker 测试最多用 8 个进程，再加主进程。

## 3. 单元测试

| 测试 | 结果 | 用时 | 要点 |
|---|---|---:|---|
| `test_engine_vectorized.R` | 通过 | 233 s | 3,456 种情形，闭式解与逐周期递推最大差 5.2e-15；死亡来源合计差 2.2e-16；`os_fast` 与 `survival_engine` 差 2.2e-16；DR_first 与 In_DR_early 检查差 0；`survival_engine` 每次 32.0 ms |
| `test_engine_interface.R` | 通过 | 10 s | 重新生成的 `output/phase1/engine_interface_test.csv` 与仓库中的逐字节相同 |
| `test_efs5_constraint.R` | 通过 | 9 s | |
| `test_econ.R` | 通过 | 10 s | 重新生成的 `output/phase2/econ_unit_tests.csv` 只有一个值不同（加入运动效应后的 QALY 差：0.776576681589509 → 0.776576681589493，差 1.6e-14） |
| `test_bootstrap_workers.R` | **退出码 1** | 138 s | 见下 |

`test_bootstrap_workers.R` 用 4 个与 8 个进程，各跑第 1 至 4 个样本（第 1 阶段的种子 20261021）：

| 矩阵 | 值的个数 | 4 与 8 个进程相同 | 差 | 与本机第 1 阶段相同 | 与本机第 1 阶段的最大差 |
|---|---:|---|---:|---|---:|
| efs | 44 | 是 | 0 | 否 | 2.6e-6 |
| os_models | 32 | 是 | 0 | 否 | 6.9e-9 |
| pcr_preprog | 52 | 是 | 0 | 是 | 0 |
| calibration | 92 | 是 | 0 | 否 | 2.8e-6 |
| outputs（百分点） | 244 | 是 | 0 | 否 | 3.1e-7 |
| targets7 | 36 | 是 | 0 | 是 | 0 |

- 在 Longleaf 上，结果与进程数无关：4 个与 8 个进程逐位相同。
- 这个测试还要求与本机第 1 阶段的结果逐位相同（`identical`）。这在同一台机器上成立；换了平台（Windows ucrt 对 conda Linux + OpenBLAS）不能指望逐位相同。
- 差异只出现在拟合与校准的结果中，量级与核对 B 相同；重抽样和抽取的部分完全相同。
- 测试代码未改。
- 测试写出的 3 个文件中，`bootstrap_workers_test.csv` 与 `econ_unit_tests.csv` 有变化，已恢复为仓库中的版本，未提交；`engine_interface_test.csv` 没有变化。Longleaf 上的结果另存在 `/users/y/i/yihanzh/exercise_cea_runs/tests/regenerated/`。

## 4. 核对 A（引擎）

**做法**：按原样运行 `R/07_engine_outputs.R`。它从 `data/bootstrap/boot_replicates.rds`、`data/fits/` 等重建 1,000 个样本，重算 0 至 20 年的曲线和 5、7、10、20 年的表，并写入 `output/phase1/`。然后把重新生成的文件与仓库中的版本（git HEAD）逐值比较。

| 比较的内容 | 说明 |
|---|---|
| `engine_curves.csv` 与 `engine_outputs.csv` | 重新生成的文件 vs 仓库中的文件 |
| `bootstrap_rebuild_check.csv` | 步骤 7 自带的检查：在 Longleaf 上重建的 1,000 个样本的 5、7、10、20 年输出，与本机 `06_bootstrap.R` 存在 `boot_replicates.rds` 中的值比较（双精度，全部值） |

| 文件 | 列 | 值的个数 | 有差的个数 | 最大绝对差 | 位置 |
|---|---|---:|---:|---:|---|
| engine_curves.csv | EFS | 2169 | 235 | 1.14e-13 | arm=chemo, pcr=all, scenario=base, time=6.75 |
| engine_curves.csv | OS | 2169 | 260 | 1.14e-13 | arm=pembro, pcr=pCR, scenario=base, time=12.8333333333333 |
| engine_curves.csv | EFS_lo | 2169 | 292 | 1.14e-13 | arm=chemo, pcr=nonpCR, scenario=base, time=0.833333333333333 |
| engine_curves.csv | EFS_med | 2169 | 244 | 1.14e-13 | arm=chemo, pcr=all, scenario=base, time=11.1666666666667 |
| engine_curves.csv | EFS_hi | 2169 | 266 | 1.14e-13 | arm=pembro, pcr=all, scenario=base, time=12.8333333333333 |
| engine_curves.csv | OS_lo | 2169 | 308 | 1.14e-13 | arm=chemo, pcr=nonpCR, scenario=base, time=1.16666666666667 |
| engine_curves.csv | OS_med | 2169 | 301 | 1.14e-13 | arm=chemo, pcr=all, scenario=base, time=9.66666666666667 |
| engine_curves.csv | OS_hi | 2169 | 330 | 1.14e-13 | arm=chemo, pcr=all, scenario=base, time=4.5 |
| engine_outputs.csv | base | 60 | 8 | 9.95e-14 | endpoint=EFS, scenario=base, arm=chemo, pcr=nonpCR, year=5 |
| engine_outputs.csv | boot_lo | 60 | 8 | 9.95e-14 | endpoint=EFS, scenario=base, arm=chemo, pcr=nonpCR, year=7 |
| engine_outputs.csv | boot_median | 60 | 12 | 1.07e-13 | endpoint=OS, scenario=base, arm=pembro, pcr=nonpCR, year=20 |
| engine_outputs.csv | boot_hi | 60 | 10 | 9.95e-14 | endpoint=EFS, scenario=base, arm=chemo, pcr=all, year=5 |
| engine_outputs.csv | n_replicates | 60 | 0 | 0 | endpoint=EFS, scenario=base, arm=chemo, pcr=all, year=5 |
| bootstrap_rebuild_check.csv（与 boot_replicates.rds 中存的值比） | max_abs_diff | 1000 | — | 1.21e-13 |  |

- **结果**：最大绝对差 1.21e-13 < 1e-10，**通过**。
- CSV 按 15 位有效数字写出；对 40 至 90 之间的值，1e-13 左右的差就是最后一位数字的差。
- 重新生成的文件已恢复为仓库中的版本，未提交。Longleaf 上的结果另存在 `/users/y/i/yihanzh/exercise_cea_runs/checkA/phase1_longleaf/`。
- **用时**：`07_engine_outputs.R` 共 421.7 秒。其中 11 个工作进程里有 9 个启动时等了约 60 秒：renv 提示激活 sandbox 超时，这是同时启动的进程在 NFS 上的锁等待，不影响结果。
- 主进程 CPU 305 秒（计算基准曲线、汇总分位数、作图）。工作进程各 34 至 43 秒，计算期占用率 67% 至 84%。

## 5. 核对 B（bootstrap）

**做法**：`Rscript R/06c_bootstrap_check.R longleaf 10`，用 10 个进程；本机参照用了 11 个。每个样本开始时设 `set.seed(20261023 + b)`，所以结果与进程数无关（见第 3 节）。脚本写出：

- `output/check/bootstrap10_longleaf.rds`
- `output/check/bootstrap10_compare_longleaf.csv`

以下判定根据这两个文件与 `bootstrap10_local.rds` 逐样本比较的结果。

### 判定一：OS 与 EFS

各臂、各时点，10 个样本中的最大绝对差（百分点）。标准：≤ 0.05。

| 臂 | 终点 | 1 年 | 2 年 | 3 年 | 5 年 | 7 年 | 10 年 | 20 年 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| chemo | OS | 1.1e-07 | 3.3e-07 | 1.3e-07 | 5.4e-07 | 9.8e-07 | 1.4e-06 | 1.9e-06 |
| pembro | OS | 2.4e-07 | 5.0e-07 | 5.2e-07 | 4.0e-07 | 2.5e-07 | 9.9e-08 | 1.8e-07 |
| pembro_k1 | OS | 1.4e-07 | 1.5e-07 | 3.4e-08 | 3.6e-07 | 6.5e-07 | 9.5e-07 | 1.3e-06 |
| chemo | EFS | 1.8e-08 | 4.5e-08 | 5.0e-08 | 7.4e-08 | 9.0e-08 | 1.0e-07 | 1.1e-07 |
| pembro | EFS | 3.6e-08 | 6.5e-08 | 8.2e-08 | 1.0e-07 | 1.2e-07 | 1.3e-07 | 1.4e-07 |
| pembro_k1 | EFS | 3.6e-08 | 6.5e-08 | 8.2e-08 | 1.0e-07 | 1.2e-07 | 1.3e-07 | 1.4e-07 |

- 最大值为 1.90e-6（chemo，OS，20 年，样本 4），**通过**。
- pembro_k1 的 EFS 与 pembro 相同（k 不影响 EFS）。

### 判定二：5 年 RMST 两臂差

单位为年。标准：≤ 0.001。

| 样本 | 本机 | Longleaf | 绝对差 |
|---:|---:|---:|---:|
| 1 | 0.118691990 | 0.118691990 | 1.93e-11 |
| 2 | 0.135181137 | 0.135181136 | 6.11e-10 |
| 3 | 0.155611776 | 0.155611776 | 9.68e-11 |
| 4 | 0.140743171 | 0.140743189 | 1.81e-08 |
| 5 | 0.104803572 | 0.104803572 | 5.46e-11 |
| 6 | -0.023067320 | -0.023067318 | 1.80e-09 |
| 7 | 0.071039774 | 0.071039775 | 6.00e-10 |
| 8 | 0.130219249 | 0.130219249 | 1.33e-10 |
| 9 | 0.091266956 | 0.091266956 | 8.08e-11 |
| 10 | 0.138542930 | 0.138542931 | 9.01e-10 |

- 最大值为 1.81e-8（样本 4），**通过**。
- 只供参考：臂 × pCR 的全部输出（`outputs_all`，1,050 个值），最大绝对差 2.65e-6 个百分点。

### 参数（只报告，不作判定）

全表在 `output/check/longleaf_check_params.csv`：95 行（参数，以及约束标志和校准诊断量），列出最大绝对差、最大相对差、所在样本，以及本机与 Longleaf 贴边界的样本。

| 部分 | 参数个数 | 最大绝对差 | 最大相对差 |
|---|---:|---:|---:|
| EFS 模型参数（拟合） | 10 | 9.65e-07 | 8.75e-09 |
| EFS 5 年约束是否起作用（标志） | 4 | 0 | 0 |
| OS 模型参数（拟合，只保存） | 7 | 2.18e-08 | 3.23e-08 |
| pCR 比例与 PreProg 份额（重抽样） | 12 | 0 | 0 |
| 手术前 KM（重抽样） | 32 | 0 | 0 |
| 7 年目标点（抽取） | 8 | 0 | 0 |
| 校准参数（PreProg 中位数与 shape、DR shape、k） | 4 | 2.96e-07 | 3.45e-07 |
| DR 中位数（早、晚；抽取） | 2 | 1.55e-15 | 1.04e-15 |

- 重抽样和抽取的部分（pCR 比例、PreProg 份额、手术前 KM、7 年目标点）完全相同，DR 中位数只差约 1e-15。
- 差异只出现在拟合和校准的参数中。
- 两台机器的重抽次数（`attempts`）都是每个样本 1 次。

**EFS 模型参数**：是否贴边界，指 5 年 EFS 约束是否起作用。

| 参数 | 最大绝对差 | 最大相对差 | 本机 5 年约束起作用的样本 | Longleaf 同 |
|---|---:|---:|---|---|
| EFS_pembro_pCR_shape | 4.94e-09 | 7.06e-09 | 2,3,5 | 2,3,5 |
| EFS_pembro_pCR_scale | 9.65e-07 | 3.18e-09 | 2,3,5 | 2,3,5 |
| EFS_pembro_nonpCR_theta | 2.23e-10 | 3.46e-10 | 无 | 无 |
| EFS_pembro_nonpCR_shape | 7.24e-09 | 8.75e-09 | 无 | 无 |
| EFS_pembro_nonpCR_scale | 5.33e-09 | 4.08e-09 | 无 | 无 |
| EFS_placebo_pCR_shape | 4.83e-09 | 4.68e-09 | 6 | 6 |
| EFS_placebo_pCR_scale | 1.20e-07 | 2.76e-09 | 6 | 6 |
| EFS_placebo_nonpCR_theta | 1.64e-10 | 3.59e-10 | 3,8,9 | 3,8,9 |
| EFS_placebo_nonpCR_shape | 5.80e-09 | 2.68e-09 | 3,8,9 | 3,8,9 |
| EFS_placebo_nonpCR_scale | 4.49e-09 | 4.40e-09 | 3,8,9 | 3,8,9 |

**校准参数**：下表的数值为本机值，差 = Longleaf − 本机。

- 各参数的边界：
  - PreProg 中位数：10 或 26 个月；
  - PreProg shape：u = 1 表示 5 年 PreProg 生存 = 5% 的约束起作用；
  - DR shape：0.01 或 50；
  - k：0.25 或 4。
- 每个样本贴边界的情况，本机与 Longleaf 完全相同。

| 样本 | PreProg 中位数（月） | 边界 | PreProg shape | 边界 | DR shape | 边界 | k | 边界 | 差：中位数 | 差：shape | 差：DR shape | 差：k |
|---:|---:|---|---:|---|---:|---|---:|---|---:|---:|---:|---:|
| 1 | 13.175 | — | 1.9368 | u = 1 | 0.8597 | — | 4.0000 | 4 | -1.1e-08 | -1.3e-08 | 1.1e-08 | 0 |
| 2 | 10.000 | 10 个月 | 1.6387 | u = 1 | 4.2983 | — | 4.0000 | 4 | 0 | 0 | -2.9e-09 | 0 |
| 3 | 10.000 | 10 个月 | 1.6387 | u = 1 | 2.2525 | — | 0.5474 | — | 0 | 0 | 3.9e-08 | -5.9e-09 |
| 4 | 10.000 | 10 个月 | 1.6387 | u = 1 | 0.8575 | — | 1.2253 | — | 0 | 0 | 3.0e-07 | -2.4e-07 |
| 5 | 10.000 | 10 个月 | 1.6387 | u = 1 | 0.6552 | — | 1.2759 | — | 0 | 0 | 1.0e-09 | -5.5e-10 |
| 6 | 10.000 | 10 个月 | 1.6387 | u = 1 | 0.5505 | — | 4.0000 | 4 | 0 | 0 | -5.7e-09 | 0 |
| 7 | 10.000 | 10 个月 | 1.6387 | u = 1 | 1.6585 | — | 4.0000 | 4 | 0 | 0 | 2.9e-08 | 0 |
| 8 | 23.769 | — | 3.1710 | u = 1 | 0.2013 | — | 1.9106 | — | 2.3e-09 | 3.9e-09 | 4.7e-10 | -2.8e-09 |
| 9 | 14.392 | — | 2.0567 | u = 1 | 0.2758 | — | 1.6361 | — | -8.4e-10 | -1.0e-09 | -4.1e-10 | -2.4e-08 |
| 10 | 10.000 | 10 个月 | 1.6387 | u = 1 | 50.0000 | 50 | 2.9475 | — | 0 | 0 | 2.1e-14 | 2.7e-07 |

本机贴边界的情况：

| 参数 | 贴边界的样本 |
|---|---|
| PreProg shape | 全部 10 个样本 u = 1 |
| PreProg 中位数 | 样本 2–7 与 10 在 10 个月 |
| k | 样本 1、2、6、7 在上界 4 |
| DR shape | 样本 10 在上界 50 |

- 贴边界的参数，差为 0 或接近 0。
- 差最大的是样本 4 的 DR shape（3.0e-7）和 k（2.4e-7），这个样本不贴这两个边界。

**L-BFGS-B 的收敛代码**：只有以下两个样本两边不同，最终的目标函数值一致。`bootstrap10_compare_longleaf.csv` 中 calibration 一行的最大差 52（相对差 1e12），就是这个收敛代码。

| 样本 | 本机 | Longleaf |
|---:|---|---|
| 4 | 正常收敛（代码 0） | 最好的起点以代码 52（线搜索失败）结束，按规则加 5 个随机起点，取到的最优解使参数移动 3.3e-7，最终代码 0 |
| 7 | 代码 52，随机起点没有改进，最终代码 52 | 正常收敛（代码 0） |

- 两个样本的目标函数值（SSE）一致：样本 4 差 5.0e-6，样本 7 差 2.6e-6。全部 10 个样本的 SSE 差都在这个量级（绝对值 1.1e-8 至 5.0e-6）。
- OS 输出的最大差（1.9e-6 个百分点）也出现在样本 4。

## 6. 用时与 CPU 占用率（核对 B）

**总用时**：

| 计时 | 秒 |
|---|---:|
| `boot_run()`（脚本记录的 1.86 分钟，含启动工作进程） | 111.4 |
| 整个 `Rscript` | 120.1 |
| 作业 | 131 |

本机参照：11 个进程，2.88 分钟。

**平均每次用时**：

- 10 个进程各跑 1 个样本，所以每个样本的计算时间 ≈ 它所在工作进程的 CPU 时间：平均 59.9 秒，范围 40.0 至 100.6 秒，合计 598.9 CPU 秒。
- 按墙钟算，总用时 ÷ 10 = 11.1 秒（10 个样本并行）。

**每个进程的 CPU 占用率**：每 5 秒读一次各进程的 `/proc/<pid>/stat`。

- 存活期占用率 = CPU 时间 ÷ 进程存活时间；
- 计算期占用率 = 只算 CPU 时间有增长的采样区间。

| 进程 | CPU 时间（秒） | 存活时间（秒） | 存活期 CPU 占用率 | 计算期 CPU 占用率 | 计算时间（秒） |
|---|---:|---:|---:|---:|---:|
| 主进程 | 5.7 | 108.1 | 5% | 36% | 10 |
| renv watchdog | 0.4 | 107.5 | 0% | — | 0 |
| 工作进程 1 | 54.2 | 99.7 | 54% | 91% | 56 |
| 工作进程 2 | 61.7 | 99.7 | 62% | 90% | 66 |
| 工作进程 3 | 45.7 | 99.7 | 46% | 89% | 48 |
| 工作进程 4 | 65.6 | 99.7 | 66% | 95% | 66 |
| 工作进程 5 | 69.8 | 99.7 | 70% | 87% | 76 |
| 工作进程 6 | 40.0 | 99.7 | 40% | 91% | 41 |
| 工作进程 7 | 100.6 | 99.7 | 101% | 100% | 97 |
| 工作进程 8 | 44.5 | 99.7 | 45% | 86% | 48 |
| 工作进程 9 | 67.0 | 99.7 | 67% | 97% | 66 |
| 工作进程 10 | 49.6 | 99.7 | 50% | 83% | 56 |

- 工作进程在计算期的占用率为 83% 至 100%（中位数 90%），没有多线程超订：每个进程最多 2 个线程，BLAS 为 1 个线程。
- 存活期占用率较低（40% 至 101%），是因为先算完的进程要等最慢的样本（100.6 秒）。
- 采样间隔为 5 秒，开始和结束所在的区间会拉低计算期的估计。
- 工作进程按启动顺序编号，与样本号没有对应关系（样本由 `parLapplyLB` 分配）。

核对 A 的进程见第 4 节。

## 7. 文件

本次提交：

- `output/check/longleaf_check.md`（本文件）
- `output/check/bootstrap10_longleaf.rds`、`output/check/bootstrap10_compare_longleaf.csv`（`06c_bootstrap_check.R` 写出）
- `output/check/longleaf_check_params.csv`（核对 B 的参数全表）

只在 Longleaf 上，未提交：`/users/y/i/yihanzh/exercise_cea_runs/`。

| 子目录 | 内容 |
|---|---|
| `restore/` | `renv::restore()` 的脚本与日志 |
| `tools/` | 线程设定的启动文件、CPU 采样脚本 |
| `checkA/`、`checkB/`、`tests/` | 作业脚本、日志、每个进程的 CPU 采样，以及重新生成的输出 |
