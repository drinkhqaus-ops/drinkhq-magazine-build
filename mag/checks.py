"""Publish checks for DrinkHQ Magazine. Run from mag/ after the build.

Fails (exit 1) if any check fails, and writes checks-report.md for the build summary.
"""
import glob, os, re, sys
import cv2, numpy as np, pymupdf
from playwright.sync_api import sync_playwright

# Words that must never appear in a published issue (withdrawn products, dropped venues, stale notes).
BANNED = [
    (r'\bRiche\b(?!lieu)', 'Riche (Traveller replaced by Caretaker’s Cottage)'),
    (r'Full Series', 'Full Series Package (withdrawn 25 Oct 2026)'),
    (r'Judge’?s Table|Judge\'s Table', 'Judge’s Table (withdrawn ticket)'),
    (r'All-Access Pass', 'All-Access Pass (withdrawn ticket)'),
    (r'\b1902\b', 'premium-rate 1902 number'),
    (r'not built yet', 'unfinished-page note'),
    (r'10,000 copies', '10,000-copies claim (dropped 25 Oct 2026)'),
    (r'169 Water St', 'old Water St address'),
]
PRESS_MAX = 10 * 1024 * 1024

results = []
def check(name, ok, detail=''):
    results.append((name, ok, detail))
    print(('PASS ' if ok else 'FAIL ') + name + (f' — {detail}' if detail else ''))

# 1. Text overflow on any page
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for f in sorted(glob.glob('out/DrinkHQ-Magazine_Issue-01_*pp_Official-Record.html')):
        p = b.new_page(viewport={'width': 1400, 'height': 900})
        p.goto('file://' + os.path.abspath(f)); p.wait_for_timeout(1500)
        ov = p.evaluate("""()=>[...document.querySelectorAll('.page')].map(pg=>{const s=pg.querySelector('.safe');
            return s&&(s.scrollHeight>s.clientHeight+2||s.scrollWidth>s.clientWidth+2)?pg.dataset.page:null}).filter(Boolean)""")
        ed = re.search(r'(\d+pp)', f).group(1)
        check(f'No overflowing text ({ed})', not ov, 'pages ' + ', '.join(ov) if ov else '')
        p.close()
    b.close()

for pdf in sorted(glob.glob('pdf/DrinkHQ-Magazine-Issue-01-*October-2026.pdf')):
    name = os.path.basename(pdf)
    d = pymupdf.open(pdf)
    text = ''.join(pg.get_text() for pg in d)
    # 2. Banned words
    hits = [label for pat, label in BANNED if re.search(pat, text)]
    check(f'No withdrawn or stale content ({name})', not hits, '; '.join(hits))
    # 3. QR codes decode
    found = []
    for pg in d:
        if 'scan' not in pg.get_text().lower() and 'qr' not in pg.get_text().lower():
            continue
        pix = pg.get_pixmap(dpi=300)
        im = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)[:, :, :3]
        ok, dec, _, _ = cv2.QRCodeDetector().detectAndDecodeMulti(cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
        if ok:
            found += [x for x in dec if x]
    check(f'QR codes scan ({name})', len(found) > 0, ', '.join(sorted(set(found))))
    # 4. Press PDF size
    if 'Press' in name:
        sz = os.path.getsize(pdf)
        check(f'Press PDF under 10 MB ({name})', sz < PRESS_MAX, f'{sz/1048576:.1f} MB')

with open('checks-report.md', 'w') as fh:
    fh.write('## Magazine publish checks\n\n')
    for n, ok, det in results:
        mark = 'PASS' if ok else 'FAIL'
        extra = (' - ' + det) if det else ''
        fh.write(f'- {mark}: {n}{extra}\n')

sys.exit(0 if all(ok for _, ok, _ in results) else 1)
