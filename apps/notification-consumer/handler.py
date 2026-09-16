"""Pure consumer logic, intentionally independent from Kafka for fast unit tests."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Notification:
    event_id: str
    customer_email: str
    order_id: str
    total: float


class EventStore(Protocol):
    def seen(self, event_id: str) -> bool: ...
    def mark_seen(self, event_id: str) -> None: ...


class NotificationSink(Protocol):
    def send(self, notification: Notification) -> None: ...


class DeadLetterSink(Protocol):
    def send(self, event: dict, reason: str) -> None: ...


class InMemoryEventStore:
    def __init__(self) -> None:
        self.ids: set[str] = set()

    def seen(self, event_id: str) -> bool:
        return event_id in self.ids

    def mark_seen(self, event_id: str) -> None:
        self.ids.add(event_id)


class RecordingNotificationSink:
    def __init__(self, failures: int = 0) -> None:
        self.notifications: list[Notification] = []
        self.failures = failures

    def send(self, notification: Notification) -> None:
        if self.failures > 0:
            self.failures -= 1
            raise RuntimeError("transient notification failure")
        self.notifications.append(notification)


class RecordingDeadLetterSink:
    def __init__(self) -> None:
        self.messages: list[tuple[dict, str]] = []

    def send(self, event: dict, reason: str) -> None:
        self.messages.append((event, reason))


def validate_event(event: dict) -> None:
    if event.get("event_type") != "order.created":
        raise ValueError("unsupported event type")
    if event.get("event_version") != 1:
        raise ValueError("unsupported event version")
    if not event.get("event_id"):
        raise ValueError("missing event id")
    payload = event.get("payload") or {}
    required = ("order_id", "customer_email", "total")
    if any(field not in payload for field in required):
        raise ValueError("invalid order payload")


def handle_event(
    event: dict,
    event_store: EventStore,
    notification_sink: NotificationSink,
    dead_letter_sink: DeadLetterSink,
    max_retries: int = 2,
) -> str:
    """Process once, retry transient sink failures, and route permanent failures to DLQ."""
    try:
        validate_event(event)
    except ValueError as exc:
        dead_letter_sink.send(event, str(exc))
        return "dead_lettered"

    event_id = event["event_id"]
    if event_store.seen(event_id):
        return "duplicate"

    payload = event["payload"]
    notification = Notification(
        event_id=event_id,
        customer_email=payload["customer_email"],
        order_id=payload["order_id"],
        total=float(payload["total"]),
    )

    for attempt in range(max_retries + 1):
        try:
            notification_sink.send(notification)
            event_store.mark_seen(event_id)
            return "processed"
        except Exception as exc:  # noqa: BLE001 - consumer boundary must classify failures
            if attempt == max_retries:
                dead_letter_sink.send(event, f"notification failed after {max_retries + 1} attempts: {exc}")
                return "dead_lettered"

    raise AssertionError("unreachable")
