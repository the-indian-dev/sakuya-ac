from struct import pack, unpack

class FSNETCMD_UNJOIN: #12
    """
    This is sent client to server when the client leaves.
    The explosion doesn't seem to actually do anything in YS.
    There is a comment saying "add explosion here"... Not helpful.
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.object_id = None
        self.explosion = None
        if should_decode:
            self.decode()

    def decode(self):
        variables = unpack("IIhh", self.buffer[0:12])
        self.object_id = variables[1]
        self.explosion = bool(variables[2])

    @staticmethod
    def encode(object_id, explosion, with_size:bool=False):
        buffer = pack("I", 12)+pack("IIhh", 12, object_id, explosion)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer