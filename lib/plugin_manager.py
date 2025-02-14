import importlib
import os
import sys
from logging import info

PLUGIN_DIR = os.path.join(os.path.dirname(__file__), '../plugins')
sys.path.append(PLUGIN_DIR)

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.hooks= {}
        self.load_plugins()

    def load_plugins(self):
        for plugin in os.listdir(PLUGIN_DIR):
            plugin_path = os.path.join(PLUGIN_DIR, plugin)
            if plugin.endswith('.py') and not plugin.startswith('__'):
                plugin_name = plugin[:-3]
                plugin_module = importlib.import_module(plugin_name)
                if hasattr(plugin_module, 'Plugin'):
                    if plugin_module.ENABLED:
                        plugin_instance = plugin_module.Plugin()
                        self.register_plugin(plugin_instance)
                        info(f"Loaded plugin {plugin_name}")
                        self.plugins[plugin_name] = plugin_instance
            elif os.path.isdir(plugin_path) and os.path.exists(os.path.join(plugin_path, '__init__.py')):
                plugin_module = importlib.import_module(plugin)
                if hasattr(plugin_module, 'Plugin'):
                    if plugin_module.ENABLED:
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

    def triggar_hook(self, hook_name, data, *args, **kwargs):
        """Triggars the callbacks for the hook.
        If a callback returns False, then the original data is set to None
        and not forwarded to the destination. This is useful for modifying
        packets."""
        keep_orignal = True
        if hook_name in self.hooks:
            for callback in self.hooks[hook_name]:
                keep = callback(data, *args, **kwargs)
                if keep == False:
                    keep_orignal = False
        return keep_orignal
