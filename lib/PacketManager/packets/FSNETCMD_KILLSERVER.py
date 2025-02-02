from struct import pack
from .FSNETCMD_EMPTYPACKET import FSNETCMD_EMPTYPACKET

class FSNETCMD_KILLSERVER(FSNETCMD_EMPTYPACKET): #15
    """
    This is unimplemented in YS, but it would shutdown the server
    The actual server functionality is disabled.
    """
    @staticmethod
    def encode(with_size:bool=False):
        buffer = pack("I",15)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer