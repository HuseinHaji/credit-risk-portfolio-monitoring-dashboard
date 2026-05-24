-- Rating migration matrix and downgrade analysis.

WITH migrations AS (
    SELECT
        reporting_month,
        previous_risk_rating,
        risk_rating AS current_risk_rating,
        rating_movement,
        COUNT(DISTINCT customer_id) AS customer_count,
        SUM(current_exposure) AS exposure_amount
    FROM powerbi_credit_risk_dashboard
    GROUP BY reporting_month, previous_risk_rating, risk_rating, rating_movement
)
SELECT
    reporting_month,
    previous_risk_rating,
    current_risk_rating,
    rating_movement,
    customer_count,
    exposure_amount,
    customer_count::NUMERIC / NULLIF(SUM(customer_count) OVER (PARTITION BY reporting_month), 0) AS migration_share
FROM migrations
ORDER BY reporting_month, previous_risk_rating, current_risk_rating;
