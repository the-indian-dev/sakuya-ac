from struct import pack, unpack

class FSNETCMD_SKYCOLOR:
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.redValue = 0
        self.greenValue = 0
        self.blueValue = 0
        if should_decode:
            self.decode()

    def decode(self):
        self.redValue = self.buffer[4]
        self.greenValue = self.buffer[5]
        self.blueValue = self.buffer[6]

    @staticmethod
    def encode(redValue:int, greenValue:int, blueValue:int, with_size:bool=False):
        buffer = pack("IBBB", 49, redValue, greenValue, blueValue)
        if with_size: buffer = (pack("I", len(buffer))) + buffer
        return buffer
