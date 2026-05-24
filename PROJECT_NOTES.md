# Project Notes — Credit Risk Portfolio Monitoring Dashboard

## Business problem
Provide portfolio-level visibility for credit exposure, overdue balances, rating migration, and default trends for a fictional credit insurer's commercial portfolio.

## What I built
- Synthetic data generation and transformation pipeline in `src/generate_data.py` and `src/transform_data.py`.
- SQL schema and KPI queries for reporting and dashboard-ready data.
- Power BI export pipeline via `src/export_powerbi.py`.
- Streamlit demo at `src/app.py` with metrics and bar charts.

## Key technical points
- Data modelling using dimension and fact tables.
- Financial KPIs: utilization, overdue ratio, default rate, concentration risk.
- Reproducibility through Docker, CI, and sample dataset.
- Added smoke-test CI workflow to validate the Streamlit app start.

## Project story
1. Challenge: stakeholders need regular monitoring of portfolio risk and overdue exposure.
2. Solution: build a synthetic end-to-end workflow from raw data to dashboard-ready outputs.
3. Impact: enables portfolio review, risk escalation, and prioritisation by customer, country, and industry.
4. Tradeoffs: synthetic data simplifies assumptions while demonstrating analytics design and BI delivery.

## Lessons and improvements
- Next step: add scenario/stress-testing and forward-looking exposure forecast.
- Key points: explain data assumptions, KPI definitions, and how the demo ties back to business needs.
