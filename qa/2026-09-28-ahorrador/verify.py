"""Catalog/PDP integration and A/B regression. Writes only this dated directory.
Python Playwright + Pillow, Chromium DPR 1, production preview. No purchases.
Exploratory captures (extra sizes/text enlargement) stay in C:/tmp.
"""
from pathlib import Path
import json, os
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
CAP=ROOT/'after';CAP.mkdir(exist_ok=True)
URL=os.environ.get('ARTIDORO_REVIEW_URL','http://127.0.0.1:4175')
checks=[];geometry=[];pixels=[];historical=[]
variants=json.loads((ROOT.parents[1]/'src/amazonas-variants.json').read_text())['variants']
old=json.loads((ROOT.parent/'measurements.json').read_text())
def check(name,ok,detail=None):
    checks.append({'name':name,'passed':bool(ok),'detail':detail})
    if not ok: print('FAIL',name,detail,flush=True)
def ready(page):
    page.evaluate('document.fonts.ready')
def enter(page,selector):
    page.locator(selector).evaluate('(e)=>e.scrollIntoView({behavior:"instant",block:"start"})')
def decoded(page,selector):
    if selector=='#shop':
        page.wait_for_function('[...document.querySelectorAll("#shop [data-catalog-src]")].every(i=>i.hasAttribute("src"))')
    page.locator(selector+' img[src]').evaluate_all('async imgs=>Promise.all(imgs.map(i=>{i.loading="eager";return i.decode()}))')
def wait_product(page):
    page.wait_for_function('!document.querySelector("#producto-amazonas").hidden')
    page.wait_for_timeout(80)
def wait_home(page):
    page.wait_for_function('document.querySelector("#producto-amazonas").hidden')
    page.wait_for_timeout(80)

