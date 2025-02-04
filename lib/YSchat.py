from struct import pack, unpack
from lib.PacketManager.packets import FSNETCMD_TEXTMESSAGE
#Re-write this to wrap the FSNETCMD_TEXTMESSAGE class

def send(buffer: bytes):
    """
    Add to a packet the 'size' information
    """
    return pack("I", len(buffer)) + buffer

def reply(type, buffer:bytes):
    """
    Generate packets to send
    """
    return send(pack("I", type) + buffer)

def message(msg: str):
    """
    Generate packets for sending messages
    """
    decode = "l" + str(len(msg) + 2) + "s"
    msg_buffer = bytes(msg, 'utf-8')
    buffer = pack(decode, 0, msg_buffer)
    return reply(32, buffer)
