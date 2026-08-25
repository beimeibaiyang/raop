# Innovus detailed-routing environment manifest

This public manifest records the environment fields needed to interpret the
reported physical-only routing results. It omits internal file locations,
licence configuration, and launch history.

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
| Evaluated suites in the manuscript | Compatibility-processed ISPD 2015 and ICCAD 2017 |
| Evaluation metrics | DRC, wirelength, runtime |

## Routing configuration

| Setting | Recorded value | Evidence |
|---|---|---|
| Routing layers | Metal1-Metal9 | User-provided environment metadata |
| Preferred direction | LEF-defined | User-provided environment metadata |
| CPUs enabled for the reported flow | 8 | Recorded environment metadata |
| Timing constraints | None; physical-only flow | User-provided environment metadata |
| Congestion analysis | Enabled | User-provided environment metadata |
| Post-route via swapping | Enabled | User-provided environment metadata |
| Post-route wire spreading | Enabled | User-provided environment metadata |
| Via optimization | Enabled | User-provided environment metadata |

The routing procedure reads the physical and DEF-based netlist data, initializes
the design, runs detailed routing, reports routing and DRC summaries, writes the
routed DEF, and resets the design between cases. Superblue designs use the
recorded 28-nm setting; the remaining ISPD 2015 designs use the recorded 65-nm
setting.

## Reproducibility boundary

The tool version, principal host specifications, routing engine, and high-level
settings are disclosed. Exact launch context, full licence configuration,
complete Innovus defaults, environment modules, benchmark inputs, and raw logs
are not disclosed. The results are therefore auditable at the recorded-metadata
level but are not independently reproducible outside a licensed environment.
