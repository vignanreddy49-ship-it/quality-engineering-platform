"""API-level checks for request and event correlation propagation."""

from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_request_id_is_echoed_and_propagated_to_event_headers():
    request_id = "corr-qa-123"
    response = client.post(
        "/api/orders",
        headers={"X-Request-ID": request_id},
        json={
            "customer_email": "trace@example.com",
            "items": [{"product_id": "p-100", "quantity": 1}],
        },
    )

    assert response.status_code == 201
    assert response.headers["X-Request-ID"] == request_id

    event_headers = client.get("/api/event-headers").json()
    assert event_headers[-1]["x-correlation-id"] == request_id
    assert event_headers[-1]["traceparent"].startswith("00-")
