from functools import cache

from httpx import AsyncHTTPTransport


@cache
def get_http_transport() -> AsyncHTTPTransport:
    return AsyncHTTPTransport(retries=3)
