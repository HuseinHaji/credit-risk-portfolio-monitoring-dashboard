"""Small Streamlit preview for generated portfolio monitoring outputs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
POWERBI_EXPORT = ROOT / "output" / "powerbi" / "powerbi_credit_risk_dashboard.csv"
SAMPLE_DATA = ROOT / "data" / "sample" / "sample_customers.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load the generated dashboard export, with a small fallback for smoke tests."""
    if POWERBI_EXPORT.exists():
        return pd.read_csv(POWERBI_EXPORT)
    sample = pd.read_csv(SAMPLE_DATA)
    return sample.rename(
        columns={
            "exposure": "current_exposure",
            "credit_limit": "credit_limit",
            "customer_name": "customer_name",
        }
    )


def main() -> None:
    st.title("Credit Risk Monitoring Dashboard")
    st.caption("Synthetic credit portfolio analytics prototype")

    df = load_data()
    latest = df
    if "reporting_month" in df.columns:
        latest = df[df["reporting_month"] == df["reporting_month"].max()]

    total_exposure = latest["current_exposure"].sum()
    total_credit = latest["credit_limit"].sum()
    utilization = total_exposure / total_credit if total_credit else 0
    overdue_amount = latest["overdue_amount"].sum() if "overdue_amount" in latest.columns else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Exposure", f"EUR {total_exposure:,.0f}")
    col2.metric("Credit Limit", f"EUR {total_credit:,.0f}")
    col3.metric("Utilization", f"{utilization:.1%}")
    col4.metric("Overdue", f"EUR {overdue_amount:,.0f}")

    if "risk_rating" in latest.columns:
        st.subheader("Exposure by Risk Rating")
        rating_chart = latest.groupby("risk_rating")["current_exposure"].sum().sort_index()
        st.bar_chart(rating_chart)

    st.subheader("Customer Risk View")
    st.dataframe(latest.head(50), use_container_width=True)


if __name__ == "__main__":
    main()
