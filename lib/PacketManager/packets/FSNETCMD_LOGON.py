from struct import pack, unpack

class FSNETCMD_LOGON: #1
    """
    This is a logon packet, used to logon to the server.
    The client sends this to the server on login, and the server replies to acknowledge.
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.version = None
        self.username = None
        self.alias = None #Alias is the longer form of the username, if they're longer than 16 chars

        #If the YS version is 2018 (or YSCE) then the server will reply with an
        # empty packet on login-complete.
        if len(self.buffer)>5 and should_decode:
            #We can decode the packet.
            self.decode()

    def decode(self):
        self.username, self.version = unpack("16sI",self.buffer[4:24])
        if len(self.buffer)>24:
            self.alias = self.buffer[24:].decode().strip('\x00')
        else:
            self.alias = self.username

    @staticmethod   #Method to create a logon packet, if required.
    def encode(username, version, with_size:bool=False):
        if len(username)>15:
            shortform = username[:15]
            alias = username
        else:
            shortform = username
            alias = None
        buffer = pack("I16sI", 1, shortform.encode(), version)
        if alias:
            buffer += alias.encode()

        if with_size:
            return pack("I",len(buffer))+buffer

        return buffer