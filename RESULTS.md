# Result inventory

## ISPD 2015 main comparison

`results/ispd2015/main/table1_e0_e1_e4.csv` is the authoritative 20-instance
machine-readable source for the manuscript's E0 (no inflation), E1 (original
legacy), and E4 (RAOP) comparison. It includes the placement times recovered
from the corresponding placement-run summaries. The final row contains the
arithmetic mean of the 20 matched experiment/E4 ratios used in Table 1.

The E4 comparison must be read together with the processed-input boundary in
the root README. In particular, these are not official ISPD 2015 contest
scores and do not imply that the original fence constraints were retained.

## ISPD 2015 controls

`results/ispd2015/ablations/` contains the final 20-instance CSVs for the fixed
scalar control (E2), static selector (E3), and the three branch-removal controls
(E5a--E5c). `table2_ablation_average_ratios.csv` records the full-precision
arithmetic averages displayed in Table 2.

`results/ispd2015/thresholds/` contains the decision-stability and redacted
classification-change records used for the one-at-a-time threshold
perturbation analysis. `results/ispd2015/decision_trace/` contains the raw
selector descriptors and normalized margins shown in the decision trace.
These files are evidence about selector decisions, not a new independent
benchmark suite.

## ICCAD 2017 standard cross-benchmark comparison

`results/iccad2017_standard/` contains the eight E0, E1, and E4 result rows
under the ordinary operator termination rules. These files reproduce the
30.44% E4-versus-E0 and 7.57% E4-versus-E1 paired geometric-mean DRC
reductions, their W/T/L counts, and the descriptive arithmetic ratios in the
manuscript.

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

Placement time is matched from each variant's corresponding placement-run
summary. Its paired geometric E4-EQ/E1-EQ ratio is `1.051135`
(`+5.113501%`), with a `+6.786848%` median change and `2/0/6` W/T/L.
