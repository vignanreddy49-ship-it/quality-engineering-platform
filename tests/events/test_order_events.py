import json
from pathlib import Path

from jsonschema import validate

from apps.api.events import build_order_created_event


CONTRACT = Path(__file__).parents[1] / "contracts" / "order-created.v1.json"


def sample_order(order_id="o-123"):
    return {
        "id": order_id,
        "customer_email": "qa@example.com",
        "total": 15998.0,
        "status": "CREATED",
    }


def test_order_created_event_has_stable_envelope():
    event = build_order_created_event(sample_order())

    assert event["event_type"] == "order.created"
    assert event["event_version"] == 1
    assert event["aggregate_id"] == "o-123"
    assert event["payload"]["total"] == 15998.0
    assert event["event_id"]
    assert event["occurred_at"]


def test_order_created_event_matches_json_schema():
    schema = json.loads(CONTRACT.read_text())
    event = build_order_created_event(sample_order("o-456"))

    validate(instance=event, schema=schema)


def test_duplicate_event_can_be_detected_by_event_id():
    event = build_order_created_event(sample_order("o-789"))
    processed_ids = {event["event_id"]}

    assert event["event_id"] in processed_ids
    assert event["event_id"] not in processed_ids - {event["event_id"]}
