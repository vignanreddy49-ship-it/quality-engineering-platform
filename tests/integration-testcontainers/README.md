# Testcontainers Integration Tests

This layer starts real disposable dependencies instead of replacing every dependency with mocks.

## Current coverage

- **Kafka:** publish an `order.created` event to a real containerized broker, consume it, and assert the event envelope and aggregate correlation.
- **Consumer semantics:** feed the broker-delivered event into the notification consumer handler and verify successful notification delivery.

## Target dependencies

- PostgreSQL
- Kafka
- WireMock for external payment/notification APIs

## Why

This layer catches configuration, serialization, networking, persistence and integration defects that unit/API tests against mocks can miss.

## Run locally

```bash
pip install -r tests/integration-testcontainers/requirements.txt
pytest -q tests/integration-testcontainers -m integration
```

Docker must be available because Testcontainers provisions the broker dynamically. The CI workflow runs this suite on pull requests that touch the distributed-system test surface.
