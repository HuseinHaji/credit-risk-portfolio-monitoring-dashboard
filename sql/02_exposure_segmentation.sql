-- Exposure segmentation by country, industry, company size, and rating.

WITH latest AS (
    SELECT *
    FROM powerbi_credit_risk_dashboard
    WHERE reporting_month = (SELECT MAX(reporting_month) FROM powerbi_credit_risk_dashboard)
),
segment_rollup AS (
    SELECT 'country' AS segment_type, country AS segment_name, SUM(current_exposure) AS exposure_amount
    FROM latest
    GROUP BY country
    UNION ALL
    SELECT 'industry', industry, SUM(current_exposure)
    FROM latest
    GROUP BY industry
    UNION ALL
    SELECT 'company_size', company_size, SUM(current_exposure)
    FROM latest
    GROUP BY company_size
    UNION ALL
    SELECT 'risk_rating', risk_rating, SUM(current_exposure)
    FROM latest
    GROUP BY risk_rating
)
SELECT
    segment_type,
    segment_name,
    exposure_amount,
    exposure_amount / NULLIF(SUM(exposure_amount) OVER (PARTITION BY segment_type), 0) AS exposure_share,
    RANK() OVER (PARTITION BY segment_type ORDER BY exposure_amount DESC) AS exposure_rank
FROM segment_rollup
ORDER BY segment_type, exposure_rank;
