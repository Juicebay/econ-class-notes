# Metrics 1 class notes — LaTeX format

Typeset versions of the handwritten lesson exports and of the problem sets, in
one fixed format.

```
metrics 1 class note*/
├── Lesson 1.pdf            original export
├── Lesson 1 - Linear Regression Model, OLS and Instruments (LaTeX).pdf   built from lesson01.tex
├── lesson 2.pdf            original export
├── Lesson 2 - IV, GMM, Gauss-Markov and the Geometry of OLS (LaTeX).pdf   built from lesson02.tex
├── Lesson 3.pdf            original export
├── Lesson 3 - Projection Matrices, R-squared and Partitioned Regression (LaTeX).pdf   built from lesson03.tex
├── Lesson 4.pdf            original export
├── Lesson 4 - FWL, Omitted Variables and the Linear Hypothesis (LaTeX).pdf   built from lesson04.tex
├── Lesson 5.pdf            original export
├── Lesson 5 - Quadratic Forms and the F Test (LaTeX).pdf   built from lesson05.tex
├── Lesson 6.pdf            original export
├── Lesson 6 - F Test via RSS and Restricted Least Squares (LaTeX).pdf   built from lesson06.tex
├── Lesson 7.pdf            original export
├── Lesson 7 - LM Test, Testing Principles and GLS (LaTeX).pdf   built from lesson07.tex
├── Lesson 8.pdf            original export
├── Lesson 8 - Heteroskedasticity (WLS) and AR(1) Errors (GLS) (LaTeX).pdf   built from lesson08.tex
├── Lesson 8 (LaTeX).pdf    older render of Lesson 8 (pre-revision), kept
├── Lesson 9.pdf            original export
├── Lesson 9 - Cochrane-Orcutt, Stochastic Regressors and Consistency (LaTeX).pdf   built from lesson09.tex
├── Lesson 10.pdf           original export
├── Lesson 10 - Orders of Magnitude, Asymptotics of OLS and Nonlinear Least Squares (LaTeX).pdf   built from lesson10.tex
├── Lesson 11.pdf           original export
├── Lesson 11 - Nonlinear Least Squares and the Gauss-Newton Regression (LaTeX).pdf   built from lesson11.tex
├── Lesson 12.pdf           original export
├── Lesson 12 - Asymptotics of NLS and Hypothesis Testing with the GNR (LaTeX).pdf   built from lesson12.tex
├── Lesson 12 Supplement - NLS Asymptotics Derivations (LaTeX).pdf   built from lesson12_supplement.tex
├── Lesson 14.pdf           original export
├── Lesson 14 - GNR Tests with AR(1) Errors, Jacobians and the Idea of ML (LaTeX).pdf   built from lesson14.tex
├── MLE1.pdf, MLE2.pdf      photographed instructor handouts (I) and (II) on maximum likelihood
├── MLE 1 - Maximum Likelihood Estimation (LaTeX).pdf   built from mle1.tex
├── MLE 2 - More on Maximum Likelihood - Covariance Estimators and Jacobian Terms (LaTeX).pdf   built from mle2.tex
├── MLE5.pdf                photographed handout (V): Hausman test, LM by artificial regression
├── MLE 5 - Hausman Specification Testing and the LM Test by Artificial Regression (LaTeX).pdf   built from mle5.tex
├── GMM after MLE.... with a little bit of IV.pdf   class notes on IV/2SLS + photographed handout "Lecture on GMM"
├── GMM 1 - Generalized Method of Moments - GIV, GMM as GLS, Asymptotics and the Sargan-Hansen Test (LaTeX).pdf   built from gmm1.tex
├── Metrics HW1/
│   ├── HW 1.pdf                           built from hw01.tex  (Assignment #1, ECON*6140)
│   ├── HW 1 solution for question 1.tex/.pdf   Q1 solution; source lives here, uses ../LaTeX/metricsstyle
│   ├── HW1.ipynb, requirements.txt, .venv/   Python env (kernel "Python (Metrics HW1)")
└── LaTeX/
    ├── metricsstyle.sty        THE FORMAT — edit here, not in the lessons
    ├── lesson01.tex
    ├── lesson02.tex
    ├── lesson03.tex
    ├── lesson04.tex            FWL, omitted/irrelevant variables, Rβ = r
    ├── lesson05.tex            χ² quadratic forms, spectral decomposition, F test of Rβ = r
    ├── lesson06.tex            F as RSSR vs USSR, restricted least squares, bias/variance of b*
    ├── lesson07.tex            Wald vs LM, principles of testing, GLS with u ~ N(0, σ²Ω)
    ├── lesson08.tex            heteroskedasticity/WLS, AR(1) errors and their Ω, GLS with known ρ, AR(2)
    ├── lesson09.tex            Cochrane–Orcutt (unknown ρ), stochastic X, E(u|X) vs E(X'u), plim/LLN/CLT, bias vs consistency
    ├── lesson10.tex            O(n)/o(n), X'X/n → Σ_XX, consistency and √n-normality of b, nonlinear least squares
    ├── lesson11.tex            NLS first-order conditions, X(β), Gauss–Newton regression and iteration, asymptotics of NLS
    ├── lesson12.tex            NLS residual variance and asymptotic normality, GNR covariance, restricted GNR tests
    ├── lesson12_supplement.tex derivation supplement: derivative of the FOC, √n-scaled step, Slutsky (built by hand)
    ├── lesson13.tex            restricted GNR tests, test for AR(1) errors, GNR under σ²Ω
    ├── lesson14.tex            GNR tests with AR(1) errors (ρ known / unknown), Jacobian of a transformation, idea of ML
    ├── mle1.tex                handout MLE I: notation, invariance, asymptotic normality, information matrix equality
    ├── mle2.tex                handout MLE II: Cramér–Rao, covariance estimators/OPG, normal NLS as ML, Jacobians, Box–Cox
    ├── mle5.tex                handout MLE V: Hausman contrast test, LM = ESS = nR² from an artificial regression, test for AR(1) errors
    ├── gmm1.tex                IV/2SLS (class) + handout GMM: orthogonality conditions, GMM = GLS on W'y, GIV/IV/OLS/GLS as special cases, asymptotics, Sargan–Hansen
    ├── hw01.tex                Assignment #1, ECON*6140, due 2026-10-14
    ├── lessonXX_template.tex   copy this to start a new lesson
    ├── extract_pages.py        render a handwritten PDF to PNGs for reading
    └── build.sh                builds every lesson and problem set, copies PDFs up
```

