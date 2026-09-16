# Architecture

## Quality architecture

The platform uses a layered strategy so that fast tests provide rapid feedback while deeper tests validate system behavior.

```text
                 Business journeys
                       │
                Playwright E2E
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
        API       Contract       Event
        tests       tests        tests
          │            │            │
          └────────────┼────────────┘
                       ▼
                 Integration
                Testcontainers
                       │
              ┌────────┴────────┐
              ▼                 ▼
         Performance         Security
             k6                 ZAP
              │                 │
              └────────┬────────┘
                       ▼
                 AI Evaluation
              RAG / Agent / LLM
```

## Design decisions

- **Playwright + TypeScript:** strong browser automation and API support with one modern language.
- **pytest + Python:** concise backend/data/AI test implementation and easy ecosystem integration.
- **FastAPI:** intentionally lightweight application code so quality engineering remains the focus.
- **Docker:** deterministic local execution.
- **Kubernetes/Terraform:** deployment patterns will mirror production platform concerns without requiring a cloud account.
- **Observability:** failures should be diagnosable from traces and metrics, not only screenshots/logs.

## Failure investigation flow

1. CI quality gate identifies the failed layer.
2. Test artifacts provide request/response, trace and screenshot evidence.
3. OpenTelemetry correlates the application operation across services.
4. Prometheus metrics identify resource or latency anomalies.
5. The RCA records defect category, impact and prevention action.
