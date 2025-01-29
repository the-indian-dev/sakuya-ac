"""
Sakuya AC : Perfect and Elegant Proxy for your YSFlight Server
Lisenced under GPLv3
"""

import asyncio
from struct import unpack, pack
from lib.parseFlightData import parseFlightData
from lib import YSchat, YSplayer, YSendFlight, YSundead, YSviaversion
import logging
from logging import critical, warning, info, debug
from config import *

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
    player = YSplayer.Player("username", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "0.0.0.0",
                -1, -1, -1, -1, 0, client_writer)
    try:
        # Connect to the actual server
        server_reader, server_writer = await asyncio.open_connection(SERVER_HOST, SERVER_PORT)
        peername = client_writer.get_extra_info('peername')
        if peername:
            ipAddr, clientPort = peername
            debug("Player object initiated")

        async def forward(reader, writer, direction, player=player):
            while True:
                try:
                    data = await reader.read(4096)
                    if not data:
                        break
                    if direction == "client_to_server":
                        try:
                            length, packet_type = unpack("<I I", data[:8])
                            debug("C2S" + str(packet_type))
                            debug(data)
                            if packet_type == 11:  # Flight data packet
                                    playerData = parseFlightData(data)
                                    player.playerId = playerData[1]
                                    player.x = playerData[2]
                                    player.y = playerData[3]
                                    player.z = playerData[4]
                                    player.throttle = playerData[22]
                                    player.aam = playerData[18]
                                    player.agm = playerData[19]
                                    player.gunAmmo = playerData[16]
                                    player.rktAmmo = playerData[17]
                                    player.fuel = playerData[12]
                                    player.gValue = playerData[28]
                                    debug(player)

                                    # Check if health increased
                                    if player.life == -1:
                                        player.life = playerData[21]

                                    elif playerData[21] > player.life:
                                        cheatingMsg = YSchat.message(f"{HEALTH_HACK_MESSAGE} by {player.username}")
                                        writer.write(cheatingMsg)
                                        await writer.drain()

                                    player.life = playerData[21]

                                    if player.life < SMOKE_LIFE and SMOKE_PLANE :
                                        targetWriter = player.streamWriterObject
                                        if not player.warningSent:
                                            warningMsg = YSchat.message(f"Your engine has been damaged! You can't turn on afterburner")
                                            debug(f"Sending warning to {player.username}")
                                            targetWriter.write(warningMsg)
                                            await targetWriter.drain()
                                            player.warningSent = True
                                        # add smoke
                                        # assuming packet version 5
                                        # TODO : Make it dynamic for every pack version
                                        # Since broken aircrafts will fly at < 400kts
                                        # version 5 packets will do fine
                                        data = data[0:60] + pack("h", -254) + data[62:]
                                        writer.write(YSundead.smokedPlane(player.playerId))
                                        await writer.drain()

                                    if abs(player.gValue) > G_LIM and player.gValue < 23:
                                        deathMsg = YSchat.message(f"{player.username}'s G-Force exceeded the limit, gValue = {player.gValue}!")
                                        endPacket = YSendFlight.endFlight(player.playerId)
                                        writer.write(deathMsg)
                                        writer.write(endPacket)
                                        await writer.drain()


                                # parsed_data = parseFlightData(data)
                                # tRemote, playerId, x, y, z, *_ = parsed_data
                                # gunAmmo, rktAmmo, aam, agm, *_ = parsed_data[16:]
                                # fuel = parsed_data[12]
                                # throttle = parsed_data[22]

                                # Print the parsed flight data
                                # print(f"Player ID: {playerId}, X: {x}, Y: {y}, Z: {z}, "
                                #      f"Throttle: {throttle}, AAM: {aam}, AGM: {agm}, "
                                #      f"Gun Ammo: {gunAmmo}, Rocket Ammo: {rktAmmo}, Fuel: {fuel}")
                            elif packet_type == 1: # Connection Request
                                extracted = unpack("II16cI", data)
                                # username = (b''.join(unpack("II16cI", data)[2:16])).decode('ascii').strip('\x00')
                                username = b''.join(extracted[2:16]).decode('ascii').strip('\x00')
                                version = extracted[-1]
                                info(f"Connection request by {player.username} : {ipAddr}; YSFVERSION = {version}")
                                player.username = username
                                player.ip = ipAddr
                                debug("Player object fixed!")
                                debug(player)
                                if version != YSF_VERSION and VIA_VERSION:
                                    info(f"ViaVersion enabled : Porting {username} from {YSF_VERSION} to {version}")
                                    targetWriter = player.streamWriterObject
                                    targetWriter.write(YSchat.message(f"Porting you to YSFlight {YSF_VERSION}, This is currently Experimental"))
                                    targetWriter.write(YSchat.message(f"Please report any bugs to the server admin or join with the correct version"))
                                    await targetWriter.drain()
                                    data = YSviaversion.genViaVersion(username, YSF_VERSION)

                            elif packet_type == 12: # End Flight
                                    player.playerId = 0
                                    player.life = -1
                                    player.warningSent = False
                                    debug("Health resseted to -1")

                            elif packet_type == 36: # Weapon config
                                # here we patch the packet to have smoke forcefully
                                # This part also is for regen, so we disable cheat detection for health
                                player.life = -1
                            """
                                if player.life < 5:
                                    targetPlayer = player
                                    data = YSundead.undeadPatch(targetPlayer.playerId, data)
                                    writer.write(data)
                                    await writer.drain()
                            """
                            """
                            elif packet_type == 32: # Char message
                                # will be used for commands
                                msg = YSchat.message("Pong!")
                                writer.write(msg)
                                await writer.drain()
                            """

                        except Exception as e:
                            warning(f"Error parsing flight data: {e}")
                    else :
                        length, packet_type = unpack("<I I", data[:8])
                        debug("S2C" + str(packet_type))
                        debug(data)
                        if packet_type == 36:
                            # print("S2C ", str(data))
                            pass
                        """
                            targetWriter = player.streamWriterObject
                            id = player.playerId
                            data = YSundead.undeadPatch(id, data)
                            targetWriter.write(data)
                            await targetWriter.drain()
                        """

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
