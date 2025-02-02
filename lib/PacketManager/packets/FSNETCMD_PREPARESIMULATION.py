from struct import pack
from .FSNETCMD_EMPTYPACKET import FSNETCMD_EMPTYPACKET

class FSNETCMD_PREPARESIMULATION(FSNETCMD_EMPTYPACKET): #16
    """
    This is sent from server to client when they've almost finished
    logging in.
    """
    @staticmethod
    def encode(with_size:bool=False):
        buffer = pack("I",16)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer