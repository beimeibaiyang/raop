# RAOP evidence package

This public repository is a compact, auditable evidence package for the
manuscript **RAOP: Runtime-Adaptive Operator Selection for
Routability-Driven Placement**. It intentionally contains selected results,
protocols, code provenance, verification scripts, and checksums rather than
restricted benchmark inputs or proprietary detailed-routing artifacts.

## Contents

- `results/ispd2015/`: the 20-instance compatibility-processed `ispd2015_fix`
  results used for the main comparison, selector controls, branch ablations,
  and threshold-stability analysis.
- `results/iccad2017_equal_route/`: the final eight-instance E1-EQ (G1_EQB15)
  and E4-EQ (G4_EQB15) CSVs. The placement-time field is transcribed by
  design from the corresponding placement-run summary.
- `audit/iccad2017_equal_route/`: redacted budget-verification artifacts. All
  16 variant--design cases pass 15 counted route-optimization rounds and 16
  global-routing candidates.
- `protocols/`: frozen experimental procedures and the equal-route runner and
  verifier.
- `code/`: the equal-route experiment commit, its patch, and the upstream
  licence notice.
- `provenance/`: input hashes with filesystem paths removed, plus checksums for
  every file distributed in this package.

## Interpretation boundaries

The ISPD 2015 results are matched within-flow measurements on the
compatibility-preprocessed `ispd2015_fix` inputs. They are not official contest
scores; fence-region constraints were removed for the nine instances marked in
the manuscript.

The ICCAD 2017 control matches route-opportunity counts only: 15 counted
rounds and 16 global-router evaluations per variant--design pair. It does not
equalize wall time, computational work, state trajectories, or detailed-routing
cost.

Raw/routed DEF files, LEF files, original benchmark inputs, Innovus raw logs,
per-repeat reports, licences, and internal filesystem paths are intentionally
excluded. DRC, DRWL, and via counts in the published final CSVs are the common
values across three Innovus runs; detailed-routing time is their arithmetic
mean. Repeat-level data are unavailable here because they remain in a
restricted, licensed environment.

## Verification

Run the following from the repository root:

```bash
sha256sum -c provenance/SHA256SUMS
python3 scripts/recompute_equal_route.py
```

The second command recomputes the paired geometric ratios, medians, and
win/tie/loss counts from the two final ICCAD CSVs. It should reproduce the
reported DRC ratio of `0.958013` (a `-4.198711%` change) and the DRC W/T/L of
`3/0/5`.

## Citation and versioning

Use the tagged repository release that accompanies a manuscript version. This
package is evidence-only and does not make a claim of full external Innovus
reproducibility.
