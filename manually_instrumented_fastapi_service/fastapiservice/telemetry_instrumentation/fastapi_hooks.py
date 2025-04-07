import logging

from opentelemetry.metrics import Counter

logger = logging.getLogger(__name__)


class FastApiServiceServerRequestHook:
    """
    hook for the requests to the api
    mainly used to emit the exact number of requests - used for alarming
    """

    def __init__(self, total_request_counter: Counter):
        self.total_request_counter = total_request_counter

    def hook(self, span, scope):
        logger.info(f'Custom server request hook called: span: {span}, scope: {scope}')
        if scope['type'] not in ('http', 'websocket'):
            return
        self.total_request_counter.add(1)


def custom_client_request_hook(span, scope, message):
    logger.info(f'Custom client request hook called: span: {span}, scope: {scope}, message: {message}')


class FastapiClientResponseHook:
    """
    hook for the responses
    mainly used to emit exact count of 4xx and 5xx status codes for alarming
    """

    def __init__(self, total_5xx_counter: Counter):
        self.total_5xx_counter = total_5xx_counter

    def hook(self, span, scope, message):
        """
        # TODO: handle websockets

        :param span:
        :param scope:
        :param message:
        :return:
        """
        logger.info(f'Custom client response hook called: span: {span}, scope: {scope}, message: {message}')
        if message['type'] == "http.response.start":
            http_status_code = message['status']
            if http_status_code >= 500:
                self.total_5xx_counter.add(1)
