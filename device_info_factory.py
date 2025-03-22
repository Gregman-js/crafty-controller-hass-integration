from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN


def create_device_info(server_id: str, server_name: str) -> DeviceInfo:
    """Factory function to create device info for a Crafty server."""
    return DeviceInfo(
        identifiers={(DOMAIN, server_id)},
        name=f"{server_name}",
        manufacturer="Crafty",
        model=server_name,
        model_id=server_id,
        serial_number=server_id,
    )
