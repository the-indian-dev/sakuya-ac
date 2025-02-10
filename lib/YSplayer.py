class Player:
    def __init__(self,username, playerId, x, y, z, throttle, aam, agm,
                gunAmmo, rktAmmo, fuel, ipAddr, life, vx, vy, vz, gValue,
                streamWriterObject=None, warningSent=False, smokedAdded=False):
        self.username = username
        self.ip = ipAddr
        self.playerId = playerId
        self.position = [x, y, z]
        self.throttle = throttle
        self.aam = aam
        self.agm = agm
        self.gunAmmo = gunAmmo
        self.rktAmmo = rktAmmo
        self.fuel = fuel
        self.life = life
        self.velocity = [vx, vy, vz]
        self.gValue = gValue
        self.streamWriterObject = streamWriterObject
        self.warningSent = warningSent
        self.smokeAdded = smokedAdded

    def __str__(self):
        return f"Username: {self.username}, IP: {self.ip}, " \
               f"Player ID: {self.playerId}, X: {self.getX()}, Y: {self.getY()}, Z: {self.getZ()}, " \
               f"Throttle: {self.throttle}, AAM: {self.aam}, AGM: {self.agm}, " \
               f"Gun Ammo: {self.gunAmmo}, Rocket Ammo: {self.rktAmmo}, Fuel: {self.fuel}" \
                f"Life: {self.life}, gValue: {self.gValue}"
    
    def getX(self):
        return self.position[0]

    def getY(self):
        return self.position[1]
    
    def getZ(self):
        return self.position[2]
    
    def setX(self, x):
        self.position[0] = x
    
    def setY(self, y):
        self.position[1] = y
    
    def setZ(self, z):
        self.position[2] = z
        
    
