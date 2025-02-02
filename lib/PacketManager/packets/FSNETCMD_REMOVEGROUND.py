from struct import pack
from .FSNETCMD_UNJOIN import FSNETCMD_UNJOIN

class FSNETCMD_REMOVEGROUND(FSNETCMD_UNJOIN): #19
    """
    This is the same as FSNETCMD_UNJOIN/Remove aircraft, but for ground objects.
    """
    @staticmethod
    def encode(object_id, explosion, with_size:bool=False):
        buffer =pack("I",19)+pack("IIhh", 19, object_id, explosion)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer