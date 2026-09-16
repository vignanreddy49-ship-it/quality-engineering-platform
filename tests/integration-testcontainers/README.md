# Testcontainers Integration Tests

Integration tests will start real disposable dependencies instead of replacing every dependency with mocks.

Target dependencies:

- PostgreSQL
- Kafka
- WireMock for external payment/notification APIs

## Why

This layer catches configuration, serialization, persistence and integration defects that unit/API tests against mocks can miss.
