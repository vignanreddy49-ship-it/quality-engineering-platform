"""Fast security regression checks that run without external scanners."""
from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_unknown_product_does_not_expose_internal_details():
    response = client.get("/api/products/does-not-exist")
    assert response.status_code == 404
    body = response.text.lower()
    assert "traceback" not in body
    assert "password" not in body
    assert "secret" not in body


def test_order_validation_rejects_excessive_quantity():
    response = client.post(
        "/api/orders",
        json={
            "customer_email": "security@example.com",
            "items": [{"product_id": "p-100", "quantity": 21}],
        },
    )
    assert response.status_code == 422


def test_metrics_endpoint_does_not_expose_request_headers():
    response = client.get("/metrics", headers={"Authorization": "Bearer test-only-token"})
    assert response.status_code == 200
    assert "test-only-token" not in response.text
    assert "authorization" not in response.text.lower()
