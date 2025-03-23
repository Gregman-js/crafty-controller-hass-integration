from typing_extensions import TypeVar

from homeassistant.components.sensor import SensorEntity, RestoreSensor
from homeassistant.core import callback

from .entity import MinecraftServerEntity
from .const import DOMAIN, API_SERVER_ID, API_SERVER_NAME, CONF_PANEL_URL
import logging
from .coordinator import CraftyServerCoordinator

_LOGGER = logging.getLogger(__name__)


class CraftyPlayersSensor(MinecraftServerEntity, SensorEntity):
    _attr_should_poll = False
    _attr_name = "Players Online"
    _attr_icon = "mdi:account-multiple"

    def __init__(
        self,
        coordinator: CraftyServerCoordinator,
        server_id: str,
        server_name: str,
        panel_url: str,
    ):
        super().__init__(coordinator, server_id, server_name, panel_url)
        self._attr_unique_id = f"{server_id}_players"
        self._update_data()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_data(True)

    def _update_data(self, write=False):
        self._attr_native_value = self.getData().online
        if write:
            self.async_write_ha_state()


class CraftyPortSensor(MinecraftServerEntity, RestoreSensor):
    _attr_should_poll = False
    _attr_name = "Port"
    _attr_icon = "mdi:ethernet"

    def __init__(
        self,
        coordinator: CraftyServerCoordinator,
        server_id: str,
        server_name: str,
        panel_url: str,
    ):
        super().__init__(coordinator, server_id, server_name, panel_url)
        self._attr_unique_id = f"{server_id}_port"
        self._update_data()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_data(True)

    def _update_data(self, write=False):
        self._attr_native_value = str(self.getData().server_port)
        if write:
            self.async_write_ha_state()


class CraftyVersionSensor(MinecraftServerEntity, RestoreSensor):
    _attr_should_poll = False
    _attr_name = "Version"
    _attr_icon = "mdi:ethernet"

    def __init__(
        self,
        coordinator: CraftyServerCoordinator,
        server_id: str,
        server_name: str,
        panel_url: str,
    ):
        super().__init__(coordinator, server_id, server_name, panel_url)
        self._attr_unique_id = f"{server_id}_version"
        self._update_data()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_data(True)

    def _update_data(self, write=False) -> None:
        value = self.getData().version
        if value not in (None, "", "False", False):
            self._attr_native_value = value
            if write:
                self.async_write_ha_state()

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        last_sensor_data = await self.async_get_last_sensor_data()
        if last_sensor_data is not None:
            self._attr_native_value = last_sensor_data.native_value

        self._update_data(True)


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    sensors = []
    for server in data["servers"]:
        coordinator = data["coordinators"][server[API_SERVER_ID]]
        sensors.append(
            CraftyPlayersSensor(
                coordinator,
                server[API_SERVER_ID],
                server[API_SERVER_NAME],
                entry.data[CONF_PANEL_URL],
            )
        )
        sensors.append(
            CraftyPortSensor(
                coordinator,
                server[API_SERVER_ID],
                server[API_SERVER_NAME],
                entry.data[CONF_PANEL_URL],
            )
        )
        sensors.append(
            CraftyVersionSensor(
                coordinator,
                server[API_SERVER_ID],
                server[API_SERVER_NAME],
                entry.data[CONF_PANEL_URL],
            )
        )
    async_add_entities(sensors)
