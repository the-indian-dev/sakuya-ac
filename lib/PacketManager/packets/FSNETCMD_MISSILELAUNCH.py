from struct import pack, unpack
from .constants import FSWEAPON_DICT, GUIDEDWEAPONS

class FSNETCMD_MISSILELAUNCH: #20
    """
    Sent when a missile has been launched
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.weapon_type = None
        self.position = [0,0,0]
        self.atti = [0,0,0]
        self.velocity = None
        self.life_remaining = None
        self.power = None
        self.fired_by_aircraft = None
        self.fired_by = None
        self.v_max = None
        self.mobility = None
        self.radar = None
        self.fired_at_aircraft = None
        self.fired_at = None
        if should_decode:
            self.decode()

    def decode(self):
        self.weapon_type = unpack("H", self.buffer[4:6])[0]
        self.position = list(unpack("fff", self.buffer[6:18]))
        self.atti = list(unpack("fff", self.buffer[18:30]))
        self.velocity, self.life_remaining, self.power = unpack("ffH", self.buffer[30:38])
        self.fired_by_aircraft = bool(unpack("I", self.buffer[38:42])[0])
        self.fired_by = unpack("I", self.buffer[42:46])[0]
        if self.weapon_type in FSWEAPON_DICT:
            self.weapon_type = FSWEAPON_DICT[self.weapon_type]

        if self.weapon_type in GUIDEDWEAPONS:
            self.v_max, self.mobility, self.radar = unpack("fff", self.buffer[46:58])
            self.fired_at_aircraft = bool(unpack("I", self.buffer[58:62])[0])
            self.fired_at = unpack("I", self.buffer[62:66])[0]
        elif self.weapon_type == "FSWEAPON_FLARE":
            self.v_max = unpack("f", self.buffer[46:50])[0]

    @staticmethod
    def encode(weapon_type, position, atti, velocity, life_remaining, power,
               fired_by_aircraft, fired_by, v_max=None, mobility=None,
               radar=None, fired_at_aircraft=None, fired_at=None, with_size:bool=False):
        if weapon_type in FSWEAPON_DICT and isinstance(weapon_type,int):
            weapon_type_name = FSWEAPON_DICT[weapon_type]
        else:
            weapon_type_name = weapon_type
            weapon_type = list(FSWEAPON_DICT.keys())[list(FSWEAPON_DICT.values()).index(weapon_type)]
        buffer = pack("I",20)+pack("Hfff", weapon_type, *position)+pack("fff", *atti)+pack("ffH", velocity, life_remaining, power)
        buffer += pack("I",fired_by_aircraft)+pack("I",fired_by)
        if weapon_type_name in GUIDEDWEAPONS:
            buffer += pack("fff", v_max, mobility, radar)
            if isinstance(fired_at_aircraft, bool):
                fired_at_aircraft = int(fired_at_aircraft)
            buffer += pack("II", fired_at_aircraft, fired_at)
        if weapon_type_name == "FSWEAPON_FLARE":
            buffer += pack("f", v_max)

        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer