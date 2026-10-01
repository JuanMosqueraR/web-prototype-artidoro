"""2026-10-01: a direct visit to a PDP no longer downloads the home hero video; it is requested when the home is shown.
Python Playwright, Chromium, DPR 1, production build over HTTP. Writes only this dated directory (checks.json).
Usage: ARTIDORO_REVIEW_URL=http://127.0.0.1:4192 python qa/2026-10-01-hero-pdp/verify.py
"""
from pathlib import Path
import json, os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
URL = os.environ.get('ARTIDORO_REVIEW_URL', 'http://127.0.0.1:4192').rstrip('/')
checks = []


def check(name, ok, detail=None):
    checks.append({'name': name, 'passed': bool(ok), 'detail': detail})
    if not ok:
        print('FAIL', name, detail, flush=True)


with sync_playwright() as p:
    b = p.chromium.launch(); version = b.version
    for name, w, h in [('desktop', 1440, 900), ('mobile', 390, 844)]:
        mob = w <= 760
        hero = 'hero-mobile.mp4' if mob else 'hero-desktop.mp4'
        for route in ['#producto-amazonas', '#producto-ahorrador']:
            ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, is_mobile=mob, has_touch=mob); pg = ctx.new_page(); reqs = []; errs = []
            pg.on('request', lambda r: reqs.append(r.url.split('/')[-1]) if r.url.endswith('.mp4') or '/hero-seq/' in r.url else None)
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto(URL + '/' + route); pg.wait_for_timeout(4500)
            pg.evaluate('scrollBy(0, 700)'); pg.wait_for_timeout(1500)
            on_pdp = list(reqs)
            check(f'{name} {route}: no hero video or image sequence requested while on the PDP', not on_pdp, on_pdp)
            pg.click(f'{route} [data-product-back]'); pg.wait_for_timeout(800)
            pg.evaluate('scrollTo(0, 0)')
            try:
                pg.wait_for_function("document.querySelector('#direction-a').dataset.media === 'video'", timeout=15000); ok = True
            except Exception:
                ok = False
            check(f'{name} {route}: back on the home, the hero requests its own video and plays it', ok and hero in reqs and not errs, [reqs, errs])
            ctx.close()
    b.close()

json.dump({'chromium': version, 'url': URL, 'checks': checks}, open(ROOT / 'checks.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(sum(c['passed'] for c in checks), '/', len(checks))
