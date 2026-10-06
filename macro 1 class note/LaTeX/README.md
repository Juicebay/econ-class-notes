# Macro 1 class notes — LaTeX format

`macrostyle.sty` (v2.0, 2026-09-30) = house style: coloured headings, running header, and reading aids —
`keyresult` (blue, results to remember), `intuition` (green), `pitfall` (orange), `extra` (dashed,
**material not on the slides**), `recap`; `\why{...}` puts the reason for a derivation line at the right
margin; `\slides{...}` names the slides a section follows; `\step{n}{...}` numbers derivation steps.
Solow shorthands `\kh \yh \ch \ih \dk \gr{X} \gam` unchanged.

* `solow.tex` — Lectures 1–3 (Solow model), ordered like the decks: L1 (§1–4) → EV (§5–7) →
  DE (§8, differential equations / speed of convergence) → PO (§9) → assessment (§10) → formula sheet.
* `solow.pdf` — compiled output (`latexmk -pdf solow.tex`).
* `./build.sh` copies the PDF to `../Solow Model - Lectures 1-3 (LaTeX).pdf` — **that file currently holds
  hand annotations exported from iPad; rename it before running build.sh.**
* `backup_2026-09-30/` — the version before the readability rewrite.
* Sources: the slide PDFs in `../ECON6020 (01) F26 - .../`.

## Comp review notes (`comp_review/`)

Self-contained macro comprehensive-exam review, transcribed from handwritten notes (CamScanner scan,
2026-10-06) with full step-by-step derivations; errors in the handwritten notes are corrected silently.

* `main.tex` — preamble + `\input` of the sections: `s1_growth` (facts, Solow) → `s2_ramsey` (Ramsey, taxes,
  infrastructure/AK) → `s3_tools` (HJB, KFE, Brownian motion, Itô, Markov chains) → `s4_assets` (Lucas tree,
  complete markets) → `s5_hetero` (Huggett/Bewley/Aiyagari, Zipf) → `s6_cycles` (HP filter, RBC) →
  `s7_monetary` (Barro–Gordon) → appendix `s8_micro` (competitive markets, welfare, monopoly, price discrimination).
* Build: `pdflatex main.tex` (run 2–3 times for the TOC); the compiled copy is `../Macro Comp Review Notes.pdf`.
