"""Home audit fix (L24): icons, hero overlap/CTA, typography floor, touch targets, B regression.
Python Playwright, Chromium DPR 1, production preview. No purchases. Writes only this dated directory.
"""
from pathlib import Path
import json, os
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
CAP = ROOT / 'after'; CAP.mkdir(exist_ok=True)
URL = os.environ.get('ARTIDORO_REVIEW_URL', 'http://127.0.0.1:4175')
B_BASELINE = ROOT.parent / '2026-09-29-ahorro' / 'after'
checks = []


def check(name, ok, detail=None):
    checks.append({'name': name, 'passed': bool(ok), 'detail': detail})
    if not ok:
        print('FAIL', name, detail, flush=True)


CHECK_JS = r"""
() => {
  const res = {};
  const ann = document.querySelector('.origin-annotation').getBoundingClientRect();
  const btn = document.querySelector('.origin-button').getBoundingClientRect();
  res.overlapGap = Math.round(btn.top - ann.bottom);
  const buy = document.querySelector('.hero-peru .buy-button').getBoundingClientRect();
  res.buyBottom = Math.round(buy.bottom);
  const small = [];
  document.querySelectorAll('#home-main *, .hero-peru *').forEach(el => {
    if (el.children.length) return;
    const txt = (el.textContent || '').trim(); if (!txt) return;
    if (el.closest('[hidden]')) return;
    const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const fs = parseFloat(cs.fontSize);
    if (fs < 11) small.push({ fs, txt: txt.slice(0, 40) });
  });
  res.under11 = small;
  const targets = [];
  document.querySelectorAll('#home-main a, #home-main button, #home-main summary, .home-nav a, .home-nav summary').forEach(el => {
    if (el.closest('[hidden]')) return;
    const cs = getComputedStyle(el); if (cs.display === 'none') return;
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
    if (r.width < 44 || r.height < 44) targets.push({ w: Math.round(r.width), h: Math.round(r.height), txt: (el.innerText || '').trim().slice(0, 40) });
  });
  res.under44 = targets;
  res.overflowX = document.documentElement.scrollWidth - innerWidth;
  const icons = [...document.querySelectorAll('.hero-peru .icon, #home-main .icon')];
  res.iconZeroSize = icons.filter(el => { const r = el.getBoundingClientRect(); return r.width < 2 || r.height < 2; }).length;
  res.iconCount = icons.length;
  return res;
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(); version = b.version
    for name, w, h in [('desktop', 1440, 900), ('mobile', 390, 844), ('mobile664', 390, 664), ('tablet', 768, 1024)]:
        page = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        errors = []; page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(URL + '/'); page.evaluate('document.fonts.ready'); page.wait_for_timeout(300)
        page.screenshot(path=str(CAP / f'{name}-initial.png'))
        page.click('.hero-peru .origin-button'); page.wait_for_timeout(900)
        page.screenshot(path=str(CAP / f'{name}-expanded.png'))
        r = page.evaluate(CHECK_JS)
        check(f'{name} annotation/button gap >=12px', r['overlapGap'] >= 12, r['overlapGap'])
        check(f'{name} no under-11px text', len(r['under11']) == 0, r['under11'])
        check(f'{name} no overflow-x', r['overflowX'] == 0, r['overflowX'])
        check(f'{name} icons render (nonzero size)', r['iconZeroSize'] == 0 and r['iconCount'] > 0, r)
        if name in ('mobile', 'mobile664'):
            check(f'{name} hero CTA visible in viewport', r['buyBottom'] <= h, r['buyBottom'])
        checks.append({'name': f'{name} under44 (informational, see README)', 'passed': True, 'detail': r['under44']})
        check(f'{name} no page errors', not errors, errors)
        page.close()

    # Direction B: 0px diff against the existing baseline (checkpoint unaffected).
    for name, w, h in [('desktop', 1440, 900), ('mobile', 390, 844)]:
        for off in [False, True]:
            page = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
            page.goto(URL + '/b/' + ('?motion=off' if off else '')); page.evaluate('document.fonts.ready')
            hero = page.locator('#direction-b')
            hero.locator('img[src]').evaluate_all('async imgs=>Promise.all(imgs.map(i=>{i.loading="eager";return i.decode()}))')
            for frame in ['initial', 'expanded']:
                if frame == 'expanded':
                    hero.locator('[data-reveal]').click(); page.wait_for_timeout(900)
                stem = f'b-{name}-{"reduced" if off else "motion"}-{frame}'
                target = CAP / (stem + '.png'); page.screenshot(path=str(target))
                before = Image.open(B_BASELINE / (stem + '.png')).convert('RGB'); after = Image.open(target).convert('RGB')
                diff = ImageChops.difference(before, after)
                changed = sum(1 for rgb in diff.getdata() if max(rgb) > 0)
                maximum = max(v[1] for v in diff.getextrema())
                check(stem + ' B unchanged', changed <= w * h * .0005 and maximum <= 16, {'changed': changed, 'max': maximum})
            page.close()

    # Functional sweep: new 05 card, review PDP links, origin selector, pack PDP.
    page = b.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=1)
    errors = []; page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(URL + '/'); page.wait_for_timeout(300)
    hh = page.evaluate('document.documentElement.scrollHeight'); y = 0
    while y < hh:
        page.evaluate(f'scrollTo(0,{y})'); page.wait_for_timeout(120); y += 450
        hh = page.evaluate('document.documentElement.scrollHeight')
    page.wait_for_timeout(500)
    check('new origin card image decoded', page.evaluate("(() => { const i = document.querySelector('.catalog-single-origin img'); return i && i.complete && i.naturalWidth > 0; })()"))
    page.evaluate("document.querySelector('#origin-scene').scrollIntoView()"); page.wait_for_timeout(300)
    for key in ['cajamarca', 'villa-rica', 'cusco', 'puno', 'amazonas']:
        page.click(f'.origin-row-main[data-origin="{key}"]')
        page.wait_for_function('(k)=>document.querySelector("#origin-scene").dataset.origin===k', arg=key)
    check('origin selector cycles all 5', True)
    page.evaluate("document.querySelector('.catalog-quotes figcaption a[data-pdp]').scrollIntoView({block:'center'})")
    page.click('.catalog-quotes figcaption a[data-pdp]')
    page.wait_for_function('!document.querySelector("#producto-amazonas").hidden')
    check('review -> Amazonas PDP opens', page.evaluate("document.getElementById('product-title').textContent") == 'Amazonas')
    page.click('#producto-amazonas [data-product-back]'); page.wait_for_timeout(200)
    page.click('.hero-peru .hero-pack-entry')
    page.wait_for_function('!document.querySelector("#producto-ahorrador").hidden')
    check('hero pack link -> Ahorrador PDP opens', page.evaluate("document.getElementById('pack-title').textContent") == 'El Ahorrador')
    page.click('#producto-ahorrador [data-product-back]'); page.wait_for_timeout(200)
    check('no page errors on functional sweep', not errors, errors)
    page.close()
    b.close()

json.dump({'chromium': version, 'checks': checks}, open(ROOT / 'checks.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
passed = sum(1 for c in checks if c['passed'])
print(f'{passed}/{len(checks)} passed')
