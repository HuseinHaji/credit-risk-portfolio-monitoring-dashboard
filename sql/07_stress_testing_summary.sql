-- Stress testing summary for baseline and downturn scenarios.

SELECT
    scenario_name,
    reporting_month,
    stressed_exposure,
    stressed_pd_proxy,
    stressed_loss_proxy,
    incremental_loss_proxy,
    high_risk_exposure_share,
    affected_customers,
    scenario_commentary,
    RANK() OVER (ORDER BY stressed_loss_proxy DESC) AS loss_rank
FROM stress_test_results
ORDER BY stressed_loss_proxy DESC;
