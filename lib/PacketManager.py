from struct import unpack, pack

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

ERROR_CODES = ["FSNETERR_NOERR",
	"FSNETERR_VERSIONCONFLICT",
	"FSNETERR_CANNOTADDOBJECT",
	"FSNETERR_REJECT",
	"FSNETERR_CANNOTSUSTAIN"]

def decode(buffer:bytes, with_size:bool=False):
    """
    Takes incomming packets from client or server and decodes them.
    """
    
    if with_size:
        # Strips away the size, so we've just got the message.
        buffer = buffer[4:]
    
    # Pull out the message type
    msg_type = unpack("I", buffer[:4])[0]

    # Find message type on the message_types list
    if msg_type < len(MESSAGE_TYPES):
        msg_type = MESSAGE_TYPES[msg_type]
    else:
        return "Unknown message type: {}".format(msg_type)
    

class FSNETCMD_NULL: #0
    """
    This is a 'null' packet, there is nothing to process.
    """
    def __init__(self,buffer:bytes):
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
    def __init__(self, buffer:bytes):
        self.buffer = buffer
        self.version = None
        self.username = None
        self.alias = None #Alias is the longer form of the username, if they're longer than 16 chars.
        
        #If the YS version is 2018 (or YSCE) then the server will reply with an empty packet on login-complete.
        if len(self.buffer)>5:
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
    def __init__(self, buffer:bytes):
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
    def __init__(self, buffer:bytes):
        self.buffer = buffer
        self.error_code = None
        self.error_message = None
        
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
    This packet is sent by the server along with the field info. When received, the client replies with the same packet.
    """
    def __init__(self, buffer:bytes):
        self.buffer = buffer
        self.field = None
        self.fieldShortName = None
        self.flags = None
        self.pos = [0,0,0]
        self.atti = [0,0,0]
        if len(buffer) == 64:
            self.decode()
    
    def decode(self):
        self.field, self.flags, self.pos[0], self.pos[1], self.pos[2], self.atti[0], self.atti[1], self.atti[2] = unpack("32sIffffff", self.buffer[4:])
        self.fieldShortName = self.field.split(b'\x00')[0].decode()
    
    @staticmethod
    def encode(field, flags, pos, atti, with_size:bool=False):
        buffer = pack("I32sIffffff", 4, field.encode(), flags, pos[0], pos[1], pos[2], atti[0], atti[1], atti[2])
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer

class FSNETCMD_ADDOBJECT: #5
    """
    This packet is sent by the server to add an object to the client.
    """
    def __init__(self, buffer:bytes):
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

        if len(buffer)>=120:
            self.decode()
        
    def decode(self):
        self.object_type, self.net_type = unpack("HH", self.buffer[4:8])
        #If object_type = 0, then it's an aircraft, and client will send FSNETREADBACK_ADDAIRPLANE
        #If object_types = 1, then it's a ground object, and client will send FSNETREADBACK_ADDGROUND
        self.object_id = unpack("I", self.buffer[8:12])[0]
        self.iff, padding = unpack("HH", self.buffer[12:16])
        self.pos = unpack("fff", self.buffer[16:28])
        self.atti = unpack("fff", self.buffer[28:40])
        self.identifier = unpack("32s", self.buffer[40:72])[0].decode().strip('\x00')
        self.substrname = unpack("32s", self.buffer[72:104])[0].decode().strip('\x00')
        self.ysfid = unpack("I", self.buffer[104:108])[0]
        self.flags, self.flags0 = unpack("II", self.buffer[108:116])
        self.outsideRadius = unpack("f", self.buffer[116:120])[0]

        if len(self.buffer)>=128:
            self.aircraft_class, self.aircraft_category = unpack("HH", self.buffer[120:124])
            #There is an extra short, but it's just set to 0
        if len(self.buffer) >= 176:
            self.pilot = unpack("32s", self.buffer[124:156])[0].decode().strip('\x00')

    @staticmethod
    def encode(object_type, net_type, object_id, iff, pos, atti, identifier, substrname, ysfid, flags, flags0, outside_radius, aircraft_class=None, aircraft_category=None, pilot=None, with_size:bool=False):
        buffer = pack("IHHIHHfff32s32sIIIf", 5, object_type, net_type, object_id, iff, 0, pos[0], pos[1], pos[2], atti[0], atti[1], atti[2], identifier.encode(), substrname.encode(), ysfid, flags, flags0, outside_radius)
        if aircraft_class and aircraft_category:
            buffer += pack("HHH", aircraft_class, aircraft_category, 0)
        if pilot:
            buffer += pack("32s", pilot.encode())
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer

class FSNETCMD_READBACK: #6
    """
    Sent from client to server and back to acknowledge various packets.

    *   Client sends FSNETREADBACK_ADDAIRPLAN or FSNETREADBACK_ADDGROUND to acknowledge FSNETCMD_ADDOBJECT
    *   Client sends FSNETREADBACK_REMOVEAIRPLANE or FSNETREADBACK_REMOVEGROUND to acknowledge FSNETCMD_REMOVEAIRPLANE or FSNETCMD_REMOVEGROUND
    *   Client sends FSNETREADBACK_ENVIRONMENT to acknowledge FSNETCMD_ENVIRONMENT
    *   Client sends FSNETREADBACK_JOINREQUEST to acknowledge FSNETCMD_JOINREQUEST
    *   Client sends FSNETREADBACK_PREPARE to acknowledge FSNETCMD_PREPARESIMULATION
    *   Client sends FSNETREADBACK_USEMISSILE to acknowledge FSNETCMD_USEMISSILE
    *   Client sends FSNETREADBACK_USEUNGUIDEDWEAPON to acknowledge FSNETCMD_USEUNGUIDEDWEAPON
    *   Client sends FSNETREADBACK_CTRLSHOWUSERNAME to acknowledge FSNETCMD_CTRLSHOWUSERNAME
        
    *   Server sends FSNETREADBACK_JOINREQUEST to acknowledge FSNETCMD_JOINREQUEST - Will punt the user if the server receives this from them
    

    """

    def __init__(self, buffer:bytes):
        self.buffer = buffer
        self.read_back_type = None
        self.read_back_param

        self.decode()
    
    def decode(self):
        self.read_back_type, padding, self.read_back_param = unpack("HHI", self.buffer[4:12])
    
    @staticmethod
    def encode(read_back_type, read_back_param, with_size:bool=False):
        buffer = pack("IHHI", 6, read_back_type, 0, read_back_param)
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer

