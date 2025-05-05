# import pudb
import logging

from opentelemetry.instrumentation.requests import RequestsInstrumentor
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from fastapiservice.api.v1.routes.dummy_routes import dummy_router
from fastapiservice.api.v1.routes.throttle_optimization import throttle_router

# pudb.set_trace()
import fastapi

from fastapiservice.telemetry_instrumentation.alert_metric_middleware import AlertMetricMiddleware
from fastapiservice.telemetry_instrumentation.fastapi_setup import instrument_fastapi
from fastapiservice.telemetry_instrumentation.otel import initialize_opentelemetry

# import debugpy


logger = logging.getLogger(__name__)


def create_app():

    app = fastapi.FastAPI()
    app.include_router(dummy_router, prefix='/api/v1/dummy', tags=["dummy"])
    app.include_router(throttle_router, prefix='/api/v1/throttle', tags=["throttle"])
    instrument_for_telemetry(app)

    app.add_exception_handler(Exception, exception_handler)
    app.add_exception_handler(500, exception_handler)

    return app


async def exception_handler(request: Request, exc: Exception) -> Response:
    return JSONResponse(
        status_code=500,
        content={"message": f"An error occurred: {exc.__class__.__name__}"},
    )


def instrument_for_telemetry(app: fastapi.FastAPI):
    """
    - configures the opentelemetry providers (metrics, traces)
    - instruments requests
    - instruments fastapi with OpentelemetryMiddleware

    :param app:
    :return:
    """
    initialize_opentelemetry()

    # instrument the desired packages
    instrument_fastapi(app)
    RequestsInstrumentor().instrument()
    app.add_middleware(AlertMetricMiddleware)
