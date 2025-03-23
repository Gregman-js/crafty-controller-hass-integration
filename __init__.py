from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_BASE_URL, CONF_TOKEN, API_SERVER_ID
from .api import CraftyControllerAPI
from .coordinator import CraftyServerCoordinator


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
    await data["api"].close()
    return True
