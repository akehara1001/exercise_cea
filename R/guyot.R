# guyot.R
# Guyot et al. (BMC Med Res Methodol 2012;12:9) IPD reconstruction, following the
# published R code. Inputs are the digitized KM coordinates (t.S, S on 0-1 scale) and
# the risk table (t.risk, n.risk). tot.events is optional and left NULL here so that the
# reconstructed event count can be checked against the reported one.

# Make Guyot input from a step-vertex list: monotone, t >= 0, plus one point at every
# risk-table time (value of the step function there) so that no interval is empty.
guyot_prepare <- function(time, surv, t.risk, n.risk) {
  o <- order(time, -surv)
  time <- pmax(time[o], 0); surv <- pmin(cummin(surv[o]), 1)
  time[1] <- 0; surv[1] <- 1
  keep_rt <- t.risk <= max(time)
  t.risk <- t.risk[keep_rt]; n.risk <- n.risk[keep_rt]
  step_at <- function(t) min(surv[time <= t + 1e-9])
  add <- data.frame(time = t.risk, surv = vapply(t.risk, step_at, 0))
  d <- rbind(data.frame(time = time, surv = surv), add)
  d <- d[order(d$time, -d$surv), ]
  d <- d[!duplicated(d[, c("time", "surv")]), ]
  d$surv <- cummin(d$surv)
  lower <- vapply(t.risk, function(t) min(which(d$time >= t - 1e-9)), 0L)
  upper <- c(lower[-1] - 1L, nrow(d))
  stopifnot(all(upper >= lower))
  list(t.S = d$time, S = d$surv, t.risk = t.risk, n.risk = n.risk, lower = lower, upper = upper)
}

