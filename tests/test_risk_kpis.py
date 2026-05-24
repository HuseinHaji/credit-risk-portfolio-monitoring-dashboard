"""Business rule tests for risk KPI outputs."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "output" / "reports"
WATCHLIST = ROOT / "output" / "watchlist"
STRESS = ROOT / "output" / "stress_tests"


def test_customer_risk_summary_business_ranges():
    df = pd.read_csv(REPORTS / "customer_risk_summary.csv")
    assert df["current_exposure"].ge(0).all()
    assert df["overdue_amount"].ge(0).all()
    assert (df["overdue_amount"] <= df["outstanding_amount"]).all()
    assert df["exposure_utilization"].ge(0).all()
    assert df["probability_of_default_proxy"].between(0, 1).all()


def test_risk_categories_are_valid():
    df = pd.read_csv(REPORTS / "customer_risk_summary.csv")
    valid_categories = {"Low Risk", "Moderate Risk", "Elevated Risk", "High Risk", "Critical Watchlist"}
    assert set(df["risk_category"]).issubset(valid_categories)


def test_watchlist_severity_values_are_valid():
    watchlist = pd.read_csv(WATCHLIST / "high_risk_watchlist.csv")
    assert not watchlist.empty
    assert set(watchlist["severity"]).issubset({"Medium", "High", "Critical"})
    assert watchlist["watchlist_reason"].str.len().gt(0).all()


def test_stress_test_output_is_not_empty():
    stress = pd.read_csv(STRESS / "stress_test_results.csv")
    assert not stress.empty
    assert {"Baseline", "Mild Downturn", "Sector Stress", "Severe Downturn"}.issubset(set(stress["scenario_name"]))
    assert stress["stressed_loss_proxy"].ge(0).all()
