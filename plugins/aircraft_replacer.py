"""This plugin will replace the aircraft of the player
with the aircraft specified in the plugin. It is a template
for creating plugins that modify the aircraft of the player."""
from lib.PacketManager.packets import FSNETCMD_ADDOBJECT, FSNETCMD_JOINREQUEST, FSNETCMD_READBACK, FSNETCMD_AIRPLANESTATE
from config import G_LIM
import time

# CONFIG
ENABLED = False # Enable or disable the plugin

class Plugin:
    def __init__(self):
        self.plugin_manager = None
        self.first_add_object = False

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        # self.plugin_manager.register_hook('on_flight_data', self.on_flight_data)
        self.plugin_manager.register_hook('on_add_object_server', self.on_add_object_server)
        # self.plugin_manager.register_hook('on_flight_data_server', self.on_flight_data_server)
        self.plugin_manager.register_hook('on_join_request', self.on_join_request)


    def on_add_object_server(self, data, player, messages_to_client, *args):
        packet = FSNETCMD_ADDOBJECT(data)
        #Swap the aircraft and position
        if packet.pilot == player.username:
            packet.identifier = "EUROFIGHTER_TYPHOON"
            messages_to_client.append(packet.to_packet())
            self.first_add_object = True
            return False
        return True

    # def on_flight_data(self, data, player, messages_to_client, *args):
    #     packet = FSNETCMD_AIRPLANESTATE(data)
    #     if packet.player_id == player.aircraft.id:

    #     return True

    # def on_flight_data_server(self, data, player, messages_to_client, *args):
    #     packet = FSNETCMD_AIRPLANESTATE(data)
    #     if packet.player_id == player.aircraft.id and self.first_add_object:
    #         packet.position = [0,2000.0,0]
    #         packet.velocity = [25,0,25]
    #         messages_to_client.append(packet.to_packet())

    #         self.first_add_object = False
    #         return False
    #     return True

    def on_join_request(self, data, player, messages_to_client, message_to_server, *args):
        packet = FSNETCMD_JOINREQUEST(data)
        #Replace the aircraft:
        packet.aircraft = "EUROFIGHTER_TYPHOON"
        message_to_server.append(packet.to_packet())
        return False

    # def on_receive(self, data, player, messages_to_client, *args):
    #     if ENABLED:
    #         if abs(player.aircraft.last_packet.g_value)> G_LIM:
    #             if time.time() - player.aircraft.last_over_g_message > INTERVAL:
    #                 player.aircraft.last_over_g_message = time.time()
    #                 damage_packet = FSNETCMD_GETDAMAGE.encode(player.aircraft.id,
    #                                                         1, 1,
    #                                                         player.aircraft.id,
    #                                                         1, 11,0, True)
    #                 warning_message = FSNETCMD_TEXTMESSAGE.encode(f"You are exceeding the G Limit for the aircraft!, gValue = {player.aircraft.last_packet.g_value}!",True)
    #                 messages_to_client.append(damage_packet)
    #                 messages_to_client.append(warning_message)
    #     return True
