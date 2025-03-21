from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

class CraftyRunningSensor(SensorEntity):
    def __init__(self, coordinator, server_id, server_name):
        self.coordinator = coordinator
        self.server_id = server_id
        self._attr_name = f"{server_name} Is Running"
        self._attr_unique_id = f"{server_id}_running"
        self._attr_device_info = {"identifiers": {(DOMAIN, server_id)}}

    @property
    def native_value(self):
        return "Running" if self.coordinator.data.get("running") else "Stopped"

class CraftyPlayersSensor(SensorEntity):
    def __init__(self, coordinator, server_id, server_name):
        self.coordinator = coordinator
        self.server_id = server_id
        self._attr_name = f"{server_name} Players Online"
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
        sensors.append(CraftyRunningSensor(coordinator, server["server_id"], server["server_name"]))
        sensors.append(CraftyPlayersSensor(coordinator, server["server_id"], server["server_name"]))
    async_add_entities(sensors)