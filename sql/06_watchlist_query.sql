-- Explainable high-risk customer watchlist logic.

WITH latest AS (
    SELECT *
    FROM powerbi_credit_risk_dashboard
    WHERE reporting_month = (SELECT MAX(reporting_month) FROM powerbi_credit_risk_dashboard)
),
scored AS (
    SELECT
        *,
        CASE
            WHEN days_past_due >= 90 OR risk_rating IN ('B', 'CCC') THEN 'Critical'
            WHEN days_past_due >= 60 OR risk_rating = 'BB' THEN 'High'
            ELSE 'Medium'
        END AS calculated_severity
    FROM latest
    WHERE watchlist_flag = TRUE
       OR days_past_due >= 45
       OR overdue_amount / NULLIF(outstanding_amount, 0) >= 0.12
       OR exposure_utilization >= 0.90
       OR risk_rating IN ('BB', 'B', 'CCC')
       OR rating_movement = 'Downgrade'
)
SELECT
    customer_id,
    customer_name,
    country,
    industry,
    current_exposure,
    overdue_amount,
    days_past_due,
    risk_rating,
    rating_movement,
    probability_of_default_proxy,
    expected_loss_proxy,
    watchlist_reason,
    calculated_severity AS severity,
    recommended_action
FROM scored
ORDER BY expected_loss_proxy DESC;
