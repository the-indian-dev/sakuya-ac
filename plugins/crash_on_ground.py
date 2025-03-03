# This plugin renders the dead plane until crashes in ground
# Thus disabling mid air dispawning when dead
from lib.PacketManager.packets import FSNETCMD_REMOVEAIRPLANE, FSNETCMD_READBACK

ENABLED = True

class Plugin:
    def __init__(self):
        self.plugin_manager = None

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        #self.plugin_manager.register_hook('on_unjoin', self.on_death)
        self.plugin_manager.register_hook('on_remove_airplane_server', self.on_death)

    def on_death(self, data, player, message_to_client, message_to_server):
        if player.aircraft.id != -1:
            if player.aircraft.id == FSNETCMD_REMOVEAIRPLANE(data).object_id:
                return True
            else:
                a = FSNETCMD_READBACK.encode(2, player.aircraft.id, True)
                message_to_server.append(a)
                return False
        else:
            return True
