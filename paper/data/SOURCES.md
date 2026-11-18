# Provenance of every number in `data/`

No row-level generation or score records were available to the paper authors' tooling
(raw records live on `$SCRATCH/a10/runs/` on NYU Torch and are intentionally excluded from Git).
Every value below is transcribed verbatim from the project repository (`a10-kgw-key-audit`):

| File | Source in repository |
|---|---|
| `security_pilot_v2_per_key.csv` | `docs/SECURITY_PILOT_RESULTS_2026-11-12.md`, tables "Aggregate outcome by key" and "Detector outcome" |
| `calibration_v1_mean_z.csv` | `docs/EXPERIMENT_STATUS.md` ("Full dose response") and `docs/HPC_RUN_LOG.md` job 22638147 |

Additional scalars used in the text (same sources): corrected smoke 960 rows, mean z 0.995,
2/480 at z>=4 (job 22623551); micro-calibration 90 rows, primary cell mean z 1.758, 1/15 at z>=4
(job 22631551); full calibration primary cell 174/1200 at z>=4; K0000 paired table 24/5/2/41.

Derived quantities (Wilson intervals, Spearman correlations, exact McNemar p, implied green
fractions, runtime projections) are computed by `scripts/make_figures.py` and printed to
`data/derived_stats.txt`.
