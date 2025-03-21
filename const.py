"""Constants for the Crafty integration."""

DOMAIN = "crafty"

# Configuration keys
CONF_BASE_URL = "base_url"
CONF_TOKEN = "token"

# Endpoints
SERVERS_ENDPOINT = "/api/v2/servers"
STATS_ENDPOINT = "/api/v2/servers/{server_id}/stats"
ACTION_ENDPOINT = "https://127.0.0.1:8443/api/v2/servers/{server_id}/action/{action}"

# Update interval (in seconds)
UPDATE_INTERVAL = 30
