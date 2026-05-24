import streamlit as st
import pandas as pd
import os


@st.cache_data
def load_data(path: str):
    return pd.read_csv(path)


DATA_PATH = os.path.join("data", "sample", "sample_customers.csv")


def main():
    st.title("Credit Risk Portfolio Monitoring — Demo")

    df = load_data(DATA_PATH)

    total_exposure = df["exposure"].sum()
    total_credit = df["credit_limit"].sum()
    utilization = (df["exposure"] / df["credit_limit"]).mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Exposure", f"{total_exposure:,.0f}")
    col2.metric("Total Credit Limit", f"{total_credit:,.0f}")
    col3.metric("Avg Utilization", f"{utilization:.2%}")

    st.subheader("Sample Customers")
    st.dataframe(df)

    st.subheader("Exposure by Customer")
    chart_df = df.set_index("customer_name")["exposure"]
    st.bar_chart(chart_df)


if __name__ == "__main__":
    main()
