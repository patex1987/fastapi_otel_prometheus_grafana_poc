import pudb
pudb.set_trace()

import fastapi
# import debugpy
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.trace import (
    get_tracer_provider,
    set_tracer_provider,
)

from opentelemetry.instrumentation.requests import RequestsInstrumentor
RequestsInstrumentor().instrument()

# Create FastAPI app
app = fastapi.FastAPI()

set_tracer_provider(TracerProvider())
tracer_provider: TracerProvider = get_tracer_provider()
tracer = tracer_provider.get_tracer(__name__)


otlp_span_exporter = OTLPSpanExporter()
span_processor = BatchSpanProcessor(otlp_span_exporter)
tracer_provider.add_span_processor(span_processor)

console_exporter = ConsoleSpanExporter()
span_processor = BatchSpanProcessor(console_exporter)
tracer_provider.add_span_processor(span_processor)




FastAPIInstrumentor.instrument_app(app)



# Instrument FastAPI with OpenTelemetry
# FastAPIInstrumentor.instrument_app(app)
