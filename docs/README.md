# Sakuya AC API Documentation

Sakuya AC : The perfect and elegant YSFlight Proxy Software. It is written in Python. Uses
asyncio so that it doesn't lag. This documentation will guide you through creating your
own Plugin for Sakuya AC.

## Getting Started

To get started with Sakuya AC, you need to have Python 3.9 or higher installed on your system.

### Basic Structure of a Plugin

There are two ways to work with the proxy:
1. Hooks : These actually modify the incoming/outgoing packets from YSF Server, these are blocking
and can be used to modify the packets.
- Example : G Limiter, Chat Filter; As these need to modify the packets at that instant

2. Commands : These are non essential and do not modify the incoming/outgong packets, you can send your
own packets to server/client. These are non blocking.
- Example : Fog color changer, Ban command; these do not need to modify any commands at that instant

- All plugins are saved in plugins directory in the root of the project.

### Simple Command Plugin

```python
"""
This is an example test command!
"""

from lib import YSchat
from time import sleep

ENABLED = False

class Plugin:
    def __init__(self):
        self.plugin_manager = None

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugin_manager.register_command('test', self.test)
        self.plugin_manager.register_command('timer', self.timer)

    def test(self, full_message, player, message_to_client, message_to_server):
        message_to_client.append(YSchat.message("Test command received"))
        return True

    def timer(self, full_message, player, message_to_client, message_to_server):
        sleep(5)
        message_to_client.append(YSchat.message("Timer ended"))
        return True
```
- You start the plugin by giving it a description,
- You must have a global ENABLED variable, which is set by the user
  if they wish to enable the plugin or not
- You must have a class Plugin, which has a register method
  use ``register_command`` to register a command.
  -- ``self.plugin_manager.register_command('command_name', self.function_name)``
- now self.function_name must take the shown parameters

### Simple Hooks Plugin

```python
"""This plugin will flash the lights/fog colour whenever a flight status update
is sent
It can be enabled here by changing the value of ENABLED to True."""
from lib.PacketManager.packets import FSNETCMD_SKYCOLOR, FSNETCMD_FOGCOLOR
from random import randint
ENABLED = True

class Plugin:
    def __init__(self):
        self.plugin_manager = None

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugin_manager.register_hook('on_flight_data', self.on_receive)

    def on_receive(self, data, player, messages_to_client, *args):
        sky_colour_packet = FSNETCMD_SKYCOLOR.encode(randint(0, 255), randint(0, 255), randint(0, 255), True)
        fog_colour_packet = FSNETCMD_FOGCOLOR.encode(randint(0, 255), randint(0, 255), randint(0, 255), True)
        messages_to_client.append(sky_colour_packet)
        messages_to_client.append(fog_colour_packet)
        return True
```
- Unlike the previous example, this uses a hook which modifies the packet from the server at that instant
- You must return True at the end of the function to indicate that the original packet will be sent
  -- (In this case, the orginal packet is the flight data, not sending will cause the client to
  not receive the flight data)
- returning False, means the orginal packet which triggered the hook will not be sent to the YSF server,
this is useful for chat filters etc.

## Object Descriptions

### ``Aircraft`` Class

An aircraft class designed to hold information from airplane state and related packets within a flight simulation environment. This class manages aircraft properties such as position, attitude,
life, configuration etc.

#### Attributes

*   `parent`:  Reference to the parent object.
*   `name` (*str*):  Aircraft name (empty initially).
*   `position` (*list[float]*):  3D position [x, y, z] (initially `[0, 0, 0]`).
*   `attitude` (*list[float]*): Attitude angles (initially `[0, 0, 0]`).
*   `initial_config` (*dict*): Initial configuration parameters (empty initially).
*   `custom_config` (*dict*): Custom configuration parameters (empty initially).
*   `life` (*int*):  Current life/health (initially `-1`).
*   `prev_life` (*int*): Previous life value (initially `-1`).
*   `id` (*int*):  Unique identifier (initially `-1`).
*   `last_packet`: Last received packet (initially `None`).
*   `damage_engine_warn_sent` (*bool*): Damage engine warning flag (initially `False`).
*   `last_over_g_message` (*int*): Last over-G message timestamp (initially `0`).
*   `just_repaired` (*bool*): Just repaired flag (initially `False`).

#### Methods

##### `reset(self)`

**Description:**

Resets all aircraft attributes to their initial defaults.

**Parameters:**

*   `self`: The `Aircraft` instance.

**Returns:**

*   `None`

**Resets attributes:** `name`, `position`, `attitude`, `initial_config`, `custom_config`, `life`, `prev_life`, `id`, `last_packet`, `damage_engine_warn_sent`, `just_repaired`.

##### `set_position(self, position: list)`

**Description:**

Sets the aircraft's 3D position.

**Parameters:**

*   `self`: The `Aircraft` instance.
*   `position` (*list[float]*): [x, y, z] coordinates.

**Returns:**

*   `None`

##### `set_attitude(self, attitude: list)`

**Description:**

Sets the aircraft's attitude.

**Parameters:**

*   `self`: The `Aircraft` instance.
*   `attitude` (*list[float]*): Attitude angles.

**Returns:**

*   `None`

##### `get_position(self)`

**Description:**

Returns the aircraft's 3D position.

**Parameters:**

*   `self`: The `Aircraft` instance.

**Returns:**

*   *list[float]*: [x, y, z] coordinates.

##### `get_altitude(self)`

