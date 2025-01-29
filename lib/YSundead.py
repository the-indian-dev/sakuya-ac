# Black smoke, 50 fuel, no load extra
# Comptaible with every type of plane
# just before their death
#
from struct import pack

def undeadPatch(id:int, data:bytes):
    buffer = data[0:8] + pack("I", id) + data[12:]
    return buffer

def smokedPlane(id:int):
    data = b'"\x00\x00\x00$\x00\x00\x00*\x03\x01\x00\x0c\x00\xc8\x00\x14\x00 \x00\x08!!\x00\x08!"\x00\x08!\x00\x00\xb8\x0b\xc8\x00\x14\x00'
    return undeadPatch(id, data)
