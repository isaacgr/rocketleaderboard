from typing import Dict, List, cast
from strawberry.types.info import RootValueType
from rocketleaderboard.gql.schema import Player, Segment, Session
from rocketleaderboard.typedefs import T_CONTEXT
import strawberry
import logging


log = logging.getLogger('gql.query')


@strawberry.type
class Query:

    @strawberry.field
    async def player(
        self,
        info: strawberry.Info[T_CONTEXT, RootValueType],
        id: str
    ) -> Player:
        rl_api_manager = info.context['rl_api_manager']
        player = await rl_api_manager.get_player(id)
        return Player(
            platform_info=player['platformInfo'],
            segments=player['segments'],
            available_segments=player['availableSegments']
        )

    @strawberry.field
    async def segments(
        self,
        info: strawberry.Info[T_CONTEXT, RootValueType],
        id: str,
        season: int
    ) -> List[Segment]:
        pass

    @strawberry.field
    async def sessions(
        self,
        info: strawberry.Info[T_CONTEXT, RootValueType],
        id: str,
    ) -> List[Session]:
        pass
