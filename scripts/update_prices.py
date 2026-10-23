#!/usr/bin/env python3
"""Re-check StackCost price sources and flag changes. No agent needed.
Usage: python3 scripts/update_prices.py [--no-browser]
 - Linode & Vultr: public JSON APIs (exact compare).
 - Other hosts: fetch page (plain HTTP, or headless Chromium via Playwright for JS pages),
   then confirm every recorded price still appears on the page, and diff the set of $/€ prices vs last run.
Writes data/check_report.json and exits 1 if anything needs human review. Never edits hosts.json prices."""
import json,re,sys,html,urllib.request,datetime,pathlib
R=pathlib.Path(__file__).resolve().parent.parent; DATA=R/"data/hosts.json"; SNAP=R/"data/price_snapshot.json"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
JS_PAGES={"contabo","n8n","ovh","elestio","railway","digitalocean"}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=30).read().decode("utf-8","ignore")
def text(h): return html.unescape(re.sub(r"<[^>]+>"," ",re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>"," ",h)))
_b=None
def render(u,click=None):
    global _b
    from playwright.sync_api import sync_playwright
    if _b is None:
        pw=sync_playwright().start()
        try: _b=pw.chromium.launch()
        except Exception: _b=pw.chromium.launch(executable_path="/usr/bin/google-chrome")
    p=_b.new_page(user_agent=UA); p.goto(u,wait_until="domcontentloaded",timeout=45000); p.wait_for_timeout(5000)
    t=p.inner_text("body")
    if click:
        try: p.get_by_text(click,exact=True).first.click(); p.wait_for_timeout(1500); t+="\n"+p.inner_text("body")
        except Exception: pass
    p.close(); return t
def fmt(v): return f"{v:.2f}".rstrip("0").rstrip(".") if v==int(v) else f"{v:.2f}"
def present(v,t): return any(s in t for s in {f"{v:.2f}",fmt(v),f"{v:,.2f}"})
def main():
    nob="--no-browser" in sys.argv; d=json.load(open(DATA)); snap=json.load(open(SNAP)) if SNAP.exists() else {}
    issues=[];newsnap={}
    def page(id,u,click=None):
        if id in JS_PAGES and not nob: return render(u,click)
        return text(get(u))
    for h in d["hosts"]:
        try:
            if h["id"]=="linode":
                T={(t["vcpus"],t["memory"]//1024):t["price"]["monthly"] for t in json.loads(get(h["api"]))["data"] if t["class"] in("nanode","standard")}
                for p in h["plans"]:
                    n=T.get((p["vcpu"],p["ram_gb"]))
                    if n!=p["intro_price_mo"]: issues.append(f"linode {p['name']}: stored {p['intro_price_mo']} now {n}")
                continue
            if h["id"]=="vultr":
                T={x["id"]:x["monthly_cost"] for x in json.loads(get(h["api"]))["plans"]}
                for p in h["plans"]:
                    n=T.get(p["name"])
                    if n!=p["intro_price_mo"]: issues.append(f"vultr {p['name']}: stored {p['intro_price_mo']} now {n}")
                continue
            t=page(h["id"],h["url"])
            for p in h["plans"]:
                for k in("intro_price_mo","renewal_price_mo"):
                    v=p[k]
                    if v is not None and p["verified"] and not present(v,t): issues.append(f"{h['id']} {p['name']} {k}={v} no longer found on page")
            newsnap[h["id"]]=sorted(set(re.findall(r"[$€]\s?\d+(?:\.\d{2})?",t)))
        except Exception as e: issues.append(f"{h['id']}: fetch failed ({e.__class__.__name__}: {e})")
    try:
        n=d["n8n_cloud"]; t=page("n8n",n["url"],click="Monthly")
        for p in n["plans"]:
            for k in("monthly","annual_mo"):
                if p.get(k) and f"${p[k]:,}" not in t: issues.append(f"n8n {p['name']} {k}=${p[k]} not found")
        newsnap["n8n"]=sorted(set(re.findall(r"\$\s?\d[\d,]*",t)))
    except Exception as e: issues.append(f"n8n: fetch failed ({e})")
    for k,v in newsnap.items():
        if k in snap and set(v)!=set(snap[k]):
            add=sorted(set(v)-set(snap[k])); rem=sorted(set(snap[k])-set(v))
            issues.append(f"{k}: prices on page changed (+{add[:10]} -{rem[:10]})")
    json.dump(newsnap,open(SNAP,"w"),indent=1)
    rep=dict(checked=datetime.datetime.now().isoformat(timespec="minutes"),issues=issues)
    json.dump(rep,open(R/"data/check_report.json","w"),indent=1)
    print("\n".join(issues) if issues else "OK: all recorded prices still found.")
    if _b: _b.close()
    sys.exit(1 if issues else 0)
main()
