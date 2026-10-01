"""L31 (2026-10-01): El Ahorrador as the fourth size of the Amazonas PDP, the 1 kg nudge and the discovery-only lower section.
Python Playwright, Chromium, DPR 1, production build served over HTTP. Writes only this dated directory.
Usage: ARTIDORO_REVIEW_URL=http://127.0.0.1:4192 python qa/2026-10-01-pdp-pack/verify.py
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
pack = min(v['price'] for v in PACK['variants']); compare = 33000
kilo = min(v['price'] for v in AMZ['variants'] if v['option1'] == '1kg')
checks = []


def check(name, ok, detail=None):
    checks.append({'name': name, 'passed': bool(ok), 'detail': detail})
    if not ok:
        print('FAIL', name, detail, flush=True)


SMALL = """sel => { const out = []; document.querySelector(sel).querySelectorAll('*').forEach(el => { if (el.children.length) return; const t = (el.textContent || '').trim(); if (!t) return;
  const c = getComputedStyle(el); if (c.display === 'none' || c.visibility === 'hidden' || !el.getClientRects().length) return; if (parseFloat(c.fontSize) < 11) out.push(t.slice(0, 30)); }); return out; }"""
A = '#producto-amazonas'
Q = """s => { const e = document.querySelector('#producto-amazonas ' + s); return e ? e.textContent.replace(/\\s+/g, ' ').trim() : null; }"""

with sync_playwright() as p:
    b = p.chromium.launch(); version = b.version
    for name, w, h in [('desktop', 1440, 900), ('mobile', 390, 844)]:
        mob = w <= 760
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, is_mobile=mob, has_touch=mob); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(URL + '/?motion=off'); pg.wait_for_timeout(1000)
        pg.click('.hero-peru .buy-button'); pg.wait_for_function("!document.querySelector('#producto-amazonas').hidden"); pg.wait_for_timeout(800)
        t = lambda s: pg.evaluate(Q, s)
        tier = [t('[data-pack-price]'), t('[data-pack-compare]'), t('[data-pack-kilo]'), pg.evaluate("!document.querySelector('[data-pack-badge]').hidden")]
        want = [f'S/ {pack // 100}', f'S/ {compare // 100}', f'S/ {round(pack / 3) / 100:.2f} el kilo', pack / 3 < kilo]
        check(f'{name} pack tier inside «Tamaño»: price, crossed normal price, price per kilo and «El kilo más barato» from the snapshots', tier == want, [tier, want])
        nudge = [pg.evaluate("document.querySelector('[data-pack-nudge]').hidden")]
        pg.click(f'{A} input[value="1kg"] + span'); pg.wait_for_timeout(200)
        nudge.append(pg.evaluate("document.querySelector('[data-pack-nudge]').hidden"))
        nudge.append(t('[data-pack-saving-amount]'))
        check(f'{name} 1 kg nudge appears only with 1 kg and states the official saving', nudge == [True, False, f'S/ {(compare - pack) // 100}'], nudge)
        pg.evaluate(f"document.querySelector('{A} .pdp-sizes').scrollIntoView({{block: 'center'}})"); pg.wait_for_timeout(200)
        pg.screenshot(path=str(CAP / f'{name}-1kg-nudge.png'))
        pg.click('[data-pick-pack]'); pg.wait_for_timeout(300)
        st = pg.evaluate("""(() => { const q = s => document.querySelector('#producto-amazonas ' + s); return {checked: q('input[value=pack]').checked, price: q('.product-price').textContent, yield: q('[data-yield]').textContent,
          grind: q('.pdp-grind-field').hidden, note: !q('[data-pack-note]').hidden, cta: q('.pdp-cta').textContent.trim(), internal: q('.pdp-cta').hasAttribute('data-pack-pdp') && !q('.pdp-cta').target,
          icon: q('.pdp-cta .icon').className, bar: [q('.pdp-bar-info b').textContent, q('[data-bar-price]').textContent, q('.pdp-bar a').hasAttribute('data-pack-pdp')], handoff: q('.product-handoff').textContent}; })()""")
        check(f'{name} choosing the pack: price, cups, grind hidden with its note, «Armar mi pack», internal route, bar and handoff text',
              st['checked'] and st['price'] == f'S/ {pack / 100:.2f}' and st['yield'] == '3 bolsas de 1 kg · unas 195 tazas' and st['grind'] and st['note']
              and st['cta'] == f'Armar mi pack · S/ {pack // 100}' and st['internal'] and 'icon-arrow' in st['icon'] and st['bar'] == ['El Ahorrador · 3 kg', f'S/ {pack / 100:.2f}', True]
              and st['handoff'].startswith('Te llevamos a armar tu pack'), st)
        pg.evaluate(f"document.querySelector('{A} .pdp-pack-tier').scrollIntoView({{block: 'center'}})"); pg.wait_for_timeout(200)
        pg.screenshot(path=str(CAP / f'{name}-pack-chosen.png'))
        small = pg.evaluate(SMALL, A)
        check(f'{name} no visible text < 11 px in the Amazonas PDP with the pack chosen', not small, small)
        check(f'{name} no horizontal overflow', pg.evaluate('document.documentElement.scrollWidth - innerWidth') == 0)
        # Prepare a different first bag in the pack, then come from Amazonas: bag 1 starts on Amazonas
        pg.evaluate("document.querySelector('#producto-ahorrador input[name=bag1][value=\"Puno\"]').checked = true")
        pg.click(f'{A} .pdp-cta'); pg.wait_for_function("!document.querySelector('#producto-ahorrador').hidden"); pg.wait_for_timeout(700)
        bag1 = pg.evaluate("document.querySelector('#producto-ahorrador input[name=bag1]:checked').value")
        check(f'{name} «Armar mi pack» opens the pack PDP with Amazonas in bag 1', bag1 == 'Amazonas' and pg.evaluate('location.hash') == '#producto-ahorrador', bag1)
        pg.click('#producto-ahorrador [data-product-back]'); pg.wait_for_timeout(800)
        check(f'{name} back from the pack returns to the Amazonas PDP with the pack still chosen',
              pg.evaluate('location.hash') == A and pg.evaluate("document.querySelector('#producto-amazonas input[value=pack]').checked"))
        pg.click(f'{A} input[value="250g"] + span'); pg.wait_for_timeout(200)
        v = next(x for x in AMZ['variants'] if x['option1'] == '250g' and x['option2'] == 'Grano')
        st = pg.evaluate("""(() => { const q = s => document.querySelector('#producto-amazonas ' + s); return [q('.pdp-cta').textContent.trim(), q('.pdp-cta').target, q('.pdp-cta').hasAttribute('data-pack-pdp'), q('.pdp-cta').href, q('.pdp-grind-field').hidden, q('.pdp-bar-info b').textContent, q('.pdp-bar a').target]; })()""")
        check(f'{name} back to 250 g: external CTA to the official variant, grind visible, bar restored',
              st[0] == 'Continuar en la tienda' and st[1] == '_blank' and not st[2] and st[3].endswith(f"variant={v['id']}") and not st[4] and st[5] == 'Amazonas' and st[6] == '_blank', st)
        more = pg.evaluate(f"[document.querySelector('{A} .pdp-more [data-pack-pdp]'), document.querySelectorAll('{A} .pdp-more .pdp-card').length, document.querySelectorAll('{A} .pdp-origins li').length, document.querySelector('#pdp-more-amazonas').textContent]")
        check(f'{name} lower section is discovery only: no pack card, El Explorador and the four other origins', more[0] is None and more[1] == 1 and more[2] == 4 and 'Prueba los' in more[3], more)
        check(f'{name} no page errors', not errs, errs)
        ctx.close()
    b.close()

json.dump({'chromium': version, 'url': URL, 'checks': checks}, open(ROOT / 'checks.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(sum(c['passed'] for c in checks), '/', len(checks))
