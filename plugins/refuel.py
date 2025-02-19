"""
This plugin enables you to perform air to air refueling.
"""
import math
from lib.PacketManager.packets import FSNETCMD_AIRCMD, FSNETCMD_AIRPLANESTATE

ENABLED = True
REFUEL_RADIUS = 100 # in meters

refuelers = {}
refueling = {}

class Plugin:
    def __init__(self):
        def __init__(self):
            self.plugin_manager = None

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugin_manager.register_command('refuel', self.refuel)
        self.plugin_manager.register_command('k', self.refueler)
        self.plugin_manager.register_hook('on_flight_data', self.on_flight_data)

    def refueler(self, full_message, player, message_to_client, message_to_server):
        if player in refuelers:
            refuelers.pop(player)
        else:
            refuelers[player] = [0, [], False]

    def refuel(self, full_message, player, message_to_client, message_to_server):
        #a = FSNETCMD_AIRCMD.set_command(player.aircraft.id, "INITFUEL", "3750kg", True)
        #message_to_client.append(a)
        #print(player in refueling)
        if player in refueling:
            refueling.pop(player)
        else:
            refueling[player] = [0, []]

    def on_flight_data(self, data, player, message_to_client, message_to_server):
        decode = FSNETCMD_AIRPLANESTATE(data)
        print(player.username, decode.position)
        print(refuelers, refueling)
        if player in refueling:
            for player in refuelers:
                refueling[player] = [decode.fuel, decode.position]
                if self.in_range(refuelers[player][1], decode.position):
                    print("here!")
                    refuelers[player][2] = True
                    max_lim = int((player.aircraft.initial_config['WEIGFUEL'])[:-2])
                    if decode.fuel < max_lim:
                        a = FSNETCMD_AIRCMD.set_command(player.aircraft.id, "INITFUEL", f"{decode.fuel+100}kg", True)
                        message_to_client.append(a)
                else:
                    refuelers[player][2] = False


        elif player in refuelers:
            refuelers[player] = [decode.fuel, decode.position, refuelers[player][2]]
            if decode.fuel-100 > 0 and refuelers[player][2]:
                a = FSNETCMD_AIRCMD.set_command(player.aircraft.id, "INITFUEL", f"{decode.fuel-5}kg", True)
                message_to_client.append(a)
        return True

    @staticmethod
    def in_range(refueler_cord:list, refueled_cord:list):
        # the plane to be refueled must be below and behind the
        # refueler plane, ysf sends cords in list[x, y, z]
        # implement this later
        # for now we just use distance formula in a 3d space
        print(refueler_cord, refueled_cord)
        dist = math.sqrt((refueler_cord[0]-refueled_cord[0])**2 + (refueler_cord[1]-refueled_cord[1])**2 + (refueler_cord[2]-refueled_cord[2])**2)
        print(dist)
        if dist < REFUEL_RADIUS:
            return True
        else:
            return False
