# 10_read_params.R
# Reads input/params/parameters_v10.xlsx (sheet パラメータ; v1 to v9 are in input/params/archive/) into a long table
# (data/params_long.csv: one row per parameter x 基本値/下限/上限) and writes
# output/params_check.md (unfilled rows by owner; non-numeric 基本値; value without source;
# 下限 > 基本値 or 基本値 > 上限; returned sheets of Ozaki against the internal sheet).
# Ozaki's values (2026-10-25: input/params/ozaki/parameters_v1_尾崎記入案.xlsx, his v1 with six rows
# appended) are copied into the internal sheet by R/py/22_params_v7.py, which also sets the ranges he
# left blank (docs/model_spec.md section 6); R/py/23_params_v8.py then applies the range rules for
# drug costs at list price (薬価固定) and for rates of 0 events, and R/py/24_params_v9.py the Poisson ranges of
# B33P and B33C and Ozaki's lower bound of F05. Here the returned sheets in input/params/ozaki/ (file
# names with "_v1" or "_v2", at most one of each) are checked against the internal sheet, so that no
# row he filled is dropped silently: a row counts as filled where it differs from the sheet as
# delivered; it is matched by param_id, or by oz_map for the rows he appended whose param_id is not in
# the internal sheet; X01 is checked against E06 - E07 and not entered. The script stops on any other
# param_id, and on a 基本値, 下限, 上限 or 出典 that differs from the internal sheet (a bound he left
# blank must carry the note of R/py/22_params_v7.py instead; on a 薬価固定 row a side he gave must be his,
# a side he left blank the rule's: 0.75 x 基本値 for 下限, 基本値 for 上限). Rows owned by 原 come from the internal
# sheet; an entry of Ozaki's on them is listed, not used.
# Probability distributions are set here, not in the sheet: costs and durations gamma,
# proportions and utilities beta, hazard ratios lognormal; parameters from 下限 and 上限 taken
# as a 95% interval (counts per patient, unit 件/人, gamma as well: B33P, B33C, v9). Rows under 薬価固定 or
# 0例：PSAは固定 are fixed at 基本値 (dist "fixed"; 下限 and
# 上限 are the one-way range only). Rows without both bounds get no distribution yet.
# v10 (R/py/25_params_v10.py, 2026-10-26) adds the column シナリオ値 and the sheets シナリオ and 計算根拠_原 (scenario
# values of docs/analysis_plan_phase2.md section 9, read by R/22_phase2b_main.R plan9); the column is not used here.
# Output: data/params_dist.csv (range_rule: the rule by which we set the range, docs/model_spec.md
# section 6; blank where the range is the owner's)

root <- Sys.getenv("EXERCISE_CEA_ROOT", "C:/Users/原明美/Documents/ClaudeCode/exercise_cea")
suppressPackageStartupMessages(library(readxl))
src <- file.path(root, "input", "params", "parameters_v10.xlsx")
need <- c("param_id", "区分", "項目", "適用する群", "適用する状態", "単位", "基本値", "下限", "上限",
          "価格の年度", "出典", "出典の該当箇所", "担当", "備考")
fill_cols <- c("基本値", "下限", "上限", "価格の年度", "出典", "出典の該当箇所", "備考")
read_sheet <- function(path, extra = character(0)) {   # extra: columns after 備考 (the internal sheet v10: シナリオ値)
  s <- as.data.frame(read_excel(path, sheet = "パラメータ", col_types = "text"), stringsAsFactors = FALSE)
  stopifnot(identical(names(s), c(need, extra)), !anyDuplicated(s$param_id))
  s
}
x <- read_sheet(src, extra = "シナリオ値")
blank <- function(v) is.na(v) | trimws(v) == ""
num <- function(v) suppressWarnings(as.numeric(gsub(",", "", trimws(v))))
same_num <- function(a, b) abs(a - b) <= 1e-9 * pmax(1, abs(b))
RANGE_NOTE <- c("薬価固定" = "幅の規則：薬価固定", "0例：PSAは固定" = "幅の規則：0例：PSAは固定",
                "±25%" = "幅は原が設定（基本値 ±25%）", "片側対称" = "片側を対称に補った")   # first match wins
