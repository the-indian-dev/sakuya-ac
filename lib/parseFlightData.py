from math import pi
from struct import unpack as up

# Authored by https://theindiandev.in
# Date : Jan 26 2025
# Not more than 80 characters per line

def parseFlightData(data: bytes):
    """
    Input  : Bytecode, Type 11 datapackets from ysflight server,
             do NOT strip the heading(first 8 octets)
    Output : tuple

    Tested only on 20150425 version of ysflight
    """
    # Assuming version(info1) = 5,4 when speed < 400kts
    # version(info1) = 3 when speed > 400kts OR just spawning in the server
    version = up("h", data[16:18])[0]
    if version == 5 or version == 4:
        tRemote = up("f", data[8:12])[0]       # Remote Timer from client
        playerId = up("I", data[12:16])[0]
        x,y,z = up("fff", data[18:30])
        # Heading, Pitch and Bank values are correct but cannot be interepeted
        # correctly
        # FIXME
        h, p, b = up("hhh", data[30:36])
        heading = (h*pi/32768.0)
        aoa = (p*pi/32768.0)
        bank = (b*pi/32760.0)
        vx, vy, vz = up("hhh", data[36:42])
        # FIXME : Unkown padding of 2 bytes, it seems to be from the fuel as a
        # integer however correct values only with a short
        smokeOil, fuel, payload, _ = up("hhhh", data[48:56])
        flightState, vgw = up("BB", data[56:58])
        gunAmmo, rktAmmo = up("hh", data[62:66])
        # FIXME : aam count incorrect
        aam, agm, bomb, life = up("BBBB", data[66:70]) # aam, agm, bomb, life
        gValue = (up("B", data[70:71])[0])/10
        throttle, elev, ail, rud, trim, bombBayInfo = up("BBBBBB", data[71:77])
    elif version == 3:
        tRemote = up("f", data[8:12])[0]
        playerId = up("I", data[12:16])[0]
        x,y,z = up("fff", data[20:32])
        h, p, b = up("hhh", data[32:38])
        heading = (h*pi/32768.0)
        aoa = (p*pi/32768.0)
        bank = (b*pi/32760.0)
        vx, vy, vz = up("hhh", data[38:44])
        gValue = (up("h", data[50:52])[0])/100
        gunAmmo, aam, agm, bomb, smokeOil = up("5h", data[52:62])
        fuel, payload = up("2f", data[62:70])
        life = up("h", data[70:72])[0]
        flightState, vgw = up("BB", data[72:74])
        throttle, elev, ail, rud, trim = up("B4c", data[80:85])
        rktAmmo = up("h", data[85:87])[0]
        bombBayInfo = up("B", data[89:90])[0]
    else:
        print(f"Unkown version {version}")
        print("Payload Dump:")
        print(data)
        raise ValueError("Unknown version of ysflight")


    return (tRemote, playerId, x, y, z, heading, aoa, bank, vx, vy, vz,
            smokeOil, fuel, payload, flightState, vgw, gunAmmo, rktAmmo,
            aam, agm, bomb, life, throttle, elev, ail, rud, trim,
            bombBayInfo, gValue)
