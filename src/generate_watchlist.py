"""Generate an explainable high-risk customer watchlist."""

from __future__ import annotations

import pandas as pd

from config import REPORTS_DIR, WATCHLIST_DIR, ensure_directories


def _watchlist_reason(row: pd.Series) -> str:
    reasons = []
    if row["days_past_due"] >= 60:
        reasons.append("high days past due")
    if row["overdue_amount"] / row["outstanding_amount"] >= 0.12 if row["outstanding_amount"] else False:
        reasons.append("overdue ratio above threshold")
    if row["exposure_utilization"] >= 0.90:
        reasons.append("high exposure utilization")
    if row["risk_rating"] in ["BB", "B", "CCC"]:
        reasons.append("weak risk rating")
    if row["rating_movement"] == "Downgrade":
        reasons.append("rating downgrade")
    if row["expected_loss_proxy"] >= 50_000:
        reasons.append("high expected loss proxy")
    concentration_threshold = row.get("concentration_threshold", float("inf"))
    if row["current_exposure"] >= concentration_threshold:
        reasons.append("large exposure concentration")
    return "; ".join(reasons) or "monthly monitoring trigger"


def _severity(row: pd.Series) -> str:
    overdue_ratio = row["overdue_amount"] / row["outstanding_amount"] if row["outstanding_amount"] else 0
    if row["risk_rating"] in ["B", "CCC"] or row["days_past_due"] >= 90 or row["expected_loss_proxy"] >= 100_000:
        return "Critical"
    if row["risk_rating"] == "BB" or row["days_past_due"] >= 60 or overdue_ratio >= 0.18:
        return "High"
    return "Medium"


def _recommended_action(row: pd.Series) -> str:
    if row["severity"] == "Critical":
        return "Place on critical watchlist"
    if row["days_past_due"] >= 60:
        return "Follow up on overdue balance"
    if row["exposure_utilization"] >= 0.90:
        return "Review credit limit"
    if row["risk_rating"] in ["BB", "B", "CCC"]:
        return "Request updated financials"
    return "Monitor monthly"


def main() -> None:
    ensure_directories()
    customers = pd.read_csv(REPORTS_DIR / "customer_risk_summary.csv")
    threshold = customers["current_exposure"].quantile(0.90)
    customers["concentration_threshold"] = threshold
    watchlist = customers[
        (customers["watchlist_flag"])
        | (customers["days_past_due"] >= 45)
        | (customers["risk_rating"].isin(["BB", "B", "CCC"]))
        | (customers["current_exposure"] >= threshold)
    ].copy()
    watchlist["watchlist_reason"] = watchlist.apply(_watchlist_reason, axis=1)
    watchlist["severity"] = watchlist.apply(_severity, axis=1)
    watchlist["recommended_action"] = watchlist.apply(_recommended_action, axis=1)
    output = watchlist[
        [
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
        ]
    ].sort_values(["severity", "expected_loss_proxy"], ascending=[True, False])
    output.to_csv(WATCHLIST_DIR / "high_risk_watchlist.csv", index=False)
    print(f"High-risk customer watchlist saved to {WATCHLIST_DIR}")


if __name__ == "__main__":
    main()
