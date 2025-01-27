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

# G Limit (abs(g) >= limit) and the player gets killed
G_LIM = 4

# Will appear as message + player name
# eg. Detected health hack by <player name>
HEALTH_HACK_MESSAGE = "Detected for health hack"
