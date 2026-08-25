# Result inventory

## ISPD 2015 main comparison

`results/ispd2015/main/` provides the 20-instance, machine-readable source
tables for the manuscript's E0 (no inflation), E1 (original legacy), and E4
(RAOP) comparison. Every row contains detailed routed wirelength, via count,
DRC count, placement time, and detailed-routing time.

The E4 comparison must be read together with the processed-input boundary in
the root README. In particular, these are not official ISPD 2015 contest
scores and do not imply that the original fence constraints were retained.

## ISPD 2015 controls

`results/ispd2015/ablations/` contains the full 20-instance final CSVs for the
fixed scalar control (E2), static selector (E3), and the three branch-removal
controls used in the manuscript table (E5a--E5c). These files support checking
the arithmetic per-instance ratios whose averages appear in the ablation table.

`results/ispd2015/thresholds/` contains the decision-stability and
classification-change records used for the one-at-a-time threshold perturbation
analysis. They are evidence about selector decisions, not a new independent
benchmark suite.

## ICCAD 2017 equal-route-opportunity control

The two final CSVs cover eight compatibility-processed designs. E1-EQ/G1 and
E4-EQ/G4 each have 15 counted route-optimization rounds and 16 global-routing
candidates per design, as recorded in the redacted audit. The primary DRC
aggregate is the paired geometric ratio:

```text
exp(mean(log(DRC_E4-EQ / DRC_E1-EQ))) = 0.958013
```

This equals a `-4.198711%` aggregate change. The same data give `3/0/5`
DRC wins/ties/losses and a `+2.128495%` median per-design change. These
quantities must be reported together; the result does not show a majority or
typical-design advantage.
