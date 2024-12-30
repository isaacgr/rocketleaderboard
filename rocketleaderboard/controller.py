import asyncio
from typing import Any, Dict

from rocketleaderboard.config.ini import RL_TRACKER_CONFIG_SECTION, RL_TRACKER_HOSTS_SECTION
from rocketleaderboard.managers.rltracker import RlTrackerManager
from rocketleaderboard.server.server import HttpServer
from rocketleaderboard.typedefs import T_CONTROL_ADDRESS


class ServerController:

    def __init__(
        self,
        host: T_CONTROL_ADDRESS,
        server: HttpServer,
        rl_api_manager: RlTrackerManager
    ):
        self._host = host
        self._server = server
        self._rl_api_manager = rl_api_manager

    @property
    def host(self):
        return self._host

    @property
    def rl_api_manager(self):
        return self._rl_api_manager

    @classmethod
    def from_config(
        cls,
        host: T_CONTROL_ADDRESS,
        config: Dict[str, Dict[str, Any]],
    ):
        rl_api_config = config[RL_TRACKER_CONFIG_SECTION]
        rl_api_hosts = config[RL_TRACKER_HOSTS_SECTION]

        rl_api_manager = cls.get_rl_api_manager(rl_api_config, rl_api_hosts)

        assert isinstance(rl_api_manager, RlTrackerManager)

        server = HttpServer(
            host,
            rl_api_manager,
            config,
        )

        return cls(host, server, rl_api_manager)

    @classmethod
    def get_rl_api_manager(
        cls,
        config: Dict[str, Any],
        hosts: Dict[str, Any],
    ) -> RlTrackerManager:
        return RlTrackerManager(hosts)

    def start(self) -> None:
        asyncio.create_task(self._server.start())

    async def shutdown(self) -> None:
        await self._server.shutdown()
