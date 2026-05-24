import os


def test_sample_customer_exists():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "sample", "sample_customers.csv")
    assert os.path.exists(path)
