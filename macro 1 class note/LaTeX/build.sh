#!/usr/bin/env bash
# Build solow.tex (lectures 1-3 combined) in this folder and drop the finished PDFs one level
# up, next to the lecture slide folder, as "Solow Model - Lectures 1-3 (LaTeX).pdf".
set -euo pipefail
cd "$(dirname "$0")"

if [ -x /Library/TeX/texbin/latexmk ]; then
  LATEXMK=/Library/TeX/texbin/latexmk
else
  LATEXMK=$(command -v latexmk)
fi
[ -n "$LATEXMK" ] || { echo "latexmk not found (install TeX Live / MacTeX)" >&2; exit 1; }

shopt -s nullglob
for f in solow.tex; do
  echo "== building ${f}"
  "$LATEXMK" -pdf -interaction=nonstopmode -halt-on-error -silent "$f"
  cp -f solow.pdf "../Solow Model - Lectures 1-3 (LaTeX).pdf"
  echo "   -> ../Solow Model - Lectures 1-3 (LaTeX).pdf"
done

# remove .aux/.log/.fls/.fdb_latexmk, keep the PDFs
"$LATEXMK" -c -silent >/dev/null 2>&1 || true

echo "done."
