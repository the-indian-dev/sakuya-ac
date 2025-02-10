"""
Sakuya AC : Perfect and Elegant Proxy for your YSFlight Server
Lisenced under GPLv3
"""

import asyncio
from struct import unpack, pack
from lib.parseFlightData import parseFlightData
from lib import YSchat, YSplayer, YSendFlight, YSundead, YSviaversion, Player, Aircraft
from lib.PacketManager.PacketManager import PacketManager
from lib.PacketManager.packets import *
import logging
from logging import critical, warning, info, debug
from config import *
from time import sleep

# Configuration
SERVER_HOST = SERVER_HOST
SERVER_PORT = SERVER_PORT
PROXY_PORT = PROXY_PORT
CONNECTED_PLAYERS = [] # List of connected players
logging.basicConfig(level=LOGGING_LEVEL)

info("Welcome to Sakuya AC")
info("Perfect and Elegant Proxy for your Ysflight Server")
info("Lisenced under GPLv3")

# Handle client connections
async def handle_client(client_reader, client_writer):
    message_to_client = []
    message_to_server = []
    player = Player.Player(message_to_server, message_to_client, client_writer) #Initialise the player.


    try:
        # Connect to the actual server
        server_reader, server_writer = await asyncio.open_connection(SERVER_HOST, SERVER_PORT)
        peername = client_writer.get_extra_info('peername')
        if peername:
            ipAddr, clientPort = peername
            player.set_ip(ipAddr)

            debug("Player object initiated")

        async def forward(reader, writer, direction, player=player):

            while True:
                try:
                    #Test if there are any unsent messages to the client or server from other processes.
                    if len(message_to_client) > 0:
                        client_writer.write(message_to_client.pop(0))
                        await client_writer.drain()
                    if len(message_to_server) > 0:
                        server_writer.write(message_to_server.pop(0))
                        await server_writer.drain()

                    if not reader.at_eof(): # Connection closed
                        header = await reader.readexactly(4)  # Ensures we always get 4 bytes
                        if not header:
                            break  # Connection closed

                        length = unpack("I", header)[0]

                        packet = await reader.read(length)

                        if not packet:
                            break

                        data = header + packet
                        packet_type = PacketManager().get_packet_type(packet)
                        if direction == "client_to_server":
                            debug("C2S" + str(packet_type))
                            debug(data)

                            try:

                                if packet_type == "FSNETCMD_LOGON":
                                    player.login(FSNETCMD_LOGON(packet))

                                elif packet_type == "FSNETCMD_AIRPLANESTATE":
                                    # print("Damaging!")
                                    # damageData = FSNETCMD_GETDAMAGE.encode(player.aircraft.id, 1, 1, player.aircraft.id, 1, 11, 0, True)
                                    # print("custom", damageData)
                                    # message_to_server.append(damageData)
                                    # message_to_client.append(damageData)

                                    packet = player.aircraft.add_state(FSNETCMD_AIRPLANESTATE(packet))

                                    """
                                    Just for fun!
                                    if packet.flags['firing']:
                                        bomb_drop = FSNETCMD_MISSILELAUNCH.drop_bombs(player.aircraft)
                                        message_to_server.append(bomb_drop)
                                        message_to_client.append(bomb_drop)
                                    """
                                    if player.aircraft.last_packet.g_value > G_LIM:
                                        debug("G Value exceeded : ", player.aircraft.last_packet.g_value)
                                        # We make a packet which damages the aircraft using the same pilot ID, using a gun
                                        damageData = FSNETCMD_GETDAMAGE.encode(player.aircraft.id, 1, 1, player.aircraft.id, 1, 11, 0, True)
                                        warnMsg = YSchat.message(f"You are exceeding the G Limit for the aircraft!, gValue = {player.aircraft.last_packet.g_value}!")
                                        message_to_client.append(damageData)
                                        message_to_client.append(warnMsg)

                                    prev_life = player.aircraft.prev_life
                                    if player.aircraft.life == -1: #Uninitialised
                                        player.aircraft.life = prev_life

                                    elif prev_life > player.aircraft.life:
                                        cheatingMsg = YSchat.message(f"{HEALTH_HACK_MESSAGE} by {player.username}")
                                        writer.write(cheatingMsg)
                                        await writer.drain()

                                    elif player.aircraft.life < SMOKE_LIFE and SMOKE_PLANE:

                                        if not player.aircraft.damage_engine_warn_sent:
                                            warningMsg = YSchat.message(f"Your engine has been damaged! You can't turn on afterburner")
                                            debug(f"Sending warning to {player.username}")
                                            message_to_client.append(warningMsg)
                                            player.aircraft.damage_engine_warn_sent = True

                                    player.aircraft.life = prev_life

                                elif packet_type == "FSNETCMD_UNJOIN":
                                    player.aircraft.reset()

                                elif packet_type == "FSNETCMD_AIRCMD":
                                    h = FSNETCMD_AIRCMD(packet)
                                    print(h.decode)

                                # elif packet_type == "FSNETCMD_GETDAMAGE":
                                #    h = FSNETCMD_GETDAMAGE(packet, True)
                                #    print(h)

                                # if packet_type == 11:  # Flight data packet
                                #         playerData = parseFlightData(data)
                                #         player.playerId = playerData[1]
                                #         player.x = playerData[2]
                                #         player.y = playerData[3]
                                #         player.z = playerData[4]
                                #         player.throttle = playerData[22]
                                #         player.aam = playerData[18]
                                #         player.agm = playerData[19]
                                #         player.gunAmmo = playerData[16]
                                #         player.rktAmmo = playerData[17]
                                #         player.fuel = playerData[12]
                                #         player.gValue = playerData[28]
                                #         debug(player)

                                #         # Check if health increased
                                #         if player.life == -1:
                                #             player.life = playerData[21]

                                #         elif playerData[21] > player.life:
                                #             cheatingMsg = YSchat.message(f"{HEALTH_HACK_MESSAGE} by {player.username}")
                                #             writer.write(cheatingMsg)
                                #             await writer.drain()

                                #         player.life = playerData[21]

                                #         if player.life < SMOKE_LIFE and SMOKE_PLANE :
                                #             #TODO: Rework this with AIRCMD to remove AB, smoke packet can still be implemented.
                                #             #However will need to provide the aircraft with some smoke.
                                #             targetWriter = player.streamWriterObject
                                #             if not player.warningSent:
                                #                 warningMsg = YSchat.message(f"Your engine has been damaged! You can't turn on afterburner")
                                #                 debug(f"Sending warning to {player.username}")
                                #                 targetWriter.write(warningMsg)
                                #                 await targetWriter.drain()
                                #                 player.warningSent = True
                                #             # add smoke
                                #             # assuming packet version 5
                                #             # TODO : Make it dynamic for every pack version
                                #             # Since broken aircrafts will fly at < 400kts
                                #             # version 5 packets will do fine
                                #             data = data[0:60] + pack("h", -254) + data[62:]
                                #             writer.write(YSundead.smokedPlane(player.playerId))
                                #             await writer.drain()

                                #         if abs(player.gValue) > G_LIM and player.gValue < 23:
                                #             deathMsg = YSchat.message(f"{player.username}'s G-Force exceeded the limit, gValue = {player.gValue}!")
                                #             endPacket = YSendFlight.endFlight(player.playerId)
                                #             writer.write(deathMsg)
                                #             writer.write(endPacket)
                                #             await writer.drain()

                                # elif packet_type == 1: # Connection Request
                                #     extracted = unpack("II16cI", data)
                                #     # username = (b''.join(unpack("II16cI", data)[2:16])).decode('ascii').strip('\x00')
                                #     username = b''.join(extracted[2:16]).decode('ascii').strip('\x00')
                                #     version = extracted[-1]
                                #     info(f"Connection request by {username} : {ipAddr}; YSFVERSION = {version}")
                                #     player.username = username
                                #     player.ip = ipAddr
                                #     debug("Player object fixed!")
                                #     debug(player)
                                #     # targetWriter = player.streamWriterObject
                                #     # targetWriter.write(b'\x04\x00\x00\x00\x10\x00\x00\x00')
                                #     print("16 packet sent!")
                                #     # await targetWriter.drain()
                                #     if version != YSF_VERSION and VIA_VERSION:
                                #         info(f"ViaVersion enabled : Porting {username} from {YSF_VERSION} to {version}")
                                #         targetWriter = player.streamWriterObject
                                #         targetWriter.write(YSchat.message(f"Porting you to YSFlight {YSF_VERSION}, This is currently Experimental"))
                                #         targetWriter.write(YSchat.message(f"Please report any bugs to the server admin or join with the correct version"))
                                #         await targetWriter.drain()
                                #         data = YSviaversion.genViaVersion(username, YSF_VERSION)

                                # elif packet_type == 12: # End Flight
                                #         player.playerId = 0
                                #         player.life = -1
                                #         player.warningSent = False
                                #         debug("Health resseted to -1")

                                # elif packet_type == 36: # Weapon config
                                #     # here we patch the packet to have smoke forcefully
                                #     # This part also is for regen, so we disable cheat detection for health
                                #     player.life = -1
                                # elif packet_type == 44:
                                #     # We drop the packets from YSFlight and use it for ourselves
                                #     debug("Packet verification unimplemented!")
                                #     continue

                            except Exception as e:
                                warning(f"Error parsing flight data: {e}", exc_info=True)

                        else :
                            debug("S2C" + str(packet_type))
                            debug(data)

                            #Coming from the server to the client
                            if packet_type == "FSNETCMD_ADDOBJECT":
                                    if player.check_add_object(FSNETCMD_ADDOBJECT(packet)):
                                        info(f"{player.username} has spawned an aircraft")
                                        addSmoke = FSNETCMD_WEAPONCONFIG.addSmoke(player.aircraft.id)
                                        message_to_server.append(addSmoke)

                            elif packet_type == "FSNETCMD_AIRCMD":
                                #Check the configs against the current aircraft
                                command = FSNETCMD_AIRCMD(packet)
                                player.aircraft.check_command(command)

                            elif packet_type == "FSNETCMD_PREPARESIMULATION":
                                welcomeMsg = YSchat.message(WELCOME_MESSAGE.format(username=player.username))
                                message_to_server.append(welcomeMsg)

                        # Forward the packet to the other endpoint
                        writer.write(data)
                        await writer.drain()
                except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError) as e:
                    if e == BrokenPipeError:
                        info(f"Connection closed by {player.username} : {player.ip}")
                    else:
                        warning(f"Connection error during packet forwarding: {e}")
                    break

        # Start forwarding data between client and server
        await asyncio.gather(
            forward(client_reader, server_writer, "client_to_server"),
            forward(server_reader, client_writer, "server_to_client"),
        )
    except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError) as e:
        critical(f"Connection error: {e}")
    finally:
        try:
            client_writer.close()
            await client_writer.wait_closed()
        except Exception as e:
            critical(f"Error closing client connection: {e}")


# Start the proxy server
async def start_proxy():
    server = await asyncio.start_server(handle_client, "0.0.0.0", PROXY_PORT)
    info(f"Proxy server listening on port {PROXY_PORT}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(start_proxy())
