-- Portfolio exposure overview for an executive credit risk dashboard.
-- PostgreSQL-style query using the Power BI dashboard export as base table.

WITH latest_month AS (
    SELECT MAX(reporting_month) AS reporting_month
    FROM powerbi_credit_risk_dashboard
),
portfolio AS (
    SELECT d.*
    FROM powerbi_credit_risk_dashboard d
    JOIN latest_month m
      ON d.reporting_month = m.reporting_month
)
SELECT
    reporting_month,
    COUNT(DISTINCT customer_id) AS total_customers,
    SUM(credit_limit) AS total_credit_limit,
    SUM(current_exposure) AS total_exposure,
    SUM(outstanding_amount) AS outstanding_amount,
    SUM(overdue_amount) AS overdue_amount,
    SUM(current_exposure) / NULLIF(SUM(credit_limit), 0) AS exposure_utilization,
    SUM(overdue_amount) / NULLIF(SUM(outstanding_amount), 0) AS overdue_rate,
    AVG(default_flag::INT) AS default_rate,
    SUM(expected_loss_proxy) AS expected_loss_proxy
FROM portfolio
GROUP BY reporting_month;
