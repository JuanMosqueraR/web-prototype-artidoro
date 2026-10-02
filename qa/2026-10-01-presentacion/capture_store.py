"""Read-only visit to the official store: screenshots for the deck («Hoy») and evidence to re-check the diagnosis findings."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / 'store'  # screenshots stay out of the repo unless copied to deliverables/presentacion/
OUT.mkdir(exist_ok=True)
BASE = 'https://www.artidororodriguez.com'
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1'
EVIDENCE = r"""() => {
  const vis = e => { const r = e.getBoundingClientRect(); const c = getComputedStyle(e); return r.width && r.height && c.visibility !== 'hidden' && c.display !== 'none'; };
  const inFold = e => { const r = e.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0; };
  const texts = [...document.querySelectorAll('h1, h2, .heading, [class*="hero"] p')].filter(vis).filter(inFold).map(e => e.innerText.trim()).filter(Boolean).slice(0, 8);
  const prices = [...document.querySelectorAll('[class*="price"], sale-price, regular-price')].filter(vis).filter(inFold).map(e => e.innerText.trim()).filter(Boolean).slice(0, 6);
  const buttons = [...document.querySelectorAll('a, button')].filter(vis).filter(inFold).map(e => e.innerText.trim()).filter(t => /compr|agreg|añad|carrito|explor/i.test(t)).slice(0, 6);
  const atc = [...document.querySelectorAll('button')].find(b => /agregar|añadir|carrito|comprar/i.test(b.innerText));
  const stars = document.querySelector('.jdgm-prev-badge, .jdgm-widget');
  return {url: location.pathname, foldTexts: texts, foldPrices: prices, foldButtons: buttons,
          atcTop: atc ? Math.round(atc.getBoundingClientRect().top + scrollY) : null, atcText: atc ? atc.innerText.trim() : null,
          starsTop: stars ? Math.round(stars.getBoundingClientRect().top + scrollY) : null, starsText: stars ? stars.innerText.trim().slice(0, 40) : null,
          bodyHas: {envio: /env[ií]o|delivery/i.test(document.body.innerText), devol: /devoluci/i.test(document.body.innerText), garant: /garant/i.test(document.body.innerText), cuotas: /cuotas/i.test(document.body.innerText)},
          pageH: document.documentElement.scrollHeight};
}"""


def close_popups(pg):
    for sel in ['text=No gracias', 'button[aria-label*="Cerrar" i]', 'button[aria-label*="close" i]', '.needsclick button']:
        try:
            el = pg.locator(sel).first
            if el.is_visible(timeout=500): el.click(timeout=1000); pg.wait_for_timeout(400)
        except Exception:
            pass
    pg.keyboard.press('Escape')


with sync_playwright() as p:
    b = p.chromium.launch()
    report = {}
    for name, vp, mob in [('mobile', {'width': 390, 'height': 844}, True), ('desktop', {'width': 1440, 'height': 900}, False)]:
        ctx = b.new_context(viewport=vp, device_scale_factor=2 if mob else 1, is_mobile=mob, has_touch=mob, user_agent=UA if mob else None, locale='es-PE')
        pg = ctx.new_page()
        for slug, path in [('home', '/'), ('coleccion', '/collections/cafe'), ('pdp', '/products/cafe-amazonas'), ('pack', '/products/pack-3kg-origenes-1')]:
            pg.goto(BASE + path, wait_until='load', timeout=90000); pg.wait_for_timeout(5000)
            close_popups(pg); pg.wait_for_timeout(800)
            pg.screenshot(path=str(OUT / f'{name}-{slug}.png'))
            report[f'{name}-{slug}'] = pg.evaluate(EVIDENCE)
            if slug == 'pdp' or slug == 'pack':
                pg.screenshot(path=str(OUT / f'{name}-{slug}-full.png'), full_page=True)
        ctx.close()
    b.close()
(OUT.parent / 'store-evidence.json').write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=1)[:6000])
