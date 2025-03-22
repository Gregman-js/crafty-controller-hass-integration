from homeassistant.components.sensor import SensorEntity, RestoreSensor
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .device_info_factory import create_device_info, create_minimal_device_info
from .const import DOMAIN, API_SERVER_ID, API_SERVER_NAME, CONF_PANEL_URL
import logging

_LOGGER = logging.getLogger(__name__)


class CraftyPlayersSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, server_id: str, server_name: str):
        super().__init__(coordinator)
        self.server_id = server_id
        self._attr_name = f"{server_name} Players Online"
        self._attr_icon = "mdi:account-multiple"
        self._attr_unique_id = f"{server_id}_players"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return create_minimal_device_info(self.server_id)

    @property
    def native_value(self):
        return self.coordinator.data.get("online", 0)


class CraftyPortSensor(CoordinatorEntity, RestoreSensor):
    def __init__(self, coordinator, server_id: str, server_name: str):
        super().__init__(coordinator)
        self.server_id = server_id
        self._attr_name = f"{server_name} Port"
        self._attr_icon = "mdi:ethernet"
        self._attr_unique_id = f"{server_id}_port"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return create_minimal_device_info(self.server_id)

    @property
    def native_value(self):
        return str(self.coordinator.data.get("server_port"))


class CraftyVersionSensor(CoordinatorEntity, RestoreSensor):
    def __init__(self, coordinator, server_id: str, server_name: str):
        super().__init__(coordinator)
        self.server_id = server_id
        self._attr_name = f"{server_name} Version"
        self._attr_icon = "mdi:ethernet"
        self._attr_unique_id = f"{server_id}_version"
        self._last_valid_value = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return create_minimal_device_info(self.server_id)

    @property
    def native_value(self):
        value = self.coordinator.data.get("version")
        if value not in (None, "", "False", False):
            self._last_valid_value = value

        return self._last_valid_value

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        last_sensor_data = await self.async_get_last_sensor_data()
        if last_sensor_data is not None:
            self._last_valid_value = last_sensor_data.native_value


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
            )
        )
        sensors.append(
            CraftyPortSensor(
                coordinator,
                server[API_SERVER_ID],
                server[API_SERVER_NAME],
            )
        )
        sensors.append(
            CraftyVersionSensor(
                coordinator,
                server[API_SERVER_ID],
                server[API_SERVER_NAME],
            )
        )
    async_add_entities(sensors)
