"""This plugin will set the weather based on a chat message.
"""
from lib.PacketManager.packets import FSNETCMD_SKYCOLOR, FSNETCMD_FOGCOLOR, FSNETCMD_TEXTMESSAGE, FSNETCMD_ENVIRONMENT
from random import randint
ENABLED = True

class Plugin:
    def __init__(self):
        self.initialWeather = None
        self.plugin_manager = None

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugin_manager.register_hook('on_chat', self.on_chat)
        self.plugin_manager.register_hook('on_environment_server', self.on_environment)

    def on_chat(self, data, player, messages_to_client, *args):
        if ENABLED:
            message = FSNETCMD_TEXTMESSAGE(data).message
            if message[:3].lower() == 'fog':
                #We'll split the fog r,g,b message into a list of 3 integers
                fog = list(map(int, message[4:].split(',')))
                fog_colour_packet = FSNETCMD_FOGCOLOR.encode(fog[0], fog[1], fog[2], True)
                messages_to_client.append(fog_colour_packet)

            if message[:3].lower() == 'sky':
                sky = list(map(int, message[4:].split(',')))
                sky_colour_packet = FSNETCMD_SKYCOLOR.encode(sky[0], sky[1], sky[2], True)
                messages_to_client.append(sky_colour_packet)

            if message[:3].lower() == 'day' and self.initialWeather:
                packet = FSNETCMD_ENVIRONMENT.set_time(self.initialWeather.buffer, False, True)
                self.initialWeather = FSNETCMD_ENVIRONMENT(packet[4:])
                messages_to_client.append(packet)

            if message[:5].lower() == 'night' and self.initialWeather:
                packet = FSNETCMD_ENVIRONMENT.set_time(self.initialWeather.buffer, True, True)
                self.initialWeather = FSNETCMD_ENVIRONMENT(packet[4:])
                messages_to_client.append(packet)

            if message[:3].lower() == 'vis':
                visibility = int(message[4:])
                returnpacket = FSNETCMD_ENVIRONMENT.set_visibility(self.initialWeather.buffer, visibility, True)
                self.initialWeather = FSNETCMD_ENVIRONMENT(returnpacket[4:])
                messages_to_client.append(returnpacket)
        return False

    def on_environment(self, data, *args):
        """Store the initial weather packet for the server."""
        if ENABLED:
            self.initialWeather = FSNETCMD_ENVIRONMENT(data)
        return True
