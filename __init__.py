import logging
from datetime import timedelta

import async_timeout
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import UPDATE_INTERVAL, CONF_BASE_URL, CONF_TOKEN, SERVERS_ENDPOINT
from .coordinator import CraftyDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up crafty from a config entry."""
    base_url = entry.data[CONF_BASE_URL]
    token = entry.data[CONF_TOKEN]

    coordinator = CraftyDataUpdateCoordinator(
        hass,
        base_url=base_url,
        token=token,
        update_interval=timedelta(seconds=UPDATE_INTERVAL),
    )

    # Perform the first update to fetch the list of servers
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault("crafty", {})[entry.entry_id] = coordinator

    # Forward setup to platforms (sensor and switch)
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "switch")
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload crafty config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    unload_ok &= await hass.config_entries.async_forward_entry_unload(entry, "switch")
    if unload_ok:
        hass.data["crafty"].pop(entry.entry_id)
    return unload_ok
