from typing import TYPE_CHECKING, Any, Dict, TypedDict
from aiohttp.web import Request, StreamResponse

if TYPE_CHECKING:
    from rocketleaderboard.managers.rltracker import RlTrackerManager


# GraphQL
#


class T_CONTEXT(TypedDict):
    request: Request
    response: StreamResponse
    rl_api_manager: 'RlTrackerManager'
    config: Dict[str, Any]


class T_CONTROL_ADDRESS(TypedDict):
    host: str
    port: int
