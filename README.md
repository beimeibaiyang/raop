# RAOP evidence package

This repository is a compact, auditable evidence package for the manuscript
**RAOP: Runtime-Adaptive Operator Selection for Routability-Driven
Placement**. It contains the releasable machine-readable results, selector and
equal-route protocols, input-transformation records, implementation evidence,
verification scripts, manuscript snapshots, and checksums needed to check the
reported claims. Restricted benchmark inputs and proprietary detailed-routing
artifacts are not included.

## Contents

- `ARTIFACT_INDEX.md`: claim-to-file map and the authoritative inclusion and
  exclusion boundary for this evidence package.
- `paper/`: the manuscript and Supplementary Material snapshots associated
  with this package.
- `results/ispd2015/`: the final 20-instance compatibility-processed ISPD 2015
  tables used for the main comparison, selector controls, branch ablations,
  decision trace, and threshold-stability analysis.
- `results/iccad2017_standard/`: the E0, E1, and E4 cross-benchmark results on
  eight compatibility-processed ICCAD 2017 instances.
- `results/iccad2017_equal_route/`: the final eight-instance E1-EQ (G1_EQB15)
  and E4-EQ (G4_EQB15) CSVs. The placement-time field is transcribed by
  design from the corresponding placement-run summary.
- `audit/iccad2017_equal_route/`: redacted budget-verification artifacts. All
  16 variant--design cases pass 15 counted route-optimization rounds and 16
  global-routing candidates.
- `protocols/`: selector settings, the recorded Innovus environment, and the
  equal-route procedure, runner, and verifier.
- `code/`: the equal-route experiment commit, a code-only implementation diff,
  and the upstream licence notice.
- `provenance/`: public input-transformation audits, input hashes with paths
  removed, code identifiers, and checksums for every distributed file.

## Interpretation boundaries

The ISPD 2015 results are matched within-flow measurements on
compatibility-processed inputs. They are not official contest scores;
fence-region constraints were removed for the nine instances marked in the
manuscript.

The ICCAD 2017 control matches route-opportunity counts only: 15 counted
rounds and 16 global-router evaluations per variant--design pair. It does not
equalize wall time, computational work, state trajectories, or detailed-routing
cost.

Raw/routed DEF files, LEF files, original benchmark inputs, Innovus raw logs,
per-repeat reports, licence configuration, complete source code, and internal
filesystem paths are intentionally excluded. DRC, DRWL, and via counts in the
published final CSVs are the common values across three Innovus runs;
detailed-routing time is their arithmetic mean. Repeat-level data remain in a
restricted, licensed environment.

## Verification

Run the following from the repository root:

```bash
sha256sum -c provenance/SHA256SUMS
python3 scripts/recompute_reported_results.py
```

The second command checks the ISPD 2015 main and ablation tables, selector
allocation and threshold stability, the standard ICCAD 2017 comparison, and
the equal-route-opportunity results. It fails if a distributed source table no
longer reproduces the manuscript values.

## Citation and versioning

For manuscript v55, use tag `v1.1-evidence`. The `v1.0-evidence` tag is retained
as a historical pre-v55 package. This package is evidence-only and does not make
a claim of full external Innovus reproducibility.