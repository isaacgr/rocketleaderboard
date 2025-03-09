from typing import Any, Dict
from rocketleaderboard.clients.base import ClientFactory
from rocketleaderboard.clients.rltracker.client import RLTrackerClient


class RLTrackerClientFactory(ClientFactory):

    def __init__(
        self,
        hosts: Dict[str, Any],
    ):
        self.host = hosts['host']

    def get_client(self) -> RLTrackerClient:
        return RLTrackerClient(self)
