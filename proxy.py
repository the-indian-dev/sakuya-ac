"""
Sakuya AC : Perfect and Elegant Proxy for your YSFlight Server
Lisenced under GPLv3
"""

import asyncio
from struct import unpack
from lib.parseFlightData import parseFlightData
from lib import YSchat, YSplayer, YSendFlight
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
                                        # TODO : Remove in production
                                        elif player.life == 0:
                                            debug(data)
                                        elif playerData[21] > player.life:
                                            cheatingMsg = YSchat.message(f"{HEALTH_HACK_MESSAGE} by {player.username}")
                                            writer.write(cheatingMsg)
                                            await writer.drain()

                                        player.life = playerData[21]
                                        if abs(player.gValue) > G_LIM and player.gValue < 23: # TODO : Add limiter to read from a json file
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
                                            -1, -1, -1, -1, 0)
                                CONNECTED_PLAYERS.append(playerObject)
                            elif packet_type == 12: # End Flight
                                for player in CONNECTED_PLAYERS:
                                    if player.ip == ipAddr:
                                        player.playerId = 0
                                        player.life = -1
                                        debug("Health resseted to -1")
                                        break

                            """
                            elif packet_type == 32: # Aircraft list transmission end
                                print("Aircraft list transmission end")
                                welcomeMsg = YSchat.message("Welcome to YSFlight Proxy!")
                                writer.write(welcomeMsg)
                                await writer.drain()
                            """

                        except Exception as e:
                            warn(f"Error parsing flight data: {e}")
                    else :
                        length, packet_type = unpack("<I I", data[:8])
                        debug("S2C" + str(packet_type))
                        debug(data)

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
