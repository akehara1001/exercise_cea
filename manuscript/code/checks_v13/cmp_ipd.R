# Instruction v13 step 3: data/ipd written by a rerun of R/03_reconstruct_ipd.R (in a copy of the public directory)
# against data/ipd of the public directory, by value (csv by read.csv; rds by identical()) and byte for byte.
# usage: Rscript cmp_ipd.R <rerun copy root> <public root>
a <- commandArgs(TRUE)
new <- file.path(a[1], "data", "ipd"); old <- file.path(a[2], "data", "ipd")
fn <- sort(list.files(old, recursive = TRUE)); fnew <- sort(list.files(new, recursive = TRUE))
cat("files in public data/ipd:", length(fn), "; in the rerun copy:", length(fnew), "; same names:", identical(fn, fnew), "\n")
written <- c(sprintf("%s.csv", c(
  paste0("K20_F2_EFS_", c("pembro", "placebo")), paste0("K22_F1_EFS_", c("pembro", "placebo")),
  paste0("K22_F3_OS_", c("pembro", "placebo")), paste0("K24_F1A_OS_", c("pembro", "placebo")),
  paste0("K24_F2A_EFS_", c("pembro", "placebo")), paste0("Y22_F4A_EFS_TNBC_RCB", 0:3),
  paste0("K22_S3_DRFS_", c("pembro", "placebo")),
  paste0("K22_S4_EFS_pCR_", c("pembro_pCR", "placebo_pCR", "pembro_nonpCR", "placebo_nonpCR")),
  paste0("K24_S4_OS_pCR_", c("pembro_pCR", "placebo_pCR", "pembro_nonpCR", "placebo_nonpCR")))), "ipd_all.rds")
cat("written by 03_reconstruct_ipd.R:", length(written), "; all present:", all(written %in% fn),
    "; other files (not written by it):", paste(setdiff(fn, written), collapse = ", "), "\n")
res <- t(sapply(fn, function(f) {
  p1 <- file.path(new, f); p0 <- file.path(old, f)
  v <- if (grepl("[.]csv$", f)) identical(read.csv(p1), read.csv(p0)) else identical(readRDS(p1), readRDS(p0))
  b <- identical(unname(tools::md5sum(p1)), unname(tools::md5sum(p0)))
  c(value = v, bytes = b)
}))
w <- res[written, , drop = FALSE]
cat("written files equal by value:", sum(w[, "value"]), "of", nrow(w), "; byte for byte:", sum(w[, "bytes"]), "of", nrow(w), "\n")
cat("differing by value:", if (any(!res[, "value"])) paste(rownames(res)[!res[, "value"]], collapse = ", ") else "none", "\n")
x <- readRDS(file.path(new, "ipd_all.rds")); y <- readRDS(file.path(old, "ipd_all.rds"))
cat("ipd_all.rds: elements", length(x), "; rows", sum(sapply(x, nrow)), "; identical by value:", identical(x, y), "\n")
