from struct import unpack, pack

class FSNETCMD_SMOKECOLOR: #7
    """The server sends this to the client when another aircraft
    joins with smoke, and the client sends it to the server if
    they're joining with smoke.
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.aircraft_id = None
        self.smoke_quantity = None
        self.color = None
        if should_decode:
            self.decode()

    def decode(self):
        self.aircraft_id, self.smoke_quantity, r, g, b = unpack("IBBBB", self.buffer[4:9])
        self.color = (r,g,b)

    @staticmethod
    def encode(aircraft_id, smoke_quantity, color, with_size:bool=False):
        buffer = pack("IIBBBB", 7, aircraft_id, smoke_quantity, color[0], color[1], color[2])
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer