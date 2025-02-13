"""This plugin will cause damage to the aircraft if
it exceeds the g-force limit set in the config file."""
from lib.PacketManager.packets import FSNETCMD_GETDAMAGE, FSNETCMD_TEXTMESSAGE
from config import G_LIM
import time
ENABLED = True

class Plugin:
    def __init__(self):
        self.plugin_manager = None

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugin_manager.register_hook('on_flight_data', self.on_receive)

    def on_receive(self, data, player, messages_to_client, *args):
        if ENABLED:
            if abs(player.aircraft.last_packet.g_value)> G_LIM:
                if time.time() - player.aircraft.last_over_g_message > 1: # Only send every second.
                    player.aircraft.last_over_g_message = time.time()
                    damage_packet = FSNETCMD_GETDAMAGE.encode(player.aircraft.id,
                                                            1, 1,
                                                            player.aircraft.id,
                                                            1, 11,0, True)
                    warning_message = FSNETCMD_TEXTMESSAGE.encode(f"You are exceeding the G Limit for the aircraft!, gValue = {player.aircraft.last_packet.g_value}!",True)
                    messages_to_client.append(damage_packet)
                    messages_to_client.append(warning_message)
        return True
