from struct import pack

class FSNETCMD_LOGOFF: #2
    """
    This is a logoff packet, used to logoff from the server.
    It appeasr to be un-used by YS. Including it for completeness.
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer

    def decode(self):
        pass

    @staticmethod
    def encode( with_size:bool=False):
        buffer = pack("I",2)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer