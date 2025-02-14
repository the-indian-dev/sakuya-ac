"""TThis plugin will cause the aircraft to emit smoke if it's health is below a certain threshold.
It is also an example of a plugin as a folder/module.
This can be used as a basis for more complex plugins that may need multiple files."""
from lib.PacketManager.packets import List_Constructor
from json import load
from struct import pack
from logging import error
ENABLED = True
custom_list_file = "plugins\\custom_aircraft_list\\custom_list.json"

class Plugin:
    def __init__(self):
        self.plugin_manager = None
        self.aircraft_list = []

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        with open(custom_list_file, 'r', encoding='utf-8') as f:
            json_file = load(f)
            if isinstance(json_file,list):
                self.aircraft_list = json_file
            else:
                error(f"Invalid JSON file {custom_list_file}. Must be a list of aircraft.")
        self.plugin_manager.register_hook('on_list', self.on_list)
        self.plugin_manager.register_hook('on_list_server', self.on_list_server)

    def on_list(self, packet, player, message_to_client, message_to_server):
        if ENABLED:
            return False
        return True

    def on_list_server(self, packet, player, message_to_client, message_to_server):
        if ENABLED:
            #Send the packet straight back to the server, and prevent it being passed to the client.
            packet = pack("I",len(packet)) + packet
            message_to_server.append(packet)
            if not hasattr(player, 'custom_packet_sent'):
                player.custom_packet_sent=True
                #Send the custom list packets.
                lc = List_Constructor(self.aircraft_list).get_packets()
                for packet in lc:
                    message_to_client.append(packet)
            return False
        return True
