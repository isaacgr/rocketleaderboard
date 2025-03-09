import logging
from abc import ABC, abstractmethod
from rocketleaderboard.clients.rltracker.base import RLTrackerClientFactory

log = logging.getLogger('clients.client')


class RLClient(ABC):

    @abstractmethod
    def __init__(
        self,
        factory: RLTrackerClientFactory
    ):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    @abstractmethod
    def target(self, path) -> str:
        pass

    @abstractmethod
    async def make_req(self, url: str):
        pass

    async def get_player(self, id: str):
        pass

    async def get_playlist(self, id: str, season: int):
        pass

    async def get_sessions(self, id: str):
        pass
