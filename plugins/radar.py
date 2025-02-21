"""
This plugin allows you have to Radar features similar to that of
original WW3 server.
"""
import math
from lib.PacketManager.packets import FSNETCMD_AIRPLANESTATE
from lib.YSchat import send
import struct
import traceback

ENABLED = True
RADIUS = 500 # in meters, within this range planes with different IFF can see each other on radar

flying_players = {}

class Plugin:
    def __init__(self):
        self.plugin_manager = None

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugin_manager.register_hook('on_flight_data_server', self.on_flight_data_server)
        self.plugin_manager.register_hook('on_flight_data', self.on_flight_data)
        self.plugin_manager.register_hook('on_unjoin', self.on_unjoin)

    def on_flight_data(self, data, player, message_to_client, message_to_server):
        flying_players[player.aircraft.id][1] = FSNETCMD_AIRPLANESTATE(data).position
        return True

    def on_flight_data_server(self, data, player, message_to_client, message_to_server):
        # TODO : This is very primitive, we need to implement a better way to keep track of players
        try:
            if player.aircraft.id not in flying_players and player.aircraft.id != -1:
                flying_players[player.aircraft.id] = [player, []]
            elif player.aircraft.id == -1:
                return True

            decode = FSNETCMD_AIRPLANESTATE(data)

            if decode.player_id == player.aircraft.id:
                return True
            elif self.get_player_by_pilotid(int(decode.player_id)).iff == player.iff:
                return True
            elif self.in_range(flying_players[player.aircraft.id][1], decode.position):
                print(flying_players[player.aircraft.id][1], decode.position)
                print("HERE")
                return True
            else:
                try:
                    position_data = struct.pack("3f", -1, 1000.0, 1000.0)
                    if decode.packet_version == 4 or 5:
                        updated_data = data[:14] + position_data + data[26:]
                    else:
                        updated_data = data[:16] + position_data + data[28:]
                except:
                    traceback.print_exc()

                player.streamWriterObject.write(send(updated_data))
                player.streamWriterObject.drain()
                return False
        except:
            traceback.print_exc()

    def on_unjoin(self, data, player, message_to_client, message_to_server):
        return True

    @staticmethod
    def in_range(pos1, pos2):
        # pos1 and pos2 are lists of [x,y,z]
        dist = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2)
        return dist <= RADIUS

    @staticmethod
    def get_player_by_pilotid(pilotid:int):
        for playerid in flying_players:
            if playerid == pilotid:
                return flying_players[playerid][0]
        return None
