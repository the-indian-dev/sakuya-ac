# Black smoke, 50 fuel, no load extra
# Comptaible with every type of plane
# just before their death
#
from struct import pack

def undeadPatch(id:int, data:bytes):
    buffer = data[0:8] + pack("I", id) + data[12:]
    return buffer
