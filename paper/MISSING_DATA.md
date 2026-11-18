# Missing data required before submission

Every item below is a number or artefact that the paper needs but that could not be verified
from the repository snapshot (raw run records live only on the cluster scratch filesystem).

| # | Needed for | Item | Where to get it |
|---|---|---|---|
| D1 | Table 1, Threats | Exact Qwen commit and Transformers/PyTorch versions resolved by the **pilot** (config said `revision: main`) | `model_revision`/`tokenizer_hash` fields of pilot `generations.jsonl`; job manifests in `ledger/jobs/` |
| D2 | Sec. 5.2 | Mean output length and z>=4 counts for **every** calibration cell (only the primary cell's 174/1200 is reported) | calibration JSONL under `runs/kgw-qwen25-coder-7b-pilot/calibration/` |
| D3 | Gate N | Cross-key null scores (key-specific FPR at z>=4), paired z shifts | `a10 validate-kgw` (P0 validation) — **not yet run** per `HPC_RUN_LOG.md` |
| D4 | Gate M | Synthetic conformance green fraction per key on the cluster environment | P0 validation `report.json` — not yet run. (Locally: the 4 Transformers-dependent tests were skipped because torch/transformers could not be installed in the drafting sandbox; 28 other tests passed.) |
| D5 | Sec. 5.3 | Row-level pilot records to compute **task-clustered** bootstrap intervals and a proper $\hat\sigma^2_\mathcal{K}$ (current intervals are row-level Wilson, anti-conservative) | merged pilot parquet; run `scripts/make_figures.py` extension |
| D6 | Main table (AAAI spec asks mean ± std across seeds) | Per-seed rates per key | same as D5 — `[TBD_METRIC]`; not reported in paper |
| D7 | Sec. 5.3 | Per-family security label table (paper only states the qualitative family inspection) | pilot score records grouped by `evaluation.family` |
| D8 | Sec. 5.4 | Whether the Transformers detector excluded repeated n-grams | detector config in pilot environment |
| D9 | Whole paper | CWEval integration, corrected pilot rerun, 100-key main run | future experiments (see `docs/ARXIV_READINESS_PLAN.md`) |
| D10 | Abstract/Intro | Token-pair audit risk score ($\rho$ in decision rule) results | `a10 audit` outputs — not run |
