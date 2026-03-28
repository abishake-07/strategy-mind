"""OpenTelemetry tracing setup for StrategyMind.

Exports traces to Jaeger or Zipkin if configured via env vars.
Call `setup_tracing()` at app startup.
"""
import os
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def setup_tracing(service_name="strategymind"):
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # Console exporter for dev (disabled to reduce noise)
    # provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
