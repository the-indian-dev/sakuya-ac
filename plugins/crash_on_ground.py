# This plugin renders the dead plane until crashes in ground
# Thus disabling mid air dispawning when dead
from lib.PacketManager.packets import FSNETCMD_REMOVEAIRPLANE, FSNETCMD_READBACK, FSNETCMD_GETDAMAGE

ENABLED = True

class Plugin:
    def __init__(self):
        self.plugin_manager = None

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugin_manager.register_hook('on_remove_airplane_server', self.on_death)

    def on_death(self, data, player, message_to_client, message_to_server):
        if player.aircraft.id != -1:
            if player.aircraft.id == FSNETCMD_REMOVEAIRPLANE(data).object_id:
                return True
            else:
                decode = FSNETCMD_REMOVEAIRPLANE(data)
                b = FSNETCMD_GETDAMAGE.encode(decode.object_id, 1, 1,
                    player.aircraft.id, 10000,
                    11, 0, True)
                message_to_client.append(b)
                message_to_server.append(b)
                a = FSNETCMD_READBACK.encode(2, player.aircraft.id, True)
                message_to_server.append(a)
                return False
        else:
            return True
