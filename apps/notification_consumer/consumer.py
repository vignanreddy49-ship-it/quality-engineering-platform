"""Kafka adapter for the ShopSphere notification consumer."""
import json
import logging
import os

from confluent_kafka import Consumer, KafkaException, Producer
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor

from apps.api.observability import extract_trace_headers
from apps.notification_consumer.handler import (
    InMemoryEventStore,
    RecordingDeadLetterSink,
    RecordingNotificationSink,
    handle_event,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
LOG = logging.getLogger("shopsphere-notification-consumer")


def configure_tracing() -> None:
    provider = TracerProvider(
        resource=Resource.create(
            {
                "service.name": os.getenv("OTEL_SERVICE_NAME", "shopsphere-notification-consumer"),
                "service.version": os.getenv("OTEL_SERVICE_VERSION", "0.4.0"),
            }
        )
    )
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint:
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True)))
    else:
        provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)


def run() -> None:
    configure_tracing()
    tracer = trace.get_tracer("shopsphere.notification-consumer")
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
            if message is None:
                continue
            if message.error():
                raise KafkaException(message.error())
            raw_headers = {
                key: value.decode("utf-8") if value is not None else ""
                for key, value in (message.headers() or [])
            }
            parent_context = extract_trace_headers(raw_headers)
            correlation_id = raw_headers.get("x-correlation-id", "unknown")
            with tracer.start_as_current_span(
                "shopsphere.kafka.process_order_created",
                context=parent_context,
                attributes={
                    "messaging.system": "kafka",
                    "messaging.destination.name": topic,
                    "shopsphere.correlation_id": correlation_id,
                },
            ) as span:
                try:
                    event = json.loads(message.value().decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    span.record_exception(exc)
                    LOG.error("event_decode_failed reason=%s", exc)
                    producer.produce(dlq_topic, key=message.key(), value=message.value())
                    producer.flush(5)
                    consumer.commit(message=message, asynchronous=False)
                    continue
                span.set_attribute("shopsphere.event_id", event.get("event_id", "unknown"))
                result = handle_event(event, store, sink, dlq)
                LOG.info("event_processed event_id=%s result=%s", event.get("event_id"), result)
                if result == "dead_lettered":
                    producer.produce(dlq_topic, key=message.key(), value=json.dumps(event))
                    producer.flush(5)
                consumer.commit(message=message, asynchronous=False)
    finally:
        consumer.close()


if __name__ == "__main__":
    run()
