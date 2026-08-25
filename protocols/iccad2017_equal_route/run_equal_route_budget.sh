#!/usr/bin/env bash
set -euo pipefail

experiment_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${experiment_root}/../.." && pwd)"
gpu_index="${1:-7}"
run_stamp="$(date +%Y%m%dT%H%M%S%z)"
formal_root="${experiment_root}/formal_runs/${run_stamp}"

mkdir -p "${formal_root}"

git -C "${repo_root}" rev-parse HEAD > "${formal_root}/git_head.txt"
git -C "${repo_root}" status --short --branch > "${formal_root}/git_status_before_run.txt"
nvidia-smi \
  --query-gpu=index,name,driver_version,memory.total \
  --format=csv,noheader > "${formal_root}/gpu_environment.csv"

run_variant() {
  local label="$1"
  shift
  local result_root="${formal_root}/${label}"
  mkdir -p "${result_root}"

  (
    cd "${repo_root}"
    CUDA_VISIBLE_DEVICES="${gpu_index}" python main.py \
      --dataset iccad2017_fix \
      --run_all True \
      --use_cell_inflate True \
      --equal_route_budget_control True \
      --equal_route_budget_rounds 15 \
      --result_dir "${result_root}" \
      --exp_id "_${label}" \
      "$@"
  ) 2>&1 | tee "${formal_root}/${label}.console.log"

  find "${result_root}" -mindepth 1 -maxdepth 1 -type d -printf '%p\n' \
    | sort | tail -n 1 > "${formal_root}/${label}.run_path.txt"
}

run_variant G1_EQB15
run_variant G4_EQB15 --use_cell_inflate_momentum True

python "${experiment_root}/verify_equal_route_budget.py" \
  --g1-run "$(<"${formal_root}/G1_EQB15.run_path.txt")" \
  --g4-run "$(<"${formal_root}/G4_EQB15.run_path.txt")" \
  --output-dir "${formal_root}/audit"

printf '%s\n' "${formal_root}" > "${experiment_root}/LATEST_FORMAL_RUN.txt"
printf 'Formal equal-route-budget run complete: %s\n' "${formal_root}"
