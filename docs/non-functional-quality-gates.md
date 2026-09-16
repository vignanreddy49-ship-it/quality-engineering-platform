# Non-Functional Quality Gates

ShopSphere treats non-functional quality as executable engineering signals rather than a checklist at the end of testing.

## Performance

- **k6 smoke/baseline:** validates health and catalog behavior under a small controlled load.
- **k6 order flow:** exercises the state-changing order API with explicit p95/p99 latency and error-rate thresholds.
- Thresholds are intentionally separated by endpoint tags so a slow order path is visible without hiding behind aggregate latency.

## Security

- **Fast regression tests:** verify that common API errors do not expose stack traces or obvious secret material and that validation rejects unsafe input sizes.
- **OWASP ZAP baseline:** scans the running API surface in CI. Scanner findings are currently non-blocking while the application is still evolving; the fast security regression suite is the blocking signal.

## Observability

The API exposes Prometheus-compatible counters for request count and cumulative request duration. Contract tests verify metric names, types and content so monitoring regressions can be caught during development.

## CI model

```text
PR
 ├── fast security + observability regressions  (blocking)
 ├── k6 order-flow performance gate             (blocking)
 └── ZAP baseline scan                          (visibility/non-blocking)
```

The next production-grade step is distributed tracing with OpenTelemetry, correlation propagation across Kafka consumers, and release-time performance trend comparison rather than relying only on single-run thresholds.
