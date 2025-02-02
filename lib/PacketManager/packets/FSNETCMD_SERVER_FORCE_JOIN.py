from struct import pack, unpack
from .FSNETCMD_NULL import FSNETCMD_NULL

class FSNETCMD_SERVER_FORCE_JOIN(FSNETCMD_NULL):
    """
    Sent by the server to force the player to join
    This literally just presses J. Wild.
    """
    @staticmethod
    def encode(player_id, with_size:bool=False):
        buffer = pack("I", 47)
        if with_size:
            return pack("I", len(buffer)) + buffer
        return buffer