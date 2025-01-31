from struct import unpack, pack
from math import pi

MESSAGE_TYPES = [
    "FSNETCMD_NULL",                   #   0
    "FSNETCMD_LOGON",                  #   1 Cli ->Svr",  (Svr->Cli for log-on complete acknowledgement.)
    "FSNETCMD_LOGOFF",                 #   2
    "FSNETCMD_ERROR",                  #   3
    "FSNETCMD_LOADFIELD",              #   4 Svr ->Cli",   Cli->Svr for read back
    "FSNETCMD_ADDOBJECT",              #   5 Svr ->Cli
    "FSNETCMD_READBACK",               #   6 Svr<->Cli
    "FSNETCMD_SMOKECOLOR",             #   7 Svr<->Cli
    "FSNETCMD_JOINREQUEST",            #   8 Svr<- Cli
    "FSNETCMD_JOINAPPROVAL",           #   9 Svr ->Cli
    "FSNETCMD_REJECTJOINREQ",          #  10
    "FSNETCMD_AIRPLANESTATE",          #  11 Svr<->Cli   # Be careful in FsDeleteOldStatePacket when modify
    "FSNETCMD_UNJOIN",                 #  12 Svr<- Cli
    "FSNETCMD_REMOVEAIRPLANE",         #  13 Svr<->Cli
    "FSNETCMD_REQUESTTESTAIRPLANE",    #  14
    "FSNETCMD_KILLSERVER",             #  15 Svr<- Cli
    "FSNETCMD_PREPARESIMULATION",      #  16 Svr ->Cli
    "FSNETCMD_TESTPACKET",             #  17
    "FSNETCMD_LOCKON",                 #  18 Svr<->Cli
    "FSNETCMD_REMOVEGROUND",           #  19 Svr<->Cli
    "FSNETCMD_MISSILELAUNCH",          #  20 Svr<->Cli   # fsweapon.cpp is responsible for encoding/decoding
    "FSNETCMD_GROUNDSTATE",            #  21 Svr<->Cli   # Be careful in FsDeleteOldStatePacket when modify
    "FSNETCMD_GETDAMAGE",              #  22 Svr<->Cli
    "FSNETCMD_GNDTURRETSTATE",         #  23 Svr<->Cli
    "FSNETCMD_SETTESTAUTOPILOT",       #  24 Svr ->Cli
    "FSNETCMD_REQTOBESIDEWINDOWOFSVR", #  25 Svr<- Cli
    "FSNETCMD_ASSIGNSIDEWINDOW",       #  26 Svr ->Cli
    "FSNETCMD_RESENDAIRREQUEST",       #  27 Svr<- Cli
    "FSNETCMD_RESENDGNDREQUEST",       #  28 Svr<- Cli
    "FSNETCMD_VERSIONNOTIFY",          #  29 Svr ->Cli
    "FSNETCMD_AIRCMD",                 #  30 Svr<->Cli   # After 2001/06/24
    "FSNETCMD_USEMISSILE",             #  31 Svr ->Cli   # After 2001/06/24
    "FSNETCMD_TEXTMESSAGE",            #  32 Svr<->Cli
    "FSNETCMD_ENVIRONMENT",            #  33 Svr<->Cli  (*1)
    "FSNETCMD_NEEDRESENDJOINAPPROVAL", #  34 Svr<- Cli
    "FSNETCMD_REVIVEGROUND",           #  35 Svr ->Cli   # After 2004
    "FSNETCMD_WEAPONCONFIG",           #  36 Svr<->Cli   # After 20040618
    "FSNETCMD_LISTUSER",               #  37 Svr<->Cli   # After 20040726
    "FSNETCMD_QUERYAIRSTATE",          #  38 Cli ->Svr   # After 20050207
    "FSNETCMD_USEUNGUIDEDWEAPON",      #  39 Svr ->Cli   # After 20050323
    "FSNETCMD_AIRTURRETSTATE",         #  40 Svr<->Cli   # After 20050701
    "FSNETCMD_CTRLSHOWUSERNAME",       #  41 Svr ->Cli   # After 20050914
    "FSNETCMD_CONFIRMEXISTENCE",       #  42 Not Used
    "FSNETCMD_CONFIGSTRING",           #  43 Svr ->Cli   # After 20060514    Cli->Svr for read back
    "FSNETCMD_LIST",                   #  44 Svr ->Cli   # After 20060514    Cli->Svr for read back
    "FSNETCMD_GNDCMD",                 #  45 Svr<->Cli
    "FSNETCMD_REPORTSCORE",            #  46 Svr -> Cli  # After 20100630    (Older version will ignore)
    "FSNETCMD_SERVER_FORCE_JOIN",      #  47 Svr -> Cli
    "FSNETCMD_FOGCOLOR",               #  48 Svr -> Cli
    "FSNETCMD_SKYCOLOR",               #  49 Svr -> Cli
    "FSNETCMD_GNDCOLOR",               #  50 Svr -> Cli
    "FSNETCMD_RESERVED_FOR_LIGHTCOLOR",#  51 Svr -> Cli
    "FSNETCMD_GENERATEATTACKER",             #  52
    "FSNETCMD_RESERVED22",             #  53
    "FSNETCMD_RESERVED23",             #  54
    "FSNETCMD_RESERVED24",             #  55
    "FSNETCMD_RESERVED25",             #  56
    "FSNETCMD_RESERVED26",             #  57
    "FSNETCMD_RESERVED27",             #  58
    "FSNETCMD_RESERVED28",             #  59
    "FSNETCMD_RESERVED29",             #  60
    "FSNETCMD_RESERVED30",             #  61
    "FSNETCMD_RESERVED31",             #  62
    "FSNETCMD_RESERVED32",             #  63
    "FSNETCMD_OPENYSF_RESERVED33",     #  64 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED34",     #  65 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED35",     #  66 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED36",     #  67 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED37",     #  68 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED38",     #  69 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED39",     #  70 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED40",     #  71 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED41",     #  72 Reserved for OpenYSF
    "FSNETCMD_OPENYSF_RESERVED42",     #  73 Reserved for OpenYSF
    "FSNETCMD_RESERVED43",             #  74
    "FSNETCMD_RESERVED44",             #  75
    "FSNETCMD_RESERVED45",             #  76
    "FSNETCMD_RESERVED46",             #  77
    "FSNETCMD_RESERVED47",             #  78
    "FSNETCMD_RESERVED48",             #  79
    "FSNETCMD_RESERVED49",             #  80
    "FSNETCMD_NOP"
]

