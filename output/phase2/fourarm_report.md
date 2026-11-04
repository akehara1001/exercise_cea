# 运动 CEA 第 11 节：四组增量分析与净收益分界点（内部检查用）

生成：2026-11-04 14:59 EST，`R/25_four_arm.R`（运行时 git HEAD 744048c「Plan section 11: four-arm incremental analysis and NMB break-even (before computation)」；`R/25_four_arm.R` 的 git blob 862a22d83161072022da6d8f2752368fce424e97，脚本与结果在同一提交）。依据：`docs/analysis_plan_phase2.md` 第 11 节（尾崎 2026-11-04 邮件）。计算部分运行时间 0.1 分钟。

**本报告只供内部检查。** 入力表中备考有【要確認】的 9 行（B03、B04、B07、B08、B09、B10、D02、E03、F01P）为暂定值（计划第 7 节）。

确定性计算：基准参数、基准栏（不用「早期复发后 k（外部）」，不用 S-JP）；运动效应为路径 A 基准定义（随机化后 5 年内保持 hr0，之后半衰期 1 年），两个运动组同一 hr0。运动方案费用 E02（192,400 日元，时点 0 全员）计入两个运动组的总费用。金额单位千日元（half up）。净收益 = λ × QALY − 费用。

## A. 四组的增量分析（方案费用 E02）

按总费用升序。Δ与 ICER 相对「对照」列的组（费用低于该组的最近的前沿组）；被强支配的组只给 Δ，不给 ICER。

### hr0 = 0.95

| 组 | 总费用（千日元） | 总 QALY | 对照 | Δ费用（千日元） | ΔQALY | ICER（千日元/QALY） | status | 相对化疗的净收益（λ 500 万，千日元） |
|---|---|---|---|---|---|---|---|---|
| 化疗 + 运动 | 12,112 | 17.073 | — | — | — | — | frontier | 931 |
| 化疗 | 12,202 | 16.905 | 化疗 + 运动 | 91 | -0.168 | — | dominated（被化疗 + 运动支配） | 0 |
| 化疗 + 帕博利珠单抗 + 运动 | 16,592 | 19.194 | 化疗 + 运动 | 4,480 | 2.121 | 2,112 | frontier | 7,056 |
| 化疗 + 帕博利珠单抗 | 16,629 | 19.061 | 化疗 + 帕博利珠单抗 + 运动 | 37 | -0.133 | — | dominated（被化疗 + 帕博利珠单抗 + 运动支配） | 6,355 |

### hr0 = 0.85

| 组 | 总费用（千日元） | 总 QALY | 对照 | Δ费用（千日元） | ΔQALY | ICER（千日元/QALY） | status | 相对化疗的净收益（λ 500 万，千日元） |
|---|---|---|---|---|---|---|---|---|
| 化疗 + 运动 | 11,525 | 17.420 | — | — | — | — | frontier | 3,250 |
| 化疗 | 12,202 | 16.905 | 化疗 + 运动 | 677 | -0.515 | — | dominated（被化疗 + 运动支配） | 0 |
| 化疗 + 帕博利珠单抗 + 运动 | 16,120 | 19.466 | 化疗 + 运动 | 4,594 | 2.047 | 2,245 | frontier | 8,889 |
| 化疗 + 帕博利珠单抗 | 16,629 | 19.061 | 化疗 + 帕博利珠单抗 + 运动 | 509 | -0.405 | — | dominated（被化疗 + 帕博利珠单抗 + 运动支配） | 6,355 |

### hr0 = 0.72

| 组 | 总费用（千日元） | 总 QALY | 对照 | Δ费用（千日元） | ΔQALY | ICER（千日元/QALY） | status | 相对化疗的净收益（λ 500 万，千日元） |
|---|---|---|---|---|---|---|---|---|
| 化疗 + 运动 | 10,723 | 17.892 | — | — | — | — | frontier | 6,413 |
| 化疗 | 12,202 | 16.905 | 化疗 + 运动 | 1,479 | -0.987 | — | dominated（被化疗 + 运动支配） | 0 |
| 化疗 + 帕博利珠单抗 + 运动 | 15,479 | 19.834 | 化疗 + 运动 | 4,756 | 1.942 | 2,449 | frontier | 11,368 |
| 化疗 + 帕博利珠单抗 | 16,629 | 19.061 | 化疗 + 帕博利珠单抗 + 运动 | 1,150 | -0.773 | — | dominated（被化疗 + 帕博利珠单抗 + 运动支配） | 6,355 |

