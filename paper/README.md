# AAAI-26 manuscript: KGW watermark-key audit for secure code generation

**Title:** *Are Valid Watermark Keys Interchangeable? A Paired Protocol and Pilot Evidence for
KGW-Watermarked Secure Code Generation* (anonymous submission build)

> Scope note: the request asked for an "IIDE" paper, but the linked GitHub repository was empty and
> every supplied artefact is the A10 KGW key-audit project. The author chose to write this paper
> from the A10 materials. Nothing in it concerns IIDE.

## Build

```bash
python3 scripts/make_figures.py          # figures/*.pdf + data/derived_stats.txt
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Requires TeX Live (latex-extra, fonts-recommended, cm-super for figure text) and Python with
matplotlib + scipy. Last build: 0 errors, 0 undefined refs, 0 overfull boxes, all fonts Type 1.
**Main text ends on page 6** (limit 7). References start on page 7, and the checklist follows on a new page.

## Layout

| Path | Content |
|---|---|
| `main.tex` | AAAI-26 root; 5 candidate titles listed in comments |
| `sections/00–06` | abstract, intro, related work, preliminaries, method, experiments, conclusion + ethics |
| `ReproducibilityChecklist.tex` | official AAAI-26 checklist, answered |
| `references.bib` | 23 hand-verified entries |
| `figures/` | `dose_response.pdf`, `per_key_outcomes.pdf`, `z_vs_functional.pdf` (pipeline diagram is TikZ in §4) |
| `data/` | aggregate tables transcribed from the repo + `SOURCES.md` provenance + `derived_stats.txt` |
| `scripts/make_figures.py` | the only code that produces numbers not copied verbatim from the repo |
| `notes/NOTATION.md`, `notes/macros.tex` | notation lock |
| `MISSING_DATA.md`, `MISSING_CITATIONS.md` | what a human must still supply or check |

## AAAI-26 author kit provenance (important)

`aaai.org` and Overleaf were unreachable from the drafting sandbox. The style files came from public
GitHub mirrors:

- `aaai2026.sty`: version `2026/06/17` with the checklist hooks, from the
  `QuenithAI/aaai-26-reproduction-checklist` copy of the kit (sha256 `6f90c4d7…`). It differs from
  the older `2026/04/29` mirror copy only in the date line and the two checklist lines.
- `aaai2026.bst`: identical sha256 (`ac26e2c6…`) in two independent mirrors
  (`lizhemin15/AAAI-2026-Latex-Unified`, `davila7/claude-code-templates`).
- `ReproducibilityChecklist.tex`: the official template from the same kit copy. Only the
  "Type your response here" answers were changed.

**Before submitting, replace all three files with the copies in the official AAAI-26 Author Kit
and rebuild.**

## How the numbers were verified

- Every reported count, rate and z-value matches `docs/SECURITY_PILOT_RESULTS_2026-11-12.md`,
  `docs/EXPERIMENT_STATUS.md` and `docs/HPC_RUN_LOG.md` in the A10 repo.
  `make_figures.py` asserts internal consistency: each key's security labels sum to 72, the pooled
  secure-and-functional count is 231/720, and 21 outputs reach z ≥ 4.
- Recomputed independently: the K0000 exact McNemar p = 0.453 (repo says ≈ 0.45), the functional
  range 12.5–70.8% and the secure-and-functional range 5.6–43.1%.
- Code claims (key derivation, sandbox flags, fail-closed preflight, z recomputation, gates) were
  checked against `src/a10_keyaudit/*.py`. Repo unit tests run on a copy: 28 passed, 4 skipped
  (the 4 need torch/transformers, which were unavailable in the sandbox).
- No row-level records were available, so all intervals are row-level Wilson intervals. The paper
  labels them as anti-conservative.

## Honest framing (what the paper does and does not claim)

The paper claims a formulation (two estimands and two short propositions), a protocol, and pilot
diagnostics. It explicitly does **not** claim a key-dependent security effect, a weak key, an
average watermark cost, or generality beyond one model. The P0 validation and the 13-setting sharded
calibration exist in code but have no run record, so they are described as planned gates, not
results.

## Open items before submission

See `MISSING_DATA.md` (D1–D10) and `MISSING_CITATIONS.md`. The most important: run Gate N (P0
validation), pin the pilot's resolved model commit, and obtain row-level records so clustered
intervals can replace the Wilson intervals.
