# 21_phase2a_report.R
# Builds output/phase2/phase2a_report.md from the code outputs: unit tests of the cost and QALY
# layer (output/phase2/econ_unit_tests.csv) and the list of sources for the rows owned by 原
# (data/params_hara/hara_values.csv). By instruction it contains no ICER or other result value.

source("C:/Users/原明美/Documents/ClaudeCode/exercise_cea/R/config.R")
out_dir <- file.path(ROOT, "output", "phase2")
rd <- function(...) read.csv(file.path(ROOT, ...), stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)
md_table <- function(df) {
  esc <- function(x) gsub("\\|", "\\\\|", ifelse(is.na(x), "", as.character(x)))
  c(paste0("| ", paste(names(df), collapse = " | "), " |"),
    paste0("|", paste(rep("---", ncol(df)), collapse = "|"), "|"),
    apply(df, 1, function(r) paste0("| ", paste(esc(r), collapse = " | "), " |")))
}
UT <- rd("output", "phase2", "econ_unit_tests.csv")
HV <- rd("data", "params_hara", "hara_values.csv")
PL <- rd("data", "params_long.csv")
base <- PL[PL$stat == "基本値", ]
L <- character(0); add <- function(...) L <<- c(L, ...)

add("# 第2阶段 2a 报告：费用与 QALY 层（单元测试）与原负责的参数来源", "",
    sprintf("生成时间：%s。由 `R/21_phase2a_report.R` 从代码输出生成。按指示本报告不含任何 ICER 或结果数值。", format(Sys.time(), "%Y-%m-%d %H:%M")), "")
add("## 1. 状态", "",
    sprintf("- 入力表 v4（`input/params/parameters_v4.xlsx`；v1 至 v3 移至 `input/params/archive/`）：原负责的 %d 行已填写（另有此前已填的 F07、F08；v3 新增 B32P、B32C，v4 新增 B33P、B33C，供 U05 使用）；尾崎负责的行未动，其中已填写 %d / %d 行。",
            nrow(HV), sum(!is.na(base$value) & base$担当 == "尾崎"), sum(base$担当 == "尾崎")),
    "- 费用与 QALY 层：`R/econ.R`（规格见 `docs/model_spec.md` 第 5 节）。尾崎的行尚未返回，故只用合成数值做单元测试（`R/test_econ.R`）；生存参数用第 1 阶段第六轮的校准值，测试中 k 设为测试值 1.5（只检验结构）。严重不良事件的效用下降 U05 乘以各臂 6 种 3 级以上不良事件发生率之和（按事件计，B33P、B33C；与来源 Favre-Bulle 2024 的口径一致，v4）；任何 3 级以上不良事件的发生率（B32P、B32C）为情景。v3 把口径改成「任何 3 级以上」是指令错误，v4 已改回。",
    "- 未计入（待尾崎回答或第 2 阶段后续）：S-JP 的费用（F02、F05、F06）与混合方式；运动效应参数。", "")
add("## 2. 单元测试（`output/phase2/econ_unit_tests.csv`）", "",
    md_table(data.frame(测试 = UT$test, 结果 = ifelse(UT$result == "pass", "通过", "**不通过**"),
                        检查的差或比较值 = ifelse(is.na(UT$value), "", formatC(UT$value, format = "g", digits = 3)), check.names = FALSE)), "",
    sprintf("共 %d 项，通过 %d 项。第 6、8 项的数值为比较量之差（全部死亡对癌症死亡的终末期费用；运动对单用化疗的 QALY），只用于判断方向，不是模型结果。", nrow(UT), sum(UT$result == "pass")), "")
add("## 3. 原负责的参数与来源（详见 `input/params/sources_hara.md`）", "",
    md_table(data.frame(param_id = HV$param_id, 出典 = HV$出典, 该当箇所 = HV$出典の該当箇所, check.names = FALSE)), "")
writeLines(L, file.path(out_dir, "phase2a_report.md"), useBytes = TRUE)
cat("wrote phase2a_report.md:", length(L), "lines\n")
