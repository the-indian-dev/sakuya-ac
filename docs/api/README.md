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