READBACKS = ["FSNETREADBACK_ADDAIRPLANE",
    "FSNETREADBACK_ADDGROUND",
    "FSNETREADBACK_REMOVEAIRPLANE",
    "FSNETREADBACK_REMOVEGROUND",
    "FSNETREADBACK_ENVIRONMENT",
    "FSNETREADBACK_JOINREQUEST",
    "FSNETREADBACK_JOINAPPROVAL",
    "FSNETREADBACK_PREPARE",
    "FSNETREADBACK____UNUSED____",
    "FSNETREADBACK_USEMISSILE",
    "FSNETREADBACK_USEUNGUIDEDWEAPON",
    "FSNETREADBACK_CTRLSHOWUSERNAME"]

FSWEAPON_DICT = {
    0: "FSWEAPON_GUN",
    1: "FSWEAPON_AIM9",
    2: "FSWEAPON_AGM65",
    3: "FSWEAPON_BOMB",
    4: "FSWEAPON_ROCKET",
    5: "FSWEAPON_FLARE",
    6: "FSWEAPON_AIM120",
    7: "FSWEAPON_BOMB250",
    8: "FSWEAPON_SMOKE",
    9: "FSWEAPON_BOMB500HD",
    10: "FSWEAPON_AIM9X",
    11: "FSWEAPON_FLAREPOD",
    12: "FSWEAPON_FUELTANK",
    13: "FSWEAPON_RESERVED13",
    14: "FSWEAPON_RESERVED14",
    15: "FSWEAPON_RESERVED15",
    16: "FSWEAPON_RESERVED16",
    17: "FSWEAPON_RESERVED17",
    18: "FSWEAPON_RESERVED18",
    19: "FSWEAPON_RESERVED19",
    20: "FSWEAPON_RESERVED20",
    21: "FSWEAPON_RESERVED21",
    22: "FSWEAPON_RESERVED22",
    23: "FSWEAPON_RESERVED23",
    24: "FSWEAPON_RESERVED24",
    25: "FSWEAPON_RESERVED25",
    26: "FSWEAPON_RESERVED26",
    27: "FSWEAPON_RESERVED27",
    28: "FSWEAPON_RESERVED28",
    29: "FSWEAPON_RESERVED29",
    30: "FSWEAPON_RESERVED30",
    31: "FSWEAPON_RESERVED31",
    32: "FSWEAPON_SMOKE0",
    33: "FSWEAPON_SMOKE1",
    34: "FSWEAPON_SMOKE2",
    35: "FSWEAPON_SMOKE3",
    36: "FSWEAPON_SMOKE4",
    37: "FSWEAPON_SMOKE5",
    38: "FSWEAPON_SMOKE6",
    39: "FSWEAPON_SMOKE7",
    40: "FSWEAPON_RESERVED40",
    41: "FSWEAPON_RESERVED41",
    42: "FSWEAPON_RESERVED42",
    43: "FSWEAPON_RESERVED43",
    44: "FSWEAPON_RESERVED44",
    45: "FSWEAPON_RESERVED45",
    46: "FSWEAPON_RESERVED46",
    47: "FSWEAPON_RESERVED47",
    48: "FSWEAPON_NUMWEAPONTYPE",
    127: "FSWEAPON_NULL",
    128: "FSWEAPON_DEBRIS",
    200: "FSWEAPON_FLARE_INTERNAL"
}

