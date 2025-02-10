from struct import unpack, pack
from lib.PacketManager.packets.constants import MESSAGE_TYPES, FSWEAPON_DICT, GUIDEDWEAPONS


class PacketManager:

    def __init__(self):
        pass

    def get_packet_type(self, data: bytes):
        #Returns the message type of that packet.
        if len(data) < 4:
            return None
        return MESSAGE_TYPES[unpack("<I", data[:4])[0]]