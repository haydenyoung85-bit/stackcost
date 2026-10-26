"""One-time seed of data/hosts.json from manual verification on 2026-10-22. Values copied from source pages; null = not verified."""
import json
D="2026-10-22"
def P(name,vcpu,ram,disk,intro,renew,term,cur="USD",note=None,verified=True,disk_type=None):
    return dict(name=name,vcpu=vcpu,ram_gb=ram,storage_gb=disk,storage_type=disk_type,currency=cur,intro_price_mo=intro,renewal_price_mo=renew,term=term,verified=verified,note=note)
H=[
 dict(id="hostinger",name="Hostinger",type="vps",one_click_n8n=True,url="https://www.hostinger.com/self-hosted-n8n",affiliate_url=None,
  notes="Intro price requires 24-month prepay; renews at the listed renewal price.",plans=[
  P("KVM 1",1,4,50,6.49,11.99,"24 months prepaid",disk_type="NVMe"),P("KVM 2",2,8,100,8.79,14.99,"24 months prepaid",disk_type="NVMe"),
  P("KVM 4",4,16,200,12.99,28.99,"24 months prepaid",disk_type="NVMe"),P("KVM 8",8,32,400,25.99,49.99,"24 months prepaid",disk_type="NVMe")]),
 dict(id="contabo",name="Contabo",type="vps",one_click_n8n=True,url="https://contabo.com/en-us/n8n-hosting/",affiliate_url=None,
  notes="Intro price is 'for the first 24 months' on a 24-month term (incl. applicable taxes). Renewal shown = struck-through regular price on the same page; not explicitly labelled as renewal.",plans=[
  P("Cloud VPS 10 (n8n)",4,8,100,5.28,6.60,"24 months",disk_type="SSD",note="Renewal = regular list price (assumed)"),
  P("Cloud VPS 20 (n8n)",6,12,200,7.20,9.00,"24 months",disk_type="SSD",note="Renewal = regular list price (assumed)"),
  P("Cloud VPS 40 (n8n)",12,48,400,24.00,30.00,"24 months",disk_type="SSD",note="Renewal = regular list price (assumed)"),
  P("Cloud VPS 60 (n8n)",18,96,600,47.04,58.80,"24 months",disk_type="SSD",note="Renewal = regular list price (assumed)")]),
 dict(id="hetzner",name="Hetzner Cloud",type="vps",one_click_n8n=False,url="https://www.hetzner.com/cloud/",affiliate_url=None,
  notes="Prices EUR excl. VAT, hourly billing, no term. Only 'starting from' prices were readable; per-plan prices load client-side and were not captured. n8n is not in Hetzner's one-click app list (Docker CE / Coolify are).",plans=[
  P("Cost-Optimized (from, e.g. CX23)",2,4,40,5.99,5.99,"none (hourly)","EUR",note="'starting from' price; plan marked currently unavailable",disk_type="NVMe"),
  P("Regular Performance (from, CPX)",None,None,None,6.49,6.49,"none (hourly)","EUR",note="'starting from' price; which spec it maps to not verified",disk_type="NVMe"),
  P("CPX22",2,4,80,None,None,"none (hourly)","EUR",verified=False,note="Price not captured",disk_type="NVMe")]),
 dict(id="ovh",name="OVHcloud",type="vps",one_click_n8n=None,url="https://us.ovhcloud.com/vps/",affiliate_url=None,
  notes="'Starting at' prices (US site). Renewal / commitment conditions not verified.",plans=[
  P("VPS-1",2,4,40,4.54,None,"not verified",disk_type="NVMe"),P("VPS-2",4,8,75,8.50,None,"not verified",disk_type="NVMe"),
  P("VPS-3",6,12,100,12.32,None,"not verified",disk_type="NVMe"),P("VPS-4",8,24,200,23.37,None,"not verified",disk_type="NVMe")]),
 dict(id="racknerd",name="RackNerd",type="vps",one_click_n8n=None,url="https://www.racknerd.com/kvm-vps",affiliate_url=None,
  notes="Standard KVM list prices. RackNerd's famous cheap deals are time-limited promos and are not included.",plans=[
  P("KVM 2 GB",3,2,75,20.59,20.59,"monthly",disk_type="SSD RAID-10"),P("KVM 4 GB",4,4,130,24.59,24.59,"monthly",disk_type="SSD RAID-10"),
  P("KVM 8 GB",6,8,220,36.59,36.59,"monthly",disk_type="SSD RAID-10")]),
 dict(id="digitalocean",name="DigitalOcean",type="vps",one_click_n8n=None,url="https://www.digitalocean.com/pricing/droplets",affiliate_url=None,
  notes="Basic Droplets (Regular CPU). Hourly billing, no term.",plans=[
  P("Basic 2 GB",1,2,50,12.00,12.00,"none (hourly)"),P("Basic 4 GB",2,4,80,24.00,24.00,"none (hourly)"),P("Basic 8 GB",4,8,160,48.00,48.00,"none (hourly)")]),
 dict(id="vultr",name="Vultr",type="vps",one_click_n8n=None,url="https://www.vultr.com/pricing/",api="https://api.vultr.com/v2/plans?type=vc2",affiliate_url=None,
  notes="Cloud Compute Regular Performance. Hourly billing.",plans=[
  P("vc2-1c-2gb",1,2,55,10.00,10.00,"none (hourly)"),P("vc2-2c-4gb",2,4,80,20.00,20.00,"none (hourly)"),P("vc2-4c-8gb",4,8,160,40.00,40.00,"none (hourly)")]),
 dict(id="linode",name="Akamai / Linode",type="vps",one_click_n8n=None,url="https://www.akamai.com/cloud/pricing",api="https://api.linode.com/v4/linode/types",affiliate_url=None,
  notes="Shared CPU plans, prices from Linode's public types API.",plans=[
  P("Linode 2 GB",1,2,50,12.00,12.00,"none (hourly)"),P("Linode 4 GB",2,4,80,24.00,24.00,"none (hourly)"),P("Linode 8 GB",4,8,160,48.00,48.00,"none (hourly)")]),
 dict(id="railway",name="Railway",type="paas",one_click_n8n=None,url="https://railway.com/pricing",affiliate_url=None,
  notes="Usage-based PaaS: Hobby $5/mo minimum incl. $5 usage credit; RAM $0.00000386/GB-sec, CPU $0.00000772/vCPU-sec. Real n8n cost depends on usage, so no fixed plan price.",plans=[
  P("Hobby (usage-based)",None,None,5,5.00,5.00,"monthly",note="$5 is the minimum; actual bill = usage. Up to 5 GB storage."),
  P("Pro (usage-based)",None,None,None,20.00,20.00,"monthly",note="$20 minimum usage")]),
 dict(id="elestio",name="Elestio",type="managed",one_click_n8n=True,url="https://elest.io/open-source/n8n",affiliate_url=None,
  notes="Fully managed n8n on your choice of cloud. Only the 'starting at' price was verified; specs per tier not captured.",plans=[
  P("Managed n8n (from)",None,None,None,11.00,None,"monthly",note="'starting at $11/mo'; specs not verified")]),
]
n8n=dict(url="https://n8n.io/pricing/",checked=D,notes="Executions = full workflow runs, unlimited steps. Business is listed as self-hosted.",plans=[
 dict(name="Starter",hosting="cloud",monthly=24,annual_mo=20,executions=2500,concurrency=5),
 dict(name="Pro",hosting="cloud",monthly=60,annual_mo=50,executions=10000,concurrency=50),
 dict(name="Business",hosting="self-hosted",monthly=960,annual_mo=800,executions=40000,concurrency=None),
 dict(name="Enterprise",hosting="cloud or self-hosted",monthly=None,annual_mo=None,executions=None,concurrency=200,note="Contact sales")])
for h in H: h["checked"]=D
json.dump(dict(updated=D,hosts=H,n8n_cloud=n8n),open("data/hosts.json","w"),indent=1)
print(sum(len(h['plans']) for h in H),"plans",sum(p['verified'] and p['intro_price_mo'] is not None for h in H for p in h['plans']),"verified")
