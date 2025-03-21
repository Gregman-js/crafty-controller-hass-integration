import logging
import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from .const import DOMAIN, SERVERS_ENDPOINT, CONF_BASE_URL, CONF_TOKEN

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_BASE_URL): str,
    vol.Required(CONF_TOKEN): str,
})


async def validate_input(hass, base_url, token):
    """Validate the user input allows us to connect to crafty."""
    url = f"{base_url.rstrip('/')}{SERVERS_ENDPOINT}"
    headers = {"Authorization": token}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=False) as response:
            if response.status != 200:
                raise Exception("Invalid response from crafty server")
            data = await response.json()
            if data.get("status") != "ok":
                raise Exception("Crafty returned error status")
    return data


class CraftyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Crafty integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            base_url = user_input[CONF_BASE_URL]
            token = user_input[CONF_TOKEN]
            try:
                # Validate input by calling the servers endpoint
                await validate_input(self.hass, base_url, token)
            except Exception as err:
                _LOGGER.error("Error validating crafty server: %s", err)
                errors["base"] = "cannot_connect"
            else:
                # If valid, create the entry
                return self.async_create_entry(title="Crafty Controller", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
