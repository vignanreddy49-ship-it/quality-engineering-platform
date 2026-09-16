"""Kafka adapter for the ShopSphere notification consumer."""
import json
import logging
import os
from confluent_kafka import Consumer, KafkaException, Producer
from apps.notification_consumer.handler import InMemoryEventStore, RecordingDeadLetterSink, RecordingNotificationSink, handle_event

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
LOG = logging.getLogger("shopsphere-notification-consumer")

def run() -> None:
    bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topic = os.getenv("KAFKA_ORDER_TOPIC", "orders")
    group = os.getenv("KAFKA_CONSUMER_GROUP", "notification-service")
    dlq_topic = os.getenv("KAFKA_DLQ_TOPIC", "orders.dlq")
    consumer = Consumer({"bootstrap.servers": bootstrap, "group.id": group, "auto.offset.reset": "earliest", "enable.auto.commit": False})
    producer = Producer({"bootstrap.servers": bootstrap})
    store, sink, dlq = InMemoryEventStore(), RecordingNotificationSink(), RecordingDeadLetterSink()
    consumer.subscribe([topic])
    LOG.info("consumer_started topic=%s group=%s", topic, group)
    try:
        while True:
            message = consumer.poll(1.0)
            if message is None: continue
            if message.error(): raise KafkaException(message.error())
            try:
                event = json.loads(message.value().decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                LOG.error("event_decode_failed reason=%s", exc)
                producer.produce(dlq_topic, key=message.key(), value=message.value())
                producer.flush(5)
                consumer.commit(message=message, asynchronous=False)
                continue
            result = handle_event(event, store, sink, dlq)
            LOG.info("event_processed event_id=%s result=%s", event.get("event_id"), result)
            if result == "dead_lettered":
                producer.produce(dlq_topic, key=message.key(), value=json.dumps(event))
                producer.flush(5)
            consumer.commit(message=message, asynchronous=False)
    finally:
        consumer.close()

if __name__ == "__main__": run()
