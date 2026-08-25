#!/usr/bin/env python3
"""Recompute the manuscript's reported aggregates from public CSV files."""

from __future__ import annotations

import csv
import math
import statistics
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METRICS = {
    "DRWL": "DRWL",
    "vias": "#DRVias",
    "DRC": "#DRCs",
    "PT": "place_design_time",
    "RT": "DR Total Time (s)",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def geometric_mean(values: list[float]) -> float:
    if not values or any(value <= 0 for value in values):
        raise ValueError("geometric means require nonempty positive values")
    return math.exp(sum(math.log(value) for value in values) / len(values))


def ratio_summary(candidate: dict[str, float], reference: dict[str, float]):
    if candidate.keys() != reference.keys():
        raise ValueError("candidate and reference design sets differ")
    ratios = [candidate[design] / reference[design] for design in candidate]
    return {
        "ratio": geometric_mean(ratios),
        "change": 100.0 * (geometric_mean(ratios) - 1.0),
        "median": statistics.median(100.0 * (ratio - 1.0) for ratio in ratios),
        "wtl": (
            sum(ratio < 1.0 for ratio in ratios),
            sum(ratio == 1.0 for ratio in ratios),
            sum(ratio > 1.0 for ratio in ratios),
        ),
    }


def assert_close(actual: float, expected: float, tolerance: float = 5e-6) -> None:
    if not math.isclose(actual, expected, rel_tol=0.0, abs_tol=tolerance):
        raise AssertionError(f"expected {expected}, obtained {actual}")


def load_main_table():
    path = ROOT / "results/ispd2015/main/table1_e0_e1_e4.csv"
    rows = read_csv(path)
    if len(rows) != 21 or rows[-1]["design"] != "average_ratio_vs_E4":
        raise AssertionError("unexpected ISPD 2015 main-table shape")
    data_rows, aggregate_row = rows[:-1], rows[-1]
    groups = {}
    for group in ("E0", "E1", "E4"):
        groups[group] = {
            metric: {
                row["design"]: float(row[f"{group}_{suffix}"])
                for row in data_rows
            }
            for metric, suffix in {
                "DRWL": "DRWL",
                "vias": "DRVias",
                "DRC": "DRCs",
                "PT": "PT_s",
                "RT": "RT_s",
            }.items()
        }
    return groups, aggregate_row


def load_simple_variant(path: Path):
    rows = read_csv(path)
    if len(rows) not in (8, 20):
        raise AssertionError(f"unexpected row count in {path}: {len(rows)}")
    return {
        metric: {row["design"]: float(row[column]) for row in rows}
        for metric, column in METRICS.items()
    }


def check_ispd_main(groups, aggregate_row):
    print("ISPD 2015 main comparison")
    for reference, expected_reduction, expected_wtl in (
        ("E0", 73.8166585395, (19, 0, 1)),
        ("E1", 27.4861678692, (18, 0, 2)),
    ):
        summary = ratio_summary(groups["E4"]["DRC"], groups[reference]["DRC"])
        reduction = -summary["change"]
        assert_close(reduction, expected_reduction)
        if summary["wtl"] != expected_wtl:
            raise AssertionError(f"unexpected E4/{reference} W/T/L")
        print(f"  E4 vs {reference}: DRC reduction {reduction:.2f}%; W/T/L {summary['wtl']}")

    for group in ("E0", "E1", "E4"):
        for metric, suffix in {
            "DRWL": "DRWL",
            "vias": "DRVias",
            "DRC": "DRCs",
            "PT": "PT_s",
            "RT": "RT_s",
        }.items():
            ratios = [
                groups[group][metric][design] / groups["E4"][metric][design]
                for design in groups["E4"][metric]
            ]
            actual = sum(ratios) / len(ratios)
            expected = float(aggregate_row[f"{group}_{suffix}"])
            assert_close(actual, expected, tolerance=1e-12)
    print("  Table 1 arithmetic ratio row: PASS")


def check_ispd_ablations(groups):
    print("ISPD 2015 controls and branch ablations")
    files = {
        "E2": "E2_fixed_scalar.csv",
        "E3": "E3_static_selector.csv",
        "E5a": "E5a_without_legacy.csv",
        "E5b": "E5b_without_xy.csv",
        "E5c": "E5c_without_no_deflation.csv",
    }
    variants = {
        group: load_simple_variant(ROOT / "results/ispd2015/ablations" / name)
        for group, name in files.items()
    }
    variants["E4"] = groups["E4"]

    published = {
        row["experiment"]: row
        for row in read_csv(
            ROOT / "results/ispd2015/ablations/table2_ablation_average_ratios.csv"
        )
    }
    suffixes = {
        "DRWL": "DRWL_avg_ratio_vs_E4",
        "vias": "DRVias_avg_ratio_vs_E4",
        "DRC": "DRCs_avg_ratio_vs_E4",
        "PT": "PT_avg_ratio_vs_E4",
        "RT": "RT_avg_ratio_vs_E4",
    }
    for group in ("E2", "E3", "E4", "E5a", "E5b", "E5c"):
        for metric, column in suffixes.items():
            ratios = [
                variants[group][metric][design] / groups["E4"][metric][design]
                for design in groups["E4"][metric]
            ]
            assert_close(
                sum(ratios) / len(ratios),
                float(published[group][column]),
                tolerance=1e-12,
            )
    print("  Table 2 arithmetic ratios: PASS")

    for group, expected, expected_wtl in (
        ("E2", 21.22, (11, 8, 1)),
        ("E3", 4.16, (6, 14, 0)),
    ):
        summary = ratio_summary(groups["E4"]["DRC"], variants[group]["DRC"])
        assert_close(-summary["change"], expected, tolerance=0.005)
        if summary["wtl"] != expected_wtl:
            raise AssertionError(f"unexpected E4/{group} W/T/L")
        print(f"  E4 vs {group}: DRC reduction {-summary['change']:.2f}%; W/T/L {summary['wtl']}")

    expected_branch = {
        "E5a": (1, 96.86, -96.86, (1, 0, 0)),
        "E5b": (5, 8.78, -2.35, (4, 0, 1)),
        "E5c": (6, 13.21, -12.53, (6, 0, 0)),
    }
    for group, (count, reduction, median, wtl) in expected_branch.items():
        affected = {
            design
            for design in groups["E4"]["DRC"]
            if groups["E4"]["DRC"][design] != variants[group]["DRC"][design]
        }
        summary = ratio_summary(
            {design: groups["E4"]["DRC"][design] for design in affected},
            {design: variants[group]["DRC"][design] for design in affected},
        )
        if len(affected) != count or summary["wtl"] != wtl:
            raise AssertionError(f"unexpected affected-case record for {group}")
        assert_close(-summary["change"], reduction, tolerance=0.005)
        assert_close(summary["median"], median, tolerance=0.005)
        print(f"  E4 vs {group}, affected cases: n={count}, reduction {-summary['change']:.2f}%")


def check_selector_records():
    print("Selector allocation and threshold stability")
    trace = read_csv(
        ROOT / "results/ispd2015/decision_trace/decision_trace_and_margins.csv"
    )
    allocation = Counter(row["base_category"] for row in trace)
    expected = Counter({"legacy": 1, "xy": 5, "no_deflation": 6, "scalar": 8})
    if allocation != expected:
        raise AssertionError(f"unexpected selector allocation: {allocation}")
    stability = read_csv(
        ROOT / "results/ispd2015/thresholds/configuration_stability.csv"
    )
    unchanged = sum(int(row["unchanged_count"]) for row in stability)
    changed_designs = {
        design
        for row in stability
        for design in row["changed_designs"].split(";")
        if design
    }
    if unchanged != 394 or len(changed_designs) != 3:
        raise AssertionError("threshold-stability totals do not match the manuscript")
    changes = read_csv(
        ROOT / "results/ispd2015/thresholds/classification_changes.csv"
    )
    if len(changes) != 6 or {row["threshold"] for row in changes} != {
        "top1_mass",
        "hv_imbalance",
    }:
        raise AssertionError("unexpected threshold classification-change record")
    print(f"  allocation {dict(allocation)}; OAT unchanged {unchanged}/400; fully stable 17/20")


def check_iccad_standard():
    print("ICCAD 2017 standard comparison")
    data = {
        group: load_simple_variant(ROOT / "results/iccad2017_standard" / filename)
        for group, filename in {
            "E0": "E0_no_inflation.csv",
            "E1": "E1_fixed_legacy.csv",
            "E4": "E4_raop.csv",
        }.items()
    }
    for reference, expected_reduction, expected_wtl in (
        ("E0", 30.4367811199, (5, 0, 3)),
        ("E1", 7.5667438775, (3, 0, 5)),
    ):
        summary = ratio_summary(data["E4"]["DRC"], data[reference]["DRC"])
        assert_close(-summary["change"], expected_reduction)
        if summary["wtl"] != expected_wtl:
            raise AssertionError(f"unexpected ICCAD E4/{reference} W/T/L")
        print(f"  E4 vs {reference}: DRC reduction {-summary['change']:.2f}%; W/T/L {summary['wtl']}")
    expected_e1 = {"DRWL": 1.0306549184, "vias": 0.9980966833, "DRC": 1.1436807795, "PT": 0.4420057597, "RT": 0.8947545003}
    for metric, expected in expected_e1.items():
        ratios = [
            data["E1"][metric][design] / data["E4"][metric][design]
            for design in data["E4"][metric]
        ]
        assert_close(sum(ratios) / len(ratios), expected)
    print("  E1/E4 descriptive arithmetic ratios: PASS")


def check_equal_route():
    print("ICCAD 2017 equal-route-opportunity control")
    e1 = load_simple_variant(ROOT / "results/iccad2017_equal_route/G1_EQB15.csv")
    e4 = load_simple_variant(ROOT / "results/iccad2017_equal_route/G4_EQB15.csv")
    expected = {
        "DRC": (0.958013, 2.128495, (3, 0, 5)),
        "DRWL": (0.982446, 0.938068, (3, 0, 5)),
        "vias": (1.004875, 1.580226, (1, 0, 7)),
        "PT": (1.051135, 6.786848, (2, 0, 6)),
        "RT": (1.292371, 7.575607, (2, 0, 6)),
    }
    for metric, (ratio, median, wtl) in expected.items():
        summary = ratio_summary(e4[metric], e1[metric])
        assert_close(summary["ratio"], ratio, tolerance=5e-7)
        assert_close(summary["median"], median, tolerance=5e-7)
        if summary["wtl"] != wtl:
            raise AssertionError(f"unexpected equal-route {metric} W/T/L")
        print(f"  {metric}: ratio {summary['ratio']:.6f}; median {summary['median']:+.6f}%; W/T/L {wtl}")

    audit = read_csv(
        ROOT / "audit/iccad2017_equal_route/budget_audit_public.csv"
    )
    if len(audit) != 16 or any(row["status"] != "PASS" for row in audit):
        raise AssertionError("equal-route opportunity audit is incomplete")
    print("  opportunity-count audit: 16/16 PASS")


def main() -> None:
    groups, aggregate_row = load_main_table()
    check_ispd_main(groups, aggregate_row)
    check_ispd_ablations(groups)
    check_selector_records()
    check_iccad_standard()
    check_equal_route()
    print("All public result checks passed.")


if __name__ == "__main__":
    main()
