# Decision trace

`decision_trace_and_margins.csv` contains the 20 frozen selector allocations,
the raw first-route descriptors, the probe response where applicable, signed
normalized distances `(value - threshold) / abs(threshold)`, and the nearest
one-threshold-at-a-time policy-changing boundary.

The margins are rule-boundary distances, not probabilities or calibrated
confidence values. The three smallest margins are associated with the same
instances that account for the observed one-at-a-time allocation changes.
