# Observability Strategy

Quality failures should be diagnosable without guessing.

## Signals

- **Logs:** structured application events
- **Metrics:** request count, errors, latency and business counters
- **Traces:** request path across service boundaries

## Current stack

```text
HTTP request
    │
    ▼
ShopSphere API ── OpenTelemetry FastAPI instrumentation
    │
    ├── business span: shopsphere.order.create
    │
    └── Kafka producer
           │  W3C traceparent + x-correlation-id headers
           ▼
      orders topic
           │
           ▼
Notification consumer
    │
    └── child span: shopsphere.kafka.process_order_created
           │
           ▼
OpenTelemetry Collector ──► Jaeger

Metrics ──────────────────► Prometheus ──► Grafana
```

## Trace propagation

- HTTP requests receive or generate `X-Request-ID`.
- The request ID is returned on the response and copied to Kafka as `x-correlation-id`.
- The active OpenTelemetry span is injected as W3C `traceparent` into Kafka headers.
- The notification consumer extracts that context and starts a child processing span.
- Event payloads remain unchanged; correlation and trace context travel in message metadata, avoiding an unnecessary event-schema version change.

## Local trace backend

Start the local Jaeger + OpenTelemetry Collector stack:

```bash
docker compose -f infrastructure/observability/docker-compose.tracing.yml up -d
OTEL_EXPORTER_OTLP_ENDPOINT=localhost:4319 uvicorn apps.api.main:app --reload
```

Open Jaeger at `http://localhost:16686` and search for the `shopsphere-api` service. The collector receives OTLP/gRPC on host port `4319` and forwards traces to Jaeger.

## QE use cases

- correlate a slow E2E test with API latency
- follow an order from HTTP request to Kafka consumer processing
- identify error spikes during performance tests
- validate that important business events are emitted
- inspect downstream dependency failures
- support RCA with objective telemetry
