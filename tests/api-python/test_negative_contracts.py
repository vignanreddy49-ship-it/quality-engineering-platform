import requests

BASE_URL = "http://127.0.0.1:8000"


def test_unknown_product_returns_404():
    response = requests.get(f"{BASE_URL}/api/products/does-not-exist")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_unknown_order_returns_404():
    response = requests.get(f"{BASE_URL}/api/orders/o-missing")
    assert response.status_code == 404


def test_insufficient_stock_is_rejected():
    response = requests.post(
        f"{BASE_URL}/api/orders",
        json={
            "customer_email": "qa@example.com",
            "items": [{"product_id": "p-100", "quantity": 26}],
        },
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Insufficient stock"


def test_order_total_is_deterministic():
    response = requests.post(
        f"{BASE_URL}/api/orders",
        json={
            "customer_email": "qa@example.com",
            "items": [
                {"product_id": "p-100", "quantity": 2},
                {"product_id": "p-101", "quantity": 1},
            ],
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["total"] == 22497.0
    assert body["status"] == "CREATED"
