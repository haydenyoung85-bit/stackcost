from playwright.sync_api import sync_playwright
P=["index","calculator","compare/hostinger-vs-contabo-n8n","compare/n8n-cloud-vs-self-hosted"]
with sync_playwright() as p:
  b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
  for nm,vp in [("desktop",dict(width=1366,height=900)),("mobile390",dict(width=390,height=844))]:
    c=b.new_context(viewport=vp,device_scale_factor=2 if "mobile" in nm else 1,is_mobile="mobile" in nm);pg=c.new_page();errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    for u in P:
      pg.goto(f"http://localhost:8765/{u}.html");pg.wait_for_timeout(500)
      f=f"/workspace/stackcost/screenshots/{u.split('/')[-1]}-{nm}.png";pg.screenshot(path=f,full_page=True)
      print(f,pg.evaluate("document.documentElement.scrollWidth"),pg.evaluate("document.documentElement.scrollHeight"))
    print(errs)
