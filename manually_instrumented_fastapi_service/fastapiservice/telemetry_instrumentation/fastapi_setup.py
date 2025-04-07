from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.metrics import get_meter_provider
from opentelemetry.trace import get_tracer_provider

from fastapiservice.telemetry_instrumentation.fastapi_hooks import (
    FastapiClientResponseHook,
    FastApiServiceServerRequestHook,
    custom_client_request_hook,
)


def instrument_fastapi(app):
    """
    instruments fastapi with `OpentelemetryMiddleware`
    (`FastAPIInstrumentor.instrument_app`) sets it up with custom server and
    client hooks, that have properly initialized with 0
    https://prometheus.io/docs/practices/instrumentation/#avoid-missing-metrics

    Currently, it counts the total number of requests and the responses resulting
    in http status 5xx. these metrics can be used to calculate the failure ratio
    and alarming

    :param app:
    :return:
    """

    meter = get_meter_provider().get_meter(__name__)

    counter_5xx = meter.create_counter('hook_http_5xx_failures')
    counter_5xx.add(0)
    custom_client_response_hook = FastapiClientResponseHook(total_5xx_counter=counter_5xx)

    counter_total_requests = meter.create_counter('hook_total_api_requests')
    counter_total_requests.add(0)
    custom_server_request_hook = FastApiServiceServerRequestHook(total_request_counter=counter_total_requests)

    FastAPIInstrumentor.instrument_app(
        app,
        server_request_hook=custom_server_request_hook.hook,
        client_request_hook=custom_client_request_hook,
        client_response_hook=custom_client_response_hook.hook,
        tracer_provider=get_tracer_provider(),
        meter_provider=get_meter_provider(),
    )
