"""L31 (2026-10-01): renewed PDPs (Amazonas, El Ahorrador) — six blocks, gallery with zoom, sticky bar, pack chips.
Python Playwright, Chromium, DPR 1, production build served over HTTP. Writes only this dated directory.
Usage: ARTIDORO_REVIEW_URL=http://127.0.0.1:4192 python qa/2026-10-01-pdp/verify.py
"""
from pathlib import Path
import json, os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
CAP = ROOT / 'after'; CAP.mkdir(exist_ok=True)
URL = os.environ.get('ARTIDORO_REVIEW_URL', 'http://127.0.0.1:4192').rstrip('/')
REPO = ROOT.parents[1]
AMZ = json.loads((REPO / 'src/amazonas-variants.json').read_text(encoding='utf-8'))
PACK = json.loads((REPO / 'src/ahorrador-variants.json').read_text(encoding='utf-8'))
checks = []


def check(name, ok, detail=None):
    checks.append({'name': name, 'passed': bool(ok), 'detail': detail})
    if not ok:
        print('FAIL', name, detail, flush=True)


SMALL = """sel => { const out = []; document.querySelector(sel).querySelectorAll('*').forEach(el => { if (el.children.length) return; const t = (el.textContent || '').trim(); if (!t) return;
  const c = getComputedStyle(el); if (c.display === 'none' || c.visibility === 'hidden' || !el.getClientRects().length) return; if (parseFloat(c.fontSize) < 11) out.push(t.slice(0, 30)); }); return out; }"""
TEXT = lambda pg, s: pg.evaluate(f"document.querySelector({json.dumps(s)}).textContent.replace(/\\s+/g, ' ').trim()")

