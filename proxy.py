"""
Sakuya AC : Perfect and Elegant Proxy for your YSFlight Server
Lisenced under GPLv3
"""

import platform, sys
from struct import unpack, pack
from lib.parseFlightData import parseFlightData
from lib import YSchat, YSviaversion, Player, Aircraft, triggerCommand
from lib.triggerRespectiveHook import triggerRespectiveHook, triggerRespectiveHookServer
from lib.plugin_manager import PluginManager
from lib.PacketManager.PacketManager import PacketManager
from lib.PacketManager.packets import *
import logging
from logging import critical, warning, info, debug
from config import *
if DISCORD_ENABLED: from lib.discordSync import *
import traceback

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
        file_name = record.pathname.split('/')[-1]  # Extract just the filename
        log_message = f"{log_color}{record.levelname} [{file_name}:{record.lineno}]: {record.getMessage()}{reset}"
        return log_message

logging.basicConfig(level=LOGGING_LEVEL)

# Get the default handler and set the colored formatter
handler = logging.getLogger().handlers[0]
handler.setFormatter(ColoredFormatter("%(levelname)s: %(message)c"))

# we try to setup uvloop for faster io after setting the logging
# its supposed to give faster proxy but we will have to test that

if platform.system() != "Windows":
    try:
        import uvloop
        uvloop.install()
        info("uvloop found! Using uvloop for fast I/O")
    except ImportError:
        info("uvloop not found but can be installed! Use ``pip install uvloop``, uvloop gives faster I/O on unix systems!")
else:
    info("Running on Windows, using standard event loop")

import asyncio

info("Welcome to Sakuya AC")
info("Perfect and Elegant Proxy for your YSFlight Server")
info("Lisenced under GPLv3")
info("Press CTRL+C to stop the proxy")

#Load the plugins
plugin_manager = PluginManager(CONNECTED_PLAYERS)

# Close Connection
async def close_connection(client_writer, server_writer):
    try:
        if client_writer and not client_writer.is_closing():
            client_writer.close()
            await client_writer.wait_closed()
    except Exception as e:
        warning(f"Error closing client connection: {e}")

    try:
        if server_writer and not server_writer.is_closing():
            server_writer.close()
            await server_writer.wait_closed()
    except Exception as e:
        warning(f"Error closing server connection: {e}")


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
            try:
                while True:
                    try:
                        #Test if there are any unsent messages to the client or
                        # server from other processes.
                        keep_message = True # Reset this before each loop.
                        if direction == "client_to_server" and message_to_server and writer and not writer.is_closing():
                            writer.write(message_to_server.pop(0))
                            await writer.drain()
                        elif direction == "server_to_client" and message_to_client and writer and not writer.is_closing():
                            client_writer.write(message_to_client.pop(0))
                            await client_writer.drain()

                        if not reader.at_eof() or not reader._connection_lost : # Connection closed
                            try:
                                header = await reader.readexactly(4)  # Ensures we always get 4 bytes
                            except asyncio.IncompleteReadError:
                                await close_connection(client_writer, server_writer)
                                break
                            except ConnectionResetError:
                                await close_connection(client_writer, server_writer)
                                break
                            except Exception as e:
                                await close_connection(client_writer, server_writer)
                                critical(f"Error reading header: {e}")
                                break

                            if not header:
                                break  # Connection closed

                            length = unpack("I", header)[0]

                            packet = await reader.read(length)

                            if not packet:
                                await close_connection(client_writer, server_writer)
                                break

                            data = header + packet
                            packet_type = PacketManager().get_packet_type(packet)
                            if direction == "client_to_server":
                                debug("C2S" + str(packet_type) + str(player.username))
                                debug(data)

                                try:

                                    if packet_type == "FSNETCMD_LOGON":
                                        decode = FSNETCMD_LOGON(packet)
                                        """
                                        for p in CONNECTED_PLAYERS:
                                            if p.username == decode.username:
                                                client_writer.write(YSchat.message(f"Same username {decode.username} is aldready connected to server! Kicked {ipAddr}"))
                                                data = None
                                                info(f"Same username {decode.username} is aldready connected to server! Kicked {ipAddr}")
                                                CONNECTED_PLAYERS.remove(player)
                                                await close_connection(client_writer, server_writer)
                                        """

                                        player.login(decode)
                                        info(f"Player {player.username} connected from {player.ip}")

                                        if player.version != YSF_VERSION and VIA_VERSION:
                                            info(f"ViaVersion enabled : Porting {player.username} from {player.version} to {YSF_VERSION}")
                                            message_to_client.append(YSchat.message(f"Porting you to YSFlight {YSF_VERSION}, This is currently Experimental"))
                                            message_to_client.append(YSchat.message(f"Please report any bugs to the server admin or join with the correct version"))
                                            data = YSviaversion.genViaVersion(player.username, YSF_VERSION) #TODO: Refactor using the FSNETCMD packet.
                                            writer.write(data)
                                            continue

                                    elif packet_type == "FSNETCMD_JOINREQUEST":
                                        decode  = FSNETCMD_JOINREQUEST(packet)
                                        player.iff = decode.iff
                                        if DISCORD_ENABLED:
                                            asyncio.create_task(discord_send_message(CHANNEL_ID, f"{player.username} has took off in a {decode.aircraft}! 🛫"))

                                    elif packet_type == "FSNETCMD_AIRPLANESTATE":
                                        decode = FSNETCMD_AIRPLANESTATE(packet)
                                        player.aircraft.add_state(decode)

                                        #TODO: Do we want to convert all this to plugins? Probably not, but there is duplicated functionality
                                        # keep_message = plugin_manager.triggar_hook('on_flight_data', packet, player, message_to_client, message_to_server)
                                        # if not keep_message:
                                        #    data = None

                                        if player.aircraft.prev_life < player.aircraft.life and player.aircraft.prev_life != -1 and not player.aircraft.just_repaired:
                                            cheatingMsg = YSchat.message(f"{HEALTH_HACK_MESSAGE} by {player.username}")
                                            warning(f"Health hack detected for {player.username}, Connected from {player.ip}")
                                            message_to_server.append(cheatingMsg)

                                        player.aircraft.just_repaired = False

                                    elif packet_type == "FSNETCMD_UNJOIN":
                                        if DISCORD_ENABLED:
                                            asyncio.create_task(discord_send_message(CHANNEL_ID, f"{player.username} has left the airplane! 🛬"))
                                        player.aircraft.reset()

                                    elif packet_type == "FSNETCMD_WEAPONCONFIG":
                                        #keep_message = plugin_manager.triggar_hook('on_weapon_config', packet, player, message_to_client, message_to_server)
                                        #if not keep_message:
                                        #    data = None
                                        pass

                                    elif packet_type == "FSNETCMD_TEXTMESSAGE":
                                        msg = FSNETCMD_TEXTMESSAGE(packet)
                                        # keep_message = plugin_manager.triggar_hook('on_chat', packet, player, message_to_client, message_to_server)
                                        # if not keep_message:
                                        #    data = None

                                        finalMsg = (f"{player.username} : {msg.message}")
                                        if msg.message.startswith(PREFIX):
                                            data = None
                                            command = msg.message.split(" ")[0][1:]
                                            asyncio.create_task(triggerCommand.triggerCommand(command, msg.message, player, message_to_client, message_to_server, plugin_manager))
                                            info(f"Command {command} triggered by {player.username}")
                                        else:
                                            if DISCORD_ENABLED:
                                                # Make it non blocking!
                                                asyncio.create_task(discord_send_message(CHANNEL_ID, finalMsg))

                                    elif packet_type == "FSNETCMD_LIST":
                                        # keep_message = plugin_manager.triggar_hook('on_list', packet, player, message_to_client, message_to_server)
                                    # if not keep_message:
                                    #   data = None
                                        pass

                                    keep_message = triggerRespectiveHook(packet_type, packet, player, message_to_client, message_to_server, plugin_manager)
                                    if not keep_message: data = None

                                except Exception as e:
                                    warning(f"Error parsing flight data: {e}", exc_info=True)
                                    traceback.print_exc()  # This will display the full traceback

                            else :
                                debug("S2C" + str(packet_type) + str(player.username))
                                debug(data)

                                #if packet_type == "FSNETCMD_AIRCMD":
                                #    print(FSNETCMD_AIRCMD.decode(packet))

                                keep_message = triggerRespectiveHookServer(packet_type, packet, player, message_to_client, message_to_server, plugin_manager)
                                if not keep_message: data = None

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

                            # Forward the packet to the other endpoint if the data packet still exists.
                            if data:
                                writer.write(data)
                                await writer.drain()
                    except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError) as e:
                        if not player.connection_closed:
                            await close_connection(client_writer, server_writer)
                            if isinstance(e, (BrokenPipeError, ConnectionResetError, asyncio.CancelledError)):
                                info(f"Connection closed by {player.username} : {player.ip}")
                            else:
                                warning(f"Connection error during packet forwarding: {e}")
                                break
            except Exception as e:
                debug(f"Forward function exiting for {player.username} in {direction}")
                player.connection_closed = True
                await close_connection(client_writer, server_writer)

        """
        # Start forwarding data between client and server
        await asyncio.gather(
            forward(client_reader, server_writer, "client_to_server"),
            forward(server_reader, client_writer, "server_to_client"),
        )
        """

        client_to_server_task = None
        server_to_client_task = None

        try:
            # Start forwarding data between client and server
            client_to_server_task = asyncio.create_task(
                forward(client_reader, server_writer, "client_to_server")
            )
            server_to_client_task = asyncio.create_task(
                forward(server_reader, client_writer, "server_to_client")
            )

            # Wait for either task to complete
            done, pending = await asyncio.wait(
                [client_to_server_task, server_to_client_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            # Cancel pending tasks
            for task in pending:
                task.cancel()

            # Wait for cancelled tasks to finish
            if pending:
                await asyncio.wait(pending, return_when=asyncio.ALL_COMPLETED)

        except Exception as e:
            warning(f"Error in client handler: {e}")
        finally:
            # Clean up tasks if they still exist
            for task in [t for t in [client_to_server_task, server_to_client_task] if t and not t.done()]:
                task.cancel()

    except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError) as e:
        if not isinstance(e, BrokenPipeError):
            critical(f"Connection error: {e}")
    finally:
        try:
            if player in CONNECTED_PLAYERS:
                player.connection_closed = True
                CONNECTED_PLAYERS.remove(player)
                if not player.is_a_bot:
                    for p in CONNECTED_PLAYERS:
                        try:
                            if p.streamWriterObject and not p.streamWriterObject.is_closing():
                                p.streamWriterObject.write(YSchat.message(f"{player.username} has left the server!"))
                                await p.streamWriterObject.drain()
                        except Exception as e:
                            warning(f"Error sending disconnect message: {e}")

                    if DISCORD_ENABLED:
                        await discord_send_message(CHANNEL_ID, f"{player.username} has left the server!")

            # Always close connections, regardless of previous state
            try:
                if client_writer and not client_writer.is_closing():
                    client_writer.close()
                    await client_writer.wait_closed()
            except Exception as e:
                warning(f"Error closing client connection: {e}")

            try:
                if server_writer and not server_writer.is_closing():
                    server_writer.close()
                    await server_writer.wait_closed()
            except Exception as e:
                warning(f"Error closing server connection: {e}")

        except Exception as e:
            critical(f"Error during connection cleanup: {e}")
            traceback.print_exc()

# Start the proxy server
async def start_proxy():
    server = await asyncio.start_server(handle_client, "0.0.0.0", PROXY_PORT, backlog=100)
    info(f"Proxy server listening on port {PROXY_PORT}")
    if DISCORD_ENABLED:
        await asyncio.create_task(monitor_channel(CHANNEL_ID, CONNECTED_PLAYERS))
        # await asyncio.create_task(set_bot_status_online())
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        if DISCORD_ENABLED:
            asyncio.run(discord_send_message(CHANNEL_ID, "✅ Server has started."))
        asyncio.run(start_proxy())
    except KeyboardInterrupt:
        if DISCORD_ENABLED:
            asyncio.run(discord_send_message(CHANNEL_ID, "❌ Server has stopped."))
        info("Goodbye!")
