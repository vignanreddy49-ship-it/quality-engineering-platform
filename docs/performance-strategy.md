# Performance Strategy

## Scenarios

- product catalog read
- product detail read
- order creation
- order retrieval
- mixed read/write workload

## k6 thresholds

The initial target is to keep normal API traffic below a defined p95 latency threshold and maintain an acceptable error rate. Thresholds will be tightened as the application and environment become more realistic.

Example:

```javascript
thresholds: {
  http_req_failed: ['rate<0.01'],
  http_req_duration: ['p(95)<500'],
}
```

## Test types

- smoke load: validate script and environment
- baseline: establish normal latency
- load: expected traffic
- stress: determine degradation point
- soak: identify long-running instability

Performance results should be compared against a baseline rather than interpreted from a single run.
