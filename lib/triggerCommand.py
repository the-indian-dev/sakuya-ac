from config import *
from lib import YSchat
from logging import debug

async def triggerCommand(command, full_message, player, message_to_client, message_to_server, plugin_manager):
    debug(f"{player.username} triggered command {command}")
    if command == "help":
        message_to_client.append(YSchat.message(plugin_manager.help_message))
        return 0

    h = plugin_manager.trigger_command(command, player, full_message , message_to_client, message_to_server)
    if not h:
        message_to_client.append(YSchat.message(f"Command not found, Type {PREFIX}help for all commands."))
