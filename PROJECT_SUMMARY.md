# Project Summary

## Problem

Credit risk and portfolio teams need regular visibility into customer exposure, overdue behavior, defaults, rating migration, and concentration risk. This simulated business case asks how a financial services or credit insurance team could convert loan-level or customer-level records into reliable management reporting.

## Solution

This project builds a reproducible credit risk analytics prototype using a synthetic credit portfolio dataset. Python scripts generate raw customer, exposure, rating, payment, default, and scenario records, validate data quality, engineer risk features, calculate portfolio KPIs, produce a high-risk customer watchlist, run stress testing, and export a BI-ready dashboard table.

## Workflow

```text
synthetic raw data
  -> validation and audit report
  -> enriched customer-month risk table
  -> portfolio and customer KPI reports
  -> watchlist with reasons and actions
  -> stress test results
  -> Power BI-ready export
  -> PostgreSQL-style SQL analytics layer
```

## Business Value

- Tracks credit exposure, overdue behavior, default indicators, and risk ratings.
- Identifies high-risk customers requiring review.
- Measures concentration risk by customer, country, industry, company size, and rating.
- Produces clean BI-ready datasets for portfolio risk dashboarding.
- Demonstrates explainable stress testing and risk reporting logic.

## Technical Skills Demonstrated

| Skill | Where demonstrated |
|---|---|
| Python | pipeline scripts, synthetic data generation, risk KPI calculations |
| pandas | joins, transformations, aggregations, output tables |
| numpy | deterministic synthetic data generation and numeric simulation |
| SQL | PostgreSQL-style monitoring queries with CTEs and window functions |
| Credit risk analytics | exposure, overdue, default, ratings, expected loss proxy |
| Portfolio monitoring | concentration, high-risk exposure, customer summaries |
| Stress testing | PD, LGD, and exposure shocks by scenario |
| KPI design | utilization, overdue rate, default rate, expected loss proxy |
| Data validation | schema, duplicate, domain, and consistency checks |
| Power BI-ready modeling | flat export table for dashboard design |
| pytest | output, schema, validation, and KPI tests |
| CI/CD | GitHub Actions pipeline smoke test and pytest |

## Outputs

- Executive portfolio summary.
- Customer-level risk summary.
- High-risk customer watchlist.
- Rating migration summary.
- Stress test results.
- Power BI-ready dashboard export.
- Data quality audit report.

## How This Maps To Real Analyst Work

The project mirrors common analyst responsibilities in financial services and insurance analytics: reconciling raw data, validating data quality, creating KPI logic, segmenting exposure, explaining risk drivers, building management-ready outputs, writing SQL for dashboard layers, documenting assumptions, and testing the pipeline so recurring reporting is reliable.

The implementation is intentionally framed as a portfolio implementation using synthetic data. It demonstrates practical analytics thinking without claiming real company data, production use, or measured business impact.
