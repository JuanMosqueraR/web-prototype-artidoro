"""L29 (2026-10-01): home review fixes (P1), copy clean-up (P2) and 04 «Nos vemos en Miraflores» (P3).
Starts from the L28 regression (qa/2026-09-30-l28/verify.py, adapted: the hero has two text steps now) and adds the
checks of this round at the end. Python Playwright, Chromium, DPR 1, production build served over HTTP with Range support.
Writes only this dated directory (after/ and checks.json). Includes B and PDP regression.
Usage: ARTIDORO_REVIEW_URL=http://127.0.0.1:4192 python qa/2026-10-01-revision/verify.py
"""
from pathlib import Path
import json, os, re
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
CAP = ROOT / 'after'; CAP.mkdir(exist_ok=True)
URL = os.environ.get('ARTIDORO_REVIEW_URL', 'http://127.0.0.1:4192').rstrip('/')
B_BASE = ROOT.parent / '2026-09-29-ahorro' / 'after'
checks = []


def check(name, ok, detail=None):
    checks.append({'name': name, 'passed': bool(ok), 'detail': detail})
    if not ok:
        print('FAIL', name, detail, flush=True)


RECT = """s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return {top: b.top, bottom: b.bottom, left: b.left, right: b.right, w: b.width, h: b.height}; }"""
SMALL = """sel => { const out = []; document.querySelectorAll(sel).forEach(root => root.querySelectorAll('*').forEach(el => {
  if (el.children.length) return; const t = (el.textContent || '').trim(); if (!t) return; const c = getComputedStyle(el);
  if (c.display === 'none' || c.visibility === 'hidden') return; if (parseFloat(c.fontSize) < 11) out.push(t.slice(0, 30)); })); return out; }"""
TARGETS = """sel => { const out = []; document.querySelectorAll(sel).forEach(root => root.querySelectorAll('a, button').forEach(el => {
  if (el.closest('p') && el.closest('p').textContent.trim() !== el.textContent.trim()) return;
  const b = el.getBoundingClientRect(); if (b.width && b.height && (b.width < 44 || b.height < 44)) out.push([(el.innerText || '').trim().slice(0, 24), Math.round(b.width), Math.round(b.height)]); })); return out; }"""


def goto(pg, query=''):
    pg.goto(URL + '/' + query)
    pg.evaluate('document.fonts.ready')


def scene_scroll(pg, sel, f):
    """Scroll so the pinned scene sits at progress f."""
    pg.evaluate(f"""(() => {{ const s = document.querySelector('{sel}'); const st = s.firstElementChild;
      const top = parseFloat(getComputedStyle(st).top) || 0; const y = s.getBoundingClientRect().top + scrollY - top;
      scrollTo(0, y + (s.offsetHeight - st.offsetHeight) * {f}); }})()""")


