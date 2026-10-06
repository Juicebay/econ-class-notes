# Metrics 1 class notes — LaTeX format

Typeset versions of the handwritten lesson exports and of the problem sets, in
one fixed format.

```
metrics 1 class note*/
├── Lesson 1.pdf            original export
├── Lesson 1 (LaTeX).pdf    built from lesson01.tex
├── lesson 2.pdf            original export
├── Lesson 2 (LaTeX).pdf    built from lesson02.tex
├── Class 3.pdf             original export
├── Class 3 (LaTeX).pdf     copy of Lesson 3 (LaTeX).pdf
├── Lesson 3 (LaTeX).pdf    built from lesson03.tex
├── Lesson 4.pdf            original export
├── Lesson 4 (LaTeX).pdf    built from lesson04.tex
├── lecture 5.pdf           original export
├── Lesson 5 (LaTeX).pdf    built from lesson05.tex
├── Lesson 6.pdf            original export
├── Lesson 6 (LaTeX).pdf    built from lesson06.tex
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
./build.sh                    # -> ../Lesson 2 (LaTeX).pdf   (+ lesson02.pdf)
```

For a problem set, copy `hw01.tex` to `hwNN.tex`, write `\hwheader{N}{term}{due}`
and keep the `transcriptnotes` block; `build.sh` then drops `HW N.pdf` into `../Metrics HWN/`
(or `../` if that folder does not exist).
Solution write-ups live in `../Metrics HWN/` next to their PDF; build one there
with `latexmk -pdf "HW 1 solution for question 1.tex"`.

`build.sh` rebuilds everything, so use it rather than calling `pdflatex` by hand;
that keeps the numbering, the file names and the copied output consistent.

## The format

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
