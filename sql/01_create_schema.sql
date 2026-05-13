-- Create schema for credit risk monitoring data model

CREATE TABLE dim_country (
    country_id SERIAL PRIMARY KEY,
    country_name TEXT NOT NULL,
    region TEXT NOT NULL
);

CREATE TABLE dim_industry (
    industry_id SERIAL PRIMARY KEY,
    industry_name TEXT NOT NULL
);

CREATE TABLE dim_risk_rating (
    rating_code TEXT PRIMARY KEY,
    rating_label TEXT NOT NULL,
    risk_weight INTEGER NOT NULL
);

CREATE TABLE dim_customer (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    country_id INTEGER NOT NULL REFERENCES dim_country(country_id),
    industry_id INTEGER NOT NULL REFERENCES dim_industry(industry_id),
    rating_code TEXT NOT NULL REFERENCES dim_risk_rating(rating_code),
    credit_limit NUMERIC(12,2) NOT NULL
);

CREATE TABLE dim_date (
    month_key TEXT PRIMARY KEY,
    month_start DATE NOT NULL,
    month_label TEXT NOT NULL
);

CREATE TABLE fact_exposure_snapshot (
    snapshot_id SERIAL PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES dim_customer(customer_id),
    month_key TEXT NOT NULL REFERENCES dim_date(month_key),
    exposure_amount NUMERIC(12,2) NOT NULL,
    overdue_amount NUMERIC(12,2) NOT NULL,
    default_flag BOOLEAN NOT NULL,
    open_invoices INTEGER NOT NULL
);

CREATE TABLE fact_invoice (
    invoice_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES dim_customer(customer_id),
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    invoice_amount NUMERIC(12,2) NOT NULL,
    overdue_flag BOOLEAN NOT NULL
);

CREATE TABLE fact_payment (
    payment_id TEXT PRIMARY KEY,
    invoice_id TEXT NOT NULL REFERENCES fact_invoice(invoice_id),
    payment_date DATE NOT NULL,
    payment_amount NUMERIC(12,2) NOT NULL
);

CREATE TABLE fact_default_event (
    default_id SERIAL PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES dim_customer(customer_id),
    default_date DATE NOT NULL,
    default_amount NUMERIC(12,2) NOT NULL,
    recovery_amount NUMERIC(12,2) NOT NULL
);
