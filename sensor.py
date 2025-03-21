import logging
from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors for each crafty server."""
    coordinator = hass.data["crafty"][entry.entry_id]
    servers_data = coordinator.data.get("data", [])
    sensors = []

    for server in servers_data:
        server_id = server["server_id"]
        server_name = server["server_name"]

        sensors.append(CraftyRunningSensor(coordinator, server_id, server_name))
        sensors.append(CraftyPlayersSensor(coordinator, server_id, server_name))

    async_add_entities(sensors, update_before_add=True)


class CraftyRunningSensor(SensorEntity):
    """Sensor to show if the server is running."""

    def __init__(self, coordinator, server_id, server_name):
        self.coordinator = coordinator
        self.server_id = server_id
        self._attr_name = f"{server_name} Is Running"
        self._attr_unique_id = f"{server_id}_running"
        self.server_name = server_name

    @property
    def state(self):
        stats = self.coordinator.hass.loop.run_until_complete(
            self.coordinator.fetch_server_stats(self.server_id)
        )
        if stats and "data" in stats:
            return stats["data"].get("running", False)
        return False

    @property
    def extra_state_attributes(self):
        return {"server_id": self.server_id}


class CraftyPlayersSensor(SensorEntity):
    """Sensor to show the number of players online."""

    def __init__(self, coordinator, server_id, server_name):
        self.coordinator = coordinator
        self.server_id = server_id
        self._attr_name = f"{server_name} Players Online"
        self._attr_unique_id = f"{server_id}_players"
        self.server_name = server_name

    @property
    def state(self):
        stats = self.coordinator.hass.loop.run_until_complete(
            self.coordinator.fetch_server_stats(self.server_id)
        )
        if stats and "data" in stats:
            return stats["data"].get("online", 0)
        return 0

    @property
    def extra_state_attributes(self):
        return {"server_id": self.server_id}
