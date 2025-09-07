import voluptuous as vol
from homeassistant import config_entries
from . import DOMAIN

DATA_SCHEMA = vol.Schema({
    vol.Required("name", default="Kapego Controller"): str,
    vol.Required("host", default="0.0.0.1"): str,
    vol.Required("port", default=8899): int,
})

class KapegoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """ Handle a config flow for a Kapego Controller """
    async def async_step_ip(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input['name'], data=user_input)

        return self.async_show_form(step_id='user', data_schema=DATA_SCHEMA)
