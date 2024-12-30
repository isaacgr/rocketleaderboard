from typing import Callable, List
from rocketleaderboard.middleware.exception import error_middleware
from rocketleaderboard.middleware.rate_limit import TokenRateLimiter, \
    token_rate_limit_middleware_factory


def get_middlewares() -> List[Callable]:
    rate_limiter = token_rate_limit_middleware_factory(TokenRateLimiter())
    error = error_middleware

    return [rate_limiter, error]
