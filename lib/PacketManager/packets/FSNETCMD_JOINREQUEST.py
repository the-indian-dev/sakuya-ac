from struct import pack, unpack

class FSNETCMD_JOINREQUEST: #8
    """
    The client sends a join request to the server with their iff, aircraft, start position, fuel and smoke
    The server replies with the join request readback,The server replies with the join request readback
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.iff = 0 # The IFF sent is 1 subtracted from the selected value by the player
        self.aircraft = None
        self.start_pos = None #It's the STP name
        self.fuel = None
        self.smoke = None
        if should_decode:
            self.decode()

    def decode(self):
        self.iff, _, self.aircraft, self.start_pos, _, self.fuel, self.smoke = unpack("HH32s32sHHH", self.buffer[4:78])
        self.start_pos = self.start_pos.decode().strip('\x00')
        self.aircraft = self.aircraft.decode().strip('\x00')

    @staticmethod
    def encode(iff, aircraft, start_pos, fuel, smoke, with_size:bool=False):
        buffer = pack("IHH32s32sHHH", 8, iff, 0, aircraft.encode(),
                      start_pos.encode(), 1, fuel, smoke)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer
