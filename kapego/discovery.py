""" What do we know about the discovery?

    Port 80 is open
        PORT   STATE         SERVICE VERSION
        80/tcp open          http    LimitlessLED smart lightbulb bridge httpd
    Port 8899 is used for data
"""
import asyncio, socket
from . import DOMAIN

DATAPORT=48899

async def discover_devices(hass):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(2)
    sock.sendto(b"DISCOVER", ("255.255.255.255", DATAPORT))

    try:
        while True:
            data, adr = sock.recvfrom(1024)
            device_info = data.decode()

            # Discovery flow
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    DOMAIN,
                    context={"source": "discovery"},
                    data={"host": adr[0], "info": device_info}
                )
            )
    except socket.timeout:
        pass
    finally:
        sock.close()
