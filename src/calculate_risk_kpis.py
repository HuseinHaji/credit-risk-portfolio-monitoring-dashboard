"""Calculate portfolio-level and customer-level credit risk KPI tables."""

from __future__ import annotations

import pandas as pd

from config import PROCESSED_DIR, REPORTS_DIR, ensure_directories


def _weighted_average(values: pd.Series, weights: pd.Series) -> float:
    total_weight = weights.sum()
    if total_weight == 0:
        return 0.0
    return float((values * weights).sum() / total_weight)


def calculate_portfolio_summary(dataset: pd.DataFrame) -> pd.DataFrame:
    """Aggregate executive portfolio KPIs by reporting month."""
    rows = []
    for month, month_df in dataset.groupby("reporting_month"):
        total_exposure = month_df["current_exposure"].sum()
        top_10_exposure = month_df.nlargest(10, "current_exposure")["current_exposure"].sum()
        high_risk_exposure = month_df.loc[month_df["high_risk_flag"], "current_exposure"].sum()
        rows.append(
            {
                "reporting_month": month,
                "total_customers": month_df["customer_id"].nunique(),
                "active_customers": int(month_df.loc[month_df["active_flag"] == 1, "customer_id"].nunique()),
                "total_credit_limit": round(month_df["credit_limit"].sum(), 2),
                "total_exposure": round(total_exposure, 2),
                "outstanding_amount": round(month_df["outstanding_amount"].sum(), 2),
                "overdue_amount": round(month_df["overdue_amount"].sum(), 2),
                "exposure_utilization": round(total_exposure / month_df["credit_limit"].sum(), 4),
                "overdue_rate": round(month_df["overdue_amount"].sum() / month_df["outstanding_amount"].sum(), 4),
                "default_rate": round(month_df["default_flag"].sum() / len(month_df), 4),
                "high_risk_exposure": round(high_risk_exposure, 2),
                "high_risk_exposure_share": round(high_risk_exposure / total_exposure, 4),
                "top_10_customer_concentration": round(top_10_exposure / total_exposure, 4),
                "weighted_avg_risk_score": round(_weighted_average(month_df["rating_score"], month_df["current_exposure"]), 3),
                "expected_loss_proxy": round(month_df["expected_loss_proxy"].sum(), 2),
            }
        )
    return pd.DataFrame(rows).sort_values("reporting_month")


def calculate_customer_summary(dataset: pd.DataFrame) -> pd.DataFrame:
    """Create latest-month customer risk summary for reporting and watchlist use."""
    latest_month = dataset["reporting_month"].max()
    latest = dataset[dataset["reporting_month"] == latest_month].copy()
    latest["watchlist_flag"] = (
        (latest["days_past_due"] >= 45)
        | (latest["overdue_ratio"] >= 0.12)
        | (latest["exposure_utilization"] >= 0.9)
        | (latest["risk_rating"].isin(["BB", "B", "CCC"]))
        | (latest["rating_movement"] == "Downgrade")
        | (latest["default_flag"] == 1)
        | (latest["large_exposure_flag"])
    )
    latest["recommended_action"] = "Monitor monthly"
    latest.loc[latest["days_past_due"] >= 45, "recommended_action"] = "Follow up on overdue balance"
    latest.loc[latest["exposure_utilization"] >= 0.9, "recommended_action"] = "Review credit limit"
    latest.loc[latest["risk_rating"].isin(["B", "CCC"]) | (latest["default_flag"] == 1), "recommended_action"] = "Escalate to risk team"
    latest.loc[(latest["risk_rating"] == "CCC") | (latest["days_past_due"] >= 90), "recommended_action"] = "Place on critical watchlist"

    columns = [
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
    ]
    return latest[columns].sort_values(["watchlist_flag", "expected_loss_proxy"], ascending=[False, False])


def calculate_rating_migration(dataset: pd.DataFrame) -> pd.DataFrame:
    """Summarize rating movements by month and exposure amount."""
    grouped = (
        dataset.groupby(["reporting_month", "previous_risk_rating", "risk_rating", "rating_movement"], as_index=False)
        .agg(customer_count=("customer_id", "nunique"), exposure_amount=("current_exposure", "sum"))
        .rename(columns={"risk_rating": "current_risk_rating", "rating_movement": "migration_type"})
    )
    totals = grouped.groupby("reporting_month")["customer_count"].transform("sum")
    grouped["migration_share"] = (grouped["customer_count"] / totals).round(4)
    grouped["exposure_amount"] = grouped["exposure_amount"].round(2)
    return grouped.sort_values(["reporting_month", "previous_risk_rating", "current_risk_rating"])


def main() -> None:
    ensure_directories()
    dataset = pd.read_csv(PROCESSED_DIR / "credit_risk_customer_month.csv")
    portfolio = calculate_portfolio_summary(dataset)
    customers = calculate_customer_summary(dataset)
    migration = calculate_rating_migration(dataset)

    portfolio.to_csv(REPORTS_DIR / "portfolio_risk_summary.csv", index=False)
    customers.to_csv(REPORTS_DIR / "customer_risk_summary.csv", index=False)
    migration.to_csv(REPORTS_DIR / "rating_migration_summary.csv", index=False)
    print(f"Risk KPI reports saved to {REPORTS_DIR}")


if __name__ == "__main__":
    main()
