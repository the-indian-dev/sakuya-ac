"""
This plugin allows you have to Radar features similar to that of
original WW3 server.
"""
import math
from lib.PacketManager.packets import FSNETCMD_AIRPLANESTATE
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
        self.plugin_manager.register_hook('on_unjoin', self.on_unjoin)

    def on_flight_data_server(self, data, player, message_to_client, message_to_server):
        decode = FSNETCMD_AIRPLANESTATE(data)
        if decode.player_id == player.aircraft.id:
            return True
        else:
            try:
                print(decode.packet_version)
                print(*decode.position, *decode.atti, *decode.velocity, *decode.atti_velocity)
                message_to_client.append(FSNETCMD_AIRPLANESTATE.encode(decode.remote_time, decode.player_id, decode.packet_version, [0.0,0.0,0.0], decode.atti, decode.velocity, decode.atti_velocity,
                       decode.smoke_oil, decode.fuel, decode.payload, decode.flight_state, decode.vgw, decode.spoiler, decode.landing_gear, decode.flap, decode.brake,
                       decode.flags, decode.gun_ammo, decode.rocket_ammo, decode.aam, decode.agm, decode.bomb, decode.life, decode.g_value, decode.throttle, decode.elev, decode.ail, decode.rud,
                       decode.trim, decode.thrust_vector, decode.bomb_bay_info, True))
            except:
                traceback.print_exc()
            return False

    def on_unjoin(self, data, player, message_to_client, message_to_server):
        return True

    @staticmethod
    def in_range(pos1, pos2):
        # pos1 and pos2 are lists of [x,y,z]
        dist = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2)
        return dist <= RADIUS
