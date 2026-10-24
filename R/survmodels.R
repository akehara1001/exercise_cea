# survmodels.R
# A fitted survival model is kept as a plain "spec" (family, distribution, natural-scale
# parameters, spline knots) so that the engine and the bootstrap do not depend on fit objects.
#   family "std"  : all-cause survival from a standard distribution
#   family "rp"   : all-cause survival from a Royston-Parmar spline (flexsurvspline)
#   family "cure" : relative-survival mixture cure model; the spec gives NET survival
#                   theta + (1 - theta) * S_u(t); all-cause = S_pop * net

suppressPackageStartupMessages({
  library(flexsurv)
  library(flexsurvcure)
})

STD_DISTS <- c("exp", "weibull", "lnorm", "llogis", "gompertz", "gengamma")

.base_p <- function(dist, t, p) switch(dist,
  exp = pexp(t, p[["rate"]]),
  weibull = pweibull(t, p[["shape"]], p[["scale"]]),
  lnorm = plnorm(t, p[["meanlog"]], p[["sdlog"]]),
  llogis = flexsurv::pllogis(t, p[["shape"]], p[["scale"]]),
  gompertz = flexsurv::pgompertz(t, p[["shape"]], p[["rate"]]),
  gengamma = flexsurv::pgengamma(t, p[["mu"]], p[["sigma"]], p[["Q"]]))
.base_d <- function(dist, t, p) switch(dist,
  exp = dexp(t, p[["rate"]]),
  weibull = dweibull(t, p[["shape"]], p[["scale"]]),
  lnorm = dlnorm(t, p[["meanlog"]], p[["sdlog"]]),
  llogis = flexsurv::dllogis(t, p[["shape"]], p[["scale"]]),
  gompertz = flexsurv::dgompertz(t, p[["shape"]], p[["rate"]]),
  gengamma = flexsurv::dgengamma(t, p[["mu"]], p[["sigma"]], p[["Q"]]))

# survival of the spec (all-cause for std/rp, net for cure)
spec_surv <- function(spec, t) {
  p <- spec$pars
  switch(spec$family,
    std = 1 - .base_p(spec$dist, t, p),
    rp = flexsurv::psurvspline(t, gamma = p, knots = spec$knots, scale = spec$scale, lower.tail = FALSE),
    cure = p[["theta"]] + (1 - p[["theta"]]) * (1 - .base_p(spec$dist, t, p)))
}

# hazard of the spec (all-cause for std/rp, excess for cure)
spec_haz <- function(spec, t) {
  p <- spec$pars
  switch(spec$family,
    std = .base_d(spec$dist, t, p) / pmax(1 - .base_p(spec$dist, t, p), 1e-300),
    rp = flexsurv::hsurvspline(t, gamma = p, knots = spec$knots, scale = spec$scale),
    cure = (1 - p[["theta"]]) * .base_d(spec$dist, t, p) / pmax(spec_surv(spec, t), 1e-300))
}

# all-cause survival and hazard for a cohort entering at age a0
allcause_surv <- function(spec, t, a0) if (spec$family == "cure") S_pop(a0, t) * spec_surv(spec, t) else spec_surv(spec, t)
allcause_haz <- function(spec, t, a0) if (spec$family == "cure") mu_pop(a0 + t) + spec_haz(spec, t) else spec_haz(spec, t)
# excess over background (may be negative for std/rp models whose hazard falls below the population)
excess_haz <- function(spec, t, a0) allcause_haz(spec, t, a0) - mu_pop(a0 + t)

# all-cause log-likelihood (comparable across families)
allcause_loglik <- function(spec, time, status, a0) {
  sum(status * log(pmax(allcause_haz(spec, time, a0), 1e-300)) + log(pmax(allcause_surv(spec, time, a0), 1e-300)))
}

