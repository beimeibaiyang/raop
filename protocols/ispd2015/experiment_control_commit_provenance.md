# E2-E6 experiment-control commit provenance

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: validate + handoff
- Origin Date: 2026-08-09
- Verification Status: VERIFIED
- Runtime base commit: `5dfda745fcc5d88baf184dd41bee643e17b5d233`
- Post-run archival commit: `66b7aa9941cdaf608e9c233cc183c8096017f4ca`
- Commit subject: `experiment: add routing policy ablation controls`

## Provenance rule

The post-run commit must not be described as if it existed when E2-E6 were
executed. Runtime provenance remains the recorded base commit plus the exact
experiment-control patch used by each run:

| Runtime group | Runtime base | Runtime patch SHA-256 |
|---|---|---|
| E2 / E3 | `5dfda745fcc5d88baf184dd41bee643e17b5d233` | `47f7f4d38b93d79dd4579815507a1a66bdda2acce7270b485c07545c9cb7968b` |
| E5a-E5d | `5dfda745fcc5d88baf184dd41bee643e17b5d233` | `1ae102440b9b14a7a4c5de6f4e097ea4d3f2abd42575a02a0e89f337aae2a1ae` |
| E6 | `5dfda745fcc5d88baf184dd41bee643e17b5d233` | `7d836f67c9218ff0880c236cf4708fe01e241211b88eec90b2c6586030ca2fbd` |

The archival commit contains the final superset used by E6. The binary diff
from the runtime base to the archival commit is exactly:

```text
7d836f67c9218ff0880c236cf4708fe01e241211b88eec90b2c6586030ca2fbd
```

Committed file SHA-256 values:

```text
b0430a0a7559c3f8e070481f641377417096eb5a9c5ffd90163a18f8be0c3129  main.py
fe3dda2b41e56f391244af7af0991002a0b399ec5b1507248166e67b8e78e93f  src/core/route_force.py
e2f10b9caa333cae8d7246fdd190f4c62b8987ad299826e3ebec6f4274ea158c  tests/test_momentum_inflation.py
```

Pre-commit validation: 58 unit tests passed and `git diff --check` passed.
The existing `experiment/momentum-scalar-v1` tag remains at the runtime base
commit and was not moved.

## Classifier-robustness threshold-control commit

The robustness check required CLI threshold overrides while preserving E4
defaults. That change was committed separately after the ablation controls:

```text
commit
  9abcf2fb0146c4a3b7faf9f54bd6a3bdce64ba53
parent
  66b7aa9941cdaf608e9c233cc183c8096017f4ca
subject
  experiment: parameterize routing classifier thresholds
binary diff SHA-256
  fc917b0c0f59a4b0469882ed69517dff3e00a603fb3fb16737fefa606d8c47a2
```

This commit also modifies exactly the same three experiment-control files.
All CLI defaults equal the frozen E4 thresholds, and omitting the override
flags retains `routing_policy_mode=auto`. Validation after this commit: 59
unit tests passed and `git diff --check` passed. The eight robustness reruns
record this commit, its parent and its patch SHA in
`classifier_robustness/run_metadata.csv`.
