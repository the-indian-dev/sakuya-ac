"""TThis plugin will cause the aircraft to emit smoke if it's health is below a certain threshold.
It is also an example of a plugin as a folder/module.
This can be used as a basis for more complex plugins that may need multiple files."""
from lib.PacketManager.packets import FSNETCMD_AIRCMD, FSNETCMD_AIRPLANESTATE, FSNETCMD_TEXTMESSAGE
from logging import debug
from config import SMOKE_LIFE, SMOKE_PLANE
ENABLED = True

class Plugin:
    def __init__(self):
        self.plugin_manager = None

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugin_manager.register_hook('on_flight_data', self.on_flight_data)
        self.plugin_manager.register_hook('on_weapon_config', self.on_weapon_config)

    def on_flight_data(self, data, player,message_to_client, message_to_server):
        """After the initial incoming flight packet, check whether 
        the health is below the threshold, if so add smoke"""
        if ENABLED and SMOKE_PLANE and player.aircraft.life<SMOKE_LIFE:
            
            #Add smoke to the plane
            smoke_packet = FSNETCMD_AIRPLANESTATE(data).smoke()
            #forward it on to the server
            
            message_to_server.append(smoke_packet)
            
            
            
            if not player.aircraft.damage_engine_warn_sent:
                player.aircraft.damage_engine_warn_sent = True
                #Warn the player
                message = "Your engine has been damaged! You can't turn on your afterburner!"
                message_to_client.append(FSNETCMD_TEXTMESSAGE.encode(message,True))
                
                debug(f"Engine damage warning sent to {player.username}")
                
                message_to_client.append(FSNETCMD_AIRCMD.set_afterburner(player.aircraft.id, False, True))
            
        return False
    
    def on_weapon_config(self, data, player, message_to_client, message_to_server):
        if ENABLED:
            player.aircraft.just_repaired = True
            if player.aircraft.get_initial_config_value("AFTBURNR") == "TRUE":
                message_to_client.append(FSNETCMD_AIRCMD.set_afterburner(player.aircraft.id, True, True))
        return True
