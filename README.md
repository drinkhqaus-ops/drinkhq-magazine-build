# DrinkHQ Magazine build — DrinkHQ Group

The files that produce DrinkHQ Magazine Issue 01 (16 and 32 pages) and the magazine media kit.
Saved from the working session of 26 Oct 2026. The live websites are always the master for
anything on a server (drinkhqmedia.com plugins, DrinkHQ Ops); the copy of the Contribute plugin
here is for reference only.

## Needs
Python 3 with pymupdf, segno, Pillow, opencv-python; Node with Playwright (Chromium); Ghostscript.

## Magazine (folder mag/)
1. `python3 gen.py` — builds the screen/editable HTML for 16pp and 32pp into out/
2. `python3 shot.py` — page-spread previews into qa/ and an overflow check
3. `DHQ_IMGDIR=web_print DHQ_OUTDIR=out_press python3 gen.py` — print-resolution HTML
4. `python3 makepdf.py render` — press PDF (CMYK, 3 mm bleed, under 10 MB) and email PDF into pdf/
5. `python3 makecanva.py` — Canva PDFs (4 x 8 pages) into canva/
6. `python3 canvas.py 32 blobs32.json <outdir> "DrinkHQ Magazine Issue 01 · 32pp"` — design-canvas pages
   for the mock-up artifact (blob ids map images to that artifact's asset store; 16pp uses blobs16.json)

Page content lives in gen.py (P[...] page lists for 16pp and 32pp); styles in style.css.
Images: web/ (screen), web_print/ (print). Images extracted from the archive: img/. The original archive PDFs (Drink 2007, the legacy media kit, the Official Record) are kept in Drive, not in this package.

## Media kit (folder kit/)
`python3 kit.py`, then `python3 render.py` and `python3 final.py` (CMYK + trim box).
Reads images from ../mag/web and kit/pg.

## Restoring
The package is split into several zip files, each a normal zip. Unzip them all into the same folder; together they rebuild the drinkhq-magazine-build folder.

## Publishing from GitHub
Actions → "Publish magazine issue" → Run workflow. The build makes every PDF, runs the checks
(no overflowing text, no withdrawn or stale content, QR codes scan, press PDF under 10 MB) and keeps
the files for 30 days on the run page. If any check fails, the run is marked failed and says which.
The Ops "Publish issue" button starts the same run. Checks live in mag/checks.py.
