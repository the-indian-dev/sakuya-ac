"""
This plugin enables you to perform air to air refueling.
"""
from ast import alias
import math
from lib.PacketManager.packets import FSNETCMD_AIRCMD, FSNETCMD_AIRPLANESTATE
from lib import YSchat
import asyncio

ENABLED = True
REFUEL_RADIUS = 500
# in meters, recomended to set +100-200m more than
# required range to compensate for distance lag caused by network.
FUEL_RATE = 50 # in kg/s (aprroximately a second, timing is not accurate)

refuelers = {}
refueling = {}

class Plugin:
    def __init__(self):
        self.plugin_manager = None

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugin_manager.register_command('refuel', self.refuel, "Allows you to get refuled", alias = "r")
        self.plugin_manager.register_command('refueler', self.refueler, "Allows other players to refuel from you", alias = "rf")
        self.plugin_manager.register_hook('on_flight_data', self.on_flight_data)
        self.plugin_manager.register_hook('on_unjoin', self.on_unjoin)

    def refueler(self, full_message, player, message_to_client, message_to_server):
        if player in refueling:
            a = YSchat.message("You cannot be refueled while being a refueler")

        elif player in refuelers:
            a = YSchat.message("You are no more refueling!")
            refuelers.pop(player)
        else:
            a = YSchat.message(f"You are now refueling other players! To refuel the plane must be within {REFUEL_RADIUS}m and have same IFF")
            refuelers[player] = [0, [], False]
        message_to_client.append(a)

    def refuel(self, full_message, player, message_to_client, message_to_server):
        #a = FSNETCMD_AIRCMD.set_command(player.aircraft.id, "INITFUEL", "3750kg", True)
        #message_to_client.append(a)
        #print(player in refueling)
        if player in refuelers:
            a = YSchat.message("You cannot be a refueler while being refueled")
        elif player in refueling:
            a = YSchat.message("You are no more refueling!")
            refueling.pop(player)
        else:
            a = YSchat.message(f"You can now be refueled by other players! To refuel the plane must be within {REFUEL_RADIUS}m and have same IFF")
            refueling[player] = [0, []]
        message_to_client.append(a)

    def on_flight_data(self, data, player, message_to_client, message_to_server):
        asyncio.create_task(self.refuel_logic(data, player))
        return True

    def on_unjoin(self, data, player, message_to_client, message_to_server):
        if player in refuelers:
            refuelers.pop(player)
        elif player in refueling:
            refueling.pop(player)
        return True

    @staticmethod
    def in_range(refueler_cord:list, refueled_cord:list):
        # the plane to be refueled must be below and behind the
        # refueler plane, ysf sends cords in list[x, y, z]
        # implement this later
        # for now we just use distance formula in a 3d space
        dist = math.sqrt((refueler_cord[0]-refueled_cord[0])**2 + (refueler_cord[1]-refueled_cord[1])**2 + (refueler_cord[2]-refueled_cord[2])**2)
        if dist < REFUEL_RADIUS:
            return True
        else:
            return False

    async def refuel_logic(self, data, player):
        decode = FSNETCMD_AIRPLANESTATE(data)
        k = player.streamWriterObject
        if player in refueling:
            for refueler in refuelers:
                if refueler.iff == player.iff:
                    refueling[player] = [decode.fuel, decode.position]
                    if self.in_range(refuelers[refueler][1], decode.position):
                        refuelers[refueler][2] = True
                        max_lim = int((player.aircraft.initial_config['WEIGFUEL'])[:-2])
                        if decode.fuel < max_lim:
                            #a = FSNETCMD_AIRCMD.set_command(player.aircraft.id, "INITFUEL", f"{decode.fuel+FUEL_RATE}kg", True)
                            #message_to_client.append(a)
                            k.write(FSNETCMD_AIRCMD.set_command(player.aircraft.id, "INITFUEL", f"{decode.fuel+FUEL_RATE}kg", True))
                        elif decode.fuel >= max_lim:
                            a = YSchat.message("The plane is full!")
                            refuelers[refueler][2] = False # No longer refueling
                            k.write(a)
                            #message_to_client.append(a)

                        if refuelers[refueler][0] < FUEL_RATE:
                            a = YSchat.message("The refueler ran out of fuel!")
                            k.write(a)
                            #message_to_client.append(a)
                    else:
                        refuelers[refueler][2] = False # No longer refueling


        elif player in refuelers:
            refuelers[player] = [decode.fuel, decode.position, refuelers[player][2]]
            if decode.fuel-FUEL_RATE > 0 and refuelers[player][2]:
                a = FSNETCMD_AIRCMD.set_command(player.aircraft.id, "INITFUEL", f"{decode.fuel-FUEL_RATE}kg", True)
                #message_to_client.append(a)
                k.write(a)
