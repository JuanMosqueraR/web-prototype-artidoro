"""Prepare the link-preview image (og:image) of the home: public/assets/og-share.jpg, 1200 x 630.

Derived from the real page, not drawn: a screenshot of the hero in its final, static state (?motion=off) at the
Open Graph size, so it shows exactly what a visitor sees, including the «Escena conceptual generada para esta demo.»
notice. Requires Playwright (Python, Chromium) and Pillow. Needs a served build of the site:

    python scripts/prepare-og-image.py http://127.0.0.1:4192

Reproducible apart from the (non-deterministic) generated footage the page itself shows.
"""
from pathlib import Path
import io
import sys
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:4192').rstrip('/')
OUT = ROOT / 'public/assets/og-share.jpg'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1200, 'height': 630}, device_scale_factor=1)
    page.goto(URL + '/?motion=off')
    page.evaluate('document.fonts.ready')
    page.wait_for_function("document.querySelector('.hs-end img')?.complete && document.querySelector('.hs-end img').naturalWidth > 0", timeout=20000)
    page.wait_for_timeout(800)
    png = page.screenshot()
    browser.close()

image = Image.open(io.BytesIO(png)).convert('RGB')
assert image.size == (1200, 630), image.size
image.save(OUT, quality=88, optimize=True, progressive=True)
print(OUT.name, image.size, OUT.stat().st_size)
