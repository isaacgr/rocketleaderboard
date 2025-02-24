from abc import abstractmethod, ABC
from typing import Any, Dict

from rocketleaderboard.clients.client import RlClient


class ClientFactory(ABC):

    @abstractmethod
    def __init__(
        self,
        hosts: Dict[str, Any],
    ):
        self._host = hosts['host']

    @abstractmethod
    def get_client(self) -> RlClient:
        pass
