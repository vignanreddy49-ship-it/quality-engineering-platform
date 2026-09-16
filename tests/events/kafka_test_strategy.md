# Kafka test strategy

## Test pyramid for asynchronous workflows

| Layer | Purpose | Example |
|---|---|---|
| Unit | Pure event transformation | Order → event envelope |
| Contract | Producer/consumer compatibility | `order.created.v1` schema |
| Component | Consumer behavior in isolation | Notification consumer |
| Integration | Broker + consumer + persistence | Kafka + PostgreSQL |
| E2E | Business journey | Checkout → notification |

## Reliability scenarios

- **At-least-once delivery:** duplicate delivery must not create duplicate notifications.
- **Idempotency:** consumer stores a processed-event key and safely ignores replays.
- **Retry:** transient downstream failures are retried with bounded backoff.
- **Dead letter:** permanently invalid events are isolated rather than retried forever.
- **Ordering:** events for the same aggregate are processed in the expected order.
- **Schema evolution:** incompatible payload changes fail contract validation before deployment.
- **Eventual consistency:** tests poll for a bounded period rather than using arbitrary sleeps.

## Quality gate proposal

PR: schema + unit/component tests.

Main branch: integration tests with Kafka/PostgreSQL.

Scheduled: failure injection, replay/idempotency and larger event-volume tests.
