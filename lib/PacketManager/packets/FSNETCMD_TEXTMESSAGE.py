from struct import pack
import re

class FSNETCMD_TEXTMESSAGE: #32
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.raw_message = None
        self.user = None
        self.message = None
        if should_decode:
            self.decode()

    def decode(self):
        self.raw_message = self.buffer[12:].decode("utf-8").strip("\x00")
        match = re.match(r"^\(([^)]+)\)(.+)", self.raw_message)
        if match:
            self.user. self.message = match.groups()

    @staticmethod
    def encode(message:str, with_size:bool=False):
        buffer = pack("III",32,0,0)+message.encode("utf-8")+b"\x00"
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer
