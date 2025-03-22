from time import time
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .device_info_factory import create_device_info
from .const import (
    DOMAIN,
    OPTIMISTIC_TIMEOUT,
    API_SERVER_ID,
    API_SERVER_NAME,
    CONF_PANEL_URL,
)


class CraftyServerSwitch(CoordinatorEntity, SwitchEntity):
    def __init__(
        self, coordinator, api, server_id: str, server_name: str, panel_url: str
    ):
        super().__init__(coordinator)
        self.api = api
        self.server_id = server_id
        self.server_name = server_name
        self.panel_url = panel_url
        self._attr_name = server_name
        self._attr_icon = "mdi:minecraft"
        self._attr_unique_id = f"{server_id}_switch"
        self._attr_device_info = {"identifiers": {(DOMAIN, server_id)}}
        self._optimistic_state = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return create_device_info(self.server_id, self.server_name, self.panel_url)

    @property
    def is_on(self) -> bool:
        if self._optimistic_state is not None:
            state, expires_at = self._optimistic_state
            if time() < expires_at:
                return state
            else:
                self._optimistic_state = None

        return self.coordinator.data.get("running", False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.api.send_server_action(self.server_id, "start_server")
        self._set_optimistic_state(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.api.send_server_action(self.server_id, "stop_server")
        self._set_optimistic_state(False)
        await self.coordinator.async_request_refresh()

    def _set_optimistic_state(self, state: bool) -> None:
        self._optimistic_state = (state, time() + OPTIMISTIC_TIMEOUT)
        self.async_write_ha_state()


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    switches = []
    for server in data["servers"]:
        coordinator = data["coordinators"][server[API_SERVER_ID]]
        switches.append(
            CraftyServerSwitch(
                coordinator,
                data["api"],
                server[API_SERVER_ID],
                server[API_SERVER_NAME],
                entry.data[CONF_PANEL_URL],
            )
        )
    async_add_entities(switches)
