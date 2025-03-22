from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from datetime import timedelta
import logging
from .const import UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class CraftyServerCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api, server_id):
        super().__init__(
            hass,
            logger=_LOGGER,
            name=f"Crafty Server {server_id}",
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.api = api
        self.server_id = server_id

    async def _async_update_data(self):
        return await self.api.get_server_stats(self.server_id)
