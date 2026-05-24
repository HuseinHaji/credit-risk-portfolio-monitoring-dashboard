"""Run scenario-based analytical stress testing on the synthetic portfolio."""

from __future__ import annotations

import pandas as pd

from config import RAW_DIR, STRESS_TEST_DIR, PROCESSED_DIR, ensure_directories

BASE_LGD_PROXY = 0.45


def run_stress_tests(dataset: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    """Apply PD, LGD, and exposure shocks to the latest reporting month."""
    latest_month = dataset["reporting_month"].max()
    latest = dataset[dataset["reporting_month"] == latest_month].copy()
    baseline_loss = (latest["current_exposure"] * latest["probability_of_default_proxy"] * BASE_LGD_PROXY).sum()
    rows = []
    for scenario in scenarios.itertuples(index=False):
        stressed_exposure = latest["current_exposure"] * scenario.exposure_shock
        stressed_pd = (latest["probability_of_default_proxy"] * scenario.pd_shock).clip(upper=0.85)
        stressed_loss = (stressed_exposure * stressed_pd * BASE_LGD_PROXY * scenario.lgd_shock).sum()
        high_risk_exposure = stressed_exposure[latest["risk_category"].isin(["High Risk", "Critical Watchlist"])].sum()
        affected = latest[(stressed_pd >= 0.06) | (latest["days_past_due"] >= 45)]["customer_id"].nunique()
        rows.append(
            {
                "scenario_name": scenario.scenario_name,
                "reporting_month": latest_month,
                "stressed_exposure": round(stressed_exposure.sum(), 2),
                "stressed_pd_proxy": round(stressed_pd.mean(), 4),
                "stressed_loss_proxy": round(stressed_loss, 2),
                "incremental_loss_proxy": round(stressed_loss - baseline_loss, 2),
                "high_risk_exposure_share": round(high_risk_exposure / stressed_exposure.sum(), 4),
                "affected_customers": int(affected),
                "scenario_commentary": scenario.description,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    ensure_directories()
    dataset = pd.read_csv(PROCESSED_DIR / "credit_risk_customer_month.csv")
    scenarios = pd.read_csv(RAW_DIR / "macroeconomic_scenarios.csv")
    results = run_stress_tests(dataset, scenarios)
    output_path = STRESS_TEST_DIR / "stress_test_results.csv"
    results.to_csv(output_path, index=False)
    print(f"Stress test results saved to {output_path}")


if __name__ == "__main__":
    main()
