# Credit Risk Portfolio Monitoring Dashboard

## Business Context

This project simulates a credit risk monitoring dashboard for a fictional credit insurer and corporate lending team. The dashboard provides a portfolio-level view of credit exposure, rating distribution, overdue balances, default trends, and concentration by country and industry.

A reporting user wants clear business reporting for credit portfolio management, underwriting review, and risk monitoring.

## Business Value

- Provides portfolio visibility for total exposure and credit limit utilisation.
- Highlights overdue exposure and default risk by customer, industry and country.
- Supports underwriting decisions and monthly risk review meetings.
- Enables monitoring of rating migration and concentration risk.

## Tech Stack

- Python 3.10+ (pandas, numpy)
- PostgreSQL-style SQL
- Power BI-ready CSV outputs
- Jupyter Notebook for exploratory analysis

## Dataset

All data is synthetic and created for portfolio demonstration purposes. The project includes customer master data, country and industry reference tables, monthly exposure snapshots, invoices, payments, and default events.

## Data Model

- `dim_customer`: customer master list with risk rating, industry, country, credit limit.
- `dim_country`: country reference table.
- `dim_industry`: industry reference table.
- `dim_risk_rating`: risk rating definitions.
- `dim_date`: monthly reporting calendar.
- `fact_exposure_snapshot`: monthly exposure and overdue amounts by customer.
- `fact_invoice`: invoice issuance details.
- `fact_payment`: payment records.
- `fact_default_event`: customer default records.

## Key KPIs

- Total credit exposure
- Total credit limit
- Utilization rate = exposure / credit limit
- Overdue exposure and overdue ratio
- Default rate
- Exposure-weighted risk score
- Exposure by country, industry, risk rating
- Monthly exposure trend and default trend
- Top 20 customers by exposure
- Rating migration summary

## Project Structure

```text
credit-risk-portfolio-monitoring-dashboard/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   ├── processed/
│   └── powerbi/
├── sql/
│   ├── 01_create_schema.sql
│   ├── 02_load_tables.sql
│   ├── 03_kpi_queries.sql
│   └── 04_dashboard_views.sql
├── src/
│   ├── generate_data.py
│   ├── transform_data.py
│   └── export_powerbi.py
├── notebooks/
│   └── credit_risk_analysis.ipynb
└── screenshots/
    └── .gitkeep
```

## How to Run

```bash
cd credit-risk-portfolio-monitoring-dashboard
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/generate_data.py
python src/transform_data.py
python src/export_powerbi.py
```

For Windows:

```powershell
.venv\Scriptsctivate
```

## Dashboard Design

Power BI pages:

1. Portfolio Overview
2. Risk Segmentation
3. Country & Industry Exposure
4. Default and Overdue Trends
5. Customer Drilldown

## Example Insights

- The portfolio shows concentrated exposure in Germany and the Manufacturing sector.
- Overdue exposure is highest for customers with lower risk ratings and older invoices.
- Rating migration indicates the majority of borrowers remain stable, with a small watchlist cohort moving toward higher risk.

## Future Improvements

- Add scenario analysis for stress testing.
- Integrate credit limit utilisation forecasts.
- Add support for monthly comparative reporting with prior year.

## Disclaimer

This project uses fully synthetic data created for portfolio demonstration purposes. It does not contain confidential, proprietary, or real company data.
