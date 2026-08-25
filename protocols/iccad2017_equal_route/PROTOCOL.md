# RAOP ICCAD 2017 Equal-Route-Budget Control Protocol

## Material Passport

- Origin Skill: `academic-research-suite/experiment-agent`
- Origin Mode: `plan` -> `run`
- Experiment ID: `raop-iccad2017-equal-route-budget-v23`
- Status: `PREREGISTERED_BEFORE_FORMAL_RUN`
- Frozen ancestor: `a7ba8007c19a49c162f432b5cc119274c15ef47f`
- Dataset: `data/raw/iccad2017_fix` (8 compatibility-processed designs)
- Seed: `0`
- Deterministic: `True`

## Research question

Does the observed ICCAD 2017 E4-versus-E1 detailed-routing DRC contrast remain
when both systems receive the same realized number of global-routing and
placement-refinement opportunities?

## Controlled budget

The budget is exactly 15 routability-optimization rounds per design after the
initial placement phase. A final global-routing evaluation is then performed for
candidate selection. Therefore every successful design/variant run must record:

- 15 `Route Iter` events;
- 16 actual global-router invocations/candidates, including the final evaluation;
- a real placement-refinement phase between consecutive budgeted route events.

The value 15 is the frozen algorithm's existing default maximum and was selected
before inspecting any equal-budget detailed-routing result.

If a policy's original actuation termination condition fires before round 15,
its cell-size state is frozen, but placement refinement and GR evaluation
continue. Repeated GR calls without intervening refinement are prohibited.

## Experiment matrix

| Filesystem label | Manuscript label | Policy | Budget |
|---|---|---|---|
| `G1_EQB15` | `E1-EQ` | fixed legacy inflation | 15 route-optimization rounds |
| `G4_EQB15` | `E4-EQ` | frozen four-policy RAOP | 15 route-optimization rounds |

The original E1/E4 results remain the unconstrained complete-system results.
These controls are additional variants and do not replace or overwrite them.

## Frozen factors

- selector thresholds, probe, rollback, actuation, tolerances, and per-policy
  candidate selectors remain unchanged;
- input transformations and design set remain unchanged;
- seed, deterministic mode, placement/legalization flow, and output format remain
  unchanged;
- equal-budget flags default to off and cannot alter historical commands.

Only the external opportunity/termination controller is changed. Accordingly,
the control removes the known route-call imbalance but is not described as a
perfect single-factor causal isolation of the selector.

## Formal commands

```bash
CUDA_VISIBLE_DEVICES=7 python main.py \
  --dataset iccad2017_fix --run_all True \
  --use_cell_inflate True \
  --equal_route_budget_control True \
  --equal_route_budget_rounds 15

CUDA_VISIBLE_DEVICES=7 python main.py \
  --dataset iccad2017_fix --run_all True \
  --use_cell_inflate True \
  --use_cell_inflate_momentum True \
  --equal_route_budget_control True \
  --equal_route_budget_rounds 15
```

## Success and fail-closed criteria

- Both commands exit with status 0.
- Each output contains exactly the same 8 unique designs and 8 DEF files.
- Every design has exactly 15 `Route Iter` events and 16 GR candidates.
- Every adjacent budgeted GR event has intervening placement iterations.
- E4 selector decisions and selected policies are present for all 8 designs.
- No PA-recovery/P2/P3 marker is present.
- Any missing design, budget mismatch, duplicate DEF, crash, or timeout is
  retained and reported; it is not silently retried or excluded.

## Innovus handoff

Every new DEF is routed independently three times with Innovus
`22.30-s003_1`. Return the per-repeat DRC, DRWL, via count, route time, raw log,
and report. DRWL/via/DRC are expected to be invariant; only route time is
averaged. Any non-runtime divergence is flagged rather than silently averaged.

## Analysis lock

- Primary endpoint: final detailed-routing DRC.
- Primary contrast: paired `E4-EQ` versus `E1-EQ` across all 8 designs.
- Report every per-design result, W/T/L, and the paired geometric reduction when
  all DRC values are positive.
- If any DRC is zero, W/T/L and per-design counts remain primary; a `DRC+1`
  geometric ratio may be reported only as an explicitly labeled sensitivity.
- DRWL, via count, placement time, and routing time are descriptive secondary
  metrics.
- Do not claim population statistical significance from eight deterministic
  benchmark instances.
