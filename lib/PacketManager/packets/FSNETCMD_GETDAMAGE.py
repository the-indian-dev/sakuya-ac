from struct import pack, unpack
from . import FSWEAPON_DICT

class FSNETCMD_GETDAMAGE: #22
    """
    Sent when an aircraft or ground target has taken damage
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.victim_id = None
        self.victim_type = None
        self.attacker_type = None
        self.attacker_id = None
        self.damage = None
        self.died_of = None
        self.weapon_type = None
        if should_decode:
            self.decode()

    def decode(self):
        variables = unpack("IIIIIHHH", self.buffer[0:26])
        self.victim_id = variables[2]
        self.victim_type = variables[1]
        self.attacker_type = variables[3]
        self.attacker_id = variables[4]
        self.damage = variables[5]
        self.died_of = variables[6]
        self.weapon_type = variables[7]
        if self.weapon_type in FSWEAPON_DICT:
            self.weapon_type = FSWEAPON_DICT[self.weapon_type]
        

    @staticmethod
    def encode(victim_id, victim_type, attacker_type, attacker_id, damage, died_of,
               weapon_type, with_size:bool=False):
        if weapon_type in FSWEAPON_DICT and not isinstance(weapon_type,int):
            weapon_type = list(FSWEAPON_DICT.keys())[list(FSWEAPON_DICT.values()).index(weapon_type)]

        buffer = pack("I",22)+pack("IIIIIHHH", victim_id, victim_type, attacker_type,
                                   attacker_id, damage, died_of, weapon_type)
        if with_size:
            return pack("I", len(buffer))+buffer
        return buffer
