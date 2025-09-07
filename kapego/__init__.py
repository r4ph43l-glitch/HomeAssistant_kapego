""" Integration for Kapego Light Controllers """

from homeassistant.core import HomeAssistant

DOMAIN = "kapego"

async def async_setup(hass: HomeAssistant, config: dict):
    """ Set up from configuration.yaml (not used if config_flow is present)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """ Setup from UI config entry """
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "controller")
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """ Unload a config entry. """
    unload_ok = await
    hass.config_entries.async_forward_entry_unload(entry, "controller")

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok