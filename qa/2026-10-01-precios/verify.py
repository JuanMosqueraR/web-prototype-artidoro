"""L31 (2026-10-01): prices corrected to the official store snapshot audit/source/prices-2026-10-01.json.
Checks every price the home and both PDPs show against that snapshot, and that no old price is left.
Python Playwright, Chromium, DPR 1, production build served over HTTP. Writes only this dated directory.
Usage: ARTIDORO_REVIEW_URL=http://127.0.0.1:4192 python qa/2026-10-01-precios/verify.py
"""
from pathlib import Path
import json, os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
CAP = ROOT / 'after'; CAP.mkdir(exist_ok=True)
URL = os.environ.get('ARTIDORO_REVIEW_URL', 'http://127.0.0.1:4192').rstrip('/')
SNAP = json.loads((ROOT.parents[1] / 'audit/source/prices-2026-10-01.json').read_text(encoding='utf-8'))['products']
checks = []


def check(name, ok, detail=None):
    checks.append({'name': name, 'passed': bool(ok), 'detail': detail})
    if not ok:
        print('FAIL', name, detail, flush=True)


def soles(cents):
    return f'S/ {cents / 100:.2f}'


price = lambda h, i=0: SNAP[h]['variants'][i]['price']
pack_price, pack_compare = price('pack-3kg-origenes-1'), SNAP['pack-3kg-origenes-1']['variants'][0]['compare_at_price']
saving = f'Ahorras S/ {(pack_compare - pack_price) // 100}'
miel_300 = next(v['price'] for v in SNAP['miel-de-abeja-perfil-frutal']['variants'] if v['options'] == ['300gr'])

with sync_playwright() as p:
    b = p.chromium.launch(); version = b.version
    for name, w, h in [('desktop', 1440, 900), ('mobile', 390, 844)]:
        mob = w <= 760
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, is_mobile=mob, has_touch=mob); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(URL + '/?motion=off'); pg.wait_for_timeout(800)
        t = lambda s: pg.evaluate(f"document.querySelector({json.dumps(s)}).textContent.replace(/\\s+/g, ' ').trim()")
        check(f'{name} hero: Amazonas 250 g and pack (crossed normal price, pack price)',
              soles(price('cafe-amazonas')) in t('.hero-price') and t('.hero-pack-entry .pack-entry-price s').endswith(f'S/ {pack_compare // 100}') and t('.hero-pack-entry .pack-entry-price strong') == f'S/ {pack_price // 100}',
              [t('.hero-price'), t('.hero-pack-entry .pack-entry-price')])
        check(f'{name} 02: every origin S/ {price("cafe-amazonas") / 100:.2f} and pack link price',
              all(r == soles(price('cafe-' + o)) for r, o in zip(pg.evaluate("[...document.querySelectorAll('.origin-rec-price')].map(e => e.textContent.trim())"), ['amazonas', 'cajamarca', 'villa-rica', 'cusco', 'puno']))
              and f'S/ {pack_price // 100}' in t('.origin-pack-entry'), [t('.origin-pack-entry')])
        shop = pg.evaluate("[...document.querySelectorAll('#shop strong')].map(e => e.textContent.trim())")
        want = [soles(pack_price), soles(price('la-expedicion-coleccion-travel-line-preventa')), soles(price('cafe-amazonas')),
                soles(price('pack-el-explorador-250gr-de-cada-origen')), soles(miel_300)]
        check(f'{name} 05: pack, Travel Line, café de origen, El Explorador, miel 300 g', [s for s in shop if s.startswith('S/')] == want and saving in t('#shop .pack-saving'), [shop, t('#shop .pack-saving')])
        allText = pg.evaluate("document.body.textContent.replace(/\\s+/g, ' ')")
        old = [x for x in ['S/ 280', 'Ahorras S/ 50', 'S/ 180.00', 'S/ 99.00'] if x in allText]
        check(f'{name} no old price left anywhere in the document (home and hidden PDPs)', not old, old)
        pg.screenshot(path=str(CAP / f'{name}-hero.png'))
        pg.evaluate("document.querySelector('#shop').scrollIntoView()"); pg.wait_for_timeout(300); pg.screenshot(path=str(CAP / f'{name}-shop.png'))
        # Amazonas PDP: each size shows the official price
        pg.goto(URL + '/#producto-amazonas'); pg.wait_for_timeout(800)
        got = []
        for size in ['250g', '454gr', '1kg']:
            pg.click(f'#producto-amazonas input[name=size][value="{size}"] + span'); pg.wait_for_timeout(150)
            got.append(t('#producto-amazonas .product-price'))
        want = [soles(next(v['price'] for v in SNAP['cafe-amazonas']['variants'] if v['options'][0] == s)) for s in ['250g', '454gr', '1kg']]
        check(f'{name} Amazonas PDP: 250 g / 454 g / 1 kg prices', got == want, [got, want])
        pg.screenshot(path=str(CAP / f'{name}-pdp-amazonas-1kg.png'))
        pg.goto(URL + '/#producto-ahorrador'); pg.wait_for_timeout(800)
        pr = [t('#producto-ahorrador .product-price'), t('#producto-ahorrador .pack-total strong'), t('[data-pack-saving]'), t('[data-pack-total-saving]')]
        check(f'{name} pack PDP: price, total and saving', pr[0] == pr[1] == soles(pack_price) and saving in pr[2] and saving in pr[3], pr)
        pg.screenshot(path=str(CAP / f'{name}-pdp-pack.png'))
        check(f'{name} no page errors', not errs, errs)
        ctx.close()
    pg = b.new_page(); pg.goto(URL + '/')
    og = pg.evaluate("fetch('/assets/og-share.jpg').then(r => r.ok)")
    check('share image exists (regenerated with the new hero pack price; visual check in after/ is manual)', og)
    pg.close(); b.close()

json.dump({'chromium': version, 'url': URL, 'snapshot': 'audit/source/prices-2026-10-01.json', 'checks': checks}, open(ROOT / 'checks.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(sum(c['passed'] for c in checks), '/', len(checks))
