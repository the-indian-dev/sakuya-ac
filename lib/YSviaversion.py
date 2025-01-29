from struct import pack

def genViaVersion(username: str, finalVersion: int):
    """
    Generates Packets for porting the version
    """
    padding = 16-len(username)
    byteUserame = []
    for char in username:
        byteUserame.append(char.encode('ascii'))
    return pack("II16cI", 24, 1, *byteUserame+(padding*[b"\x00"]), finalVersion)
