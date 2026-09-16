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
| Event-driven testing | Kafka-ready architecture |
| Contract testing | Pact-ready structure |
| Service virtualization | WireMock-ready structure |
| Integration testing | Testcontainers-ready structure |
| Performance | k6 |
| Security | OWASP ZAP |
| Containers | Docker / Compose |
| CI/CD | GitHub Actions |
| Kubernetes | K8s manifests |
| Infrastructure | Terraform structure |
| Observability | OpenTelemetry / Prometheus / Grafana |
| AI quality | RAG, LLM and agent evaluation structure |

## System under test

ShopSphere is a deliberately small e-commerce platform designed to create realistic quality-engineering problems: product search, inventory, checkout, order creation, payment events and downstream notifications.

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
                    │   API Gateway   │
                    └────────┬────────┘
                             │
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
       Product Service  Order Service  Payment Service
             │               │               │
             └───────────────┼───────────────┘
                             ▼
                         PostgreSQL
                             │
                           Kafka
                             │
                   ┌─────────┴─────────┐
                   ▼                   ▼
            Notifications         Analytics

      OpenTelemetry → Prometheus → Grafana

      Quality gates:
      UI | API | Contract | Integration | Security | Performance | AI
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
- Kafka events and consumer validation
- Pact consumer/provider contracts
- WireMock downstream simulation
- Testcontainers integration environment

### Phase 3 — Non-functional quality
- k6 performance thresholds
- OWASP ZAP baseline security scan
- OpenTelemetry instrumentation
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

Run API tests:

```bash
cd tests/api-python
pip install -r requirements.txt
pytest -q
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

## Documentation

- [Architecture](docs/architecture.md)
- [Test strategy](docs/test-strategy.md)
- [Quality gates](docs/quality-gates.md)
- [AI testing strategy](docs/ai-testing-strategy.md)
- [Security testing](docs/security-testing.md)
- [Performance strategy](docs/performance-strategy.md)
- [Observability](docs/observability.md)

## Portfolio positioning

This project is intentionally broader than a conventional UI automation framework. It demonstrates the engineering mindset required to own quality for distributed systems: design the quality architecture, automate UI/API/events, validate data and contracts, run tests in CI and containers, measure performance, test security, observe failures and evaluate AI behavior.
