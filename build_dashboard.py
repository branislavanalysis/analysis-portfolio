"""
Builds an interactive, self-contained HTML dashboard (Power BI-style) for bank customer churn,
plus a static PNG version for reports.
Author: Branislav Petkovic
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plotly.offline import get_plotlyjs

B = Path(__file__).parent
df = pd.read_csv(B / "data" / "customers_powerbi.csv")

# ---------- compact data for the browser ----------
rows = df[["geography", "gender", "age", "num_of_products", "is_active_member", "balance", "credit_score",
           "tenure", "exited"]].copy()
rows["balance"] = rows["balance"].round(0).astype(int)
data_json = json.dumps(rows.values.tolist(), separators=(",", ":"))

html = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bank Customer Churn Dashboard</title>
<script>__PLOTLY__</script>
<style>
:root{--navy:#1F4E5F;--teal:#3A9AB5;--bg:#F4F7F8;--card:#fff;--grey:#595959;--red:#C0504D}
*{box-sizing:border-box}body{margin:0;font-family:Segoe UI,Helvetica,Arial,sans-serif;background:var(--bg);color:#222}
header{background:var(--navy);color:#fff;padding:14px 24px;display:flex;flex-wrap:wrap;align-items:center;gap:16px;justify-content:space-between}
header h1{font-size:19px;margin:0;font-weight:600}header .sub{font-size:12px;opacity:.8}
.filters{display:flex;gap:12px;flex-wrap:wrap}.filters label{font-size:11px;display:flex;flex-direction:column;gap:3px}
select{padding:5px 8px;border-radius:4px;border:0;font-size:13px;min-width:120px}
main{padding:16px 24px;max-width:1400px;margin:0 auto}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:14px}
.kpi{background:var(--card);border-radius:6px;padding:12px 14px;border-left:4px solid var(--teal);box-shadow:0 1px 2px rgba(0,0,0,.06)}
.kpi .l{font-size:11px;color:var(--grey);text-transform:uppercase;letter-spacing:.4px}.kpi .v{font-size:24px;font-weight:600;color:var(--navy);margin-top:4px}
.kpi.alert{border-left-color:var(--red)}.kpi.alert .v{color:var(--red)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:12px}
.card{background:var(--card);border-radius:6px;padding:8px 10px;box-shadow:0 1px 2px rgba(0,0,0,.06)}
.card h3{font-size:13px;margin:4px 6px 0;color:var(--navy)}.chart{height:280px}
footer{font-size:11px;color:var(--grey);padding:8px 24px 18px;max-width:1400px;margin:0 auto}
</style></head><body>
<header><div><h1>Bank Customer Churn Dashboard</h1><div class="sub">10,000 retail customers &middot; churn = customer closed the account</div></div>
<div class="filters">
<label>Country<select id="fGeo"><option>All</option><option>France</option><option>Germany</option><option>Spain</option></select></label>
<label>Gender<select id="fGen"><option>All</option><option>Female</option><option>Male</option></select></label>
<label>Activity<select id="fAct"><option>All</option><option value="1">Active</option><option value="0">Inactive</option></select></label>
<label>Products<select id="fProd"><option>All</option><option>1</option><option>2</option><option>3</option><option>4</option></select></label>
</div></header>
<main>
<div class="kpis">
<div class="kpi"><div class="l">Customers</div><div class="v" id="kCust"></div></div>
<div class="kpi alert"><div class="l">Churned customers</div><div class="v" id="kChurn"></div></div>
<div class="kpi alert"><div class="l">Churn rate</div><div class="v" id="kRate"></div></div>
<div class="kpi"><div class="l">Avg. balance (EUR)</div><div class="v" id="kBal"></div></div>
<div class="kpi alert"><div class="l">Balances lost (EUR m)</div><div class="v" id="kLost"></div></div>
</div>
<div class="grid">
<div class="card"><h3>Churn rate by country</h3><div class="chart" id="cGeo"></div></div>
<div class="card"><h3>Churn rate by age band</h3><div class="chart" id="cAge"></div></div>
<div class="card"><h3>Churn rate by number of products</h3><div class="chart" id="cProd"></div></div>
<div class="card"><h3>Churn rate: active vs. inactive members</h3><div class="chart" id="cAct"></div></div>
</div>
</main>
<footer>Built by Branislav Petkovic &middot; Python + Plotly &middot; Data: public "Bank Customer Churn" dataset (10,000 customers, France / Germany / Spain).
The same model is provided for Power BI (customers_powerbi.csv + DAX measures).</footer>
<script>
const D = __DATA__; // [geo, gender, age, products, active, balance, score, tenure, exited]
const NAVY="#1F4E5F", TEAL="#3A9AB5", RED="#C0504D";
const AGE=["18-29","30-39","40-49","50-59","60+"];
const ageBand=a=>a<30?AGE[0]:a<40?AGE[1]:a<50?AGE[2]:a<60?AGE[3]:AGE[4];
const fmt=(n,d=0)=>n.toLocaleString("en-US",{minimumFractionDigits:d,maximumFractionDigits:d});
function group(rows,key,order){const m={};rows.forEach(r=>{const k=key(r);(m[k]=m[k]||[0,0]);m[k][0]++;m[k][1]+=r[8];});
 const ks=order||Object.keys(m).sort();return ks.filter(k=>m[k]).map(k=>({k:String(k),n:m[k][0],rate:100*m[k][1]/m[k][0]}));}
function bar(id,g,overall,horizontal){
 const colors=g.map(x=>x.rate>overall?RED:TEAL);
 const t={type:"bar",x:horizontal?g.map(x=>x.rate):g.map(x=>x.k),y:horizontal?g.map(x=>x.k):g.map(x=>x.rate),
  orientation:horizontal?"h":"v",marker:{color:colors},text:g.map(x=>x.rate.toFixed(1)+"%"),textposition:"outside",
  customdata:g.map(x=>x.n),hovertemplate:"%{"+(horizontal?"y":"x")+"}<br>Churn rate: %{text}<br>Customers: %{customdata:,}<extra></extra>"};
 const ax={title:"Churn rate (%)",rangemode:"tozero",gridcolor:"#eee"};
 const lay={margin:{l:horizontal?70:45,r:20,t:10,b:40},paper_bgcolor:"rgba(0,0,0,0)",plot_bgcolor:"rgba(0,0,0,0)",
  font:{size:11},showlegend:false,shapes:[horizontal?{type:"line",x0:overall,x1:overall,y0:-0.5,y1:g.length-0.5,line:{dash:"dot",color:NAVY}}
  :{type:"line",y0:overall,y1:overall,x0:-0.5,x1:g.length-0.5,line:{dash:"dot",color:NAVY}}]};
 if(horizontal){lay.xaxis=Object.assign(ax,{range:[0,Math.max(...g.map(x=>x.rate))*1.25]});lay.yaxis={type:"category"};}
 else{lay.yaxis=Object.assign(ax,{range:[0,Math.max(...g.map(x=>x.rate))*1.2]});lay.xaxis={type:"category"};}
 Plotly.react(id,[t],lay,{displayModeBar:false,responsive:true});}
function update(){
 const geo=fGeo.value,gen=fGen.value,act=fAct.value,prod=fProd.value;
 const R=D.filter(r=>(geo==="All"||r[0]===geo)&&(gen==="All"||r[1]===gen)&&(act==="All"||String(r[4])===act)&&(prod==="All"||String(r[3])===prod));
 const n=R.length,c=R.reduce((s,r)=>s+r[8],0),bal=R.reduce((s,r)=>s+r[5],0),lost=R.reduce((s,r)=>s+(r[8]?r[5]:0),0);
 const overall=n?100*c/n:0;
 kCust.textContent=fmt(n);kChurn.textContent=fmt(c);kRate.textContent=fmt(overall,1)+"%";
 kBal.textContent=n?fmt(bal/n):"-";kLost.textContent=fmt(lost/1e6,1);
 bar("cGeo",group(R,r=>r[0]),overall,true);
 bar("cAge",group(R,r=>ageBand(r[2]),AGE),overall,false);
 bar("cProd",group(R,r=>r[3],[1,2,3,4]),overall,false);
 bar("cAct",group(R,r=>r[4]?"Active":"Inactive",["Active","Inactive"]),overall,true);}
[fGeo,fGen,fAct,fProd].forEach(e=>e.addEventListener("change",update));update();
</script></body></html>"""
html = html.replace("__PLOTLY__", get_plotlyjs()).replace("__DATA__", data_json)
(B / "Bank_Churn_Dashboard.html").write_text(html, encoding="utf-8")

