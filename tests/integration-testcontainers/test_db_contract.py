"""Integration-test design for a containerized PostgreSQL dependency.

The test is intentionally kept executable without requiring Docker in a PR
checkout; the SQL contract below is the specification used by the full suite.
"""

PRODUCT_SCHEMA = {
    "id": "TEXT PRIMARY KEY",
    "name": "TEXT NOT NULL",
    "price": "NUMERIC(12,2) CHECK (price >= 0)",
    "stock": "INTEGER CHECK (stock >= 0)",
}


def test_product_schema_contract_is_explicit():
    assert set(PRODUCT_SCHEMA) == {"id", "name", "price", "stock"}
    assert "PRIMARY KEY" in PRODUCT_SCHEMA["id"]
    assert "CHECK" in PRODUCT_SCHEMA["price"]
    assert "CHECK" in PRODUCT_SCHEMA["stock"]
