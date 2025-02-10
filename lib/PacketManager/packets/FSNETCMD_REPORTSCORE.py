from struct import pack, unpack
from . import FSWEAPON_DICT
"""
This is the score card for when an aircraft/ground object is destroyed.
"""
class FSNETCMD_REPORTSCORE:
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.scored = None
        self.weapon_type = None
        self.position = [0,0,0]
        self.score_time = None
        self.killer_id = None
        self.killer_name = None
        self.killer_plane = None
        self.victim_id = None
        self.victim_name = None
        self.victim_plane = None

        if should_decode:
            self.decode()
        
    def decode(self):
        self.scored = bool(unpack("H", self.buffer[4:6])[0])
        self.weapon_type = unpack("H", self.buffer[6:8])[0]
        if self.weapon_type in FSWEAPON_DICT:
            self.weapon_type = FSWEAPON_DICT[self.weapon_type]
        self.position = list(unpack("fff", self.buffer[8:20]))
        self.score_time = unpack("f", self.buffer[20:24])[0]
        self.killer_id = unpack("I", self.buffer[28:32])[0]
        self.killer_name = self.buffer[32:64].decode("utf-8").rstrip("\x00")
        self.killer_plane = self.buffer[64:96].decode("utf-8").rstrip("\x00")
        self.victim_id = unpack("I", self.buffer[100:104])[0]
        self.victim_name = self.buffer[104:136].decode("utf-8").rstrip("\x00")
        self.victim_plane = self.buffer[136:168].decode("utf-8").rstrip("\x00")
    
    @staticmethod
    def encode(scored, weapon_type, position, score_time, killer_id, killer_name,
               killer_plane, victim_id, victim_name, victim_plane, with_size:bool=False):
        if weapon_type in FSWEAPON_DICT and not isinstance(weapon_type,int):
            weapon_type = list(FSWEAPON_DICT.keys())[list(FSWEAPON_DICT.values()).index(weapon_type)]
        
        buffer = pack("IHHffffII32s32sII32s32s", 46,
                      int(scored), weapon_type, *position, score_time, 0, killer_id,
                      killer_name.encode("utf-8"), killer_plane.encode("utf-8"),0,
                      victim_id, victim_name.encode("utf-8"), victim_plane.encode("utf-8"))
        if with_size:
            return pack("I", len(buffer))+buffer

        return buffer