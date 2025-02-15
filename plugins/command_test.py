"""
This is an example test command!
"""

from lib import YSchat
from time import sleep

ENABLED = False

class Plugin:
    def __init__(self):
        self.plugin_manager = None

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugin_manager.register_command('test', self.test)
        self.plugin_manager.register_command('timer', self.timer)

    def test(self, full_message, player, message_to_client, message_to_server):
        message_to_client.append(YSchat.message("Test command received"))
        return True

    def timer(self, full_message, player, message_to_client, message_to_server):
        sleep(5)
        message_to_client.append(YSchat.message("Timer ended"))
        return True
