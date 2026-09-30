"""L27: closing bands of 05 (trust, reviews with stars, FAQ, explore tiles). Python Playwright, Chromium DPR 1, production build.
Writes only this dated directory. Includes PDP and B regression.
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
 const root = document.querySelector('#close-bands');
 const small = [], hits = [], fonts = {};
 root.querySelectorAll('*').forEach(el => {
   if (el.children.length) return; const t = (el.textContent||'').trim(); if (!t) return;
   const c = getComputedStyle(el); if (c.display==='none') return; if (parseFloat(c.fontSize) < 11) small.push(t.slice(0,30));
 });
 root.querySelectorAll('a, summary, button').forEach(el => { if (el.parentElement.tagName === 'P') return; const r = el.getBoundingClientRect(); if (r.width && r.height && (r.width < 44 || r.height < 44)) hits.push({t:(el.innerText||'').trim().slice(0,30), w:Math.round(r.width), h:Math.round(r.height)}); });
 const q = document.querySelector('.review-card blockquote'), s = document.querySelector('.close-faq summary'), p = document.querySelector('.close-faq details p');
 return { small, hits, quote: parseFloat(getComputedStyle(q).fontSize), summary: parseFloat(getComputedStyle(s).fontSize),
   stars: document.querySelectorAll('.stars[role=img]').length, starsW: document.querySelector('.stars').getBoundingClientRect().width,
   tiles: document.querySelectorAll('.tile').length, imgs: [...root.querySelectorAll('img')].map(i => i.complete && i.naturalWidth > 0),
   overflow: document.documentElement.scrollWidth - innerWidth, sources: (root.textContent.match(/tienda oficial/g)||[]).length };
}"""

with sync_playwright() as p:
    b = p.chromium.launch(); version = b.version
    for name, w, h in [('desktop', 1440, 900), ('mobile', 390, 844), ('mobile664', 390, 664), ('tablet', 768, 1024), ('w320', 320, 640)]:
        pg = b.new_page(viewport={'width': w, 'height': h}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(URL + '/'); pg.wait_for_timeout(400)
        y = 0; hh = pg.evaluate('document.documentElement.scrollHeight')
        while y < hh:
            pg.evaluate(f'scrollTo(0,{y})'); pg.wait_for_timeout(80); y += h // 2; hh = pg.evaluate('document.documentElement.scrollHeight')
        pg.wait_for_timeout(1200)
        pg.locator('#close-bands').screenshot(path=str(CAP / f'{name}-bands.png'))
        r = pg.evaluate(JS)
        check(f'{name} no text <11px', not r['small'], r['small'])
        check(f'{name} quote >=19px and FAQ question >=16px', r['quote'] >= 19 and r['summary'] >= 16, [r['quote'], r['summary']])
        check(f'{name} 2 review cards with 5 stars', r['stars'] == 2 and abs(r['starsW'] - 120) < 2, [r['stars'], r['starsW']])
        check(f'{name} 4 tiles, images decoded', r['tiles'] == 4 and all(r['imgs']) and len(r['imgs']) == 4, r['imgs'])
        check(f'{name} touch targets >=44px', not r['hits'], r['hits'])
        check(f'{name} no overflow', r['overflow'] == 0, r['overflow'])
        check(f'{name} no page errors', not errs, errs)
        pg.close()

    pg = b.new_page(viewport={'width': 1440, 'height': 900}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e))); pg.goto(URL + '/'); pg.wait_for_timeout(400)
    pg.evaluate("document.querySelector('.close-faq').scrollIntoView()")
    first = pg.locator('.close-faq summary').first
    first.focus(); pg.keyboard.press('Enter')
    check('FAQ opens by keyboard', pg.evaluate("document.querySelector('.close-faq details').open"))
    check('FAQ shows visible focus', pg.evaluate("getComputedStyle(document.querySelector('.close-faq summary:focus-visible')||document.body).outlineStyle") != 'none')
    pg.keyboard.press('Enter')
    pg.evaluate("document.querySelector('.review-card a[data-pdp]').scrollIntoView({block:'center'})"); pg.click('.review-card a[data-pdp]')
    pg.wait_for_function('!document.querySelector("#producto-amazonas").hidden')
    check('review product link opens Amazonas PDP', pg.evaluate("document.getElementById('product-title').textContent") == 'Amazonas')
    check('PDP FAQ keeps its own styling (no close-faq)', pg.evaluate("!document.querySelector('#producto-amazonas .catalog-faq').closest('.close-faq')"))
    pg.click('#producto-amazonas [data-product-back]'); pg.wait_for_timeout(200)
    pg.evaluate("document.querySelector('.review-card a[data-pack-pdp]').scrollIntoView({block:'center'})"); pg.click('.review-card a[data-pack-pdp]')
    pg.wait_for_function('!document.querySelector("#producto-ahorrador").hidden')
    check('review pack link opens El Ahorrador PDP', pg.evaluate("document.getElementById('pack-title').textContent") == 'El Ahorrador')
    check('no page errors in interactions', not errs, errs); pg.close()

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
