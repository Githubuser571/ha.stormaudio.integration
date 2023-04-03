"""Support for StormAudio."""
import logging
import telnetlib

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_ZONE,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

CONF_VOLUME = "volume"

DEFAULT_NAME = "StormAudio"
DEFAULT_PORT = 23
DEFAULT_SCAN_INTERVAL = 10

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ZONE): cv.positive_int,
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): (
            vol.All(vol.Coerce(int), vol.Range(min=1))
        ),
        vol.Optional(CONF_VOLUME): cv.boolean,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the StormAudio platform."""
    zone = config.get(CONF_ZONE)
    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    port = config.get(CONF_PORT)
    scan_interval = config.get(CONF_SCAN_INTERVAL)
    volume_enabled = config.get(CONF_VOLUME)

    entities = []
    entities.append(StormAudioSensor(zone, host, name, port, scan_interval))
    if volume_enabled:
        entities.append(VolumeSensor(zone, host, name, port, scan_interval))
    add_entities(entities)


class StormAudioSensor(Entity):
    """Representation of a StormAudio Sensor."""

    def __init__(self, zone, host, name, port, scan_interval):
        """Initialize the sensor."""
        self._name = name
        self._state = None
        self._zone = zone
        self._host = host
        self._port = port
        self._scan_interval = scan_interval

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "dB"

    def telnet_command(self, command):
        """Send a command to the StormAudio via telnet."""
        try:
            tn = telnetlib.Telnet(self._host, self._port)
            tn.write(command.encode("ascii") + b"\r")
            response = tn.read_until(b"\r\n", timeout=1)
            tn.close()
            return response
        except ConnectionRefusedError:
            _LOGGER.warning("Connection refused to %s", self._host)
            return None

    def update(self):
        """Update the state of the sensor."""
        response = self.telnet_command("ZGET {} LEVEL".format(self._zone))
        if response is not None:
            response = response.decode("ascii").strip()
            try:
                self._state = int(response)
            except ValueError:
                _LOGGER.warning(
                    "Unable to parse response from StormAudio: %s", response
                )
        else:
            self._state = None


class VolumeSensor(StormAudioSensor):
    """Representation of a StormAudio Volume Sensor."""

    @property
    def name(self):
        """Return the name of the sensor."""
