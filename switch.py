from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN


class CraftyServerSwitch(SwitchEntity):
    def __init__(self, coordinator, api, server_id, server_name):
        self.coordinator = coordinator
        self.api = api
        self.server_id = server_id
        self._attr_name = server_name
        self._attr_unique_id = f"{server_id}_switch"
        self._attr_device_info = {"identifiers": {(DOMAIN, server_id)}}

    @property
    def is_on(self):
        return self.coordinator.data.get("running", False)

    async def async_turn_on(self, **kwargs):
        await self.api.send_server_action(self.server_id, "start_server")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.api.send_server_action(self.server_id, "stop_server")
        await self.coordinator.async_request_refresh()

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    switches = []
    for server in data["servers"]:
        coordinator = data["coordinators"][server["server_id"]]
        switches.append(CraftyServerSwitch(
            coordinator, data["api"], server["server_id"], server["server_name"]
        ))
    async_add_entities(switches)