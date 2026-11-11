#!/usr/bin/env bash
# Build every *.tex note in this folder and copy the PDFs one level up as
# "<STEM> - <shortname> (LaTeX).pdf" (shortname from the "%% shortname:" line).
set -euo pipefail
cd "$(dirname "$0")"
LATEXMK=/Library/TeX/texbin/latexmk; [ -x "$LATEXMK" ] || LATEXMK=$(command -v latexmk)
shopt -s nullglob
for f in *.tex; do
  echo "== building ${f}"
  "$LATEXMK" -pdf -interaction=nonstopmode -halt-on-error -silent "$f"
  name=$(sed -n 's/^%% shortname: *//p' "$f" | head -n 1)
  out="${f%.tex} - ${name} (LaTeX).pdf"
  cp -f "${f%.tex}.pdf" "../${out}"; echo "   -> ../${out}"
done
"$LATEXMK" -c -silent >/dev/null 2>&1 || true
echo done.
