from struct import pack, unpack
from math import pi
import math

class FSNETCMD_AIRPLANESTATE: #11
    """
    This packet is sent by the client to the server to update the state of the aircraft.
    The server sends this to the client to update the state of the aircraft.

    Versions:
    Version 0: vh, vp and vr are 16bit shorts
    >= 1: vh, vp and vr are 32bit integer appended at the end. Because ...why?
    >=2: includes thrust vector, reverser and bombbay
    >=3: idOnServer is 32bit int
    4 and 5: Short version of vh, vp and vr
    4: thrust vector and bombbay
    5: no thrust vector or bombbay
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.remote_time = None
        self.player_id = None
        self.packet_version = None
        self.position = [0,0,0]
        self.atti = [0,0,0]
        self.velocity = [0,0,0]
        self.atti_velocity = [0,0,0]
        self.smoke_oil = None
        self.fuel = None
        self.payload = None
        self.flight_state = None
        self.vgw = None
        self.spoiler = None
        self.landing_gear = None
        self.flap = None
        self.brake = None
        self.flags = {
            "ab": None,
            "firing": None,
            "smoke": None,
            "nav_lights": False,
            "beacon": False,
            "strobe": False,
            "landing_lights": False,
        }
        self.gun_ammo = None
        self.rocket_ammo = None
        self.aam = None
        self.agm = None
        self.bomb = None
        self.life = None
        self.g_value = None
        self.throttle = None
        self.elev = None
        self.ail = None
        self.rud = None
        self.trim = None
        self.thrust_vector = {
            "vector": None,
            "reverser": None
        }
        self.bomb_bay_info = None
        if should_decode:
            self.decode()

    def decode(self):
        self.remote_time, self.player_id = unpack("fI", self.buffer[4:12])
        self.packet_version = unpack("h", self.buffer[12:14])[0]

        if self.packet_version == 4 or self.packet_version == 5:

            self.position = list(unpack("fff", self.buffer[14:26]))
            self.atti = list(map(lambda x: x / (pi / 32768.0),
                                 unpack("hhh", self.buffer[26:32])))
            self.velocity = list(map(lambda x: x/10,
                                 unpack("hhh", self.buffer[32:38])))
            self.atti_velocity = list(map(lambda x: x / (pi / 32768.0),
                                 unpack("hhh", self.buffer[38:44])))
            self.smoke_oil = unpack("h", self.buffer[44:46])[0]

            self.fuel = unpack("I", self.buffer[46:50])[0]

            self.payload = unpack("h", self.buffer[50:52])[0]

            self.flight_state, self.vgw = unpack("BB", self.buffer[52:54])
            self.vgw = self.vgw / 255.0

            c = unpack("B", self.buffer[54:55])[0]
            self.spoiler = (c >> 4 & 15) / 15.0 #Bitshift 4 to the right, then mask with 15
            self.landing_gear = (c & 15) / 15.0 #Mask with 15

            c = unpack("B", self.buffer[55:56])[0]
            self.flap = (c >> 4 & 15) / 15.0
            self.brake = (c & 15) / 15.0

            flags = unpack("h", self.buffer[56:58])[0]
            self.flags["ab"] = bool(flags & 1) # Last bit
            self.flags["firing"] = bool(flags &8)
            self.flags["smoke"] = 0

            if flags & 2:
                self.flags["smoke"] = (flags >> 8) & 255 # bitshift 8 to the right, 
                #then mask with 255
                if self.flags["smoke"] == 0:
                    self.flags["smoke"] = 255 # Need to review what this actuall does!
            if flags & 16:
                self.flags["beacon"] = True
            if flags & 32:
                self.flags["nav_lights"] = True
            if flags & 64:
                self.flags["strobe"] = True
            if flags & 128:
                self.flags["landing_lights"] = True

            self.gun_ammo, self.rocket_ammo, self.aam, self.agm, self.bomb = unpack("HHBBB", self.buffer[58:65])
            self.life = unpack("B", self.buffer[65:66])[0]

            self.g_value = unpack("b", self.buffer[66:67])[0]/10.0

            self.throttle = unpack("B", self.buffer[67:68])[0]/99.0
            self.elev = unpack("b", self.buffer[68:69])[0]/99.0
            self.ail = unpack("b", self.buffer[69:70])[0]/99.0
            self.rud = unpack("b", self.buffer[70:71])[0]/99.0
            self.trim = unpack("b", self.buffer[71:72])[0]/99.0

            if self.packet_version == 4:
                c = unpack("B", self.buffer[71:72])[0]
                self.thrust_vector["vector"] = (c >> 4 & 15) / 15.0
                self.thrust_vector["reverser"] = (c & 15) / 15.0
                c = unpack("B", self.buffer[72:73])[0]
                self.bomb_bay_info = (c >> 4 & 15) / 15.0

        else:

            self.position = list(unpack("fff", self.buffer[16:28]))
            self.atti = list(map(lambda x: x / (pi / 32768.0),
                                 unpack("hhh", self.buffer[28:34])))
            
            self.velocity = list(map(lambda x: x/10,
                                    unpack("hhh", self.buffer[34:40])))
            
            self.atti_velocity = list(map(lambda x: x / (pi / 32768.0),
                                          unpack("hhh", self.buffer[40:46])))
            self.g_value = unpack("h", self.buffer[46:48])[0]/100.0

            self.gun_ammo, self.aam, self.agm, self.bomb, self.smoke_oil = unpack("hhhhh", self.buffer[48:58])
            self.fuel = unpack("f", self.buffer[58:62])[0]
            self.payload = unpack("f", self.buffer[62:66])[0]

            self.life = unpack("h", self.buffer[66:68])[0]

            self.flight_state, self.vgw = unpack("BB", self.buffer[68:70])
            self.vgw = self.vgw / 255.0
            self.spoiler = unpack("B", self.buffer[70:71])[0]/255.0
            self.landing_gear = unpack("B", self.buffer[71:72])[0]/255.0
            self.flap = unpack("B", self.buffer[72:73])[0]/255.0
            self.brake = unpack("B", self.buffer[73:74])[0]/255.0

            flags = unpack("H", self.buffer[74:76])[0]
            self.flags["ab"] = bool(flags & 1)
            self.flags["firing"] = bool(flags & 8)
            self.flags["smoke"] = 0
            if flags & 2:
                self.flags["smoke"] = (flags >> 8) & 255
                if self.flags["smoke"] == 0:
                    self.flags["smoke"] = 255

            self.throttle = unpack("B", self.buffer[76:77])[0]/99.0
            self.elev = unpack("b", self.buffer[77:78])[0]/99.0
            self.ail = unpack("b", self.buffer[78:79])[0]/99.0
            self.rud = unpack("b", self.buffer[79:80])[0]/99.0
            self.trim = unpack("b", self.buffer[80:81])[0]/99.0

            self.rocket_ammo = unpack("H", self.buffer[81:83])[0]

            if self.packet_version >= 1:

                self.atti_velocity = list(map(lambda x: x / (pi / 32768.0),
                                          unpack("fff", self.buffer[83:95])))

            if self.packet_version >= 2:
                self.thrust_vector["vector"] = unpack("B", self.buffer[95:96])[0]/255.0
                self.thrust_vector["reverser"] = unpack("B", self.buffer[96:97])[0]/255.0
                self.bomb_bay_info = unpack("B", self.buffer[97:98])[0]/255.0

    @staticmethod
    def get_life(buffer:bytes):
        version = unpack("h", buffer[12:14])[0]
        if version == 5 or version == 4:
            return unpack("B", buffer[65:66])[0]
        else:
            return unpack("H", buffer[66:68])[0]


    @staticmethod
    def encode(remote_time, player_id, packet_version, position, atti, velocity, atti_velocity,
               smoke_oil, fuel, payload, flight_state, vgw, spoiler, landing_gear, flap, brake,
               flags, gun_ammo, rocket_ammo, aam, agm, bomb, life, g_value, throttle, elev, ail, rud,
               trim, thrust_vector, bomb_bay_info, with_size:bool=False):
        buffer = pack("IfI", 11, remote_time, player_id)
        buffer += pack("H", packet_version)
        if packet_version == 4 or packet_version == 5:
            buffer += pack("fffhhhhhhhhh", *position, *atti, *velocity, *atti_velocity)
            buffer += pack("hhhh", smoke_oil, fuel, payload, 0)
            buffer += pack("BB", flight_state, int(vgw*255))
            buffer += pack("BB", int(spoiler*15)<<4 | int(landing_gear*15), int(flap*15)<<4 | int(brake*15))
            flagschar = 0
            if flags["ab"]:
                flagschar |= 1
            if flags["firing"]:
                flagschar |= 8
            if flags["smoke"]:
                flagschar |= flags["smoke"] << 8
            if flags["beacon"]:
                flagschar |= 16
            if flags["nav_lights"]:
                flagschar |= 32
            if flags["strobe"]:
                flagschar |= 64
            if flags["landing_lights"]:
                flagschar |= 128
            buffer += pack("h", flagschar)
            buffer += pack("HHBBB", gun_ammo, rocket_ammo, aam, agm, bomb)
            buffer += pack("B", life)
            buffer += pack("b", int(g_value*10))
            buffer += pack("B", int(throttle*99))
            buffer += pack("b", int(elev*99))
            buffer += pack("b", int(ail*99))
            buffer += pack("b", int(rud*99))
            buffer += pack("b", int(trim*99))

            if packet_version == 4:
                buffer += pack("BB", int(thrust_vector["vector"]*15)<<4 | int(thrust_vector["reverser"]*15),
                    int(bomb_bay_info*15))

        else:
            buffer += pack("fffhhhfff", *position, *atti, *velocity, *atti_velocity)
            buffer += pack("HHHHH", gun_ammo, aam, agm, bomb, smoke_oil)
            buffer += pack("f", payload)
            buffer += pack("H", life)
            buffer += pack("BB", flight_state, int(vgw*255))
            buffer += pack("BBBB", int(spoiler*15), int(landing_gear*15),
                int(flap*15), int(brake*15))
            flagschar = 0
            if flags["ab"]:
                flagschar |= 1
            if flags["firing"]:
                flagschar |= 8
            if flags["smoke"]:
                flagschar |= flags["smoke"] << 8
            buffer += pack("H", flagschar)
            buffer += pack("B", int(throttle*99))
            buffer += pack("b", int(elev*99))
            buffer += pack("b", int(ail*99))
            buffer += pack("b", int(rud*99))
            buffer += pack("b", int(trim*99))
            buffer += pack("H", rocket_ammo)
            if packet_version >= 1:
                buffer += pack("fff", *atti_velocity)
            if packet_version >= 2:
                buffer += pack("BBB", int(thrust_vector["vector"]*255), int(thrust_vector["reverser"]*255),
                    int(bomb_bay_info*255))

        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer
