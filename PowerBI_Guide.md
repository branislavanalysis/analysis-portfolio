# Rebuilding the dashboard in Power BI

Data file: `data/customers_powerbi.csv` (10,000 rows, one row per customer).

## 1. Load and prepare
1. **Home → Get data → Text/CSV** → select `customers_powerbi.csv` → **Transform Data**.
2. Check data types: `balance`, `estimated_salary` = Decimal; `exited`, `is_active_member`, `has_cr_card`, `num_of_products`, `age`, `tenure`, `credit_score` = Whole number.
3. Add a column **Add Column → Conditional Column** named `Age Band`:
   18-29, 30-39, 40-49, 50-59, 60+ (based on `age`).
4. Add a column `Activity` = `if [is_active_member] = 1 then "Active" else "Inactive"`.
5. **Close & Apply**.

## 2. DAX measures
```DAX
Customers        = COUNTROWS ( customers_powerbi )
Churned          = SUM ( customers_powerbi[exited] )
Churn Rate       = DIVIDE ( [Churned], [Customers] )
Avg Balance      = AVERAGE ( customers_powerbi[balance] )
Balance Lost     = CALCULATE ( SUM ( customers_powerbi[balance] ), customers_powerbi[exited] = 1 )
Overall Churn Rate =
    CALCULATE ( [Churn Rate], REMOVEFILTERS ( customers_powerbi ) )
Churn vs Overall =
    [Churn Rate] - [Overall Churn Rate]
```
Format `Churn Rate`, `Overall Churn Rate` and `Churn vs Overall` as **Percentage, 1 decimal**.

## 3. Report page
| Visual | Fields |
|---|---|
| 5 × Card | Customers, Churned, Churn Rate, Avg Balance, Balance Lost |
| Clustered bar chart | Y: `geography`, X: `Churn Rate` |
| Clustered column chart | X: `Age Band`, Y: `Churn Rate` |
| Clustered column chart | X: `num_of_products`, Y: `Churn Rate` |
| Clustered bar chart | Y: `Activity`, X: `Churn Rate` |
| 4 × Slicer | `geography`, `gender`, `Activity`, `num_of_products` |

**Conditional colour:** in each chart, *Format → Columns → Colors → fx* → Rules on `Churn vs Overall`:
greater than 0 → red `#C0504D`, otherwise teal `#3A9AB5`.
**Reference line:** *Analytics pane → Constant line* = `Overall Churn Rate`, dotted, navy `#1F4E5F`.

Theme colours used: navy `#1F4E5F`, teal `#3A9AB5`, red `#C0504D`, background `#F4F7F8`.
