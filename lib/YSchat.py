from struct import pack, unpack
from lib.PacketManager.packets import FSNETCMD_TEXTMESSAGE

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
    return FSNETCMD_TEXTMESSAGE.encode(msg,True)
