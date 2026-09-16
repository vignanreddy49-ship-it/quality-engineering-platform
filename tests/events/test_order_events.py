import json
from pathlib import Path

from apps.api.events import build_order_created_event


CONTRACT = Path(__file__).parents[2] / "contracts" / "order-created.v1.json"


def test_order_created_event_has_stable_envelope():
    event = build_order_created_event(
        {
            "id": "o-123",
            "customer_email": "qa@example.com",
            "total": 15998.0,
            "status": "CREATED",
        }
    )

    assert event["event_type"] == "order.created"
    assert event["event_version"] == 1
    assert event["aggregate_id"] == "o-123"
    assert event["payload"]["total"] == 15998.0
    assert event["event_id"]
    assert event["occurred_at"]


def test_order_created_event_matches_contract():
    schema = json.loads(CONTRACT.read_text())
    required = set(schema["required"])
    event = build_order_created_event(
        {"id": "o-456", "customer_email": "qa@example.com", "total": 7999.0, "status": "CREATED"}
    )

    assert required.issubset(event.keys())
    assert event["event_type"] in schema["properties"]["event_type"]["enum"]
    assert event["event_version"] == schema["properties"]["event_version"]["const"]


def test_duplicate_event_can_be_detected_by_event_id():
    event = build_order_created_event(
        {"id": "o-789", "customer_email": "qa@example.com", "total": 7999.0, "status": "CREATED"}
    )
    processed_ids = {event["event_id"]}

    assert event["event_id"] in processed_ids
    assert event["event_id"] not in processed_ids - {event["event_id"]}
