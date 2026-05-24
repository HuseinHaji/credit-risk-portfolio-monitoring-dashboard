# Project Notes

## Dataset Design

The project uses a synthetic B2B credit portfolio dataset. Raw tables cover customer master data, monthly exposure snapshots, monthly risk ratings, payment behavior, default events, and macroeconomic stress scenarios.

The grain of the main processed dataset is one row per customer, exposure, and reporting month. This supports portfolio monitoring, customer drilldown, rating migration, overdue analysis, and Power BI dashboarding.

## Pipeline Architecture

1. `src/generate_synthetic_data.py`: creates deterministic raw CSV files.
2. `src/validate_data.py`: runs schema, key, domain, date, null, and range checks.
3. `src/transform_data.py`: joins raw files into an enriched customer-month dataset.
4. `src/calculate_risk_kpis.py`: produces portfolio, customer, and migration reports.
5. `src/generate_watchlist.py`: applies transparent high-risk customer rules.
6. `src/stress_testing.py`: applies scenario shocks to exposure, PD proxy, and LGD proxy.
7. `src/export_powerbi.py`: creates a flat BI-ready dashboard export.

## Validation Checks

The audit layer checks required columns, duplicate customer IDs, duplicate exposure IDs, cross-table customer key consistency, non-negative financial values, overdue amount versus outstanding amount, utilization reasonableness, valid ratings, valid flags, valid dates, and nulls in critical fields.

The validation output is saved to `output/audit/data_quality_report.csv`.

## KPI Formulas

- Exposure utilization = `current_exposure / credit_limit`
- Overdue rate = `overdue_amount / outstanding_amount`
- Default rate = `default_flag customer-month count / customer-month count`
- Expected loss proxy = `current_exposure * probability_of_default_proxy * 45% LGD proxy`
- Weighted average risk score = `sum(rating_score * current_exposure) / sum(current_exposure)`
- Top 10 customer concentration = `top 10 customer exposure / portfolio exposure`
- High-risk exposure share = `high-risk exposure / portfolio exposure`

These are analytical portfolio monitoring metrics, not regulatory capital model calculations.

## Risk Category Logic

- `AAA`, `AA`: Low Risk
- `A`: Moderate Risk
- `BBB`: Elevated Risk
- `BB`: High Risk
- `B`, `CCC`: Critical Watchlist

## Watchlist Logic

Customers are flagged when one or more conditions are present:

- Days past due exceeds the monitoring threshold.
- Overdue ratio is above threshold.
- Exposure utilization is high.
- Current risk rating is weak.
- Rating movement is a downgrade.
- Expected loss proxy is high.
- Default indicator exists.
- Exposure is large relative to the portfolio.

Watchlist records include severity, reason text, and recommended action. The logic is designed to be explainable for portfolio review meetings.

## Stress Testing Assumptions

Scenarios apply shocks to PD proxy, LGD proxy, and exposure:

- Baseline: no additional stress.
- Mild Downturn: moderate deterioration.
- Sector Stress: higher risk affecting cyclical or weak segments.
- Severe Downturn: broad deterioration in defaults, recoveries, and exposure.

This is an analytical stress-testing prototype using synthetic data. It is not a regulatory capital model.

## SQL Layer

The SQL files use PostgreSQL-style syntax and demonstrate dashboard analytics patterns:

- CTEs for staged transformations.
- `CASE WHEN` for watchlist and severity logic.
- Aggregations for portfolio KPIs.
- Window functions for concentration and migration shares.
- Joins and date filtering for latest-month reporting.

## Power BI Export Design

`output/powerbi/powerbi_credit_risk_dashboard.csv` is a flat dashboard-ready table. It includes customer attributes, exposure values, payment risk features, risk rating fields, default indicator, expected loss proxy, watchlist attributes, and recommended actions.

The table is intentionally denormalized to simplify Power BI visuals while preserving the analytical grain needed for customer drilldown.

## Testing Approach

The `tests/` folder verifies:

- Raw synthetic files are created.
- Required outputs exist.
- Required columns are present.
- Exposure values are non-negative.
- Overdue amount does not exceed outstanding amount.
- KPI rates are within valid ranges.
- Risk categories and watchlist severities are valid.
- Stress test and Power BI outputs are not empty.
- Data quality report is populated and has no failed critical checks.

## Known Limitations

- Data is synthetic and simplified.
- PD proxy and LGD proxy are not calibrated from historical default data.
- Default events are generated for demonstration, not statistical modeling.
- Stress scenarios are illustrative and not linked to official macroeconomic forecasts.
- No real company data or real business impact is claimed.

## Future Extensions

- Add a Power BI dashboard file or a richer Streamlit dashboard.
- Add screenshots for each dashboard page.
- Add industry-specific stress multipliers.
- Add migration trend commentary.
- Add SQL loading scripts for PostgreSQL.
- Add monthly automated report generation.
