# CI Quality Gates

## Pull request

```text
Lint → Unit → API → Contract → Playwright Smoke → Quality Gate
```

The PR pipeline should stay fast. It should prevent obvious regressions before merge.

## Release / scheduled

```text
Full Regression
      ↓
Integration + Kafka
      ↓
Security / ZAP
      ↓
Performance / k6
      ↓
AI Evaluation
      ↓
Observability Checks
      ↓
Release Gate
```

## Example policy

- Any critical API regression blocks the pipeline.
- Contract incompatibility blocks deployment.
- Security findings are classified by severity and policy threshold.
- Performance thresholds are versioned with the service.
- AI evaluation uses a fixed dataset and explicit pass criteria.
- Flaky tests are tracked separately rather than silently ignored.

## Quality scorecard

Future pipeline iterations will publish:

- pass/fail rate
- flaky test rate
- regression duration
- API error rate
- p95 latency
- security findings
- contract compatibility
- AI evaluation score
- escaped-defect trend
