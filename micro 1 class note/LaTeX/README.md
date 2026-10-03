# Micro 1 class notes — LaTeX format

Typeset versions of the handwritten lesson exports, in one fixed format.

```
micro 1 class note*/
├── Lesson 1.pdf  Lesson 3.pdf  lesson 4.pdf  Lesson 6.pdf  Lesson 7.pdf   original exports
├── Lesson 1 (LaTeX).pdf      built from lesson01.tex
├── Lesson 3 (LaTeX).pdf      built from lesson03.tex
├── Lesson 4 (LaTeX).pdf      built from lesson04.tex
├── Lesson 6 (LaTeX).pdf      built from lesson06.tex
├── Lesson 7 (LaTeX).pdf      built from lesson07.tex
└── LaTeX/
    ├── microstyle.sty          THE FORMAT — edit here, not in the lessons
    ├── lesson01.tex  lesson03.tex  lesson04.tex  lesson06.tex  lesson07.tex
    ├── lessonXX_template.tex   copy this to start a new lesson
    ├── extract_pages.py        render a handwritten export to PNGs to read from
    └── build.sh                builds every lesson and copies the PDFs up
```

## Add a new lesson

```bash
cd "LaTeX"
cp lessonXX_template.tex lesson04.tex
$EDITOR lesson04.tex          # fill in \lessonheader and the body
./build.sh                    # -> ../Lesson 4 (LaTeX).pdf   (+ lesson04.pdf)
```

`build.sh` rebuilds all lessons, so use it rather than calling `pdflatex` by hand;
that keeps the numbering, the file names and the copied output consistent.

## The format

* `\documentclass[11pt]{article}` + `\usepackage{microstyle}` and nothing else in
  the preamble. Paper A4, 2.5 cm margins, numbered sections, bold `\topic{}` /
  `\runin{}` headings.
* Title block: `\lessonheader{<lesson number>}{<subtitle>}{<date or nothing>}`.
* Lists: `flatlist` (bullets) and `flatnum` (numbers).
* Maths: `amsmath`/`amssymb` are loaded; `\R` is `\mathbb{R}`, `\pd{f}{x}` is a
  partial derivative.
* Diagrams: `\ecaxes{x-max}{y-max}` plus the TikZ styles `budget`, `bundle`,
  `ecnode`.
* Every lesson ends with a `transcriptnotes` block: small print listing what was
  corrected in the transcription and anything illegible. Keep it — it is the audit
  trail back to the handwritten original.

Because the style lives only in `microstyle.sty`, changing it once restyles every
lesson on the next build.
