from typing import Any, Dict, Optional
from aiohttp import web
from strawberry.schema.config import StrawberryConfig
from rocketleaderboard.gql.query import Query
from rocketleaderboard.managers.rltracker import RlTrackerManager
from rocketleaderboard.middleware import get_middlewares
from rocketleaderboard.typedefs import T_CONTEXT, T_CONTROL_ADDRESS
from strawberry.aiohttp.views import GraphQLView
import strawberry
import asyncio
import logging

log = logging.getLogger('server.server')


class GraphQLViewHandler():

    def __init__(
        self,
        rl_api_manager: RlTrackerManager,
        config: Dict[str, Any] = {}
    ) -> None:
        self._rl_api_manager = rl_api_manager
        self._config = config
        self._supported_versions = ['1.0']
        self._schema = strawberry.Schema(
            query=Query,
            config=StrawberryConfig()
        )

    async def _get_context(
        self,
        request: web.Request,
        response: web.StreamResponse,
    ) -> T_CONTEXT:
        return {
            'request': request,
            'response': response,
            'config': self._config,
            'rl_api_manager': self._rl_api_manager

        }

    async def handle_graphql(
        self,
        request: web.Request,
    ) -> web.StreamResponse:
        html_list = ''.join(
            [
                f'<li><a href="/graphql/v{v}">{v}</a></li>'
                for v in self._supported_versions
            ],
        )
        html_output = f'<ul>{html_list}</ul>'
        return web.Response(
            text=html_output,
            content_type='text/html',
        )

    async def handle_graphql_v1(
        self,
        request: web.Request
    ) -> web.StreamResponse:
        view = GraphQLView(
            schema=self._schema,
            allow_queries_via_get=False,
            graphql_ide=None
        )
        view.get_context = self._get_context
        return await view(request)


class HttpServer():
    def __init__(
        self,
        host_address: T_CONTROL_ADDRESS,
        rl_api_manager: RlTrackerManager,
        config: Dict[str, Any] = {},
    ) -> None:
        self._host_address = host_address
        self.server: Optional[web.Application] = None
        self._config = config
        self._rl_api_manager = rl_api_manager

    @property
    def host_address(self):
        return self._host_address

    async def start(self) -> None:
        # start aiohttp server
        handler = GraphQLViewHandler(
            self._rl_api_manager,
            config=self._config
        )
        app = web.Application(middlewares=get_middlewares())

        app.add_routes(
            [
                web.view('/graphql', handler.handle_graphql),
                web.view('/graphql/v1.0', handler.handle_graphql_v1),
            ]
        )
        host = self.host_address['host']
        port = self.host_address['port']
        loop = asyncio.get_event_loop()
        loop.create_task(
            web._run_app(app, host=host, port=port, access_log=None)
        )
        self.server = app

    async def shutdown(self) -> None:
        log.info('Shutdown on HTTP server requested.')
        if self.server is not None:
            await self.server.shutdown()
            await self.server.cleanup()
        log.info('Shutdown on HTTP server complete.')
