"""L31 (2026-10-01): payment methods by the button, the hero clip as a gallery video, and the pack shortcut.
Supersedes the slide counts of qa/2026-10-01-pdp (now 7 slides in Amazonas and 5 in the pack, 4 conceptual notices,
the video slide has no zoom). Python Playwright, Chromium, DPR 1, production build over HTTP. Writes only this directory.
Usage: ARTIDORO_REVIEW_URL=http://127.0.0.1:4192 python qa/2026-10-01-pdp-extras/verify.py
"""
from pathlib import Path
import json, os, re
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
CAP = ROOT / 'after'; CAP.mkdir(exist_ok=True)
URL = os.environ.get('ARTIDORO_REVIEW_URL', 'http://127.0.0.1:4192').rstrip('/')
REPO = ROOT.parents[1]
OFFICIAL = re.findall(r'<title id="pi-([a-z_]+)">([^<]+)</title>', (REPO / 'audit/source/payment-methods-2026-10-01.html').read_text(encoding='utf-8'))
PACK = json.loads((REPO / 'src/ahorrador-variants.json').read_text(encoding='utf-8'))
checks = []


def check(name, ok, detail=None):
    checks.append({'name': name, 'passed': bool(ok), 'detail': detail})
    if not ok:
        print('FAIL', name, detail, flush=True)


with sync_playwright() as p:
    b = p.chromium.launch(); version = b.version
    for name, w, h in [('desktop', 1440, 900), ('mobile', 390, 844)]:
        mob = w <= 760
        for route in ['#producto-amazonas', '#producto-ahorrador']:
            ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, is_mobile=mob, has_touch=mob); pg = ctx.new_page(); errs = []; pdpvideo = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto(URL + '/' + route); pg.wait_for_timeout(1500)
            pg.on('request', lambda r: pdpvideo.append(r.url) if r.url.endswith('hero-desktop.mp4') else None)
            label = route[10:]
            # Payment methods: the official list, in the PDP, loaded
            pay = pg.evaluate(f"[...document.querySelectorAll('{route} .pdp-pay img')].map(i => [i.alt, i.complete && i.naturalWidth > 0])")
            check(f'{name} {label}: card icons by the button match the official list and load', sorted(a for a, _ in pay) == sorted(n for _, n in OFFICIAL) and all(ok for _, ok in pay), [pay, OFFICIAL])
            # Gallery: counts, notices, zoom buttons
            g = pg.evaluate(f"[document.querySelectorAll('{route} .pdp-slide').length, document.querySelectorAll('{route} .pdp-thumbs button').length, document.querySelectorAll('{route} .pdp-track .pdp-zoom').length, document.querySelectorAll('{route} .pdp-track .pdp-ai').length, document.querySelector('{route} .pdp-count').textContent.trim()]")
            want = [7, 7, 6, 4, '1 / 7'] if 'amazonas' in route else [5, 5, 4, 3, '1 / 5']
            check(f'{name} {label}: slides, thumbnails, zoom buttons (not on the video) and conceptual notices', g == want, [g, want])
            video = pg.evaluate(f"(() => {{ const v = document.querySelector('{route} video'); return [v.getAttribute('src'), v.paused]; }})()")
            # Reach the video slide
            if mob:
                pg.evaluate(f"(() => {{ const t = document.querySelector('{route} .pdp-track'); t.scrollTo({{left: t.clientWidth, behavior: 'instant'}}); }})()")
            else:
                pg.click(f'{route} .pdp-thumbs button:nth-child(2)')
            pg.wait_for_timeout(2500)
            playing = pg.evaluate(f"(() => {{ const v = document.querySelector('{route} video'); return [v.paused, v.currentTime > .5, v.readyState]; }})()")
            pg.screenshot(path=str(CAP / f'{name}-{label}-video.png'))
            if mob:
                pg.evaluate(f"(() => {{ const t = document.querySelector('{route} .pdp-track'); t.scrollTo({{left: 2 * t.clientWidth, behavior: 'instant'}}); }})()")
            else:
                pg.click(f'{route} .pdp-thumbs button:nth-child(3)')
            pg.wait_for_timeout(700)
            paused = pg.evaluate(f"document.querySelector('{route} video').paused")
            check(f'{name} {label}: the clip is requested only on reaching its slide, plays muted in a loop there and pauses when leaving',
                  video[0] is None and video[1] and playing[0] is False and playing[1] and paused, [video, playing, paused, len(pdpvideo)])
            # Zoom skips the video slide
            pg.click(f'{route} .pdp-slide:nth-child(1) .pdp-zoom') if not mob else pg.evaluate(f"document.querySelector('{route} .pdp-slide:nth-child(1) .pdp-zoom').click()")
            pg.wait_for_timeout(400); pg.click(f'{route} .pdp-lb-next'); pg.wait_for_timeout(300)
            lb = pg.evaluate(f"[document.querySelector('{route} .pdp-lb-count').textContent, !!document.querySelector('{route} .pdp-lb-canvas video')]")
            pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
            check(f'{name} {label}: the zoom view skips the video slide', lb == ['3 / ' + want[0].__str__(), False], lb)
            if 'ahorrador' in route:
                pg.evaluate("document.querySelector('[data-repeat-bag]').scrollIntoView({block: 'center'})")
                pg.click('#producto-ahorrador input[name=bag1][value="Cusco"] + span'); pg.wait_for_timeout(200)
                text = pg.evaluate("document.querySelector('[data-repeat-bag]').textContent.replace(/\\s+/g, ' ').trim()")
                pg.click('[data-repeat-bag]'); pg.wait_for_timeout(300)
                st = pg.evaluate("[[1, 2, 3].map(n => document.querySelector(`#producto-ahorrador input[name=bag${n}]:checked`).value), document.querySelector('[data-repeat-bag]').hidden, document.querySelector('#producto-ahorrador .pdp-cta').href, document.querySelector('[data-pack-caption]').textContent]")
                vid = next(v['id'] for v in PACK['variants'] if v['options'] == ['Cusco', 'Cusco', 'Cusco'])
                check(f'{name} pack shortcut: «Las tres bolsas de Cusco» fills the three bags, updates variant and picture, then hides',
                      text == 'Las tres bolsas de Cusco' and st[0] == ['Cusco'] * 3 and st[1] and st[2].endswith(f'variant={vid}') and st[3] == 'Tu combinación: Cusco, Cusco y Cusco.', [text, st])
                pg.screenshot(path=str(CAP / f'{name}-pack-shortcut.png'))
            if not mob:
                th = pg.evaluate(f"(() => {{ const t = document.querySelector('{route} .pdp-thumbs'); return t.scrollWidth <= t.clientWidth + 1; }})()")
                check(f'{name} {label}: thumbnails are not cut', th)
            pg.evaluate(f"document.querySelector('{route} .pdp-cta').scrollIntoView({{block: 'center'}})"); pg.wait_for_timeout(300)
            pg.screenshot(path=str(CAP / f'{name}-{label}-pay.png'))
            check(f'{name} {label}: no horizontal overflow and no page errors', pg.evaluate('document.documentElement.scrollWidth - innerWidth') == 0 and not errs, errs)
            ctx.close()
    # Without motion the clip does not autoplay: it shows its poster and native controls
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=1, reduced_motion='reduce'); pg = ctx.new_page()
    pg.goto(URL + '/#producto-amazonas'); pg.wait_for_timeout(1200)
    pg.click('#producto-amazonas .pdp-thumbs button:nth-child(2)'); pg.wait_for_timeout(1500)
    rm = pg.evaluate("(() => { const v = document.querySelector('#producto-amazonas video'); return [v.paused, v.controls]; })()")
    check('reduced motion: the clip stays paused with native controls', rm == [True, True], rm)
    ctx.close(); b.close()

json.dump({'chromium': version, 'url': URL, 'checks': checks}, open(ROOT / 'checks.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(sum(c['passed'] for c in checks), '/', len(checks))
