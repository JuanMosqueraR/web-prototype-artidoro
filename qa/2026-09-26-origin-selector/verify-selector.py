"""Selector QA. Chromium/DPR1; only this new evidence directory is written.
Run after a production build served at ARTIDORO_REVIEW_URL (default :4175).
Before captures are immutable evidence from checkpoint 7b122b9.
"""
import asyncio,json,os
from pathlib import Path
from PIL import Image,ImageChops
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parent
CAP=ROOT/'after';CAP.mkdir(exist_ok=True)
SCRATCH=Path('C:/tmp/origin-selector');SCRATCH.mkdir(exist_ok=True)
URL=os.environ.get('ARTIDORO_REVIEW_URL','http://127.0.0.1:4175')
checks=[];geometry=[];historical=[]
KEYS=['amazonas','cajamarca','villa-rica','cusco','puno']
def check(name,ok,detail=None):
 checks.append({'name':name,'passed':bool(ok),'detail':detail})
 if not ok:print('FAIL',name,detail,flush=True)
async def enter(page):
 await page.goto(URL)
 await page.evaluate('document.fonts.ready')
 await page.locator('#origin-scene').evaluate('(s)=>scrollTo(0,s.offsetTop-(innerWidth<=760?64:72))')
 await page.wait_for_timeout(180)
async def selected(page,key):
 await page.wait_for_function('(key)=>document.querySelector("#origin-scene").dataset.origin===key',arg=key)
async def geometry_of(page):
 return await page.evaluate('''()=>{const rect=s=>{let r=document.querySelector(s).getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,bottom:r.bottom}};return {section:rect('#origin-scene'),cta:rect('.origin-buy'),bag:rect('.origin-slot[data-offset="0"]'),price:rect('.origin-record[aria-hidden="false"] .origin-rec-price'),tabs:[...document.querySelectorAll('.origin-row-main')].map(x=>{let r=x.getBoundingClientRect();return {y:r.y,width:r.width,height:r.height}}),overflow:document.documentElement.scrollWidth>innerWidth}}''')
async def baseline(browser):
 old=json.loads((ROOT.parent/'measurements.json').read_text())
 for name,w,h in [('mobile',390,844),('desktop',1440,900)]:
  for direction in ['a','b']:
   for off in [False,True]:
    page=await browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
    await page.goto(URL+'/?direction='+direction+('&motion=off' if off else ''))
    await page.evaluate('document.fonts.ready')
    hero=page.locator('#direction-'+direction)
    await hero.locator('img[src]').evaluate_all('async imgs=>Promise.all(imgs.map(x=>x.decode().catch(()=>{})))')
    for expanded in [False,True]:
     if expanded:
      await hero.locator('[data-reveal]').click();await page.wait_for_timeout(900)
     filename=f'{direction}-{name}-{off}-{expanded}.png'
     await page.screenshot(path=str(CAP/filename))
     bounds=await hero.bounding_box();bottom=min(h,round(bounds['y']+bounds['height']))
     difference=ImageChops.difference(Image.open(ROOT/'before'/filename).convert('RGB').crop((0,0,w,bottom)),Image.open(CAP/filename).convert('RGB').crop((0,0,w,bottom)))
     # Repeated captures of unchanged B's SVG produce 0–320 low-amplitude
     # antialias pixels in Chromium. Keep the measured delta, not an exact-byte claim.
     pixels=list(difference.getdata()) if difference.getbbox() else []
     changed=sum(max(pixel)>0 for pixel in pixels)
     peak=max((max(pixel) for pixel in pixels),default=0)
     check('baseline pixels '+filename,changed/(w*bottom)<=.0005 and peak<=16,{'changed_pixels':changed,'max_channel_delta':peak,'crop_height':bottom})
     cta=await hero.locator('.buy-button').bounding_box()
     previous=next(row for row in old if row['variant']=='direction-'+direction and row['body']['width']==w and row['expanded']==str(expanded).lower())['cta']
     historical.append({'state':filename,'cta_delta_from_historical_lab':{key:round(cta[key]-previous[key],3) for key in ['x','y','width','height']}})
     check('baseline CTA '+filename,cta['y']+cta['height']<=h)
    if direction=='b':
     check('B hides 02 '+name+str(off),await page.locator('#origin-scene').is_hidden())
    await page.close()
