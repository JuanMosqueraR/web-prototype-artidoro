"""L25: hero origin detail automatic (no toggle), pack secondary button, Travel Line weight, scroll behaviour, motion control moved.
Python Playwright, Chromium DPR 1, production build served statically. Writes only this dated directory.
"""
from pathlib import Path
import json, os
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
CAP = ROOT / 'after'; CAP.mkdir(exist_ok=True)
URL = os.environ.get('ARTIDORO_REVIEW_URL', 'http://127.0.0.1:4175')
B_BASE = ROOT.parent / '2026-09-29-ahorro' / 'after'
checks = []


def check(name, ok, detail=None):
    checks.append({'name': name, 'passed': bool(ok), 'detail': detail})
    if not ok:
        print('FAIL', name, detail, flush=True)


JS = r"""() => {
 const q = s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return {t:r.top,b:r.bottom,l:r.left,r:r.right}; };
 const ov = (a,b) => a && b && a.l < b.r && a.r > b.l && a.t < b.b && a.b > b.t;
 const ann = q('.origin-annotation'), cs = getComputedStyle(document.querySelector('.origin-annotation'));
 const small = [];
 document.querySelectorAll('#home-main *').forEach(el => {
   if (el.children.length) return; const t = (el.textContent||'').trim(); if (!t || el.closest('[hidden]')) return;
   const c = getComputedStyle(el); if (c.display==='none' || c.visibility==='hidden') return;
   if (parseFloat(c.fontSize) < 11) small.push(t.slice(0,30));
 });
 return { annVisible: cs.opacity==='1' && cs.clipPath!=='inset(0px 100% 0px 0px)',
   heroButton: !!document.querySelector('#direction-a .origin-button'),
   sensoryControl: document.querySelectorAll('.sensory-control').length,
   overlaps: {bag: ov(ann,q('.product-peru')), price: ov(ann,q('.hero-price')), copy: ov(ann,q('.value-proposition')), buy: ov(ann,q('.hero-peru .buy-button'))},
   buyBottom: q('.hero-peru .buy-button').b, packH: q('.hero-pack-entry').b - q('.hero-pack-entry').t,
   under11: small, overflow: document.documentElement.scrollWidth - innerWidth,
   zoom: getComputedStyle(document.querySelector('.landscape-far')).transform };
}"""

with sync_playwright() as p:
    b = p.chromium.launch(); version = b.version
    for name, w, h in [('desktop', 1440, 900), ('mobile', 390, 844), ('mobile664', 390, 664), ('tablet', 768, 1024)]:
        pg = b.new_page(viewport={'width': w, 'height': h}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(URL + '/'); pg.wait_for_timeout(3200)
        pg.screenshot(path=str(CAP / f'{name}-hero.png'))
        r = pg.evaluate(JS)
        check(f'{name} detail auto-visible', r['annVisible'])
        check(f'{name} no hero toggle button', not r['heroButton'])
        check(f'{name} no 03 motion control', r['sensoryControl'] == 0)
        check(f'{name} annotation overlaps nothing', not any(r['overlaps'].values()), r['overlaps'])
        check(f'{name} zoom reached 1.12', r['zoom'].startswith('matrix(1.12'), r['zoom'])
        check(f'{name} pack button height >=48', r['packH'] >= 48, r['packH'])
        check(f'{name} no text <11px', not r['under11'], r['under11'])
        check(f'{name} no overflow', r['overflow'] == 0, r['overflow'])
        if name.startswith('mobile'):
            check(f'{name} CTA inside viewport', r['buyBottom'] <= h, r['buyBottom'])
        check(f'{name} no page errors', not errs, errs)
        pg.close()

    ctx = b.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce'); pg = ctx.new_page()
    pg.goto(URL + '/'); pg.wait_for_timeout(300)
    r = pg.evaluate(JS)
    check('reduced motion: detail visible, no zoom', r['annVisible'] and r['zoom'] == 'none', r['zoom'])
    ctx.close()

    pg = b.new_page(viewport={'width': 390, 'height': 844}); pg.goto(URL + '/'); pg.wait_for_timeout(2500)
    pg.click('.store-menu summary'); pg.click('.store-menu nav a[href="#origin-scene"]'); pg.wait_for_timeout(120)
    mid = pg.evaluate('scrollY'); pg.wait_for_timeout(1500)
    check('anchor not crossing 03 scrolls smoothly', 0 < mid < pg.evaluate('scrollY'), mid)
    pg.click('.home-nav .nav-buy'); pg.wait_for_timeout(60)
    top = pg.evaluate("document.querySelector('#shop').getBoundingClientRect().top")
    check('anchor crossing 03 jumps instantly with arrival fade',
          abs(top - 76) < 4 and pg.evaluate("document.querySelector('#shop').classList.contains('anchor-arrive')"), top)
    pg.evaluate("document.querySelector('.review-details').scrollIntoView()")
    pg.click('.review-details summary'); pg.click('.motion-toggle')
    check('motion toggle lives in Acerca de esta demo',
          pg.evaluate("document.documentElement.classList.contains('no-motion')") and pg.locator('[data-home-motion]').count() == 1)
    pg.close()

    pg = b.new_page(viewport={'width': 1440, 'height': 900}); pg.goto(URL + '/'); pg.wait_for_timeout(500)
    pg.evaluate("document.querySelector('.catalog-edit').scrollIntoView()"); pg.wait_for_timeout(1000)
    pg.screenshot(path=str(CAP / 'desktop-05.png'))
    pack = pg.locator('.pack-feature .catalog-link').bounding_box(); trav = pg.locator('.catalog-travel .catalog-link').bounding_box()
    check('Travel Line CTA is a button as large as the pack CTA', abs(trav['height'] - pack['height']) < 4, [pack['height'], trav['height']])
    pg.close()

    for name, w, h in [('desktop', 1440, 900), ('mobile', 390, 844)]:
        for off in [False, True]:
            pg = b.new_page(viewport={'width': w, 'height': h}); pg.goto(URL + '/b/' + ('?motion=off' if off else '')); pg.evaluate('document.fonts.ready')
            hero = pg.locator('#direction-b')
            hero.locator('img[src]').evaluate_all('async i=>Promise.all(i.map(x=>{x.loading="eager";return x.decode()}))')
            for frame in ['initial', 'expanded']:
                if frame == 'expanded':
                    hero.locator('[data-reveal]').click(); pg.wait_for_timeout(900)
                stem = f'b-{name}-{"reduced" if off else "motion"}-{frame}'
                t = CAP / (stem + '.png'); pg.screenshot(path=str(t))
                d = ImageChops.difference(Image.open(B_BASE / (stem + '.png')).convert('RGB'), Image.open(t).convert('RGB'))
                n = sum(1 for x in d.getdata() if max(x) > 0)
                check(stem + ' B unchanged', n <= w * h * .0005 and max(v[1] for v in d.getextrema()) <= 16, n)
            pg.close()
    b.close()

json.dump({'chromium': version, 'checks': checks}, open(ROOT / 'checks.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(sum(c['passed'] for c in checks), '/', len(checks))
