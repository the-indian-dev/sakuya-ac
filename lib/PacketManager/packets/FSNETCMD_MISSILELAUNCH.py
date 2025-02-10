from struct import pack, unpack
from .constants import FSWEAPON_DICT, GUIDEDWEAPONS
from lib.Aircraft import Aircraft
from math import pi
import random

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
        print(self.buffer)
        # _ = unpack("I", self.buffer[:4])[0] #Packet type 
        # IH # 6
        # fff # 12
        # fff # 12
        # ffH #10
        # II # 8
        self.weapon_type = unpack("H", self.buffer[4:6])[0]
        self.position = list(unpack("fff", self.buffer[6:18]))
        self.atti = list(unpack("fff", self.buffer[18:30]))
        self.velocity, self.life_remaining, self.power = unpack("ffH", self.buffer[30:40])
        self.fired_by_aircraft = unpack("I", self.buffer[40:44])[0]
        self.fired_by = unpack("I", self.buffer[44:48])[0]
        if self.weapon_type in FSWEAPON_DICT:
            self.weapon_type = FSWEAPON_DICT[self.weapon_type]

        if self.weapon_type in GUIDEDWEAPONS:
            self.v_max, self.mobility, self.radar = unpack("fff", self.buffer[48:60])
            self.fired_at_aircraft = bool(unpack("I", self.buffer[60:64])[0])
            self.fired_at = unpack("I", self.buffer[64:68])[0]
        elif self.weapon_type == "FSWEAPON_FLARE":
            self.v_max = unpack("f", self.buffer[48:52])[0]

    

    @staticmethod
    def encode(weapon_type, position, atti, velocity, life_remaining, power,
               fired_by_aircraft, fired_by, v_max=1000, mobility=0,
               radar=0, fired_at_aircraft=False, fired_at=0, with_size:bool=False):
        if weapon_type in FSWEAPON_DICT and isinstance(weapon_type,int):
            weapon_type_name = FSWEAPON_DICT[weapon_type]
        else:
            weapon_type_name = weapon_type
            weapon_type = list(FSWEAPON_DICT.keys())[list(FSWEAPON_DICT.values()).index(weapon_type)]
        buffer = pack("I",20) #Packet type 0:4

        buffer += pack("H", weapon_type) #Weapon type 4:6
        buffer += pack("f", position[0]) #6:10
        buffer += pack("f", position[1]) #10:14
        buffer += pack("f", position[2]) #Position #14:18
        buffer += pack("f", atti[0]) #18:22
        buffer += pack("f", atti[1]) #22:26
        buffer += pack("f", atti[2]) #Attitude #26:30
        buffer += pack("ffH", velocity, life_remaining, power) #Velocity, life remaining, power #30:40
        buffer += pack("II",fired_by_aircraft,fired_by) #Fired by aircraft, fired by #40:48
        print(buffer)
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

    @staticmethod
    def drop_bombs(aircraft:Aircraft):
        position = aircraft.position
        atti = aircraft.attitude
        # atti = [(value*(32768/ pi)) for value in atti]
        atti[2] =0
        weapon_type = random.randint(0,13)
        packet = FSNETCMD_MISSILELAUNCH.encode(weapon_type, position=position, atti=atti, velocity=20, life_remaining=30000, power=999, fired_by_aircraft=0, fired_by=aircraft.id, v_max=1000, with_size=True)
        print(packet)
        return packet