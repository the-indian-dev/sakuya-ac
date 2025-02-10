from struct import pack
from .FSNETCMD_EMPTYPACKET import FSNETCMD_EMPTYPACKET

class FSNETCMD_TESTPACKET(FSNETCMD_EMPTYPACKET): #17
    """
    This is just an empty packet.
    Just overwrite the encode.
    """
    @staticmethod
    def encode(with_size:bool=False):
        buffer = pack("I",17)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer