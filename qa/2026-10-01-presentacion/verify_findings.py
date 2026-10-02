"""Re-check, read-only, the diagnosis findings (22.09) against the official store on 01.10."""
import json
from playwright.sync_api import sync_playwright

UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1'
B = 'https://www.artidororodriguez.com'
out = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, user_agent=UA, locale='es-PE'); pg = ctx.new_page()
    pg.goto(B + '/', wait_until='load', timeout=90000); pg.wait_for_timeout(4000)
    out['home'] = pg.evaluate("""() => {
      const txt = document.body.innerText;
      const q = [...document.querySelectorAll('summary, button, h3, h4, .accordion__toggle')].map(e => e.innerText.trim()).filter(t => t.endsWith('?')).slice(0, 12);
      const acc = [...document.querySelectorAll('summary, details > summary, .accordion__toggle, button[aria-expanded]')].map(e => e.innerText.trim()).filter(Boolean).slice(0, 20);
      const cta = [...document.querySelectorAll('a')].find(a => /explorar los or/i.test(a.innerText));
      const cs = cta && getComputedStyle(cta);
      return {questions: q, accordions: acc, howItWorks: /c[oó]mo funciona|c[oó]mo tostamos|nuestro proceso/i.test(txt),
              cta: cta && {bg: cs.backgroundColor, border: cs.borderStyle + ' ' + cs.borderWidth, h: Math.round(cta.getBoundingClientRect().height)},
              heroVideo: !!document.querySelector('video'), sca: /83pts SCA/.test(txt)}; }""")
    pg.goto(B + '/collections/cafe', wait_until='load', timeout=90000); pg.wait_for_timeout(4000)
    out['collection'] = pg.evaluate("""() => {
      const cards = [...document.querySelectorAll('product-card, .product-card, [class*="product-card"]')].filter(c => c.getBoundingClientRect().height > 100);
      const first = cards[0];
      return {cards: cards.length, firstCardTop: first ? Math.round(first.getBoundingClientRect().top + scrollY) : null,
              withPrice: cards.filter(c => /S\\/\\.?\\s?\\d/.test(c.innerText)).length,
              sample: cards.slice(0, 3).map(c => c.innerText.replace(/\\s+/g, ' ').trim().slice(0, 90)),
              badges: [...new Set([...document.querySelectorAll('[class*="badge"], .label')].map(e => e.innerText.trim()).filter(Boolean))].slice(0, 6),
              stars: !!document.querySelector('.jdgm-prev-badge')}; }""")
    for slug in ['cafe-amazonas', 'pack-3kg-origenes-1']:
        pg.goto(B + '/products/' + slug, wait_until='load', timeout=90000); pg.wait_for_timeout(4000)
        out[slug] = pg.evaluate("""() => {
          const atc = [...document.querySelectorAll('button')].find(b => /a[ñn]adir a la cesta/i.test(b.innerText));
          const form = atc && atc.closest('form, product-form, .product-info, .product__info') || document.body;
          const zone = (atc ? (atc.closest('.product-info, .product__info, .product-info__block-list, section') || form) : form).innerText;
          const price = document.querySelector('sale-price, .price');
          const pr = price && price.getBoundingClientRect(), st = document.querySelector('.jdgm-prev-badge');
          const sticky = [...document.querySelectorAll('*')].some(e => { const c = getComputedStyle(e); return (c.position === 'fixed' || c.position === 'sticky') && /a[ñn]adir|comprar/i.test(e.innerText || '') && e.getBoundingClientRect().height < 200; });
          return {atcTop: atc ? Math.round(atc.getBoundingClientRect().top + scrollY) : null, stickyBuy: sticky,
                  zoneMentions: {envio: /env[ií]o|delivery|despach/i.test(zone), devolucion: /devoluci|cambio/i.test(zone), garantia: /garant/i.test(zone), pago: /visa|mastercard|pago seguro|yape/i.test(zone), cuotas: /cuotas/i.test(zone)},
                  starsNearPrice: !!(st && pr && Math.abs(st.getBoundingClientRect().top - pr.top) < 160), compareAt: !!document.querySelector('compare-at-price, .price--compare, s'),
                  video: !!document.querySelector('.product-gallery video, media-gallery video, video'), thumbs: document.querySelectorAll('.product-gallery__thumbnail, .product-thumbnail, [class*="thumbnail"] img').length,
                  related: /productos relacionados|tambi[eé]n te puede/i.test(document.body.innerText), molienda: /molid|molienda/i.test(document.body.innerText)}; }""")
    ctx.close(); b.close()
print(json.dumps(out, ensure_ascii=False, indent=1))
