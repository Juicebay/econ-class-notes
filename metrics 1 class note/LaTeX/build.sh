#!/usr/bin/env bash
# Build every lessonNN.tex in this folder and drop the finished PDFs one level
# up, next to the original handwritten export, as "Lesson N (LaTeX).pdf".
set -euo pipefail
cd "$(dirname "$0")"

if [ -x /Library/TeX/texbin/latexmk ]; then
  LATEXMK=/Library/TeX/texbin/latexmk
else
  LATEXMK=$(command -v latexmk)
fi
[ -n "$LATEXMK" ] || { echo "latexmk not found (install TeX Live / MacTeX)" >&2; exit 1; }

shopt -s nullglob
for f in lesson[0-9][0-9].tex hw[0-9][0-9].tex hw[0-9][0-9]q[0-9]*.tex; do
  echo "== building ${f}"
  "$LATEXMK" -pdf -interaction=nonstopmode -halt-on-error -silent "$f"
  n=$(printf '%s' "$f" | sed -E 's/^[a-z]*0*([0-9]+).*\.tex$/\1/')
  # problem sets go into "../Metrics HW N/" when that folder exists
  hwdir=".."; [ -d "../Metrics HW${n}" ] && hwdir="../Metrics HW${n}"
  case "$f" in
    lesson*) out="../Lesson ${n} (LaTeX).pdf" ;;
    hw*q*)   q=$(printf '%s' "$f" | sed -E 's/^hw[0-9]+q0*([0-9]+)\.tex$/\1/')
             out="${hwdir}/HW ${n} solution for question ${q}.pdf" ;;
    hw*)     out="${hwdir}/HW ${n}.pdf" ;;
  esac
  cp -f "${f%.tex}.pdf" "$out"
  echo "   -> $out"
done

# remove .aux/.log/.fls/.fdb_latexmk, keep the PDFs
"$LATEXMK" -c -silent >/dev/null 2>&1 || true

echo "done."
