# 07_engine_outputs.R
# Step 7: survival engine outputs with the parameters adopted in step 5 (data/fits/engine_params.rds)
# and bootstrap 95% percentile intervals (step 6, data/bootstrap/boot_replicates.rds).
#   - 5-, 10- and 20-year EFS and OS from randomization by arm x pCR (all, pCR, non-pCR); in
#     phase 1 the exercise arms equal their non-exercise arms (no exercise parameters yet);
#   - the scenario k = 1 (common post-DR mortality) for the pembrolizumab arms (OS only; EFS is
#     unchanged by it);
#   - curves to 20 years with bootstrap bands, against the reconstructed KM curves.
# Each replicate's engine is rebuilt from the saved parameter matrices; its 5/10/20-year values must
# equal those stored by 06_bootstrap.R (check of the saved matrices).
# Outputs: output/phase1/engine_outputs.csv, engine_curves.csv, bootstrap_rebuild_check.csv,
#          fig_engine_outputs.png

source("C:/Users/原明美/Documents/ClaudeCode/exercise_cea/R/config.R")
source(file.path(ROOT, "R", "survmodels.R"))
source(file.path(ROOT, "R", "engine.R"))
suppressPackageStartupMessages({
  library(survival)
  library(parallel)
  library(ggplot2)
})
out_dir <- file.path(ROOT, "output", "phase1")
P <- readRDS(file.path(ROOT, "data", "fits", "engine_params.rds"))
BR <- readRDS(file.path(ROOT, "data", "bootstrap", "boot_replicates.rds"))
fits <- readRDS(file.path(ROOT, "data", "fits", "fits.rds"))
ipd <- readRDS(file.path(ROOT, "data", "ipd", "ipd_all.rds"))
Lm <- CFG$landmark_months

# parameter set of replicate i, rebuilt from the saved matrices
rebuild <- function(i) {
  Pb <- P
  e <- BR$efs[i, ]; pc <- BR$pcr_preprog[i, ]; ps <- BR$pre_surv[i, ]; cb <- BR$calibration[i, ]
  for (a in c("pembro", "placebo")) {
    for (s in c("pCR", "nonpCR")) {
      cv <- paste0("EFS_", a, "_", s)
      sp <- fits$selected[[cv]]
      sp$pars <- setNames(e[paste0(cv, "_", names(sp$pars))], names(sp$pars))
      Pb$efs[[a]][[s]] <- sp
      Pb$pre_surv[[a]][[s]] <- data.frame(time = (0:Lm) / 12, surv = unname(ps[paste0("pre_surv_", a, "_", s, "_m", 0:Lm)]))
    }
    Pb$p_pcr[[a]] <- unname(pc[paste0("p_pcr_", a)])
    Pb$q_pre[[a]] <- c(pCR = 0, nonpCR = unname(pc[paste0("q_pre_", a)]))
  }
  Pb$preprog <- list(dist = "llogis", shape = unname(cb["preprog_shape"]), scale = unname(cb["preprog_median"]))
  Pb$dr <- list(dist = "llogis", shape = unname(cb["dr_shape"]), scale = unname(cb["dr_median"]))
  Pb$pembro_dr_k <- unname(cb["pembro_dr_k"])
  Pb
}

grid_y <- seq(0, 20, by = 1 / 12)
curves_of <- function(Pb) {
  out <- list()
  for (arm in c("chemo", "pembro")) for (pc in c("all", "pCR", "nonpCR")) {
    r <- survival_engine(arm, pc, times = grid_y, params = Pb)
    out[[length(out) + 1]] <- data.frame(arm = arm, pcr = pc, scenario = "base", time = grid_y, EFS = 100 * r$EFS, OS = 100 * r$OS)
    if (arm == "pembro") {
      r <- survival_engine(arm, pc, times = grid_y, params = Pb, common_dr = TRUE)
      out[[length(out) + 1]] <- data.frame(arm = arm, pcr = pc, scenario = "k = 1", time = grid_y, EFS = 100 * r$EFS, OS = 100 * r$OS)
    }
  }
  do.call(rbind, out)
}

base_curves <- curves_of(P)
cl <- makeCluster(min(11, detectCores() - 1))
clusterExport(cl, c("ROOT"))
invisible(clusterEvalQ(cl, {
  source(file.path(ROOT, "R", "config.R")); source(file.path(ROOT, "R", "survmodels.R")); source(file.path(ROOT, "R", "engine.R"))
  suppressPackageStartupMessages(library(survival)); NULL
}))
clusterExport(cl, c("P", "BR", "fits", "Lm", "rebuild", "grid_y", "curves_of"))
BC <- parLapply(cl, seq_len(nrow(BR$calibration)), function(i) { x <- curves_of(rebuild(i)); x$rep <- i; x })
stopCluster(cl)
BC <- do.call(rbind, BC)

# check: rebuilt replicates reproduce the stored 5/10/20-year outputs
chk <- do.call(rbind, lapply(seq_len(nrow(BR$outputs)), function(i) {
  o <- BR$outputs[i, ]; x <- BC[BC$rep == i & round(BC$time, 9) %in% c(5, 10, 20), ]
  d <- c()
  for (j in seq_len(nrow(x))) {
    if (x$scenario[j] == "base") {
      d <- c(d, x$EFS[j] - o[[sprintf("EFS_%gy_%s_%s", x$time[j], x$arm[j], x$pcr[j])]], x$OS[j] - o[[sprintf("OS_%gy_%s_%s", x$time[j], x$arm[j], x$pcr[j])]])
    } else d <- c(d, x$OS[j] - o[[sprintf("OS_%gy_pembro_k1_%s", x$time[j], x$pcr[j])]])
  }
  data.frame(rep = BR$outputs[i, "b"], max_abs_diff = max(abs(d)))
}))
write.csv(data.frame(replicates = nrow(chk), max_abs_diff = max(chk$max_abs_diff)), file.path(out_dir, "bootstrap_rebuild_check.csv"), row.names = FALSE)
cat(sprintf("rebuild check: %d replicates, max abs difference %.2e\n", nrow(chk), max(chk$max_abs_diff)))
stopifnot(max(chk$max_abs_diff) < 1e-8)

