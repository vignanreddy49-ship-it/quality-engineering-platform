# ADR 0001 — Quality Engineering Stack

## Status

Accepted

## Context

The project needs to demonstrate modern quality engineering across browser, API, distributed systems, non-functional testing, DevOps and AI without turning into unrelated technology samples.

## Decision

Use Playwright/TypeScript for UI and API smoke, Python/pytest for backend/data/AI-oriented testing, Docker for reproducibility, Kafka/Pact/Testcontainers for distributed-system quality, k6 for performance, OWASP ZAP for security, and OpenTelemetry/Prometheus/Grafana for observability.

## Consequences

The stack is broad, but every component has a defined quality purpose and can be demonstrated through the same ShopSphere system.
