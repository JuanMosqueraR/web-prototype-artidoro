"""Real local MP4 recovery tests with Playwright network fault injection.
Not an iOS or Claude Artifacts host test. Writes this dated QA directory only.
"""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parent
URL='http://127.0.0.1:4174/'
results=[]
async def check(name,value):
    results.append({'name':name,'passed':bool(value)})
    if not value:print('FAIL',name,flush=True)
async def enter(page):
    await page.goto(URL)
    await page.evaluate('scrollTo(0,document.querySelector("#sensory-scene").offsetTop-(innerWidth<=760?64:72))')
async def scenario(browser,name,w,h):
    page=await browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
    first=True
    async def delay(route):
        nonlocal first
        if first:first=False;await asyncio.sleep(17)
        await route.continue_()
    await page.route('**/scene03-*.mp4',delay)
    await enter(page)
    await page.wait_for_function('!document.querySelector(".sensory-retry").hidden',timeout=7000)
    await check(name+': activation offered during stalled startup',True)
    await page.wait_for_function('document.querySelector("#sensory-scene").dataset.media==="poster"',timeout=13000)
    await check(name+': timeout retains media request',await page.locator('video').get_attribute('src') is not None)
    await page.screenshot(path=str(ROOT/f'{name}-waiting.png'))
    await page.wait_for_function('document.querySelector("#sensory-scene").classList.contains("is-cinematic")',timeout=10000)
    await check(name+': late video recovers without reload',True)
    await check(name+': activation hidden after recovery',await page.locator('.sensory-retry').is_hidden())
    await page.close()

    page=await browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
    broken=True
    async def fail(route):
        if broken:await route.abort()
        else:await route.continue_()
    await page.route('**/scene03-*.mp4',fail)
    await enter(page)
    await page.wait_for_function('document.querySelector(".sensory-retry").textContent.includes("Reintentar")')
    await check(name+': network error offers retry',await page.locator('.sensory-retry').is_visible())
    await page.emulate_media(reduced_motion='reduce')
    await page.wait_for_function('document.querySelector(".sensory-retry").hidden')
    await check(name+': reduced motion hides retry',await page.locator('.sensory-retry').is_hidden())
    await page.emulate_media(reduced_motion='no-preference')
    await page.wait_for_function('!document.querySelector(".sensory-retry").hidden')
    await check(name+': retry survives preference round trip',await page.locator('.sensory-retry').is_visible())
    broken=False
    await page.locator('.sensory-retry').click()
    await page.wait_for_function('document.querySelector("#sensory-scene").classList.contains("is-cinematic")')
    await page.wait_for_timeout(250)
    await check(name+': retry resumes scroll, not continuous playback',await page.locator('video').evaluate('(v)=>v.paused'))
    await page.evaluate('const s=document.querySelector("#sensory-scene");scrollTo(0,s.offsetTop-(innerWidth<=760?64:72)+(s.offsetHeight-s.querySelector(".sensory-stage").offsetHeight)*.5)')
    await page.wait_for_timeout(500)
    await check(name+': recovered video follows scroll',abs(await page.locator('video').evaluate('(v)=>v.currentTime')-3.49)<.2)
    await page.close()

    page=await browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
    await page.add_init_script('''const original=HTMLMediaElement.prototype.addEventListener;
      HTMLMediaElement.prototype.addEventListener=function(type,...args){if(type!=="loadeddata")return original.call(this,type,...args)};''')
    await enter(page)
    await page.wait_for_function('document.querySelector("#sensory-scene").classList.contains("is-cinematic")')
    await check(name+': startup works without loadeddata handler',True)
    await page.close()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True)
        version=b.version
        await asyncio.gather(scenario(b,'desktop',1440,900),scenario(b,'mobile',390,844))
        await b.close()
    report={'conditions':'Chromium '+version+', DPR1; local production preview, 17s first-MP4 delay, aborted network then manual retry, reduced-motion change, loadeddata listener suppression. No real iOS/Artifacts validation.',
        'checks':results,'passed':sum(x['passed'] for x in results),'failed':sum(not x['passed'] for x in results)}
    (ROOT/'recovery.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'passed':report['passed'],'failed':report['failed']}),flush=True)
    assert not report['failed']
asyncio.run(main())
