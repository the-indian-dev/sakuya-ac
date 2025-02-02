from struct import pack, unpack

class FSNETCMD_LOADFIELD: #4
    """
    This packet is sent by the server along with the field info. When received,
    the client replies with the same packet.
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.field = None
        self.fieldShortName = None
        self.flags = None
        self.pos = [0,0,0]
        self.atti = [0,0,0]
        if len(buffer) == 64 and should_decode:
            self.decode()

    def decode(self):
        self.field, self.flags, self.pos[0], self.pos[1], self.pos[2], self.atti[0], self.atti[1], self.atti[2] = unpack("32sIffffff", self.buffer[4:])
        self.fieldShortName = self.field.split(b'\x00')[0].decode()

    @staticmethod
    def encode(field, flags, pos, atti, with_size:bool=False):
        if isinstance(field, str):
            field = field.encode()
        buffer = pack("I32sIffffff", 4, field, flags, pos[0], pos[1],
                      pos[2], atti[0], atti[1], atti[2])
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer