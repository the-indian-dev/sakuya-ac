from struct import pack

class FSNETCMD_JOINAPPROVAL: #9
    """
    When the server sends the "add aircraft" command, and
    receves the readback from the client, they'll send this
    It's an empty packet, but can be useful to know the client is about to join.
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        if should_decode:
            self.decode()

    def decode(self):
        pass

    @staticmethod
    def encode(with_size:bool=False):
        buffer = pack("I",9)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer