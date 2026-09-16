from apps.notification_consumer.handler import (
    InMemoryEventStore,
    RecordingDeadLetterSink,
    RecordingNotificationSink,
    handle_event,
)


def event(event_id="evt-1"):
    return {
        "event_id": event_id,
        "event_type": "order.created",
        "event_version": 1,
        "occurred_at": "2026-09-16T09:00:00+00:00",
        "aggregate_id": "o-123",
        "payload": {"order_id": "o-123", "customer_email": "qa@example.com", "total": 100.0, "status": "CREATED"},
    }


def test_valid_event_sends_one_notification():
    store, sink, dlq = InMemoryEventStore(), RecordingNotificationSink(), RecordingDeadLetterSink()
    assert handle_event(event(), store, sink, dlq) == "processed"
    assert len(sink.notifications) == 1
    assert not dlq.messages


def test_duplicate_event_is_ignored():
    store, sink, dlq = InMemoryEventStore(), RecordingNotificationSink(), RecordingDeadLetterSink()
    assert handle_event(event(), store, sink, dlq) == "processed"
    assert handle_event(event(), store, sink, dlq) == "duplicate"
    assert len(sink.notifications) == 1


def test_transient_failure_is_retried_with_bound():
    store, sink, dlq = InMemoryEventStore(), RecordingNotificationSink(failures=2), RecordingDeadLetterSink()
    assert handle_event(event(), store, sink, dlq, max_retries=2) == "processed"
    assert len(sink.notifications) == 1


def test_permanent_failure_goes_to_dlq():
    store, sink, dlq = InMemoryEventStore(), RecordingNotificationSink(failures=10), RecordingDeadLetterSink()
    assert handle_event(event(), store, sink, dlq, max_retries=2) == "dead_lettered"
    assert len(sink.notifications) == 0
    assert "3 attempts" in dlq.messages[0][1]


def test_unsupported_schema_version_goes_to_dlq():
    bad = event()
    bad["event_version"] = 2
    store, sink, dlq = InMemoryEventStore(), RecordingNotificationSink(), RecordingDeadLetterSink()
    assert handle_event(bad, store, sink, dlq) == "dead_lettered"
    assert "unsupported event version" in dlq.messages[0][1]


def test_missing_payload_goes_to_dlq():
    bad = event()
    bad["payload"] = {}
    store, sink, dlq = InMemoryEventStore(), RecordingNotificationSink(), RecordingDeadLetterSink()
    assert handle_event(bad, store, sink, dlq) == "dead_lettered"
