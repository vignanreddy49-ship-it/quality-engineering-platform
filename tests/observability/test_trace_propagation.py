"""Unit tests for distributed trace propagation without requiring a collector."""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

from apps.api.observability import extract_trace_headers, inject_trace_headers


def test_w3c_trace_context_round_trips_through_headers():
    provider = TracerProvider()
    previous = trace.get_tracer_provider()
    trace.set_tracer_provider(provider)
    try:
        tracer = trace.get_tracer("test")
        with tracer.start_as_current_span("producer") as span:
            headers = inject_trace_headers()
            assert "traceparent" in headers
            extracted = extract_trace_headers(headers)
            assert extracted["traceparent"] == headers["traceparent"]
            assert span.get_span_context().trace_id != 0
    finally:
        # OpenTelemetry protects the global provider from replacement after first use;
        # this test deliberately uses the SDK's isolated propagation behavior only.
        _ = previous


def test_injection_preserves_existing_headers():
    headers = inject_trace_headers({"x-correlation-id": "corr-123"})
    assert headers["x-correlation-id"] == "corr-123"