GUIDEDWEAPONS = missiles = ["FSWEAPON_AGM65", "FSWEAPON_AIM9", "FSWEAPON_AIM120",
                            "FSWEAPON_AIM9X", "FSWEAPON_ROCKET"]

ERROR_CODES = ["FSNETERR_NOERR",
	"FSNETERR_VERSIONCONFLICT",
	"FSNETERR_CANNOTADDOBJECT",
	"FSNETERR_REJECT",
	"FSNETERR_CANNOTSUSTAIN"]

def decode(buffer:bytes, with_size:bool=False, should_decode=True):
    """
    Takes incomming packets from client or server and decodes them.
    If with_size is True, then the packet size is included in the buffer.
    If decode is False, then the packet is just returned as is.
    If it is true, then the packet will be decoded.
    """

    if with_size:
        # Strips away the size, so we've just got the message.
        buffer = buffer[4:]

    # Pull out the message type
    msg_type = unpack("I", buffer[:4])[0]

    # Find message type on the message_types list
    if msg_type < len(MESSAGE_TYPES):
        msg_type = MESSAGE_TYPES[msg_type]
        packet_class = None
        if msg_type == "FSNETCMD_NULL":
            packet_class = FSNETCMD_NULL
        elif msg_type == "FSNETCMD_LOGON":
            packet_class = FSNETCMD_LOGON
        elif msg_type == "FSNETCMD_LOGOFF":
            packet_class = FSNETCMD_LOGOFF
        elif msg_type == "FSNETCMD_ERROR":
            packet_class = FSNETCMD_ERROR
        elif msg_type == "FSNETCMD_LOADFIELD":
            packet_class = FSNETCMD_LOADFIELD
        elif msg_type == "FSNETCMD_ADDOBJECT":
            packet_class = FSNETCMD_ADDOBJECT
        elif msg_type == "FSNETCMD_READBACK":
            packet_class = FSNETCMD_READBACK

        if packet_class:
            return packet_class(buffer, should_decode)
        return None

    return None


class FSNETCMD_NULL: #0
    """
    This is a 'null' packet, there is nothing to process.
    """
    def __init__(self,buffer:bytes, should_decode:bool=True):
        pass

    def decode(self):
        return None

    def encode(self, with_size:bool=False):
        if with_size:
            return pack("II",4,0)
        return pack("I", 0)


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


class FSNETCMD_LOGOFF: #2
    """
    This is a logoff packet, used to logoff from the server.
    It appeasr to be un-used by YS. Including it for completeness.
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer

    def decode(self):
        pass

    @staticmethod
    def encode( with_size:bool=False):
        buffer = pack("I",2)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer


class FSNETCMD_ERROR: #3
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.error_code = None
        self.error_message = None
        if should_decode:
            self.decode()

    def decode(self):
        errorCode = unpack("I",self.buffer[4:8])[0]
        if errorCode < len(ERROR_CODES):
            self.error_message = ERROR_CODES[errorCode]

    @staticmethod
    def encode(error_code, with_size:bool=False):
        buffer = pack("I",3)+pack("I",error_code)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer


class FSNETCMD_LOADFIELD: #4
    """
    This packet is sent by the server along with the field info. When received,
    the client replies with the same packet.
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.field = None
        self.fieldShortName = None
        self.flags = None
        self.pos = [0,0,0]
        self.atti = [0,0,0]
        if len(buffer) == 64 and should_decode:
            self.decode()

    def decode(self):
        self.field, self.flags, self.pos[0], self.pos[1], self.pos[2], self.atti[0], self.atti[1], self.atti[2] = unpack("32sIffffff", self.buffer[4:])
        self.fieldShortName = self.field.split(b'\x00')[0].decode()

    @staticmethod
    def encode(field, flags, pos, atti, with_size:bool=False):
        buffer = pack("I32sIffffff", 4, field.encode(), flags, pos[0], pos[1],
                      pos[2], atti[0], atti[1], atti[2])
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer


