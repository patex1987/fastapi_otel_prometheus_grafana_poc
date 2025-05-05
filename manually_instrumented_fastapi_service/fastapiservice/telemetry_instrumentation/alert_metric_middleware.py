from functools import wraps
from typing import Any, Callable, Awaitable

from opentelemetry import metrics


class AlertMetricMiddleware:
    """The ASGI application middleware.

    This class is an ASGI middleware that starts and annotates spans for any
    requests it is invoked with.

    Args:
        app: The ASGI application callable to forward requests to.
        tracer:
        meter:
    """

    # pylint: disable=too-many-branches
    def __init__(
        self,
        app,
        tracer=None,
        meter=None,
    ):
        self.app = app
        if meter is None:
            meter = metrics.get_meter(__name__)
        self.total_requests = meter.create_counter(name='middleware_total_requests')
        self.total_requests.add(0)
        self.failure_requests = meter.create_counter(name='middleware_failed_requests')
        self.failure_requests.add(0, attributes={'type': '4xx'})
        self.failure_requests.add(0, attributes={'type': '5xx'})

    async def __call__(
        self,
        scope: dict[str, Any],
        receive: Callable[[], Awaitable[dict[str, Any]]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        if scope["type"] not in ("http", "websocket"):
            return await self.app(scope, receive, send)

        self.total_requests.add(1)

        attributes = {}
        instrumented_send = get_instrumented_send(send, scope, attributes)
        try:
            await self.app(scope, receive, instrumented_send)
        except Exception as exc:
            self.failure_requests.add(
                1, attributes={'type': 'unhandled_exception', 'exception_class': exc.__class__.__name__}
            )
        #     raise exc
        finally:
            status_code = attributes.get('status_code')
            if status_code and 400 <= status_code < 500:
                self.failure_requests.add(1, attributes={'type': '4xx'})
            if status_code and 500 <= status_code < 600:
                self.failure_requests.add(1, attributes={'type': '5xx'})


def get_instrumented_send(send, scope, attributes):

    @wraps(send)
    async def instrumented_send(message: dict[str, Any]):
        status_code = None

        if message['type'] == 'http.response.start':
            status_code = message['status']
        if message['type'] == 'websocket.send':
            status_code = 200

        if status_code:
            attributes['status_code'] = status_code

        await send(message)

    return instrumented_send
