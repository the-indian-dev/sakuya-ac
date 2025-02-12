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
if DISCORD_ENABLED: from lib.discordSync import *
import traceback

# TODO: Remove in Production
# from random import randint

# Configuration
SERVER_HOST = SERVER_HOST
SERVER_PORT = SERVER_PORT
PROXY_PORT = PROXY_PORT

# Hold all Connected Players

CONNECTED_PLAYERS = []

# ANSI escape codes for colors
COLORS = {
    "DEBUG": "\033[92m",  # Green
    "INFO": "\033[94m",   # Blue
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",  # Red
    "CRITICAL": "\033[91;1m",  # Bold Red
    "RESET": "\033[0m"    # Reset color
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = COLORS.get(record.levelname, COLORS["RESET"])
        reset = COLORS["RESET"]
        log_message = f"{log_color}{record.levelname}: {record.getMessage()}{reset}"
        return log_message

logging.basicConfig(level=LOGGING_LEVEL)

# Get the default handler and set the colored formatter
handler = logging.getLogger().handlers[0]
handler.setFormatter(ColoredFormatter("%(levelname)s: %(message)c"))

info("Welcome to Sakuya AC")
info("Perfect and Elegant Proxy for your YSFlight Server")
info("Lisenced under GPLv3")
info("Press CTRL+C to stop the proxy")

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
            CONNECTED_PLAYERS.append(player)
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
                        try:
                            header = await reader.readexactly(4)  # Ensures we always get 4 bytes
                        except asyncio.IncompleteReadError:
                            break
                        except ConnectionResetError:
                            break
                        except Exception as e:
                            critical(f"Error reading header: {e}")
                            break

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
                                    if player.version != YSF_VERSION and VIA_VERSION:
                                        info(f"ViaVersion enabled : Porting {player.username} from {player.version} to {YSF_VERSION}")
                                        message_to_client.append(YSchat.message(f"Porting you to YSFlight {YSF_VERSION}, This is currently Experimental"))
                                        message_to_client.append(YSchat.message(f"Please report any bugs to the server admin or join with the correct version"))
                                        data = YSviaversion.genViaVersion(player.username, YSF_VERSION)
                                        writer.write(data)
                                        continue

                                elif packet_type == "FSNETCMD_AIRPLANESTATE":
                                    packet = player.aircraft.add_state(FSNETCMD_AIRPLANESTATE(packet))

                                    # Disco lights
                                    # Just for fun remove in production
                                    #skycolorPacket = FSNETCMD_SKYCOLOR.encode(randint(0,255), randint(0,255), randint(0,255), True)
                                    #fogcolorpacket = FSNETCMD_FOGCOLOR.encode(randint(0,255), randint(0,255), randint(0,255), True)
                                    #message_to_server.append(skycolorPacket)
                                    #message_to_client.append(skycolorPacket)
                                    #message_to_server.append(fogcolorpacket)
                                    #message_to_client.append(fogcolorpacket)

                                    if abs(player.aircraft.last_packet.g_value) > G_LIM:
                                        debug("G Value exceeded : ", player.aircraft.last_packet.g_value)
                                        # We make a packet which damages the aircraft using the same pilot ID, using a gun
                                        damageData = FSNETCMD_GETDAMAGE.encode(player.aircraft.id, 1, 1, player.aircraft.id, 1, 11, 0, True)
                                        warnMsg = YSchat.message(f"You are exceeding the G Limit for the aircraft!, gValue = {player.aircraft.last_packet.g_value}!")
                                        message_to_client.append(damageData)
                                        message_to_client.append(warnMsg)

                                    if player.aircraft.life == -1: #Uninitialised
                                        player.aircraft.prev_life = player.aircraft.life

                                    elif player.aircraft.prev_life < player.aircraft.life and player.aircraft.prev_life != -1 and not player.aircraft.just_repaired:
                                        cheatingMsg = YSchat.message(f"{HEALTH_HACK_MESSAGE} by {player.username}")
                                        warning(f"Health hack detected for {player.username}, Connected from {player.ip}")
                                        message_to_server.append(cheatingMsg)

                                    elif player.aircraft.life < SMOKE_LIFE and SMOKE_PLANE:
                                        # We patch the packet to have smoke forcefully
                                        data = FSNETCMD_AIRPLANESTATE(data[4:]).smoke()
                                        if not player.aircraft.damage_engine_warn_sent:
                                            warningMsg = YSchat.message(f"Your engine has been damaged! You can't turn on afterburner")
                                            debug(f"Sending warning to {player.username}")
                                            message_to_client.append(warningMsg)
                                            player.aircraft.damage_engine_warn_sent = True
                                            message_to_client.append(FSNETCMD_AIRCMD.set_afterburner(player.aircraft.id, False, True))

                                    player.aircraft.prev_life = player.aircraft.life
                                    player.aircraft.just_repaired = False

                                elif packet_type == "FSNETCMD_UNJOIN":
                                    player.aircraft.reset()

                                elif packet_type == "FSNETCMD_WEAPONCONFIG":
                                    player.aircraft.just_repaired = True
                                    if player.aircraft.get_initial_config_value("AFTBURNR") == "TRUE": message_to_client.append(player.aircraft.set_afterburner(True))
                                    debug("Aircraft repaired!")

                                elif packet_type == "FSNETCMD_TEXTMESSAGE":
                                    msg = FSNETCMD_TEXTMESSAGE(packet)
                                    finalMsg = (f"{player.username} : {msg.message}")
                                    # TODO: Remove in production
                                    # skyColor = FSNETCMD_SKYCOLOR.encode(136, 34, 34, True) # Top Gradient
                                    # fogColor = FSNETCMD_FOGCOLOR.encode(237, 156, 21, True) # Bottom Gradient
                                    # fogColor = FSNETCMD_FOGCOLOR.encode(136, 34, 34, True) # Dark Orange
                                    fogColor = FSNETCMD_FOGCOLOR.encode(120, 30, 30, True) # Magenta Tint
                                    # message_to_client.append(skyColor)
                                    message_to_client.append(fogColor)
                                    # message_to_server.append(skyColor)
                                    message_to_server.append(fogColor)

                                    if DISCORD_ENABLED:
                                        # Make it non blocking!
                                        asyncio.create_task(discord_send_message(CHANNEL_ID, finalMsg))

                            except Exception as e:
                                warning(f"Error parsing flight data: {e}", exc_info=True)
                                traceback.print_exc()  # This will display the full traceback

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
                                #These come server to client, not the other way around.
                                command = FSNETCMD_AIRCMD(packet)
                                player.aircraft.check_command(command)

                            elif packet_type == "FSNETCMD_PREPARESIMULATION":
                                welcomeMsg = YSchat.message(WELCOME_MESSAGE.format(username=player.username))
                                message_to_server.append(welcomeMsg)
                                player.is_a_bot = False
                                if DISCORD_ENABLED:
                                    asyncio.create_task(discord_send_message(CHANNEL_ID, f"{player.username} has joined the server!"))

                            elif packet_type == "FSNETCMD_ENVIRONMENT":
                                # We set time to night
                                pck = FSNETCMD_ENVIRONMENT.setTime(packet, True, False)
                                data = pack("I", len(pck)) + pck

                        # Forward the packet to the other endpoint
                        writer.write(data)
                        await writer.drain()
                except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError) as e:
                    if e == BrokenPipeError or  ConnectionResetError or asyncio.CancelledError:
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
        if not isinstance(e, BrokenPipeError):
            critical(f"Connection error: {e}")
    finally:
        try:
            client_writer.close()
            await client_writer.wait_closed()
        except Exception as e:
            if not isinstance(e, BrokenPipeError):
                critical(f"Error closing client connection: {e}")


# Start the proxy server
async def start_proxy():
    server = await asyncio.start_server(handle_client, "0.0.0.0", PROXY_PORT)
    info(f"Proxy server listening on port {PROXY_PORT}")
    if DISCORD_ENABLED:
        await asyncio.create_task(monitor_channel(CHANNEL_ID, CONNECTED_PLAYERS))
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(start_proxy())
    except KeyboardInterrupt:
        info("Goodbye!")
