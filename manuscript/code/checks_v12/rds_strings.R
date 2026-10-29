# rds_strings.R: every character string inside an rds file (values, names, attributes, recursively, also inside
# environments and functions as deparsed text), one per line, for the name check of the public directory.
# usage: Rscript rds_strings.R <file.rds> <out.txt>
a <- commandArgs(trailingOnly = TRUE)
x <- readRDS(a[1])
acc <- character(0)
seen <- new.env()
walk <- function(o, depth = 0) {
  if (depth > 60) return(invisible())
  at <- attributes(o)
  if (!is.null(at)) { acc <<- c(acc, names(at)); for (v in at) walk(v, depth + 1) }
  if (is.character(o)) acc <<- c(acc, o[!is.na(o)])
  else if (is.list(o)) for (v in o) walk(v, depth + 1)
  else if (is.environment(o)) {
    k <- format(o); if (!is.null(seen[[k]])) return(invisible()); assign(k, TRUE, envir = seen)
    for (n in ls(o, all.names = TRUE)) { acc <<- c(acc, n); walk(get(n, envir = o), depth + 1) }
  } else if (is.function(o) || is.language(o)) acc <<- c(acc, deparse(o))
}
walk(x)
writeLines(enc2utf8(acc), a[2], useBytes = TRUE)
cat(length(acc), "strings\n")
