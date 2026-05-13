-- KPI queries for portfolio monitoring

-- Total credit exposure
SELECT SUM(exposure_amount) AS total_exposure
FROM fact_exposure_snapshot;

-- Total credit limit
SELECT SUM(c.credit_limit) AS total_credit_limit
FROM dim_customer c;

-- Utilization rate
SELECT SUM(f.exposure_amount) / SUM(c.credit_limit) AS utilization_rate
FROM fact_exposure_snapshot f
JOIN dim_customer c ON f.customer_id = c.customer_id;

-- Overdue exposure and ratio
SELECT SUM(overdue_amount) AS total_overdue,
       SUM(overdue_amount) / SUM(exposure_amount) AS overdue_ratio
FROM fact_exposure_snapshot;

-- Default rate
SELECT SUM(CASE WHEN default_flag THEN 1 ELSE 0 END)::NUMERIC / COUNT(*) AS default_rate
FROM fact_exposure_snapshot;

-- Exposure-weighted risk score
SELECT SUM(f.exposure_amount * r.risk_weight)::NUMERIC / SUM(f.exposure_amount) AS exposure_weighted_risk_score
FROM fact_exposure_snapshot f
JOIN dim_customer c ON f.customer_id = c.customer_id
JOIN dim_risk_rating r ON c.rating_code = r.rating_code;

-- Exposure by country
SELECT d.country_name, SUM(f.exposure_amount) AS exposure
FROM fact_exposure_snapshot f
JOIN dim_customer c ON f.customer_id = c.customer_id
JOIN dim_country d ON c.country_id = d.country_id
GROUP BY d.country_name
ORDER BY exposure DESC;

-- Monthly exposure trend
SELECT m.month_label, SUM(f.exposure_amount) AS exposure
FROM fact_exposure_snapshot f
JOIN dim_date m ON f.month_key = m.month_key
GROUP BY m.month_label
ORDER BY m.month_start;