# ---------- static PNG version ----------
NAVY, TEAL, RED, GREY = "#1F4E5F", "#3A9AB5", "#C0504D", "#595959"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
overall = df.exited.mean() * 100
df["age_band"] = pd.cut(df.age, [0, 29, 39, 49, 59, 200], labels=["18-29", "30-39", "40-49", "50-59", "60+"])
fig = plt.figure(figsize=(11, 6.6), dpi=150, facecolor="#F4F7F8")
fig.text(0.02, 0.955, "Bank Customer Churn Dashboard", fontsize=16, fontweight="bold", color=NAVY)
fig.text(0.02, 0.925, "10,000 retail customers  |  France, Germany, Spain", fontsize=9, color=GREY)
kpis = [("Customers", f"{len(df):,}", False), ("Churned", f"{int(df.exited.sum()):,}", True),
        ("Churn rate", f"{overall:.1f}%", True), ("Avg. balance (EUR)", f"{df.balance.mean():,.0f}", False),
        ("Balances lost (EUR m)", f"{df.loc[df.exited == 1, 'balance'].sum() / 1e6:,.1f}", True)]
for i, (l, v, alert) in enumerate(kpis):
    ax = fig.add_axes([0.02 + i * 0.196, 0.78, 0.18, 0.11]); ax.set_xticks([]); ax.set_yticks([])
    ax.set_facecolor("white"); [s.set_visible(False) for s in ax.spines.values()]
    ax.axvline(0, color=RED if alert else TEAL, lw=6)
    ax.text(0.08, 0.68, l.upper(), fontsize=7.5, color=GREY, transform=ax.transAxes)
    ax.text(0.08, 0.2, v, fontsize=17, fontweight="bold", color=RED if alert else NAVY, transform=ax.transAxes)

