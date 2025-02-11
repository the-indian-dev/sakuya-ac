from logging import DEBUG, WARN, INFO, CRITICAL

# Configuration
# Logging Level : Most of the times having INFO level is enough
# But while submitting issues, please consider sending the logs with DEBUG level
LOGGING_LEVEL = INFO

# Server Configuration
# Replace with the YSFlight server address
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7915 # Please put where the normal YSFlight server is running
# Port for the proxy server
PROXY_PORT = 9000

# Welcome Message to the playe
# For formatting use {username}
# eg. "Welcome {username} to the server!"
# > Welcome Sakuya to the server!
WELCOME_MESSAGE = "Welcome {username} to the server!"

# Native YSFlight Server
# Please select the YSFlight server version for the
# local ysflight server
# Tested only with 20150425 version

YSF_VERSION = 20150425

# Enable ViaVersion? This allows you clients post-20150425 versions
# to join your YSFlight server, this may however raise some issues
# Currently experimental

VIA_VERSION = True

# G Limit (abs(g) >= limit) and the player gets killed
# If you wish to turn off G Limiter, consider using some
# aribitary value like 100
G_LIM = 4

# Will appear as message + player name
# eg. Detected health hack by <player name>
HEALTH_HACK_MESSAGE = "Detected for health hack"

# Enable planes smoking on low life
# If true, planes on life < SMOKE_LIFE will emit black smoke
# They will also have an engine breakdown, not being able to turn
# on afterburner. Also they won't be able to fire missiles

SMOKE_PLANE = True

# Planes smoking minimum life

SMOKE_LIFE = 5


# Discord chat integration
# ```bash
# pip install -r requirements.txt
# ```
# to install dependencies required to run the discord chat integration
#
# On Modern Linux distros you may need to create a virtual environment to install
# the dependencies

DISCORD_ENABLED = True

# Make sure to enable read message intent for the bot.

DISCORD_TOKEN = "DISCORD_BOT_TOKEN"

# Channel ID for the chat
CHANNEL_ID = 0 # Channel ID, as an integer