**Description:**

Returns the aircraft's altitude (Z-coordinate) in meters.

**Parameters:**

*   `self`: The `Aircraft` instance.

**Returns:**

*   *float*: Altitude in meters.

##### `get_attitude(self)`

**Description:**

Returns the aircraft's attitude.

**Parameters:**

*   `self`: The `Aircraft` instance.

**Returns:**

*   *list[float]*: Attitude angles.

##### `set_initial_config(self, config: dict)`

**Description:**

Sets the aircraft's initial configuration.

**Parameters:**

*   `self`: The `Aircraft` instance.
*   `config` (*dict*): Initial configuration key-value pairs.

**Returns:**

*   `None`

##### `get_initial_config_value(self, key: str)`

**Description:**

Retrieves a value from `initial_config`.

**Parameters:**

*   `self`: The `Aircraft` instance.
*   `key` (*str*): Configuration key.

**Returns:**

*   *Any*: Configuration value or `None` if key not found.

##### `set_custom_config_value(self, key: str, value)`

**Description:**

Sets a custom configuration value.

**Parameters:**

*   `self`: The `Aircraft` instance.
*   `key` (*str*): Configuration key.
*   `value` (*Any*): Configuration value.

**Returns:**

*   `None`

##### `add_state(self, packet: FSNETCMD_AIRPLANESTATE)`

**Description:**

Updates aircraft state from an `FSNETCMD_AIRPLANESTATE` packet.

**Parameters:**

*   `self`: The `Aircraft` instance.
*   `packet` (*FSNETCMD_AIRPLANESTATE*): Airplane state packet.

**Returns:**

*   *FSNETCMD_AIRPLANESTATE* or *None*: Input `packet` if processed, `None` if ID mismatch.

**Functionality:** Updates `life`, `position`, `attitude` and stores the `last_packet`.

##### `check_command(self, command: FSNETCMD_AIRCMD)`

**Description:**

Processes an `FSNETCMD_AIRCMD` packet for configuration commands.

**Parameters:**

*   `self`: The `Aircraft` instance.
*   `command` (*FSNETCMD_AIRCMD*): Air command packet.

**Returns:**

*   `None`

**Functionality:** Updates `initial_config` based on the command. Logs the command in debug.

##### `set_afterburner(self, enabled: bool)`

**Description:**

Toggles the afterburner if available.

**Parameters:**

*   `self`: The `Aircraft` instance.
*   `enabled` (*bool*): `True` to enable, `False` to disable.

**Returns:**

*   *FSNETCMD_AIRCMD* or *None*: Result of `FSNETCMD_AIRCMD.set_afterburner` if afterburner available, else `None`.

**Functionality:** Checks for "AFTBURNR" in `initial_config` and sends command if available.

### `Player` Class

The `Player` class represents a connected client. It stores key information such as their username, alias, IP address,
 and the `Aircraft` object they are currently piloting.

#### Attributes

*   **`username`**:  The player's username (string). Set via the `login` method.
*   **`alias`**: The player's alias (string). Set via the `login` method.
*   **`aircraft`**: An `Aircraft` object instance representing the aircraft the player is currently flying. Initially an empty `Aircraft` object and populated through `check_add_object` or `set_aircraft`.
*   **`version`**: The client version (integer). Set via the `login` method.
*   **`ip`**: The player's IP address (string). Set via the `set_ip` method.
*   **`streamWriterObject`**: Object for handling network communication with the player's client.
*   **`is_a_bot`**: A boolean flag indicating if the player is considered a bot. Initially `True`, and is intended to be set to `False` after a successful `LOGIN` packet is processed, to differentiate real players from initial bot-like states.

#### Methods

##### `set_aircraft(aircraft: Aircraft)`

```python
set_aircraft(aircraft: Aircraft)
```
Assigns a specific `Aircraft` object to this player, representing the aircraft they are currently flying. Useful when you need to manually set or update the player's aircraft.

*   **`aircraft`**: An `Aircraft` object instance.

##### `login(packet: FSNETCMD_LOGON)`

```python
login(packet: FSNETCMD_LOGON)
```
Processes a login packet (`FSNETCMD_LOGON`) to extract and set the player's `username`, `alias`, and client `version`. This is typically called upon receiving a successful login packet from the client.

*   **`packet`**: An `FSNETCMD_LOGON` packet instance containing login details.

##### `set_ip(ip)`

```python
set_ip(ip)
```
Sets the IP address associated with this player's connection.

*   **`ip`**: A string representing the player's IP address.

##### `check_add_object(packet: FSNETCMD_ADDOBJECT)`

```python
check_add_object(packet: FSNETCMD_ADDOBJECT)
```
Checks if an `ADDOBJECT` packet (`FSNETCMD_ADDOBJECT`) pertains to this player based on the pilot's username in the packet. If it does, it initializes a new `Aircraft` object for the player using data from the packet, effectively setting the aircraft they are flying. Returns `True` if the aircraft was initialized, `False` otherwise.

*   **`packet`**: An `FSNETCMD_ADDOBJECT` packet instance containing aircraft creation details.
*   **Returns**: `True` if the packet was for this player and the aircraft was initialized, `False` otherwise.

##### `__str__()`

```python
__str__()
```
Returns a user-friendly string representation of the `Player` object. This string includes the player's `username`, the name of their `aircraft`, and its current `position`. Useful for logging and debugging purposes.

*   **Returns**: A descriptive string of the `Player` object.
