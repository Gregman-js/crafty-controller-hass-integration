import logging
import aiohttp
import async_timeout

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN, ACTION_ENDPOINT, CONF_TOKEN, CONF_BASE_URL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up switches for each crafty server."""
    coordinator = hass.data["crafty"][entry.entry_id]
    servers_data = coordinator.data.get("data", [])
    switches = []

    for server in servers_data:
        server_id = server["server_id"]
        server_name = server["server_name"]

        switches.append(CraftyServerSwitch(hass, coordinator, server_id, server_name, entry.data))
    async_add_entities(switches, update_before_add=True)


class CraftyServerSwitch(SwitchEntity):
    """Switch to start/stop a crafty server."""

    def __init__(self, hass, coordinator, server_id, server_name, config):
        self.hass = hass
        self.coordinator = coordinator
        self.server_id = server_id
        self.server_name = server_name
        self.config = config
        self._attr_name = server_name
        self._attr_unique_id = f"{server_id}_switch"
        self._is_on = False  # local state

    @property
    def is_on(self):
        """Return true if the server is running."""
        stats = self.hass.loop.run_until_complete(
            self.coordinator.fetch_server_stats(self.server_id)
        )
        if stats and "data" in stats:
            self._is_on = stats["data"].get("running", False)
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn the server on."""
        await self._send_action("start_server")
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the server off."""
        await self._send_action("stop_server")
        self._is_on = False
        self.async_write_ha_state()

    async def _send_action(self, action: str):
        """Send a POST request to change server state."""
        base_url = self.config[CONF_BASE_URL].rstrip("/")
        token = self.config[CONF_TOKEN]
        url = ACTION_ENDPOINT.format(server_id=self.server_id, action=action)
        headers = {"Authorization": token}
        async with aiohttp.ClientSession() as session:
            try:
                async with async_timeout.timeout(10):
                    async with session.post(url, headers=headers, ssl=False) as response:
                        if response.status != 200:
                            _LOGGER.error("Error sending %s action to server %s: %s", action, self.server_id, response.status)
            except Exception as err:
                _LOGGER.error("Exception when sending %s action to server %s: %s", action, self.server_id, err)
