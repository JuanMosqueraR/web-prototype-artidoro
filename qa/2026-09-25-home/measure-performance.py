"""Lab observations, not field CWV or a Lighthouse score. No generated media API calls."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json

results=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    for name,w,h in [('desktop',1440,900),('mobile',390,844)]:
        page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
        cdp=page.context.new_cdp_session(page)
        cdp.send('Network.enable')
        cdp.send('Network.setCacheDisabled',{'cacheDisabled':True})
        cdp.send('Network.emulateNetworkConditions',{'offline':False,'latency':150,
            'downloadThroughput':1.6*1024*1024/8,'uploadThroughput':750*1024/8})
        cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
        page.add_init_script('''window.__perf={lcp:0,cls:0,longTasks:[]};
        new PerformanceObserver(l=>{for(const e of l.getEntries())window.__perf.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});
        new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__perf.cls+=e.value}).observe({type:'layout-shift',buffered:true});
        new PerformanceObserver(l=>{for(const e of l.getEntries())window.__perf.longTasks.push(e.duration)}).observe({type:'longtask',buffered:true});''')
        page.goto('http://127.0.0.1:4174/',wait_until='load')
        page.wait_for_timeout(5000)
        data=page.evaluate('''()=>({lcp_ms:window.__perf.lcp,
            fcp_ms:performance.getEntriesByName('first-contentful-paint')[0]?.startTime,
            cls:window.__perf.cls,
            observed_blocking_ms:window.__perf.longTasks.reduce((s,x)=>s+Math.max(0,x-50),0),
            resources:performance.getEntriesByType('resource').map(x=>({name:x.name.split('/').pop(),bytes:x.transferSize,duration_ms:x.duration})),
            video_src:document.querySelector('video').getAttribute('src')})''')
        data.update({'viewport':[w,h],'device':name,'browser':browser.version,
            'conditions':'Local production preview; Chromium CDP, DPR1, cache disabled, latency 150ms, downstream 1.6Mbps, upstream 750Kbps, CPU 4x slowdown. One run; lab observations, not field CWV or Lighthouse score.'})
        data['resource_transfer_bytes']=sum(x['bytes'] for x in data['resources'])
        results.append(data)
        print(json.dumps({k:v for k,v in data.items() if k not in ['resources','conditions']}),flush=True)
        page.close()
    browser.close()
Path(__file__).with_name('performance.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
