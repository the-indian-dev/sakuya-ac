import importlib
import os
import sys
from logging import info, warning

PLUGIN_DIR = os.path.join(os.path.dirname(__file__), '../plugins')
sys.path.append(PLUGIN_DIR)

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.hooks= {}
        self.commands = {}
        self.help_message = "List of Available Commands:\n"
        self.load_plugins()

    def load_plugins(self):
        for plugin in os.listdir(PLUGIN_DIR):
            plugin_path = os.path.join(PLUGIN_DIR, plugin)
            if plugin.endswith('.py') and not plugin.startswith('__'):
                plugin_name = plugin[:-3]
                plugin_module = importlib.import_module(plugin_name)
                if hasattr(plugin_module, 'ENABLED') and plugin_module.ENABLED:
                    if hasattr(plugin_module, 'Plugin'):
                        plugin_instance = plugin_module.Plugin()
                        self.register_plugin(plugin_instance)
                        info(f"Loaded plugin {plugin_name}")
                        self.plugins[plugin_name] = plugin_instance
            elif os.path.isdir(plugin_path) and os.path.exists(os.path.join(plugin_path, '__init__.py')):
                plugin_module = importlib.import_module(plugin)
                if hasattr(plugin_module, 'ENABLED') and plugin_module.ENABLED:
                    if hasattr(plugin_module, 'Plugin'):
                        plugin_instance = plugin_module.Plugin()
                        self.register_plugin(plugin_instance)
                        info(f"Loaded plugin {plugin}")
                        self.plugins[plugin] = plugin_instance

    def register_plugin(self, plugin):
        """Registers the plugin with the plugin manager"""
        plugin.register(self)

    def register_hook(self, hook_name, callback):
        """Registers the hook with the plugin manager"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(callback)

    def register_command(self, command_name, callback, help_text="No Description", alias:str=None):
        """Registers the command with the plugin manager
        Set help text to help users understand what your command does.
        """
        if command_name in self.commands:
            warning(f"Command {command_name} already registered, Ignoring this registration")
        else:
            self.commands[command_name] = callback
            if alias == None:
                self.help_message = self.help_message + f"/{command_name} : {help_text}\n"
        if alias != None:
            if alias in self.commands:
                warning(f"Command {alias} already registered, Ignoring this registration")
            else:
                self.commands[alias] = callback
                self.help_message = self.help_message + f"/{command_name} [{alias}] : {help_text}\n"



    def triggar_hook(self, hook_name, data, *args, **kwargs):
        """Triggars the callbacks for the hook.
        If a callback returns False, then the original data is set to None
        and not forwarded to the destination. This is useful for modifying
        packets."""
        keep_original = True
        if hook_name in self.hooks:
            for callback in self.hooks[hook_name]:
                keep = callback(data, *args, **kwargs)
                if type(keep) == bool:
                    if keep == False:
                        keep_original = False
                else:
                    warning(f"Return value of {callback} is not a boolean")
        return keep_original

    def trigger_command(self, command:str, player,  full_message:str, message_to_client:list, message_to_server:list):
        """Triggers the command"""
        if command in self.commands:
            self.commands[command](full_message, player, message_to_client, message_to_server)
            return True
        return False
