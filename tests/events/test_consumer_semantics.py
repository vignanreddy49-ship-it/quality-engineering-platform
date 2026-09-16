from apps.api.events import build_order_created_event
from tests.events.consumer import IdempotentEventConsumer


def test_duplicate_event_is_not_processed_twice():
    received = []
    consumer = IdempotentEventConsumer(received.append)
    event = build_order_created_event(
        {"id": "o-100", "customer_email": "qa@example.com", "total": 7999.0, "status": "CREATED"}
    )

    assert consumer.process(event) is True
    assert consumer.process(event) is False
    assert received == [event]


def test_distinct_events_are_processed_independently():
    received = []
    consumer = IdempotentEventConsumer(received.append)

    first = build_order_created_event(
        {"id": "o-101", "customer_email": "qa@example.com", "total": 7999.0, "status": "CREATED"}
    )
    second = build_order_created_event(
        {"id": "o-102", "customer_email": "qa@example.com", "total": 6499.0, "status": "CREATED"}
    )

    assert consumer.process(first) is True
    assert consumer.process(second) is True
    assert [event["aggregate_id"] for event in received] == ["o-101", "o-102"]
