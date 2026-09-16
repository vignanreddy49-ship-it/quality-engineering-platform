"""Consumer contract for the ShopSphere product API."""
import atexit
import json
from pathlib import Path

import requests
from pact import Consumer, Provider

PACT_DIR = Path(__file__).parent / "pacts"
pact = Consumer("web-store").has_pact_with(
    Provider("shopsphere-api"),
    port=9222,
    pact_dir=str(PACT_DIR),
)
pact.start_service()
atexit.register(pact.stop_service)


def test_get_product_contract():
    expected = {
        "id": "p-100",
        "name": "Wireless Headphones",
        "price": 7999.0,
        "stock": 25,
    }
    (
        pact.given("product p-100 exists")
        .upon_receiving("a request for product p-100")
        .with_request("GET", "/api/products/p-100")
        .will_respond_with(200, body=expected)
    )

    with pact:
        response = requests.get(f"{pact.uri}/api/products/p-100", timeout=5)

    assert response.status_code == 200
    assert response.json() == expected


def test_generated_pact_has_explicit_consumer_provider():
    """Keep the contract artifact understandable during portfolio review."""
    test_get_product_contract()
    pact_file = PACT_DIR / "web-store-shopsphere-api.json"
    document = json.loads(pact_file.read_text())
    assert document["consumer"]["name"] == "web-store"
    assert document["provider"]["name"] == "shopsphere-api"
