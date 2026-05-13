import numpy as np
import pandas as pd
from pathlib import Path

RANDOM_SEED = 42
RAW_PATH = Path(__file__).resolve().parents[1] / 'data' / 'raw'

COUNTRIES = [
    {'country_id': 1, 'country_name': 'Germany', 'region': 'Europe'},
    {'country_id': 2, 'country_name': 'France', 'region': 'Europe'},
    {'country_id': 3, 'country_name': 'Netherlands', 'region': 'Europe'},
    {'country_id': 4, 'country_name': 'Austria', 'region': 'Europe'},
    {'country_id': 5, 'country_name': 'Sweden', 'region': 'Europe'},
    {'country_id': 6, 'country_name': 'Italy', 'region': 'Europe'},
    {'country_id': 7, 'country_name': 'Poland', 'region': 'Europe'},
    {'country_id': 8, 'country_name': 'Spain', 'region': 'Europe'},
]

INDUSTRIES = [
    'Manufacturing', 'Wholesale', 'Logistics', 'Energy', 'Construction',
    'Technology', 'Chemicals', 'Pharma', 'Food & Beverage', 'Utilities'
]

RISK_RATINGS = [
    {'rating_code': 'AAA', 'rating_label': 'Low Risk', 'risk_weight': 1},
    {'rating_code': 'AA', 'rating_label': 'Good', 'risk_weight': 2},
    {'rating_code': 'A', 'rating_label': 'Medium', 'risk_weight': 3},
    {'rating_code': 'BBB', 'rating_label': 'Watchlist', 'risk_weight': 5},
    {'rating_code': 'BB', 'rating_label': 'High Risk', 'risk_weight': 8},
]

CUSTOMER_COUNT = 40
MONTH_COUNT = 24


def create_customers(rng):
    customers = []
    for i in range(1, CUSTOMER_COUNT + 1):
        country = rng.choice(COUNTRIES)
        industry = rng.choice(INDUSTRIES)
        rating = rng.choice(RISK_RATINGS, p=[0.15, 0.25, 0.30, 0.20, 0.10])
        credit_limit = rng.integers(400000, 2200000)
        customers.append({
            'customer_id': f'CUST{i:03d}',
            'customer_name': f'Industrial Partner {i:02d}',
            'country_id': country['country_id'],
            'industry_name': industry,
            'rating_code': rating['rating_code'],
            'credit_limit': float(credit_limit),
        })
    return pd.DataFrame(customers)


def make_lookup(df, key, value):
    return df.drop_duplicates(subset=[key])[[key, value]]


def generate_date_table():
    months = pd.date_range('2023-01-01', periods=MONTH_COUNT, freq='MS')
    return pd.DataFrame({
        'month_key': months.strftime('%Y-%m'),
        'month_start': months,
        'month_label': months.strftime('%b %Y'),
    })


def generate_exposure_snapshots(customers, dates, rng):
    rows = []
    for _, cust in customers.iterrows():
        base_util = rng.uniform(0.28, 0.75)
        util_trend = rng.normal(0, 0.03, len(dates))
        for idx, month in dates.iterrows():
            exposure = max(0.0, (base_util + util_trend[idx]) * cust['credit_limit'])
            exposure = round(exposure, 2)
            overdue_rate = 0.03 + (0.01 if cust['rating_code'] in ['BB', 'BBB'] else 0.0)
            overdue_amt = round(exposure * rng.uniform(overdue_rate, overdue_rate + 0.05), 2)
            default_flag = False
            if cust['rating_code'] == 'BB' and rng.random() < 0.06:
                default_flag = True
            if cust['rating_code'] == 'BBB' and rng.random() < 0.03:
                default_flag = True
            open_invoices = int(rng.integers(1, 8))
            rows.append({
                'customer_id': cust['customer_id'],
                'month_key': month['month_key'],
                'exposure_amount': exposure,
                'overdue_amount': overdue_amt,
                'default_flag': default_flag,
                'open_invoices': open_invoices,
            })
    return pd.DataFrame(rows)


def generate_invoices(customers, rng):
    invoices = []
    for i, cust in customers.iterrows():
        for invoice_index in range(10):
            issue_date = rng.choice(pd.date_range('2023-01-01', '2024-12-01', freq='MS'))
            invoice_date = pd.to_datetime(issue_date).date()
            amount = round(rng.uniform(15000, 120000), 2)
            due_date = pd.to_datetime(issue_date) + pd.Timedelta(days=30)
            overdue_flag = rng.random() < 0.18
            invoices.append({
                'invoice_id': f'INV{(i*10+invoice_index+1):05d}',
                'customer_id': cust['customer_id'],
                'invoice_date': invoice_date,
                'due_date': due_date.date(),
                'invoice_amount': amount,
                'overdue_flag': overdue_flag,
            })
    return pd.DataFrame(invoices)


def generate_payments(invoices, rng):
    payments = []
    for _, invoice in invoices.iterrows():
        if rng.random() < 0.90:
            payment_date = pd.to_datetime(invoice['invoice_date']) + pd.Timedelta(days=rng.integers(10, 70))
            amount = invoice['invoice_amount'] * rng.uniform(0.85, 1.00)
            payments.append({
                'payment_id': f'PMT{len(payments)+1:06d}',
                'invoice_id': invoice['invoice_id'],
                'payment_date': payment_date.date(),
                'payment_amount': round(amount, 2),
            })
    return pd.DataFrame(payments)


def generate_default_events(exposures, rng):
    defaults = []
    default_customers = exposures[exposures['default_flag']].customer_id.unique()
    for customer_id in default_customers:
        sample = exposures[exposures['customer_id'] == customer_id].sample(1, random_state=rng)
        default_date = pd.to_datetime(sample['month_key'].iloc[0] + '-01') + pd.Timedelta(days=15)
        default_amount = float(sample['exposure_amount'].iloc[0] * rng.uniform(0.4, 0.9))
        recovery_amount = round(default_amount * rng.uniform(0.15, 0.45), 2)
        defaults.append({
            'customer_id': customer_id,
            'default_date': default_date.date(),
            'default_amount': round(default_amount, 2),
            'recovery_amount': recovery_amount,
        })
    return pd.DataFrame(defaults)


def main():
    rng = np.random.default_rng(RANDOM_SEED)
    RAW_PATH.mkdir(parents=True, exist_ok=True)

    dim_country = pd.DataFrame(COUNTRIES)
    dim_industry = pd.DataFrame({'industry_id': list(range(1, len(INDUSTRIES)+1)), 'industry_name': INDUSTRIES})
    dim_risk_rating = pd.DataFrame(RISK_RATINGS)
    customers = create_customers(rng)
    customers = customers.merge(dim_industry, on='industry_name', how='left')
    customers = customers[['customer_id', 'customer_name', 'country_id', 'industry_id', 'rating_code', 'credit_limit']]

    dim_date = generate_date_table()
    exposures = generate_exposure_snapshots(customers, dim_date, rng)
    invoices = generate_invoices(customers, rng)
    payments = generate_payments(invoices, rng)
    defaults = generate_default_events(exposures, rng)

    dim_country.to_csv(RAW_PATH / 'dim_country.csv', index=False)
    dim_industry.to_csv(RAW_PATH / 'dim_industry.csv', index=False)
    dim_risk_rating.to_csv(RAW_PATH / 'dim_risk_rating.csv', index=False)
    customers.to_csv(RAW_PATH / 'dim_customer.csv', index=False)
    dim_date.to_csv(RAW_PATH / 'dim_date.csv', index=False)
    exposures.to_csv(RAW_PATH / 'fact_exposure_snapshot.csv', index=False)
    invoices.to_csv(RAW_PATH / 'fact_invoice.csv', index=False)
    payments.to_csv(RAW_PATH / 'fact_payment.csv', index=False)
    defaults.to_csv(RAW_PATH / 'fact_default_event.csv', index=False)

    print('Credit risk raw data generated to', RAW_PATH)

if __name__ == '__main__':
    main()
