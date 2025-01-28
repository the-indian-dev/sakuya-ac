"""
Sakuya AC : Perfect and Elegant Proxy for your YSFlight Server
Lisenced under GPLv3
"""

import asyncio
from os import write
from struct import unpack, pack
from lib.parseFlightData import parseFlightData
from lib import YSchat, YSplayer, YSendFlight, YSundead
import logging
from logging import critical, warn, info, debug
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
    try:
        # Connect to the actual server
        server_reader, server_writer = await asyncio.open_connection(SERVER_HOST, SERVER_PORT)
        peername = client_writer.get_extra_info('peername')
        if peername:
            ipAddr, clientPort = peername

        async def forward(reader, writer, direction):
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
                                for player in CONNECTED_PLAYERS:
                                    if player.ip == ipAddr:
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

                                        if player.life < 5:
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
                                            writer.write(b'"\x00\x00\x00$\x00\x00\x00*\x03\x01\x00\x0c\x00\xc8\x00\x14\x00 \x00\x08!!\x00\x08!"\x00\x08!\x00\x00\xb8\x0b\xc8\x00\x14\x00')
                                            await writer.drain()
                                            targetWriter.write(YSundead.undeadState)
                                            await targetWriter.drain()

                                        if abs(player.gValue) > G_LIM and player.gValue < 23:
                                            deathMsg = YSchat.message(f"{player.username}'s G-Force exceeded the limit, gValue = {player.gValue}!")
                                            endPacket = YSendFlight.endFlight(player.playerId)
                                            writer.write(deathMsg)
                                            writer.write(endPacket)
                                            await writer.drain()
                                        break


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
                                info("Connection Request")
                                username = (b''.join(unpack("II16cI", data)[2:16])).decode('ascii').strip('\x00')
                                playerObject = YSplayer.Player(username, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ipAddr,
                                            -1, -1, -1, -1, 0, client_writer)
                                CONNECTED_PLAYERS.append(playerObject)
                            elif packet_type == 12: # End Flight
                                for player in CONNECTED_PLAYERS:
                                    if player.ip == ipAddr:
                                        player.playerId = 0
                                        player.life = -1
                                        player.warningSent = False
                                        debug("Health resseted to -1")
                                        break
                            elif packet_type == 36: # Weapon config
                            # here we patch the packet to have smoke forcefully
                                for player in CONNECTED_PLAYERS:
                                    if player.ip == ipAddr:
                                        targetPlayer = player
                                    break
                                    data = YSundead.undeadPatch(targetPlayer.playerId, data)
                                    writer.write(data)
                                    await writer.drain()
                            """
                            elif packet_type == 32: # Char message
                                # will be used for commands
                                msg = YSchat.message("Pong!")
                                writer.write(msg)
                                await writer.drain()
                            """

                        except Exception as e:
                            warn(f"Error parsing flight data: {e}")
                    else :
                        length, packet_type = unpack("<I I", data[:8])
                        debug("S2C" + str(packet_type))
                        debug(data)
                        if packet_type == 36:
                            for player in CONNECTED_PLAYERS:
                                if player.ip == ipAddr:
                                    targetWriter = player.streamWriterObject
                                    id = player.playerId
                                    break
                            data = YSundead.undeadPatch(id, data)
                            targetWriter.write(data)
                            await targetWriter.drain()

                    # Forward the packet to the other endpoint
                    writer.write(data)
                    await writer.drain()
                except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError) as e:
                    warn(f"Connection error during packet forwarding: {e}")
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