guyot <- function(prep, tot.events = NULL) {
  t.S <- prep$t.S; S <- prep$S; t.risk <- prep$t.risk; n.risk <- prep$n.risk
  lower <- prep$lower; upper <- prep$upper
  n.int <- length(n.risk); n.t <- upper[n.int]
  n.censor <- rep(0, n.int)
  n.hat <- rep(n.risk[1] + 1, n.t + 1)
  cen <- rep(0, n.t); d <- rep(0, n.t); KM.hat <- rep(1, n.t)
  last.i <- rep(1, n.int); sumdL <- 0
  # hist(x, breaks = br)$counts, but zero-width bins (vertical drops give tied times) are allowed
  hist_counts <- function(x, br) {
    nb <- length(br) - 1
    if (nb < 1) return(numeric(0))
    vapply(seq_len(nb), function(j) {
      lo <- br[j]; hi <- br[j + 1]
      if (hi <= lo) return(0)
      sum(if (j == 1) x >= lo & x <= hi else x > lo & x <= hi)
    }, 0)
  }
  if (n.int > 1) {
    for (i in 1:(n.int - 1)) {
      n.censor[i] <- round(n.risk[i] * S[lower[i + 1]] / S[lower[i]] - n.risk[i + 1])
      iter <- 0
      while ((n.hat[lower[i + 1]] > n.risk[i + 1]) ||
             ((n.hat[lower[i + 1]] < n.risk[i + 1]) && (n.censor[i] > 0))) {
        iter <- iter + 1
        if (iter > 1000) stop("Guyot: no convergence in interval ", i)
        if (n.censor[i] <= 0) { cen[lower[i]:upper[i]] <- 0; n.censor[i] <- 0 }
        if (n.censor[i] > 0) {
          cen.t <- t.S[lower[i]] + (1:n.censor[i]) * (t.S[lower[i + 1]] - t.S[lower[i]]) / (n.censor[i] + 1)
          cen[lower[i]:upper[i]] <- hist_counts(cen.t, t.S[lower[i]:lower[i + 1]])
        }
        n.hat[lower[i]] <- n.risk[i]
        last <- last.i[i]
        for (k in lower[i]:upper[i]) {
          if (i == 1 && k == lower[i]) {
            d[k] <- 0; KM.hat[k] <- 1
          } else {
            d[k] <- round(n.hat[k] * (1 - (S[k] / KM.hat[last])))
            KM.hat[k] <- KM.hat[last] * (1 - (d[k] / n.hat[k]))
          }
          n.hat[k + 1] <- n.hat[k] - d[k] - cen[k]
          if (d[k] != 0) last <- k
        }
        n.censor[i] <- n.censor[i] + (n.hat[lower[i + 1]] - n.risk[i + 1])
      }
      if (n.hat[lower[i + 1]] < n.risk[i + 1]) n.risk[i + 1] <- n.hat[lower[i + 1]]
      last.i[i + 1] <- last
    }
  }
  last_interval <- function(n.cens.last) {
    if (n.cens.last <= 0) {
      if (upper[n.int] > lower[n.int]) cen[lower[n.int]:(upper[n.int] - 1)] <<- 0
      n.cens.last <- 0
    } else {
      cen.t <- t.S[lower[n.int]] + (1:n.cens.last) * (t.S[upper[n.int]] - t.S[lower[n.int]]) / (n.cens.last + 1)
      if (upper[n.int] > lower[n.int])
        cen[lower[n.int]:(upper[n.int] - 1)] <<- hist_counts(cen.t, t.S[lower[n.int]:upper[n.int]])
    }
    n.hat[lower[n.int]] <<- n.risk[n.int]
    last <- last.i[n.int]
    for (k in lower[n.int]:upper[n.int]) {
      d[k] <<- if (KM.hat[last] != 0) round(n.hat[k] * (1 - (S[k] / KM.hat[last]))) else 0
      KM.hat[k] <<- KM.hat[last] * (1 - (d[k] / n.hat[k]))
      n.hat[k + 1] <<- n.hat[k] - d[k] - cen[k]
      if (n.hat[k + 1] < 0) { n.hat[k + 1] <<- 0; cen[k] <<- n.hat[k] - d[k] }
      if (d[k] != 0) last <- k
    }
    n.cens.last
  }
  if (n.int > 1) {
    n.censor[n.int] <- min(round(sum(n.censor[1:(n.int - 1)]) * (t.S[upper[n.int]] - t.S[lower[n.int]]) /
                                   (t.S[upper[n.int - 1]] - t.S[lower[1]])), n.risk[n.int])
  }
  n.censor[n.int] <- last_interval(n.censor[n.int])
  if (!is.null(tot.events)) {
    if (n.int > 1) sumdL <- sum(d[1:upper[n.int - 1]])
    sumd <- sum(d[1:upper[n.int]])
    iter <- 0
    while ((sumd > tot.events) || ((sumd < tot.events) && (n.censor[n.int] > 0))) {
      iter <- iter + 1
      if (iter > 1000) stop("Guyot: no convergence matching tot.events")
      n.censor[n.int] <- n.censor[n.int] + (sumd - tot.events)
      n.censor[n.int] <- last_interval(n.censor[n.int])
      sumd <- sum(d[1:upper[n.int]])
    }
  }
  # IPD: events at the digitized times, censorings at interval midpoints, the rest at the end
  N <- prep$n.risk[1]
  t.IPD <- rep(t.S[n.t], N); ev <- rep(0L, N); k <- 1
  for (j in 1:n.t) if (d[j] != 0) {
    t.IPD[k:(k + d[j] - 1)] <- t.S[j]; ev[k:(k + d[j] - 1)] <- 1L; k <- k + d[j]
  }
  for (j in seq_len(n.t - 1)) if (cen[j] != 0) {
    t.IPD[k:(k + cen[j] - 1)] <- (t.S[j] + t.S[j + 1]) / 2; ev[k:(k + cen[j] - 1)] <- 0L; k <- k + cen[j]
  }
  stopifnot(k - 1 <= N)
  data.frame(time = t.IPD, status = ev)
}
