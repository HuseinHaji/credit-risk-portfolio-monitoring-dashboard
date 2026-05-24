# Credit Risk Monitoring Dashboard

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL--style-informational)
![pandas](https://img.shields.io/badge/pandas-analytics-success)
![Credit Risk](https://img.shields.io/badge/Credit%20Risk-portfolio%20monitoring-critical)
![Tests](https://img.shields.io/badge/tests-pytest-brightgreen)
![Synthetic Data](https://img.shields.io/badge/data-synthetic-lightgrey)

Credit Risk Monitoring Dashboard is a synthetic credit portfolio analytics project that demonstrates how customer exposure, payment behavior, risk ratings, and default indicators can be transformed into portfolio KPIs, high-risk watchlists, stress testing outputs, and dashboard-ready datasets.

## Business Context

A financial services, lending, or credit insurance analytics team needs to monitor customer-level exposure, overdue balances, rating migration, default events, and concentration risk. This simulated business case builds a reproducible portfolio implementation for management reporting and BI dashboarding.

The project is designed for Data Analyst, BI Analyst, Credit Risk Analyst, Portfolio Analyst, and financial services analytics roles in Germany. It uses only a synthetic credit portfolio dataset and does not represent real company data or real business impact.

## Business Problem

How can a credit risk team monitor portfolio exposure, default risk, concentration, rating migration, and high-risk customers using a clean, automated, dashboard-ready analytics workflow?

## Solution Overview

The workflow converts synthetic customer, exposure, rating, payment, and default records into validated risk analytics outputs:

```text
Synthetic credit portfolio records
    -> data validation checks
    -> customer-month feature engineering
    -> portfolio and customer risk KPIs
    -> high-risk customer watchlist
    -> scenario stress testing
    -> Power BI-ready dashboard export
    -> PostgreSQL-style analytics queries
```

## Dataset Description

The raw data is generated with deterministic Python logic and saved in `data/raw/`:

- `customers.csv`: customer master data with country, region, industry, company size, onboarding date, and active flag.
- `credit_exposures.csv`: monthly exposure snapshots with credit limit, current exposure, outstanding amount, overdue amount, days past due, collateral, status, and currency.
- `risk_ratings.csv`: monthly current and previous risk ratings, rating score, PD proxy, and rating outlook.
- `default_events.csv`: synthetic default event flags, reasons, recovery amount, and loss amount.
- `payments.csv`: expected and actual payment behavior with days late.
- `macroeconomic_scenarios.csv`: baseline, mild downturn, sector stress, and severe downturn assumptions.

## Workflow

Run the full pipeline from the repository root:

```bash
python src/generate_synthetic_data.py
python src/validate_data.py
python src/transform_data.py
python src/calculate_risk_kpis.py
python src/generate_watchlist.py
python src/stress_testing.py
python src/export_powerbi.py
pytest
```

Install dependencies first:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Data Validation Layer

`src/validate_data.py` writes `output/audit/data_quality_report.csv` and checks:

- Required columns exist across all raw tables.
- Customer and exposure keys are unique.
- Customer IDs match across exposures, ratings, defaults, and payments.
- Credit limits, exposures, outstanding amounts, overdue amounts, payments, recoveries, and loss amounts are non-negative.
- Overdue amount does not exceed outstanding amount.
- Exposure utilization remains within a reasonable range.
- Risk ratings, default flags, active flags, reporting months, and event dates are valid.
- Critical fields are not null.

## Risk KPI Logic

`src/calculate_risk_kpis.py` creates executive and customer-level risk outputs:

- Total exposure and credit limit.
- Exposure utilization.
- Outstanding and overdue amount.
- Overdue rate and default rate.
- High-risk exposure and high-risk exposure share.
- Expected loss proxy: `current_exposure * probability_of_default_proxy * 45% LGD proxy`.
- Weighted average risk score.
- Top 10 customer concentration.
- Rating migration, downgrade count, and exposure by migrated rating.

Risk categories are business-readable:

- Low Risk
- Moderate Risk
- Elevated Risk
- High Risk
- Critical Watchlist

## Watchlist Logic

`src/generate_watchlist.py` creates `output/watchlist/high_risk_watchlist.csv`.

A customer can be flagged by one or more transparent rules:

- High days past due.
- Overdue ratio above threshold.
- High exposure utilization.
- Weak risk rating.
- Rating downgrade.
- High expected loss proxy.
- Recent default indicator.
- Large exposure concentration.

Each watchlist record includes severity, watchlist reason, and recommended action such as reviewing credit limits, requesting updated financials, escalating to the risk team, reducing exposure, or placing the customer on critical watchlist.

## Stress Testing Logic

`src/stress_testing.py` applies scenario-based PD, LGD, and exposure shocks:

- Baseline
- Mild Downturn
- Sector Stress
- Severe Downturn

The output includes stressed exposure, stressed PD proxy, stressed loss proxy, incremental loss proxy, high-risk exposure share, affected customers, and scenario commentary. This is an analytical stress-testing prototype using synthetic data, not a regulatory capital model.

## SQL Analytics Layer

The `sql/` folder contains PostgreSQL-style analytics queries using CTEs, joins, `CASE WHEN`, aggregations, date logic, and window functions:

- Portfolio exposure overview.
- Exposure segmentation by country, industry, company size, and risk rating.
- Default and overdue rate analysis.
- Rating migration matrix.
- Customer concentration risk.
- Watchlist query logic.
- Stress testing summary.
- Dashboard export base query.
- Expected loss proxy calculation.

## Dashboard Design

The BI-ready export is `output/powerbi/powerbi_credit_risk_dashboard.csv`. Suggested dashboard pages:

1. Executive Overview: total exposure, credit limit, utilization, overdue amount, default rate, high-risk exposure share, expected loss proxy, and watchlist customer count.
2. Exposure Segmentation: exposure by country, industry, company size, customer, and top 10 concentration.
3. Risk Rating Analysis: exposure by risk rating, weighted average risk score, migration matrix, downgrades, and outlook distribution.
4. Overdue & Default Monitoring: overdue amount by segment, days past due distribution, default events, overdue rate trend, and worsening payment behavior.
5. Watchlist: high-risk customers, severity, reasons, recommended actions, and exposure at risk.
6. Stress Testing: baseline versus downturn scenarios, stressed loss proxy, incremental loss proxy, affected customers, and commentary.

## Repository Structure

```text
data/
  raw/                  synthetic source tables
  processed/            enriched customer-month dataset
  reference/            scenario reference copy
output/
  audit/                data quality report
  reports/              portfolio, customer, and rating migration summaries
  stress_tests/         scenario stress test results
  watchlist/            high-risk customer watchlist
  powerbi/              flat dashboard-ready export
src/
  config.py
  generate_synthetic_data.py
  validate_data.py
  transform_data.py
  calculate_risk_kpis.py
  generate_watchlist.py
  stress_testing.py
  export_powerbi.py
sql/
  01_portfolio_overview.sql
  ...
tests/
  pytest validation, schema, KPI, and output tests
```

## Outputs

- `output/reports/portfolio_risk_summary.csv`
- `output/reports/customer_risk_summary.csv`
- `output/reports/rating_migration_summary.csv`
- `output/watchlist/high_risk_watchlist.csv`
- `output/stress_tests/stress_test_results.csv`
- `output/powerbi/powerbi_credit_risk_dashboard.csv`
- `output/audit/data_quality_report.csv`

## Example Insights

The generated outputs are intended to support example portfolio observations such as:

- Which countries, industries, and customers drive the largest exposure concentration.
- Which risk ratings account for the highest expected loss proxy.
- Which customers require review due to overdue balances, downgrades, weak ratings, or high utilization.
- How stressed loss proxy changes under mild, sector-specific, and severe downturn assumptions.

## Skills Demonstrated

| Skill | Where demonstrated |
|---|---|
| Python | pipeline scripts, synthetic data generation, risk KPI calculations |
| pandas | joins, transformations, aggregations, output tables |
| SQL | portfolio monitoring queries, exposure segmentation, watchlist logic |
| Credit risk analytics | exposure, overdue, default, rating, expected loss proxy |
| Portfolio monitoring | concentration, high-risk exposure, customer risk summaries |
| Stress testing | scenario-based PD/LGD/exposure shocks |
| KPI design | exposure utilization, default rate, overdue rate, expected loss proxy |
| Data validation | schema checks, audit report, duplicate checks |
| Power BI-ready modeling | flat dashboard export table |
| pytest | validation tests and output checks |
| CI/CD | GitHub Actions test workflow |
| Business analytics | risk reporting, management dashboard logic, recommended actions |

## Limitations

- The dataset is synthetic and simplified for portfolio demonstration.
- PD and LGD values are analytical proxies, not calibrated regulatory model outputs.
- Stress testing is scenario-based and illustrative, not a capital adequacy model.
- The project does not claim real company data, production deployment, or measured business impact.

## Future Improvements

- Add a Streamlit or Power BI dashboard with final screenshots.
- Add customer-level trend pages and cohort migration analysis.
- Add SQL DDL/load scripts for PostgreSQL ingestion of the final output layer.
- Add scenario assumptions by industry and country.
- Add monthly portfolio review commentary generated from KPI thresholds.

## GitHub Repo Polish

Suggested GitHub About:

`Synthetic credit risk monitoring dashboard project using Python, SQL, risk KPIs, watchlists, stress testing, validation checks, and BI-ready outputs.`

Suggested Topics:

`credit-risk`, `portfolio-monitoring`, `risk-analytics`, `data-analytics`, `business-intelligence`, `python`, `sql`, `pandas`, `powerbi`, `kpi-dashboard`, `portfolio-project`, `synthetic-data`, `stress-testing`

## Disclaimer

This credit risk analytics prototype uses a synthetic credit portfolio dataset for a simulated business case. It does not contain confidential, proprietary, or real company data and does not claim real business impact.
