import sys
from pathlib import Path
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Preformatted, Table, TableStyle, KeepTogether
sys.path.insert(0, str(Path(__file__).parent))
from report_kit import *

B = Path(__file__).parent; F = B / "figures"
q = {i: pd.read_csv(F / f"q{i}.csv") for i in range(1, 9)}
k = q[1].iloc[0]
code_style = ParagraphStyle("code", fontName="Courier", fontSize=7.3, leading=9)

def code(text):
    t = Table([[Preformatted(text.strip("\n"), code_style)]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F3F3F3")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 6),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return KeepTogether([t, Spacer(1, 6)])

sql = (B / "sql" / "churn_analysis.sql").read_text()
q6 = sql.split("-- Q6.")[1].split("-- Q7.")[0].split("\n", 2)[2]
q7 = sql.split("-- Q7.")[1].split("-- Q8.")[0].split("\n", 1)[1]
ger = q[2].set_index("geography")
prod = q[4].set_index("num_of_products")
age = q[3].set_index("age_band")
seg1 = q[6].iloc[0]

st = header_block("Bank Customer Churn: SQL Analysis & Interactive Dashboard",
                  "Segment analysis in SQL and a Power BI-style dashboard to monitor churn",
                  "Branislav Petkovic  |  Data: 10,000 retail bank customers in France, Germany and Spain")
st.append(keybox("Key findings", [
    f"<b>{k.churn_rate_pct:.1f}%</b> of customers churned ({int(k.churned):,} of {int(k.customers):,}), taking "
    f"<b>EUR {k.balance_lost_mn:.1f} million</b> in balances with them.",
    f"<b>Germany</b> churns at {ger.loc['Germany','churn_rate_pct']:.1f}%, twice the rate of France and Spain, and "
    f"accounts for {q[7].iloc[0].share_of_total_loss_pct:.0f}% of all lost balances.",
    f"Churn rises sharply with age: {age.loc['18-29','churn_rate_pct']:.1f}% for 18-29 year olds vs. "
    f"<b>{age.loc['50-59','churn_rate_pct']:.1f}%</b> for 50-59.",
    f"Customers with <b>2 products</b> are the most loyal ({prod.loc[2,'churn_rate_pct']:.1f}% churn); with 3 or more "
    f"products churn exceeds 80%, which points to a product or service problem worth investigating.",
    f"The riskiest segment is <b>inactive German customers aged 40-59</b>: {seg1.churn_rate_pct:.1f}% churn and "
    f"EUR {seg1.balance_lost_mn:.1f} million lost.",
]))

st += [p("1. Objective and approach", "h1"),
       p("Customer churn directly reduces deposits and future revenue. The aim of this project is to answer, with SQL, "
         "<i>who</i> is leaving and <i>how much it costs</i>, and to give management a dashboard to monitor churn by "
         "segment."),
       p("The public <i>Bank Customer Churn</i> dataset (10,000 customers) was loaded into a SQLite database. Eight "
         "SQL queries cover KPIs, breakdowns by country, age, products and activity, and a ranking of high-risk "
         "segments using a CTE and window functions. Results feed an interactive HTML dashboard; the same data model "
         "with DAX measures is provided for Power BI.")]

st += [p("2. The dashboard", "h1"),
       fig(F / "dashboard.png", "Figure 1. Static view of the dashboard. Red bars are above the overall churn rate "
           "(dotted line). The interactive HTML version has filters for country, gender, activity and products."),
       p("The interactive version (<i>Bank_Churn_Dashboard.html</i>) opens in any browser with no installation. "
         "Selecting a filter recalculates every KPI and chart, in the same way as Power BI slicers.")]

st += [p("3. Results by dimension", "h1"),
       p("<b>Country.</b> German customers hold larger balances on average and leave twice as often:"),
       table(q[2], col_widths=[30*mm, 25*mm, 22*mm, 28*mm, 28*mm],
             fmt={"customers": lambda v: f"{int(v):,}", "churned": lambda v: f"{int(v):,}",
                  "churn_rate_pct": lambda v: f"{v:.1f}%", "avg_balance": lambda v: f"{v:,.0f}"}),
       p("<b>Products and activity.</b> Holding two products is linked to the lowest churn. Inactive members churn at "
         "roughly twice the rate of active members for both genders:"),
       Table([[table(q[4], col_widths=[30*mm, 22*mm, 26*mm],
                     fmt={"num_of_products": lambda v: f"{int(v)}", "customers": lambda v: f"{int(v):,}",
                          "churn_rate_pct": lambda v: f"{v:.1f}%"}, keep=False),
               table(q[5], col_widths=[20*mm, 30*mm, 32*mm],
                     fmt={"churn_active_pct": lambda v: f"{v:.1f}%", "churn_inactive_pct": lambda v: f"{v:.1f}%"}, keep=False)]],
             colWidths=[84*mm, 90*mm], style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]),
       p("<b>Credit score.</b> Churn is almost flat across credit-score bands (18.6% to 22.0%), so credit quality is "
         "not a useful signal for retention targeting.")]

st += [p("4. Finding the highest-risk segments", "h1"),
       p("Combining country, age band and activity status shows where retention effort pays off most. The query uses "
         "a CTE to build segments and <font face='Courier'>RANK() OVER</font> to order them by churn rate:"),
       code(q6),
       table(q[6].rename(columns={"churn_rate_pct": "Churn rate", "balance_lost_mn": "Lost (EUR m)", "risk_rank": "Rank"}),
             col_widths=[20*mm, 20*mm, 18*mm, 20*mm, 17*mm, 22*mm, 24*mm, 14*mm],
             fmt={"customers": lambda v: f"{int(v):,}", "churned": lambda v: f"{int(v):,}",
                  "Churn rate": lambda v: f"{v:.1f}%", "Lost (EUR m)": lambda v: f"{v:.2f}",
                  "Rank": lambda v: f"{int(v)}"}),
       KeepTogether([p("Lost balances by country use a window function over an aggregate to compute each country's share of the "
         "total loss in a single query:"),
       code(q7),
       table(q[7].rename(columns={"balance_lost_mn": "Balance lost (EUR m)", "share_of_total_loss_pct": "Share of total loss"}),
             col_widths=[30*mm, 36*mm, 36*mm],
             fmt={"Balance lost (EUR m)": lambda v: f"{v:.1f}", "Share of total loss": lambda v: f"{v:.1f}%"})])]

st += [p("5. Recommendations", "h1")] + bullets([
    "<b>Focus retention on customers aged 40-59</b>, starting with inactive customers in Germany: the top segment "
    "alone lost over EUR 40 million in balances.",
    "<b>Re-engage inactive members</b> (for example with targeted offers or relationship-manager contact), since "
    "activity roughly halves churn.",
    "<b>Encourage a second product</b>, but review the 3-4 product offering, whose very high churn suggests "
    "mis-selling or poor service.",
    "<b>Investigate Germany</b> separately: pricing, competition and service quality may differ from France and Spain.",
    "<b>Track these KPIs monthly</b> in the dashboard and set alerts when a segment's churn moves above the overall rate.",
]) + [Spacer(1, 6), p("<b>Tools:</b> SQL (SQLite: CTEs, CASE, window functions), Python (pandas), Plotly (interactive "
                       "dashboard), Power BI (data model and DAX measures in <i>PowerBI_Guide.md</i>).")]

build(B / "Bank_Churn_SQL_Report.pdf", st, "Bank Customer Churn: SQL & Dashboard  |  Branislav Petkovic")
print("ok")
