from struct import pack, unpack

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
        self.object_type, self.net_type = unpack("HH", self.buffer[4:8])
        #If object_type = 0, then it's an aircraft, and client will send
        # FSNETREADBACK_ADDAIRPLANE
        #If object_types = 1, then it's a ground object, and client will send
        # FSNETREADBACK_ADDGROUND
        self.object_id = unpack("I", self.buffer[8:12])[0]
        self.iff, _ = unpack("hh", self.buffer[12:16])
        self.pos = list(unpack("fff", self.buffer[16:28]))
        self.atti = list(unpack("fff", self.buffer[28:40]))
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
    
    def to_dict(self):
        return {
            "object_type": self.object_type,
            "net_type": self.net_type,
            "object_id": self.object_id,
            "iff": self.iff,
            "pos": self.pos,
            "atti": self.atti,
            "identifier": self.identifier,
            "substrname": self.substrname,
            "ysfid": self.ysfid,
            "flags": self.flags,
            "flags0": self.flags0,
            "outside_radius": self.outsideRadius,
            "aircraft_class": self.aircraft_class,
            "aircraft_category": self.aircraft_category,
            "pilot": self.pilot
        }

    def to_packet(self, with_size:bool=True):
        return FSNETCMD_ADDOBJECT.encode(self.object_type, self.net_type,
                                         self.object_id, self.iff, self.pos,
                                         self.atti, self.identifier, self.substrname,
                                         self.ysfid, self.flags, self.flags0,
                                         self.outsideRadius, self.aircraft_class,
                                         self.aircraft_category, self.pilot, with_size)
    
    @staticmethod
    def encode(object_type, net_type, object_id, iff, pos, atti, identifier, substrname, ysfid,
               flags, flags0, outside_radius, aircraft_class=None, aircraft_category=None,
               pilot=None, with_size:bool=False):

        buffer = pack('IHH', 5, object_type, net_type)
        buffer += pack('IHHffffff', object_id, iff, 0, pos[0], pos[1], pos[2], atti[0], atti[1], atti[2])
        buffer += pack('32s32sI', identifier.encode(), substrname.encode(), ysfid)
        buffer += pack('II', flags, flags0)
        buffer += pack('f', outside_radius)
        
        if aircraft_class and aircraft_category:
            buffer += pack("hhh", aircraft_class, aircraft_category, 0)
        if pilot:
            buffer += pack("32s", pilot.encode())
        if with_size:
            return pack("I",len(buffer))+buffer
        return buffer