with sync_playwright() as p:
    b = p.chromium.launch(); version = b.version
    for name, w, h in [('desktop', 1440, 900), ('mobile', 390, 844)]:
        mob = w <= 760
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, is_mobile=mob, has_touch=mob)
        pg = ctx.new_page(); errs = []; reqs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('request', lambda r: reqs.append(r.url))
        # Home: no PDP-only picture is requested before a PDP opens
        pg.goto(URL + '/?motion=off'); pg.wait_for_timeout(1500)
        early = [u for u in reqs if any(k in u for k in ['pdp-', 'ahorrador-villa-rica', 'ahorrador-cusco'])]
        check(f'{name} home load requests no PDP-only picture', not early, early)
        check(f'{name} header «Comprar café» visible on the home', pg.evaluate("getComputedStyle(document.querySelector('.home-nav .nav-buy')).display") != 'none')
        # Amazonas PDP from the hero
        pg.click('.hero-peru .buy-button'); pg.wait_for_function("!document.querySelector('#producto-amazonas').hidden"); pg.wait_for_timeout(900)
        amz = '#producto-amazonas'
        check(f'{name} hero CTA opens the Amazonas PDP, title focused, header buy link hidden',
              TEXT(pg, amz + ' h1') == 'Amazonas' and pg.evaluate("document.activeElement.id") == 'product-title' and pg.evaluate("getComputedStyle(document.querySelector('.home-nav .nav-buy')).display") == 'none')
        pg.evaluate(f"Promise.all([...document.querySelectorAll('{amz} img[src]')].map(i => {{ i.loading = 'eager'; return i.decode().catch(() => null); }}))"); pg.wait_for_timeout(300)
        broken = pg.evaluate(f"[...document.querySelectorAll('{amz} img')].filter(i => !(i.complete && i.naturalWidth)).map(i => i.dataset.pdpSrc || i.src)")
        check(f'{name} Amazonas: every picture loaded once the PDP opens', not broken, broken)
        check(f'{name} Amazonas: rating next to the price (5,0 · 3 reseñas) linking to the reviews block',
              TEXT(pg, amz + ' .pdp-rating') == '5,0 · 3 reseñas en la tienda oficial' and pg.evaluate(f"document.querySelector('{amz} .pdp-rating').getAttribute('href')") == '#pdp-reviews-amazonas')
        sizes = pg.evaluate(f"[...document.querySelectorAll('{amz} [data-size-price]')].map(e => e.textContent)")
        want = [f"S/ {min(v['price'] for v in AMZ['variants'] if v['option1'] == s) / 100:.2f}" for s in ['250g', '454gr', '1kg']]
        check(f'{name} Amazonas: each size button shows its official price', sizes == want, [sizes, want])
        pg.click(f'{amz} input[value="1kg"] + span'); pg.click(f'{amz} input[value="Molido Medio"] + span'); pg.wait_for_timeout(200)
        v = next(x for x in AMZ['variants'] if x['option1'] == '1kg' and x['option2'] == 'Molido Medio')
        st = pg.evaluate(f"""(() => {{ const q = s => document.querySelector('{amz} ' + s); return {{price: q('.product-price').textContent, yield: q('[data-yield]').textContent, href: q('.pdp-cta').href,
          bar: q('[data-bar-price]').textContent, barHref: q('.pdp-bar a').href, barSel: q('[data-bar-selection]').textContent}}; }})()""")
        check(f'{name} Amazonas 1 kg molido medio: price, cups (FAQ: unas 65), CTA variant and sticky bar in sync',
              st['price'] == f"S/ {v['price'] / 100:.2f}" and st['yield'] == 'Bolsa de 1 kg · unas 65 tazas' and st['href'].endswith(f"variant={v['id']}") and st['bar'] == st['price'] and st['barHref'] == st['href'] and st['barSel'] == '1 kg · Molido Medio', st)
        notices = pg.evaluate(f"[...document.querySelectorAll('{amz} .pdp-ai')].length")
        check(f'{name} Amazonas: conceptual pictures carry their notice (3 slides) and the process band its credit', notices == 3 and 'conceptuales' in TEXT(pg, amz + ' .pdp-credit'), notices)
        # Gallery
        if mob:
            pg.evaluate(f"document.querySelector('{amz} .pdp-track').scrollTo({{left: 2 * document.querySelector('{amz} .pdp-track').clientWidth, behavior: 'instant'}})"); pg.wait_for_timeout(400)
            idx = TEXT(pg, amz + ' [data-gallery-index]')
            check(f'{name} gallery: swiping (horizontal scroll) moves the counter', idx == '3', idx)
        else:
            pg.click(f'{amz} [data-gallery-next]'); pg.wait_for_timeout(700); a = TEXT(pg, amz + ' [data-gallery-index]')
            pg.click(f'{amz} .pdp-thumbs button:nth-child(3)'); pg.wait_for_timeout(700); c = TEXT(pg, amz + ' [data-gallery-index]')
            cur = pg.evaluate(f"document.querySelector('{amz} .pdp-thumbs button:nth-child(3)').getAttribute('aria-current')")
            check(f'{name} gallery: arrow and thumbnails move the slide and mark the thumbnail', a == '2' and c == '3' and cur == 'true', [a, c, cur])
        pg.screenshot(path=str(CAP / f'{name}-amazonas-fold.png'))
        # Zoom: every slide has a button; the photo opens full screen, a tap/click zooms in, arrows browse, Escape closes
        pg.evaluate(f"document.querySelector('{amz} .pdp-track').scrollTo({{left: 0, behavior: 'instant'}})"); pg.wait_for_timeout(300)
        buttons = pg.evaluate(f"[document.querySelectorAll('{amz} .pdp-slide').length, document.querySelectorAll('{amz} .pdp-track .pdp-zoom').length]")
        pg.click(f'{amz} .pdp-slide:nth-child(1) .pdp-zoom'); pg.wait_for_timeout(500)
        opened = pg.evaluate(f"[document.querySelector('{amz} .pdp-lightbox').open, document.documentElement.classList.contains('lb-open')]")
        box = pg.evaluate(f"(() => {{ const c = document.querySelector('{amz} .pdp-lb-canvas').getBoundingClientRect(); return [c.width / 2, c.height * .6]; }})()")
        if mob: pg.tap(f'{amz} .pdp-lb-canvas', position={'x': box[0], 'y': box[1]})
        else: pg.click(f'{amz} .pdp-lb-canvas', position={'x': box[0], 'y': box[1]})
        pg.wait_for_timeout(400)
        zoomed = pg.evaluate(f"(() => {{ const s = document.querySelector('{amz} .pdp-lb-stage'); return [document.querySelector('{amz} .pdp-lightbox').classList.contains('is-zoomed'), s.scrollWidth > s.clientWidth + 100]; }})()")
        pg.screenshot(path=str(CAP / f'{name}-amazonas-zoom.png'))
        pg.click(f'{amz} .pdp-lb-zoom'); pg.click(f'{amz} .pdp-lb-next'); pg.click(f'{amz} .pdp-lb-next'); pg.wait_for_timeout(300)
        count = TEXT(pg, amz + ' .pdp-lb-count')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(800)
        closed = pg.evaluate(f"[document.querySelector('{amz} .pdp-lightbox').open, document.documentElement.classList.contains('lb-open'), document.querySelector('{amz} [data-gallery-index]').textContent]")
        check(f'{name} zoom: button on every slide, opens full screen, zooms in at the tap, browses, Escape closes and the gallery follows',
              buttons[0] == buttons[1] == 6 and opened == [True, True] and zoomed == [True, True] and count == '3 / 6' and closed == [False, False, '3'], [buttons, opened, zoomed, count, closed])
        # Sticky bar: hidden while the main button is on screen, shown when it is not
        pg.evaluate(f"document.querySelector('{amz} .pdp-cta').scrollIntoView({{block: 'center'}})"); pg.wait_for_timeout(500)
        on_cta = pg.evaluate(f"document.querySelector('{amz} [data-pdp-bar]').classList.contains('is-shown')")
        pg.evaluate(f"document.querySelector('{amz} .pdp-origin').scrollIntoView()"); pg.wait_for_timeout(500)
        later = pg.evaluate(f"document.querySelector('{amz} [data-pdp-bar]').classList.contains('is-shown')")
        check(f'{name} sticky bar: hidden with the main button on screen, shown after it', not on_cta and later, [on_cta, later])
        pg.screenshot(path=str(CAP / f'{name}-amazonas-origin.png'))
        small = pg.evaluate(SMALL, amz)
        check(f'{name} Amazonas: no visible text < 11 px', not small, small)
        check(f'{name} Amazonas: no horizontal overflow', pg.evaluate('document.documentElement.scrollWidth - innerWidth') == 0)
        pg.evaluate("Promise.all([...document.querySelectorAll('#producto-amazonas img[src]')].map(i => i.decode().catch(() => null)))")
        pg.screenshot(path=str(CAP / f'{name}-amazonas-full.png'), full_page=True)
        # Back to the home, then the pack from 05
        pg.click(f'{amz} [data-product-back]'); pg.wait_for_timeout(800)
        check(f'{name} back link returns to the home with the header buy link again', not pg.evaluate("document.querySelector('#home-main').hidden") and pg.evaluate("getComputedStyle(document.querySelector('.home-nav .nav-buy')).display") != 'none')
        pg.evaluate("document.querySelector('#shop').scrollIntoView()"); pg.wait_for_timeout(500)
        pg.click('#shop .pack-feature .catalog-link'); pg.wait_for_function("!document.querySelector('#producto-ahorrador').hidden"); pg.wait_for_timeout(900)
        pk = '#producto-ahorrador'
        chips = pg.evaluate(f"[...document.querySelectorAll('{pk} .pdp-chip input')].map(i => i.name + ':' + i.value + (i.checked ? '*' : ''))")
        check(f'{name} pack: 3 × 5 origin chips in the official order, defaults Amazonas / Cajamarca / Puno',
              len(chips) == 15 and [c for c in chips if c.endswith('*')] == ['bag1:Amazonas*', 'bag2:Cajamarca*', 'bag3:Puno*'], chips)
        for bag, origin in [(1, 'Villa Rica'), (2, 'Cusco'), (3, 'Cusco')]:
            pg.click(f'{pk} input[name="bag{bag}"][value="{origin}"] + span')
        pg.wait_for_timeout(300)
        vv = next(x for x in PACK['variants'] if x['options'] == ['Villa Rica', 'Cusco', 'Cusco'])
        st = pg.evaluate(f"""(() => {{ const q = s => document.querySelector('{pk} ' + s); return {{imgs: [...document.querySelectorAll('{pk} [data-pack-visual] img')].map(i => i.getAttribute('src')), cap: q('[data-pack-caption]').textContent,
          price: q('.product-price').textContent, total: q('.pack-total strong').textContent, saving: q('[data-pack-saving]').textContent, href: q('.pdp-cta').href, bar: q('[data-bar-selection]').textContent}}; }})()""")
        check(f'{name} pack Villa Rica · Cusco · Cusco: picture, caption, price, saving, CTA variant and bar follow the choice',
              st['imgs'] == ['/assets/ahorrador-villa-rica-1kg.webp', '/assets/ahorrador-cusco-1kg.webp', '/assets/ahorrador-cusco-1kg.webp'] and st['cap'] == 'Tu combinación: Villa Rica, Cusco y Cusco.'
              and st['price'] == st['total'] == f"S/ {vv['price'] / 100:.2f}" and 'Ahorras S/ 20' in st['saving'] and st['href'].endswith(f"variant={vv['id']}") and st['bar'] == 'Villa Rica · Cusco · Cusco', st)
        pg.evaluate(f"Promise.all([...document.querySelectorAll('{pk} img[src]')].map(i => {{ i.loading = 'eager'; return i.decode().catch(() => null); }}))"); pg.wait_for_timeout(300)
        broken = pg.evaluate(f"[...document.querySelectorAll('{pk} img')].filter(i => !(i.complete && i.naturalWidth)).map(i => i.dataset.packSrc || i.src)")
        check(f'{name} pack: every picture loaded', not broken, broken)
        small = pg.evaluate(SMALL, pk)
        check(f'{name} pack: no visible text < 11 px', not small, small)
        check(f'{name} pack: no horizontal overflow', pg.evaluate('document.documentElement.scrollWidth - innerWidth') == 0)
        pg.screenshot(path=str(CAP / f'{name}-pack-fold.png'))
        pg.click(f'{pk} .pdp-slide:nth-child(1) .pdp-zoom'); pg.wait_for_timeout(500)
        srcs = pg.evaluate(f"[...document.querySelectorAll('{pk} .pdp-lb-canvas [data-pack-visual] img')].map(i => i.getAttribute('src'))")
        pg.screenshot(path=str(CAP / f'{name}-pack-zoom.png'))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
        check(f'{name} pack zoom shows the chosen combination', srcs == ['/assets/ahorrador-villa-rica-1kg.webp', '/assets/ahorrador-cusco-1kg.webp', '/assets/ahorrador-cusco-1kg.webp'], srcs)
        pg.screenshot(path=str(CAP / f'{name}-pack-full.png'), full_page=True)
        check(f'{name} no page errors', not errs, errs)
        ctx.close()
    for w, h in [(320, 640), (768, 1024), (1024, 768), (1920, 1080)]:
        pg = b.new_page(viewport={'width': w, 'height': h})
        for route in ['#producto-amazonas', '#producto-ahorrador']:
            pg.goto(URL + '/?motion=off' + route); pg.wait_for_timeout(600)
            check(f'{w}x{h} {route}: no horizontal overflow', pg.evaluate('document.documentElement.scrollWidth - innerWidth') == 0)
        pg.close()
    b.close()

json.dump({'chromium': version, 'url': URL, 'checks': checks}, open(ROOT / 'checks.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(sum(c['passed'] for c in checks), '/', len(checks))
