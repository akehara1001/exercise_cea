# 10_read_params.R
# Reads input/params/parameters_v6.xlsx (sheet パラメータ; v1 to v5 are in input/params/archive/) into a long table
# (data/params_long.csv: one row per parameter x 基本値/下限/上限) and writes
# output/params_check.md (unfilled rows by owner; non-numeric 基本値; value without source;
# 下限 > 基本値 or 基本値 > 上限).
# Ozaki's returned sheets (2026-10-23): put in input/params/ozaki/, file names containing
# "template_v1" or "template_v2" (at most one of each). Rows owned by 尾崎 take 基本値 to 備考 from
# them, matched by param_id; a row filled in v2 (changed from the delivered v2) is taken from v2,
# otherwise from v1 (Ozaki may fill v1 and only the rows added in v2). Rows owned by 原 always come
# from the internal sheet.
# Probability distributions are set here, not in the sheet: costs and durations gamma,
# proportions and utilities beta, hazard ratios lognormal; parameters from 下限 and 上限 taken
# as a 95% interval. Rows without both bounds get no distribution yet (ranges to be set by us).
# Output: data/params_dist.csv

root <- Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea")
suppressPackageStartupMessages(library(readxl))
src <- file.path(root, "input", "params", "parameters_v6.xlsx")
need <- c("param_id", "区分", "項目", "適用する群", "適用する状態", "単位", "基本値", "下限", "上限",
          "価格の年度", "出典", "出典の該当箇所", "担当", "備考")
fill_cols <- c("基本値", "下限", "上限", "価格の年度", "出典", "出典の該当箇所", "備考")
read_sheet <- function(path) {
  s <- as.data.frame(read_excel(path, sheet = "パラメータ", col_types = "text"), stringsAsFactors = FALSE)
  stopifnot(identical(names(s), need), !anyDuplicated(s$param_id))
  s
}
x <- read_sheet(src)
blank <- function(v) is.na(v) | trimws(v) == ""
num <- function(v) suppressWarnings(as.numeric(gsub(",", "", trimws(v))))

# Ozaki's returned v1 / v2
oz_dir <- file.path(root, "input", "params", "ozaki")
oz_file <- function(ver) {
  f <- list.files(oz_dir, pattern = paste0("template_", ver, ".*\\.xlsx$"), full.names = TRUE)
  f <- f[!grepl("^~\\$", basename(f))]
  if (length(f) > 1) stop("more than one returned ", ver, " in ", oz_dir, ": ", paste(basename(f), collapse = ", "))
  if (length(f)) f else NA_character_
}
oz_files <- c(v1 = oz_file("v1"), v2 = oz_file("v2"))
oz <- lapply(oz_files, function(f) if (is.na(f)) NULL else read_sheet(f))
# the sheets as delivered: a returned row counts as filled only where it differs from these
# (the delivered sheets already hold our 備考 on some rows of 尾崎, and our values on rows of 原)
tpl <- list(v1 = read_sheet(file.path(root, "input", "params", "archive", "parameters_template_v1.xlsx")),
            v2 = read_sheet(file.path(root, "input", "params", "parameters_template_v2.xlsx")))
norm <- function(v) ifelse(blank(v), "", trimws(v))
filled_in <- function(ver, id) {   # the returned row for id if 基本値 to 備考 differ from the delivered sheet, else NULL
  s <- oz[[ver]]; t <- tpl[[ver]]
  if (is.null(s) || !(id %in% s$param_id)) return(NULL)
  r <- s[s$param_id == id, , drop = FALSE]
  r0 <- if (id %in% t$param_id) t[t$param_id == id, fill_cols] else rep(NA, length(fill_cols))
  if (identical(norm(unlist(r[fill_cols])), norm(unlist(r0)))) NULL else r
}
x$記入元 <- ifelse(x$担当 == "尾崎", "", "内部表")
conflict <- character(0)
for (id in x$param_id[x$担当 == "尾崎"]) {
  r1 <- filled_in("v1", id); r2 <- filled_in("v2", id)
  use <- if (!is.null(r2)) r2 else r1
  if (is.null(use)) next
  if (!is.null(r1) && !is.null(r2) && !identical(unlist(r1[fill_cols]), unlist(r2[fill_cols]))) conflict <- c(conflict, id)
  x[x$param_id == id, fill_cols] <- use[fill_cols]
  x$記入元[x$param_id == id] <- if (!is.null(r2)) "尾崎 v2" else "尾崎 v1"
}
oz_not_owned <- unique(unlist(lapply(names(oz), function(ver) if (is.null(oz[[ver]])) NULL else
  Filter(function(id) !is.null(filled_in(ver, id)), setdiff(oz[[ver]]$param_id, x$param_id[x$担当 == "尾崎"])))))
