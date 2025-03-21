from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

class CraftyPlayersSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, server_id, server_name):
        super().__init__(coordinator)
        self.server_id = server_id
        self._attr_name = f"{server_name} Players Online"
        self._attr_icon = "mdi:account-multiple"
        self._attr_unique_id = f"{server_id}_players"
        self._attr_native_unit_of_measurement = "players"
        self._attr_device_info = {"identifiers": {(DOMAIN, server_id)}}

    @property
    def native_value(self):
        return self.coordinator.data.get("online", 0)

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    sensors = []
    for server in data["servers"]:
        coordinator = data["coordinators"][server["server_id"]]
        sensors.append(CraftyPlayersSensor(coordinator, server["server_id"], server["server_name"]))
    async_add_entities(sensors)