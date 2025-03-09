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
        #self.plugin_manager.register_hook('on_chat', self.on_chat)
        self.plugin_manager.register_hook('on_environment_server', self.on_environment)
        self.plugin_manager.register_command('fog', self.fog, "Sets fog color. Usage : /fog r,g,b")
        self.plugin_manager.register_command('sky', self.sky, "Sets sky color. Usage : /sky r,g,b")
        self.plugin_manager.register_command('time', self.time, "Sets time. Usage : /time <day|night>")
        self.plugin_manager.register_command('visibility', self.visibility, "Sets Visibilty : /vis <visibilty in meters>", "vis")

    def fog(self, full_message, player, message_to_client, message_to_server):
        try:
            args = list(map(int, full_message[4:].split(',')))
        except:
            message_to_client.append(FSNETCMD_TEXTMESSAGE.encode("Invalid fog argument, usage /fog r,g,b", True))
            return
        fog_colour_packet = FSNETCMD_FOGCOLOR.encode(args[0], args[1], args[2], True)
        message_to_client.append(fog_colour_packet)

    def sky(self, full_message, player, message_to_client, message_to_server):
        try:
            args = list(map(int, full_message[4:].split(',')))
        except Exception as e:
            message_to_client.append(FSNETCMD_TEXTMESSAGE.encode("Invalid sky argument, usage /sky r,g,b", True))
            return True
        sky_colour_packet = FSNETCMD_SKYCOLOR.encode(args[0], args[1], args[2], True)
        message_to_client.append(sky_colour_packet)
        return True

    def time(self, full_message, player, message_to_client, message_to_server):
        requested = full_message[6:].lower()
        if  requested == 'day' and self.initialWeather:
            packet = FSNETCMD_ENVIRONMENT.set_time(self.initialWeather.buffer, False, True)
            self.initialWeather = FSNETCMD_ENVIRONMENT(packet[4:])
            message_to_client.append(packet)

        elif requested == 'night' and self.initialWeather:
            packet = FSNETCMD_ENVIRONMENT.set_time(self.initialWeather.buffer, True, True)
            self.initialWeather = FSNETCMD_ENVIRONMENT(packet[4:])
            message_to_client.append(packet)

        else:
            message_to_client.append(FSNETCMD_TEXTMESSAGE.encode("Invalid time argument, usage /time night or /time day", True))
        return True

    def visibility(self, full_message, player, message_to_client, message_to_server):
        visibility = int(full_message[4:])
        returnpacket = FSNETCMD_ENVIRONMENT.set_visibility(self.initialWeather.buffer, visibility, True)
        self.initialWeather = FSNETCMD_ENVIRONMENT(returnpacket[4:])
        message_to_client.append(returnpacket)
        return True

    """
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
        """


    def on_environment(self, data, *args):
        """Store the initial weather packet for the server."""
        self.initialWeather = FSNETCMD_ENVIRONMENT(data)
        return True
