"""L31, adjustments after the user's iPhone test (2026-10-01): no focus ring on the PDP title focused by script,
and the mobile «Del cafetal a tu taza» carousel keeps its 22 px side margin when it snaps.
Python Playwright, Chromium, DPR 1, production build served over HTTP. Writes only this dated directory.
Usage: ARTIDORO_REVIEW_URL=http://127.0.0.1:4192 python qa/2026-10-01-pdp-ajustes/verify.py
"""
from pathlib import Path
import json, os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
CAP = ROOT / 'after'; CAP.mkdir(exist_ok=True)
URL = os.environ.get('ARTIDORO_REVIEW_URL', 'http://127.0.0.1:4192').rstrip('/')
checks = []


def check(name, ok, detail=None):
    checks.append({'name': name, 'passed': bool(ok), 'detail': detail})
    if not ok:
        print('FAIL', name, detail, flush=True)


with sync_playwright() as p:
    b = p.chromium.launch(); version = b.version
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True); pg = ctx.new_page()
    pg.goto(URL + '/?motion=off'); pg.wait_for_timeout(1000)
    pg.tap('.hero-peru .buy-button'); pg.wait_for_timeout(900)
    title = pg.evaluate("[document.activeElement.id, getComputedStyle(document.activeElement).outlineStyle]")
    check('PDP title receives focus on open (screen readers) without a focus ring', title == ['product-title', 'none'], title)
    pg.keyboard.press('Tab'); pg.wait_for_timeout(200)
    nxt = pg.evaluate("getComputedStyle(document.activeElement).outlineStyle")
    check('the next control keeps its keyboard focus ring', nxt != 'none', nxt)
    pg.screenshot(path=str(CAP / 'mobile-title.png'))
    for route in ['#producto-amazonas', '#producto-ahorrador']:
        pg.goto(URL + '/?motion=off' + route); pg.wait_for_timeout(900)
        sel = f'{route} .pdp-steps'
        pg.evaluate(f"document.querySelector('{sel}').scrollIntoView()"); pg.wait_for_timeout(300)
        first = pg.evaluate(f"Math.round(document.querySelector('{sel} li').getBoundingClientRect().left)")
        pg.screenshot(path=str(CAP / f'mobile-steps-{route[10:]}.png'))
        pg.evaluate(f"document.querySelector('{sel}').scrollTo({{left: 300, behavior: 'smooth'}})"); pg.wait_for_timeout(900)
        snapped = pg.evaluate(f"[...document.querySelectorAll('{sel} li')].map(l => Math.round(l.getBoundingClientRect().left))")
        check(f'{route} mobile steps: first card at the 22 px margin and snapping aligns to it', first == 22 and 22 in snapped, [first, snapped])
    ctx.close(); b.close()

json.dump({'chromium': version, 'url': URL, 'checks': checks}, open(ROOT / 'checks.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(sum(c['passed'] for c in checks), '/', len(checks))
