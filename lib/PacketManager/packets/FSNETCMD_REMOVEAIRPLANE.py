from .FSNETCMD_UNJOIN import FSNETCMD_UNJOIN
from struct import pack

class FSNETCMD_REMOVEAIRPLANE(FSNETCMD_UNJOIN): #13
    """
    Seems to just be the same as 12. No idea why Soji made 2.
    We'll just extend UNJOIN."""
    @staticmethod
    def encode(object_id, explosion, with_size:bool=False):
        buffer = pack("I", 12)+pack("IIhh", 13, object_id, explosion)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer