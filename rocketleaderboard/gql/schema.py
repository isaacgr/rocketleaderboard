
import strawberry
from typing import List, Optional, cast


@strawberry.type
class SeasonRewardsMetadata:
    rank_name: str
    icon_url: str


@strawberry.type
class Performance:
    percentile: str
    display_name: str
    display_value: str
    value: float
    metadata: Optional[SeasonRewardsMetadata]


@strawberry.type
class Metadata:
    name: str
    start_date: str
    end_date: str
    result: str
    playlist: str
    date_collected: str


@strawberry.type
class Attributes:
    season: int


@strawberry.type
class Tier:
    metadata: Metadata


@strawberry.type
class Stats:
    tier: Tier
    division: Tier
    matches_played: Performance
    win_streak: Performance
    rating: Performance


@strawberry.type
class Segment:
    type: str
    metadata: Metadata
    attributes: Attributes
    stats: 'Stats | Overview'


@strawberry.type
class PlatformInfo:
    platform_user_handle: str
    avatar_url: str


@strawberry.type
class Overview:
    wins: Performance
    goals: Performance
    saves: Performance
    mvps: Performance
    shots: Performance
    assists: Performance
    goal_shot_ratio: Performance
    season_reward_level: Performance
    matches_played: Performance


@strawberry.type
class Matches:
    metadata: Metadata
    stats: Overview


@strawberry.type
class Session:
    metadata: Metadata
    matches: List[Matches]


@strawberry.type
class Player:
    platform_info: PlatformInfo
    segments: List[Segment]
    available_segments: List[Segment]

    @strawberry.field
    def overview(self) -> Optional[Overview]:
        for segment in self.segments:
            if segment.type == 'overview':
                overview = cast(Overview, segment.stats)
                return overview
        return None
