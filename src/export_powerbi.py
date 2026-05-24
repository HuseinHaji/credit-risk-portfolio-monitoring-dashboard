"""Export a flat Power BI-ready credit risk dashboard dataset."""

from __future__ import annotations

import pandas as pd

from config import POWERBI_DIR, PROCESSED_DIR, REPORTS_DIR, WATCHLIST_DIR, ensure_directories


def main() -> None:
    ensure_directories()
    dataset = pd.read_csv(PROCESSED_DIR / "credit_risk_customer_month.csv")
    watchlist = pd.read_csv(WATCHLIST_DIR / "high_risk_watchlist.csv")
    customer_summary = pd.read_csv(REPORTS_DIR / "customer_risk_summary.csv")[
        ["customer_id", "watchlist_flag", "recommended_action"]
    ]
    watchlist_reasons = watchlist[["customer_id", "watchlist_reason", "severity"]]

    export = (
        dataset.merge(customer_summary, on="customer_id", how="left")
        .merge(watchlist_reasons, on="customer_id", how="left")
        .rename(
            columns={
                "reporting_month": "reporting_month",
                "customer_id": "customer_id",
                "customer_name": "customer_name",
                "current_exposure": "current_exposure",
                "expected_loss_proxy": "expected_loss_proxy",
            }
        )
    )
    export["watchlist_flag"] = export["watchlist_flag"].fillna(False).astype(bool)
    export["watchlist_reason"] = export["watchlist_reason"].fillna("Not on watchlist")
    export["severity"] = export["severity"].fillna("None")
    export["recommended_action"] = export["recommended_action"].fillna("Monitor monthly")
    export["dashboard_month"] = pd.to_datetime(export["reporting_month"]).dt.strftime("%Y-%m")

    columns = [
        "dashboard_month",
        "reporting_month",
        "exposure_id",
        "customer_id",
        "customer_name",
        "country",
        "region",
        "industry",
        "company_size",
        "credit_limit",
        "current_exposure",
        "outstanding_amount",
        "overdue_amount",
        "days_past_due",
        "exposure_utilization",
        "overdue_rate",
        "collateral_value",
        "collateral_coverage",
        "currency",
        "risk_rating",
        "previous_risk_rating",
        "rating_score",
        "rating_movement",
        "rating_outlook",
        "probability_of_default_proxy",
        "expected_loss_proxy",
        "risk_category",
        "default_flag",
        "watchlist_flag",
        "watchlist_reason",
        "severity",
        "recommended_action",
    ]
    output = export[columns].sort_values(["reporting_month", "country", "industry", "customer_id"])
    output_path = POWERBI_DIR / "powerbi_credit_risk_dashboard.csv"
    output.to_csv(output_path, index=False)
    print(f"Power BI-ready dashboard export saved to {output_path}")


if __name__ == "__main__":
    main()
