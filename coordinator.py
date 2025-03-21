import logging
import aiohttp
import async_timeout
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import SERVERS_ENDPOINT, STATS_ENDPOINT, CONF_BASE_URL, CONF_TOKEN

_LOGGER = logging.getLogger(__name__)


class CraftyDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Crafty controller."""

    def __init__(self, hass, base_url, token, update_interval: timedelta):
        """Initialize."""
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.session = aiohttp.ClientSession()
        super().__init__(hass, _LOGGER, name="crafty", update_interval=update_interval)

    async def _async_update_data(self):
        """Fetch data from crafty."""
        url = f"{self.base_url}{SERVERS_ENDPOINT}"
        headers = {"Authorization": self.token}
        try:
            async with async_timeout.timeout(10):
                async with self.session.get(url, headers=headers, ssl=False) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error fetching servers: {response.status}")
                    data = await response.json()
                    return data
        except Exception as err:
            raise UpdateFailed(err)

    async def fetch_server_stats(self, server_id: str):
        """Fetch stats for a given server."""
        url = f"{self.base_url}{STATS_ENDPOINT.format(server_id=server_id)}"
        headers = {"Authorization": self.token}
        try:
            async with async_timeout.timeout(10):
                async with self.session.get(url, headers=headers, ssl=False) as response:
                    if response.status != 200:
                        _LOGGER.error("Error fetching stats for server %s: %s", server_id, response.status)
                        return None
                    return await response.json()
        except Exception as err:
            _LOGGER.error("Exception fetching stats for server %s: %s", server_id, err)
            return None
