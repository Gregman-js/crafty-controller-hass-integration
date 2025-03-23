import logging
from time import time
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import callback
from homeassistant.helpers.restore_state import RestoreEntity

from .entity import MinecraftServerEntity
from .const import (
    DOMAIN,
    OPTIMISTIC_TIMEOUT,
    API_SERVER_ID,
    API_SERVER_NAME,
    CONF_PANEL_URL,
)
from .coordinator import CraftyServerCoordinator

_LOGGER = logging.getLogger(__name__)


class CraftyServerSwitch(MinecraftServerEntity, RestoreEntity, SwitchEntity):
    _attr_icon = "mdi:minecraft"
    _attr_name = None

    def __init__(
        self,
        coordinator: CraftyServerCoordinator,
        server_id: str,
        server_name: str,
        panel_url: str,
    ):
        super().__init__(coordinator, server_id, server_name, panel_url)
        self.server_id = server_id
        self._attr_unique_id = f"{server_id}_switch"
        self._optimistic_state = None
        self._update_data()

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state is not None:
            self._attr_is_on = last_state.state == "on"
            if last_state.attributes:
                self._attr_entity_picture = last_state.attributes.get("entity_picture")

        self._update_data(True)

    def _update_data(self, write=False):
        if self._optimistic_state is not None:
            state, expires_at = self._optimistic_state
            if time() < expires_at:
                return
            else:
                self._optimistic_state = None

        self._attr_is_on = self.getData().running
        if write:
            self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        base64_icon = self.getData().icon
        if base64_icon:
            self._attr_entity_picture = f"data:image/png;base64,{base64_icon}"

        self._update_data(True)

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.coordinator.api.send_server_action(self.server_id, "start_server")
        self._set_optimistic_state(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.coordinator.api.send_server_action(self.server_id, "stop_server")
        self._set_optimistic_state(False)
        await self.coordinator.async_request_refresh()

    def _set_optimistic_state(self, state: bool) -> None:
        self._optimistic_state = (state, time() + OPTIMISTIC_TIMEOUT)
        self._attr_is_on = state
        self.async_write_ha_state()


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    switches = []
    for server in data["servers"]:
        coordinator = data["coordinators"][server[API_SERVER_ID]]
        switches.append(
            CraftyServerSwitch(
                coordinator,
                server[API_SERVER_ID],
                server[API_SERVER_NAME],
                entry.data[CONF_PANEL_URL],
            )
        )
    async_add_entities(switches)
