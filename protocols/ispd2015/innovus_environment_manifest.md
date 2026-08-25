# Innovus detailed-routing environment manifest

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent
- Origin Mode: validate
- Origin Date: 2026-08-10
- Verification Status: ANALYZED; external environment metadata and dataset applicability confirmed by user
- Version Label: `innovus_environment_integrated_v2`

## Provenance

| Source | SHA-256 | Role |
|---|---|---|
| `final_result/innovus_environment.md` | `55602069c9ceb4e80319cbb7917f7ad6811fe550dce3172301a0b840e8347d3e` | User-provided tool, host and routing-setting metadata |
| `final_result/run_all_route_xplace_route.tcl` | `cdb87183c8c97435d71f5536daa8d4818c8cf186bf472bf93be1438f1ecaf6cc` | Archived Innovus routing procedure for the ISPD2015 design list |

The Innovus execution occurred in a confidential institutional environment.
Metadata not present in the two sources above is recorded as not disclosed; it
is not inferred from the local XPlace host.

## Tool and host

| Item | Recorded value |
|---|---|
| EDA tool | Cadence Innovus Implementation System |
| Innovus / routing-engine version | `v22.30-s003_1` |
| Placement framework label | `xplace_route` |
| Routing engine | NanoRoute |
| Operating system | CentOS Linux 7.9 |
| CPU | Intel Xeon Gold 6430 |
| CPU cores | 32 |
| Memory | 178 GB |
| Original metadata benchmark field | ISPD2015 / ISPD2019 |
| User-confirmed command applicability | ISPD2015 / ISPD2019 / ISPD2018 / ISPD2014 |
| Evaluation metrics | DRC, wirelength, runtime |

The user clarified that `Threads = 8` reports `Total CPU(s) enabled with current
License(s): 8`. The archived TCL requests
`set_multi_cpu_usage -local_cpu 10`, and observed execution used 10 threads.
Accordingly, 10 is the experimental routing-thread setting; 8 is retained only
as license-report metadata and is not used as the runtime thread count.

## Routing configuration

| Setting | Recorded value | Evidence |
|---|---|---|
| Routing layers | Metal1-Metal9 | User-provided environment metadata |
| Preferred direction | LEF-defined | User-provided environment metadata |
| Script-level local CPUs | 10 | Archived TCL |
| Timing constraints | None; physical-only flow | User-provided environment metadata |
| Congestion analysis | Enabled | User-provided environment metadata |
| Post-route via swapping | Enabled | User-provided environment metadata |
| Post-route wire spreading | Enabled | User-provided environment metadata |
| Via optimization | Enabled | User-provided environment metadata |

The archived TCL performs, in order, `read_physical`, `read_netlist -def`,
`init_design`, `route_design`, `report_route -summary`,
`check_drc -limit 100000000`, `write_def -routing`, and `reset_design` for each
design. It selects process node 28 for names matching `superblue` and process
node 65 otherwise.

## Dataset applicability

- **ISPD2015:** the archived TCL contains the exact design list and
  `ispd2015_fix` input/output path pattern.
- **ISPD2019, ISPD2018 and ISPD2014:** the user confirmed that each dataset
  uses the same TCL routing commands and changes only the design list and
  input/output paths.

The dataset-specific expanded TCL files are not archived, so this is a
user-confirmed procedural equivalence rather than a byte-identical script claim.

## Reproducibility boundary

The tool version, principal host specifications, routing engine, high-level
settings and one routing script are now archived. Exact command-line launch
context, full license configuration, full Innovus defaults, environment modules
and dataset-specific expanded TCL variants are not disclosed. Therefore
the external routing results are auditable at the recorded-metadata level but
are not independently reproducible outside the confidential environment.
