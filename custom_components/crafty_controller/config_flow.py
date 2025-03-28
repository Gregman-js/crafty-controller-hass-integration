import logging
import voluptuous as vol
from .api import CraftyControllerAPI
from homeassistant.config_entries import ConfigFlow

from .const import DOMAIN, CONF_API_URL, CONF_TOKEN, CONF_PANEL_URL

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_URL): str,
        vol.Required(CONF_PANEL_URL): str,
        vol.Required(CONF_TOKEN): str,
    }
)


class CraftyConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Crafty Controller integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            config = {
                CONF_API_URL: user_input[CONF_API_URL].rstrip("/"),
                CONF_PANEL_URL: user_input[CONF_PANEL_URL].rstrip("/"),
                CONF_TOKEN: user_input[CONF_TOKEN],
            }
            api = CraftyControllerAPI(config[CONF_API_URL], config[CONF_TOKEN])
            try:
                await api.validateController()
            except Exception as err:
                _LOGGER.error("Error validating crafty server: %s", err)
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title="Crafty Controller", data=config)
            finally:
                await api.close()

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
