"""The Storm Audio ISP MK2 integration."""
import telnetlib

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers import discovery
from homeassistant.helpers.entity import Entity

DOMAIN = "stormaudio"
DEFAULT_PORT = 23

CONF_ZONES = "zones"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_HOST): cv.string,
                vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
                vol.Required(CONF_ZONES): vol.All(cv.ensure_list, [cv.string]),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


def setup(hass, config):
    """Set up the Storm Audio ISP MK2 component."""

    host = config[DOMAIN][CONF_HOST]
    port = config[DOMAIN][CONF_PORT]
    zones = config[DOMAIN][CONF_ZONES]

    # Verify that we can connect to the ISP MK2 and get some data
    try:
        with telnetlib.Telnet(host, port) as tn:
            tn.write(b"?ZONES\r\n")
            result = tn.read_until(b"\n").decode().strip()
            if result != "ZONES={}".format(",".join(zones)):
                raise Exception("Zones do not match!")
    except Exception:
        return False

    # Add the entities for each zone
    for zone in zones:
        discovery.load_platform(
            hass,
            "sensor",
            DOMAIN,
            {"zone": zone, "host": host, "port": port},
            config,
        )

    return True


class StormAudioZone(Entity):
    """Representation of a Storm Audio zone."""

    def __init__(self, zone, host, port):
        """Initialize the zone."""
        self._name = f"Storm Audio Zone {zone}"
        self._state = None
        self._zone = zone
        self._host = host
        self._port = port

    @property
    def name(self):
        """Return the name of the zone."""
        return self._name

    @property
    def state(self):
        """Return the current state of the zone."""
        return self._state

    def update(self):
        """Get the latest data and updates the state."""
        with telnetlib.Telnet(self._host, self._port) as tn:
            tn.write(f"?{self._zone} STATUS\r\n".encode())
            result = tn.read_until(b"\n").decode().strip()
            self._state = result.split("=")[-1].strip()

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of the zone."""
        return None
