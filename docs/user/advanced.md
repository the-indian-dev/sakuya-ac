# `config.py` Configuration

The `config.py` file is the main configuration file for Sakuya AC. It contains the following configuration options:

### `LOGGING_LEVEL`

The logging level for the proxy. The logging level can be one of the following:
1. `DEBUG` : Logs all messages (Recomedded for debugging and reporting issues)
2. `INFO` : Logs only informational messages (Default, Recomended for normal use)
3. `WARNING` : Logs only warning messages
4. `CRTITICAL` : Logs only critical messages

### `SERVER_HOST`

The IP address of the YSF Server. The proxy will connect to this IP address.
For local server, use `"127.0.0.1"`, It takes string values, so make sure to
put quotaion marks around the IP address.

### `SERVER_PORT`

The port of the YSF Server. The proxy will connect to this port. The default is
`7915`, which is the default port for YSF Server. It takes integer values. Do not
put quotation marks around the port number.

### `PROXY_PORT`

The port on which the proxy will run. The default is `9000`. It takes integer values.

### `WELCOME_MESSAGE`

The welcome message that will be displayed when a client logs in to the YSFlight server.
It takes string values. You can use the following placeholders in the message:
- `{username}` : The username of the client
> eg. `Welcome {username} to the server!`
> This will display `Welcome Sakuya to the server!` when a client with username
> `Sakuya` logs in.

### `PREFIX`

This is the prefix for the chat commands in your server. The default is `/`.
It takes string values. Make sure to put quotation marks around the prefix.
> eg. If you set the prefix to `!`, then the command to change fog color would be `!fog`

!> Messages starting with prefix will be treated as commands. Make sure to set a
   prefix that is not used in normal chat messages.

### `YSF_VERSION`

The version for your YSFlight server. The default is `20150425`. It takes integer values.

### `G_LIM`

The G-Limiter value for your server. The default is `4`. It takes integer values.
The client will take damage if absolute value of their G force exceeds this value.

- To change the interval at which the client takes G Force Damage, change the value of
`INTERVAL` in `plugins/over_g_damage.py`. The default is `0.2`, which means the client
takes damage every 0.2 seconds.

### `HEALTH_HACK_MESSAGE`

The message that will be displayed when a client tries to hack their health. It takes
string values. The username of the client is automatically appended to the end of the
message

>eg. `HEALTH_HACK_MESSAGE = "Detected for Health Hack"`
> This will display `Detected for Health Hack by Sakuya` when a client tries to cheat.

### `SMOKE_PLANE`

If the plane should smoke when it has a life lower than `SMOKE_LIFE`. The default is `True`.

### `SMOKE_LIFE`

The life value below which the plane should start smoking. The default is `5`. It takes integer values.

### `DISCORD_ENABLED`

If the Discord Chat Sync should be enabled. The default is `False`. It takes boolean values.
You must `aiohttp` installed to use this feature.

Setting up Discord Chat Sync is documented [here](/user/discord.md)

### `DISCORD_TOKEN`

The Discord Bot Token for the Discord Chat Sync. It takes string values.

### `CHANNEL_ID`

The Channel ID of the channel where the chat messages will be sent. It takes integer values.
