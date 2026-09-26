"""Focused Tarata QA. Local production preview, no external navigation or API calls.
Writes only this dated evidence directory. Old captures remain untouched.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

ROOT = Path(__file__).resolve().parent
CAP = ROOT / 'captures'
CAP.mkdir(exist_ok=True)
URL = 'http://127.0.0.1:4174/'
checks = []
def check(name, value, detail=None):
    checks.append({'name':name,'passed':bool(value),'detail':detail})
    if not value: print('FAIL', name, detail, flush=True)

def at_seat(page):
    page.evaluate('scrollTo(0,document.querySelector("#seat-scene").getBoundingClientRect().top+scrollY-(innerWidth<=760?64:72))')

def decode(page):
    page.wait_for_function('[...document.querySelectorAll("#seat-scene img[src]")].filter(i=>i.getBoundingClientRect().width>0).length===2')
    page.locator('#seat-scene img[src]').evaluate_all('imgs=>Promise.all(imgs.map(i=>i.decode()))')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    version = browser.version
    for name,w,h in [('desktop',1440,900),('mobile',390,844)]:
        page = browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
        errors = []
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(URL)
        page.evaluate('document.fonts.ready')
        initial = page.evaluate('performance.getEntriesByType("resource").filter(r=>/tarata-(facade|interior)/.test(r.name)).map(r=>r.name)')
        check(f'{name}: Tarata photographs deferred at initial load',not initial,initial)
        at_seat(page)
        page.wait_for_function('document.querySelector("#seat-scene").getAnimations({subtree:true}).some(a=>a.playState==="running")')
        check(f'{name}: entrance animation runs',True)
        decode(page)
        page.wait_for_timeout(1350)
        check(f'{name}: entrance settles',page.locator('#seat-scene').evaluate('(s)=>s.getAnimations({subtree:true}).every(a=>a.playState!=="running")'))
        check(f'{name}: photographs visible after entrance',page.locator('.seat-photo').evaluate_all('items=>items.every(i=>getComputedStyle(i).opacity==="1")'))
        interior = page.locator('.seat-interior img').evaluate('(i)=>i.currentSrc')
        check(f'{name}: correct responsive photograph',('mobile' in interior)==(name=='mobile'),interior)
        check(f'{name}: two photographs, no video/selector',page.locator('#seat-scene img').count()==2 and page.locator('#seat-scene video, #seat-scene button').count()==0)
        check(f'{name}: free document flow',page.locator('#seat-scene').evaluate('(s)=>!["fixed","sticky"].includes(getComputedStyle(s).position)'))
        check(f'{name}: map link retained',page.locator('.seat-visit a').get_attribute('href')=='https://maps.app.goo.gl/8obmU6zC2Uh49pyy8')
        check(f'{name}: viewport correct',page.evaluate('[innerWidth,innerHeight]')==[w,h])
        check(f'{name}: no horizontal overflow',page.evaluate('document.documentElement.scrollWidth===innerWidth'))
        page.screenshot(path=str(CAP/f'{name}-04-motion-rest.png'))
        page.locator('#seat-scene').screenshot(path=str(CAP/f'{name}-04-section.png'))
        page.evaluate('scrollTo(0,0)');page.wait_for_timeout(100);at_seat(page);page.wait_for_timeout(100)
        check(f'{name}: no replay on return',page.locator('#seat-scene').evaluate('(s)=>s.getAnimations({subtree:true}).every(a=>a.playState!=="running")'))
        page.locator('[data-home-motion]').click()
        at_seat(page)
        check(f'{name}: site reduced motion removes entrance animation',page.locator('.seat-photo, .home-seat-copy').evaluate_all('items=>items.every(i=>getComputedStyle(i).animationName==="none")'))
        check(f'{name}: no JS errors',not errors,errors)
        page.close()

        page = browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1,reduced_motion='reduce')
        page.goto(URL);page.evaluate('document.fonts.ready');at_seat(page);decode(page)
        check(f'{name}: OS reduced motion no entrance animation',page.locator('#seat-scene').evaluate('(s)=>s.getAnimations({subtree:true}).length===0'))
        page.screenshot(path=str(CAP/f'{name}-04-reduced.png'))
        # Capture both boundaries with settled images; no generated media request.
        page.evaluate('scrollBy(0,-230)')
        page.screenshot(path=str(CAP/f'{name}-03-to-04.png'))
        at_seat(page);page.evaluate('scrollBy(0,300)')
        page.screenshot(path=str(CAP/f'{name}-04-to-05.png'))
        page.close()

        page = browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1,java_script_enabled=False)
        page.goto(URL);at_seat(page);decode(page)
        check(f'{name}: no-JS images and link visible',page.locator('.seat-visit a').is_visible() and page.locator('.seat-photo').evaluate_all('items=>items.every(i=>getComputedStyle(i).opacity==="1")'))
        page.close()
    browser.close()

report = {'date':'2026-09-26','browser':version,'dpr':1,
    'conditions':'Chromium headless emulated 1440x900 and 390x844, local production preview, exact viewport checked. No map navigation or purchase. Motion settled after 1.35s; complete journey captured separately with reduced motion.',
    'checks':checks,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks)}
(ROOT/'tarata-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'passed':report['passed'],'failed':report['failed']}),flush=True)
if report['failed']:raise SystemExit(1)
