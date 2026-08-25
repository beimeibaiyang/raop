#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


EXPECTED_DESIGNS = (
    "des_perf_b_md1",
    "des_perf_b_md2",
    "edit_dist_1_md1",
    "edit_dist_a_md2",
    "fft_2_md2",
    "fft_a_md2",
    "fft_a_md3",
    "pci_bridge32_a_md1",
)
EXPECTED_ROUTE_ITERS = 15
EXPECTED_GR_CALLS = 16


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_run(run_dir, label):
    run_dir = Path(run_dir).resolve()
    log_path = run_dir / "log" / "test.log"
    csv_path = run_dir / "log" / "run_all.csv"
    if not log_path.is_file() or not csv_path.is_file():
        raise FileNotFoundError(f"missing run log/CSV under {run_dir}")

    with csv_path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    designs = [row["design"] for row in rows]
    if tuple(designs) != EXPECTED_DESIGNS:
        raise ValueError(f"{label}: unexpected design order/set: {designs}")

    sections = {design: [] for design in designs}
    current = None
    for line in log_path.read_text(errors="replace").splitlines():
        match = re.match(r"design_name:\s*(\S+)\s*$", line)
        if match and match.group(1) in sections:
            current = match.group(1)
        if current is not None:
            sections[current].append(line)

    def_paths = sorted((run_dir / "output").glob("*.def"))
    def_by_design = {}
    for design in designs:
        matches = [path for path in def_paths if path.name == f"placement_{design}_dp.def"]
        if len(matches) != 1:
            raise ValueError(f"{label}/{design}: expected one DEF, found {len(matches)}")
        def_by_design[design] = matches[0]

    audit_rows = []
    failures = []
    for design in designs:
        lines = sections[design]
        route_iters = sum("Route Iter:" in line for line in lines)
        gr_positions = [
            int(match.group(1))
            for line in lines
            if (match := re.search(r"Start GR in Iter:\s*(\d+)", line))
        ]
        gr_calls = len(gr_positions)
        intervening_refinement = all(
            later > earlier for earlier, later in zip(gr_positions, gr_positions[1:])
        )
        budget_audits = [line for line in lines if "Equal route budget audit |" in line]
        policies = [
            match.group(1)
            for line in lines
            if (match := re.search(r"Evaluation routing policy selected:\s*(\S+)", line))
        ]
        frozen_rounds = [
            int(match.group(1))
            for line in lines
            if (
                match := re.search(
                    r"policy actuation frozen at round\s+(\d+)", line
                )
            )
        ]
        row_ok = (
            route_iters == EXPECTED_ROUTE_ITERS
            and gr_calls == EXPECTED_GR_CALLS
            and intervening_refinement
            and len(budget_audits) == 1
            and (label != "G4_EQB15" or len(policies) == 1)
        )
        if not row_ok:
            failures.append(
                f"{label}/{design}: route_iters={route_iters}, gr_calls={gr_calls}, "
                f"refinement={intervening_refinement}, audits={len(budget_audits)}, "
                f"policies={policies}"
            )
        audit_rows.append(
            {
                "variant": label,
                "design": design,
                "route_iters": route_iters,
                "gr_calls": gr_calls,
                "gr_placement_iterations": ";".join(map(str, gr_positions)),
                "intervening_refinement": intervening_refinement,
                "selected_policy": policies[0] if policies else "",
                "actuation_frozen_round": frozen_rounds[0] if frozen_rounds else "",
                "def_path": str(def_by_design[design]),
                "def_sha256": sha256(def_by_design[design]),
                "status": "PASS" if row_ok else "FAIL",
            }
        )

    log_text = log_path.read_text(errors="replace")
    forbidden_markers = (
        "pa_recovery_mode",
        "P2 retry",
        "P3 retry",
        "candidate recovery",
    )
    found_forbidden = [marker for marker in forbidden_markers if marker in log_text]
    if found_forbidden:
        failures.append(f"{label}: forbidden PA-recovery markers: {found_forbidden}")

    return {
        "label": label,
        "run_dir": str(run_dir),
        "log_path": str(log_path),
        "run_all_csv": str(csv_path),
        "run_all_csv_sha256": sha256(csv_path),
        "log_sha256": sha256(log_path),
        "rows": audit_rows,
        "failures": failures,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--g1-run", required=True)
    parser.add_argument("--g4-run", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=False)
    runs = [
        load_run(args.g1_run, "G1_EQB15"),
        load_run(args.g4_run, "G4_EQB15"),
    ]
    rows = [row for run in runs for row in run["rows"]]
    failures = [failure for run in runs for failure in run["failures"]]

    with (output_dir / "budget_audit.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    report = {
        "experiment_id": "raop-iccad2017-equal-route-budget-v23",
        "expected_designs": list(EXPECTED_DESIGNS),
        "expected_route_iters_per_design": EXPECTED_ROUTE_ITERS,
        "expected_gr_calls_per_design": EXPECTED_GR_CALLS,
        "runs": [
            {key: value for key, value in run.items() if key != "rows"}
            for run in runs
        ],
        "def_count": len(rows),
        "pass_count": sum(row["status"] == "PASS" for row in rows),
        "failures": failures,
        "verdict": "PASS" if not failures else "FAIL",
    }
    (output_dir / "verification_report.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
