"""Observability contract checks for the ShopSphere metrics surface."""
from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_metrics_is_prometheus_compatible_and_contains_request_counter():
    client.get("/health")
    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert "# TYPE shopsphere_http_requests_total counter" in response.text
    assert "shopsphere_http_requests_total{" in response.text


def test_metrics_contains_duration_metric():
    client.get("/api/products")
    response = client.get("/metrics")

    assert "# TYPE shopsphere_http_request_duration_seconds_total counter" in response.text
    assert "shopsphere_http_request_duration_seconds_total{" in response.text
