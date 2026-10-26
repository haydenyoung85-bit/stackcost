#!/usr/bin/env python3
"""Headless overflow QA: every page at phone widths 320-430 + desktop. Usage: qa_overflow.py [site_dir] [--shots]"""
import sys, threading, http.server, functools, pathlib, json
from playwright.sync_api import sync_playwright
root = pathlib.Path(sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('--') else '/workspace/stackcost/site')
shots = '--shots' in sys.argv
out = pathlib.Path('/workspace/stackcost/screenshots/qa'); out.mkdir(parents=True, exist_ok=True)
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))

srv = http.server.ThreadingHTTPServer(('127.0.0.1', 18432), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
pages = sorted(str(p.relative_to(root)) for p in root.rglob('*.html'))
JS = """() => {
 const vw = document.documentElement.clientWidth, bad = [];
 document.querySelectorAll('body *').forEach(e => {
   if (e.closest('nav')) return;
   const r = e.getBoundingClientRect(); if (!r.width) return;
   const cs = getComputedStyle(e);
   if (cs.display==='none' || cs.visibility==='hidden') return;
   if (r.right > vw + 0.5 || r.left < -0.5) bad.push('OUT '+e.tagName+'.'+e.className+' '+Math.round(r.left)+'..'+Math.round(r.right)+' "'+(e.textContent||'').trim().slice(0,30)+'"');
   if (e.scrollWidth > e.clientWidth + 1 && /hidden|clip/.test(cs.overflowX) && e.clientWidth>0 && e.tagName!=='TABLE') bad.push('CLIP '+e.tagName+'.'+e.className+' '+e.scrollWidth+'>'+e.clientWidth);
   if (cs.textOverflow==='ellipsis') bad.push('ELLIPSIS '+e.tagName+'.'+e.className);
 });
 return {sw: document.documentElement.scrollWidth, vw, bad: bad.slice(0,8), h: document.documentElement.scrollHeight};
}"""
fails = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    for w in (320, 360, 375, 390, 414, 430, 1366):
        ctx = b.new_context(viewport={'width': w, 'height': 800}, device_scale_factor=2, is_mobile=w < 700, has_touch=w < 700)
        for pg in pages:
            page = ctx.new_page(); errs = []
            page.on('pageerror', lambda e: errs.append(str(e)))
            page.route('**/*', lambda r: r.abort() if 'goatcounter' in r.request.url or 'kit.com' in r.request.url else r.continue_())
            page.goto(f'http://127.0.0.1:18432/{pg}', wait_until='domcontentloaded'); page.wait_for_timeout(250)
            res = page.evaluate(JS)
            ok = res['sw'] <= res['vw'] and not res['bad'] and not errs
            if not ok: fails += 1
            print(('OK  ' if ok else 'FAIL'), w, pg, 'sw=%d vw=%d h=%d' % (res['sw'], res['vw'], res['h']), res['bad'] if res['bad'] else '', errs or '')
            if shots and pg in ('index.html', 'calculator.html') and w in (320, 390):
                page.screenshot(path=str(out / f"{pg.replace('/','_').replace('.html','')}_{w}.png"), full_page=(pg!='index.html'))
            page.close()
        ctx.close()
    b.close()
print('FAILS', fails); sys.exit(1 if fails else 0)
