#!/usr/bin/env python3
"""Render a handwritten / scanned PDF into PNG strips you can read page by page.

Usage:
    python3 extract_pages.py "<source.pdf>" [outdir]

Writes, for every page:
    <outdir>/<stem>_p<N>.png       the whole page at --dpi
    <outdir>/<stem>_p<N>_top.png   upper half at --dpi
    <outdir>/<stem>_p<N>_bot.png   lower half at --dpi

Half-page strips keep the resolution high enough to read handwriting; read the
full page first, then re-render a strip (or pass --clip) for anything illegible.
Note that note-app exports (GoodNotes, Notability, ...) usually carry a garbled
OCR text layer -- useful as a cross-check, never as the transcription.
"""
import argparse
import os

import fitz  # PyMuPDF


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("outdir", nargs="?", default="renders")
    ap.add_argument("--dpi", type=int, default=140, help="full-page dpi (default 140)")
    ap.add_argument("--strip-dpi", type=int, default=260, help="half-page dpi (default 260)")
    ap.add_argument("--clip", nargs=4, type=float, metavar=("X0", "Y0", "X1", "Y1"),
                    help="instead of the whole document, render only this box on the given page")
    ap.add_argument("--page", type=int, default=1, help="1-based page for --clip")
    args = ap.parse_args()

    doc = fitz.open(args.pdf)
    os.makedirs(args.outdir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(args.pdf))[0]

    if args.clip:
        page = doc[args.page - 1]
        # clip values are fractions of the page when <= 1, else points
        r = page.rect
        x0, y0, x1, y1 = args.clip
        if x1 <= 1 and y1 <= 1:
            x0, x1 = x0 * r.width, x1 * r.width
            y0, y1 = y0 * r.height, y1 * r.height
        out = os.path.join(args.outdir, f"{stem}_p{args.page}_clip.png")
        page.get_pixmap(dpi=520, clip=fitz.Rect(x0, y0, x1, y1)).save(out)
        print(out)
        return

    print(f"{args.pdf}: {doc.page_count} pages")
    for i, page in enumerate(doc):
        n = i + 1
        page.get_pixmap(dpi=args.dpi).save(
            os.path.join(args.outdir, f"{stem}_p{n}.png"))
        h = page.rect.height
        w = page.rect.width
        for tag, (a, b) in (("top", (0.0, 0.5)), ("bot", (0.5, 1.0))):
            page.get_pixmap(dpi=args.strip_dpi,
                            clip=fitz.Rect(0, h * a, w, h * b)).save(
                os.path.join(args.outdir, f"{stem}_p{n}_{tag}.png"))
        words = page.get_text("words")
        print(f"  p{n}: {len(words)} OCR word(s) -> {stem}_p{n}.png")
    print(f"-> {args.outdir}/")


if __name__ == "__main__":
    main()
