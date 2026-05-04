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
            description="""Resolve the approximate geographic location (city-level) of a device or network from its
public IP address. Returns country, region, city, postal code, and approximate latitude/longitude.
Use this tool when you have a public IPv4 or IPv6 address and need to infer its physical location.
Do NOT use for precise location — IP geolocation is approximate (city-level accuracy at best)
and should not be used as a substitute for GPS or address-based geocoding.
Do NOT use with private/reserved IP addresses (e.g., 192.168.x.x, 10.x.x.x, 127.0.0.1) —
those will not resolve to a meaningful location.
For WiFi-based location, use geo_locate_wifi_access_point instead.

Output: Object with country, region/state, city, postal code, approximate latitude/longitude, and ISP information for the given IP address.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "ip_address": {
                        "type": "string",
                        "description": (
                            "Public IPv4 or IPv6 address to geolocate (e.g., '8.8.8.8' or '2001:4860:4860::8888'). "
                            "Must be a routable public IP address. Private/reserved addresses will not return a location."
                        )
                    }
                },
                "required": ["ip_address"]
            }
        ),
        Tool(
            name="geo_locate_wifi_access_point",
            description="""Resolve the geographic location of a device from nearby WiFi access point signal data.
Returns latitude, longitude, and accuracy radius based on the MAC address, optionally signal
strength of the observed WiFi access point(s). Use this tool when you have WiFi scanning data
(MAC address, signal strength) and need to determine physical location without GPS.
Do NOT use if you have an IP address — use geo_locate_ip_address instead.
Do NOT use if you have a street address — use geocode instead.

Output: Object with latitude, longitude, and accuracy radius (in meters) for the resolved
location of the WiFi access point.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "wifi_data": {
                        "type": "object",
                        "description": "WiFi access point signal data for location resolution.",
                        "properties": {
                            "servingCell": {
                                "type": "object",
                                "description": "The primary WiFi access point being used for geolocation.",
                                "properties": {
                                    "mac": {
                                        "type": "string",
                                        "description": "MAC address of the WiFi access point in colon-separated hex format (e.g., '00:22:75:10:d5:91')."
                                    },
                                    "rssi": {
                                        "type": "string",
                                        "description": "Received Signal Strength Indicator in dBm as a string (e.g., '-90'). Negative values expected."
                                    }
                                },
                                "required": ["mac"]
                            }
                        },
                        "required": ["servingCell"]
                    }
                },
                "required": ["wifi_data"]
            }
        ),
    ]

