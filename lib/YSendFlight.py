from struct import pack
from lib.YSchat import reply

def endFlight(id: int):
    buffer = pack("Ih", id, 0)
    return reply(12, buffer)
