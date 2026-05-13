import pandas as pd
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[1]
RAW_PATH = BASE_PATH / 'data' / 'raw'
PROCESSED_PATH = BASE_PATH / 'data' / 'processed'


def clean_csv(name):
    df = pd.read_csv(RAW_PATH / f'{name}.csv')
    if name == 'dim_customer':
        df['credit_limit'] = df['credit_limit'].astype(float)
    elif name in ['fact_exposure_snapshot', 'fact_invoice', 'fact_payment', 'fact_default_event']:
        for col in df.columns:
            if 'amount' in col or 'limit' in col or 'open_invoices' in col:
                df[col] = df[col].astype(float)
    return df


def main():
    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
    tables = [
        'dim_country', 'dim_industry', 'dim_risk_rating',
        'dim_customer', 'dim_date', 'fact_exposure_snapshot',
        'fact_invoice', 'fact_payment', 'fact_default_event'
    ]
    for table in tables:
        df = clean_csv(table)
        df.to_csv(PROCESSED_PATH / f'{table}.csv', index=False)

    print('Processed files saved to', PROCESSED_PATH)

if __name__ == '__main__':
    main()
