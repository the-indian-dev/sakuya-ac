"""This plugin will flash the lights/fog colour whenever a flight status update
is sent
It can be enabled here by changing the value of ENABLED to True."""
from lib.PacketManager.packets import FSNETCMD_SKYCOLOR, FSNETCMD_FOGCOLOR
from random import randint
ENABLED = False

class Plugin:
    def __init__(self):
        self.plugin_manager = None

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugin_manager.register_hook('on_flight_data', self.on_receive)

    def on_receive(self, data, player, messages_to_client, *args):
        if ENABLED:
            sky_colour_packet = FSNETCMD_SKYCOLOR.encode(randint(0, 255), randint(0, 255), randint(0, 255), True)
            fog_colour_packet = FSNETCMD_FOGCOLOR.encode(randint(0, 255), randint(0, 255), randint(0, 255), True)
            messages_to_client.append(sky_colour_packet)
            messages_to_client.append(fog_colour_packet)
        return True
