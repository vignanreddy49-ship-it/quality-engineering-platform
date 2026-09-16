# Test Strategy

## Risk-based test pyramid

| Layer | Primary goal | Examples | Expected feedback |
|---|---|---|---|
| Unit | Business rules | pricing, validation | seconds |
| API | Service behavior | products, orders | seconds |
| Contract | Service compatibility | schemas/events | seconds |
| Integration | Real dependencies | PostgreSQL/Kafka | minutes |
| UI E2E | Critical journeys | browse → checkout | minutes |
| Performance | Capacity and latency | checkout load | scheduled/release |
| Security | Vulnerabilities and abuse | auth/input/ZAP | scheduled/release |
| AI evaluation | Behavioral quality | RAG/agent scenarios | PR + scheduled |

## Critical business journeys

1. Browse product catalog.
2. Retrieve product details.
3. Create an order with valid inventory.
4. Reject unknown products.
5. Reject invalid quantities.
6. Validate order totals.
7. Publish and consume order events.
8. Complete payment workflow.

## Quality attributes

- Correctness
- Reliability
- Compatibility
- Performance
- Security
- Observability
- Resilience
- AI factuality and relevance

## Definition of Done

A feature is not considered production-ready until functional tests, relevant contracts, security checks, performance expectations and observability requirements are satisfied at the appropriate pipeline stage.
