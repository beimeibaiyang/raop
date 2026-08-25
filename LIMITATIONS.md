# Access and reproducibility limitations

1. The benchmark inputs are not distributed. The evaluated ISPD 2015 and
   ICCAD 2017 inputs are compatibility-processed datasets; their hashes are
   provenance anchors rather than redistributed benchmark content.
2. Cadence Innovus execution took place in a restricted institutional
   environment. The raw logs, reports, licence configuration, and complete
   environment are not available for external redistribution.
3. Placement time in the equal-route CSVs is the per-design value recorded by
   the corresponding placement run. The detailed-routing metrics were supplied after
   three independent runs per reported DEF. DRC, DRWL, and via counts were
   invariant; the reported detailed-routing time is the arithmetic mean. This
   package cannot independently assess repeat-level time dispersion.
4. The equal-route-opportunity control equalizes the stated event counts only;
   it is not an equal-compute or equal-wall-time experiment.
5. The evidence supports the finite, processed benchmark comparisons recorded
   here. It does not support statistical-significance claims or broad
   population-level generalization.
6. The complete XPlace/RAOP source tree is not distributed. The public
   implementation diff and protocol document the equal-route controller but do
   not by themselves reproduce the licensed end-to-end flow.
