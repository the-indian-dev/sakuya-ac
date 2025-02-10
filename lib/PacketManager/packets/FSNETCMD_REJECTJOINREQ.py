from struct import pack

class FSNETCMD_REJECTJOINREQ: #10
    """
    If the server rejects the join request, they'll send this.
    It's usually followed by a chat message saying why.
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        if should_decode:
            self.decode()

    def decode(self):
        pass

    @staticmethod
    def encode(with_size:bool=False):
        buffer = pack("I",10)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer