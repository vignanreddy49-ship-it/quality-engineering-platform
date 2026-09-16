import re
from datetime import datetime

from apps.api.events import build_order_created_event


def sample_order():
    return {
        "id": "o-a1b2c3",
        "customer_email": "qa@example.com",
        "total": 7999.0,
        "status": "CREATED",
    }


def test_event_timestamp_is_iso_8601():
    event = build_order_created_event(sample_order())
    datetime.fromisoformat(event["occurred_at"].replace("Z", "+00:00"))


def test_aggregate_id_is_safe_for_topic_partitioning():
    event = build_order_created_event(sample_order())
    assert re.fullmatch(r"o-[a-z0-9]+", event["aggregate_id"])


def test_event_payload_references_same_aggregate():
    event = build_order_created_event(sample_order())
    assert event["payload"]["order_id"] == event["aggregate_id"]


def test_each_new_event_gets_unique_event_id():
    first = build_order_created_event(sample_order())
    second = build_order_created_event(sample_order())
    assert first["event_id"] != second["event_id"]
