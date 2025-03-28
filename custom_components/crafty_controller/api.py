import aiohttp
import logging

from .types import CraftyServerStats
from .const import (
    API_DATA,
    API_STATUS,
    API_STATUS_OK,
    PATH_API_BASE,
    PATH_SERVERS,
    PATH_STATS,
    PATH_ACTION,
)

_LOGGER = logging.getLogger(__name__)


class CraftyControllerAPI:
    def __init__(self, api_url: str, auth_token: str):
        self.session = aiohttp.ClientSession(
            base_url=f"{api_url}{PATH_API_BASE}",
            headers={"Authorization": auth_token},
            connector=aiohttp.TCPConnector(ssl=False),
        )

    async def get_servers(self):
        async with self.session.get(PATH_SERVERS) as response:
            response.raise_for_status()
            data = await response.json()
            return data[API_DATA] if data[API_STATUS] == API_STATUS_OK else []

    async def get_server_stats(self, server_id: str) -> CraftyServerStats:
        async with self.session.get(PATH_STATS.format(server_id)) as response:
            response.raise_for_status()
            data = await response.json()
            if data[API_STATUS] != API_STATUS_OK:
                raise Exception("Crafty controller returned error status")

            return CraftyServerStats.from_dict(data[API_DATA])

    async def send_server_action(self, server_id: str, action: str):
        async with self.session.post(PATH_ACTION.format(server_id, action)) as response:
            response.raise_for_status()

    async def close(self):
        await self.session.close()

    async def validateController(self):
        async with self.session.get("") as response:
            if response.status != 200:
                raise Exception("Invalid response from crafty controller")
            data = await response.json()
            if data.get(API_STATUS) != API_STATUS_OK:
                raise Exception("Crafty controller returned error status")