oz_unknown <- unique(unlist(lapply(oz, function(s) setdiff(s$param_id, x$param_id))))

meta <- x[, c("param_id", "区分", "項目", "適用する群", "適用する状態", "単位", "担当", "記入元", "価格の年度", "出典", "出典の該当箇所", "備考")]
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

# notes on single rows (Ozaki's reply of 2026-10-23)
note_of <- setNames(rep("", nrow(x)), x$param_id)
if (x$記入元[x$param_id == "F01"] == "尾崎 v1")
  note_of["F01"] <- "v1 で記入された値。定義を gBRCA 陰性例の中での割合に変えたため、尾崎先生の確認が必要"
for (id in c("F01P", "F04P")) if (unfilled[x$param_id == id]) note_of[id] <- "臨床の先生の回答待ち"

# check report
lst <- function(idx) if (!any(idx)) "- なし" else
  sprintf("- %s %s（%s）%s", x$param_id[idx], x$項目[idx], x$担当[idx],
          ifelse(note_of[x$param_id[idx]] == "", "", paste0("：", note_of[x$param_id[idx]])))
ids_or_none <- function(v) if (length(v)) paste(v, collapse = "、") else "なし"
oz_line <- function(ver) if (is.na(oz_files[[ver]])) sprintf("- %s：未着（`input/params/ozaki/` に該当ファイルなし）", ver) else
  sprintf("- %s：`%s`（記入のある尾崎の行 %d）", ver, basename(oz_files[[ver]]), sum(x$記入元 == paste("尾崎", ver)))
L <- c("# パラメータ入力表の確認",
       "",
       sprintf("対象：`input/params/parameters_v6.xlsx`（%d 行）。`R/10_read_params.R` が生成。", nrow(x)),
       "",
       "## 0. 尾崎先生の返送分（param_id で結合、v2 に記入のある行は v2、なければ v1）", "",
       oz_line("v1"), oz_line("v2"),
       sprintf("- v1 と v2 の両方に記入があり内容が異なる行（v2 を採用）：%s", ids_or_none(conflict)),
       sprintf("- 担当が尾崎でない行への記入（採用しない）：%s", ids_or_none(oz_not_owned)),
       sprintf("- 内部表にない param_id：%s", ids_or_none(oz_unknown)),
       "",
       "## 1. 基本値が未記入の行（担当別）", "")
for (ow in c("尾崎", "原")) {
  idx <- unfilled & x$担当 == ow
  L <- c(L, sprintf("### %s（%d / %d 行）", ow, sum(idx), sum(x$担当 == ow)), "", lst(idx), "")
}
noted <- note_of != "" & !unfilled
L <- c(L, "## 2. 基本値が数値でない行", "", lst(nonnum), "",
       "## 3. 値はあるが出典がない行", "", lst(nosrc), "",
       "## 4. 下限 > 基本値 または 基本値 > 上限 の行", "", lst(badrng), "",
       "## 5. 記入済みで確認が必要な行", "", lst(noted), "",
       "## 参考：下限または上限が数値でない行", "", lst(nonnum_bounds), "",
       "## 参考：確率分布（コードで設定）", "",
       "費用と期間はガンマ分布、割合と効用値はベータ分布、ハザード比は対数正規分布。下限と上限を95%区間とみなしてパラメータを求める（`data/params_dist.csv`）。",
       "",
       sprintf("- 分布のパラメータが決まった行：%d", sum(!is.na(D$p1))),
       sprintf("- 幅未設定の行（基本値あり、下限か上限が空欄）：%d", sum(D$note == "幅未設定")))
writeLines(L, file.path(root, "output", "params_check.md"), useBytes = TRUE)
cat(sprintf("rows %d; unfilled 尾崎 %d/%d, 原 %d/%d; non-numeric %d; no source %d; bad range %d; Ozaki v1 %s, v2 %s\n", nrow(x),
            sum(unfilled & x$担当 == "尾崎"), sum(x$担当 == "尾崎"), sum(unfilled & x$担当 == "原"), sum(x$担当 == "原"),
            sum(nonnum), sum(nosrc), sum(badrng), basename(oz_files[["v1"]]), basename(oz_files[["v2"]])))