async def functional(browser):
 for w,h in [(390,844),(1440,900),(390,700),(360,740),(768,1024),(1023,900),(1024,768),(320,740)]:
  page=await browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1,has_touch=w<600)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  await enter(page);await page.wait_for_timeout(250)
  first=await geometry_of(page);geometry.append({'viewport':[w,h],**first})
  label=f'{w}x{h}'
  check(label+' no overflow',not first['overflow'])
  if w in [390,360,1440]:
   check(label+' CTA fits',first['cta']['bottom']<=h,first['cta'])
   check(label+' full central bag fits',first['bag']['y']>=64 and first['bag']['bottom']<=h)
  check(label+' five names in one row',len(set(round(t['y']) for t in first['tabs']))==1)
  check(label+' controls at least 44px',all(t['width']>=44 and t['height']>=44 for t in first['tabs']))
  for key in KEYS:
   await page.locator(f'.origin-row-main[data-origin="{key}"]').click();await selected(page,key);await page.wait_for_timeout(360)
   check(label+' purchase '+key,(await page.locator('.origin-buy').get_attribute('href')).endswith('/cafe-'+key))
   check(label+' matching bag '+key,await page.locator('.origin-slot[data-offset="0"]').get_attribute('data-coffee')==key)
   check(label+' decoded bag '+key,await page.locator(f'.origin-bag[data-origin="{key}"]').evaluate('(x)=>x.complete&&x.naturalWidth>0'))
   current=await geometry_of(page)
   check(label+' stable CTA '+key,abs(first['cta']['y']-current['cta']['y'])<.1)
   check(label+' stable price '+key,abs(first['price']['y']-current['price']['y'])<.1)
  await page.locator('.origin-next').click();await selected(page,'amazonas');await page.wait_for_timeout(360)
  check(label+' wrap Puno to Amazonas',True)
  if (w,h) in [(390,844),(1440,900)]:
   name='mobile' if w==390 else 'desktop'
   await page.screenshot(path=str(CAP/f'02-{name}.png'))
   await page.locator('.origin-slot[data-coffee="cajamarca"]').click();await selected(page,'cajamarca');await page.wait_for_timeout(360)
   check(label+' neighbor click',True)
   await page.screenshot(path=str(CAP/f'02-{name}-cajamarca.png'))
   await page.locator('.origin-row-main[data-origin="cajamarca"]').focus();await page.keyboard.press('ArrowRight');await selected(page,'villa-rica')
   await page.keyboard.press('End');await selected(page,'puno')
   await page.keyboard.press('Home');await selected(page,'amazonas');await page.wait_for_timeout(360)
   check(label+' keyboard right/end/home',True)
   # Mouse drag on the stage, one origin per gesture.
   box=await page.locator('.origin-stage').bounding_box();x=box['x']+box['width']/2;y=box['y']+80
   await page.mouse.move(x,y);await page.mouse.down();await page.mouse.move(x-90,y,steps=10);await page.mouse.up();await selected(page,'cajamarca');await page.wait_for_timeout(380)
   check(label+' drag advances exactly one',await page.locator('#origin-scene').get_attribute('data-origin')=='cajamarca')
   await page.locator('.origin-row-main[data-origin="amazonas"]').click();await selected(page,'amazonas');await page.wait_for_timeout(360)
   await page.screenshot(path=str(CAP/f'sequence-{name}-0.png'))
   await page.locator('.origin-row-main[data-origin="cajamarca"]').evaluate('(x)=>x.click()')
   await page.wait_for_timeout(110);await page.screenshot(path=str(CAP/f'sequence-{name}-1.png'))
   await page.wait_for_timeout(110);await page.screenshot(path=str(CAP/f'sequence-{name}-2.png'))
   await page.wait_for_timeout(220);await page.screenshot(path=str(CAP/f'sequence-{name}-3.png'))
  else:await page.screenshot(path=str(SCRATCH/f'qa-{w}-{h}.png'))
  check(label+' no JS errors',not errors,errors)
  await page.close()
async def touch(browser):
 page=await browser.new_page(viewport={'width':390,'height':844},has_touch=True,is_mobile=True)
 await enter(page)
 client=await page.context.new_cdp_session(page)
 async def swipe(x,y,dx,dy):
  await client.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
  for i in range(1,9):
   await client.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+dx*i/8,'y':y+dy*i/8}]});await page.wait_for_timeout(20)
  await client.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
 await swipe(215,320,-110,2);await selected(page,'cajamarca');await page.wait_for_timeout(400)
 check('touch horizontal swipe selects one',await page.locator('#origin-scene').get_attribute('data-origin')=='cajamarca')
 before=await page.evaluate('scrollY');await swipe(195,380,2,-150);await page.wait_for_timeout(300)
 check('touch vertical gesture scrolls page',await page.evaluate('scrollY')>before+50)
 check('touch vertical gesture keeps selection',await page.locator('#origin-scene').get_attribute('data-origin')=='cajamarca')
 await page.close()
