# 21_phase2a_report.R
# Builds output/phase2/phase2a_report.md from the code outputs: unit tests of the cost and QALY
# layer (output/phase2/econ_unit_tests.csv) and the list of sources for the rows owned by 原
# (data/params_long.csv, read from the internal sheet by R/10_read_params.R). By instruction it
# contains no ICER or other result value.

source(file.path(Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"), "R", "config.R"))
out_dir <- file.path(ROOT, "output", "phase2")
rd <- function(...) read.csv(file.path(ROOT, ...), stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)
md_table <- function(df) {
  esc <- function(x) gsub("\\|", "\\\\|", ifelse(is.na(x), "", as.character(x)))
  c(paste0("| ", paste(names(df), collapse = " | "), " |"),
    paste0("|", paste(rep("---", ncol(df)), collapse = "|"), "|"),
    apply(df, 1, function(r) paste0("| ", paste(esc(r), collapse = " | "), " |")))
}
UT <- rd("output", "phase2", "econ_unit_tests.csv")
PL <- rd("data", "params_long.csv")
PD <- rd("data", "params_dist.csv")
base <- PL[PL$stat == "基本値", ]
src_sheet <- sub(".*`(input/params/[^`]+)`.*", "\\1", grep("^対象：", readLines(file.path(ROOT, "output", "params_check.md"), encoding = "UTF-8"), value = TRUE)[1])
oz <- base[base$担当 == "尾崎", ]; ha <- base[base$担当 == "原", ]
L <- character(0); add <- function(...) L <<- c(L, ...)

add("# 第2阶段 2a 报告：费用与 QALY 层（单元测试）与原负责的参数来源", "",
    sprintf("生成时间：%s。由 `R/21_phase2a_report.R` 从代码输出生成。按指示本报告不含任何 ICER 或结果数值。", format(Sys.time(), "%Y-%m-%d %H:%M")), "")
add("## 1. 状态", "",
    sprintf("- 内部入力表（`%s`；此前各版在 `input/params/archive/`）：原负责的 %d 行中已填写 %d 行；尾崎负责的 %d 行中已填写 %d 行（`output/params_check.md`）。",
            src_sheet, nrow(ha), sum(!is.na(ha$value)), nrow(oz), sum(!is.na(oz$value))),
    "- 费用与 QALY 层：`R/econ.R`（规格见 `docs/model_spec.md` 第 2、5 节）。单元测试（`R/test_econ.R`）只用合成数值，检验结构，不用入力表的值；生存参数为第 1 阶段的引擎默认（`data/fits/engine_params.rds`，第十五轮）；k 开关的测试用测试值 k = 1.5。",
    "- 已实现（2026-10-25）：运动的筋骨格系有害事象（费用：加运动的两臂 E06 × E08、不加运动的两臂 E07 × E08；效用：E09 或 E10 × U05 × 12.5 周；都在时点 0 一次计入，E09、E10 为空时不计效用损失）；S-JP 的三条曲线按 `sjp_mix()` 的权重混合，F02、F05 计入接受者（手术时点仍无事件的 non-pCR 患者 × 组权重，折现到手术时点）；F06（BRCA 检测）在时点 0 对全部患者计入四个组；远处复发一线治疗的月额与持续期间按组取值（含帕博利珠单抗的两组用 D03P、D04P，其余用 D03、D04；D05 共用）。",
    sprintf("- 尾崎的数值（2026-10-25 取入：记入案 v1 → 内部入力表 v7，`R/py/22_params_v7.py`；v8 起按幅的规则调整，`R/py/23_params_v8.py`；审阅记录 `output/params_ozaki_v1_review.md`）：%d 行全部填写；备考有【要確認】的 %d 行作为暂定值使用。",
            nrow(oz), sum(grepl("【要確認", oz$備考, fixed = TRUE))),
    sprintf("- 幅的规则（`data/params_dist.csv` 的 range_rule，`docs/model_spec.md` 第 6 节）：基本值 ±25%% 或单侧对称 %d 行，薬価固定 %d 行，0例：PSAは固定 %d 行；概率敏感性分析中固定为基本值的共 %d 行；既无分布参数也未指定固定的 %d 行%s。按指示尚未运行任何经济学结果，不输出任何结果数值。",
            sum(PD$range_rule %in% c("±25%", "片側対称")), sum(PD$range_rule == "薬価固定"), sum(PD$range_rule == "0例：PSAは固定"),
            sum(PD$dist %in% "fixed"), sum(is.na(PD$p1) & !(PD$dist %in% "fixed")),
            if (any(is.na(PD$p1) & !(PD$dist %in% "fixed"))) paste0("（", paste(PD$param_id[is.na(PD$p1) & !(PD$dist %in% "fixed")], collapse = "、"), "，待定）") else ""), "")
diff_tests <- grepl("终末期费用|加入运动效应", UT$test)
add("## 2. 单元测试（`output/phase2/econ_unit_tests.csv`）", "",
    md_table(data.frame(序号 = seq_len(nrow(UT)), 测试 = UT$test, 结果 = ifelse(UT$result == "pass", "通过", "**不通过**"),
                        检查的差或比较值 = ifelse(is.na(UT$value), "", formatC(UT$value, format = "g", digits = 3)), check.names = FALSE)), "",
    sprintf("共 %d 项，通过 %d 项（第 1 至 11 项为原有各项，其中第 3 项自 2026-10-25 起同时要求 E06 = E07 且 E09 = E10；第 12 至 %d 项为 2026-10-25 新增）。数值一栏为检查的偏差；其中第 %s 项为比较量之差（全部死亡对癌症死亡的终末期费用；运动对单用化疗的 QALY），只用于判断方向，不是模型结果。",
            nrow(UT), sum(UT$result == "pass"), nrow(UT), paste(which(diff_tests), collapse = "、")), "")
add("## 3. 原负责的参数与来源（详见 `input/params/sources_hara.md`、`input/params/efficacy_sources.md`、`input/papers/SOURCE.md`）", "",
    md_table(data.frame(param_id = ha$param_id, 出典 = ha$出典, 该当箇所 = ha$出典の該当箇所, check.names = FALSE)), "")
writeLines(L, file.path(out_dir, "phase2a_report.md"), useBytes = TRUE)
cat("wrote phase2a_report.md:", length(L), "lines\n")
