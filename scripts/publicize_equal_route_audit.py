#!/usr/bin/env python3
"""Create public audit files by removing internal paths from formal-run outputs."""

import argparse
import csv
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-csv", type=Path, required=True)
    parser.add_argument("--report-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if any(args.output_dir.iterdir()):
        raise SystemExit(f"refusing to overwrite non-empty directory: {args.output_dir}")

    with args.audit_csv.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    fields = [field for field in rows[0] if field != "def_path"]
    with (args.output_dir / "budget_audit_public.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{key: value for key, value in row.items() if key in fields} for row in rows])

    report = json.loads(args.report_json.read_text())
    for run in report.get("runs", []):
        for key in ("run_dir", "log_path", "run_all_csv"):
            run.pop(key, None)
    (args.output_dir / "verification_report_public.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )


if __name__ == "__main__":
    main()
