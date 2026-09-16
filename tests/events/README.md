# Event-driven quality

This suite demonstrates how a QE engineer tests asynchronous workflows without making every test an end-to-end test.

## Current scenarios

- Versioned event envelope
- Event schema compatibility
- Required-field validation
- Event identity for idempotency

## Kafka scenarios planned

1. Publish `order.created` to Kafka.
2. Consume it from the notification consumer group.
3. Assert the notification side effect.
4. Replay the same event and assert idempotency.
5. Inject consumer failure and verify retry/backoff behavior.
6. Verify eventual consistency between order and inventory state.
7. Verify incompatible event versions are rejected safely.

The event contract lives in `tests/contracts/order-created.v1.json` so producers and consumers can validate the same source of truth.
