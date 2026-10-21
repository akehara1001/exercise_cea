# lifetable.R
# Background mortality: Japanese female abridged life table 2025 (data/lifetable_female_2025.csv),
# hazard constant within each year of age (mu = -log(1 - qx); mx above 105).

LT <- read.csv(file.path(ROOT, "data", "lifetable_female_2025.csv"))
.mu <- LT$mu
.cumH <- c(0, cumsum(.mu))          # cumulative hazard at integer ages 0, 1, ..., 106

# hazard at age a (vectorised)
mu_pop <- function(a) .mu[pmin(floor(a), length(.mu) - 1) + 1]

# cumulative hazard from birth to age a
H_age <- function(a) {
  a <- pmin(a, length(.mu) - 1e-9)
  k <- floor(a)
  .cumH[k + 1] + .mu[k + 1] * (a - k)
}

# cumulative background hazard and survival over t years starting at age a0
H_pop <- function(a0, t) H_age(a0 + t) - H_age(a0)
S_pop <- function(a0, t) exp(-H_pop(a0, t))
