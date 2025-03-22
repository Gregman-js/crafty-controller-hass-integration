from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN, PANEL_SERVER_DETAILS


def create_device_info(server_id: str, server_name: str, panel_url: str) -> DeviceInfo:
    """Factory function to create device info for a Crafty server."""
    return DeviceInfo(
        identifiers={(DOMAIN, server_id)},
        configuration_url=f"{panel_url}{PANEL_SERVER_DETAILS.format(server_id)}",
        name=f"{server_name}",
        manufacturer="Crafty Controller",
        model=server_name,
        serial_number=server_id,
    )


def create_minimal_device_info(server_id: str) -> DeviceInfo:
    """Factory function to create minimal device info for a Crafty server."""
    return DeviceInfo(
        identifiers={(DOMAIN, server_id)},
    )
