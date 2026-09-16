"""Event publisher abstractions for local and Kafka-backed execution."""

import json
import os
from typing import Protocol


class EventPublisher(Protocol):
    def publish(self, event: dict) -> None: ...


class InMemoryEventPublisher:
    def __init__(self) -> None:
        self.events: list[dict] = []

    def publish(self, event: dict) -> None:
        self.events.append(event)


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

    def publish(self, event: dict) -> None:
        producer = self._get_producer()
        producer.produce(
            self.topic,
            key=event["aggregate_id"],
            value=json.dumps(event),
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
