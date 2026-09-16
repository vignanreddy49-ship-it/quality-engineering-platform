import os
import httpx

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def test_health():
    response = httpx.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "UP"


def test_products_have_required_contract():
    response = httpx.get(f"{BASE_URL}/api/products")
    assert response.status_code == 200
    products = response.json()
    assert len(products) >= 3
    for product in products:
        assert {"id", "name", "price", "stock"} <= product.keys()
        assert product["price"] > 0
        assert product["stock"] >= 0


def test_get_unknown_product_returns_404():
    response = httpx.get(f"{BASE_URL}/api/products/does-not-exist")
    assert response.status_code == 404


def test_create_order_calculates_total():
    payload = {
        "customer_email": "qa@example.com",
        "items": [{"product_id": "p-100", "quantity": 2}],
    }
    response = httpx.post(f"{BASE_URL}/api/orders", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "CREATED"
    assert body["total"] == 15998.0


def test_order_rejects_unknown_product():
    payload = {
        "customer_email": "qa@example.com",
        "items": [{"product_id": "invalid", "quantity": 1}],
    }
    response = httpx.post(f"{BASE_URL}/api/orders", json=payload)
    assert response.status_code == 400


def test_order_rejects_excessive_quantity():
    payload = {
        "customer_email": "qa@example.com",
        "items": [{"product_id": "p-100", "quantity": 21}],
    }
    response = httpx.post(f"{BASE_URL}/api/orders", json=payload)
    assert response.status_code == 422
