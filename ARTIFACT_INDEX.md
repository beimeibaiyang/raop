# Public artifact index

This index maps the manuscript's empirical claims to the smallest public set
needed to check them. `provenance/SHA256SUMS` is the integrity manifest for the
whole package.

| Manuscript claim or definition | Public evidence |
|---|---|
| ISPD 2015 E0/E1/E4 per-design results and 27.49%/73.82% paired DRC reductions | `results/ispd2015/main/table1_e0_e1_e4.csv` |
| Fixed-scalar, static-selector, and branch-knockout results | `results/ispd2015/ablations/` |
| Frozen five-threshold selector and branch allocation | `protocols/ispd2015/SELECTOR_PROTOCOL.md`, `results/ispd2015/decision_trace/decision_trace_and_margins.csv` |
| One-at-a-time threshold stability | `results/ispd2015/thresholds/` |
| Standard ICCAD 2017 E0/E1/E4 comparison | `results/iccad2017_standard/` |
| ICCAD 2017 equal-route E1-EQ/E4-EQ results and opportunity counts | `results/iccad2017_equal_route/`, `audit/iccad2017_equal_route/`, `protocols/iccad2017_equal_route/` |
| Equal-route controller implementation | `code/EQUAL_ROUTE_EXPERIMENT_COMMIT.txt`, `code/equal_route_budget_implementation.diff` |
| ISPD 2015 compatibility-processing scope | `provenance/ispd2015_transformations_public.csv` |
| ICCAD 2017 compatibility-processing and exact reconstruction checks | `provenance/iccad2017_reconstruction_audit_public.csv`, `provenance/iccad2017_input_hashes_public.csv` |
| Tool and host settings | `protocols/ispd2015/innovus_environment_manifest.md` |
| Numerical recomputation | `scripts/recompute_reported_results.py` |
| Paper wording, operator constants, and full Supplement tables | `paper/` |

## Included because they are necessary

- Final machine-readable result tables for every quantitative results section.
- Selector descriptors, margins, threshold-stability records, and experiment
  protocols needed to interpret the comparisons.
- Public transformation audits, input hashes, opportunity-count audits, code
  identifiers, and a code-only diff needed to connect the reported control to
  its implementation.
- A single comprehensive recomputation script, manuscript snapshots, scope
  limitations, notices, and package checksums.

## Intentionally excluded

- Original or processed benchmark LEF/DEF inputs where redistribution rights
  are not established.
- Generated or routed DEFs, proprietary Innovus reports and raw logs,
  per-repeat reports, licence settings, and institutional filesystem paths.
- The complete XPlace/RAOP source tree, unrelated experiments, failed runs,
  development timelines, worktree names, and non-public commit ancestry.

The exclusions limit independent end-to-end reproduction, but they do not
prevent recomputation of the paper's reported aggregates from the released
final tables.
