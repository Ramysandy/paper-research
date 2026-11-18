# CLAUDE.md — AAAI-26 Paper Automation Spec (project copy)

> Project override (from the requesting author, 2026-11-18): **do not push to GitHub and do not
> modify existing experiments.** Section 5 step 3 (git commit/push) is therefore disabled for this
> paper directory.

## 1. Standard
- Thesis-level rigor: every claim backed by a definition, derivation, complexity analysis,
  empirical result, or grounded error analysis.
- Phase 1 (generalist): Title, Abstract, Introduction must be clear and concrete.
- Phase 2 (specialist): Preliminaries, Method, proofs and analyses must satisfy domain experts.
- Zero fabrication: missing citation -> `\cite{VERIFY_AuthorYear}` + `MISSING_CITATIONS.md`;
  missing number -> `[TBD_METRIC]` + `MISSING_DATA.md`.

## 2. AAAI-26 formatting rules
- Preamble order exactly as in `main.tex` (`\usepackage[submission]{aaai2026}` for review).
- Banned: hyperref, navigator, geometry, titlesec, fontenc, setspace, parskip, balance, flushend,
  subcaption/minipage figure grouping, `\pagestyle`, `\thispagestyle`, negative `\vspace`,
  `\baselinestretch`, `\linespread`, `\enlargethispage`, body text < 10pt; never alter the
  copyright slug.
- Main paper <= 7 pages incl. figures, tables and Ethical Statement; references unlimited;
  `ReproducibilityChecklist.tex` after the bibliography.
- Captions below figures and tables, plain 10pt roman. Vector PDF figures, Type 1/TrueType only,
  labels >= 9pt, grayscale-readable. booktabs tables; bold best, underline second best.
- Double-blind: no names, affiliations, acknowledgements, identifying links; own prior work in
  third person.

## 3. Layout
main.tex, aaai2026.sty, aaai2026.bst, ReproducibilityChecklist.tex, references.bib,
notes/NOTATION.md, figures/, sections/00_abstract.tex … 06_conclusion.tex,
MISSING_CITATIONS.md, MISSING_DATA.md.

## 4. Steps 0–7
0 scaffold + notation lock; 1 titles + abstract (180–220 words, 5 beats, no cites/macros);
2 introduction (motivation, bottleneck, approach, 3–4 falsifiable contributions);
3 related work (3 thematic subsections, each ending with a contrast);
4 preliminaries (spaces, objective, assumptions, formal problem);
5 method (pipeline figure*, derivations, >=1 proposition with proof, Big-O, algorithm);
6 experiments (setup, main table mean±std, ablation, sensitivity/efficiency/failure analysis);
7 conclusion + ethics + checklist + full audit.

## 5. Build audit
1. Static scan for banned packages/commands and identifying strings.
2. `pdflatex; bibtex; pdflatex; pdflatex` — zero undefined refs; main text ends by page 7.
3. (Disabled for this project) git commit and push.
