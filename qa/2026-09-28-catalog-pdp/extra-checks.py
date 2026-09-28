import json
from pathlib import Path
from playwright.sync_api import sync_playwright
checks=[]
def check(name,value,detail=None):
    checks.append({'name':name,'passed':bool(value),'detail':detail})
with sync_playwright() as p:
    b=p.chromium.launch()
    page=b.new_page(viewport={'width':390,'height':844})
    page.goto('http://127.0.0.1:4175/');page.evaluate('document.fonts.ready');page.wait_for_timeout(300)
    resources=page.evaluate('performance.getEntriesByType("resource").map(r=>({name:new URL(r.name).pathname,bytes:r.transferSize}))')
    check('No new catalog photos or MP4 on initial mobile load',not any('catalog-' in r['name'] or '.mp4' in r['name'] for r in resources),resources)
    page.locator('#shop').evaluate('(e)=>e.scrollIntoView()')
    page.evaluate('''()=>{let els=[...document.querySelectorAll('#shop *')];let sizes=els.map(e=>parseFloat(getComputedStyle(e).fontSize));els.forEach((e,i)=>e.style.fontSize=sizes[i]*2+'px')}''')
    overflow=page.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth,els:[...document.querySelectorAll("#shop *")].filter(e=>e.getBoundingClientRect().right>innerWidth).map(e=>({tag:e.tagName,cls:e.className,text:e.innerText?.slice(0,60)}))})')
    check('05 200% text no horizontal overflow',overflow['width']==overflow['scroll'],overflow)
    page.close()
    page=b.new_page(viewport={'width':390,'height':844})
    page.route('**/scene03-*.mp4',lambda r:r.abort())
    page.goto('http://127.0.0.1:4175/')
    page.locator('#sensory-scene').evaluate('(e)=>e.scrollIntoView()')
    page.wait_for_function('document.querySelector("#sensory-scene").dataset.media==="poster"')
    check('Video failure keeps poster',page.locator('.sensory-media img').evaluate('(i)=>i.complete&&i.naturalWidth>0'))
    page.locator('.sensory-top a').click();page.locator('[data-pdp]').click()
    page.wait_for_function('!document.querySelector("#producto-amazonas").hidden')
    check('Video failure still reaches configured purchase',page.locator('.product-continue').get_attribute('href').endswith('48502437282035'))
    # Defensive branch when a future snapshot has no matching combination.
    page.locator('input[name="size"]:checked').evaluate('(e)=>{e.value="invalid";e.dispatchEvent(new Event("change",{bubbles:true}))}')
    check('Unknown variant cannot continue',page.locator('.product-continue').get_attribute('href') is None and page.locator('.product-continue').get_attribute('aria-disabled')=='true')
    page.close();b.close()
print(json.dumps(checks))
Path(__file__).with_name('extra-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