## B. 分界点

QALY 相等：「化疗 + 运动 对 化疗」的 ΔQALY = 「化疗 + 帕博利珠单抗 对 化疗」的 ΔQALY（同一把尺子，`det_yardstick.csv`）。净收益相等：λ × ΔQALY_运动 − Δ费用_运动（不含方案费用） − E02 = λ × ΔQALY_帕博利珠单抗 − Δ费用_帕博利珠单抗，即两组都计入 E02 时净收益相等；hr0 轴 [0.30, 1.00]（路径 A 基准定义），pCR 轴为 pCR 比例的提高幅度 [0, 37] 个百分点（路径 B）；`uniroot`，tol 1e-6。

| 分界点 | λ（万日元/QALY） | hr0 | pCR 提高（个百分点） |
|---|---|---|---|
| QALY 相等 | — | 0.425 | 35.9 |
| 净收益相等（E02） | 500 | 0.722 | 19.0 |
| 净收益相等（E02） | 750 | 0.638 | 24.1 |

各分界点在区间两端的 f（= 左边 − 右边，千日元）与备注：

| λ（万日元/QALY） | 轴 | 根 | f（下端） | f（上端） | 备注 |
|---|---|---|---|---|---|
| 500 | hr0 | 0.7223 | 11,541 | -6,548 | — |
| 500 | pcr | 18.96 | -6,548 | 6,233 | outside the main axis (pCR gain > 10 points) |
| 750 | hr0 | 0.6379 | 12,890 | -11,939 | outside the main axis (hr0 < 0.70) |
| 750 | pcr | 24.08 | -11,939 | 6,405 | outside the main axis (pCR gain > 10 points) |

QALY 相等（`det_yardstick.csv`）：hr0 在主轴之外、pCR 在主轴之外（主轴为 hr0 0.70–1.00、pCR 提高 0–10 个百分点）。pCR 轴的根以个百分点表示（上表为两位小数）。

## C. 方案费用取 E01、E03 时的 status（脚注用）

E01 239,508 日元，E02 192,400 日元，E03 11,260 日元（基本值）。E01、E03 的总费用由 `econ_arm()` 以 `exercise_cost = "E01"`、`"E03"` 重跑得到。

| hr0 | 方案费用 | 化疗 | 化疗 + 运动 | 化疗 + 帕博利珠单抗 | 化疗 + 帕博利珠单抗 + 运动 |
|---|---|---|---|---|---|
| 0.95 | E01 | dominated（被化疗 + 运动支配） | frontier | extendedly dominated（介于化疗 + 运动与化疗 + 帕博利珠单抗 + 运动之间） | frontier |
| 0.95 | E02（主） | dominated（被化疗 + 运动支配） | frontier | dominated（被化疗 + 帕博利珠单抗 + 运动支配） | frontier |
| 0.95 | E03 | dominated（被化疗 + 运动支配） | frontier | dominated（被化疗 + 帕博利珠单抗 + 运动支配） | frontier |
| 0.85 | E01 | dominated（被化疗 + 运动支配） | frontier | dominated（被化疗 + 帕博利珠单抗 + 运动支配） | frontier |
| 0.85 | E02（主） | dominated（被化疗 + 运动支配） | frontier | dominated（被化疗 + 帕博利珠单抗 + 运动支配） | frontier |
| 0.85 | E03 | dominated（被化疗 + 运动支配） | frontier | dominated（被化疗 + 帕博利珠单抗 + 运动支配） | frontier |
| 0.72 | E01 | dominated（被化疗 + 运动支配） | frontier | dominated（被化疗 + 帕博利珠单抗 + 运动支配） | frontier |
| 0.72 | E02（主） | dominated（被化疗 + 运动支配） | frontier | dominated（被化疗 + 帕博利珠单抗 + 运动支配） | frontier |
| 0.72 | E03 | dominated（被化疗 + 运动支配） | frontier | dominated（被化疗 + 帕博利珠单抗 + 运动支配） | frontier |

## 核对

