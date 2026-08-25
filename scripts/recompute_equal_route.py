#!/usr/bin/env python3
"""Recompute published equal-route aggregates from the two final CSV files."""

import csv
import math
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "iccad2017_equal_route"
METRICS = {
    "DRC": "#DRCs",
    "DRWL": "DRWL",
    "DR vias": "#DRVias",
    "Placement time": "place_design_time",
    "Per-DEF mean DR time": "DR Total Time (s)",
}


def read_rows(name):
    with (RESULTS / name).open(newline="") as handle:
        return {row["design"]: row for row in csv.DictReader(handle)}


def main():
    baseline = read_rows("G1_EQB15.csv")
    raop = read_rows("G4_EQB15.csv")
    if set(baseline) != set(raop) or len(baseline) != 8:
        raise SystemExit("expected the same eight designs in both final CSVs")

    for label, column in METRICS.items():
        ratios = [float(raop[d][column]) / float(baseline[d][column]) for d in sorted(baseline)]
        geometric = math.exp(sum(math.log(x) for x in ratios) / len(ratios))
        changes = [(x - 1.0) * 100.0 for x in ratios]
        wins = sum(x < 1.0 for x in ratios)
        ties = sum(x == 1.0 for x in ratios)
        losses = sum(x > 1.0 for x in ratios)
        print(
            f"{label}: ratio={geometric:.6f}; change={(geometric - 1) * 100:.6f}%; "
            f"median={median(changes):+.6f}%; W/T/L={wins}/{ties}/{losses}"
        )


if __name__ == "__main__":
    main()