# 5-year EFS constraint (decision 2026-10-22). For an EFS model landmarked at L (years) with KM
# pre at the landmark, the 5-year EFS from randomization is 100 * pre * S(5 - L). If it lies in
# [lo, hi] the spec is returned unchanged; otherwise the all-cause likelihood is maximised on the
# nearer bound, where one parameter follows from the others (cure Weibull: theta; Weibull: scale).
# at: the time from randomization in years (round 11: 7, the final analysis; the value is still
# returned as efs5).
constrain_efs5 <- function(spec, d, a0, pre, L, lo, hi, at = 5) {
  tau <- at - L
  v <- 100 * pre * allcause_surv(spec, tau, a0)
  if (v >= lo && v <= hi) return(list(spec = spec, binding = FALSE, bound = NA_real_, efs5 = v, converged = TRUE))
  b <- if (v < lo) lo else hi
  s_star <- b / (100 * pre)                                   # all-cause survival at tau on the bound
  make <- switch(paste(spec$family, spec$dist),
    "cure weibull" = function(x) {
      sw <- 1 - pweibull(tau, exp(x[1]), exp(x[2]))
      th <- (s_star / S_pop(a0, tau) - sw) / (1 - sw)
      if (!is.finite(th) || th <= 0 || th >= 1) return(NULL)
      s <- spec; s$pars <- c(theta = th, shape = exp(x[1]), scale = exp(x[2])); s
    },
    "std weibull" = function(x) {
      s <- spec; s$pars <- c(shape = exp(x[1]), scale = tau / (-log(s_star))^(1 / exp(x[1]))); s
    },
    stop("5-year constraint not implemented for ", spec$family, " ", spec$dist))
  nll <- function(x) { s <- make(x); if (is.null(s)) return(1e10); -allcause_loglik(s, d$time, d$status, a0) }
  if (spec$family == "std") {
    o <- optimize(nll, log(spec$pars[["shape"]]) + c(-3, 3))
    x <- o$minimum; ok <- TRUE
  } else {
    x0 <- unname(log(spec$pars[c("shape", "scale")]))
    starts <- c(list(x0), lapply(c(-1, -0.5, 0.5, 1), function(dx) x0 + c(0, dx)))
    best <- NULL
    for (s0 in starts) {
      if (nll(s0) >= 1e10) next
      o <- optim(s0, nll, method = "Nelder-Mead", control = list(maxit = 5000, reltol = 1e-12))
      if (is.null(best) || o$value < best$value) best <- o
    }
    if (is.null(best)) return(list(spec = spec, binding = TRUE, bound = b, efs5 = v, converged = FALSE))
    x <- best$par; ok <- best$convergence == 0
  }
  s <- make(x)
  list(spec = s, binding = TRUE, bound = b, efs5 = 100 * pre * allcause_surv(s, tau, a0), converged = ok)
}

spec_from_fit <- function(fit, family, dist = NULL, k = NULL, scale = NULL) {
  est <- setNames(fit$res[, "est"], rownames(fit$res))   # keeps the name when there is one parameter
  list(family = family, dist = dist, k = k, scale = scale, pars = est,
       knots = if (family == "rp") fit$knots else NULL)
}

CANDIDATES <- c(
  lapply(STD_DISTS, function(d) list(id = d, family = "std", dist = d)),
  unlist(lapply(c("hazard", "odds"), function(sc) lapply(1:3, function(k)
    list(id = sprintf("rp_%s_k%d", sc, k), family = "rp", k = k, scale = sc))), recursive = FALSE),
  lapply(c("weibull", "lnorm", "llogis"), function(d) list(id = paste0("cure_", d), family = "cure", dist = d))
)

# fit one candidate; d has columns time, status, bh (background hazard at the event time)
fit_candidate <- function(cand, d, knots = NULL) {
  f <- switch(cand$family,
    std = flexsurvreg(Surv(time, status) ~ 1, data = d, dist = cand$dist),
    rp = if (is.null(knots)) flexsurvspline(Surv(time, status) ~ 1, data = d, k = cand$k, scale = cand$scale)
         else flexsurvspline(Surv(time, status) ~ 1, data = d, knots = knots[-c(1, length(knots))],
                             bknots = knots[c(1, length(knots))], scale = cand$scale),
    cure = flexsurvcure(Surv(time, status) ~ 1, data = d, dist = cand$dist, mixture = TRUE, bhazard = bh))
  list(fit = f, spec = spec_from_fit(f, cand$family, cand$dist, cand$k, cand$scale))
}
