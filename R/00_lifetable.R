# 00_lifetable.R
# 厚生労働省 令和7(2025)年簡易生命表（女）を年齢各歳の CSV に整える。
# 入力: input/lifetable/life25-12.xlsx（2 枚目のシート = 女）
# 出力: data/lifetable_female_2025.csv
#   age, qx, lx, dx, Lx, Tx, ex, mu (= -log(1 - qx)、年齢区間内一定の背景ハザード)

suppressPackageStartupMessages(library(readxl))

root <- "C:/Users/原明美/Documents/ClaudeCode/exercise_cea"
src <- file.path(root, "input", "lifetable", "life25-12.xlsx")
out <- file.path(root, "data", "lifetable_female_2025.csv")

sheets <- excel_sheets(src)
sh <- sheets[grepl("女", sheets)]
stopifnot(length(sh) == 1)

raw <- read_excel(src, sheet = sh, col_names = FALSE, .name_repair = "minimal")
lab <- as.character(raw[[1]])
yr <- grepl("^[0-9]+年$", lab)          # 年齢各歳の行だけ（週・月の行は除く）
lt <- data.frame(
  age = as.integer(sub("年$", "", lab[yr])),
  qx  = as.numeric(raw[[2]][yr]),
  lx  = as.numeric(raw[[3]][yr]),
  dx  = as.numeric(raw[[4]][yr]),
  Lx  = as.numeric(raw[[5]][yr]),
  Tx  = as.numeric(raw[[6]][yr]),
  ex  = as.numeric(raw[[7]][yr])
)
lt$mu <- ifelse(lt$qx >= 1, NA_real_, -log(1 - lt$qx))
# 105 歳以上（qx = 1）の区間は mx = dx / Lx を一定ハザードとする
lt$mu[lt$qx >= 1] <- lt$dx[lt$qx >= 1] / lt$Lx[lt$qx >= 1]

stopifnot(identical(lt$age, 0:105), lt$lx[1] == 100000, all(!is.na(lt$mu)))
write.csv(lt, out, row.names = FALSE)
cat(sprintf("sheet=%s rows=%d e0=%.2f e50=%.2f -> %s\n",
            sh, nrow(lt), lt$ex[lt$age == 0], lt$ex[lt$age == 50], out))
