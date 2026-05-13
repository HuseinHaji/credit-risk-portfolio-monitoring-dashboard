-- Load CSV files into PostgreSQL tables

\COPY dim_country FROM 'data/processed/dim_country.csv' CSV HEADER;
\COPY dim_industry FROM 'data/processed/dim_industry.csv' CSV HEADER;
\COPY dim_risk_rating FROM 'data/processed/dim_risk_rating.csv' CSV HEADER;
\COPY dim_customer FROM 'data/processed/dim_customer.csv' CSV HEADER;
\COPY dim_date FROM 'data/processed/dim_date.csv' CSV HEADER;
\COPY fact_exposure_snapshot FROM 'data/processed/fact_exposure_snapshot.csv' CSV HEADER;
\COPY fact_invoice FROM 'data/processed/fact_invoice.csv' CSV HEADER;
\COPY fact_payment FROM 'data/processed/fact_payment.csv' CSV HEADER;
\COPY fact_default_event FROM 'data/processed/fact_default_event.csv' CSV HEADER;