with sync_playwright() as p:
    b = p.chromium.launch(); version = b.version
    # --- Motion on: hero, 03, bands, header -----------------------------------------------
    for name, w, h in [('desktop', 1440, 900), ('mobile', 390, 844), ('mobile664', 390, 664), ('tablet', 768, 1024)]:
        mob = w <= 760
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, is_mobile=mob, has_touch=mob)
        pg = ctx.new_page(); errs = []; media = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('request', lambda r: media.append(r.url) if r.url.endswith('.mp4') or 'hero-seq' in r.url else None)
        goto(pg)
        first = {k: pg.evaluate(RECT, s) for k, s in [('buy', '.hero-peru .buy-button'), ('pack', '.hero-peru .hero-pack-entry'), ('h1', '#title-a'), ('status', '.hero-peru .asset-status')]}
        check(f'{name} hero CTA, trust and pack inside the first viewport', first['pack']['bottom'] <= h and first['buy']['top'] > 0, first)
        check(f'{name} header transparent over the hero', pg.evaluate("document.documentElement.classList.contains('nav-over-hero')"))
        check(f'{name} no horizontal overflow at the top', pg.evaluate('document.documentElement.scrollWidth - innerWidth') == 0)
        try:
            pg.wait_for_function("document.querySelector('#direction-a').dataset.media === 'video' && document.querySelector('#direction-a').classList.contains('has-video')", timeout=20000); ok = True
        except Exception:
            ok = False
        check(f'{name} hero media path is the video', ok, pg.evaluate("document.querySelector('#direction-a').dataset.media"))
        seq = [u for u in media if 'hero-seq' in u]
        mp4 = [u for u in media if u.endswith('.mp4')]
        expected = 'hero-mobile.mp4' if mob else 'hero-desktop.mp4'
        check(f'{name} hero loads only its own video and no image sequence', mp4 and all(u.endswith(expected) for u in mp4) and not seq, [mp4, len(seq)])
        pg.wait_for_timeout(800)
        pg.screenshot(path=str(CAP / f'{name}-hero-0.png'))
        marks = []
        for i, f in enumerate([.5, 1.0]):
            scene_scroll(pg, '#direction-a', f); pg.wait_for_timeout(1600)
            marks.append(pg.evaluate("document.querySelector('.hs-video').currentTime"))
            pg.screenshot(path=str(CAP / f'{name}-hero-{i + 1}.png'))
        check(f'{name} video follows the scroll (mid ~5 s, end ~9.9 s)', 4.2 < marks[0] < 5.8 and marks[1] > 9.6, marks)
        state = pg.evaluate("(() => { const h = document.querySelector('#direction-a'), s = getComputedStyle(h); return {bag: +s.getPropertyValue('--bag'), step: h.dataset.step, texts: [...h.querySelectorAll('.hs-step')].map(e => +getComputedStyle(e).opacity)}; })()")
        check(f'{name} hero ends on step 3 with the bag in place and no step text over it', state['step'] == '3' and state['bag'] > .99 and len(state['texts']) == 2 and max(state['texts']) < .01, state)
        # 03
        steps = []
        for i, f in enumerate([.1, .35, .6, .95]):
            scene_scroll(pg, '#sensory-scene', f); pg.wait_for_timeout(1700)
            steps.append(pg.evaluate("document.querySelector('#sensory-scene').dataset.step"))
            pg.screenshot(path=str(CAP / f'{name}-cup-{i}.png'))
        check(f'{name} 03 steps 1 → 2 → 2 → 3', steps == ['1', '2', '2', '3'], steps)
        final = pg.evaluate("(() => { const bag = document.querySelector('.cs-bag'); const t = document.querySelector('#cup-title').getBoundingClientRect(); return {bag: +getComputedStyle(bag).opacity, loaded: bag.complete && bag.naturalWidth > 0, frames: [...document.querySelectorAll('.cs-frame img')].map(i => i.complete && i.naturalWidth > 0), title: t.top >= 0 && t.bottom <= innerHeight}; })()")
        check(f'{name} 03 final: frames decoded, bag shown, title on screen', final['bag'] > .95 and final['loaded'] and all(final['frames']) and final['title'], final)
        # Pace of 03 (scroll-linked, first configuration): how long each text stays fully readable while the scene is on screen,
        # scrolling at human speeds. Regression for the middle step being readable for only ~0.4 s when transitions were
        # time-based and triggered at a cut. Speeds are in screen heights per second so they scale with the viewport.
        if mob:
            for factor, need in [(.95, (1500, 800, 900)), (1.18, (1200, 600, 600))]:
                speed = round(factor * h)
                pg.goto(URL + '/'); pg.wait_for_timeout(2000)
                meta = pg.evaluate("""() => { const s = document.querySelector('#sensory-scene'); window.__log = [];
                  window.__iv = setInterval(() => { const c = document.querySelector('#sensory-scene'), r = c.getBoundingClientRect(); const op = e => +getComputedStyle(e).opacity;
                    window.__log.push({t: performance.now(), texts: [...c.querySelectorAll('.cs-step')].map(op), bag: op(c.querySelector('.cs-bag')), bottom: r.bottom}); }, 30);
                  return {top: s.getBoundingClientRect().top + scrollY - 64, range: s.offsetHeight - s.firstElementChild.offsetHeight}; }""")
                pg.evaluate(f"scrollTo(0, {meta['top']} - 780)"); pg.wait_for_timeout(500)
                import time
                t0 = time.time(); y = meta['top'] - 780
                while y < meta['top'] + meta['range'] + 900:
                    y = meta['top'] - 780 + (time.time() - t0) * speed; pg.evaluate(f"scrollTo(0, {y})"); pg.wait_for_timeout(16)
                pg.wait_for_timeout(400)
                log = pg.evaluate("(() => { clearInterval(window.__iv); return window.__log; })()")
                on = [e for e in log if e['bottom'] > 220]
                dt = (log[-1]['t'] - log[0]['t']) / max(1, len(log) - 1)
                readable = [round(sum(1 for e in on if e['texts'][i] > .9) * dt) for i in range(3)]
                check(f'{name} 03 at {factor} screens/s ({speed} px/s): each step readable >= {need} ms (first, middle, final)', all(r >= n for r, n in zip(readable, need)), [speed, readable])
            pg.goto(URL + '/'); pg.wait_for_timeout(1500)
            scene_scroll(pg, '#sensory-scene', 1); pg.wait_for_timeout(2500)
        check(f'{name} header solid after the hero', not pg.evaluate("document.documentElement.classList.contains('nav-over-hero')"))
        # Bands
        pg.evaluate("document.querySelector('.grinds').scrollIntoView({block: 'center'})"); pg.wait_for_timeout(1300)
        g = pg.evaluate("(() => { const t = document.querySelector('#grinds-title'); return {items: document.querySelectorAll('.grinds-list li').length, revealed: t.classList.contains('is-revealed'), visible: getComputedStyle(t.querySelector('.rl > span') || t).transform}; })()")
        check(f'{name} grinds band: 4 items, title revealed', g['items'] == 4 and g['revealed'] and g['visible'] in ('none', 'matrix(1, 0, 0, 1, 0, 0)'), g)
        pg.locator('.grinds').screenshot(path=str(CAP / f'{name}-grinds.png'))
        check(f'{name} no text < 11 px in the new sections', not pg.evaluate(SMALL, '.hero-peru, .cup-scene, .grinds, .close-trust'), pg.evaluate(SMALL, '.hero-peru, .cup-scene, .grinds, .close-trust'))
        trust = pg.evaluate("[...document.querySelectorAll('.close-trust li')].map(li => li.textContent.trim())")
        check(f'{name} 05 trust has 4 items incl. Precio justo al caficultor', len(trust) == 4 and trust[-1] == 'Precio justo al caficultor', trust)
        pg.evaluate("document.querySelector('.close-trust').scrollIntoView({block: 'center'})"); pg.wait_for_timeout(300)
        pg.locator('.close-trust').screenshot(path=str(CAP / f'{name}-trust.png'))
        check(f'{name} no buy bar (removed at user request)', not pg.evaluate("document.querySelector('[data-buy-bar]')"))
        if mob:
            scene_scroll(pg, '#sensory-scene', 1); pg.wait_for_timeout(1800)
            ov = pg.evaluate("(() => { const bag = document.querySelector('.cs-bag').getBoundingClientRect(), t = document.querySelector('#cup-title').getBoundingClientRect(); return {bagBottom: Math.round(bag.bottom), titleTop: Math.round(t.top), kicker: getComputedStyle(document.querySelector('.cs-final .home-kicker')).display}; })()")
            check(f'{name} 03 final: title below the bag, kicker hidden', ov['titleTop'] >= ov['bagBottom'] and ov['kicker'] == 'none', ov)
        check(f'{name} touch targets >= 44 px in hero and 03', not pg.evaluate(TARGETS, '.hero-peru, .cup-scene'), pg.evaluate(TARGETS, '.hero-peru, .cup-scene'))
        check(f'{name} no page errors', not errs, errs)
        ctx.close()

    # --- Motion off (site switch) and reduced motion (system): static, no video requested -------
    for name, w, h in [('desktop', 1440, 900), ('mobile', 390, 844)]:
        mob = w <= 760
        for mode in ['motion-off', 'reduced']:
            ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, is_mobile=mob, has_touch=mob, reduced_motion='reduce' if mode == 'reduced' else 'no-preference')
            pg = ctx.new_page(); errs = []; media = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('request', lambda r: media.append(r.url) if r.url.endswith('.mp4') or 'hero-seq' in r.url else None)
            goto(pg, '?motion=off' if mode == 'motion-off' else '')
            pg.wait_for_timeout(2500)
            st = pg.evaluate("""(() => { const h = document.querySelector('#direction-a'), c = document.querySelector('#sensory-scene');
              const end = h.querySelector('.hs-end img'); return {heroStatic: h.classList.contains('is-static'), cupStatic: c.classList.contains('is-static'),
              heroPinned: h.offsetHeight > h.firstElementChild.offsetHeight + 2, cupPinned: c.offsetHeight > c.firstElementChild.offsetHeight + 2,
              end: end.complete && end.naturalWidth > 0, endOpacity: +getComputedStyle(h.querySelector('.hs-end')).opacity, bag: +getComputedStyle(h.querySelector('.product-peru')).opacity,
              cupStep: c.dataset.step, titles: [...document.querySelectorAll('[data-reveal-lines]')].every(t => !t.querySelector('.rl') || getComputedStyle(t.querySelector('.rl > span')).transform === 'none')}; })()""")
            check(f'{name} {mode}: both scenes static, final state, no video requested', st['heroStatic'] and st['cupStatic'] and not st['heroPinned'] and not st['cupPinned'] and st['end'] and st['endOpacity'] > .99 and st['bag'] > .99 and st['cupStep'] == '3' and not media, {**st, 'media': media})
            check(f'{name} {mode}: titles visible without animation', st['titles'])
            first = pg.evaluate(RECT, '.hero-peru .hero-pack-entry')
            check(f'{name} {mode}: CTA and pack in the first viewport', first['bottom'] <= h, first)
            pg.screenshot(path=str(CAP / f'{name}-{mode}-hero.png'))
            pg.evaluate("document.querySelector('#sensory-scene').scrollIntoView()"); pg.wait_for_timeout(400)
            pg.screenshot(path=str(CAP / f'{name}-{mode}-cup.png'))
            check(f'{name} {mode}: no page errors', not errs, errs)
            ctx.close()

    # --- Desktop inertia: the wheel glides; touch keeps native scrolling ------------------------------
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=1); pg = ctx.new_page(); goto(pg)
    pg.evaluate("scrollTo(0, 3000)"); pg.wait_for_timeout(300); pg.mouse.move(700, 450)
    pg.mouse.wheel(0, 600); pg.wait_for_timeout(40); early = pg.evaluate('scrollY'); pg.wait_for_timeout(1200); late = pg.evaluate('scrollY')
    check('desktop inertia: wheel glides to its target', 3000 < early < 3590 and abs(late - 3600) <= 2, [early, late])
    pg.keyboard.press('End'); pg.wait_for_timeout(600)
    check('desktop inertia: keyboard still reaches the end', pg.evaluate('scrollY + innerHeight >= document.documentElement.scrollHeight - 2'))
    ctx.close()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=1, reduced_motion='reduce'); pg = ctx.new_page(); goto(pg)
    pg.evaluate("scrollTo(0, 3000)"); pg.mouse.move(700, 450); pg.mouse.wheel(0, 600); pg.wait_for_timeout(60)
    check('desktop reduced motion: wheel is native (no glide)', abs(pg.evaluate('scrollY') - 3600) <= 2, pg.evaluate('scrollY'))
    ctx.close()

    # --- Mobile browser toolbars: media stage uses the tall viewport, content stays in the small one ---------------
    ctx = b.new_context(viewport={'width': 390, 'height': 664}, device_scale_factor=1, is_mobile=True, has_touch=True); pg = ctx.new_page(); goto(pg)
    pg.wait_for_timeout(1500)
    pg.evaluate("document.documentElement.style.setProperty('--bars', '110px')"); pg.wait_for_timeout(300)
    geo = pg.evaluate("(() => { const st = document.querySelector('.hs-stage').getBoundingClientRect(), pk = document.querySelector('.hero-pack-entry').getBoundingClientRect(); return {stage: Math.round(st.height), packBottom: Math.round(pk.bottom), small: innerHeight}; })()")
    check('toolbars hidden (--bars 110 px): stage is 110 px taller and the pack stays inside the small viewport', geo['stage'] == 664 + 110 and geo['packBottom'] <= geo['small'], geo)
    ctx.close()
    # --- 02 carousel swipe (touch) ------------------------------------------------------------------------------------
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True); pg = ctx.new_page(); goto(pg); pg.wait_for_timeout(1500)
    pg.evaluate("document.querySelector('#origin-scene').scrollIntoView()"); pg.wait_for_timeout(600)
    cdp = ctx.new_cdp_session(pg)
    cx, cy = pg.evaluate("(() => { const r = document.querySelector('.origin-stage').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; })()")
    def touch(t, px, py): cdp.send('Input.dispatchTouchEvent', {'type': t, 'touchPoints': ([{'x': px, 'y': py}] if t not in ('touchEnd', 'touchCancel') else [])})
    before = pg.evaluate("document.querySelector('#origin-scene').dataset.origin")
    touch('touchStart', cx + 90, cy)
    for i in range(1, 10): touch('touchMove', cx + 90 - i * 20, cy + (i % 3)); pg.wait_for_timeout(16)
    touch('touchEnd', 0, 0); pg.wait_for_timeout(1400)
    check('02 carousel: horizontal swipe changes the origin', before == 'amazonas' and pg.evaluate("document.querySelector('#origin-scene').dataset.origin") == 'cajamarca', pg.evaluate("document.querySelector('#origin-scene').dataset.origin"))
    # A short fast flick (34 px in 50 ms) back to the right, and a swipe the OS cancels as the finger lifts (iOS does this).
    def swipe(dx, dur, end):
        touch('touchStart', cx - dx / 2, cy)
        n = max(3, round(dur / 16))
        for i in range(1, n + 1): touch('touchMove', cx - dx / 2 + dx * i / n, cy + (i % 3)); pg.wait_for_timeout(dur / n)
        touch(end, 0, 0); pg.wait_for_timeout(1000)
        return pg.evaluate("document.querySelector('#origin-scene').dataset.origin")
    check('02 carousel: a short fast flick (34 px / 50 ms) changes the origin', swipe(34, 50, 'touchEnd') == 'amazonas')
    check('02 carousel: a 90 px swipe cancelled by the OS as the finger lifts still counts', swipe(-90, 150, 'touchCancel') == 'cajamarca')
    ctx.close()
    # --- Video not usable (blocked): the same shot is drawn from the image sequence -------------------------------------
    for label, blocked, want_ext, want_n in [('AVIF', ['**/*.mp4'], 'avif', 121), ('WebP (no AVIF either)', ['**/*.mp4', '**/*.avif'], 'webp', 61)]:
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
        for pattern in blocked:
            ctx.route(pattern, lambda route: route.abort())
        pg = ctx.new_page(); sq = []
        pg.on('request', lambda r: sq.append(r.url) if 'hero-seq' in r.url and r.url.endswith(('.avif', '.webp')) else None)
        goto(pg); pg.wait_for_timeout(8000)
        mid = []
        for f in [.5, 1.0]:
            scene_scroll(pg, '#direction-a', f); pg.wait_for_timeout(1500)
            mid.append(pg.evaluate("(() => { const c = document.querySelector('.hs-seq'); const d = c.getContext('2d').getImageData(c.width / 2, c.height / 3, 1, 1).data; return [...d].slice(0, 3); })()"))
        media_state = pg.evaluate("document.querySelector('#direction-a').dataset.media + ' ' + document.querySelector('#direction-a').className")
        check(f'video blocked ({label}): sequence takes over, loads {want_n} {want_ext} frames and repaints with the scroll',
              'sequence' in media_state and 'has-seq' in media_state and len({u for u in sq if u.endswith('.' + want_ext)}) == want_n and mid[0] != mid[1] and sum(mid[1]) > 0, [media_state, len(sq), mid])
        ctx.close()

    # --- Link-preview tags (Open Graph / Twitter) and the share image ------------------------------------------------------
    pg = b.new_page(viewport={'width': 1440, 'height': 900}); goto(pg)
    og = pg.evaluate("Object.fromEntries([...document.querySelectorAll('meta[property^=\"og:\"], meta[name^=\"twitter:\"]')].map(m => [m.getAttribute('property') || m.name, m.content]))")
    img_ok = pg.evaluate("fetch((document.querySelector('meta[property=\"og:image\"]').content).replace(/^https:\/\/[^/]+\/[^/]+\//, '/')).then(r => r.ok && r.headers.get('content-type').includes('image/jpeg'))")
    check('share tags: demo-marked title, absolute 1200x630 JPEG image that exists, large-image card',
          og.get('og:title', '').startswith('Demo') and og.get('og:image', '').startswith('https://') and og.get('og:image', '').endswith('/assets/og-share.jpg')
          and og.get('og:image:width') == '1200' and og.get('og:image:height') == '630' and og.get('twitter:card') == 'summary_large_image' and img_ok, [og.get('og:title'), og.get('og:image'), img_ok])
    pg.close()

    # --- PDP entries from the hero -----------------------------------------------------------------------
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=1); pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e))); goto(pg)
    pg.click('.hero-peru .buy-button'); pg.wait_for_function('!document.querySelector("#producto-amazonas").hidden')
    check('hero CTA opens the Amazonas PDP', pg.evaluate("document.getElementById('product-title').textContent") == 'Amazonas')
    pg.click('#producto-amazonas [data-product-back]'); pg.wait_for_timeout(300)
    pg.evaluate('scrollTo(0, 0)'); pg.wait_for_timeout(300)
    pg.click('.hero-peru .hero-pack-entry'); pg.wait_for_function('!document.querySelector("#producto-ahorrador").hidden')
    check('hero pack entry opens the El Ahorrador PDP', pg.evaluate("document.getElementById('pack-title').textContent") == 'El Ahorrador')
    check('PDP interactions without page errors', not errs, errs)
    ctx.close()

    # --- B unchanged against the 2026-09-29 baseline ------------------------------------------------------
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
    # --- L29: this round --------------------------------------------------------------------------------------
    for name, w, h in [('desktop', 1440, 900), ('mobile', 390, 844)]:
        mob = w <= 760
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, is_mobile=mob, has_touch=mob); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); goto(pg, '?motion=off'); pg.wait_for_timeout(800)
        small = pg.evaluate(SMALL.replace("c.visibility === 'hidden'", "c.visibility === 'hidden' || !el.getClientRects().length"), '.home-nav, #home-main, .home-footer')
        check(f'{name} L29 no visible text < 11 px anywhere in the home (header, sections, footer)', not small, small)
        icons = pg.evaluate("""[...document.querySelectorAll('.footer-links a')].map(a => { const i = a.querySelector('.icon'); if (!i) return null; const r = a.getBoundingClientRect(), k = i.getBoundingClientRect();
          return {t: a.textContent.trim(), inside: k.left >= r.left && k.right <= r.right + 1 && k.top >= r.top && k.bottom <= r.bottom, w: Math.round(k.width), h: Math.round(r.height)}; }).filter(Boolean)""")
        check(f'{name} L29 footer: external icons sit inside their links, on the same line', icons and all(i['inside'] and i['w'] < 20 and i['h'] <= 48 for i in icons), icons)
        txt = pg.evaluate("document.querySelector('#home-main').innerText")
        # The 02 carousel position («01 / 05») is a counter, not a section number.
        num = pg.evaluate("(() => { const c = document.querySelector('.origin-count'), keep = c.textContent; c.textContent = ''; const t = document.querySelector('#home-main').innerText; c.textContent = keep; return t; })()")
        check(f'{name} L29 no section numbering (NN / ...) left in the home', not re.search(r'(^|\n)\s*0\d\s*/', num), re.findall(r'0\d\s*/[^\n]{0,30}', num))
        faq = pg.evaluate("document.querySelector('.close-faq').textContent")
        check(f'{name} L29 copy: «justo antes de enviarlo» once, «Para tus días» gone, FAQ «¿Qué molienda elijo?» kept',
              txt.lower().count('justo antes de enviarlo') == 1 and 'Para tus días' not in txt and '¿Qué molienda elijo?' in faq, txt.lower().count('justo antes de enviarlo'))
        heads = pg.evaluate("['reviews-title', 'faq-title', 'explore-title'].map(id => document.getElementById(id).tagName)")
        check(f'{name} L29 reviews, FAQ and explore titles are h2', heads == ['H2', 'H2', 'H2'], heads)
        rl = pg.evaluate("(() => { const a = document.querySelector('.close-reviews .close-link'); return [a.href, a.target, a.textContent.trim()]; })()")
        check(f'{name} L29 reviews link names its destination (Amazonas page of the official store)', rl[0] == 'https://www.artidororodriguez.com/products/cafe-amazonas' and rl[1] == '_blank' and 'Amazonas' in rl[2], rl)
        places = pg.evaluate("""[...document.querySelectorAll('.seat-place')].map(p => ({name: p.querySelector('h3').textContent, address: p.querySelector('.seat-place-address').textContent,
          hours: [...p.querySelectorAll('.seat-hours div')].map(d => d.querySelector('dt').textContent + ' ' + d.querySelector('dd').textContent), maps: p.querySelector('a').href}))""")
        want = [{'name': 'Tarata', 'address': 'Calle Tarata 285, Miraflores', 'hours': ['Lunes a sábado 08:00 a.m. – 09:00 p.m.', 'Domingo 09:00 a.m. – 03:00 p.m.'], 'maps': 'https://maps.app.goo.gl/8obmU6zC2Uh49pyy8'},
                {'name': 'La Mar', 'address': 'Av. Mariscal La Mar 342, Miraflores', 'hours': ['Lunes a sábado 07:30 a.m. – 09:00 p.m.', 'Domingo Cerrado'], 'maps': 'https://maps.app.goo.gl/SBhmFixmTuRCkyPt8'}]
        check(f'{name} L29 04: two cafés with the official address, hours and map link', places == want, places)
        kick = pg.evaluate("document.querySelector('#seat-scene .home-kicker').textContent")
        check(f'{name} L29 04 kicker «Nos vemos en Miraflores»', kick == 'Nos vemos en Miraflores', kick)
        pg.evaluate("document.querySelector('#seat-scene').scrollIntoView()"); pg.wait_for_timeout(500)
        pg.locator('#seat-scene').screenshot(path=str(CAP / f'{name}-04.png'))
        for sel, stem in [('.close-reviews', 'reviews'), ('#shop', 'shop-head')]:
            pg.evaluate(f"document.querySelector('{sel}').scrollIntoView()"); pg.wait_for_timeout(300)
            pg.screenshot(path=str(CAP / f'{name}-{stem}.png'))
        pg.evaluate("scrollTo(0, document.documentElement.scrollHeight)"); pg.wait_for_timeout(300)
        pg.screenshot(path=str(CAP / f'{name}-footer.png'))
        # 02: the CTA icon tells the internal destination (Amazonas demo PDP) from the external ones (official store)
        pg.evaluate("document.querySelector('#origin-scene').scrollIntoView()"); pg.wait_for_timeout(300)
        ic = [pg.evaluate("document.querySelector('.origin-buy .icon').className")]
        pg.click('.origin-next'); pg.wait_for_timeout(1200)
        ic.append(pg.evaluate("document.querySelector('.origin-buy .icon').className"))
        href = pg.evaluate("document.querySelector('.origin-buy').href")
        check(f'{name} L29 02 CTA icon: arrow for Amazonas (demo PDP), external for the other origins', 'icon-arrow' in ic[0] and 'icon-ext' not in ic[0] and 'icon-ext' in ic[1] and 'icon-arrow' not in ic[1] and 'cafe-amazonas' not in href, [ic, href])
        check(f'{name} L29 no page errors', not errs, errs)
        ctx.close()
    # 04 title not covered by a photo, and no horizontal overflow, across widths (desktop and tablet compositions)
    for w, h in [(320, 640), (360, 740), (768, 1024), (900, 900), (1024, 768), (1051, 800), (1280, 800), (1440, 900), (1920, 1080)]:
        pg = b.new_page(viewport={'width': w, 'height': h}); goto(pg, '?motion=off'); pg.wait_for_timeout(300)
        g = pg.evaluate("""(() => { const sp = document.querySelectorAll('#seat-title span'); const r = document.createRange(); r.selectNodeContents(sp[sp.length - 1]); const t = r.getBoundingClientRect();
          const f = document.querySelector('.seat-facade').getBoundingClientRect(), i = document.querySelector('.seat-interior').getBoundingClientRect(), v = document.querySelector('.seat-visit').getBoundingClientRect();
          const hit = b => b.left < t.right && b.right > t.left && b.top < t.bottom && b.bottom > t.top;
          return {coveredByFacade: hit(f), coveredByInterior: hit(i), facadeAboveVisit: f.bottom <= v.top, overflow: document.documentElement.scrollWidth - innerWidth}; })()""")
        if w > 760:
            check(f'{w}x{h} L29 04: «asiento.» not covered by a photo; facade clear of the café cards', not g['coveredByFacade'] and not g['coveredByInterior'] and g['facadeAboveVisit'], g)
        check(f'{w}x{h} L29 no horizontal overflow', g['overflow'] == 0, g['overflow'])
        pg.close()
    b.close()

json.dump({'chromium': version, 'url': URL, 'checks': checks}, open(ROOT / 'checks.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(sum(c['passed'] for c in checks), '/', len(checks))
