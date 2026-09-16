# Distributed systems testing playbook

ShopSphere intentionally models asynchronous behavior so the quality strategy can demonstrate more than browser automation.

## Key risks

- duplicate messages
- delayed messages
- out-of-order messages
- partial service failure
- retry storms
- incompatible event contracts
- stale database state
- downstream timeout

## Assertion patterns

### Avoid fixed sleeps

Prefer bounded polling:

```text
until deadline:
    state = read_state()
    if state == expected:
        pass
    wait briefly
fail with diagnostic context
```

### Correlation

Every business event carries an `event_id`, aggregate identifier and timestamp. Tests use these values to correlate producer activity with consumer side effects.

### Failure diagnostics

A failed asynchronous test should report:

- correlation/event ID
- aggregate ID
- topic and partition when available
- consumer group
- retry count
- observed state transitions
- relevant service logs/traces

This is the foundation for the later OpenTelemetry implementation.
