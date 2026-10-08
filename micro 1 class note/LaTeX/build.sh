#!/usr/bin/env bash
# Build every lessonNN.tex in this folder and drop the finished PDFs one level
# up, next to the original handwritten exports, as
# "Lesson NN - <shortname> (LaTeX).pdf", where <shortname> is read from the
# "%% shortname: ..." line at the top of each lessonNN.tex.
set -euo pipefail
cd "$(dirname "$0")"

if [ -x /Library/TeX/texbin/latexmk ]; then
  LATEXMK=/Library/TeX/texbin/latexmk
else
  LATEXMK=$(command -v latexmk)
fi
[ -n "$LATEXMK" ] || { echo "latexmk not found (install TeX Live / MacTeX)" >&2; exit 1; }

shopt -s nullglob
for f in lesson[0-9][0-9].tex; do
  echo "== building ${f}"
  "$LATEXMK" -pdf -interaction=nonstopmode -halt-on-error -silent "$f"
  n=$(printf '%s' "$f" | sed -E 's/^lesson([0-9]+)\.tex$/\1/')
  name=$(sed -n 's/^%% shortname: *//p' "$f" | head -n 1)
  if [ -n "$name" ]; then out="Lesson ${n} - ${name} (LaTeX).pdf"; else out="Lesson ${n} (LaTeX).pdf"; fi
  cp -f "${f%.tex}.pdf" "../${out}"
  echo "   -> ../${out}"
done

# remove .aux/.log/.fls/.fdb_latexmk, keep the PDFs
"$LATEXMK" -c -silent >/dev/null 2>&1 || true

echo "done."
