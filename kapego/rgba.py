""" RGBA Controller Class
    =====================

    Identifier for HW:
    ------------------

    MAC Adress starts with 98:D8:63:XX:XX:XX

    Identified Interface:
    ---------------------

    UDP to port 8899

    Identified Commands: 
        identification method <SNOOP>
        -----------------------------

        - ON:   send 'B ' # ! space afterwards is important? 
        - OFF:  send 'A '

    Identified Assumptions:
        2 bytes. always.

        Bytemasks used for everything?
        thus would result in 
        1010    A
        1011    B
"""
import socket
from homeassistant.components.controller import ControllerEntity
from . import DOMAIN

# Command Reference
COMMANDS={
    "ON":  "B ",
    "OFF": "A ",
}

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([KapegoRGBA()])

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([KapegoRGBA(**entry.data)])


class KapegoRGBA(ControllerEntity):
    """ RGBA Controller """

    def __init__(self, **kwargs):
        self._attr_name = kwargs["name"]
        _idn = kwargs["name"].lower().replace(' ', '_')
        _idi = kwargs["host"].replace('.', '_')
        self._attr_unique_id = f"rgba_controller{_idn}{_idi}"

        self._host = kwargs["host"]
        self._port = kwargs["port"]


    async def async_turn_on(self, **kwargs):
        """ Send the "on"-Signal """
        self._is_on = True
        await self._send("ON")
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """ Send the "off"-Signal """
        self._is_on = False
        await self._send("OFF")
        self.async_write_ha_state()

    async def _send(self, message: str):
        """ Send out a UDP Telegram using COMMANDS
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            payload = COMMANDS[message].encode('utf-8')
            sock.sendto(payload, (self._host, self._ip))
        finally:
            sock.close()
