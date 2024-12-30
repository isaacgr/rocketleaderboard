from aiohttp import web
from collections import defaultdict
from typing import Any, Callable, Dict
import logging
import time
import math

log = logging.getLogger('middleware.rate_limit')


class TokenRateLimiter:
    """
    Rate limits an HTTP client. Calls are rate-limited by host.
    This class is not thread-safe.
    """
    RATE = 10
    MAX_TOKENS = 100

    def __init__(self):
        self.client_tokens = defaultdict(lambda: self.MAX_TOKENS)
        self.client_update_time = defaultdict(lambda: time.monotonic())

    @property
    def client_tokens(self):
        return self._client_tokens

    @client_tokens.setter
    def client_tokens(self, client_tokens: Dict[str, int]):
        self._client_tokens = client_tokens

    @property
    def client_update_time(self):
        return self._client_update_time

    @client_update_time.setter
    def client_update_time(self, client_update_time: Dict[str, float]):
        self._client_update_time = client_update_time

    async def wait_for_token(self, client_ip: str):
        log.debug(f'Waiting for token. Client [{client_ip}].')
        await self.add_new_tokens(client_ip)
        self.client_tokens[client_ip] -= 1

    async def add_new_tokens(self, client_ip: str):
        log.debug(f'Adding new tokens. Client [{client_ip}].')
        client_tokens = self.client_tokens[client_ip]
        now = time.monotonic()
        time_since_update = now - self.client_update_time[client_ip]
        new_tokens = math.floor(time_since_update * self.RATE)
        if client_tokens + new_tokens >= 1:
            self.client_tokens[client_ip] = min(
                client_tokens + new_tokens,
                self.MAX_TOKENS,
            )
            self.client_update_time[client_ip] = now


def token_rate_limit_middleware_factory(limiter: TokenRateLimiter):
    @web.middleware
    async def token_rate_limit_middleware(
        request: web.Request,
        handler: Callable[['web.Request'], Any],
    ):
        client_ip = request.remote
        assert client_ip
        await limiter.wait_for_token(client_ip)
        if limiter.client_tokens[client_ip] <= 0:
            log.debug(
                f'Request was rate limited. Client [{client_ip}]. '
                f'Waiting [{limiter.RATE}]',
            )
            return web.json_response(
                {'error': 'Request was rate limited'},
                status=429,
                headers={'Retry-After': str(limiter.RATE)}
            )
        return await handler(request)
    return token_rate_limit_middleware
