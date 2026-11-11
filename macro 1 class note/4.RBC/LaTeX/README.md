# Macro 1 notes: LaTeX format (topic 4, RBC)

The format is the micro 1 house style (`macrostyle.sty` is a copy of `microstyle.sty`
with a macro title block). The derivation layout follows the Concordia ECON615 notes:
a Bellman equation with a Lagrange multiplier, FOCs labelled by variable, the envelope
theorem, then "update" and "eliminate the multipliers" steps.

* `RGM3.tex`: Ramsey growth model in discrete time (Hamiltonian, then DP)
* `RBC1.tex`: the baseline RBC model
* `./build.sh` builds every `*.tex` and writes `../<STEM> - <shortname> (LaTeX).pdf`

Preamble: `\documentclass[11pt]{article}` + `\usepackage{macrostyle}` only.
Title block: `\noteheader{title}{subtitle}{date}`. FOC lines: `\foc{c_t}{u'(c_t)=\lambda_t}`
inside `align`. Each note ends with a `transcriptnotes` block (the audit trail).
