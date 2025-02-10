from struct import pack, unpack

class FSNETCMD_READBACK: #6
    """
    Sent from client to server and back to acknowledge various packets.

    *   Client sends FSNETREADBACK_ADDAIRPLAN or FSNETREADBACK_ADDGROUND to
        acknowledge FSNETCMD_ADDOBJECT
    *   Client sends FSNETREADBACK_REMOVEAIRPLANE or FSNETREADBACK_REMOVEGROUND 
        to acknowledge FSNETCMD_REMOVEAIRPLANE or FSNETCMD_REMOVEGROUND
    *   Client sends FSNETREADBACK_ENVIRONMENT to acknowledge FSNETCMD_ENVIRONMENT
    *   Client sends FSNETREADBACK_JOINREQUEST to acknowledge FSNETCMD_JOINREQUEST
    *   Client sends FSNETREADBACK_PREPARE to acknowledge FSNETCMD_PREPARESIMULATION
    *   Client sends FSNETREADBACK_USEMISSILE to acknowledge FSNETCMD_USEMISSILE
    *   Client sends FSNETREADBACK_USEUNGUIDEDWEAPON to acknowledge FSNETCMD_USEUNGUIDEDWEAPON
    *   Client sends FSNETREADBACK_CTRLSHOWUSERNAME to acknowledge FSNETCMD_CTRLSHOWUSERNAME
        
    *   Server sends FSNETREADBACK_JOINREQUEST to acknowledge FSNETCMD_JOINREQUEST -
        Will punt the user if the server receives this from them
    *   There are probably more, but I've not gone into much detail here yet.

    """

    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.read_back_type = None
        self.read_back_param = None
        if should_decode:
            self.decode()

    def decode(self):
        self.read_back_type, _, self.read_back_param = unpack("HHI", self.buffer[4:12])

    @staticmethod
    def encode(read_back_type, read_back_param, with_size:bool=False):
        buffer = pack("IhhI", 6, read_back_type, 0, read_back_param)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer