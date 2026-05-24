-- Default, overdue, and delinquency monitoring by month.

SELECT
    reporting_month,
    country,
    industry,
    COUNT(DISTINCT customer_id) AS customers,
    SUM(current_exposure) AS exposure_amount,
    SUM(overdue_amount) AS overdue_amount,
    SUM(overdue_amount) / NULLIF(SUM(outstanding_amount), 0) AS overdue_rate,
    AVG(CASE WHEN days_past_due >= 30 THEN 1 ELSE 0 END)::NUMERIC AS thirty_plus_dpd_rate,
    AVG(CASE WHEN days_past_due >= 60 THEN 1 ELSE 0 END)::NUMERIC AS sixty_plus_dpd_rate,
    AVG(default_flag::INT)::NUMERIC AS default_rate
FROM powerbi_credit_risk_dashboard
GROUP BY reporting_month, country, industry
ORDER BY reporting_month, overdue_rate DESC;