class FSNETCMD_ADDOBJECT: #5
    """
    This packet is sent by the server to add an object to the client.
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.object_type = None
        self.net_type = None
        self.object_id = None
        self.iff = None
        self.pos = [0,0,0]
        self.atti = [0,0,0]
        self.identifier = None
        self.substrname = None
        self.ysfid = None
        self.flags = None
        self.flags0 = None
        self.outsideRadius = None
        self.aircraft_class = None
        self.aircraft_category = None
        self.pilot = None

        if len(buffer)>=120 and should_decode:
            self.decode()

    def decode(self):
        self.object_type, self.net_type = unpack("hh", self.buffer[4:8])
        #If object_type = 0, then it's an aircraft, and client will send
        # FSNETREADBACK_ADDAIRPLANE
        #If object_types = 1, then it's a ground object, and client will send
        # FSNETREADBACK_ADDGROUND
        self.object_id = unpack("I", self.buffer[8:12])[0]
        self.iff, _ = unpack("hh", self.buffer[12:16])
        self.pos = unpack("fff", self.buffer[16:28])
        self.atti = unpack("fff", self.buffer[28:40])
        self.identifier = unpack("32s", self.buffer[40:72])[0].decode().strip('\x00')
        self.substrname = unpack("32s", self.buffer[72:104])[0].decode().strip('\x00')
        self.ysfid = unpack("I", self.buffer[104:108])[0]
        self.flags, self.flags0 = unpack("II", self.buffer[108:116])
        self.outsideRadius = unpack("f", self.buffer[116:120])[0]

        if len(self.buffer)>=128:
            self.aircraft_class, self.aircraft_category = unpack("hh", self.buffer[120:124])
            #There is an extra short, but it's just set to 0
        if len(self.buffer) >= 176:
            self.pilot = unpack("32s", self.buffer[124:156])[0].decode().strip('\x00')

    @staticmethod
    def encode(object_type, net_type, object_id, iff, pos, atti, identifier, substrname, ysfid,
               flags, flags0, outside_radius, aircraft_class=None, aircraft_category=None,
               pilot=None, with_size:bool=False):

        buffer = pack("IHHIHHfff32s32sIIIf", 5, object_type, net_type, object_id,
                      iff, 0, pos[0], pos[1], pos[2], atti[0], atti[1], atti[2],
                      identifier.encode(), substrname.encode(), ysfid, flags,
                      flags0, outside_radius)
        if aircraft_class and aircraft_category:
            buffer += pack("hhh", aircraft_class, aircraft_category, 0)
        if pilot:
            buffer += pack("32s", pilot.encode())
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer


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


class FSNETCMD_SMOKECOLOR: #7
    """The server sends this to the client when another aircraft
    joins with smoke, and the client sends it to the server if
    they're joining with smoke.
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.aircraft_id = None
        self.smoke_quantity = None
        self.color = None
        if should_decode:
            self.decode()

    def decode(self):
        self.aircraft_id, self.smoke_quantity, r, g, b = unpack("IBBBB", self.buffer[4:9])
        self.color = (r,g,b)

    @staticmethod
    def encode(aircraft_id, smoke_quantity, color, with_size:bool=False):
        buffer = pack("IIBBBB", 7, aircraft_id, smoke_quantity, color[0], color[1], color[2])
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer


