"""OpenTelemetry setup and trace propagation helpers for ShopSphere."""

import os
from contextlib import contextmanager
from typing import Iterator

from opentelemetry import trace
from opentelemetry.propagate import extract, inject
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor


def configure_tracing() -> TracerProvider:
    """Configure tracing with console output locally and optional OTLP export."""
    provider = TracerProvider(
        resource=Resource.create(
            {
                "service.name": os.getenv("OTEL_SERVICE_NAME", "shopsphere-api"),
                "service.version": os.getenv("OTEL_SERVICE_VERSION", "0.4.0"),
                "deployment.environment.name": os.getenv("OTEL_ENVIRONMENT", "local"),
            }
        )
    )
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint:
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True)))
    else:
        provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    return provider


def get_tracer(name: str = "shopsphere"):
    return trace.get_tracer(name)


def inject_trace_headers(headers: dict[str, str] | None = None) -> dict[str, str]:
    """Inject W3C trace context into a string Kafka/HTTP-style header map."""
    carrier = dict(headers or {})
    inject(carrier)
    return carrier


def extract_trace_headers(headers: dict[str, str] | None = None):
    """Extract W3C trace context from a string Kafka/HTTP-style header map."""
    return extract(dict(headers or {}))


@contextmanager
def traced_operation(name: str, attributes: dict[str, str] | None = None) -> Iterator:
    """Create a span that is convenient for service-level business operations."""
    with get_tracer().start_as_current_span(name, attributes=attributes or {}) as span:
        yield span