def panel(rect, s, title, horizontal=False):
    ax = fig.add_axes(rect); ax.set_facecolor("white")
    vals = s.values * 100; cols = [RED if v > overall else TEAL for v in vals]
    labels = [str(x) for x in s.index]
    if horizontal:
        ax.barh(labels, vals, color=cols); ax.axvline(overall, color=NAVY, ls=":", lw=1)
        for i, v in enumerate(vals): ax.text(v + 0.8, i, f"{v:.1f}%", va="center", fontsize=8)
        ax.set_xlim(0, vals.max() * 1.25)
    else:
        ax.bar(labels, vals, color=cols); ax.axhline(overall, color=NAVY, ls=":", lw=1)
        for i, v in enumerate(vals): ax.text(i, v + 1.5, f"{v:.1f}%", ha="center", fontsize=8)
        ax.set_ylim(0, vals.max() * 1.2)
    ax.set_title(title, loc="left", fontweight="bold", color=NAVY, fontsize=10)

panel([0.06, 0.42, 0.40, 0.29], df.groupby("geography").exited.mean().sort_values(), "Churn rate by country", True)
panel([0.56, 0.42, 0.42, 0.29], df.groupby("age_band", observed=True).exited.mean(), "Churn rate by age band")
panel([0.06, 0.06, 0.40, 0.27], df.groupby("num_of_products").exited.mean(), "Churn rate by number of products")
panel([0.56, 0.06, 0.42, 0.27], df.groupby(df.is_active_member.map({1: "Active", 0: "Inactive"})).exited.mean(),
      "Churn rate: active vs. inactive", True)
fig.savefig(B / "figures" / "dashboard.png", facecolor=fig.get_facecolor())
print("dashboard ok")
