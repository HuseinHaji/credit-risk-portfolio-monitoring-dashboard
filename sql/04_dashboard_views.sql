-- Dashboard views for Power BI-ready reporting

CREATE VIEW v_portfolio_exposure AS
SELECT m.month_label,
       c.customer_name,
       cc.country_name,
       i.industry_name,
       r.rating_label,
       f.exposure_amount,
       f.overdue_amount,
       f.default_flag
FROM fact_exposure_snapshot f
JOIN dim_customer c ON f.customer_id = c.customer_id
JOIN dim_country cc ON c.country_id = cc.country_id
JOIN dim_industry i ON c.industry_id = i.industry_id
JOIN dim_risk_rating r ON c.rating_code = r.rating_code
JOIN dim_date m ON f.month_key = m.month_key;

CREATE VIEW v_country_industry_exposure AS
SELECT cc.country_name,
       i.industry_name,
       SUM(f.exposure_amount) AS total_exposure,
       SUM(f.overdue_amount) AS total_overdue
FROM fact_exposure_snapshot f
JOIN dim_customer c ON f.customer_id = c.customer_id
JOIN dim_country cc ON c.country_id = cc.country_id
JOIN dim_industry i ON c.industry_id = i.industry_id
GROUP BY cc.country_name, i.industry_name;
