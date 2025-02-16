# Introduction

Hooks are blocking functions that are called when a specific event occurs.
They are used to modify the behavior of the proxy. Every hook function
must return a `bool` value, `True` if the packet that triggered the hook
should be sent to the client/server or `False` if the packet should be
dropped and not sent.

# Hook Structure

In main `Plugin` Class, there must be a `register` method, under which
you must declare your hooks.
> eg.
> ```python
> def register(self, plugin_manager):
>        self.plugin_manager = plugin_manager
>        self.plugin_manager.register_hook('on_flight_data', self.on_receive)
>```
> This will trigger the `on_receive` method of your plugin when the `on_flight_data` hook is triggered.

# Hook Function Structure

Every hook function must have the following structure:
```python
def on_receive(self, data, player, message_to_client, message_to_server)
```
Where:
- `data` is the packet object that triggered the hook, It is a `bytes` object.
The data is sent without the header.(that is the size of the packet)

- `player` is the `Player` object that triggered the hook.

- `message_to_client` is the list that contains the packets that will be sent to the client.
  you must append to it and return a value for the packet to be sent.

- `message_to_server` is the list that contains the packets that will be sent to the server.
  you must append to it and return a value for the packet to be sent.

> You must return a `bool` value, `True` if the packet that triggered the hook should be
> sent to the client/server or `False` if the packet should be dropped and not sent.

# Hook List

## Client to Server Side

| Hook                    | Packet Object         |
|-------------------------|-----------------------|
| `on_login`              | `FSNETCMD_LOGON`      |
| `on_logout`             | `FSNETCMD_LOGOFF`     |
| `on_error`              | `FSNETCMD_ERROR`      |
| `on_load_field`         | `FSNETCMD_LOADFIELD`  |
| `on_add_object`         | `FSNETCMD_ADDOBJECT`  |
| `on_readback`           | `FSNETCMD_READBACK`   |
| `on_smoke_color`        | `FSNETCMD_SMOKECOLOR` |
| `on_join_request`       | `FSNETCMD_JOINREQUEST`|
| `on_join_approval`      | `FSNETCMD_JOINAPPROVAL`|
| `on_reject_join_request`| `FSNETCMD_REJECTJOINREQ`|
| `on_flight_data`        | `FSNETCMD_AIRPLANESTATE`|
| `on_unjoin`             | `FSNETCMD_UNJOIN`     |
| `on_remove_airplane`    | `FSNETCMD_REMOVEAIRPLANE`|
| `on_request_test_airplane`| `FSNETCMD_REQUESTTESTAIRPLANE`|
| `on_kill_server`        | `FSNETCMD_KILLSERVER` |
| `on_prepare_simulation` | `FSNETCMD_PREPARESIMULATION`|
| `on_test_packet`        | `FSNETCMD_TESTPACKET` |
| `on_lockon`             | `FSNETCMD_LOCKON`     |
| `on_remove_ground`      | `FSNETCMD_REMOVEGROUND`|
| `on_missile_launch`     | `FSNETCMD_MISSILELAUNCH`|
| `on_get_damage`         | `FSNETCMD_GETDAMAGE`  |
| `on_weapon_config`      | `FSNETCMD_WEAPONCONFIG`|
| `on_air_cmd`            | `FSNETCMD_AIRCMD`     |
| `on_chat`               | `FSNETCMD_TEXTMESSAGE`|
| `on_environment`        | `FSNETCMD_ENVIRONMENT`|
| `on_sky_color`          | `FSNETCMD_SKYCOLOR`   |
| `on_fog_color`          | `FSNETCMD_FOGCOLOR`   |
| `on_list`               | `FSNETCMD_LIST`       |

<br>

## Server to Client Side

| Hook                          | Packet Object         |
|-------------------------------|-----------------------|
| `on_login_server`             | `FSNETCMD_LOGON`      |
| `on_logout_server`            | `FSNETCMD_LOGOFF`     |
| `on_error_server`             | `FSNETCMD_ERROR`      |
| `on_load_field_server`        | `FSNETCMD_LOADFIELD`  |
| `on_add_object_server`        | `FSNETCMD_ADDOBJECT`  |
| `on_readback_server`          | `FSNETCMD_READBACK`   |
| `on_smoke_color_server`       | `FSNETCMD_SMOKECOLOR` |
| `on_join_request_server`      | `FSNETCMD_JOINREQUEST`|
| `on_join_approval_server`     | `FSNETCMD_JOINAPPROVAL`|
| `on_reject_join_request_server`| `FSNETCMD_REJECTJOINREQ`|
| `on_flight_data_server`       | `FSNETCMD_AIRPLANESTATE`|
| `on_unjoin_server`            | `FSNETCMD_UNJOIN`     |
| `on_remove_airplane_server`   | `FSNETCMD_REMOVEAIRPLANE`|
| `on_request_test_airplane_server`| `FSNETCMD_REQUESTTESTAIRPLANE`|
| `on_kill_server_server`       | `FSNETCMD_KILLSERVER` |
| `on_prepare_simulation_server`| `FSNETCMD_PREPARESIMULATION`|
| `on_test_packet_server`       | `FSNETCMD_TESTPACKET` |
| `on_lockon_server`            | `FSNETCMD_LOCKON`     |
| `on_remove_ground_server`     | `FSNETCMD_REMOVEGROUND`|
| `on_missile_launch_server`    | `FSNETCMD_MISSILELAUNCH`|
| `on_get_damage_server`        | `FSNETCMD_GETDAMAGE`  |
| `on_weapon_config_server`     | `FSNETCMD_WEAPONCONFIG`|
| `on_air_cmd_server`           | `FSNETCMD_AIRCMD`     |
| `on_chat_server`              | `FSNETCMD_TEXTMESSAGE`|
| `on_environment_server`       | `FSNETCMD_ENVIRONMENT`|
| `on_sky_color_server`         | `FSNETCMD_SKYCOLOR`   |
| `on_fog_color_server`         | `FSNETCMD_FOGCOLOR`   |
| `on_list_server`              | `FSNETCMD_LIST`       |
