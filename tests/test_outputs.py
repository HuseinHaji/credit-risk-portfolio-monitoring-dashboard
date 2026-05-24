"""Output-level regression tests for the credit risk pipeline."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"


def test_required_output_files_exist():
    expected_files = [
        OUTPUT / "reports" / "portfolio_risk_summary.csv",
        OUTPUT / "reports" / "customer_risk_summary.csv",
        OUTPUT / "reports" / "rating_migration_summary.csv",
        OUTPUT / "watchlist" / "high_risk_watchlist.csv",
        OUTPUT / "stress_tests" / "stress_test_results.csv",
        OUTPUT / "powerbi" / "powerbi_credit_risk_dashboard.csv",
        OUTPUT / "audit" / "data_quality_report.csv",
    ]
    for path in expected_files:
        assert path.exists(), f"Missing output file: {path}"


def test_portfolio_summary_required_columns_and_ranges():
    df = pd.read_csv(OUTPUT / "reports" / "portfolio_risk_summary.csv")
    required = {
        "reporting_month",
        "total_customers",
        "active_customers",
        "total_credit_limit",
        "total_exposure",
        "overdue_rate",
        "default_rate",
        "high_risk_exposure_share",
        "top_10_customer_concentration",
        "weighted_avg_risk_score",
        "expected_loss_proxy",
    }
    assert required.issubset(df.columns)
    assert not df.empty
    assert df["total_exposure"].ge(0).all()
    assert df["overdue_rate"].between(0, 1).all()
    assert df["default_rate"].between(0, 1).all()
    assert df["high_risk_exposure_share"].between(0, 1).all()


def test_powerbi_export_is_not_empty():
    df = pd.read_csv(OUTPUT / "powerbi" / "powerbi_credit_risk_dashboard.csv")
    assert not df.empty
    assert {"customer_id", "current_exposure", "risk_rating", "watchlist_flag"}.issubset(df.columns)
