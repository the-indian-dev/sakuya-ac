class Player:
    def __init__(self,username, playerId, x, y, z, throttle, aam, agm,
                gunAmmo, rktAmmo, fuel, ipAddr, life, vx, vy, vz, gValue):
        self.username = username
        self.ip = ipAddr
        self.playerId = playerId
        self.x = x
        self.y = y
        self.z = z
        self.throttle = throttle
        self.aam = aam
        self.agm = agm
        self.gunAmmo = gunAmmo
        self.rktAmmo = rktAmmo
        self.fuel = fuel
        self.life = life
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.gValue = gValue

    def __str__(self):
        return f"Username: {self.username}, IP: {self.ip}, " \
               f"Player ID: {self.playerId}, X: {self.x}, Y: {self.y}, Z: {self.z}, " \
               f"Throttle: {self.throttle}, AAM: {self.aam}, AGM: {self.agm}, " \
               f"Gun Ammo: {self.gunAmmo}, Rocket Ammo: {self.rktAmmo}, Fuel: {self.fuel}" \
                f"Life: {self.life}, gValue: {self.gValue}"
