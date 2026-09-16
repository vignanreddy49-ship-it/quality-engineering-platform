# Notification Consumer

Reference consumer boundary for the ShopSphere `order.created` event.

The consumer contract is intentionally separated from the API so the test suite can validate an event-driven workflow independently from HTTP behavior.

Planned production-style behavior:

1. Consume `order.created` from Kafka.
2. Validate the event against `tests/contracts/order-created.v1.json`.
3. Use `event_id` for idempotency.
4. Correlate logs with `aggregate_id`.
5. Retry transient failures and route poison messages to a DLQ.
6. Emit a notification side effect only after successful processing.

For the portfolio implementation, the consumer will first be exercised with deterministic test doubles before introducing external infrastructure into every PR run.
