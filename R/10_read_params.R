# 10_read_params.R
# Reads input/params/parameters_v4.xlsx (sheet パラメータ; v1 to v3 are in input/params/archive/) into a long table
# (data/params_long.csv: one row per parameter x 基本値/下限/上限) and writes
# output/params_check.md (unfilled rows by owner; non-numeric 基本値; value without source;
# 下限 > 基本値 or 基本値 > 上限).
# Probability distributions are set here, not in the sheet: costs and durations gamma,
# proportions and utilities beta, hazard ratios lognormal; parameters from 下限 and 上限 taken
# as a 95% interval. Rows without both bounds get no distribution yet (ranges to be set by us).
# Output: data/params_dist.csv

root <- Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea")
suppressPackageStartupMessages(library(readxl))
src <- file.path(root, "input", "params", "parameters_v4.xlsx")
x <- read_excel(src, sheet = "パラメータ", col_types = "text")
x <- as.data.frame(x, stringsAsFactors = FALSE)
need <- c("param_id", "区分", "項目", "適用する群", "適用する状態", "単位", "基本値", "下限", "上限",
          "価格の年度", "出典", "出典の該当箇所", "担当", "備考")
stopifnot(identical(names(x), need), !anyDuplicated(x$param_id))
blank <- function(v) is.na(v) | trimws(v) == ""
num <- function(v) suppressWarnings(as.numeric(gsub(",", "", trimws(v))))

meta <- x[, c("param_id", "区分", "項目", "適用する群", "適用する状態", "単位", "担当", "価格の年度", "出典", "出典の該当箇所", "備考")]
long <- do.call(rbind, lapply(c("基本値", "下限", "上限"), function(st)
  data.frame(meta, stat = st, value_raw = x[[st]], value = num(x[[st]]), stringsAsFactors = FALSE)))
long <- long[order(match(long$param_id, x$param_id), match(long$stat, c("基本値", "下限", "上限"))), ]
write.csv(long, file.path(root, "data", "params_long.csv"), row.names = FALSE, fileEncoding = "UTF-8", na = "")

b <- num(x$基本値); lo <- num(x$下限); hi <- num(x$上限)
unfilled <- blank(x$基本値)
nonnum <- !blank(x$基本値) & is.na(b)
nosrc <- !blank(x$基本値) & blank(x$出典)
badrng <- (!is.na(lo) & !is.na(b) & lo > b) | (!is.na(hi) & !is.na(b) & b > hi)
nonnum_bounds <- (!blank(x$下限) & is.na(lo)) | (!blank(x$上限) & is.na(hi))

# distributions
dist_of <- function(unit) ifelse(grepl("ハザード比", unit), "lognormal",
                          ifelse(grepl("^割合|^効用値", unit), "beta",
                          ifelse(grepl("^円|^月", unit), "gamma", NA)))
z <- qnorm(0.975)
D <- data.frame(param_id = x$param_id, 単位 = x$単位, dist = dist_of(x$単位), base = b, lower = lo, upper = hi,
                p1 = NA_real_, p2 = NA_real_, note = "", stringsAsFactors = FALSE)
for (i in seq_len(nrow(D))) {
  if (is.na(D$base[i])) { D$note[i] <- "基本値未記入"; next }
  if (is.na(D$lower[i]) || is.na(D$upper[i])) { D$note[i] <- "幅未設定"; next }
  if (D$dist[i] == "lognormal") {
    D$p1[i] <- log(D$base[i]); D$p2[i] <- (log(D$upper[i]) - log(D$lower[i])) / (2 * z)     # meanlog, sdlog
  } else {
    s <- (D$upper[i] - D$lower[i]) / (2 * z)
    if (D$dist[i] == "gamma") {
      D$p1[i] <- (D$base[i] / s)^2; D$p2[i] <- s^2 / D$base[i]                               # shape, scale
    } else {
      k <- D$base[i] * (1 - D$base[i]) / s^2 - 1
      if (k <= 0) { D$note[i] <- "幅が広すぎてベータ分布にできない"; next }
      D$p1[i] <- D$base[i] * k; D$p2[i] <- (1 - D$base[i]) * k                              # alpha, beta
    }
  }
}
write.csv(D, file.path(root, "data", "params_dist.csv"), row.names = FALSE, fileEncoding = "UTF-8", na = "")

# check report
lst <- function(idx) if (!any(idx)) "- なし" else
  sprintf("- %s %s（%s）", x$param_id[idx], x$項目[idx], x$担当[idx])
L <- c("# パラメータ入力表の確認",
       "",
       sprintf("対象：`input/params/parameters_v4.xlsx`（%d 行）。`R/10_read_params.R` が生成。", nrow(x)),
       "",
       "## 1. 基本値が未記入の行（担当別）", "")
for (ow in c("尾崎", "原")) {
  idx <- unfilled & x$担当 == ow
  L <- c(L, sprintf("### %s（%d / %d 行）", ow, sum(idx), sum(x$担当 == ow)), "", lst(idx), "")
}
L <- c(L, "## 2. 基本値が数値でない行", "", lst(nonnum), "",
       "## 3. 値はあるが出典がない行", "", lst(nosrc), "",
       "## 4. 下限 > 基本値 または 基本値 > 上限 の行", "", lst(badrng), "",
       "## 参考：下限または上限が数値でない行", "", lst(nonnum_bounds), "",
       "## 参考：確率分布（コードで設定）", "",
       "費用と期間はガンマ分布、割合と効用値はベータ分布、ハザード比は対数正規分布。下限と上限を95%区間とみなしてパラメータを求める（`data/params_dist.csv`）。",
       "",
       sprintf("- 分布のパラメータが決まった行：%d", sum(!is.na(D$p1))),
       sprintf("- 幅未設定の行（基本値あり、下限か上限が空欄）：%d", sum(D$note == "幅未設定")))
writeLines(L, file.path(root, "output", "params_check.md"), useBytes = TRUE)
cat(sprintf("rows %d; unfilled 尾崎 %d/%d, 原 %d/%d; non-numeric %d; no source %d; bad range %d\n", nrow(x),
            sum(unfilled & x$担当 == "尾崎"), sum(x$担当 == "尾崎"), sum(unfilled & x$担当 == "原"), sum(x$担当 == "原"),
            sum(nonnum), sum(nosrc), sum(badrng)))
