from struct import pack, unpack
from . import FSWEAPON_DICT

class FSNETCMD_WEAPONCONFIG:
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.aircraft_id = None
        self.number = None
        self.weapon_config = {}


        if should_decode:
            self.decode()

    def decode(self):
        self.aircraft_id, self.number = unpack("Ih",self.buffer[4:10])
        self.weapon_config = {}
        self.number = self.number & (~1)

        for i in range(self.number // 2):
            typ, count = unpack("hh",self.buffer[10+i*4:14+i*4])
            if typ in FSWEAPON_DICT:
                typ = FSWEAPON_DICT[typ]
            if "SMOKE" in typ:
                #the count is actually the RGB value, formatted like a ballbag.
                r = (count >>10)&31
                g = (count >>5)&31
                b = count&31
                r = (r>>2)+(r<<3)
                g = (g>>2)+(g<<3)
                b = (b>>2)+(b<<3)
                count = [r,g,b]
            self.weapon_config[typ] = count
            print(self.weapon_config)

    @staticmethod
    def encode(aircraft_id:int, weapon_config:dict, with_size:bool=False):
        buffer = pack("IIh", 36, aircraft_id, len(weapon_config)*2)
        for typ, count in weapon_config.items():
            if typ in FSWEAPON_DICT.values() and isinstance(typ, str):
                typ = [k for k,v in FSWEAPON_DICT.items() if v == typ][0]
            if typ >=32 and typ <=39 and isinstance(count,list): #Smoke
                r,g,b = count
                r = (r*31)/255
                g = (g*31)/255
                b = (b*31)/255
                count = (int(r)<<10)+(int(g)<<5)+int(b)
            buffer += pack("hh", typ, count)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer

    @staticmethod
    def addSmoke(aircraft_id:int):
        return FSNETCMD_WEAPONCONFIG.encode(aircraft_id, {32:[66,66,66]}, True)
