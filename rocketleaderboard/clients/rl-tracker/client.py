
import logging
from typing import Any, Dict
from playwright.async_api import async_playwright
from rocketleaderboard.clients.client import RlClient

BASE_URL = '/api/v2'
PLAYER_URL = '/rocket-league/standard/profile/steam/%s'
PLAYLIST_URL = PLAYER_URL + '/segments/playlist?season=%s'
SESSIONS_URL = PLAYER_URL + '/sessions'


log = logging.getLogger('clients.rl-tracker.client')


class RlTrackerClient(RlClient):

    def __init__(
        self,
        hosts: Dict[str, Any],
    ):
        self._host = hosts['host']

    def start(self):
        pass

    async def stop(self):
        pass

    def target(self, path) -> str:
        return f'{BASE_URL}' + f'{path}'

    async def _handle_response(self, response) -> Dict[str, Any]:
        data = {}
        try:
            data = await response.json()
        except Exception as e:
            log.error(f'RL Tracker request error. Error [{e}]')
        finally:
            return data

    async def make_req(self, url: str):

        p = await async_playwright().start()

        browser = await p.chromium.launch(args=['--no-sandbox'])
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/83.0.4103.116 Safari/537.36"
        )

        await page.set_extra_http_headers({"Accept-Language": "en"})
        response = await page.goto(
            'https://' + self.host + url,
            wait_until="networkidle",
        )
        _response = await self._handle_response(response)
        await browser.close()
        return _response.get('data', {})

    async def get_player(self, id: str):
        target = self.target(PLAYER_URL % id)
        return await self.make_tracker_req(target)

    async def get_playlist(self, id: str, season: int):
        pass

    async def get_sessions(self, id: str):
        pass
