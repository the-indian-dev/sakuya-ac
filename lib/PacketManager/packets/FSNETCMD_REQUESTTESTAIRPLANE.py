from struct import pack
from .FSNETCMD_EMPTYPACKET import FSNETCMD_EMPTYPACKET

class FSNETCMD_REQUESTTESTAIRPLANE(FSNETCMD_EMPTYPACKET): #14
    """
    Spawns an F-15C at NORTH1000_01 in dogfight mode
    There is no way of calling this from YS.
    """
    @staticmethod
    def encode(with_size:bool=False):
        buffer = pack("I",14)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer