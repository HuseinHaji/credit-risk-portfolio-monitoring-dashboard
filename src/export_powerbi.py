import pandas as pd
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[1]
PROCESSED_PATH = BASE_PATH / 'data' / 'processed'
POWERBI_PATH = BASE_PATH / 'data' / 'powerbi'


def main():
    POWERBI_PATH.mkdir(parents=True, exist_ok=True)
    exposures = pd.read_csv(PROCESSED_PATH / 'fact_exposure_snapshot.csv')
    customers = pd.read_csv(PROCESSED_PATH / 'dim_customer.csv')
    countries = pd.read_csv(PROCESSED_PATH / 'dim_country.csv')
    industries = pd.read_csv(PROCESSED_PATH / 'dim_industry.csv')
    ratings = pd.read_csv(PROCESSED_PATH / 'dim_risk_rating.csv')
    date = pd.read_csv(PROCESSED_PATH / 'dim_date.csv')

    customers = customers.merge(countries, on='country_id', how='left')
    customers = customers.merge(industries, on='industry_id', how='left')
    customers = customers.merge(ratings, on='rating_code', how='left')
    exposures = exposures.merge(customers, on='customer_id', how='left')
    exposures = exposures.merge(date, on='month_key', how='left')

    exposure_by_country = exposures.groupby('country_name', as_index=False)['exposure_amount'].sum().rename(columns={'exposure_amount': 'total_exposure'})
    exposure_by_industry = exposures.groupby('industry_name', as_index=False)['exposure_amount'].sum().rename(columns={'exposure_amount': 'total_exposure'})
    exposure_by_rating = exposures.groupby('rating_label', as_index=False)['exposure_amount'].sum().rename(columns={'exposure_amount': 'total_exposure'})
    monthly_trend = (
        exposures.groupby(['month_key', 'month_label'], as_index=False)
        .agg({'exposure_amount': 'sum', 'overdue_amount': 'sum'})
        .sort_values('month_key')
    )
    top_customers = exposures.groupby(['customer_id', 'customer_name'], as_index=False)['exposure_amount'].sum().sort_values('exposure_amount', ascending=False).head(20)

    rating_migration = exposures.sort_values(['customer_id', 'month_key']).groupby('customer_id').agg(
        first_rating=('rating_label', 'first'),
        last_rating=('rating_label', 'last'),
        exposure_change=('exposure_amount', 'last')
    ).reset_index()

    exposure_by_country.to_csv(POWERBI_PATH / 'exposure_by_country.csv', index=False)
    exposure_by_industry.to_csv(POWERBI_PATH / 'exposure_by_industry.csv', index=False)
    exposure_by_rating.to_csv(POWERBI_PATH / 'exposure_by_rating.csv', index=False)
    monthly_trend.to_csv(POWERBI_PATH / 'monthly_trend.csv', index=False)
    top_customers.to_csv(POWERBI_PATH / 'top_customers_by_exposure.csv', index=False)
    rating_migration.to_csv(POWERBI_PATH / 'rating_migration_summary.csv', index=False)

    print('Power BI-ready files saved to', POWERBI_PATH)

if __name__ == '__main__':
    main()
