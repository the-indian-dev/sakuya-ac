from struct import pack

class FSNETCMD_NULL: #0
    """
    This is a 'null' packet, there is nothing to process.
    """
    def __init__(self,buffer:bytes, should_decode:bool=True):
        pass

    def decode(self):
        return None

    def encode(self, with_size:bool=False):
        if with_size:
            return pack("II",4,0)
        return pack("I", 0)
