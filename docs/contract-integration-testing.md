# Contract and Integration Testing

ShopSphere uses multiple test layers so failures are localized before they become end-to-end defects.

## Event contract

`tests/contracts/order-created.v1.json` defines the stable envelope for `order.created` events. The producer and consumer tests validate the event type, version, aggregate identity and payload shape.

## Integration boundary

`tests/integration-testcontainers/test_kafka_order_flow.py` starts a disposable Kafka broker with Testcontainers and verifies:

1. the producer can publish a real JSON event;
2. a consumer can retrieve the event from Kafka;
3. the event retains its aggregate correlation;
4. the notification handler can process the broker-delivered event.

The test deliberately keeps business assertions in the pure consumer handler so the suite separates **infrastructure failures** from **consumer logic failures**.

## Quality strategy

```text
Producer
   │
   ├── JSON Schema contract ──> fast contract tests
   │
   ▼
 Kafka container
   │
   ▼
Consumer adapter
   │
   └── handler ──> idempotency / retry / DLQ tests
```

The integration suite is slower than unit tests and therefore runs as a dedicated GitHub Actions quality gate.
