# Installing Plugins
!> Plugins can be harmful to your computer, please install from trusted sources.
  We are NOT responsible for installing plugins from untrusted sources.

1. Download plugins from a trusted source
2.
- If the plugin is a ``.py`` file then put it in the ``plugins`` directory
- If the plugin is a ``.zip`` file then extract it and put it in the ``plugins`` directory
3. Set the ``ENABLED`` variable in the plugin file to ``True``

# Configuring Plugins

Plugins installed are located in the ``plugins`` directory in root.

- For single file plugins

  Single file plugins are those which only have a single ``.py`` file and are
  located under the ``plugins`` directory directly.

  1. Open the ``.py`` file of the plugin
  2. You will see configurable variables on the top of the file which will be written in
  capital letters
  > eg.
  > ```python
  > ENABLED = True # Enable the Plugin, setting to false will not load the plugin into Sakuya AC
  > OTHER_VAR = 10 # Some other variable, can be changed accordingly
  >
  > another_var = 120 # Since this is in small letter,
  > # not recommended to change, these are inner workings of the plugin
  > ```
  3. Save the edited file and run the proxy

- For multi file plugins

  1. Open the sub directory, the folor inside ``Plugins`` folder where the plugin is located
  2. You will see the main ``Plugin.py`` file along with other file. Edit this file to configure the plugin.
  3. Follow the same instructions as above to configure the plugin.

# Standard Plugin Configuration

## Over G Damage

This plugin allows you to set the damage that a player will take when they go over the G limit.
The G limit is congigurable in the main ``config.py`` file.

Configurable Variables:
- ``INTERVAL`` : The interval in which the plugin checks for G Limit, measured in seconds. Default is ``0.2`` seconds.

## Radar

This plugin allows radar functionality in the game. It will not allow
enemy aircrafts of different IFFs to be seen on each other's radar while not in range

- Configurable Variables:
  - ``RADIUS`` : The range of the radar in meters. Default is ``5000`` meters.
    1. ``5000`` meters is quite small, it is only for testing reasons. Can be fun
      for hide and seek games.
    2. For relastic combat, set it to ``50000`` meters.
    3. For fast paced games, I recommend setting it to ``20000`` meters.

## Refuel

This plugin adds Mid air refueling functionality to the game.

- Configurable Variables:
  - ``FUEL_RATE`` : The rate at which the aircraft refuels in liters per second. Default is ``50`` kgs per second.
    This might be bit fast compared to real world. For realistic gameplay, set it to ``10`` kgs per second.

  - ``REFUEL_RADIUS`` : The radius in which the aircraft can refuel. Default is ``500`` meters.
    YSFlight is prone to distance lag, please set it 100-200 m more than what you want to account for distance lag.

## Custom Aircraft List

This plugin allows you send custom aircraft lst to the all the Player. It is more
of a example plugin and doesnt have any real use case.

- ``custom_list.json`` file contains the list of aircraft's to be sent to the client via the plugin

## Smoke on Damage

This plugins allows Engine breakdown mechanics(The plane cant turn on afterburner when it haslow health) and
plane release smoke when it is damaged. The minimum life at which this happens can be configured
via the main ``config.py`` file.

## Aircraft Replacer

Example Plugin for developers to understand, replaces any aircraft that player flies with a
EUROFIGHTER Typhoon.

## All Caps

Example Plugin, converts all the chat messages to uppercase.

## Chat Weather Setter

This plugin allows the clients to set the weather for themselves client side via chat commands.
It allows for people to take cool screenshots. No configurable variable.

## Command Test

Template plugin for developers

## Discolight

!> Ellipsy Warning! This plugin is not recommended for use in public servers as it can cause seizures.

Changes the sky and fog color rapidly to simulate "disco" lights.
