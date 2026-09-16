"""Service-virtualization checks against a disposable WireMock container."""
import requests
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs


def test_payment_authorization_and_decline_scenarios():
    container = (
        DockerContainer("wiremock/wiremock:3.9.2")
        .with_volume_mapping(
            "tests/service-virtualization/wiremock",
            "/home/wiremock",
            mode="ro",
        )
        .with_exposed_ports(8080)
    )
    with container:
        wait_for_logs(container, "port: 8080", timeout=60)
        port = container.get_exposed_port(8080)
        base_url = f"http://localhost:{port}"

        approved = requests.post(
            f"{base_url}/payments/authorize",
            json={"order_id": "o-abc123", "amount": 7999.0},
            timeout=5,
        )
        assert approved.status_code == 200
        assert approved.json()["status"] == "AUTHORIZED"

        declined = requests.post(
            f"{base_url}/payments/authorize",
            json={"order_id": "o-expensive", "amount": 100000.0},
            timeout=5,
        )
        assert declined.status_code == 402
        assert declined.json()["code"] == "PAYMENT_DECLINED"
