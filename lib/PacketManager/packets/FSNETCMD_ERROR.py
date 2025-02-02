from struct import pack, unpack
from . import ERROR_CODES

class FSNETCMD_ERROR: #3
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.error_code = None
        self.error_message = None
        if should_decode:
            self.decode()

    def decode(self):
        errorCode = unpack("I",self.buffer[4:8])[0]
        if errorCode < len(ERROR_CODES):
            self.error_message = ERROR_CODES[errorCode]

    @staticmethod
    def encode(error_code, with_size:bool=False):
        buffer = pack("I",3)+pack("I",error_code)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer
