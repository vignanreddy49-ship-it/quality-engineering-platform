"""Event publisher abstractions for local and Kafka-backed execution."""

import json
import os
from typing import Protocol

from apps.api.observability import inject_trace_headers


class EventPublisher(Protocol):
    def publish(self, event: dict, headers: dict[str, str] | None = None) -> None: ...


class InMemoryEventPublisher:
    def __init__(self) -> None:
        self.events: list[dict] = []
        self.headers: list[dict[str, str]] = []

    def publish(self, event: dict, headers: dict[str, str] | None = None) -> None:
        self.events.append(event)
        self.headers.append(dict(headers or {}))


class KafkaEventPublisher:
    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self._producer = None

    def _get_producer(self):
        if self._producer is None:
            from confluent_kafka import Producer
            self._producer = Producer({"bootstrap.servers": self.bootstrap_servers})
        return self._producer

    def publish(self, event: dict, headers: dict[str, str] | None = None) -> None:
        producer = self._get_producer()
        propagated = inject_trace_headers(headers)
        kafka_headers = [(key, value.encode("utf-8")) for key, value in propagated.items()]
        producer.produce(
            self.topic,
            key=event["aggregate_id"],
            value=json.dumps(event),
            headers=kafka_headers,
        )
        producer.flush(5)


def create_event_publisher() -> EventPublisher:
    mode = os.getenv("EVENT_PUBLISHER", "memory").lower()
    if mode == "kafka":
        return KafkaEventPublisher(
            os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            os.getenv("KAFKA_ORDER_TOPIC", "orders"),
        )
    return InMemoryEventPublisher()