async def loading(browser):
 for mode in ['error','slow','timeout']:
  page=await browser.new_page(viewport={'width':390,'height':844});state={'fault':True}
  async def fault(route):
   if state['fault']:
    if mode=='error':await route.abort();return
    await asyncio.sleep(.8 if mode=='slow' else 4.5)
   await route.continue_()
  await page.route('**/cusco-250g.webp',fault)
  await enter(page)
  await page.locator('.origin-row-main[data-origin="cusco"]').click()
  check(mode+' holds old product while pending',await page.locator('#origin-scene').get_attribute('data-origin')=='amazonas')
  check(mode+' holds old CTA while pending',(await page.locator('.origin-buy').get_attribute('href')).endswith('amazonas'))
  if mode=='slow':
   await page.locator('.origin-row-main[data-origin="puno"]').click();await selected(page,'puno');await page.wait_for_timeout(1100)
   check('last request wins despite late decode',await page.locator('#origin-scene').get_attribute('data-origin')=='puno')
  else:
   await page.wait_for_function('document.querySelector(".origin-status").textContent.includes("reintentar")')
   await page.wait_for_timeout(700 if mode=='timeout' else 30)
   check(mode+' keeps old state after failure',await page.locator('#origin-scene').get_attribute('data-origin')=='amazonas')
   state['fault']=False
   await page.locator('.origin-row-main[data-origin="cusco"]').click();await selected(page,'cusco')
   check(mode+' explicit retry succeeds',True)
  await page.close()
async def accessibility(browser):
 for mode in ['system','toggle','no-js','large-text']:
  page=await browser.new_page(viewport={'width':390,'height':844},java_script_enabled=mode!='no-js',reduced_motion='reduce' if mode=='system' else 'no-preference')
  await enter(page)
  if mode=='no-js':
   check('no-JS Amazonas purchase',(await page.locator('.origin-buy').get_attribute('href')).endswith('amazonas'))
   check('no-JS inactive controls hidden',await page.locator('.origin-index').is_hidden() and await page.locator('.origin-prev').is_hidden())
   check('no-JS bag visible',await page.locator('.origin-bag[data-origin="amazonas"]').is_visible())
  elif mode=='large-text':
   await page.evaluate('''()=>{const items=[...document.querySelectorAll('#origin-scene h2,#origin-scene h3,#origin-scene p,.origin-row-main,.origin-buy,.origin-catalog,.origin-rec-notes span')].map(x=>[x,parseFloat(getComputedStyle(x).fontSize),parseFloat(getComputedStyle(x).lineHeight)]);for(const [x,f,l] of items){x.style.fontSize=f*2+'px';x.style.lineHeight=(Number.isFinite(l)?l*2:f*2.4)+'px'}}''')
   check('200% text grows section',await page.locator('#origin-scene').evaluate('(s)=>s.offsetHeight')>800)
   check('200% text no horizontal overflow',await page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
   check('200% text CTA reachable',await page.locator('.origin-buy').is_visible())
   await page.screenshot(path=str(SCRATCH/'large-text.png'),full_page=True)
  else:
   if mode=='toggle':await page.evaluate('document.documentElement.classList.add("no-motion")')
   await page.locator('.origin-row-main[data-origin="puno"]').click();await selected(page,'puno')
   check(mode+' reduced motion immediate',await page.locator('.origin-slot').first.evaluate('(s)=>getComputedStyle(s).transitionDuration')=='0s')
  await page.close()
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch()
  for task in [baseline,functional,touch,loading,accessibility]:
   print('RUN',task.__name__,flush=True);await task(browser)
  await browser.close()
  report={'browser':browser.version,'dpr':1,'url':URL,'checks':checks,'geometry':geometry,'historical_lab_deltas':historical,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks)}
  (ROOT/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
  print(json.dumps({'passed':report['passed'],'failed':report['failed']}),flush=True)
  if report['failed']:raise SystemExit(1)
asyncio.run(main())
