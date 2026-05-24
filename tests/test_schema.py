"""Schema tests for core dashboard-ready datasets."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"


def test_customer_summary_schema():
    df = pd.read_csv(OUTPUT / "reports" / "customer_risk_summary.csv")
    required = {
        "customer_id",
        "customer_name",
        "country",
        "region",
        "industry",
        "company_size",
        "reporting_month",
        "credit_limit",
        "current_exposure",
        "outstanding_amount",
        "overdue_amount",
        "days_past_due",
        "exposure_utilization",
        "risk_rating",
        "previous_risk_rating",
        "rating_movement",
        "probability_of_default_proxy",
        "expected_loss_proxy",
        "risk_category",
        "watchlist_flag",
        "recommended_action",
    }
    assert required.issubset(df.columns)


def test_watchlist_schema():
    df = pd.read_csv(OUTPUT / "watchlist" / "high_risk_watchlist.csv")
    required = {
        "customer_id",
        "customer_name",
        "country",
        "industry",
        "current_exposure",
        "overdue_amount",
        "days_past_due",
        "risk_rating",
        "rating_movement",
        "probability_of_default_proxy",
        "expected_loss_proxy",
        "watchlist_reason",
        "severity",
        "recommended_action",
    }
    assert required.issubset(df.columns)
