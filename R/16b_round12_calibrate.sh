#!/usr/bin/env bash
# 16b_round12_calibrate.sh
# Round 12 (docs/acceptance_rule_round12.md): with the fixed engine, refit (04) and recalibrate (05)
# one EFS constraint setting and keep its outputs apart:
#   output/phase1/round12/<label>/ (calibration outputs, efs constraint table, logs)
#   data/fits/round12/<label>/      (fits.rds, calibration_candidates.rds, engine_params.rds if accepted)
# The main output/phase1 and data/fits files are left as 05 wrote them; the caller restores or adopts.
# Usage: bash R/16b_round12_calibrate.sh <label> <years,type>   e.g. round11_setting 7,equal
set -euo pipefail
ROOT="${EXERCISE_CEA_ROOT:-C:/Users/原明美/Documents/ClaudeCode/exercise_cea}"
RS="${RSCRIPT:-/c/Program Files (x86)/R/R-4.5.1/bin/Rscript.exe}"
label="$1"; setting="$2"
out="$ROOT/output/phase1/round12/$label"; fits="$ROOT/data/fits/round12/$label"
mkdir -p "$out" "$fits"
export EXERCISE_CEA_EFS_CONSTRAINT="$setting"
"$RS" "$ROOT/R/04_fit_models.R" > "$out/04_fit_models.log" 2>&1 || true
grep -q "Execution halted" "$out/04_fit_models.log" && { echo "04 failed"; exit 1; }
"$RS" "$ROOT/R/05_calibrate.R" > "$out/05_calibrate.log" 2>&1 || true
grep -q "Execution halted" "$out/05_calibrate.log" && { echo "05 failed"; exit 1; }
cd "$ROOT/output/phase1"
cp -p calibration*.csv dr_early_share.csv dr_survival_implied.csv ae_deaths.csv engine_checks.csv scenario_k1*.csv \
      fig_calibration_OS.png fig_engine_checks.png "$out/"
y="${setting%%,*}"; t="${setting##*,}"
if [ "$t" = "equal" ]; then cp -p "efs${y}_equality_constraint.csv" "$out/"; else cp -p "efs${y}_constraint.csv" "$out/"; fi
cd "$ROOT/data/fits"
cp -p fits.rds calibration_candidates.rds "$fits/"
[ -f engine_params.rds ] && cp -p engine_params.rds "$fits/" || true
cat "$ROOT/output/phase1/calibration_status.csv"
