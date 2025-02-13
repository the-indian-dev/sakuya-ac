"""This plugin will convert all chat messages to all caps.
It can be enabled here by changing the value of ENABLED to True."""
from lib.PacketManager.packets import FSNETCMD_TEXTMESSAGE
from logging import info
ENABLED = False

class Plugin:
    def __init__(self):
        self.plugin_manager = None

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugin_manager.register_hook('on_chat', self.on_chat)

    def on_chat(self, data, player,message_to_client, message_to_server):
        if ENABLED:
            message = FSNETCMD_TEXTMESSAGE(data, should_decode=True)
            message.message = message.message.upper()
            message = FSNETCMD_TEXTMESSAGE.encode(f"({message.user}){message.message}", with_size=True)
            message_to_server.append(message)
            

        return False
