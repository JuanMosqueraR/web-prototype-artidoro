"""Comprobaciones del ahorro visible de El Ahorrador (L23). Preview activo en :4175."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
URL = 'http://127.0.0.1:4175/'
checks = []


def check(name, passed, detail=None):
    checks.append({'name': name, 'passed': bool(passed), 'detail': detail})


with sync_playwright() as p:
    browser = p.chromium.launch()
    for label, (w, h) in {'desktop': (1440, 900), 'mobile': (390, 844)}.items():
        page = browser.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(URL + '#shop'); page.wait_for_load_state('networkidle')
        card = page.locator('.pack-feature .pack-saving')
        # Texto normalizado: incluye la etiqueta «Precio normal» destinada a lectores de pantalla.
        norm = lambda loc: ' '.join(loc.text_content().split())
        check(f'{label} 05 saving text', norm(card) == 'Precio normal S/ 330.00 · Ahorras S/ 50', norm(card))
        check(f'{label} 05 saving visible', card.is_visible())
        check(f'{label} 05 regular price struck', page.locator('.pack-feature .pack-saving s').evaluate('e => getComputedStyle(e).textDecorationLine') == 'line-through')
        check(f'{label} 05 screen-reader label', 'Precio normal' in page.locator('.pack-feature .pack-saving s').text_content())
        page.goto(URL + '#producto-ahorrador'); page.wait_for_timeout(400)
        pdp = page.locator('[data-pack-saving]'); total = page.locator('[data-pack-total-saving]')
        check(f'{label} PDP saving initial', pdp.is_visible() and norm(pdp) == 'Precio normal S/ 330.00 · Ahorras S/ 50', norm(pdp))
        check(f'{label} PDP total saving initial', total.is_visible() and total.inner_text().strip() == '· Ahorras S/ 50', total.inner_text())
        for combo in (('Puno', 'Puno', 'Puno'), ('Cusco', 'Villa Rica', 'Amazonas')):
            for i, origin in enumerate(combo, 1):
                page.select_option(f'#pack-bag-{i}', origin)
            check(f'{label} PDP saving {"/".join(combo)}', pdp.is_visible() and 'Ahorras S/ 50' in pdp.inner_text() and total.is_visible())
        page.evaluate("""() => { const s = document.querySelector('#pack-bag-1'); const o = new Option('Inexistente', 'Inexistente'); s.add(o); s.value = 'Inexistente'; s.dispatchEvent(new Event('change', {bubbles: true})); }""")
        check(f'{label} PDP saving hidden for unavailable combination', not pdp.is_visible() and not total.is_visible())
        check(f'{label} no JS errors', not errors, errors)
        page.close()
    browser.close()

report = {'date': '2026-09-29', 'browser': '148.0.7778.96', 'dpr': 1, 'url': URL, 'checks': checks,
          'passed': sum(c['passed'] for c in checks), 'failed': sum(not c['passed'] for c in checks)}
(ROOT / 'saving-checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(report['passed'], 'passed', report['failed'], 'failed')
for c in checks:
    if not c['passed']:
        print('FAIL', c)
