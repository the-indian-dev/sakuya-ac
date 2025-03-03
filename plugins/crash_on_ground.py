# This plugin renders the dead plane until crashes in ground
# Thus disabling mid air dispawning when dead

ENABLED = True

class Plugin:
    def __init__(self):
        self.plugin_manager = None

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugin_manager.register_hook('on_unjoin', self.on_death)

    def on_death(self, data, player, message_to_client, message_to_server):
        return False
