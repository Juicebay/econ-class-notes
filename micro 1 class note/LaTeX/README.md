# Micro 1 class notes — LaTeX format

Typeset versions of the handwritten lesson exports, in one fixed format.

```
micro 1 class note/
├── 00 Course Info/              Schedule, syllabus
├── 01 Labs/                     instructor lab slides + handouts (Lab 02, 05, 08, 12, 17)
├── 02 Lectures/
│   └── Lesson NN - <shortname>/ "... (handwritten).pdf" + "... (LaTeX).pdf"
├── 03 Assignments/              HW1, HW2
├── 04 Exams/
├── 05 Textbooks & Supplements/  MWG, Munoz-Garcia, Econ709
└── LaTeX/
    ├── microstyle.sty          THE FORMAT — edit here, not in the lessons
    ├── lesson01.tex … lesson18.tex
    ├── lessonXX_template.tex   copy this to start a new lesson
    ├── extract_pages.py        render a handwritten export to PNGs to read from
    └── build.sh                builds every lesson into ../02 Lectures/Lesson NN - <shortname>/
```

## Add a new lesson

```bash
cd "LaTeX"
cp lessonXX_template.tex lesson19.tex
$EDITOR lesson19.tex          # fill in the shortname line, \lessonheader and the body
./build.sh                    # -> ../02 Lectures/Lesson 19 - <shortname>/Lesson 19 - <shortname> (LaTeX).pdf
```

`build.sh` rebuilds all lessons, so use it rather than calling `pdflatex` by hand;
that keeps the numbering, the file names and the copied output consistent.

## The format

* Line 1 is `%% shortname: <Short Topic Title>`; `build.sh` uses it to name the
  output PDF `Lesson NN - <shortname> (LaTeX).pdf`. Keep it free of `/` and `'`.
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
