"""Lab performance of the home (LCP, FCP, CLS, TBT approximation, weight, requests). Read-only.
Python Playwright + CDP throttling, Chromium, cache disabled, 3 runs per profile, median reported.
Usage: python qa/2026-09-30-performance/perf.py [URL]; writes perf.json next to this file.
Not Lighthouse and not field data (see README).
"""
from pathlib import Path
import json, statistics, sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
URL = sys.argv[1] if len(sys.argv) > 1 else 'https://juanmosquerar.github.io/web-prototype-artidoro/'
PROFILES = {
    'mobile-slow4g-cpu4x': dict(vw=390, vh=844, cpu=4, net=(150, 1.6 * 1024 * 1024 / 8, 750 * 1024 / 8)),
    'desktop-unthrottled': dict(vw=1440, vh=900, cpu=1, net=None),
}
INIT = """
window.__m = {lcp:0, cls:0, longtasks:[], lcpEl:''};
new PerformanceObserver(l => { for (const e of l.getEntries()) { window.__m.lcp = e.startTime; window.__m.lcpEl = (e.element && (e.element.className||e.element.tagName)) + ' ' + (e.url||''); } }).observe({type:'largest-contentful-paint', buffered:true});
new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__m.cls += e.value; }).observe({type:'layout-shift', buffered:true});
new PerformanceObserver(l => { for (const e of l.getEntries()) window.__m.longtasks.push([e.startTime, e.duration]); }).observe({type:'longtask', buffered:true});
"""
out = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, cfg in PROFILES.items():
        runs = []
        for i in range(3):
            ctx = b.new_context(viewport={'width': cfg['vw'], 'height': cfg['vh']}, device_scale_factor=1, is_mobile=cfg['vw'] < 500, has_touch=cfg['vw'] < 500)
            pg = ctx.new_page(); ctx.add_init_script(INIT)
            cdp = ctx.new_cdp_session(pg)
            cdp.send('Network.enable'); cdp.send('Network.setCacheDisabled', {'cacheDisabled': True})
            if cfg['cpu'] > 1: cdp.send('Emulation.setCPUThrottlingRate', {'rate': cfg['cpu']})
            if cfg['net']:
                lat, down, up = cfg['net']
                cdp.send('Network.emulateNetworkConditions', {'offline': False, 'latency': lat, 'downloadThroughput': down, 'uploadThroughput': up})
            reqs = []
            pg.on('response', lambda r: reqs.append((r.url, r.status)))
            sizes = {}
            cdp.on('Network.loadingFinished', lambda e: sizes.__setitem__(e['requestId'], e['encodedDataLength']))
            pg.goto(URL, wait_until='load', timeout=120000)
            pg.wait_for_timeout(4000)
            m = pg.evaluate('window.__m')
            nav = pg.evaluate("(()=>{const n=performance.getEntriesByType('navigation')[0];const f=performance.getEntriesByName('first-contentful-paint')[0];return {fcp:f?f.startTime:0,dcl:n.domContentLoadedEventEnd,load:n.loadEventEnd}})()")
            fcp = nav['fcp']
            tbt = sum(max(0, d - 50) for s, d in m['longtasks'] if s > fcp)
            runs.append({'fcp': round(fcp), 'lcp': round(m['lcp']), 'cls': round(m['cls'], 3), 'tbt': round(tbt), 'load': round(nav['load']),
                         'kb': round(sum(sizes.values()) / 1024), 'requests': len(reqs), 'bad': [u for u, s in reqs if s >= 400], 'lcpEl': m['lcpEl'][:90]})
            ctx.close()
        med = {k: statistics.median(r[k] for r in runs) for k in ('fcp', 'lcp', 'cls', 'tbt', 'load', 'kb', 'requests')}
        out[name] = {'median': med, 'runs': runs}
    b.close()
print(json.dumps(out, indent=1))
json.dump(out, open(ROOT / 'perf.json', 'w'), indent=1)
