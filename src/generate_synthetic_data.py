"""Generate a deterministic synthetic B2B credit portfolio dataset."""

from __future__ import annotations

import numpy as np
import pandas as pd

from config import RAW_DIR, RANDOM_SEED, REFERENCE_DIR, RISK_SCORE_MAP, VALID_RISK_RATINGS, ensure_directories

CUSTOMER_COUNT = 120
MONTHS = pd.date_range("2024-01-01", periods=18, freq="MS")

COUNTRIES = [
    ("Germany", "DACH"),
    ("Austria", "DACH"),
    ("Switzerland", "DACH"),
    ("France", "Western Europe"),
    ("Netherlands", "Western Europe"),
    ("Belgium", "Western Europe"),
    ("Poland", "Central Europe"),
    ("Italy", "Southern Europe"),
    ("Spain", "Southern Europe"),
    ("Sweden", "Nordics"),
]

INDUSTRIES = [
    "Manufacturing",
    "Wholesale",
    "Construction",
    "Logistics",
    "Automotive Suppliers",
    "Chemicals",
    "Technology",
    "Food & Beverage",
    "Retail",
    "Energy",
]

COMPANY_SIZES = ["Small", "Mid-Market", "Large", "Enterprise"]
OUTLOOKS = ["Positive", "Stable", "Negative"]

PD_PROXY = {
    "AAA": 0.002,
    "AA": 0.004,
    "A": 0.008,
    "BBB": 0.018,
    "BB": 0.045,
    "B": 0.095,
    "CCC": 0.18,
}


def _rating_shift(base_rating: str, month_index: int, rng: np.random.Generator) -> str:
    ratings = VALID_RISK_RATINGS
    base_index = ratings.index(base_rating)
    drift = 1 if month_index > 9 and rng.random() < 0.12 else 0
    random_move = rng.choice([-1, 0, 0, 0, 1], p=[0.08, 0.34, 0.34, 0.16, 0.08])
    new_index = min(max(base_index + drift + random_move, 0), len(ratings) - 1)
    return ratings[new_index]


def create_customers(rng: np.random.Generator) -> pd.DataFrame:
    """Create synthetic customer master data for a commercial credit portfolio."""
    rows = []
    for customer_number in range(1, CUSTOMER_COUNT + 1):
        country, region = COUNTRIES[int(rng.integers(0, len(COUNTRIES)))]
        company_size = rng.choice(COMPANY_SIZES, p=[0.25, 0.42, 0.23, 0.10])
        onboarding_date = pd.Timestamp("2018-01-01") + pd.to_timedelta(int(rng.integers(0, 2100)), unit="D")
        rows.append(
            {
                "customer_id": f"CUST{customer_number:04d}",
                "customer_name": f"Portfolio Customer {customer_number:04d}",
                "country": country,
                "region": region,
                "industry": rng.choice(INDUSTRIES),
                "company_size": company_size,
                "onboarding_date": onboarding_date.date().isoformat(),
                "active_flag": int(rng.random() > 0.06),
            }
        )
    return pd.DataFrame(rows)


