"""
Timezone Tools Module
Contains 2 tools for timezone lookups by address and coordinates
"""
from mcp.types import Tool
from mcp_servers.tools.base_tool import handle_tool_call  # noqa: F401


def get_tools() -> list[Tool]:
    """Returns list of timezone tool definitions"""
    return [
        Tool(
            name="timezone_addresses",
            description=(
                "Look up the timezone for one or more addresses, including UTC offset and DST status, "
                "optionally at a specific point in time. "
                "Returns the IANA timezone name (e.g., 'America/New_York'), UTC offset in hours and minutes, "
                "and whether daylight saving time (DST) is in effect at the given timestamp. "
                "Use this tool when you have street addresses and need timezone information. "
                "Do NOT use if you have coordinates instead of addresses — use timezone_locations instead. "
                "Supports multiple addresses in a single call.\n\n"
                "Output: Array of timezone result objects (one per input address), each containing "
                "the IANA timezone ID, UTC offset, DST status, and the input address id for correlation."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "description": "Timezone lookup request payload.",
                        "properties": {
                            "addresses": {
                                "type": "array",
                                "description": "List of addresses to resolve timezone for.",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "timestamp": {
                                            "type": "integer",
                                            "description": (
                                                "Unix timestamp in milliseconds for which to evaluate timezone/DST status "
                                                "(e.g., 1691138974831). If omitted, the current server time is used."
                                            )
                                        },
                                        "address": {
                                            "type": "object",
                                            "description": "Structured address object.",
                                            "properties": {
                                                "id": {
                                                    "type": "string",
                                                    "description": "Client-supplied identifier to correlate this input with its output (e.g., '1')."
                                                },
                                                "addressLines": {
                                                    "type": "array",
                                                    "items": {"type": "string"},
                                                    "description": "Street address lines (e.g., ['1700 District Ave, Burlington, MA']).",
                                                    "minItems": 1
                                                },
                                                "country": {
                                                    "type": "string",
                                                    "description": "ISO 3-letter country code (e.g., 'USA'). Default: 'USA'."
                                                }
                                            },
                                            "required": ["id", "addressLines"]
                                        }
                                    },
                                    "required": ["address"]
                                },
                                "minItems": 1
                            }
                        },
                        "required": ["addresses"]
                    }
                },
                "required": ["data"]
            }
        ),
        Tool(
            name="timezone_locations",
            description=(
                "Look up the timezone for one or more geographic coordinates (longitude, latitude), "
                "including UTC offset and DST status, optionally at a specific point in time. "
                "Returns the IANA timezone name (e.g., 'America/Chicago'), UTC offset in hours and minutes, "
                "and whether daylight saving time (DST) is in effect at the given timestamp. "
                "Use this tool when you have coordinate pairs and need timezone information. "
                "Do NOT use if you have street addresses instead of coordinates — use timezone_addresses instead. "
                "Supports multiple coordinate pairs in a single call.\n\n"
                "Output: Array of timezone result objects (one per input coordinate), each containing "
                "the IANA timezone ID, UTC offset, DST status, and the input id for correlation."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "description": "Timezone lookup request payload.",
                        "properties": {
                            "locations": {
                                "type": "array",
                                "description": "List of coordinate pairs to resolve timezone for.",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "string",
                                            "description": "Client-supplied identifier to correlate this input with its output (e.g., '1')."
                                        },
                                        "timestamp": {
                                            "type": "integer",
                                            "description": (
                                                "Unix timestamp in milliseconds for which to evaluate timezone/DST status "
                                                "(e.g., 1691138974831). If omitted, the current server time is used."
                                            )
                                        },
                                        "geometry": {
                                            "type": "object",
                                            "description": "GeoJSON-style geometry object with coordinates.",
                                            "properties": {
                                                "coordinates": {
                                                    "type": "array",
                                                    "items": {"type": "number"},
                                                    "description": "Coordinates as [longitude, latitude] (e.g., [-71.0589, 42.3601]).",
                                                    "minItems": 2,
                                                    "maxItems": 2
                                                }
                                            },
                                            "required": ["coordinates"]
                                        }
                                    },
                                    "required": ["id", "geometry"]
                                },
                                "minItems": 1
                            }
                        },
                        "required": ["locations"]
                    }
                },
                "required": ["data"]
            }
        ),
    ]

