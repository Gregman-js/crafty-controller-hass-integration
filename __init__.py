from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from .const import DOMAIN, CONF_BASE_URL, CONF_TOKEN, API_SERVER_ID
from .api import CraftyControllerAPI
from .coordinator import CraftyServerCoordinator
from homeassistant.helpers.entity_registry import async_entries_for_device, async_get


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    api = CraftyControllerAPI(entry.data[CONF_BASE_URL], entry.data[CONF_TOKEN])
    servers = await api.get_servers()
    coordinators = {}
    for server in servers:
        coordinator = CraftyServerCoordinator(hass, api, server[API_SERVER_ID])
        await coordinator.async_config_entry_first_refresh()
        coordinators[server[API_SERVER_ID]] = coordinator

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinators": coordinators,
        "servers": servers,
    }

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "switch"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_unload_platforms(entry, ["sensor", "switch"])
    data = hass.data[DOMAIN].pop(entry.entry_id)
    for coordinator in data["coordinators"].values():
        await coordinator.api.close()
    return True


async def async_remove_config_entry_device(
    hass: HomeAssistant, config_entry: ConfigEntry, device: DeviceEntry
) -> bool:
    """Determine if a device can be removed from a config entry.

    Returns True if no entities associated with the device belong to the config entry.
    Otherwise, returns False to block removal.
    """
    entity_registry = async_get(hass)
    entries = async_entries_for_device(entity_registry, device.id)

    for entry in entries:
        if entry.config_entry_id == config_entry.entry_id:
            return False

    return True
