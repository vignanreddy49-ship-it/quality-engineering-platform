"""Unit tests for distributed trace propagation without requiring a collector."""

from opentelemetry import trace
from opentelemetry.trace import NonRecordingSpan, SpanContext, TraceFlags

from apps.api.observability import extract_trace_headers, inject_trace_headers


def test_w3c_trace_context_round_trips_through_headers():
    span_context = SpanContext(
        trace_id=0x1234567890ABCDEF1234567890ABCDEF,
        span_id=0x1234567890ABCDEF,
        is_remote=False,
        trace_flags=TraceFlags(TraceFlags.SAMPLED),
    )
    context = trace.set_span_in_context(NonRecordingSpan(span_context))
    token = trace.attach(context)
    try:
        headers = inject_trace_headers()
        assert headers["traceparent"].startswith("00-1234567890abcdef1234567890abcdef-")
        extracted = extract_trace_headers(headers)
        assert extracted is not None
    finally:
        trace.detach(token)


def test_injection_preserves_existing_headers():
    headers = inject_trace_headers({"x-correlation-id": "corr-123"})
    assert headers["x-correlation-id"] == "corr-123"