def create_ratings(customers: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Create monthly rating snapshots with previous rating and PD proxy fields."""
    base_ratings = rng.choice(VALID_RISK_RATINGS, size=len(customers), p=[0.08, 0.14, 0.27, 0.24, 0.16, 0.08, 0.03])
    rows = []
    for customer_id, base_rating in zip(customers["customer_id"], base_ratings):
        previous_rating = base_rating
        for month_index, month in enumerate(MONTHS):
            current_rating = _rating_shift(previous_rating if month_index else base_rating, month_index, rng)
            pd_noise = rng.uniform(0.85, 1.25)
            rows.append(
                {
                    "customer_id": customer_id,
                    "reporting_month": month.date().isoformat(),
                    "risk_rating": current_rating,
                    "previous_risk_rating": previous_rating,
                    "rating_score": RISK_SCORE_MAP[current_rating],
                    "probability_of_default_proxy": round(PD_PROXY[current_rating] * pd_noise, 4),
                    "rating_outlook": rng.choice(OUTLOOKS, p=[0.12, 0.68, 0.20]),
                }
            )
            previous_rating = current_rating
    return pd.DataFrame(rows)


def create_exposures(customers: pd.DataFrame, ratings: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Create monthly exposure snapshots with overdue and collateral behavior."""
    size_limit = {
        "Small": (75_000, 550_000),
        "Mid-Market": (350_000, 2_200_000),
        "Large": (1_250_000, 6_500_000),
        "Enterprise": (4_000_000, 14_000_000),
    }
    customer_limits = {
        row.customer_id: float(rng.integers(*size_limit[row.company_size]))
        for row in customers.itertuples(index=False)
    }
    rating_lookup = ratings.set_index(["customer_id", "reporting_month"])
    rows = []
    exposure_id = 1
    for customer in customers.itertuples(index=False):
        base_limit = customer_limits[customer.customer_id]
        base_utilization = rng.uniform(0.22, 0.76)
        for month_index, month in enumerate(MONTHS):
            rating_row = rating_lookup.loc[(customer.customer_id, month.date().isoformat())]
            rating_score = float(rating_row["rating_score"])
            seasonal_factor = 1 + 0.06 * np.sin(month_index / 2.5)
            utilization = np.clip(base_utilization + (rating_score - 4) * 0.035 + rng.normal(0, 0.07), 0.04, 1.25)
            credit_limit = round(base_limit * rng.uniform(0.96, 1.05), 2)
            current_exposure = round(credit_limit * utilization * seasonal_factor, 2)
            outstanding_amount = round(current_exposure * rng.uniform(0.72, 1.02), 2)
            overdue_ratio = np.clip((rating_score / 10) * rng.uniform(0.01, 0.18), 0, 0.55)
            overdue_amount = round(min(outstanding_amount, outstanding_amount * overdue_ratio), 2)
            days_past_due = int(max(0, rng.normal(overdue_ratio * 160, 18))) if overdue_amount > 0 else 0
            collateral_value = round(current_exposure * rng.uniform(0.05, 0.65), 2)
            rows.append(
                {
                    "exposure_id": f"EXP{exposure_id:07d}",
                    "customer_id": customer.customer_id,
                    "reporting_month": month.date().isoformat(),
                    "credit_limit": credit_limit,
                    "current_exposure": current_exposure,
                    "outstanding_amount": outstanding_amount,
                    "overdue_amount": overdue_amount,
                    "days_past_due": days_past_due,
                    "collateral_value": collateral_value,
                    "exposure_status": "Closed" if customer.active_flag == 0 else "Active",
                    "currency": "EUR",
                }
            )
            exposure_id += 1
    return pd.DataFrame(rows)


def create_default_events(
    exposures: pd.DataFrame,
    ratings: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Create a small number of synthetic default events for weak-rated customers."""
    latest_ratings = ratings.sort_values("reporting_month").groupby("customer_id").tail(1)
    weak_customers = latest_ratings[latest_ratings["risk_rating"].isin(["BB", "B", "CCC"])]["customer_id"].tolist()
    columns = [
        "default_event_id",
        "customer_id",
        "event_date",
        "default_flag",
        "default_reason",
        "recovery_amount",
        "loss_amount",
    ]
    if not weak_customers:
        return pd.DataFrame(columns=columns)

    selected = rng.choice(weak_customers, size=min(14, len(weak_customers)), replace=False)
    rows = []
    for event_number, customer_id in enumerate(selected, start=1):
        exposure_sample = exposures[exposures["customer_id"] == customer_id].sample(1, random_state=RANDOM_SEED + event_number)
        event_date = pd.to_datetime(exposure_sample["reporting_month"].iloc[0]) + pd.to_timedelta(int(rng.integers(4, 26)), unit="D")
        outstanding = float(exposure_sample["outstanding_amount"].iloc[0])
        loss_amount = round(outstanding * rng.uniform(0.18, 0.62), 2)
        rows.append(
            {
                "default_event_id": f"DEF{event_number:05d}",
                "customer_id": customer_id,
                "event_date": event_date.date().isoformat(),
                "default_flag": 1,
                "default_reason": rng.choice(["Insolvency filing", "Payment default", "Restructuring", "Covenant breach"]),
                "recovery_amount": round(loss_amount * rng.uniform(0.08, 0.45), 2),
                "loss_amount": loss_amount,
            }
        )
    return pd.DataFrame(rows, columns=columns)


def create_payments(exposures: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Create monthly expected and actual payment behavior."""
    rows = []
    latest_exposures = exposures.copy()
    for payment_number, row in enumerate(latest_exposures.itertuples(index=False), start=1):
        expected_amount = round(row.outstanding_amount * rng.uniform(0.08, 0.22), 2)
        shortfall_factor = rng.uniform(0.72, 1.03) if row.days_past_due > 30 else rng.uniform(0.92, 1.04)
        payment_amount = round(min(expected_amount * shortfall_factor, expected_amount), 2)
        payment_date = pd.to_datetime(row.reporting_month) + pd.to_timedelta(int(rng.integers(18, 58)), unit="D")
        rows.append(
            {
                "payment_id": f"PAY{payment_number:08d}",
                "customer_id": row.customer_id,
                "payment_date": payment_date.date().isoformat(),
                "payment_amount": payment_amount,
                "expected_payment_amount": expected_amount,
                "days_late": int(max(0, row.days_past_due + rng.normal(0, 7))),
            }
        )
    return pd.DataFrame(rows)


def create_scenarios() -> pd.DataFrame:
    """Create analytical stress testing scenarios for a synthetic portfolio."""
    return pd.DataFrame(
        [
            {
                "scenario_id": "S1",
                "scenario_name": "Baseline",
                "pd_shock": 1.00,
                "lgd_shock": 1.00,
                "exposure_shock": 1.00,
                "description": "Current portfolio conditions without additional stress.",
            },
            {
                "scenario_id": "S2",
                "scenario_name": "Mild Downturn",
                "pd_shock": 1.25,
                "lgd_shock": 1.10,
                "exposure_shock": 1.03,
                "description": "Moderate deterioration in payment behavior and recoveries.",
            },
            {
                "scenario_id": "S3",
                "scenario_name": "Sector Stress",
                "pd_shock": 1.55,
                "lgd_shock": 1.18,
                "exposure_shock": 1.06,
                "description": "Targeted stress affecting cyclical industries and weak ratings.",
            },
            {
                "scenario_id": "S4",
                "scenario_name": "Severe Downturn",
                "pd_shock": 2.10,
                "lgd_shock": 1.35,
                "exposure_shock": 1.10,
                "description": "Broad macroeconomic stress with higher default and loss proxies.",
            },
        ]
    )


def main() -> None:
    ensure_directories()
    rng = np.random.default_rng(RANDOM_SEED)

    customers = create_customers(rng)
    ratings = create_ratings(customers, rng)
    exposures = create_exposures(customers, ratings, rng)
    defaults = create_default_events(exposures, ratings, rng)
    payments = create_payments(exposures, rng)
    scenarios = create_scenarios()

    customers.to_csv(RAW_DIR / "customers.csv", index=False)
    exposures.to_csv(RAW_DIR / "credit_exposures.csv", index=False)
    ratings.to_csv(RAW_DIR / "risk_ratings.csv", index=False)
    defaults.to_csv(RAW_DIR / "default_events.csv", index=False)
    payments.to_csv(RAW_DIR / "payments.csv", index=False)
    scenarios.to_csv(RAW_DIR / "macroeconomic_scenarios.csv", index=False)
    scenarios.to_csv(REFERENCE_DIR / "macroeconomic_scenarios.csv", index=False)

    print(f"Synthetic credit portfolio data generated in {RAW_DIR}")


if __name__ == "__main__":
    main()
