"""Central configuration for the credit risk analytics pipeline."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REFERENCE_DIR = DATA_DIR / "reference"

OUTPUT_DIR = ROOT_DIR / "output"
REPORTS_DIR = OUTPUT_DIR / "reports"
POWERBI_DIR = OUTPUT_DIR / "powerbi"
AUDIT_DIR = OUTPUT_DIR / "audit"
WATCHLIST_DIR = OUTPUT_DIR / "watchlist"
STRESS_TEST_DIR = OUTPUT_DIR / "stress_tests"
SCREENSHOTS_DIR = ROOT_DIR / "screenshots"

RANDOM_SEED = 42

VALID_RISK_RATINGS = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC"]
RISK_SCORE_MAP = {
    "AAA": 1,
    "AA": 2,
    "A": 3,
    "BBB": 5,
    "BB": 7,
    "B": 9,
    "CCC": 10,
}
RISK_CATEGORY_MAP = {
    "AAA": "Low Risk",
    "AA": "Low Risk",
    "A": "Moderate Risk",
    "BBB": "Elevated Risk",
    "BB": "High Risk",
    "B": "Critical Watchlist",
    "CCC": "Critical Watchlist",
}

ALL_DIRECTORIES = [
    RAW_DIR,
    PROCESSED_DIR,
    REFERENCE_DIR,
    REPORTS_DIR,
    POWERBI_DIR,
    AUDIT_DIR,
    WATCHLIST_DIR,
    STRESS_TEST_DIR,
    SCREENSHOTS_DIR,
]


def ensure_directories() -> None:
    """Create the project data and output directories."""
    for directory in ALL_DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)
