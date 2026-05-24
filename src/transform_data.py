"""Create cleaned and enriched customer-month credit risk datasets."""

from __future__ import annotations

import pandas as pd

from config import PROCESSED_DIR, RAW_DIR, RISK_CATEGORY_MAP, ensure_directories

LGD_PROXY = 0.45


def classify_rating_movement(previous_rating: str, current_rating: str) -> str:
    """Classify risk rating movement from the borrower's perspective."""
    order = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC"]
    previous_index = order.index(previous_rating)
    current_index = order.index(current_rating)
    if current_index > previous_index:
        return "Downgrade"
    if current_index < previous_index:
        return "Upgrade"
    return "Stable"


def build_customer_month_dataset() -> pd.DataFrame:
    """Join raw tables and calculate reusable customer-month risk features."""
    customers = pd.read_csv(RAW_DIR / "customers.csv")
    exposures = pd.read_csv(RAW_DIR / "credit_exposures.csv")
    ratings = pd.read_csv(RAW_DIR / "risk_ratings.csv")
    defaults = pd.read_csv(RAW_DIR / "default_events.csv")

    default_customers = defaults.assign(default_flag=1)[["customer_id", "default_flag"]].drop_duplicates()

    dataset = (
        exposures.merge(customers, on="customer_id", how="left")
        .merge(ratings, on=["customer_id", "reporting_month"], how="left")
        .merge(default_customers, on="customer_id", how="left")
    )
    dataset["default_flag"] = dataset["default_flag"].fillna(0).astype(int)
    dataset["reporting_month"] = pd.to_datetime(dataset["reporting_month"]).dt.date.astype(str)
    dataset["exposure_utilization"] = dataset["current_exposure"] / dataset["credit_limit"].replace(0, pd.NA)
    dataset["overdue_rate"] = dataset["overdue_amount"] / dataset["outstanding_amount"].replace(0, pd.NA)
    dataset["collateral_coverage"] = dataset["collateral_value"] / dataset["current_exposure"].replace(0, pd.NA)
    dataset["expected_loss_proxy"] = (
        dataset["current_exposure"] * dataset["probability_of_default_proxy"] * LGD_PROXY
    ).round(2)
    dataset["risk_category"] = dataset["risk_rating"].map(RISK_CATEGORY_MAP)
    dataset["rating_movement"] = dataset.apply(
        lambda row: classify_rating_movement(row["previous_risk_rating"], row["risk_rating"]),
        axis=1,
    )
    dataset["overdue_ratio"] = dataset["overdue_rate"].fillna(0)
    dataset["large_exposure_flag"] = dataset["current_exposure"] >= dataset["current_exposure"].quantile(0.90)
    dataset["high_risk_flag"] = dataset["risk_category"].isin(["High Risk", "Critical Watchlist"])

    columns = [
        "exposure_id",
        "customer_id",
        "customer_name",
        "country",
        "region",
        "industry",
        "company_size",
        "active_flag",
        "reporting_month",
        "credit_limit",
        "current_exposure",
        "outstanding_amount",
        "overdue_amount",
        "days_past_due",
        "collateral_value",
        "collateral_coverage",
        "exposure_status",
        "currency",
        "risk_rating",
        "previous_risk_rating",
        "rating_score",
        "rating_movement",
        "probability_of_default_proxy",
        "rating_outlook",
        "default_flag",
        "exposure_utilization",
        "overdue_rate",
        "overdue_ratio",
        "expected_loss_proxy",
        "risk_category",
        "large_exposure_flag",
        "high_risk_flag",
    ]
    return dataset[columns].sort_values(["reporting_month", "customer_id"])


def main() -> None:
    ensure_directories()
    dataset = build_customer_month_dataset()
    output_path = PROCESSED_DIR / "credit_risk_customer_month.csv"
    dataset.to_csv(output_path, index=False)
    print(f"Processed customer-month dataset saved to {output_path}")


if __name__ == "__main__":
    main()
