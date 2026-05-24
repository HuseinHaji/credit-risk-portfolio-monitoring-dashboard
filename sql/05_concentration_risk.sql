-- Top customer concentration and cumulative exposure share.

WITH latest AS (
    SELECT *
    FROM powerbi_credit_risk_dashboard
    WHERE reporting_month = (SELECT MAX(reporting_month) FROM powerbi_credit_risk_dashboard)
),
customer_exposure AS (
    SELECT
        customer_id,
        customer_name,
        country,
        industry,
        risk_rating,
        SUM(current_exposure) AS exposure_amount
    FROM latest
    GROUP BY customer_id, customer_name, country, industry, risk_rating
),
ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (ORDER BY exposure_amount DESC) AS exposure_rank,
        SUM(exposure_amount) OVER (ORDER BY exposure_amount DESC) AS cumulative_exposure,
        SUM(exposure_amount) OVER () AS portfolio_exposure
    FROM customer_exposure
)
SELECT
    exposure_rank,
    customer_id,
    customer_name,
    country,
    industry,
    risk_rating,
    exposure_amount,
    exposure_amount / NULLIF(portfolio_exposure, 0) AS exposure_share,
    cumulative_exposure / NULLIF(portfolio_exposure, 0) AS cumulative_exposure_share
FROM ranked
WHERE exposure_rank <= 20
ORDER BY exposure_rank;
