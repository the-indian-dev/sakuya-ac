from struct import unpack, pack
from PacketManager.packets import MESSAGE_TYPES, FSWEAPON_DICT, GUIDEDWEAPONS


class PacketManager:

    def __init__(self):
        pass

    def decode(self, buffer:bytes, with_size:bool=False, should_decode=True):
        """
        Takes incomming packets from client or server and decodes them.
        If with_size is True, then the packet size is included in the buffer.
        If decode is False, then the packet is just returned as is.
        If it is true, then the packet will be decoded.
        """

        if with_size:
            # Strips away the size, so we've just got the message.
            buffer = buffer[4:]

        # Pull out the message type
        msg_type = unpack("I", buffer[:4])[0]

        # Find message type on the message_types list
        if msg_type < len(MESSAGE_TYPES):
            msg_type = MESSAGE_TYPES[msg_type]
            packet_class = None
            try:
                # Try to import the packet class
                packet_class = __import__("PacketManager.packets."+msg_type, fromlist=[msg_type])
            except ImportError as e:
                print(f"Error importing packet: {msg_type}")
                print(e)
            if packet_class:
                return packet_class(buffer, should_decode)
            return None

        return None