FIXED_RULES <- c("薬価固定", "0例：PSAは固定")                                             # fixed in the PSA
rule_of <- function(note) {
  r <- rep("", length(note))
  for (k in rev(names(RANGE_NOTE))) r[grepl(RANGE_NOTE[[k]], note, fixed = TRUE)] <- k
  r
}

# Ozaki's returned v1 / v2
oz_dir <- file.path(root, "input", "params", "ozaki")
oz_file <- function(ver) {
  f <- list.files(oz_dir, pattern = paste0("_", ver, "[_.].*\\.xlsx$"), full.names = TRUE)
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
oz_map <- c(X02 = "E08")     # appended 2026-10-25: cost per musculoskeletal adverse event
oz_check_only <- "X01"       # appended 2026-10-25: increment of the musculoskeletal rate; the model uses E06 and E07
x$記入元 <- ifelse(x$担当 == "尾崎", "", "内部表")
oz_not_owned <- oz_mapped <- oz_checked <- oz_by_rule <- character(0)
for (ver in names(oz)) {
  if (is.null(oz[[ver]])) next
  for (id in oz[[ver]]$param_id) {
    r <- filled_in(ver, id)
    if (is.null(r)) next
    if (id %in% oz_check_only) {
      e67 <- num(x$基本値[x$param_id == "E06"]) - num(x$基本値[x$param_id == "E07"])
      if (!isTRUE(round(e67, 2) == num(r$基本値))) stop(id, " (", r$基本値, ") does not agree with E06 - E07 = ", e67)
      oz_checked <- c(oz_checked, sprintf("%s %s = E06 − E07（%s − %s = %.5f、小数 2 桁で一致）。モデルの行は設けない", id, r$基本値,
                                          x$基本値[x$param_id == "E06"], x$基本値[x$param_id == "E07"], e67))
      next
    }
    tg <- if (id %in% x$param_id) id else if (id %in% names(oz_map)) oz_map[[id]] else
      stop("Ozaki's ", ver, " has row ", id, ", which is not in the internal sheet and has no mapping in oz_map")
    if (x$担当[x$param_id == tg] != "尾崎") { oz_not_owned <- c(oz_not_owned, id); next }
    i <- which(x$param_id == tg)
    bad <- character(0)
    if (!isTRUE(same_num(num(r$基本値), num(x$基本値[i])))) bad <- c(bad, "基本値")
    if (rule_of(x$備考[i]) == "薬価固定") {      # a side he gave is his, a side he left blank the rule's (v9)
      rule <- c(下限 = 0.75, 上限 = 1) * num(x$基本値[i])
      for (k in c("下限", "上限")) {
        want <- if (blank(r[[k]])) rule[[k]] else num(r[[k]])
        if (!isTRUE(same_num(num(x[[k]][i]), want))) bad <- c(bad, k)
        if (blank(r[[k]])) oz_by_rule <- c(oz_by_rule, sprintf("%s の%s（薬価固定：空欄 → %s）", id, k, x[[k]][i]))
      }
    } else for (k in c("下限", "上限")) {
      if (blank(r[[k]])) { if (blank(x[[k]][i]) || rule_of(x$備考[i]) == "") bad <- c(bad, k) }
      else if (!isTRUE(same_num(num(r[[k]]), num(x[[k]][i])))) bad <- c(bad, k)
    }
    if (norm(r$出典) != norm(x$出典[i])) bad <- c(bad, "出典")
    if (length(bad)) stop("internal sheet differs from Ozaki's ", ver, " on ", id, if (tg != id) paste0(" (", tg, ")"), ": ", paste(bad, collapse = ", "))
    x$記入元[i] <- paste0(if (x$記入元[i] == "") "" else paste0(x$記入元[i], "、"), "尾崎 ", ver, if (tg != id) paste0("（", id, "）"))
    if (tg != id) oz_mapped <- c(oz_mapped, sprintf("%s → %s", id, tg))
  }
}

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
range_rule <- rule_of(x$備考)
provisional <- grepl("【要確認", x$備考, fixed = TRUE)

# distributions
dist_of <- function(unit) ifelse(grepl("ハザード比", unit), "lognormal",
                          ifelse(grepl("^割合|^効用値", unit), "beta",
                          ifelse(grepl("^円|^月|^件", unit), "gamma", NA)))
z <- qnorm(0.975)
D <- data.frame(param_id = x$param_id, 単位 = x$単位, dist = dist_of(x$単位), base = b, lower = lo, upper = hi,
                p1 = NA_real_, p2 = NA_real_, note = "", range_rule = range_rule, stringsAsFactors = FALSE)
for (i in seq_len(nrow(D))) {
  if (is.na(D$base[i])) { D$note[i] <- "基本値未記入"; next }
  if (D$range_rule[i] %in% FIXED_RULES) { D$dist[i] <- "fixed"; D$note[i] <- "PSAは基本値に固定（下限と上限は一元感度分析の幅）"; next }
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

# notes on single rows
note_of <- setNames(rep("", nrow(x)), x$param_id)
note_of[provisional] <- "暫定値（尾崎先生の備考に【要確認】）"
confirmed <- c(F01 = "v1 の項目名は旧定義だが、値は gBRCA 陰性の non-pCR 例での割合（新定義）。根拠：尾崎 2026-10-25 メール",
               F01P = "定義は内部表のとおり gBRCA 陰性の non-pCR 例での割合。根拠：尾崎 2026-10-25 メール第 2 点（値は暫定、第 5 節）")
no_dist <- is.na(D$p1) & !(D$dist %in% "fixed") & !unfilled      # neither distribution parameters nor fixed

# check report
lst <- function(idx, notes = note_of) if (!any(idx)) "- なし" else
  sprintf("- %s %s（%s）%s", x$param_id[idx], x$項目[idx], x$担当[idx],
          ifelse(notes[x$param_id[idx]] == "", "", paste0("：", notes[x$param_id[idx]])))
ids_or_none <- function(v) if (length(v)) paste(v, collapse = "、") else "なし"
oz_line <- function(ver) if (is.na(oz_files[[ver]])) sprintf("- %s：未着（`input/params/ozaki/` に該当ファイルなし）", ver) else
  sprintf("- %s：`%s`（記入のある行のうち内部表と照合した尾崎の行 %d）", ver, basename(oz_files[[ver]]), sum(grepl(paste("尾崎", ver), x$記入元)))
L <- c("# パラメータ入力表の確認",
       "",
       sprintf("対象：`input/params/parameters_v10.xlsx`（%d 行）。`R/10_read_params.R` が生成。", nrow(x)),
       "",
       "## 0. 尾崎先生の返送分（値は `R/py/22_params_v7.py` が内部表に写し、`R/py/23_params_v8.py` と `R/py/24_params_v9.py` が幅の規則を当てた。ここでは返送表の記入のある行を内部表と照合する）", "",
       oz_line("v1"), oz_line("v2"),
       "- 内部表と異なる値：なし（基本値、下限、上限、出典を照合。異なればここで停止する。返送表で空欄の下限と上限は、内部表の備考に原が設定した旨があることを確認）",
       sprintf("- 薬価固定の規則で補った側（尾崎先生が空欄にした側だけ。示された側はそのまま）：%s", ids_or_none(oz_by_rule)),
       sprintf("- 対応づけた追加行：%s", ids_or_none(oz_mapped)),
       sprintf("- 照合だけで内部表に入れない追加行：%s", ids_or_none(oz_checked)),
       sprintf("- 担当が尾崎でない行への記入（採用しない）：%s", ids_or_none(oz_not_owned)),
       "- 内部表になく対応も決めていない param_id：なし（あればここで停止する）",
       "",
       "## 1. 基本値が未記入の行（担当別）", "")
for (ow in c("尾崎", "原")) {
  idx <- unfilled & x$担当 == ow
  L <- c(L, sprintf("### %s（%d / %d 行）", ow, sum(idx), sum(x$担当 == ow)), "", lst(idx), "")
}
noted <- note_of != "" & !unfilled
rule_notes <- setNames(c("±25%" = "基本値 ±25%", "片側対称" = "片側を対称に補った", "薬価固定" = "PSA は基本値に固定、一元感度分析は基本値の 75% まで下方だけ",
                         "0例：PSAは固定" = "PSA は 0 に固定、一元感度分析の上限は 0 例の Clopper-Pearson 95% 上限")[range_rule], x$param_id)
rule_sec <- function(rules, title) {
  idx <- range_rule %in% rules
  c(sprintf("### %s（%d 行）", title, sum(idx)), "", lst(idx, rule_notes), "")
}
L <- c(L, "## 2. 基本値が数値でない行", "", lst(nonnum), "",
       "## 3. 値はあるが出典がない行", "", lst(nosrc), "",
       "## 4. 下限 > 基本値 または 基本値 > 上限 の行", "", lst(badrng), "",
       "## 5. 記入済みで確認が必要な行（暫定値として使う）", "", lst(noted), "",
       "## 6. 確認済みの行", "", lst(x$param_id %in% names(confirmed), setNames(confirmed[x$param_id], x$param_id)), "",
       sprintf("## 7. 幅の規則を当てた行（%d 行、`data/params_dist.csv` の range_rule。`docs/model_spec.md` 第 6 節）", sum(range_rule != "")), "",
       rule_sec(c("±25%", "片側対称"), "幅を原が設定した行（一元感度分析の図表で「範囲は仮定値」と注記する）"),
       rule_sec("薬価固定", "薬価固定（薬価と規定用量で計算した薬剤費）"),
       rule_sec("0例：PSAは固定", "0例：PSAは固定（基本値が 0 の発現率）"),
       "## 8. 確率分布の確認（モデルに入る全行）", "",
       sprintf("- 分布のパラメータが決まった行：%d", sum(!is.na(D$p1))),
       sprintf("- PSA で固定する行（dist = fixed）：%d（%s）", sum(D$dist %in% "fixed"), ids_or_none(D$param_id[D$dist %in% "fixed"])),
       sprintf("- 分布のパラメータも固定の指定もない行：%d", sum(no_dist)), "",
       lst(no_dist, setNames(D$note, x$param_id)), "",
       "## 参考：下限または上限が数値でない行", "", lst(nonnum_bounds), "",
       "## 参考：確率分布（コードで設定）", "",
       "費用と期間はガンマ分布、割合と効用値はベータ分布、ハザード比は対数正規分布、1 人あたりの件数（件/人：B33P、B33C）はガンマ分布。下限と上限を95%区間とみなしてパラメータを求める（`data/params_dist.csv`）。",
       "薬価固定と 0例：PSAは固定の行は PSA で基本値に固定し（dist = fixed）、下限と上限は一元感度分析だけに使う。")
writeLines(L, file.path(root, "output", "params_check.md"), useBytes = TRUE)
cat(sprintf("rows %d; unfilled 尾崎 %d/%d, 原 %d/%d; non-numeric %d; no source %d; bad range %d; Ozaki v1 %s, v2 %s; checked %d; ranges by rule %d; fixed %d; no distribution %d (%s)\n", nrow(x),
            sum(unfilled & x$担当 == "尾崎"), sum(x$担当 == "尾崎"), sum(unfilled & x$担当 == "原"), sum(x$担当 == "原"),
            sum(nonnum), sum(nosrc), sum(badrng), basename(oz_files[["v1"]]), basename(oz_files[["v2"]]),
            sum(grepl("尾崎 v", x$記入元)), sum(range_rule != ""), sum(D$dist %in% "fixed"), sum(no_dist), paste(D$param_id[no_dist], collapse = ", ")))