with sync_playwright() as p:
    b=p.chromium.launch();version=b.version
    for name,w,h in [('desktop',1440,900),('mobile',390,844)]:
        for direction in ['a','b']:
            for off in [False,True]:
                page=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                page.goto(URL+'/'+direction+'/'+('?motion=off' if off else ''));ready(page)
                hero=page.locator('#direction-'+direction);decoded(page,'#direction-'+direction)
                for frame in ['initial','expanded']:
                    if frame=='expanded':
                        hero.locator('[data-reveal]').click();page.wait_for_timeout(900)
                    stem=f'{direction}-{name}-{"reduced" if off else "motion"}-{frame}'
                    target=CAP/(stem+'.png');page.screenshot(path=str(target))
                    cta=hero.locator('.buy-button').bounding_box()
                    check(stem+' CTA visible',cta['y']>=0 and cta['y']+cta['height']<=h,cta)
                    check(stem+' no overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                    prior=next(x for x in old if x['test']==f'{direction.upper()} {name} {"after" if frame=="expanded" else "before"}')
                    historical.append({'state':stem,'cta_delta':{k:round(cta[k]-prior['cta'][k],4) for k in ['x','y','width','height']}})
                    before=Image.open(ROOT.parent/'2026-09-28-catalog-pdp'/'after'/(stem+'.png')).convert('RGB');after=Image.open(target).convert('RGB')
                    # A navigation intentionally changes; compare the unchanged hero below it.
                    crop=(0,(64 if w<=760 else 72) if direction=='a' else 0,w,(710 if w<=760 else 745) if direction=='a' else h)
                    diff=ImageChops.difference(before.crop(crop),after.crop(crop))
                    changed=sum(1 for rgb in diff.getdata() if max(rgb)>0);maximum=max(v[1] for v in diff.getextrema())
                    result={'state':stem,'changed':changed,'max_channel':maximum,'crop':crop};pixels.append(result)
                    check(stem+' hero unchanged',changed<=w*h*.0005 and maximum<=16,result)
                if direction=='b':
                    check(f'{name} B home/PDP hidden',page.locator('#shop').is_hidden() and page.locator('#producto-amazonas').is_hidden())
                    check(f'{name} B media absent',page.locator('video').get_attribute('src') is None)
                check(f'{name} {direction} errors',not errors,errors);page.close()

        page=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(URL);ready(page)
        # Hero entry and back, preserving history and focus.
        page.locator('.hero-peru .buy-button').click();wait_product(page)
        check(name+' hero opens PDP',page.url.endswith('#producto-amazonas'))
        page.locator('#producto-amazonas [data-product-back]').click();wait_home(page)
        check(name+' return hero restores focus',page.locator('.hero-peru .buy-button').evaluate('(e)=>e===document.activeElement'))
        enter(page,'#origin-scene')
        for key in ['cajamarca','villa-rica','cusco','puno','amazonas']:
            page.locator('.origin-row-main[data-origin="'+key+'"]').click()
            page.wait_for_function('(k)=>document.querySelector("#origin-scene").dataset.origin===k',arg=key)
            check(name+' '+key+' correct destination',page.locator('.origin-buy').get_attribute('href').endswith('/cafe-'+key))
            check(name+' '+key+' decoded',page.locator('.origin-bag[data-origin="'+key+'"]').evaluate('(i)=>i.complete&&i.naturalWidth>0'))
        y=page.evaluate('scrollY')
        page.locator('.origin-buy').click();wait_product(page)
        for v in variants:
            page.locator(f'input[name="size"][value="{v["option1"]}"]').locator('..').click()
            page.locator(f'input[name="grind"][value="{v["option2"]}"]').locator('..').click()
            cta=page.locator('#producto-amazonas .product-continue')
            check(name+' variant '+str(v['id']),cta.get_attribute('href').endswith('?variant='+str(v['id'])) and page.locator('#producto-amazonas .product-price').inner_text()==f'S/ {v["price"]/100:.2f}' and cta.get_attribute('aria-disabled')==str(not v['available']).lower())
        page.go_back();wait_home(page)
        check(name+' back preserves 02 scroll',abs(page.evaluate('scrollY')-y)<2)
        check(name+' back preserves 02 selection',page.locator('#origin-scene').get_attribute('data-origin')=='amazonas')
        page.go_forward();wait_product(page)
        check(name+' forward retains variant',page.locator('#producto-amazonas .product-continue').get_attribute('href').endswith(str(variants[-1]['id'])))
        page.locator('.nav-buy').click();wait_home(page)
        check(name+' PDP header buy reaches 05',abs(page.locator('#shop').bounding_box()['y']-(76 if w<=760 else 88))<2)
        # Native dropdown: keyboard, Escape, outside click, and navigation.
        page.locator('.store-menu summary').focus();page.keyboard.press('Enter')
        check(name+' store menu keyboard',page.locator('.store-menu').get_attribute('open') is not None)
        page.keyboard.press('Escape')
        check(name+' store menu Escape focus',page.locator('.store-menu').get_attribute('open') is None and page.locator('.store-menu summary').evaluate('(e)=>e===document.activeElement'))
        page.locator('.store-menu summary').click();page.locator('#shop-title').click()
        check(name+' store menu outside close',page.locator('.store-menu').get_attribute('open') is None)
        page.locator('.store-menu summary').click();page.locator('.store-menu a[href="#origin-scene"]').click()
        check(name+' store origins link',abs(page.locator('#origin-scene').bounding_box()['y']-(76 if w<=760 else 88))<2)
        # 03 untouched: seek after PDP home roundtrip and correct shortcut.
        enter(page,'#sensory-scene')
        page.wait_for_function('document.querySelector("#sensory-scene").classList.contains("is-cinematic")')
        for progress in [.1,.75,.3]:
            page.evaluate('(p)=>{const s=document.querySelector("#sensory-scene");scrollTo(0,s.offsetTop-(innerWidth<=760?64:72)+(s.offsetHeight-s.querySelector(".sensory-stage").offsetHeight)*p)}',progress)
            page.wait_for_timeout(450)
            current=page.locator('video').evaluate('(v)=>v.currentTime')
            check(name+' 03 seeks '+str(progress),abs(current-progress*6.981667)<.16,current)
        page.locator('.sensory-top a').click()
        check(name+' 03 reaches purchase',abs(page.locator('#shop').bounding_box()['y']-(76 if w<=760 else 88))<2)
        decoded(page,'#shop')
        check(name+' fallback HTML not exposed', '<img' not in page.locator('#shop').inner_text())
        if w<=390: check(name+' decoded 05 expanded catalog height bound',page.locator('#shop').bounding_box()['height']<=2020)
        links=page.locator('#shop a').evaluate_all('(els)=>els.map(e=>e.href)')
        check(name+' breadth links',all(any(fragment in url for url in links) for fragment in ['travel-line','pack-el-explorador','miel-de-abeja','packs-de-cafe','nanolotes','nuevos-ingresos']))
        check(name+' reviews attributed',page.locator('.catalog-quotes figcaption').count()==2)
        page.locator('#shop').screenshot(path=str(CAP/f'{name}-05.png'))
        for summary in page.locator('#shop .catalog-faq summary').all():
            summary.focus();page.keyboard.press('Enter')
            check(name+' FAQ keyboard '+summary.inner_text(),summary.locator('..').get_attribute('open') is not None)
            page.keyboard.press('Enter')
        enter(page,'#origin-scene');page.locator('.origin-row-main[data-origin="cajamarca"]').click()
        page.wait_for_function('document.querySelector("#origin-scene").dataset.origin==="cajamarca"')
        check(name+' 05 independent',links==page.locator('#shop a').evaluate_all('(els)=>els.map(e=>e.href)'))
        enter(page,'#shop');page.locator('.pack-feature [data-pack-pdp]').last.click();page.wait_for_function('!document.querySelector("#producto-ahorrador").hidden');page.locator('#producto-ahorrador [data-product-back]').click();page.wait_for_function('!document.querySelector("#home-main").hidden');enter(page,'#origin-scene');page.locator('.origin-row-main[data-origin="amazonas"]').click();page.wait_for_function('document.querySelector("#origin-scene").dataset.origin==="amazonas"');page.locator('.origin-buy').click();wait_product(page)
        page.locator('#producto-amazonas [data-product-back]').click();wait_home(page)
        check(name+' PDP preserves restored selection',page.locator('#origin-scene').get_attribute('data-origin')=='amazonas')
        check(name+' no journey JS errors',not errors,errors)
        page.close()

        # Reduced motion complete home, no-JS commercial links, direct PDP without video.
        page=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1,reduced_motion='reduce')
        page.goto(URL);ready(page)
        enter(page,'#seat-scene');page.wait_for_timeout(150);decoded(page,'#seat-scene')
        enter(page,'#shop');decoded(page,'#shop');page.evaluate('scrollTo(0,0)')
        page.screenshot(path=str(CAP/f'{name}-home.png'),full_page=True)
        check(name+' reduced motion no video',page.locator('video').get_attribute('src') is None)
        page.close()
        page=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1,java_script_enabled=False)
        page.goto(URL)
        check(name+' no JS coffee purchase',page.locator('.hero-peru .buy-button').get_attribute('href').startswith('https://'))
        check(name+' no JS catalog/reviews/FAQ',page.locator('.catalog-small').count()==2 and page.locator('#shop .catalog-faq details').count()==4 and page.locator('#producto-amazonas').is_hidden())
        enter(page,'#shop')
        check(name+' no JS catalog photos visible',all(i.is_visible() for i in page.locator('#shop noscript img').all()) and page.locator('#shop noscript img').count()==6)
        page.close()

    for w,h in [(1440,900),(390,844),(390,700),(360,740),(768,1024),(1024,900)]:
        page=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
        page.goto(URL+'/#producto-amazonas');ready(page);wait_product(page)
        cta=page.locator('#producto-amazonas .product-continue').bounding_box()
        check(f'{w}x{h} direct PDP no video',page.locator('video').get_attribute('src') is None)
        check(f'{w}x{h} PDP CTA within viewport',cta['y']+cta['height']<=h,cta)
        check(f'{w}x{h} PDP no overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        if (w,h) in [(1440,900),(390,844)]:
            name='desktop' if w==1440 else 'mobile'
            page.screenshot(path=str(CAP/f'{name}-pdp-top.png'))
            page.screenshot(path=str(CAP/f'{name}-pdp.png'),full_page=True)
        page.locator('input[name="size"][value="250g"]').focus();page.keyboard.press('ArrowRight')
        check(f'{w}x{h} variant keyboard',page.locator('#producto-amazonas .product-price').inner_text()=='S/ 60.00')
        page.reload();wait_product(page)
        check(f'{w}x{h} reload default',page.locator('#producto-amazonas .product-price').inner_text()=='S/ 39.90')
        page.locator('#producto-amazonas [data-product-back]').click();wait_home(page)
        check(f'{w}x{h} direct return origins',page.url.endswith('#origin-scene'))
        enter(page,'#shop')
        decoded(page,'#shop')
        box=page.locator('#shop').bounding_box();geometry.append({'viewport':[w,h],'shopHeight':box['height'],'pdpCTA':cta})
        if w<=390: check(f'{w}x{h} 05 expanded catalog height bound',box['height']<=2020,box['height'])
        check(f'{w}x{h} home no overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        # CSS text enlargement probe: natural growth, no clipped options or fixed-height copy.
        if w==390 and h==844:
            page.goto(URL+'/#producto-amazonas');wait_product(page)
            page.evaluate('''()=>{let els=[...document.querySelectorAll('#producto-amazonas *')];let sizes=els.map(e=>parseFloat(getComputedStyle(e).fontSize));els.forEach((e,i)=>e.style.fontSize=sizes[i]*2+'px')}''')
            check('PDP 200% text no horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.close()
    b.close()

report={'date':'2026-09-28','browser':version,'dpr':1,'url':URL,'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'geometry':geometry,'hero_pixel_comparison':pixels,'historical_cta_deltas':historical}
(ROOT/'checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'passed':report['passed'],'failed':report['failed'],'geometry':geometry}))
if report['failed']: raise SystemExit(1)
