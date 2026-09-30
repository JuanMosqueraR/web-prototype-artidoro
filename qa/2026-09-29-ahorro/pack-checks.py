"""Pack-specific integration. Chromium DPR 1; no cart or purchase requests.
Writes results and baseline captures here; exploratory sizes in C:/tmp.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
URL='http://127.0.0.1:4175/'
variants=json.loads((ROOT.parents[1]/'src/ahorrador-variants.json').read_text())['variants']
checks=[];geometry=[]
def check(name,value,detail=None):
    checks.append(dict(name=name,passed=bool(value),detail=detail))
    if not value: print('FAIL',name,detail,flush=True)
def shown(page):
    page.wait_for_function('!document.querySelector("#producto-ahorrador").hidden')
    page.wait_for_timeout(100)
def home(page):
    page.wait_for_function('!document.querySelector("#home-main").hidden')
    page.wait_for_timeout(100)
with sync_playwright() as p:
    b=p.chromium.launch();version=b.version
    for name,w,h in [('desktop',1440,900),('mobile',390,844)]:
        page=b.new_page(viewport=dict(width=w,height=h),device_scale_factor=1)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(URL);page.evaluate('document.fonts.ready')
        check(name+' no initial pack images/video',not any('ahorrador-' in u or '.mp4' in u for u in page.evaluate('performance.getEntriesByType("resource").map(r=>r.name)')))
        hero=page.locator('.hero-pack-entry').bounding_box()
        check(name+' pack entry first viewport',hero['y']+hero['height']<=h,hero)
        page.locator('.hero-pack-entry').click();shown(page)
        check(name+' hero pack route',page.url.endswith('#producto-ahorrador'))
        page.locator('#producto-ahorrador [data-product-back]').click();home(page)
        check(name+' return focuses hero pack',page.locator('.hero-pack-entry').evaluate('(e)=>e===document.activeElement'))
        page.locator('#origin-scene').evaluate('(e)=>e.scrollIntoView({behavior:"instant"})')
        page.locator('.origin-row-main[data-origin="cusco"]').click()
        page.wait_for_function('document.querySelector("#origin-scene").dataset.origin==="cusco"')
        page.locator('.origin-pack-entry').click();shown(page)
        check(name+' 02 does not configure pack',page.locator('#pack-bag-1').input_value()=='Amazonas' and page.locator('#pack-bag-2').input_value()=='Cajamarca' and page.locator('#pack-bag-3').input_value()=='Puno')
        page.locator('#producto-ahorrador [data-product-back]').click();home(page)
        check(name+' pack roundtrip retains Cusco',page.locator('#origin-scene').get_attribute('data-origin')=='cusco')
        page.locator('.store-menu summary').click();page.locator('.store-menu [data-pack-pdp]').click();shown(page)
        check(name+' menu opens pack',page.url.endswith('#producto-ahorrador'))
        for v in variants:
            for i,value in enumerate(v['options'],1): page.select_option('#pack-bag-'+str(i),value)
            link=page.locator('.pack-continue')
            check(name+' variant '+str(v['id']),link.get_attribute('href').endswith('?variant='+str(v['id'])) and page.locator('#producto-ahorrador .product-price').inner_text()==f'S/ {v["price"]/100:.2f}' and page.locator('.pack-selection').inner_text()==' · '.join(v['options']) and link.get_attribute('aria-disabled')=='false')
        page.locator('#pack-bag-1').focus();page.keyboard.press('Home');page.keyboard.press('ArrowDown');page.keyboard.press('Enter')
        check(name+' native select keyboard',page.locator('#pack-bag-1').input_value()=='Villa Rica')
        page.locator('#pack-bag-1').evaluate('(e)=>{e.value="missing";e.dispatchEvent(new Event("change",{bubbles:true}))}')
        check(name+' missing combination blocks purchase',page.locator('.pack-continue').get_attribute('href') is None and page.locator('.pack-continue').get_attribute('aria-disabled')=='true')
        page.select_option('#pack-bag-1','Amazonas')
        check(name+' valid selection recovers',page.locator('.pack-continue').get_attribute('href') is not None)
        page.locator('.nav-buy').click();home(page)
        page.locator('.pack-feature .catalog-link').click();shown(page)
        check(name+' 05 opens pack',page.url.endswith('#producto-ahorrador'))
        check(name+' no script errors',not errors,errors)
        page.close()
    for w,h in [(1440,900),(390,844),(390,700),(360,740),(768,1024),(1024,900)]:
        page=b.new_page(viewport=dict(width=w,height=h),device_scale_factor=1)
        page.goto(URL+'#producto-ahorrador');shown(page);page.evaluate('document.fonts.ready')
        page.locator('[data-pack-src]').evaluate_all('async imgs=>Promise.all(imgs.map(i=>i.decode()))')
        cta=page.locator('.pack-continue').bounding_box();geometry.append(dict(viewport=[w,h],cta=cta))
        check(f'{w}x{h} pack CTA visible',cta['y']+cta['height']<=h,cta)
        check(f'{w}x{h} no overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        check(f'{w}x{h} direct pack no video',page.locator('video').get_attribute('src') is None)
        check(f'{w}x{h} example caption visible',page.locator('.pack-visual figcaption').is_visible())
        if (w,h) in [(1440,900),(390,844)]:
            name='desktop' if w==1440 else 'mobile'
            page.screenshot(path=str(ROOT/'after'/f'{name}-pack-top.png'))
            page.screenshot(path=str(ROOT/'after'/f'{name}-pack.png'),full_page=True)
        page.reload();shown(page)
        check(f'{w}x{h} reload default',page.locator('#pack-bag-3').input_value()=='Puno')
        page.locator('#producto-ahorrador [data-product-back]').click();home(page)
        check(f'{w}x{h} direct return 05',page.url.endswith('#shop'))
        if (w,h)==(390,844):
            for region,route in [('#shop',''),('#producto-ahorrador','#producto-ahorrador')]:
                page.goto(URL+route)
                if route: shown(page)
                page.locator(region).evaluate('e=>e.scrollIntoView({behavior:"instant"})')
                page.locator(region).evaluate('e=>{let els=[...e.querySelectorAll("*")];let sizes=els.map(x=>parseFloat(getComputedStyle(x).fontSize));els.forEach((x,i)=>x.style.fontSize=sizes[i]*2+"px")}')
                check(region+' 200% text no overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.close()
    page=b.new_page(viewport=dict(width=390,height=844),java_script_enabled=False)
    page.goto(URL)
    check('No JS pack entries official',all('https://www.artidororodriguez.com/products/pack-3kg-origenes-1'==link.get_attribute('href') for link in page.locator('[data-pack-pdp]').all()))
    check('No JS PDP hidden',page.locator('#producto-ahorrador').is_hidden());page.close()
    page=b.new_page(viewport=dict(width=390,height=844))
    page.route('**/scene03-*.mp4',lambda r:r.abort());page.goto(URL)
    page.locator('#sensory-scene').evaluate('(e)=>e.scrollIntoView()')
    page.wait_for_function('document.querySelector("#sensory-scene").dataset.media==="poster"')
    check('Video failure poster remains',page.locator('.sensory-media img').evaluate('(i)=>i.complete&&i.naturalWidth>0'))
    page.locator('.sensory-top a').click();page.locator('.pack-feature .catalog-link').click();shown(page)
    check('Video failure still permits pack purchase',page.locator('.pack-continue').get_attribute('href') is not None)
    page.close();b.close()
report=dict(browser=version,dpr=1,date='2026-09-29',checks=checks,geometry=geometry,passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks))
(ROOT/'pack-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(passed=report['passed'],failed=report['failed'],geometry=geometry)))
if report['failed']: raise SystemExit(1)