## Add a new lesson

```bash
cd "LaTeX"
cp lessonXX_template.tex lesson02.tex
$EDITOR lesson02.tex          # fill in \lessonheader and the body
./build.sh                    # -> ../Lesson 2 - <title> (LaTeX).pdf   (+ lesson02.pdf)
```

For a problem set, copy `hw01.tex` to `hwNN.tex`, write `\hwheader{N}{term}{due}`
and keep the `transcriptnotes` block; `build.sh` then drops `HW N.pdf` into `../Metrics HWN/`
(or `../` if that folder does not exist).
Solution write-ups live in `../Metrics HWN/` next to their PDF; build one there
with `latexmk -pdf "HW 1 solution for question 1.tex"`.

`build.sh` rebuilds everything, so use it rather than calling `pdflatex` by hand;
that keeps the numbering, the file names and the copied output consistent.
Supplements that should not be numbered as a new lesson (e.g.
`lesson12_supplement.tex`) are outside `build.sh`'s `lessonNN.tex` glob; build
one with `latexmk -pdf lesson12_supplement.tex`.

## The format

* File name: the first line of each lesson is `%% title: <short title>`; `build.sh`
  names the output `Lesson N - <short title> (LaTeX).pdf` (no line: `Lesson N (LaTeX).pdf`).
* `\documentclass[11pt]{article}` + `\usepackage{metricsstyle}` and nothing else in
  the preamble. Paper A4, 2.5 cm margins, numbered sections, bold `\topic{}` /
  `\runin{}` headings.
* Title block: `\lessonheader{<lesson number>}{<subtitle>}{<date or nothing>}`
  — put it after `\begin{document}`.
* Problem sets: `\hwheader{<assignment number>}{<term>}{<due date>}`, then one
  `\question{(N)}` per question.
* Lists: `flatlist` (bullets, also `\item[(a)]` for lettered parts) and `flatnum`
  (numbers).
* Maths: `amsmath`/`amssymb` are loaded. Shorthands: `\R`, `\E` (expectation),
  `\Var`, `\Cov`, `\rank`, `\xT` (transpose). Matrices with `bmatrix`. Numbered
  equations print their own tag with `\begin{equation}\tag{1}`.
* Diagrams: `\ecaxes{x-max}{y-max}` plus the TikZ styles `budget`, `bundle`,
  `ecnode`.
* Every file ends with a `transcriptnotes` block: small print listing what was
  corrected in the transcription and anything illegible, plus a page-by-page map
  back to the original. Keep it — it is the audit trail.
* Reading photographed pages: iPhone exports are often landscape with the page
  on its side and named `.png` while actually being HEIC. Fix both before OCR:

  ```bash
  sips -s format jpeg in.png --out work.jpg   # HEIC masquerading as PNG
  sips -r 90 work.jpg --out work_r90.jpg      # undo the rotation
  tesseract work_r90.jpg - --psm 6            # printed sheets read cleanly
  ```

  `extract_pages.py` is the equivalent for handwritten PDF exports.

This style is the sibling of `microstyle.sty` in `micro 1 class note*/LaTeX/`
(same design, different course line). If you restyle one, restyle the other.
