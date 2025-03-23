"""Base entity for the Minecraft Server integration."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .types import CraftyServerStats
from .const import DOMAIN, PANEL_SERVER_DETAILS
from .coordinator import CraftyServerCoordinator

MANUFACTURER = "Mojang Studios"


class MinecraftServerEntity(CoordinatorEntity[CraftyServerCoordinator]):
    """Representation of a Minecraft Server base entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CraftyServerCoordinator,
        server_id: str,
        server_name: str,
        panel_url: str,
    ) -> None:
        """Initialize base entity."""
        super().__init__(coordinator)

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, server_id)},
            configuration_url=f"{panel_url}{PANEL_SERVER_DETAILS.format(server_id)}",
            name=f"{server_name}",
            manufacturer="Crafty Controller",
            model=server_name,
            serial_number=server_id,
        )

    def getData(self) -> CraftyServerStats:
        """Return the entity data."""
        return self.coordinator.data
