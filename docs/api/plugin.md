# Single File Plugins

These plugins are contained in a single `.py` files, recomemded for small plugins.

```python
"""
This is an example test command!
"""

from lib import YSchat

# ENABLED variable must be present in your plugin otherwise it will
# fail to load. This is used by user to change the state of the plugin

ENABLED = True

class Plugin:
    def __init__(self):
        # Intialise the plugin here
        self.plugin_manager = None

    def register(self, plugin_manager):
        # Here you declare functions of your plugin
        # Bind to plugin manager
        self.plugin_manager = plugin_manager
        # Register your plugin commands
        self.plugin_manager.register_command('test', self.test)
        # Register your plugin hooks
        self.plugin_manager.register_hook('on_flight_data', self.on_receive)

    # Command Function
    def test(self, full_message, player, message_to_client, message_to_server):
        message_to_client.append(YSchat.message("Test command received"))
        return True

    # Hook Function
    def on_receive(self, data, player, message_to_client, message_to_server):
        print(f"Received flight data of {player.username}")
        return True
```

# Multi File Plugins

These plugins are contained in a directory with multiple files, recomemded for large plugins.

```bash
plugin/
├── Plugin.py
└── __init__.py
```

```python
# __init__.py
from .Plugin import Plugin
from .Plugin import ENABLED
```

```python
# Plugin.py
"""
This is a multi file plugin example
"""
ENABLED = True

class Plugin:
    def __init__(self):
        self.plugin_manager = None

    def register(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.plugin_manager.register_hook('on_flight_data', self.on_flight_data)

    def on_flight_data(self, data, player,message_to_client, message_to_server):
        print(f"Received flight data of {player.username}")
        return True
```
