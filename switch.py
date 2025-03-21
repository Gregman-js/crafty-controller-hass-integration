import asyncio
import time

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, OPTIMISTIC_TIMEOUT

class CraftyServerSwitch(CoordinatorEntity, SwitchEntity):
    def __init__(self, coordinator, api, server_id, server_name):
        super().__init__(coordinator)
        self.api = api
        self.server_id = server_id
        self._attr_name = server_name
        self._attr_icon = "mdi:minecraft"
        self._attr_unique_id = f"{server_id}_switch"
        self._attr_device_info = {"identifiers": {(DOMAIN, server_id)}}
        self._optimistic_state = None

    @property
    def is_on(self):
        if self._optimistic_state is None:
            return self.coordinator.data.get("running", False)

        state, expires_at = self._optimistic_state
        if time.time() < expires_at:
            return state
        else:
            self._optimistic_state = None

    async def async_turn_on(self, **kwargs):
        await self.api.send_server_action(self.server_id, "start_server")
        self._set_optimistic_state(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.api.send_server_action(self.server_id, "stop_server")
        self._set_optimistic_state(False)
        await self.coordinator.async_request_refresh()

    def _set_optimistic_state(self, state: bool):
        self._optimistic_state = (state, time.time() + OPTIMISTIC_TIMEOUT)
        self.async_write_ha_state()

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    switches = []
    for server in data["servers"]:
        coordinator = data["coordinators"][server["server_id"]]
        switches.append(CraftyServerSwitch(
            coordinator, data["api"], server["server_id"], server["server_name"]
        ))
    async_add_entities(switches)