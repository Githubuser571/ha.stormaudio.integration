import logging

from homeassistant.components.switch import SwitchEntity

from .const import (
    ATTR_POWER,
    DOMAIN,
    DEFAULT_ZONE,
    DEFAULT_NAME,
    DEFAULT_ICON,
    ATTR_STATUS,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add switch entities for power state"""
    stormaudio = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([StormAudioPowerSwitch(stormaudio, config_entry)])

class StormAudioPowerSwitch(SwitchEntity):
    """Representation of a Storm Audio power switch."""

    def __init__(self, stormaudio, config_entry):
        self._stormaudio = stormaudio
        self._config_entry = config_entry
        self._name = f"{DEFAULT_NAME} Power"
        self._icon = DEFAULT_ICON
        self._state = False
        self._unique_id = f"{config_entry.entry_id}_power"

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return the state of the switch."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the switch."""
        return self._icon

    @property
    def unique_id(self):
        """Return the unique id of the switch."""
        return self._unique_id

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        if await self._stormaudio.async_power_on():
            self._state = True
            self.async_schedule_update_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        if await self._stormaudio.async_power_off():
            self._state = False
            self.async_schedule_update_ha_state()

    async def async_update(self):
        """Update the state of the switch."""
        self._state = await self._stormaudio.async_is_power_on()
        _LOGGER.debug("Updated power switch state to %s", self._state)
