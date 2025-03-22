import logging
import voluptuous as vol
from .api import CraftyControllerAPI
from homeassistant.config_entries import ConfigFlow

from .const import DOMAIN, CONF_BASE_URL, CONF_TOKEN, CONF_PANEL_URL

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_BASE_URL): str,
        vol.Required(CONF_PANEL_URL): str,
        vol.Required(CONF_TOKEN): str,
    }
)


class CraftyConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Crafty integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            config = {
                CONF_BASE_URL: user_input[CONF_BASE_URL].rstrip("/"),
                CONF_PANEL_URL: user_input[CONF_PANEL_URL].rstrip("/"),
                CONF_TOKEN: user_input[CONF_TOKEN],
            }
            try:
                await CraftyControllerAPI(
                    config[CONF_BASE_URL], config[CONF_TOKEN]
                ).validateController()
            except Exception as err:
                _LOGGER.error("Error validating crafty server: %s", err)
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title="Crafty Controller", data=config)

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
