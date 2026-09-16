# Quality Engineering Platform — ShopSphere

A portfolio-grade Quality Engineering reference implementation for a distributed e-commerce platform.

> **Portfolio goal:** demonstrate Staff/Lead SDET, Quality Engineering Architect and AI Quality Engineering skills through one coherent, runnable system.

## Coverage

| Capability | Implementation |
|---|---|
| UI automation | Playwright + TypeScript |
| API automation | Python + pytest |
| Backend | FastAPI |
| Database | PostgreSQL |
| Event-driven testing | Kafka producer + notification consumer |
| Event contracts | JSON Schema for `order.created.v1` |
| Event reliability | Idempotency, bounded retry and DLQ handling |
| Contract testing | Pact-ready structure |
| Service virtualization | WireMock-ready structure |
| Integration testing | Testcontainers-ready structure |
| Performance | k6 |
| Security | OWASP ZAP |
| Containers | Docker / Compose |
| CI/CD | GitHub Actions |
| Kubernetes | K8s manifests |
| Infrastructure | Terraform structure |
| Observability | Prometheus / Grafana |
| AI quality | RAG, LLM and agent evaluation structure |

## System under test

ShopSphere is a deliberately small e-commerce platform designed to create realistic quality-engineering problems: product search, inventory, checkout, order creation and downstream notifications.

```text
                         ShopSphere
                             │
                    ┌────────▼────────┐
                    │    Web Store    │
                    └────────┬────────┘
                             │
                        Playwright
                             │
                    ┌────────▼────────┐
                    │   ShopSphere API │
                    └────────┬────────┘
                             │
                        Order Created
                             │
                    ┌────────▼────────┐
                    │      Kafka      │
                    │     orders      │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Notification    │
                    │ Consumer        │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Email / Sink    │
                    └─────────────────┘

             Invalid / failed events → orders.dlq

      Prometheus → Grafana

      Quality gates:
      UI | API | Events | Contract | Security | Performance | AI
```

## Repository roadmap

### Phase 1 — Core platform
- FastAPI product and order services
- PostgreSQL persistence
- Docker Compose
- Python API tests
- Playwright UI smoke suite
- GitHub Actions PR quality gate

### Phase 2 — Distributed systems quality
- Kafka producer and notification consumer
- JSON Schema event validation
- Idempotency and bounded retry behavior
- Dead-letter queue handling
- Pact consumer/provider contracts
- WireMock downstream simulation
- Testcontainers integration environment

### Phase 3 — Non-functional quality
- k6 performance thresholds
- OWASP ZAP baseline security scan
- Prometheus/Grafana dashboards

### Phase 4 — AI quality engineering
- Evaluation dataset
- RAG correctness/relevance checks
- hallucination checks
- prompt-injection/adversarial tests
- LLM-as-a-judge pattern
- agent workflow evaluation

### Phase 5 — Platform engineering
- Kubernetes deployment
- Terraform/AWS structure
- deeper CI/CD gates
- quality scorecard and release policy

## Kafka quick start

Start Kafka and create the required topics:

```bash
docker compose -f infrastructure/docker/kafka/docker-compose.kafka.yml up -d
# Run the topic bootstrap script from a Kafka-enabled environment.
./infrastructure/docker/kafka/init-topics.sh
```

Run the API in memory mode for normal local development (default), or enable Kafka publishing:

```bash
export EVENT_PUBLISHER=kafka
export KAFKA_BOOTSTRAP_SERVERS=localhost:9092
uvicorn apps.api.main:app --reload
```

Run the notification consumer:

```bash
export KAFKA_BOOTSTRAP_SERVERS=localhost:9092
python -m apps.notification_consumer.consumer
```

The consumer uses manual offset commits, validates the event envelope, ignores duplicate `event_id` values, retries notification delivery within a fixed bound, and publishes terminal failures to `orders.dlq`.

## Quick start

```bash
# start the sample API + PostgreSQL
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API docs: `http://localhost:8000/docs`

Run API and event tests:

```bash
pip install -r apps/api/requirements.txt pytest==8.3.4 jsonschema==4.23.0
pytest -q tests/api-python tests/events
```

Run UI tests after the web application is available:

```bash
cd tests/ui-playwright
npm install
npx playwright install --with-deps
npm test
```

## Engineering principles

1. Test at the lowest reliable layer; reserve E2E for critical business journeys.
2. Make environments reproducible and observable.
3. Treat reliability, performance, security and AI behavior as quality attributes.
4. Keep PR feedback fast and push deeper suites to scheduled/release pipelines.
5. Make quality gates explicit and measurable.
6. Design event consumers for at-least-once delivery rather than assuming exactly-once behavior.

## Documentation

- [Architecture](docs/architecture.md)
- [Test strategy](docs/test-strategy.md)
- [Distributed testing](docs/distributed-testing.md)
- [Quality gates](docs/quality-gates.md)
- [AI testing strategy](docs/ai-testing-strategy.md)
- [Security testing](docs/security-testing.md)
- [Performance strategy](docs/performance-strategy.md)
- [Observability](docs/observability.md)

## Portfolio positioning

This project is intentionally broader than a conventional UI automation framework. It demonstrates the engineering mindset required to own quality for distributed systems: design the quality architecture, automate UI/API/events, validate data and contracts, handle retries and duplicates, run tests in CI and containers, measure performance, test security, observe failures and evaluate AI behavior.
