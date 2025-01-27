import httpx
import pudb
pudb.set_trace()

import time
import random

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
    SpanKind,
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

# Example endpoint
@app.get("/")
async def read_root():
    #import pudb
    #pudb.set_trace()
    print(__file__)
    time.sleep(random.randint(2,5))
    return {"message": "Hello, OpenTelemetry!"}

@app.get("/slow")
async def slow():
    time.sleep(random.randint(10, 15))
    random_payload = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=100))
    return {"message": "Hello, OpenTelemetry!",  "payload": random_payload}

@app.get("/not-working")
async def not_working():
    # time.sleep(random.randint(10, 15))
    random_payload = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=100))
    raise ValueError('something went wrong')
    return {"message": "Hello, OpenTelemetry!",  "payload": random_payload}

@app.get("/call-with-httpx")
async def call_with_httpx():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = httpx.get(url)

    return {"message": "Hello, OpenTelemetry!", "httpx_response": response.json()}

@app.get("/call-with-httpx-async")
async def call_with_httpx_async():
    url = "https://jsonplaceholder.typicode.com/posts"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return {"message": "Hello, OpenTelemetry!", "httpx_response": response.json()}

# Instrument FastAPI with OpenTelemetry
# FastAPIInstrumentor.instrument_app(app)
