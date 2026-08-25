# RAOP selector protocol

This file records the selector definition applied to the compatibility-processed
ISPD 2015 suite and then held fixed for the ICCAD 2017 evaluation. Final
Innovus detailed-routing DRC is downstream evaluation only and is not a
selector input.

## Ordered gates

The five selector thresholds are
`(mean congestion, top-1% mass, connected hotspot mass, H/V imbalance,
probe overflow response) = (0.010, 0.20, 0.10, 3.0, -0.10)`.

1. Select legacy inflation when mean congestion is at least `0.010`, top-1%
   congestion mass is at least `0.20`, and connected hotspot mass is at least
   `0.10`.
2. Otherwise select directional XY when H/V imbalance is at least `3.0`.
3. Otherwise execute one rollback-capable scalar probe. Select no-deflation
   when `(overflow_before - overflow_after) / max(overflow_before, 1)` is at
   most `-0.10`; otherwise retain the probe and select scalar.

The frozen ISPD 2015 allocation is one legacy, five XY, six no-deflation, and
eight scalar instances. Thus 14 of 20 instances reach the probe. The full raw
descriptor and normalized-margin record is
`results/ispd2015/decision_trace/decision_trace_and_margins.csv`.

## Evaluation boundary

The settings are flow-specific heuristic thresholds. Their one-at-a-time
stability record is provided under `results/ispd2015/thresholds/`. Holding the
selector fixed before the ICCAD 2017 evaluation prevents feedback from that
downstream benchmark into these settings; it does not establish universal
threshold validity across other placers, routers, technologies, or datasets.
