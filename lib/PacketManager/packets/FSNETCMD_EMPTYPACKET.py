from struct import pack

class FSNETCMD_EMPTYPACKET:
    """
    A template function for empty packets"""
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        if should_decode:
            self.decode()

    def decode(self):
        pass # There are no messages in this packet!

    @staticmethod
    def encode(with_size:bool=False): #This will be extended by each func.
        buffer = pack("I",14)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer