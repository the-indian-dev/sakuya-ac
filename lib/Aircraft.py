from lib.PacketManager.packets import FSNETCMD_AIRPLANESTATE, FSNETCMD_AIRCMD
class Aircraft:
    """
    An aircraft class - this will hold the info from the Airplane state, weapons etc packets."""
    def __init__(self, parent=None):
        self.parent = parent
        self.name = ""
        self.position = [0,0,0]
        self.attitude = [0,0,0]
        self.initial_config = {}
        self.custom_config = {}
        self.life = -1
        self.prev_life = -1
        self.id = -1
        self.last_packet = None
    
    def reset(self):
        """Resets the aircraft"""
        self.name = ""
        self.position = [0,0,0]
        self.attitude = [0,0,0]
        self.initial_config = {}
        self.custom_config = {}
        self.life = -1
        self.prev_life = -1
        self.id = -1
        self.last_packet = None
    
    def set_position(self, position:list):
        """Sets the position of the aircraft from the Airplane state packet"""
        self.position = position

    def set_attitude(self, attitude:list):
        """Sets the attitude of the aircraft from the Airplane state packet"""
        self.attitude = attitude
    
    def get_position(self):
        """Returns the position of the aircraft"""
        return self.position
    
    def get_altitude(self):
        """Returns the altitude in m"""
        return self.position[2]
    
    def get_attitude(self):
        """Returns the attitude of the aircraft"""
        return self.attitude
    
    def set_initial_config(self, config:dict):
        """Sets the initial config of the aircraft"""
        for key in config:
            self.initial_config[key] = config[key]
        
    def get_initial_config_value(self, key:str):
        """Returns the value of the initial config"""
        if key in self.initial_config:
            return self.initial_config[key]
        
        return None
    
    def set_custom_config_value(self, key:str, value):
        """Sets a custom config value"""
        self.custom_config[key] = value
        #Send this to the client.
    
    def add_state(self, packet:FSNETCMD_AIRPLANESTATE):
        """Adds the state of the aircraft"""
        if packet.player_id != self.id:
            return None
        self.prev_life = self.life
        self.life = packet.life
        self.set_position(packet.position)
        self.set_attitude(packet.atti)
        self.last_packet = packet
        return packet
    
    def check_command(self,command:FSNETCMD_AIRCMD):
        """Checks the command"""
        if command.aircraft_id != self.id:
            return
        if command.command:
            self.initial_config[command.command[0]] = command.command[1]
        print(f"Command: {command.command}")