# bands and the 5/10/20-year table
band <- aggregate(cbind(EFS, OS) ~ arm + pcr + scenario + time, data = BC, FUN = function(v) quantile(v, c(0.025, 0.5, 0.975)))
band <- data.frame(band[, 1:4], EFS_lo = band$EFS[, 1], EFS_med = band$EFS[, 2], EFS_hi = band$EFS[, 3],
                   OS_lo = band$OS[, 1], OS_med = band$OS[, 2], OS_hi = band$OS[, 3])
n_rep <- aggregate(rep ~ arm + pcr + scenario, data = unique(BC[, c("arm", "pcr", "scenario", "rep")]), FUN = length)
CU <- merge(base_curves, band, by = c("arm", "pcr", "scenario", "time"))
CU <- CU[order(CU$scenario, CU$arm, CU$pcr, CU$time), ]
write.csv(CU, file.path(out_dir, "engine_curves.csv"), row.names = FALSE)
arm_lab <- c(chemo = "chemo (= chemo + exercise in phase 1)", pembro = "pembro (= pembro + exercise in phase 1)")
TB <- do.call(rbind, lapply(c("EFS", "OS"), function(ep) {
  x <- CU[round(CU$time, 9) %in% c(5, 10, 20), ]
  if (ep == "EFS") x <- x[x$scenario == "base", ]
  data.frame(endpoint = ep, scenario = x$scenario, arm = x$arm, pcr = x$pcr, year = x$time, base = x[[ep]],
             boot_lo = x[[paste0(ep, "_lo")]], boot_median = x[[paste0(ep, "_med")]], boot_hi = x[[paste0(ep, "_hi")]])
}))
TB <- merge(TB, setNames(n_rep, c("arm", "pcr", "scenario", "n_replicates")), by = c("arm", "pcr", "scenario"))
TB <- TB[order(TB$endpoint, TB$scenario, TB$arm, TB$pcr, TB$year), c("endpoint", "scenario", "arm", "pcr", "year", "base", "boot_lo", "boot_median", "boot_hi", "n_replicates")]
write.csv(TB, file.path(out_dir, "engine_outputs.csv"), row.names = FALSE)
print(TB, row.names = FALSE)

# figure: engine (base) with bootstrap bands vs reconstructed KM
km_df <- function(d, arm, pcr, ep) { f <- survfit(Surv(time / 12, status) ~ 1, data = d)
  data.frame(arm = arm, pcr = pcr, endpoint = ep, time = c(0, f$time), surv = 100 * c(1, f$surv)) }
KM <- do.call(rbind, lapply(c(pembro = "pembro", chemo = "placebo"), function(a) {
  arm <- if (a == "pembro") "pembro" else "chemo"
  rbind(km_df(ipd[[paste0("K24_F2A_EFS_", a)]], arm, "all", "EFS"), km_df(ipd[[paste0("K24_F1A_OS_", a)]], arm, "all", "OS"),
        km_df(ipd[[paste0("K22_S4_EFS_pCR_", a, "_pCR")]], arm, "pCR", "EFS"), km_df(ipd[[paste0("K22_S4_EFS_pCR_", a, "_nonpCR")]], arm, "nonpCR", "EFS"),
        km_df(ipd[[paste0("K24_S4_OS_pCR_", a, "_pCR")]], arm, "pCR", "OS"), km_df(ipd[[paste0("K24_S4_OS_pCR_", a, "_nonpCR")]], arm, "nonpCR", "OS"))
}))
bb <- CU[CU$scenario == "base", ]
pl <- rbind(data.frame(bb[, c("arm", "pcr", "time")], endpoint = "EFS", v = bb$EFS, lo = bb$EFS_lo, hi = bb$EFS_hi),
            data.frame(bb[, c("arm", "pcr", "time")], endpoint = "OS", v = bb$OS, lo = bb$OS_lo, hi = bb$OS_hi))
pl$pcr <- factor(pl$pcr, c("all", "pCR", "nonpCR")); KM$pcr <- factor(KM$pcr, c("all", "pCR", "nonpCR"))
cols <- c(chemo = "#2E86C1", pembro = "#C0392B")
g <- ggplot() +
  geom_ribbon(data = pl, aes(time, ymin = lo, ymax = hi, fill = arm), alpha = 0.2) +
  geom_line(data = pl, aes(time, v, colour = arm), linewidth = 0.7) +
  geom_step(data = KM, aes(time, surv, colour = arm), linewidth = 0.35, linetype = "22") +
  facet_grid(endpoint ~ pcr) + scale_colour_manual(values = cols) + scale_fill_manual(values = cols) +
  labs(x = "Years from randomization", y = "%", colour = NULL, fill = NULL,
       title = "Survival engine (solid; band: bootstrap 95% interval) and reconstructed KM (dashed)") +
  coord_cartesian(ylim = c(30, 100)) + theme_bw(base_size = 9) + theme(legend.position = "bottom")
ggsave(file.path(out_dir, "fig_engine_outputs.png"), g, width = 9, height = 6, dpi = 200)
cat("done\n")
