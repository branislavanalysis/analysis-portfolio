# Data Analysis Portfolio – Branislav Petkovic

Three end-to-end projects on real public data, covering statistics, econometrics, SQL and dashboards.
Each folder contains the PDF report (main deliverable), the code, the data and the charts.

| # | Project | Skills | Main file |
|---|---|---|---|
| 1 | EUR/USD Time Series Analysis & Forecast | Econometrics, ADF, ARIMA, forecasting (EViews workflow) | `01_EURUSD_Time_Series/EURUSD_Time_Series_Report.pdf` |
| 2 | Bank Term-Deposit Campaign: Statistical Analysis | Chi-square, t-tests, logistic regression, SPSS syntax | `02_Bank_Marketing_Statistics/Bank_Marketing_Statistical_Report.pdf` |
| 3 | Bank Customer Churn: SQL & Dashboard | SQL (CTE, window functions), dashboard, Power BI DAX | `03_Bank_Churn_SQL_Dashboard/Bank_Churn_SQL_Report.pdf` + `Bank_Churn_Dashboard.html` |

## How to re-run
```bash
pip install pandas numpy scipy statsmodels scikit-learn matplotlib plotly reportlab pillow
# Project 1
cd 01_EURUSD_Time_Series && python analysis.py && python make_report.py
# Project 2
cd 02_Bank_Marketing_Statistics && python analysis.py && python make_report.py
# Project 3
cd 03_Bank_Churn_SQL_Dashboard && python run_sql.py && python build_dashboard.py && python make_report.py
```

## Data sources
- **EUR/USD:** Federal Reserve H.10 monthly exchange rates, via the `datasets/exchange-rates` repository on GitHub (Jan 1999 – Oct 2026).
- **Bank Marketing:** UCI Machine Learning Repository, *bank-additional-full* (Moro, Cortez & Rita, 2014, *Decision Support Systems*).
- **Bank Churn:** public "Churn Modelling" dataset (10,000 bank customers), widely used for churn analysis. The surname column was removed.

---

## Ready-to-paste Upwork portfolio entries

### 1. EUR/USD Exchange Rate – Time Series Analysis & Forecast
**Cover image:** `_Upwork_Cover_Images/01_EURUSD_Forecast_cover.png`
**Description:**
Econometric analysis of the monthly EUR/USD exchange rate (1999–2026). I tested for stationarity with the Augmented Dickey-Fuller test, identified the model from the ACF/PACF, selected ARIMA(0,1,1) by AIC, and validated it with Ljung-Box and Jarque-Bera tests. In a 24-month out-of-sample test the model beat the random-walk benchmark by 7% in RMSE. Delivered a 12-month forecast with 95% confidence intervals and a 4-page report explaining every step in plain language.
**Skills:** Time Series Analysis, Econometrics, EViews, Python, Forecasting, Statistical Analysis

### 2. Bank Marketing Campaign – Statistical Analysis
**Cover image:** `_Upwork_Cover_Images/02_Bank_Marketing_cover.png`
**Description:**
Statistical analysis of 41,188 bank telemarketing calls to find what drives term-deposit subscriptions. Chi-square tests with Cramér's V, Welch t-tests and Mann-Whitney U tests with effect sizes, and a binary logistic regression with odds ratios. The model reaches AUC 0.80 on a hold-out sample: calling the top 10% of clients by score reaches 43% of all subscribers (4.3x better than random). Includes clear business recommendations and equivalent IBM SPSS syntax.
**Skills:** Statistical Analysis, IBM SPSS, Logistic Regression, Hypothesis Testing, Python, Data Analysis

### 3. Bank Customer Churn – SQL Analysis & Interactive Dashboard
**Cover image:** `_Upwork_Cover_Images/03_Bank_Churn_cover.png`
**Description:**
SQL analysis of 10,000 bank customers to find who leaves and how much it costs. Eight queries using CASE, GROUP BY, CTEs and window functions (RANK, share of total) identify the highest-risk segments, e.g. inactive German customers aged 40–59 with 61% churn. Built an interactive dashboard with KPI cards and filters (country, gender, activity, products) and a Power BI version with DAX measures.
**Skills:** SQL, Microsoft Power BI, Dashboard, Data Visualization, Python, Data Analysis
