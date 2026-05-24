-- Expected loss proxy calculation by customer and segment.
-- This is an analytical proxy, not a regulatory capital model.

WITH latest AS (
    SELECT *
    FROM powerbi_credit_risk_dashboard
    WHERE reporting_month = (SELECT MAX(reporting_month) FROM powerbi_credit_risk_dashboard)
)
SELECT
    customer_id,
    customer_name,
    country,
    industry,
    risk_rating,
    current_exposure,
    probability_of_default_proxy,
    0.45 AS lgd_proxy,
    current_exposure * probability_of_default_proxy * 0.45 AS expected_loss_proxy_calculated,
    expected_loss_proxy AS expected_loss_proxy_reported
FROM latest
ORDER BY expected_loss_proxy_calculated DESC;
