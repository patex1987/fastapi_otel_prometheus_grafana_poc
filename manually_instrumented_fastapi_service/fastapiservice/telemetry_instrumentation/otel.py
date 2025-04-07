from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace import set_tracer_provider, get_tracer_provider


def initialize_opentelemetry():
    """
    Configures all opentelemetry related components for the application
    Namely:
    - sets up tracing
        - sets the Tracer Provider
        - sending traces to the console
        - sending traces to otel collector using grpc
    - sets up metrics
        - sets the Metric Provider
        - sending metrics to the console
        - sending metrics to otel collector using grpc

    TODO: make the selection of exporters configurable through env vars like
        its done in auto-instrumentations
    TODO: create a common resource (`from opentelemetry.sdk.resources import Resource`)
    """
    set_tracer_provider(TracerProvider())
    tracer_provider: TracerProvider = get_tracer_provider()

    # export spans to otel
    otlp_span_exporter = OTLPSpanExporter()
    span_processor = BatchSpanProcessor(otlp_span_exporter)
    tracer_provider.add_span_processor(span_processor)

    # print the spans to the console
    console_exporter = ConsoleSpanExporter()
    span_processor = BatchSpanProcessor(console_exporter)
    tracer_provider.add_span_processor(span_processor)

    # send metrics to otel
    otlp_metric_exporter = OTLPMetricExporter()
    otlp_metric_reader = PeriodicExportingMetricReader(otlp_metric_exporter)

    # send metrics to console
    console_metric_exporter = ConsoleMetricExporter()
    console_metric_reader = PeriodicExportingMetricReader(console_metric_exporter)
    metric_readers = [otlp_metric_reader, console_metric_reader]

    meter_provider = MeterProvider(metric_readers=metric_readers)
    metrics.set_meter_provider(meter_provider)
