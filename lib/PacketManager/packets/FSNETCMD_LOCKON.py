from struct import pack, unpack

class FSNETCMD_LOCKON: #18
    """
    Sent from server to client, and client to server
    when someone locks onto someone else
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.locker_id = None
        self.locker_is_air = False
        self.lockee_id = None
        self.lockee_is_air = False
        if should_decode:
            self.decode()

    def decode(self):
        self.locker_id, self.locker_is_air, self.lockee_id, self.lockee_is_air = unpack("IIII", self.buffer[4:20])
        self.locker_is_air = bool(self.locker_is_air)
        self.lockee_is_air = bool(self.lockee_is_air)

    @staticmethod
    def encode(locker_id, locker_is_air, lockee_id, lockee_is_air, with_size:bool=False):
        if isinstance(locker_is_air, bool):
            locker_is_air = int(locker_is_air)
        if isinstance(lockee_is_air, bool):
            lockee_is_air = int(lockee_is_air)
        buffer = pack("I",18)+pack("IIII", locker_id, locker_is_air, lockee_id, lockee_is_air)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer