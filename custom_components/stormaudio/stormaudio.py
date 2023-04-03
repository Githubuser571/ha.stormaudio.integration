import requests
from homeassistant.components.switch import SwitchEntity

DOMAIN = "stormaudio"
SERVICE_STORMAUDIO = "stormaudio"

def set_power(power_state):
    ip_address = "192.168.42.10"
    power_endpoint = f"http://{ip_address}/api/power"
    payload = {"state": power_state}
    response = requests.post(power_endpoint, json=payload)
    response.raise_for_status()

def set_volume(volume_level):
    ip_address = "192.168.42.10"
    volume_endpoint = f"http://{ip_address}/api/volume"
    payload = {"level": volume_level}
    response = requests.post(volume_endpoint, json=payload)
    response.raise_for_status()

def set_stormaudio_state(state):
    if state == "on":
        set_power("on")
        set_volume(50)  # Set default volume to 50%
    elif state == "off":
        set_power("off")

class StormAudioSwitch(SwitchEntity):
    def __init__(self):
        self._state = False

    @property
    def name(self):
        return "Storm Audio"

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        self._state = True

    def turn_off(self, **kwargs):
        self._state = False

def setup_platform(hass, config, add_entities, discovery_info=None):
    def stormaudio_service(call):
        set_stormaudio_state(call.data["state"])

    hass.services.register("switch", SERVICE_STORMAUDIO, stormaudio_service)

    add_entities([StormAudioSwitch()])

setup_platform(None, None, print)  # Test the setup function
