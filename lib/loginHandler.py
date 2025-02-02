class Login:
    def __init__(self):
        self.lastPacket = b''
        self.loggedIn = False

    def setLastPacket(self, newPacket):
        """
        Sets the latest packet
        input : newest packet
        output : None
        """
        self.lastPacket = newPacket

    def verifyIntegrity(self, packet):
        """
        Verifies intigrity of the packet recived right now
        input : packet
        output : (bool) True if Tampered; vice versa
        """
        return packet == self.lastPacket

    def logInComplete(self):
        self.loggedIn = True