| 核对 | 内容 | 值 | 界限 | 结果 |
|---|---|---|---|---|
| programme_E01 | cost_E01 − cost：运动两组 = E01 − E02，其余两组 = 0（12 行） | 8.44011e-10 | 1e-06 | 通过 |
| programme_E03 | cost_E03 − cost：运动两组 = E03 − E02，其余两组 = 0（12 行） | 0 | 1e-06 | 通过 |
| expected_hr0_500 | λ 500 万的 hr0 根（det_caps.csv 次比较 hr0 0.700、0.725 的 cap_500 线性内插 = 0.7223） | 0.722294 | [0.700, 0.725] | 通过 |
| expected_hr0_750 | λ 750 万的 hr0 根 | 0.637851 | < 0.70 | 通过 |
| det_caps_secondary_0.95 | exercise 对 chemo（hr0 0.95）的 dQ、dC（减 E02）对 det_caps.csv secondary/base：最大绝对差 | 5.64614e-09 | 1e-06 | 通过 |
| det_caps_main_0.95 | both 对 pembro（hr0 0.95）的 dQ、dC（减 E02）对 det_caps.csv main/base：最大绝对差 | 2.20316e-08 | 1e-06 | 通过 |
| det_caps_secondary_0.85 | exercise 对 chemo（hr0 0.85）的 dQ、dC（减 E02）对 det_caps.csv secondary/base：最大绝对差 | 3.31784e-08 | 1e-06 | 通过 |
| det_caps_main_0.85 | both 对 pembro（hr0 0.85）的 dQ、dC（减 E02）对 det_caps.csv main/base：最大绝对差 | 3.31784e-08 | 1e-06 | 通过 |
| det_reference | pembro 对 chemo 的 dC、dQ（三个 hr0 的行）对 det_reference.csv base：最大绝对差 | 2.04891e-08 | 1e-06 | 通过 |
| yardstick_hr0 | solve() 解 dQ_sec(hr0) = dQ_ref（det_yardstick.csv：0.424844，tol 1e-7） | 0.424844 | 0.4248（4 位小数） | 通过 |

### 单元测试

`Rscript R/25_four_arm.R tests`（2026-11-04 15:00 EST；运行时 `R/25_four_arm.R` 的 git blob 862a22d83161072022da6d8f2752368fce424e97，`R/test_four_arm.R` 的 git blob 500af0499a4c2ff4f9e35053a6011b768a9e9f56）。每个测试以 `Rscript -e "source('R/<测试>'); cat('<完成标记>')"` 运行。

判定（与计划 11.4 不同，见计划 11.4 追记）：完成标记出现（测试脚本运行到最后，`stopifnot` 等未报错）且输出中没有 "Execution halted"。计划写的「退出码 0」在本机不能用：本机的 R 是 x64 版在 ARM64 上仿真，Rscript 正常结束后退出码也是 127（直接运行）或 255（经 `system2`），例如 `R/test_econ.R` 打印 "all econ unit tests passed" 后退出码 127。退出码只作记录。

| 测试 | 完成标记 | Execution halted | 退出码 | 结果 | 时间（分钟） |
|---|---|---|---|---|---|
| `R/test_bootstrap_workers.R` | 有 | 无 | 255 | 通过 | 0.7 |
| `R/test_econ.R` | 有 | 无 | 255 | 通过 | 0.3 |
| `R/test_efs5_constraint.R` | 有 | 无 | 255 | 通过 | 0.3 |
| `R/test_engine_efs_consistency.R` | 有 | 无 | 255 | 通过 | 0.2 |
| `R/test_engine_interface.R` | 有 | 无 | 255 | 通过 | 0.2 |
| `R/test_engine_vectorized.R` | 有 | 无 | 255 | 通过 | 19.5 |
| `R/test_four_arm.R` | 有 | 无 | 255 | 通过 | 0.2 |

合计 7/7 通过。

## 文件

`output/phase2/main/` 中：`fourarm_totals.csv`（四组的总量与净收益）、`fourarm_incremental.csv`（增量分析，programme 列 E01–E03）、`fourarm_nmb_equal.csv`（净收益分界点）、`fourarm_checks.csv`（核对）、`fourarm_run.csv`（运行信息）、`fourarm_unit_tests.csv`（`R/test_four_arm.R` 的结果）、`fourarm_test_runs.csv`（单元测试的运行记录）。