class FSNETCMD_JOINREQUEST: #8
    """
    The client sends a join request to the server with their iff, aircraft, start position, fuel and smoke
    The server replies with the join request readback,The server replies with the join request readback
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.iff = None
        self.aircraft = None
        self.start_pos = None #It's the STP name
        self.fuel = None
        self.smoke = None
        if should_decode:
            self.decode()

    def decode(self):
        self.iff, _, self.aircraft, self.start_pos, _, self.fuel, self.smoke = unpack("HH32s32sHHH", self.buffer[4:78])
        self.start_pos = self.start_pos.decode().strip('\x00')
        self.aircraft = self.aircraft.decode().strip('\x00')

    @staticmethod
    def encode(iff, aircraft, start_pos, fuel, smoke, with_size:bool=False):
        buffer = pack("IHH32s32sHHH", 8, iff, 0, aircraft.encode(),
                      start_pos.encode(), 0, fuel, smoke)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer


class FSNETCMD_JOINAPPROVAL: #9
    """
    When the server sends the "add aircraft" command, and
    receves the readback from the client, they'll send this
    It's an empty packet, but can be useful to know the client is about to join.
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        if should_decode:
            self.decode()

    def decode(self):
        pass

    @staticmethod
    def encode(with_size:bool=False):
        buffer = pack("I",9)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer


class FSNETCMD_REJECTJOINREQ: #10
    """
    If the server rejects the join request, they'll send this.
    It's usually followed by a chat message saying why.
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        if should_decode:
            self.decode()

    def decode(self):
        pass

    @staticmethod
    def encode(with_size:bool=False):
        buffer = pack("I",10)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer

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
        self.packet_version = unpack("H", self.buffer[16:18])[0]
        if self.packet_version == 4 or self.packet_version == 5:

            self.position = list(unpack("fff", self.buffer[18:30]))
            self.atti = list(map(lambda x: x / (pi / 32768.0),
                                 unpack("hhh", self.buffer[30:36])))
            self.velocity = list(map(lambda x: x/10,
                                 unpack("hhh", self.buffer[36:42])))
            self.atti_velocity = list(map(lambda x: x / (pi / 32768.0),
                                 unpack("hhh", self.buffer[42:48])))
            self.smoke_oil, self.fuel, self.payload, _ = unpack("hhhh", self.buffer[48:56])

            self.flight_state, self.vgw = unpack("BB", self.buffer[56:58])
            self.vgw = self.vgw / 255.0

            c = unpack("B", self.buffer[58:59])[0]
            self.spoiler = (c >> 4 & 15) / 15.0 #Bitshift 4 to the right, then mask with 15
            self.landing_gear = (c & 15) / 15.0 #Mask with 15

            c = unpack("B", self.buffer[59:60])[0]
            self.flap = (c >> 4 & 15) / 15.0
            self.brake = (c & 15) / 15.0

            flags = unpack("h", self.buffer[60:62])[0]
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

            self.gun_ammo, self.rocket_ammo, self.aam, self.agm, self.bomb = unpack("HHBBB", self.buffer[62:68])
            self.life = unpack("B", self.buffer[68:69])[0]

            self.g_value = unpack("b", self.buffer[69:70])[0]/10.0

            self.throttle = unpack("B", self.buffer[70:71])[0]/99.0
            self.elev = unpack("b", self.buffer[71:72])[0]/99.0
            self.ail = unpack("b", self.buffer[72:73])[0]/99.0
            self.rud = unpack("b", self.buffer[73:74])[0]/99.0
            self.trim = unpack("b", self.buffer[74:75])[0]/99.0

            if self.packet_version == 4:
                c = unpack("B", self.buffer[75:76])[0]
                self.thrust_vector["vector"] = (c >> 4 & 15) / 15.0
                self.thrust_vector["reverser"] = (c & 15) / 15.0
                c = unpack("B", self.buffer[76:77])[0]
                self.bomb_bay_info = (c >> 4 & 15) / 15.0
        
        else:
            
            self.position = list(unpack("fff", self.buffer[20:32]))
            self.atti = list(map(lambda x: x / (pi / 32768.0),
                                 unpack("hhh", self.buffer[32:38])))
            
            self.velocity = list(map(lambda x: x/10,
                                    unpack("hhh", self.buffer[38:44])))
            
            self.atti_velocity = list(map(lambda x: x / (pi / 32768.0),
                                          unpack("hhh", self.buffer[44:50])))
            self.g_value = unpack("h", self.buffer[50:52])[0]/100.0

            self.gun_ammo, self.aam, self.agm, self.bomb, self.smoke_oil = unpack("HHHHH", self.buffer[52:62])

            self.payload = unpack("f", self.buffer[62:66])[0]

            self.life = unpack("H", self.buffer[66:68])[0]

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
    def encode(remote_time, player_id, packet_version, position, atti, velocity, atti_velocity,
               smoke_oil, fuel, payload, flight_state, vgw, spoiler, landing_gear, flap, brake,
               flags, gun_ammo, rocket_ammo, aam, agm, bomb, life, g_value, throttle, elev, ail, rud,
               trim, thrust_vector, bomb_bay_info, with_size:bool=False):
        buffer = pack("IfI", 11, remote_time, player_id)
        buffer += pack("H", packet_version)
        if packet_version == 4 or packet_version == 5:
            buffer += pack("fffhhhfff", *position, *atti, *velocity, *atti_velocity)
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


class FSNETCMD_UNJOIN: #12
    """
    This is sent client to server when the client leaves.
    The explosion doesn't seem to actually do anything in YS.
    There is a comment saying "add explosion here"... Not helpful.
    """
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.object_id = None
        self.explosion = None
        if should_decode:
            self.decode()

    def decode(self):
        variables = unpack("IIhh", self.buffer[0:12])
        self.object_id = variables[1]
        self.explosion = bool(variables[2])

    @staticmethod
    def encode(object_id, explosion, with_size:bool=False):
        buffer = pack("I", 12)+pack("IIhh", 12, object_id, explosion)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer


class FSNETCMD_REMOVEAIRPLANE(FSNETCMD_UNJOIN): #13
    """
    Seems to just be the same as 12. No idea why Soji made 2.
    We'll just extend UNJOIN."""
    @staticmethod
    def encode(object_id, explosion, with_size:bool=False):
        buffer = pack("I", 12)+pack("IIhh", 13, object_id, explosion)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer


class FSNETCMD_EMPTYPACKET:
    """
    A template function for empty packets"""
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        if should_decode:
            self.decode()
    
    def decode(self):
        pass # There are no messages in this packet!

    @staticmethod
    def encode(with_size:bool=False): #This will be extended by each func.
        buffer = pack("I",14)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer


class FSNETCMD_REQUESTTESTAIRPLANE(FSNETCMD_EMPTYPACKET): #14
    """
    Spawns an F-15C at NORTH1000_01 in dogfight mode
    There is no way of calling this from YS.
    """
    @staticmethod
    def encode(with_size:bool=False):
        buffer = pack("I",14)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer


class FSNETCMD_KILLSERVER(FSNETCMD_EMPTYPACKET): #15
    """
    This is unimplemented in YS, but it would shutdown the server
    The actual server functionality is disabled.
    """
    @staticmethod
    def encode(with_size:bool=False):
        buffer = pack("I",15)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer


class FSNETCMD_PREPARESIMULATION(FSNETCMD_EMPTYPACKET): #16
    """
    This is sent from server to client when they've almost finished
    logging in.
    """
    @staticmethod
    def encode(with_size:bool=False):
        buffer = pack("I",16)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer


class FSNETCMD_TESTPACKET(FSNETCMD_EMPTYPACKET): #17
    """
    This is just an empty packet.
    Just overwrite the encode.
    """
    @staticmethod
    def encode(with_size:bool=False):
        buffer = pack("I",17)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer

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


class FSNETCMD_REMOVEGROUND(FSNETCMD_UNJOIN): #19
    """
    This is the same as FSNETCMD_UNJOIN/Remove aircraft, but for ground objects.
    """
    @staticmethod
    def encode(object_id, explosion, with_size:bool=False):
        buffer =pack("I",19)+pack("IIhh", 19, object_id, explosion)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer


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
    def encode(weapon_type, position, atti, velocity, life_remaining, power, fired_by_aircraft, fired_by,
               v_max=None, mobility=None, radar=None, fired_at_aircraft=None, fired_at=None, with_size:bool=False):
        if weapon_type in FSWEAPON_DICT and isinstance(weapon_type,int):
            weapon_type_name = FSWEAPON_DICT[weapon_type]
        else:
            weapon_type_name = weapon_type
            weapon_type = list(FSWEAPON_DICT.keys())[list(FSWEAPON_DICT.values()).index(weapon_type)]
        buffer = pack("I",20)+pack("Hfff", weapon_type, *position)+pack("fff", *atti)+pack("ffH", velocity, life_remaining, power)

        if weapon_type_name in GUIDEDWEAPONS:
            buffer += pack("fff", v_max, mobility, radar)
            if isinstance(fired_at_aircraft, bool):
                fired_at_aircraft = int(fired_at_aircraft)
            buffer += pack("II", fired_by_aircraft, fired_by)
        if weapon_type_name == "FSWEAPON_FLARE":
            buffer += pack("f", v_max)
        
        if with_size:
            return pack("I",len(buffer))+buffer


