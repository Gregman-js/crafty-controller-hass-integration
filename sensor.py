from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .device_info_factory import create_device_info
from .const import DOMAIN, API_SERVER_ID, API_SERVER_NAME
import logging

_LOGGER = logging.getLogger(__name__)


class CraftyPlayersSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, server_id, server_name):
        super().__init__(coordinator)
        self.server_id = server_id
        self.server_name = server_name
        self._attr_name = f"{server_name} Players Online"
        self._attr_icon = "mdi:account-multiple"
        self._attr_unique_id = f"{server_id}_players"
        self._attr_native_unit_of_measurement = "players"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return create_device_info(self.server_id, self.server_name)

    @property
    def native_value(self):
        return self.coordinator.data.get("online", 0)


async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    sensors = []
    for server in data["servers"]:
        coordinator = data["coordinators"][server[API_SERVER_ID]]
        sensors.append(
            CraftyPlayersSensor(
                coordinator, server[API_SERVER_ID], server[API_SERVER_NAME]
            )
        )
    async_add_entities(sensors)
