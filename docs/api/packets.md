# Introduction

Packet objects provide an easy interface to decode and encode the
packet data. These can then be used for interaction with the
YSFlight server.

All Packet objects are stored in ``lib.PacketManager.packets``.

# Packet Object Reference

## FSNETCMD_ADDOBJECT

This packet is sent by the server to add an object to the client.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `object_type`: `int`, optional
    *   The type of object being added.
    *   0: Aircraft
    *   1: Ground Object
*   `net_type`: `int`, optional
    *   The network type of the object.
*   `object_id`: `int`, optional
    *   Unique identifier for the object.
*   `iff`: `int`, optional
    *   Identification Friend or Foe status of the object.
*   `pos`: `list[float]`, optional, size: 3
    *   The 3D position of the object [x, y, z].
*   `atti`: `list[float]`, optional, size: 3
    *   The 3D attitude of the object [roll, pitch, yaw].
*   `identifier`: `str`, optional, size: 32
    *   Identifier string for the object.
*   `substrname`: `str`, optional, size: 32
    *   Sub-string name for the object.
*   `ysfid`: `int`, optional
    *   YSF Identifier of the object.
*   `flags`: `int`, optional
    *   Flags associated with the object.
*   `flags0`: `int`, optional
    *   Additional flags associated with the object.
*   `outsideRadius`: `float`, optional
    *   The outside radius of the object.
*   `aircraft_class`: `int`, optional
    *   Class of the aircraft (only present if buffer length is sufficient).
*   `aircraft_category`: `int`, optional
    *   Category of the aircraft (only present if buffer length is sufficient).
*   `pilot`: `str`, optional, size: 32
    *   Name of the pilot (only present if buffer length is sufficient).
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_ADDOBJECT` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Uses `struct.unpack` to interpret the byte data.
    *   Returns: `None`

*   `encode(object_type, net_type, object_id, iff, pos, atti, identifier, substrname, ysfid, flags, flags0, outside_radius, aircraft_class=None, aircraft_category=None, pilot=None, with_size: bool = False)`
    *   Encodes the provided parameters into a byte buffer representing the `FSNETCMD_ADDOBJECT` packet.
    *   Uses `struct.pack` to create the byte data.
    *   Parameters:
        *   `object_type`: `int`
            *   The type of object.
        *   `net_type`: `int`
            *   The network type.
        *   `object_id`: `int`
            *   The object ID.
        *   `iff`: `int`
            *   The IFF status.
        *   `pos`: `list[float]`
            *   The 3D position.
        *   `atti`: `list[float]`
            *   The 3D attitude.
        *   `identifier`: `str`
            *   The object identifier.
        *   `substrname`: `str`
            *   The sub-string name.
        *   `ysfid`: `int`
            *   The YSF ID.
        *   `flags`: `int`
            *   Flags.
        *   `flags0`: `int`
            *   Additional flags.
        *   `outside_radius`: `float`
            *   Outside radius.
        *   `aircraft_class`: `int`, optional
            *   Aircraft class (optional).
        *   `aircraft_category`: `int`, optional
            *   Aircraft category (optional).
        *   `pilot`: `str`, optional
            *   Pilot name (optional).
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.


## FSNETCMD_AIRCMD

This packet is used to send aircraft commands to the client.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `aircraft_id`: `int`, optional
    *   The ID of the aircraft to which the command is directed.
*   `message`: `str`, optional
    *   The raw message string sent in the packet.
*   `command`: `tuple[str, str]`, optional
    *   If the message starts with '*', this attribute will be populated with a tuple:
        *   `command[0]`: `str` - The command keyword (extracted from `AIRCMD_KEYWORDS`).
        *   `command[1]`: `str` - The value associated with the command.
        *   If the message does not start with '*', this will be `None`.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_AIRCMD` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Extracts `aircraft_id` and `message` from the buffer.
    *   Calls `get_command_from_message` if the message starts with '*'.
    *   Returns: `None`

*   `get_command_from_message(self, message: str)`
    *   Parses a message string to extract engine command information.
    *   Expected message format: `"*<code> <value>"`
    *   Looks up the command keyword in `AIRCMD_KEYWORDS` using the `code`.
    *   Parameters:
        *   `message`: `str`
            *   The message string to parse.
    *   Returns: `tuple[str, str]`, optional
        *   A tuple containing the command keyword and value if parsing is successful.
        *   Returns `None` if the `engine_code` cannot be converted to an integer or if the command is not found in `AIRCMD_KEYWORDS`.

*   `encode(aircraft_id: int, message: str, with_size: bool = False)`
    *   Encodes the provided parameters into a byte buffer representing the `FSNETCMD_AIRCMD` packet.
    *   Parameters:
        *   `aircraft_id`: `int`
            *   The ID of the aircraft.
        *   `message`: `str`
            *   The message string to send.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.

*   `set_payload(aircraft_id: int, payload: int, units: str = 'kg', with_size: bool = False)`
    *   Static method to create and encode a command to set the aircraft payload.
    *   Uses the `INITLOAD` command.
    *   Parameters:
        *   `aircraft_id`: `int`
            *   The ID of the aircraft.
        *   `payload`: `int`
            *   The payload value.
        *   `units`: `str`, default = `'kg'`
            *   The units of the payload.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size.
    *   Returns: `bytes`
        *   The encoded byte buffer.

*   `set_command(aircraft_id: int, command: str, value: Union[str, int], with_size: bool = False)`
    *   Static method to create and encode a command to set a generic aircraft command.
    *   Uses the `*<command_code> <value>` format.
    *   If the `command` is found in `AIRCMD_KEYWORDS`, its index is used as the `command_code`. Otherwise, `command` is assumed to be the code itself.
    *   Parameters:
        *   `aircraft_id`: `int`
            *   The ID of the aircraft.
        *   `command`: `str`
            *   The command keyword or code.
        *   `value`: `Union[str, int]`
            *   The value for the command.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size.
    *   Returns: `bytes`
        *   The encoded byte buffer.

*   `set_afterburner(aircarft_id: int, enabled: int, with_size: bool = False)`
    *   Static method to create and encode a command to set the afterburner state of an aircraft.
    *   Uses the `AFTBURNR` command.
    *   Parameters:
        *   `aircarft_id`: `int`
            *   The ID of the aircraft.
        *   `enabled`: `int`
            *   `1` to enable afterburner, `0` to disable.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size.
    *   Returns: `bytes`
        *   The encoded byte buffer.

*   `__str__(self)`
    *   Returns a string representation of the `FSNETCMD_AIRCMD` object for debugging and logging.
    *   Returns: `str`
        *   A formatted string showing `aircraft_id`, `message`, and `command` attributes.

## FSNETCMD_AIRPLANESTATE

This packet is sent by the client to the server to update the state of the aircraft, and vice versa.

Versions:
* Version 0: `vh`, `vp`, and `vr` (velocity components) are 16-bit shorts.
* Version >= 1: `vh`, `vp`, and `vr` are 32-bit integers appended at the end.
* Version >= 2: Includes thrust vector, reverser, and bomb bay information.
* Version >= 3: `idOnServer` (player ID) is 32-bit integer.
* Version 4 & 5: Short version of `vh`, `vp`, and `vr` (16-bit shorts again).
    * Version 4: Includes thrust vector and bomb bay.
    * Version 5: No thrust vector or bomb bay.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `remote_time`: `float`, optional
    *   Remote time, likely representing server or simulation time.
*   `player_id`: `int`, optional
    *   The ID of the player or aircraft.
*   `packet_version`: `int`, optional
    *   Version of the `FSNETCMD_AIRPLANESTATE` packet. Different versions have different data layouts.
*   `position`: `list[float]`, optional, size: 3
    *   The 3D position of the aircraft in world coordinates: `[x, y, z]`.
*   `atti`: `list[float]`, optional, size: 3
    *   The 3D attitude of the aircraft, likely in radians: `[roll, pitch, yaw]`.
*   `velocity`: `list[float]`, optional, size: 3
    *   The 3D velocity vector of the aircraft: `[vx, vy, vz]`.
*   `atti_velocity`: `list[float]`, optional, size: 3
    *   The 3D angular velocity vector of the aircraft, likely in radians per second: `[roll_rate, pitch_rate, yaw_rate]`.
*   `smoke_oil`: `int`, optional
    *   Level of smoke oil remaining.
*   `fuel`: `int` or `float`, optional
    *   Amount of fuel remaining. Type depends on the packet version (likely `int` for older, `float` for newer).
*   `payload`: `int` or `float`, optional
    *   Current payload of the aircraft. Type depends on the packet version (likely `int` for older, `float` for newer).
*   `flight_state`: `int`, optional
    *   Current flight state of the aircraft (e.g., flying, landed, crashed).
*   `vgw`: `float`, optional
    *   Variable Geometry Wing position, typically a value between 0.0 and 1.0.
*   `spoiler`: `float`, optional
    *   Spoiler deployment, typically a value between 0.0 and 1.0.
*   `landing_gear`: `float`, optional
    *   Landing gear deployment, typically a value between 0.0 and 1.0.
*   `flap`: `float`, optional
    *   Flap deployment, typically a value between 0.0 and 1.0.
*   `brake`: `float`, optional
    *   Brake application, typically a value between 0.0 and 1.0.
*   `flags`: `dict[str, Union[bool, int]]`, optional
    *   A dictionary containing various boolean and integer flags representing aircraft status:
        *   `"ab"`: `bool` - Afterburner status (True if active).
        *   `"firing"`: `bool` - Firing weapons status (True if firing).
        *   `"smoke"`: `int` - Smoke generation level.
        *   `"nav_lights"`: `bool` - Navigation lights status (True if on).
        *   `"beacon"`: `bool` - Beacon lights status (True if on).
        *   `"strobe"`: `bool` - Strobe lights status (True if on).
        *   `"landing_lights"`: `bool` - Landing lights status (True if on).
*   `gun_ammo`: `int`, optional
    *   Remaining gun ammunition.
*   `rocket_ammo`: `int`, optional
    *   Remaining rocket ammunition.
*   `aam`: `int`, optional
    *   Remaining Air-to-Air Missiles.
*   `agm`: `int`, optional
    *   Remaining Air-to-Ground Missiles.
*   `bomb`: `int`, optional
    *   Remaining bombs.
*   `life`: `int`, optional
    *   Aircraft life or health points.
*   `g_value`: `float`, optional
    *   Current G-force value experienced by the aircraft.
*   `throttle`: `float`, optional
    *   Throttle input, typically a value between 0.0 and 1.0.
*   `elev`: `float`, optional
    *   Elevator input, typically a value between -1.0 and 1.0.
*   `ail`: `float`, optional
    *   Aileron input, typically a value between -1.0 and 1.0.
*   `rud`: `float`, optional
    *   Rudder input, typically a value between -1.0 and 1.0.
*   `trim`: `float`, optional
    *   Trim input, typically a value between -1.0 and 1.0.
*   `thrust_vector`: `dict[str, float]`, optional
    *   Dictionary containing thrust vectoring information:
        *   `"vector"`: `float` - Thrust vectoring position, typically 0.0 to 1.0.
        *   `"reverser"`: `float` - Thrust reverser position, typically 0.0 to 1.0.
*   `bomb_bay_info`: `float`, optional
    *   Bomb bay status or deployment, typically 0.0 to 1.0.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_AIRPLANESTATE` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes based on the `packet_version`.
    *   Handles different packet versions and their corresponding data structures.
    *   Returns: `None`

*   `smoke(self)`
    *   Modifies the packet buffer to enable the aircraft's smoke generation.
    *   Returns: `bytes`
        *   A new byte buffer with the smoke flag enabled.

*   `stop_firing(self)`
    *   Modifies the packet buffer to stop the aircraft from firing weapons.
    *   Returns: `bytes`
        *   A new byte buffer with the firing flag disabled.

*   `get_life(buffer: bytes)`
    *   Static method to extract the aircraft's life value from a raw packet buffer.
    *   Version aware, returns life based on the packet version.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
    *   Returns: `int`
        *   The aircraft's life value.

*   `encode(remote_time, player_id, packet_version, position, atti, velocity, atti_velocity, smoke_oil, fuel, payload, flight_state, vgw, spoiler, landing_gear, flap, brake, flags, gun_ammo, rocket_ammo, aam, agm, bomb, life, g_value, throttle, elev, ail, rud, trim, thrust_vector, bomb_bay_info, with_size: bool = False)`
    *   Static method to encode aircraft state data into a byte buffer representing the `FSNETCMD_AIRPLANESTATE` packet.
    *   Handles different packet versions during encoding.
    *   Parameters: (Numerous, corresponding to the class attributes)
        *   `remote_time`: `float`
        *   `player_id`: `int`
        *   `packet_version`: `int`
        *   `position`: `list[float]`
        *   `atti`: `list[float]`
        *   `velocity`: `list[float]`
        *   `atti_velocity`: `list[float]`
        *   `smoke_oil`: `int`
        *   `fuel`: `int` or `float`
        *   `payload`: `int` or `float`
        *   `flight_state`: `int`
        *   `vgw`: `float`
        *   `spoiler`: `float`
        *   `landing_gear`: `float`
        *   `flap`: `float`
        *   `brake`: `float`
        *   `flags`: `dict[str, Union[bool, int]]`
        *   `gun_ammo`: `int`
        *   `rocket_ammo`: `int`
        *   `aam`: `int`
        *   `agm`: `int`
        *   `bomb`: `int`
        *   `life`: `int`
        *   `g_value`: `float`
        *   `throttle`: `float`
        *   `elev`: `float`
        *   `ail`: `float`
        *   `rud`: `float`
        *   `trim`: `float`
        *   `thrust_vector`: `dict[str, float]`
        *   `bomb_bay_info`: `float`
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.

*   `__str__(self)`
    *   Returns a string representation of the `FSNETCMD_AIRPLANESTATE` object for debugging and logging purposes, including key attributes.
    *   Returns: `str`
        *   A formatted string showing the state of the `FSNETCMD_AIRPLANESTATE` object.

## FSNETCMD_EMPTYPACKET

A template class for empty packets, containing no data beyond the packet identifier.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.  While this class represents an empty packet, the base class structure includes a buffer attribute.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`. In this class, decoding is a no-op.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_EMPTYPACKET` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data. Although intended to be empty, it's included for consistency with other packet classes.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the `decode` method will be called upon object creation. For this class, `decode` performs no action.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes   the `buffer` attribute.  For `FSNETCMD_EMPTYPACKET`, this method does nothing as there is no data to decode.
    *   Returns: `None`

*   `encode(with_size: bool = False)`
    *   Encodes the packet identifier into a byte buffer representing the `FSNETCMD_EMPTYPACKET` packet.
    *   Parameters:
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer containing just the packet identifier.


## FSNETCMD_ENVIRONMENT

This packet is used to update the environment settings on the client.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `day_night`: `int`, optional
    *   Indicates the time of day.
        *   `-1`: Default value, likely unchanged.
        *   `0`: Day time.
        *   `1`: Night time.
*   `flags`: `dict[str, bool]`, optional
    *   A dictionary containing boolean flags for environmental effects:
        *   `"fog"`: `bool` -  Indicates whether fog is enabled.
        *   `"blackout"`: `bool` - Indicates whether blackout conditions are enabled (reduced visibility).
        *   `"midair"`: `bool` - Indicates whether mid-air start is enforced.
        *   `"can_land_anywhere"`: `bool` - Indicates whether landing is allowed anywhere or restricted to airfields.
*   `wind`: `list[float]`, optional, size: 3
    *   The 3D wind vector: `[x, y, z]` representing wind direction and strength.
*   `visibility`: `float`, optional
    *   The visibility range in the environment.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_ENVIRONMENT` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Uses `struct.unpack` to extract environment variables, flags, wind, and visibility from the byte data.
    *   Parses flag bits to set the boolean values in the `flags` dictionary.
    *   Returns: `None`

*   `encode(day_night, fog, blackout, midair, can_land_anywhere, wind, visibility, with_size: bool = False)`
    *   Static method to encode environment data into a byte buffer representing the `FSNETCMD_ENVIRONMENT` packet.
    *   Parameters:
        *   `day_night`: `int`
            *   Time of day (0 for day, 1 for night).
        *   `fog`: `bool`
            *   Enable fog.
        *   `blackout`: `bool`
            *   Enable blackout.
        *   `midair`: `bool`
            *   Enable mid-air start.
        *   `can_land_anywhere`: `bool`
            *   Enable landing anywhere.
        *   `wind`: `list[float]`
            *   3D wind vector.
        *   `visibility`: `float`
            *   Visibility range.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.

*   `set_time(buffer: bytes, night: bool, with_size: bool = True)`
    *   Static method to modify an existing `FSNETCMD_ENVIRONMENT` packet buffer to set the time of day.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer of an existing `FSNETCMD_ENVIRONMENT` packet.
        *   `night`: `bool`
            *   `True` for night, `False` for day.
        *   `with_size`: `bool`, default = `True`
            *   If `True`, prepends the buffer with its size.
    *   Returns: `bytes`
        *   The modified byte buffer.

*   `set_visibility(buffer: bytes, visibility: int, with_size: bool = True)`
    *   Static method to modify an existing `FSNETCMD_ENVIRONMENT` packet buffer to set the visibility range.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer of an existing `FSNETCMD_ENVIRONMENT` packet.
        *   `visibility`: `int`
            *   The visibility range value to set.
        *   `with_size`: `bool`, default = `True`
            *   If `True`, prepends the buffer with its size.
    *   Returns: `bytes`
        *   The modified byte buffer.


## FSNETCMD_ERROR

This packet is used to transmit error information from the server to the client.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `error_code`: `int`, optional
    *   Numerical code representing the specific error.
*   `error_message`: `str`, optional
    *   Human-readable error message corresponding to the `error_code`.
    *   The message is looked up in the `ERROR_CODES` constant list based on the `error_code`.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_ERROR` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Extracts the `error_code` from the buffer using `struct.unpack`.
    *   Attempts to retrieve the corresponding `error_message` from the `ERROR_CODES` constant list using the `error_code` as an index.
    *   Returns: `None`

*   `encode(error_code, with_size: bool = False)`
    *   Static method to encode error information into a byte buffer representing the `FSNETCMD_ERROR` packet.
    *   Parameters:
        *   `error_code`: `int`
            *   The numerical error code to encode.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.

## FSNETCMD_FOGCOLOR

This packet is used to set the fog color on the client side.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `redValue`: `int`, optional
    *   Red component of the fog color (0-255).
*   `greenValue`: `int`, optional
    *   Green component of the fog color (0-255).
*   `blueValue`: `int`, optional
    *   Blue component of the fog color (0-255).
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_FOGCOLOR` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Extracts the red, green, and blue color values from the buffer.
    *   Returns: `None`

*   `encode(redValue: int, greenValue: int, blueValue: int, with_size: bool = False)`
    *   Static method to encode fog color data into a byte buffer representing the `FSNETCMD_FOGCOLOR` packet.
    *   Parameters:
        *   `redValue`: `int`
            *   Red color component (0-255).
        *   `greenValue`: `int`
            *   Green color component (0-255).
        *   `blueValue`: `int`
            *   Blue color component (0-255).
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.

## FSNETCMD_GETDAMAGE

Sent when an aircraft or ground target has taken damage.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `victim_id`: `int`, optional
    *   ID of the victim object that received damage.
*   `victim_type`: `int`, optional
    *   Type of the victim object.
*   `attacker_type`: `int`, optional
    *   Type of the attacker object that caused the damage.
*   `attacker_id`: `int`, optional
    *   ID of the attacker object that caused the damage.
*   `damage`: `int`, optional
    *   Amount of damage inflicted.
*   `died_of`: `int`, optional
    *   Indicates the cause of death, if the damage was fatal.
*   `weapon_type`: `int` or `str`, optional
    *   Type of weapon used to inflict the damage.
    *   If the `weapon_type` is decodable from `FSWEAPON_DICT`, it will be a `str` representing the weapon name. Otherwise, it remains an `int` representing the weapon code.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_GETDAMAGE` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Uses `struct.unpack` to extract damage information from the byte data.
    *   Attempts to convert the numerical `weapon_type` code into a human-readable weapon name using `FSWEAPON_DICT`.
    *   Returns: `None`

*   `encode(victim_id, victim_type, attacker_type, attacker_id, damage, died_of, weapon_type, with_size: bool = False)`
    *   Static method to encode damage information into a byte buffer representing the `FSNETCMD_GETDAMAGE` packet.
    *   Parameters:
        *   `victim_id`: `int`
            *   ID of the victim.
        *   `victim_type`: `int`
            *   Type of the victim.
        *   `attacker_type`: `int`
            *   Type of the attacker.
        *   `attacker_id`: `int`
            *   ID of the attacker.
        *   `damage`: `int`
            *   Damage amount.
        *   `died_of`: `int`
            *   Cause of death code.
        *   `weapon_type`: `int` or `str`
            *   Weapon type, can be either the integer code or the string name (which will be converted to code during encoding).
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.

*   `__str__(self)`
    *   Returns a string representation of the `FSNETCMD_GETDAMAGE` object for debugging and logging purposes.
    *   Returns: `str`
        *   A formatted string showing the damage event details including victim, attacker, damage amount, death cause, and weapon.


## FSNETCMD_JOINAPPROVAL

When the server sends the "add aircraft" command, and receives the readback from the client, they'll send this packet. It's an empty packet, but can be useful to know the client is about to join.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data. Although this is designed to be an empty packet, the base class structure includes a buffer attribute.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`. For this class, `decode` is a no-op.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_JOINAPPROVAL` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data. Even though this is intended to be an empty packet, the buffer is included for class consistency.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the `decode` method will be called upon object creation.  For this class, `decode` performs no action.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute. For `FSNETCMD_JOINAPPROVAL`, this method does nothing as the packet is intentionally empty.
    *   Returns: `None`

*   `encode(with_size: bool = False)`
    *   Encodes the packet identifier into a byte buffer representing the `FSNETCMD_JOINAPPROVAL` packet.
    *   Parameters:
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer, containing only the packet identifier.

## FSNETCMD_JOINREQUEST

The client sends a join request to the server with their IFF, aircraft type, start position, fuel, and smoke settings. The server should reply with a join request readback.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `iff`: `int`, optional
    *   Identification Friend or Foe setting requested by the client.
*   `aircraft`: `str`, optional, size: 32
    *   Name of the aircraft requested by the client.
*   `start_pos`: `str`, optional, size: 32
    *   Name of the starting position requested by the client (STP name).
*   `fuel`: `int`, optional
    *   Fuel level requested by the client.
*   `smoke`: `int`, optional
    *   Smoke setting requested by the client.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_JOINREQUEST` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Uses `struct.unpack` to extract IFF, aircraft name, start position, fuel, and smoke settings from the byte data.
    *   Decodes and strips null byte padding from the `aircraft` and `start_pos` attributes.
    *   Returns: `None`

*   `encode(iff, aircraft, start_pos, fuel, smoke, with_size: bool = False)`
    *   Static method to encode join request data into a byte buffer representing the `FSNETCMD_JOINREQUEST` packet.
    *   Parameters:
        *   `iff`: `int`
            *   The IFF setting.
        *   `aircraft`: `str`
            *   The aircraft name.
        *   `start_pos`: `str`
            *   The starting position name.
        *   `fuel`: `int`
            *   The fuel level.
        *   `smoke`: `int`
            *   The smoke setting.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.

## FSNETCMD_KILLSERVER

This packet is intended to signal the server to shut down.  However, the actual server-side functionality to process this command and initiate a shutdown is unimplemented in the current YS server.  Therefore, sending this packet will not result in the server being terminated.

This class inherits from `FSNETCMD_EMPTYPACKET`, and thus shares its basic structure.

### Attributes

*   `buffer`: `bytes` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   The raw byte buffer of the packet data. As an empty packet type, this will primarily contain the packet identifier.
*   `should_decode`: `bool` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`. Decoding has no effect for this empty packet type.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   Constructor for the `FSNETCMD_KILLSERVER` class.  Inherits the constructor from `FSNETCMD_EMPTYPACKET`.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the `decode` method will be called (though it performs no operation in this case).
    *   Returns: `None`

*   `decode(self)` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   Decode method for the `FSNETCMD_KILLSERVER` class. Inherited from `FSNETCMD_EMPTYPACKET`, it performs no action as this is an empty packet.
    *   Returns: `None`

*   `encode(with_size: bool = False)`
    *   Static method to encode the `FSNETCMD_KILLSERVER` packet, which consists only of its identifier.  Overrides the `encode` method from `FSNETCMD_EMPTYPACKET` to specifically set the packet ID for `FSNETCMD_KILLSERVER`.
    *   Parameters:
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer containing the packet identifier.


## FSNETCMD_LIST

This packet is used to transmit lists of data, such as aircraft lists, from the server to the client.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `list_type`: `int`, optional
    *   Specifies the type of list being transmitted. The specific meaning of different list types is context-dependent.
*   `num_of_items`: `int`, optional
    *   The number of items included in the list within this packet.
*   `list`: `list[bytes]`, optional
    *   A list of byte strings, where each element represents an item in the transmitted list. Items are extracted by splitting the buffer by null bytes.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_LIST` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Unpacks the packet type, `list_type`, and `num_of_items` from the buffer header.
    *   Splits the remaining buffer content by null bytes (`\x00`) to create a list of byte strings, and stores it in the `list` attribute.  The last element after the split is discarded as it's expected to be an empty byte string resulting from the final null byte delimiter.
    *   Returns: `None`

*   `encode(list_type: int = 1, list_buffer: bytes = b'', num_of_items: int = 0, with_size: bool = False)`
    *   Static method to encode list data into a byte buffer representing the `FSNETCMD_LIST` packet.
    *   The maximum length of the encoded packet (including header) should not exceed 1024 bytes, leaving a maximum of 1015 bytes for the list itself after the 8-byte header.
    *   Parameters:
        *   `list_type`: `int`, default = `1`
            *   The type of list.
        *   `list_buffer`: `bytes`, default = `b''`
            *   The byte string containing the list items, typically null-byte separated.
        *   `num_of_items`: `int`, default = `0`
            *   The number of items in the `list_buffer`.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.

---

## List\_Constructor

This class is designed to take a list of strings (e.g., aircraft names) and break it down into a series of `FSNETCMD_LIST` packets. This is necessary because `FSNETCMD_LIST` packets have a size limitation.  It's mentioned in the code comments that if sending custom lists, client and server side `FSNETCMD_LIST` reply/command handling may need to be blocked to avoid conflicts or loops.

### Attributes

*   `aircraftList`: `list[str]`
    *   The input list of aircraft names (strings) to be packetized.
*   `packet_list`: `list[bytes]`
    *   A list of encoded `FSNETCMD_LIST` packets (byte strings) generated by the `construct_packets` method.
*   `num_of_packets`: `int`
    *   The number of `FSNETCMD_LIST` packets created.
*   `with_size`: `bool`
    *   A flag indicating whether to include the packet size at the beginning of each encoded packet. This value is passed down to the `FSNETCMD_LIST.encode` method.

### Methods

*   `__init__(self, aircraftList: list[str], with_size: bool = True)`
    *   Constructor for the `List_Constructor` class.
    *   Parameters:
        *   `aircraftList`: `list[str]`
            *   The list of aircraft names to be packetized.
        *   `with_size`: `bool`, default = `True`
            *   If `True`, encoded packets will include the size prefix.
    *   Returns: `None`

*   `construct_packets(self)`
    *   This method is the core logic for breaking down the `aircraftList` into multiple `FSNETCMD_LIST` packets.
    *   Iterates through the `aircraftList`. For each aircraft name:
        *   Replaces spaces in the aircraft name with underscores.
        *   Encodes the aircraft name to bytes and appends a null terminator (`\x00`).
        *   Checks if adding the current aircraft name to the current packet would exceed the packet size limit (1015 bytes for the list content).
        *   If it fits, appends the aircraft name to the current packet.
        *   If it doesn't fit, or if the current packet already contains 32 items, it encodes the current packet using `FSNETCMD_LIST.encode`, adds it to the `packet_list`, and starts a new packet with the current aircraft name.
    *   After processing all aircraft names, it encodes any remaining content in the `packet` buffer into a final `FSNETCMD_LIST` packet and appends it to `packet_list`.
    *   Updates `num_of_packets` to reflect the total number of packets created.
    *   Returns: `None`

*   `check_fit(self, packet: bytes, aircraft: bytes)`
    *   Checks if adding a new `aircraft` (in bytes) to the current `packet` (also in bytes) would exceed the size limit for the list content within an `FSNETCMD_LIST` packet (1015 bytes).
    *   Parameters:
        *   `packet`: `bytes`
            *   The current byte string representing the content of the packet being built.
        *   `aircraft`: `bytes`
            *   The byte string representing the aircraft name to be added.
    *   Returns: `bool`
        *   `True` if the `aircraft` can be added to the `packet` without exceeding the size limit, `False` otherwise.

*   `get_packets(self)`
    *   Returns the list of generated `FSNETCMD_LIST` packets.
    *   Returns: `list[bytes]`
        *   The `packet_list` containing encoded `FSNETCMD_LIST` packets.


## FSNETCMD_LOADFIELD

This packet is sent by the server along with the field information. When received, the client replies with the same packet as a confirmation.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `field`: `bytes`, size: 32, optional
    *   The name of the field as a byte string, null-padded to 32 bytes.
*   `fieldShortName`: `str`, optional
    *   The decoded short name of the field, extracted from the `field` attribute by removing null byte padding and decoding to a string.
*   `flags`: `int`, optional
    *   Flags associated with the loaded field.
*   `pos`: `list[float]`, optional, size: 3
    *   The 3D position of the field: `[x, y, z]`.
*   `atti`: `list[float]`, optional, size: 3
    *   The 3D attitude of the field: `[roll, pitch, yaw]`.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_LOADFIELD` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True` and the buffer length is 64 bytes, the `decode` method will be called immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Uses `struct.unpack` to extract the field name, flags, position, and attitude from the byte data.
    *   Sets the `fieldShortName` attribute by decoding the `field` attribute and removing trailing null bytes.
    *   Returns: `None`

*   `encode(field, flags, pos, atti, with_size: bool = False)`
    *   Static method to encode field loading data into a byte buffer representing the `FSNETCMD_LOADFIELD` packet.
    *   Parameters:
        *   `field`: `str` or `bytes`
            *   The name of the field. If a string is provided, it will be encoded to bytes.
        *   `flags`: `int`
            *   The field flags.
        *   `pos`: `list[float]`
            *   The 3D position of the field.
        *   `atti`: `list[float]`
            *   The 3D attitude of the field.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.


## FSNETCMD_LOCKON

This packet is sent both from the server to clients and from clients to the server to communicate lock-on events between entities in the simulation. It signals when one entity (the locker) successfully locks onto another entity (the lockee).

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `locker_id`: `int`, optional
    *   The ID of the entity that is performing the lock-on (the locker).
*   `locker_is_air`: `bool`, optional
    *   A boolean flag indicating whether the locker entity is an aircraft (`True`) or not (`False`).
*   `lockee_id`: `int`, optional
    *   The ID of the entity that is being locked onto (the lockee).
*   `lockee_is_air`: `bool`, optional
    *   A boolean flag indicating whether the lockee entity is an aircraft (`True`) or not (`False`).
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_LOCKON` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Uses `struct.unpack` to extract the locker ID, locker `is_air` flag, lockee ID, and lockee `is_air` flag from the buffer.
    *   Converts the integer flags for `locker_is_air` and `lockee_is_air` to boolean values.
    *   Returns: `None`

*   `encode(locker_id, locker_is_air, lockee_id, lockee_is_air, with_size: bool = False)`
    *   Static method to encode lock-on event data into a byte buffer representing the `FSNETCMD_LOCKON` packet.
    *   Parameters:
        *   `locker_id`: `int`
            *   The ID of the locker entity.
        *   `locker_is_air`: `bool` or `int`
            *   Boolean or integer (0 or 1) indicating if the locker is an aircraft.
        *   `lockee_id`: `int`
            *   The ID of the lockee entity.
        *   `lockee_is_air`: `bool` or `int`
            *   Boolean or integer (0 or 1) indicating if the lockee is an aircraft.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.


## FSNETCMD_LOGOFF

This packet is a logoff signal, intended to be used to disconnect from the server.  However, it appears to be functionally unused or unimplemented within the current YS server codebase. It is included here for completeness in documenting the packet structure.

As an empty packet, it contains no data beyond the standard packet identifier.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.  Although designed to be an empty packet, the class structure includes a buffer attribute to maintain consistency with other packet types.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.  For `FSNETCMD_LOGOFF`, the decode operation is effectively empty.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_LOGOFF` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data. Even though this is an empty packet, a buffer is provided for consistency.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the `decode` method will be called during object initialization. For this packet, `decode` does nothing.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute. For the `FSNETCMD_LOGOFF` packet, this method performs no operations, as there is no data to decode.
    *   Returns: `None`

*   `encode(with_size: bool = False)`
    *   Static method to encode the `FSNETCMD_LOGOFF` packet into a byte buffer.  The packet consists only of its identifier.
    *   Parameters:
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer containing the packet identifier.


## FSNETCMD_LOGON

This packet is used for the initial logon process, exchanged between the client and server when a client attempts to connect and log in. The client sends this packet to the server upon login, and the server typically replies with an acknowledgment (often an empty packet for newer YS versions).

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `version`: `int`, optional
    *   The version number of the client or the network protocol being used.
*   `username`: `str`, optional
    *   The username provided by the client for login, limited to 16 characters in its short form within the packet.
*   `alias`: `str`, optional
    *   An extended alias or full username, used if the username exceeds 16 characters. This is appended to the packet after the standard username and version.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_LOGON` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True` and the buffer length is greater than 5 bytes, the `decode` method will be called immediately upon object creation to parse the logon information.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Unpacks the initial part of the buffer to extract the `username` (as a 16-byte string) and `version` (as an integer).
    *   Checks if the buffer length is greater than 24 bytes, indicating the presence of an `alias`. If an alias is present, it is decoded and stripped of null byte padding. Otherwise, the `alias` is set to be the same as the `username`.
    *   Decodes both `username` and `alias` from bytes to strings and removes any trailing null characters.
    *   Returns: `None`

*   `encode(username, version, with_size: bool = False)`
    *   Static method to encode logon data into a byte buffer representing the `FSNETCMD_LOGON` packet.
    *   Parameters:
        *   `username`: `str`
            *   The username to be used for login.
        *   `version`: `int`
            *   The client or protocol version number.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.
    *   Encoding Logic:
        *   If the `username` is longer than 15 characters, a shortened 15-character `shortform` is created, and the full `username` is used as the `alias`. Otherwise, `shortform` is the full `username`, and `alias` is `None`.
        *   Packs the packet ID, `shortform` username (as 16-byte null padded string), and `version` into the buffer.
        *   If an `alias` is present:
            *   Encodes the `alias` to bytes.
            *   If the `alias` length is less than 200 bytes, right-justifies it with null bytes to 200 bytes and appends 4 more null bytes.
            *   Appends the (potentially padded) `alias` to the buffer.
        *   Optionally prepends the buffer size if `with_size` is `True`.

*   `alter_version(buffer: bytes, new_version: int)`
    *   Static method to modify the version number within an existing `FSNETCMD_LOGON` packet buffer.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer of an existing `FSNETCMD_LOGON` packet.
        *   `new_version`: `int`
            *   The new version number to set in the packet.
    *   Returns: `bytes`
        *   The modified byte buffer with the updated version.
    *   Modification Logic:
        *   Extracts the part of the buffer before the version field (first 20 bytes).
        *   Packs the `new_version` into a 4-byte integer.
        *   Concatenates the initial part, the new version, and the part of the buffer after the original version field (from byte 24 onwards), effectively replacing the old version with the `new_version`.


## FSNETCMD_MISSILELAUNCH

This packet is sent when a missile or bomb is launched by an aircraft or other entity in the game. It contains information about the launched weapon, its initial state, and launch parameters.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `weapon_type`: `int` or `str`, optional
    *   The type of weapon launched. It can be an integer representing the weapon code or a string representing the weapon name (looked up from `FSWEAPON_DICT` during decoding).
*   `position`: `list[float]`, optional, size: 3
    *   The 3D position at which the weapon is launched: `[x, y, z]`.
*   `atti`: `list[float]`, optional, size: 3
    *   The 3D attitude (orientation) of the launched weapon, likely in radians: `[roll, pitch, yaw]`.
*   `velocity`: `float`, optional
    *   The initial velocity magnitude of the launched weapon.
*   `life_remaining`: `float`, optional
    *   The remaining lifespan of the weapon, likely in milliseconds.
*   `power`: `int`, optional
    *   The power or damage potential of the weapon.
*   `fired_by_aircraft`: `int`, optional
    *   ID of the aircraft that fired the weapon. `0` if fired by a ground unit or environment.
*   `fired_by`: `int`, optional
    *   ID of the entity (aircraft or ground unit) that launched the weapon.
*   `v_max`: `float`, optional
    *   Maximum velocity of the weapon, applicable to guided weapons and flares.
*   `mobility`: `float`, optional
    *   Mobility or maneuverability parameter of the weapon, specific to guided weapons.
*   `radar`: `float`, optional
    *   Radar cross-section or radar-related property of the weapon, specific to guided weapons.
*   `fired_at_aircraft`: `bool`, optional
    *   Boolean flag indicating if the weapon is fired at an aircraft (`True`) or a ground target (`False`), specific to guided weapons.
*   `fired_at`: `int`, optional
    *   ID of the target entity being fired at, specific to guided weapons.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_MISSILELAUNCH` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes based on the packet structure and weapon type.
    *   Unpacks data from the buffer based on predefined offsets and data types using `struct.unpack`.
    *   Decodes `weapon_type` integer code to weapon name string if found in `FSWEAPON_DICT`.
    *   For guided weapons (`GUIDEDWEAPONS`) and flares (`FSWEAPON_FLARE`), it unpacks additional specific parameters like `v_max`, `mobility`, `radar`, `fired_at_aircraft`, and `fired_at` if present in the buffer.
    *   Returns: `None`

*   `encode(weapon_type, position, atti, velocity, life_remaining, power, fired_by_aircraft, fired_by, v_max=1000, mobility=0, radar=0, fired_at_aircraft=False, fired_at=0, with_size: bool = False)`
    *   Static method to encode missile launch data into a byte buffer representing the `FSNETCMD_MISSILELAUNCH` packet.
    *   Parameters:
        *   `weapon_type`: `int` or `str`
            *   The type of weapon. Can be integer code or weapon name string. If string, it will be converted to integer code using `FSWEAPON_DICT`.
        *   `position`: `list[float]`
            *   The 3D launch position.
        *   `atti`: `list[float]`
            *   The 3D launch attitude.
        *   `velocity`: `float`
            *   Initial velocity.
        *   `life_remaining`: `float`
            *   Weapon's lifespan.
        *   `power`: `int`
            *   Weapon power.
        *   `fired_by_aircraft`: `int`
            *   ID of firing aircraft.
        *   `fired_by`: `int`
            *   ID of firing entity.
        *   `v_max`: `float`, default = `1000`
            *   Maximum velocity (for guided weapons/flares).
        *   `mobility`: `float`, default = `0`
            *   Mobility parameter (for guided weapons).
        *   `radar`: `float`, default = `0`
            *   Radar parameter (for guided weapons).
        *   `fired_at_aircraft`: `bool`, default = `False`
            *   Is target an aircraft (for guided weapons).
        *   `fired_at`: `int`, default = `0`
            *   Target ID (for guided weapons).
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.
    *   Encoding Logic:
        *   Converts weapon name string to integer code using `FSWEAPON_DICT` if necessary.
        *   Packs the packet ID and base missile launch data (`weapon_type`, `position`, `atti`, `velocity`, `life_remaining`, `power`, `fired_by_aircraft`, `fired_by`) using `struct.pack`.
        *   If the `weapon_type_name` is in `GUIDEDWEAPONS`, it packs guided weapon specific parameters (`v_max`, `mobility`, `radar`, `fired_at_aircraft`, `fired_at`).
        *   If the `weapon_type_name` is `"FSWEAPON_FLARE"`, it packs flare-specific parameter (`v_max`).
        *   Optionally prepends the buffer size if `with_size` is `True`.

*   `drop_bombs(aircraft: Aircraft)`
    *   Static method to create and encode a `FSNETCMD_MISSILELAUNCH` packet representing a bomb drop from a given `Aircraft` object.
    *   Parameters:
        *   `aircraft`: `Aircraft`
            *   The `Aircraft` object dropping the bombs.
    *   Returns: `bytes`
        *   The encoded byte buffer for the bomb drop packet.
    *   Functionality:
        *   Retrieves the aircraft's `position` and `attitude`.
        *   Sets the `atti[2]` (yaw) to `0`.
        *   Randomly selects a `weapon_type` integer code between 0 and 13 (inclusive).
        *   Calls `FSNETCMD_MISSILELAUNCH.encode` to create the packet with bomb-like parameters: `weapon_type`, aircraft's `position` and modified `atti`, `velocity=20`, `life_remaining=30000`, `power=999`, `fired_by_aircraft=0`, `fired_by=aircraft.id`, `v_max=1000`, and `with_size=True`.
        *   Returns the encoded packet.


## FSNETCMD_NULL

This packet represents a 'null' command within the FSNETCMD protocol. It is designed to be a minimal packet, containing no substantive data payload.  Its purpose is typically for basic communication such as keep-alive signals or simple acknowledgements where no further information needs to be transmitted.

### Attributes

*   `buffer`: `bytes`
    *   While the base class structure includes a `buffer` attribute, for `FSNETCMD_NULL` packets, this attribute is effectively unused as there is no packet data to store or process.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`. For `FSNETCMD_NULL`, the `decode` method is a no-op, so this flag has no practical effect.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_NULL` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer, though not used by `FSNETCMD_NULL`, is included for consistency with other packet classes.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the `decode` method will be called (though it performs no action).
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute. For the `FSNETCMD_NULL` packet, this method performs no operation and simply returns `None`, as there is no data to decode.
    *   Returns: `None`

*   `encode(self, with_size: bool = False)`
    *   Encodes the `FSNETCMD_NULL` packet into a byte buffer. The encoded packet consists solely of the packet identifier.
    *   Parameters:
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer. For `FSNETCMD_NULL` with size, it encodes the size (4 bytes) and the packet ID (0 - 4 bytes), resulting in an 8-byte buffer.
    *   Returns: `bytes`
        *   The encoded byte buffer containing the packet identifier (and optionally the size prefix).


## FSNETCMD_PREPARESIMULATION

This packet is sent by the server to the client during the login sequence, specifically when the server is nearly finished processing the client's login request and is about to start the simulation. It acts as a signal to the client that the game is preparing to begin.

This class inherits from `FSNETCMD_EMPTYPACKET`, meaning it is also an empty packet with no data beyond the packet identifier.

### Attributes

*   `buffer`: `bytes` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   The raw byte buffer of the packet data.  Being an empty packet, this mainly contains the packet identifier.
*   `should_decode`: `bool` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`. Decoding is a no-op for this empty packet type.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   Constructor for the `FSNETCMD_PREPARESIMULATION` class. Inherits the constructor from `FSNETCMD_EMPTYPACKET`.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the `decode` method will be called (although it has no effect).
    *   Returns: `None`

*   `decode(self)` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   Decode method for the `FSNETCMD_PREPARESIMULATION` class. Inherited from `FSNETCMD_EMPTYPACKET`, it performs no action as this is an empty packet type.
    *   Returns: `None`

*   `encode(with_size: bool = False)`
    *   Static method to encode the `FSNETCMD_PREPARESIMULATION` packet, which solely consists of its identifier. Overrides the `encode` method from `FSNETCMD_EMPTYPACKET` to set the correct packet ID.
    *   Parameters:
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer containing the packet identifier.


## FSNETCMD_READBACK

Sent from client to server and back to acknowledge various packets. This packet serves as a general acknowledgment mechanism in the FSNET protocol.

**Packet Acknowledgment Types:**

*   **Client to Server Acknowledgments:**
    *   `FSNETREADBACK_ADDAIRPLAN` or `FSNETREADBACK_ADDGROUND` acknowledge `FSNETCMD_ADDOBJECT` (Add Object command).
    *   `FSNETREADBACK_REMOVEAIRPLANE` or `FSNETREADBACK_REMOVEGROUND` acknowledge `FSNETCMD_REMOVEAIRPLANE` or `FSNETCMD_REMOVEGROUND` (Remove Object commands).
    *   `FSNETREADBACK_ENVIRONMENT` acknowledges `FSNETCMD_ENVIRONMENT` (Environment update command).
    *   `FSNETREADBACK_JOINREQUEST` acknowledges `FSNETCMD_JOINREQUEST` (Join Request command).
    *   `FSNETREADBACK_PREPARE` acknowledges `FSNETCMD_PREPARESIMULATION` (Prepare Simulation command).
    *   `FSNETREADBACK_USEMISSILE` acknowledges `FSNETCMD_USEMISSILE` (Use Missile command).
    *   `FSNETREADBACK_USEUNGUIDEDWEAPON` acknowledges `FSNETCMD_USEUNGUIDEDWEAPON` (Use Unguided Weapon command).
    *   `FSNETREADBACK_CTRLSHOWUSERNAME` acknowledges `FSNETCMD_CTRLSHOWUSERNAME` (Control Show Username command).

*   **Server to Client Acknowledgments:**
    *   `FSNETREADBACK_JOINREQUEST` acknowledges `FSNETCMD_JOINREQUEST`. Note: If the server receives this acknowledgment from a client after the server itself sent a `FSNETCMD_JOINREQUEST` readback, it may interpret it as an error or misuse and potentially disconnect (punt) the user.

*   **Note:** There might be more acknowledgment scenarios, but the provided list highlights the common use cases.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `read_back_type`: `int`, optional
    *   Specifies the type of packet being acknowledged. This value indicates which command is being read back.
*   `read_back_param`: `int`, optional
    *   An additional parameter associated with the readback. The meaning of this parameter is context-dependent and related to the specific `read_back_type`.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_READBACK` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Uses `struct.unpack` to extract the `read_back_type` and `read_back_param` from the byte data.
    *   Returns: `None`

*   `encode(read_back_type, read_back_param, with_size: bool = False)`
    *   Static method to encode readback data into a byte buffer representing the `FSNETCMD_READBACK` packet.
    *   Parameters:
        *   `read_back_type`: `int`
            *   The type of packet being acknowledged (the `read_back_type`).
        *   `read_back_param`: `int`
            *   The parameter associated with the readback.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.


## FSNETCMD_REJECTJOINREQ

If the server rejects a client's join request, it will send this `FSNETCMD_REJECTJOINREQ` packet to inform the client of the rejection. This packet is often followed by a separate chat message from the server providing the reason for the rejection.

As an empty packet, `FSNETCMD_REJECTJOINREQ` contains no data payload beyond its packet identifier.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data. While `FSNETCMD_REJECTJOINREQ` is an empty packet, the base class structure incorporates a buffer attribute.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`. For this class, the `decode` method is a no-operation.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_REJECTJOINREQ` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.  Even though this is intended as an empty packet, the buffer is included for consistency across packet classes.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the `decode` method will be invoked upon object creation.  In the case of `FSNETCMD_REJECTJOINREQ`, `decode` does nothing.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute. For `FSNETCMD_REJECTJOINREQ`, this method is intentionally empty as there is no data within the packet to decode.
    *   Returns: `None`

*   `encode(with_size: bool = False)`
    *   Encodes the packet identifier into a byte buffer, creating the `FSNETCMD_REJECTJOINREQ` packet.
    *   Parameters:
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer, consisting only of the packet identifier.


## FSNETCMD_REMOVEAIRPLANE

This packet is used to signal the removal of an airplane object from the simulation. It appears to be functionally very similar to `FSNETCMD_UNJOIN` (Packet ID 12), and in this implementation, it even inherits from `FSNETCMD_UNJOIN`. The reason for having two separate packet types for seemingly the same action is unclear, as suggested by the comment in the code.

This class extends `FSNETCMD_UNJOIN`, inheriting its attributes and basic functionality.

### Attributes

*   `buffer`: `bytes` (Inherited from `FSNETCMD_UNJOIN`)
    *   The raw byte buffer of the packet data.
*   `object_id`: `int`, optional (Inherited from `FSNETCMD_UNJOIN`)
    *   The ID of the airplane object to be removed from the simulation.
*   `explosion`: `int`, optional (Inherited from `FSNETCMD_UNJOIN`)
    *   A value indicating whether an explosion effect should be associated with the removal. Typically, `1` for explosion and `0` for no explosion.
*   `should_decode`: `bool` (Inherited from `FSNETCMD_UNJOIN`)
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)` (Inherited from `FSNETCMD_UNJOIN`)
    *   Constructor for the `FSNETCMD_REMOVEAIRPLANE` class.  It inherits the constructor from `FSNETCMD_UNJOIN`.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the `decode` method will be called (inherited from `FSNETCMD_UNJOIN`).
    *   Returns: `None`

*   `decode(self)` (Inherited from `FSNETCMD_UNJOIN`)
    *   Decode method for the `FSNETCMD_REMOVEAIRPLANE` class. It inherits the `decode` method from `FSNETCMD_UNJOIN`, which is responsible for unpacking the `object_id` and `explosion` attributes from the buffer.
    *   Returns: `None`

*   `encode(object_id, explosion, with_size: bool = False)`
    *   Static method to encode airplane removal data into a byte buffer representing the `FSNETCMD_REMOVEAIRPLANE` packet.
    *   Parameters:
        *   `object_id`: `int`
            *   The ID of the airplane object to remove.
        *   `explosion`: `int`
            *   Indicates if an explosion should occur upon removal (e.g., `1` for yes, `0` for no).
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.
    *   Encoding Logic:
        *   Packs the packet ID for `FSNETCMD_UNJOIN` (12) followed by the packet ID for `FSNETCMD_REMOVEAIRPLANE` (13), then the `object_id`, and the `explosion` value into the buffer.
        *   Optionally prepends the buffer size if `with_size` is `True`.

**Note:**  As highlighted by the code comment, the functionality of `FSNETCMD_REMOVEAIRPLANE` seems almost identical to `FSNETCMD_UNJOIN`. The distinction, and the reason for its existence as a separate packet type, are not immediately clear from the provided information and may be historical or related to specific server-side logic in the original implementation.


## FSNETCMD_REMOVEGROUND

This packet is used to signal the removal of a ground object from the simulation.  As indicated in the docstring, its functionality is very similar to `FSNETCMD_UNJOIN` and `FSNETCMD_REMOVEAIRPLANE`, but specifically targeted at ground-based objects.

This class extends `FSNETCMD_UNJOIN`, inheriting its core structure and functionality.

### Attributes

*   `buffer`: `bytes` (Inherited from `FSNETCMD_UNJOIN`)
    *   The raw byte buffer of the packet data.
*   `object_id`: `int`, optional (Inherited from `FSNETCMD_UNJOIN`)
    *   The ID of the ground object to be removed from the simulation.
*   `explosion`: `int`, optional (Inherited from `FSNETCMD_UNJOIN`)
    *   A value indicating whether an explosion effect should be associated with the removal. Typically `1` for explosion and `0` for no explosion.
*   `should_decode`: `bool` (Inherited from `FSNETCMD_UNJOIN`)
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)` (Inherited from `FSNETCMD_UNJOIN`)
    *   Constructor for the `FSNETCMD_REMOVEGROUND` class. It inherits the constructor from `FSNETCMD_UNJOIN`.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the `decode` method will be called (inherited from `FSNETCMD_UNJOIN`).
    *   Returns: `None`

*   `decode(self)` (Inherited from `FSNETCMD_UNJOIN`)
    *   Decode method for the `FSNETCMD_REMOVEGROUND` class. It inherits the `decode` method from `FSNETCMD_UNJOIN`, which is responsible for unpacking the `object_id` and `explosion` attributes from the buffer.
    *   Returns: `None`

*   `encode(object_id, explosion, with_size: bool = False)`
    *   Static method to encode ground object removal data into a byte buffer representing the `FSNETCMD_REMOVEGROUND` packet.
    *   Parameters:
        *   `object_id`: `int`
            *   The ID of the ground object to remove.
        *   `explosion`: `int`
            *   Indicates if an explosion should occur upon removal (e.g., `1` for yes, `0` for no).
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.
    *   Encoding Logic:
        *   Packs the packet ID for `FSNETCMD_REMOVEGROUND` (19), followed by the packet ID again (19 - likely a mistake or redundancy in the original code), then the `object_id`, and the `explosion` value into the buffer.
        *   Optionally prepends the buffer size if `with_size` is `True`.

**Note:**  Similar to `FSNETCMD_REMOVEAIRPLANE`, the functionality of `FSNETCMD_REMOVEGROUND` is very close to `FSNETCMD_UNJOIN`, but specialized for ground objects. The reason for having distinct packet types might relate to how the server processes object removal based on object type, even though the underlying data structure and encoding are highly similar to `FSNETCMD_UNJOIN`.  The redundant packet ID packing in the `encode` method (packing ID 19 twice) might be a coding error or an artifact from the original implementation that should be reviewed for correctness.



## FSNETCMD_REPORTSCORE

This packet is used to report scoring events when an aircraft or ground object is destroyed. It provides details about the kill, including the weapon used, the location, time, killer, and victim information.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `scored`: `bool`, optional
    *   Indicates whether the event resulted in a score. `True` if scored, `False` otherwise.
*   `weapon_type`: `int` or `str`, optional
    *   The type of weapon used to destroy the object. It can be an integer representing the weapon code or a string representing the weapon name (looked up from `FSWEAPON_DICT` during decoding).
*   `position`: `list[float]`, optional, size: 3
    *   The 3D position of the destruction event: `[x, y, z]`.
*   `score_time`: `float`, optional
    *   The time at which the score event occurred.
*   `killer_id`: `int`, optional
    *   The ID of the object (usually an aircraft) that caused the destruction.
*   `killer_name`: `str`, optional, size: 32
    *   The name of the player or AI who was credited with the kill, as a UTF-8 decoded string.
*   `killer_plane`: `str`, optional, size: 32
    *   The aircraft type used by the killer, as a UTF-8 decoded string.
*   `victim_id`: `int`, optional
    *   The ID of the object (aircraft or ground object) that was destroyed.
*   `victim_name`: `str`, optional, size: 32
    *   The name of the player or AI whose object was destroyed, as a UTF-8 decoded string.
*   `victim_plane`: `str`, optional, size: 32
    *   The aircraft or ground object type that was destroyed, as a UTF-8 decoded string.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_REPORTSCORE` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Uses `struct.unpack` to extract score report information from the byte data.
    *   Converts the `weapon_type` integer code to a weapon name string if it exists in `FSWEAPON_DICT`.
    *   Decodes `killer_name`, `killer_plane`, `victim_name`, and `victim_plane` from UTF-8 byte strings and removes trailing null characters.
    *   Returns: `None`

*   `encode(scored, weapon_type, position, score_time, killer_id, killer_name, killer_plane, victim_id, victim_name, victim_plane, with_size: bool = False)`
    *   Static method to encode score report data into a byte buffer representing the `FSNETCMD_REPORTSCORE` packet.
    *   Parameters:
        *   `scored`: `bool`
            *   Whether the event is scored (`True`) or not (`False`).
        *   `weapon_type`: `int` or `str`
            *   The type of weapon used. Can be integer code or weapon name string. If string, it will be converted to integer code using `FSWEAPON_DICT`.
        *   `position`: `list[float]`
            *   The 3D position of the event.
        *   `score_time`: `float`
            *   The time of the score event.
        *   `killer_id`: `int`
            *   ID of the killer object.
        *   `killer_name`: `str`
            *   Name of the killer.
        *   `killer_plane`: `str`
            *   Aircraft type of the killer.
        *   `victim_id`: `int`
            *   ID of the victim object.
        *   `victim_name`: `str`
            *   Name of the victim.
        *   `victim_plane`: `str`
            *   Object type of the victim.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.
    *   Encoding Logic:
        *   Converts `weapon_type` name string to integer code using `FSWEAPON_DICT` if necessary.
        *   Encodes `killer_name`, `killer_plane`, `victim_name`, and `victim_plane` to UTF-8 byte strings.
        *   Packs all the score report data into a byte buffer using `struct.pack` according to the defined format.
        *   Optionally prepends the buffer size if `with_size` is `True`.


## FSNETCMD_REQUESTTESTAIRPLANE

This packet is designed to request the server to spawn a test aircraft, specifically an F-15C, at a predefined location named "NORTH1000_01" and set the game mode to dogfight.  However, as noted in the code comments, there is no standard way to trigger this command from within the Yellow Sky (YS) game environment itself. It might be intended for debugging, testing purposes, or specific server-side scripts outside of typical gameplay.

This class inherits from `FSNETCMD_EMPTYPACKET`, indicating it is an empty packet type.

### Attributes

*   `buffer`: `bytes` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   The raw byte buffer of the packet data. As an empty packet, this will primarily contain just the packet identifier.
*   `should_decode`: `bool` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`. For `FSNETCMD_REQUESTTESTAIRPLANE`, the `decode` method (inherited from `FSNETCMD_EMPTYPACKET`) performs no action.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   Constructor for the `FSNETCMD_REQUESTTESTAIRPLANE` class. Inherits the constructor from `FSNETCMD_EMPTYPACKET`.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the `decode` method will be called, though it has no effect for this packet type.
    *   Returns: `None`

*   `decode(self)` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   Decode method for the `FSNETCMD_REQUESTTESTAIRPLANE` class.  Inherited from `FSNETCMD_EMPTYPACKET`, this method performs no action as it's designed to be an empty packet.
    *   Returns: `None`

*   `encode(with_size: bool = False)`
    *   Static method to encode the `FSNETCMD_REQUESTTESTAIRPLANE` packet. The packet only contains its identifier. Overrides the `encode` method from `FSNETCMD_EMPTYPACKET` to set the specific packet ID for `FSNETCMD_REQUESTTESTAIRPLANE`.
    *   Parameters:
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer containing the packet identifier.


## FSNETCMD_SERVER_FORCE_JOIN

This packet is sent by the server to a specific client to force that client to join the active game session. As indicated in the comments, this command essentially simulates the player pressing the 'J' key (the typical in-game key for joining a session), initiating the join process on the client's side.

This class inherits from `FSNETCMD_NULL`, inheriting its basic empty packet structure.

### Attributes

*   `buffer`: `bytes` (Inherited from `FSNETCMD_NULL`)
    *   The raw byte buffer of the packet data. As it inherits from `FSNETCMD_NULL`, this packet is essentially empty, with the buffer mainly containing the packet identifier.
*   `should_decode`: `bool` (Inherited from `FSNETCMD_NULL`)
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`. As it inherits from `FSNETCMD_NULL`, the `decode` method is a no-op, and this flag is effectively unused.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)` (Inherited from `FSNETCMD_NULL`)
    *   Constructor for the `FSNETCMD_SERVER_FORCE_JOIN` class.  It inherits the constructor from `FSNETCMD_NULL`.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data (though largely unused in this class).
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the `decode` method will be called (but it performs no action).
    *   Returns: `None`

*   `decode(self)` (Inherited from `FSNETCMD_NULL`)
    *   Decode method for the `FSNETCMD_SERVER_FORCE_JOIN` class.  It inherits the `decode` method from `FSNETCMD_NULL`, which performs no action since this is an empty packet.
    *   Returns: `None`

*   `encode(player_id, with_size: bool = False)`
    *   Static method to encode the `FSNETCMD_SERVER_FORCE_JOIN` packet.  Despite the parameter `player_id`, the current implementation does *not* actually include the player ID in the encoded packet.  The packet solely consists of its identifier.
    *   Parameters:
        *   `player_id`: `int`
            *   **Note:** While this parameter exists in the method signature, it is currently **unused** in the packet encoding logic. The packet as encoded does not contain player-specific identification.  It's possible this parameter is a remnant of a planned feature or an oversight.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer containing the packet identifier.
    *   Encoding Logic:
        *   Packs the packet ID for `FSNETCMD_SERVER_FORCE_JOIN` (47) into the buffer.
        *   Optionally prepends the buffer size if `with_size` is `True`.

**Important Note:**  The `encode` method currently ignores the `player_id` parameter.  The encoded packet, as it stands, is a general "force join" command and does not appear to be targeted at a specific player based on the provided code. If player-specific forced joining was intended, the encoding logic would need to be updated to include the `player_id` in the packet data.


## FSNETCMD_SKYCOLOR

This packet is used to set the sky color on the client side. This allows the server to control the visual appearance of the sky for connected clients, potentially for effects like time of day changes or weather conditions.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `redValue`: `int`, optional
    *   Red component of the sky color (0-255).
*   `greenValue`: `int`, optional
    *   Green component of the sky color (0-255).
*   `blueValue`: `int`, optional
    *   Blue component of the sky color (0-255).
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_SKYCOLOR` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Extracts the red, green, and blue color values from the buffer bytes at index 4, 5, and 6 respectively.
    *   Assigns these extracted values to the `redValue`, `greenValue`, and `blueValue` attributes.
    *   Returns: `None`

*   `encode(redValue: int, greenValue: int, blueValue: int, with_size: bool = False)`
    *   Static method to encode sky color data into a byte buffer representing the `FSNETCMD_SKYCOLOR` packet.
    *   Parameters:
        *   `redValue`: `int`
            *   Red color component (0-255).
        *   `greenValue`: `int`
            *   Green color component (0-255).
        *   `blueValue`: `int`
            *   Blue color component (0-255).
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.
    *   Encoding Logic:
        *   Packs the packet ID (49), `redValue`, `greenValue`, and `blueValue` into a byte buffer using `struct.pack` with the format string `"IBBB"`.
        *   If `with_size` is `True`, it prepends the buffer with its total length (including the size bytes themselves) as a 4-byte integer.


## FSNETCMD_SMOKECOLOR

This packet is used to communicate smoke color settings for aircraft. It is sent by the server to clients when a new aircraft joins with smoke enabled, and it's also sent by clients to the server when they join a session with smoke. This ensures that all clients are aware of the smoke settings of other players' aircraft.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `aircraft_id`: `int`, optional
    *   The ID of the aircraft for which the smoke color is being set.
*   `smoke_quantity`: `int`, optional
    *   Represents the quantity or density of the smoke. The exact meaning is game-specific, but it likely controls the visibility or thickness of the smoke trail.
*   `color`: `tuple[int, int, int]`, optional
    *   A tuple representing the RGB color of the smoke. Each value is an integer between 0 and 255, corresponding to the red, green, and blue components respectively.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_SMOKECOLOR` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Uses `struct.unpack` to extract the `aircraft_id`, `smoke_quantity`, and RGB color components from the byte data.
    *   Creates a tuple `color` from the unpacked red, green, and blue color values.
    *   Returns: `None`

*   `encode(aircraft_id, smoke_quantity, color, with_size: bool = False)`
    *   Static method to encode smoke color data into a byte buffer representing the `FSNETCMD_SMOKECOLOR` packet.
    *   Parameters:
        *   `aircraft_id`: `int`
            *   The ID of the aircraft.
        *   `smoke_quantity`: `int`
            *   The smoke quantity.
        *   `color`: `tuple[int, int, int]`
            *   A tuple containing the RGB color components for the smoke.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.
    *   Encoding Logic:
        *   Packs the packet ID (7), `aircraft_id`, `smoke_quantity`, and the individual red, green, and blue color components from the `color` tuple into a byte buffer using `struct.pack` with the format string `"IIBBBB"`.
        *   If `with_size` is `True`, it prepends the buffer with its total length (including the size bytes themselves) as a 4-byte integer.


## FSNETCMD_TESTPACKET

This packet, as indicated by its name, is primarily intended for testing and debugging purposes within the FSNET protocol. It is explicitly designed to be an empty packet, carrying no data payload beyond its identifier.

This class inherits from `FSNETCMD_EMPTYPACKET`, and therefore shares the basic structure of an empty packet type.

### Attributes

*   `buffer`: `bytes` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   The raw byte buffer of the packet data. Being an empty packet, this will mainly consist of the packet identifier.
*   `should_decode`: `bool` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.  For `FSNETCMD_TESTPACKET`, the `decode` method (inherited from `FSNETCMD_EMPTYPACKET`) performs no action.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   Constructor for the `FSNETCMD_TESTPACKET` class. Inherits the constructor from `FSNETCMD_EMPTYPACKET`.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the `decode` method will be called (although it has no effect).
    *   Returns: `None`

*   `decode(self)` (Inherited from `FSNETCMD_EMPTYPACKET`)
    *   Decode method for the `FSNETCMD_TESTPACKET` class. Inherited from `FSNETCMD_EMPTYPACKET`, this method performs no operation as it is intended to be an empty packet.
    *   Returns: `None`

*   `encode(with_size: bool = False)`
    *   Static method to encode the `FSNETCMD_TESTPACKET` packet.  The packet solely contains its identifier.  Overrides the `encode` method from `FSNETCMD_EMPTYPACKET` to specifically set the packet ID for `FSNETCMD_TESTPACKET`.
    *   Parameters:
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer containing the packet identifier.

## FSNETCMD_TEXTMESSAGE

This packet is used to transmit text messages within the game. It's used for in-game chat functionality.

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `raw_message`: `str`, optional
    *   The complete decoded text message directly from the buffer (from byte 12 onwards), before being parsed into user and message content.
*   `user`: `str`, optional
    *   The username of the message sender, extracted from the `raw_message` using regular expression parsing. This is typically enclosed in parentheses at the beginning of the message.
*   `message`: `str`, optional
    *   The actual text content of the message, extracted from the `raw_message` after the username (if present) is parsed out.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_TEXTMESSAGE` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Decodes the part of the buffer starting from byte 12 as a UTF-8 string and removes any trailing null characters, storing it in `self.raw_message`.
    *   Uses a regular expression `r"^\(([^)]+)\)(.+)"` to parse the `raw_message`:
        *   `^`: Matches the beginning of the string.
        *   `\(([^)]+)\)`: Matches a username enclosed in parentheses.
            *   `\(` and `\)`: Match literal parentheses.
            *   `([^)]+)`: Captures one or more characters that are not a closing parenthesis `)`. This captured group is assigned to `self.user`.
        *   `(.+)`: Matches and captures the rest of the string after the username part. This captured group is assigned to `self.message`.
    *   If the regular expression finds a match, it populates `self.user` and `self.message` with the captured groups. If no match is found, `self.user` will remain `None` and `self.message` might contain the entire `raw_message` or be an empty string depending on the regex outcome in that case.
    *   Returns: `None`

*   `encode(message: str, with_size: bool = False)`
    *   Static method to encode a text message into a byte buffer representing the `FSNETCMD_TEXTMESSAGE` packet.
    *   Parameters:
        *   `message`: `str`
            *   The text message content to be sent.
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.
    *   Encoding Logic:
        *   Packs the packet ID (32) and two placeholder integers (0, 0 - likely unused or reserved for future use) using `struct.pack` with the format string `"III"`.
        *   Encodes the input `message` string to UTF-8 bytes.
        *   Appends a null terminator byte (`b"\x00"`) to the encoded message.
        *   Concatenates the header (packet ID and placeholders) with the encoded message and null terminator to create the full buffer.
        *   If `with_size` is `True`, it prepends the buffer with its total length (including the size bytes themselves) as a 4-byte integer.

## FSNETCMD_WEAPONCONFIG

This packet is used to transmit weapon configuration settings for aircraft. It allows the server to inform clients about the weapon loadout of a specific aircraft, and potentially for clients to communicate their desired weapon configurations to the server (though the direction of communication isn't explicitly stated but implied by the class name).

### Attributes

*   `buffer`: `bytes`
    *   The raw byte buffer of the packet data.
*   `aircraft_id`: `int`, optional
    *   The ID of the aircraft to which this weapon configuration applies.
*   `number`: `int`, optional
    *   The number of weapon configuration entries.  Note in the `decode` method, this number is modified by `self.number = self.number & (~1)`, which effectively makes it an even number by clearing the least significant bit. This suggests weapon configurations might be sent in pairs.
*   `weapon_config`: `dict[str, int or list[int]]`, optional
    *   A dictionary representing the weapon configuration.
        *   Keys are weapon type names (strings, looked up from `FSWEAPON_DICT`).
        *   Values are either:
            *   An integer representing the count of the weapon.
            *   For smoke weapons, a list of 3 integers `[r, g, b]` representing the RGB color components.
*   `should_decode`: `bool`
    *   A flag indicating whether the buffer should be decoded upon initialization. Defaults to `True`.

### Methods

*   `__init__(self, buffer: bytes, should_decode: bool = True)`
    *   Constructor for the `FSNETCMD_WEAPONCONFIG` class.
    *   Parameters:
        *   `buffer`: `bytes`
            *   The byte buffer containing the packet data.
        *   `should_decode`: `bool`, default = `True`
            *   If `True`, the buffer will be decoded immediately upon object creation.
    *   Returns: `None`

*   `decode(self)`
    *   Decodes the `buffer` attribute to populate the object's attributes.
    *   Unpacks the `aircraft_id` and `number` of weapon entries from the buffer header.
    *   Applies bitwise AND with the inverse of 1 (`~1`) to `self.number` to ensure it's even: `self.number = self.number & (~1)`.
    *   Iterates through pairs of weapon type and count based on `self.number // 2`.
    *   For each pair:
        *   Unpacks a weapon type code (`typ`) and a count (`count`).
        *   Looks up the weapon type name string from `FSWEAPON_DICT` using the code `typ`.
        *   If the weapon type name contains "SMOKE", it interprets the `count` as a packed RGB color value and unpacks it into individual `r`, `g`, `b` components using bitwise operations:
            *   `r = (count >> 10) & 31`
            *   `g = (count >> 5) & 31`
            *   `b = count & 31`
            *   Then scales these 5-bit color components back to 8-bit range:
                *   `r = (r >> 2) + (r << 3)`
                *   `g = (g >> 2) + (g << 3)`
                *   `b = (b >> 2) + (b << 3)`
            *   Stores the color as a list `[r, g, b]` as the value in `self.weapon_config` for the corresponding weapon type.
        *   Otherwise (if not a smoke weapon), stores the unpacked `count` directly as the value in `self.weapon_config` for the weapon type name.
    *   Returns: `None`

*   `encode(aircraft_id: int, weapon_config: dict, with_size: bool = False)`
    *   Static method to encode weapon configuration data into a byte buffer representing the `FSNETCMD_WEAPONCONFIG` packet.
    *   Parameters:
        *   `aircraft_id`: `int`
            *   The ID of the aircraft.
        *   `weapon_config`: `dict[str, int or list[int]]`
            *   A dictionary containing the weapon configuration (weapon type names as keys, counts or RGB color lists as values).
        *   `with_size`: `bool`, default = `False`
            *   If `True`, prepends the buffer with its size as a 4-byte integer.
    *   Returns: `bytes`
        *   The encoded byte buffer.
    *   Encoding Logic:
        *   Packs the packet ID (36), `aircraft_id`, and the number of weapon configuration entries (multiplied by 2, as pairs of weapon type and count are expected) into the buffer.
        *   Iterates through the `weapon_config` dictionary.
        *   For each weapon type and count:
            *   If the weapon type is a string (name) and is present in `FSWEAPON_DICT.values()`, it retrieves the integer weapon code from `FSWEAPON_DICT.keys()`.
            *   If the weapon type code is in the smoke weapon range (32-39) and the count is a list (assumed to be RGB color):
                *   Extracts `r`, `g`, `b` from the `count` list.
                *   Scales down the 8-bit color components to 5-bit range:
                    *   `r = (r * 31) / 255`
                    *   `g = (g * 31) / 255`
                    *   `b = (b * 31) / 255`
                *   Packs the 5-bit RGB values into a single integer `count` using bitwise operations: `count = (int(r) << 10) + (int(g) << 5) + int(b)`.
            *   Packs the weapon type code (`typ`) and the (potentially modified) `count` as two short integers into the buffer.
        *   If `with_size` is `True`, it prepends the buffer with its total length (including the size bytes themselves) as a 4-byte integer.

*   `addSmoke(aircraft_id: int)`
    *   Static method to quickly create and encode a `FSNETCMD_WEAPONCONFIG` packet to add smoke weapons to an aircraft.
    *   Parameters:
        *   `aircraft_id`: `int`
            *   The ID of the aircraft to add smoke to.
    *   Returns: `bytes`
        *   The encoded byte buffer for adding smoke weapons.
    *   Functionality:
        *   Calls `FSNETCMD_WEAPONCONFIG.encode` to create the packet.
        *   Sets the `aircraft_id`.
        *   Creates a `weapon_config` dictionary with three smoke weapon types (32, 33, 34 - likely representing different smoke launcher positions or types) and sets their color to gray `[66, 66, 66]`.
        *   Sets `with_size=True` to include the packet size prefix in the encoded buffer.
