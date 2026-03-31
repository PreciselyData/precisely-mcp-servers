"""
Geolocation Tools Module
Contains 2 tools for IP and WiFi geolocation
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401


def get_tools() -> list[Tool]:
    """Returns list of geolocation tool definitions"""
    return [
        Tool(
            name="geo_locate_ip_address",
            description="Geolocate IP address. Example: {'ip_address': '8.8.8.8'}",
            inputSchema={
                "type": "object",
                "properties": {
                    "ip_address": {"type": "string"}
                },
                "required": ["ip_address"]
            }
        ),
        Tool(
            name="geo_locate_wifi_access_point",
            description="Geolocate WiFi access point. Example: {'wifi_data': {'servingCell': {'mac': '00:22:75:10:d5:91', 'rssi': '-90'}}}",
            inputSchema={
                "type": "object",
                "properties": {
                    "wifi_data": {"type": "object"}
                },
                "required": ["wifi_data"]
            }
        ),
    ]

