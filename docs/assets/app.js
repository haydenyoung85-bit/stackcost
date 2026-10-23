(function(){var D=window.SC,$=function(s){return document.querySelector(s)};
var sym={USD:"$",EUR:"€"};function money(v,c){return v==null?null:(sym[c]||"")+v.toFixed(2)}
var rows=[];D.hosts.forEach(function(h){h.plans.forEach(function(p){rows.push({h:h,p:p,renew:p.renewal_price_mo,intro:p.intro_price_mo,ram:p.ram_gb,vcpu:p.vcpu})})});
window.SCrows=rows;
var tb=$("#tbody");if(tb){var sk="renew",dir=1;
 function oc(v){return v===true?'<span class="tag">1-click n8n</span>':v===false?'<span class="tag g">Docker install</span>':'<span class="tag u">1-click: unverified</span>'}
 function draw(){var q=($("#q").value||"").toLowerCase(),mr=+$("#ram").value||0,oneOnly=$("#oc").checked,ty=$("#ty").value;
  var r=rows.filter(function(x){return (x.h.name+" "+x.p.name).toLowerCase().indexOf(q)>-1&&(!mr||(x.ram||0)>=mr)&&(!oneOnly||x.h.one_click_n8n===true)&&(!ty||x.h.type===ty)});
  r.sort(function(a,b){var A=a[sk],B=b[sk];if(sk=="host"){A=a.h.name;B=b.h.name;return A<B?-dir:A>B?dir:0}if(A==null)return 1;if(B==null)return -1;return (A-B)*dir});
  tb.innerHTML=r.map(function(x){var p=x.p,h=x.h,c=p.currency,rn=money(p.renewal_price_mo,c),it=money(p.intro_price_mo,c);
   var spec=[p.vcpu!=null?p.vcpu+" vCPU":"? vCPU",p.ram_gb!=null?p.ram_gb+" GB RAM":"? RAM",p.storage_gb!=null?p.storage_gb+" GB "+(p.storage_type||""):"? disk"].join(" · ");
   return '<tr><td class="h">'+h.name+'<div class="small">'+p.name+'</div></td><td class="spec">'+spec+'</td>'+
   '<td class="price num">'+(rn?'<div class="renew">'+rn+'<span class="small">/mo</span></div>':'<span class="tag u">renewal unverified</span>')+(it&&it!==rn?'<div class="intro">intro '+it+'</div>':'')+(c!="USD"?'<div class="intro">'+c+(h.id=="hetzner"?" excl. VAT":"")+'</div>':'')+'</td>'+
   '<td class="meta">'+p.term+' '+oc(h.one_click_n8n)+(p.note?' <span title="'+p.note.replace(/"/g,"&quot;")+'" class="tag u">note</span>':'')+' <a href="'+h.url+'" rel="nofollow noopener" target="_blank">source</a> <span>checked '+h.checked+'</span> <a class="btn s" href="'+h.affiliate+'" rel="sponsored nofollow" data-todo="affiliate-link">View deal*</a></td></tr>'}).join("")||'<tr><td>No plans match.</td></tr>';
  $("#count").textContent=r.length+" plans";var m=$("#more");m.textContent="Show all "+r.length+" plans";m.classList.toggle("show",r.length>8&&tb.parentNode.classList.contains("lim"))}
 $("#more").onclick=function(){tb.parentNode.classList.remove("lim");this.classList.remove("show")};
 ["#q","#ram","#oc","#ty"].forEach(function(s){$(s).addEventListener("input",draw)});
 document.querySelectorAll("th[data-k]").forEach(function(th){th.addEventListener("click",function(){var k=th.dataset.k;dir=k==sk?-dir:1;sk=k;draw()})});draw()}
// calculator
var cf=$("#calc");if(cf){var list=$("#wfs");
 function addRow(n,f){var d=document.createElement("div");d.className="wf";d.innerHTML='<label class="small">Workflows<input type="number" min="0" value="'+n+'" class="n"></label><label class="small">Each runs<select class="fq"><option value="43200">every minute</option><option value="8640">every 5 min</option><option value="2880">every 15 min</option><option value="720">hourly</option><option value="30">daily</option><option value="4">weekly</option><option value="1">monthly</option><option value="100">~100×/mo (webhook)</option><option value="1000">~1,000×/mo (webhook)</option></select></label><button type="button" class="btn s" aria-label="remove">✕</button>';
  d.querySelector(".fq").value=f;d.querySelector("button").onclick=function(){d.remove();calc()};list.appendChild(d)}
 function calc(){var ex=0;list.querySelectorAll(".wf").forEach(function(r){ex+=(+r.querySelector(".n").value||0)*(+r.querySelector(".fq").value)});
  var bill=$("#bill").value,tiers=D.n8n_cloud.plans.filter(function(p){return p.hosting=="cloud"&&p.monthly});
  var t=tiers.filter(function(p){return p.executions>=ex}).sort(function(a,b){return a.monthly-b.monthly})[0];
  var need=ex>200000?8:ex>20000?4:2;
  var v=rows.filter(function(x){return x.p.verified&&x.p.currency=="USD"&&x.renew!=null&&x.ram!=null&&x.ram>=need&&x.h.type!="paas"}).sort(function(a,b){return a.renew-b.renew})[0];
  $("#ex").textContent=Math.round(ex).toLocaleString();
  var cc=t?(bill=="annual"?t.annual_mo:t.monthly):null;
  $("#cloud").innerHTML=t?"$"+cc+"<span class=small>/mo</span>":"Enterprise";$("#cloudn").textContent=t?"n8n "+t.name+" ("+t.executions.toLocaleString()+" exec/mo)":"over "+tiers[tiers.length-1].executions.toLocaleString()+" exec/mo — contact n8n sales";
  $("#vps").innerHTML=v?"$"+v.renew.toFixed(2)+"<span class=small>/mo</span>":"—";$("#vpsn").textContent=v?v.h.name+" "+v.p.name+" ("+v.ram+" GB RAM, renewal price)":"";
  var s=$("#save");if(t&&v){var y=(cc-v.renew)*12;s.innerHTML=(y>=0?"Self-hosting saves <b>$"+y.toFixed(0)+"/yr</b>":"n8n Cloud is cheaper by <b>$"+(-y).toFixed(0)+"/yr</b>")+" on sticker price. Add your own time for updates & backups (est. 1–2 h/mo).";}
  else s.innerHTML="Above n8n Cloud's published tiers, self-hosting is the only fixed-price option: from <b>$"+(v?v.renew.toFixed(2):"?")+"/mo</b> with unlimited executions.";
  $("#needram").textContent=need}
 addRow(5,"720");addRow(3,"30");$("#add").onclick=function(){addRow(1,"30");calc()};cf.addEventListener("input",calc);cf.addEventListener("change",calc);calc()}
var nf=$("#newsletter");if(nf)nf.addEventListener("submit",function(e){e.preventDefault();$("#nlmsg").textContent="Thanks! (Placeholder — no email service is connected yet, nothing was sent.)"})
})();
