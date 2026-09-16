import json
import time

import pytest
from confluent_kafka import Consumer, Producer
from testcontainers.kafka import KafkaContainer

from apps.api.events import build_order_created_event
from apps.notification_consumer.handler import (
    InMemoryEventStore,
    RecordingDeadLetterSink,
    RecordingNotificationSink,
    handle_event,
)


@pytest.mark.integration

def test_order_created_event_round_trips_through_kafka():
    """Exercise the real broker boundary, then assert consumer semantics separately."""
    with KafkaContainer("confluentinc/cp-kafka:7.7.1") as kafka:
        bootstrap = kafka.get_bootstrap_server()
        topic = "orders.integration"
        producer = Producer({"bootstrap.servers": bootstrap})
        consumer = Consumer({
            "bootstrap.servers": bootstrap,
            "group.id": "integration-test",
            "auto.offset.reset": "earliest",
        })
        consumer.subscribe([topic])

        event = build_order_created_event({
            "id": "o-integration",
            "customer_email": "integration@example.com",
            "total": 12998.0,
            "status": "CREATED",
        })
        producer.produce(topic, key=event["aggregate_id"], value=json.dumps(event))
        producer.flush(10)

        received = None
        deadline = time.time() + 20
        while time.time() < deadline and received is None:
            message = consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                raise RuntimeError(message.error())
            received = json.loads(message.value().decode("utf-8"))

        consumer.close()

        assert received is not None
        assert received["event_type"] == "order.created"
        assert received["aggregate_id"] == "o-integration"
        assert received["payload"]["order_id"] == received["aggregate_id"]

        store = InMemoryEventStore()
        sink = RecordingNotificationSink()
        dlq = RecordingDeadLetterSink()
        assert handle_event(received, store, sink, dlq) == "processed"
        assert len(sink.notifications) == 1
        assert not dlq.messages
