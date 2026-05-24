"""Validation tests for raw data and audit output."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
AUDIT = ROOT / "output" / "audit"


def test_synthetic_raw_files_are_created():
    for name in [
        "customers.csv",
        "credit_exposures.csv",
        "risk_ratings.csv",
        "default_events.csv",
        "payments.csv",
        "macroeconomic_scenarios.csv",
    ]:
        assert (RAW / name).exists()


def test_no_duplicate_raw_keys():
    customers = pd.read_csv(RAW / "customers.csv")
    exposures = pd.read_csv(RAW / "credit_exposures.csv")
    assert customers["customer_id"].is_unique
    assert exposures["exposure_id"].is_unique


def test_data_quality_report_is_not_empty_and_has_no_failed_critical_checks():
    report = pd.read_csv(AUDIT / "data_quality_report.csv")
    assert not report.empty
    failed_critical = report[(report["status"] == "Fail") & (report["severity"] == "Critical")]
    assert failed_critical.empty
