# Introduction

Commands can be called by users joined in the server using the prefix defined
in the `config.py` file concartinated with the command name. Commands, unlike hooks
are *non-blocking*. Meaning the proxy continues its operation without waiting for
the function to return a value. It is useful when sending your own packets to the
server or client.

# Command Structure

In main `Plugin` Class, there must be a `register` method, under which
you must declare your commands.
> eg.
> ```python
> def register(self, plugin_manager):
>        self.plugin_manager = plugin_manager
>        self.plugin_manager.register_command('test', self.test, "This is a test command", 'alias')
>```

``register_command`` takes 4 arguments:
- Command Name (string) : This is the first argument, which tells the main command name for your command.
- Callback : This is function that will be run when a user runs your command. Structure of a command
function is shown below.
- Help text (string, optional) : This string contains what your command does, it will be displayed in ``help`` command.
- Alias (string, optional) : Helps you define an alias for your command. Useful for creating shorter command name for ease of use.

# Command Function Structure

Every command function must have the following structure:
```python
def test(self, full_message, player, message_to_client, message_to_server)
```
Where:
- `full_message` is the full message sent by the user. (including the command, but excluding the username)
- `player` is the `Player` object that triggered the command.
- `message_to_client` is the list that contains the packets that will be sent to the client.
  you must append to it and return a value for the packet to be sent.
- `message_to_server` is the list that contains the packets that will be sent to the server.
  you must append to it and return a value for the packet to be sent.

> You must always return a `True` value, otherwise the proxy thinks your command ran into an error.
