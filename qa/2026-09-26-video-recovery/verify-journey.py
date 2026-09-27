"""Focused browser QA for the authorized home; Python Playwright, Chromium, DPR 1.
Uses the production preview by default. Writes only this dated evidence directory.
No purchase, external navigation, baseline overwrite, or remote mutation.
"""
from pathlib import Path
import json
import os
import time
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
CAP = ROOT / 'captures'
CAP.mkdir(exist_ok=True)
URL = os.environ.get('ARTIDORO_REVIEW_URL', 'http://127.0.0.1:4174')
checks = []
def check(name, value, detail=None):
    checks.append({'name':name,'passed':bool(value),'detail':detail})
    if not value: print('FAIL:',name,detail,flush=True)

def section_top(page, selector):
    page.evaluate('(selector)=>{const el=document.querySelector(selector);scrollTo(0,el.getBoundingClientRect().top+scrollY-(innerWidth<=760?64:72))}',selector)

def images(page):
    page.evaluate('async()=>{await document.fonts.ready;await Promise.all([...document.querySelectorAll("img[src]")].map(img=>{img.loading="eager";return img.decode().catch(()=>{})}))}')

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    version = browser.version
    for name,width,height in [('desktop',1440,900),('mobile',390,844)]:
        for direction in ['a','b']:
            for off in [False,True]:
                page = browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
                errors=[]
                page.on('pageerror',lambda error:errors.append(str(error)))
                page.goto(f'{URL}/{direction}/' + ('?motion=off' if off else ''))
                page.evaluate('document.fonts.ready')
                hero=page.locator('#direction-'+direction)
                hero.locator('img[src]').evaluate_all('async imgs=>Promise.all(imgs.map(img=>{img.loading="eager";return img.decode().catch(()=>{})}))')
                for expanded in [False,True]:
                    if expanded:
                        hero.locator('[data-reveal]').click()
                        page.wait_for_timeout(850 if not off else 50)
                    frame='expanded' if expanded else 'initial'
                    mode='reduced' if off else 'motion'
                    box=hero.locator('.buy-button').bounding_box()
                    check(f'{direction}-{name}-{mode}-{frame}: CTA within viewport',box and box['y']>=0 and box['y']+box['height']<=height,box)
                    check(f'{direction}-{name}-{mode}-{frame}: no horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                    page.screenshot(path=str(CAP/f'{direction}-{name}-{mode}-{frame}.png'))
                if direction=='b':
                    check(f'b-{name}-{mode}: home hidden',page.locator('#shop').is_hidden() and page.locator('#sensory-scene').is_hidden())
                    check(f'b-{name}-{mode}: no video request',page.locator('video').get_attribute('src') is None)
                check(f'{direction}-{name}-{mode}: no JS errors',not errors,errors)
                page.close()

        # Normal interaction: deferred load, independent origins, scrubbing, purchase shortcut.
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.goto(URL)
        page.evaluate('document.fonts.ready')
        check(f'{name}: video absent on initial load',page.locator('video').get_attribute('src') is None)
        check(f'{name}: hero price visible',page.locator('.hero-price').is_visible())
        section_top(page,'#origin-scene')
        for origin in ['cajamarca','villa-rica','cusco','puno','amazonas']:
            page.locator(f'button[data-origin="{origin}"]').click()
            page.wait_for_function('(origin)=>document.querySelector("#origin-scene").dataset.origin===origin',arg=origin)
            check(f'{name}: {origin} updates purchase',page.locator('.origin-buy').get_attribute('href').endswith('/cafe-'+origin))
            check(f'{name}: {origin} bag decoded',page.locator(f'.origin-bag[data-origin="{origin}"]').evaluate('(img)=>img.complete&&img.naturalWidth>0'))
        page.screenshot(path=str(CAP/f'{name}-02.png'))
        links_before=page.locator('.shop-buy').evaluate_all('(links)=>links.map(x=>x.href)')
        page.locator('button[data-origin="cajamarca"]').click()
        page.wait_for_function('document.querySelector("#origin-scene").dataset.origin==="cajamarca"')
        check(f'{name}: 05 independent of 02',links_before==page.locator('.shop-buy').evaluate_all('(links)=>links.map(x=>x.href)'))
        section_top(page,'#sensory-scene')
        page.wait_for_function('document.querySelector("#sensory-scene").classList.contains("is-cinematic")')
        source=page.locator('video').get_attribute('src')
        check(f'{name}: responsive video selected',name in source,source)
        times=[]
        for progress,label in [(0,'start'),(.5,'middle'),(1,'end'),(.25,'reverse')]:
            page.evaluate('(p)=>{const s=document.querySelector("#sensory-scene");scrollTo(0,s.offsetTop-(innerWidth<=760?64:72)+(s.offsetHeight-s.querySelector(".sensory-stage").offsetHeight)*p)}',progress)
            page.wait_for_timeout(450)
            current=page.locator('video').evaluate('(v)=>v.currentTime')
            times.append(current)
            check(f'{name}: scroll seeks {label}',abs(current-progress*6.981667)<.15,current)
            page.screenshot(path=str(CAP/f'{name}-03-{label}.png'))
        check(f'{name}: reverse decreases time',times[-1]<times[-2])
        check(f'{name}: purchase shortcut available during 03',page.locator('.sensory-top a').is_visible())
        page.locator('.sensory-top a').click()
        check(f'{name}: purchase shortcut reaches 05',abs(page.locator('#shop').bounding_box()['y']-(64 if width<761 else 72))<25)
        page.screenshot(path=str(CAP/f'{name}-05-top.png'))
        check(f'{name}: five commercial products',page.locator('.shop-coffee').count()==5)
        check(f'{name}: all prices and purchase links',page.locator('.shop-coffee-meta strong').count()==5 and len(set(links_before))==5)
        section_top(page,'#seat-scene');images(page);page.wait_for_timeout(1350)
        page.screenshot(path=str(CAP/f'{name}-04.png'))
        check(f'{name}: no cafeteria selector',page.locator('.seat-view').count()==0)
        check(f'{name}: no JS errors across journey',not errors,errors)
        page.close()

        # Full-page still evidence: explicit reduced motion, all referenced images decoded.
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1,reduced_motion='reduce')
        page.goto(URL)
        section_top(page,'#seat-scene')
        page.wait_for_function('document.querySelector(".seat-facade img").getAttribute("src")!==null')
        images(page)
        page.evaluate('scrollTo(0,0)')
        page.screenshot(path=str(CAP/f'{name}-home-complete.png'),full_page=True)
        section_top(page,'#sensory-scene');images(page)
        page.screenshot(path=str(CAP/f'{name}-03-poster.png'))
        check(f'{name}: system reduced motion does not request video',page.locator('video').get_attribute('src') is None)
        check(f'{name}: system reduced motion does not pin',not page.locator('#sensory-scene').evaluate('(s)=>s.classList.contains("is-cinematic")'))
        check(f'{name}: poster decoded',page.locator('.sensory-media img').evaluate('(img)=>img.naturalWidth>0'))
        page.close()

        # Simulated media failure must preserve the page and buying path.
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        page.route('**/scene03-*.mp4',lambda route:route.abort())
        page.goto(URL);section_top(page,'#sensory-scene')
        page.wait_for_function('document.querySelector("#sensory-scene").dataset.media==="poster"')
        check(f'{name}: failed video collapses to poster',not page.locator('#sensory-scene').evaluate('(s)=>s.classList.contains("is-cinematic")'))
        page.locator('.sensory-top a').click()
        check(f'{name}: failed video leaves purchase reachable',page.locator('.shop-buy').first.is_visible())
        page.close()

        # No JS: content and product links must already be HTML.
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1,java_script_enabled=False)
        page.goto(URL)
        check(f'{name}: no-JS purchase links',page.locator('.shop-buy').count()==5 and page.locator('.hero-price').is_visible())
        check(f'{name}: no-JS video absent',page.locator('video').get_attribute('src') is None)
        page.close()

    # Exploratory responsive widths, not an additional browser/device support claim.
    for width,height in [(320,740),(360,800),(768,1024),(1024,768),(1920,1080)]:
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        page.goto(URL+'/?motion=off');page.evaluate('document.fonts.ready')
        check(f'exploratory {width}x{height}: no horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.close()
    browser.close()

report={'date':'2026-09-26','url':URL,'browser':version,'dpr':1,
    'conditions':'Desktop 1440x900 and mobile 390x844, emulated Chromium. Full home captures use OS reduced motion and decoded images; 03 stage captures use scroll video. No purchase executed.',
    'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks)}
(ROOT/'checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'passed':report['passed'],'failed':report['failed'],'browser':version}),flush=True)
if report['failed']:raise SystemExit(1)
