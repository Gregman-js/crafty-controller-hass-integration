"""Constants for the Crafty integration."""

DOMAIN = "crafty"

# Configuration keys
CONF_BASE_URL = "base_url"
CONF_PANEL_URL = "panel_url"
CONF_TOKEN = "token"

# Endpoint paths
PATH_API_BASE = "/api/v2/"
PATH_SERVERS = "servers"
PATH_STATS = "servers/{}/stats"
PATH_ACTION = "servers/{}/action/{}"

# Crafty Controller Panel
PANEL_SERVER_DETAILS = "/panel/server_detail?id={}"

# Update interval (in seconds)
UPDATE_INTERVAL = 30
OPTIMISTIC_TIMEOUT = 30

# REST FIELDS
API_SERVER_ID = "server_id"
API_SERVER_NAME = "server_name"
API_DATA = "data"
API_STATUS = "status"
API_STATUS_OK = "ok"
