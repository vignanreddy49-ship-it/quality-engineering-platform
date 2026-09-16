# Pact Contract Testing

This suite will verify that consumers and providers agree on API/event contracts.

## Planned flow

```text
Consumer test
     │
     ▼
  Pact file
     │
     ▼
Provider verification
     │
  ┌──┴──┐
 PASS  FAIL
```

The important QE behavior is that a breaking provider change is detected before deployment, without requiring a full end-to-end environment.
