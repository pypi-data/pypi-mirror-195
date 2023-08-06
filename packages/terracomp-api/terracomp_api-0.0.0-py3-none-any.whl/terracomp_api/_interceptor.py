from typing import Any, Callable

from grpc_interceptor import ClientCallDetails, ClientInterceptor


class TokenInterceptor(ClientInterceptor):
    def __init__(self, token: str) -> None:
        self.token = token

    def intercept(self, method: Callable, request_or_iterator: Any, call_details: ClientCallDetails) -> Any:
        new_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            [("authorization", "token " + self.token)],
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression,
        )
        return method(request_or_iterator, new_details)
