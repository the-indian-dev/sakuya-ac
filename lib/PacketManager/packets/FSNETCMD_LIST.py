from struct import unpack, pack
class FSNETCMD_LIST: #44
    def __init__(self, buffer:bytes, should_decode:bool=True):
        self.buffer = buffer
        self.list_type = None
        self.num_of_items = 0
        self.list = []
        if should_decode:
            self.decode()
    
    def decode(self):
        packet_type = unpack('I', self.buffer[:4])[0]
        self.list_type = unpack('B', self.buffer[4:5])[0]
        self.num_of_items = unpack('B', self.buffer[5:6])[0]
        #Then there is a spacer.
        _ = unpack('BB', self.buffer[6:8])
        self.list = self.buffer[8:].split(b'\x00')[:-1]

    @staticmethod
    def encode(list_type:int=1, list_buffer:bytes=b'', num_of_items:int=0, with_size:bool=False):
        #Max length of the packet is 1024 bytes.
        # 8+1 bytes for the header, leaving 1015 bytes for the list.
        buffer = pack('IBBBB', 44, list_type, num_of_items, 0, 0)
        buffer += list_buffer
        if with_size:
            return pack("I", len(buffer)) + buffer
        return buffer


class List_Constructor:
    """Takes a list of aircraft, and constructes a list of FSNETCMD_LIST packets for sending.
    If sending custom lists to clients, the client FSNETCMD_LIST reply must be blocked from the server
    and the server FSNETCMD_LIST command must also be blocked.
    """
    def __init__(self, aircraftList:list, with_size:bool=True):
        self.aircraftList = aircraftList
        self.packet_list = []
        self.num_of_packets = 0
        self.with_size = with_size
        self.construct_packets()

    def construct_packets(self):
        packet = b''
        packet_length = 0
        for aircraft in self.aircraftList:
            aircraft = aircraft.replace(' ', '_')
            aircraft = aircraft.encode() + b'\x00'
            if self.check_fit(packet, aircraft) and packet_length<32:
                packet += aircraft
                packet_length += 1
            else:
                packet = FSNETCMD_LIST.encode(1,packet, packet_length,self.with_size)
                self.packet_list.append(packet)
                packet = b''
                packet += aircraft
                self.num_of_packets += 1
                packet_length = 1
        #Append whatever is left over.
        if len(packet) > 0:
            packet = FSNETCMD_LIST.encode(1,packet, packet_length,self.with_size)
            self.packet_list.append(packet)
            self.num_of_packets += 1    

    def check_fit(self, packet, aircraft):
        if len(packet) + len(aircraft) + 1 > 1015:
            return False
        return True

    def get_packets(self):
        return self.packet_list
