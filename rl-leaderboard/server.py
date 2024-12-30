import subprocess
import asyncio
import logging
from aiohttp import web
from aiohttp_cache import setup_cache, cache
import aiohttp_cors
import subprocess
import json

log = logging.getLogger('server')


class RlLeaderboardApiHandler(object):
    loop = asyncio.get_event_loop()

    @cache(expires=300)
    async def handle_get_player(self, request):
        id = request.rel_url.query.get('id')
        cmd = "node server/puppetGet.js ---url=https://api.tracker.gg/api/v2/rocket-league/standard/profile/steam/%s" % id
        process = await self.loop.run_in_executor(
            None,
            lambda: subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
        )
        stdout, stderr = process.communicate()
        if stderr:
            raise web.HTTPInternalServerError(reason=str(stderr))
        return web.json_response(json.loads(stdout), status=200)

    @cache(expires=300)
    async def handle_get_playlist(self, request):
        id = request.rel_url.query.get('id')
        season = request.rel_url.query.get('season')
        cmd = "node server/puppetGet.js --url=https://api.tracker.gg/api/v2/rocket-league/standard/profile/steam/%s/segments/playlist?season=%s" % (
            id, season)
        process = await self.loop.run_in_executor(
            None,
            lambda: subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
        )
        stdout, stderr = process.communicate()
        if stderr:
            raise web.HTTPInternalServerError(reason=str(stderr))
        return web.json_response(json.loads(stdout), status=200)

    @cache(expires=300)
    async def handle_get_sessions(self, request):
        id = request.rel_url.query.get('id')
        cmd = "node server/puppetGet.js --url=https://api.tracker.gg/api/v2/rocket-league/standard/profile/steam/%s/sessions" % id
        process = await self.loop.run_in_executor(
            None,
            lambda: subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
        )
        stdout, stderr = process.communicate()
        if stderr:
            raise web.HTTPInternalServerError(reason=str(stderr))
        return web.json_response(json.loads(stdout), status=200)


app = web.Application()

handler = RlLeaderboardApiHandler()
setup_cache(app)

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*"
    )}
)

cors.add(
    app.router.add_route(
        'GET',
        '/player',
        handler.handle_get_player
    )
)

cors.add(
    app.router.add_route(
        'GET',
        '/playlist',
        handler.handle_get_playlist
    )
)

cors.add(
    app.router.add_route(
        'GET',
        '/sessions',
        handler.handle_get_sessions
    )
)


async def start_server(
    app: web.Application,
    host: str = '127.0.0.1',
    port: int = 8080,
):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()

    log.info("======= Serving on %s:%s ======" % (host, port))

    while True:
        await asyncio.sleep(3600)  # sleep forever
