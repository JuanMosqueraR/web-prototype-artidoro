from playwright.sync_api import sync_playwright
import json
from pathlib import Path
results=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    for handle,variant in [('pack-3kg-origenes-1', '48578579431667'), ('pack-3kg-origenes-1', '48578657255667')]:
        page=b.new_page(viewport={'width':390,'height':844})
        url='https://www.artidororodriguez.com/products/'+handle+'?variant='+variant
        response=page.goto(url,wait_until='domcontentloaded')
        page.wait_for_timeout(1200)
        values=page.locator('form[action*="/cart/add"] [name="id"]').evaluate_all('(els)=>els.map(e=>e.value)')
        result={'url':url,'status':response.status,'variant_inputs':values,'passed':variant in values}
        results.append(result);print(json.dumps(result))
        page.close()
    b.close()
Path(__file__).with_name('external-links.json').write_text(json.dumps({'date':'2026-09-28','conditions':'Read-only official product page visit. No cart or purchase. Chromium mobile viewport; not a physical iPhone.','results':results},indent=2),encoding='utf-8')
